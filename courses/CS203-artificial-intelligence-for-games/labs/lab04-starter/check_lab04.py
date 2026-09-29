"""Checks for CS203 Lab 04. Run: python check_lab04.py

Exits with status 0 when every check passes, 1 otherwise. On the untouched
starter every check fails; that is expected.
"""
import sys
from pathlib import Path

import pathgrid as pg

MAPS = {p.stem: pg.Grid.load(p) for p in sorted(Path(__file__).with_name("maps").glob("*.txt"))}
results = []


def check(name, fn):
    try:
        ok, detail = fn()
    except NotImplementedError as exc:
        ok, detail = False, f"not written yet ({exc})"
    except Exception as exc:  # show the student what broke
        ok, detail = False, f"{type(exc).__name__}: {exc}"
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + ("" if ok else f"  -> {detail}"))


def heuristics():
    got = (pg.manhattan((0, 0), (3, 5)), pg.octile((0, 0), (3, 5)),
           pg.octile((3, 5), (0, 0)), pg.octile((4, 4), (4, 4)), pg.octile((1, 1), (1, 9)))
    want = (80, 62, 62, 0, 80)
    return got == want, f"got {got}, want {want}"


def valid_path(grid, path, cost):
    if not path or path[0] != grid.start or path[-1] != grid.goal:
        return False, "path must run from S to G"
    total = 0
    for a, b in zip(path, path[1:]):
        steps = dict(grid.neighbors(a))
        if b not in steps:
            return False, f"illegal move {a} -> {b}"
        total += steps[b]
    return total == cost, f"path sums to {total} but cost says {cost}"


def optimal_everywhere():
    for name, grid in MAPS.items():
        ref, _, _ = pg.dijkstra(grid, grid.start, grid.goal)
        cost, path, _ = pg.astar(grid, grid.start, grid.goal, pg.octile)
        if cost != ref:
            return False, f"{name}: A* cost {cost}, Dijkstra cost {ref}"
        ok, why = valid_path(grid, path, cost)
        if not ok:
            return False, f"{name}: {why}"
    return True, ""


def fewer_expansions():
    for name in ("open", "wall", "trap"):
        grid = MAPS[name]
        _, _, d = pg.dijkstra(grid, grid.start, grid.goal)
        _, _, a = pg.astar(grid, grid.start, grid.goal, pg.octile)
        if not a < d:
            return False, f"{name}: A* expanded {a}, Dijkstra {d}"
    return True, ""


def weighted_bound():
    for name, grid in MAPS.items():
        ref, _, _ = pg.dijkstra(grid, grid.start, grid.goal)
        cost, path, _ = pg.astar(grid, grid.start, grid.goal, pg.octile, weight=2.0)
        if cost > 2 * ref:
            return False, f"{name}: weighted cost {cost} exceeds 2 x {ref}"
        ok, why = valid_path(grid, path, cost)
        if not ok:
            return False, f"{name}: {why}"
    return True, ""


def admissibility():
    for name, grid in MAPS.items():
        over = pg.max_overestimate(grid, grid.goal, pg.octile)
        if over != 0:
            return False, f"{name}: octile overestimates by {over}"
    grid = MAPS["open"]
    over = pg.max_overestimate(grid, grid.goal, pg.manhattan)
    return over == 72, f"open map, manhattan: got {over}, want 72"


check("step 1: manhattan and octile return the right costs", heuristics)
check("step 2: A* with octile matches Dijkstra's cost on every map, valid path", optimal_everywhere)
check("step 3: A* with octile expands fewer cells than Dijkstra on open, wall, trap", fewer_expansions)
check("step 3: weighted A* (w=2) stays within 2x optimal", weighted_bound)
check("step 4: max_overestimate finds octile admissible and manhattan off by 72", admissibility)

print(f"\n{sum(results)}/{len(results)} checks pass")
sys.exit(0 if all(results) else 1)
