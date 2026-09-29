"""MA201 Lab 02 starter: the isometric picker.

A 2x2 matrix is a tuple of rows ((a, b), (c, d)). Its columns are where the x and y
axes land (lecture section 2). Vectors are (x, y) tuples. Screen y points down.
Fill in every function that raises NotImplementedError, then run:  python test_lab02.py
Standard library only.
"""
import math

EPS = 1e-9


# ---------- Part A: 2x2 matrix operations ----------

def mat_vec(M, v):
    """M times the column vector v."""
    raise NotImplementedError("TODO")


def mat_mul(A, B):
    """The product A B (apply B first, then A)."""
    raise NotImplementedError("TODO")


def det(M):
    raise NotImplementedError("TODO")


def inverse(M):
    """The inverse of M, or None if |det(M)| < EPS."""
    raise NotImplementedError("TODO")


def columns(M):
    """The two columns of M as vectors. Given."""
    (a, b), (c, d) = M
    return (a, c), (b, d)


# ---------- Part B: tiles and screens ----------

def tile_matrix(w, h):
    """Tile-to-screen matrix for diamond tiles w pixels wide and h tall:
    one step in i goes (w/2, h/2), one step in j goes (-w/2, h/2)."""
    raise NotImplementedError("TODO")


def tile_to_screen(M, origin, i, j):
    """Screen position of tile coordinate (i, j): M (i, j) + origin."""
    raise NotImplementedError("TODO")


def screen_to_tile(M, origin, x, y):
    """The integer tile (floor(i), floor(j)) under the screen point (x, y),
    or None if M has no inverse. Use floor, not int()."""
    raise NotImplementedError("TODO")


def rect_pick(w, h, x, y):
    """The rectangle method from lecture section 3, for the default tile matrix and
    origin (0, 0): the tile drawn in the middle of the w x h rectangle containing
    (x, y). Given. Wrong for half of all clicks."""
    k = math.floor((x + w / 2) / w)
    m = math.floor(y / h)
    return (k + m, m - k)


def error_rate(w, h, x0, x1, y0, y1):
    """Fraction of pixel centres (x + 0.5, y + 0.5), for integer x in [x0, x1) and
    y in [y0, y1), where rect_pick disagrees with screen_to_tile(tile_matrix(w, h),
    (0, 0), ...)."""
    raise NotImplementedError("TODO")


# ---------- Part C: camera zoom and mirroring ----------

def zoom(k):
    """Uniform zoom by k about the screen origin."""
    raise NotImplementedError("TODO")


MIRROR_X = ((-1, 0), (0, 1))
