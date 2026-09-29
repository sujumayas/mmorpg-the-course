#!/usr/bin/env python3
"""PR201 lab 09: release burn-up forecast, scenario table and cut check. Standard library only.

Usage: python burnup_forecast.py history.csv [--sprints-left 2] [--plan mean|min|max] [--cuts cuts.csv]

history.csv has one row per sprint end; row 0 is the plan (scope only).
Model (PR201 week 9, sections 3 and 4):
  v_min, v_mean, v_max  from velocity_h
  g          = (scope_last - scope_0) / sprints so far
  remaining  = scope_last - sum(velocity_h)
  capacity   = N * (v - g)            g = 0 when frozen
  cut        = max(0, remaining - capacity)
  finish     = current + remaining / (v - g), if v > g
Cut check (with --cuts): the plan scenario is the chosen v with a freeze.
  'now' cuts must total at least that scenario's cut.
  'now' + 'next' cuts must total at least the cut for v_min with a freeze.
  No cut story may have ids in needed_by (a kept story that depends on it).
Prints PASS or NOT READY and exits 1 on a failed check.
"""
import argparse
import csv
import sys


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("history")
    ap.add_argument("--sprints-left", type=float, default=2)
    ap.add_argument("--plan", choices=["min", "mean", "max"], default="mean")
    ap.add_argument("--cuts")
    a = ap.parse_args()
    rows = read(a.history)
    vel = [float(r["velocity_h"]) for r in rows[1:]]
    scope0, scope = float(rows[0]["scope_h"]), float(rows[-1]["scope_h"])
    s = len(vel)
    v = {"min": min(vel), "mean": sum(vel) / s, "max": max(vel)}
    g = (scope - scope0) / s
    done = sum(vel)
    remaining = scope - done
    N = a.sprints_left
    print(f"v_min {v['min']:g}  v_mean {v['mean']:.1f}  v_max {v['max']:g}  g {g:.1f}  done {done:g}  remaining {remaining:g}  N {N:g}")

    print("\nDone-line-only forecast at each review (ignores scope growth):")
    d = 0.0
    for i, r in enumerate(rows[1:], start=1):
        d += float(r["velocity_h"])
        vm = d / i
        print(f"  after sprint {i}: finish at sprint {i + (float(r['scope_h']) - d) / vm:.1f}")

    def cut(vv, gg):
        return max(0.0, remaining - N * (vv - gg))

    print(f"\n{'scenario':<28}{'v':>6}{'g':>6}{'capacity':>10}{'cut':>8}{'finish':>9}")
    for name, key, gg in (("good sprints, freeze", "max", 0), ("typical sprints, freeze", "mean", 0),
                          ("typical sprints, no freeze", "mean", g), ("bad sprints, no freeze", "min", g)):
        net = v[key] - gg
        fin = f"{s + remaining / net:.1f}" if net > 0 else "never"
        print(f"{name:<28}{v[key]:>6.1f}{gg:>6.1f}{N * net:>10.1f}{cut(v[key], gg):>8.1f}{fin:>9}")

    if not a.cuts:
        return
    need_now = cut(v[a.plan], 0)
    need_all = cut(v["min"], 0)
    problems = []
    now = nxt = 0.0
    for r in read(a.cuts):
        when = r["when"].strip()
        h = float(r["estimate_h"])
        if when == "now":
            now += h
        elif when == "next":
            nxt += h
        if when in ("now", "next") and r["needed_by"].strip():
            problems.append(f"{r['id']} is cut but kept stories need it: {r['needed_by']}")
    print(f"\ncuts now {now:g} h (need {need_now:.1f} for v_{a.plan} with freeze); "
          f"now + next {now + nxt:g} h (need {need_all:.1f} for v_min with freeze)")
    if now + 1e-9 < need_now:
        problems.append(f"'now' cuts total {now:g} h, short of {need_now:.1f}")
    if now + nxt + 1e-9 < need_all:
        problems.append(f"'now' + 'next' cuts total {now + nxt:g} h, short of {need_all:.1f}")
    if problems:
        for p in problems:
            print("  -", p)
        print("NOT READY")
        sys.exit(1)
    print("PASS")


if __name__ == "__main__":
    main()
