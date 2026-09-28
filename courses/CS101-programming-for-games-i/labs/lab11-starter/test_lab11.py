"""Tests for CS101 Lab 11. Run:  python test_lab11.py"""
import ghosts
import game_flow as gf


def close(a, b):
    return abs(a - b) <= 0.05   # within a few frames at 60 fps


def test_schedule_no_pellet():
    log = ghosts.run(until=90)
    times = [t for t, _, _ in log]
    want = [7, 27, 34, 54, 59, 79, 84]
    assert len(times) == 7 and all(close(a, b) for a, b in zip(times, want)), times
    assert log[-1][2] == 7


def test_pellet_shifts_schedule():
    log = ghosts.run(pellets=[25], until=91)
    times = [t for t, _, _ in log]
    want = [7, 25, 31, 33, 40, 60, 65, 85, 90]
    assert len(times) == 9 and all(close(a, b) for a, b in zip(times, want)), times
    assert log[-1][2] == 8, log[-1]


def test_no_reversal_leaving_frightened():
    log = ghosts.run(pellets=[25], until=32)
    fright_end = [row for row in log if close(row[0], 31)][0]
    before = [row for row in log if close(row[0], 25)][0]
    assert fright_end[1] == "chase" and fright_end[2] == before[2], log


def test_two_pellets_endless_chase():
    log = ghosts.run(pellets=[30, 70], until=100)
    assert close(log[-1][0], 96) and log[-1][1] == "chase", log[-1]


def test_pellet_while_frightened():
    g = ghosts.new_ghost()
    ghosts.eat_power_pellet(g, 6.0)
    r = g["reversals"]
    ghosts.update(g, 3.0)
    ghosts.eat_power_pellet(g, 6.0)
    assert g["reversals"] == r and g["fright_left"] == 6.0


def test_flow_happy_path():
    g = gf.new_game()
    assert gf.handle(g, "start") and g["state"] == "PLAY" and g["clock_running"]
    assert gf.handle(g, "pause") and g["state"] == "PAUSE" and not g["clock_running"]
    assert gf.handle(g, "resume") and g["state"] == "PLAY"
    assert gf.handle(g, "out_of_lives") and g["state"] == "GAME_OVER"
    assert gf.handle(g, "quit") and g["state"] == "MENU"


def test_ignored_events():
    g = gf.new_game()
    assert gf.handle(g, "pause") is False and g["state"] == "MENU"
    assert gf.handle(g, "resume") is False
    gf.handle(g, "start")
    assert gf.handle(g, "retry") is False and g["state"] == "PLAY"


def test_unpause_keeps_score():
    g = gf.new_game()
    gf.handle(g, "start")
    gf.score_points(g, 500)
    g["lives"] = 1
    gf.handle(g, "pause")
    gf.handle(g, "resume")
    assert g["score"] == 500 and g["lives"] == 1, g


def test_game_over_lock_and_retry():
    g = gf.new_game()
    gf.handle(g, "start")
    gf.score_points(g, 300)
    gf.handle(g, "out_of_lives")
    assert g["high_score"] == 300
    gf.update(g, 0.5)
    assert gf.handle(g, "retry") is False, "retry must be ignored during the 1 s lock"
    gf.update(g, 0.6)
    assert gf.handle(g, "retry") and g["score"] == 0 and g["lives"] == 3


def test_paused_clock_stops_play_time():
    g = gf.new_game()
    gf.handle(g, "start")
    gf.update(g, 2.0)
    gf.handle(g, "pause")
    gf.update(g, 5.0)
    assert g["play_time"] == 2.0


TESTS = [v for k, v in dict(globals()).items() if k.startswith("test_")]

if __name__ == "__main__":
    passed = 0
    for t in TESTS:
        try:
            t()
            print("PASS", t.__name__)
            passed += 1
        except NotImplementedError:
            print("TODO", t.__name__)
        except AssertionError as e:
            print("FAIL", t.__name__, e)
        except Exception as e:
            print("ERROR", t.__name__, type(e).__name__, e)
    print(f"{passed}/{len(TESTS)} tests passed")
