#!/usr/bin/env python3
"""PR401 lab 03: do the hours follow the pillars? Standard library only.

Usage: python check_pillars.py pillars.csv features.csv [--s-min 0.20] [--o-max 0.10]

Model (PR401 week 3, section 2):
  share_p = sum_f hours_f * w_fp / sum_f hours_f
  orphan  = sum_f hours_f * (1 - sum_p w_fp) / sum_f hours_f
PASS when every pillar share >= s_min, orphan <= o_max, every feature's weights sum to 0 or 1,
there are 2 to 4 pillars and at least 2 anti-pillars, and every pillar has a question,
an observable and a threshold. Rows with kind = foundation are listed and excluded.
"""
import argparse
import csv
import sys


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pillars")
    ap.add_argument("features")
    ap.add_argument("--s-min", type=float, default=0.20)
    ap.add_argument("--o-max", type=float, default=0.10)
    a = ap.parse_args()
    problems = []
    prow = read(a.pillars)
    pillars = [r for r in prow if r["kind"].strip() == "pillar"]
    anti = [r for r in prow if r["kind"].strip() == "anti"]
    if not 2 <= len(pillars) <= 4:
        problems.append(f"{len(pillars)} pillars (need 2 to 4)")
    if len(anti) < 2:
        problems.append(f"{len(anti)} anti-pillars (need at least 2)")
    for r in pillars:
        for col in ("question", "observable", "threshold"):
            if not r.get(col, "").strip():
                problems.append(f"{r['id']}: missing {col}")
    ids = [r["id"].strip() for r in pillars]
    feats = read(a.features)
    total, found = 0.0, 0.0
    hours = {p: 0.0 for p in ids}
    orphan = 0.0
    for r in feats:
        h = float(r["hours"])
        if r.get("kind", "").strip() == "foundation":
            found += h
            continue
        total += h
        ws = {p: float(r.get(p) or 0) for p in ids}
        s = sum(ws.values())
        if s > 1e-9 and abs(s - 1) > 1e-6:
            problems.append(f"{r['feature']}: weights sum to {s:g} (must be 0 or 1)")
        for p, w in ws.items():
            hours[p] += h * w
        orphan += h * (1 - s) if s <= 1 else 0
    if total == 0:
        print("NOT READY: no feature hours")
        sys.exit(1)
    print(f"feature hours {total:g} (foundation listed separately: {found:g})")
    for p in ids:
        sh = hours[p] / total
        flag = "" if sh >= a.s_min - 1e-9 else f"  < {a.s_min:.0%}"
        print(f"  {p:<4}{hours[p]:>8.1f} h {sh:>7.1%}{flag}")
        if flag:
            problems.append(f"{p} share {sh:.1%} below s_min {a.s_min:.0%}")
    osh = orphan / total
    print(f"  orph{orphan:>8.1f} h {osh:>7.1%}")
    if osh > a.o_max + 1e-9:
        problems.append(f"orphan share {osh:.1%} above o_max {a.o_max:.0%}")
    for p in problems:
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
