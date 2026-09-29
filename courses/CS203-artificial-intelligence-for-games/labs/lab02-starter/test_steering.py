"""Tests for Lab 02. Values come from the week 2 lecture.
Run with `python3 test_steering.py` or `pytest test_steering.py`."""
from steering import (arrive, blend, braking_distance, chase, flee, pursue, run_line,
                      seek, step)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def test_braking_distance():
    assert close(braking_distance(6, 12), 1.5)
    assert close(braking_distance(8, 16), 2.0)


def test_step_limits_acceleration():
    pos, vel = step((0.0, 0.0), (0.0, 0.0), (6.0, 0.0), 6.0, 12.0)
    assert close(vel[0], 0.2) and close(vel[1], 0.0)          # 12 m/s^2 * 1/60 s
    assert close(pos[0], 0.2 / 60)


def test_step_limits_speed():
    _, vel = step((0.0, 0.0), (5.9, 0.0), (0.0, 9.0), 6.0, 1000.0)
    assert close((vel[0] ** 2 + vel[1] ** 2) ** 0.5, 6.0)


def test_seek_and_flee_directions():
    assert seek((0, 0), (3, 4), 10) == (6.0, 8.0)
    assert flee((0, 0), (3, 4), 10) == (-6.0, -8.0)
    assert seek((1, 1), (1, 1), 10) == (0, 0)


def test_arrive_ramp():
    assert arrive((0, 0), (10, 0), 6, 2) == (6.0, 0.0)      # outside the radius
    v = arrive((9, 0), (10, 0), 6, 2)                        # halfway into it
    assert close(v[0], 3.0) and close(v[1], 0.0)
    assert arrive((10, 0), (10, 0), 6, 2) == (0, 0)


def test_seek_overshoots_by_braking_distance():
    over, settled = run_line()
    assert abs(over - 1.5) < 0.01
    assert settled is None


def test_arrive_table():
    expected = {0.75: (0.80, 4.78), 1.0: (0.50, 4.68), 1.5: (0.00, 3.83),
                3.0: (0.00, 5.45), 6.0: (0.00, 7.35)}
    for r, (over, t) in expected.items():
        o, s = run_line(slow_radius=r)
        assert abs(o - over) < 0.006, (r, o)
        assert abs(s - t) < 0.006, (r, s)


def test_pursue_prediction():
    aim = pursue((0, 0), (20, 0), (0, 5), 10)   # T = 2 s, aims at (20, 10)
    assert close(aim[0], 10 * 20 / 500 ** 0.5) and close(aim[1], 10 * 10 / 500 ** 0.5)


def test_pursue_beats_seek():
    assert abs(chase(3.0, False) - 2.40) < 0.006
    assert abs(chase(3.0, True) - 2.15) < 0.006
    assert abs(chase(4.5, False) - 4.10) < 0.006
    assert abs(chase(4.5, True) - 3.05) < 0.006


def test_blend_stalemate():
    b = blend([(4, 0), (-4, 0.5)], [0.5, 0.5])
    assert close(b[0], 0.0) and close(b[1], 0.25)


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
    print(f"\n{failed} test(s) not passing" if failed else "\nall tests pass")
    raise SystemExit(1 if failed else 0)
