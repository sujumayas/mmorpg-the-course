"""MA102 lab 12 starter: summarizing a playtest.

Run it as a script (python lab12_starter.py) or paste it into a notebook.
Standard library only. If you prefer pandas, pd.read_csv("playtest_w12.csv")
loads the same table; numpy.percentile uses the same inclusive rule by default.

What is done for you:
    load_rows()                   the CSV as a list of dicts (all values are strings)
    column(rows, name)            one numeric column, blanks skipped
    inclusive_percentile(v, p)    the week 12 rule, p in [0, 100]; matches PERCENTILE.INC

What you write: everything in steps 1 to 7 of the lab handout. The
`summarize` stub below is a place to start.
"""
import csv
import math
from pathlib import Path

HERE = Path(__file__).parent


def load_rows(name="playtest_w12.csv"):
    with open(HERE / name, newline="") as f:
        return list(csv.DictReader(f))


def column(rows, name):
    return [float(r[name]) for r in rows if r[name] != ""]


def inclusive_percentile(values, p):
    """Sort, take position h = (n - 1) * p/100 + 1 (1-based), interpolate."""
    v = sorted(values)
    h = (len(v) - 1) * p / 100
    lo = math.floor(h)
    hi = min(lo + 1, len(v) - 1)
    return v[lo] + (h - lo) * (v[hi] - v[lo])


def summarize(values):
    """Return n, mean, median, sample SD, Q1, Q3, IQR, P90 and the 1.5 x IQR fences."""
    raise NotImplementedError("Step 2: write summarize().")


if __name__ == "__main__":
    rows = load_rows()
    print(len(rows), "rows")
    times = column(rows, "clear_minutes")
    print("median clear time", inclusive_percentile(times, 50))
