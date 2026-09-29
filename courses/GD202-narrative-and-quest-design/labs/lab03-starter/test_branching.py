"""Tests for GD202 Lab 03. Values come from the week 3 lecture.
Run with `python test_branching.py` or `pytest test_branching.py`."""
import os

from branching import (build_structure, count_paths, endings, formula, load,
                       mean_path_nodes, reachable, report)

HERE = os.path.dirname(os.path.abspath(__file__))

# (k, nodes, endings, seen) for b = 3, d = 5, from the lecture's fold table
FOLD_TABLE = [(5, 364, 243, 6), (4, 125, 3, 7), (3, 53, 9, 7), (2, 30, 3, 8), (1, 20, 3, 10)]


def test_formula_matches_lecture():
    for k, nodes, ends, seen in FOLD_TABLE:
        r = formula(3, 5, k)
        assert (r["nodes"], r["endings"], r["paths"], r["seen"]) == (nodes, ends, 243, seen), k


def test_formula_depth_table():
    assert formula(3, 10, 10)["nodes"] == 88_573
    assert formula(3, 10, 10)["endings"] == 59_049
    assert formula(2, 4, 4)["nodes"] == 31


def test_graph_matches_formula():
    for b, d in [(2, 4), (3, 5), (4, 3)]:
        for k in range(1, d + 1):
            g = build_structure(b, d, k)
            f = formula(b, d, k)
            assert len(reachable(g, "S")) == f["nodes"], (b, d, k)
            assert len(endings(g, "S")) == f["endings"], (b, d, k)
            assert count_paths(g, "S") == f["paths"], (b, d, k)
            assert abs(mean_path_nodes(g, "S") - f["seen"]) < 1e-9, (b, d, k)


def test_big_fold_is_fast():
    g = build_structure(3, 20, 1)          # 3**20 = 3,486,784,401 paths
    assert count_paths(g, "S") == 3 ** 20
    assert len(reachable(g, "S")) == 1 + 19 * 4 + 3


def test_sample_ferry():
    g, start = load(os.path.join(HERE, "ferry.json"))
    assert endings(g, start) == ["drowned", "leave", "shore", "stay"]
    r = report(g, start)
    assert r["nodes"] == 17
    assert r["paths"] == 20
    assert abs(r["mean_path_nodes"] - 144 / 20) < 1e-9


def test_unreachable_node_ignored():
    g = {"a": ["b"], "b": [], "orphan": ["b"]}
    assert reachable(g, "a") == {"a", "b"}
    assert count_paths(g, "a") == 1


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
