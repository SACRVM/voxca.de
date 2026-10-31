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

  The logo is a scratch game whose title says VOXCADE
  (`c.title_screen.logo = { "VOXCADE" }`, `logo_colors = { "#ffb347" }`),
  shot with `--screen title`, cut out from its dark ground. Pictures go in
  as WebP; the film is the five games' clips joined with fades, H.264
  without sound.

## Credits

Sokovox's puzzles are David W. Skinner's Microban, passed on with his
credit as he asks.
