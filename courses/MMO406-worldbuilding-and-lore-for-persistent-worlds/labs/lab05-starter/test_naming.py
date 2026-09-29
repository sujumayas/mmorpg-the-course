"""Tests for MMO406 Lab 05. Values come from the week 5 lecture and lab05.md.
Run with `.venv/bin/python test_naming.py` (from any folder) or pytest."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cultures import DURHK, VESSARI  # noqa: E402
from naming import ambiguity, could_pass, generate, mixed_ambiguity, overlap  # noqa: E402

TOL = 1e-9


def test_overlap_both_views_both_directions():
    assert abs(overlap(VESSARI, DURHK, weighted=False) - 4 / 12) < TOL
    assert abs(overlap(DURHK, VESSARI, weighted=False) - 4 / 8) < TOL
    assert abs(overlap(VESSARI, DURHK) - 0.60) < TOL
    assert abs(overlap(DURHK, VESSARI) - 0.25) < TOL


def test_lecture_table():
    assert abs(ambiguity(0.6, 2) - 0.36) < TOL
    assert abs(ambiguity(0.6, 3) - 0.216) < TOL
    assert abs(ambiguity(0.25, 2) - 0.0625) < TOL
    assert abs(ambiguity(0.6, 2, m=0.5) - 0.18) < TOL
    assert ambiguity(0.6, 2, m=1) == 0


def test_check_yourself_values():
    assert abs(ambiguity(0.3, 2) - 0.09) < TOL
    assert abs(ambiguity(0.3, 3) - 0.027) < TOL


def test_mixed_lengths():
    assert abs(mixed_ambiguity(0.6, {2: 0.5, 3: 0.5}) - 0.288) < TOL
    assert abs(mixed_ambiguity(0.6, {2: 1.0}, m=0.5) - 0.18) < TOL


def test_generate_shape_and_repeatability():
    a = generate(VESSARI, 50, 3, seed=7)
    b = generate(VESSARI, 50, 3, seed=7)
    assert a == b
    assert len(a) == 50 and all(len(n) == 3 and all(s in VESSARI for s in n) for n in a)


def test_generate_matches_model():
    names = generate(VESSARI, 20000, 2, seed=3)
    share = sum(could_pass(n, DURHK) for n in names) / len(names)
    assert abs(share - 0.36) < 0.015


def test_full_marker_removes_ambiguity():
    marker = {s for s in VESSARI if s not in DURHK}
    names = generate(VESSARI, 2000, 2, seed=5, marker=marker, m=1.0)
    assert all(n[-1] in marker for n in names)
    assert not any(could_pass(n, DURHK) for n in names)


def test_partial_marker_matches_model():
    marker = {s for s in VESSARI if s not in DURHK}
    names = generate(VESSARI, 20000, 2, seed=11, marker=marker, m=0.5)
    share = sum(could_pass(n, DURHK) for n in names) / len(names)
    assert abs(share - 0.18) < 0.015


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
    print(f"\n{failed} test(s) not passing" if failed else "\nAll tests pass.")
    sys.exit(1 if failed else 0)
