"""MMO403 Lab 02 starter: the LTV curve and payback day. Standard library only.

Fill in the TODO functions, then run the tests:

    python3 test_ltv.py        (or: pytest test_ltv.py)

The model is the one from the week 2 lecture, section 2:

    R(d)    = w x qs^d + (1 - w) x qt^d          share of installs active on day d
    LTV(T)  = ARPDAU x (1 - f) x [R(0) + R(1) + ... + R(T-1)]
    payback = first day index D with LTV(D + 1) >= CAC

Day 0 is the install day. f is the platform fee as a fraction (0.30 means 30%).
"""
import csv
import os
from dataclasses import dataclass

HERE = os.path.dirname(os.path.abspath(__file__))


@dataclass
class Game:
    w: float = 0.25        # share of stayers in each install cohort
    qs: float = 0.98       # daily survival of a stayer
    qt: float = 0.40       # daily survival of a tourist
    arpdau: float = 0.20   # gross revenue per daily active user, dollars
    fee: float = 0.30      # platform fee as a fraction of gross


def retention(g, d):
    """TODO step 1. R(d), the share of an install cohort active on day d."""
    raise NotImplementedError("retention() is yours to write")


def ltv(g, T):
    """TODO step 2. Net revenue per install from days 0 .. T-1 (T days in total)."""
    raise NotImplementedError("ltv() is yours to write")


def lifetime_ltv(g):
    """TODO step 3. Net revenue per install over an unlimited horizon (closed form)."""
    raise NotImplementedError("lifetime_ltv() is yours to write")


def payback_day(g, cac, horizon=3650):
    """TODO step 4. The first day index D (0-based) on which cumulative net revenue per
    install reaches cac, i.e. the smallest D with ltv(g, D + 1) >= cac. None if never
    within the horizon."""
    raise NotImplementedError("payback_day() is yours to write")


def load_channels(path=os.path.join(HERE, "channels.csv")):
    """Return a list of dicts, one per acquisition channel, with numeric fields as floats."""
    rows = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            rows.append({k: (v if k == "channel" else float(v)) for k, v in row.items()})
    return rows


def channel_report(rows, horizon=180):
    """TODO step 5. For each channel return (name, lifetime LTV, LTV/CAC, payback day or
    None, LTV at the horizon). Each row gives cac, w, qs, qt and arpdau; fee is 0.30."""
    raise NotImplementedError("channel_report() is yours to write")


if __name__ == "__main__":
    g = Game()
    for d in (0, 1, 7, 30, 90, 180):
        print(f"day {d:3d}: R = {retention(g, d):.4f}  LTV to date = ${ltv(g, d + 1):.3f}")
    print(f"lifetime LTV ${lifetime_ltv(g):.3f}, payback at CAC $1.50: day {payback_day(g, 1.50)}")
