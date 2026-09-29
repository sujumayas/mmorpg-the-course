#!/usr/bin/env python3
"""PR401 lab 04: which prototype first? Standard library only.

Usage: python check_risks.py risks.csv [--budget 45.5] [--skip]

Model (PR401 week 4, section 2):
  E = p * L      V = q * E      ratio = V / c
Risks with ratio >= 1 are taken in descending ratio order into prototype 1 while the
cumulative cost fits the budget. By default the picker stops at the first risk that does not
fit (the guide's spare hours rule); --skip lets it try the next one instead. Prototype 2 is
filled the same way with a fresh budget. The chosen column in risks.csv (P1, P2 or none) must
match the picker, or carry a written deviation in the note column.
PASS when every row is complete and valid and every chosen value matches or is justified.
"""
import argparse
import csv
import sys


def pick(rows, budget, skip):
    queue = sorted([r for r in rows if r["ratio"] >= 1], key=lambda r: -r["ratio"])
    out = {}
    for proto in ("P1", "P2"):
        used, rest = 0.0, []
        stopped = False
        for r in queue:
            if not stopped and used + r["c"] <= budget + 1e-9:
                out[r["id"]] = proto
                used += r["c"]
            else:
                rest.append(r)
                if not skip:
                    stopped = True
        queue = rest
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("risks")
    ap.add_argument("--budget", type=float, default=45.5)
    ap.add_argument("--skip", action="store_true")
    a = ap.parse_args()
    problems, rows = [], []
    with open(a.risks, newline="") as f:
        for r in csv.DictReader(f):
            try:
                p, L, c, q = (float(r[k]) for k in ("p", "L", "c", "q"))
            except (KeyError, ValueError):
                problems.append(f"{r.get('id', '?')}: p, L, c and q must be numbers")
                continue
            if not (0 <= p <= 1 and 0 <= q <= 1 and c > 0):
                problems.append(f"{r['id']}: p and q must be in [0, 1] and c > 0")
            if not r.get("estimated_by", "").strip() or r.get("estimated_by") == r.get("owner"):
                problems.append(f"{r['id']}: estimated_by must be filled and differ from owner")
            E = p * L
            rows.append(dict(r, p=p, L=L, c=c, q=q, E=E, V=q * E, ratio=q * E / c))
    chosen = pick(rows, a.budget, a.skip)
    print(f"{'id':<5}{'E':>7}{'V':>7}{'c':>6}{'ratio':>7}  picker  team")
    for r in rows:
        want = chosen.get(r["id"], "none")
        team = r.get("chosen", "").strip() or "?"
        print(f"{r['id']:<5}{r['E']:>7.1f}{r['V']:>7.1f}{r['c']:>6.0f}{r['ratio']:>7.2f}  {want:<6}  {team}")
        if team != want and not r.get("note", "").strip():
            problems.append(f"{r['id']}: chosen '{team}' differs from picker '{want}' with no note")
    total = sum(r["E"] for r in rows)
    after1 = total - sum(r["V"] for r in rows if chosen.get(r["id"]) == "P1")
    after2 = after1 - sum(r["V"] for r in rows if chosen.get(r["id"]) == "P2")
    for proto in ("P1", "P2"):
        used = sum(r["c"] for r in rows if chosen.get(r["id"]) == proto)
        print(f"{proto}: {used:g} of {a.budget:g} h")
    print(f"exposure burn-down: now {total:.1f} h, after P1 {after1:.1f} h, after P2 {after2:.1f} h")
    for p in problems:
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
