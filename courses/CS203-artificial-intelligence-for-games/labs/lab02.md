# CS203 · Lab 02: A steering toolkit

**Week:** 2, steering behaviors ([lecture](../lectures/w02-steering-behaviors.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the labs (50% of the course). Keep your toolkit; later labs that move agents can build on it.

## Objective

Build the vehicle model and five steering behaviors for a 2D point mass, reproduce the lecture's overshoot and pursuit numbers, then tune arrive for three different bodies and write a movement spec another programmer could implement from.

## Starter materials

All in [`lab02-starter/`](lab02-starter/). Standard-library Python 3, no packages.

- [`steering.py`](lab02-starter/steering.py) has small vector helpers (`add`, `sub`, `scale`, `length`, `truncate`), seven empty functions (`braking_distance`, `step`, `seek`, `flee`, `arrive`, `pursue`, `blend`), and two finished experiments that call them: `run_line`, the lecture's 20 m approach, and `chase`, the lecture's pursuit test. Running the file prints the lecture's tables once your functions work.
- [`test_steering.py`](lab02-starter/test_steering.py) checks the lecture's numbers: braking distance 1.5 m for the soldier, seek overshoot 1.50 m with no settling, the arrive table (0.80, 0.50, 0.00 m of overshoot and settle times 4.78, 4.68, 3.83, 5.45, 7.35 s), pursuit catch times 2.15 s and 3.05 s against seek's 2.40 s and 4.10 s, the prediction point `(20, 10)` from check-yourself question 3, and the blend stalemate `(0, 0.25)`.
- The [interactive](../examples/w02-seek-vs-arrive.html), to compare your runs with the reference.

Run the tests from the starter folder with `python3 test_steering.py` (or the course's `.venv/bin/python`). On the starter every test prints `TODO` and the script exits with status 1.

## Steps

1. **`braking_distance`.** One line, `v² / (2a)`.
2. **`step`.** Implement the vehicle model exactly as the docstring says. Order matters. Truncate the change, then truncate the speed, then move with the new velocity.
3. **`seek` and `flee`.** Normalize the offset and scale by `max_speed`. Return `(0, 0)` when the offset is zero rather than dividing by zero. Remember the sign warning from the lecture.
4. **`arrive`.** Ramp the desired speed inside the slowing radius.
5. **`pursue`.** Predict with `T = distance / max_speed`, then seek the predicted point.
6. **`blend`.** Weighted sum. Run the tests until all pass, then run `python3 steering.py` and compare its output with the lecture.
7. **Tune three bodies.** For the rat (8 m/s, 40 m/s²), the soldier (6, 12) and the ogre (4, 3), call `run_line` with a range of slowing radii. For each body, find the smallest radius with no overshoot and the radius with the fastest settle time. Record both, with `b` and `2b` from `braking_distance`.
8. **Stopping distance.** Add an optional `stop_distance` to `run_line`. When the agent is closer than that and slower than 0.5 m/s, set its velocity to zero. For the ogre at `r = 2b`, find the largest stop distance that still stops within 5 cm of the target, and report the new settle time.
9. **Stalemate.** Build a two-behavior bot in a 2D test of your own: seek a target 10 m east, and avoid an obstacle 3 m east of the start (flee from it, weighted by `1 / distance`). Show that with equal weights the bot stalls. Then implement one fix from the lecture (priority, or picking the less-blocked of two directions) and show the bot reaching the target.

## Deliverable

- `steering.py` with all tests passing, the `stop_distance` option and your stalemate experiment.
- A tuning table for the three bodies: `b`, `2b`, smallest clean radius, fastest radius, chosen radius, stop distance, settle time.
- A movement spec of at most 300 words. For each body give the chosen parameters and one sentence on how the numbers make the character look (heavy, snappy, nervous). Add one paragraph on your stalemate fix and a case where it would still fail.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Correctness | All tests pass; `python3 steering.py` reproduces the lecture's numbers | Tests pass with small unexplained differences | Tests fail | 30% |
| Tuning table | All three bodies complete, radii consistent with `b` and `2b`, stop distance justified by measurement | Table complete but choices not tied to the model | Incomplete | 25% |
| Stalemate experiment | Stall demonstrated numerically, fix implemented, a remaining failure case named | Stall shown, fix sketched but not run | Missing | 20% |
| Movement spec | Another programmer could reproduce the tuning; look and feel tied to numbers | Parameters given, reasons vague | Missing or unusable | 15% |
| Code quality | Behaviors are pure functions of their inputs; no duplicated vector math | Works but repetitive | Hard to follow | 10% |
