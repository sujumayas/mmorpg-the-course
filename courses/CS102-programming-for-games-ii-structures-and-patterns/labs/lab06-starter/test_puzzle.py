"""CS102 Lab 06 checks. Run: python test_puzzle.py  (no pytest needed)."""
from puzzle import Board, Move, History, simulate_buffer

R, L, D, U = (1, 0), (-1, 0), (0, 1), (0, -1)


def snapshot(b):
    return b.player, frozenset(b.boxes)


def test_undo_restores_push():
    b, h = Board(), History()
    start = snapshot(b)
    assert h.run(Move(*R), b)                     # pushes the box
    assert h.undo(b)
    assert snapshot(b) == start, "undo must pull the box back too"


def test_undo_redo_round_trip():
    b, h = Board(), History()
    states = [snapshot(b)]
    for d in (R, R, D, L):
        h.run(Move(*d), b)
        states.append(snapshot(b))
    for i in range(4):
        h.undo(b)
        assert snapshot(b) == states[-2 - i]
    assert not h.undo(b), "nothing left to undo"
    for i in range(4):
        h.redo(b)
        assert snapshot(b) == states[i + 1]
    assert not h.redo(b)


def test_new_move_clears_redo():
    b, h = Board(), History()
    h.run(Move(*R), b)
    h.run(Move(*D), b)
    h.undo(b)
    assert len(h.redo_stack) == 1
    h.run(Move(*U), b)
    assert h.redo_stack == [], "a new move must clear the redo stack"


def test_blocked_move_not_recorded():
    b, h = Board(), History()
    for _ in range(3):
        h.run(Move(*U), b)                        # wall after one step
    assert len(h.undo_stack) == 1


def test_bounded_history():
    b, h = Board(), History(limit=3)
    for d in (D, L, U, U):                        # seven moves in total, only the last 3 are kept
        h.run(Move(*d), b)
    for d in (R, D, D):
        h.run(Move(*d), b)
    assert len(h.undo_stack) == 3
    while h.undo(b):
        pass
    assert len(h.redo_stack) == 3


def test_input_buffer_lecture_numbers():
    taps = [0, 40, 80, 120, 160]
    assert simulate_buffer(taps, 150, None) == ([0, 150, 300, 450, 600], 750)
    assert simulate_buffer(taps, 150, 2) == ([0, 150, 300, 450], 600)
    assert simulate_buffer(taps, 150, 1) == ([0, 150, 300], 450)
    assert simulate_buffer(taps, 150, 0) == ([0, 160], 310)


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print("PASS", name)
            except NotImplementedError as e:
                failed += 1
                print("TODO", name, "-", e)
            except AssertionError as e:
                failed += 1
                print("FAIL", name, "-", e)
    print(f"{failed} of the checks still to do" if failed else "all checks pass")
