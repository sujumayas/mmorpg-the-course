"""MMO407 lab 07 tests. Run with: python -m unittest test_realm_balance.py
Every test fails on the starter and passes once the TODOs are done."""
import unittest

from realm_balance import (LECTURE, first_week_at, newcomer_share,
                           realm_choice, share, simulate, week)


class TestRule(unittest.TestCase):
    def test_newcomer_share(self):
        self.assertAlmostEqual(newcomer_share(0.5, 3), 0.5)
        self.assertAlmostEqual(newcomer_share(0.55, 2), 0.599, places=3)
        self.assertAlmostEqual(newcomer_share(0.6, 2), 0.6923, places=4)
        self.assertAlmostEqual(newcomer_share(0.6, 1), 0.6)


class TestLectureRealm(unittest.TestCase):
    def test_first_week(self):
        A, B, t = week(5500, 4500, **LECTURE)
        self.assertAlmostEqual(A, 5824.0, places=1)
        self.assertAlmostEqual(B, 4586.0, places=1)
        self.assertEqual(t, 0)

    def test_year(self):
        rows, _ = simulate(5500, 4500, 52, **LECTURE)
        self.assertAlmostEqual(100 * share(rows[8]), 68.1, places=1)
        self.assertAlmostEqual(100 * share(rows[16]), 90.7, places=1)
        self.assertEqual(first_week_at(rows, 0.7), 9)
        self.assertEqual(first_week_at(rows, 0.9), 16)
        self.assertAlmostEqual(sum(rows[52]), 18688, delta=1)

    def test_neutral_never_moves(self):
        rows, _ = simulate(5500, 4500, 52, J=1000, c=0.05, k=1, e=0)
        self.assertAlmostEqual(share(rows[52]), 0.55, places=9)
        self.assertIsNone(first_week_at(rows, 0.6))


class TestLock(unittest.TestCase):
    def test_lock_holds(self):
        rows, turned = simulate(5500, 4500, 52, lock=0.55, **LECTURE)
        self.assertAlmostEqual(100 * share(rows[52]), 54.9, places=1)
        self.assertAlmostEqual(min(rows[52]), 7121, delta=1)
        self.assertAlmostEqual(turned, 3653, delta=1)


class TestRealms(unittest.TestCase):
    def test_realm_choice(self):
        got = realm_choice([2000, 1000, 1000], 600, 2)
        for g, want in zip(got, [400, 100, 100]):
            self.assertAlmostEqual(g, want)
        self.assertAlmostEqual(sum(realm_choice([3, 2, 1], 60, 1)), 60)


if __name__ == "__main__":
    unittest.main()
