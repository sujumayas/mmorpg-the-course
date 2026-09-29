"""MA201 Lab 13 starter: the archer's aim.

Standard library only. Positions and velocities are tuples. The top-down
functions use 2D tuples (x, y). The ballistic functions use 3D tuples
(x, y, z) with y up.

Five functions are stubs (marked TODO). As shipped they return None or 0, so
the file runs, the duel prints, and the exact aim never fires. Fill them in
using lecture sections 2 to 4, then run `python test_lab13.py`.

    python aim.py                          # TF2 table and a duel table
    python aim.py --speed 15 --jink 0.3    # duel with another shot speed
"""
import argparse
import math
import random


def dot(a, b):
    return sum(p * q for p, q in zip(a, b))


# ------------------------------------------------------------- your code
def intercept_time(D, u, s, delay=0.0):
    """Flight time after release of a straight shot at speed s that hits a
    target starting at D (relative to the shooter) with constant velocity u.
    The shot leaves `delay` seconds after the decision (cast time or latency).
    Return the smallest positive root, or None if no aim can hit."""
    # TODO: shift D by u * delay, build a, b, c, handle a == 0 (use a
    # tolerance), check the discriminant, return the smallest positive root.
    return None


def aim_point(D, u, s, delay=0.0):
    """The point the shot must be aimed at, or None."""
    # TODO: use intercept_time; the target is at D + u * (delay + t).
    return None


def launch_angles(x, y, s, g=9.81):
    """Elevation angles in degrees (low, high) that hit a fixed point at
    horizontal distance x > 0 and height y, launch speed s. None if out of reach."""
    # TODO: the launch angle formula from section 3.
    return None


def ballistic_intercept(D, u, s, g=9.81, t_max=20.0, n=2000):
    """Earliest flight time t and launch velocity v (3D, y up) of a shot at
    speed s under gravity g that hits a target at D moving at u.
    Return (t, v) or None. Scan for the first sign change of
    f(t) = |D + u t + (0, g t^2 / 2, 0)| - s t, then bisect."""
    # TODO: section 4.
    return None


def dodge_budget(target_speed, flight_time, delay, reaction):
    """How far the target can move after it notices the shot (section 4)."""
    # TODO
    return 0.0


# ------------------------------------------------------------- given
def estimate_time(D, u, s):
    """CS203's one-step estimate: flight time to where the target is now."""
    return math.sqrt(dot(D, D)) / s


def aim_direction(mode, D, u, s):
    """Unit aim direction for 'body', 'estimate' or 'exact', or None."""
    if mode == "body":
        p = D
    elif mode == "estimate":
        T = estimate_time(D, u, s)
        p = (D[0] + u[0] * T, D[1] + u[1] * T)
    else:
        p = aim_point(D, u, s)
        if p is None:
            return None
    n = math.hypot(*p)
    return (p[0] / n, p[1] / n) if n > 0 else None


def simulate_duel(mode, s, shots=500, jink=0.0, target_speed=6.0,
                  radius=0.6, dt=1 / 60, seed=13):
    """Fire `shots` shots at a target 10 to 30 m away moving at target_speed.
    Every 0.1 s the target picks a new random heading with probability `jink`.
    Returns the fraction of shots that hit (a miss if the aim is None)."""
    rng = random.Random(seed)
    hits = 0
    for _ in range(shots):
        r, ang = rng.uniform(10, 30), rng.uniform(0, 2 * math.pi)
        tx, ty = r * math.cos(ang), r * math.sin(ang)
        h = rng.uniform(0, 2 * math.pi)
        ux, uy = target_speed * math.cos(h), target_speed * math.sin(h)
        d = aim_direction(mode, (tx, ty), (ux, uy), s)
        if d is None:
            continue
        px = py = 0.0
        vx, vy = d[0] * s, d[1] * s
        step = 0
        while px * px + py * py < 60 * 60:
            step += 1
            if step % 6 == 0 and rng.random() < jink:
                h = rng.uniform(0, 2 * math.pi)
                ux, uy = target_speed * math.cos(h), target_speed * math.sin(h)
            px, py = px + vx * dt, py + vy * dt
            tx, ty = tx + ux * dt, ty + uy * dt
            if math.hypot(px - tx, py - ty) < radius:
                hits += 1
                break
    return hits / shots


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--speed", type=float, default=25.0, help="shot speed m/s")
    ap.add_argument("--jink", type=float, default=0.0, help="heading change chance per 0.1 s")
    args = ap.parse_args()

    D, s = (1000.0, 0.0), 1100.0
    print("TF2 check (lecture section 2)")
    for name, u in [("toward", (-400, 0)), ("across", (0, 400)),
                    ("away", (400, 0)), ("Heavy across", (0, 230))]:
        t = intercept_time(D, u, s)
        print(f"  {name:12} t = {t}" if t is None else f"  {name:12} t = {t:.4f} s")

    print(f"\nDuel, shot speed {args.speed} m/s, jink {args.jink}")
    for mode in ("body", "estimate", "exact"):
        print(f"  {mode:8} hit rate {simulate_duel(mode, args.speed, jink=args.jink):.3f}")


if __name__ == "__main__":
    main()
