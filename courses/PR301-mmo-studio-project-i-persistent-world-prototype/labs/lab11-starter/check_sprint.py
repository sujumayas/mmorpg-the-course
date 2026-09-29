#!/usr/bin/env python3
"""PR301 lab 11: check a one-week sprint plan against the capacity rule. Standard library only.

Usage: python check_sprint.py velocity.csv availability.csv backlog.csv

Model (PR301 week 11, section 2):
  weekly velocity  = done_hours / weeks, for each past sprint (use the last three)
  availability     = sum(available_days) / sum(full_days)
  capacity_low     = min(weekly velocity) x availability
  capacity_mean    = mean(weekly velocity) x availability
  bug reserve      = sum of hours with status "bug"
  commit (status "commit") must be <= capacity_low - bug reserve
  stretch (status "stretch") must be <= capacity_mean - bug reserve - commit
Every committed item's dependencies must be "done" or "commit". Every stretch item's
dependencies must be "done", "commit" or "stretch". Items with status "deferred" or "cut"
need a note. At least one note must start with "rescoped".
"""
import csv
import sys

STATUSES = {"done", "commit", "stretch", "bug", "deferred", "cut"}


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    problems = []
    vel = read(sys.argv[1])[-3:]
    weekly = [float(r["done_hours"]) / float(r["weeks"]) for r in vel]
    people = read(sys.argv[2])
    full = sum(float(p["full_days"]) for p in people)
    avail = sum(float(p["available_days"]) for p in people) / full
    low = min(weekly) * avail
    mean = sum(weekly) / len(weekly) * avail
    items = read(sys.argv[3])
    status = {}
    for r in items:
        s = r["status"].strip().lower()
        if s not in STATUSES:
            problems.append(f"{r['id']}: status '{s}' is not one of {sorted(STATUSES)}")
        status[r["id"]] = s
    pts = lambda s: sum(float(r["hours"]) for r in items if status[r["id"]] == s)
    reserve, commit, stretch = pts("bug"), pts("commit"), pts("stretch")
    print("weekly velocity: " + ", ".join(f"{w:.2f}" for w in weekly))
    print(f"availability {avail:.3f}  capacity_low {low:.1f}  capacity_mean {mean:.1f}")
    print(f"bug reserve {reserve:g}  commit {commit:g}  stretch {stretch:g}")
    if commit > low - reserve + 1e-9:
        problems.append(f"commit {commit:g} exceeds capacity_low - reserve = {low - reserve:.1f}")
    if stretch > mean - reserve - commit + 1e-9:
        problems.append(f"stretch {stretch:g} exceeds capacity_mean - reserve - commit = "
                        f"{mean - reserve - commit:.1f}")
    allowed = {"commit": {"done", "commit"}, "stretch": {"done", "commit", "stretch"}}
    for r in items:
        s = status[r["id"]]
        for d in filter(None, (x.strip() for x in r["depends_on"].split(";"))):
            if d not in status:
                problems.append(f"{r['id']}: depends on unknown id {d}")
            elif s in allowed and status[d] not in allowed[s]:
                problems.append(f"{r['id']} ({s}) depends on {d}, which is {status[d]}")
        if s in {"deferred", "cut"} and not r["note"].strip():
            problems.append(f"{r['id']}: {s} without a note")
    if not any(r["note"].strip().lower().startswith("rescoped") for r in items):
        problems.append("no item has a note starting with 'rescoped'")
    for p in problems:
        print("  -", p)
    print("PASS" if not problems else "NOT READY")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
