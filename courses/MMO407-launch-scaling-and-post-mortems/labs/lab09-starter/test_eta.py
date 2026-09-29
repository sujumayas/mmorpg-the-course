"""MMO407 lab 09 tests. Run with: python -m unittest test_eta.py
Every test fails on the starter and passes once the TODOs are done."""
import unittest

from eta import (LECTURE_LOG, best_eta, cost, fixed_extensions, load,
                 mean_left, misses, reforecast)


class TestForecast(unittest.TestCase):
    def test_cost(self):
        self.assertAlmostEqual(cost(60, LECTURE_LOG), 150.5)
        self.assertAlmostEqual(cost(105, LECTURE_LOG), 141.5)
        self.assertAlmostEqual(cost(120, LECTURE_LOG), 143.0)

    def test_best_eta(self):
        self.assertEqual(best_eta(LECTURE_LOG), 105)
        self.assertEqual(best_eta(LECTURE_LOG, 3, 1), 120)
        self.assertEqual(best_eta(LECTURE_LOG, 1, 1), 60)

    def test_best_is_cheapest(self):
        T = best_eta(LECTURE_LOG)
        self.assertTrue(all(cost(T, LECTURE_LOG) <= cost(x, LECTURE_LOG) + 1e-9
                            for x in range(0, 700, 5)))

    def test_mean_left(self):
        self.assertAlmostEqual(mean_left(LECTURE_LOG, 0), 116.5)
        self.assertAlmostEqual(mean_left(LECTURE_LOG, 60), 153.333, places=3)
        self.assertAlmostEqual(mean_left(LECTURE_LOG, 240), 240.0)
        self.assertIsNone(mean_left(LECTURE_LOG, 600))


class TestPolicies(unittest.TestCase):
    def test_fixed(self):
        self.assertEqual(misses(fixed_extensions(600, LECTURE_LOG)), 18)
        self.assertEqual(fixed_extensions(150, LECTURE_LOG), [60, 90, 120, 150])
        avg = sum(misses(fixed_extensions(d, LECTURE_LOG)) for d in LECTURE_LOG) / 20
        self.assertAlmostEqual(avg, 2.35)

    def test_reforecast(self):
        self.assertEqual(reforecast(600, LECTURE_LOG), [105, 240, 600])
        self.assertEqual(reforecast(90, LECTURE_LOG), [105])
        avg = sum(misses(reforecast(d, LECTURE_LOG)) for d in LECTURE_LOG) / 20
        self.assertAlmostEqual(avg, 0.4)
        self.assertEqual(reforecast(900, LECTURE_LOG), [105, 240, 600, 960])

    def test_csv(self):
        self.assertEqual(len(load()), 200)
        self.assertEqual(len(load(kind="database")), 60)
        self.assertEqual(best_eta(load(kind="database")), 145)
        self.assertEqual(best_eta(load()), 70)


if __name__ == "__main__":
    unittest.main()
