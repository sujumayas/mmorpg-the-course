# MA201 · Lab 08: A force accumulator and three drag models

**Week:** 8, forces, mass and drag ([lecture](../lectures/w08-forces-mass-and-drag.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Work mode:** pairs.
**Weight:** part of the problem sets (40%). The `Body` class is the starting point for the physics sandbox.

## Objective

Turn the lecture's drag formulas into code you can trust. You will reproduce Minecraft's documented terminal velocities from its per-tick rules, port the player's fall from 20 Hz to 60 Hz and 144 Hz without changing how it feels, break the naive damping formula on purpose, and finish with a small force-accumulator body you will reuse in the sandbox.

## Starter materials

All in [`lab08-starter/`](lab08-starter/). Python 3.10 or later, standard library only.

- [`forces.py`](lab08-starter/forces.py). Given: the four operation orders (`"PAD"`, `"APD"`, `"ADP"`, `"PDA"`) with the Minecraft entity types that use each, a `fall_table` helper and a runner. You write eleven small pieces in four parts:
  - Part A: `tick_entity`, `terminal_velocity`, `ticks_to_fraction`.
  - Part B: `drag_coefficient`, `per_step_factor`, `per_step_gravity`, `damp`.
  - Part C: `quake_friction`.
  - Part D: `Body.add_force` and `Body.step`.
- [`test_lab08.py`](lab08-starter/test_lab08.py): eleven tests. Run `python test_lab08.py` inside the folder. On the starter it reports `0/11 tests passed`.
- The week 8 interactive, [`examples/w08-terminal-velocity.html`](../examples/w08-terminal-velocity.html).

## Steps

### Part A: per-tick rules (30 min)

1. **Predict.** On paper, compute the velocity after two ticks for a Minecraft player (`g = 0.08`, `d = 0.98`, order `"PAD"`) and for an item (`g = 0.04`, `d = 0.98`, order `"APD"`). Also compute each one's position after two ticks. Note which one has moved after the first tick and why.
2. **Implement** `tick_entity`, `terminal_velocity` and `ticks_to_fraction`. `terminal_velocity` must handle all four orders. Derive the drag-before-acceleration case yourself from the fixed-point equation, as the lecture did for the other case.
3. **Pass** `test_orders_matter_on_first_tick`, `test_player_first_second`, `test_wiki_terminal_velocities`, `test_simulation_reaches_formula` and `test_ninety_percent`.

### Part B: coefficients and tick rates (35 min)

4. **Implement** `drag_coefficient`, `per_step_factor`, `per_step_gravity` and `damp`.
5. Run `python forces.py`. It prints the player fall at 20 Hz and at 60 Hz with converted numbers. The two tables should agree to within 1%. The terminal speed at 60 Hz comes out near 78.9 blocks/s, not 78.4. Explain the 0.7% difference in two sentences. (Hint: which of `g·d/(1 − d)` and `g/c` is the continuous limit?)
6. Add a 144 Hz run. Produce one plot of speed against time for 20, 60 and 144 Hz with converted numbers, and a second plot for 60 and 144 Hz with the 20 Hz numbers copied unchanged. Label each curve with its terminal speed.
7. For `h = 1/60`, tabulate the three damping formulas for `c` = 10, 30, 60, 90, 120 and 150 per second. Mark where `linear` first goes negative and where it first has magnitude above 1. Check both against `c·h = 1` and `c·h = 2`.

### Part C: Quake friction (20 min)

8. **Implement** `quake_friction` and pass `test_quake_stop`.
9. Simulate a stop from the full run speed of 320 units/s at frame rates of 20, 60, 72 and 144 fps. Tabulate the stop time and slide distance at each rate. Compare with the continuous estimate of about 0.54 s from the lecture. Which rate is furthest off, and in which direction?

### Part D: the body (25 min)

10. **Implement** `Body.add_force` and `Body.step` (semi-implicit Euler with the Padé damping factor, forces cleared every step, no motion or gravity for `inv_mass == 0`). Pass the last two tests.
11. Drop two bodies of 1 kg and 4 kg from rest with no damping, but with a quadratic drag force `−k·|v|·v` added through `add_force` each step (`k = 0.012` kg/m). Record both terminal speeds and check them against `√(m·g/k)`. Then repeat with `damping = 0.4` and no drag force. Write two sentences on what changed.

## Deliverable

- The completed `forces.py` passing all eleven tests, including your 144 Hz run and the Part D experiment.
- A PDF of at most 3 pages containing: the two Part B plots, the damping table, the Quake table, the Part D terminal speeds, and a one-page drag spec for one of these feels: "floaty moon jump", "heavy mech that coasts on ice", "arrow that drops late". The spec must give `g` and drag as per-second values, the order of operations, the tick rate, the terminal speed and the time to 90%, and show that it survives a change to 30 Hz.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Implementation | All eleven tests pass, 144 Hz run added | Nine or ten tests pass | Eight or fewer pass | 30 |
| Tick-rate study (Part B) | Both plots correct and labelled; 0.7% gap explained correctly; damping table marks both thresholds | Plots present, explanation vague or thresholds missed | Missing | 25 |
| Quake and mass studies (Parts C, D) | Tables complete, rate error direction explained, terminal speeds match `√(m·g/k)` within 1%, damping contrast stated | One part complete | Missing | 20 |
| Drag spec | Per-second values, order, rate, terminal speed and 90% time given and checked at 30 Hz | Spec complete but not checked at 30 Hz | Missing or raw per-tick factors only | 25 |
| **Total** | | | | **100** |
