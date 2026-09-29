"""Checks for MA201 Lab 11. Run: python check_lab11.py

Exits 0 when every check passes, 1 otherwise. On the untouched starter every
check fails; that is expected.
"""
import random
import sys

import partition as p

results = []
PTS, N_TOWN = p.make_scene()
SAMPLE = list(range(0, 4000, 97))          # 42 ids across city and wilderness


def check(name, fn):
    try:
        ok, detail = fn()
    except NotImplementedError as exc:
        ok, detail = False, f"not written yet ({exc})"
    except Exception as exc:
        ok, detail = False, f"{type(exc).__name__}: {exc}"
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + ("" if ok else f"  -> {detail}"))


def radius(i):
    return p.R_TOWN if i < N_TOWN else p.R_WILD


def cell_size():
    got = [p.best_cell_size(4, 2000 / 64 ** 2), p.best_cell_size(10, 0.02),
           p.best_cell_size(10, 0.02, k=0.25)]
    want = [2.5398, 10.0, 6.2996]
    return all(abs(g - w) < 1e-3 for g, w in zip(got, want)), f"got {got}, want {want}"


def grid_exact():
    for s in (2.5, 8, 40):
        g = p.Grid(PTS, s)
        for i in SAMPLE:
            got, want = g.query(i, radius(i)), p.brute_neighbors(PTS, i, radius(i))
            if got != want:
                return False, f"s={s}, id {i}: got {len(got)} ids, brute force finds {len(want)}"
    return True, ""


def grid_counts():
    g = p.Grid(PTS, 16)
    g.query(2500, p.R_WILD)
    x, y = PTS[2500]
    cells = (int((x + 30) // 16) - int((x - 30) // 16) + 1) * (int((y + 30) // 16) - int((y - 30) // 16) + 1)
    return g.cells_visited == cells and g.tested > 0, f"cells_visited {g.cells_visited}, want {cells}"


def grid_move():
    g = p.Grid(PTS, 8)
    rng = random.Random(4)
    changed = 0
    pts = list(PTS)
    for _ in range(3000):
        i = rng.randrange(len(pts))
        x, y = pts[i]
        nx, ny = min(1023.9, max(0, x + rng.uniform(-3, 3))), min(1023.9, max(0, y + rng.uniform(-3, 3)))
        changed += g.move(i, nx, ny)
        pts[i] = (nx, ny)
    if not 0 < changed < 3000:
        return False, f"{changed} of 3000 small moves changed cell; expected some but not all"
    total = sum(len(v) for v in g.cells.values())
    if total != len(pts):
        return False, f"cells hold {total} ids, want {len(pts)} (duplicates or losses)"
    for i in SAMPLE:
        if g.query(i, radius(i)) != p.brute_neighbors(pts, i, radius(i)):
            return False, f"after moves, query for id {i} disagrees with brute force"
    return True, ""


def tree_shape():
    tree = p.build_tree(PTS)
    leaves = tree.leaves()
    n = sum(len(l.ids) for l in leaves)
    over = [l for l in leaves if len(l.ids) > 8 and l.depth < 10]
    small = min(l.size for l in leaves)
    ok = n == len(PTS) and not over and small == 2.0 and len(leaves) > 500
    return ok, f"ids {n}, overfull leaves {len(over)}, smallest leaf {small}, leaves {len(leaves)}"


def tree_exact():
    tree = p.build_tree(PTS)
    for i in SAMPLE:
        if tree.query(i, radius(i)) != p.brute_neighbors(PTS, i, radius(i)):
            return False, f"id {i} disagrees with brute force"
    return True, ""


def tree_stacked():
    pts = [(100.0, 100.0)] * 50 + [(900.0, 900.0)]
    tree = p.build_tree(pts)
    deep = max(l.depth for l in tree.leaves())
    got = tree.query(0, 1.0)
    return deep == 10 and got == list(range(1, 50)), f"max depth {deep} (want 10), {len(got)} neighbors (want 49)"


check("step 1: best_cell_size, including the weighted form", cell_size)
check("step 2: grid query matches brute force at three cell sizes", grid_exact)
check("step 2: grid counts the cells it visits", grid_counts)
check("step 3: grid move keeps every id exactly once", grid_move)
check("step 4: quadtree leaves obey capacity and depth", tree_shape)
check("step 4: quadtree query matches brute force", tree_exact)
check("step 4: 50 entities on one spot stop at max depth", tree_stacked)
print(f"{sum(results)}/{len(results)} checks pass")
sys.exit(0 if all(results) else 1)
