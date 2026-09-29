"""AR101 Lab 11 starter: a visual hierarchy audit. Standard library only.

Fill in the four TODO functions, then run the tests:

    python test_hierarchy.py        (or: pytest test_hierarchy.py)

When the tests pass, audit a panel:

    python hierarchy.py loot_labels.csv --ground 525252      (a gray of L* 34.9)

The model is the one in the week 11 lecture, section 2:

    W  = A x dV        A = area in body-text lines (text of the same length: A = s * s)
    dV = |L*(element) - L*(what is behind it)|

A label with a plate adds two parts: the plate against the ground, and the text
against the plate. Levels: 1 is the least important, higher numbers matter more.
"""
import csv
import sys


def lightness(rgb):
    """(r, g, b) 0-255 -> CIE L* 0-100. You wrote this in lab 1; it is provided here."""
    def lin(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return 116 * y ** (1 / 3) - 16 if y > 216 / 24389 else y * 24389 / 27


def hex_to_rgb(h):
    h = h.strip().lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def weight(area, v_fig, v_ground):
    """Visual weight of one part: area times the value gap |v_fig - v_ground|."""
    raise NotImplementedError("weight")


def element_weight(el, v_ground):
    """Total weight of one element.

    el is a dict with keys:
        size        text size relative to body text (s)
        text_v      L* of the text
        plate_v     L* of the plate, or None if the element has no plate
        plate_area  plate area in body-text lines (ignored if plate_v is None)
    Without a plate: s*s x |text_v - v_ground|.
    With a plate:    plate_area x |plate_v - v_ground|  +  s*s x |text_v - plate_v|.
    """
    raise NotImplementedError("element_weight")


def inversions(levels, weights):
    """Count pairs where the less important element is heavier.

    levels and weights are parallel lists. Only compare elements on different
    levels: a pair (i, j) is inverted if levels[i] < levels[j] and
    weights[i] > weights[j].
    """
    raise NotImplementedError("inversions")


def weak_steps(levels, weights, min_ratio=1.5):
    """Check the step between each pair of adjacent levels.

    For each level L that has a level above it (the next larger level number
    present), ratio = (smallest weight on the upper level) / (largest weight on L).
    Return a list of (lower_level, upper_level, ratio) for every ratio below
    min_ratio, in rising level order.
    """
    raise NotImplementedError("weak_steps")


# ---- provided: loading and the report --------------------------------------

def load(path):
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            rows.append({
                "name": r["name"],
                "level": int(r["level"]),
                "size": float(r["size"]),
                "text_v": lightness(hex_to_rgb(r["text"])),
                "plate_v": lightness(hex_to_rgb(r["plate"])) if r["plate"].strip() else None,
                "plate_area": float(r["plate_area"] or 0),
            })
    return rows


def report(rows, v_ground):
    rows = sorted(rows, key=lambda r: r["level"])
    ws = [element_weight(r, v_ground) for r in rows]
    lv = [r["level"] for r in rows]
    print(f"ground L* = {v_ground:.1f}")
    print(f"{'element':<26}{'level':>6}{'text L*':>9}{'plate L*':>10}{'W':>9}")
    for r, w in zip(rows, ws):
        pv = "-" if r["plate_v"] is None else f"{r['plate_v']:.1f}"
        print(f"{r['name']:<26}{r['level']:>6}{r['text_v']:9.1f}{pv:>10}{w:9.1f}")
    pairs = sum(1 for i in range(len(lv)) for j in range(i + 1, len(lv)) if lv[i] != lv[j])
    print(f"\ninversions: {inversions(lv, ws)} of {pairs} cross-level pairs")
    weak = weak_steps(lv, ws)
    print(f"weak steps (< 1.5x): {len(weak)}")
    for lo, hi, ratio in weak:
        print(f"  level {lo} -> {hi}: {ratio:.2f}x")


if __name__ == "__main__":
    args = sys.argv[1:]
    ground = "525252"
    if "--ground" in args:
        i = args.index("--ground")
        ground = args[i + 1]
        args = args[:i] + args[i + 2:]
    report(load(args[0] if args else "loot_labels.csv"), lightness(hex_to_rgb(ground)))
