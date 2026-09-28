"""Print what happens when a sequence of elements sweeps across a small world.

Usage: python scenario.py fire water electric
"""
import sys

import chemistry as chem


def main(elements):
    world = [cls(cls.__name__.lower()) for cls in chem.all_material_classes()]
    for element in elements:
        print(f"-- {element}")
        for name, result in chem.apply(element, world):
            print(f"   {name:10s} {result or '-'}")


if __name__ == "__main__":
    main(sys.argv[1:] or chem.ELEMENTS)
