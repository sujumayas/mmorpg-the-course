"""MA201 Lab 09 starter: a narrow phase that returns contacts.

Standard library only. Every test returns either None (no overlap) or a pair
(normal, depth): normal is a unit vector (tuple) pointing from the FIRST shape
toward the SECOND, depth is how far they overlap along it.

The functions marked TODO are stubs that always answer None, so this file runs
but finds no collisions. Fill them in from lecture sections 2 to 4, then run
`python test_lab09.py`.

    python narrow.py            # false-hit experiment (Part C)
"""
import math
import random


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


# ------------------------------------------------------------- part A: 3D
def sphere_sphere(ca, ra, cb, rb):
    """Spheres (center, radius). If the centers coincide use normal (0, 1, 0)."""
    # TODO
    return None


def aabb_aabb(ca, ha, cb, hb):
    """Boxes as (center, half-extents), 3D. Normal is +/- a world axis."""
    # TODO: smallest-depth axis, signed from A toward B
    return None


def aabb_sphere(bc, bh, sc, r):
    """Box (center, half-extents) against sphere. Normal points box -> sphere.
    Clamp the sphere center into the box to find the closest point."""
    # TODO (you may ignore the case of a center inside the box)
    return None


# ------------------------------------------------------ part B: 2D oriented boxes
def make_box(center, half_w, half_h, angle_deg):
    t = math.radians(angle_deg)
    return {
        "c": tuple(center),
        "h": (half_w, half_h),
        "axes": ((math.cos(t), math.sin(t)), (-math.sin(t), math.cos(t))),
    }


def projection_radius(box, n):
    """Half-width of the box's shadow on unit axis n: hu*|u.n| + hv*|v.n|."""
    # TODO
    return 0.0


def sat_obb(a, b):
    """Separating axis test for two oriented rectangles. Test a's two axes, then
    b's two. Return None on the first gap (overlap <= 0), else (normal, depth)
    for the smallest overlap, normal pointing from a toward b."""
    # TODO
    return None


def aabb_of(box):
    """Axis-aligned half-extents of an oriented box (already written for you)."""
    return (projection_radius(box, (1.0, 0.0)), projection_radius(box, (0.0, 1.0)))


# ------------------------------------------------- part C: false-hit experiment
def false_hit_rate(angle_deg, trials=20000, seed=7):
    """Two 2 x 1 boxes (half-extents 1, 0.5); B rotated by angle_deg, placed at a
    random offset in [-3, 3]^2. Of the placements where the AABB test says hit,
    what fraction does SAT say miss?"""
    rng = random.Random(seed)
    a = make_box((0, 0), 1, 0.5, 0)
    aabb_hits = false_hits = 0
    for _ in range(trials):
        b = make_box((rng.uniform(-3, 3), rng.uniform(-3, 3)), 1, 0.5, angle_deg)
        hb = aabb_of(b)
        if all(abs(b["c"][i]) < a["h"][i] + hb[i] for i in (0, 1)):
            aabb_hits += 1
            if sat_obb(a, b) is None:
                false_hits += 1
    return false_hits / aabb_hits if aabb_hits else float("nan")


if __name__ == "__main__":
    for ang in (0, 15, 30, 45, 60, 75, 90):
        print(f"B rotated {ang:2d} deg: false-hit rate of AABB test {false_hit_rate(ang):.3f}")
