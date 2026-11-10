# voxca.de

The website of Voxcade, a voxel arcade engine: <https://voxca.de/>.
Plain static HTML, served by GitHub Pages from `main` on the custom
domain (`CNAME`). No cookies, no tracking, nothing loaded from other
servers.

## Languages

English at the root, German in `de/`. The words live in `lang/*.toml`, the
pages in `src/*.html` with `{{section.key}}` where a string goes;
`tools/bake.py` writes every page in every language (and `sitemap.xml`).
The baked pages are committed, since Pages serves the files as they are.

```bash
python3 tools/bake.py
```

A new language: copy `lang/en.toml` to `lang/CODE.toml`, set its `meta`
(`code`, `name`, `dir = "CODE/"`, `locale`) and translate. The bake names
any key it lacks; the language links and `hreflang` follow by themselves.

## A release and the blog

The downloads are the releases of the engine's repository
(SACRVM/voxcade, public; its Builds workflow makes one for every `v*` tag).
A new version, once that release is there:

```bash
gh release download vX.Y.Z --repo SACRVM/voxcade --dir /tmp/vX.Y.Z && sha256sum /tmp/vX.Y.Z/*
```

Then `release.toml` (version, date, the files' addresses, sizes in MB
and `sha256`: `sha256sum` of each file; the program reads this file to
know of a new version and takes a package only with that checksum, so
push it only once the release's files are up) and a post: `posts/X.Y.Z/en.md` and `de.md`, each a head of
`title`, `date` and `summary`, then Markdown (`##` headings, lists,
links, `code`): what is new, what changed, what was mended. Bake, look,
push. The blog lists the posts newest first and writes `blog/feed.xml`
(Atom) in each language.

## Fonts, icons, pictures

- `assets/fonts/voxcade-pixel.woff2`: the pixel font of the engine's menus,
  built from the engine's source (`src/ui.rs`):
  `python3 tools/make-pixel-font.py ../voxcade/src/ui.rs`
- `favicon.svg`, `favicon.png`, `assets/img/og.png`:
  `python3 tools/make-icons.py`
- The logo, screenshots and the film are the engine's own pictures, drawn
  without a window from the games' replays (in the engine's repo):

```bash
voxcade shot games/moreblood --replay games/moreblood/replays/20261015-171938-14600.toml --frames 3600 --size 1600x900 --out shots/moreblood.png
voxcade shot games/pulsar --replay games/pulsar/replays/tests/two_ships.toml --frames 600 --size 1600x900 --out shots/pulsar-two.png
voxcade film games/voxkeep games/voxkeep/replays/demo.toml --from 24 --to 30 --size 1280x720 --out shots/voxkeep.mp4
voxcade ide games/voxkeep --shot shots/ide.png --play 600 --size 1600x900
```

  The quick start's pictures are a copy of the jump & run template
  (`templates/platformer`) as "My Game", drawn with an empty config
  folder (`XDG_CONFIG_HOME`) so no paths of this machine show:
  `voxcade ide "My Game" --shot ... --play 420` and `--open main.lua`,
  cut to 1600 by 520.

  The logo is a scratch game whose title says VOXCADE
  (`c.title_screen.logo = { "VOXCADE" }`, `logo_colors = { "#ffb347" }`),
  shot with `--screen title`, cut out from its dark ground. Pictures go in
  as WebP; the film is the five games' clips joined with fades, H.264
  without sound. BunnyFarm speaks English, German and French: the film
  and its picture come in the page's language (`media` in each
  `lang/*.toml`), from a copy of its demo replay with the `language`
  line changed.

## Credits

Sokovox's puzzles are David W. Skinner's Microban, passed on with his
credit as he asks.
