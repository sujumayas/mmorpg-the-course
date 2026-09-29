"""MMO406 Lab 03 starter: faction web analyser (structural balance). Standard library only.

A web file lists "factions" (names, in a fixed order) and "edges" as
[a, b, sign] with sign +1 (allies) or -1 (enemies). Pairs not listed are neutral (0).

Fill in the TODO functions, then run the tests from this folder:

    ../../../../.venv/bin/python test_factions.py

Report on a web:

    ../../../../.venv/bin/python factions.py bribe.json
"""
import json
import os
import sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))


def load(path):
    """Read a web file. Returns (factions, edges) with edges keyed by frozenset pairs (given)."""
    with open(path) as f:
        data = json.load(f)
    edges = {frozenset((a, b)): s for a, b, s in data["edges"]}
    return data["factions"], edges


def sign(edges, a, b):
    """Sign of the pair a, b: +1, -1, or 0 if neutral (given)."""
    return edges.get(frozenset((a, b)), 0)


def triads(factions, edges):
    """TODO: return a list of (a, b, c, product) for every complete triad.

    Iterate with itertools.combinations(factions, 3) so the order follows the file.
    A triad is complete if none of its three pairs is neutral.
    """
    raise NotImplementedError


def tension(factions, edges):
    """TODO: return (unbalanced, complete) counts."""
    raise NotImplementedError


def camps(factions, edges):
    """TODO: if every pair is signed and there are no unbalanced triads, return the
    two camps as a tuple of two lists: the camp containing factions[0] first, each
    list in file order. The second list may be empty. Otherwise return None.

    Hint: put factions[0] in camp 0; every other faction x goes in camp 0 if
    sign(factions[0], x) is +1 and camp 1 if it is -1.
    """
    raise NotImplementedError


def edge_triads(factions, edges, a, b):
    """TODO: return how many complete triads contain the pair a, b."""
    raise NotImplementedError


def best_flip(factions, edges):
    """TODO: try reversing the sign of each signed pair, one at a time.

    Return ((a, b), unbalanced_after) for the flip with the fewest unbalanced
    triads afterwards. Name the pair in alphabetical order. Break ties by the
    alphabetical order of the pair. Return None if no pair is signed.
    """
    raise NotImplementedError


def report(factions, edges):
    """Print a web report (given, relies on your functions)."""
    u, t = tension(factions, edges)
    print(f"factions: {', '.join(factions)}")
    for a, b, c, p in triads(factions, edges):
        print(f"  {a} / {b} / {c}: {'balanced' if p > 0 else 'UNBALANCED'}")
    print(f"  T = {u}/{t}" if t else "  T = n/a (no complete triads)")
    split = camps(factions, edges)
    if split:
        print(f"  camps: {split[0]} vs {split[1]}")
    flip = best_flip(factions, edges)
    if flip:
        print(f"  best single flip: {flip[0][0]} - {flip[0][1]} -> {flip[1]} unbalanced")


if __name__ == "__main__":
    report(*load(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "bribe.json")))
