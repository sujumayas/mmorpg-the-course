# CS101 · Lab 09: One game, every frame rate

**Week:** 9, delta time and frame-rate independence ([lecture](../lectures/w09-delta-time-and-frame-rate-independence.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the weekly exercises (40%). Mini-game 1 is graded at 30 and 144 fps, so this lab is your insurance.

## Objective

Take a game update that was only ever tested at 60 fps, prove with a test harness that it is four different games at four frame rates, fix it line by line, and then show that a fixed-timestep accumulator makes even the jump identical on every machine.

## Starter materials

All in [`lab09-starter/`](lab09-starter/). Standard-library Python 3.10 or later, no packages.

- [`frame_rates.py`](lab09-starter/frame_rates.py). Part A, `BrokenGame`, has one `update(dt)` with four frame-rate bugs: movement per frame, damping per frame, a cooldown counted in frames, and a jump integrated with variable `dt`. Every comment says what the author *meant*. Part B has four things for you to write: `FixedGame.update`, `run_variable`, `accumulate` and `run_fixed`. Part C prints a table comparing the broken game, your fixed game with variable `dt`, and your fixed game driven by the accumulator.
- [`test_lab09.py`](lab09-starter/test_lab09.py): nine tests. Run `python test_lab09.py`. On the starter it reports `1/9 tests passed`. The one that passes proves the broken game really is broken.
- Godot 4.x for step 7.

## Steps

1. **Predict.** Before writing code, fill in a table by hand: for `BrokenGame` after 1 second at 30, 60, 144 and 240 fps, predict `x`, how many dashes happened in 3 seconds, and whether the knock-back fades faster or slower than at 60 fps. Use the lecture's model (`speed = s × fps`).
2. **Runner.** Write `run_variable`. Run `test_broken_game_really_is_broken` and `test_run_variable_frame_count`.
3. **Fix movement and the cooldown.** In `FixedGame`, move by `300 * dt`. Store the cooldown as 1.5 seconds and subtract `dt`. When it runs out, *add* 1.5 rather than setting it to 1.5, so the leftover fraction of a frame is not lost. Explain in one sentence what drift the "set to 1.5" version causes over a long session.
4. **Fix the damping.** Replace `slide *= 0.9` with the power form from the lecture. `test_damping_per_second` checks that the speed left after one second matches the 60 fps original at every frame rate.
5. **Look closely at `slide_x`.** Run Part C. Your fixed game's knock-back *speed* now fades identically, yet the *distance* it pushes the player (`slide_x`) still differs between 30 and 240 fps. Write two or three sentences explaining why, using the idea of integration error from lecture section 3.
6. **Accumulator.** Write `accumulate`, then `run_fixed` using it. Make `test_accumulate_144`, `test_accumulate_50_and_hitch` and `test_fixed_step_apex_identical` pass. In Part C's last column the apex should read 76.67 at every frame rate. Check that `slide_x` in fixed-step mode is identical across frame rates too, and add a column for it.
7. **Engine check.** In Godot, put a jump with `v0 = 400` and gravity 1000 in `_process` (variable `dt`) on one `Node2D` and in `_physics_process` on another, each recording its maximum height. Run with Max FPS set to 30 and then to 144 (vsync off). Record four apex heights and compare with your Python columns.
8. **Hunt in your own code.** Open your mini-game project and search for every `+=`, `-=` and `*=` in `_process` or `_physics_process`. Classify each line as correct, needs `dt`, needs a power, or belongs in the fixed step. List at least five lines with their classification.

## Deliverable

Your edited `frame_rates.py` with `python test_lab09.py` reporting `9/9 tests passed`, and a note of at most 400 words containing: your step 1 predictions next to the actual values, the step 3 sentence, the step 5 explanation, Part C's output with the added `slide_x` column, your four Godot apex heights, and the step 8 list.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tests pass | 9/9 | 6-8 | 5 or fewer | 30% |
| Predictions | All four `x` values and dash counts predicted correctly from the model before running | Most correct, or corrected afterwards with a reason | Missing | 10% |
| Explanations (steps 3 and 5) | Names the lost remainder and the integration error precisely, with a number from the output | Right idea, no numbers | Wrong or missing | 20% |
| Accumulator and fixed-step results | Identical apex and `slide_x` across rates, clamp behaviour matches the lecture's hitch numbers | Apex identical, other parts incomplete | Missing | 20% |
| Godot comparison | Four heights recorded and matched to the Python columns within 0.1 px, or differences explained | Recorded, not compared | Missing | 10% |
| Own-code audit | Five or more lines, each classification correct and fixed | Fewer lines or some misclassified | Missing | 10% |
