"""Tests for Lab 06. Values come from the week 6 lecture.
Run with `python test_catchup.py` or `pytest test_catchup.py`."""
import math

from catchup import (Rule, allowance, catch_up_week, finish_week, free_window, population,
                     simulate)

N, L = 9_000, 750


def test_allowance():
    assert allowance(4, Rule(L=750)) == 3_000
    assert allowance(4, Rule(L=750, head_start=750)) == 3_750
    r = Rule(L=550, raise_at=10, L2=1_100)
    assert allowance(10, r) == 5_500 and allowance(12, r) == 7_700
    assert allowance(9, Rule(L=100, remove_at=8)) == math.inf


def test_lecture_table():
    roll = simulate(Rule(L=L), 6, 1_500, N, 18)
    week = simulate(Rule(L=L, rolling=False), 6, 1_500, N, 18)
    assert [roll[w] for w in (6, 7, 8, 10, 12)] == [0, 1_500, 3_000, 6_000, 9_000]
    assert [week[w] for w in (7, 8, 10, 12, 14, 18)] == [750, 1_500, 3_000, 4_500, 6_000, 9_000]
    assert finish_week(roll, N) == 12 and finish_week(week, N) == 18


def test_speed_table():
    assert catch_up_week(6, 1_000, L) == 24
    assert catch_up_week(6, 1_500, L) == 12
    assert catch_up_week(6, 750, L) == math.inf
    finishes = [finish_week(simulate(Rule(L=L), 6, v, N, 30), N) for v in (1_000, 1_125, 1_500, 3_000)]
    assert finishes == [15, 14, 12, 12]


def test_free_window():
    assert free_window(N, L, 1_500) == 6
    assert free_window(N, L, 3_000) == 9
    assert free_window(N, L, 500) == 0
    assert free_window(7_200, 600, 1_800) == 8


def test_levers():
    # Check yourself 5: cap removed after week 8, heavy veteran at 3,000 per week.
    heavy = simulate(Rule(L=L, remove_at=8), 0, 3_000, N, 14)
    assert heavy[8] == 6_000 and finish_week(heavy, N) == 9
    light = simulate(Rule(L=L, remove_at=8), 0, 750, N, 14)
    assert finish_week(light, N) == 12
    # Raising L after week 10 to 1,500: capped heavy veteran finishes in week 11.
    raised = simulate(Rule(L=L, raise_at=10, L2=1_500), 0, 1_500, N, 14)
    assert raised[10] == 7_500 and finish_week(raised, N) == 11
    # Weekly base rule, cap removed after week 8, late player j = 6 at 1,500.
    late = simulate(Rule(L=L, rolling=False, remove_at=8), 6, 1_500, N, 16)
    assert late[8] == 1_500 and finish_week(late, N) == 13


def test_population():
    a = population(1_000, 7, 10, [500, 750, 1_500, 3_000])
    assert a == population(1_000, 7, 10, [500, 750, 1_500, 3_000])
    assert all(0 <= j <= 10 for j, _ in a) and {v for _, v in a} == {500, 750, 1_500, 3_000}


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
            except AssertionError:
                failed += 1
                print(f"FAIL {name}")
    print("all tests pass" if not failed else f"{failed} test(s) not passing yet")
    raise SystemExit(1 if failed else 0)
