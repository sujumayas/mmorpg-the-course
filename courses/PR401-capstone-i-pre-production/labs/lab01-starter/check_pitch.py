#!/usr/bin/env python3
"""PR401 lab 01: will the content last until the patch? Standard library only.

Usage: python check_pitch.py pitch.csv claims.csv

Model (PR401 week 1, section 2; PR201 week 1; MMO306 week 1):
  plannable per person = (1 - buffer) * (hours_per_week - c * (team_size - 1)) * weeks
  C  = content_share * team_plannable / authoring_ratio      one-pass content hours
  T  = 7 * C * replay / h                                     days until exhaustion
  L  = live_days / T                                          locust ratio
  r_needed = h * live_days / (7 * C)
PASS when the median player's L <= 1 (or median_L_accepted is set with a reason)
and the claims sheet is valid.
"""
import csv
import sys

LEVELS = {"assumed", "estimated", "tested"}
REQUIRED = ["team_size", "hours_per_week", "weeks", "c", "buffer", "content_share",
            "authoring_ratio", "replay", "live_days", "h_light", "h_median", "h_keen", "h_heavy"]


def read_pitch(path):
    with open(path, newline="") as f:
        rows = {r["key"].strip(): r["value"].strip() for r in csv.DictReader(f)}
    missing = [k for k in REQUIRED if not rows.get(k)]
    return rows, missing


def check_claims(path):
    problems = []
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    if not 8 <= len(rows) <= 15:
        problems.append(f"claims.csv has {len(rows)} claims (need 8 to 15)")
    risky = 0
    for r in rows:
        cid = r.get("id", "?")
        if r.get("evidence", "").strip() not in LEVELS:
            problems.append(f"{cid}: evidence must be one of {sorted(LEVELS)}")
        if r.get("load_bearing", "").strip() not in {"yes", "no"}:
            problems.append(f"{cid}: load_bearing must be yes or no")
        if not r.get("owner", "").strip():
            problems.append(f"{cid}: no owner")
        if r.get("load_bearing", "").strip() == "yes" and r.get("evidence", "").strip() == "assumed":
            risky += 1
    if risky == 0:
        problems.append("no load-bearing claim is tagged 'assumed'; week 1 pitches always have one")
    return problems


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    p, missing = read_pitch(sys.argv[1])
    if missing:
        print("NOT READY: missing values for", ", ".join(missing))
        sys.exit(1)
    f = {k: float(p[k]) for k in REQUIRED}
    n = f["team_size"]
    per = (1 - f["buffer"]) * (f["hours_per_week"] - f["c"] * (n - 1)) * f["weeks"]
    team = per * n
    C = f["content_share"] * team / f["authoring_ratio"]
    print(f"plannable per person {per:.1f} h, team {team:.1f} h, one-pass content C = {C:.2f} h")
    print(f"{'player':<8}{'h':>5}{'T days':>9}{'L':>7}{'r_needed':>10}")
    med_L = None
    for name in ("light", "median", "keen", "heavy"):
        h = f["h_" + name]
        T = 7 * C * f["replay"] / h
        L = f["live_days"] / T
        print(f"{name:<8}{h:>5.0f}{T:>9.1f}{L:>7.2f}{h * f['live_days'] / (7 * C):>10.2f}")
        if name == "median":
            med_L = L
    problems = check_claims(sys.argv[2])
    accepted = p.get("median_L_accepted", "")
    if med_L > 1 + 1e-9 and not accepted:
        problems.insert(0, f"FAIL: median L = {med_L:.2f}")
    for pr in problems:
        print("  -", pr)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
