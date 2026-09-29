"""MA201 Lab 11 starter: grids, quadtrees and a world boss.

Run:   python partition.py       times each index on the lecture scene and the boss session
Check: python check_lab11.py     exits 0 only when your work is complete

You write the parts marked TODO: best_cell_size(), Grid.query(), Grid.move(),
QuadTree.insert() and QuadTree.query(). Scenes, brute force and timing are provided.
Entities are identified by their index i in the positions list.
"""
import math
import random
import time

WORLD = 1024.0
R_TOWN, R_WILD = 4.0, 30.0


# ---------------------------------------------------------------- provided

def make_scene(seed=7):
    """The lecture's scene: 2,000 in a 64 m city, 2,000 in the wilderness.
    Returns (positions, n_town). Entities 0..n_town-1 are the city."""
    rng = random.Random(seed)
    town = [(rng.uniform(480, 544), rng.uniform(480, 544)) for _ in range(2000)]
    wild = []
    while len(wild) < 2000:
        x, y = rng.uniform(0, WORLD), rng.uniform(0, WORLD)
        if not (416 < x < 608 and 416 < y < 608):
            wild.append((x, y))
    return town + wild, 2000


def boss_session(frames=60, seed=3):
    """Yield (frame, positions). City players walk to a world boss at (200, 800)
    and gather in a 20 m circle; the wilderness stays put."""
    pts, n_town = make_scene()
    rng = random.Random(seed)
    goals = []
    for _ in range(n_town):
        a, d = rng.uniform(0, 2 * math.pi), 10 * math.sqrt(rng.random())
        goals.append((200 + d * math.cos(a), 800 + d * math.sin(a)))
    for f in range(frames + 1):
        t = f / frames
        cur = [(x + (gx - x) * t, y + (gy - y) * t) for (x, y), (gx, gy) in zip(pts[:n_town], goals)]
        yield f, cur + pts[n_town:]


def brute_neighbors(points, i, r):
    """Every j != i with distance <= r, as a sorted list. The truth to test against."""
    x, y = points[i]
    r2 = r * r
    return sorted(j for j, (px, py) in enumerate(points)
                  if j != i and (px - x) ** 2 + (py - y) ** 2 <= r2)


# ---------------------------------------------------------------- TODO: yours

def best_cell_size(r, rho, k=1.0):
    """Cell size minimizing W(s) = k (2r/s + 1)^2 + rho (2r + s)^2.

    k is the cost of visiting a cell relative to testing one entity.
    With k = 1 this is the lecture's (2r / rho)^(1/3). Derive the general case.
    """
    raise NotImplementedError("best_cell_size")  # TODO


class Grid:
    """Hashed uniform grid: dict (cx, cy) -> list of entity ids."""

    def __init__(self, points, s):
        self.s = s
        self.points = list(points)          # current position of each id
        self.cells = {}
        self.cell_of = []                   # current cell key of each id
        for i, (x, y) in enumerate(self.points):
            key = self.key(x, y)
            self.cells.setdefault(key, []).append(i)
            self.cell_of.append(key)
        self.cells_visited = 0              # add to these in query()
        self.tested = 0

    def key(self, x, y):
        return (int(x // self.s), int(y // self.s))

    def query(self, i, r):
        """Sorted ids j != i within distance r of entity i (squared distances).
        Visit every cell overlapping the square of half-width r; add the
        number of cells to self.cells_visited and entities tested to self.tested."""
        raise NotImplementedError("Grid.query")  # TODO

    def move(self, i, x, y):
        """Entity i moves to (x, y). Touch the cell lists only if its cell changed.
        Return True if it changed cell."""
        raise NotImplementedError("Grid.move")  # TODO


class QuadTree:
    """Point quadtree. A leaf splits when it holds more than CAPACITY ids and
    its depth is below MAX_DEPTH. Child order: index = (y >= mid) * 2 + (x >= mid)."""
    CAPACITY, MAX_DEPTH = 8, 10

    def __init__(self, points, x=0.0, y=0.0, size=WORLD, depth=0):
        self.points = points                # shared list of positions
        self.x, self.y, self.size, self.depth = x, y, size, depth
        self.ids, self.kids = [], None
        self.nodes_visited = 0              # root only: add to these in query()
        self.tested = 0

    def insert(self, i):
        """Insert id i at self.points[i]."""
        raise NotImplementedError("QuadTree.insert")  # TODO

    def query(self, i, r):
        """Sorted ids j != i within distance r of entity i. Count, on the node
        query() is called on, every node visited and every entity tested."""
        raise NotImplementedError("QuadTree.query")  # TODO

    def leaves(self):
        if self.kids is None:
            return [self]
        return [leaf for k in self.kids for leaf in k.leaves()]


def build_tree(points):
    tree = QuadTree(points)
    for i in range(len(points)):
        tree.insert(i)
    return tree


# ---------------------------------------------------------------- timing

def time_queries(index, points, n_town):
    t0 = time.perf_counter()
    for i in range(len(points)):
        index.query(i, R_TOWN if i < n_town else R_WILD)
    return (time.perf_counter() - t0) * 1000


if __name__ == "__main__":
    pts, n_town = make_scene()
    try:
        for s in (4, 8, 16):
            g = Grid(pts, s)
            ms = time_queries(g, pts, n_town)
            print(f"grid s={s:2d}: {ms:7.1f} ms, cells {g.cells_visited:,}, tested {g.tested:,}")
        t0 = time.perf_counter()
        tree = build_tree(pts)
        build = (time.perf_counter() - t0) * 1000
        ms = time_queries(tree, pts, n_town)
        print(f"quadtree : {ms:7.1f} ms (+{build:.1f} ms build), nodes {tree.nodes_visited:,}, "
              f"tested {tree.tested:,}")
    except NotImplementedError as exc:
        print(f"-- {exc} not written yet")
