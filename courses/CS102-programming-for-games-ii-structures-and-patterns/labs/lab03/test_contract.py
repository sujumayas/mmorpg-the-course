"""Contract test: every Material subclass must honour the react() contract.

Run with: python -m unittest -v
New classes you add to chemistry.py are picked up automatically.
"""
import itertools
import unittest

import chemistry as chem

PROBES = chem.ELEMENTS + ["", "wind", "FIRE", "not-an-element"]


class TestContract(unittest.TestCase):
    def test_every_material_honours_contract(self):
        for cls in chem.all_material_classes():
            for seq in itertools.product(PROBES, repeat=2):
                with self.subTest(material=cls.__name__, sequence=seq):
                    m = cls(cls.__name__.lower())
                    for element in seq:
                        result = m.react(element)
                        self.assertTrue(result is None or isinstance(result, str))
                        self.assertIn(m.state, chem.STATES)


class TestStarterReactions(unittest.TestCase):
    def test_world(self):
        world = [chem.Grass("grass"), chem.Wood("crate"), chem.Metal("sword"), chem.Stone("boulder")]
        self.assertEqual(chem.apply("fire", world), [
            ("grass", "catches fire and spreads"), ("crate", "burns"),
            ("sword", None), ("boulder", None)])
        self.assertEqual(chem.apply("water", world), [
            ("grass", "gets wet"), ("crate", "is put out"),
            ("sword", None), ("boulder", None)])

    def test_wet_grass_does_not_burn(self):
        g = chem.Grass("grass")
        g.react("water")
        self.assertIsNone(g.react("fire"))
        self.assertEqual(g.state, "wet")


if __name__ == "__main__":
    unittest.main()
