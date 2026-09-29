"""Tests for Lab 14. Values come from the week 14 lecture and encounters.json.
Run with ../../../../.venv/bin/python test_cue_audit.py (or pytest)."""
from cue_audit import (audit, blocked_groups, cheapest_fix, fight_shut_out, load,
                       shut_out_of, spans_two_senses)

PROFILES, COSTS, BOSSES = load()


def close(a, b, tol=1e-9):
    return abs(a - b) < tol


def test_shut_out_and_E():
    assert shut_out_of({"colour"}, PROFILES) == {"colour-deficient"}
    assert shut_out_of({"colour", "shape"}, PROFILES) == set()
    assert shut_out_of({"icon", "text"}, PROFILES) == {"low vision"}
    assert close(fight_shut_out(BOSSES["Twin Wardens"], PROFILES), 0.22)
    assert close(fight_shut_out(BOSSES["Hollow King"], PROFILES), 0.17)
    assert close(fight_shut_out(BOSSES["Hollow King"], PROFILES, essential_only=False), 0.22)
    assert close(fight_shut_out(BOSSES["Glass Choir"], PROFILES), 0.02)


def test_blocked_groups():
    assert close(blocked_groups(0.22, 5), 0.7112825632)
    assert close(blocked_groups(0.02, 20), 0.332392028, 1e-8)
    assert blocked_groups(0.0, 40) == 0.0
    assert close(blocked_groups(1 / 12, 20), 0.824519533, 1e-8)   # the lecture's hook


def test_two_senses():
    assert spans_two_senses({"colour", "sound"})
    assert not spans_two_senses({"colour", "icon"})
    assert not spans_two_senses({"colour", "haptic"})
    assert spans_two_senses({"text", "sound", "haptic"})


def test_cheapest_fix():
    assert cheapest_fix({"colour", "shape"}, PROFILES, COSTS) == (0, ())
    assert cheapest_fix({"colour"}, PROFILES, COSTS) == (1, ("text",))
    assert cheapest_fix({"sound"}, PROFILES, COSTS) == (1, ("colour",))
    assert cheapest_fix({"icon", "text"}, PROFILES, COSTS) == (1, ("colour",))
    assert cheapest_fix({"colour"}, PROFILES, COSTS, require_two_senses=True) == (3, ("sound",))
    assert cheapest_fix({"shape"}, PROFILES, COSTS, require_two_senses=True) == (3, ("sound",))


def test_audit():
    assert audit(BOSSES["Twin Wardens"], PROFILES, COSTS) == (
        3, {"polarity": ("text",), "whisper": ("colour",), "chains": ("colour",)})
    assert audit(BOSSES["Hollow King"], PROFILES, COSTS) == (
        2, {"toll": ("colour",), "crown mark": ("colour",)})
    assert audit(BOSSES["Twin Wardens"], PROFILES, COSTS, require_two_senses=True) == (
        10, {"polarity": ("sound",), "burning ground": ("sound",),
             "whisper": ("colour",), "chains": ("sound",)})
    assert audit(BOSSES["Glass Choir"], PROFILES, COSTS, require_two_senses=True) == (
        6, {"refrain": ("sound",), "harmony": ("sound",)})


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print("PASS", name)
            except Exception as e:  # noqa: BLE001
                failed += 1
                print("FAIL", name, type(e).__name__, e)
    raise SystemExit(1 if failed else 0)
