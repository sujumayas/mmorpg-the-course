"""MMO308 Lab 07 starter: segment a retention drop into mix and rate effects.

Standard library only. Fill in every function marked TODO, then run
    .venv/bin/python courses/MMO308-live-operations-analytics-and-experimentation/labs/lab07-starter/test_segments.py
from the repository root. The tests use the week 7 lecture's numbers and the
provided new_players.csv.

Conventions used by the tests:
- A "table" maps a segment name (or a tuple of names) to (n, rate), where n is
  the number of players and rate is the share of them retained at D7.
- A "shares" dict maps the same keys to (w, rate), where w is n / total.
"""
import csv
import math
from pathlib import Path

DATA = Path(__file__).with_name("new_players.csv")


def load_players(path=DATA):
    """Return a list of dicts with keys player_id, install_week (int),
    account, region and retained_d7 (int 0 or 1). Provided."""
    with open(path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        r["install_week"] = int(r["install_week"])
        r["retained_d7"] = int(r["retained_d7"])
    return rows


def week(rows, w):
    """Rows for install week w. Provided."""
    return [r for r in rows if r["install_week"] == w]


def rate(rows):
    """Share of rows with retained_d7 == 1. Return 0.0 for an empty list.
    TODO"""
    raise NotImplementedError


def segment_table(rows, key):
    """Group rows by r[key] and return {segment: (n, rate)}.
    If key is a tuple of column names, the segment is a tuple of values,
    for example ("free", "ASIA"). TODO"""
    raise NotImplementedError


def shares(table):
    """Turn {seg: (n, rate)} into {seg: (w, rate)} with w = n / total. TODO"""
    raise NotImplementedError


def overall(table):
    """Overall rate from a segment table (the weighted mean). TODO"""
    raise NotImplementedError


def decompose(before, after, ordering="old"):
    """Split overall(after) - overall(before) into (mix, rate_effect).

    before and after are segment tables with the same keys.
    ordering="old":      mix at old rates, rate effect at new shares (lecture default)
    ordering="new":      mix at new rates, rate effect at old shares
    ordering="midpoint": the average of the two orderings
    mix + rate_effect must equal the total change in every ordering. TODO"""
    raise NotImplementedError


def margin95(m, n):
    """95% margin of error of a rate m measured on n players,
    1.96 * sqrt(m (1 - m) / n), as in MA102 week 13. TODO"""
    raise NotImplementedError


if __name__ == "__main__":
    players = load_players()
    print(f"{len(players)} players loaded")
    for w in (0, 1):
        print(f"week {w}:", segment_table(week(players, w), "account"))
