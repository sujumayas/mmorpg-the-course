"""MA201 Lab 14 tests. Run `python test_lab14.py` (or `pytest test_lab14.py`).
On the untouched starter every test fails."""
import math

from precision import (gap32, walk_speed, freeze_distance, float_clock,
                       state_hash, first_divergence, arena_run)


def near(a, b, tol=1e-3):
    return a is not None and abs(a - b) < tol


def test_gap32():
    assert gap32(1.0) == 2.0 ** -23
    assert gap32(5000.0) == 2.0 ** -11
    assert gap32(200_000.0) == 2.0 ** -6
    assert gap32(-3.0) == 2.0 ** -22
    assert gap32(30_000_000.0) == 2.0


def test_walk_speed_float32_staircase():
    dt = 1 / 60
    assert near(walk_speed(100_000, 1.4, dt), 1.40625)
    assert near(walk_speed(200_000, 1.4, dt), 0.9375)
    assert near(walk_speed(300_000, 1.4, dt), 1.875)
    assert walk_speed(600_000, 1.4, dt) == 0.0


def test_walk_speed_other_representations():
    dt = 1 / 60
    assert near(walk_speed(30_000_000, 1.4, dt, rep="f64"), 1.4, 1e-6)
    assert near(walk_speed(300_000, 1.4, dt, rep="mm"), 1.38)
    assert near(walk_speed(1, 1.4, dt, rep="mm"), 1.38)


def test_freeze_distance():
    assert freeze_distance(1.4, 1 / 60) == 524_288
    assert freeze_distance(6.0, 1 / 60) == 2_097_152
    assert freeze_distance(0.5, 1 / 30) == 524_288


def test_float_clock():
    assert near(float_clock(80, 600, 1 / 60), 18.75)
    assert near(float_clock(1, 600, 1 / 60), 9.961, 0.001)
    assert float_clock(150, 600, 1 / 60) == 0.0


def test_state_hash_is_bit_exact():
    s = (0.1, -0.8, 0.5, 0.25)
    h = state_hash(s)
    assert isinstance(h, int) and h == state_hash((0.1, -0.8, 0.5, 0.25))
    t = (math.nextafter(0.1, 1.0), -0.8, 0.5, 0.25)          # one ulp away
    assert state_hash(t) != h
    assert state_hash((0.0,)) != state_hash((-0.0,))          # bits, not values


def test_first_divergence():
    assert first_divergence([1, 2, 3, 4], [1, 2, 9, 4]) == 2
    assert first_divergence([5, 6], [5, 6]) is None


def test_arena_same_build_agrees():
    a = [state_hash(s) for s in arena_run(2400, fused=True)]
    b = [state_hash(s) for s in arena_run(2400, fused=True)]
    assert len(set(a)) > 2000                      # the state really changes
    assert first_divergence(a, b) is None


def test_arena_fma_diverges_at_first_bounce():
    a = [state_hash(s) for s in arena_run(2400, fused=False)]
    b = [state_hash(s) for s in arena_run(2400, fused=True)]
    assert first_divergence(a, b) == 191


TESTS = [v for k, v in dict(globals()).items() if k.startswith("test_")]

if __name__ == "__main__":
    passed = 0
    for test in TESTS:
        try:
            test()
            passed += 1
            print(f"PASS {test.__name__}")
        except Exception as e:  # noqa: BLE001
            print(f"FAIL {test.__name__}: {type(e).__name__} {e}")
    print(f"{passed}/{len(TESTS)} tests passed")
