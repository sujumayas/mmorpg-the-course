"""MMO305 Lab 03 starter: a seeded matchmaker Monte Carlo.

Standard library only. Usage:
    python3 matchmaker.py                 # baseline table for N = 60, 200, 1000
    python3 matchmaker.py 500 30          # one pool size N and run count r

Model (week 3, section 3): each run, the whole pool of N players is shuffled
and cut into groups of m + 1. Every player meets m others per run. After r runs,
a partner met at least k times counts as an acquaintance.

Your tasks are marked TODO.
"""
import math
import random
import sys
from collections import Counter


def simulate(N, r, m=4, k=3, s=0.0, seed=305):
    """Return (mean distinct people met, mean acquaintances) per player.

    s is the requeue share: the chance that a whole group from the previous run
    queues again together and is kept intact. s = 0 is pure random matching.
    """
    size = m + 1
    if N % size:
        raise ValueError(f"N must be a multiple of the group size {size}")
    rng = random.Random(seed)
    meetings = [Counter() for _ in range(N)]
    groups = None
    for _ in range(r):
        if groups is None or s == 0:
            kept, free = [], list(range(N))
        else:
            # TODO (step 4): keep each previous group with probability s,
            # and put everyone else into `free`.
            raise NotImplementedError("requeue rule not written yet")
        rng.shuffle(free)
        groups = kept + [free[i:i + size] for i in range(0, len(free), size)]
        for g in groups:
            for a in g:
                for b in g:
                    if a != b:
                        meetings[a][b] += 1
    distinct = sum(len(c) for c in meetings) / N
    acquaint = sum(sum(1 for v in c.values() if v >= k) for c in meetings) / N
    return distinct, acquaint


def formula(N, r, m=4, k=3):
    """TODO (step 2): return (D, A) from the binomial formulas in week 3."""
    raise NotImplementedError


if __name__ == "__main__":
    if len(sys.argv) == 3:
        cases = [(int(sys.argv[1]), int(sys.argv[2]))]
    else:
        cases = [(60, 20), (200, 20), (1000, 20)]
    print("N      r    distinct  acquaintances   (seed 305, m = 4, k = 3)")
    for N, r in cases:
        d, a = simulate(N, r)
        print(f"{N:<6} {r:<4} {d:8.2f}  {a:8.2f}")
