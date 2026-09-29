"""AR101 Lab 04 starter: a value-preserving palette swapper. Standard library only.

Fill in the five TODO functions, then run the tests from the repository root:

    .venv/bin/python courses/AR101-visual-foundations-for-games/labs/lab04-starter/test_color_tools.py

When the tests pass, swap any palette file (one hex color per line, the
Lospec .hex format; lines starting with ";" are comments):

    .venv/bin/python .../color_tools.py slime.hex 120          (keep value)
    .venv/bin/python .../color_tools.py slime.hex 120 naive    (plain hue rotation)

Conventions follow the week 4 lecture: hue in degrees 0-360, saturation and
HSV V in percent 0-100, lightness as CIE L* 0-100 (week 1).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


# ---- provided: week 1's lightness and file helpers -------------------------

def lightness(r, g, b):
    """CIE L* (0-100) of an sRGB color with 0-255 channels, as in week 1."""
    def lin(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    y = 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
    return 116 * y ** (1 / 3) - 16 if y > 216 / 24389 else 24389 / 27 * y


def load_hex_file(path):
    with open(path) as f:
        return [s.strip() for s in f if s.strip() and not s.strip().startswith(";")]


def to_hex(rgb):
    return "{:02x}{:02x}{:02x}".format(*rgb)


# ---- your work --------------------------------------------------------------

def hex_to_rgb(text):
    """'#FF004D' or 'ff004d' -> (255, 0, 77). Ignore surrounding spaces."""
    raise NotImplementedError("hex_to_rgb")


def rgb_to_hsv(r, g, b):
    """0-255 channels -> (hue degrees, saturation %, HSV value %).

    A gray (all channels equal) has hue 0 by convention.
    """
    raise NotImplementedError("rgb_to_hsv")


def hsv_to_rgb(h, s, v):
    """Hue in degrees (any number, wrap it), S and V in percent -> 0-255 ints.

    Use the sector rule from lecture section 2 and round each channel with
    int(x * 255 + 0.5).
    """
    raise NotImplementedError("hsv_to_rgb")


def match_value(target, h, s):
    """Find (s, v) at hue h whose L* is as close as possible to target.

    Step 1: if L* at (h, s, 100) is at least target, keep s and bisect v in
            [0, 100] for the smallest v whose L* >= target.
    Step 2: otherwise set v = 100 and bisect s in [0, s] for the largest s
            whose L* >= target.
    40 bisection steps is plenty. Return (s, v) as floats.
    """
    raise NotImplementedError("match_value")


def swap(hexes, rotation, keep_value=True):
    """Rotate every color's hue by `rotation` degrees; return new hex strings.

    keep_value=False: keep S and V (the naive swap).
    keep_value=True:  use match_value so each color keeps its original L*.
    Grays (S = 0) come back unchanged in both modes.
    """
    raise NotImplementedError("swap")


def nearest_value(target_hex, palette):
    """Return the palette color, other than target_hex itself, whose L* is
    closest to target_hex's. This is how you pick a swap in a fixed palette
    such as PICO-8's, where you cannot solve for V."""
    raise NotImplementedError("nearest_value")


# ---- provided: command line -------------------------------------------------

def main(argv):
    path = argv[1] if len(argv) > 1 else os.path.join(HERE, "slime.hex")
    rotation = float(argv[2]) if len(argv) > 2 else 120
    keep = not (len(argv) > 3 and argv[3] == "naive")
    old = load_hex_file(path)
    new = swap(old, rotation, keep)
    print(f"{'old':8} {'L*':>5}   {'new':8} {'L*':>5}  {'S':>5} {'V':>5}")
    for a, b in zip(old, new):
        ra, rb = hex_to_rgb(a), hex_to_rgb(b)
        _, s, v = rgb_to_hsv(*rb)
        print(f"{a:8} {lightness(*ra):5.1f}   {b:8} {lightness(*rb):5.1f}  {s:5.1f} {v:5.1f}")


if __name__ == "__main__":
    main(sys.argv)
