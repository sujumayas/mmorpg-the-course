"""MMO405 lab 12: the review lottery.

Python 3, standard library only. Fill in the five TODOs, then run
    python -m unittest test_committee.py
from inside this folder (from the repository root, .venv/bin/python is the course Python).
Running this file prints the report once the TODOs are done.

Model (lecture week 12, section 2): each paper has quality Q ~ N(0, 1). A
committee's score is S = sqrt(rho) * Q + sqrt(1 - rho) * E with independent
noise E ~ N(0, 1), so two committees' scores correlate at rho. Each committee
accepts its top share a of papers.
"""
import random
from math import sqrt
from statistics import NormalDist

N = NormalDist()


def spearman_brown(rho1, k):
    """TODO 1. Reliability of the mean of k reviewers with single-reviewer reliability rho1."""
    raise NotImplementedError("TODO 1")


def reviewers_needed(rho1, target):
    """TODO 2. Smallest whole number k with spearman_brown(rho1, k) >= target."""
    raise NotImplementedError("TODO 2")


def both_accept(a, rho, steps=2000):
    """TODO 3. P(both committees accept) for acceptance share a and correlation rho.

    Integrate phi(x) * (1 - Phi((z - rho x) / sqrt(1 - rho^2))) for x from z to 8
    with Simpson's rule (steps must be even), where z = N.inv_cdf(1 - a).
    For rho >= 1 return a exactly.
    """
    raise NotImplementedError("TODO 3")


def simulate(n_papers, a, rho, seed):
    """TODO 4. Simulate two committees and return the table as a dict with keys
    "AA", "AR", "RA", "RR" (first letter committee 1, second committee 2).

    Use rng = random.Random(seed) and rng.gauss(0, 1) for Q, E1 and E2, drawn in
    that order for each paper. Each committee accepts its top round(a * n_papers)
    papers by score.
    """
    raise NotImplementedError("TODO 4")


def summarize(table):
    """TODO 5. Return (precision, inconsistency) from a table.

    precision = AA / (average of committee 1's and committee 2's accept counts)
    inconsistency = (AR + RA) / total
    """
    raise NotImplementedError("TODO 5")


def report():
    rho = spearman_brown(0.29, 3)
    print(f"rho for 3 reviewers at rho1 = 0.29: {rho:.3f}")
    for a in (0.26, 0.10):
        b = both_accept(a, 0.55)
        print(f"formula, rho 0.55, a {a:.2f}: precision {b / a:.3f}, inconsistency {2 * (a - b):.3f}")
    t = simulate(166, 43.5 / 166, 0.55, seed=2014)
    print("one simulated NeurIPS-sized experiment:", t, "-> precision %.3f, inconsistency %.3f" % summarize(t))
    t = simulate(20000, 0.26, 0.55, seed=1)
    print("20,000 papers:", "precision %.3f, inconsistency %.3f" % summarize(t))
    print("reviewers for rho 0.9 at rho1 0.29:", reviewers_needed(0.29, 0.9))


if __name__ == "__main__":
    report()
