"""AU101 Lab 13 tests. Do not edit.

    .venv/bin/python courses/AU101-audio-for-games/labs/lab13-starter/test_subtitles.py [path/to/your_module.py]

With no argument the tests load subtitles.py from this folder. Each test prints
PASS, FAIL or TODO. The script exits with status 1 unless every test passes.
"""
import importlib.util
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
target = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "subtitles.py"
spec = importlib.util.spec_from_file_location("subtitles_under_test", target)
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


def test_required_duration():
    assert close(s.required_duration(48, 17, 1.0), 48 / 17)
    assert close(s.required_duration(8, 17, 1.0), 1.0), "short lines use d_min"
    assert close(s.required_duration(56, 20, 1.0), 2.8)


def test_unread_fraction():
    assert close(s.unread_fraction(56, 2.3, 17), 0.3018)
    assert close(s.unread_fraction(48, 2.2, 17), 0.2208)
    assert close(s.unread_fraction(20, 1.2, 17), 0.0), "never negative"


def test_time_line():
    t = s.time_line("The bridge is out. We cross at the mill instead.", 2.2, 0.4, 17, 1.0)
    assert t["n"] == 48
    assert close(t["cps"], 21.818)
    assert close(t["hold"], 0.6235)
    assert t["fits"] is False
    assert t["n_max"] == 44
    t = s.time_line("The bridge is out. We cross at the mill instead.", 2.2, 0.4, 20, 1.0)
    assert close(t["hold"], 0.2) and t["fits"] is True
    t = s.time_line("Grenade!", 0.5, 0.3, 17, 1.0)
    assert close(t["hold"], 0.5) and t["fits"] is False, "d_min pushes the hold past the gap"
    t = s.time_line("Behind you!", 0.6, float("inf"), 17, 1.0)
    assert t["fits"] is True and t["n_max"] is None


def test_wrap():
    rows = s.wrap("All units, the convoy leaves at dawn. Anyone not on it stays behind.")
    assert rows == ["All units, the convoy leaves at dawn.", "Anyone not on it stays behind."], rows
    assert all(len(r) <= 42 for r in s.wrap("word " * 30))
    assert s.wrap("a" * 50) == ["a" * 50], "an overlong word gets its own row"
    assert s.needs_split("It held last winter, and the winter before that, "
                         "and nobody on this crew fixed it then either.") is True
    assert s.needs_split("Keep your head down.") is False


def test_bearing_and_arrows():
    o = (0.0, 0.0)
    assert close(s.relative_bearing(o, 0, (3, 4)), 36.870)
    assert close(s.relative_bearing(o, 90, (3, 4)), -53.130)
    assert close(s.relative_bearing(o, 0, (0, -1)), 180.0), "straight behind is +180, not -180"
    assert close(s.relative_bearing(o, 350, (1, 0)), 100.0), "wrap across north"
    assert s.cue_arrow(o, 0, (3, 4)) == ""
    assert s.cue_arrow(o, 0, (-5, 1)) == "<"
    assert s.cue_arrow(o, 0, (6, 2)) == ">"
    assert s.cue_arrow(o, 0, (4, -5)) == "v"
    assert s.cue_arrow(o, 90, (3, 4)) == "<"


def test_sector():
    assert s.sector(36.87) == 1
    assert s.sector(-78.69) == 6
    assert s.sector(180.0) == 4
    assert s.sector(-10.0, k=4) == 0


def test_report_runs():
    s.report(HERE / "dialogue.csv", 17, 1.0)


TESTS = [test_required_duration, test_unread_fraction, test_time_line, test_wrap,
         test_bearing_and_arrows, test_sector, test_report_runs]

if __name__ == "__main__":
    failed = 0
    for t in TESTS:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except NotImplementedError:
            failed += 1
            print(f"TODO  {t.__name__}")
        except Exception:
            failed += 1
            print(f"FAIL  {t.__name__}")
            traceback.print_exc(limit=1)
    print(f"{len(TESTS) - failed}/{len(TESTS)} passed")
    sys.exit(1 if failed else 0)
