"""MA101 Lab 10 starter: orbits and bursts.

Python 3, standard library only. Fill in every function marked TODO,
then run `python3 test_lab10.py`. Every line must print `ok`.
Angles inside this file are in radians unless a name ends in _deg.
"""
import math


class Vec2:
    """A 2D vector with +, - and scalar *. Given, do not change."""

    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, o):
        return Vec2(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Vec2(self.x - o.x, self.y - o.y)

    def __mul__(self, k):
        return Vec2(self.x * k, self.y * k)

    __rmul__ = __mul__

    def __repr__(self):
        return f"Vec2({self.x:.3f}, {self.y:.3f})"


def deg_to_rad(d):
    """Degrees to radians."""
    raise NotImplementedError("TODO")


def rad_to_deg(r):
    """Radians to degrees."""
    raise NotImplementedError("TODO")


def orbit_positions(center, r, n, omega, t, theta0=0.0):
    """Positions of n orbs on a ring of radius r around center (a Vec2).
    Orb k is at angle theta0 + omega*t + 2*pi*k/n. Returns a list of Vec2."""
    raise NotImplementedError("TODO")


def chord_gap(r, n):
    """Straight-line gap between neighbouring orbs: 2 r sin(pi / n)."""
    raise NotImplementedError("TODO")


def hits_per_second(n, omega):
    """How often an orb passes a fixed spot on the ring: n omega / (2 pi)."""
    raise NotImplementedError("TODO")


def burst_velocities(speed, n, theta0=0.0):
    """n velocities of length `speed`, evenly spaced around the full circle."""
    raise NotImplementedError("TODO")


def spread_velocities(speed, aim, spread, n):
    """n velocities across a cone of total angle `spread` centred on `aim`.
    Pellet k is at aim - spread/2 + spread*k/(n-1). Handle n == 1."""
    raise NotImplementedError("TODO")
