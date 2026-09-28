#!/usr/bin/env python3
"""UX201 Lab 08 starter: summarise a RITE usability test.

Inputs (CSV, see the example files):
  observations.csv  tester, build, minute, task, issue_id, kind, note
                    kind is 'error' or 'failure' (week 8 definitions); one row per issue per tester
                    (log an issue once per tester even if it recurs; note repeats in 'note').
  changes.csv       after_tester, issue_id, change, refix_of
                    one row per change to the build; for a re-fix, put the issue_id again and
                    set refix_of to the after_tester value of the earlier change.

Prints: errors and failures per tester with build boundaries, each issue's sightings, fix status,
sightings after its fix (a failed fix), verification confidence 1 - (1 - p)^m for p = 0.1 and 0.3
where m is the number of testers since the last fix with no sighting, and the impact and re-fix
ratios from Medlock et al. (2002).

Usage:  python3 rite_report.py observations.csv changes.csv
Standard library only.
"""
import csv
import sys
from collections import defaultdict


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def main(obs_path, chg_path):
    obs = read(obs_path)
    chg = read(chg_path)
    testers = sorted({int(r["tester"]) for r in obs})
    n = max(testers)
    per = defaultdict(lambda: {"error": 0, "failure": 0})
    build_of = {}
    seen = defaultdict(list)
    for r in obs:
        t = int(r["tester"])
        per[t][r["kind"].strip().lower()] += 1
        build_of[t] = r["build"]
        seen[r["issue_id"].strip()].append(t)
    fixes = defaultdict(list)
    for r in chg:
        fixes[r["issue_id"].strip()].append(int(r["after_tester"]))
    change_points = sorted({int(r["after_tester"]) for r in chg})

    print("Per tester (| marks a build change after that tester)")
    for t in range(1, n + 1):
        e, f = per[t]["error"], per[t]["failure"]
        bar = "#" * e + "X" * f
        mark = " |" if t in change_points else ""
        print(f"  tester {t:2d} build {build_of.get(t, '?'):>3}: errors {e:2d} failures {f:2d}  {bar}{mark}")

    print("\nIssues")
    print(f"  {'id':<6}{'seen by testers':<22}{'fixed after':<14}{'seen after fix':<16}{'m':>3}{'conf p=.1':>11}{'conf p=.3':>11}")
    found = set(seen)
    fixed = {i for i in fixes}
    for i in sorted(found | fixed):
        ts = sorted(seen.get(i, []))
        last_fix = max(fixes[i]) if i in fixes else None
        after = [t for t in ts if last_fix is not None and t > last_fix]
        if last_fix is not None and not after:
            m = n - last_fix
            c1 = 1 - 0.9 ** m
            c3 = 1 - 0.7 ** m
            conf = f"{m:3d}{c1:11.3f}{c3:11.3f}"
        else:
            conf = f"{'-':>3}{'-':>11}{'-':>11}"
        print(f"  {i:<6}{','.join(map(str, ts)) or '-':<22}{','.join(map(str, fixes.get(i, []))) or 'open':<14}"
              f"{','.join(map(str, after)) or '-':<16}{conf}")

    total_found = len(found)
    got_fix = len(found & fixed)
    total_changes = len(chg)
    refixes = sum(1 for r in chg if (r.get("refix_of") or "").strip())
    print(f"\nImpact ratio  = {got_fix}/{total_found} = {got_fix / total_found:.0%}  (issues found that received a fix)")
    if total_changes:
        print(f"Re-fix ratio  = {refixes}/{total_changes} = {refixes / total_changes:.0%}  (changes that redid an earlier fix)")
    failed = [i for i in fixed if any(t > max(fixes[i]) for t in seen.get(i, []))]
    if failed:
        print("Fixes contradicted by later sightings (need a re-fix):", ", ".join(sorted(failed)))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
