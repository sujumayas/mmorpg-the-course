"""MA201 Lab 05: a quaternion toolkit.

Plain Python 3.10+, standard library only. Quaternions are tuples (w, x, y, z)
in this file. Engines and glTF often print them as (x, y, z, w); convert when
you read engine output. Angles in the public functions are in degrees.
Axes: +y is up, the object's forward is (0, 0, -1), right-handed.

Fill in every function marked TODO. Run `python test_lab05.py` to check.
"""
import csv
import math

UP, RIGHT, BACK = (0.0, 1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0)


def dot(a, b):
    """Given: 4D dot product."""
    return sum(p * q for p, q in zip(a, b))


def conj(q):
    """Given: conjugate (the inverse, for a unit quaternion)."""
    return (q[0], -q[1], -q[2], -q[3])


def yaw_of(q):
    """Given: yaw in degrees (-180, 180] of the object's forward vector after q."""
    f = rotate(q, (0.0, 0.0, -1.0))
    return math.degrees(math.atan2(-f[0], -f[2]))


# ---------------------------------------------------------------- part A

def from_axis_angle(axis, deg):
    """TODO: unit quaternion for a turn of `deg` degrees about `axis`.
    Normalize the axis first so callers can pass (0, 2, 0)."""
    raise NotImplementedError


def to_axis_angle(q):
    """TODO: return (axis, deg) with deg in [0, 360]. For the identity return
    ((0, 1, 0), 0.0)."""
    raise NotImplementedError


def normalize(q):
    """TODO: scale q to length 1."""
    raise NotImplementedError


def mul(a, b):
    """TODO: quaternion product a * b ('apply b first, then a')."""
    raise NotImplementedError


def rotate(q, v):
    """TODO: rotate 3D vector v by q with q * (0, v) * conj(q). Return a 3-tuple."""
    raise NotImplementedError


def from_euler_yxz(yaw, pitch, roll):
    """TODO: Godot's default order, q = q_y(yaw) * q_x(pitch) * q_z(roll)."""
    raise NotImplementedError


def turn_between(a, b):
    """TODO: the smallest rotation angle in degrees that takes orientation a to b."""
    raise NotImplementedError


# ---------------------------------------------------------------- part B

def slerp(a, b, t, shortest=True):
    """TODO: spherical linear interpolation. With shortest=True, flip b when
    dot(a, b) < 0. When sin(omega) < 1e-6, fall back to normalized lerp."""
    raise NotImplementedError


def nlerp(a, b, t, shortest=True):
    """TODO: normalize((1 - t) * a + t * b), with the same sign rule."""
    raise NotImplementedError


# ---------------------------------------------------------------- part C

def load_keys(path):
    """Given: read turret_keys.csv -> list of (time, q) with q as (w, x, y, z)."""
    keys = []
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            q = (float(row["qw"]), float(row["qx"]), float(row["qy"]), float(row["qz"]))
            keys.append((float(row["time"]), q))
    return keys


def long_way_segments(keys):
    """TODO: indices i of the segments keys[i] -> keys[i+1] where a naive
    (unchecked) slerp turns more than 180 degrees."""
    raise NotImplementedError


def max_yaw_step(keys, fps=60, shortest=True):
    """TODO: replay the keys at `fps` frames per second with slerp (checked or
    not) and return the largest change in yaw between two consecutive frames,
    in degrees, measured the short way (wrap the difference to [-180, 180])."""
    raise NotImplementedError


if __name__ == "__main__":
    a, b = from_axis_angle(UP, 170), from_axis_angle(UP, -170)
    print("dot", round(dot(a, b), 4), "turn", round(turn_between(a, b), 2))
    for t in (0, 0.25, 0.5, 0.75, 1):
        print(t, round(yaw_of(slerp(a, b, t, False)), 2), round(yaw_of(slerp(a, b, t)), 2))
