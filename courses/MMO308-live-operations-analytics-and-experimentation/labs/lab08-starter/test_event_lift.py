"""Tests for MMO308 Lab 08. Values come from the week 8 lecture and daily_hours.csv.

Run with `.venv/bin/python test_event_lift.py` (exits 1 while any test fails)
or with pytest if you have it.
"""
import sys

from event_lift import (CLEAN, EVENT, POST, PRE, baseline_series, flat_baseline,
                        lift_summary, load_hours, recovery_lift, weekday_medians,
                        yearly_lift_days)


def close(a, b, tol=1e-6):
    return abs(a - b) < tol


def lecture_series():
    """The lecture's flat example: 14 pre days, 10 event days, 14 post days."""
    B = 10_000
    actual = [B * 0.90] * 14 + [B * 1.60] * 10 + [B * 0.85] * 14
    return actual, [B] * 38


def test_lecture_lift():
    actual, base = lecture_series()
    s = lift_summary(actual, base, (0, 14), (14, 24), (24, 38))
    assert close(s["gross"], 60_000) and close(s["borrowed"], 35_000)
    assert close(s["net"], 25_000) and close(s["ratio"], 25 / 60)


def test_lecture_week_before():
    actual, _ = lecture_series()
    fb = flat_baseline(actual, 7, 14)
    assert len(fb) == 38 and close(fb[0], 9_000)
    s = lift_summary(actual, fb, (0, 14), (14, 24), (24, 38))
    assert close(s["gross"], 70_000)


def test_zero_gross():
    s = lift_summary([5, 5, 5], [5, 5, 5], (0, 1), (1, 2), (2, 3))
    assert s["ratio"] == 0.0


def test_recovery_table():
    expected = {30: (0.379, 46.1), 45: (0.466, 37.8), 60: (0.519, 31.6),
                90: (0.570, 23.1), 120: (0.589, 17.9)}
    for g, (lift, days) in expected.items():
        assert close(recovery_lift(g, 0.6, 30), lift, 5e-4)
        assert close(yearly_lift_days(g, 0.6, 30, 10), days, 0.05)


def test_csv_baseline():
    hours = load_hours()
    assert len(hours) == 120
    med = weekday_medians(hours, CLEAN)
    assert med == [10065.5, 9442.0, 9414.5, 10216.5, 10975.5, 12529.5, 11773.0]
    base = baseline_series(med, 120)
    assert base[84] == med[0] and base[89] == med[5]


def test_csv_lift():
    hours = load_hours()
    base = baseline_series(weekday_medians(hours, CLEAN), 120)
    s = lift_summary(hours, base, PRE, EVENT, POST)
    assert close(s["gross"], 55_311.5) and close(s["borrowed"], 29_978)
    assert close(s["net"], 25_333.5) and close(s["ratio"], 0.4580, 1e-4)


def test_csv_contaminated():
    hours = load_hours()
    s = lift_summary(hours, flat_baseline(hours, 77, 84), PRE, EVENT, POST)
    assert close(s["gross"], 61_355.714, 1e-2)


TESTS = [test_lecture_lift, test_lecture_week_before, test_zero_gross,
         test_recovery_table, test_csv_baseline, test_csv_lift, test_csv_contaminated]

if __name__ == "__main__":
    failed = 0
    for t in TESTS:
        try:
            t()
            print(f"PASS {t.__name__}")
        except Exception as e:  # NotImplementedError, AssertionError, ...
            failed += 1
            print(f"FAIL {t.__name__}: {type(e).__name__} {e}")
    print(f"{len(TESTS) - failed}/{len(TESTS)} passed")
    sys.exit(1 if failed else 0)
