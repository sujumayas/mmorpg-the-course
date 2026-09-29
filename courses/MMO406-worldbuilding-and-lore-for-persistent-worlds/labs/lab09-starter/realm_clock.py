"""Lab 09: the realm clock.

Fill in every function marked TODO. Run the tests with
    ../../../../.venv/bin/python test_realm_clock.py
from this folder (or with pytest). All tests fail until you implement the functions.

Symbols follow the week 9 lecture:
    n     active players on a realm
    q     daily participation share, u units per participant per day
    d     daily fatigue factor (1.0 means no fatigue)
    goal  units the realm must deliver (fixed G, or g * n for a scaled goal)
Days are whole days; contributions for day t arrive at the end of day t.
"""
import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def daily_rate(n, q, u):
    """R = n * q * u."""
    raise NotImplementedError("TODO")


def finish_day(goal, rate, d=1.0):
    """First whole day on which cumulative contributions reach the goal, or None if never.

    No fatigue: ceil(goal / rate). With fatigue: x = 1 - goal * (1 - d) / rate;
    None if x <= 0, else ceil(ln x / ln d). Subtract a tolerance of 1e-9 before ceil
    so that an exact whole number of days is not rounded up.
    """
    raise NotImplementedError("TODO")


def ceiling_per_player(q, u, d):
    """Most a realm can ever deliver per active player under fatigue: q * u / (1 - d)."""
    raise NotImplementedError("TODO")


def largest_g(q, u, d, d_max):
    """Largest scaled goal per active player that is reached by day d_max.

    No fatigue: q * u * d_max. With fatigue: q * u * (1 - d ** d_max) / (1 - d).
    """
    raise NotImplementedError("TODO")


def simulate(n, q0, u, goal, d=1.0, days=120, target_day=None, behind=0.8, penalty=0.9):
    """Day-by-day simulation with an optional discouragement loop.

    Start with q = q0 and total = 0. For t = 1..days:
      1. total += n * q * u
      2. if total >= goal (tolerance 1e-9), return t
      3. q *= d
      4. if target_day is not None and total < behind * goal * t / target_day,
         the realm feels behind schedule: q *= penalty
    Return None if the goal is not reached within `days`.
    """
    raise NotImplementedError("TODO")


def load_realms(path=HERE / "realms.csv"):
    """Return a list of (realm, active players) tuples, with the count as an int."""
    raise NotImplementedError("TODO")


def plan(realms, q, u, d, rule, value, d_min, d_max):
    """For each realm return {name: (finish day or None, status)}.

    rule is "fixed" (goal = value) or "scaled" (goal = value * n).
    status is "never", "early" (day < d_min), "late" (day > d_max) or "ok".
    """
    raise NotImplementedError("TODO")


if __name__ == "__main__":
    realms = load_realms()
    for label, d, rule, value in (("fixed, no fatigue", 1.0, "fixed", 300_000),
                                  ("fixed, fatigue", 0.97, "fixed", 300_000),
                                  ("scaled 45, fatigue", 0.97, "scaled", 45)):
        print(label, plan(realms, 0.2, 10, d, rule, value, 14, 42))
