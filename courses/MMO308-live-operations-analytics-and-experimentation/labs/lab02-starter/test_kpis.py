"""Tests for MMO308 Lab 02. Values come from the week 2 lecture.
Run `python gen_activity.py` once, then `python test_kpis.py`."""
from pathlib import Path

from kpis import (dau_series, kpi_tree, load_activity, load_payments, month_model,
                  regulars, revenue_factors, rolling_mau, window_mau)

HERE = Path(__file__).resolve().parent


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# a tiny log: A plays days 0-3, B days 0 and 2, C only day 1, D only day 5
TINY = {0: {"A", "B"}, 1: {"A", "C"}, 2: {"A", "B"}, 3: {"A"}, 5: {"D"}}
TINY_PAY = [(0, "A", 10.0), (0, "A", 5.0), (2, "B", 4.0), (5, "D", 1.0)]


def test_month_model_lecture_values():
    m = month_model(1_100_000, 0.40, 700_000, 2)
    assert m["mau"] == 1_800_000
    assert close(m["player_days"], 14_600_000)
    assert round(m["mean_dau"]) == 486_667
    assert abs(m["stickiness"] - 0.2704) < 1e-4
    b = month_model(1_000_000, 0.40, 200_000, 2)
    assert round(b["mean_dau"]) == 413_333 and abs(b["stickiness"] - 0.3444) < 1e-4


def test_dau_and_windows():
    assert dau_series(TINY, 0, 5) == [2, 2, 2, 1, 0, 1]
    assert window_mau(TINY, 0, 3) == 3
    assert window_mau(TINY, 0, 5) == 4
    assert rolling_mau(TINY, 3, window=2) == 2      # days 2-3: A, B
    assert rolling_mau(TINY, 5, window=3) == 2      # days 3-5: A, D


def test_regulars():
    assert regulars(TINY, 3, min_days=2, window=4) == 2   # A (4 days), B (2 days)
    assert regulars(TINY, 3, min_days=3, window=4) == 1


def test_kpi_tree_identities():
    t = kpi_tree(TINY, TINY_PAY, 0, 3)
    assert t["days"] == 4 and t["player_days"] == 7 and t["mau"] == 3
    assert close(t["mean_dau"], 1.75) and close(t["stickiness"], 1.75 / 3)
    assert close(t["revenue"], 19.0) and t["payer_days"] == 2
    assert close(t["arpdau"], 19 / 7) and close(t["arppu"], 9.5)
    assert close(t["payer_rate"], 2 / 7)
    assert close(t["arpdau"], t["payer_rate"] * t["arppu"])
    assert close(t["revenue_per_day"], t["mean_dau"] * t["arpdau"])


def test_rolling_echo():
    # 100 regulars every day, 50 tourists on day 0 only
    log = {d: {f"R{i}" for i in range(100)} for d in range(-5, 40)}
    log[0] = log[0] | {f"T{i}" for i in range(50)}
    assert rolling_mau(log, 29) == 150
    assert rolling_mau(log, 30) == 100


def test_revenue_factors():
    t0 = {"mean_dau": 200_000.0, "arpdau": 0.25, "revenue_per_day": 50_000.0}
    t1 = {"mean_dau": 240_000.0, "arpdau": 0.225, "revenue_per_day": 54_000.0}
    d, a, r = revenue_factors(t0, t1)
    assert close(d, 1.2) and close(a, 0.9) and close(r, 1.08) and close(d * a, r)


def test_generated_data():
    if not (HERE / "activity.csv").exists():
        raise AssertionError("run gen_activity.py first")
    act, pay = load_activity(), load_payments()
    for a, b in ((0, 29), (30, 59), (60, 89)):
        t = kpi_tree(act, pay, a, b)
        assert close(t["player_days"], sum(dau_series(act, a, b)))
        assert close(t["revenue_per_day"], t["mean_dau"] * t["arpdau"], 1e-9)
        assert t["mau"] == window_mau(act, a, b)
    assert rolling_mau(act, 69) > rolling_mau(act, 71)   # the free weekend leaves the window


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS {name}")
            except NotImplementedError as e:
                failed += 1
                print(f"TODO {name}: {e}")
            except AssertionError as e:
                failed += 1
                print(f"FAIL {name} {e}")
    print("all tests pass" if not failed else f"{failed} test(s) not passing yet")
    raise SystemExit(1 if failed else 0)
