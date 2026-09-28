"""Tests for CS101 Lab 10. Run:  python test_lab10.py
Prints each test's result and a final 'N/M tests passed' line."""
import collision as c

P = {"x": 100, "y": 100, "w": 32, "h": 48}
A = {"x": 120, "y": 130, "w": 32, "h": 32}
B = {"x": 140, "y": 110, "w": 32, "h": 32}
C = {"x": 132, "y": 100, "w": 32, "h": 32}
D = {"x": 60, "y": 60, "w": 32, "h": 32}
E = {"x": 90, "y": 140, "w": 60, "h": 8}


def test_lecture_table():
    got = [c.aabb_overlap(P, box) for box in (A, B, C, D, E)]
    assert got == [True, False, False, False, True], got


def test_symmetric():
    for box in (A, B, C, D, E):
        assert c.aabb_overlap(P, box) == c.aabb_overlap(box, P)


def test_plus_sign():
    tall = {"x": 110, "y": 80, "w": 10, "h": 90}
    wide = {"x": 90, "y": 110, "w": 60, "h": 20}
    assert c.aabb_overlap(tall, wide)


def test_circles():
    coin = {"cx": 200, "cy": 100, "r": 8}
    assert not c.circle_overlap({"cx": 180, "cy": 115, "r": 16}, coin)
    assert c.circle_overlap({"cx": 182, "cy": 114, "r": 16}, coin)
    assert not c.circle_overlap({"cx": 0, "cy": 0, "r": 10}, {"cx": 18, "cy": 16, "r": 14})


def test_circle_box():
    assert not c.circle_box_overlap({"cx": 135, "cy": 151, "r": 4}, P)
    assert c.circle_box_overlap({"cx": 134, "cy": 150, "r": 4}, P)
    assert c.circle_box_overlap({"cx": 116, "cy": 124, "r": 2}, P)  # center inside


def test_depth():
    assert c.overlap_depth(P, A) == (12, 18)
    assert c.overlap_depth(P, E) == (32, 8)


def test_push_out():
    moved = c.push_out(P, A)
    assert moved == {"x": 88, "y": 100, "w": 32, "h": 48}, moved
    assert P["x"] == 100, "push_out must not modify its input"
    assert not c.aabb_overlap(moved, A)
    up = c.push_out(P, E)
    assert up["y"] == 92 and up["x"] == 100, up
    assert c.push_out(P, B) == P


def test_tunneling():
    assert c.bullet_hits_wall(900, 60) is not None
    assert c.bullet_hits_wall(900, 30) is None
    assert c.bullet_hits_wall(900, 30, substeps=4) is not None


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
