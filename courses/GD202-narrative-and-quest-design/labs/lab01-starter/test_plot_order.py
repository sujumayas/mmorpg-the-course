"""Tests for GD202 Lab 01. Values come from the week 1 lecture.
Run with `python test_plot_order.py` or `pytest test_plot_order.py`."""
import os

from plot_order import inversions, load_log, open_questions, scramble, validate

HERE = os.path.dirname(os.path.abspath(__file__))
TELLINGS = {
    "chronological": ([1, 2, 3, 4, 5, 6, 7, 8], 0),
    "in medias res": ([6, 1, 2, 3, 4, 5, 7, 8], 5),
    "mystery": ([5, 6, 7, 2, 3, 4, 1, 8], 15),
    "reverse": ([8, 7, 6, 5, 4, 3, 2, 1], 28),
}


def test_validate():
    assert validate([3, 1, 2]) is None
    for bad in ([1, 1, 2], [0, 1, 2], [1, 2, 4], [2, 3]):
        try:
            validate(bad)
        except ValueError:
            continue
        raise AssertionError(f"validate accepted {bad}")


def test_lecture_tellings():
    for name, (plot, expected) in TELLINGS.items():
        assert inversions(plot) == expected, name


def test_scramble():
    assert abs(scramble([6, 1, 2, 3, 4, 5, 7, 8]) - 5 / 28) < 1e-9
    assert abs(scramble([3, 1, 2, 6, 4, 5]) - 4 / 15) < 1e-9
    assert scramble([1]) == 0.0
    assert scramble([8, 7, 6, 5, 4, 3, 2, 1]) == 1.0


def test_same_count_different_shape():
    assert inversions([8, 1, 2, 3, 4, 5, 6, 7]) == 7
    assert inversions([3, 2, 1, 6, 5, 4, 8, 7]) == 7


def test_open_questions():
    assert open_questions([6, 1, 2, 3, 4, 5, 7, 8]) == [1, 1, 1, 1, 1, 0, 0, 0]
    assert open_questions([1, 2, 3, 4]) == [0, 0, 0, 0]
    assert open_questions([5, 6, 7, 2, 3, 4, 1, 8]) == [1, 2, 3, 4, 5, 6, 0, 0]


def test_sample_log():
    plot = load_log(os.path.join(HERE, "sample_log.csv"))
    assert plot == [5, 6, 7, 2, 3, 4, 1, 8]
    assert inversions(plot) == 15


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
