"""Tests for Lab 06, from the week 6 lecture: tank 500 TPS, head start 1,500.
Run with `python3 test_threat.py` or `pytest test_threat.py`."""
from threat_sim import DT, Combatant, pull_time_closed_form, simulate

TANK = Combatant("tank", dps=500)
L = 1_500


def close(a, b, tol):
    return a is not None and abs(a - b) <= tol


def test_closed_form():
    assert close(pull_time_closed_form(500, 700, L, 1.1), 11.0, 1e-9)
    assert close(pull_time_closed_form(500, 700, L, 1.3), 39.0, 1e-9)
    assert pull_time_closed_form(500, 550, L, 1.1) is None


def first_pull(dps):
    pulls = simulate(TANK, [dps], L)
    return pulls[0][0] if pulls else None


def test_melee_700():
    assert close(first_pull(Combatant("rogue", dps=700)), 11.0, DT + 1e-6)


def test_ranged_700():
    assert close(first_pull(Combatant("mage", dps=700, ranged=True)), 39.0, DT + 1e-6)


def test_melee_550_never():
    assert first_pull(Combatant("rogue", dps=550)) is None


def test_taunt_second_pull():
    # Taunt at the first pull (11.0 s): second pull at 11 + 0.1 x 7,700 / 150 = 16.13 s.
    pulls = simulate(TANK, [Combatant("rogue", dps=700)], L, taunt_on_pull=True)
    assert len(pulls) >= 2
    assert close(pulls[1][0], 16.13, 2 * DT + 1e-6)


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS {name}")
            except NotImplementedError as e:
                failed += 1
                print(f"TODO {name}: {e}")
            except AssertionError:
                failed += 1
                print(f"FAIL {name}")
    print("all tests pass" if not failed else f"{failed} test(s) not passing yet")
