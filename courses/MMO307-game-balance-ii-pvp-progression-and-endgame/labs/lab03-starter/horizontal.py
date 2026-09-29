"""MMO307 Lab 03: horizontal reward track.

Standard-library Python. Fill in every function marked TODO, then run
    python test_horizontal.py
Notation follows the week 3 lecture: frequencies f (a list summing to 1),
bonus b, upgrade margin u, rotation strength lam.
"""
import csv
import math
from itertools import combinations
from pathlib import Path

DATA = Path(__file__).with_name("play_log.csv")
SITUATIONS = ["boss_heavy", "trash_heavy", "armored", "swarm", "vertical_zone", "arena"]


def load_log(path=DATA):
    """Rows of play_log.csv as dicts: player, segment, situation, minutes."""
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def estimate_mix(rows, segment, situations=SITUATIONS):
    """Share of the segment's minutes spent in each situation, in the order
    given by `situations`. The result sums to 1."""
    raise NotImplementedError("estimate_mix")


def zipf(n):
    """Frequencies proportional to 1/i for i = 1..n, normalised to sum 1."""
    raise NotImplementedError("zipf")


def rotate(f, lam):
    """Season-average mix under a rotation of strength lam:
    f'_i = lam / n + (1 - lam) * f_i."""
    raise NotImplementedError("rotate")


def values(f, b):
    """Marginal value of each tool, b * f_i."""
    raise NotImplementedError("values")


def n_eff(f):
    """Effective number of situations, 1 / sum(f_i^2)."""
    raise NotImplementedError("n_eff")


def gap_ceiling(f, b):
    """(1 + b) / (1 + b * max(f))."""
    raise NotImplementedError("gap_ceiling")


def tools_worth_chasing(f, b, u):
    """How many tools have value b * f_i >= u (use a 1e-12 tolerance)."""
    raise NotImplementedError("tools_worth_chasing")


def gate_share(owned, activities):
    """Share of activities (each a set of required counters) that the owned
    counters open."""
    raise NotImplementedError("gate_share")


def gate_marginals(m, r):
    """Activities are all r-subsets of m counters, equally common. Return the
    list of marginal shares gained by owning counters 0, 1, ..., m-1 in order
    (length m)."""
    raise NotImplementedError("gate_marginals")


if __name__ == "__main__":
    rows = load_log()
    for seg in ("raider", "pvp"):
        f = estimate_mix(rows, seg)
        print(seg, [round(x, 3) for x in f], "N_eff", round(n_eff(f), 2))
