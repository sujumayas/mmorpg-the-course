"""MMO405 lab 03: from an event log to hours played, and a self-report audit.

Python 3.10+, standard library only. Fill in the three TODOs, then run
    python -m unittest test_telemetry.py
from inside this folder (from the repository root, .venv/bin/python is the course Python).
Running this file directly prints the report once the TODOs are done.
"""
import csv
from math import sqrt
from pathlib import Path
from statistics import correlation, mean

HERE = Path(__file__).parent


def load_events(path=HERE / "events.csv"):
    """Return {account_id: [(minute, type), ...]} with each list sorted by minute."""
    out = {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            out.setdefault(r["account_id"], []).append((int(r["minute"]), r["type"]))
    for evs in out.values():
        evs.sort()
    return out


def load_survey(path=HERE / "survey.csv"):
    """Return {account_id: (reported_hours, satisfaction)}."""
    with open(path, newline="") as f:
        return {r["account_id"]: (float(r["reported_hours"]), int(r["satisfaction"]))
                for r in csv.DictReader(f)}


def login_logout_hours(events):
    """Hours from each login to the next logout. Given, as a model for TODO 1.

    `events` is one account's sorted list of (minute, type). A login with no
    later logout is ignored.
    """
    total, start = 0, None
    for minute, kind in events:
        if kind == "login":
            start = minute
        elif kind == "logout" and start is not None:
            total += minute - start
            start = None
    return total / 60


def sessionize(events, gap):
    """TODO 1. Activity sessions for one account.

    Use only events of type "activity". Consecutive activity events belong to
    the same session when the time between them is at most `gap` minutes; a
    longer gap starts a new session. Return a list of (start, end) minute pairs,
    where start is the first and end the last activity event of the session.
    A session with a single event has start == end.
    """
    raise NotImplementedError("TODO 1")


def hours_by_account(all_events, gap, accounts=None):
    """TODO 2. Activity hours per account under a gap rule.

    Sum (end - start) over each account's sessions and convert to hours.
    If `accounts` is given, return a value for every account in it, with 0.0
    for accounts that have no events. Otherwise return one per account in all_events.
    """
    raise NotImplementedError("TODO 2")


def corrected_r(r_sy, r_sx, rel_y=1.0):
    """TODO 3. Spearman's correction for attenuation.

    r_sx is the correlation between the self-report and the logs, so the
    self-report's reliability is r_sx ** 2. Return r_sy / sqrt(r_sx**2 * rel_y).
    """
    raise NotImplementedError("TODO 3")


if __name__ == "__main__":
    ev = load_events()
    sv = load_survey()
    players = sorted(sv)                      # the 300 surveyed accounts; bots are not in it
    said = [sv[a][0] for a in players]
    sat = [sv[a][1] for a in players]
    print(f"accounts in log: {len(ev)}   surveyed: {len(players)}")
    rules = {"login-logout": {a: login_logout_hours(ev.get(a, [])) for a in players}}
    for g in (10, 30):
        rules[f"activity, gap {g}"] = hours_by_account(ev, g, players)
    for name, h in rules.items():
        logged = [h[a] for a in players]
        r_sx = correlation(said, logged)
        r_sy = correlation(said, sat)
        print(f"{name:>16}: mean {mean(logged):5.2f} h   r(said, logged)={r_sx:.3f}   "
              f"r(logged, satisfaction)={correlation(logged, sat):.3f}   "
              f"corrected from self-report={corrected_r(r_sy, r_sx):.3f}")
    print(f"r(said, satisfaction)={correlation(said, sat):.3f}   mean said {mean(said):.2f} h")
