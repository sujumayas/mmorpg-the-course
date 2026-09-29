"""MA201 Lab 08 starter: a force accumulator and three drag models.

Standard library only. Every function marked TODO is a stub that returns a
harmless placeholder, so the file runs but the numbers are wrong. Fill them in
from lecture sections 1 to 4, then run `python test_lab08.py`.

    python forces.py              # prints the Minecraft fall table at 20 Hz and 60 Hz
"""
import math

# Per-tick operation orders, named by their first letters:
#   "PAD" position, acceleration, drag     (Minecraft players and mobs)
#   "APD" acceleration, position, drag     (items, falling blocks, XP orbs)
#   "ADP" acceleration, drag, position     (thrown projectiles, Java 1.21.2+)
#   "PDA" position, drag, acceleration     (thrown projectiles before 1.21.2)
ORDERS = ("PAD", "APD", "ADP", "PDA")


# ------------------------------------------------------- part A: per-tick rules
def tick_entity(y, v, g, d, order):
    """Run one tick. Gravity g > 0 pulls toward negative y. Returns (y, v)."""
    for op in order:
        if op == "P":
            pass  # TODO: position update
        elif op == "A":
            pass  # TODO: acceleration (gravity)
        elif op == "D":
            pass  # TODO: drag
    return y, v


def terminal_velocity(g, d, order):
    """Fixed point of the per-tick rule, in units per tick (negative = down)."""
    # TODO: drag after acceleration -> -g*d/(1-d); drag before acceleration -> -g/(1-d)
    return 0.0


def ticks_to_fraction(d, fraction):
    """Smallest whole number of ticks n with 1 - d**n >= fraction, from rest."""
    # TODO
    return 0


# ------------------------------------------------ part B: coefficients and rates
def drag_coefficient(d, rate):
    """Per-tick factor d at `rate` ticks per second -> coefficient c in 1/s."""
    # TODO: c = -ln(d) / dt
    return 0.0


def per_step_factor(d, from_rate, to_rate):
    """Same continuous drag, re-expressed as a factor per step at `to_rate`."""
    # TODO
    return d


def per_step_gravity(g, from_rate, to_rate):
    """Gravity given per tick^2 at from_rate, re-expressed per step^2 at to_rate."""
    # TODO
    return g


def damp(v, c, h, method):
    """Multiply velocity by one step of damping. method: exact, pade or linear."""
    # TODO
    return v


# ---------------------------------------------------------- part C: Quake friction
def quake_friction(speed, dt, friction=4.0, stopspeed=100.0):
    """One frame of Quake's SV_UserFriction on a horizontal speed (>= 0)."""
    # TODO: newspeed = speed - dt * friction * max(speed, stopspeed), not below 0
    return speed


# --------------------------------------------------- part D: the force accumulator
class Body:
    def __init__(self, mass, damping=0.0):
        self.inv_mass = 0.0 if mass == math.inf else 1.0 / mass
        self.damping = damping          # coefficient c in 1/s, Pade form
        self.pos = [0.0, 0.0]
        self.vel = [0.0, 0.0]
        self.force = [0.0, 0.0]

    def add_force(self, fx, fy):
        # TODO: accumulate
        pass

    def step(self, h, gravity=(0.0, -9.81)):
        """Semi-implicit Euler: v += (F/m + g) h, damp, x += v h, clear forces.
        Bodies with inv_mass == 0 do not move and get no gravity."""
        # TODO
        self.force = [0.0, 0.0]


# ------------------------------------------------------------------ runner
def fall_table(g, d, rate, order="PAD", seconds=(1, 2, 5, 10)):
    y = v = 0.0
    rows = []
    for n in range(1, int(max(seconds) * rate) + 1):
        y, v = tick_entity(y, v, g, d, order)
        if n / rate in seconds:
            rows.append((n / rate, -v * rate, -y))
    return rows


if __name__ == "__main__":
    for rate in (20, 60):
        g = per_step_gravity(0.08, 20, rate)
        d = per_step_factor(0.98, 20, rate)
        term = -terminal_velocity(g, d, "PAD") * rate
        print(f"{rate} Hz: g={g:.6f} d={d:.6f} terminal={term:.2f} blocks/s")
        for t, speed, fallen in fall_table(g, d, rate):
            print(f"   t={t:4.1f}s  speed {speed:6.2f}  fallen {fallen:7.2f}")
