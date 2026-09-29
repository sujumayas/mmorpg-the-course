"""MMO307 Lab 02: power creep audit.

Standard-library Python. Fill in every function marked TODO, then run
    python test_creep.py
Notation follows the week 2 lecture: D rungs, spacing s, upgrade margin u,
overlap rule o, T tiers per expansion, g power per item level, band F.
"""
import csv
import math
from pathlib import Path

DATA = Path(__file__).with_name("itemlevels.csv")


def load_series(path, series):
    """Return the 'top' column (as ints) for one series in itemlevels.csv,
    in file order. Series names: wow_native, wow_bfa_scale, wow_sl_scale,
    wow_mn_scale, ffxiv."""
    with open(path, newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["series"] == series]
    return [int(r["top"]) for r in rows]


def increments(tops):
    """Differences between consecutive tops."""
    raise NotImplementedError("increments")


def ratios(tops):
    """Ratios between consecutive tops (later / earlier)."""
    raise NotImplementedError("ratios")


def fit_additive(tops):
    """Least-squares line top = a + b * index (index 0, 1, 2, ...).
    Return (b, sse) where sse is the sum of squared errors in item levels."""
    raise NotImplementedError("fit_additive")


def fit_multiplicative(tops):
    """Least-squares line on log(top) = a + b * index.
    Return (growth_ratio, sse) where growth_ratio = exp(b) and sse is the sum
    of squared errors of exp(a + b * index) against top, in item levels."""
    raise NotImplementedError("fit_multiplicative")


def creep_per_tier(o, s, u):
    """The ratchet: c = o * s + u."""
    raise NotImplementedError("creep_per_tier")


def creep_per_expansion(T, o, s, u):
    """C = T * c."""
    raise NotImplementedError("creep_per_expansion")


def shelf_life(c, g, F):
    """t* = ln F / (c * ln(1 + g)); return math.inf when c == 0."""
    raise NotImplementedError("shelf_life")


def max_creep(g, F, t_target):
    """Largest c with shelf_life(c, g, F) >= t_target."""
    raise NotImplementedError("max_creep")


def largest_overlap(D, s, u, g, F, t_target):
    """Largest rung index o in 0..D-1 whose shelf life is at least t_target,
    or None if even o = 0 fails."""
    raise NotImplementedError("largest_overlap")


if __name__ == "__main__":
    for name in ("wow_native", "ffxiv"):
        tops = load_series(DATA, name)
        print(name, tops)
        print("  increments", increments(tops))
        print("  additive fit", fit_additive(tops))
        print("  multiplicative fit", fit_multiplicative(tops))
