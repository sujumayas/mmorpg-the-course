"""MMO306 Lab 08 starter: rotations and caps.

Fill in every function marked TODO. Standard library only.
Run the checks with:   python test_lab08.py
Run the report with:   python repeatables.py
"""
import csv
import math
import random


# ---------- Part A: rotations ----------

def expected_repeats(S, a):
    """Expected number of today's a items that were also on yesterday's board (random draw)."""
    raise NotImplementedError("TODO: expected_repeats")


def exposure(S, a, d, mode="random"):
    """Expected share of the pool seen after d periods.
    mode "random": 1 - (1 - a/S)^d.  mode "cycle": min(1, d * a / S)."""
    raise NotImplementedError("TODO: exposure")


def periods_to(S, a, x):
    """Periods for random-draw exposure to reach share x (a real number, not rounded).
    Return 1.0 when a == S."""
    raise NotImplementedError("TODO: periods_to")


def pool_for_target(a, x, d):
    """Smallest whole pool size S such that random-draw exposure after d periods is at most x."""
    raise NotImplementedError("TODO: pool_for_target")


def simulate_exposure(S, a, d, trials, seed, no_repeat_yesterday=False):
    """Average share of the pool seen after d periods over `trials` simulated players.
    Each period draws a items without replacement (random.Random(seed).sample).
    With no_repeat_yesterday, draw from items not on yesterday's board; if fewer
    than a remain, take all of them and fill the rest at random from yesterday's."""
    raise NotImplementedError("TODO: simulate_exposure")


# ---------- Part B: caps ----------

def weeks_to_goal(hours, rate, cap, goal, accumulate=False):
    """hours: list of hours played in weeks 1, 2, ...; rate: currency per hour;
    cap: weekly cap (None for no cap); goal: currency needed.
    Hard cap: each week earns min(rate * h, cap).
    Accumulating cap: total after week w is min(total + rate * h, cap * w).
    Return the first week number (1-based) at which the total reaches goal, or None."""
    raise NotImplementedError("TODO: weeks_to_goal")


def percentile(values, p):
    """Inclusive linear-interpolation percentile (MA102 week 12), p in [0, 1]."""
    raise NotImplementedError("TODO: percentile")


def finish_weeks(table, rate, cap, goal, accumulate=False, horizon=16):
    """Weeks to goal for every player; players who never reach it count as horizon + 1."""
    raise NotImplementedError("TODO: finish_weeks")


def load_hours(path):
    """Return a list of 16-element lists of weekly hours, one per player."""
    with open(path, newline="") as f:
        return [[float(x) for x in list(r.values())[1:]] for r in csv.DictReader(f)]


def report():
    for S, a in [(22, 6), (55, 18), (44, 6)]:
        print(f"S={S:2} a={a:2} repeats={expected_repeats(S, a):.2f} "
              f"X(3)={exposure(S, a, 3):.3f} to90%={periods_to(S, a, 0.9):.1f} "
              f"sim X(3)={simulate_exposure(S, a, 3, 2000, 1):.3f}")
    print("pool for <=75% in 7 days, a=6:", pool_for_target(6, 0.75, 7))
    table = load_hours("hours.csv")
    for label, cap, acc in [("no cap", None, False), ("hard 450", 450, False), ("accum 450", 450, True)]:
        f = finish_weeks(table, 60, cap, 3600, acc)
        print(f"{label:10} p25={percentile(f, .25):.1f} p50={percentile(f, .5):.1f} "
              f"p90={percentile(f, .9):.1f} p10={percentile(f, .1):.1f} "
              f"unfinished={sum(x == 17 for x in f)}")


if __name__ == "__main__":
    report()
