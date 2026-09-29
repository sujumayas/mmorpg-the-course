#!/usr/bin/env python3
"""PR201 lab 10: alpha gate check and gate-bug forecast. Standard library only.

Usage: python check_alpha.py bugs.csv forecast.csv [criteria.csv] [--cut FEATURE] [--f0-after-cut N] [--days 8]

Model (PR101 week 10, as used in PR201 week 10):
  priority  P = clamp(S + F - 1, 1, 4), F = 0 always, 1 often, 2 rare
  gate bugs = open bugs with P1 or P2 (status not fixed, verified, closed or cut)
  found[t]  = round_half_up(f0 * d ** (t - 1))
  reg[t]    = round_half_up(r * fixed[t - 1])
  fixed[t]  = min(c, B[t-1] + found[t] + reg[t])
  B[t]      = B[t-1] + found[t] + reg[t] - fixed[t]
--cut FEATURE drops the open bugs tagged with that feature (a cut behind a flag) before the forecast.
Checks: team priorities match the matrix; every gate bug has an owner; every criterion has an owner
and evidence; A4 is 'fail' while any gate bug is open. Prints PASS or NOT READY; exits 1 on failure.
"""
import argparse
import csv
import math
import sys

BAND = {"always": 0, "often": 1, "rare": 2}
CLOSED = {"fixed", "verified", "closed", "cut"}


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def rhu(x):
    return math.floor(x + 0.5)


def forecast(b0, f0, d, c, r, days):
    rows, b, prev = [], b0, 0
    for t in range(1, days + 1):
        found = rhu(f0 * d ** (t - 1))
        reg = rhu(r * prev)
        fixed = min(c, b + found + reg)
        b = b + found + reg - fixed
        prev = fixed
        rows.append((t, found, reg, fixed, b))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bugs")
    ap.add_argument("forecast")
    ap.add_argument("criteria", nargs="?")
    ap.add_argument("--cut")
    ap.add_argument("--f0-after-cut", type=float)
    ap.add_argument("--days", type=int, default=8)
    a = ap.parse_args()
    kv = {r["key"]: float(r["value"]) for r in read(a.forecast)}
    problems = []

    gate = []
    print(f"{'id':<6}{'S':>2} {'freq':<7}{'P':>3} {'team':>5}  status")
    for b in read(a.bugs):
        s, f = int(b["severity"]), BAND[b["frequency"].strip()]
        p = max(1, min(4, s + f - 1))
        team = b["priority"].strip()
        st = b["status"].strip().lower()
        if a.cut and b.get("feature", "").strip() == a.cut and st not in CLOSED:
            st = "cut"
        print(f"{b['id']:<6}{s:>2} {b['frequency']:<7}{'P' + str(p):>3} {('P' + team) if team else '?':>5}  {st}")
        if not team:
            problems.append(f"{b['id']}: priority blank")
        elif int(team) != p:
            problems.append(f"{b['id']}: team priority P{team}, matrix gives P{p}")
        if p <= 2 and st not in CLOSED:
            gate.append(b)
            if not b["owner"].strip():
                problems.append(f"{b['id']}: gate bug with no owner")

    b0 = len(gate)
    f0 = a.f0_after_cut if (a.cut and a.f0_after_cut is not None) else kv["f0"]
    day = int(kv["review_day"])
    rows = forecast(b0, f0, kv["d"], int(kv["c"]), kv["r"], max(a.days, day))
    print(f"\ngate bugs open: {b0}" + (f" (after cutting '{a.cut}')" if a.cut else ""))
    print(f"forecast with f0={f0:g}, d={kv['d']:g}, c={int(kv['c'])}, r={kv['r']:g}")
    print(" day found reg fixed open")
    print(f"{0:>4}{'':>6}{'':>4}{'':>6}{b0:>5}")
    for t, found, reg, fixed, b in rows:
        print(f"{t:>4}{found:>6}{reg:>4}{fixed:>6}{b:>5}")
    at_review = rows[day - 1][4]
    zero = next((t for t, *_, b in rows if b == 0), None)
    print(f"open on review day {day}: {at_review}; zero on day {zero if zero else 'after ' + str(len(rows))}")
    print("forecast verdict: gate " + ("passes" if at_review == 0 else "fails") + " on the review day")

    if a.criteria:
        for c in read(a.criteria):
            if not c["owner"].strip():
                problems.append(f"{c['id']}: no owner")
            if not c["evidence"].strip():
                problems.append(f"{c['id']}: no evidence")
            status = c["status"].strip().lower()
            if status not in ("pass", "fail"):
                problems.append(f"{c['id']}: status must be pass or fail")
            if c["id"] == "A4" and status == "pass" and b0 > 0:
                problems.append(f"A4 marked pass with {b0} gate bugs open")

    if problems:
        print()
        for p in problems:
            print("  -", p)
        print("NOT READY")
        sys.exit(1)
    print("PASS")


if __name__ == "__main__":
    main()
