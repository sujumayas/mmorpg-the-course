"""MMO406 Lab 02 starter: resource locality and spawn checks. Standard library only.

A world file lists resource "types" and "regions" (region name -> list of types).
A recipe file maps recipe names to the list of types each recipe needs.
A spawn file lists creatures with a trophic "level", a "count" and a "mass_kg".

Fill in the TODO functions, then run the tests from this folder:

    ../../../../.venv/bin/python test_regions.py

Report on a world and recipe list:

    ../../../../.venv/bin/python regions.py albion.json recipes.json
"""
import json
import os
import sys
from fractions import Fraction
from itertools import combinations
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))


def load(path):
    """Read a JSON file (given)."""
    with open(path) as f:
        return json.load(f)


def local_share(M, r, k):
    """TODO: return C(r, k) / C(M, k) as an exact Fraction (0 if k > r)."""
    raise NotImplementedError


def makeable_here(region_types, recipes):
    """TODO: return the sorted list of recipe names whose types are all in region_types."""
    raise NotImplementedError


def makeable_anywhere(regions, recipes):
    """TODO: return the sorted list of recipe names that at least one region can make alone."""
    raise NotImplementedError


def combo_coverage(types, regions, k):
    """TODO: return (covered, total) for all k-type combinations of `types`.

    A combination is covered if it is a subset of at least one region's types.
    total is C(len(types), k).
    """
    raise NotImplementedError


def predator_ratio(spawns):
    """TODO: return total carnivore mass / total herbivore mass as a Fraction.

    Carnivores are any level other than "herbivore". Mass is count * mass_kg.
    """
    raise NotImplementedError


def report(world, book):
    """Print a locality report (given, relies on your functions)."""
    types, regions, recipes = world["types"], world["regions"], book["recipes"]
    print(world["name"], "|", book["name"])
    for name, held in regions.items():
        here = makeable_here(held, recipes)
        print(f"  {name:10s} r={len(held)}  makes {len(here):2d}/{len(recipes)} recipes at home")
    anywhere = makeable_anywhere(regions, recipes)
    print(f"  makeable in some single region: {len(anywhere)}/{len(recipes)}")
    for k in (1, 2, 3):
        cov, tot = combo_coverage(types, regions, k)
        print(f"  k={k}: {cov}/{tot} type combinations gatherable in one region")


if __name__ == "__main__":
    w = load(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "albion.json"))
    b = load(sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "recipes.json"))
    report(w, b)
