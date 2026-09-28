"""Tests for Lab 08, from the week 8 lecture.
Run with `python3 test_cc_planner.py` or `pytest test_cc_planner.py`."""
from cc_planner import RULE_A, back_to_back, simulate, total_control, uptime_ceiling


def near(a, b, tol=1e-9):
    return abs(a - b) <= tol


def test_three_six_second_stuns():
    eff = simulate(back_to_back([6, 6, 6]), RULE_A)
    assert [e["multiplier"] for e in eff] == [1, 0.5, 0.25]
    assert near(total_control(eff), 10.5)


def test_fourth_is_immune():
    eff = simulate(back_to_back([6, 6, 6, 6]), RULE_A)
    assert eff[-1]["multiplier"] == 0
    assert near(total_control(eff), 10.5)


def test_order_matters():
    assert near(total_control(simulate(back_to_back([6, 4, 3]), RULE_A)), 8.75)
    assert near(total_control(simulate(back_to_back([3, 4, 6]), RULE_A)), 6.5)


def test_reset_window():
    # 18.1 s after the first stun ends, the counter has reset.
    chain = [{"time": 0.0, "ability": "a", "category": "stun", "base": 6},
             {"time": 24.1, "ability": "b", "category": "stun", "base": 6}]
    assert [e["multiplier"] for e in simulate(chain, RULE_A)] == [1, 1]
    chain[1]["time"] = 23.9
    assert [e["multiplier"] for e in simulate(chain, RULE_A)] == [1, 0.5]


def test_categories_are_separate():
    chain = back_to_back([6, 6, 6]) + [{"time": 10.5, "ability": "x", "category": "incapacitate", "base": 6}]
    assert simulate(chain, RULE_A)[-1]["multiplier"] == 1


def test_uptime_ceiling():
    assert near(uptime_ceiling(6, RULE_A), 10.5 / 28.5)       # 36.8%
    assert round(100 * uptime_ceiling(6, RULE_A), 1) == 36.8


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
