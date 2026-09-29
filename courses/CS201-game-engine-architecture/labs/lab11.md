# CS201 · Lab 11: Islands, sleep and a safe event queue

**Week:** 11 ([Physics integration basics](../lectures/w11-physics-integration-basics.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually; compare your part B curves with a neighbor at the end

## Objective

Write the engine-side pieces that decide what a physics world costs once the action stops. You will group bodies into islands with union-find, apply the lecture's sleep rule with wake-on-touch, and process contact events safely after the step. Then you will measure how pile layout and the sleep threshold change the number of awake bodies, and recommend settings for a level. No solver is involved. Speeds are supplied by a finished driver, so everything you measure comes from your own sleep and island code.

## Starter materials

- Python 3.10 or later, standard library only. In this repository, `.venv/bin/python`.
- [`lab11-starter/physics_sleep.py`](lab11-starter/physics_sleep.py). It contains a finished toy `World` that locks itself during `step()`, and a finished driver `settle()` that feeds decaying speeds into your sleep system for any number of identical stacks. You write `build_islands()`, `sleep_time_alone()`, `SleepSystem.tick()` and `process_contacts()`. Each docstring is the specification.
- [`lab11-starter/test_physics_sleep.py`](lab11-starter/test_physics_sleep.py). Run `python test_physics_sleep.py` from inside the starter folder. It prints PASS or FAIL for seven checks and exits with status 1 until all pass. On the untouched starter all seven fail.
- The interactive [`examples/w11-sleeping-islands.html`](../examples/w11-sleeping-islands.html), to predict curves before you compute them.

## Steps

### Part A: the pieces (70 minutes)

1. Write `build_islands()` with union-find (path compression is enough, union by rank is optional). Static bodies never join an island and never connect two. Check 1 includes a floor touched by every crate and a 1,000-body chain. In one sentence, explain why a floor must not merge islands, using the cost formula from the lecture.
2. Write `sleep_time_alone()` from the lecture's closed form. Check 2 compares it with the lecture's table.
3. Write `SleepSystem.tick()`. Follow the four rules in the docstring in that order. Checks 3a and 3b reproduce the lecture's stack (asleep at tick 161, 2.683 s), its 1,000-crate version, and the jittery crate at two thresholds. Check 3c tests wake-on-touch. Explain in two sentences why the check expects the woken bodies' timers to be 1 and not 30.
4. Write `process_contacts()`. Damage is applied for every event a body appears in, and destruction happens once per body, after all damage, in ascending id order. Check 4b also shows that destroying inside the callback raises, as the lecture's section 4 warned.

### Part B: measure (35 minutes)

5. Use `settle()` with the lecture's five speeds and `stacks=200`. Plot awake bodies against time from 0 to 10 s for three cases: no jitter, one jittery crate (floor 0.06 m/s) in 10% of stacks, and the same with `v_sleep = 0.10`. You will need to call `settle()` separately for jittery and calm stacks and add the counts. Report awake body-seconds over 10 s for each case.
6. Island size. Keep 1,000 crates but arrange them as 1,000 islands of 1, 200 islands of 5, 20 islands of 50 and 1 island of 1,000. For the larger islands, repeat the five speeds cyclically (`v0s * 10` for 50). Report when each layout reaches zero awake bodies and its awake body-seconds. Then wake one island of each layout at `t = 5 s` (reset those bodies' timers, or run a second `settle()` for that island and add it) and report the size of the spike.
7. Using the lecture's cost `C_step ≈ a × awake + b × contacts` with `a = 4 µs`, `b = 1.5 µs`, and one contact per body in a chain, convert your step 6 spike into milliseconds of frame time.

### Part C: the recommendation (at home)

8. Your level has a collapsed library: 600 books, 40 shelves that can topple, and 12 reading tables. Measurements show books jitter at up to 0.04 m/s when stacked, shelves at up to 0.08 m/s. Pick `v_sleep` and `t_sleep`, decide which objects are static, dynamic, or dynamic only after being hit, and decide how many islands you will allow. Use your code to estimate the settle time and the worst wake spike.
9. Write a note of at most 300 words to the level designer. State your settings, the settle time, the worst wake spike in milliseconds, and one visible side effect of your `v_sleep` choice (for example, a slow-rolling book stopping early) and whether you accept it.

## Deliverable

Your completed `physics_sleep.py`, with `test_physics_sleep.py` passing (paste its output). Also a PDF with the step 1 and step 3 explanations, the step 5 plot and body-seconds, the step 6 table and spikes, the step 7 conversion, the step 8 plan and estimates, and the note.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Correct pieces (35%) | All seven checks pass; union-find is near-linear; step 1 and step 3 explanations use the model correctly | All checks pass, explanations vague | Islands and sleep time work, tick or events fail | Code missing or broken |
| Measurement (30%) | Step 5 plot with three labeled curves and body-seconds; step 6 table for four layouts with settle time, body-seconds and wake spike; step 7 in ms | All numbers present, one case unexplained | Only one of steps 5 and 6 | Missing |
| Recommendation (20%) | Settings justified from measured jitter; body types and island count argued from cost; estimates computed with the code | Settings and estimates, weak justification | Settings only | Missing |
| Note (15%) | Clear, numbers quoted, visible side effect named and a decision taken | Numbers present, side effect vague | Few numbers | Missing |
