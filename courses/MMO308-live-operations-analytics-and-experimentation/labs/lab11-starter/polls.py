"""Lab 11: the poll archive.

osrs_polls.csv has one row per yes/no question from Old School RuneScape polls,
14 March 2013 to 21 September 2026: opened (ISO date the poll opened), poll, yes, no,
skip, question. Vote counts come from the Old School RuneScape Wiki's poll pages
(CC BY-NC-SA 3.0), tallied for this course in September 2026.

Thresholds are whole percentages (70 means 70%). Use integer arithmetic for pass and
fail so a question sitting exactly on the line is decided correctly.
Fill in the five functions marked TODO (lecture week 11, section 2). Standard-library only.

    ../../../../.venv/bin/python polls.py
"""
import csv

CHANGE_DATE = "2022-10-27"  # threshold lowered from 75% to 70%


def read_polls(path="osrs_polls.csv"):
    with open(path, newline="", encoding="utf-8") as f:
        return [dict(opened=r["opened"], poll=r["poll"], yes=int(r["yes"]), no=int(r["no"]),
                     skip=int(r["skip"]), question=r["question"]) for r in csv.DictReader(f)]


def yes_share(yes, no):
    """Yes votes as a share of yes + no (skips excluded), as a float between 0 and 1."""
    # TODO
    raise NotImplementedError


def passes(yes, no, t_pct):
    """True if yes / (yes + no) >= t_pct / 100. Integer arithmetic only."""
    # TODO
    raise NotImplementedError


def no_votes_to_block(yes, t_pct):
    """Smallest number of 'no' votes that makes a question with `yes` votes fail at t_pct."""
    # TODO
    raise NotImplementedError


def in_period(rows, start=None, end=None):
    """Rows whose opened date is >= start (if given) and < end (if given). ISO strings compare correctly."""
    return [r for r in rows if (start is None or r["opened"] >= start) and (end is None or r["opened"] < end)]


def pass_count(rows, t_pct):
    """Number of rows that pass at t_pct."""
    # TODO
    raise NotImplementedError


def flipped(rows, t_low, t_high):
    """Rows that pass at t_low but fail at t_high (t_low < t_high)."""
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    rows = read_polls()
    before, after = in_period(rows, end=CHANGE_DATE), in_period(rows, start=CHANGE_DATE)
    print(f"questions {len(rows)}: {len(before)} before {CHANGE_DATE}, {len(after)} from it")
    for t in (50, 60, 70, 75, 80, 90):
        print(f"pass at {t}%: {pass_count(rows, t):5d} ({pass_count(rows, t) / len(rows):.1%})")
    print(f"pass at 70 but not 75: before {len(flipped(before, 70, 75))}, after {len(flipped(after, 70, 75))}")
    print(f"Sailing blocks at {no_votes_to_block(112_976, 70):,} no votes (70%)")
