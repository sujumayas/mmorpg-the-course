"""MMO407 lab 13 tests. Run with: python -m unittest test_launch_risk.py
Every test fails on the starter and passes once the TODOs are done."""
import unittest

from launch_risk import (LECTURE_D, LECTURE_FIXES, LECTURE_RISKS, apply_fixes,
                         choose, exceedance, expected_loss, loss_distribution,
                         scenario_distribution)


def plan(chosen):
    return loss_distribution(apply_fixes(LECTURE_RISKS, LECTURE_FIXES, chosen))


class TestDistribution(unittest.TestCase):
    def test_sums_to_one_and_mean(self):
        dist = loss_distribution(LECTURE_RISKS)
        self.assertAlmostEqual(sum(dist.values()), 1.0)
        self.assertAlmostEqual(expected_loss(dist), 115.0)
        self.assertAlmostEqual(dist[0], 0.2 * 0.6 * 0.95 * 0.98)
        self.assertEqual(max(dist), 1625)

    def test_merges_equal_totals(self):
        dist = loss_distribution({"a": (0.5, 10), "b": (0.5, 10)})
        self.assertEqual(dist, {0: 0.25, 10: 0.5, 20: 0.25})


class TestTail(unittest.TestCase):
    def test_lecture_table(self):
        expected = {(): (115.0, 0.069), ("M1", "M2"): (62.5, 0.069),
                    ("M1", "M3"): (63.0, 0.020), ("M3", "M4"): (75.0, 0.0)}
        for chosen, (e, p) in expected.items():
            dist = plan(chosen)
            self.assertAlmostEqual(expected_loss(dist), e, places=6)
            self.assertAlmostEqual(exceedance(dist, LECTURE_D), p, places=6)

    def test_strictly_greater(self):
        dist = loss_distribution({"a": (0.5, 300)})
        self.assertEqual(exceedance(dist, 300), 0)
        self.assertAlmostEqual(exceedance(dist, 299), 0.5)
        self.assertAlmostEqual(exceedance(plan(()), 100), 1 - 0.68 * 0.931, places=6)


class TestChoose(unittest.TestCase):
    def test_three_rules(self):
        args = (LECTURE_RISKS, LECTURE_FIXES, 2, LECTURE_D)
        self.assertEqual(choose(*args, rule="expected"), ("M1", "M2"))
        self.assertEqual(choose(*args, rule="penalty", B=100), ("M1", "M3"))
        self.assertEqual(choose(*args, rule="penalty", B=1000), ("M3", "M4"))
        self.assertEqual(choose(*args, rule="limit", max_p=0.0), ("M3", "M4"))
        self.assertEqual(choose(*args, rule="limit", max_p=0.03), ("M1", "M3"))

    def test_budget_three_and_none(self):
        self.assertEqual(choose(LECTURE_RISKS, LECTURE_FIXES, 3, LECTURE_D, rule="limit"),
                         ("M1", "M3", "M4"))
        self.assertIsNone(choose(LECTURE_RISKS, LECTURE_FIXES, 1, LECTURE_D, rule="limit"))


class TestScenario(unittest.TestCase):
    def test_same_mean_fatter_joint_tail(self):
        dist = scenario_distribution(LECTURE_RISKS, 0.1, {"queues", "auth"})
        self.assertAlmostEqual(sum(dist.values()), 1.0)
        self.assertAlmostEqual(expected_loss(dist), 115.0)
        self.assertAlmostEqual(exceedance(dist, 100), 1 - (1 - 1 / 3) * 0.931, places=6)

    def test_zero_scenario_is_independent(self):
        a = scenario_distribution(LECTURE_RISKS, 0.0, {"queues", "auth"})
        b = loss_distribution(LECTURE_RISKS)
        self.assertEqual(set(a), set(b))
        for k in a:
            self.assertAlmostEqual(a[k], b[k])


if __name__ == "__main__":
    unittest.main()
