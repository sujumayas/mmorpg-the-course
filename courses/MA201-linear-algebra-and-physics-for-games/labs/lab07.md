# MA201 · Lab 07: Three integrators and an energy meter

**Week:** 7, numerical integration ([lecture](../lectures/w07-numerical-integration-euler-semi-implicit-verlet.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Work mode:** pairs.
**Weight:** part of the problem sets (40%). The step functions are reused in the physics sandbox.

## Objective

Implement explicit Euler, semi-implicit Euler and velocity Verlet as three small functions, prove them against the lecture's hand-computed numbers, and then measure what the lecture only claimed: which rule leaks energy, how the error shrinks with the step, and where a stiff spring stops being stable. You finish with a recommendation you could defend in a code review.

## Starter materials

All in [`lab07-starter/`](lab07-starter/). Python 3.10 or later, standard library only.

- [`integrators.py`](lab07-starter/integrators.py). Given: `gravity` (inverse-square, GM = 1), `make_spring(w)`, `orbit_energy`, `spring_amplitude`, `run`, `max_energy_error`, and a command-line runner that prints the lecture's orbit table and can write every step to CSV. You write the bodies of `explicit_euler`, `semi_implicit` and `velocity_verlet`. As shipped they return the state unchanged, so the file runs and nothing moves.
- [`test_lab07.py`](lab07-starter/test_lab07.py): nine tests. Run `python test_lab07.py` from inside the folder. On the starter it reports `0/9 tests passed`.
- The week 7 interactive, [`examples/w07-orbit-integrators.html`](../examples/w07-orbit-integrators.html), for checking orbits by eye.
- For plots: `matplotlib` if you have it, or open the CSV in any spreadsheet.

## Steps

### Part A: implement and verify (40 min)

1. **Predict.** Before coding, write down by hand the state after one step of each rule from `(1, 0)`, `(0, 1)` with `dt = 0.1`. The lecture's section 2 table gives the answers. Cover it first.
2. **Implement** the three step functions. Each must call `accel` once for Euler and semi-implicit, and at most twice for Verlet. Run the tests until the three `first_step` tests pass.
3. **Run** `python integrators.py`. Your output must match the lecture's printed block to every digit shown. Then run the full test file. All nine should pass.

### Part B: the elliptical orbit (35 min)

4. Run `python integrators.py --v0 1.2 --steps 2000 --csv ellipse.csv`. Plot the three trajectories (x against y) on one figure with equal axis scales, and energy against time on a second.
5. Using `max_energy_error`, fill this table for `v0 = 1.2` and 10 orbits:

   | Steps per orbit | Explicit | Semi-implicit | Verlet |
   |---|---|---|---|
   | 60 | | | |
   | 120 | | | |
   | 240 | | | |
   | 480 | | | |

   Add a column with the ratio between consecutive rows for each method. Your semi-implicit ratios should sit near 2 and your Verlet ratios near 4. State in one sentence what that tells you about each method's order.
6. Repeat the table for `v0 = 1.0` (the circle). Explain in two sentences why the semi-implicit ratio changes.

### Part C: the stiff spring (30 min)

7. With `make_spring(w)` and `dt = 1/60`, find by bisection the smallest `w` (to 0.1 rad/s) at which semi-implicit Euler's peak `|x|` over 10 s exceeds 1,000. Compare with the lecture's limit `ω·dt = 2`.
8. Repeat at `dt = 1/120` and `dt = 1/240`. Plot the critical `w` against `1/dt`. It should be a straight line. Give its slope.
9. A designer wants a grappling rope with `k / m = 40,000` in a 60 Hz game. Using your line, state the smallest number of sub-steps per tick that keeps it stable with a safety margin of 25% on `ω·dt` (that is, `ω·dt ≤ 1.5`).

### Part D: the recommendation (15 min)

10. Pick one system from this list: an orbiting moon in a space sandbox, a rope bridge made of 40 particles, a player's jump in a platformer, a homing missile with a turning spring. Write a 300-word recommendation naming the integrator, the tick rate and any sub-steps, citing your own numbers from Parts B and C.

## Deliverable

- The completed `integrators.py` passing all nine tests.
- A PDF of at most 3 pages: the Part B plots and two tables, the Part C bisection results and plot, and the Part D recommendation.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Implementation (Part A) | All nine tests pass; printed table matches the lecture | Seven or eight tests pass | Six or fewer pass | 30 |
| Convergence study (Part B) | Both tables complete, ratios computed, order stated correctly, circle vs ellipse explained | Tables complete, interpretation vague or partly wrong | Missing | 25 |
| Stability study (Part C) | Critical `w` found at three steps, straight-line fit with slope near 2, sub-step answer correct | Two of the three parts correct | Missing | 25 |
| Recommendation (Part D) | Names integrator, rate and sub-steps, uses the pair's own numbers, states one cost | Plausible but not backed by measurements | Missing | 20 |
| **Total** | | | | **100** |
