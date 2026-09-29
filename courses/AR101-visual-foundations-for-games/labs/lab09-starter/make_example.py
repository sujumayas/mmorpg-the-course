"""Write example_doorway.png: the week 9 scene A (6x4 cells of 40 px) padded to 8x5.
Each cell is the sRGB grey whose L* is nearest the cell's value.

    .venv/bin/python make_example.py
Then:
    .venv/bin/python focal_map.py example_doorway.png --target 1,4,1,4
"""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = [[20, 20, 25, 20, 20, 20, 20, 20],
        [20, 20, 20, 20, 85, 20, 20, 20],
        [30, 25, 20, 20, 30, 20, 20, 20],
        [35, 35, 35, 35, 35, 35, 35, 35],
        [35, 35, 35, 35, 35, 35, 35, 35]]
CELL = 40


def grey_for(v):
    """sRGB grey level (0-255) whose CIE L* is closest to v."""
    def L(g):
        c = g / 255
        y = c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        return 116 * y ** (1 / 3) - 16 if y > 216 / 24389 else 24389 / 27 * y
    return min(range(256), key=lambda g: abs(L(g) - v))

img = Image.new("RGB", (8 * CELL, 5 * CELL))
for r, row in enumerate(ROWS):
    for c, v in enumerate(row):
        g = grey_for(v)
        img.paste((g, g, g), (c * CELL, r * CELL, (c + 1) * CELL, (r + 1) * CELL))
out = os.path.join(HERE, "example_doorway.png")
img.save(out)
print("wrote", out)
