"""MA201 Lab 10 starter: an impulse resolver for 2D circles and walls.

Run:   python impulses.py        prints the lecture's cases and a drop test
Check: python check_lab10.py     exits 0 only when your work is complete

You write the five functions marked TODO. Detection (circle_contact,
floor_contact) and the stepping loop (step, drop_test) are provided.
Units are metres, kilograms and seconds. Gravity points along -y.
"""
import math

G = 9.81
DT = 1.0 / 240.0           # physics step, seconds (small so drops are accurate)


class Body:
    """A circle. inv_mass = 0 makes it immovable (a wall or the floor)."""

    def __init__(self, x, y, vx, vy, radius=0.1, mass=1.0, bounce=0.0):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.radius = radius
        self.inv_mass = 0.0 if mass is None else 1.0 / mass
        self.bounce = bounce

    def momentum(self):
        m = 0.0 if self.inv_mass == 0 else 1.0 / self.inv_mass
        return (m * self.vx, m * self.vy)

    def energy(self):
        m = 0.0 if self.inv_mass == 0 else 1.0 / self.inv_mass
        return 0.5 * m * (self.vx ** 2 + self.vy ** 2)


# ---------------------------------------------------------------- TODO: yours

def combine(e_a, e_b, rule):
    """Restitution for a pair. rule is one of:
    "max" (Box2D), "average" (Unity default), "min", "multiply" (Unity modes),
    "add" (Godot built-in: sum clamped to [0, 1])."""
    raise NotImplementedError("combine")  # TODO


def resolve_velocity(a, b, nx, ny, e, threshold=0.0):
    """Apply the normal impulse to a and b in place and return j.

    (nx, ny) is the unit normal from a to b.
    v_n = (v_b - v_a) . n. If v_n >= 0 return 0 and change nothing.
    If the approach speed -v_n is below threshold, use e = 0.
    j = -(1 + e) v_n / (inv_a + inv_b); a loses j*inv_a*n, b gains j*inv_b*n.
    If both inverse masses are 0, return 0.
    """
    raise NotImplementedError("resolve_velocity")  # TODO


def apply_friction(a, b, nx, ny, j, mu):
    """Apply the Coulomb friction impulse in place and return it (signed).

    Tangential relative velocity: v_rel - (v_rel . n) n. If its length is
    below 1e-12, return 0. t is its unit direction.
    j_t = -(v_rel . t) / (inv_a + inv_b), clamped to [-mu*j, +mu*j].
    a loses j_t*inv_a*t, b gains j_t*inv_b*t.
    """
    raise NotImplementedError("apply_friction")  # TODO


def correct_position(a, b, nx, ny, depth, percent=0.2, slop=0.005):
    """Move a and b apart along n in place, without touching velocities.

    Total correction = percent * max(depth - slop, 0), split by inverse mass:
    a moves back by corr * inv_a / (inv_a + inv_b), b forward by the rest.
    Return the total correction.
    """
    raise NotImplementedError("correct_position")  # TODO


def reduced_mass_loss(m_a, m_b, e, v_n):
    """Kinetic energy lost: 0.5 * mu * (1 - e^2) * v_n^2, mu = 1/(1/m_a + 1/m_b).
    A mass of None is immovable (its inverse mass is 0)."""
    raise NotImplementedError("reduced_mass_loss")  # TODO


# ---------------------------------------------------------------- provided

def circle_contact(a, b):
    """Return (nx, ny, depth) if circles a and b overlap, else None."""
    dx, dy = b.x - a.x, b.y - a.y
    dist = math.hypot(dx, dy)
    depth = a.radius + b.radius - dist
    if depth <= 0:
        return None
    if dist < 1e-12:
        return (1.0, 0.0, depth)
    return (dx / dist, dy / dist, depth)


def floor_contact(ball, floor_y=0.0):
    """Contact between the floor (as body a, below) and a ball (body b)."""
    depth = floor_y + ball.radius - ball.y
    return (0.0, 1.0, depth) if depth > 0 else None


def drop_test(h, e_ball, e_floor, rule, threshold, seconds=6.0, mu=0.0):
    """Drop a 0.1 m ball from height h (bottom of ball) onto a static floor.

    Returns the list of bounce heights (bottom of ball at each apex). A
    'bounce' is an impact after which the ball leaves the floor faster
    than 0.05 m/s.
    """
    floor = Body(0, -1e9, 0, 0, radius=0, mass=None, bounce=e_floor)
    ball = Body(0, h + 0.1, 0, 0, radius=0.1, mass=1.0, bounce=e_ball)
    e = combine(e_ball, e_floor, rule)
    heights, rising, apex = [], False, None
    for _ in range(int(seconds / DT)):
        ball.vy -= G * DT                     # semi-implicit Euler (week 7)
        ball.x += ball.vx * DT
        ball.y += ball.vy * DT
        c = floor_contact(ball)
        if c:
            nx, ny, depth = c
            j = resolve_velocity(floor, ball, nx, ny, e, threshold)
            apply_friction(floor, ball, nx, ny, j, mu)
            correct_position(floor, ball, nx, ny, depth, percent=1.0, slop=0.0)
            if ball.vy > 0.05:
                rising, apex = True, ball.y - 0.1
        if rising:
            apex = max(apex, ball.y - 0.1)
            if ball.vy <= 0:
                heights.append(apex)
                rising = False
    return heights


if __name__ == "__main__":
    cases = [("pool 0.95", 0.17, 0.17, 0.95), ("rail 0.75", 0.17, None, 0.75),
             ("heavy->light", 10.0, 1.0, 1.0), ("light->heavy", 1.0, 10.0, 1.0)]
    for name, ma, mb, e in cases:
        a = Body(0, 0, 2.0, 0, mass=ma)
        b = Body(0.2, 0, 0.0, 0, mass=mb)
        try:
            j = resolve_velocity(a, b, 1.0, 0.0, e)
            print(f"{name:13s} j={j:.3f} v_a'={a.vx:+.3f} v_b'={b.vx:+.3f}")
        except NotImplementedError as exc:
            print(f"{name:13s} -- ({exc} not written yet)")
    try:
        for thr in (0.0, 1.0, 2.0):
            hs = drop_test(1.0, 0.8, 0.0, "max", thr)
            print(f"drop 1 m, e 0.8, threshold {thr}: {len(hs)} bounces, "
                  f"last {hs[-1] if hs else 0:.3f} m")
    except NotImplementedError as exc:
        print(f"drop test -- ({exc} not written yet)")
