# CS101 · Lab 08: Input you can trust

**Week:** 8, input handling and movement ([lecture](../lectures/w08-input-handling-and-movement.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the weekly exercises (40%). Your jump code carries into mini-game 1.

## Objective

Write the lecture's input model as testable Python, replay 60 recorded jump attempts through it, and measure how many a strict jump throws away. Then show, with numbers, why forgiveness windows must be stored in seconds and not frames, and tune a jump in Godot that a classmate can't break.

## Starter materials

All in [`lab08-starter/`](lab08-starter/). Standard-library Python 3.10 or later, no packages.

- [`jump_input.py`](lab08-starter/jump_input.py). Part A has five things for you to write: `edges`, the `JumpInput` class (timers in seconds), the `JumpInputFrames` class (timers in frames), `approach`, and `frames_to_top_speed`. Part B, done for you, has two scenario runners. `run_ledge` replays a press relative to running off a ledge. `run_landing` replays a press relative to landing. Part C prints the success count for a strict jump and a forgiving one.
- [`attempts.csv`](lab08-starter/attempts.csv): 60 recorded attempts from a playtest. Rows 1 to 40 are "jump at the last moment off the ledge" (`press_offset_s` is seconds after leaving the ground, negative if the player pressed while still on it). Rows 41 to 60 are "jump again as soon as you land" (seconds relative to landing, negative means early).
- [`test_lab08.py`](lab08-starter/test_lab08.py): ten tests taken from the lecture's tables and check-yourself answers. Run `python test_lab08.py`. On the starter it reports `0/10 tests passed`.
- Godot 4.x and any scene with a `CharacterBody2D`, floor, a ledge and a gap, for steps 6 and 7.

## Steps

1. **Edges.** Write `edges(held)`. Check it against the lecture's seven-frame trace before running the test.
2. **Two timers in seconds.** Write `JumpInput.update` exactly as the lecture's model. `test_one_press_one_jump` holds the key on the ground for 30 frames and expects one jump, not thirty. If you get thirty, you are jumping on `held`.
3. **The same model in frames.** Write `JumpInputFrames.update`. It is the same code with the timers counting frames. `test_frames_model_changes_with_fps` should now pass, and it is the bug from the lecture's second table.
4. **Replay the playtest.** Run `python jump_input.py`. Record how many of the 60 attempts jump with the strict rule (`C = B = 0`) and with `C = B = 0.1` s. Then write a loop that tries `C` and `B` from 0 to 0.2 s in steps of 0.02 and prints a small table of success counts. Find the pair with the smallest sum `C + B` that saves at least 55 attempts.
5. **Frame rate audit.** Replay all 60 attempts with `JumpInput(0.1, 0.1)` and with `JumpInputFrames(6, 6)` at 30, 60 and 144 fps. Put the six success counts in a table. One model's row should be nearly flat (it may move by one attempt, because a press can only be seen on a frame boundary) and the other's should swing by more than 20 attempts. Explain which is which and why in two sentences.
6. **Acceleration.** Write `approach` and `frames_to_top_speed`. In Godot, implement the lecture's `CharacterBody2D` script with Celeste's numbers. Measure how many physics frames it takes to reach 90 px/s by printing `velocity.x` each tick, and compare with your Python.
7. **Tune and defend.** In Godot, add your two-timer jump with the `C` and `B` from step 4. Swap laptops with another pair. They get five minutes to find a case where your jump feels wrong (a jump from thin air, a lost press, a double jump from one press). Fix what they find or explain why it's intended.

## Deliverable

Your edited `jump_input.py` with `python test_lab08.py` reporting `10/10 tests passed`, your step 4 and 5 code, and a note of at most 300 words containing: the two counts from step 4 and your chosen `C` and `B`, the six-cell table from step 5 with the two-sentence explanation, the measured and predicted frames from step 6, and what the other pair found in step 7 and what you did about it.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tests pass | 10/10 | 7-9 | 6 or fewer | 30% |
| Playtest replay and tuning | Sweep table correct; chosen `C` and `B` have the smallest sum that saves 55, justified | Counts correct, choice not justified | Replay missing or wrong | 20% |
| Frame rate audit | Six counts correct; explanation names seconds versus frames and the `frames / fps` relationship | Counts correct, explanation vague | Missing | 20% |
| Godot acceleration check | Measured frames match Python, or the difference is explained (for example, first tick timing) | Measured, no comparison | Missing | 15% |
| Peer test | Specific failure found or ruled out, with a fix or a design reason | Generic comment | Missing | 15% |
