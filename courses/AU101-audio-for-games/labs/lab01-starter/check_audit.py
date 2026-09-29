"""AU101 Lab 01: check a sound audit CSV and print its summary numbers.

Usage (from the repository root):

    .venv/bin/python courses/AU101-audio-for-games/labs/lab01-starter/check_audit.py my_audit.csv

Standard library only. The script exits with status 1 and lists every problem
if the sheet breaks a rule, and prints the summary your memo must quote if it
passes. Rules are in labs/lab01.md, step 3.
"""
import csv
import re
import sys
from collections import Counter

COLUMNS = ["time", "event", "on_screen", "job", "second_job", "feedback_kind",
           "diegetic", "trigger", "mute_cost", "notes"]
JOBS = {"feedback", "space", "emotion"}
KINDS = {"confirm", "report", "forecast"}
YES_NO = {"yes", "no"}
TRIGGERS = {"input", "state"}
MIN_ROWS = 40
TIME = re.compile(r"^\d{1,2}:[0-5]\d$")


def seconds(stamp):
    minutes, secs = stamp.split(":")
    return int(minutes) * 60 + int(secs)


def check_rows(rows):
    """Return a list of problem strings. An empty list means the sheet is valid."""
    problems = []
    last = -1
    for n, row in enumerate(rows, start=2):  # row 1 is the header
        v = {k: (row.get(k) or "").strip().lower() for k in COLUMNS}
        if not TIME.match(v["time"]):
            problems.append(f"row {n}: time '{row.get('time')}' is not mm:ss")
        else:
            t = seconds(v["time"])
            if t < last:
                problems.append(f"row {n}: time goes backwards")
            last = t
        if not v["event"]:
            problems.append(f"row {n}: event is empty")
        if v["on_screen"] not in YES_NO:
            problems.append(f"row {n}: on_screen must be yes or no")
        if v["job"] not in JOBS:
            problems.append(f"row {n}: job must be one of {sorted(JOBS)}")
        if v["second_job"] and (v["second_job"] not in JOBS or v["second_job"] == v["job"]):
            problems.append(f"row {n}: second_job must be empty or a different job")
        if "feedback" in (v["job"], v["second_job"]):
            if v["feedback_kind"] not in KINDS:
                problems.append(f"row {n}: feedback rows need feedback_kind in {sorted(KINDS)}")
        elif v["feedback_kind"]:
            problems.append(f"row {n}: feedback_kind is only for feedback rows")
        if v["diegetic"] not in YES_NO:
            problems.append(f"row {n}: diegetic must be yes or no")
        if v["trigger"] not in TRIGGERS:
            problems.append(f"row {n}: trigger must be input or state")
        if v["mute_cost"] not in {"1", "2", "3"}:
            problems.append(f"row {n}: mute_cost must be 1, 2 or 3")
    if len(rows) < MIN_ROWS:
        problems.append(f"only {len(rows)} events; the lab needs at least {MIN_ROWS}")
    return problems


def summary(rows):
    """Percentages the memo quotes. Keys are stable so you can cite them."""
    n = len(rows)
    low = [{k: (r.get(k) or "").strip().lower() for k in COLUMNS} for r in rows]
    jobs = Counter(r["job"] for r in low)
    kinds = Counter(r["feedback_kind"] for r in low if r["feedback_kind"])
    pct = lambda k: round(100 * k / n, 1) if n else 0.0
    return {
        "events": n,
        "job_feedback_pct": pct(jobs["feedback"]),
        "job_space_pct": pct(jobs["space"]),
        "job_emotion_pct": pct(jobs["emotion"]),
        "off_screen_pct": pct(sum(r["on_screen"] == "no" for r in low)),
        "forecast_pct_of_feedback": round(100 * kinds["forecast"] / max(1, sum(kinds.values())), 1),
        "state_triggered_pct": pct(sum(r["trigger"] == "state" for r in low)),
        "mute_cost_3_count": sum(r["mute_cost"] == "3" for r in low),
    }


def main(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            print(f"missing columns: {missing}")
            return 1
        rows = list(reader)
    problems = check_rows(rows)
    for key, value in summary(rows).items():
        print(f"{key:>26}: {value}")
    if problems:
        print(f"\n{len(problems)} problem(s):")
        for p in problems:
            print("  -", p)
        return 1
    print("\nOK: the sheet passes every rule.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
