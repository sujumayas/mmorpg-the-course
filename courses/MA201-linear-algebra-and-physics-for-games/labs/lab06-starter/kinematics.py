"""MA201 Lab 06: moving frames.

Plain Python 3.10+, standard library only. 2D vectors are (x, y) tuples with
y UP (the lecture's convention; Godot 2D flips the sign of y). 3D vectors are
(x, y, z) tuples. Units: pixels and seconds unless stated.

Fill in every function marked TODO. Run `python test_lab06.py` to check.
"""
import csv

G = 980.0        # gravity, px/s^2, pointing down
JUMP = 400.0     # jump speed relative to the platform, px/s


# ---------------------------------------------------------------- part A: derivatives from samples

def forward_diff(xs, h):
    """TODO: list of (xs[i+1] - xs[i]) / h, length len(xs) - 1."""
    raise NotImplementedError


def central_diff(xs, h):
    """TODO: list of (xs[i+1] - xs[i-1]) / (2h) for i = 1 .. len(xs) - 2."""
    raise NotImplementedError


def second_diff(xs, h):
    """TODO: list of (xs[i+1] - 2 xs[i] + xs[i-1]) / h^2 for i = 1 .. len(xs) - 2."""
    raise NotImplementedError


# ---------------------------------------------------------------- part B: leaving a platform

def launch_velocity(mode, v_p, jump=JUMP, cap_x=None, cap_up=None):
    """TODO: world velocity at take-off for a player standing still on a platform
    moving at v_p = (vx, vy), who jumps with (0, jump) relative to it.
    mode is 'add', 'upward' or 'nothing' (Godot's three platform_on_leave modes).
    If cap_x is given, clamp the inherited x part to [-cap_x, cap_x]. If cap_up is
    given, clamp the inherited upward part to at most cap_up (Celeste's lift boost)."""
    raise NotImplementedError


def relative_landing(v_launch, v_p, a_p=(0.0, 0.0), g=G):
    """TODO: the player leaves a platform with world velocity v_launch. The platform
    had velocity v_p at take-off and keeps a constant acceleration a_p.
    Return (t_land, dx): the time until the player is back at the platform's
    height, and the horizontal offset from the take-off spot, both measured in
    the platform's frame. Return (None, None) if the player never comes back
    down to the platform (relative launch speed <= 0 or g + a_p.y <= 0)."""
    raise NotImplementedError


# ---------------------------------------------------------------- part C: rotating platforms

def cross(a, b):
    """TODO: 3D cross product a x b."""
    raise NotImplementedError


def point_velocity(omega, r):
    """TODO: velocity of a point at offset r from the center of a platform
    spinning with angular velocity vector omega (rad/s): omega x r."""
    raise NotImplementedError


def centripetal(omega_mag, radius):
    """TODO: size of the centripetal acceleration, omega^2 * r."""
    raise NotImplementedError


# ---------------------------------------------------------------- part D: the log

def load_log(path):
    """Given: platform_log.csv -> dict of lists t, platform_x, player_x, player_y."""
    cols = {"t": [], "platform_x": [], "player_x": [], "player_y": []}
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            for k in cols:
                cols[k].append(float(row[k]))
    return cols


def find_jumps(log):
    """TODO: indices i where player_y[i] == 0 and player_y[i + 1] > 0."""
    raise NotImplementedError


if __name__ == "__main__":
    for vp in [(150.0, 0.0), (0.0, 100.0), (0.0, -100.0)]:
        for mode in ("add", "upward", "nothing"):
            v = launch_velocity(mode, vp)
            print(vp, mode, v, relative_landing(v, vp))
