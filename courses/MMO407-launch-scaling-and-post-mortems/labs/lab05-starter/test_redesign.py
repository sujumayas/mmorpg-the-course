"""MMO407 lab 05 tests. Run with: python -m unittest test_redesign.py
Every test fails on the starter and passes once the TODOs are done."""
import math
import unittest

from redesign import (A, G_NEW, G_OLD, HUBS, S0, SEGMENTS, break_even, chance_by_month,
                      compound, departure_share, second_round)


class TestLecture(unittest.TestCase):
    def test_departure_share(self):
        self.assertAlmostEqual(departure_share(SEGMENTS), 0.29)
        protected = dict(SEGMENTS, **{"crafters and traders": (0.25, 0.15)})
        self.assertAlmostEqual(departure_share(protected), 0.215)

    def test_break_even(self):
        self.assertAlmostEqual(break_even(58_000, A, 0.25, G_NEW, G_OLD), 58_000 / 6_000)
        self.assertAlmostEqual(break_even(58_000, A, 0.05, G_NEW, G_OLD), 29.0)
        self.assertAlmostEqual(break_even(58_000, A, 0.25, G_NEW, 0), 29.0)
        self.assertEqual(break_even(58_000, A, 0.15, G_NEW, 0), math.inf)
        self.assertEqual(break_even(58_000, A, 0.0, 5_000, 1_000), math.inf)

    def test_compound(self):
        self.assertAlmostEqual(compound([0.10, 0.29]), 0.639)
        self.assertAlmostEqual(compound([0.15, 0.20]), 0.68)
        self.assertAlmostEqual(compound([]), 1.0)

    def test_second_round(self):
        self.assertAlmostEqual(second_round(S0, SEGMENTS, HUBS, 0.5), 9_185.625)
        self.assertAlmostEqual(second_round(S0, SEGMENTS, HUBS, 0.0), 0.0)

    def test_monte_carlo_edges(self):
        # Collapsed ranges make the outcome certain.
        self.assertEqual(chance_by_month(12, 200, 1, (0.25, 0.25), (4_000, 4_000), 0.0), 1.0)
        self.assertEqual(chance_by_month(9, 200, 1, (0.25, 0.25), (4_000, 4_000), 0.0), 0.0)
        p = chance_by_month(12, 2_000, 7, (0.05, 0.35), (0, 8_000), 0.1)
        self.assertTrue(0.0 < p < 1.0)
        self.assertEqual(p, chance_by_month(12, 2_000, 7, (0.05, 0.35), (0, 8_000), 0.1))


if __name__ == "__main__":
    unittest.main()
