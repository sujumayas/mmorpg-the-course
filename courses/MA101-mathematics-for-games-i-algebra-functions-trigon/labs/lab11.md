# MA101 · Lab 11: Turrets that turn

Assigned in week 11 ([lecture](../lectures/w11-atan2-turning-toward-a-target.md)). Due at the start of week 12. Counts toward the problem-set grade.

## Objective

Build a turret that finds its target with `atan2`, turns the short way at a capped rate, and fires once the target is inside an aim cone. Then build a homing missile, predict from `R = v/ω` when it will orbit instead of hit, and confirm the prediction by simulation.

## Starter materials

- [`starter/lab11_starter.py`](starter/lab11_starter.py). Python 3, standard library only. It imports the `Vec2` class from `lab10_starter.py` (keep both in one folder) and defines empty functions:
  - `angle_to(from_pos, to_pos)` returns the `atan2` angle in radians.
  - `shortest_delta(current, target)` returns the wrapped difference in (−π, π].
  - `turn_step(current, target, omega, dt)` returns the new facing after one capped step.
  - `time_to_act(delta, turn_rate_dota, cone_deg)` returns seconds, using the lecture's Dota 2 formula.
  - `simulate_missile(start, heading, v, omega, target, dt, lifetime, hit_radius=10)` returns a list of positions and a result string, `"hit"` (within `hit_radius` px) or `"timeout"`.
- [`starter/test_lab11.py`](starter/test_lab11.py): checks with the lecture's test values (the `atan2` table, the wrap table, the Dota turn-time table).
- [`starter/targets.csv`](starter/targets.csv): 12 target positions around a turret at (0, 0), columns `name, x, y`.
- The week 11 interactive, [`examples/w11-turn-toward-target.html`](../examples/w11-turn-toward-target.html), to check individual cases.

## Steps

1. **Angle to target.** Implement `angle_to` with `math.atan2(dy, dx)`. Add a second function `angle_to_naive` that uses `math.atan(dy / dx)` and returns `None` when `dx = 0`. For every row of `targets.csv`, print both in degrees. Mark the rows where they differ by more than 0.5°, and state the rule that predicts which rows those are.
2. **Shortest delta.** Implement `shortest_delta` using `raw − 2π × round(raw / 2π)`. Test it on the lecture's wrap table. Then write a version with Python's `%` and a version that imitates C's `%` (use `math.fmod`). Show one input where the `fmod` version gives the long way round.
3. **Capped turning.** Implement `turn_step` with `clamp(delta, −ω dt, ω dt)`. Simulate a turret starting at 0° turning toward each target at `ω = 180°/s`, `dt = 1/60`. Record the number of frames until `|delta| ≤ 5°`. Compare with the formula `(|delta| − 5°)/ω` and explain any difference of one frame.
4. **Dota 2 check.** Implement `time_to_act`. Reproduce the lecture's table for turn rates 0.5 and 0.6 and add a column for 0.8. Plot time to act against `|delta|` from 0° to 180° for the three turn rates on one chart. Label where each line leaves zero, and explain why that point is the same for all three.
5. **Smooth turning.** Implement exponential turning `facing += delta × (1 − e^(−k dt))` with `k = 10`. Run it at `dt = 1/30` and at `dt = 1/144` for 0.5 s from 0° toward 150°. Show that both end at the same angle to within 0.5°. Then replace `1 − e^(−k dt)` with a constant 0.2 and show that the two frame rates now disagree.
6. **Homing missile.** Implement `simulate_missile` with the step 3 turning. Use `v = 400 px/s`, start at (0, 0) heading 0°, target stationary. Compute `R = v/ω` for `ω = 90°, 180°, 360°` per second. For each `ω`, place the target at (0, 0.8R) and at (0, 2.5R) and run for 6 s. Record hit or timeout and plot all six trails on one chart with the turning circles drawn.
7. **Fix the orbit.** Choose one fix from the lecture (raise `ω` when close, slow down when turning hard, or cap the lifetime). Implement it and show the `(0, 0.8R)` case now hits or ends cleanly. Report what the fix costs in feel, in one sentence with a number (for example the tightest radius reached, or the time added).

## Deliverable

`lab11_starter.py` with tests passing; a spreadsheet or image with the step 4 chart and the step 6 trail chart; a text file with the answers to steps 1, 2, 3, 5 and 7, each two to four sentences with numbers.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| atan2 versus atan | Both computed; differing rows marked; rule stated as "dx < 0" or equivalent | Computed, rule vague | Only one computed | 15% |
| Shortest delta | All three versions; `fmod` failure case shown | Correct function, no failure case | Wrong wrap on any lecture test | 15% |
| Capped turning and Dota check | Frame counts match formula to one frame; chart correct and labeled | Small numeric errors | Missing or wrong model | 25% |
| Smooth turning | Frame-rate independence shown and broken correctly | Only one half shown | Missing | 15% |
| Homing missile | Six runs with trails and circles; predictions match results | Runs done, circles missing | Missing | 20% |
| Fix and trade-off | Fix works and its cost is stated with a number | Fix works, cost not measured | No fix | 10% |
