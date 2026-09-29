"""Tests for PR101 lab 09. Do not edit. Run: python -m unittest test_cone -v"""
import os
import unittest

import cone

HERE = os.path.dirname(os.path.abspath(__file__))


def row(task, hour, spent, rem, status, team="Z"):
    return {"team": team, "task": task, "hour": float(hour), "spent": float(spent),
            "remaining_est": float(rem), "status": status}


# The enemy-spawner task from lecture section 2.
SPAWNER = [row("S", 0, 0, 3, "open"), row("S", 6, 2, 2, "open"), row("S", 12, 5, 1, "open"),
           row("S", 18, 7, 1.5, "open"), row("S", 24, 8, 0, "done")]
CUT = [row("C", 0, 0, 2, "open"), row("C", 6, 1, 2, "open"), row("C", 12, 1.5, 0, "cut")]
CLAIM = [row("Q", 0, 0, 2, "open"), row("Q", 6, 2, 0, "open"), row("Q", 12, 3, 0, "done")]


class TestRatios(unittest.TestCase):
    def test_spawner_ratios(self):
        got = cone.checkpoint_ratios(SPAWNER)
        want = [(0.0, 8 / 3, 8 / 3), (0.25, 2.0, 3.0), (0.625, 8 / 6, 3.0), (0.875, 8 / 8.5, 1 / 1.5)]
        self.assertEqual(len(got), 4)
        for g, w in zip(got, want):
            for a, b in zip(g, w):
                self.assertAlmostEqual(a, b, places=9)

    def test_cut_task_has_no_ratios(self):
        self.assertEqual(cone.checkpoint_ratios(CUT), [])

    def test_zero_claim_skipped_and_counted(self):
        self.assertEqual(len(cone.checkpoint_ratios(CLAIM)), 1)
        self.assertEqual(cone.zero_claims(SPAWNER + CUT + CLAIM), 1)


class TestBands(unittest.TestCase):
    def test_band_inclusive(self):
        p10, p50, p90 = cone.band(list(range(1, 11)))
        self.assertAlmostEqual(p10, 1.9)
        self.assertAlmostEqual(p50, 5.5)
        self.assertAlmostEqual(p90, 9.1)

    def test_initial_bias(self):
        # finished tasks: S (8 / 3) and Q (3 / 2); median of two values is their mean
        self.assertAlmostEqual(cone.initial_bias(SPAWNER + CUT + CLAIM), (8 / 3 + 1.5) / 2)


class TestConeTable(unittest.TestCase):
    def setUp(self):
        self.rows = cone.load_log(os.path.join(HERE, "jam_log_sample.csv"))
        self.table = cone.cone_table(self.rows)

    def test_bins_cover_every_point(self):
        pts = sum(len(cone.checkpoint_ratios(h)) for h in cone.task_histories(self.rows).values())
        self.assertEqual(len(self.table), 4)
        self.assertEqual(sum(b["n"] for b in self.table), pts)
        self.assertEqual([b["lo"] for b in self.table], [0.0, 0.25, 0.5, 0.75])

    def test_total_view_narrows_remaining_view_does_not(self):
        first, last = self.table[0], self.table[-1]
        spread = lambda t: t[2] / t[0]
        self.assertLess(spread(last["total"]), spread(first["total"]))
        self.assertGreater(spread(last["remaining"]), 2.0)

    def test_small_bin_is_none(self):
        t = cone.cone_table(SPAWNER, edges=(0.0, 0.5, 1.0))
        self.assertEqual(t[0]["n"], 2)
        self.assertIsNotNone(t[0]["total"])
        t = cone.cone_table(SPAWNER, edges=(0.0, 0.1, 1.0))
        self.assertEqual(t[0]["n"], 1)
        self.assertIsNone(t[0]["total"])


if __name__ == "__main__":
    unittest.main()
