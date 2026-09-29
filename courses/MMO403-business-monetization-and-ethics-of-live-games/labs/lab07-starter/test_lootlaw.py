"""Tests for MMO403 Lab 07. Values come from the week 7 lecture.

Run with `.venv/bin/python test_lootlaw.py` (exits 1 while any test fails)
or with pytest if you have it.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lootlaw import (PRESETS, Design, assess, assess_all, compliance, fixes,  # noqa: E402
                     must_remove, switch_off_cost)

A, B, C, D, E, F = (PRESETS[k] for k in "ABCDEF")


def test_preset_a():
    assert assess_all(A) == {"BE": "remove", "NL": "none", "UK": "voluntary", "CN": "odds",
                             "KR": "odds", "BR": "remove", "AU": "rating_M", "PEGI": "rating_16"}


def test_b_matches_a():
    assert assess_all(B) == assess_all(A)


def test_remove_counts():
    assert must_remove(A) == ["BE", "BR"]
    assert must_remove(C) == ["BE", "NL", "UK"]
    assert must_remove(D) == ["BE", "NL", "BR"]
    assert must_remove(E) == [] and must_remove(F) == []
    assert set(assess_all(E).values()) == {"none"}


def test_transfer_ladder():
    assert must_remove(Design(True, True, "trade", False, True)) == ["BE", "NL", "BR"]
    assert must_remove(Design(True, True, "cashout", False, True)) == ["BE", "NL", "UK", "BR"]
    assert assess(Design(True, True, "cashout", True, False), "NL") == "none"
    assert assess(Design(True, True, "cashout", True, False), "UK") == "remove"
    assert assess(Design(True, True, "trade", True, False), "NL") == "none"


def test_compliance():
    assert compliance(A, "CN") == "breach"
    shown = Design(True, True, "none", False, True, odds_shown=True)
    assert compliance(shown, "CN") == "ok"
    assert compliance(shown, "UK") == "gap"
    both = Design(True, True, "none", False, True, odds_shown=True, parental_gate=True)
    assert compliance(both, "UK") == "ok"
    assert compliance(both, "BE") == "remove"
    assert compliance(both, "AU") == "ok"


def test_fixes():
    assert fixes(A) == [frozenset({("chance", False)}), frozenset({("paid", False)})]
    assert fixes(C, ["NL", "UK"]) == [frozenset({("chance", False)}), frozenset({("paid", False)}),
                                      frozenset({("transfer", "none")})]
    assert fixes(E) == [frozenset()]
    assert fixes(D, ["NL", "BR"]) == [frozenset({("chance", False)}), frozenset({("paid", False)})]
    assert fixes(D, ["NL"]) == [frozenset({("chance", False)}), frozenset({("paid", False)}),
                                frozenset({("skill", True)}), frozenset({("transfer", "none")})]


def test_cost():
    shares = {"BE": 0.004, "BR": 0.02, "NL": 0.015}
    regional, glob = switch_off_cost(50_000_000, 0.30, 0.5, shares, A)
    assert abs(regional - 180_000) < 1e-6 and abs(glob - 7_500_000) < 1e-6
    regional, _ = switch_off_cost(20_000_000, 0.40, 0.4, {"NL": 0.015}, D)
    assert abs(regional - 72_000) < 1e-6


TESTS = [v for k, v in dict(globals()).items() if k.startswith("test_")]

if __name__ == "__main__":
    failed = 0
    for t in TESTS:
        try:
            t()
            print("PASS", t.__name__)
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print("FAIL", t.__name__, type(exc).__name__, exc)
    print(f"{len(TESTS) - failed}/{len(TESTS)} passed")
    sys.exit(1 if failed else 0)
