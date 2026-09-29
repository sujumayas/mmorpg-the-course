"""CS203 Lab 04 starter: A* on an 8-connected tactical grid.

Grid files use one character per cell:
    .  floor (terrain cost 1)
    ~  mud   (terrain cost 3)
    #  wall  (impassable)
    S  start (floor), G goal (floor)

Moving into a cell costs step x terrain, where step is 10 for a straight move
and 14 for a diagonal move (14 is 10 x sqrt(2) rounded, so every cost is an int).
Diagonal moves may not cut corners: both orthogonal neighbours must be passable.

Run:   python pathgrid.py            prints a comparison table for every map
Check: python check_lab04.py         exits 0 only when your work is complete

You edit the four functions marked TODO. Leave dijkstra() and true_costs_to()
alone: the checker uses them as the reference answer.
"""
import heapq
import math
import sys
from pathlib import Path

STRAIGHT, DIAGONAL = 10, 14
TERRAIN = {".": 1, "S": 1, "G": 1, "~": 3}
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]


class Grid:
    def __init__(self, text):
        self.rows = [line for line in text.splitlines() if line.strip()]
        self.h, self.w = len(self.rows), len(self.rows[0])
        self.start = self.find("S")
        self.goal = self.find("G")

    @classmethod
    def load(cls, path):
        return cls(Path(path).read_text())

    def find(self, ch):
        for r, row in enumerate(self.rows):
            c = row.find(ch)
            if c >= 0:
                return (r, c)
        return None

    def passable(self, cell):
        r, c = cell
        return 0 <= r < self.h and 0 <= c < self.w and self.rows[r][c] != "#"

    def terrain(self, cell):
        return TERRAIN[self.rows[cell[0]][cell[1]]]

    def neighbors(self, cell):
        """Yield (next_cell, move_cost) for every legal move out of cell."""
        r, c = cell
        for dr, dc in MOVES:
            nxt = (r + dr, c + dc)
            if not self.passable(nxt):
                continue
            if dr and dc and not (self.passable((r + dr, c)) and self.passable((r, c + dc))):
                continue  # no corner cutting
            step = DIAGONAL if dr and dc else STRAIGHT
            yield nxt, step * self.terrain(nxt)


def rebuild(parent, goal):
    path, cell = [], goal
    while cell is not None:
        path.append(cell)
        cell = parent[cell]
    return path[::-1]


def dijkstra(grid, start, goal):
    """Reference answer. Returns (cost, path, expanded). Do not edit."""
    g = {start: 0}
    parent = {start: None}
    frontier = [(0, start)]
    closed = set()
    while frontier:
        cost, cell = heapq.heappop(frontier)
        if cell in closed:
            continue
        closed.add(cell)
        if cell == goal:
            return cost, rebuild(parent, goal), len(closed)
        for nxt, step in grid.neighbors(cell):
            new_g = cost + step
            if new_g < g.get(nxt, math.inf):
                g[nxt] = new_g
                parent[nxt] = cell
                heapq.heappush(frontier, (new_g, nxt))
    return math.inf, [], len(closed)


def true_costs_to(grid, goal):
    """Exact cheapest cost from every reachable cell TO goal. Do not edit.

    Runs Dijkstra backwards: the edge u -> v costs step x terrain(v), so when we
    walk from v back to u we pay the terrain of v, the cell being entered.
    """
    dist = {goal: 0}
    frontier = [(0, goal)]
    while frontier:
        d, v = heapq.heappop(frontier)
        if d > dist[v]:
            continue
        for u, _ in grid.neighbors(v):
            # moves are symmetric in geometry; recompute the cost of u -> v
            step = DIAGONAL if (u[0] != v[0] and u[1] != v[1]) else STRAIGHT
            nd = d + step * grid.terrain(v)
            if nd < dist.get(u, math.inf):
                dist[u] = nd
                heapq.heappush(frontier, (nd, u))
    return dist


# ---------------------------------------------------------------- your work


def manhattan(a, b):
    """TODO step 1: 10 x (|dr| + |dc|)."""
    return 0


def octile(a, b):
    """TODO step 1: exact cost on an empty floor grid with 10/14 moves."""
    return 0


def astar(grid, start, goal, h, weight=1.0):
    """TODO step 2: A* search. Returns (cost, path, expanded).

    Order the open list by f = g + weight * h(cell, goal). Break ties on f
    by preferring the smaller h. 'expanded' counts cells removed from the open
    list for the first time (the goal included), exactly as dijkstra() does.
    """
    raise NotImplementedError("write astar() in step 2")


def max_overestimate(grid, goal, h):
    """TODO step 4: the largest h(cell, goal) - true_cost(cell), or 0.

    Use true_costs_to(). A heuristic is admissible when this returns 0.
    """
    raise NotImplementedError("write max_overestimate() in step 4")


# ---------------------------------------------------------------- report


def main():
    maps = sorted(Path(__file__).with_name("maps").glob("*.txt"))
    print(f"{'map':8} {'search':22} {'cost':>6} {'expanded':>9}")
    for path in maps:
        grid = Grid.load(path)
        rows = [("Dijkstra", lambda: dijkstra(grid, grid.start, grid.goal))]
        for name, h, w in [("A* manhattan", manhattan, 1.0),
                           ("A* octile", octile, 1.0),
                           ("A* octile w=2", octile, 2.0)]:
            rows.append((name, lambda h=h, w=w: astar(grid, grid.start, grid.goal, h, w)))
        for name, run in rows:
            try:
                cost, _, expanded = run()
                print(f"{path.stem:8} {name:22} {cost:>6} {expanded:>9}")
            except NotImplementedError as exc:
                print(f"{path.stem:8} {name:22} {'-':>6} {'-':>9}  ({exc})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
