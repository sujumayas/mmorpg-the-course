"""Tests for MMO406 Lab 13. Values come from the week 13 lecture and lab13.md.
Run with `.venv/bin/python test_rp_hubs.py` (from any folder) or pytest.
Every test fails on the starter and passes on a correct rp_hubs.py."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from rp_hubs import best_hubs, choose_plan, day_plan, p_at_least, scene_share, viable_hubs  # noqa: E402


def close(a, b, tol=1e-3):
    return abs(a - b) < tol


def load():
    with open(os.path.join(HERE, "dikeholm_rp.json")) as f:
        return json.load(f)


def test_p_at_least():
    assert close(p_at_least(4, 4), 0.5665)
    assert close(p_at_least(5, 3), 0.8753)
    assert p_at_least(2.5, 0) == 1.0
    assert close(p_at_least(3, 1), 1 - 0.049787)


def test_lecture_table():
    rows = {1: (1.00, 1.000), 4: (3.40, 0.938), 5: (3.53, 0.857),
            6: (3.40, 0.762), 8: (2.82, 0.577), 12: (1.71, 0.323)}
    for H, (v, s) in rows.items():
        assert close(viable_hubs(24, H, 4), v, 0.006), H
        assert close(scene_share(24, H, 4), s, 0.0006), H


def test_best_hubs():
    assert best_hubs(24, 4) == 5
    assert best_hubs(6, 4) == 1
    assert best_hubs(30, 4) == 6
    assert best_hubs(30, 10) == 2
    assert best_hubs(8, 4) == 2
    assert best_hubs(15, 3) == 4


def test_day_plan_without_fallback():
    h = load()["hourly"]
    p1 = day_plan(h, 4, 1)
    assert close(p1["live_hub_hours"], 16.407) and close(p1["share"], 0.9450)
    assert p1["worst_hour"][0] == 6 and close(p1["worst_hour"][1], 0.0803)
    p4 = day_plan(h, 4, 4)
    assert close(p4["live_hub_hours"], 23.822) and close(p4["share"], 0.6557)


def test_day_plan_with_fallback():
    h = load()["hourly"]
    p4 = day_plan(h, 4, 4, fallback_below=12)
    assert close(p4["live_hub_hours"], 29.543) and close(p4["share"], 0.8700)
    assert p4["worst_hour"][0] == 6
    p5 = day_plan(h, 4, 5, fallback_below=12)
    assert close(p5["live_hub_hours"], 29.822) and close(p5["share"], 0.8138)


def test_day_plan_skips_empty_hours():
    p = day_plan([0, 0, 24, 0], 4, 5)
    assert close(p["live_hub_hours"], 3.529) and close(p["share"], 0.857)
    assert p["worst_hour"][0] == 2


def test_choose_plan():
    h = load()["hourly"]
    assert choose_plan(h, 4, 0.85) == 1
    assert choose_plan(h, 4, 0.85, fallback_below=12) == 4
    assert choose_plan(h, 4, 0.80, fallback_below=12) == 5
    assert choose_plan(h, 4, 0.99) is None


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
    print(f"\n{failed} test(s) not passing" if failed else "\nAll tests pass.")
    sys.exit(1 if failed else 0)
