"""CS203 Lab 02 starter: a steering toolkit for a 2D point mass. Standard library only.

Fill in the TODO functions, then run the tests:

    python3 test_steering.py        (or: pytest test_steering.py)

Vectors are plain (x, y) tuples. Units: metres, seconds, m/s, m/s^2.
The update rule and the numbers follow the week 2 lecture.
"""
import math

DT = 1 / 60                               # one frame at 60 Hz


# ------------------------------------------------------- provided helpers

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def scale(a, k):
    return (a[0] * k, a[1] * k)


def length(a):
    return math.hypot(a[0], a[1])


def truncate(a, limit):
    """Clamp the length of a to at most limit, keeping its direction."""
    n = length(a)
    return a if n <= limit else scale(a, limit / n)


# ------------------------------------------------------------- your code

def braking_distance(max_speed, max_accel):
    """TODO step 1. Distance needed to stop from max_speed at max_accel."""
    raise NotImplementedError("braking_distance() is yours to write")


def step(pos, vel, desired_vel, max_speed, max_accel):
    """TODO step 2. One frame of the vehicle model. Return (new_pos, new_vel).
    dv = truncate(desired_vel - vel, max_accel * DT)
    vel = truncate(vel + dv, max_speed); pos = pos + vel * DT."""
    raise NotImplementedError("step() is yours to write")


def seek(pos, target, max_speed):
    """TODO step 3. Desired velocity: full speed straight at target.
    Return (0, 0) if pos == target."""
    raise NotImplementedError("seek() is yours to write")


def flee(pos, threat, max_speed):
    """TODO step 3. Desired velocity: full speed straight away from threat."""
    raise NotImplementedError("flee() is yours to write")


def arrive(pos, target, max_speed, slow_radius):
    """TODO step 4. Like seek, but the desired speed is
    max_speed * min(1, distance / slow_radius). Return (0, 0) at the target."""
    raise NotImplementedError("arrive() is yours to write")


def pursue(pos, quarry_pos, quarry_vel, max_speed):
    """TODO step 5. Seek the quarry's predicted position after T seconds,
    with T = distance / max_speed (Reynolds's T = D * c, c = 1 / max_speed)."""
    raise NotImplementedError("pursue() is yours to write")


def blend(requests, weights):
    """TODO step 6. Weighted sum of desired velocities: sum of w * r."""
    raise NotImplementedError("blend() is yours to write")


# ---------------------------------------- provided: the lecture's experiments

def run_line(slow_radius=0.0, max_speed=6.0, max_accel=12.0, target=(20.0, 0.0), seconds=8.0):
    """Start at rest at the origin, head for target. slow_radius 0 means seek.
    Returns (overshoot past the target in x, settle time or None)."""
    pos, vel, furthest, settled = (0.0, 0.0), (0.0, 0.0), 0.0, None
    for frame in range(round(seconds / DT)):
        if slow_radius > 0:
            want = arrive(pos, target, max_speed, slow_radius)
        else:
            want = seek(pos, target, max_speed)
        pos, vel = step(pos, vel, want, max_speed, max_accel)
        furthest = max(furthest, pos[0])
        near = length(sub(target, pos)) < 0.05 and length(vel) < 0.05
        if not near:
            settled = None
        elif settled is None:
            settled = (frame + 1) * DT
    return max(0.0, furthest - target[0]), settled


def chase(quarry_speed, predict, max_speed=6.0, max_accel=12.0, seconds=20.0):
    """Pursuer at the origin, quarry at (10, 0) running along +y.
    Returns the time until they are within 0.5 m, or None."""
    p, v = (0.0, 0.0), (0.0, 0.0)
    q, qv = (10.0, 0.0), (0.0, quarry_speed)
    for frame in range(1, round(seconds / DT)):
        want = pursue(p, q, qv, max_speed) if predict else seek(p, q, max_speed)
        p, v = step(p, v, want, max_speed, max_accel)
        q = add(q, scale(qv, DT))
        if length(sub(p, q)) < 0.5:
            return frame * DT
    return None


if __name__ == "__main__":
    print(f"braking distance: {braking_distance(6, 12)} m")
    print("seek:            overshoot %.2f m, settled %s" % run_line())
    for r in (1.0, 1.5, 3.0):
        over, t = run_line(slow_radius=r)
        print(f"arrive r = {r}:  overshoot {over:.2f} m, settled {t:.2f} s")
    for s in (3.0, 4.5):
        print(f"quarry {s} m/s: seek {chase(s, False):.2f} s, pursue {chase(s, True):.2f} s")
