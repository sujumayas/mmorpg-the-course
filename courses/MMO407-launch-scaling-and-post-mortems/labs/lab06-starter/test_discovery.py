"""MMO407 lab 06 tests. Run with: python -m unittest test_discovery.py
Every test fails on the starter and passes once the TODOs are done."""
import math
import unittest

from discovery import (fit_least_squares, fit_two_points, next_week, remaining,
                       reopen_week, sse)

A, B = 12.0, math.log(2) / 2


class TestLecture(unittest.TestCase):
    def test_fit_two_points(self):
        a, b = fit_two_points(6, 9, 2)
        self.assertAlmostEqual(a, 12.0)
        self.assertAlmostEqual(b, 0.346574, places=6)
        a, b = fit_two_points(8, 12, 3)
        self.assertAlmostEqual(a, 16.0)
        self.assertAlmostEqual(b, 0.231049, places=6)
        with self.assertRaises(ValueError):
            fit_two_points(5, 10, 2)

    def test_remaining(self):
        self.assertAlmostEqual(remaining(4, A, B), 3.0)
        self.assertAlmostEqual(remaining(8, A, B, [(6, 4)]), 2.75)
        self.assertAlmostEqual(remaining(5, A, B, [(6, 4)]), 12 * 2 ** -2.5)

    def test_next_week(self):
        e, p = next_week(4, A, B)
        self.assertAlmostEqual(e, 0.878680, places=5)
        self.assertAlmostEqual(p, 0.584669, places=5)
        e, p = next_week(8, A, B, [(6, 4)])
        self.assertAlmostEqual(p, 0.553, places=3)

    def test_reopen(self):
        self.assertAlmostEqual(reopen_week(A, B, 0.10), 10.13, places=2)
        self.assertAlmostEqual(reopen_week(A, B, 0.10, [(6, 4)]), 13.87, places=2)
        self.assertAlmostEqual(reopen_week(A, B, 0.20), 7.96, places=2)


class TestLeastSquares(unittest.TestCase):
    def test_exact_curve_recovered(self):
        weeks = list(range(1, 9))
        counts = [A * (1 - math.exp(-B * t)) for t in weeks]
        a, b, err = fit_least_squares(weeks, counts)
        self.assertAlmostEqual(a, 12.0, delta=0.1)
        self.assertAlmostEqual(b, B, delta=0.005)
        self.assertLess(err, 0.01)

    def test_beats_two_point_fit(self):
        weeks, counts = [1, 2, 3, 4], [4, 7, 9, 10]
        a2, b2 = fit_two_points(7, 9, 2)
        a, b, err = fit_least_squares(weeks, counts)
        self.assertLessEqual(err, sse(weeks, counts, a2, b2) + 1e-12)


if __name__ == "__main__":
    unittest.main()
