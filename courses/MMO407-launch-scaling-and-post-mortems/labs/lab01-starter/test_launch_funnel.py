"""MMO407 lab 01 tests. Run with: python -m unittest test_launch_funnel.py
Every test fails on the starter and passes once the TODOs are done."""
import unittest

from launch_funnel import (LECTURE_ARRIVALS, LECTURE_PLANS, LECTURE_STAGES,
                           apply_kill_switches, availability, backlog,
                           simulate_retries, throughput)


class TestFunnel(unittest.TestCase):
    def test_lecture_plans(self):
        expected = {"as built": ("authentication", 600, 24000),
                    "2x character select": ("authentication", 600, 24000),
                    "2x authentication": ("world entry", 900, 6000),
                    "2x auth + 2x world entry": ("authentication", 1000, 0)}
        for label, change in LECTURE_PLANS.items():
            s = {**LECTURE_STAGES, **change}
            name, x = throughput(s, LECTURE_ARRIVALS)
            self.assertEqual((name, x, backlog(s, LECTURE_ARRIVALS, 60)), expected[label], label)

    def test_arrivals_below_every_stage(self):
        self.assertEqual(throughput({"a": 500, "b": 300}, 200), ("b", 200))
        self.assertEqual(backlog({"a": 500, "b": 300}, 200, 60), 0)


class TestRetries(unittest.TestCase):
    def test_matches_lecture_table(self):
        log = simulate_retries(600, 1000, 6)
        self.assertAlmostEqual(log[0][1], 555.6, places=1)
        self.assertAlmostEqual(log[2][0], 2975, delta=1)
        self.assertAlmostEqual(log[2][1], 336.1, places=1)
        self.assertAlmostEqual(log[4][1], 8.2, places=1)
        self.assertEqual(log[5][1], 0)

    def test_free_rejections_do_not_collapse(self):
        log = simulate_retries(600, 1000, 30, reject_cost=0.0)
        self.assertTrue(all(abs(ok - 600) < 1e-9 for _, ok in log))


class TestAvailability(unittest.TestCase):
    def test_product(self):
        self.assertAlmostEqual(availability([0.995] * 8), 0.9607, places=4)
        self.assertAlmostEqual(availability([0.995] * 12), 0.9416, places=4)

    def test_kill_switches(self):
        svc = {"auth": 0.999, "world": 0.998, "store": 0.99, "friends": 0.99}
        left = apply_kill_switches(svc, {"store", "friends"})
        self.assertEqual(set(left), {"auth", "world"})
        self.assertAlmostEqual(availability(left.values()), 0.999 * 0.998)


if __name__ == "__main__":
    unittest.main()
