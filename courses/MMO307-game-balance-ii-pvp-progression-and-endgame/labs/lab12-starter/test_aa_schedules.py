"""Lab 12 tests. Run with `python3 test_aa_schedules.py` (or pytest).
Every test fails on the starter and passes once the TODOs are done."""
import sys
from aa_schedules import cost_of_point, points_after, power, evaluate, LECTURE_DESIGNS


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def test_cost_of_point():
    assert cost_of_point(7, "flat", {"cost": 10}) == 10
    assert cost_of_point(5, "linear", {"step": 2}) == 10
    assert close(cost_of_point(3, "geometric", {"first": 2, "ratio": 1.05}), 2.205)


def test_points_after():
    assert points_after(0, "flat", {"cost": 10}) == 0
    assert points_after(260, "flat", {"cost": 10}) == 26
    assert points_after(1040, "linear", {"step": 2}) == 31
    assert points_after(260, "geometric", {"first": 2, "ratio": 1.05}) == 41
    assert points_after(3120, "geometric", {"first": 2, "ratio": 1.05}) == 89


def test_power():
    assert close(power(104, "constant", {"v": 0.01}), 2.04)
    assert close(power(312, "decaying", {"v0": 0.02, "d": 0.98}), 1.998, 1e-3)
    assert close(power(0, "decaying", {"v0": 0.02, "d": 0.98}), 1.0)
    assert close(power(60, "capped", {"v": 0.01, "cap": 50}), 1.5)


def test_lecture_designs():
    flat = evaluate(LECTURE_DESIGNS["flat"])
    geo = evaluate(LECTURE_DESIGNS["geometric"])
    assert close(flat["ratio_final"], 2.315, 1e-3)
    assert close(geo["ratio_final"], 1.174, 1e-3)
    assert close(geo["heavy_weeks_per_point_year3"], 6.50, 0.01)
    assert geo["light_points_week10"] == 16


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS {name}")
            except Exception as e:
                failed += 1
                print(f"FAIL {name}: {type(e).__name__} {e}")
    sys.exit(1 if failed else 0)
