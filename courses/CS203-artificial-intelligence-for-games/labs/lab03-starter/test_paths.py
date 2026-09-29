"""Tests for Lab 03. Values come from the week 3 lecture.
Run with `python3 test_paths.py` or `pytest test_paths.py`."""
from paths import (LECTURE_MAP, dijkstra, flee_map, load_map, movement_range, path_to)

GRID = load_map(LECTURE_MAP)
START, GOAL = (0, 2), (5, 2)
EXPECTED_G = ["2 3 4 5 6 7", "1 3 5 7 7 8", "0 2 5 8 9 9", "1 3 # 7 7 8", "2 3 4 5 6 7"]


def test_lecture_cost_grid():
    g, _ = dijkstra(GRID, [START])
    for y, line in enumerate(EXPECTED_G):
        for x, v in enumerate(line.split()):
            if v == "#":
                assert (x, y) not in g
            else:
                assert g[(x, y)] == int(v), ((x, y), g.get((x, y)))


def test_lecture_path():
    _, prev = dijkstra(GRID, [START])
    path = path_to(prev, GOAL)
    assert path[0] == START and path[-1] == GOAL
    assert len(path) - 1 == 9
    assert path == [(0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (5, 1), (5, 2)]


def test_unreached_path_is_empty():
    _, prev = dijkstra(GRID, [START], budget=2)
    assert path_to(prev, GOAL) == []


def test_movement_range_counts():
    assert len(movement_range(GRID, START, 4)) == 12
    assert len(movement_range(GRID, START, 3)) == 10
    assert movement_range(GRID, START, 0) == {START}


def test_multi_source():
    corridor = load_map("......")
    g, prev = dijkstra(corridor, [(0, 0), (5, 0)])
    assert [g[(x, 0)] for x in range(6)] == [0, 1, 2, 2, 1, 0]
    assert prev[(0, 0)] is None and prev[(5, 0)] is None


def test_flee_map_corridor():
    corridor = load_map("......")
    v = flee_map(corridor, [(0, 0)])
    got = [v[(x, 0)] for x in range(6)]
    for a, b in zip(got, [-1, -2, -3, -4, -5, -6]):
        assert abs(a - b) < 1e-9, got


def test_flee_map_rescan():
    # Threat at column 2 of a 10-cell corridor. Before the rescan the values are
    # -1.2 x distance. The rescan pulls every cell toward the long, safe end, so
    # cells just right of the threat drop well below -1.2 x their distance.
    corridor = load_map("..........")
    v = flee_map(corridor, [(2, 0)])
    want = [-2.4, -1.4, -1.4, -2.4, -3.4, -4.4, -5.4, -6.4, -7.4, -8.4]
    got = [v[(x, 0)] for x in range(10)]
    for a, b in zip(got, want):
        assert abs(a - b) < 1e-9, got


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS {name}")
            except NotImplementedError as e:
                failed += 1
                print(f"TODO {name}: {e}")
            except AssertionError as e:
                failed += 1
                print(f"FAIL {name} {e}")
    print(f"\n{failed} test(s) not passing" if failed else "\nall tests pass")
    raise SystemExit(1 if failed else 0)
