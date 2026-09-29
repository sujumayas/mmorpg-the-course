"""MMO307 Lab 05 starter: the squish planner. Standard library only.

Fill in every function that raises NotImplementedError, then run the tests:

    python test_squish.py        (or: pytest test_squish.py)

Notation follows the week 5 lecture: v_e is a typical value of era e, d_e the
divisor a squish applies to era e, a and b the readable band, m_e = d_E / d_e
the compensation multiplier for old content, R the growth per year.
"""
import csv
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load_eras(path=os.path.join(HERE, "eras.csv")):
    """Return a list of dicts, one per era, with numeric fields converted to int."""
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in ("era", "creature_health", "boss_health", "dot_tick"):
            r[k] = int(r[k])
    return rows


def dynamic_range(values):
    """Ratio of the largest value to the smallest."""
    raise NotImplementedError("dynamic_range() is yours to write")


def uniform_divisor_range(values, a, b):
    """Return (lo, hi), the range of single divisors d that put every value in [a, b],
    or None when no single divisor works."""
    raise NotImplementedError("uniform_divisor_range() is yours to write")


def squish(values, divisors):
    """Divide each value by its era's divisor."""
    raise NotImplementedError("squish() is yours to write")


def compensation(divisors):
    """m_e = d_E / d_e, where d_E is the last (current) era's divisor."""
    raise NotImplementedError("compensation() is yours to write")


def hits_to_kill(health, hit):
    """Whole hits needed to bring health to zero (ceil of health / hit)."""
    raise NotImplementedError("hits_to_kill() is yours to write")


def power_law(values, b, p):
    """Curve squish: new = v**p * (b / max(values)**p), so the largest value lands at b."""
    raise NotImplementedError("power_law() is yours to write")


def headroom(d, R):
    """Years until numbers growing by R per year regain the size a squish by d removed."""
    raise NotImplementedError("headroom() is yours to write")


def scale_error(f, args, d, degree=1, scaled=None):
    """Squish-safety test. Divide the arguments marked True in `scaled` (all of them when
    scaled is None) by d, call f, and compare with f(*args) / d**degree.
    Return the relative error new / expected - 1 (0.0 means squish-safe for these inputs)."""
    raise NotImplementedError("scale_error() is yours to write")


# The game's formulas. Test each one with scale_error in step 4 of the lab.

def armor_mitigation(armor, k):
    """Divisive armor from MMO303 week 2."""
    return armor / (armor + k)


def floored_damage(attack, defense, floor=5):
    """Subtractive damage with a minimum of `floor`."""
    return max(floor, attack - defense)


def dot_tick(total, ticks):
    """Damage over time, shown and applied as whole numbers per tick."""
    return round(total / ticks)


def time_to_die(health, incoming_dps):
    """GD203 week 4: seconds until health runs out."""
    return health / incoming_dps


if __name__ == "__main__":
    eras = load_eras()
    for e in eras:
        print(e["era"], e["name"], e["creature_health"])
