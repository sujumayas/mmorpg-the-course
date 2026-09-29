"""MA201 Lab 07 tests. Run `python test_lab07.py` (or `pytest test_lab07.py`).
On the untouched starter every test fails, because the stubs never move."""
import math

from integrators import (explicit_euler, semi_implicit, velocity_verlet, gravity,
                         make_spring, run, orbit_energy, spring_amplitude,
                         max_energy_error)

START = (1.0, 0.0, 0.0, 1.0)


def close(a, b, tol=1e-5):
    return all(abs(p - q) < tol for p, q in zip(a, b))


def test_explicit_first_step():
    assert close(explicit_euler(START, 0.1, gravity), (1.0, 0.1, -0.1, 1.0))


def test_semi_implicit_first_step():
    assert close(semi_implicit(START, 0.1, gravity), (0.99, 0.1, -0.1, 1.0))


def test_verlet_first_step():
    assert close(velocity_verlet(START, 0.1, gravity), (0.995, 0.1, -0.09975, 0.995))


def test_explicit_orbit_spirals_out():
    s = run(explicit_euler, START, 0.1, 1000, gravity)[-1]
    assert abs(math.hypot(s[0], s[1]) - 3.3949) < 1e-3
    assert orbit_energy(s) > -0.2


def test_semi_implicit_orbit_stays_bounded():
    states = run(semi_implicit, START, 0.1, 1000, gravity)
    radii = [math.hypot(s[0], s[1]) for s in states]
    assert 0.95 < min(radii) and max(radii) < 1.06
    assert abs(math.hypot(states[99][0], states[99][1]) - 1.0379) < 1e-3


def test_verlet_energy_error_tiny():
    quarter = run(velocity_verlet, START, 2 * math.pi / 60, 15, gravity)[-1]
    assert close(quarter[:2], (0.0, 1.0), 0.01)          # it really moved
    assert max_energy_error(velocity_verlet, 1.0, 60) < 2e-5


def test_explicit_spring_growth_factor():
    # Squared amplitude grows by exactly (1 + w^2 dt^2) per step.
    w, dt = 10.0, 1 / 60
    s = run(explicit_euler, (1.0, 0.0, 0.0, 0.0), dt, 60, make_spring(w))[-1]
    assert abs(spring_amplitude(s, w) - (1 + (w * dt) ** 2) ** 30) < 1e-9


def test_semi_implicit_stability_limit():
    dt = 1 / 60
    below = run(semi_implicit, (1.0, 0.0, 0.0, 0.0), dt, 600, make_spring(119.0))
    above = run(semi_implicit, (1.0, 0.0, 0.0, 0.0), dt, 600, make_spring(121.0))
    assert max(abs(s[0]) for s in below) < 8
    assert max(abs(s[0]) for s in above) > 1e6


def test_convergence_order_on_ellipse():
    # Halving the step roughly halves semi-implicit error and quarters Verlet error.
    semi = [max_energy_error(semi_implicit, 1.2, n) for n in (120, 240)]
    verl = [max_energy_error(velocity_verlet, 1.2, n) for n in (120, 240)]
    assert 1.7 < semi[0] / semi[1] < 2.5
    assert 3.4 < verl[0] / verl[1] < 4.6


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    passed = 0
    for name, fn in tests:
        try:
            fn()
            passed += 1
            print(f"PASS {name}")
        except Exception as e:  # noqa: BLE001  (show any failure, including stubs)
            print(f"FAIL {name}: {type(e).__name__} {e}")
    print(f"{passed}/{len(tests)} tests passed")
