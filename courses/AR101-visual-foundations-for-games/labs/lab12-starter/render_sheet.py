"""AR101 Lab 12: render a four-up sheet of a raid arena through all four viewers.

    python render_sheet.py raid_palette.csv            # writes raid_palette_fourup.png

Needs Pillow (in the course .venv) and a working `simulate` in cvd_check.py.
The palette CSV must name `floor`, `danger` and `safe`. Two optional names:
`rim` draws a dark ring around the danger zone, and `safe_ring` draws the safe
zone as a dashed ring with inward chevrons in that color instead of a filled circle.
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

from cvd_check import MODES, load_palette, simulate

SIZE = 320


def draw_arena(colors, mode):
    c = {k: simulate(v, mode) for k, v in colors.items()}
    img = Image.new("RGB", (SIZE, SIZE), c["floor"])
    d = ImageDraw.Draw(img)
    # boss marker: a dark hexagon at top center
    cx, cy, r = SIZE // 2, 48, 26
    d.polygon([(cx + r * math.cos(math.radians(60 * i + 30)), cy + r * math.sin(math.radians(60 * i + 30)))
               for i in range(6)], fill=simulate((30, 30, 36), mode))
    # danger zone
    dx, dy, dr = 110, 200, 88
    if "rim" in c:
        d.ellipse([dx - dr - 6, dy - dr - 6, dx + dr + 6, dy + dr + 6], fill=c["rim"])
    d.ellipse([dx - dr, dy - dr, dx + dr, dy + dr], fill=c["danger"])
    # safe zone
    sx, sy, sr = 250, 230, 56
    if "safe_ring" in c:
        for a in range(0, 360, 20):
            d.arc([sx - sr, sy - sr, sx + sr, sy + sr], a, a + 11, fill=c["safe_ring"], width=5)
        for a in range(0, 360, 90):
            t = math.radians(a)
            tip = (sx + 28 * math.cos(t), sy + 28 * math.sin(t))
            l = (sx + 44 * math.cos(t + 0.35), sy + 44 * math.sin(t + 0.35))
            rr = (sx + 44 * math.cos(t - 0.35), sy + 44 * math.sin(t - 0.35))
            d.line([l, tip, rr], fill=c["safe_ring"], width=4)
    else:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=c["safe"])
    d.text((8, SIZE - 18), mode, fill=(255, 255, 255))
    return img


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "raid_palette.csv"
    colors = load_palette(path)
    sheet = Image.new("RGB", (2 * SIZE + 12, 2 * SIZE + 12), (20, 20, 20))
    for i, mode in enumerate(MODES):
        sheet.paste(draw_arena(colors, mode), (4 + (i % 2) * (SIZE + 4), 4 + (i // 2) * (SIZE + 4)))
    out = Path(path).with_name(Path(path).stem + "_fourup.png")
    sheet.save(out)
    print(f"wrote {out}")
