"""Tests for Lab 10, using the week 10 lecture's values. Run: python3 test_lab10.py"""
import math
from lab10_starter import Vec2, deg_to_rad, rad_to_deg, orbit_positions, chord_gap, \
    hits_per_second, burst_velocities, spread_velocities


def check(name, got, want, tol=0.05):
    ok = abs(got - want) <= tol
    print(("ok  " if ok else "FAIL") + f" {name}: got {got:.4f}, want {want:.4f}")
    return ok


check("deg_to_rad(90)", deg_to_rad(90), 1.5708, 1e-4)
check("rad_to_deg(pi)", rad_to_deg(math.pi), 180.0, 1e-6)
check("rad_to_deg(1)", rad_to_deg(1), 57.2958, 1e-4)

# Lecture section 4 table: N = 3, r = 100, omega = pi, theta0 = 0, centre at origin.
table = {0.0: [(100.0, 0.0), (-50.0, 86.6), (-50.0, -86.6)],
         0.25: [(70.7, 70.7), (-96.6, 25.9), (25.9, -96.6)]}
for t, rows in table.items():
    ps = orbit_positions(Vec2(0, 0), 100, 3, math.pi, t)
    for k, (x, y) in enumerate(rows):
        check(f"orb {k} x at t={t}", ps[k].x, x)
        check(f"orb {k} y at t={t}", ps[k].y, y)

check("chord_gap(100, 3)", chord_gap(100, 3), 173.2)
check("chord_gap(100, 6)", chord_gap(100, 6), 100.0)
check("hits_per_second(3, pi)", hits_per_second(3, math.pi), 1.5, 1e-9)

for i, v in enumerate(burst_velocities(300, 8)):
    check(f"burst {i} length", math.hypot(v.x, v.y), 300.0, 1e-6)

angles = [math.degrees(math.atan2(v.y, v.x))
          for v in spread_velocities(1.0, deg_to_rad(30), deg_to_rad(20), 5)]
for got, want in zip(angles, [20, 25, 30, 35, 40]):
    check("spread angle", got, want, 1e-6)
