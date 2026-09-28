# MA101 · Lab 12: A movement controller you can trust

Assigned in week 12 ([lecture](../lectures/w12-2d-vectors.md)). Due at the start of week 13. Counts toward the problem-set grade.

## Objective

Build a small 2D vector toolkit and a top-down movement controller. Measure the controller's speed in every direction, reproduce the diagonal movement bug, and fix it two ways: normalizing for keys and clamping the length for sticks. Your `Vec2` class carries into Lab 13's guard vision work.

## Starter materials

- [`starter/lab12_starter.py`](starter/lab12_starter.py). Python 3, standard library only. It defines an empty `Vec2` class and a `Controller` class with a `speed` field and an empty `velocity(input_vec, mode)` method, where `mode` is `"raw"`, `"normalize"` or `"clamp"`.
- [`starter/test_lab12.py`](starter/test_lab12.py): checks for the vector operations and the lecture's movement table.
- [`starter/stick_log.csv`](starter/stick_log.csv): 500 gamepad samples 0.02 s apart, columns `t, x, y`. The player walks slowly for 3 s (stick length 0.30 to 0.40), pushes to full tilt, then sprints in circles on a square gate. Most sprint samples away from the axes have length above 1, up to about 1.37.
- The week 12 interactive, [`examples/w12-diagonal-movement.html`](../examples/w12-diagonal-movement.html).

## Steps

1. **Vec2.** Implement `+`, `-`, scalar `*`, `length()` and `normalized()`. `normalized()` must return `Vec2(0, 0)` for vectors shorter than `1e-9`, never `NaN`. Tests include `(3, 4)` → length 5, normalized `(0.6, 0.8)`, and `(0, 0)` → `(0, 0)`.
2. **Controller.** Implement `velocity` for the three modes. `raw` is `speed × input`. `normalize` is `speed × input.normalized()`. `clamp` shrinks input to length 1 only when it is longer. Tests use the lecture's table with `speed = 5`.
3. **Speed by direction, keyboard.** Enumerate all 16 combinations of W, A, S, D held or not. For each, record the input vector and the speed under each mode. Put the table in a spreadsheet. How many distinct speeds does each mode produce?
4. **Race.** Simulate a character moving from (0, 0) to (100, 100) with input (1, 1) at `speed = 5`, `dt = 1/60`, in raw and normalize modes. Report arrival times and compare with the lecture's 20.0 s and 28.3 s.
5. **Speed by direction, stick.** Run every sample in `stick_log.csv` through the three modes at `speed = 5`. Plot speed against time for all three on one chart. Mark the stretch where the player walks slowly. Write two sentences on what each mode does to that stretch.
6. **Polar plot.** For stick directions every 5° from 0° to 355°, at full tilt on a square gate (the input `(cos θ, sin θ)` scaled so that its larger component is 1), compute speed in each mode. Plot speed against angle. The raw curve should peak at 45°, 135°, 225° and 315° with value 7.07.
7. **Sprint audit.** Add sprint as a multiplier of 1.5 applied after the mode. Check that sprint in `normalize` and `clamp` gives exactly 7.5 on every keyboard diagonal. Then apply sprint before the mode instead of after it. Record the sprint speed on a straight key and on a diagonal in each mode, and explain in one sentence why the multiplier has to come after the length rule.
8. **Recommendation.** Your team's game ships on PC and console. Write 150 to 250 words recommending which mode to use for each input device and why. Cite at least three numbers from your tables or plots.

## Deliverable

`lab12_starter.py` with tests passing; one spreadsheet with the step 3 table and the step 5 and step 6 charts; a text file with the step 4 times, the step 7 explanation and the step 8 recommendation.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Vec2 and zero guard | All tests pass; no NaN reachable from any input | Tests pass; guard uses exact `== 0` only | NaN possible or tests fail | 20% |
| Keyboard table and race | All 16 rows correct; distinct speeds counted; race times within 0.05 s | One mode has an error | Table or race missing | 20% |
| Stick analysis | Chart shows normalize destroying slow walking; sentences use numbers | Chart correct, discussion thin | Missing | 20% |
| Polar plot | Three curves correct with peaks labeled | Raw curve correct only | Missing | 15% |
| Sprint audit | Both orderings measured; the lost sprint explained | Values correct, no explanation | Missing | 10% |
| Recommendation | Device-specific choice justified with three or more numbers | Choice justified without numbers | No clear recommendation | 15% |
