"""Tests for GD202 Lab 04. Values come from the week 4 lecture and lab04.md.
Run with `.venv/bin/python test_rules.py` (from any folder) or pytest."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dialogue_rules import BARKEEP, BARKEEP_DOMAINS, Rule, all_states, audit, matches, winners  # noqa: E402


def S(met, wolves, thief):
    return {"met": met, "wolves_dead": wolves, "thief": thief}


def test_matches():
    assert matches(BARKEEP[0], S(False, False, False))
    assert matches(BARKEEP[4], S(True, True, False))
    assert not matches(BARKEEP[4], S(True, False, False))
    assert matches(Rule("x", [("speech", ">=", 50)]), {"speech": 50})
    assert not matches(Rule("x", [("speech", ">=", 50)]), {"speech": 49})


def test_winners_table():
    assert winners(BARKEEP, S(False, False, False)) == ["R0"]
    assert winners(BARKEEP, S(False, True, True)) == ["R5"]
    assert winners(BARKEEP, S(True, False, False)) == ["R1"]
    assert winners(BARKEEP, S(True, False, True)) == ["R1", "R3"]
    assert winners(BARKEEP, S(True, True, True)) == ["R4", "R5"]


def test_no_match_is_empty():
    assert winners(BARKEEP[1:], S(False, False, False)) == []


def test_all_states():
    states = all_states({"a": [False, True], "stage": [0, 10, 20]})
    assert len(states) == 6
    assert states[0] == {"a": False, "stage": 0}
    assert states[-1] == {"a": True, "stage": 20}


def test_barkeep_audit():
    r = audit(BARKEEP, BARKEEP_DOMAINS)
    assert r["states"] == 8
    assert r["silent"] == []
    assert sorted(names for _, names in r["ties"]) == [["R1", "R3"], ["R4", "R5"]]
    assert r["wins"] == {"R0": 1, "R1": 1, "R2": 1, "R3": 1, "R4": 1, "R5": 1}
    assert r["dead"] == [] and r["only_ties"] == []


def test_add_r6():
    r6 = Rule("R6", [("met", "==", True), ("thief", "==", True)], "You've got a nerve.")
    r = audit(BARKEEP + [r6], BARKEEP_DOMAINS)
    assert [names for _, names in r["ties"]] == [["R4", "R5", "R6"]]
    assert r["wins"]["R6"] == 1 and r["wins"]["R3"] == 1


def test_no_fallback_is_silent():
    r = audit(BARKEEP[1:], BARKEEP_DOMAINS)
    assert r["silent"] == [S(False, False, False)]


def test_fourth_flag_doubles():
    domains = dict(BARKEEP_DOMAINS, paid_debt=[False, True])
    r = audit(BARKEEP, domains)
    assert r["states"] == 16 and len(r["ties"]) == 4


def test_dead_and_only_ties():
    rules = [
        Rule("base", [], "Hm."),
        Rule("impossible", [("wolves", "==", 10), ("wolves", ">=", 20)], "Never heard."),
        Rule("a", [("met", "==", True)], "A."),
        Rule("b", [("met", "==", True)], "B."),
    ]
    r = audit(rules, {"met": [False, True], "wolves": [0, 10, 20, 30]})
    assert r["dead"] == ["impossible"]
    assert r["only_ties"] == ["a", "b"]
    assert r["wins"]["base"] == 4


def test_skill_check_fallback():
    # Fallout: New Vegas style: a threshold rule beats the weak fallback line.
    rules = [
        Rule("weak", [("asked", "==", True)], "Um. Dynamite, please?"),
        Rule("strong", [("asked", "==", True), ("explosives", ">=", 25)], "A reasoned case."),
        Rule("idle", [], "..."),
    ]
    assert winners(rules, {"asked": True, "explosives": 24}) == ["weak"]
    assert winners(rules, {"asked": True, "explosives": 25}) == ["strong"]


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
