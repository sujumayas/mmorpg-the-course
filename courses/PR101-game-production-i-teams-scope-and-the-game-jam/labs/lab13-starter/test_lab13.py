"""PR101 lab 13 tests. Run: python test_lab13.py

Plain asserts, no packages. Each test prints PASS or FAIL with a reason.
"""
import shutil
import tempfile
from pathlib import Path

import release_check as R

HERE = Path(__file__).resolve().parent
SAMPLE = HERE / "sample_build"


def test_parse_valid():
    assert R.parse_version("1.2.3") == (1, 2, 3, ()), R.parse_version("1.2.3")
    assert R.parse_version(" 0.10.0\n") == (0, 10, 0, ()), "whitespace not stripped"
    assert R.parse_version("1.0.0-rc.10+a3f9c21") == (1, 0, 0, ("rc", 10)), \
        R.parse_version("1.0.0-rc.10+a3f9c21")
    assert R.parse_version("2.0.0+build.7") == (2, 0, 0, ()), "build metadata must be ignored"


def test_parse_invalid():
    for bad in ["1.0", "v1.0.0", "1.0.0-", "a.b.c", "1.02.0", "1.0.0.0", ""]:
        try:
            R.parse_version(bad)
        except ValueError:
            continue
        raise AssertionError(f"{bad!r} should raise ValueError")


def test_is_newer():
    cases = [("1.0.0", "0.9.2", True), ("0.9.2", "0.9.2", False), ("0.9.10", "0.9.9", True),
             ("1.0.0", "1.0.0-rc.2", True), ("1.0.0-rc.2", "1.0.0", False),
             ("1.0.0-rc.10", "1.0.0-rc.2", True), ("1.0.0-rc.2", "1.0.0-rc.10", False),
             ("0.9.3", "1.0.0-rc.1", False)]
    for new, old, want in cases:
        got = R.is_newer(new, old)
        assert got is want, f"is_newer({new!r}, {old!r}) returned {got}, expected {want}"


def test_debug_flags():
    text = "[debug]\nshow_fps=true\ngod_mode = False\n; level_skip=true\nverbose_log= YES\nlevel_skip=0\n"
    assert R.debug_flags_on(text) == ["show_fps", "verbose_log"], R.debug_flags_on(text)
    assert R.debug_flags_on("[display]\nvsync=true\n") == [], "vsync is not a debug key"


def test_missing_files():
    manifest = "# comment\nassets/sprites/player.png\n\nassets/music/boss.ogg\nassets/music/title.ogg\n"
    got = R.missing_files(SAMPLE, manifest)
    assert got == ["assets/music/boss.ogg"], got


def test_changelog():
    log = "# Changelog\n\n## 1.0.0\n- Release.\n\n## 0.9.2\n- Fix.\n"
    assert R.changelog_has(log, "1.0.0") is True
    assert R.changelog_has(log, "0.9.2") is True
    assert R.changelog_has(log, "1.0.1") is False, "found a version that is not there"
    assert R.changelog_has("### 1.0.1\n", "1.0.1") is False, "heading level must be ##"


def test_release_risk():
    # Lecture section 2: N = 20, p = 3%.
    none = R.release_risk([0.03] * 20, [0.0] * 20)
    full = R.release_risk([0.03] * 20, [0.9] * 20)
    half = R.release_risk([0.03] * 20, [0.9] * 10 + [0.0] * 10)
    assert abs(none - 0.5438) < 1e-3, none
    assert abs(full - 0.9417) < 1e-3, full
    assert abs(half - 0.7156) < 1e-3, half


def test_sample_build_fails_everything():
    results = {name: ok for name, ok, _ in R.run_checks(SAMPLE)}
    failing = sorted(name for name, ok in results.items() if not ok)
    assert failing == sorted(results), f"sample build should fail all 5 checks, fails only {failing}"


def test_fixed_build_passes():
    with tempfile.TemporaryDirectory() as tmp:
        build = Path(tmp) / "build"
        shutil.copytree(SAMPLE, build)
        (build / "version.txt").write_text("1.0.0-rc.1\n")
        log = (build / "CHANGELOG.md").read_text()
        (build / "CHANGELOG.md").write_text(log.replace("## 0.9.2", "## 1.0.0-rc.1\n- Final level.\n\n## 0.9.2", 1))
        cfg = (build / "settings.cfg").read_text()
        (build / "settings.cfg").write_text(cfg.replace("show_fps=true", "show_fps=false"))
        (build / "assets/music/boss.ogg").write_text("ogg")
        results = R.run_checks(build)
        bad = [(n, d) for n, ok, d in results if not ok]
        assert not bad, f"fixed build still fails: {bad}"


TESTS = [v for k, v in dict(globals()).items() if k.startswith("test_")]

if __name__ == "__main__":
    passed = 0
    for t in TESTS:
        try:
            t()
            print(f"PASS {t.__name__}")
            passed += 1
        except Exception as err:  # report and keep going
            print(f"FAIL {t.__name__}: {type(err).__name__}: {err}")
    print(f"{passed}/{len(TESTS)} tests passed")
    raise SystemExit(0 if passed == len(TESTS) else 1)
