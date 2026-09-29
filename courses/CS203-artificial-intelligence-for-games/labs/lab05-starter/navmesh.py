"""CS203 Lab 05 starter: a navigation mesh by hand.

A mesh is a list of convex polygons. Each polygon is a list of (x, y)
vertices in counter-clockwise order. Two polygons are neighbours when one
lists an edge a -> b and the other lists the same edge as b -> a. Vertices
that sit in the middle of a straight side are allowed (they let a big room
share just part of one wall with a small door).

Run:   python navmesh.py        prints the lecture's example path
Check: python check_lab05.py    exits 0 only when your work is complete

Edit the five functions marked TODO. corridor() and plan() are written for
you and call your functions.
"""
import math
import sys
from collections import deque

# The level from lecture section 2, with extra vertices where portals meet walls.
LEVEL = [
    [(0, 0), (4, 0), (4, 1), (4, 3), (4, 4), (0, 4)],                  # 0 room A
    [(4, 1), (10, 1), (10, 3), (4, 3)],                                # 1 corridor
    [(10, 0), (14, 0), (14, 8), (12, 8), (10, 8), (10, 3), (10, 1)],   # 2 room B
    [(10, 8), (12, 8), (12, 9), (10, 9)],                              # 3 door
    [(8, 9), (10, 9), (12, 9), (14, 9), (14, 13), (8, 13)],            # 4 north room
]


def cross(o, a, b):
    """2D cross product of (a - o) and (b - o). Positive: b is left of o->a."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def length(points):
    return sum(math.dist(a, b) for a, b in zip(points, points[1:]))


# ---------------------------------------------------------------- your work


def point_in_convex(poly, p):
    """TODO step 1: True if p is inside or on the boundary of the CCW polygon."""
    raise NotImplementedError("write point_in_convex() in step 1")


def find_poly(mesh, p):
    """TODO step 1: index of the first polygon containing p, or None."""
    raise NotImplementedError("write find_poly() in step 1")


def find_portals(mesh):
    """TODO step 2: {(i, j): (a, b)} for every pair of neighbours.

    (a, b) is the shared edge in the order polygon i lists it. Include both
    (i, j) and (j, i).
    """
    raise NotImplementedError("write find_portals() in step 2")


def oriented_portal(mesh, portals, i, j):
    """TODO step 3: (left, right) endpoints seen by someone walking from i into j."""
    raise NotImplementedError("write oriented_portal() in step 3")


def funnel(start, goal, portals):
    """TODO step 4: simple stupid funnel. portals = [(left, right), ...]."""
    raise NotImplementedError("write funnel() in step 4")


# ---------------------------------------------------------------- provided


def corridor(mesh, start, goal):
    """Polygon indices from start's polygon to goal's (breadth-first search)."""
    s, g = find_poly(mesh, start), find_poly(mesh, goal)
    if s is None or g is None:
        return None
    links = find_portals(mesh)
    parent = {s: None}
    queue = deque([s])
    while queue:
        i = queue.popleft()
        if i == g:
            break
        for (a, b) in links:
            if a == i and b not in parent:
                parent[b] = i
                queue.append(b)
    if g not in parent:
        return None
    path, i = [], g
    while i is not None:
        path.append(i)
        i = parent[i]
    return path[::-1]


def plan(mesh, start, goal):
    """Return (funnel_path, midpoint_path) from start to goal, or None."""
    polys = corridor(mesh, start, goal)
    if polys is None:
        return None
    links = find_portals(mesh)
    portals = [oriented_portal(mesh, links, a, b) for a, b in zip(polys, polys[1:])]
    mids = [((l[0] + r[0]) / 2, (l[1] + r[1]) / 2) for l, r in portals]
    return funnel(start, goal, portals), [start] + mids + [goal]


def main():
    try:
        pulled, mids = plan(LEVEL, (1, 1), (13, 11))
    except NotImplementedError as exc:
        print(f"not finished: {exc}")
        return 0
    print("funnel:  ", pulled, f"{length(pulled):.2f} m")
    print("midpoint:", mids, f"{length(mids):.2f} m")
    return 0


if __name__ == "__main__":
    sys.exit(main())
