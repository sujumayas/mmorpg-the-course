"""PR101 lab 08: check a jam log before you hand it in.

Run from this folder:
    python check_log.py jam_log_template.csv
    python check_log.py ../our_jam_log.csv

Format, one row per task per checkpoint:
    team, task, hour, spent, remaining_est, status
Rules checked:
  - hour is one of 0, 6, 12, ..., 48 (a task may start at any checkpoint)
  - a task's first row has spent 0 and status open
  - spent never decreases; remaining_est is 0 or more
  - status is open, done or cut, and nothing follows a done or cut row
  - a done row has remaining_est 0
Exit code 0 means the log is ready for lab 09.
"""
import csv
import sys

CHECKPOINTS = set(range(0, 49, 6))
STATUSES = ("open", "done", "cut")


def check(path):
    problems = []
    tasks = {}
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        need = ["team", "task", "hour", "spent", "remaining_est", "status"]
        if reader.fieldnames != need:
            return [f"header must be exactly {','.join(need)}"], {}
        for i, r in enumerate(reader, start=2):
            try:
                hour, spent, rem = float(r["hour"]), float(r["spent"]), float(r["remaining_est"])
            except ValueError:
                problems.append(f"line {i}: hour, spent and remaining_est must be numbers")
                continue
            if hour not in CHECKPOINTS:
                problems.append(f"line {i}: hour {hour:g} is not a checkpoint (0, 6, ..., 48)")
            if r["status"] not in STATUSES:
                problems.append(f"line {i}: status {r['status']!r} is not open, done or cut")
            if rem < 0 or spent < 0:
                problems.append(f"line {i}: negative hours")
            tasks.setdefault(r["task"], []).append((hour, spent, rem, r["status"], i))
    for task, hist in tasks.items():
        hist.sort()
        if hist[0][1] != 0 or hist[0][3] != "open":
            problems.append(f"{task}: first row must be open with spent 0")
        for (h0, s0, _, st0, _), (h1, s1, _, _, line) in zip(hist, hist[1:]):
            if h1 == h0:
                problems.append(f"{task}: two rows at hour {h1:g} (line {line})")
            if s1 < s0:
                problems.append(f"{task}: spent went down at line {line}")
            if st0 != "open":
                problems.append(f"{task}: a row follows a {st0} row (line {line})")
        last = hist[-1]
        if last[3] == "done" and last[2] != 0:
            problems.append(f"{task}: done row must have remaining_est 0")
    return problems, tasks


def main(path):
    problems, tasks = check(path)
    done = sum(1 for h in tasks.values() if h[-1][3] == "done")
    cut = sum(1 for h in tasks.values() if h[-1][3] == "cut")
    print(f"{path}: {len(tasks)} tasks, {done} done, {cut} cut, {len(tasks) - done - cut} still open")
    for p in problems:
        print("  PROBLEM:", p)
    if problems:
        sys.exit(1)
    print("  log OK")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "jam_log_template.csv")
