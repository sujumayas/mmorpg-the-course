"""PR101 Lab 06 starter: estimate ratios, skew and the whole-plan ratio.

Files:
  jam_plans_example.csv  an invented set of first-evening jam plans from a
                         fictional earlier cohort: teams A-F used no task-size
                         rule (rule "none"), teams G-L split every task to
                         4 hours or less (rule "split4")
  our_plan.csv           an empty file with the same columns for your team

Each row is one task from a team's hour-0 plan: estimate_h is the estimate
in person-hours and actual_h what the task really took. A blank actual_h
means the task was cut before it was finished; cut rows have no ratio.

Run the tests:   python test_lab06.py
Print a report:  python estimates.py jam_plans_example.csv
"""
import csv
import math
import sys


def load_log(path):
    """Read a plan CSV into a list of dicts. Done for you.
    estimate_h becomes a float, actual_h a float or None (cut)."""
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            actual = r["actual_h"].strip()
            rows.append({
                "team": r["team"],
                "rule": r["rule"],
                "task": r["task"],
                "estimate_h": float(r["estimate_h"]),
                "actual_h": float(actual) if actual else None,
            })
    return rows


def finished(rows, rule=None):
    """Rows that have an actual (not cut), optionally only one rule's teams.
    Done for you."""
    return [r for r in rows if r["actual_h"] is not None
            and (rule is None or r["rule"] == rule)]


def ratio(estimate, actual):
    """Return actual / estimate, the lecture's r.
    Raise ValueError if estimate is zero or negative."""
    raise NotImplementedError


def median(values):
    """Return the median of a non-empty list (average the middle two when
    the length is even). Raise ValueError for an empty list.
    Do not change the caller's list."""
    raise NotImplementedError


def percentile(values, p):
    """Return the p-th quantile (p between 0 and 1) with linear
    interpolation, the lecture's method: sort the values, set
    h = (n - 1) * p, and move the fraction h - floor(h) of the way from the
    value at index floor(h) to the next one.
    percentile(v, 0.5) must equal median(v).
    Raise ValueError for an empty list or p outside [0, 1]."""
    raise NotImplementedError


def summary(rows, rule=None):
    """Summarize the finished rows (optionally one rule's teams) as a dict:
      "n"        number of finished rows
      "p10"      10th percentile of the ratios
      "median"   median ratio
      "p90"      90th percentile of the ratios
      "mean"     arithmetic mean of the ratios
      "project"  sum of actuals / sum of estimates
    Cut rows are skipped."""
    raise NotImplementedError


def skew_penalty(sigma):
    """The lecture's e^(sigma^2 / 2): how far the mean ratio sits above the
    geometric mean when ratios are log-normal."""
    raise NotImplementedError


def buffer_for(project_r):
    """The buffer fraction b (week 4) that would have exactly absorbed a
    project ratio project_r: plan P = (1 - b) * C and need P * project_r = C.
    Return 0.0 when project_r <= 1 (no buffer needed)."""
    raise NotImplementedError


def corrected_estimate(raw, band):
    """Turn a raw estimate into a range using a (p10, median, p90) band.
    Return a tuple (low, likely, high)."""
    raise NotImplementedError


def report(path):
    """Print a summary per rule. Done for you; it works once the functions
    above do."""
    rows = load_log(path)
    print(f"{path}: {len(rows)} tasks, {len(finished(rows))} finished")
    print("rule      n   p10  median   p90  mean  project  buffer")
    for rule in sorted({r["rule"] for r in rows}):
        s = summary(rows, rule)
        print(f"{rule:<7} {s['n']:>3}  {s['p10']:4.2f}   {s['median']:4.2f}  "
              f"{s['p90']:4.2f}  {s['mean']:4.2f}    {s['project']:4.2f}   "
              f"{buffer_for(s['project']):4.2f}")


if __name__ == "__main__":
    report(sys.argv[1] if len(sys.argv) > 1 else "jam_plans_example.csv")
