"""Run with:  python test_lab09.py   (from inside lab09-starter/)"""
import frame_rates as fr

RATES = fr.FRAME_RATES


def close(a, b, tol):
    return abs(a - b) <= tol


def test_broken_game_really_is_broken():
    xs = []
    for fps in RATES:
        g = fr.BrokenGame()
        for _ in range(fps):
            g.update(1 / fps)
        xs.append(g.x)
    assert xs == [150.0, 300.0, 720.0, 1200.0], xs


def test_run_variable_frame_count():
    class Counter:
        n = 0
        def update(self, dt):
            self.n += 1
    assert fr.run_variable(Counter(), 144, 2).n == 288


def test_position_per_second():
    for fps in RATES:
        g = fr.run_variable(fr.FixedGame(), fps, 1)
        assert close(g.x, 300.0, 1e-6), (fps, g.x)


def test_damping_per_second():
    target = 600 * 0.9 ** 60               # speed left after 1 s at 60 fps
    for fps in RATES:
        g = fr.run_variable(fr.FixedGame(), fps, 1)
        assert close(g.slide, target, 1e-6), (fps, g.slide)


def test_cooldown_in_seconds():
    for fps in RATES:
        g = fr.run_variable(fr.FixedGame(), fps, 3.01)
        assert g.dashes == 2, (fps, g.dashes)
        g = fr.run_variable(fr.FixedGame(), fps, 1.45)
        assert g.dashes == 0, (fps, g.dashes)


def test_accumulate_144():
    rows = fr.accumulate([1 / 144] * 12)
    assert [r[0] for r in rows] == [0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1]
    assert close(rows[2][1], 0.0041667, 1e-6)
    assert close(rows[6][2], 0.9167, 1e-3)


def test_accumulate_50_and_hitch():
    assert [r[0] for r in fr.accumulate([0.02] * 5)] == [1, 1, 1, 1, 2]
    assert [r[0] for r in fr.accumulate([1 / 60, 0.3, 1 / 60])] == [1, 15, 1]
    assert [r[0] for r in fr.accumulate([1 / 60, 0.3], max_frame=1.0)] == [1, 18]


def test_fixed_step_apex_identical():
    apexes = {round(fr.run_fixed(fr.FixedGame(), fps, 1).apex, 6) for fps in RATES}
    assert len(apexes) == 1, apexes
    assert close(apexes.pop(), 76.666667, 1e-3)


def test_variable_step_apex_differs():
    a30 = fr.run_variable(fr.FixedGame(), 30, 1).apex
    a144 = fr.run_variable(fr.FixedGame(), 144, 1).apex
    assert close(a30, 73.33, 0.01) and close(a144, 78.62, 0.01), (a30, a144)


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except NotImplementedError:
            print(f"FAIL  {t.__name__}: not implemented yet")
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e or 'assertion failed'}")
    print(f"\n{passed}/{len(tests)} tests passed")
    raise SystemExit(0 if passed == len(tests) else 1)
