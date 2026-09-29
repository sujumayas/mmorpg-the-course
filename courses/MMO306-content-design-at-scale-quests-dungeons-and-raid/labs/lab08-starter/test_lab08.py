"""Checks for MMO306 Lab 08. Run from this folder:  python test_lab08.py
Each check prints PASS or FAIL. A NotImplementedError counts as FAIL."""
import traceback

import repeatables as r


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


def test_expected_repeats():
    assert close(r.expected_repeats(22, 6), 36 / 22)
    assert close(r.expected_repeats(55, 18), 324 / 55)
    assert close(r.expected_repeats(19, 19), 19)


def test_exposure_lecture_table():
    assert close(r.exposure(22, 6, 3), 0.615)
    assert close(r.exposure(22, 6, 7), 0.892)
    assert close(r.exposure(55, 18, 7), 0.938)
    assert close(r.exposure(44, 6, 3), 0.356)
    assert close(r.exposure(22, 6, 3, mode="cycle"), 18 / 22)
    assert close(r.exposure(22, 6, 4, mode="cycle"), 1.0)


def test_periods_to():
    assert close(r.periods_to(22, 6, 0.9), 7.23, 0.01)
    assert close(r.periods_to(8, 2, 0.9), 8.00, 0.01)
    assert close(r.periods_to(19, 19, 0.9), 1.0)


def test_pool_for_target():
    assert r.pool_for_target(6, 0.75, 7) == 34
    assert r.pool_for_target(5, 0.60, 5) == 30


def test_simulate_exposure_matches_formula():
    sim = r.simulate_exposure(22, 6, 3, 3000, seed=7)
    assert abs(sim - r.exposure(22, 6, 3)) < 0.01
    # never offering yesterday's items can only raise exposure
    sim_nr = r.simulate_exposure(22, 6, 3, 3000, seed=7, no_repeat_yesterday=True)
    assert sim_nr > sim + 0.05
    assert r.simulate_exposure(12, 6, 2, 50, seed=1, no_repeat_yesterday=True) == 1.0


def test_weeks_to_goal_lecture():
    h30 = [0, 0, 0] + [30] * 13
    h8 = [0, 0, 0] + [8] * 13
    assert r.weeks_to_goal([30] * 16, 60, None, 3600) == 2
    assert r.weeks_to_goal([30] * 16, 60, 450, 3600) == 8
    assert r.weeks_to_goal(h30, 60, 450, 3600) == 11
    assert r.weeks_to_goal(h30, 60, 450, 3600, accumulate=True) == 8
    assert r.weeks_to_goal(h8, 60, 450, 3600, accumulate=True) == 11
    assert r.weeks_to_goal([0, 0, 0] + [15] * 13, 60, 450, 3600, accumulate=True) == 8
    assert r.weeks_to_goal([1] * 16, 60, 450, 3600) is None


def test_percentile():
    assert close(r.percentile([1, 2, 3, 4], 0.5), 2.5)
    assert close(r.percentile([10, 20, 30, 40, 50], 0.25), 20)
    assert close(r.percentile([5], 0.9), 5)


def test_dataset():
    table = r.load_hours("hours.csv")
    assert len(table) == 400 and all(len(row) == 16 for row in table)
    hard = r.finish_weeks(table, 60, 450, 3600)
    acc = r.finish_weeks(table, 60, 450, 3600, accumulate=True)
    assert [r.percentile(hard, p) for p in (0.1, 0.5)] == [8.0, 10.0]
    assert [r.percentile(acc, p) for p in (0.1, 0.5)] == [8.0, 9.0]
    assert sum(x == 17 for x in hard) == 90


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("test_")]

if __name__ == "__main__":
    passed = 0
    for fn in TESTS:
        try:
            fn()
            print(f"PASS {fn.__name__}")
            passed += 1
        except NotImplementedError:
            print(f"FAIL {fn.__name__} (not implemented yet)")
        except Exception:
            print(f"FAIL {fn.__name__}")
            traceback.print_exc(limit=1)
    print(f"{passed}/{len(TESTS)} checks passed")
    raise SystemExit(0 if passed == len(TESTS) else 1)
