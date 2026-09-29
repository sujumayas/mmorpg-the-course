"""Checks for MA201 Lab 12. Run: python check_lab12.py

Exits 0 when every check passes, 1 otherwise. On the untouched starter every
check fails; that is expected.
"""
import math
import sys

import raycast as p

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


def close(a, b, tol=1e-3):
    return a is not None and b is not None and abs(a - b) <= tol


def walk_lecture():
    a = math.radians(20)
    hit = p.grid_walk(p.LECTURE_MAP, 2.5, 4.5, math.cos(a), math.sin(a))
    if not hit or not close(hit[0], 3.725) or hit[1] != (6, 5) or hit[2] != "x":
        return False, f"20 deg ray: got {hit}, want (3.725, (6, 5), 'x')"
    up = p.grid_walk(p.LECTURE_MAP, 2.5, 4.5, 0.0, -1.0)
    if not up or not close(up[0], 3.5) or up[1] != (2, 0) or up[2] != "y":
        return False, f"straight up: got {up}, want (3.5, (2, 0), 'y')"
    capped = p.grid_walk(p.LECTURE_MAP, 2.5, 4.5, 1.0, 0.0, t_max=3.0)
    return capped is None, f"t_max 3.0 before a wall at 3.5 should give None, got {capped}"


def walk_ties():
    s = 0.7071
    hit = p.grid_walk(["#####", "#...#", "#.#.#", "#...#", "#####"], 1.5, 1.5, s, s)
    return hit is not None and hit[1] == (2, 2) and hit[2] == "x", f"got {hit}, want cell (2, 2) entered by an x crossing"


def heights():
    off = p.column_heights(p.LECTURE_MAP, 2.5, 4.5, 0, 60, 7, perp=False)
    on = p.column_heights(p.LECTURE_MAP, 2.5, 4.5, 0, 60, 7, perp=True)
    want_off = [59.4, 64.4, 67.5, 68.6, 67.5, 64.4, 59.4]
    ok = all(close(g, w, 0.06) for g, w in zip(off, want_off)) and all(close(g, 68.571, 0.01) for g in on)
    return ok, f"off {[round(x, 1) for x in off]}, on {[round(x, 1) for x in on]}"


def sphere():
    o, d = (0, 0, 0), (1, 0, 0)
    got = [p.ray_sphere(o, d, (10, y, 0), 0.5) for y in (0.0, 0.3, 0.5, 0.6)]
    got += [p.ray_sphere((10, 0, 0), d, (10, 0, 0), 0.5), p.ray_sphere(o, d, (-10, 0, 0), 0.5)]
    want = [9.5, 9.6, 10.0, None, 0.0, None]
    ok = all((g is None and w is None) or close(g, w) for g, w in zip(got, want))
    return ok, f"got {got}, want {want}"


def box():
    s = 1 / math.sqrt(2)
    got = [p.ray_aabb((0, 0, 0), (1, 0, 0), (4, -1, -1), (6, 1, 1)),
           p.ray_aabb((0, 0, 0), (s, s, 0), (4, 3, -1), (6, 5, 1)),
           p.ray_aabb((0, 0, 0), (s, s, 0), (4, 0, -1), (6, 2, 1)),
           p.ray_aabb((0, 0, 0), (0.6, 0.8, 0), (3, 2, -1), (5, 6, 1)),
           p.ray_aabb((0, 5, 0), (1, 0, 0), (4, -1, -1), (6, 1, 1)),
           p.ray_aabb((5, 0, 0), (1, 0, 0), (4, -1, -1), (6, 1, 1))]
    want = [4.0, 5.657, None, 5.0, None, 0.0]
    ok = all((g is None and w is None) or close(g, w) for g, w in zip(got, want))
    return ok, f"got {got}, want {want}"


def sight():
    open_pair = p.can_see(p.ARENA, (1.5, 1.5), (10.5, 1.5))
    blocked = p.can_see(p.ARENA, (1.5, 4.5), (10.5, 4.5))
    corner = p.can_see(["####", "#.##", "##.#", "####"], (1.5, 1.5), (2.5, 2.5))
    return open_pair and not blocked and not corner, \
        f"open {open_pair} (want True), through pillar {blocked} (want False), corner {corner} (want False)"


def exploit():
    a, b = (1.5, 1.5), (4.2, 4.0)
    old, new = p.sampled_can_see(p.ARENA, a, b), p.can_see(p.ARENA, a, b)
    return old and not new, f"sampled says {old}, walk says {new}; want True then False"


check("step 1: grid walk on the lecture map, with t_max", walk_lecture)
check("step 1: exact tie goes to y first", walk_ties)
check("step 2: column heights with and without the correction", heights)
check("step 3: ray against sphere", sphere)
check("step 3: slab test, including parallel and inside", box)
check("step 4: exact line of sight", sight)
check("step 5: the planted exploit is closed", exploit)
print(f"{sum(results)}/{len(results)} checks pass")
sys.exit(0 if all(results) else 1)
