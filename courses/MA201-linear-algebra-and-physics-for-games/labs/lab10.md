# MA201 · Lab 10: An impulse resolver

**Week:** 10 ([Collision response and impulses](../lectures/w10-collision-response-and-impulses.md))
**Time:** one 2-hour lab session plus up to 2 hours at home
**Work:** individually; compare material tables with a neighbor at the end
**Counts toward:** problem sets (40%). The resolver is reused in the final physics sandbox.

## Objective

Write the collision response for 2D circles and immovable walls: the normal impulse with restitution and a threshold, the Coulomb friction clamp, and positional correction with slop. Prove it correct against the lecture's numbers and against conservation of momentum. Then use it as a designer: pick a combine rule and a material table that meet three bounce targets, and explain the result with `e² h`.

## Starter materials

- Python 3.10 or later, standard library only. In this repository, `.venv/bin/python`.
- [`labs/lab10-starter/impulses.py`](lab10-starter/impulses.py). It has a `Body` class (position, velocity, radius, inverse mass, bounce), detection helpers `circle_contact()` and `floor_contact()` (week 9's job, provided), and a `drop_test()` that drops a ball on a floor with semi-implicit Euler at 240 Hz and records the height of every bounce. You write five functions: `combine()`, `resolve_velocity()`, `apply_friction()`, `correct_position()` and `reduced_mass_loss()`. Running `python impulses.py` prints the lecture's collision cases and a drop test, or a note for each function not yet written.
- [`labs/lab10-starter/check_lab10.py`](lab10-starter/check_lab10.py). Run `python check_lab10.py` inside the starter folder. It prints PASS or FAIL for seven checks and exits with status 1 until all pass. On the untouched starter all seven fail.
- The interactive [`examples/w10-impulse-bounce.html`](../examples/w10-impulse-bounce.html), whose presets use the same numbers as the checks.

## Steps

### Part A: the resolver (70 minutes)

1. Write `resolve_velocity(a, b, nx, ny, e, threshold)`. Compute `v_n`, return 0 for separating pairs, drop `e` to 0 below the threshold, then apply `j` by inverse mass. Before running the checker, work the lecture's pool row by hand and confirm your code prints `j = 0.332`.
2. Write `reduced_mass_loss()`. The step 2 check fires 200 random collisions at random angles and masses and requires that total momentum never changes and that the kinetic energy lost equals your formula to 1e-9. If momentum drifts, look for a sign error on `n`.
3. Write `apply_friction()`. Take the tangential part of the relative velocity, compute the impulse that would stop it, and clamp it to `±μ j`. The check lands the lecture's 10 kg crate at `(3, −2)` m/s with `μ = 0.5` and `μ = 1.5`.
4. Write `correct_position()`. It must move positions only, never velocities, and a wall (inverse mass 0) must not move. Explain in one sentence in your report why the check expects no movement at a depth of 3 mm.

### Part B: bounces (30 minutes)

5. Write `combine()` for the five rules in the docstring. Run `python impulses.py`. Your drop test should report 7 bounces at a threshold of 1 m/s and 4 at 2, as in the lecture, but the last heights come out lower (about 0.035 m and 0.155 m against the lecture's 0.044 and 0.168), and threshold 0 gives 15 bounces, not 48. Find the two causes. Hint: one is in `drop_test()`'s definition of a bounce, the other is what a 240 Hz step does to the moment of impact. Measure the size of each: change the 0.05 m/s bounce floor, then change `DT`, and record the bounce counts.

### Part C: tune the materials (at home)

6. You are the physics designer for a toy-box level. Using `drop_test()` (you may add a loop over materials), choose **one combine rule** for the whole game and bounce values for four materials: `rubber_ball`, `wood_floor`, `mud` and `trampoline`, all between 0 and 1, and one threshold. The targets are:
   - the rubber ball dropped 3 m onto wood bounces at least 5 times;
   - the rubber ball dropped 3 m onto mud bounces at most 2 times;
   - a wooden block (bounce 0.1) dropped 1 m onto the trampoline rises at least 0.5 m on its first bounce.
7. Try the same materials under a second rule. Record which targets break and why, in terms of the combined `e` and `e² h`.
8. Write a note of at most 300 words to the level designer. Give your rule, material table and threshold, the bounce counts and first-bounce heights that meet each target, and one situation in the toy box your table handles badly (for example, two trampolines, or the rubber ball on the trampoline). Say what you would change if the designer adds a "super ball" that must bounce 20 times.

## Deliverable

Your completed `impulses.py` with `check_lab10.py` passing (paste its output), the step 5 measurements with your two causes, and a PDF with the material table, the step 7 comparison and the designer note.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Resolver correctness (35%) | All seven checks pass; code is short and uses inverse mass throughout with no special case for walls | All pass, with special cases or duplicated code | Normal impulse passes, friction or correction fails | Fewer than three checks pass |
| Drop-test analysis (20%) | Both causes named and measured with before-and-after bounce counts | Both causes named, one measured | One cause named | Missing |
| Material table (25%) | One rule, all three targets met and shown with numbers; step 7 explains each broken target with the combined `e` | Targets met, step 7 thin | Two targets met | Missing |
| Designer note (20%) | Numbers for every target, a concrete bad case, a costed super-ball plan (threshold or `e`, with the bounce count it gives) | Numbers present, weak bad case | No numbers | Missing |
