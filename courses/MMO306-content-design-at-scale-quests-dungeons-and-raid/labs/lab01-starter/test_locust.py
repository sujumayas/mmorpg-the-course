"""Tests for Lab 01. Values come from the week 1 lecture and from players.csv.
Run with ../../../../.venv/bin/python test_locust.py (or pytest)."""
from locust import (cheapest_plan, drought_days, exhaust_days, load_hours, locust_ratio,
                    percentile, share_with_content)

HOURS = load_hours()
OPTS = ([10, 15, 20, 25, 30, 40], [1, 2, 3, 4, 5, 6, 8, 10], [None, 30, 20, 15, 12, 10, 8])


def close(a, b, tol=1e-6):
    return abs(a - b) < tol


def test_lecture_table():
    # Design A, B and C from section 2 of the lecture (C = 20, P = 175).
    assert close(exhaust_days(20, 1, 6), 23.333333, 1e-5)
    assert close(locust_ratio(175, 20, 1, 60), 75.0)
    assert close(exhaust_days(20, 6, 34), 24.705882, 1e-5)
    assert close(exhaust_days(20, 6, 60, gate=12), 70.0)
    assert close(exhaust_days(20, 6, 6, gate=12), 140.0)   # gate above h changes nothing
    assert close(drought_days(175, 20, 6, 6), 35.0)
    assert drought_days(175, 40, 6, 6) == 0                 # outlasts the cycle


def test_percentile():
    assert percentile([4, 1, 3, 2], 0.5) == 2
    assert percentile([4, 1, 3, 2], 0.75) == 3
    assert percentile([4, 1, 3, 2], 1.0) == 4
    assert close(percentile(HOURS, 0.5), 6.0)
    assert close(percentile(HOURS, 0.99), 34.8)


def test_share_with_content():
    assert share_with_content(HOURS, 0, 20, 6) == 1.0
    assert close(share_with_content(HOURS, 30, 20, 6), 0.984)
    assert close(share_with_content(HOURS, 30, 20, 6, gate=12), 1.0)
    assert close(share_with_content(HOURS, 90, 20, 6), 0.7255)
    assert close(share_with_content(HOURS, 150, 20, 6), 0.465)


def test_cheapest_plan():
    assert cheapest_plan(HOURS, 175, *OPTS) == (115.0, 25, 6, 15)
    assert cheapest_plan(HOURS, 175, OPTS[0], OPTS[1], [None]) == (162.0, 30, 10, None)
    assert cheapest_plan(HOURS, 175, *OPTS, p99_max_ratio=1.5) == (115.0, 25, 6, 8)
    assert cheapest_plan(HOURS, 175, [5], [1], [None]) is None


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print("PASS", name)
            except Exception as e:  # noqa: BLE001
                failed += 1
                print("FAIL", name, type(e).__name__, e)
    raise SystemExit(1 if failed else 0)
