# MA201 · Lab 06: Moving frames

**Week:** 6, kinematics ([lecture](../lectures/w06-kinematics-position-velocity-acceleration.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the problem sets (40%).

## Objective

Turn the lecture's relative-motion model into tested code, then use it on a real-looking log. A playtester reports that on the "swinging platform" the first jump works and the second one drops them into the pit, though they did the same thing both times. You will estimate the platform's velocity and acceleration from logged positions, predict both landings, show which term in the model causes the fall, and choose a fix.

## Starter materials

All in [`lab06-starter/`](lab06-starter/). Python 3.10 or later, standard library only.

- [`kinematics.py`](lab06-starter/kinematics.py). 2D vectors use y up. You write:
  - Part A: `forward_diff`, `central_diff`, `second_diff`.
  - Part B: `launch_velocity` for Godot's three `platform_on_leave` modes, with optional Celeste-style caps, and `relative_landing` for a platform with constant velocity and acceleration.
  - Part C: `cross`, `point_velocity` (`ω × r`) and `centripetal`.
  - Part D: `find_jumps` on the log. `load_log` is given.
- [`platform_log.csv`](lab06-starter/platform_log.csv): 3.5 s of play at 60 samples per second, columns `t, platform_x, player_x, player_y`. Positions are rounded to whole pixels, so each can be off by up to 0.5 px. The platform is 80 px wide (half-width 40) and its surface is at `y = 0`.
- [`make_log.py`](lab06-starter/make_log.py): the script that produced the log. Do not open it until step 7.
- [`test_lab06.py`](lab06-starter/test_lab06.py): eight tests. Run `python test_lab06.py` in the folder. On the starter it reports `0/8 tests passed`.
- The week 6 interactive, [`examples/w06-moving-platform.html`](../examples/w06-moving-platform.html).

## Steps

1. **Predict.** From the lecture's model only, write down where the player lands relative to the take-off spot for: a platform moving at a constant 200 px/s under each of the three modes; an elevator descending at 150 px/s under `add` and `upward`.
2. **Part A.** Implement the three differences. The tests use the lecture's platform samples and the drone from Check yourself question 1.
3. **Part B.** Implement `launch_velocity` and `relative_landing`. The tests reproduce the lecture's tables and the mine-cart drift of −66.6 px. Then run your step 1 cases through the code and compare.
4. **Part C.** Implement the rotation helpers. For a turntable spinning at 0.8 rad/s about the up axis, compute the take-off velocity of a player standing at `(3, 0, 0)`, `(0, 0, 3)` and `(2, 0, 2)` m, and the centripetal acceleration at each point.
5. **Read the log.** Implement `find_jumps`; it should find jumps at 0.5 s and 2.0 s. At each jump, estimate the platform's velocity with a central difference over one sample (`h = 1/60`) and over five samples on each side (`h_eff = 10/60`). Estimate its acceleration with a second difference over one sample and over fifteen samples on each side. Tabulate all eight numbers. Which estimates can you trust, and why? Use the lecture's noise bounds `2e/h` and `4e/h²`.
6. **Predict the landings.** For each jump, use your trusted velocity and acceleration with `relative_landing` in `add` mode to predict the landing offset. Add the offset to where the player stood on the platform before the jump. Compare with the log: find the sample where the player lands (or falls past `y = 0` outside the platform) and read the actual offset. Explain which term, inherited velocity or platform acceleration, is responsible for the second jump's miss.
7. **Check the truth.** Now open `make_log.py`. The platform follows `x_p(t) = 260·sin(πt/4)`. Compute the exact velocity and acceleration at each jump and the exact landing offsets. How far off were your step 6 predictions, and in which direction for each jump? The model assumes constant acceleration, but this platform's acceleration changes during the 0.816 s of air time. Explain why that makes the model miss by several pixels on the first jump and by only about 2 px on the second.
8. **Fix the level.** Choose one fix and show with numbers that both jumps now land: a wider platform, a slower platform (change the 260 or the π/4), caps on inherited velocity, or keeping the player attached to the platform frame while airborne. For the attach option, state the offset it gives and one gameplay side effect.

## Deliverable

Your `kinematics.py` with `python test_lab06.py` reporting `8/8 tests passed`, plus a design note of at most one page:

- The step 1 predictions next to the code's results.
- The step 4 velocities and accelerations.
- The step 5 table of eight estimates and your trust judgment.
- The step 6 and 7 predicted and actual offsets for both jumps, and the one-sentence cause.
- The step 8 fix with its numbers and side effect.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tests pass | 8/8 | 6-7 | 5 or fewer | 30% |
| Rotating platform (step 4) | All three velocities with correct direction, centripetal values right | Magnitudes right, directions wrong | Missing | 10% |
| Estimates from the log (step 5) | All eight numbers, trust judgment uses the noise bounds with numbers, rejects the one-sample acceleration | Numbers right, judgment without bounds | Missing or wrong | 20% |
| Landing analysis (steps 6 and 7) | Predictions computed with the model and compared with the log, cause named as platform acceleration with the `½·a_p·T²` term, each prediction error explained by the changing acceleration | Predictions made, cause vague | Missing | 25% |
| Fix (step 8) | Both landings shown inside the platform with numbers, side effect named | Fix proposed, only one landing checked | Missing | 15% |
