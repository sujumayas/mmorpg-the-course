"""MA201 Lab 04: a software camera.

Plain Python 3.10+, standard library only. Column vectors: M @ v, and the
matrix nearest the vector acts first. Matrices are lists of 4 rows.
View space looks down -z (OpenGL / Godot / glTF convention).

Fill in every function marked TODO. Run `python test_lab04.py` to check.
"""
import math

# ---------------------------------------------------------------- given helpers

def identity():
    return [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]


def mat_mul(A, B):
    """Return A @ B for two 4x4 matrices."""
    return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def apply(M, v):
    """Return M @ v for a 4x4 matrix and a 4-vector."""
    return [sum(M[i][k] * v[k] for k in range(4)) for i in range(4)]


def rot_y(deg):
    """Rotation about +y by deg degrees (right-handed)."""
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]]


# ---------------------------------------------------------------- part A: affine

def translate(tx, ty, tz):
    """TODO: 4x4 translation matrix."""
    raise NotImplementedError


def scale(sx, sy, sz):
    """TODO: 4x4 scale matrix."""
    raise NotImplementedError


def point(x, y, z):
    """TODO: homogeneous point (w = 1) as a list of 4 floats."""
    raise NotImplementedError


def direction(x, y, z):
    """TODO: homogeneous direction (w = 0) as a list of 4 floats."""
    raise NotImplementedError


def rigid_inverse(M):
    """TODO: inverse of a rotation + translation matrix, using
    [R t; 0 1]^-1 = [R^T  -R^T t; 0 1]. Do not use a general inverse."""
    raise NotImplementedError


# ---------------------------------------------------------------- part B: projection

def perspective(vfov_deg, aspect, near, far):
    """TODO: OpenGL-style perspective matrix (lecture section 4)."""
    raise NotImplementedError


def project(P, V, p_world, width, height):
    """TODO: world-space point (x, y, z) -> (pixel_x, pixel_y, z_ndc), or None
    if the point is outside the frustum (test -w <= x, y, z <= w in clip space,
    and w > 0). Pixel y grows downward."""
    raise NotImplementedError


# ---------------------------------------------------------------- part C: FOV conventions

def hfov_from_vfov(vfov_deg, aspect):
    """TODO: horizontal FOV in degrees from vertical FOV."""
    raise NotImplementedError


def vfov_from_hfov(hfov_deg, aspect):
    """TODO: vertical FOV in degrees from horizontal FOV."""
    raise NotImplementedError


def vfov_from_setting(value_deg, convention, aspect):
    """TODO: convert a settings value to vertical FOV in degrees.
    convention is 'vertical', 'horizontal' or 'horizontal43'."""
    raise NotImplementedError


# ---------------------------------------------------------------- part D: depth

def z_ndc(depth, near, far):
    """TODO: NDC depth in [-1, 1] of a point `depth` metres in front of the camera."""
    raise NotImplementedError


def depth_step(depth, near, far, bits=24):
    """TODO: the smallest change in depth (metres) the depth buffer can resolve
    at this depth. The buffer stores (z_ndc + 1) / 2 in `bits` bits, so one
    step in z_ndc is 2 / 2**bits. Divide it by the slope dz_ndc/dd."""
    raise NotImplementedError


if __name__ == "__main__":
    P = perspective(75, 16 / 9, 0.05, 4000)
    V = identity()
    print("lecture point:", project(P, V, (2, 1, -10), 1920, 1080))
    for a in (4 / 3, 16 / 10, 16 / 9, 21 / 9):
        print(f"aspect {a:.3f}: Godot 75 -> {hfov_from_vfov(75, a):.2f} deg across")
