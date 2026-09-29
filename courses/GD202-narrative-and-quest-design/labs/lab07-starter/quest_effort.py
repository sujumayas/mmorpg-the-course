"""GD202 Lab 07 starter: the drop-rate tax. Standard library only.

Fill in the TODO functions, then run the tests from this folder:

    ../../../../.venv/bin/python test_quest_effort.py

Notation follows the week 7 lecture. A collect quest asks for n items.
Each kill drops one item with probability p (0 < p <= 1), independently.
K is the number of kills a player needs to finish the quest.
"""
import csv
import os
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))


def check_args(n, p):
    """Raise ValueError unless n is a positive integer and 0 < p <= 1."""
    if not isinstance(n, int) or n < 1:
        raise ValueError(f"n must be a positive integer, got {n!r}")
    if not 0 < p <= 1:
        raise ValueError(f"p must be in (0, 1], got {p!r}")


def expected_kills(n, p):
    """TODO step 1. Mean of K: n / p."""
    raise NotImplementedError("expected_kills() is yours to write")


def sd_kills(n, p):
    """TODO step 1. Standard deviation of K: sqrt(n (1 - p)) / p."""
    raise NotImplementedError("sd_kills() is yours to write")


def prob_done_by(k, n, p):
    """TODO step 2. P(K <= k): the chance a player has all n items after k kills.
    This equals the chance of at least n drops in k kills (a binomial tail).
    Return 0.0 when k < n. Use math.comb."""
    raise NotImplementedError("prob_done_by() is yours to write")


def percentile_kills(n, p, q):
    """TODO step 3. Smallest whole k with P(K <= k) >= q, for 0 < q < 1.
    Compare with a tolerance of 1e-12 so rounding cannot push k up by one."""
    raise NotImplementedError("percentile_kills() is yours to write")


def same_mean_designs(mean, ns):
    """TODO step 4. For a target mean number of kills, return a list of
    (n, p) pairs, one for each n in ns, with p = n / mean. Skip any n whose
    p would exceed 1."""
    raise NotImplementedError("same_mean_designs() is yours to write")


def load_quests(path=os.path.join(HERE, "quests.csv")):
    """Read quests.csv into a list of dicts with name, n, p, seconds_per_kill."""
    with open(path, newline="") as f:
        return [
            {"name": r["name"], "n": int(r["n"]), "p": float(r["p"]),
             "seconds_per_kill": float(r["seconds_per_kill"])}
            for r in csv.DictReader(f)
        ]


if __name__ == "__main__":
    for qd in load_quests():
        n, p, s = qd["n"], qd["p"], qd["seconds_per_kill"]
        print(f"{qd['name']:28s} mean {expected_kills(n, p):6.1f} kills  "
              f"P90 {percentile_kills(n, p, 0.9):4d} kills  "
              f"P90 time {percentile_kills(n, p, 0.9) * s / 60:5.1f} min")
