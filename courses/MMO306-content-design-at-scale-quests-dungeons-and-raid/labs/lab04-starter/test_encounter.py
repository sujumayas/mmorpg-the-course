"""Tests for Lab 04. Values come from the week 4 lecture.
Run with `python test_encounter.py` (or `pytest test_encounter.py` if you have pytest)."""
from dataclasses import replace

from encounter import (GROUP_A, GROUP_B, QUAKEMAW, STITCHGUT, hidden_health, kill_time,
                       max_deaths, passes, required_paper_dps, simulate, tax, uptime)

TOL = 0.05


def close(a, b, tol=TOL):
    return a is not None and abs(a - b) <= tol


def test_tax_and_uptime():
    assert close(tax(STITCHGUT), 0.0, 1e-9)
    assert close(tax(QUAKEMAW), 0.2, 1e-9)
    assert close(uptime(QUAKEMAW, GROUP_A), 0.68, 1e-9)
    assert close(uptime(QUAKEMAW, GROUP_B), 0.80, 1e-9)
    heavy = replace(QUAKEMAW, mechanics=[(10, 10, 9)])   # tax 0.9
    assert uptime(heavy, GROUP_A) == 0
    assert kill_time(heavy, GROUP_A) is None


def test_average_kill_times():
    assert close(kill_time(STITCHGUT, GROUP_A), 287.5)
    assert close(kill_time(STITCHGUT, GROUP_B), 313.6)
    assert close(kill_time(QUAKEMAW, GROUP_A), 306.4)
    assert close(kill_time(QUAKEMAW, GROUP_B), 284.1)
    assert passes(STITCHGUT, GROUP_A) and not passes(STITCHGUT, GROUP_B)
    assert passes(QUAKEMAW, GROUP_B) and not passes(QUAKEMAW, GROUP_A)


def test_hidden_health_and_requirement():
    assert close(hidden_health(QUAKEMAW, GROUP_B), 6_250_000, 1)
    assert close(hidden_health(QUAKEMAW, GROUP_A), 7_352_941, 1)
    assert close(required_paper_dps(QUAKEMAW, GROUP_B), 20_833.3, 0.1)
    assert close(required_paper_dps(QUAKEMAW, GROUP_A), 24_509.8, 0.1)


def test_simulation_matches_lecture():
    assert close(simulate(QUAKEMAW, GROUP_B), 282.3, 1e-6)
    assert close(simulate(QUAKEMAW, GROUP_A, limit_s=600), 305.4, 1e-6)
    assert simulate(QUAKEMAW, GROUP_A) is None                  # enrage at 300 s
    assert close(simulate(STITCHGUT, GROUP_A), 287.5, 1e-6)


def test_one_death_costs_the_kill():
    assert close(simulate(QUAKEMAW, GROUP_B, deaths=[(60, 1)], limit_s=600), 301.1, 1e-6)
    assert simulate(QUAKEMAW, GROUP_B, deaths=[(60, 1)]) is None
    assert max_deaths(QUAKEMAW, GROUP_B, 60) == 0
    assert max_deaths(QUAKEMAW, GROUP_B, 250) >= 1
    assert max_deaths(QUAKEMAW, GROUP_A, 60) == -1


if __name__ == "__main__":
    import sys
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
    print(f"{failed} test(s) not passing")
    sys.exit(1 if failed else 0)
