"""AR101 Lab 01 starter: a value checker. Standard library only.

Fill in the four TODO functions, then run the tests:

    python3 test_value_check.py        (or: pytest test_value_check.py)

When the tests pass, run the report on your own palette:

    python3 value_check.py palette.csv pairs.csv --min-gap 20

Value here is CIE L*, from 0 (black) to 100 (white), computed from sRGB
exactly as in the week 1 lecture, section 2.
"""
import csv
import sys

# Weights of linear red, green and blue in relative luminance (sRGB / Rec. 709).
WEIGHTS = (0.2126, 0.7152, 0.0722)


def srgb_to_linear(c):
    """Channel value 0-255 -> linear light 0.0-1.0.

    Divide by 255. If the result is <= 0.04045, divide it by 12.92.
    Otherwise return ((c + 0.055) / 1.055) ** 2.4.
    """
    raise NotImplementedError("srgb_to_linear")


def lightness(rgb):
    """(r, g, b) in 0-255 -> CIE L* in 0-100.

    Y = weighted sum of the three linear channels (use WEIGHTS).
    If Y > 216/24389, L* = 116 * Y ** (1/3) - 16, else L* = (24389/27) * Y.
    """
    raise NotImplementedError("lightness")


def band(v, n):
    """Which of n equal value bands (0 = darkest) holds L* value v.

    Bands split 0-100 evenly. v = 100 belongs to the top band, n - 1.
    """
    raise NotImplementedError("band")


def check_scene(colors, pairs, min_gap=20):
    """Return the failing pairs, worst first.

    colors: {name: (r, g, b)}
    pairs:  [(figure_name, ground_name), ...]
    Result: [(figure_name, ground_name, gap), ...] for every pair whose value
    gap |L*(figure) - L*(ground)| is below min_gap, sorted by gap, smallest first.
    """
    raise NotImplementedError("check_scene")


# ---- provided: file loading and the report ---------------------------------

def load_palette(path):
    with open(path, newline="") as f:
        return {row["name"]: (int(row["r"]), int(row["g"]), int(row["b"]))
                for row in csv.DictReader(f)}


def load_pairs(path):
    with open(path, newline="") as f:
        return [(row["figure"], row["ground"]) for row in csv.DictReader(f)]


def report(colors, pairs, min_gap):
    print(f"{'color':<16}{'rgb':<18}{'L*':>6}  band of 4")
    for name, rgb in colors.items():
        v = lightness(rgb)
        print(f"{name:<16}{str(rgb):<18}{v:6.1f}  {band(v, 4)}")
    fails = check_scene(colors, pairs, min_gap)
    print(f"\n{len(pairs) - len(fails)} of {len(pairs)} pairs separate by at least {min_gap} L*")
    for fig, ground, gap in fails:
        print(f"  FAIL {fig} on {ground}: gap {gap:.1f}")


if __name__ == "__main__":
    args = sys.argv[1:]
    gap = 20
    if "--min-gap" in args:
        i = args.index("--min-gap")
        gap = float(args[i + 1])
        args = args[:i] + args[i + 2:]
    pal = args[0] if args else "palette.csv"
    prs = args[1] if len(args) > 1 else "pairs.csv"
    report(load_palette(pal), load_pairs(prs), gap)
