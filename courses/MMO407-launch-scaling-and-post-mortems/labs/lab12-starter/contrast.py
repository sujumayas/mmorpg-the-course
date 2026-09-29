"""MMO407 lab 12: which post-mortem lessons survive a comparison?

Standard library only. Run from inside lab12-starter/:
    python contrast.py                   # prints the report (fails until the TODOs are done)
    python -m unittest test_contrast.py
"""
import csv
import math
from pathlib import Path

DATA = Path(__file__).with_name("launches.csv")


def load(path=DATA):
    """Rows as dicts: launch id, outcome ("troubled" or "smooth"), factor columns as ints."""
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in r:
            if k not in ("launch", "outcome"):
                r[k] = int(r[k])
    return rows


def factor_names(rows):
    return [k for k in rows[0] if k not in ("launch", "outcome")]


def counts(rows, factor):
    """Return (a, n_T, b, n_S): troubled with the factor, troubled total,
    smooth with the factor, smooth total."""
    # TODO 1: count rows by outcome and by factor presence
    raise NotImplementedError("TODO 1")


def contrast(a, n_t, b, n_s, half=False):
    """Return (f_T, f_S, L).

    f_T = a / n_T, f_S = b / n_S, L = f_T / f_S.
    With half=True, use (a + 0.5) / (n_T + 1) and (b + 0.5) / (n_S + 1).
    If f_S is 0, L is math.inf.
    """
    # TODO 2
    raise NotImplementedError("TODO 2")


def rank(rows, by):
    """Factor names sorted from highest to lowest `by`, where `by` is "f_T" or "L".
    Break ties by factor name, alphabetically."""
    # TODO 3: build (value, name) pairs with counts() and contrast(), then sort
    raise NotImplementedError("TODO 3")


def biggest_rank_change(rows):
    """The factor whose position differs most between rank(rows, "f_T") and rank(rows, "L")."""
    by_ft, by_l = rank(rows, "f_T"), rank(rows, "L")
    return max(by_ft, key=lambda name: (abs(by_ft.index(name) - by_l.index(name)), name))


if __name__ == "__main__":
    rows = load()
    print(f"{'factor':20} {'a/nT':>6} {'b/nS':>6} {'f_T':>5} {'f_S':>5} {'L':>5}")
    for name in rank(rows, "L"):
        a, nt, b, ns = counts(rows, name)
        ft, fs, lift = contrast(a, nt, b, ns)
        print(f"{name:20} {a:>3}/{nt:<2} {b:>3}/{ns:<2} {ft:5.0%} {fs:5.0%} {lift:5.2f}")
    print("by f_T:", ", ".join(rank(rows, "f_T")))
    print("by L:  ", ", ".join(rank(rows, "L")))
    print("biggest change:", biggest_rank_change(rows))
