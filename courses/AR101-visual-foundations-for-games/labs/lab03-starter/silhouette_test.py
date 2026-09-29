"""AR101 Lab 03 starter: the silhouette test as a program. Standard library only.

A sprite is a text file: '#' is a filled pixel, '.' is empty, one line per row.
A mask is a Python set of (x, y) pairs for the filled pixels, with (0, 0) at
the top-left and y growing downward.

Fill in the four TODO functions, then run the tests:

    python3 test_silhouette.py        (or: pytest test_silhouette.py)

When the tests pass, run the report on a folder of sprites:

    python3 silhouette_test.py sprites --threshold 0.80
"""
import os
import sys


def iou(a, b):
    """Intersection over union of two masks: |a & b| / |a | b|.

    Two empty masks count as identical (return 1.0).
    """
    raise NotImplementedError("iou")


def normalize(mask):
    """Shift a mask so the characters stand on the same spot.

    Find the lowest filled row (largest y). Its filled pixels are the feet.
    Let fx = (min x + max x) // 2 over the feet pixels. Shift every pixel by
    (-fx, -lowest_y), so the feet centre sits at (0, 0) and the body has y <= 0.
    Return the new set. An empty mask stays empty.
    """
    raise NotImplementedError("normalize")


def downsample(mask, width, height, f):
    """Shrink a width x height mask by an integer factor f.

    Split the grid into f x f blocks, starting at (0, 0). Block (X, Y) is
    filled in the result if at least half of its f*f pixels are filled.
    Pixels past the last whole block are dropped.
    """
    raise NotImplementedError("downsample")


def worst_pairs(roster, threshold):
    """Pairs that are too alike.

    roster: {name: mask}, masks already normalized.
    Return [(name_a, name_b, iou), ...] for every unordered pair with
    iou >= threshold, name_a < name_b alphabetically, sorted by iou, highest
    first. Break ties alphabetically by (name_a, name_b).
    """
    raise NotImplementedError("worst_pairs")


# ---- provided: loading, drawing and the report -----------------------------

def load_mask(path):
    """Read a sprite file. Returns (mask, width, height)."""
    with open(path) as f:
        rows = [line.rstrip("\n") for line in f if line.strip()]
    mask = {(x, y) for y, row in enumerate(rows) for x, ch in enumerate(row) if ch == "#"}
    return mask, max(len(r) for r in rows), len(rows)


def load_roster(folder):
    roster = {}
    for name in sorted(os.listdir(folder)):
        if name.endswith(".txt"):
            roster[name[:-4]] = load_mask(os.path.join(folder, name))
    return roster


def render(mask):
    if not mask:
        return "(empty)"
    xs = [x for x, _ in mask]
    ys = [y for _, y in mask]
    return "\n".join(
        "".join("#" if (x, y) in mask else "." for x in range(min(xs), max(xs) + 1))
        for y in range(min(ys), max(ys) + 1))


def report(folder, threshold, factors=(1, 2)):
    raw = load_roster(folder)
    for f in factors:
        roster = {}
        for name, (mask, w, h) in raw.items():
            m = mask if f == 1 else downsample(mask, w, h, f)
            roster[name] = normalize(m)
        names = list(roster)
        print(f"\nscale 1/{f}: pixels " + ", ".join(f"{n} {len(roster[n])}" for n in names))
        print(" " * 10 + "".join(f"{n[:8]:>9}" for n in names))
        for a in names:
            cells = "".join(f"{iou(roster[a], roster[b]):9.3f}" for b in names)
            print(f"{a[:9]:<10}{cells}")
        bad = worst_pairs(roster, threshold)
        if bad:
            for a, b, v in bad:
                print(f"  TOO ALIKE at 1/{f}: {a} and {b} (IoU {v:.3f} >= {threshold})")
        else:
            print(f"  every pair below {threshold}")


if __name__ == "__main__":
    args = sys.argv[1:]
    thr = 0.80
    if "--threshold" in args:
        i = args.index("--threshold")
        thr = float(args[i + 1])
        args = args[:i] + args[i + 2:]
    report(args[0] if args else os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprites"), thr)
