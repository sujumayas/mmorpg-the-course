"""MMO407 lab 03 tests. Run with: python -m unittest test_beta_exposure.py
Every test fails on the starter and passes once the TODOs are done."""
import unittest

from beta_exposure import (expected_firings, exposure, hours_needed, p_seen,
                           path_exposure, phased_ladder, rule_of_three)

BETA = exposure(5_000, 20)
LAUNCH = exposure(200_000, 15)


class TestLectureTable(unittest.TestCase):
    def test_seen_and_expected(self):
        self.assertAlmostEqual(p_seen(200_000, BETA), 0.3935, places=4)
        self.assertAlmostEqual(p_seen(50_000, BETA), 0.8647, places=4)
        self.assertAlmostEqual(expected_firings(200_000, LAUNCH), 15)

    def test_rule_of_three(self):
        self.assertAlmostEqual(rule_of_three(BETA), 33_333.33, places=1)
        self.assertAlmostEqual(LAUNCH / rule_of_three(BETA), 90)

    def test_hours_needed(self):
        self.assertAlmostEqual(hours_needed(200_000), 599_146, delta=1)
        self.assertAlmostEqual(hours_needed(200_000, 0.5), 138_629, delta=1)


class TestShape(unittest.TestCase):
    def test_paths(self):
        paths = path_exposure(100_000, {"early": 60, "mid": 38, "endgame": 2})
        self.assertAlmostEqual(paths["endgame"], 2_000)
        self.assertAlmostEqual(rule_of_three(paths["endgame"]), 666.67, places=2)
        capped = path_exposure(100_000, {"early": 1, "endgame": 0})
        self.assertEqual(capped["endgame"], 0)

    def test_phased_ladder(self):
        days = phased_ladder(LAUNCH, 200_000)
        self.assertEqual(len(days), 7)
        self.assertAlmostEqual(days[0], 0.0212, places=4)
        self.assertAlmostEqual(days[-1], 0.9822, places=4)
        self.assertTrue(all(a < b for a, b in zip(days, days[1:])))


if __name__ == "__main__":
    unittest.main()
