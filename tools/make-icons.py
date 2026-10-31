# Builds favicon.svg and favicon.png (the logo's V in the pixel font, a
# voxel deep) and assets/img/og.png (the picture a link shows when shared:
# the logo, the tagline, three games).
#
# Needs assets/fonts/voxcade-pixel.woff2 (tools/make-pixel-font.py) and the
# pictures in assets/img/.
#
# Usage: python3 tools/make-icons.py   (from the repo root)
import io
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

BG, FRONT, SIDE, CREAM = "#050509", "#e8a040", "#7a5420", (236, 227, 203)
V = ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."]

# The favicon: each pixel of the V a square, its side a darker square half
# a pixel down and right, on the title screens' dark.
cells = [(x, y) for y, row in enumerate(V) for x, c in enumerate(row) if c == "#"]
side = "".join(f'<rect x="{x + 2.5}" y="{y + 1.5}" width="1" height="1"/>' for x, y in cells)
front = "".join(f'<rect x="{x + 2}" y="{y + 1}" width="1" height="1"/>' for x, y in cells)
Path("favicon.svg").write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 9 9" shape-rendering="crispEdges">'
    f'<rect width="9" height="9" rx="1" fill="{BG}"/>'
    f'<g fill="{SIDE}">{side}</g><g fill="{FRONT}">{front}</g></svg>\n')

png = Image.new("RGBA", (72, 72), (0, 0, 0, 0))
d = ImageDraw.Draw(png)
d.rounded_rectangle((0, 0, 71, 71), 8, fill=BG)
for colour, shift in ((SIDE, 4), (FRONT, 0)):
    for x, y in cells:
        x0, y0 = (x + 2) * 8 + shift, (y + 1) * 8 + shift
        d.rectangle((x0, y0, x0 + 7, y0 + 7), fill=colour)
png.resize((64, 64), Image.NEAREST).save("favicon.png", optimize=True)

# The picture for links: 1200 by 630.
font = TTFont("assets/fonts/voxcade-pixel.woff2")
font.flavor = None
ttf = io.BytesIO()
font.save(ttf)
ttf.seek(0)
pixel = ImageFont.truetype(ttf, 30)

og = Image.new("RGB", (1200, 630), BG)
logo = Image.open("assets/img/logo-1800.webp").convert("RGBA")
logo = logo.resize((900, round(logo.height * 900 / logo.width)), Image.LANCZOS)
og.paste(logo, ((1200 - logo.width) // 2, 56), logo)
text = "EVERY CLASSIC 2D GENRE, IN VOXELS."
d = ImageDraw.Draw(og)
d.text(((1200 - d.textlength(text, font=pixel)) // 2, 56 + logo.height + 34), text, font=pixel, fill=CREAM)
for i, name in enumerate(["moreblood", "voxkeep", "pulsar"]):
    shot = Image.open(f"assets/img/{name}.webp").convert("RGB").resize((360, 203), Image.LANCZOS)
    og.paste(shot, (30 + i * 390, 380))
og.save("assets/img/og.png", optimize=True)
print("favicon.svg, favicon.png, assets/img/og.png")
