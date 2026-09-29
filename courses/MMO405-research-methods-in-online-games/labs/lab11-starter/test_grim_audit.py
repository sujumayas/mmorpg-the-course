"""MMO405 lab 11 tests. Run with: python -m unittest test_grim_audit.py
Every test fails on the starter and passes once the TODOs are done."""
import unittest

from grim_audit import audit_means, grim, load_means, nearest_possible, p_consistent, t_two_sided_p


class TestGrim(unittest.TestCase):
    def test_lecture_rows(self):
        self.assertFalse(grim(3.47, 28))
        self.assertTrue(grim(3.46, 28))
        self.assertTrue(grim(3.47, 28, 4))
        self.assertFalse(grim(2.15, 45))
        self.assertTrue(grim(4.12, 60))

    def test_float_edge(self):
        # 0.29 * 100 is 28.999999999999996 in floating point; 29/100 must still pass.
        self.assertTrue(grim(0.29, 100))
        self.assertTrue(grim(4.05, 22))
        self.assertFalse(grim(0.537, 40, 1, 3))

    def test_nearest(self):
        self.assertEqual(nearest_possible(3.47, 28), (3.46, 3.5))
        self.assertEqual(nearest_possible(2.15, 45), (2.13, 2.16))


class TestP(unittest.TestCase):
    def test_provided_t(self):
        # Large df approaches the normal; df = 1 is the Cauchy distribution.
        self.assertAlmostEqual(t_two_sided_p(1.959964, 10**7), 0.05, places=5)
        self.assertAlmostEqual(t_two_sided_p(1.0, 1), 0.5, places=10)
        self.assertTrue(p_consistent(1.0, 1, "=", 0.5, 3))

    def test_equal_and_less(self):
        p = t_two_sided_p(2.31, 26)
        self.assertEqual(p_consistent(2.31, 26, "=", round(p, 3), 3), True)
        self.assertEqual(p_consistent(2.31, 26, "=", round(p, 3) + 0.002, 3), False)
        self.assertEqual(p_consistent(4.10, 27, "<", 0.001, 3), True)
        self.assertEqual(p_consistent(1.50, 27, "<", 0.05, 3), False)


class TestAudit(unittest.TestCase):
    def test_statuses(self):
        rows = [{"id": "a", "mean": 3.47, "n": 28, "items": 1, "decimals": 2},
                {"id": "b", "mean": 3.46, "n": 28, "items": 1, "decimals": 2},
                {"id": "c", "mean": 3.47, "n": 28, "items": 4, "decimals": 2}]
        self.assertEqual(audit_means(rows), [("a", "inconsistent"), ("b", "consistent"), ("c", "untestable")])

    def test_manuscript_has_problems(self):
        status = dict(audit_means(load_means()))
        self.assertEqual(len(status), 8)
        self.assertIn("inconsistent", status.values())
        self.assertIn("untestable", status.values())


if __name__ == "__main__":
    unittest.main()
