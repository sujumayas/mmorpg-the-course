#!/usr/bin/env python3
"""PR201 lab 07: check a multiplayer playtest plan and its issue log. Standard library only.

Usage: python check_playtest.py slot.csv issues.csv [--tolerance 0.01]

Model (PR201 week 7, section 4):
  per_round   = min(floor(testers / players_per_match), observers)
  rounds      = floor(window_min / (match_min + turnaround_min))
  n_match     = per_round * rounds                 matches, for per-match problems
  n_first     = per_round * players_per_match      first-time testers, for first-time problems
  reach_p     = 1 - (1 - confidence) ** (1 / n_match)
                the smallest per-match frequency the slot sees with the stated confidence
  frequency   = seen / n_match (kind = match) or seen / n_first (kind = first_time)
  band        = always (>= 0.8) -> 0, often (0.3 to 0.8) -> 1, rare (< 0.3) -> 2
  priority    = clamp(severity + band - 1, 1, 4)   (PR101 week 10)
Prints PASS or NOT READY and exits 1 when a claim or priority disagrees with the model.
"""
import argparse
import csv
import math
import sys


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def band(freq):
    if freq >= 0.8:
        return 0, "always"
    if freq >= 0.3:
        return 1, "often"
    return 2, "rare"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slot")
    ap.add_argument("issues")
    ap.add_argument("--tolerance", type=float, default=0.01)
    a = ap.parse_args()
    kv = {r["key"]: r["value"].strip() for r in read(a.slot)}
    problems = []

    t, k, obs = int(kv["testers"]), int(kv["players_per_match"]), int(kv["observers"])
    per_round = min(t // k, obs)
    rounds = int(float(kv["window_min"]) // (float(kv["match_min"]) + float(kv["turnaround_min"])))
    n_match = per_round * rounds
    n_first = per_round * k
    c = float(kv["confidence"])
    reach = 1 - (1 - c) ** (1 / n_match) if n_match else 1.0
    print(f"matches per round {per_round}, rounds {rounds}, n (per-match) {n_match}, n (first-time) {n_first}")
    print(f"reach: a per-match problem with p >= {reach:.3f} is seen with {c:.0%} confidence")
    for p in (0.05, 0.1, 0.2, 0.3):
        need = math.ceil(math.log(1 - c) / math.log(1 - p))
        print(f"  p = {p:.2f}: P(seen) = {1 - (1 - p) ** n_match:.2f}, matches for {c:.0%} = {need}")

    for key, val, fmt in (("claimed_matches", n_match, "d"), ("claimed_first_time", n_first, "d"), ("claimed_reach_p", reach, ".3f")):
        claim = kv.get(key, "")
        if not claim:
            problems.append(f"{key} is blank; compute it by hand first")
        elif abs(float(claim) - val) > (a.tolerance if isinstance(val, float) else 0):
            problems.append(f"{key} = {claim}, model says {val:{fmt}}")

    print("\nid  kind        seen  n   freq  band    P(model)  P(team)")
    for r in read(a.issues):
        n = n_match if r["kind"].strip() == "match" else n_first
        seen = int(r["seen"])
        if seen > n:
            problems.append(f"{r['id']}: seen {seen} is more than n = {n}")
        freq = seen / n if n else 0.0
        b, name = band(freq)
        pr = max(1, min(4, int(r["severity"]) + b - 1))
        team = r["priority"].strip()
        shown = f"P{pr}" if team else "?"
        print(f"{r['id']:<3} {r['kind']:<11} {seen:>4} {n:>3}  {freq:.2f}  {name:<7} {shown:<9} {('P' + team) if team else '-'}")
        if not team:
            problems.append(f"{r['id']}: priority is blank; set it before comparing")
        elif int(team) != pr:
            problems.append(f"{r['id']}: team priority {team}, model says {pr}")

    if problems:
        print()
        for p in problems:
            print("  -", p)
        print("NOT READY")
        sys.exit(1)
    print("PASS")


if __name__ == "__main__":
    main()
