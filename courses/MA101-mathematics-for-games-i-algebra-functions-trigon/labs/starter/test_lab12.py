"""Tests for Lab 12, using the week 12 lecture's values. Run: python3 test_lab12.py"""
import math
from lab12_starter import Vec2, Controller


def check(name, got, want, tol=0.01):
    ok = abs(got - want) <= tol and not math.isnan(got)
    print(("ok  " if ok else "FAIL") + f" {name}: got {got:.4f}, want {want:.4f}")


s = Vec2(1, 2) + Vec2(3, -5)
check("add x", s.x, 4); check("add y", s.y, -3)
d = Vec2(1, 2) - Vec2(3, -5)
check("sub x", d.x, -2); check("sub y", d.y, 7)
m = Vec2(1, -2) * 3
check("scale x", m.x, 3); check("scale y", m.y, -6)
check("length (3, 4)", Vec2(3, 4).length(), 5.0)
n = Vec2(3, 4).normalized()
check("normalized x", n.x, 0.6); check("normalized y", n.y, 0.8)
z = Vec2(0, 0).normalized()
check("zero guard x", z.x, 0.0); check("zero guard y", z.y, 0.0)
tiny = Vec2(1e-12, 0).normalized()
check("tiny guard x", tiny.x, 0.0)

# Lecture section 5 table, speed 5.
c = Controller(5.0)
for keys, inp, raw, norm in [("W", (0, 1), 5.00, 5.00), ("D", (1, 0), 5.00, 5.00),
                             ("W+D", (1, 1), 7.07, 5.00), ("S+A", (-1, -1), 7.07, 5.00),
                             ("W+S", (0, 0), 0.00, 0.00)]:
    v = Vec2(*inp)
    check(f"{keys} raw speed", c.velocity(v, "raw").length(), raw)
    check(f"{keys} normalize speed", c.velocity(v, "normalize").length(), norm)
    check(f"{keys} clamp speed", c.velocity(v, "clamp").length(), norm)

# Lecture section 6: clamp keeps half tilt, normalize does not.
check("stick (0.3, 0.4) clamp", c.velocity(Vec2(0.3, 0.4), "clamp").length(), 2.5)
check("stick (0.3, 0.4) normalize", c.velocity(Vec2(0.3, 0.4), "normalize").length(), 5.0)
check("stick (0.9, 0.9) clamp", c.velocity(Vec2(0.9, 0.9), "clamp").length(), 5.0)
