"""Tests for MMO308 Lab 07. Values come from the week 7 lecture and new_players.csv.

Run with `.venv/bin/python test_segments.py` (exits 1 while any test fails)
or with pytest if you have it.
"""
import sys

from segments import (decompose, load_players, margin95, overall, rate,
                      segment_table, shares, week)

TOL = 1e-9
LECTURE_BEFORE = {"paid": (9_000, 0.40), "free": (1_000, 0.15)}
LECTURE_AFTER = {"paid": (6_000, 0.42), "free": (24_000, 0.18)}


def close(a, b, tol=1e-6):
    return abs(a - b) < tol


def test_rate():
    rows = [{"retained_d7": 1}, {"retained_d7": 0}, {"retained_d7": 0}, {"retained_d7": 1}]
    assert close(rate(rows), 0.5)
    assert rate([]) == 0.0


def test_shares_and_overall():
    s = shares(LECTURE_BEFORE)
    assert close(s["paid"][0], 0.9) and close(s["free"][0], 0.1)
    assert close(overall(LECTURE_BEFORE), 0.375)
    assert close(overall(LECTURE_AFTER), 0.228)


def test_lecture_decomposition():
    mix, r = decompose(LECTURE_BEFORE, LECTURE_AFTER)
    assert close(mix, -0.175) and close(r, 0.028)
    mix, r = decompose(LECTURE_BEFORE, LECTURE_AFTER, "new")
    assert close(mix, -0.168) and close(r, 0.021)
    mix, r = decompose(LECTURE_BEFORE, LECTURE_AFTER, "midpoint")
    assert close(mix, -0.1715) and close(r, 0.0245)


def test_decomposition_is_exact():
    for ordering in ("old", "new", "midpoint"):
        mix, r = decompose(LECTURE_BEFORE, LECTURE_AFTER, ordering)
        assert close(mix + r, overall(LECTURE_AFTER) - overall(LECTURE_BEFORE), TOL)


def test_margin():
    assert close(margin95(0.24, 250), 0.05294, 1e-4)
    assert close(margin95(0.18, 24_000), 0.00486, 1e-4)


def test_csv_tables():
    players = load_players()
    assert len(players) == 8_000
    w0, w1 = week(players, 0), week(players, 1)
    assert close(rate(w0), 0.375) and close(rate(w1), 0.232)
    acc1 = segment_table(w1, "account")
    assert acc1["free"][0] == 4_800 and close(acc1["free"][1], 0.185)
    cell = segment_table(w1, ("account", "region"))
    assert cell[("free", "ASIA")] == (720, 0.1)


def test_csv_decomposition():
    players = load_players()
    b = segment_table(week(players, 0), "account")
    a = segment_table(week(players, 1), "account")
    mix, r = decompose(b, a)
    assert close(mix, -0.175) and close(r, 0.032)


TESTS = [test_rate, test_shares_and_overall, test_lecture_decomposition,
         test_decomposition_is_exact, test_margin, test_csv_tables, test_csv_decomposition]

if __name__ == "__main__":
    failed = 0
    for t in TESTS:
        try:
            t()
            print(f"PASS {t.__name__}")
        except Exception as e:  # NotImplementedError, AssertionError, KeyError ...
            failed += 1
            print(f"FAIL {t.__name__}: {type(e).__name__} {e}")
    print(f"{len(TESTS) - failed}/{len(TESTS)} passed")
    sys.exit(1 if failed else 0)
