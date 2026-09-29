"""MMO308 Lab 08 starter: measure an event's net lift and plan event spacing.

Standard library only. Fill in every function marked TODO, then run
    .venv/bin/python courses/MMO308-live-operations-analytics-and-experimentation/labs/lab08-starter/test_event_lift.py
from the repository root.

The data in daily_hours.csv is synthetic: 120 days of player-hours, day 0 is a
Monday. The event was announced on day 70, ran on days 84-93 and players
settled back to normal by day 108. Ranges below are Python-style
(start inclusive, end exclusive).
"""
import csv
import math
import statistics
from pathlib import Path

DATA = Path(__file__).with_name("daily_hours.csv")
ANNOUNCE, START, END, SETTLED = 70, 84, 94, 108
PRE = (ANNOUNCE, START)
EVENT = (START, END)
POST = (END, SETTLED)
CLEAN = (42, 70)          # four clean weeks before the announcement


def load_hours(path=DATA):
    """Return the player_hours column as a list of ints, index = day. Provided."""
    with open(path, newline="") as fh:
        return [int(r["player_hours"]) for r in csv.DictReader(fh)]


def weekday_medians(series, clean):
    """Median of series over the clean range, separately for each weekday.
    Return a list of 7 values where index k is weekday k (day % 7 == k). TODO"""
    raise NotImplementedError


def baseline_series(medians, n_days):
    """Baseline for days 0..n_days-1: the weekday median for each day. TODO"""
    raise NotImplementedError


def flat_baseline(series, start, end):
    """A constant baseline equal to the mean of series[start:end], repeated
    for every day of the series. This is the 'week before' shortcut. TODO"""
    raise NotImplementedError


def lift_summary(actual, baseline, pre, event, post):
    """Return a dict with keys gross, borrowed, net and ratio.

    gross    = sum of (actual - baseline) over the event range
    borrowed = sum of (baseline - actual) over the pre and post ranges
    net      = gross - borrowed
    ratio    = net / gross (0.0 if gross == 0)
    Each range is a (start, end) pair. TODO"""
    raise NotImplementedError


def recovery_lift(gap, l_max, tau):
    """Lift of an event held `gap` days after the last one:
    l_max * (1 - exp(-gap / tau)). TODO"""
    raise NotImplementedError


def yearly_lift_days(gap, l_max, tau, length):
    """Gross lift-days per year: (365 / gap) * recovery_lift(...) * length. TODO"""
    raise NotImplementedError


if __name__ == "__main__":
    hours = load_hours()
    base = baseline_series(weekday_medians(hours, CLEAN), len(hours))
    print(lift_summary(hours, base, PRE, EVENT, POST))
