"""Tests for MMO406 Lab 03. Values come from the week 3 lecture.
Run with `python test_factions.py` or `pytest test_factions.py`."""
import os
from itertools import combinations

from factions import (best_flip, camps, edge_triads, load, tension, triads)

HERE = os.path.dirname(os.path.abspath(__file__))


def web(factions, pos_pairs, neg_all=True):
    edges = {}
    if neg_all:
        edges = {frozenset(p): -1 for p in combinations(factions, 2)}
    for a, b in pos_pairs:
        edges[frozenset((a, b))] = 1
    return edges


def test_lecture_table():
    F = ["Crown", "Temple", "Guild", "Clans"]
    assert tension(F, web(F, [])) == (4, 4)
    blocs = web(F, [("Crown", "Temple"), ("Guild", "Clans")])
    assert tension(F, blocs) == (0, 4)
    assert camps(F, blocs) == (["Crown", "Temple"], ["Guild", "Clans"])


def test_bribe_file():
    F, E = load(os.path.join(HERE, "bribe.json"))
    assert tension(F, E) == (2, 4)
    bad = [(a, b, c) for a, b, c, p in triads(F, E) if p < 0]
    assert bad == [("Crown", "Temple", "Guild"), ("Temple", "Guild", "Clans")]
    assert camps(F, E) is None


def test_check_yourself():
    F = list("ABCDE")
    assert tension(F, web(F, [])) == (10, 10)
    E = web(F, [("A", "B"), ("A", "C"), ("B", "C"), ("D", "E"), ("A", "D")])
    assert tension(F, E) == (3, 10)


def test_flip_touches_n_minus_2():
    for n in range(3, 8):
        F = [f"F{i}" for i in range(n)]
        E = web(F, [])
        assert edge_triads(F, E, "F0", "F1") == n - 2
        assert best_flip(F, E)[1] == tension(F, E)[0] - (n - 2)


def test_best_flip_all_at_war():
    F = ["Crown", "Temple", "Guild", "Clans"]
    assert best_flip(F, web(F, [])) == (("Clans", "Crown"), 2)


def test_eve():
    F, E = load(os.path.join(HERE, "eve_fw.json"))
    assert tension(F, E) == (2, 2)
    assert edge_triads(F, E, "Amarr", "Caldari") == 0
    assert camps(F, E) is None
    assert best_flip(F, E) == (("Amarr", "Angel Cartel"), 1)


def test_neutral_only():
    F = ["Horde", "Alliance"]
    assert tension(F, {frozenset(F): -1}) == (0, 0)
    assert camps(F, {frozenset(F): -1}) == (["Horde"], ["Alliance"])
    assert best_flip(F, {}) is None


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print("PASS", name)
            except Exception as e:  # noqa: BLE001
                failed += 1
                print("FAIL", name, type(e).__name__, e)
    raise SystemExit(1 if failed else 0)
