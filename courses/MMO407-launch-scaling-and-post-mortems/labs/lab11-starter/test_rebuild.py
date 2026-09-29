"""MMO407 lab 11 tests. Run with: python -m unittest test_rebuild.py
Every test fails on the starter and passes once TODOs 1-3 are done."""
import unittest

from rebuild import (LECTURE, completeness, find_kink, fit, load_history,
                     rebuild_hours, rebuild_weeks)


class TestRebuild(unittest.TestCase):
    def test_lecture_table(self):
        expected = {1.0: 450, 0.9: 585, 0.8: 720, 0.6: 990, 0.4: 1260}
        for q, weeks in expected.items():
            self.assertAlmostEqual(rebuild_weeks(q=q, **LECTURE), weeks)

    def test_protocol_document_only_cheapens_evidence(self):
        # the in-class activity, option (b): w_evidence 40, guesses still cost 4 x 60
        self.assertAlmostEqual(rebuild_hours(2_000, 60, 4, 0.55, w_evidence=40), 260_000)
        self.assertAlmostEqual(rebuild_hours(2_000, 60, 4, 0.85, w_evidence=40), 140_000)


class TestCurve(unittest.TestCase):
    def test_kink_and_end(self):
        L = LECTURE
        self.assertAlmostEqual(completeness(0, q=0.8, **L), 0.0)
        self.assertAlmostEqual(completeness(180, q=0.8, **L), 0.4)
        self.assertAlmostEqual(completeness(360, q=0.8, **L), 0.8)
        self.assertAlmostEqual(completeness(540, q=0.8, **L), 0.9)
        self.assertAlmostEqual(completeness(720, q=0.8, **L), 1.0)
        self.assertAlmostEqual(completeness(2_000, q=0.8, **L), 1.0)
        self.assertAlmostEqual(completeness(450, q=1.0, **L), 1.0)


class TestFit(unittest.TestCase):
    def test_history(self):
        hist = load_history()
        self.assertEqual(find_kink(hist), 364)
        q, g = fit(hist)
        self.assertAlmostEqual(q, 0.56)
        self.assertAlmostEqual(g, 4.0, places=6)


if __name__ == "__main__":
    unittest.main()
