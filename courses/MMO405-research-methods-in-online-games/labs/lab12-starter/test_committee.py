"""MMO405 lab 12 tests. Run with: python -m unittest test_committee.py
Every test fails on the starter and passes once the TODOs are done."""
import unittest

from committee import both_accept, reviewers_needed, simulate, spearman_brown, summarize


class TestReliability(unittest.TestCase):
    def test_spearman_brown(self):
        self.assertAlmostEqual(spearman_brown(0.4, 4), 1.6 / 2.2, places=12)
        self.assertAlmostEqual(spearman_brown(0.29, 1), 0.29, places=12)
        self.assertAlmostEqual(spearman_brown(0.29, 3), 0.87 / 1.58, places=12)

    def test_reviewers_needed(self):
        self.assertEqual(reviewers_needed(0.4, 0.8), 6)
        self.assertEqual(reviewers_needed(0.29, 0.9), 23)
        self.assertEqual(reviewers_needed(0.9, 0.5), 1)


class TestFormula(unittest.TestCase):
    def test_pure_noise(self):
        for a in (0.1, 0.26, 0.5):
            self.assertAlmostEqual(both_accept(a, 0.0), a * a, places=6)

    def test_lecture_values(self):
        self.assertAlmostEqual(both_accept(0.26, 0.55) / 0.26, 0.517, places=3)
        self.assertAlmostEqual(both_accept(0.10, 0.55) / 0.10, 0.356, places=3)
        self.assertEqual(both_accept(0.3, 1.0), 0.3)


class TestSimulation(unittest.TestCase):
    def test_table_shape(self):
        t = simulate(166, 0.26, 0.55, seed=3)
        self.assertEqual(set(t), {"AA", "AR", "RA", "RR"})
        self.assertEqual(sum(t.values()), 166)
        self.assertEqual(t["AA"] + t["AR"], round(0.26 * 166))
        self.assertEqual(t["AA"] + t["RA"], round(0.26 * 166))

    def test_summarize_neurips_table(self):
        p, inc = summarize({"AA": 22, "AR": 21, "RA": 22, "RR": 101})
        self.assertAlmostEqual(p, 22 / 43.5, places=12)
        self.assertAlmostEqual(inc, 43 / 166, places=12)

    def test_large_simulation_matches_formula(self):
        p, inc = summarize(simulate(20000, 0.26, 0.55, seed=1))
        self.assertAlmostEqual(p, both_accept(0.26, 0.55) / 0.26, delta=0.02)
        self.assertAlmostEqual(inc, 2 * (0.26 - both_accept(0.26, 0.55)), delta=0.02)


if __name__ == "__main__":
    unittest.main()
