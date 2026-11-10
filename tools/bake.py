# Bakes the site: every page in src/ in every language in lang/, as plain
# HTML the host serves as it is. English sits at the root, every other
# language in its `dir` (de/); a new language is a new lang/CODE.toml.
#
#   {{section.key}}     a string of the page's language (inline HTML allowed;
#                       it may hold {{release.*}} in turn)
#   {{release.key}}     the release on offer (release.toml): version, date
#                       (in the language's words), the files' addresses and
#                       sizes, notes (its post)
#   {{home}}            the language's start: / or /de/
#   {{canonical}}       this page's address in this language
#   {{alternates}}      <link rel="alternate" hreflang> for every language
#   {{languages}}       the links to this page in every language
#   {{header}}          src/_header.html, {{footer}} src/_footer.html
#   {{each_language: ...}}  the text once per language, in its words (404)
#
# Pages: src/*.html but those starting with _; 404.html once, at the root.
# The blog: every posts/SLUG/CODE.md (a head of title, date, summary, then
# Markdown) becomes blog/SLUG.html through src/_post.html; blog/ lists
# them, newest first (src/_blog.html), and blog/feed.xml is their Atom
# feed, each in every language.
# A key a language lacks is an error naming it: every language is whole.
#
# Usage: python3 tools/bake.py   (from the repo root)
import html
import re
import sys
import tomllib
from datetime import date
from pathlib import Path

SITE = "https://voxca.de/"
DEFAULT = "en"

langs = {}
for f in sorted(Path("lang").glob("*.toml")):
    data = tomllib.loads(f.read_text())
    langs[data["meta"]["code"]] = data
order = [DEFAULT] + [code for code in langs if code != DEFAULT]
release = tomllib.loads(Path("release.toml").read_text())


def spoken_date(iso, code):
    words = langs[code]["dates"]
    d = date.fromisoformat(iso)
    return words["format"].format(day=d.day, month=words["months"][d.month - 1], year=d.year)


def size(mb, code):
    return f"{mb:.1f}".replace(".", langs[code]["meta"].get("decimal", ".")) + " MB"


for code, data in langs.items():
    data["release"] = {
        "version": release["version"],
        "date": spoken_date(release["date"], code),
        "iso": release["date"],
        "notes": "/" + data["meta"]["dir"] + "blog/" + release["post"] + ".html",
        **{f"{system}_{key}": (size(value, code) if key == "mb" else value)
           for system in ("windows", "linux") for key, value in release[system].items()},
    }


def lookup(data, path):
    node = data
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node if isinstance(node, str) else None


def url(code, page):
    if page.endswith("index.html"):
        page = page[:-len("index.html")]
    return langs[code]["meta"]["dir"] + page


def blocks(text, name):
    """The spans of {{name: ...}}, balanced over the {{ }} inside them."""
    start = text.find("{{" + name + ":")
    while start >= 0:
        depth, i = 0, start
        while i < len(text):
            if text.startswith("{{", i):
                depth += 1
                i += 2
            elif text.startswith("}}", i):
                depth -= 1
                i += 2
                if depth == 0:
                    break
            else:
                i += 1
        yield start, i, text[start + len(name) + 3:i - 2]
        start = text.find("{{" + name + ":", i)


def fill(text, code, page, missing, extra=None):
    data = langs[code]
    for start, end, inner in reversed(list(blocks(text, "each_language"))):
        text = text[:start] + "\n    ".join(fill(inner.strip(), c, page, missing) for c in order) + text[end:]
    special = {
        "home": "/" + data["meta"]["dir"],
        "canonical": SITE + url(code, page),
        "alternates": "\n".join(
            [f'<link rel="alternate" hreflang="{c}" href="{SITE}{url(c, page)}">' for c in order]
            + [f'<link rel="alternate" hreflang="x-default" href="{SITE}{url(DEFAULT, page)}">']),
        "languages": " ".join(
            f'<a href="/{url(c, page)}" hreflang="{c}" lang="{c}"'
            + (' aria-current="true"' if c == code else "")
            + f' title="{langs[c]["meta"]["name"]}">{c.upper()}</a>' for c in order),
        **(extra or {}),
    }
    for part in ("header", "footer"):
        if "{{" + part + "}}" in text:
            special[part] = fill(Path(f"src/_{part}.html").read_text().strip(), code, page, missing)

    def one(m):
        key = m.group(1)
        if key in special:
            return special[key]
        value = lookup(data, key)
        if value is None:
            missing.add(f"{code}: {key}")
            return m.group(0)
        return re.sub(r"\{\{\s*([\w.]+)\s*\}\}", one, value)
    return re.sub(r"\{\{\s*([\w.]+)\s*\}\}", one, text)


# --- the blog ----------------------------------------------------------------

def inline(text):
    """Markdown's inline marks: `code`, **strong**, *em*, [text](url); a
    bare & becomes &amp;, HTML passes."""
    parts = re.split(r"(`[^`]+`)", text)
    out = []
    for part in parts:
        if part.startswith("`") and part.endswith("`") and len(part) > 1:
            out.append("<code>" + html.escape(part[1:-1], quote=False) + "</code>")
            continue
        part = re.sub(r"&(?!#?\w+;)", "&amp;", part)
        part = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", part)
        part = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", part)
        part = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', part)
        out.append(part)
    return "".join(out)


