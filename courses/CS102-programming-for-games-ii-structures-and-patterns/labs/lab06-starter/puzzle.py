"""CS102 Lab 06 starter: undo/redo with two stacks, and an input buffer with a queue.

Run:  python puzzle.py          (prints a trace of the lecture's move script)
      python test_puzzle.py     (checks your History and InputBuffer work)

Your job (see lab06.md):
  1. Finish History.undo and History.redo (two stacks).
  2. Make History.run clear the redo stack when a new move succeeds.
  3. Finish InputBuffer.press and InputBuffer.finish_move (a bounded queue).
Board and Move are complete. Read Move.do and Move.undo before you start.
"""
from collections import deque

LEVEL = [
    "#######",
    "#.....#",
    "#.@B..#",
    "#.....#",
    "#######",
]


class Board:
    def __init__(self, rows=LEVEL):
        self.walls, self.boxes = set(), set()
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch == "#":
                    self.walls.add((x, y))
                elif ch == "B":
                    self.boxes.add((x, y))
                elif ch == "@":
                    self.player = (x, y)

    def free(self, pos):
        return pos not in self.walls and pos not in self.boxes


class Move:
    """One player step. A command: it can do itself and undo itself."""

    def __init__(self, dx, dy):
        self.dx, self.dy = dx, dy
        self.pushed = False          # filled in by do(), needed by undo()

    def do(self, board):
        px, py = board.player
        ahead = (px + self.dx, py + self.dy)
        if ahead in board.walls:
            return False
        if ahead in board.boxes:
            beyond = (ahead[0] + self.dx, ahead[1] + self.dy)
            if not board.free(beyond):
                return False
            board.boxes.remove(ahead)
            board.boxes.add(beyond)
            self.pushed = True
        else:
            self.pushed = False
        board.player = ahead
        return True

    def undo(self, board):
        px, py = board.player
        if self.pushed:
            box = (px + self.dx, py + self.dy)
            board.boxes.remove(box)
            board.boxes.add((px, py))
        board.player = (px - self.dx, py - self.dy)

    def __repr__(self):
        name = {(1, 0): "R", (-1, 0): "L", (0, 1): "D", (0, -1): "U"}[(self.dx, self.dy)]
        return name + ("*" if self.pushed else "")


class History:
    """Undo and redo with two stacks. limit=None means unlimited undo."""

    def __init__(self, limit=None):
        self.undo_stack = deque(maxlen=limit)   # bounded stack: oldest falls off the bottom
        self.redo_stack = []

    def run(self, cmd, board):
        if cmd.do(board):
            self.undo_stack.append(cmd)
            # TODO 2: a new action ends the old future. What must happen to redo_stack?
            return True
        return False

    def undo(self, board):
        """TODO 1: pop the last command, undo it, and push it on the redo stack.
        Return False (and change nothing) if there is nothing to undo."""
        raise NotImplementedError("History.undo")

    def redo(self, board):
        """TODO 1: pop from the redo stack, do it again, push it back on the undo stack.
        Return False if there is nothing to redo."""
        raise NotImplementedError("History.redo")


class InputBuffer:
    """Key presses that arrive while a move is still playing wait in a queue.

    step_ms  how long one move takes to play
    maxlen   how many presses may wait (None = unlimited, 0 = no buffering)
    When the queue is full, deque(maxlen=...) drops the OLDEST waiting press.
    """

    def __init__(self, step_ms, maxlen=None):
        self.step_ms = step_ms
        self.queue = deque(maxlen=maxlen)
        self.busy_until = 0
        self.starts = []                        # time each executed move started

    def press(self, t):
        """TODO 3: a key is pressed at time t (ms).
        If no move is playing (t >= busy_until) and nothing is waiting, start a move now
        (record t in self.starts, set busy_until). Otherwise append t to the queue."""
        raise NotImplementedError("InputBuffer.press")

    def finish_move(self):
        """TODO 3: the current move ends at busy_until. If a press is waiting,
        remove it from the FRONT of the queue and start the next move at busy_until."""
        raise NotImplementedError("InputBuffer.finish_move")


def simulate_buffer(taps, step_ms, maxlen):
    """Feed sorted key-press times through an InputBuffer. Returns (starts, end_time)."""
    buf = InputBuffer(step_ms, maxlen)
    for t in taps:
        while buf.queue and buf.busy_until <= t:
            buf.finish_move()
        buf.press(t)
    while buf.queue:
        buf.finish_move()
    return buf.starts, buf.busy_until


if __name__ == "__main__":
    b = Board()
    h = History()
    R, L, D, U = (1, 0), (-1, 0), (0, 1), (0, -1)
    script = [("run", R), ("run", R), ("run", D), ("undo", None), ("undo", None),
              ("redo", None), ("run", U)]
    for op, d in script:
        try:
            if op == "run":
                h.run(Move(*d), b)
            else:
                getattr(h, op)(b)
        except NotImplementedError as e:
            print(f"{op:5} TODO: {e}")
            continue
        print(f"{op:5} {str(d):8} player={b.player} boxes={sorted(b.boxes)} undo={list(h.undo_stack)} redo={h.redo_stack}")
    for maxlen in (None, 2, 1, 0):
        try:
            s, end = simulate_buffer([0, 40, 80, 120, 160], 150, maxlen)
            print("maxlen", maxlen, "starts", s, "ends", end, "moves", len(s))
        except NotImplementedError as e:
            print("maxlen", maxlen, "TODO:", e)
