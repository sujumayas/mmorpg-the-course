"""AR101 Lab 12 starter: a color-blind audit. Standard library only.

Fill in the three TODO functions, then run the tests:

    python test_cvd_check.py        (or: pytest test_cvd_check.py)

When the tests pass, audit a palette:

    python cvd_check.py raid_palette.csv raid_pairs.csv

and render a four-up sheet of the arena (needs Pillow, in the course .venv):

    python render_sheet.py raid_palette.csv

The model is the week 12 lecture, section 2: simulate each color with the
Machado, Oliveira & Fernandes (2009) severity 1.0 matrix in linear RGB, then
compare pairs by value gap (dV, week 1) and WCAG contrast ratio.
"""
import csv
import sys

MODES = ("normal", "protan", "deutan", "tritan")

CVD = {
    "protan": [[0.152286, 1.052583, -0.204868],
               [0.114503, 0.786281, 0.099216],
               [-0.003882, -0.048116, 1.051998]],
    "deutan": [[0.367322, 0.860646, -0.227968],
               [0.280085, 0.672501, 0.047413],
               [-0.011820, 0.042940, 0.968881]],
    "tritan": [[1.255528, -0.076749, -0.178779],
               [-0.078411, 0.930809, 0.147602],
               [0.004733, 0.691367, 0.303900]],
}


# ---- provided (from week 1) -------------------------------------------------

def to_linear(c):
    """sRGB channel 0-255 -> linear light 0-1."""
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def to_srgb(v):
    """Linear light 0-1 -> sRGB channel 0-255 (rounded, clipped)."""
    v = min(1.0, max(0.0, v))
    c = 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055
    return round(255 * c)


def luminance(rgb):
    """Relative luminance Y (0-1) of an sRGB color."""
    r, g, b = (to_linear(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def lightness(rgb):
    """CIE L* (0-100) of an sRGB color."""
    y = luminance(rgb)
    return 116 * y ** (1 / 3) - 16 if y > 216 / 24389 else y * 24389 / 27


def hex_to_rgb(h):
    h = h.strip().lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ---- your work ---------------------------------------------------------------

def simulate(rgb, mode):
    """Return the sRGB color (r, g, b), ints 0-255, that a viewer in `mode` sees.

    mode is one of MODES. "normal" returns the color unchanged.
    Otherwise: convert each channel to linear light, multiply by CVD[mode]
    (row i of the matrix gives output channel i), clip each result to 0-1,
    and convert back with to_srgb.
    """
    raise NotImplementedError("simulate")


def contrast_ratio(rgb1, rgb2):
    """WCAG contrast ratio (Y_light + 0.05) / (Y_dark + 0.05), from 1 to 21."""
    raise NotImplementedError("contrast_ratio")


def audit(colors, pairs, min_dv=20, min_cr=3.0):
    """Check every pair in every mode.

    colors: {name: (r, g, b)}
    pairs:  [(name_a, name_b), ...]
    Return a list of rows (name_a, name_b, mode, dv, cr, ok) in the order
    pairs x MODES, where dv = |L*(sim a) - L*(sim b)|, cr is the contrast
    ratio of the simulated colors, and ok is True when dv >= min_dv.
    The contrast ratio is reported, but only dv decides ok. Because simulate()
    rounds to whole sRGB values, dv can differ from the lecture's table by 0.1.
    """
    raise NotImplementedError("audit")


# ---- provided: files and the report -----------------------------------------

def load_palette(path):
    with open(path, newline="") as f:
        return {r["name"]: hex_to_rgb(r["hex"]) for r in csv.DictReader(f)}


def load_pairs(path):
    with open(path, newline="") as f:
        return [(r["a"], r["b"]) for r in csv.DictReader(f)]


def report(colors, pairs):
    rows = audit(colors, pairs)
    print(f"{'pair':<28}{'mode':<8}{'dV':>6}{'CR':>7}  dV>=20  CR>=3")
    for a, b, mode, dv, cr, ok in rows:
        print(f"{a + ' / ' + b:<28}{mode:<8}{dv:6.1f}{cr:7.2f}  {'pass' if ok else 'FAIL':<7} "
              f"{'pass' if cr >= 3 else 'FAIL'}")
    fails = sum(1 for r in rows if not r[5])
    print(f"\n{len(rows) - fails} of {len(rows)} pair-mode checks pass dV >= 20")


if __name__ == "__main__":
    pal = sys.argv[1] if len(sys.argv) > 1 else "raid_palette.csv"
    prs = sys.argv[2] if len(sys.argv) > 2 else "raid_pairs.csv"
    report(load_palette(pal), load_pairs(prs))
