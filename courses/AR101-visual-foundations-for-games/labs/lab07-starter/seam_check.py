"""Measure the seam ratio of a tile image and save a 3x3 repeat for eyeballing.

    .venv/bin/python seam_check.py my_grass.png

Needs Pillow (installed in the course .venv). Each pixel's value is CIE L*
(0-100), as in AR101 week 1. Uses your seam_ratio() from autotile.py.
"""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from autotile import seam_ratio  # noqa: E402


def lightness(R, G, B):
    """CIE L* of an sRGB color, 0-100 (AR101 week 1)."""
    def linear(v):
        c = v / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    Y = 0.2126 * linear(R) + 0.7152 * linear(G) + 0.0722 * linear(B)
    return 116 * Y ** (1 / 3) - 16 if Y > 216 / 24389 else 24389 / 27 * Y


def main(path):
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    if w != h:
        sys.exit(f"tile must be square, got {w}x{h}")
    px = img.load()
    tile = [[lightness(*px[x, y][:3]) for x in range(w)] for y in range(h)]
    ratio = seam_ratio(tile)
    verdict = "PASS" if ratio <= 1.5 else "SEAM VISIBLE"
    print(f"{os.path.basename(path)}: {w}x{h}, seam ratio {ratio:.2f} -> {verdict}")
    sheet = Image.new("RGBA", (w * 3, h * 3))
    for i in range(3):
        for j in range(3):
            sheet.paste(img, (i * w, j * h))
    out = os.path.splitext(path)[0] + "_repeat3x3.png"
    sheet.resize((w * 3 * 4, h * 3 * 4), Image.NEAREST).save(out)
    print("saved", out)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
