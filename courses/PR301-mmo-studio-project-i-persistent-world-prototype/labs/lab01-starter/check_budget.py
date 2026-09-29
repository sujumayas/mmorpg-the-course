#!/usr/bin/env python3
"""PR301 lab 01: does a persistent-world pitch fit the team? Standard library only.

Usage: python check_budget.py pitches.csv [--n 7] [--hours 8] [--c 0.25] [--weeks 12] [--buffer 0.3] [--margin 0.9]

Model (PR301 week 1, section 2):
  supply    = n * (1 - buffer) * (hours - c * (n - 1)) * weeks
  authored  = target_play_hours / replay            content hours the team must author
  demand    = platform_hours + system_hours + cost_per_content_hour * authored
  load      = demand / supply                        PASS when load <= margin
  break-even target hours between pitches a and b:
            T* = (F_b - F_a) / (k_a / r_a - k_b / r_b), with F = platform + system, k = cost, r = replay
"""
import argparse
import csv
import sys

FIELDS = ["name", "target_play_hours", "platform_hours", "system_hours",
          "cost_per_content_hour", "replay"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pitches")
    ap.add_argument("--n", type=int, default=7)
    ap.add_argument("--hours", type=float, default=8)
    ap.add_argument("--c", type=float, default=0.25)
    ap.add_argument("--weeks", type=float, default=12)
    ap.add_argument("--buffer", type=float, default=0.3)
    ap.add_argument("--margin", type=float, default=0.9)
    a = ap.parse_args()

    with open(a.pitches, newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("NOT READY: no pitches in file")
        sys.exit(1)
    for r in rows:
        missing = [k for k in FIELDS if not (r.get(k) or "").strip()]
        if missing:
            print(f"NOT READY: pitch {r.get('name', '?')} is missing {', '.join(missing)}")
            sys.exit(1)

    supply = a.n * (1 - a.buffer) * (a.hours - a.c * (a.n - 1)) * a.weeks
    print(f"Team supply: {a.n} people x {(1 - a.buffer):.2f} x "
          f"({a.hours} - {a.c} x {a.n - 1}) h x {a.weeks:g} weeks = {supply:.1f} h")
    print(f"{'pitch':<14}{'authored h':>11}{'demand h':>10}{'load':>7}  verdict")
    best = None
    parsed = []
    for r in rows:
        T = float(r["target_play_hours"])
        F = float(r["platform_hours"]) + float(r["system_hours"])
        k = float(r["cost_per_content_hour"])
        rep = float(r["replay"])
        authored = T / rep
        demand = F + k * authored
        load = demand / supply
        ok = load <= a.margin
        parsed.append((r["name"], F, k, rep))
        print(f"{r['name']:<14}{authored:>11.2f}{demand:>10.1f}{load:>7.2f}  "
              f"{'PASS' if ok else 'OVER'}")
        if ok and (best is None or load < best[1]):
            best = (r["name"], load)
    for i in range(len(parsed)):
        for j in range(i + 1, len(parsed)):
            na, Fa, ka, ra = parsed[i]
            nb, Fb, kb, rb = parsed[j]
            slope = ka / ra - kb / rb
            if abs(slope) < 1e-9:
                continue
            t = (Fb - Fa) / slope
            if t > 0:
                print(f"Break-even between {na} and {nb}: {t:.2f} play hours per player")
    if best:
        print(f"PASS: {best[0]} fits at load {best[1]:.2f} (margin {a.margin})")
        sys.exit(0)
    print(f"NOT READY: no pitch at or below load {a.margin}")
    sys.exit(1)


if __name__ == "__main__":
    main()
