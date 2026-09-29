#!/usr/bin/env python3
"""PR301 lab 03: does the sprint 1 plan fit the people who own it? Standard library only.

Usage: python check_sprint.py team.csv sprint.csv [--focus 0.62] [--weeks 2] [--c 0.25] [--studio 3] [--cross 1.5]

Model (PR301 week 3, section 2):
  capacity_i = focus * (hours_i - c * (n - 1)) * weeks          estimate hours person i can finish
  charge     = est_hours * cross   if the story's discipline is not the owner's primary, else est_hours
  load_i     = sum of charges on committed stories owned by i / capacity_i
  Status values: committed, stretch, studio (done together in the studio session, not charged
  to anyone, at most --studio hours in total), later.
  PASS when every goal story is committed or studio, every dependency of a committed story is
  committed, studio or done, studio hours <= --studio, and every load <= 1.
"""
import argparse
import csv
import sys


def read(path):
    with open(path, newline="") as f:
        return [{k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("team")
    ap.add_argument("sprint")
    ap.add_argument("--focus", type=float, default=0.62)
    ap.add_argument("--weeks", type=float, default=2)
    ap.add_argument("--c", type=float, default=0.25)
    ap.add_argument("--studio", type=float, default=3)
    ap.add_argument("--cross", type=float, default=1.5)
    a = ap.parse_args()
    team = {m["name"]: m for m in read(a.team)}
    stories = read(a.sprint)
    n = len(team)
    problems = []
    cap = {k: a.focus * (float(m["hours_per_week"]) - a.c * (n - 1)) * a.weeks for k, m in team.items()}
    charged = {k: 0.0 for k in team}
    by_id = {s["id"]: s for s in stories}
    in_plan = {"committed", "studio", "done"}
    studio_h = 0.0
    for s in stories:
        st = s["status"]
        if st not in {"committed", "stretch", "studio", "later", "done"}:
            problems.append(f"{s['id']}: unknown status '{st}'")
            continue
        if s["goal"].lower() == "y" and st not in in_plan:
            problems.append(f"{s['id']}: goal story is '{st}', not committed")
        if st == "studio":
            studio_h += float(s["est_hours"])
        if st == "committed":
            owner = s["owner"]
            if owner not in team:
                problems.append(f"{s['id']}: owner '{owner}' not in team.csv")
                continue
            mult = 1.0 if team[owner]["primary"] == s["discipline"] else a.cross
            charged[owner] += float(s["est_hours"]) * mult
        if st in {"committed", "studio"}:
            for d in filter(None, s["deps"].replace(";", " ").split()):
                if d not in by_id:
                    problems.append(f"{s['id']}: unknown dependency {d}")
                elif by_id[d]["status"] not in in_plan:
                    problems.append(f"{s['id']}: depends on {d}, which is '{by_id[d]['status']}'")
    if studio_h > a.studio:
        problems.append(f"studio stories total {studio_h:g} h, more than the {a.studio:g} h session")
    print(f"{'person':<8}{'primary':<12}{'capacity':>9}{'charged':>9}{'load':>7}")
    for k in team:
        load = charged[k] / cap[k]
        flag = "  OVER" if load > 1 else ""
        print(f"{k:<8}{team[k]['primary']:<12}{cap[k]:>9.2f}{charged[k]:>9.1f}{load:>7.2f}{flag}")
        if load > 1:
            problems.append(f"{k} is loaded at {load:.2f}")
    total_cap, total = sum(cap.values()), sum(charged.values())
    print(f"{'team':<20}{total_cap:>9.2f}{total:>9.1f}{total / total_cap:>7.2f}")
    for p in problems:
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
