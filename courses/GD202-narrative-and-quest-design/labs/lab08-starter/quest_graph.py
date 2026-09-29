"""GD202 Lab 08 starter: quest chains as prerequisite graphs. Standard library only.

Fill in the TODO functions, then run the tests from this folder:

    ../../../../.venv/bin/python test_quest_graph.py

Notation follows the week 8 lecture. A zone is a dict that maps each quest id
to the set of quest ids that must be finished before it unlocks:

    {"a": set(), "b": {"a"}, "c": {"a"}, "d": {"b", "c"}}

The batching player takes every unlocked quest, does them all in one trip out
of the hub, returns, turns them in, and repeats.
"""
import csv
import os
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))


def load_zones(path=os.path.join(HERE, "zones.csv")):
    """Read zones.csv into {zone_name: {quest: set(prereqs)}}.
    The prereqs column holds ids separated by ';' (empty for none)."""
    zones = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            pre = {x.strip() for x in row["prereqs"].split(";") if x.strip()}
            zones.setdefault(row["zone"], {})[row["quest"]] = pre
    return zones


def layers(zone):
    """TODO step 1. Return the batching player's trips as a list of sorted lists.
    Layer 1 holds every quest with no prerequisites. Each later layer holds the
    quests whose prerequisites all sit in earlier layers.
    Raise ValueError if a prerequisite is not a quest in the zone, or if some
    quests can never unlock (a cycle)."""
    raise NotImplementedError("layers() is yours to write")


def trips(zone):
    """TODO step 2. T, the number of layers (round trips to the hub)."""
    raise NotImplementedError("trips() is yours to write")


def width(zone):
    """TODO step 2. W, the largest number of quests open in one trip."""
    raise NotImplementedError("width() is yours to write")


def ancestors(zone, quest):
    """Every quest that must be finished, directly or indirectly, before quest."""
    seen, stack = set(), list(zone[quest])
    while stack:
        q = stack.pop()
        if q not in seen:
            seen.add(q)
            stack.extend(zone[q])
    return seen


def order_control(zone):
    """TODO step 3. C, the share of quest pairs whose order the designer fixes.
    A pair (x, y) is fixed when x is an ancestor of y or y is an ancestor of x.
    C = fixed pairs / all pairs. Return 1.0 for a zone with fewer than 2 quests."""
    raise NotImplementedError("order_control() is yours to write")


def zone_minutes(zone, work, round_trip):
    """TODO step 4. Total time = n x work + T x round_trip, in minutes."""
    raise NotImplementedError("zone_minutes() is yours to write")


if __name__ == "__main__":
    for name, z in load_zones().items():
        print(f"{name:10s} n={len(z):2d}  T={trips(z)}  W={width(z)}  "
              f"C={order_control(z):.3f}  time={zone_minutes(z, 3, 4):.0f} min")
