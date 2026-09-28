"""CS102 Lab 03: the one shipped test that FAILS on the starter.

It runs every pair of starter elements through the four starter materials twice,
once as a class from chemistry.py and once as a TableMaterial, and requires the
same description and state after each element. It fails until REACTIONS in
chemistry_table.py holds all the starter reactions (step 5).
Run with: python -m unittest -v
"""
import itertools
import unittest

import chemistry as chem
from chemistry_table import TableMaterial

STARTER = {"grass": chem.Grass, "wood": chem.Wood, "metal": chem.Metal, "stone": chem.Stone}
STARTER_ELEMENTS = ["fire", "water", "electric"]


class TestTableAgrees(unittest.TestCase):
    def test_table_matches_classes_on_starter_materials(self):
        for kind, cls in STARTER.items():
            for seq in itertools.product(STARTER_ELEMENTS, repeat=2):
                with self.subTest(material=kind, sequence=seq):
                    a, b = cls(kind), TableMaterial(kind)
                    for element in seq:
                        self.assertEqual(a.react(element), b.react(element))
                        self.assertEqual(a.state, b.state)


if __name__ == "__main__":
    unittest.main()
