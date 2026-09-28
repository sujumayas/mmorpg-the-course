"""Tests for CS101 Lab 12. Run:  python test_lab12.py

The first four tests describe behavior that already works. Keep them passing.
The three test_bug_* tests are yours to write (lab steps 2-4). Each must FAIL on the
starter code and PASS after your fix. Replace the NotImplementedError line in each.
"""
import asteroids_sim as s


def test_real_overlap_hits():
    ship = {"x": 150, "y": 110, "w": 20, "h": 20}
    assert s.overlap({"x": 140, "y": 100, "w": 16, "h": 16}, ship)


def test_far_rock_misses():
    ship = {"x": 150, "y": 110, "w": 20, "h": 20}
    assert not s.overlap({"x": 10, "y": 10, "w": 16, "h": 16}, ship)


def test_seed_is_deterministic():
    a, b = s.run(7, 600), s.run(7, 600)
    assert (a["lives"], a["score"], a["wave"]) == (b["lives"], b["score"], b["wave"])


def test_start_resets_score():
    g = s.new_game()
    s.handle_event(g, "start")
    g["score"] = 900
    s.handle_event(g, "out_of_lives")
    s.handle_event(g, "retry")
    assert g["score"] == 0


def test_bug_1_grazing_rocks():
    """Report 1: rocks skimming the top of the ship hit it; rocks skimming the bottom never do."""
    raise NotImplementedError("TODO: write a minimal failing test")


def test_bug_2_pause_refills_lives():
    """Report 2: pausing and resuming refills lives."""
    raise NotImplementedError("TODO: write a minimal failing test")


def test_bug_3_wave_256_is_easy():
    """Report 3: after wave 255 the game suddenly spawns only 3 rocks."""
    raise NotImplementedError("TODO: write a minimal failing test")


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
