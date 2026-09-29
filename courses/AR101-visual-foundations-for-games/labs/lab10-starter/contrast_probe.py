"""AR101 Lab 10: measure a telegraph's value contrast on a plate. Needs Pillow.

    python contrast_probe.py my_plate_n4.png
    python contrast_probe.py my_plate_n4.png --cx 256 --cy 300 --r 110

It samples three rings around the circle and reports the median value (CIE L*)
of each:
    inside   r-12 .. r-5   (your fill)
    edge     r-2  .. r+2   (your rim or outline)
    outside  r+6  .. r+14  (the background next to the telegraph)
Contrast is |part - outside|. The telegraph passes if its best part reaches 20,
the working gap from AR101 week 1.
"""
import math
import statistics
import sys

from PIL import Image

GAP = 20


def lightness(rgb):
    def lin(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb[:3])
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return 116 * y ** (1 / 3) - 16 if y > 216 / 24389 else y * 24389 / 27


def ring_median(img, cx, cy, r0, r1):
    px = img.load()
    vals = []
    for y in range(int(cy - r1) - 1, int(cy + r1) + 2):
        for x in range(int(cx - r1) - 1, int(cx + r1) + 2):
            if 0 <= x < img.width and 0 <= y < img.height and r0 <= math.hypot(x - cx, y - cy) <= r1:
                vals.append(lightness(px[x, y]))
    return statistics.median(vals)


def probe(path, cx=256, cy=300, r=110):
    img = Image.open(path).convert("RGB")
    inside = ring_median(img, cx, cy, r - 12, r - 5)
    edge = ring_median(img, cx, cy, r - 2, r + 2)
    outside = ring_median(img, cx, cy, r + 6, r + 14)
    c_in, c_edge = abs(inside - outside), abs(edge - outside)
    return inside, edge, outside, c_in, c_edge, max(c_in, c_edge)


def arg(name, default):
    return float(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


if __name__ == "__main__":
    files = [a for a in sys.argv[1:] if a.endswith(".png")]
    if not files:
        sys.exit(__doc__)
    cx, cy, r = arg("--cx", 256), arg("--cy", 300), arg("--r", 110)
    print(f"{'file':<22}{'inside':>7}{'edge':>7}{'outside':>8}{'C fill':>8}{'C edge':>8}{'best':>6}  verdict")
    for f in files:
        i, e, o, ci, ce, best = probe(f, cx, cy, r)
        verdict = "readable" if best >= GAP else "LOST"
        print(f"{f:<22}{i:7.1f}{e:7.1f}{o:8.1f}{ci:8.1f}{ce:8.1f}{best:6.1f}  {verdict}")
