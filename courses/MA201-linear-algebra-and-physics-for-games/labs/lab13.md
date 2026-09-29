# MA201 · Lab 13: The archer's aim

**Week:** 13, projectile motion and aiming at moving targets ([lecture](../lectures/w13-projectile-motion-and-aiming-at-moving-targets.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Work mode:** pairs.
**Weight:** part of the problem sets (40%). The aim functions are reused in the physics sandbox.

## Objective

Write the aiming code an enemy archer needs, prove it against the lecture's numbers, and then find out how much exact aim is worth once the target stops running in straight lines. You finish by tuning an archer to a hit rate a designer asks for, using the dodge budget to predict the result before you measure it.

## Starter materials

All in [`lab13-starter/`](lab13-starter/). Python 3.10 or later, standard library only.

- [`aim.py`](lab13-starter/aim.py). Given: `dot`, CS203's `estimate_time`, `aim_direction` for the three aim modes, a seeded `simulate_duel` harness, and a command-line runner. You write `intercept_time` (with a cast delay), `aim_point`, `launch_angles`, `ballistic_intercept` and `dodge_budget`. As shipped they return `None` or 0, so the file runs, the TF2 check prints `None`, and the exact archer never fires.
- [`test_lab13.py`](lab13-starter/test_lab13.py): nine tests. Run `python test_lab13.py` from inside the folder. On the starter it reports `0/9 tests passed`.
- The week 13 interactive, [`examples/w13-lead-the-target.html`](../examples/w13-lead-the-target.html), for checking single cases by eye.
- For plots, `matplotlib` if you have it, or any spreadsheet.

## Steps

### Part A: implement and verify (45 min)

1. **Predict.** Before coding, solve by hand the three radial cases in `test_radial_targets` and `test_slow_shot`. Each is a one-line linear equation. Write them in your report.
2. **Implement** `intercept_time` and `aim_point`. Handle every case from lecture section 2: `a` near zero (use a tolerance, not `== 0`), a negative discriminant, and no positive root. The cast delay shifts the start to `D + u·delay`. `aim_point` must return where the target will be at `delay + t`.
3. **Implement** `launch_angles` and `ballistic_intercept`. Check the second against the first. For a standing target the elevation must match the low arc.
4. **Implement** `dodge_budget`, then run the tests until all nine pass. Run `python aim.py` and confirm the TF2 check matches the lecture's table to four decimals.

### Part B: what exact aim is worth (35 min)

5. With `jink = 0` (straight runners), fill this table using `simulate_duel` with 500 shots.

   | Shot speed (m/s) | Body | Estimate | Exact |
   |---|---|---|---|
   | 15 | | | |
   | 25 | | | |
   | 40 | | | |

6. Repeat for `jink = 0.1` and `jink = 0.3`. You should find that exact aim's advantage shrinks as jinking grows, and that at low shot speed and high jink, aiming at the body can beat both leads. Explain that result in three sentences using the dodge budget. Hint: a target that changes heading at random is, on average, near where it started.
7. Plot hit rate against shot speed for the three modes at `jink = 0.3`. Mark where the estimate and exact curves become indistinguishable.

### Part C: tune an archer (30 min)

8. The designer's brief: "Our skeleton archer should hit a player who runs straight about 90% of the time at 20 m, and a player who jinks (`jink = 0.3`) about 40% of the time." You may change shot speed, hit radius (the `radius` argument), and aim mode, and you may add an aim error. To add error, write a new mode `"sloppy"` in `aim_direction` that rotates the exact direction by a random angle drawn from a seeded generator.
9. Before measuring, predict with the dodge budget (reaction time 0.25 s, `delay = 0`) whether a jinking player can always dodge at 20 m with your chosen speed and radius. Then measure. Report prediction and measurement side by side.
10. Write a 250-word design note to the designer. Give the chosen values and the measured rates, and describe one situation (distance, player behaviour) where the archer will feel unfair or useless.

## Deliverable

- The completed `aim.py` passing all nine tests, including your `"sloppy"` mode.
- A PDF of at most 3 pages containing the Part A hand solutions, the Part B tables, plot and explanation, and the Part C prediction, measurements and design note.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Implementation (Part A) | All nine tests pass; edge cases handled with tolerances; hand solutions correct | Seven or eight tests pass | Six or fewer pass | 35 |
| Experiment (Part B) | Three complete tables and the plot; body-beats-lead result found and explained with the dodge budget | Tables complete, explanation vague or not tied to the model | Missing | 25 |
| Tuning (Part C) | Meets both targets within 5 points; prediction made before measuring and compared honestly; sloppy mode seeded | One target met, or prediction missing | Missing | 25 |
| Design note | Names values and rates, identifies a concrete unfair or useless case, plain writing | Plausible but generic | Missing | 15 |
| **Total** | | | | **100** |
