"""CS102 Lab 08 starter: a dialogue linter built on breadth-first search.

Run it with:
    .venv/bin/python courses/CS102-programming-for-games-ii-structures-and-patterns/labs/lab08-starter.py

With no argument it lints lab08-dialogue.json (next to this file) and then runs the tests.
Pass a path to lint your own file:  ... lab08-starter.py my_dialogue.json

Dialogue file format:
    {"start": "<node id>",
     "nodes": {"<id>": {"text": "...", "choices": [{"text": "...", "goto": "<id>"}], "end": true?}}}
A node with "end": true is an ending. A node with no choices that is not an ending is a dead end.
"""
import json
import sys
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_graph(data):
    """Return an adjacency list: dict mapping every node id to the list of ids its choices go to.

    Keep targets that do not exist (they are broken links). Keep the order of choices.
    """
    raise NotImplementedError("1: build_graph")


def bfs(graph, start):
    """Breadth-first search from start.

    Return (dist, prev): dist[id] = number of choices from start, prev[id] = the node we came from
    (prev[start] = None). Skip targets that are not keys of graph.
    Use collections.deque as the queue (week 6).
    """
    raise NotImplementedError("2: bfs")


def unreachable(graph, dist):
    """Sorted list of node ids that BFS never reached."""
    raise NotImplementedError("3: unreachable")


def dead_ends(data, graph, dist):
    """Sorted list of REACHABLE ids that have no choices and are not marked "end"."""
    raise NotImplementedError("4: dead_ends")


def broken_links(graph):
    """Sorted list of (from_id, missing_target) pairs where the target is not a node."""
    raise NotImplementedError("5: broken_links")


def path_to(prev, target):
    """List of ids from start to target, following prev backwards. [] if target was not reached."""
    raise NotImplementedError("6: path_to")


def cannot_finish(data, graph, dist):
    """Stretch. Sorted list of reachable ids from which NO ending can be reached.

    Hint: reverse every edge, then run one BFS starting from all endings at once.
    """
    raise NotImplementedError("7 (stretch): cannot_finish")


def report(data):
    g = build_graph(data)
    dist, prev = bfs(g, data["start"])
    print(f"{len(g)} nodes, {sum(len(v) for v in g.values())} choices, {len(dist)} reachable")
    print("unreachable :", unreachable(g, dist))
    print("dead ends   :", dead_ends(data, g, dist))
    print("broken links:", broken_links(g))
    endings = sorted(k for k, v in data["nodes"].items() if v.get("end") and k in dist)
    for e in endings:
        print(f"shortest to {e}: {' -> '.join(path_to(prev, e))}")
    try:
        print("cannot finish:", cannot_finish(data, g, dist))
    except NotImplementedError:
        print("cannot finish: (stretch not done)")


# ---------------------------------------------------------------------------
# Tests. Do not edit below this line.
# ---------------------------------------------------------------------------


def test_graph_and_bfs():
    data = load(HERE / "lab08-dialogue.json")
    g = build_graph(data)
    assert len(g) == 12 and g["haggle"] == ["buy", "haggel_fail", "leave"], g.get("haggle")
    dist, prev = bfs(g, "greet")
    assert dist["greet"] == 0 and prev["greet"] is None
    assert dist["rumor_two"] == 2 and dist["bye_friend"] == 3, dist
    assert len(dist) == 9, len(dist)


def test_lint():
    data = load(HERE / "lab08-dialogue.json")
    g = build_graph(data)
    dist, prev = bfs(g, "greet")
    assert unreachable(g, dist) == ["haggle_fail", "old_debt", "secret_discount"]
    assert dead_ends(data, g, dist) == ["rumor_detail"]
    assert broken_links(g) == [("haggle", "haggel_fail")]
    assert path_to(prev, "bye_friend") == ["greet", "ask_price", "buy", "bye_friend"]
    assert path_to(prev, "old_debt") == []


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "lab08-dialogue.json"
    try:
        report(load(target))
    except NotImplementedError as e:
        print(f"(report needs part {e})")
    print()
    for test in (test_graph_and_bfs, test_lint):
        try:
            test()
            print(f"PASS  {test.__name__}")
        except NotImplementedError as e:
            print(f"TODO  {test.__name__}: part {e}")
        except AssertionError as e:
            print(f"FAIL  {test.__name__}: got {e}")
