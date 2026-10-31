# Bakes the site: every page in src/ in every language in lang/, as plain
# HTML the host serves as it is. English sits at the root, every other
# language in its `dir` (de/); a new language is a new lang/CODE.toml.
#
#   {{section.key}}     a string of the page's language (inline HTML allowed)
#   {{home}}            the language's start: / or /de/
#   {{canonical}}       this page's address in this language
#   {{alternates}}      <link rel="alternate" hreflang> for every language
#   {{languages}}       the links to this page in every language
#   {{footer}}          src/_footer.html in the same language
#   {{each_language: ...}}  the text once per language, in its words (404)
#
# Pages: src/*.html but those starting with _; 404.html once, at the root.
# A key a language lacks is an error naming it: every language is whole.
#
# Usage: python3 tools/bake.py   (from the repo root)
import re
import sys
import tomllib
from pathlib import Path

SITE = "https://voxca.de/"
DEFAULT = "en"

langs = {}
for f in sorted(Path("lang").glob("*.toml")):
    data = tomllib.loads(f.read_text())
    langs[data["meta"]["code"]] = data
order = [DEFAULT] + [code for code in langs if code != DEFAULT]


def lookup(data, path):
    node = data
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node if isinstance(node, str) else None


def url(code, page):
    return langs[code]["meta"]["dir"] + ("" if page == "index.html" else page)


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


def fill(text, code, page, missing):
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
    }
    if "{{footer}}" in text:
        special["footer"] = fill(Path("src/_footer.html").read_text().strip(), code, page, missing)

    def one(m):
        key = m.group(1)
        if key in special:
            return special[key]
        value = lookup(data, key)
        if value is None:
            missing.add(f"{code}: {key}")
            return m.group(0)
        return value
    return re.sub(r"\{\{\s*([\w.]+)\s*\}\}", one, text)


missing = set()
written = []
for src in sorted(Path("src").glob("*.html")):
    if src.name.startswith("_"):
        continue
    template = src.read_text()
    codes = [DEFAULT] if src.name == "404.html" else order
    for code in codes:
        out = Path(url(code, src.name) or "index.html")
        if out.suffix != ".html":
            out = out / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(fill(template, code, src.name, missing))
        written.append(str(out))

pages = sorted({src.name for src in Path("src").glob("*.html")} - {"404.html"} - {p.name for p in Path("src").glob("_*")})
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for page in pages:
    if page == "imprint.html":
        continue   # noindex
    for code in order:
        sitemap.append(f"  <url><loc>{SITE}{url(code, page)}</loc>")
        for c in order:
            sitemap.append(f'    <xhtml:link rel="alternate" hreflang="{c}" href="{SITE}{url(c, page)}"/>')
        sitemap.append("  </url>")
sitemap.append("</urlset>")
Path("sitemap.xml").write_text("\n".join(sitemap) + "\n")

if missing:
    sys.exit("missing keys:\n  " + "\n  ".join(sorted(missing)))
print("baked", ", ".join(written), "and sitemap.xml")
