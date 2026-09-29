"""GD201 Lab 07: return ratios in a vertical level.

Run:    python vertical_nav.py
Check:  python check_lab07.py

Fill in every function marked TODO. The docstrings define what each returns.
Times are in seconds, distances and heights in metres.
"""
from math import sqrt
import heapq  # you will want this for shortest_time

from levels import CLIFF_RUIN, QUARRY, QUARRY_CANDIDATES

V_RUN = 6.0          # flat ground and downhill, m/s
V_UP = 4.0           # uphill on a slope, m/s
V_CLIMB = 1.5        # climbing a ladder, m/s
V_LADDER_DOWN = 3.0  # climbing down a ladder, m/s
G = 20.0             # gravity, m/s^2
H_SAFE = 8.0         # highest harmless drop, m


def drop_time(h, g=G, h_safe=H_SAFE):
    """Seconds to fall h metres from rest: sqrt(2h/g). Return None if h > h_safe."""
    raise NotImplementedError  # TODO Part A


def climb_time(h, v_climb=V_CLIMB):
    """Seconds to climb h metres up a ladder."""
    raise NotImplementedError  # TODO Part A


def edge_times(edge, heights, h_safe=H_SAFE):
    """Turn one level edge into a list of directed edges (from, to, seconds).

    run:    both ways at d / V_RUN
    slope:  downhill (or level) at d / V_RUN, uphill at d / V_UP, using heights
    drop:   one edge from the higher node to the lower one, or [] if unsafe
    ladder: up at climb_time(dh), down at dh / V_LADDER_DOWN
    """
    raise NotImplementedError  # TODO Part A


def build_graph(level, h_safe=H_SAFE):
    """Adjacency dict {node: [(neighbour, seconds), ...]} for every node in heights."""
    raise NotImplementedError  # TODO Part B


def shortest_time(graph, start, goal):
    """Least total seconds from start to goal (Dijkstra). float('inf') if unreachable."""
    raise NotImplementedError  # TODO Part B


def return_ratio(graph, home, place):
    """shortest_time(place -> home) / shortest_time(home -> place)."""
    raise NotImplementedError  # TODO Part B


def stranded(level, home, limit=2.0):
    """Places (not home) whose return ratio from home is above limit,
    as a list of (place, ratio) sorted from worst to best."""
    raise NotImplementedError  # TODO Part C


def best_shortcut(level, home, candidates):
    """Try adding each candidate edge on its own. Return (candidate, worst_ratio)
    for the candidate whose worst return ratio over all places is lowest."""
    raise NotImplementedError  # TODO Part C


if __name__ == "__main__":
    try:
        g = build_graph(CLIFF_RUIN)
        out, back = shortest_time(g, "Camp", "Ruin"), shortest_time(g, "Ruin", "Camp")
        print(f"Cliff Ruin: out {out:.1f} s, back {back:.1f} s, ratio {back / out:.2f}")
        print("Quarry, stranded from Hub:")
        for place, r in stranded(QUARRY, "Hub"):
            print(f"  {place:8} {r:5.2f}")
        cand, worst = best_shortcut(QUARRY, "Hub", QUARRY_CANDIDATES)
        print(f"Best shortcut: {cand}, worst ratio after it {worst:.2f}")
    except NotImplementedError:
        print("Not implemented yet. Fill in the TODO functions, then run check_lab07.py.")
