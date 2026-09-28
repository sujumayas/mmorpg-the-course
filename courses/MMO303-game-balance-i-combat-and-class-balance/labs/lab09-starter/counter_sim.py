"""MMO303 Lab 09 starter: replicator dynamics for counter graphs.
Standard library only. Fill in the TODOs, then run `python3 test_counter_sim.py`
(or pytest).

Class order for the three-class arena is (Knight, Mage, Ranger), as in the
week 9 lecture. A win-rate matrix W has W[i][j] = how often class i beats j,
with 0.5 on the diagonal.
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CLASSES3 = ["Knight", "Mage", "Ranger"]


def triangle_winrates(w_kr, w_mk, w_rm):
    """Win-rate matrix for the three-class arena in the order Knight, Mage, Ranger.
    w_kr: Knight over Ranger, w_mk: Mage over Knight, w_rm: Ranger over Mage."""
    return [
        [0.5, 1 - w_mk, w_kr],
        [w_mk, 0.5, 1 - w_rm],
        [1 - w_kr, w_rm, 0.5],
    ]


def load_winrates(path=os.path.join(HERE, "five-class.csv")):
    """Return (class names, win-rate matrix) from a CSV like five-class.csv."""
    with open(path, newline="") as f:
        rows = list(csv.reader(f))
    names = rows[0][1:]
    return names, [[float(x) for x in r[1:]] for r in rows[1:]]


def margins_from_winrates(W):
    """TODO step 1. Return the margin matrix, margin = 2w - 1."""
    raise NotImplementedError("margins_from_winrates is yours to write")


def expected_margins(shares, M):
    """TODO. E_i = sum over j of M[i][j] x shares[j]."""
    raise NotImplementedError("expected_margins is yours to write")


def win_rates(shares, M):
    """Each class's win rate against the population: 0.5 + E / 2."""
    return [0.5 + e / 2 for e in expected_margins(shares, M)]


def stable_mix3(a, b, c):
    """TODO. Week 9 stable mix for margins a (Knight over Ranger),
    b (Mage over Knight), c (Ranger over Mage). Return (k, m, r)."""
    raise NotImplementedError("stable_mix3 is yours to write")


def step(shares, M, eta=1.0, reroll=0.0):
    """TODO. One week: share x (1 + eta x E), then divide by the sum.
    With reroll > 0, afterwards move that fraction of the population to a
    uniform random mix: share = (1 - reroll) x share + reroll / n."""
    raise NotImplementedError("step is yours to write")


def run(shares, M, weeks, eta=1.0, reroll=0.0):
    """TODO. Return the list of share vectors, starting with `shares`, one per week."""
    raise NotImplementedError("run is yours to write")
