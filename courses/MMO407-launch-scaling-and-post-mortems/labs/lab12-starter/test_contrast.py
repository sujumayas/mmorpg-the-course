"""MMO407 lab 12 tests. Run with: python -m unittest test_contrast.py
Every test fails on the starter and passes once TODOs 1-3 are done."""
import math
import unittest

from contrast import biggest_rank_change, contrast, counts, load, rank


class TestCounts(unittest.TestCase):
    def test_lecture_rows(self):
        rows = load()
        self.assertEqual(counts(rows, "no_full_load_test"), (12, 20, 3, 20))
        self.assertEqual(counts(rows, "queue_over_1h"), (14, 20, 13, 20))


class TestContrast(unittest.TestCase):
    def test_values(self):
        ft, fs, lift = contrast(12, 20, 3, 20)
        self.assertAlmostEqual((ft, fs, lift), (0.60, 0.15, 4.0))
        self.assertAlmostEqual(contrast(14, 20, 13, 20)[2], 14 / 13)
        self.assertAlmostEqual(contrast(9, 15, 6, 25)[2], 2.5)

    def test_zero_and_half(self):
        self.assertEqual(contrast(6, 20, 0, 20)[2], math.inf)
        ft, fs, lift = contrast(6, 20, 0, 20, half=True)
        self.assertAlmostEqual(ft, 6.5 / 21)
        self.assertAlmostEqual(lift, 13.0)


class TestRanking(unittest.TestCase):
    def test_orders(self):
        rows = load()
        self.assertEqual(rank(rows, "f_T")[:4], ["queue_over_1h", "no_full_load_test",
                                                 "paid_head_start", "beta_under_5pct"])
        self.assertEqual(rank(rows, "L")[:4], ["no_full_load_test", "beta_under_5pct",
                                               "paid_head_start", "queue_over_1h"])
        self.assertEqual(rank(rows, "L")[-1], "staggered_unlock")
        self.assertEqual(biggest_rank_change(rows), "queue_over_1h")


if __name__ == "__main__":
    unittest.main()
