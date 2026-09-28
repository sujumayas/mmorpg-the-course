"""MMO402 Lab 03 starter: count a council election two ways.

Usage:  python lab03-starter.py lab03-ballots.csv [seats]

Ballot file: CSV with header `count,ranking`. Each row is a group of identical
ballots; `ranking` lists candidates in preference order separated by `>`.

Rules implemented:
  stv()          Single transferable vote, Droop quota floor(V/(S+1)) + 1,
                 surplus transferred fractionally (every ballot of an elected
                 candidate moves on at weight surplus / tally), lowest candidate
                 eliminated when nobody reaches quota. Ties broken alphabetically.
  block_vote()   Plurality-at-large: each ballot gives one full vote to each of
                 its first S names. The S highest totals win.
Pure standard library. Python 3.8+.
"""
import csv
import sys
from collections import defaultdict


def load(path):
    ballots = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            ranking = [c.strip() for c in row["ranking"].split(">") if c.strip()]
            ballots.append([float(row["count"]), ranking])
    return ballots


def droop(total, seats):
    return int(total // (seats + 1)) + 1


def stv(ballots, seats, verbose=True):
    candidates = sorted({c for _, r in ballots for c in r})
    total = sum(n for n, _ in ballots)
    quota = droop(total, seats)
    # each entry: [weight, ranking, pointer]
    piles = [[n, r, 0] for n, r in ballots]
    hopeful = set(candidates)
    elected = []
    rnd = 0
    if verbose:
        print(f"STV: {total:.0f} ballots, {seats} seats, Droop quota {quota}")
    while len(elected) < seats and hopeful:
        rnd += 1
        if len(elected) + len(hopeful) <= seats:
            for c in sorted(hopeful):
                elected.append(c)
                if verbose:
                    print(f"  round {rnd}: {c} elected (remaining seats filled)")
            break
        tally = defaultdict(float)
        for b in piles:
            while b[2] < len(b[1]) and b[1][b[2]] not in hopeful:
                b[2] += 1
            if b[2] < len(b[1]):
                tally[b[1][b[2]]] += b[0]
        for c in hopeful:
            tally.setdefault(c, 0.0)
        top = max(sorted(hopeful), key=lambda c: tally[c])
        if tally[top] >= quota:
            surplus = tally[top] - quota
            factor = surplus / tally[top] if tally[top] else 0
            for b in piles:
                if b[2] < len(b[1]) and b[1][b[2]] == top:
                    b[0] *= factor
            hopeful.discard(top)
            elected.append(top)
            if verbose:
                print(f"  round {rnd}: {top} elected with {tally[top]:.0f}, surplus {surplus:.0f}")
        else:
            low = min(sorted(hopeful), key=lambda c: tally[c])
            hopeful.discard(low)
            if verbose:
                print(f"  round {rnd}: {low} eliminated with {tally[low]:.0f}")
    return elected


def block_vote(ballots, seats, verbose=True):
    tally = defaultdict(float)
    for n, r in ballots:
        for c in r[:seats]:
            tally[c] += n
    ranked = sorted(tally, key=lambda c: (-tally[c], c))
    if verbose:
        print("Block vote totals:", ", ".join(f"{c} {tally[c]:.0f}" for c in ranked))
    return ranked[:seats]


def scale_group(ballots, prefix, factor):
    """Return a copy of the ballots with every group whose first choice starts
    with `prefix` multiplied by `factor`. Use it to model turnout changes."""
    return [[n * factor if r and r[0].startswith(prefix) else n, list(r)] for n, r in ballots]


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "lab03-ballots.csv"
    seats = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    b = load(path)
    print("STV winners:  ", stv(b, seats))
    print("Block winners:", block_vote(b, seats))
    # TODO step 4: model lower casual turnout, e.g. scale_group(b, "H", 0.5)
