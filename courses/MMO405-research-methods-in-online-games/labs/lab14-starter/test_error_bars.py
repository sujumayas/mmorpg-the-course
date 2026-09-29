"""MMO405 lab 14 tests. Run with: python -m unittest test_error_bars.py
Every test fails on the starter and passes once the TODOs are done."""
import unittest
from math import sqrt

from error_bars import audit_slide, diff_test, load_slides, se_from_bar


class TestSE(unittest.TestCase):
    def test_bar_types(self):
        self.assertAlmostEqual(se_from_bar(0.4, "SE"), 0.4)
        self.assertAlmostEqual(se_from_bar(0.784, "CI95"), 0.4)
        self.assertAlmostEqual(se_from_bar(4.0, "SD", n=100), 0.4)

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            se_from_bar(1.0, "SD")
        with self.assertRaises(ValueError):
            se_from_bar(1.0, "IQR")


class TestDiff(unittest.TestCase):
    def test_lecture_table(self):
        # means d SEs apart, equal SE 1: p from the week 14 table
        for dist, p in [(2.0, 0.1573), (3.0, 0.0339), (2 * 1.96, 0.0056), (1.5 * 1.96, 0.0376)]:
            self.assertAlmostEqual(diff_test(0, 1, dist, 1)[3], p, places=4)

    def test_slide_case(self):
        diff, se, z, p = diff_test(6.0, 0.4, 7.2, 0.4)
        self.assertAlmostEqual(se, 0.4 * sqrt(2))
        self.assertAlmostEqual(z, 2.1213, places=4)

    def test_paired(self):
        diff, se, z, p = diff_test(42.0, 1.0, 40.5, 1.0, paired=True, rho=0.9)
        self.assertAlmostEqual(se, 0.4472, places=4)
        self.assertAlmostEqual(z, -3.354, places=3)
        self.assertLess(p, 0.001)

    def test_paired_rho_zero_equals_independent(self):
        self.assertAlmostEqual(diff_test(1, 0.5, 2, 0.5, paired=True, rho=0.0)[1],
                               diff_test(1, 0.5, 2, 0.5)[1])


class TestAudit(unittest.TestCase):
    def setUp(self):
        self.slides = {s["id"]: s for s in load_slides()}

    def test_slide1_overlap_but_significant(self):
        a = audit_slide(self.slides["slide1"])
        self.assertEqual(a["looks"], "overlap")
        self.assertAlmostEqual(a["p"], 0.034, delta=0.001)
        self.assertFalse(a["supported"])

    def test_slide2_gap_not_significant(self):
        a = audit_slide(self.slides["slide2"])
        self.assertEqual(a["looks"], "gap")
        self.assertAlmostEqual(a["p"], 0.120, delta=0.001)
        self.assertFalse(a["supported"])

    def test_slide3_paired(self):
        a = audit_slide(self.slides["slide3"])
        self.assertTrue(a["significant"])
        self.assertFalse(a["supported"])

    def test_slide4_sd_bars(self):
        a = audit_slide(self.slides["slide4"])
        self.assertEqual(a["looks"], "overlap")
        self.assertTrue(a["significant"])
        self.assertFalse(a["supported"])

    def test_slide5_difference_of_effects(self):
        a = audit_slide(self.slides["slide5"])
        self.assertEqual(a["looks"], "one significant, one not")
        self.assertAlmostEqual(a["p"], 0.239, delta=0.001)
        self.assertFalse(a["supported"])

    def test_slide6_supported(self):
        a = audit_slide(self.slides["slide6"])
        self.assertEqual(a["looks"], "gap")
        self.assertTrue(a["supported"])


if __name__ == "__main__":
    unittest.main()
