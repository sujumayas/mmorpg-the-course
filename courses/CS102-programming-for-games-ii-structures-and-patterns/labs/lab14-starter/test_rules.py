"""CS102 Lab 14 test suite. Run from this folder:  python -m unittest -v

Two example tests are written for you. Add the rest (see the lab sheet)."""
import unittest

from fakes import ScriptedRng
from rules import damage_after_armor, is_crit, rage_bonus, xp_to_next, split_gold, regen


class DamageAfterArmorExamples(unittest.TestCase):
    def test_armor_subtracts(self):
        self.assertEqual(damage_after_armor(20, 5), 15)

    def test_armor_bigger_than_hit_leaves_one(self):
        self.assertEqual(damage_after_armor(5, 20), 1)


# TODO Part A: a property test for damage_after_armor over raw 1..100, armor 0..100.
# TODO Part A: injected-roll tests for is_crit at chance 0.0, 0.25 and 1.0.
# TODO Part A: property tests for rage_bonus, xp_to_next, split_gold and regen.
# TODO Part B: data tests over ../lab13-starter/weapons.csv (or your own lab 13 folder).
# TODO Part C: a replay test using fight.py and replay_30s.json.


if __name__ == "__main__":
    unittest.main()
