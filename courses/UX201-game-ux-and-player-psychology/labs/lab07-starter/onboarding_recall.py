#!/usr/bin/env python3
"""UX201 Lab 07 starter: recall at the moment of need.

Reads an event log (CSV with columns mechanic, event, minute, note) where event is
one of teach, use, need, prompt. For every "need" row it prints the number of
practice uses before it, the stability s, the gap since last use and the recall

    recall = exp(-gap / s),   s = s0 * g ** uses

as in UX201 week 7, section 2. A "prompt" row at the same minute as a "need" row
marks the need as prompted (knowledge in the world): recall is reported as 1.0 and
the need does not count as a retrieval. Every unprompted "need" also counts as a
use for later needs, because the player had to retrieve the mechanic.

Usage:
    python3 onboarding_recall.py onboarding_events.csv
    python3 onboarding_recall.py log.csv --s0 10 --g 2      # sensitivity runs
    python3 onboarding_recall.py log.csv --target 0.8       # flag gaps below 0.8

Standard library only.
"""
import argparse
import csv
import math
from collections import defaultdict


def load(path):
    events = defaultdict(list)
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            kind = row["event"].strip().lower()
            if kind not in {"teach", "use", "need", "prompt"}:
                raise SystemExit(f"unknown event '{row['event']}' in row {row}")
            events[row["mechanic"].strip()].append(
                (float(row["minute"]), kind, (row.get("note") or "").strip()))
    for rows in events.values():
        rows.sort(key=lambda r: (r[0], ["teach", "use", "prompt", "need"].index(r[1])))
    return events


def analyse(events, s0, g, target):
    needs = []
    for mech, rows in events.items():
        taught = None
        uses = 0
        last = None
        prompts = {m for m, k, _ in rows if k == "prompt"}
        for minute, kind, note in rows:
            if kind == "teach" and taught is None:
                taught, last = minute, minute
            elif kind == "use" and taught is not None and minute > last:
                uses += 1
                last = minute
            elif kind == "need":
                if taught is None:
                    needs.append((minute, mech, note, None, None, None, None, "never taught"))
                    continue
                s = s0 * g ** uses
                gap = minute - last
                if minute in prompts:
                    needs.append((minute, mech, note, uses, s, gap, 1.0, "prompted"))
                    continue
                r = math.exp(-gap / s)
                flag = "LOW" if r < target else ""
                needs.append((minute, mech, note, uses, s, gap, r, flag))
                uses += 1          # retrieval at the need counts as practice
                last = minute
    return sorted(needs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--s0", type=float, default=20.0)
    ap.add_argument("--g", type=float, default=2.5)
    ap.add_argument("--target", type=float, default=0.8)
    a = ap.parse_args()
    needs = analyse(load(a.csv), a.s0, a.g, a.target)
    print(f"s0 = {a.s0:g} min, g = {a.g:g}, target recall = {a.target:g}\n")
    print(f"{'min':>6}  {'mechanic':<14}{'uses':>5}{'s':>9}{'gap':>7}{'recall':>8}  flag   note")
    by_minute = defaultdict(list)
    for minute, mech, note, uses, s, gap, r, flag in needs:
        if r is None:
            print(f"{minute:6.1f}  {mech:<14}{'-':>5}{'-':>9}{'-':>7}{'-':>8}  {flag}  {note}")
            continue
        print(f"{minute:6.1f}  {mech:<14}{uses:5d}{s:9.1f}{gap:7.1f}{r:8.3f}  {flag:<6} {note}")
        by_minute[(minute, note)].append(r)
    print("\nAll-ready recall per moment of need (product over mechanics needed at that minute):")
    for (minute, note), rs in sorted(by_minute.items()):
        print(f"  minute {minute:g} {note!r}: {math.prod(rs):.3f} over {len(rs)} mechanic(s); "
              f"expected missing {sum(1 - r for r in rs):.2f}")


if __name__ == "__main__":
    main()
