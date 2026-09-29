"""MMO306 Lab 01 starter: content locust math. Standard library only.

Fill in the TODO functions, then run the tests from this folder:

    ../../../../.venv/bin/python test_locust.py

Notation follows the week 1 lecture.
    C      content hours in one pass of the drop
    r      replay multiplier (hours played per hour of first-pass content)
    h      a player's hours of play per week
    gate   weekly gate g in hours, or None for no gate
    P      cadence, days until the next drop
"""
import csv
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load_hours(path=os.path.join(HERE, "players.csv")):
    """Weekly hours for every player in players.csv, as a list of floats."""
    with open(path, newline="") as f:
        return [float(row["hours_per_week"]) for row in csv.DictReader(f)]


def exhaust_days(C, r, h, gate=None):
    """TODO step 1. T = 7 x C x r / min(h, gate). With gate None, use h."""
    raise NotImplementedError("exhaust_days() is yours to write")


def locust_ratio(P, C, r, h, gate=None):
    """TODO step 1. L = P / T."""
    raise NotImplementedError("locust_ratio() is yours to write")


def drought_days(P, C, r, h, gate=None):
    """TODO step 1. D = max(0, P - T)."""
    raise NotImplementedError("drought_days() is yours to write")


def percentile(values, p):
    """TODO step 2. Nearest-rank percentile, p between 0 and 1 (exclusive of 0).
    Sort the values and return the item at index ceil(p x n) - 1.
    Example: percentile([4, 1, 3, 2], 0.5) == 2."""
    raise NotImplementedError("percentile() is yours to write")


def share_with_content(hours, t, C, r, gate=None):
    """TODO step 3. Share of players (0 to 1) whose T is strictly greater than t.
    On day 0 every player has content, so return 1.0 for t <= 0."""
    raise NotImplementedError("share_with_content() is yours to write")


def plan_cost(C, r, cost_per_hour=3.0, cost_per_replay=8.0):
    """Production cost of a plan in team-weeks: every content hour costs
    cost_per_hour, and every step of replay above 1 costs cost_per_replay.
    Gates are treated as free to build (their cost is to players, not the team)."""
    return C * cost_per_hour + (r - 1) * cost_per_replay


def cheapest_plan(hours, P, C_options, r_options, gate_options,
                  p99_max_ratio=3.0):
    """TODO step 4. Search every (C, r, gate) combination and return the cheapest
    one, as a tuple (cost, C, r, gate), that meets all three rules:
      1. the median player (percentile 0.5) has L <= 1,
      2. the p99 player (percentile 0.99) has L <= p99_max_ratio,
      3. the gate does not bind the median player (gate is None or gate >= median hours).
    Break cost ties by preferring gate None, then the larger gate, then smaller C.
    Return None if no plan meets the rules."""
    raise NotImplementedError("cheapest_plan() is yours to write")


if __name__ == "__main__":
    hours = load_hours()
    P, C = 175, 20
    for p in (0.5, 0.75, 0.9, 0.99, 0.999):
        h = percentile(hours, p)
        print(f"p{p * 100:g}: {h:5.1f} h/wk  T={exhaust_days(C, 6, h):6.1f} d  "
              f"L={locust_ratio(P, C, 6, h):5.2f}")
    for day in (30, 90, 150):
        print(f"day {day}: {share_with_content(hours, day, C, 6):.1%} still have content")
    print("cheapest plan:", cheapest_plan(hours, P, [10, 15, 20, 25, 30, 40],
                                          [1, 2, 3, 4, 5, 6, 8, 10],
                                          [None, 30, 20, 15, 12, 10, 8]))
