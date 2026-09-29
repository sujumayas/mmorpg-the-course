"""Tests for GD202 Lab 11. Values come from the week 11 lecture, sections 2 and 3.
Run with `.venv/bin/python test_loc_lint.py` (from any folder) or pytest."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from loc_lint import (budget, forms_needed, is_fragment, missing_forms,  # noqa: E402
                      plural_category, two_slot_errors)

TABLE = {  # n: [en, fr, ru, pl, ar, ja], lecture section 2
    0: ["other", "one", "many", "many", "zero", "other"],
    1: ["one", "one", "one", "one", "one", "other"],
    2: ["other", "other", "few", "few", "two", "other"],
    5: ["other", "other", "many", "many", "few", "other"],
    11: ["other", "other", "many", "many", "many", "other"],
    21: ["other", "other", "one", "many", "many", "other"],
    22: ["other", "other", "few", "few", "many", "other"],
    101: ["other", "other", "one", "many", "other", "other"],
    112: ["other", "other", "many", "many", "many", "other"],
}


def test_plural_category_table():
    for n, row in TABLE.items():
        got = [plural_category(lang, n) for lang in ["en", "fr", "ru", "pl", "ar", "ja"]]
        assert got == row, f"n={n}: {got}"


def test_plural_category_edges():
    assert plural_category("fr", 1_000_000) == "many"
    assert plural_category("fr", 2_000_000) == "many"
    assert plural_category("fr", 1_500_000) == "other"
    assert plural_category("ru", 111) == "many"
    assert plural_category("ru", 1001) == "one"
    assert plural_category("ar", 103) == "few"
    assert plural_category("ar", 200) == "other"


def test_forms_needed():
    assert forms_needed("ru", 30) == ["one", "few", "many"]
    assert forms_needed("ar", 30) == ["zero", "one", "two", "few", "many"]
    assert forms_needed("ar", 100) == ["zero", "one", "two", "few", "many", "other"]
    assert forms_needed("fr", 100) == ["one", "other"]
    assert forms_needed("fr", 1_000_000) == ["one", "many", "other"]
    assert forms_needed("ja", 50) == ["other"]
    assert forms_needed("en", 0) == ["other"]


def test_missing_forms():
    entry = {"count_max": 10, "forms": {
        "ru": {"one": "x", "many": "x"},
        "ar": {"one": "x", "other": "x"},
        "ja": {"other": "x"}}}
    assert missing_forms(entry, "ru") == ["few"]
    assert missing_forms(entry, "ar") == ["zero", "two", "few"]
    assert missing_forms(entry, "ja") == []
    assert missing_forms(entry, "pl") == ["one", "few", "many"], "no forms at all"


def test_two_slot_errors():
    assert two_slot_errors("en", 100) == 0
    assert two_slot_errors("fr", 100) == 1
    assert two_slot_errors("ru", 100) == 35
    assert two_slot_errors("pl", 100) == 27
    assert two_slot_errors("ar", 100) == 11
    assert two_slot_errors("ja", 100) == 0


def test_budget():
    assert budget("OK") == 6
    assert budget("Accept") == 18
    assert budget("Quest Log") == 27
    assert budget("Abandon quest") == 26
    assert budget("Hand in the wolf pelts") == 40
    assert budget("Speak to the ferryman at Low Crossing before dusk") == 78
    assert budget("x" * 60) == 96
    assert budget("The bridge is gone. Cross at the ford, a mile south of the ruins, and hurry.") == 99


def test_is_fragment():
    assert is_fragment("You found ")
    assert is_fragment(" in the ")
    assert is_fragment("Deliver the pelts to")
    assert is_fragment("The toll is paid, and")
    assert not is_fragment("You found {item} in {place}.")
    assert not is_fragment("Accept")
    assert not is_fragment("The Greywood")
    assert not is_fragment("Theft is a crime.")
    assert not is_fragment("The river's too high for the ferry, and I owe the toll-keeper more than I can pay.")
    assert is_fragment("with your friend")
    assert is_fragment(".")


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
            except AssertionError as e:
                failed += 1
                print(f"FAIL {name} {e}")
    print(f"\n{failed} test(s) not passing" if failed else "\nAll tests pass.")
    sys.exit(1 if failed else 0)
