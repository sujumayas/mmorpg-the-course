"""MMO407 lab 06: exploit discovery and reopening. Standard-library Python 3.10+.

Model from the week 6 lecture (Goel-Okumoto discovery curve).

  m(t) = a * (1 - exp(-b t))        found by week t
  R(t) = a * exp(-b t)              still hidden
  E(t) = R(t) * (1 - exp(-b))       expected finds in the coming week
  P(t) = 1 - exp(-E(t))             chance of at least one
  Each release (t0, n) adds n * exp(-b (t - t0)) to R(t) for t >= t0.

Fill in every function marked TODO, then run:  python -m unittest test_discovery.py
"""
import csv
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent


def fit_two_points(m1, m2, t1):
    """TODO 1. Fit a and b from m1 found by week t1 and m2 found by week 2*t1.
    Return (a, b). Raise ValueError unless 0 < m2/m1 - 1 < 1."""
    raise NotImplementedError("fit_two_points")


def remaining(t, a, b, releases=()):
    """TODO 2. Exploits still hidden at week t. The launch holds a exploits;
    releases is a sequence of (week shipped, exploits added)."""
    raise NotImplementedError("remaining")


def next_week(t, a, b, releases=()):
    """TODO 3. Return (expected finds in the coming week, chance of at least one)."""
    raise NotImplementedError("next_week")


def reopen_week(a, b, risk, releases=(), start=0.0, step=0.01):
    """TODO 4. Smallest t >= start on a grid of `step` weeks with P(t) < risk."""
    raise NotImplementedError("reopen_week")


def fit_least_squares(weeks, counts, b_grid=None):
    """TODO 5. Fit a and b to a whole log of cumulative counts.
    For each b on the grid (default 0.005 to 3.0 in steps of 0.005), the best a
    has a closed form: a = sum(y * f) / sum(f * f) with f = 1 - exp(-b t).
    Return (a, b, sse) for the b with the smallest sum of squared errors."""
    raise NotImplementedError("fit_least_squares")


# ---- helpers (provided) -----------------------------------------------------

def sse(weeks, counts, a, b):
    return sum((y - a * (1 - math.exp(-b * t))) ** 2 for t, y in zip(weeks, counts))


def simulate_log(a, b, weeks, seed):
    """One random find log: each of a exploits is found at an exponential time
    with rate b; return cumulative counts at the given weeks."""
    rng = random.Random(seed)
    times = [rng.expovariate(b) for _ in range(int(a))]
    return [sum(1 for x in times if x <= w) for w in weeks]


def load_log(name="find_log.csv"):
    with open(HERE / name, newline="") as f:
        rows = list(csv.DictReader(f))
    return [int(r["week"]) for r in rows], [int(r["found_cumulative"]) for r in rows]


if __name__ == "__main__":
    a, b = fit_two_points(6, 9, 2)
    print(f"a = {a:.1f}, b = {b:.4f}")
    for t in range(0, 13, 2):
        e, p = next_week(t, a, b)
        print(f"week {t:2}: hidden {remaining(t, a, b):5.2f}  E {e:5.3f}  P {p:5.1%}")
    print(f"reopen at 10%: week {reopen_week(a, b, 0.10):.2f}")
