"""Tests for Lab 07. Values come from the week 7 lecture and its interactive spec.
Run with ../../../../.venv/bin/python test_lore_memory.py (or pytest)."""
from lore_memory import audit, half_life, knowledge, load_beats, needed_r, steady_mix, two_group


def close(x, y, tol=1e-3):
    return abs(x - y) < tol


def test_knowledge_table():
    want = {(0.0, 12): 0.226, (0.3, 12): 0.441, (0.9, 12): 0.872, (0.0, 24): 0.064,
            (0.3, 36): 0.311}
    for (r, m), k in want.items():
        assert close(knowledge(0.8, 0.10, r, m), k), (r, m)
    assert close(knowledge(0.6, 0.05, 0.5, 24), 0.529)
    assert knowledge(0.7, 0.2, 0.4, 0) == 0.7


def test_half_life():
    assert close(half_life(0.10), 6.579)
    assert close(half_life(0.05), 13.513)


def test_needed_r():
    assert close(needed_r(0.5, 0.8, 0.10, 12), 0.382)
    assert close(needed_r(0.5, 0.8, 0.10, 24), 0.474)
    assert needed_r(0.5, 0.8, 0.10, 1) < 0  # live reach alone still meets the target
    assert close(knowledge(0.8, 0.06, needed_r(0.5, 0.8, 0.06, 20), 20), 0.5)


def test_steady_mix():
    assert close(steady_mix(0.4, 0.04, 0.5), 1 / 11)
    assert close(steady_mix(0.1, 0.1, 0.3), 0.3)


def test_two_group_matches_one_group_when_churn_is_equal():
    k = two_group(0.8, 0.3, 0.1, 0.1, 0.5, 24)
    assert len(k) == 25 and k[0] == 0.8
    for m in (1, 6, 12, 24):
        assert close(k[m], knowledge(0.8, 0.1, 0.3, m), 1e-9), m


def test_two_group_lasts_longer():
    k = two_group(0.8, 0.0, 0.4, 0.04, 0.5, 24)
    assert close(k[6], 0.5727) and close(k[12], 0.4458) and close(k[24], 0.2730)
    avg_churn = 1 / 13.75  # the steady population's average churn
    assert k[12] > knowledge(0.8, avg_churn, 0.0, 12) + 0.1


def test_beats_and_audit():
    beats = load_beats()
    assert len(beats) == 5 and beats[1] == ("The harbor city burns", 0.8, 0.0)
    table = audit(beats, 0.08)
    k12, k24 = table["The harbor city burns"]
    assert close(k12, 0.8 * 0.92**12) and close(k24, 0.8 * 0.92**24)


if __name__ == "__main__":
    import sys
    failed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("PASS", name)
            except Exception as e:  # noqa: BLE001
                failed += 1
                print("FAIL", name, type(e).__name__, e)
    print(f"{failed} failed")
    sys.exit(1 if failed else 0)
