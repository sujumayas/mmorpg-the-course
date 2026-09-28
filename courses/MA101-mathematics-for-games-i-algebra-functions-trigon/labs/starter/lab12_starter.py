"""MA101 Lab 12 starter: a movement controller you can trust.

Implement the Vec2 class and Controller.velocity, then run `python3 test_lab12.py`.
Your finished Vec2 is reused by lab13_starter.py, so keep this file next to it.
"""
import math


class Vec2:
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, o):
        raise NotImplementedError("TODO")

    def __sub__(self, o):
        raise NotImplementedError("TODO")

    def __mul__(self, k):
        """Scalar multiply: Vec2 * number."""
        raise NotImplementedError("TODO")

    __rmul__ = __mul__

    def length(self):
        raise NotImplementedError("TODO")

    def normalized(self):
        """Unit vector in the same direction. Return Vec2(0, 0) when the length
        is below 1e-9. Never return NaN."""
        raise NotImplementedError("TODO")

    def __repr__(self):
        return f"Vec2({self.x:.3f}, {self.y:.3f})"


class Controller:
    def __init__(self, speed=5.0):
        self.speed = speed

    def velocity(self, input_vec, mode):
        """mode "raw": speed * input.
        mode "normalize": speed * input.normalized().
        mode "clamp": shrink input to length 1 only if it is longer, then * speed."""
        raise NotImplementedError("TODO")
