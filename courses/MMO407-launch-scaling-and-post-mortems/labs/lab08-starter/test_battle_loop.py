"""MMO407 lab 08 tests. Run with: python -m unittest test_battle_loop.py
Every test fails on the starter and passes once the TODOs are done."""
import unittest

from battle_loop import battle, fit_rate, objective_for_length


class TestLectureBattle(unittest.TestCase):
    def test_defaults(self):
        b = battle()
        self.assertEqual(b["T"], 419)
        self.assertEqual(b["n_end"], 6000)
        self.assertAlmostEqual(b["pilot_hours"], 31441.67, delta=0.5)
        self.assertTrue(b["decided"])
        self.assertEqual(b["floor_min"], 318)

    def test_undilated(self):
        b = battle(dilate=False)
        self.assertEqual((b["T"], b["n_end"]), (60, 2200))
        self.assertEqual(b["floor_min"], 0)


class TestLevers(unittest.TestCase):
    def test_arrivals_capacity_pool(self):
        self.assertEqual(battle(r=10)["T"], 240)
        self.assertEqual(battle(C=2.0)["T"], 146)
        self.assertEqual(battle(pool=3000)["T"], 416)
        self.assertEqual(battle(G=30)["n_end"], 3380)

    def test_deadline(self):
        b = battle(deadline=240)
        self.assertEqual(b["T"], 240)
        self.assertFalse(b["decided"])
        self.assertAlmostEqual(b["game"], 42.18, delta=0.01)


class TestPlanning(unittest.TestCase):
    def test_fit_rate(self):
        self.assertAlmostEqual(fit_rate([(0, 1000), (60, 2200)]), 20.0)
        self.assertAlmostEqual(fit_rate([(0, 0), (1, 1), (2, 5)]), 2.5)

    def test_objective_for_length(self):
        self.assertEqual(objective_for_length(120, n0=1000, r=15, pool=4000), 36)
        self.assertIsNone(objective_for_length(10**6, n0=1000, r=15, pool=4000))


if __name__ == "__main__":
    unittest.main()
