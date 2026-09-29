"""MA201 Lab 07 starter: three integrators and an energy meter.

Standard library only. State is a tuple (x, y, vx, vy). Each step function
takes the state, the time step dt and an acceleration function accel(x, y)
that returns (ax, ay), and returns the new state.

The three step functions below are stubs: they return the state unchanged, so
this file runs but nothing moves. Replace each TODO with the rule from
lecture section 2. Then run `python test_lab07.py`.

    python integrators.py                 # prints the orbit table
    python integrators.py --v0 1.2        # an elliptical orbit
    python integrators.py --csv out.csv   # every step, for plotting
"""
import argparse
import csv
import math


# ---------------------------------------------------------------- forces
def gravity(x, y):
    """Inverse-square pull toward the origin with GM = 1."""
    r3 = (x * x + y * y) ** 1.5
    return -x / r3, -y / r3


def make_spring(w):
    """Spring toward the origin with a = -w^2 * position (w in rad/s)."""
    def accel(x, y):
        return -w * w * x, -w * w * y
    return accel


# ------------------------------------------------------------ integrators
def explicit_euler(state, dt, accel):
    x, y, vx, vy = state
    # TODO: move with the OLD velocity, then update the velocity with a(old x).
    return (x, y, vx, vy)


def semi_implicit(state, dt, accel):
    x, y, vx, vy = state
    # TODO: update the velocity with a(x) first, then move with the NEW velocity.
    return (x, y, vx, vy)


def velocity_verlet(state, dt, accel):
    x, y, vx, vy = state
    # TODO: x_new = x + v*dt + 0.5*a(x)*dt^2
    #       v_new = v + 0.5*(a(x) + a(x_new))*dt
    return (x, y, vx, vy)


METHODS = {
    "explicit": explicit_euler,
    "semi": semi_implicit,
    "verlet": velocity_verlet,
}


# ----------------------------------------------------------- measurement
def orbit_energy(state):
    """Kinetic plus gravitational potential energy per unit mass (GM = 1)."""
    x, y, vx, vy = state
    return 0.5 * (vx * vx + vy * vy) - 1.0 / math.hypot(x, y)


def spring_amplitude(state, w):
    """sqrt(x^2 + (v/w)^2) along x; exactly constant for the true motion."""
    x, _, vx, _ = state
    return math.sqrt(x * x + (vx / w) ** 2)


def run(step, state, dt, steps, accel):
    """Return the list of states after each step (length `steps`)."""
    out = []
    for _ in range(steps):
        state = step(state, dt, accel)
        out.append(state)
    return out


def max_energy_error(step, v0, steps_per_orbit, orbits=10):
    """Largest |E - E0| over the run, for the orbit starting at (1, 0), (0, v0)."""
    start = (1.0, 0.0, 0.0, v0)
    e0 = orbit_energy(start)
    dt = 2 * math.pi / steps_per_orbit
    states = run(step, start, dt, steps_per_orbit * orbits, gravity)
    return max(abs(orbit_energy(s) - e0) for s in states)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--v0", type=float, default=1.0)
    ap.add_argument("--dt", type=float, default=0.1)
    ap.add_argument("--steps", type=int, default=1000)
    ap.add_argument("--csv", default=None)
    args = ap.parse_args()

    start = (1.0, 0.0, 0.0, args.v0)
    rows = []
    for name, step in METHODS.items():
        states = run(step, start, args.dt, args.steps, gravity)
        for n in (1, 100, args.steps):
            s = states[n - 1]
            print(f"{name:9s} n={n:5d}  r={math.hypot(s[0], s[1]):.4f}  E={orbit_energy(s):.5f}")
        for n, s in enumerate(states, 1):
            rows.append((name, n, n * args.dt, *s, orbit_energy(s)))
    if args.csv:
        with open(args.csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["method", "step", "t", "x", "y", "vx", "vy", "E"])
            w.writerows(rows)
        print(f"wrote {len(rows)} rows to {args.csv}")


if __name__ == "__main__":
    main()
