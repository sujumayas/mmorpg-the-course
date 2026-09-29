"""GD202 Lab 03 starter: branch explosion analyzer. Standard library only.

A dialogue or story graph is a dict: node id -> list of child node ids.
A node with no children is an ending. The graphs in this lab have no cycles.

Fill in the TODO functions, then run the tests from this folder:

    ../../../../.venv/bin/python test_branching.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def build_structure(b, d, k):
    """Build the lecture's fold-back structure (given, do not edit).

    b options per choice, d choices on every path, fold every k choices.
    k >= d gives a pure tree (time cave); k = 1 gives branch and bottleneck.
    """
    graph = {"S": []}
    frontier = ["S"]
    done, seg = 0, 0
    while done < d:
        size = min(k, d - done)
        for depth in range(size):
            nxt = []
            for parent in frontier:
                for option in range(b):
                    child = f"{parent}.{option}" if parent != "S" else f"g{seg}.{option}"
                    graph[parent].append(child)
                    graph[child] = []
                    nxt.append(child)
            frontier = nxt
        done += size
        if done < d:
            hub = f"B{seg}"
            graph[hub] = []
            for leaf in frontier:
                graph[leaf].append(hub)
            frontier = [hub]
        seg += 1
    return graph


def formula(b, d, k):
    """TODO step 1. Return the lecture's closed-form numbers as a dict with keys
    "nodes", "endings", "paths", "seen" for the build_structure(b, d, k) shape.
    Use the segment formulas from lecture section 2; do not build the graph."""
    raise NotImplementedError("formula() is yours to write")


def reachable(graph, start):
    """TODO step 2. Set of node ids reachable from start (start included)."""
    raise NotImplementedError("reachable() is yours to write")


def endings(graph, start):
    """TODO step 3. Sorted list of reachable nodes with no children."""
    raise NotImplementedError("endings() is yours to write")


def count_paths(graph, start):
    """TODO step 4. Number of distinct start-to-ending paths.
    Must be fast on graphs with millions of paths: memoize per node,
    do not enumerate paths one by one."""
    raise NotImplementedError("count_paths() is yours to write")


def mean_path_nodes(graph, start):
    """TODO step 5. Average number of nodes on a start-to-ending path, with
    every path weighted equally (start and ending both counted)."""
    raise NotImplementedError("mean_path_nodes() is yours to write")


def report(graph, start):
    """Summary used by the command line and by your lab write-up."""
    nodes = len(reachable(graph, start))
    mean = mean_path_nodes(graph, start)
    return {
        "nodes": nodes,
        "endings": len(endings(graph, start)),
        "paths": count_paths(graph, start),
        "mean_path_nodes": mean,
        "share_seen": mean / nodes,
    }


def load(path):
    with open(path) as f:
        data = json.load(f)
    return data["graph"], data["start"]


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "ferry.json")
    graph, start = load(path)
    for key, value in report(graph, start).items():
        print(f"{key:16} {value:.3f}" if isinstance(value, float) else f"{key:16} {value}")
