"""GD201 Lab 02: measure a text-grid blockout.

A blockout is a text file. Each character is one grid cell:
    #          wall (blocked)
    .          floor
    A-Z        floor with a named marker (S = start, G = goal, others are beats or objectives)
The player moves between cells that share an edge (up, down, left, right), not diagonally.

Run `python blockout.py sample_mill.txt` for a report. See lecture week 2, section 3.
"""
import sys
from collections import deque

CELL_METRES = 1.0     # one grid cell is one metre
SPEED = 6.0           # player run speed in metres per second (a teaching value)


def load(path):
    """Return the grid as a list of equal-length strings."""
    with open(path) as fh:
        rows = [line.rstrip("\n") for line in fh if line.strip()]
    width = max(len(r) for r in rows)
    return [r.ljust(width, "#") for r in rows]


def markers(grid):
    """Map each marker letter to its (row, col)."""
    found = {}
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch.isalpha() and ch.isupper():
                found[ch] = (r, c)
    return found


def walkable(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] != "#"


def shortest_steps(grid, start, goal):
    """Fewest moves from start to goal (both (row, col)), or None if unreachable. Use breadth-first search."""
    # TODO: keep a queue of cells and a dict of distances; expand the four neighbours with walkable().
    raise NotImplementedError("shortest_steps")


def path_seconds(steps, cell_metres=CELL_METRES, speed=SPEED):
    """Seconds to walk `steps` cells."""
    # TODO: distance in metres divided by speed.
    raise NotImplementedError("path_seconds")


def critical_path(grid, order):
    """Total steps along the markers in `order` (for example "SABCDG"), leg by leg.

    Return (total_steps, [steps for each leg]). Return None if any leg is unreachable.
    """
    # TODO: call shortest_steps for each consecutive pair of markers in order.
    raise NotImplementedError("critical_path")


def problems_at_ship(S, N=40, M=6, f=0.5, B=80, A=32, c_g=4, c_a=16):
    """Lecture week 2: expected problems left at ship if you greybox for S hours, then do the art pass."""
    # TODO: copy the model from lecture week 2, section 2. Treat a negative art-round count as 0.
    raise NotImplementedError("problems_at_ship")


def report(path, order="SABCDG"):
    grid = load(path)
    print(f"{path}: {len(grid[0])} x {len(grid)} cells, markers {''.join(sorted(markers(grid)))}")
    result = critical_path(grid, order)
    if result is None:
        print("critical path: unreachable leg")
        return
    total, legs = result
    for (a, b), s in zip(zip(order, order[1:]), legs):
        print(f"  {a} -> {b}: {s:3d} cells, {path_seconds(s):5.1f} s")
    print(f"critical path {order}: {total} cells, {path_seconds(total):.1f} s at {SPEED} m/s")
    best = min(range(0, 49, 4), key=problems_at_ship)
    print(f"budget plan (lecture defaults): best switch point {best} h, {problems_at_ship(best):.3f} problems at ship")


if __name__ == "__main__":
    try:
        report(sys.argv[1] if len(sys.argv) > 1 else "sample_mill.txt")
    except NotImplementedError as e:
        print(f"Not implemented yet: {e}(). Fill in the TODOs, then run check_lab02.py.")
