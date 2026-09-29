"""MMO405 lab 02 tests. Run with: python -m unittest test_effects.py
Every test fails on the starter and passes once the TODOs are done."""
import unittest
from math import sqrt

from effects import by_server, cohens_d, fisher_ci, load, verdict


class TestCohensD(unittest.TestCase):
    def test_hand_example(self):
        # both groups have SD 1, means differ by 1
        self.assertAlmostEqual(cohens_d([1, 2, 3], [2, 3, 4]), 1.0, places=12)

    def test_sign_and_unequal_groups(self):
        self.assertAlmostEqual(cohens_d([2, 4, 6, 8], [1, 3]), -3 / sqrt(22 / 4), places=12)

    def test_lab_data_pooled(self):
        rows = load()
        a = [r["wellbeing"] for r in rows if r["voice_chat"] == 0]
        b = [r["wellbeing"] for r in rows if r["voice_chat"] == 1]
        self.assertAlmostEqual(cohens_d(a, b), 0.17135, places=4)


class TestVerdict(unittest.TestCase):
    def test_lecture_rows(self):
        cases = [(0.05, 100, "inconclusive"), (0.05, 1000, "no meaningful effect"),
                 (0.05, 10000, "real but trivial"), (0.05, 100000, "real but trivial"),
                 (0.30, 1000, "meaningful")]
        for d, n, want in cases:
            self.assertEqual(verdict(d, sqrt(2 / n), 0.20), want, (d, n))

    def test_negative_effects(self):
        self.assertEqual(verdict(-0.30, sqrt(2 / 1000), 0.20), "meaningful")
        self.assertEqual(verdict(-0.05, sqrt(2 / 10000), 0.20), "real but trivial")


class TestFisher(unittest.TestCase):
    def test_lecture_value(self):
        lo, hi = fisher_ci(0.10, 2500)
        self.assertAlmostEqual(lo, 0.0610, places=3)
        self.assertAlmostEqual(hi, 0.1387, places=3)

    def test_symmetric_in_z_not_r(self):
        lo, hi = fisher_ci(0.8, 50)
        self.assertGreater(0.8 - lo, hi - 0.8)


class TestByServer(unittest.TestCase):
    def test_lab_data(self):
        got = by_server(load())
        self.assertEqual(list(got), ["A", "B", "C"])
        want = {"A": 0.09890, "B": -0.03602, "C": 0.10552}
        for s, d in want.items():
            self.assertAlmostEqual(got[s][0], d, places=4)
            self.assertTrue(0.04 < got[s][1] < 0.06)


if __name__ == "__main__":
    unittest.main()
