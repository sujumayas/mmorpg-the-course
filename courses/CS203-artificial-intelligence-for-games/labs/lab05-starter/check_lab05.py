"""Checks for CS203 Lab 05. Run: python check_lab05.py

Exits with status 0 when every check passes, 1 otherwise. On the untouched
starter every check fails; that is expected.
"""
import random
import sys

import navmesh as nm

results = []


def check(name, fn):
    try:
        ok, detail = fn()
    except NotImplementedError as exc:
        ok, detail = False, f"not written yet ({exc})"
    except Exception as exc:
        ok, detail = False, f"{type(exc).__name__}: {exc}"
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + ("" if ok else f"  -> {detail}"))


SQUARE = [(0, 0), (2, 0), (2, 2), (0, 2)]
TRIANGLE = [(0, 0), (4, 0), (0, 4)]


def inside():
    cases = [(SQUARE, (1, 1), True), (SQUARE, (2, 1), True), (SQUARE, (0, 0), True),
             (SQUARE, (3, 1), False), (SQUARE, (1, -0.1), False),
             (TRIANGLE, (1, 1), True), (TRIANGLE, (3, 2), False), (TRIANGLE, (2, 2), True)]
    for poly, p, want in cases:
        if bool(nm.point_in_convex(poly, p)) != want:
            return False, f"point_in_convex({poly}, {p}) should be {want}"
    locs = [((1, 1), 0), ((6, 2), 1), ((13, 4), 2), ((11, 8.5), 3), ((9, 12), 4), ((6, 5), None)]
    for p, want in locs:
        if nm.find_poly(nm.LEVEL, p) != want:
            return False, f"find_poly(LEVEL, {p}) should be {want}"
    return True, ""


def portals():
    links = nm.find_portals(nm.LEVEL)
    want = {(0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2), (3, 4), (4, 3)}
    if set(links) != want:
        return False, f"got pairs {sorted(links)}"
    edge = links[(0, 1)]
    if set(edge) != {(4, 1), (4, 3)}:
        return False, f"portal 0-1 should join (4, 1) and (4, 3), got {edge}"
    return True, ""


def orientation():
    links = nm.find_portals(nm.LEVEL)
    cases = [((0, 1), ((4, 3), (4, 1))), ((1, 0), ((4, 1), (4, 3))),
             ((2, 3), ((10, 8), (12, 8))), ((4, 3), ((12, 9), (10, 9)))]
    for (i, j), want in cases:
        got = tuple(nm.oriented_portal(nm.LEVEL, links, i, j))
        if got != want:
            return False, f"walking {i} -> {j}: want (left, right) = {want}, got {got}"
    return True, ""


P = [((4, 3), (4, 1)), ((10, 3), (10, 1)), ((10, 8), (12, 8)), ((10, 9), (12, 9))]


def funnel_cases():
    cases = [
        ((1, 1), (13, 11), P, [(1, 1), (10, 3), (12, 9), (13, 11)]),
        ((1, 1), (9, 12), P, [(1, 1), (10, 3), (10, 9), (9, 12)]),
        ((2, 2), (13, 1), P[:2], [(2, 2), (13, 1)]),
        ((1, 3.5), (9, 12), P, [(1, 3.5), (4, 3), (10, 3), (10, 9), (9, 12)]),
        ((13, 11), (1, 1), [(r, l) for l, r in reversed(P)], [(13, 11), (12, 9), (10, 3), (1, 1)]),
    ]
    for s, g, portals, want in cases:
        got = [tuple(p) for p in nm.funnel(s, g, portals)]
        if got != want:
            return False, f"funnel {s} -> {g}: want {want}, got {got}"
    return True, ""


def on_mesh(p, eps=1e-9):
    for poly in nm.LEVEL:
        if all(nm.cross(a, b, p) >= -eps for a, b in zip(poly, poly[1:] + poly[:1])):
            return True
    return False


def random_plans():
    rng = random.Random(203)
    xs = [(0.2, 3.8, 0.2, 3.8), (10.2, 13.8, 0.2, 7.8), (8.2, 13.8, 9.2, 12.8), (4.2, 9.8, 1.2, 2.8)]
    for _ in range(200):
        a, b = rng.sample(xs, 2)
        s = (rng.uniform(a[0], a[1]), rng.uniform(a[2], a[3]))
        g = (rng.uniform(b[0], b[1]), rng.uniform(b[2], b[3]))
        pulled, mids = nm.plan(nm.LEVEL, s, g)
        if nm.length(pulled) > nm.length(mids) + 1e-9:
            return False, f"{s} -> {g}: funnel path longer than midpoint path"
        for p, q in zip(pulled, pulled[1:]):
            for k in range(51):
                t = k / 50
                pt = (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))
                if not on_mesh(pt):
                    return False, f"{s} -> {g}: path leaves the mesh near {pt}"
    return True, ""


check("step 1: point_in_convex and find_poly", inside)
check("step 2: find_portals finds the 4 shared edges both ways", portals)
check("step 3: oriented_portal gives (left, right) for the walker", orientation)
check("step 4: funnel reproduces the lecture's paths", funnel_cases)
check("step 5: 200 random plans stay on the mesh and beat the midpoint path", random_plans)

print(f"\n{sum(results)}/{len(results)} checks pass")
sys.exit(0 if all(results) else 1)