def markdown(text):
    """The Markdown a post needs: ## and ### headings, paragraphs, lists
    (- and 1.), ``` code blocks."""
    out, lines, i = [], text.strip("\n").split("\n"), 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
        elif line.startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            out.append("<pre><code>" + html.escape("\n".join(lines[i + 1:j]), quote=False) + "</code></pre>")
            i = j + 1
        elif m := re.match(r"(#{2,3}) (.*)", line):
            n = len(m.group(1))
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
            i += 1
        elif re.match(r"(- |\d+\. )", line):
            ordered = not line.startswith("- ")
            items = []
            while i < len(lines) and lines[i].strip():
                if re.match(r"(- |\d+\. )", lines[i]):
                    items.append(re.sub(r"^(- |\d+\. )", "", lines[i]))
                else:
                    items[-1] += " " + lines[i].strip()
                i += 1
            tag = "ol" if ordered else "ul"
            out.append(f'<{tag} class="points">' + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(r"(#{2,3} |- |\d+\. |```)", lines[i]):
                para.append(lines[i].strip())
                i += 1
            out.append("<p>" + inline(" ".join(para)) + "</p>")
    return "\n".join(out)


def read_post(path):
    head, body = path.read_text().split("\n---\n", 1)
    meta = dict(line.split(": ", 1) for line in head.strip().removeprefix("---").strip().split("\n"))
    return {"title": meta["title"], "iso": meta["date"], "summary": meta["summary"], "body": markdown(body)}


posts = {}   # slug -> code -> post
for slug in sorted(d.name for d in Path("posts").iterdir() if d.is_dir()):
    posts[slug] = {}
    for code in order:
        f = Path("posts") / slug / f"{code}.md"
        if not f.exists():
            sys.exit(f"posts/{slug} lacks {code}.md: every language is whole")
        posts[slug][code] = read_post(f)
slugs = sorted(posts, key=lambda s: (posts[s][DEFAULT]["iso"], s), reverse=True)


def post_words(code, slug):
    p = posts[slug][code]
    return {"post.title": inline(p["title"]), "post.date": spoken_date(p["iso"], code), "post.iso": p["iso"],
            "post.summary": inline(p["summary"]), "post.body": p["body"]}


def blog_list(code):
    items = []
    for slug in slugs:
        p = posts[slug][code]
        href = "/" + url(code, f"blog/{slug}.html")
        items.append(f'<article class="post-item">\n'
                     f'  <p class="post-date"><time datetime="{p["iso"]}">{spoken_date(p["iso"], code)}</time></p>\n'
                     f'  <h2><a href="{href}">{inline(p["title"])}</a></h2>\n'
                     f'  <p>{inline(p["summary"])}</p>\n</article>')
    return "\n".join(items)


def plain(text):
    return html.escape(html.unescape(re.sub("<[^>]+>", "", inline(text))), quote=False)


def feed(code):
    data = langs[code]
    base = SITE + url(code, "blog/index.html")
    entries = []
    for slug in slugs:
        p = posts[slug][code]
        link = SITE + url(code, f"blog/{slug}.html")
        entries.append(f"""  <entry>
    <title>{plain(p["title"])}</title>
    <link href="{link}"/>
    <id>{link}</id>
    <updated>{p["iso"]}T12:00:00Z</updated>
    <summary>{plain(p["summary"])}</summary>
    <content type="html">{html.escape(p["body"].replace('href="/', 'href="' + SITE))}</content>
  </entry>""")
    updated = posts[slugs[0]][code]["iso"] if slugs else release["date"]
    return f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="{code}">
  <title>{html.escape(data["blog"]["feed_title"], quote=False)}</title>
  <link href="{base}"/>
  <link rel="self" href="{base}feed.xml"/>
  <id>{base}</id>
  <updated>{updated}T12:00:00Z</updated>
  <author><name>SACRVM</name></author>
{chr(10).join(entries)}
</feed>
"""


# --- writing it all --------------------------------------------------------

missing = set()
written = []


def write(page, code, text):
    out = Path(langs[code]["meta"]["dir"] + page)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    written.append(str(out))


for src in sorted(Path("src").glob("*.html")):
    if src.name.startswith("_"):
        continue
    template = src.read_text()
    for code in ([DEFAULT] if src.name == "404.html" else order):
        write(src.name, code, fill(template, code, src.name, missing))

blog_template = Path("src/_blog.html").read_text()
post_template = Path("src/_post.html").read_text()
for code in order:
    write("blog/index.html", code, fill(blog_template, code, "blog/index.html", missing, {"blog.list": blog_list(code)}))
    write("blog/feed.xml", code, feed(code))
    for slug in slugs:
        page = f"blog/{slug}.html"
        write(page, code, fill(post_template, code, page, missing, post_words(code, slug)))

# The sitemap: every page but the 404 and the imprint (noindex).
pages = sorted(src.name for src in Path("src").glob("*.html")
               if not src.name.startswith("_") and src.name not in ("404.html", "imprint.html"))
pages += ["blog/index.html"] + [f"blog/{slug}.html" for slug in slugs]
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for page in pages:
    for code in order:
        sitemap.append(f"  <url><loc>{SITE}{url(code, page)}</loc>")
        for c in order:
            sitemap.append(f'    <xhtml:link rel="alternate" hreflang="{c}" href="{SITE}{url(c, page)}"/>')
        sitemap.append("  </url>")
sitemap.append("</urlset>")
Path("sitemap.xml").write_text("\n".join(sitemap) + "\n")

if missing:
    sys.exit("missing keys:\n  " + "\n  ".join(sorted(missing)))
print("baked", len(written), "files and sitemap.xml")
