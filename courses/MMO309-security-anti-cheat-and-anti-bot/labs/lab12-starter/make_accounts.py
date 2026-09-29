"""Account generator for MMO309 Lab 12. Do not edit.

make_accounts(n, seed) returns a list of dicts:
  {"cheat": bool, "aim": bool, "reports": bool, "hash": bool}
The three signals are the week 12 lecture's: an aim-snap detector, three or more player
reports, and a known-cheat file hash. Their rates are close to the lecture's, but player
reports are more likely when the aim-snap detector fired (for honest players too), so the
two signals are NOT independent. Finding that is part of the lab.
"""
import random


def make_accounts(n=200_000, seed=12):
    rng = random.Random(seed)
    rows = []
    for _ in range(n):
        cheat = rng.random() < 0.01
        if cheat:
            aim = rng.random() < 0.90
            reports = rng.random() < (0.52 if aim else 0.32)
            hsh = rng.random() < 0.60
        else:
            aim = rng.random() < 0.010
            reports = rng.random() < (0.30 if aim else 0.0475)
            hsh = rng.random() < 0.001
        rows.append({"cheat": cheat, "aim": aim, "reports": reports, "hash": hsh})
    return rows
