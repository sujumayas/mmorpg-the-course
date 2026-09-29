"""Tests for repo_model.py. Run: python test_repo_model.py
They use the lecture's numbers. All must pass."""
import math
import repo_model as m

SEMESTER = [{"path": f"art/a{i}.png", "size": 4_000_000, "versions": 9} for i in range(200)]
MIXED = SEMESTER + [
    {"path": "src/player.gd", "size": 20_000, "versions": 30},
    {"path": "music/theme.ogg", "size": 5_000_000, "versions": 3},
]
JAM = [{"path": f"jam/s{i}.png", "size": 1_500_000, "versions": 7} for i in range(60)]


def test_pointer_size():
    assert m.pointer_size(3_000_000) == 132
    assert m.pointer_size(12345) == 130
    assert m.pointer_size(7) == 126


def test_is_lfs():
    assert m.is_lfs("art/hero.png", ["*.png"])
    assert not m.is_lfs("src/main.gd", ["*.png", "*.wav"])
    assert m.is_lfs("audio/sfx/jump.wav", ["*.png", "*.wav"])
    assert not m.is_lfs("png/readme.txt", ["*.png"])
    assert not m.is_lfs("art/hero.png", [])


def test_semester_without_lfs():
    assert m.history_bytes(SEMESTER, []) == 7_200_000_000
    assert m.clone_bytes(SEMESTER, []) == 7_200_000_000
    assert m.lfs_server_bytes(SEMESTER, []) == 0


def test_semester_with_lfs():
    assert m.history_bytes(SEMESTER, ["*.png"]) == 200 * 9 * 132
    assert m.clone_bytes(SEMESTER, ["*.png"]) == 800_000_000 + 200 * 9 * 132
    assert m.lfs_server_bytes(SEMESTER, ["*.png"]) == 7_200_000_000


def test_mixed_patterns():
    pats = ["*.png"]          # the .ogg was forgotten
    expected_history = 200 * 9 * 132 + 20_000 * 30 + 5_000_000 * 3
    assert m.history_bytes(MIXED, pats) == expected_history
    assert m.clone_bytes(MIXED, pats) == expected_history + 800_000_000


def test_clone_minutes():
    assert math.isclose(m.clone_minutes(7_200_000_000, 50), 19.2)
    assert math.isclose(m.clone_minutes(m.clone_bytes(JAM, []), 10), 8.4)
    assert math.isclose(m.clone_minutes(90_000_000, 10), 1.2)


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t()
            passed += 1
            print("PASS", t.__name__)
        except Exception as e:  # noqa: BLE001
            print("FAIL", t.__name__, "-", type(e).__name__, e)
    print(f"{passed}/{len(tests)} tests passed")
    raise SystemExit(0 if passed == len(tests) else 1)
