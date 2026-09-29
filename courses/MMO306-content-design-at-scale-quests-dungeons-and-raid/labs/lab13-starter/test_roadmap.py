"""Tests for Lab 13. Values come from the week 13 lecture.
Run with ../../../../.venv/bin/python test_roadmap.py (or pytest)."""
from roadmap import (drought_days, fastest_cadence, mean_days_late, on_time_chance, pert,
                     release_days, simulate, teams_needed)


def close(a, b, tol=1e-6):
    return abs(a - b) < tol


def test_pert_and_chance():
    assert pert(240, 300, 480) == (320, 40)
    assert pert(90, 120, 210) == (130, 20)
    assert close(on_time_chance(2, 160, 320, 40), 0.5)
    assert close(on_time_chance(2, 175, 320, 40), 0.773373, 1e-5)
    assert close(on_time_chance(3, 133, 320, 40), 0.975866, 1e-5)
    assert close(mean_days_late(2, 160, 320, 40), 15.957691, 1e-5)
    assert close(mean_days_late(3, 133, 320, 40), 0.363064, 1e-5)


def test_teams_and_cadence():
    assert teams_needed(175, 320, 40, 0.9) == 3
    assert teams_needed(200, 320, 40, 0.9) == 2
    assert teams_needed(120, 320, 40, 0.9) == 4
    assert teams_needed(160, 320, 40, 0.5) == 2      # the mean plan just qualifies at 50%
    assert close(fastest_cadence(3, 320, 40, 0.9), 123.754, 1e-3)
    assert close(fastest_cadence(4, 320, 40, 0.977249868), 100.0, 1e-3)


def test_release_days():
    assert release_days([320, 350, 320, 320], 2, 160) == [160, 350, 480, 670]
    assert release_days([250, 150, 200], 2, 100) == [150, 200, 350]      # late team starts late
    assert release_days([320, 150], 2, 100) == [220, 220]                # drop 2 held by drop 1
    assert release_days([100, 100, 100], 1, 120) == [120, 240, 360]      # early drops wait


def test_drought_days():
    assert drought_days([160, 350, 480, 670], 140) == 120
    assert drought_days([160, 320, 480], 200) == 0


def test_simulate():
    share, late = simulate(3, 133, 320, 40)
    assert abs(share - 0.976) < 0.015          # cascades are rare with a large window
    share2, late2 = simulate(2, 160, 320, 40)
    assert share2 < 0.45                        # cascades make the mean plan worse than 50%
    assert late2 > 16                           # and later than one drop on its own
    assert simulate(2, 160, 320, 40) == (share2, late2)   # same seed, same answer


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
