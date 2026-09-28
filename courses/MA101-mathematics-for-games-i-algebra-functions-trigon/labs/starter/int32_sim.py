"""Imitate a signed 32-bit integer (C# int, C++ int32_t) in Python.

Python integers never overflow, so wrap every intermediate result with wrap32.
Example: wrap32(2_147_483_647 + 1) == -2_147_483_648.
"""
INT32_MAX = 2_147_483_647


def wrap32(n):
    """Wrap any integer into the signed 32-bit range, as C#/C++ int arithmetic does."""
    return ((int(n) + 2**31) % 2**32) - 2**31


def sq_dist_int32(a, b):
    """dx*dx + dy*dy + dz*dz computed entirely in 32-bit arithmetic.
    a and b are (x, y, z) tuples of ints. Each multiply and add wraps."""
    dx = wrap32(b[0] - a[0])
    dy = wrap32(b[1] - a[1])
    dz = wrap32(b[2] - a[2])
    return wrap32(wrap32(wrap32(dx * dx) + wrap32(dy * dy)) + wrap32(dz * dz))
