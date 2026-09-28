# CS101 · Lab 11: The game-flow machine

**Week:** 11, game state machines ([lecture](../lectures/w11-game-state-machines.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the weekly exercises (40%). The Godot half becomes the menu and pause system of mini-game 2.

## Objective

Implement two state machines from the lecture in Python and prove them with tests: the Pac-Man-style ghost mode machine, whose clock pauses during frightened mode, and your game's menu, play, pause and game-over machine. Then port the second one to GDScript and wire it to a real pause menu in Godot.

## Starter materials

All in [`lab11-starter/`](lab11-starter/). Standard-library Python 3.10 or later, no packages.

- [`ghosts.py`](lab11-starter/ghosts.py): the schedule, `new_ghost()` and a finished `run()` harness that steps at 1/60 s and logs every mode change. You write `change_mode`, `update` and `eat_power_pellet`.
- [`game_flow.py`](lab11-starter/game_flow.py): a transition table with two of seven rows, `new_game()`, a given per-state `update` and `score_points`. You write `handle` and `on_enter` and finish the table.
- [`test_lab11.py`](lab11-starter/test_lab11.py): ten tests. Five check the ghost schedule against the lecture's tables (within 0.05 s, since per-frame timers land up to a frame late). Five check the flow machine, including the unpause bug, ignored events, and the 1-second input lock on the game-over screen. Run `python test_lab11.py`. On the starter it reports `0/10 tests passed`.

## Steps

1. **Ghost transitions.** Write `change_mode` so it is the only line in the file that assigns `ghost["mode"]`, and apply the reversal rule there. Then write `update` and `eat_power_pellet`. Run `python ghosts.py` and compare its printout with the "without pellet" column of the lecture's table.
2. **The paused clock.** Run `ghosts.run(pellets=[25])` and check the "with pellet" column. Then answer check-yourself question 2 of the lecture by calling `ghosts.run(pellets=[30, 70])`. Record both logs.
3. **A deliberate bug.** In `update`, replace `phase_time -= duration` with `phase_time = 0`. Run `ghosts.run(dt=1/7)` (a very slow frame rate) and compare the time of the last transition with the correct version. Explain the difference in one sentence. Restore the line.
4. **Flow table.** Add the missing five rows to `TRANSITIONS`. Write `handle` and `on_enter` following their docstrings. All ten tests should pass.
5. **Break it on purpose.** Move the score and lives reset into `on_enter` for `PLAY`. Run the tests and copy the failing test's name and message into your notes. Restore it.
6. **Port to Godot.** In your mini-game project, create a `Game` node with a GDScript `enum State { MENU, PLAY, PAUSE, GAME_OVER }` and a `change_state()` function modelled on lecture section 3. Set the `Game` node's process mode to Always and the pause menu's to When Paused. The Escape key toggles pause through `_unhandled_input`. Game over ignores input for 1 second.
7. **Diagram.** Draw the final state diagram of your game, including any states you added (a "get ready" countdown, a high-score entry screen). Mark every enter action and every transition action.

## Deliverable

- `ghosts.py` and `game_flow.py` with `python test_lab11.py` reporting `10/10 tests passed`.
- The two logs from step 2 and your one-sentence explanation from step 3.
- Your Godot project folder (or a zip) with the working pause menu, and a 30-second screen recording showing start, pause, resume, game over, the input lock, and retry.
- A one-page state diagram (photo of paper is fine).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Ghost machine | All five ghost tests pass; one assignment of `mode`; step 3 explained with numbers | Tests pass but reversal logic duplicated, or step 3 vague | Fewer than four ghost tests pass | 25% |
| Flow machine | All five flow tests pass; reset lives in transitions; step 5 failure recorded | Passes but step 5 missing | Fewer than four flow tests pass | 25% |
| Godot port | Enum, `match`, correct process modes; pause, resume and lock all work in the recording | Works with one visible glitch (for example the key does nothing while paused) | Missing or still uses booleans | 30% |
| State diagram | Every state, event, enter action and transition action shown and matches the code | Minor mismatch with the code | Missing | 10% |
| Code quality | Clear names, docstrings kept, no stray flags | Minor issues | Hard to follow | 10% |
