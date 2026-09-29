"""Tests for AU101 Lab 10. Values come from the week 10 lecture.
Run with `python3 test_mixer.py` (or pytest)."""
import math

from mixer import (SCENE, Request, allocate, db_sum, duck_step, effective_priority,
                   hdr_output, hdr_step, hdr_target, run_scene)


def close(a, b, tol=0.05):
    return abs(a - b) <= tol


def test_db_sum():
    assert close(db_sum([-20]), -20)
    assert close(db_sum([-20, -20]), -16.99)
    assert close(db_sum([-20] * 10), -10)
    assert close(db_sum([-20] * 40), -3.98)
    assert close(db_sum([0, -10]), 0.41)
    assert db_sum([]) == float("-inf")


def test_hdr_target_and_step():
    assert hdr_target([20, 0, -15], threshold=0) == 20
    assert hdr_target([-15, -25], threshold=0) == 0
    assert hdr_step(20, [45, 20], 0, 20, 0.05) == 45          # instant attack
    assert close(hdr_step(45, [20], 0, 20, 0.05), 44.0)        # 1 dB per step
    assert hdr_step(20.5, [20], 0, 20, 0.05) == 20             # no undershoot


def test_hdr_output():
    assert hdr_output(-15, 20, 48) == -35
    assert hdr_output(-15, 45, 48) is None
    assert hdr_output(-15, 33, 48) == -48                      # edge is audible


def test_scene_timeline():
    rows = {round(t / 0.05): (top, outs) for t, top, outs in
            run_scene(SCENE, threshold=0, window=48, release=20, dt=0.05, t_end=2.0)}
    top, outs = rows[0]
    assert top == 45 and outs["birds"] is None and outs["gunfire"] == -25
    top, outs = rows[20]                                        # t = 1.0 s
    assert close(top, 35) and outs["birds"] is None
    top, outs = rows[22]                                        # t = 1.1 s
    assert close(top, 33) and close(outs["birds"], -48)
    top, outs = rows[30]                                        # t = 1.5 s
    assert close(top, 25) and outs["wind"] is None
    top, outs = rows[35]                                        # t = 1.75 s
    assert close(top, 20) and close(outs["wind"], -45)


def test_duck():
    g = 0.0
    for _ in range(2):                                          # 0.1 s of dialogue
        g = duck_step(g, True, depth=8, attack_time=0.1, release_time=1.0, dt=0.05)
    assert close(g, -8)
    g = duck_step(g, True, 8, 0.1, 1.0, 0.05)
    assert close(g, -8)                                         # no overshoot
    for _ in range(10):                                         # 0.5 s of silence
        g = duck_step(g, False, 8, 0.1, 1.0, 0.05)
    assert close(g, -4)


def test_priority_and_allocation():
    assert close(effective_priority(60, 20, 0, 40), 60)
    assert close(effective_priority(60, 20, 10, 40), 55)
    assert close(effective_priority(60, 20, 80, 40), 40)
    reqs = [Request("boss_roar", 90, 30, 0.0), Request("my_spell", 80, 0, 1.0),
            Request("ally_a", 60, 10, 0.5), Request("ally_b", 60, 10, 0.2),
            Request("ambience", 20, 0, 0.0)]
    assert allocate(reqs, 3, 20, 40) == ["my_spell", "boss_roar", "ally_b"]
    assert allocate(reqs, 3, 20, 40, keep="newest") == ["my_spell", "boss_roar", "ally_a"]


if __name__ == "__main__":
    failed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print("PASS", name)
            except Exception as e:  # noqa: BLE001
                failed += 1
                print("FAIL", name, type(e).__name__, e)
    raise SystemExit(1 if failed else 0)
