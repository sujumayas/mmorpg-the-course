"""MA101 Lab 13 starter: guard vision.

Uses your Vec2 from lab12_starter.py (keep it in the same folder). If your Lab 12
Vec2 is not finished, the small reference class below is used instead.
Fill in every TODO. No acos or atan2 inside in_cone.
"""
import csv
import math

try:
    from lab12_starter import Vec2
    Vec2(3, 4).normalized()  # raises NotImplementedError if Lab 12 is unfinished
except (ImportError, NotImplementedError):
    class Vec2:  # reference version, same interface as Lab 12
        def __init__(self, x=0.0, y=0.0):
            self.x, self.y = float(x), float(y)

        def __add__(self, o): return Vec2(self.x + o.x, self.y + o.y)
        def __sub__(self, o): return Vec2(self.x - o.x, self.y - o.y)
        def __mul__(self, k): return Vec2(self.x * k, self.y * k)
        __rmul__ = __mul__
        def length(self): return math.hypot(self.x, self.y)

        def normalized(self):
            n = self.length()
            return Vec2(self.x / n, self.y / n) if n >= 1e-9 else Vec2(0, 0)

        def __repr__(self): return f"Vec2({self.x:.3f}, {self.y:.3f})"


def load_guards(path="guards.csv"):
    """Returns a list of dicts: name, pos (Vec2), fwd (unit Vec2), half_angle_deg, range."""
    out = []
    for r in csv.DictReader(open(path)):
        a = math.radians(float(r["facing_deg"]))
        out.append({"name": r["name"], "pos": Vec2(float(r["x"]), float(r["y"])),
                    "fwd": Vec2(math.cos(a), math.sin(a)),
                    "half_angle_deg": float(r["half_angle_deg"]), "range": float(r["range"])})
    return out


def load_path(path="path.csv"):
    """Returns a list of (t, Vec2) samples, 0.1 s apart."""
    return [(float(r["t"]), Vec2(float(r["x"]), float(r["y"]))) for r in csv.DictReader(open(path))]


def dot(a, b):
    raise NotImplementedError("TODO")


def in_cone(guard_pos, guard_fwd, half_angle_deg, sight_range, player_pos):
    """True when the player is within sight_range and f . d_hat >= cos(half angle)."""
    raise NotImplementedError("TODO")


def side(guard_fwd, guard_pos, player_pos):
    """"left", "right" or "ahead/behind", from the perpendicular dot product."""
    raise NotImplementedError("TODO")


def focus(guard_pos, guard_fwd, half_angle_deg, player_pos):
    """clamp((f . d_hat - c) / (1 - c), 0, 1) with c = cos(half angle)."""
    raise NotImplementedError("TODO")


if __name__ == "__main__":
    # Lecture section 2 table: sentry at the origin facing +x, half-angle 30, range 20.
    expected = {(10, 0): True, (3, 1): True, (10, 5): True, (10, 6): False, (5, 5): False,
                (0, 8): False, (-6, 0): False, (18, 9): False, (25, 0): False}
    for (x, y), want in expected.items():
        got = in_cone(Vec2(0, 0), Vec2(1, 0), 30, 20, Vec2(x, y))
        print(("ok  " if got == want else "FAIL") + f" player at ({x}, {y}): seen={got}")
