#!/usr/bin/env python3
"""PR402 lab 04: triage by gates and impact per fix hour.

Usage: python check_triage.py bugs.csv --sessions 450 --capacity 31.5

Model (PR402 week 4, sections 3 and 4):
  weight   S1 = 10, S2 = 4, S3 = 1, S4 = 0.2
  impact   I = sessions * reach * weight
  priority p = I / hours
  gate     'data loss' or 'exploit' in the gate column, or S1 with reach >= 0.01
Rules: every gate bug is fixed; fixed hours (fix and workaround) <= capacity; a deferred or
       won't-fix bug that outranks a fixed non-gate bug needs a note; reach in 0..1,
       severity 1..4, decision one of fix, workaround, defer, wontfix.
"""
import argparse
import csv
import sys

WEIGHT = {1: 10, 2: 4, 3: 1, 4: 0.2}
DECISIONS = {"fix", "workaround", "defer", "wontfix"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bugs")
    ap.add_argument("--sessions", type=float, required=True)
    ap.add_argument("--capacity", type=float, required=True)
    a = ap.parse_args()
    with open(a.bugs, newline="") as f:
        bugs = list(csv.DictReader(f))
    problems = []
    for b in bugs:
        sev, reach, hours = int(b["severity"]), float(b["reach"]), float(b["hours"])
        if sev not in WEIGHT or not 0 <= reach <= 1 or hours <= 0:
            problems.append(f"{b['id']}: severity 1-4, reach 0-1 and hours > 0 required")
            sev = min(max(sev, 1), 4)
        b["I"] = a.sessions * reach * WEIGHT[sev]
        b["p"] = b["I"] / hours if hours > 0 else 0.0
        g = b["gate"].strip().lower()
        b["is_gate"] = g in ("data loss", "exploit") or (sev == 1 and reach >= 0.01)
        if b["decision"] not in DECISIONS:
            problems.append(f"{b['id']}: decision must be one of {sorted(DECISIONS)}")

    print(f"{'id':<4} {'sev':>3} {'reach':>6} {'h':>5} {'impact':>7} {'per h':>6}  gate  decision")
    for b in sorted(bugs, key=lambda b: (not b["is_gate"], -b["p"])):
        print(f"{b['id']:<4}  S{b['severity']} {float(b['reach']):6.1%} {float(b['hours']):5g} "
              f"{b['I']:7.1f} {b['p']:6.2f}  {'yes ' if b['is_gate'] else '    '}  {b['decision']}")

    used = sum(float(b["hours"]) for b in bugs if b["decision"] in ("fix", "workaround"))
    open_impact = sum(b["I"] for b in bugs if b["decision"] not in ("fix", "workaround"))
    print(f"hours planned {used:g} of {a.capacity:g}; total impact {sum(b['I'] for b in bugs):.1f}; "
          f"open impact {open_impact:.1f}")
    if used > a.capacity + 1e-9:
        problems.append(f"planned {used:g} h exceeds capacity {a.capacity:g} h")
    for b in bugs:
        if b["is_gate"] and b["decision"] != "fix":
            problems.append(f"{b['id']}: gate bug must be fixed, not '{b['decision']}'")
    fixed = [b for b in bugs if not b["is_gate"] and b["decision"] in ("fix", "workaround")]
    for b in bugs:
        if b["is_gate"] or b["decision"] in ("fix", "workaround") or b["note"].strip():
            continue
        beaten = [f["id"] for f in fixed if b["p"] > f["p"]]
        if beaten:
            problems.append(f"{b['id']} ({b['p']:.2f}/h) is deferred but outranks fixed {', '.join(beaten)}; "
                            "reorder or add a note")

    for p in problems:
        print("FAIL:", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
