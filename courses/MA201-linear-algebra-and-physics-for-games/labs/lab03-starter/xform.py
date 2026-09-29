"""MA201 Lab 03 starter: local and world space.

A 2D transform is a basis B (2x2, tuple of rows, columns = where the local axes land)
plus an origin t. Angles are degrees, counter-clockwise, y up. Local +x is "forward"
and local +y is "left" for every node in this lab.
Fill in every function that raises NotImplementedError, then run:  python test_lab03.py
Standard library only.
"""
import csv
import math

EPS = 1e-9


class Xform:
    def __init__(self, B=((1.0, 0.0), (0.0, 1.0)), t=(0.0, 0.0)):
        self.B = B
        self.t = t

    @staticmethod
    def trs(x, y, deg=0.0, sx=1.0, sy=1.0):
        """Given. B = R(deg) S(sx, sy): scale along local axes, then rotate."""
        c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        return Xform(((c * sx, -s * sy), (s * sx, c * sy)), (float(x), float(y)))

    def columns(self):
        """Given. The two basis columns (where local x and local y land)."""
        (a, b), (c, d) = self.B
        return (a, c), (b, d)

    def det(self):
        (a, b), (c, d) = self.B
        return a * d - b * c

    # ----- Part A -----

    def point(self, p):
        """B p + t."""
        raise NotImplementedError("TODO")

    def vector(self, v):
        """B v (directions ignore the origin)."""
        raise NotImplementedError("TODO")

    def __mul__(self, child):
        """self * child: the child's transform expressed in self's space.
        Basis Bp Bc, origin Bp tc + tp (lecture section 2)."""
        raise NotImplementedError("TODO")

    def inverse(self):
        """The full inverse (B^-1, -B^-1 t). Raise ValueError if |det| < EPS."""
        raise NotImplementedError("TODO")

    def transpose_inverse(self):
        """The rotation-only shortcut (B^T, -B^T t). Given. Correct only when B
        is orthonormal; compare it with inverse() in the lab."""
        (a, b), (c, d) = self.B
        Bt = ((a, c), (b, d))
        tx = -(Bt[0][0] * self.t[0] + Bt[0][1] * self.t[1])
        ty = -(Bt[1][0] * self.t[0] + Bt[1][1] * self.t[1])
        return Xform(Bt, (tx, ty))

    # ----- Part B -----

    def normal(self, n):
        """Transform a surface normal with the inverse transpose of B, then
        normalize (lecture section 4)."""
        raise NotImplementedError("TODO")

    def corner_angle(self):
        """Angle in degrees between the two basis columns. 90 means no shear."""
        raise NotImplementedError("TODO")


class Scene:
    def __init__(self, path="scene.csv"):
        """Given. self.local[name] is the node's local Xform; self.parent[name] is
        the parent's name or None."""
        self.local, self.parent = {}, {}
        with open(path, newline="") as f:
            for r in csv.DictReader(f):
                name = r["name"]
                self.parent[name] = r["parent"] or None
                self.local[name] = Xform.trs(float(r["x"]), float(r["y"]), float(r["deg"]),
                                             float(r["sx"]), float(r["sy"]))

    # ----- Part C -----

    def world(self, name):
        """The node's world transform: the product of local transforms from the root down."""
        raise NotImplementedError("TODO")

    def to_local(self, name, p_world):
        """A world point expressed in the node's local space (full inverse)."""
        raise NotImplementedError("TODO")

    def describe(self, name, p_world):
        """("ahead" or "behind", "left" or "right") for a world point, read off its
        local coordinates. A local x or y of exactly 0 counts as "ahead" or "left"."""
        raise NotImplementedError("TODO")

    def audit(self, tol_deg=0.5):
        """Sorted list of node names whose world corner angle differs from 90 degrees
        by more than tol_deg."""
        raise NotImplementedError("TODO")
