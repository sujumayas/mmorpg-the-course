# CS102 · Lab 06: Undo and the input buffer

**Week:** 6 ([Queues and stacks: undo, command buffers](../lectures/w06-queues-and-stacks-undo-and-command-buffers.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** in pairs (one shared repository, both names on the report)

## Objective

Finish a two-stack undo and redo system for a box-pushing puzzle, implement an input buffer as a bounded queue, pass the provided checks, and then use both to make and defend two feel decisions: how deep undo should go and how many presses the buffer should hold.

## Starter materials

- Python 3.10 or later, no packages. (In this repository, `.venv/bin/python`.)
- `labs/lab06-starter/puzzle.py`:
  - `Board` and `Move` are complete. `Move.do` records `pushed`; `Move.undo` uses it.
  - `History` has a working `run`, but it does not clear the redo stack yet, and `undo` and `redo` raise `NotImplementedError`.
  - `InputBuffer.press` and `InputBuffer.finish_move` raise `NotImplementedError`.
  - `simulate_buffer(taps, step_ms, maxlen)` drives an `InputBuffer` and returns `(starts, stop_time)`.
  - Running `python puzzle.py` prints the lecture's trace and the buffer table, with `TODO` where your code is missing.
- `labs/lab06-starter/test_puzzle.py`: six checks, run with `python test_puzzle.py` (no pytest needed). One passes already. All six must pass when you are done.
- Expected buffer results (from lecture, `step_ms = 150`, taps `[0, 40, 80, 120, 160]`): unlimited `[0, 150, 300, 450, 600]` stopping at 750; `maxlen 2` `[0, 150, 300, 450]` / 600; `maxlen 1` `[0, 150, 300]` / 450; `maxlen 0` `[0, 160]` / 310.

## Steps

### Part A: two stacks (30 minutes)

1. Read `Move.do` and `Move.undo`. On paper, trace the lecture script (R, R, D, undo, undo, redo, U) before writing any code.
2. Implement `History.undo` and `History.redo`. Each returns `False` and changes nothing if its stack is empty.
3. Add the redo-clearing rule to `History.run`.
4. Run `python puzzle.py` and compare with the lecture table and your paper trace. Run `python test_puzzle.py`; the four `History` checks must pass.

### Part B: the input buffer (30 minutes)

5. Implement `InputBuffer.press` and `InputBuffer.finish_move` as described in their docstrings. Use `popleft()`, not `pop(0)`.
6. Run `python test_puzzle.py` until all six checks pass.
7. Add a test of your own: `step_ms = 200`, `maxlen = 1`, taps `[0, 50, 100, 250]`. Work out the expected result by hand first. (It is in the lecture's Check yourself.)

### Part C: extend (30 minutes)

8. Add a `drop` parameter to `InputBuffer`: `"oldest"` (the current `deque` behaviour) or `"newest"` (ignore a press when the queue is full). Write one test that gives different results for the two policies.
9. Add a `Checkpoint` feature to `History`: `history.checkpoint(board)` saves a snapshot of the moving parts (player and boxes) and `history.restore(board)` returns to it, once, like Into the Breach's Reset Turn. Decide and document what `restore` does to both stacks.
10. Measure memory. Play 1,000 random legal moves on a 20 × 15 empty level with 6 boxes. Report `len(undo_stack)` and an estimate of stored values for command undo, and compare with snapshotting the full grid every move.

### Part D: feel decisions (at home)

11. Build a quick feel test. Either wire `puzzle.py` to keyboard input (any library you like, or a `input()` loop that accepts several keys per line and treats them as rapid taps), or use the lecture's interactive. Try `maxlen` 0, 1, 2 and unlimited.
12. Write at most 300 words choosing an undo depth and a buffer length for (a) a relaxed puzzle game and (b) a grid-based action game with enemies that move on a timer. Use at least two numbers from your tests and name what each choice costs the player.

## Deliverable

Your completed `puzzle.py` and `test_puzzle.py` (with your added tests), a short report with the paper trace from step 1, the memory numbers from step 10, and the feel decisions from step 12.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Undo and redo (25%) | All `History` checks pass; empty-stack cases return `False`; paper trace matches code | Checks pass, trace missing | Redo not cleared on new action | Does not run |
| Input buffer (20%) | All buffer checks pass; own test for step 7 derived by hand first | Checks pass, own test missing | `pop(0)` used or one case wrong | Missing |
| Extensions (25%) | Drop policy with a discriminating test; checkpoint with a documented rule for both stacks | Both present, one untested or undocumented | One of the two | Missing |
| Memory measurement (10%) | Counts for command and snapshot undo with the ratio | Counts without ratio | Estimate only | Missing |
| Feel decisions (20%) | Two contexts, two numbers each, costs named for each choice | Decisions with numbers, costs vague | No numbers | Missing |
