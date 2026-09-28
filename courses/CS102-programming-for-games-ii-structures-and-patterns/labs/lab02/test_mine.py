"""CS102 Lab 02: the one shipped test that FAILS on the starter.

make("mine") raises ValueError until you add the mine in step 6. Keep this file
unchanged; add your own mine and totem tests to test_behaviour.py.
Run with: python -m unittest -v
"""
import unittest

from entities import World, make


class TestMine(unittest.TestCase):
    def test_mine_explodes_on_first_overlap(self):
        w = World()
        mine = w.add(make("mine", 0, 0))          # must not raise
        gob = w.add(make("goblin", 0, 0))         # same spot: overlaps at any radius
        self.assertIsNone(mine.draw())            # mines are invisible
        w.step(0.1)
        self.assertTrue(mine.exploded)            # first step with an overlap
        self.assertEqual(gob.hp, 0)               # 30 blast damage, goblin has 30 HP


if __name__ == "__main__":
    unittest.main()
