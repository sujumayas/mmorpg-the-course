"""GD201 Lab 09: POI density audit.

Run:    python poi_density.py
Check:  python check_lab09.py

Fill in every function marked TODO. The docstrings define what each returns.
Distances are in metres, speeds in m/s, densities in POIs per square kilometre.
A POI is a tuple (name, x, y).
"""
import csv
from math import sqrt, pi
from pathlib import Path

HERE = Path(__file__).resolve().parent
ZONE = HERE / "zone_marsh.csv"
ZONE_SIZE = 2000          # the zone is ZONE_SIZE x ZONE_SIZE metres
WALK = 6.4                # design speed on foot, m/s
MOUNT = WALK * 1.6        # design speed on a +60% mount, m/s
TARGET = 40               # design travel gap for the Marsh, seconds


def spacing_for_gap(v, gap):
    """Grid spacing (m) that puts POIs `gap` seconds apart at speed v."""
    raise NotImplementedError  # TODO Part A


def density_for_gap(v, gap):
    """POIs per km² on a square grid with that spacing."""
    raise NotImplementedError  # TODO Part A


def gap_for_density(v, rho):
    """Travel gap (s) between neighbours on a square grid of density rho at speed v."""
    raise NotImplementedError  # TODO Part A


def load_zone(path=ZONE):
    """List of (name, x, y) with x and y as floats, in file order."""
    raise NotImplementedError  # TODO Part B


def nearest_neighbour_tour(pois, start):
    """Walk from the POI named `start` to the nearest unvisited POI, again and again,
    until every POI is visited. Break distance ties by POI name.
    Return a list of legs (from_name, to_name, distance_m)."""
    raise NotImplementedError  # TODO Part B


def long_gaps(tour, v, target, factor=2.0):
    """Legs whose travel time at speed v is more than factor * target seconds,
    as (from_name, to_name, seconds), in tour order."""
    raise NotImplementedError  # TODO Part B


def empty_fraction(pois, r, size=ZONE_SIZE, step=50):
    """Fraction of raster points (step/2, 3*step/2, ... in x and y) farther than r
    metres from every POI."""
    raise NotImplementedError  # TODO Part C


def largest_empty_circle(pois, size=ZONE_SIZE, step=50):
    """The raster point farthest from its nearest POI, as (x, y, distance_m).
    Break ties by the smallest x, then the smallest y."""
    raise NotImplementedError  # TODO Part C


def visible_count(pois, x, y, r):
    """Number of POIs within r metres of (x, y), not counting a POI exactly at (x, y)."""
    raise NotImplementedError  # TODO Part C


if __name__ == "__main__":
    try:
        print(f"Walk, {TARGET} s gap: spacing {spacing_for_gap(WALK, TARGET):.0f} m, "
              f"density {density_for_gap(WALK, TARGET):.1f} per km2")
        pois = load_zone()
        rho = len(pois) / (ZONE_SIZE / 1000) ** 2
        print(f"Marsh: {len(pois)} POIs, density {rho:.1f} per km2, "
              f"grid gap on foot {gap_for_density(WALK, rho):.1f} s")
        tour = nearest_neighbour_tour(pois, "P01")
        print(f"Long legs on foot (over 2 x {TARGET} s):")
        for a, b, s in long_gaps(tour, WALK, TARGET):
            print(f"  {a} -> {b}: {s:.1f} s")
        print(f"Empty beyond 250 m: {empty_fraction(pois, 250):.3f}")
        print("Largest empty circle:", largest_empty_circle(pois))
    except NotImplementedError:
        print("Not implemented yet. Fill in the TODO functions, then run check_lab09.py.")
