"""MMO405 lab 13 tests. Run with: python -m unittest test_replication.py
Every test fails on the starter and passes once the TODOs are done."""
import unittest

from replication import expected_published, load_pairs, power, replication_n, verdicts


class TestFilter(unittest.TestCase):
    def test_lecture_table(self):
        # (n, power, mean published d) from the week 13 table, true effect 0.20
        for n, pw, pub in [(20, 0.092, 0.767), (50, 0.169, 0.499), (100, 0.293, 0.366),
                           (200, 0.516, 0.277), (400, 0.807, 0.224), (1000, 0.994, 0.201)]:
            self.assertAlmostEqual(power(0.20, n), pw, delta=0.0006)
            self.assertAlmostEqual(expected_published(0.20, n), pub, delta=0.0006)

    def test_null_effect(self):
        self.assertAlmostEqual(power(0.0, 50), 0.025, delta=0.0002)
        self.assertAlmostEqual(expected_published(0.0, 50), 0.4676, delta=0.0005)

    def test_published_never_below_truth(self):
        for delta in (0.0, 0.1, 0.3, 0.6):
            for n in (10, 100, 1000):
                self.assertGreaterEqual(expected_published(delta, n), delta)


class TestVerdicts(unittest.TestCase):
    def test_lecture_case(self):
        v = verdicts(0.48, 50, 0.12, 250, sesoi=0.20)
        self.assertFalse(v["sig_same_sign"])
        self.assertFalse(v["captured"])
        self.assertAlmostEqual(v["telescope_p"], 0.020, delta=0.001)
        self.assertTrue(v["too_small"])
        self.assertFalse(v["equivalent"])
        self.assertAlmostEqual(v["pooled_d"], 0.180, places=6)
        self.assertAlmostEqual(v["pooled_p"], 0.027, delta=0.001)

    def test_clean_replication(self):
        v = verdicts(0.30, 400, 0.28, 400)
        self.assertTrue(v["sig_same_sign"])
        self.assertTrue(v["captured"])
        self.assertFalse(v["too_small"])
        self.assertFalse(v["equivalent"])

    def test_opposite_sign_is_not_a_success(self):
        v = verdicts(0.50, 50, -0.30, 1000)
        self.assertFalse(v["sig_same_sign"])

    def test_equivalent_null(self):
        v = verdicts(0.60, 40, 0.01, 2000, sesoi=0.10)
        self.assertTrue(v["equivalent"])
        self.assertTrue(v["too_small"])

    def test_lab_data(self):
        pairs = {p["study"]: p for p in load_pairs()}
        s06 = pairs["S06"]
        v = verdicts(s06["d_orig"], s06["n_orig"], s06["d_rep"], s06["n_rep"])
        self.assertTrue(v["sig_same_sign"] and v["captured"])
        s11 = pairs["S11"]
        v = verdicts(s11["d_orig"], s11["n_orig"], s11["d_rep"], s11["n_rep"])
        self.assertTrue(v["too_small"])


class TestPlanning(unittest.TestCase):
    def test_ratio(self):
        self.assertEqual(replication_n(50), 134)
        self.assertEqual(replication_n(30), 81)

    def test_higher_power_needs_more(self):
        self.assertGreater(replication_n(50, 0.95), replication_n(50, 0.80))


if __name__ == "__main__":
    unittest.main()
