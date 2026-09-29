"""Tests for Lab 09. Values come from the week 9 lecture and its interactive spec.
Run with ../../../../.venv/bin/python test_realm_clock.py (or pytest)."""
from realm_clock import (ceiling_per_player, daily_rate, finish_day, largest_g, load_realms, plan,
                         simulate)

SIZES = [1500, 3000, 6000, 12000]


def close(x, y, tol=1e-3):
    return abs(x - y) < tol


def test_rate_and_finish_no_fatigue():
    assert daily_rate(1500, 0.2, 10) == 3000
    assert [finish_day(300_000, daily_rate(n, 0.2, 10)) for n in SIZES] == [100, 50, 25, 13]
    assert [finish_day(50 * n, daily_rate(n, 0.2, 10)) for n in SIZES] == [25] * 4


def test_finish_with_fatigue():
    assert [finish_day(300_000, 2 * n, 0.97) for n in SIZES] == [None, None, 46, 16]
    assert [finish_day(50 * n, 2 * n, 0.97) for n in SIZES] == [46] * 4
    assert [finish_day(45 * n, 2 * n, 0.97) for n in SIZES] == [37] * 4
    assert finish_day(200_000, 8000, 0.95) is None


def test_ceiling_and_largest_g():
    assert close(ceiling_per_player(0.2, 10, 0.97), 66.667)
    assert close(largest_g(0.2, 10, 0.97, 42), 48.118)
    assert close(largest_g(0.25, 8, 0.95, 30), 31.414)
    assert close(largest_g(0.25, 6, 1.0, 30), 45.0)


def test_simulate_matches_formula():
    for n in SIZES:
        for goal, d in ((300_000, 1.0), (300_000, 0.97), (45 * n, 0.97)):
            assert simulate(n, 0.2, 10, goal, d) == finish_day(goal, 2 * n, d), (n, goal, d)


def test_discouragement_loop():
    assert simulate(3000, 0.2, 10, 150_000, target_day=24) == 25
    assert simulate(3000, 0.2, 10, 150_000, target_day=18, penalty=0.98) == 35
    assert simulate(3000, 0.2, 10, 300_000, target_day=30) is None
    assert simulate(12000, 0.2, 10, 300_000, 0.97, target_day=30) == 16


def test_plan():
    realms = load_realms()
    assert realms[0] == ("Small", 1500) and len(realms) == 4
    got = plan(realms, 0.2, 10, 1.0, "fixed", 300_000, 14, 42)
    assert got == {"Small": (100, "late"), "Medium": (50, "late"), "Large": (25, "ok"),
                   "Huge": (13, "early")}
    got = plan(realms, 0.2, 10, 0.97, "fixed", 300_000, 14, 42)
    assert got["Small"] == (None, "never") and got["Huge"] == (16, "ok")
    assert set(plan(realms, 0.2, 10, 0.97, "scaled", 45, 14, 42).values()) == {(37, "ok")}


if __name__ == "__main__":
    import sys
    failed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("PASS", name)
            except Exception as e:  # noqa: BLE001
                failed += 1
                print("FAIL", name, type(e).__name__, e)
    print(f"{failed} failed")
    sys.exit(1 if failed else 0)
