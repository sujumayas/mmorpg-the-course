"""Lab 13 example tests. Run with `pytest test_sim.py` or `python3 test_sim.py`.
The first passes as shipped. The second fails until plain hits work."""
from sim import load_classes, simulate


def test_every_class_runs():
    for name in load_classes():
        mean, sd, se = simulate(name, 60.0, 5, seed=1)
        assert mean >= 0 and sd >= 0 and se >= 0


def test_zero_crit_is_exact():
    # With 0% crit, 40 actions in 60 s give exactly 40 x D / 60.
    spec = dict(load_classes()["Duelist"], crit_chance=0.0)
    mean, sd, se = simulate("Duelist", 60.0, 20, seed=1, spec=spec)
    assert abs(mean - 40 * 100 / 60) < 1e-9 and sd == 0


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS {name}")
            except AssertionError:
                print(f"FAIL {name}")
