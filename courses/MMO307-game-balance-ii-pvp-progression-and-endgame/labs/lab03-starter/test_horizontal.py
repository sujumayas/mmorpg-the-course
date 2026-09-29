"""Tests for MMO307 Lab 03. Values come from the week 3 lecture and play_log.csv.
Run with `python test_horizontal.py` (or pytest if you have it)."""
from horizontal import (estimate_mix, gap_ceiling, gate_marginals, gate_share,
                        load_log, n_eff, rotate, tools_worth_chasing, values, zipf)

ROWS = load_log()


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


def lclose(xs, ys, tol=1e-3):
    return len(xs) == len(ys) and all(close(x, y, tol) for x, y in zip(xs, ys))


def test_log_loads():
    assert len(ROWS) == 200


def test_estimate_mix():
    assert lclose(estimate_mix(ROWS, "raider"), [0.40, 0.25, 0.15, 0.10, 0.06, 0.04])
    assert lclose(estimate_mix(ROWS, "pvp"), [0.10, 0.05, 0.05, 0.10, 0.20, 0.50])


def test_zipf_and_values():
    z = zipf(6)
    assert close(sum(z), 1.0, 1e-9)
    assert lclose(values(z, 0.3), [0.1224, 0.0612, 0.0408, 0.0306, 0.0245, 0.0204], 1e-4)


def test_summary_numbers():
    z = zipf(6)
    assert close(n_eff(z), 4.025)
    assert close(gap_ceiling(z, 0.3), 1.1582)
    assert close(n_eff([1 / 6] * 6), 6.0)
    assert close(gap_ceiling([1 / 6] * 6, 0.3), 1.2381)
    assert close(n_eff([0.5, 0.25, 0.15, 0.10]), 2.899)
    assert close(gap_ceiling([0.5, 0.25, 0.15, 0.10], 0.4), 1.1667)


def test_rotation():
    z = rotate(zipf(6), 0.5)
    assert close(z[0], 0.2874)
    assert close(z[-1], 0.1173)
    assert close(n_eff(z), 5.344)
    assert close(gap_ceiling(z, 0.3), 1.1968)
    assert lclose(rotate([0.4, 0.3, 0.1, 0.1, 0.1], 0.5), [0.30, 0.25, 0.15, 0.15, 0.15])


def test_worth_chasing():
    assert tools_worth_chasing(zipf(6), 0.3, 0.05) == 2
    assert tools_worth_chasing([1 / 6] * 6, 0.3, 0.05) == 6   # exactly at the margin counts
    raider = estimate_mix(ROWS, "raider")
    assert tools_worth_chasing(raider, 0.3, 0.05) == 2


def test_gates():
    acts = [{"A", "B"}, {"A", "C"}, {"B", "C"}]
    assert close(gate_share({"A"}, acts), 0.0)
    assert close(gate_share({"A", "B"}, acts), 1 / 3)
    assert close(gate_share({"A", "B", "C"}, acts), 1.0)
    assert lclose(gate_marginals(3, 2), [0.0, 1 / 3, 2 / 3])
    assert lclose(gate_marginals(4, 3), [0.0, 0.0, 0.25, 0.75])


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
    raise SystemExit(1 if failed else 0)
