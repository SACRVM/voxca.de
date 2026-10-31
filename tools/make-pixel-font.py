# Builds assets/fonts/voxcade-pixel.woff2: the pixel font of Voxcade's menus
# and HUDs (5 wide, 7 tall, two rows below the line) as a web font, so the
# site's headings are the games' own letters.
#
# The glyphs are read from the engine's source (src/ui.rs: FONT, and the
# accents of `accented` for the capitals), never copied by hand. Every pixel
# is a square of 100 units; a glyph advances 6 pixels (5 and a gap), as the
# engine sets text. Set the font at a multiple of 10px and every pixel is a
# whole number of screen pixels.
#
# Usage: python3 tools/make-pixel-font.py [path/to/voxcade/src/ui.rs]
#        (from the repo root; the default is ../voxcade/src/ui.rs)
import re
import sys
from pathlib import Path

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

UPM = 1000
PX = 100
ADVANCE = 6 * PX
ASCENT, DESCENT = 9 * PX, -2 * PX   # accents above the capitals, tails below

source = Path(sys.argv[1] if len(sys.argv) > 1 else "../voxcade/src/ui.rs").read_text()

# FONT: ('A', [".###.", ... nine rows ...]),
table = source[source.index("const FONT: &[(char, [&str; 9])] = &["):]
table = table[: table.index("\n];")]
glyphs = {}
for ch, rows in re.findall(r"\(\s*'((?:\\.|[^'\\])+)'\s*,\s*\[([^\]]*)\]\s*\)", table):
    ch = {"\\'": "'", "\\\\": "\\"}.get(ch, ch)
    glyphs[ch] = re.findall(r'"([.#]{5})"', rows)
    assert len(glyphs[ch]) == 9, ch

# accented: 'Ä' => ('A', DIAERESIS), the accent two rows over the letter.
accents = {name: [a, b] for name, a, b in
           re.findall(r'const (\w+): \[&str; 2\] = \["([.#]{5})", "([.#]{5})"\];', source)}
for ch, base, accent in re.findall(r"'(.)' => \('(.)', (\w+)\)", source[source.index("fn accented"):]):
    glyphs[ch] = accents[accent] + glyphs[base]   # eleven rows: two above the top
# Signs the engine draws as another's (`glyph`).
for alias, of in {"–": "-", "—": "-", "−": "-", "’": "'", "‘": "'", "“": '"', "”": '"', "×": "x"}.items():
    glyphs.setdefault(alias, glyphs[of])


def draw(rows):
    """Rows from the top; nine start at the cap line (row 0 at 600-700),
    eleven two rows higher. Each run of pixels in a row is one rectangle."""
    pen = TTGlyphPen(None)
    top = 7 * PX + (len(rows) - 9) * PX
    for r, row in enumerate(rows):
        y1 = top - r * PX
        y0 = y1 - PX
        c = 0
        while c < 5:
            if row[c] == "#":
                start = c
                while c < 5 and row[c] == "#":
                    c += 1
                x0, x1 = start * PX, c * PX
                pen.moveTo((x0, y0)); pen.lineTo((x0, y1)); pen.lineTo((x1, y1)); pen.lineTo((x1, y0)); pen.closePath()
            else:
                c += 1
    return pen.glyph()


names = {".notdef": None, "space": None}
cmap = {32: "space", 160: "space"}
order = [".notdef", "space"]
outlines = {".notdef": TTGlyphPen(None).glyph(), "space": TTGlyphPen(None).glyph()}
for ch, rows in sorted(glyphs.items(), key=lambda kv: ord(kv[0])):
    name = f"uni{ord(ch):04X}"
    order.append(name)
    cmap[ord(ch)] = name
    outlines[name] = draw(rows)

fb = FontBuilder(UPM, isTTF=True)
fb.setupGlyphOrder(order)
fb.setupCharacterMap(cmap)
fb.setupGlyf(outlines)
fb.setupHorizontalMetrics({name: (ADVANCE, 0) for name in order})
fb.setupHorizontalHeader(ascent=ASCENT, descent=DESCENT, lineGap=0)
fb.setupNameTable({"familyName": "Voxcade Pixel", "styleName": "Regular",
                   "copyright": "The pixel font of Voxcade's menus, by SACRVM"})
fb.setupOS2(sTypoAscender=ASCENT, sTypoDescender=DESCENT, sTypoLineGap=0,
            usWinAscent=ASCENT, usWinDescent=-DESCENT, sxHeight=4 * PX, sCapHeight=7 * PX,
            fsType=0, achVendID="SACR")
fb.setupPost(isFixedPitch=1)
fb.font.flavor = "woff2"
out = Path("assets/fonts/voxcade-pixel.woff2")
fb.save(out)
print(f"{out}: {len(glyphs)} glyphs, {out.stat().st_size} bytes")
