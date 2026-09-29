"""AR101 Lab 02 helper: measure a shape's roundness and sharpest corner.

This is a finished tool, not an exercise. Trace the outer outline of a shape as
a list of corner points (any unit: pixels, millimetres on your sketch), then:

    python3 shape_measure.py shapes.csv

shapes.csv has one row per point: name,x,y. Points of one shape must be
consecutive and go around the outline in order (either direction).

It prints, for each shape:
  C      circularity 4*pi*A / P^2  (1.0 circle, 0.785 square, 0.605 triangle)
  theta  sharpest convex corner in degrees (180 means no corner found)
  read   the week 2 lecture's rough reading of those two numbers
"""
import csv
import math
import sys
from collections import OrderedDict


def area_perimeter(pts):
    a = p = 0.0
    for i, (x1, y1) in enumerate(pts):
        x2, y2 = pts[(i + 1) % len(pts)]
        a += x1 * y2 - x2 * y1
        p += math.hypot(x2 - x1, y2 - y1)
    return a / 2, p          # signed area: its sign gives the winding direction


def circularity(pts):
    a, p = area_perimeter(pts)
    return 4 * math.pi * abs(a) / p ** 2


def sharpest_corner(pts):
    """Smallest interior angle among convex corners, in degrees."""
    sign = 1 if area_perimeter(pts)[0] > 0 else -1
    best = 180.0
    n = len(pts)
    for i in range(n):
        ax, ay = pts[i - 1]
        px, py = pts[i]
        bx, by = pts[(i + 1) % n]
        v1 = (ax - px, ay - py)
        v2 = (bx - px, by - py)
        turn = (px - ax) * (by - py) - (py - ay) * (bx - px)
        if turn * sign <= 0:          # reflex (inward) corner or straight: skip
            continue
        cos = (v1[0] * v2[0] + v1[1] * v2[1]) / (math.hypot(*v1) * math.hypot(*v2))
        best = min(best, math.degrees(math.acos(max(-1.0, min(1.0, cos)))))
    return best


def reading(c, theta):
    if theta <= 65:
        return "sharp: danger, speed, aggression"
    if c >= 0.85 and theta >= 120:
        return "round: soft, friendly, safe"
    if 75 <= theta <= 105:
        return "square: stable, solid, dependable"
    return "in between: check it by eye"


def load(path):
    shapes = OrderedDict()
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            shapes.setdefault(row["name"], []).append((float(row["x"]), float(row["y"])))
    return shapes


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "shapes.csv"
    print(f"{'shape':<16}{'points':>7}{'C':>8}{'theta':>8}  read")
    for name, pts in load(path).items():
        c, t = circularity(pts), sharpest_corner(pts)
        print(f"{name:<16}{len(pts):>7}{c:8.3f}{t:8.1f}  {reading(c, t)}")
