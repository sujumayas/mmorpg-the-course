"""MA201 Lab 01 starter: floor, wall or ceiling.

Vectors are plain tuples (x, y, z). The world is Y-up unless a function takes `up`.
Fill in every function that raises NotImplementedError, then run:  python test_lab01.py
Standard library only.
"""
import csv
import math

EPS = 1e-9

# Engine presets from the week 1 lecture, section 3.
#   kind "cos":   floor if n_hat . up >= value, otherwise wall (no ceilings reported)
#   kind "angle": floor if angle(n_hat, up) <= value (radians), else ceiling if
#                 angle(n_hat, -up) <= value, else wall
PRESETS = {
    "ue5":     ("cos", 0.71),
    "ue3":     ("cos", 0.70),
    "godot47": ("angle", math.radians(45.0) + 0.01),
}


# ---------- Part A: vector basics (given) ----------

def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def scale(a, k):
    return (a[0] * k, a[1] * k, a[2] * k)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def length(a):
    return math.sqrt(dot(a, a))


# ---------- Part B: cross product and triangles ----------

def cross(a, b):
    """The cross product a x b, by the component formula from lecture section 2."""
    raise NotImplementedError("TODO")


def normalize(a):
    """Unit vector in the direction of a, or None if length(a) < EPS."""
    raise NotImplementedError("TODO")


def triangle_normal(a, b, c):
    """Unit normal (b - a) x (c - a), or None for a degenerate triangle."""
    raise NotImplementedError("TODO")


def triangle_area(a, b, c):
    """Area of the triangle: half the length of (b - a) x (c - a)."""
    raise NotImplementedError("TODO")


# ---------- Part C: classification ----------

def classify(n_hat, preset, up=(0.0, 1.0, 0.0)):
    """Return "floor", "wall" or "ceiling" for a unit normal under a preset name
    from PRESETS. Clamp dot products to [-1, 1] before any acos."""
    raise NotImplementedError("TODO")


def side(forward, to_target, up):
    """(forward x to_target) . up. Its sign says which side the target is on;
    what "positive" means depends on the engine (lecture section 4)."""
    raise NotImplementedError("TODO")


# ---------- Part D: the level ----------

def load_level(path="level.csv"):
    """List of (name, a, b, c) with float tuples. Given."""
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            a = tuple(float(r["a" + k]) for k in "xyz")
            b = tuple(float(r["b" + k]) for k in "xyz")
            c = tuple(float(r["c" + k]) for k in "xyz")
            rows.append((r["name"], a, b, c))
    return rows


def area_by_class(triangles, preset, up=(0.0, 1.0, 0.0)):
    """Total area per class: a dict with keys "floor", "wall", "ceiling" and
    "degenerate" (triangles with no normal). Every key must be present."""
    raise NotImplementedError("TODO")
