"""MMO407 lab 10 tests. Run with: python -m unittest test_review_memory.py
Every test fails on the starter and passes once TODOs 1-4 are done."""
import math
import unittest

from review_memory import (lifetime_share, make_log, months_to_target,
                           net_returners, reviews_needed, score, weight)


class TestMixture(unittest.TestCase):
    def test_lecture_table(self):
        expected = {0: 0.350, 6: 0.442, 12: 0.505, 24: 0.587, 36: 0.637, 60: 0.696}
        for months, share in expected.items():
            self.assertAlmostEqual(lifetime_share(40_000, 0.35, 1_500 * months, 0.85), share, places=3)

    def test_reviews_needed(self):
        self.assertAlmostEqual(reviews_needed(40_000, 0.35, 0.85, 0.60), 40_000)
        self.assertAlmostEqual(months_to_target(40_000, 0.35, 0.85, 1_500, 0.70), 62.22, places=2)
        self.assertEqual(reviews_needed(40_000, 0.35, 0.85, 0.30), 0)
        self.assertEqual(reviews_needed(40_000, 0.35, 0.85, 0.85), math.inf)

    def test_check_yourself(self):
        self.assertAlmostEqual(months_to_target(25_000, 0.40, 0.88, 1_000, 0.70), 41.67, places=2)
        self.assertAlmostEqual(net_returners(600_000, 45_000, 0.04, 0.5), 11_100)


class TestWeights(unittest.TestCase):
    def test_modes(self):
        self.assertEqual(weight(500, "lifetime"), 1)
        self.assertEqual(weight(29, "recent30"), 1)
        self.assertEqual(weight(30, "recent30"), 0)
        self.assertEqual(weight(0, "reset", day=119, reset_day=120), 0)
        self.assertEqual(weight(0, "reset", day=120, reset_day=120), 1)
        self.assertAlmostEqual(weight(90, "exponential", half_life_days=90), 0.5)
        with self.assertRaises(ValueError):
            weight(1, "median")

    def test_scores_on_the_log(self):
        log = make_log()
        self.assertAlmostEqual(score(log, 29, "lifetime"), 0.35)
        self.assertAlmostEqual(score(log, 149, "recent30"), 0.84)   # floor(50*0.85)=42 of 50
        self.assertAlmostEqual(score(log, 719, "reset", reset_day=120), 0.84)
        self.assertIsNone(score(log, 100, "reset", reset_day=120))
        life = score(log, 719, "lifetime")
        self.assertAlmostEqual(life, (30 * 350 + 90 * 15 + 600 * 42) / (30_000 + 34_500))
        expo = score(log, 719, "exponential", half_life_days=90)
        self.assertTrue(life < expo < 0.84)


if __name__ == "__main__":
    unittest.main()
