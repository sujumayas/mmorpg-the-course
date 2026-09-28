"""CS102 Lab 01 tests. Run with: python -m unittest -v"""
import random
import unittest
from fractions import Fraction

from stats import Fighter, StatStages


class TestMultiplier(unittest.TestCase):
    def test_table(self):
        expected = {
            -6: Fraction(2, 8), -5: Fraction(2, 7), -4: Fraction(2, 6),
            -3: Fraction(2, 5), -2: Fraction(2, 4), -1: Fraction(2, 3),
            0: Fraction(1), 1: Fraction(3, 2), 2: Fraction(2), 3: Fraction(5, 2),
            4: Fraction(3), 5: Fraction(7, 2), 6: Fraction(4),
        }
        for stage, mult in expected.items():
            s = StatStages()
            s.change(stage)
            self.assertEqual(s.stage, stage)
            self.assertEqual(s.multiplier, mult, f"stage {stage}")


class TestChange(unittest.TestCase):
    def test_sharpen_four_times(self):
        s = StatStages()
        self.assertEqual([s.change(2) for _ in range(4)], [2, 2, 2, 0])
        self.assertEqual(s.stage, 6)

    def test_simple(self):
        s = StatStages("simple")
        self.assertEqual(s.change(2), 4)
        self.assertEqual(s.change(2), 2)
        self.assertEqual(s.stage, 6)

    def test_contrary(self):
        s = StatStages("contrary")
        self.assertEqual([s.change(2) for _ in range(4)], [-2, -2, -2, 0])
        self.assertEqual(s.multiplier, Fraction(1, 4))

    def test_contrary_near_floor(self):
        s = StatStages("contrary")
        s.change(5)                      # becomes -5
        self.assertEqual(s.change(2), -1)
        self.assertEqual(s.stage, -6)

    def test_reset(self):
        s = StatStages()
        s.change(3)
        s.reset()
        self.assertEqual(s.stage, 0)

    def test_stage_is_read_only(self):
        s = StatStages()
        with self.assertRaises(AttributeError):
            s.stage = 9

    def test_invariant_under_random_play(self):
        rng = random.Random(102)
        for ability in (None, "simple", "contrary"):
            s = StatStages(ability)
            for _ in range(2000):
                before = s.stage
                applied = s.change(rng.randint(-3, 3))
                self.assertTrue(StatStages.MIN <= s.stage <= StatStages.MAX)
                self.assertEqual(s.stage - before, applied)


class TestFighter(unittest.TestCase):
    def test_damage_and_heal(self):
        f = Fighter("Knight", 120, 50)
        self.assertEqual(f.take_damage(80), 80)
        self.assertEqual(f.heal(100), 80)
        self.assertEqual(f.hp, 120)

    def test_overkill(self):
        f = Fighter("Knight", 120, 50)
        self.assertEqual(f.take_damage(500), 120)
        self.assertEqual(f.hp, 0)
        self.assertFalse(f.is_alive)

    def test_no_heal_when_down(self):
        f = Fighter("Knight", 120, 50)
        f.take_damage(120)
        self.assertEqual(f.heal(50), 0)
        self.assertEqual(f.hp, 0)

    def test_negative_amounts_rejected(self):
        f = Fighter("Knight", 120, 50)
        with self.assertRaises(ValueError):
            f.take_damage(-5)
        with self.assertRaises(ValueError):
            f.heal(-5)

    def test_effective_attack(self):
        f = Fighter("Knight", 120, 50)
        f.attack.change(2)
        self.assertEqual(f.effective_attack(), 100)
        f.attack.change(-3)
        self.assertEqual(f.effective_attack(), Fraction(100, 3))

    def test_hp_is_read_only(self):
        f = Fighter("Knight", 120, 50)
        with self.assertRaises(AttributeError):
            f.hp = 9000

    def test_separate_objects(self):
        a = Fighter("A", 100, 10)
        b = Fighter("B", 100, 10)
        a.attack.change(2)
        self.assertEqual(b.attack.stage, 0)


if __name__ == "__main__":
    unittest.main()
