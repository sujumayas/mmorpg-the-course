#!/usr/bin/env python3
"""UX201 Lab 09 starter: how many problems did the heuristic evaluation miss?

Input: findings.csv with columns evaluator, problem_id (one row per evaluator per consolidated
problem that evaluator found). Optional: severity.csv with columns problem_id, rater, severity.

Prints, as in UX201 week 9 section 2:
  - problems found per evaluator, the union as evaluators are added, and lambda-hat
  - the found-by histogram f_k, and the Chao estimate S + f1^2 / (2 f2)
  - Lincoln-Petersen n_A n_B / m and Chapman for a split you choose (--a E1,E2), or for
    every split into two non-empty groups when --all-splits is given (min, median, max)
  - mean severity per problem if severity.csv is given

Usage:
  python3 capture.py findings.csv --a E1,E2
  python3 capture.py findings.csv --all-splits --severity severity.csv
Standard library only.
"""
import argparse
import csv
import itertools
import statistics
from collections import defaultdict


def lp(sa, sb):
    m = len(sa & sb)
    if m == 0:
        return None, None, 0
    na, nb = len(sa), len(sb)
    return na * nb / m, (na + 1) * (nb + 1) / (m + 1) - 1, m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("findings")
    ap.add_argument("--a", help="comma-separated evaluators in group A; the rest form group B")
    ap.add_argument("--all-splits", action="store_true")
    ap.add_argument("--severity")
    args = ap.parse_args()

    found = defaultdict(set)
    with open(args.findings, newline="") as f:
        for row in csv.DictReader(f):
            found[row["evaluator"].strip()].add(row["problem_id"].strip())
    evals = sorted(found)
    union = set()
    print("Evaluator  found  union so far")
    for e in evals:
        union |= found[e]
        print(f"  {e:<8}{len(found[e]):6d}{len(union):8d}")
    S = len(union)
    mean_found = statistics.mean(len(found[e]) for e in evals)

    counts = defaultdict(int)
    for p in union:
        counts[sum(p in found[e] for e in evals)] += 1
    f1, f2 = counts.get(1, 0), counts.get(2, 0)
    print("\nFound by k evaluators: " + ", ".join(f"k={k}: {counts[k]}" for k in sorted(counts)))
    if f2 > 0:
        chao = S + f1 * f1 / (2 * f2)
        label = "S + f1^2/(2 f2)"
    else:
        chao = S + f1 * (f1 - 1) / 2
        label = "bias-corrected, f2 = 0"
    print(f"S = {S}, f1 = {f1}, f2 = {f2}, Chao = {chao:.2f} ({label})")

    if args.a:
        A = {x.strip() for x in args.a.split(",")}
        B = set(evals) - A
        sa = set().union(*(found[e] for e in A))
        sb = set().union(*(found[e] for e in B))
        est, chap, m = lp(sa, sb)
        print(f"\nSplit A = {sorted(A)}, B = {sorted(B)}: n_A = {len(sa)}, n_B = {len(sb)}, m = {m}")
        if est is None:
            print("  no overlap: Lincoln-Petersen undefined")
        else:
            print(f"  Lincoln-Petersen = {est:.2f}, Chapman = {chap:.2f}")
            print(f"  lambda-hat = mean found / LP = {mean_found:.2f} / {est:.2f} = {mean_found / est:.2f}")

    if args.all_splits:
        ests = []
        for r in range(1, len(evals) // 2 + 1):
            for A in itertools.combinations(evals, r):
                B = [e for e in evals if e not in A]
                sa = set().union(*(found[e] for e in A))
                sb = set().union(*(found[e] for e in B))
                est, _, _ = lp(sa, sb)
                if est is not None:
                    ests.append(est)
        if ests:
            print(f"\nAll {len(ests)} splits with overlap: Lincoln-Petersen min {min(ests):.2f}, "
                  f"median {statistics.median(ests):.2f}, max {max(ests):.2f}")

    print(f"\nReport: {S} problems found; estimated total roughly between the Lincoln-Petersen and Chao values.")

    if args.severity:
        sev = defaultdict(list)
        with open(args.severity, newline="") as f:
            for row in csv.DictReader(f):
                sev[row["problem_id"].strip()].append(float(row["severity"]))
        print("\nMean severity (raters), sorted:")
        for p, vals in sorted(sev.items(), key=lambda kv: -statistics.mean(kv[1])):
            fb = sum(p in found[e] for e in evals)
            flag = "  (fewer than 3 raters)" if len(vals) < 3 else ""
            print(f"  {p:<8}{statistics.mean(vals):5.1f}  found by {fb}{flag}")


if __name__ == "__main__":
    main()
