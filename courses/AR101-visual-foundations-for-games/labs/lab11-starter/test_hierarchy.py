"""Tests for AR101 Lab 11. Numbers come from the week 11 lecture.
Run with `python test_hierarchy.py` or `pytest test_hierarchy.py`."""
import sys

from hierarchy import element_weight, inversions, weak_steps, weight


def close(a, b, tol=0.05):
    return abs(a - b) <= tol


def test_weight():
    assert close(weight(1.0, 100, 35), 65.0)
    assert close(weight(0.81, 55, 35), 16.2)
    assert close(weight(2.0, 10, 35), 50.0)      # darker than the ground counts too


def test_element_without_plate():
    el = {"size": 1.3, "text_v": 100, "plate_v": None, "plate_area": 0}
    assert close(element_weight(el, 15), 143.65)


def test_element_with_plate():
    rare = {"size": 1.1, "text_v": 100, "plate_v": 10, "plate_area": 2.0}
    epic = {"size": 1.25, "text_v": 10, "plate_v": 90, "plate_area": 2.6}
    assert close(element_weight(rare, 35), 158.9)
    assert close(element_weight(epic, 35), 268.0)
    assert close(element_weight(epic, 92), 130.2)


def test_inversions_wow_on_black():
    w = [64.7, 100.0, 87.9, 48.0, 47.6, 67.1]
    assert inversions([1, 2, 3, 4, 5, 6], w) == 10


def test_inversions_skip_same_level():
    assert inversions([1, 1, 2], [50, 40, 45]) == 1
    assert inversions([1, 2, 2, 3], [50, 86.4, 30, 80]) == 2


def test_weak_steps():
    lv = [1, 2, 3, 4]
    assert weak_steps(lv, [16.2, 65.0, 158.9, 268.0]) == []
    got = weak_steps(lv, [20, 30, 45, 65])
    assert len(got) == 1 and got[0][:2] == (3, 4) and close(got[0][2], 1.444, 0.01)
    got = weak_steps([1, 1, 2], [40, 60, 80], 1.5)
    assert len(got) == 1 and got[0][:2] == (1, 2) and close(got[0][2], 1.333, 0.01)
    assert weak_steps([1, 3], [10, 12], 1.5)[0][:2] == (1, 3)


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
    sys.exit(1 if failed else 0)
