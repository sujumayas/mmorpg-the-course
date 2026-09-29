"""CS203 Lab 03 starter: terrain costs, movement range and Dijkstra maps.
Standard library only.

Fill in the TODO functions, then run the tests:

    python3 test_paths.py        (or: pytest test_paths.py)

Cells are (column, row). Entering a cell costs its terrain cost, as in the
week 3 lecture. Mountains ("M") and walls ("#") cannot be entered.
"""
import heapq

COST = {".": 1, "f": 2, "h": 2, "H": 3, "M": None, "#": None}

LECTURE_MAP = """
......
.ffh..
.hHHf.
.fMf..
......
"""

# Two maps for the tuning task (steps 6 and 7). S is the start, G the goal;
# both are open ground. The designer's intent is written above each map.
TUNING_MAPS = {
    # Intent: the patrol stays on open ground and walks around the woods.
    "forest_or_open": """
S.fff.G
.#####.
.......
""",
    # Intent: the scout climbs the wooded hill only if the way around is at
    # least twice as long in tiles. Here it is 16 tiles against 10, so it
    # should walk around.
    "hill_or_around": """
S...HHH...G
.#########.
.#########.
...........
""",
}


def load_map(text):
    """Return the map as a list of row strings, blank lines removed."""
    return [row for row in text.strip("\n").split("\n") if row]


def find(grid, ch):
    """Return the (column, row) of the first ch in grid, or None."""
    for y, row in enumerate(grid):
        x = row.find(ch)
        if x >= 0:
            return (x, y)
    return None


def cost_at(grid, cell, cost=COST):
    ch = grid[cell[1]][cell[0]]
    return 1 if ch in "SG" else cost[ch]


def neighbours(grid, cell, cost=COST):
    """Yield (neighbour, cost to enter it) in the order N, E, S, W."""
    x, y = cell
    for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
            c = cost_at(grid, (nx, ny), cost)
            if c is not None:
                yield (nx, ny), c


# ------------------------------------------------------------------ your code

def dijkstra(grid, starts, budget=float("inf"), cost=COST):
    """TODO steps 1 and 3. Multi-source Dijkstra.
    starts: a list of cells that all begin at cost 0.
    Never record a cell whose cost would exceed budget.
    Return (g, prev): g maps each reached cell to its cheapest cost,
    prev maps each reached cell to the cell it was reached from (None for starts).
    Use heapq with (cost, cell) tuples and lazy deletion, as in the lecture."""
    raise NotImplementedError("dijkstra() is yours to write")


def path_to(prev, cell):
    """TODO step 1. Follow prev back to a start; return the path start-first,
    or [] if cell was not reached."""
    raise NotImplementedError("path_to() is yours to write")


def movement_range(grid, start, budget, cost=COST):
    """TODO step 2. The set of cells reachable from start within budget,
    start included."""
    raise NotImplementedError("movement_range() is yours to write")


def flee_map(grid, threats, factor=-1.2, cost=COST):
    """TODO step 4. Brogue-style safety map (Walker, RogueBasin).
    1. g = the Dijkstra map from the threats.
    2. Multiply every value by factor (negative).
    3. Rescan: repeat until nothing changes: for every reached cell c, if
       min over neighbours n of (value[n] + cost to enter c) is lower than
       value[c], lower value[c] to it.
    Return the dict of values. A fleeing monster steps to its lowest neighbour."""
    raise NotImplementedError("flee_map() is yours to write")


# ----------------------------------------------------------- provided: printing

def show(grid, values):
    """Print a grid of values; '#' for cells without a value."""
    for y in range(len(grid)):
        print(" ".join(f"{values[(x, y)]:>5.1f}" if (x, y) in values else "    #"
                       for x in range(len(grid[0]))))


if __name__ == "__main__":
    grid = load_map(LECTURE_MAP)
    g, prev = dijkstra(grid, [(0, 2)])
    show(grid, g)
    print("path:", path_to(prev, (5, 2)))
    print("range with 4 MP:", len(movement_range(grid, (0, 2), 4)), "cells")
