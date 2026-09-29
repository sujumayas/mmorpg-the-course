"""Lab 07: lore memory in a churning population.

Fill in every function marked TODO. Run the tests with
    ../../../../.venv/bin/python test_lore_memory.py
from this folder (or with pytest). All tests fail until you implement the functions.

Symbols follow the week 7 lecture:
    a  live reach, share of month-0 players who experienced the beat
    c  monthly churn, s = 1 - c
    r  catch-up reach, chance a later newcomer meets the beat
    m  months since release
"""
import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def knowledge(a, c, r, m):
    """Share of month-m players who experienced the beat: a*s^m + r*(1 - s^m)."""
    raise NotImplementedError("TODO")


def half_life(c):
    """Months until half the release cohort has left: ln 2 / -ln(1 - c)."""
    raise NotImplementedError("TODO")


def needed_r(target, a, c, months):
    """Catch-up reach needed so that knowledge(a, c, r, months) == target.

    Return the raw value, even if it is below 0 (target met by live reach alone)
    or above 1 (target unreachable).
    """
    raise NotImplementedError("TODO")


def steady_mix(c_short, c_long, w_short):
    """Share of short-stay players in a steady population.

    Newcomers are short-stay with probability w_short and long-stay otherwise.
    In a steady state each group's size is (its arrivals) / (its churn), so the
    short-stay share is (w_short / c_short) / (w_short / c_short + (1 - w_short) / c_long).
    """
    raise NotImplementedError("TODO")


def two_group(a, r, c_short, c_long, w_short, months):
    """Knowledge share for months 0..months with two kinds of player.

    Rules (apply them in this order every month):
    1. At month 0 the population has the steady_mix of short-stay and long-stay
       players, and a share a of EACH group experienced the beat.
    2. Each month, every group loses its churn share (knowers and non-knowers alike).
    3. All leavers are replaced by the same number of newcomers. A share w_short of
       newcomers are short-stay, the rest long-stay. A share r of newcomers know the beat.
    Return a list of months + 1 floats; element 0 is a.
    """
    raise NotImplementedError("TODO")


def load_beats(path=HERE / "beats.csv"):
    """Return a list of (beat, a, r) tuples from the CSV, with a and r as floats."""
    raise NotImplementedError("TODO")


def audit(beats, c, months=(12, 24)):
    """Return {beat: (K at months[0], K at months[1], ...)} using knowledge()."""
    raise NotImplementedError("TODO")


if __name__ == "__main__":
    for name, ks in audit(load_beats(), 0.08).items():
        print(f"{name:32s}" + "  ".join(f"{100 * k:5.1f}%" for k in ks))
