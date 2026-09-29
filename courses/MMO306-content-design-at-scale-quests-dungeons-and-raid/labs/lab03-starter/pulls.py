"""MMO306 Lab 03 starter: pull size and trash routes. Standard library only.

Fill in the TODO functions, then run the tests from this folder:

    ../../../../.venv/bin/python test_pulls.py

Notation follows the week 3 lecture.
    N     enemies in one pull          H    health of each enemy
    A     group AoE damage per second to each target hit
    cap   target cap m (None = no cap)
    d     damage per second one enemy deals to the tank after mitigation
    Q     healer's sustained healing per second on the tank
    B     tank's buffer (health it can lose before dying)
    walk  seconds of walking and waiting before each pull
"""
import csv
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = dict(H=1000, A=50, cap=20, d=30, Q=150, B=3200, walk=10)


def load_packs(path=os.path.join(HERE, "packs.csv")):
    """List of dicts with keys pack, enemies (int), forces (float), walk_s (float)."""
    with open(path, newline="") as f:
        return [dict(pack=r["pack"], enemies=int(r["enemies"]), forces=float(r["forces"]),
                     walk_s=float(r["walk_s"])) for r in csv.DictReader(f)]


def kill_time(N, H, A, cap):
    """TODO step 1. H / A if cap is None or N <= cap, else H x N / (A x cap)."""
    raise NotImplementedError("kill_time() is yours to write")


def survive_time(N, d, Q, B):
    """TODO step 1. B / (N x d - Q), or math.inf when N x d <= Q."""
    raise NotImplementedError("survive_time() is yours to write")


def pull_works(N, H, A, cap, d, Q, B):
    """TODO step 1. True when the pack dies no later than the tank: kill <= survive."""
    raise NotImplementedError("pull_works() is yours to write")


def clear_minutes(M, N, H, A, cap, d, Q, B, walk):
    """TODO step 2. (M / N) x (kill_time + walk) / 60, or None if the pull fails."""
    raise NotImplementedError("clear_minutes() is yours to write")


def best_pull(M, max_n=20, scale=1.0, **params):
    """TODO step 3. Try N = 1 .. max_n with every value in BASE, overridden by params,
    and with H and d both multiplied by scale. Return (N, minutes) for the fastest
    pull that works; on a tie, the smaller N. Return None if no pull works."""
    raise NotImplementedError("best_pull() is yours to write")


def route(packs, required, H, A, cap, d, Q, B):
    """TODO step 4. Choose the set of packs whose forces add up to at least `required`
    in the least total time, where each pack costs walk_s + kill_time(enemies).
    A pack that cannot be pulled safely (pull_works is False) may not be chosen.
    Search every subset (there are at most 15 packs). Return (seconds, sorted names).
    On a tie in seconds, prefer fewer packs, then the alphabetically first name list.
    Return None if no subset reaches `required`."""
    raise NotImplementedError("route() is yours to write")


if __name__ == "__main__":
    for cap in (5, 20):
        row = [clear_minutes(120, N, **{**BASE, "cap": cap}) for N in (1, 3, 5, 6, 8, 10, 12)]
        print(f"cap {cap}:", ["wipe" if m is None else round(m, 1) for m in row])
    for level in (0, 5, 10):
        print(f"+{level} levels:", best_pull(120, scale=1.08 ** level))
    p = {k: v for k, v in BASE.items() if k != "walk"}
    print("route to 30%:", route(load_packs(), 30, **p))
