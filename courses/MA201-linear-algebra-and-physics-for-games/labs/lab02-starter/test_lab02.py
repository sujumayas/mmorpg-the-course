"""Tests for Lab 02. Run from this folder: python test_lab02.py"""
import math
import sys
import traceback

import mat2 as m

TOL = 1e-6


def close(a, b, tol=TOL):
    return abs(a - b) <= tol


def mclose(A, B, tol=TOL):
    return all(close(A[r][c], B[r][c], tol) for r in (0, 1) for c in (0, 1))


def test_mat_vec():
    assert m.mat_vec(((1, 0.5), (0, 1)), (2, 2)) == (3, 2)
    assert m.mat_vec(((1, 2), (0, 1)), (3, 4)) == (11, 4)


def test_mat_mul_order():
    rot90, stretch = ((0, -1), (1, 0)), ((2, 0), (0, 1))
    assert mclose(m.mat_mul(rot90, stretch), ((0, -1), (2, 0)))
    assert mclose(m.mat_mul(stretch, rot90), ((0, -2), (1, 0)))
    A, B = ((1, 2), (3, 4)), ((0, 1), (-1, 5))
    x = (7, -2)
    assert m.mat_vec(m.mat_mul(A, B), x) == m.mat_vec(A, m.mat_vec(B, x))


def test_det_and_inverse():
    tile = ((32, -32), (16, 16))
    assert close(m.det(tile), 1024)
    assert mclose(m.inverse(tile), ((1 / 64, 1 / 32), (-1 / 64, 1 / 32)))
    assert m.inverse(((2, 4), (1, 2))) is None
    assert close(m.det(((0, 1), (1, 0))), -1)
    A = ((3, 1), (2, 5))
    assert mclose(m.mat_mul(A, m.inverse(A)), ((1, 0), (0, 1)))


def test_tile_matrix_and_table():
    M = m.tile_matrix(64, 32)
    assert mclose(M, ((32, -32), (16, 16)))
    for (i, j), want in {(0, 0): (0, 0), (1, 0): (32, 16), (0, 1): (-32, 16), (1, 1): (0, 32),
                         (3, 2): (32, 80), (2, 5): (-96, 112), (4.5, 1.5): (96, 96)}.items():
        got = m.tile_to_screen(M, (0, 0), i, j)
        assert close(got[0], want[0]) and close(got[1], want[1]), (i, j, got)


def test_screen_to_tile_table():
    M = m.tile_matrix(64, 32)
    for s, want in {(0, 8): (0, 0), (0, 31): (0, 0), (0, 33): (1, 1), (40, 30): (1, 0),
                    (30, 10): (0, -1), (-20, 50): (1, 1), (100, 120): (5, 2)}.items():
        assert m.screen_to_tile(M, (0, 0), *s) == want, (s, m.screen_to_tile(M, (0, 0), *s))


def test_origin_and_round_trip():
    M, o = m.tile_matrix(96, 48), (480, 20)
    for i in range(-3, 8):
        for j in range(-3, 8):
            x, y = m.tile_to_screen(M, o, i + 0.5, j + 0.5)
            assert m.screen_to_tile(M, o, x, y) == (i, j)
    assert m.screen_to_tile(((2, 4), (1, 2)), (0, 0), 5, 5) is None


def test_error_rate_is_half():
    assert close(m.error_rate(64, 32, -256, 256, 0, 256), 0.5, 1e-3)
    assert close(m.error_rate(96, 48, -192, 192, 0, 192), 0.5, 1e-3)


def test_zoom_and_mirror_pick():
    base = m.tile_matrix(64, 32)
    Z = m.zoom(2)
    assert mclose(Z, ((2, 0), (0, 2)))
    M = m.mat_mul(Z, base)
    assert close(m.det(M), 4096)
    x, y = m.tile_to_screen(M, (0, 0), 3.5, 2.5)
    assert (round(x, 6), round(y, 6)) == (64, 192)
    assert m.screen_to_tile(M, (0, 0), x, y) == (3, 2)
    F = m.mat_mul(m.MIRROR_X, base)
    assert close(m.det(F), -1024)
    x, y = m.tile_to_screen(F, (0, 0), 2.5, 5.5)
    assert m.screen_to_tile(F, (0, 0), x, y) == (2, 5)


TESTS = [f for k, f in dict(globals()).items() if k.startswith("test_")]

if __name__ == "__main__":
    passed = 0
    for t in TESTS:
        try:
            t()
            passed += 1
            print(f"PASS {t.__name__}")
        except NotImplementedError:
            print(f"TODO {t.__name__}")
        except Exception:
            print(f"FAIL {t.__name__}")
            traceback.print_exc(limit=1)
    print(f"{passed}/{len(TESTS)} tests passed")
    sys.exit(0 if passed == len(TESTS) else 1)
