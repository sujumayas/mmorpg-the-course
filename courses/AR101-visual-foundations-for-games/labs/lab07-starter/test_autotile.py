"""Tests for lab 07. Run with .venv/bin/python test_autotile.py (pytest also works)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from autotile import edge_index, blob_index, corner_rule, seam_ratio, tiles_used  # noqa: E402

PLAZA = [[0, 0, 0, 0, 0],
         [0, 1, 1, 1, 0],
         [0, 1, 1, 1, 0],
         [0, 0, 1, 0, 0],
         [0, 0, 1, 0, 0]]


def test_edge_plaza():
    expected = {(1, 1): 6, (1, 2): 14, (1, 3): 12, (2, 1): 3,
                (2, 2): 15, (2, 3): 9, (3, 2): 5, (4, 2): 1}
    for (r, c), want in expected.items():
        assert edge_index(PLAZA, r, c) == want, f"edge ({r},{c})"


def test_blob_plaza():
    expected = {(1, 1): 28, (1, 2): 124, (1, 3): 112, (2, 1): 7,
                (2, 2): 215, (2, 3): 193, (3, 2): 17, (4, 2): 1}
    for (r, c), want in expected.items():
        assert blob_index(PLAZA, r, c) == want, f"blob ({r},{c})"


def test_lone_plus_and_block():
    assert edge_index([[1]], 0, 0) == 0 and blob_index([[1]], 0, 0) == 0
    plus = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    assert edge_index(plus, 1, 1) == 15 and blob_index(plus, 1, 1) == 85
    block = [[1] * 3 for _ in range(3)]
    assert blob_index(block, 1, 1) == 255 and blob_index(block, 0, 0) == 28


def test_corner_rule():
    assert corner_rule(2) == 0            # NE alone: N and E missing
    assert corner_rule(1 + 2 + 4) == 7    # NE with N and E: kept
    assert corner_rule(1 + 2 + 64) == 1 + 64   # NE with N only: cleared
    assert corner_rule(255) == 255


def test_forty_seven():
    assert len({corner_rule(raw) for raw in range(256)}) == 47


def test_diagonal_touch_changes_nothing():
    base = [[1, 1, 1, 0], [1, 1, 1, 0], [1, 1, 1, 0], [0, 0, 0, 0]]
    touch = [row[:] for row in base]
    touch[3][3] = 1
    assert blob_index(base, 2, 2) == blob_index(touch, 2, 2)
    bridged = [row[:] for row in touch]
    bridged[2][3] = 1
    assert blob_index(bridged, 2, 2) != blob_index(touch, 2, 2)


def test_seam_ratio():
    diagonal = [[40, 50, 60, 50], [50, 60, 50, 40], [60, 50, 40, 50], [50, 40, 50, 60]]
    gradient = [[20, 40, 60, 80] for _ in range(4)]
    assert abs(seam_ratio(diagonal) - 1.0) < 1e-9
    assert abs(seam_ratio(gradient) - 3.0) < 1e-9
    assert seam_ratio([[50, 50], [50, 50]]) == 1.0


def test_tiles_used():
    assert len(tiles_used(PLAZA, "blob")) == 8


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print("PASS", t.__name__)
        except Exception as e:  # noqa: BLE001
            failed += 1
            print("FAIL", t.__name__, "-", type(e).__name__, e)
    print(f"{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
