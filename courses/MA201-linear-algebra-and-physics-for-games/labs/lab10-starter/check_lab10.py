"""Checks for MA201 Lab 10. Run: python check_lab10.py

Exits 0 when every check passes, 1 otherwise. On the untouched starter every
check fails; that is expected.
"""
import random
import sys

import impulses as p

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
    return abs(a - b) <= tol


def lecture_table():
    rows = [(0.17, 0.17, 0.95, 0.332, 0.050, 1.950), (0.17, None, 0.75, 0.595, -1.5, 0.0),
            (10.0, 1.0, 1.0, 3.636, 1.636, 3.636), (1.0, 10.0, 1.0, 3.636, -1.636, 0.364),
            (1.0, 1.0, 0.0, 1.0, 1.0, 1.0)]
    for ma, mb, e, j0, va, vb in rows:
        a, b = p.Body(0, 0, 2.0, 0, mass=ma), p.Body(0.2, 0, 0, 0, mass=mb)
        j = p.resolve_velocity(a, b, 1.0, 0.0, e)
        if not (close(j, j0) and close(a.vx, va) and close(b.vx, vb)):
            return False, f"masses {ma},{mb} e={e}: got j={j:.3f} {a.vx:.3f} {b.vx:.3f}"
    return True, ""


def separating_and_threshold():
    a, b = p.Body(0, 0, -1.0, 0), p.Body(0.2, 0, 1.0, 0)
    if p.resolve_velocity(a, b, 1.0, 0.0, 0.9) != 0 or a.vx != -1.0:
        return False, "separating pair must get no impulse"
    a, b = p.Body(0, 0, 0.5, 0), p.Body(0.2, 0, 0, 0, mass=None)
    p.resolve_velocity(a, b, 1.0, 0.0, 0.9, threshold=1.0)
    if not close(a.vx, 0.0):
        return False, f"0.5 m/s into a wall under a 1 m/s threshold should stop, got {a.vx}"
    a2 = p.Body(0, 0, 1.5, 0)
    p.resolve_velocity(a2, p.Body(0.2, 0, 0, 0, mass=None), 1.0, 0.0, 0.9, threshold=1.0)
    return close(a2.vx, -1.35), f"1.5 m/s above threshold should rebound at -1.35, got {a2.vx}"


def momentum_conserved():
    rng = random.Random(10)
    for _ in range(200):
        a = p.Body(0, 0, rng.uniform(-3, 3), rng.uniform(-3, 3), mass=rng.uniform(0.1, 20))
        b = p.Body(1, 1, rng.uniform(-3, 3), rng.uniform(-3, 3), mass=rng.uniform(0.1, 20))
        ang = rng.uniform(0, 6.283)
        nx, ny = p.math.cos(ang), p.math.sin(ang)
        e = rng.uniform(0, 1)
        before = [x + y for x, y in zip(a.momentum(), b.momentum())]
        ke0 = a.energy() + b.energy()
        vn = (b.vx - a.vx) * nx + (b.vy - a.vy) * ny
        ma, mb = 1 / a.inv_mass, 1 / b.inv_mass
        p.resolve_velocity(a, b, nx, ny, e)
        after = [x + y for x, y in zip(a.momentum(), b.momentum())]
        if any(abs(x - y) > 1e-9 for x, y in zip(before, after)):
            return False, "momentum changed"
        lost = ke0 - (a.energy() + b.energy())
        want = p.reduced_mass_loss(ma, mb, e, vn) if vn < 0 else 0.0
        if abs(lost - want) > 1e-9:
            return False, f"energy lost {lost:.6f}, reduced_mass_loss says {want:.6f}"
    return True, ""


def friction_clamp():
    floor = p.Body(0, -1, 0, 0, mass=None)
    crate = p.Body(0, 0, 3.0, -2.0, mass=10.0)
    j = p.resolve_velocity(floor, crate, 0.0, 1.0, 0.0)
    jt = p.apply_friction(floor, crate, 0.0, 1.0, j, 0.5)
    if not (close(j, 20) and close(abs(jt), 10) and close(crate.vx, 2.0) and close(crate.vy, 0)):
        return False, f"mu 0.5: j={j}, jt={jt}, v=({crate.vx}, {crate.vy}); want 20, 10, (2, 0)"
    crate = p.Body(0, 0, 3.0, -2.0, mass=10.0)
    j = p.resolve_velocity(floor, crate, 0.0, 1.0, 0.0)
    p.apply_friction(floor, crate, 0.0, 1.0, j, 1.5)
    return close(crate.vx, 0.0), f"mu 1.5 should stop the slide, got vx={crate.vx}"


def position_split():
    a, b = p.Body(0, 0, 0, 0, mass=1.0), p.Body(0.15, 0, 0, 0, mass=3.0)
    corr = p.correct_position(a, b, 1.0, 0.0, 0.055)
    ok = close(corr, 0.01, 1e-9) and close(a.x, -0.0075, 1e-9) and close(b.x, 0.1525, 1e-9)
    ok = ok and a.vx == 0 and b.vx == 0
    wall, ball = p.Body(0, 0, 0, 0, mass=None), p.Body(0.1, 0, 0, 0)
    p.correct_position(wall, ball, 1.0, 0.0, 0.003)
    return ok and wall.x == 0 and ball.x == 0.1, f"got corr={corr}, a.x={a.x}, b.x={b.x}"


def combine_rules():
    got = [p.combine(0.9, 0.0, r) for r in ("max", "average", "min", "multiply", "add")]
    want = [0.9, 0.45, 0.0, 0.0, 0.9]
    ok = all(close(g, w, 1e-12) for g, w in zip(got, want)) and close(p.combine(0.5, 0.7, "add"), 1.0)
    return ok, f"got {got}, want {want} and add(0.5, 0.7) = 1.0"


def drop_matches_lecture():
    counts = [len(p.drop_test(1.0, 0.8, 0.0, "max", thr)) for thr in (1.0, 2.0)]
    return counts == [7, 4], f"bounce counts at thresholds 1 and 2: got {counts}, want [7, 4]"


check("step 1: the lecture's collision table", lecture_table)
check("step 1: separating pairs and the threshold", separating_and_threshold)
check("step 2: momentum and energy over 200 random collisions", momentum_conserved)
check("step 3: friction clamp on the landing crate", friction_clamp)
check("step 4: position correction by inverse mass, with slop", position_split)
check("step 5: combine rules", combine_rules)
check("step 5: drop test reproduces 7 and 4 bounces", drop_matches_lecture)
print(f"{sum(results)}/{len(results)} checks pass")
sys.exit(0 if all(results) else 1)
