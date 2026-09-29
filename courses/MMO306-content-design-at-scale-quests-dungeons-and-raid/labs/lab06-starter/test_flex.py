"""Tests for Lab 06. Values come from the week 6 lecture.
Run with `python test_flex.py` (or `pytest test_flex.py` if you have pytest)."""
from flex import (clean_fixed, clean_raidwide, clean_targeted, health_linear, health_neutral,
                  per_dealer, roster, wipes_to_clear)

P = 0.99617  # week 5: 1,100 ms telegraph, mu 700, sigma 150


def close(a, b, tol):
    return a is not None and abs(a - b) <= tol


def test_roster():
    assert [roster(N)[2] for N in (10, 15, 20, 25, 30)] == [6, 10, 14, 18, 22]
    assert roster(12) == (2, 2, 8)
    assert roster(25, extra_tank_at=25) == (3, 5, 17)
    assert roster(24, extra_tank_at=25) == (2, 4, 18)


def test_linear_rule():
    assert health_linear(10, 5_040_000) == 2_520_000
    reqs = [per_dealer(health_linear(N, 5_040_000), N, 300, 0.8) for N in (10, 15, 20, 25, 30)]
    for got, want in zip(reqs, [1750, 1575, 1500, 1458.3, 1431.8]):
        assert close(got, want, 0.1)


def test_neutral_rule():
    hs = [health_neutral(N, 5_040_000, 300, 0.8) for N in (10, 15, 20, 25, 30)]
    for got, want in zip(hs, [2_160_000, 3_600_000, 5_040_000, 6_480_000, 7_920_000]):
        assert close(got, want, 1)
    for N in range(10, 31):
        assert close(per_dealer(health_neutral(N, 5_040_000, 300, 0.8), N, 300, 0.8), 1500, 1e-6)
    h25 = health_neutral(25, 5_040_000, 300, 0.8, extra_tank_at=25)
    assert close(h25, 6_120_000, 1)


def test_mechanic_scaling():
    assert close(clean_raidwide(P, 10, 5), 0.825, 0.001)
    assert close(clean_raidwide(P, 30, 5), 0.562, 0.001)
    assert close(clean_targeted(P, 10, 5), 0.962, 0.001)
    assert close(clean_targeted(P, 30, 5), 0.891, 0.001)
    assert close(clean_fixed(P, 3, 5), clean_targeted(P, 15, 5), 1e-12)


def test_wipes_to_clear():
    assert wipes_to_clear(1.0) == 0
    assert wipes_to_clear(0.8) == 5
    assert wipes_to_clear(0.7) == 9
    assert wipes_to_clear(2 / 3) == 10
    assert wipes_to_clear(0.6) is None


if __name__ == "__main__":
    import sys
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
    print(f"{failed} test(s) not passing")
    sys.exit(1 if failed else 0)
