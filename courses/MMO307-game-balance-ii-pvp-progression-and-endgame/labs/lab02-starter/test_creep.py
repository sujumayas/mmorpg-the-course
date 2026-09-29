"""Tests for MMO307 Lab 02. Values come from the week 2 lecture.
Run with `python test_creep.py` (or pytest if you have it)."""
import math

from creep import (DATA, creep_per_expansion, creep_per_tier, fit_additive,
                   fit_multiplicative, increments, largest_overlap, load_series,
                   max_creep, ratios, shelf_life)

WOW = load_series(DATA, "wow_native")
FF = load_series(DATA, "ffxiv")


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


def test_data():
    assert WOW == [86, 159, 284, 416, 580, 735, 1000]
    assert FF == [130, 270, 400, 530, 660, 790]


def test_increments_and_ratios():
    assert increments(WOW) == [73, 125, 132, 164, 155, 265]
    assert increments(FF) == [140, 130, 130, 130, 130]
    assert [round(r, 3) for r in ratios(WOW)] == [1.849, 1.786, 1.465, 1.394, 1.267, 1.361]
    assert close(ratios(FF)[-1], 790 / 660)


def test_squished_eras():
    sl = load_series(DATA, "wow_sl_scale")
    assert increments(sl) == [171, 217, 202]


def test_fits():
    b, sse_add = fit_additive(FF)
    assert close(b, 131.4286, 1e-3)
    assert close(sse_add, 47.619, 1e-2)
    ratio, sse_mul = fit_multiplicative(FF)
    assert sse_add < sse_mul
    b, sse_add = fit_additive(WOW)
    ratio, sse_mul = fit_multiplicative(WOW)
    assert close(b, 149.643, 1e-2)
    assert close(ratio, 1.4884, 1e-3)
    assert sse_add < sse_mul          # WoW's native era is closer to additive


def test_ratchet():
    assert [creep_per_tier(o, 10, 5) for o in range(4)] == [5, 15, 25, 35]
    assert creep_per_expansion(3, 3, 10, 5) == 105
    assert creep_per_expansion(2, 2, 12, 6) == 60


def test_shelf_life():
    assert close(shelf_life(15, 0.01, 2), 4.64, 5e-3)
    assert close(shelf_life(35, 0.01, 2), 1.99, 5e-3)
    assert close(shelf_life(30, 0.01, 2), 2.32, 5e-3)
    assert shelf_life(0, 0.01, 2) == math.inf


def test_budget():
    assert close(max_creep(0.01, 2, 3), 23.22, 5e-3)
    assert close(max_creep(0.008, 1.5, 4), 12.72, 5e-3)
    assert largest_overlap(4, 10, 5, 0.01, 2, 3) == 1
    assert largest_overlap(4, 10, 5, 0.01, 2, 2) == 2
    assert largest_overlap(4, 10, 30, 0.01, 2, 3) is None


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
