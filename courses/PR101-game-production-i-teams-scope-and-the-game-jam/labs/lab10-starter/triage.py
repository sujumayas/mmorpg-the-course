"""PR101 lab 10: bug triage and the backlog model.

Implement every function marked TODO. The rules are in the week 10 lecture,
sections 1 to 3. Run the tests from inside this folder with:

    python -m unittest -v
"""
import csv

SEVERITIES = (1, 2, 3, 4)             # S1 blocker ... S4 cosmetic
FREQUENCY_BAND = {"always": 0, "often": 1, "rare": 2}


def load_bugs(path):
    """Read a bug CSV into a list of dicts. Provided, already working.

    Columns: id, title, severity (1-4), frequency (always/often/rare), status.
    severity is converted to int; everything else stays a string.
    """
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for row in rows:
        row["severity"] = int(row["severity"])
        row["frequency"] = row["frequency"].strip().lower()
        row["status"] = row["status"].strip().lower()
    return rows


def priority(severity, frequency):
    """Return the priority 1-4 from the week 10 matrix.

    P = S + F - 1, clamped to 1..4, where F is 0 for always, 1 for often and
    2 for rare. Raise ValueError for a severity outside 1-4 or an unknown
    frequency word.
    """
    raise NotImplementedError("TODO: priority")


def find_rates(f0, d, days):
    """Daily finds after feature lock: round(f0 * d**(t-1)) for t = 1..days.

    Round half up (6.5 -> 7), not Python's round(), which rounds half to even.
    """
    raise NotImplementedError("TODO: find_rates")


def backlog(b0, found, capacity, r=0.0):
    """Open bugs at the end of each day.

    arrivals[t] = found[t] + r * fixed[t-1]   (no regressions on day 1)
    fixed[t]    = min(capacity, B[t-1] + arrivals[t])
    B[t]        = B[t-1] + arrivals[t] - fixed[t]

    Return a list with one float per day in `found` (day 0 is not included).
    """
    raise NotImplementedError("TODO: backlog")


def peak_days(open_counts):
    """Return every 1-based day on which open_counts reaches its maximum."""
    raise NotImplementedError("TODO: peak_days")


def zero_day(open_counts):
    """Return the first 1-based day with no open bugs, or None."""
    raise NotImplementedError("TODO: zero_day")


def lincoln_petersen(a_ids, b_ids):
    """Estimate the total number of findable bugs from two testers' lists.

    N = a * b / m, where a and b are the numbers of distinct ids on each
    list and m is the number on both. Raise ValueError when m is 0.
    """
    raise NotImplementedError("TODO: lincoln_petersen")


def ship_blockers(bugs):
    """Return the ids of bugs that block release, sorted.

    A bug blocks release when its status is not 'closed' or 'wontfix'
    and its priority is 1 or 2.
    """
    raise NotImplementedError("TODO: ship_blockers")
