"""CS102 Lab 02 behaviour tests. They must pass before, during and after your refactor.

Run with: python -m unittest -v
The tests use only entities.make(), entities.World and these members of an object:
name, x, y, hp, removed, exploded (for exploders), target, update(dt), take_damage(n),
draw(), overlaps(other).
"""
import unittest

from entities import World, make


class TestBehaviour(unittest.TestCase):
    def setUp(self):
        self.w = World()

    def test_bush_draws_and_ignores_damage(self):
        b = self.w.add(make("bush", 1, 2))
        self.assertEqual(b.draw(), "bush@(1.0,2.0)")
        self.assertEqual(b.take_damage(10), 0)
        self.assertIsNone(b.hp)

    def test_trigger_is_invisible_but_collides(self):
        t = self.w.add(make("trigger"))
        g = self.w.add(make("goblin", 1.5, 0))
        self.assertIsNone(t.draw())
        self.assertTrue(t.overlaps(g))

    def test_crate_breaks(self):
        c = self.w.add(make("crate"))
        self.assertEqual(c.take_damage(15), 15)
        self.assertEqual(c.take_damage(15), 5)
        self.assertTrue(c.removed)
        self.assertEqual(self.w.events, ["Crate takes 15", "Crate takes 5", "Crate is destroyed"])

    def test_goblin_chases(self):
        g = self.w.add(make("goblin", 0, 0))
        target = self.w.add(make("bush", 10, 0))
        g.target = target
        for _ in range(10):
            self.w.step(0.1)
        self.assertAlmostEqual(g.x, 2.0)
        self.assertAlmostEqual(g.y, 0.0)

    def test_grenade_fuse(self):
        gr = self.w.add(make("grenade", 0, 0))
        crate = self.w.add(make("crate", 6, 0))
        for _ in range(10):
            self.w.step(0.1)
        self.assertAlmostEqual(gr.x, 4.0, places=6)
        self.assertTrue(gr.exploded)
        self.assertEqual(crate.hp, 0)
        self.assertIn("Grenade explodes", self.w.events)

    def test_barrel_chain(self):
        b1 = self.w.add(make("barrel", 0, 0))
        b2 = self.w.add(make("barrel", 3, 0))
        gob = self.w.add(make("goblin", 20, 0))
        b1.take_damage(10)
        self.w.step(0.016)
        self.w.step(0.016)
        self.assertTrue(b1.exploded and b2.exploded)
        self.assertEqual(gob.hp, 30)
        self.assertEqual(self.w.events, [
            "Barrel takes 10", "Barrel explodes", "Barrel takes 10", "Barrel explodes"])


if __name__ == "__main__":
    unittest.main()
