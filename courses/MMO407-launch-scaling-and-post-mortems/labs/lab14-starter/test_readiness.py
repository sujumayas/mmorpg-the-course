"""MMO407 lab 14 tests. Run with: python -m unittest test_readiness.py
Every test fails on the starter and passes once the TODOs are done."""
import unittest

from readiness import (LECTURE_CRITERIA as CR, LECTURE_PLANS as PL, failed_gates,
                       geometric_score, smallest_fix, verdict, weighted_score)


def variant(plan, name, score):
    """A copy of `plan` with one criterion's score changed."""
    return {**plan, name: score}


class TestScores(unittest.TestCase):
    def test_weighted(self):
        self.assertAlmostEqual(weighted_score(CR, PL["A"]), 11 / 12)
        self.assertAlmostEqual(weighted_score(CR, PL["B"]), 0.85)
        self.assertAlmostEqual(weighted_score(CR, PL["C"]), 10.4 / 12)

    def test_geometric(self):
        self.assertEqual(geometric_score(CR, PL["A"]), 0.0)
        self.assertAlmostEqual(geometric_score(CR, PL["C"]), 0.8631, places=4)
        self.assertAlmostEqual(geometric_score(CR, variant(PL["A"], "low-end platform", 0.1)), 0.8254, places=4)

    def test_missing_evidence_is_zero(self):
        plan = variant(PL["B"], "restore drill", None)
        self.assertAlmostEqual(weighted_score(CR, plan), (0.85 * 10) / 12)
        self.assertEqual(geometric_score(CR, plan), 0.0)
        self.assertEqual(failed_gates(CR, plan), ["restore drill"])


class TestGates(unittest.TestCase):
    def test_lecture_plans(self):
        self.assertEqual(failed_gates(CR, PL["A"]), ["low-end platform"])
        self.assertEqual(failed_gates(CR, PL["B"]), [])
        self.assertEqual(failed_gates(CR, PL["C"]), [])

    def test_three_rules_disagree_on_a(self):
        a01 = variant(PL["A"], "low-end platform", 0.1)
        self.assertEqual([verdict(CR, a01, r) for r in ("average", "geometric", "gated")],
                         ["go", "go", "no-go"])
        c04 = variant(PL["C"], "beta exposure", 0.4)
        self.assertEqual([verdict(CR, c04, r) for r in ("average", "geometric", "gated")],
                         ["go", "no-go", "go"])


class TestSmallestFix(unittest.TestCase):
    def test_gate_only(self):
        self.assertEqual(smallest_fix(CR, PL["A"]), {"low-end platform": 0.7})
        self.assertEqual(smallest_fix(CR, PL["B"]), {})

    def test_gate_then_weight(self):
        plan = {name: 0.8 for name in CR}
        plan["restore drill"] = 0.5
        fix = smallest_fix(CR, plan)
        self.assertEqual(set(fix), {"restore drill", "capacity"})
        self.assertAlmostEqual(fix["restore drill"], 0.7)
        self.assertAlmostEqual(fix["capacity"], 0.8 + 0.2 / 3)
        fixed = {**plan, **fix}
        self.assertEqual(verdict(CR, fixed, "gated"), "go")

    def test_impossible(self):
        self.assertIsNone(smallest_fix(CR, PL["B"], threshold=1.01))


if __name__ == "__main__":
    unittest.main()
