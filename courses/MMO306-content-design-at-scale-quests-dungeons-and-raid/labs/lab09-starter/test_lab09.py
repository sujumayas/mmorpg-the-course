"""Checks for MMO306 Lab 09. Run from this folder:  python test_lab09.py
Each check prints PASS or FAIL. A NotImplementedError counts as FAIL."""
import traceback

import generator as g


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


def test_signature_ignores_decoration():
    a = {"layout": "Crypt", "boss": "Lich", "modifier": "Fog", "decoration_seed": 1, "torch_count": 9}
    b = dict(a, decoration_seed=99, torch_count=30)
    assert g.signature(a) == ("Crypt", "Lich", "Fog")
    assert g.signature(a) == g.signature(b)
    assert g.signature(a, ("boss",)) == ("Lich",)


def test_effective_variety():
    assert close(g.effective_variety([1, 1, 1, 1]), 4)
    assert close(g.effective_variety([4, 3, 1, 1, 1]), 1 / 0.28)
    assert close(g.effective_variety([7, 1, 1, 1]), 1 / 0.52)


def test_perceived_and_effective():
    m, me = g.perceived_and_effective()
    assert m == 100
    assert close(me, (1 / 0.24) * 4 * (1 / 0.28), 0.01)       # about 59.5
    lecture = {"layout": {i: 1 for i in range(6)}, "boss": {i: 1 for i in range(4)},
               "modifier": dict(zip("abcde", [4, 3, 1, 1, 1]))}
    assert close(g.perceived_and_effective(lecture)[1], 85.714, 0.01)


def test_repeat_probabilities():
    assert close(g.p_repeat(10, 85.714), 0.408)
    assert close(g.p_repeat(20, 85.714), 0.891)
    assert close(g.p_repeat_uniform_exact(5, 12), 0.618)
    assert close(g.p_repeat_uniform_exact(20, 120), 0.813)
    assert close(g.n50(120), 13.41, 0.01)
    assert close(g.n50(12), 4.61, 0.01)


def test_measured_m_eff():
    assert close(g.measured_m_eff(["a", "b", "c", "d"]), 4)
    assert close(g.measured_m_eff(["a", "a", "a", "b"]), 1 / (0.5625 + 0.0625))


def test_rejection():
    assert close(g.expected_attempts(0.2), 5)
    assert close(g.p_more_than(0.2, 20), 0.0115)
    assert close(g.p_more_than(0.4, 8), 0.0168)


def test_first_repeat_simulation():
    base = g.first_repeat_median(3000, seed=5)
    assert 9 <= base <= 11, base
    mem = g.first_repeat_median(3000, seed=5, memory=3)
    assert mem >= base + 1, (base, mem)
    flat = {"layout": {x: 1 for x in g.AXES["layout"]}, "boss": dict(g.AXES["boss"]),
            "modifier": {x: 1 for x in g.AXES["modifier"]}, "weather": {"Clear": 1, "Storm": 1}}
    assert 16 <= g.first_repeat_median(3000, seed=5, axes=flat) <= 18   # weather must count


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("test_")]

if __name__ == "__main__":
    passed = 0
    for fn in TESTS:
        try:
            fn()
            print(f"PASS {fn.__name__}")
            passed += 1
        except NotImplementedError:
            print(f"FAIL {fn.__name__} (not implemented yet)")
        except Exception:
            print(f"FAIL {fn.__name__}")
            traceback.print_exc(limit=1)
    print(f"{passed}/{len(TESTS)} checks passed")
    raise SystemExit(0 if passed == len(TESTS) else 1)
