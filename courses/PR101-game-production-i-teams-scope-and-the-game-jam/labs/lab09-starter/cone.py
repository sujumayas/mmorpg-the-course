"""PR101 lab 09: the cone (and the pipe) of uncertainty from a jam log.

Run from this folder:
    python cone.py                      # uses jam_log_sample.csv
    python cone.py ../my_team_log.csv   # uses your class log
    python -m unittest test_cone -v
    python cone.py my_log.csv --lab06 my_plan.csv   # convert for lab 06's module

The log format is the one from lab 08. One row per task per checkpoint:
    team, task, hour, spent, remaining_est, status
status is "open", "done" or "cut". A "done" row has spent = the task's
actual person-hours. The functions marked TODO are yours to write.
"""
import csv
import statistics
import sys

EDGES = (0.0, 0.25, 0.5, 0.75, 1.0)


def load_log(path):
    """Read the CSV into a list of dicts with numbers converted. Complete."""
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            rows.append({
                "team": r["team"],
                "task": r["task"],
                "hour": float(r["hour"]),
                "spent": float(r["spent"]),
                "remaining_est": float(r["remaining_est"]),
                "status": r["status"].strip(),
            })
    return rows


def task_histories(rows):
    """Group rows by task, each list sorted by hour. Complete."""
    out = {}
    for r in rows:
        out.setdefault(r["task"], []).append(r)
    for hist in out.values():
        hist.sort(key=lambda r: r["hour"])
    return out


def checkpoint_ratios(history):
    """Return a list of (x, total_ratio, remaining_ratio), one per usable open row.

    Only tasks whose last row is "done" have an actual, so return [] for any
    other task. Let A be the spent value on the done row. For each "open" row
    with remaining_est > 0:
        x               = spent / A
        total_ratio     = A / (spent + remaining_est)
        remaining_ratio = (A - spent) / remaining_est
    Skip open rows with remaining_est == 0 (count those with zero_claims).
    TODO
    """
    raise NotImplementedError


def zero_claims(rows):
    """Number of "open" rows whose remaining_est is 0. TODO"""
    raise NotImplementedError


def band(values):
    """Return (p10, p50, p90) of a list with at least two values.

    Use the inclusive linear-interpolation rule from MA102 week 12:
    statistics.quantiles(values, n=10, method="inclusive") returns the nine
    cut points p10 ... p90. TODO
    """
    raise NotImplementedError


def cone_table(rows, edges=EDGES):
    """Pool the checkpoint ratios of every task and summarise them per bin of x.

    Return one dict per bin [edges[i], edges[i+1]) with keys:
        "lo", "hi", "n", "total", "remaining"
    where "total" and "remaining" are band(...) tuples of the ratios whose x
    falls in the bin, or None when the bin has fewer than two points.
    TODO
    """
    raise NotImplementedError


def initial_bias(rows):
    """Median of A / first remaining_est over every task that finished. TODO"""
    raise NotImplementedError


def write_lab06_csv(rows, path, rule="jam"):
    """Write one row per task in lab 06's format (team, rule, task, estimate_h, actual_h).

    estimate_h is the task's first remaining_est; actual_h is blank for tasks
    that were not done. Complete. Lets you run lab 06's module on your jam log.
    """
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["team", "rule", "task", "estimate_h", "actual_h"])
        for task, hist in task_histories(rows).items():
            done = hist[-1]["status"] == "done"
            w.writerow([hist[0]["team"], rule, task, hist[0]["remaining_est"],
                        hist[-1]["spent"] if done else ""])


def main(path):
    rows = load_log(path)
    print(f"log: {path}, {len(rows)} rows, {len(task_histories(rows))} tasks")
    try:
        report(rows)
    except NotImplementedError:
        print("Some functions are still TODO. Run the tests to see which.")


def report(rows):
    print(f"median actual / first estimate: {initial_bias(rows):.2f}")
    print(f"open rows claiming 0 hours left: {zero_claims(rows)}")
    print()
    print("x bin        n    total p10  p50  p90  spread | remaining p10  p50  p90  spread")
    for b in cone_table(rows):
        head = f"{b['lo']:.2f}-{b['hi']:.2f}  {b['n']:3d}"
        parts = []
        for key in ("total", "remaining"):
            t = b[key]
            if t is None:
                parts.append("       (too few points)       ")
            else:
                parts.append(f"   {t[0]:.2f} {t[1]:.2f} {t[2]:.2f}  {t[2] / t[0]:5.2f} ")
        print(head + "  " + " |    ".join(parts))


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 3 and args[1] == "--lab06":
        write_lab06_csv(load_log(args[0]), args[2])
        print(f"wrote {args[2]} in lab 06 format")
    else:
        main(args[0] if args else "jam_log_sample.csv")
