"""Run with:  python test_lab08.py   (from inside lab08-starter/)"""
import jump_input as j


def test_edges_lecture_trace():
    held = [False, True, True, True, False, False, True]
    jp, jr = j.edges(held)
    assert jp == [False, True, False, False, False, False, True], jp
    assert jr == [False, False, False, False, True, False, False], jr


def test_edges_check_yourself():
    jp, jr = j.edges([False, True, False, True, True, False])
    assert jp == [False, True, False, True, False, False]
    assert jr == [False, False, True, False, False, True]


def test_strict_jump_on_ground_only():
    assert j.run_ledge(j.JumpInput(0.0, 0.0), 60, -0.05) is not None   # pressed on ground
    assert j.run_ledge(j.JumpInput(0.0, 0.0), 60, 0.02) is None        # one frame late


def test_coyote_table():
    # last allowed press time for C = 0.1 s at each frame rate
    assert j.run_ledge(j.JumpInput(0.1, 0.1), 30, 0.10) == round(3 / 30, 6)
    assert j.run_ledge(j.JumpInput(0.1, 0.1), 60, 0.10) == round(6 / 60, 6)
    assert j.run_ledge(j.JumpInput(0.1, 0.1), 144, 0.097) == round(14 / 144, 6)
    assert j.run_ledge(j.JumpInput(0.1, 0.1), 144, 0.0975) is None
    for fps in (30, 60, 144):
        assert j.run_ledge(j.JumpInput(0.1, 0.1), fps, 0.15) is None


def test_coyote_examples():
    assert j.run_ledge(j.JumpInput(0.1, 0.1), 30, 0.05) == round(2 / 30, 6)
    assert j.run_ledge(j.JumpInput(0.1, 0.1), 60, 0.05) == round(3 / 60, 6)
    assert j.run_ledge(j.JumpInput(0.1, 0.1), 144, 0.05) == round(8 / 144, 6)


def test_buffer():
    assert j.run_landing(j.JumpInput(0.1, 0.1), 60, -0.05) == 0.0
    assert j.run_landing(j.JumpInput(0.1, 0.0), 60, -0.05) is None
    assert j.run_landing(j.JumpInput(0.1, 0.1), 60, -0.15) is None


def test_one_press_one_jump():
    jumper = j.JumpInput(0.1, 0.1)
    fired = [jumper.update(True, True, 1 / 60) for _ in range(30)]   # hold on the ground
    assert fired.count(True) == 1, fired.count(True)


def test_frames_model_changes_with_fps():
    # 6-frame window: +0.08 s works at 30 and 60 fps, fails at 144 fps
    assert j.run_ledge(j.JumpInputFrames(6, 6), 30, 0.08) is not None
    assert j.run_ledge(j.JumpInputFrames(6, 6), 60, 0.08) is not None
    assert j.run_ledge(j.JumpInputFrames(6, 6), 144, 0.08) is None


def test_approach():
    assert j.approach(0, 90, 1000 / 60) == 1000 / 60
    assert j.approach(85, 90, 1000 / 60) == 90
    assert j.approach(90, 0, 1000 / 60) == 90 - 1000 / 60
    assert j.approach(5, 0, 1000 / 60) == 0
    assert j.approach(-90, 0, 10) == -80


def test_top_speed_frames():
    assert j.frames_to_top_speed(90, 1000, 60) == 6
    assert j.frames_to_top_speed(90, 650, 60) == 9
    assert j.frames_to_top_speed(90, 1000, 144) == 13


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
