"""Tests for PR101 Lab 06. Run: python test_lab06.py (from this folder)."""
import math
import estimates as m

LOG = m.load_log("jam_plans_example.csv")
TOL = 1e-3


def close(a, b, tol=TOL):
    return abs(a - b) <= tol


def test_ratio():
    assert m.ratio(4, 6) == 1.5
    assert m.ratio(2, 1) == 0.5
    for bad in (0, -1):
        try:
            m.ratio(bad, 3)
        except ValueError:
            pass
        else:
            raise AssertionError(f"ratio({bad}, 3) must raise ValueError")


def test_median():
    v = [4.0, 0.5, 1.0, 2.5, 1.0]
    assert m.median(v) == 1.0
    assert v == [4.0, 0.5, 1.0, 2.5, 1.0], "median must not reorder the caller's list"
    toy = [0.5, 0.75, 0.8, 1.0, 1.0, 1.0, 1.5, 2.0, 2.5, 4.0]   # lecture section 2
    assert m.median(toy) == 1.0
    assert m.median([1, 2, 3, 10]) == 2.5
    try:
        m.median([])
    except ValueError:
        pass
    else:
        raise AssertionError("median([]) must raise ValueError")


def test_percentile():
    v = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert close(m.percentile(v, 0.1), 1.9)
    assert close(m.percentile(v, 0.9), 9.1)
    assert close(m.percentile(v, 0.5), m.median(v))
    assert m.percentile([7], 0.9) == 7
    for bad in ((v, 1.5), ([], 0.5)):
        try:
            m.percentile(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"percentile{bad} must raise ValueError")


def test_summary_matches_lecture():
    want = {
        "none": {"n": 44, "p10": 0.500, "median": 1.000, "p90": 3.308,
                 "mean": 1.494, "project": 302.5 / 204},
        "split4": {"n": 69, "p10": 0.658, "median": 1.000, "p90": 1.667,
                   "mean": 1.074, "project": 187.0 / 176.5},
    }
    for rule, exp in want.items():
        got = m.summary(LOG, rule)
        for k, v in exp.items():
            assert close(got[k], v), f"{rule} {k}: {got[k]} != {v}"
    assert m.summary(LOG)["n"] == 113


def test_skew_penalty():
    assert m.skew_penalty(0) == 1.0
    assert close(m.skew_penalty(0.8), math.exp(0.32))
    assert close(m.skew_penalty(0.662), 1.245)


def test_buffer_for():
    assert close(m.buffer_for(1.5), 1 / 3)
    assert close(m.buffer_for(4 / 3), 0.25)
    assert m.buffer_for(1.0) == 0.0
    assert m.buffer_for(0.9) == 0.0


def test_corrected_estimate():
    lo, mid, hi = m.corrected_estimate(4, (0.5, 1.0, 3.308))
    assert close(lo, 2.0) and close(mid, 4.0) and close(hi, 13.232)


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except NotImplementedError:
            print(f"FAIL  {t.__name__}: not implemented yet")
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e or 'assertion failed'}")
    print(f"\n{passed}/{len(tests)} tests passed")
    raise SystemExit(0 if passed == len(tests) else 1)
