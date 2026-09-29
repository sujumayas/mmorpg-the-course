"""Tests for MMO406 Lab 06. Values come from the week 6 lecture and lab06.md.
Run with `.venv/bin/python test_myth.py` (from any folder) or pytest."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from myth import audit, classify_row, load_matrix, outcomes, summary  # noqa: E402

TOL = 1e-9


def test_lecture_table():
    expected = {2: (0.16, 0.0, 0.84), 3: (0.256, 0.096, 0.648), 6: (0.233472, 0.533248, 0.23328)}
    for k, (s, a, u) in expected.items():
        got = outcomes(k, 0.4, 0.2)
        assert abs(got[0] - s) < 1e-4 and abs(got[1] - a) < 1e-4 and abs(got[2] - u) < 1e-4
    assert outcomes(1, 0.4, 0.2)[1] >= 0.0


def test_shares_sum_to_one():
    for k in range(1, 9):
        for p, q in [(0.4, 0.2), (0.3, 0.3), (0.7, 0.1), (0.1, 0.0)]:
            assert abs(sum(outcomes(k, p, q)) - 1) < TOL


def test_check_yourself_two_accounts():
    s, a, u = outcomes(2, 0.5, 0.1)
    assert abs(s - 0.25) < TOL and abs(a) < TOL and abs(u - 0.75) < TOL


def test_classify_row():
    assert classify_row(["T", "T", ""]) == "settled"
    assert classify_row(["T", "T", "D:x"]) == "answerable"
    assert classify_row(["T", "", "D:x"]) == "unrecoverable"
    assert classify_row(["", "", ""]) == "unrecoverable"
    assert classify_row(["T", "D:x", "D:x"]) == "false_consensus"
    assert classify_row(["T", "T", "D:x", "D:y"]) == "answerable"


def test_sample_as_written():
    rows, accounts = load_matrix(os.path.join(HERE, "sample_matrix.csv"))
    assert summary(audit(rows, accounts)) == {
        "settled": 2, "answerable": 2, "unrecoverable": 2, "false_consensus": 2}


def test_sample_with_copy_removed():
    rows, accounts = load_matrix(os.path.join(HERE, "sample_matrix.csv"))
    classes = audit(rows, accounts, {"codex_translation": "temple_codex"})
    assert classes["F02 the god wept for seven days"] == "unrecoverable"
    assert classes["F03 the old capital sank in one night"] == "answerable"
    assert classes["F06 the god's name was taken from him"] == "unrecoverable"
    assert summary(classes) == {
        "settled": 2, "answerable": 2, "unrecoverable": 4, "false_consensus": 0}
    assert len(rows[0]) == 5  # audit must not drop columns from the caller's rows


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
