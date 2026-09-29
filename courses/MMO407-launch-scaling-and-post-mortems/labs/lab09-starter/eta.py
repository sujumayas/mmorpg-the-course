"""MMO407 lab 09: ETA forecaster and extension policies.

Durations are whole minutes. Standard library only. Run the tests from
inside lab09-starter/ with:
    python -m unittest test_eta.py
"""
import csv
import math

LECTURE_LOG = [15, 20, 25, 30, 30, 35, 40, 45, 50, 60,
               60, 75, 90, 105, 120, 150, 180, 240, 360, 600]


def load(path="outages.csv", kind=None):
    """Durations from the CSV, optionally only one kind (deploy, database, network)."""
    with open(path, newline="") as f:
        return [int(r["minutes"]) for r in csv.DictReader(f)
                if kind is None or r["kind"] == kind]


def quantile(log, q):
    """Smallest logged duration with at least a share q of the log at or below it."""
    s = sorted(log)
    return s[max(0, math.ceil(q * len(s)) - 1)]


def cost(T, log, c_late=2, c_early=1):
    """Average cost per player of announcing 'back at minute T'."""
    # TODO 1: c_late * lateness + c_early * earliness, averaged over the log
    raise NotImplementedError("TODO 1")


def best_eta(log, c_late=2, c_early=1):
    """The announcement the critical ratio c_late / (c_late + c_early) picks."""
    # TODO 2: use quantile()
    raise NotImplementedError("TODO 2")


def mean_left(log, t):
    """Average minutes still to go for logged outages longer than t (None if none)."""
    # TODO 3
    raise NotImplementedError("TODO 3")


def fixed_extensions(D, log, step=30):
    """Policy A. Announce the median of the log; after each miss add `step`.
    Returns the list of announced times, first to last."""
    # TODO 4: loop while D > the latest announcement
    raise NotImplementedError("TODO 4")


def reforecast(D, log, c_late=2, c_early=1):
    """Policy B. Announce best_eta(log); after a miss at T, announce the
    critical-ratio quantile of the logged outages longer than T.
    If no logged outage is longer than T, announce T + (T - previous T),
    or 2 * T after the first announcement. Returns the list of announcements."""
    # TODO 5
    raise NotImplementedError("TODO 5")


def misses(announcements):
    """Broken promises: every announcement but the last."""
    return len(announcements) - 1


if __name__ == "__main__":
    print("best ETA (2:1):", best_eta(LECTURE_LOG))
    for t in (0, 60, 120, 240):
        print(f"down {t:3d} min: {mean_left(LECTURE_LOG, t):.1f} min to go")
