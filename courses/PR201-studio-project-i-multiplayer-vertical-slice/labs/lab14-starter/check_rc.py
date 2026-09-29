#!/usr/bin/env python3
"""PR201 lab 14: check the release candidate fix log. Standard library only.

Usage: python check_rc.py rates.csv fixes.csv [--catch 0.7] [--high 0.3]

Model (PR201 week 14, section 2):
  per RC:  P(no regression) = product of (1 - r_i) over its fixes
           E[new defects]   = sum of r_i;  E[escaping] = E[new defects] * (1 - catch)
rates.csv gives r per change type from your tracker (regressions / fixes) with a source.
fixes.csv lists every open bug. Rules checked:
  - decision is fix, remove or known; every P1 is fix or remove
  - every fix and remove names the rc it goes into, an author and a reviewer who is not the author
  - a change with r >= --high is the only such change in its rc
"""
import argparse
import csv
import sys
from collections import defaultdict


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rates")
    ap.add_argument("fixes")
    ap.add_argument("--catch", type=float, default=0.7)
    ap.add_argument("--high", type=float, default=0.3)
    a = ap.parse_args()
    problems = []
    rates = {}
    with open(a.rates, newline="") as f:
        for row in csv.DictReader(f):
            t = row["change_type"].strip()
            try:
                fixes, regs = int(row["fixes"]), int(row["regressions"])
                rates[t] = regs / fixes
            except (ValueError, ZeroDivisionError):
                if row["default_r"].strip():
                    rates[t] = float(row["default_r"])
                    if not row["source"].strip():
                        problems.append(f"rate {t}: a default needs a reason in source")
                else:
                    problems.append(f"rate {t}: give fixes and regressions, or a default_r")
    with open(a.fixes, newline="") as f:
        bugs = list(csv.DictReader(f))
    by_rc = defaultdict(list)
    for b in bugs:
        bid, t, d = b["id"], b["change_type"].strip(), b["decision"].strip()
        if t not in rates:
            problems.append(f"{bid}: change_type '{t}' has no rate in rates.csv")
            continue
        r = rates[t]
        if d not in ("fix", "remove", "known"):
            problems.append(f"{bid}: decision must be fix, remove or known")
            continue
        if b["priority"].strip() == "P1" and d == "known":
            problems.append(f"{bid}: a P1 cannot ship as a known issue")
        if d == "remove":
            r = rates.get("config", r)
        if d in ("fix", "remove"):
            rc = b["rc"].strip()
            if not rc:
                problems.append(f"{bid}: name the rc this change goes into")
            if not b["author"].strip() or not b["reviewer"].strip():
                problems.append(f"{bid}: author and reviewer required")
            elif b["author"].strip() == b["reviewer"].strip():
                problems.append(f"{bid}: reviewer must not be the author")
            by_rc[rc].append((bid, r))
    for rc, items in sorted(by_rc.items()):
        p, e = 1.0, 0.0
        for _, r in items:
            p *= 1 - r
            e += r
        risky = [bid for bid, r in items if r >= a.high]
        print(f"{rc or '(none)'}: {', '.join(b for b, _ in items)}  P(no regression) {p:.1%}  "
              f"expected {e:.2f}  escaping {e * (1 - a.catch):.2f}")
        if len(risky) > 1:
            problems.append(f"{rc}: {len(risky)} high-risk changes ({', '.join(risky)}); one per rc")
    known = [b["id"] for b in bugs if b["decision"].strip() == "known"]
    print(f"known issues: {', '.join(known) or 'none'}")
    for p in problems:
        print("FAIL:", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
