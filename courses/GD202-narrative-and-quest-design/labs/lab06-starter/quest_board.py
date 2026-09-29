"""GD202 Lab 06 starter: the detour test for a whole quest board.

Standard library only. Fill in the five TODO functions, then run the tests:

    .venv/bin/python courses/GD202-narrative-and-quest-design/labs/lab06-starter/test_quest_board.py

Model (week 6, section 2):
    paid   = listed XP x m(delta), rounded to the nearest 5 (halves round up)
    time   = travel x travel_factor + task + complication
    rate   = paid / time
    passes if rate >= baseline
m(delta) is 100% for delta <= 5, then 80, 60, 40, 20% for delta 6..9,
and 10% for delta >= 10 (classic-era World of Warcraft, community-measured).
Work in integers where you can: percent, not 0.8.
"""
import csv
import os
from dataclasses import dataclass

HERE = os.path.dirname(os.path.abspath(__file__))


@dataclass
class Quest:
    name: str
    level: int
    xp: int               # listed (full) XP
    travel: float         # minutes to get there and back
    task: float           # minutes to do the objective
    complication: float = 0.0  # extra minutes added by a complication


def load_board(path=os.path.join(HERE, "board.csv")):
    with open(path, newline="") as f:
        return [Quest(r["name"], int(r["level"]), int(r["xp"]), float(r["travel"]),
                      float(r["task"]), float(r.get("complication") or 0))
                for r in csv.DictReader(f)]


def decay_percent(delta):
    """TODO 1. Percent of listed XP paid when the player is `delta` levels
    above the quest (delta may be zero or negative)."""
    raise NotImplementedError("decay_percent() is yours to write")


def paid_xp(quest, player_level):
    """TODO 2. XP actually paid, rounded to the nearest 5 with halves up.
    Hint: (xp * pct + 250) // 500 * 5 does this in integers."""
    raise NotImplementedError("paid_xp() is yours to write")


def minutes(quest, travel_factor=1.0):
    """TODO 3. Total minutes: travel * travel_factor + task + complication."""
    raise NotImplementedError("minutes() is yours to write")


def rate(quest, player_level, travel_factor=1.0):
    """TODO 4. Paid XP per minute."""
    raise NotImplementedError("rate() is yours to write")


def required_listed_xp(quest, player_level, baseline, travel_factor=1.0):
    """TODO 5. Smallest listed XP, a multiple of 5, whose paid XP gives a
    rate of at least `baseline`. Search upward in steps of 5 from 0, or
    solve and then check; the test values assume the paid-XP rounding above."""
    raise NotImplementedError("required_listed_xp() is yours to write")


def audit(board, player_level, baseline, travel_factor=1.0):
    """Print the board as the lecture does, sorted by listed XP. Given."""
    print(f"{'quest':24} {'XP paid':>7} {'min':>5} {'XP/min':>7}  pass")
    for q in sorted(board, key=lambda q: -q.xp):
        r = rate(q, player_level, travel_factor)
        print(f"{q.name:24} {paid_xp(q, player_level):7} {minutes(q, travel_factor):5.1f} "
              f"{r:7.1f}  {'yes' if r >= baseline else 'no'}")


if __name__ == "__main__":
    try:
        audit(load_board(), player_level=20, baseline=200)
    except NotImplementedError as e:
        raise SystemExit(f"Not finished yet: {e}. Run test_quest_board.py to see what is left.")
