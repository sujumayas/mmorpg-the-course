"""Checks for Lab 11. Run from inside lab11-starter/:  ../../../../.venv/bin/python test_lab11.py
Every check fails on the starter and passes on a correct solution."""
import polls as m

passed = failed = 0


def check(name, fn):
    global passed, failed
    try:
        fn()
        passed += 1
        print("PASS", name)
    except Exception as e:  # noqa: BLE001
        failed += 1
        print("FAIL", name, "-", type(e).__name__, e)


def t_share():
    assert abs(m.yes_share(112_976, 44_153) - 0.719) < 0.0005
    assert abs(m.yes_share(82_633, 41_726) - 0.664) < 0.0005


def t_passes():
    assert m.passes(112_976, 44_153, 70) is True
    assert m.passes(112_976, 44_153, 75) is False
    assert m.passes(70, 30, 70) is True    # exactly on the line passes
    assert m.passes(69, 31, 70) is False


def t_block():
    assert m.no_votes_to_block(112_976, 70) == 48_419
    assert m.no_votes_to_block(112_976, 75) == 37_659
    assert m.no_votes_to_block(70, 70) == 31  # 70 yes / 30 no passes, 31 no fails


def t_archive_counts():
    rows = m.read_polls()
    assert len(rows) == 3304
    assert m.pass_count(rows, 75) == 2681
    assert m.pass_count(rows, 70) == 2879


def t_flipped_by_era():
    rows = m.read_polls()
    before = m.in_period(rows, end=m.CHANGE_DATE)
    after = m.in_period(rows, start=m.CHANGE_DATE)
    assert len(m.flipped(before, 70, 75)) == 177
    flipped_after = m.flipped(after, 70, 75)
    assert len(flipped_after) == 21
    assert any("Sailing" in r["question"] for r in flipped_after)


for name, fn in [("yes share excludes skips", t_share), ("pass rule with integer maths", t_passes),
                 ("blocking 'no' count", t_block), ("archive pass counts", t_archive_counts),
                 ("questions flipped by the 2022 change", t_flipped_by_era)]:
    check(name, fn)
print(f"{passed} passed, {failed} failed")
raise SystemExit(1 if failed else 0)
