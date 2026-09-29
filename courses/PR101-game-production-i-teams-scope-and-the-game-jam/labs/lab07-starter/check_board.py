"""PR101 lab 07: check a jam board export and a definition of done.

Run from this folder:
    python check_board.py tasks_template.csv dod_template.md --people 4 --wip 4
    python check_board.py my_tasks.csv my_dod.md --people 4 --wip 4 --seed ../jam_log.csv

tasks CSV columns: task, tier, estimate_hours, owner, acceptance
    tier is must, should or could. estimate_hours is person-hours, above 0 and at most 4.
DoD file: a Markdown checklist; every line starting with "- [ ]" counts as one item.
With --seed, the script writes the hour-0 rows of the lab 08 jam log.
Exit code 0 means every check passed.
"""
import argparse
import csv
import sys

COLUMNS = ["task", "tier", "estimate_hours", "owner", "acceptance"]
TIERS = ("must", "should", "could")
MAX_TASK_HOURS = 4.0
MIN_DOD_ITEMS = 4


def check(tasks_path, dod_path, people, wip):
    problems = []
    with open(tasks_path, newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            return [f"missing columns: {missing}"], []
        tasks = list(reader)
    seen = set()
    for i, t in enumerate(tasks, start=2):
        name = t["task"].strip()
        if not name:
            problems.append(f"line {i}: empty task id")
        if name in seen:
            problems.append(f"line {i}: duplicate task id {name}")
        seen.add(name)
        if t["tier"].strip() not in TIERS:
            problems.append(f"{name}: tier must be one of {TIERS}")
        try:
            est = float(t["estimate_hours"])
            if not 0 < est <= MAX_TASK_HOURS:
                problems.append(f"{name}: estimate {est} h; split tasks above {MAX_TASK_HOURS} h")
        except ValueError:
            problems.append(f"{name}: estimate_hours is not a number")
        acc = t["acceptance"].strip()
        if len(acc.split()) < 4 or acc.lower() == name.lower():
            problems.append(f"{name}: acceptance needs a checkable sentence (4+ words)")
    with open(dod_path) as f:
        items = [ln for ln in f if ln.lstrip().startswith("- [ ]")]
    if len(items) < MIN_DOD_ITEMS:
        problems.append(f"definition of done has {len(items)} items (need {MIN_DOD_ITEMS}+)")
    if wip > people + 1:
        problems.append(f"WIP limit {wip} is above people + 1 = {people + 1}")
    return problems, tasks


def summary(tasks):
    for tier in TIERS:
        hrs = sum(float(t["estimate_hours"]) for t in tasks if t["tier"].strip() == tier)
        n = sum(1 for t in tasks if t["tier"].strip() == tier)
        print(f"  {tier:6s} {n:3d} tasks  {hrs:6.1f} person-hours")


def seed_log(tasks, team, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["team", "task", "hour", "spent", "remaining_est", "status"])
        for t in tasks:
            w.writerow([team, t["task"].strip(), 0, 0, float(t["estimate_hours"]), "open"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tasks")
    ap.add_argument("dod")
    ap.add_argument("--people", type=int, required=True)
    ap.add_argument("--wip", type=int, required=True)
    ap.add_argument("--team", default="T1")
    ap.add_argument("--seed")
    a = ap.parse_args()
    problems, tasks = check(a.tasks, a.dod, a.people, a.wip)
    print(f"{len(tasks)} tasks, {a.people} people, WIP limit {a.wip}")
    summary(tasks)
    for p in problems:
        print("  PROBLEM:", p)
    if problems:
        sys.exit(1)
    print("  all checks passed")
    if a.seed:
        seed_log(tasks, a.team, a.seed)
        print(f"  wrote hour-0 log rows to {a.seed}")


if __name__ == "__main__":
    main()
