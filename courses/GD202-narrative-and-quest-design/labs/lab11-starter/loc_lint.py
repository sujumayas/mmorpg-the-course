"""GD202 Lab 11: localization linter.

Standard library only. Fill in the TODO functions, then run the tests:

    .venv/bin/python courses/GD202-narrative-and-quest-design/labs/lab11-starter/test_loc_lint.py

Once the tests pass, lint the quest strings:

    .venv/bin/python courses/GD202-narrative-and-quest-design/labs/lab11-starter/loc_lint.py quest_strings.json

Rules come from the week 11 lecture: CLDR 48 plural rules for whole numbers
(section 2) and the W3C/IBM expansion bands (section 3).

A strings file is a JSON list of entries:
  {"id": "...", "en": "...", "note": "...",          # note may be ""
   "max_chars": 24,                                 # optional UI width
   "count_max": 30,                                 # optional: largest count shown
   "forms": {"en": {"one": "...", "other": "..."},  # optional plural forms per language
             "ru": {...}}}
"""
import json
import os
import sys

LANGS = ["en", "fr", "ru", "pl", "ar", "ja"]
ORDER = ["zero", "one", "two", "few", "many", "other"]   # CLDR's own order


def plural_category(lang, n):
    """TODO 1. Return the CLDR 48 cardinal plural category ("zero", "one",
    "two", "few", "many" or "other") of the whole number n >= 0 in `lang`,
    one of LANGS. Use the table in lecture section 2."""
    raise NotImplementedError("plural_category() is yours to write")


def forms_needed(lang, count_max):
    """TODO 2. Return the categories reached by the counts 0..count_max
    (inclusive) in `lang`, as a list sorted in ORDER."""
    raise NotImplementedError("forms_needed() is yours to write")


def missing_forms(entry, lang):
    """TODO 3. For an entry with "count_max" and "forms", return the list
    (sorted in ORDER) of categories that `lang` needs for counts
    0..count_max but that entry["forms"][lang] does not supply.
    A language with no forms at all is missing everything it needs."""
    raise NotImplementedError("missing_forms() is yours to write")


def two_slot_errors(lang, count_max):
    """TODO 4. An English-style system has one string for n == 1 and one
    "plural" string for every other n. The translator fills the plural slot
    with the single category that is right for the most counts. Return how
    many counts in 0..count_max still get the wrong category."""
    raise NotImplementedError("two_slot_errors() is yours to write")


def budget(text):
    """TODO 5. Characters to reserve for a translation of `text`: its length
    times the band factor (<=10: 3.0, 11-20: 2.0, 21-30: 1.8, 31-70: 1.6,
    over 70: 1.3), rounded to the nearest whole number."""
    raise NotImplementedError("budget() is yours to write")


# Words a whole sentence rarely ends with, and connectors it rarely starts with.
FRAGMENT_END_WORDS = {"a", "an", "the", "your", "in", "of", "to", "at", "for", "from", "with", "and"}
FRAGMENT_START_WORDS = {"in", "of", "to", "at", "for", "from", "with", "and"}


def is_fragment(text):
    """TODO 6. Return True if `text` looks like a piece of a concatenated
    sentence: it is empty or only punctuation, it starts or ends with
    whitespace, its last word is in FRAGMENT_END_WORDS, or its first word is
    in FRAGMENT_START_WORDS. Compare words in lower case with the punctuation
    .,!?;: stripped from their ends."""
    raise NotImplementedError("is_fragment() is yours to write")


# ---- Provided: the linter ---------------------------------------------------

def lint(entries):
    problems = []
    for e in entries:
        sid, en = e["id"], e["en"]
        if is_fragment(en):
            problems.append((sid, "fragment", f"looks concatenated: {en!r}"))
        if "max_chars" in e and budget(en) > e["max_chars"]:
            problems.append((sid, "width", f"needs {budget(en)} chars, has {e['max_chars']}"))
        if not e.get("note"):
            problems.append((sid, "note", "no context note for translators"))
        if "count_max" in e:
            for lang in LANGS:
                miss = missing_forms(e, lang)
                if miss:
                    problems.append((sid, "plural", f"{lang} missing {', '.join(miss)}"))
    return problems


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    path = sys.argv[1] if len(sys.argv) > 1 else "quest_strings.json"
    if not os.path.exists(path):
        path = os.path.join(here, path)
    with open(path) as fh:
        entries = json.load(fh)
    found = lint(entries)
    for sid, kind, msg in found:
        print(f"{sid:<24}{kind:<10}{msg}")
    kinds = sorted({k for _, k, _ in found})
    print(f"\n{len(entries)} strings, {len(found)} problems "
          + ", ".join(f"{k}: {sum(1 for _, x, _ in found if x == k)}" for k in kinds))
