"""Tests for Lab 11, using the week 11 lecture's tables. Run: python3 test_lab11.py"""
import math
from lab10_starter import Vec2
from lab11_starter import angle_to, shortest_delta, turn_step, time_to_act


def check(name, got, want, tol=0.05):
    ok = abs(got - want) <= tol
    print(("ok  " if ok else "FAIL") + f" {name}: got {got:.4f}, want {want:.4f}")


# atan2 table, section 2 (degrees).
for (dx, dy), want in [((300, 0), 0.0), ((200, 200), 45.0), ((0, 300), 90.0),
                       ((-300, 100), 161.6), ((-300, 0), 180.0),
                       ((100, -300), -71.6), ((-200, -200), -135.0)]:
    check(f"angle_to {dx, dy}", math.degrees(angle_to(Vec2(0, 0), Vec2(dx, dy))), want)

# Wrap table, section 3 (degrees). The tie row only checks the size.
for cur, tgt, want in [(170, -170, 20), (-170, 170, -20), (10, 350, -20), (45, 135, 90)]:
    check(f"shortest_delta {cur} -> {tgt}",
          math.degrees(shortest_delta(math.radians(cur), math.radians(tgt))), want)
check("shortest_delta 90 -> -90 (size)",
      abs(math.degrees(shortest_delta(math.radians(90), math.radians(-90)))), 180)

# Capped step: from 0 toward 90 degrees at 180 deg/s for 1/60 s turns exactly 3 degrees.
check("turn_step", math.degrees(turn_step(0.0, math.radians(90), math.pi, 1 / 60)), 3.0, 1e-6)
check("turn_step no overshoot", math.degrees(turn_step(0.0, math.radians(1), math.pi, 1 / 60)), 1.0, 1e-6)

# Dota 2 table, section 4 (seconds).
check("time_to_act 180, rate 0.5", time_to_act(math.pi, 0.5), 0.176, 0.001)
check("time_to_act 180, rate 0.6", time_to_act(math.pi, 0.6), 0.147, 0.001)
check("time_to_act 180, rate 1.0", time_to_act(math.pi, 1.0), 0.088, 0.001)
check("time_to_act 90, rate 0.5", time_to_act(math.pi / 2, 0.5), 0.082, 0.001)
check("time_to_act 10 deg (inside cone)", time_to_act(math.radians(10), 0.5), 0.0, 1e-9)
