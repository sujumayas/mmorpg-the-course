"""MMO308 Lab 03: the retention triangle.

Fill in every function marked TODO, then run `python test_retention.py`.
Run `python gen_cohorts.py` first so installs.csv and activity.csv exist.
Standard-library Python 3.10+ only.

Conventions (from the week 3 lecture and DB201 week 12):
  * A cohort is every player with the same install day c.
  * R(c, a) is exact-day retention: the share of cohort c active on day c + a.
  * A cell is complete only if c + a <= last_day. Incomplete cells are left out,
    never filled with 0.
"""
import csv
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAST_DAY = 89


# ---------------------------------------------------------------- provided

def load_installs(path=HERE / "installs.csv"):
    """Return {player_id: install_day}."""
    with open(path, newline="") as f:
        return {r["player_id"]: int(r["install_day"]) for r in csv.DictReader(f)}


def load_activity(path=HERE / "activity.csv"):
    """Return {day: set(player_id)}."""
    days = defaultdict(set)
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            days[int(r["day"])].add(r["player_id"])
    return dict(days)


# ---------------------------------------------------------------- TODO

def cohort_sizes(installs):
    """Return {install_day: number of players who installed that day}."""
    raise NotImplementedError("cohort_sizes: players per install day")


def cohort_table(installs, activity, last_day=LAST_DAY, max_age=30):
    """Return {c: {a: R(c, a)}} for every cohort c and every age 0 <= a <= max_age
    whose cell is complete (c + a <= last_day)."""
    raise NotImplementedError("cohort_table: exact-day retention per cell")


def checkpoint(table, n):
    """Return {c: R(c, n)} for every cohort that has a complete age-n cell."""
    raise NotImplementedError("checkpoint: the Dn series by install day")


def pooled(table, sizes, n, first, last):
    """Dn pooled over cohorts first..last (inclusive) that have an age-n cell:
    total retained players divided by total cohort size. Return None if no cohort qualifies."""
    raise NotImplementedError("pooled: size-weighted Dn over a range of cohorts")


def find_step(series, window=5):
    """series is {c: value}. For every c with `window` values before it
    (c - window .. c - 1) and `window` values from it (c .. c + window - 1),
    compute mean(after) - mean(before). Return (c, difference) for the c with the
    largest absolute difference."""
    raise NotImplementedError("find_step: the install day of the biggest step")


def calendar_index(table, min_age=1):
    """For each calendar day t, average the ratio R(c, a) / column_mean(a) over all
    cells with c + a == t and a >= min_age, where column_mean(a) is the mean of
    column a over all cohorts that have it. Return {t: index}. A value near 1
    is a normal day; a one-day period effect shows as a value far from 1."""
    raise NotImplementedError("calendar_index: diagonal averages of normalized cells")


# ---------------------------------------------------------------- report

if __name__ == "__main__":
    installs, activity = load_installs(), load_activity()
    sizes = cohort_sizes(installs)
    table = cohort_table(installs, activity)
    for n in (1, 7, 30):
        s = checkpoint(table, n)
        c, diff = find_step(s)
        print(f"D{n}: biggest 5-vs-5 step at install day {c} ({100 * diff:+.1f} points)")
    idx = calendar_index(table)
    low = sorted(idx.items(), key=lambda kv: kv[1])[:3]
    print("calendar days with the lowest index:", [(t, round(v, 2)) for t, v in low])
