# CS203 · Lab 01: Ghost brains

**Week:** 1, game AI vs academic AI ([lecture](../lectures/w01-game-ai-vs-academic-ai.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the labs (50% of the course).

## Objective

Rebuild the complete decision logic of Pac-Man's four ghosts (target tiles, the greedy turn rule and the scatter and chase schedule) and use a small simulation to measure what their "personalities" do for the game. Then design a fifth ghost and defend it with the five tests from lecture section 3.

## Starter materials

All in [`lab01-starter/`](lab01-starter/). Standard-library Python 3, no packages.

- [`ghosts.py`](lab01-starter/ghosts.py) has five empty functions (`ahead`, `target`, `choose_direction`, `mode_at`, `scatter_seconds`) and a finished maze simulation. The maze is the lattice from the lecture's interactive, 25 × 29 tiles with a wall wherever `x` and `y` are both odd. The published arcade schedules for level 1, levels 2 to 4 and level 5 and up are included as lists.
- [`test_ghosts.py`](lab01-starter/test_ghosts.py) checks your functions against the lecture's numbers: the board with Pac-Man at `(14, 20)`, the facing-up bug, the check-yourself answers, the tie that goes up, the never-reverse rule, and the scatter totals of 19 s, 24 s and 15 s.
- The [interactive](../examples/w01-ghost-targets.html), to spot-check targets and runs.

Run the tests from the starter folder with `python3 test_ghosts.py` (or the course's `.venv/bin/python`). On the starter every test prints `TODO` and the script exits with status 1.

## Steps

1. **`ahead`.** Return the tile `n` steps ahead. Reproduce the facing-up bug when `bug=True`.
2. **`target`.** Implement the four chase targets from the lecture's table. Clyde must compare squared distance with 64. No `sqrt`.
3. **`choose_direction`.** Implement the turn rule: never choose the reverse, pick the smallest squared distance from the next tile to the goal, break ties in the order up, left, down, right, and reverse only at a dead end.
4. **`mode_at` and `scatter_seconds`.** Walk the schedule list. Count scatter frame by frame at 60 Hz. Run the tests until all pass.
5. **Measure.** Run `python3 ghosts.py`. It prints the mean spacing between ghosts and the fraction of chase steps in which all four are bunched, first with personalities and then with every ghost using Blinky's target. A correct solution prints 7.39 tiles and 10% for the first line and 3.66 tiles and 80% for the second. Record both.
6. **Vary the schedule.** Call `simulate(schedule=LEVEL_5_UP)` and `simulate(schedule=[0, 10_000])` (chase only). Add the results to your table. Describe in two sentences what the scatter phases do to the spacing.
7. **Remove the bug.** Change `target` so the simulation can run with `bug=False` (add a parameter to `simulate` if you need to). Does the bug change the spacing on this maze? Report the numbers either way.
8. **Fifth ghost.** Add a fifth ghost with a one-line target rule of your own and a scatter corner. Add it to `simulate` and measure spacing and bunching for all five. Write the rule as a formula in the same notation as the lecture.

## Deliverable

- `ghosts.py` with all tests passing and your fifth ghost added.
- A results table: spacing and bunched fraction for each configuration in steps 5 to 8.
- A design note of at most 300 words. State the experience your fifth ghost is meant to create for the player, score it against the five tests (readable, beatable, varied, cheap, authorable) with one sentence each, and name one situation where it breaks.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Correctness | All provided tests pass; step 5 numbers reproduced exactly | Tests pass, measurements differ without explanation | Tests fail | 30% |
| Measurements | Steps 6 and 7 done with a clear table and a correct reading of what the schedule does | Table present, interpretation thin | Missing or wrong | 20% |
| Fifth ghost design | Rule stated as a formula, implemented, measured, and tied to a named player experience | Implemented but the experience goal is vague | Not implemented | 25% |
| Five-test critique | Each test answered with a mechanism, plus a concrete failure case | Tests answered with opinions rather than mechanisms | Missing | 15% |
| Code quality | Readable, no duplicated target logic, no square roots | Works but repetitive | Hard to follow | 10% |
