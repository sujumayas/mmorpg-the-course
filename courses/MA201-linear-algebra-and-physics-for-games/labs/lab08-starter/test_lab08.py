"""MA201 Lab 08 tests. Run `python test_lab08.py` (or `pytest test_lab08.py`).
On the untouched starter every test fails."""
import math

from forces import (Body, damp, drag_coefficient, per_step_factor, per_step_gravity,
                    quake_friction, terminal_velocity, tick_entity, ticks_to_fraction,
                    fall_table)


def simulate(g, d, order, ticks):
    y = v = 0.0
    for _ in range(ticks):
        y, v = tick_entity(y, v, g, d, order)
    return y, v


def test_player_first_second():
    y, v = simulate(0.08, 0.98, "PAD", 20)
    assert abs(v * 20 + 26.06) < 0.01 and abs(y + 13.25) < 0.01


def test_orders_matter_on_first_tick():
    y, v = tick_entity(0.0, 0.0, 0.08, 0.98, "PAD")
    assert y == 0.0 and abs(v + 0.0784) < 1e-12
    y, v = tick_entity(0.0, 0.0, 0.04, 0.98, "APD")
    assert abs(y + 0.04) < 1e-12 and abs(v + 0.0392) < 1e-12


def test_wiki_terminal_velocities():
    # Minecraft Wiki, Entity: 78.4, 39.2, 29.4, 59.4 blocks per second.
    assert abs(terminal_velocity(0.08, 0.98, "PAD") * 20 + 78.4) < 1e-9
    assert abs(terminal_velocity(0.04, 0.98, "APD") * 20 + 39.2) < 1e-9
    assert abs(terminal_velocity(0.03, 0.98, "APD") * 20 + 29.4) < 1e-9
    assert abs(terminal_velocity(0.03, 0.99, "ADP") * 20 + 59.4) < 1e-9
    assert abs(terminal_velocity(0.03, 0.99, "PDA") + 3.0) < 1e-9


def test_simulation_reaches_formula():
    for g, d, order in [(0.08, 0.98, "PAD"), (0.03, 0.99, "ADP"), (0.03, 0.99, "PDA")]:
        _, v = simulate(g, d, order, 5000)
        assert v < -1.0
        assert abs(v - terminal_velocity(g, d, order)) < 1e-9


def test_ninety_percent():
    assert ticks_to_fraction(0.98, 0.9) == 114


def test_coefficient_and_rate_conversion():
    assert abs(drag_coefficient(0.98, 20) - 0.40405) < 1e-4
    assert abs(per_step_factor(0.98, 20, 60) - 0.99329) < 1e-5
    assert abs(per_step_gravity(0.08, 20, 60) - 0.08 / 9) < 1e-12


def test_60hz_port_keeps_the_feel():
    slow = fall_table(0.08, 0.98, 20)
    fast = fall_table(per_step_gravity(0.08, 20, 60), per_step_factor(0.98, 20, 60), 60)
    for (t1, s1, _), (t2, s2, _) in zip(slow, fast):
        assert t1 == t2 and abs(s2 - s1) / s1 < 0.02


def test_damping_formulas():
    h = 1 / 60
    assert abs(damp(1.0, 100, h, "exact") - 0.18888) < 1e-5
    assert abs(damp(1.0, 100, h, "pade") - 0.375) < 1e-9
    assert damp(1.0, 100, h, "linear") < 0          # reverses velocity
    assert all(0 < damp(1.0, c, h, "pade") < 1 for c in (1, 50, 500, 5000))


def test_quake_stop():
    speed, t, dist, dt = 80.0, 0.0, 0.0, 1e-4
    for _ in range(100_000):                         # 10 s at most
        if speed <= 0:
            break
        speed = quake_friction(speed, dt)
        dist += speed * dt
        t += dt
    assert abs(t - 0.2) < 1e-3 and abs(dist - 8.0) < 0.05


def test_body_accumulator():
    crate = Body(2.0)
    crate.add_force(10.0, 0.0)
    crate.step(1 / 60)
    assert abs(crate.vel[0] - 0.083333) < 1e-5 and abs(crate.vel[1] + 0.1635) < 1e-5
    assert abs(crate.pos[0] - 0.083333 / 60) < 1e-6
    crate.step(1 / 60)                               # force was cleared
    assert abs(crate.vel[0] - 0.083333) < 1e-5
    wall = Body(math.inf)
    wall.add_force(1000.0, 0.0)
    wall.step(1 / 60)
    assert wall.vel == [0.0, 0.0] and wall.pos == [0.0, 0.0]


def test_heavier_body_same_force_moves_less():
    light, heavy = Body(2.0), Body(10.0)
    for b in (light, heavy):
        b.add_force(10.0, 0.0)
        b.step(1.0, gravity=(0.0, 0.0))
    assert abs(light.vel[0] / heavy.vel[0] - 5.0) < 1e-9


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    passed = 0
    for name, fn in tests:
        try:
            fn()
            passed += 1
            print(f"PASS {name}")
        except Exception as e:  # noqa: BLE001
            print(f"FAIL {name}: {type(e).__name__} {e}")
    print(f"{passed}/{len(tests)} tests passed")
