# MA101 · Lab 10: Orbits and bursts

Assigned in week 10 ([lecture](../lectures/w10-angles-radians-sin-cos.md)). Due at the start of week 11. Counts toward the problem-set grade.

## Objective

Write the orbit and aim formulas from week 10 as small, tested functions, use them to generate an orbiting shield and a radial bullet pattern, and tune a shield so that it meets a gap and hit-rate target. You will also reproduce the degrees-for-radians bug on purpose and learn to spot it from its output alone.

## Starter materials

- [`starter/lab10_starter.py`](starter/lab10_starter.py). Python 3, standard library only (`math`, `csv`). It defines a `Vec2` class with `+`, `-` and scalar `*`, and five empty functions:
  - `deg_to_rad(d)` and `rad_to_deg(r)`.
  - `orbit_positions(center, r, n, omega, t, theta0=0.0)` returns a list of `n` `Vec2` positions.
  - `chord_gap(r, n)` and `hits_per_second(n, omega)`.
  - `burst_velocities(speed, n, theta0=0.0)` returns `n` velocity `Vec2`s evenly spaced around the circle.
  - `spread_velocities(speed, aim, spread, n)` returns `n` velocities across a cone of total angle `spread` centered on `aim`.
- [`starter/test_lab10.py`](starter/test_lab10.py): checks using the lecture's test values. Run `python3 test_lab10.py`; every line must print `ok`.
- Spreadsheet route for steps 4 to 7: build the columns yourself from the same formulas. Spreadsheet `SIN` and `COS` also take radians; use `RADIANS()` to convert.
- The week 10 interactive, [`examples/w10-orbit-and-waves.html`](../examples/w10-orbit-and-waves.html), to check individual positions.

If you prefer an engine (Godot 4 or Unity 6), you may do steps 4 to 6 there instead, but steps 1 to 3 must be in the starter so the tests can run.

## Steps

1. **Conversions.** Implement `deg_to_rad` and `rad_to_deg`. The tests check 90° → 1.5708, π → 180 and 1 rad → 57.2958°.
2. **Orbit positions.** Implement `orbit_positions` with `θ_k = θ0 + ωt + 2πk/N`. The tests check the lecture's table: `N = 3, r = 100, ω = π` at `t = 0` and `t = 0.25`, to one decimal.
3. **Gap and hit rate.** Implement `chord_gap` (`2r sin(π/N)`) and `hits_per_second` (`Nω/2π`). Check `N = 3, r = 100` gives 173.2 and 1.5.
4. **Sample an orbit.** Write positions of orb 0 for `t = 0` to `2` s in steps of `1/60` s to `orbit.csv`. Plot x against t and y against t in a spreadsheet. Label the period on the plot and show that it equals `2π/ω`.
5. **Bursts and spreads.** Implement `burst_velocities` and `spread_velocities`. For a burst of 8 at speed 300, print the velocities and check that every one has length 300. For a spread of 5 pellets, 20° total, aim 30°, print the angles and confirm they are 20°, 25°, 30°, 35°, 40°. Then generate a spiral: 6 waves of a 12-bullet burst, adding 10° to `θ0` each wave. Plot the bullet positions 0.5 s after each wave fires on one scatter chart.
6. **The bug on purpose.** Copy `orbit_positions` to `orbit_positions_buggy` and remove the conversion so that it treats `ωt` in degrees but passes it to `math.cos` and `math.sin` as radians. Sample it as in step 4 and plot it next to the correct version. Write two sentences on how you would recognize this bug from a screen recording, with no access to the code.
7. **Tune a guardian ring.** A boss ring must satisfy all three: chord gap minus orb diameter (20 px) between 30 and 40 px; at least 2 hits per second on any spot of the ring; orb speed no more than 400 px/s so it stays readable. The ring radius must be between 100 and 160 px. Find one `(r, N, ω)` that works and one that fails each rule. Present them in a table.
8. **Memo.** Your designer wants an upgrade that "makes the shield bigger". Using your step 7 numbers, recommend how the upgrade should change `r`, `N` and `ω` together so that coverage and hit rate do not get worse. 150 to 250 words.

## Deliverable

`lab10_starter.py` with all functions implemented and `test_lab10.py` passing; `orbit.csv`; one spreadsheet with the step 4, 5 and 6 plots and the step 7 table; the memo as a text file or a sheet.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Functions and tests | All tests pass; code converts units at one boundary only | Tests pass with a hard-coded value or a duplicated conversion | Tests fail | 25% |
| Orbit plot | x and y traces correct, period labeled and matches `2π/ω` | Traces correct, period missing or wrong | Plot missing or traces wrong | 15% |
| Bursts, spreads, spiral | All lengths 300, spread angles exact, spiral visible | One of the three has a small error | Two or more missing | 20% |
| Degrees bug | Buggy plot shown; recognition sentences name a visible symptom | Plot shown, description vague | Missing | 10% |
| Guardian ring table | One passing and three failing designs, all computed correctly | Passing design correct, failing cases incomplete | No valid design | 15% |
| Memo | Recommendation changes at least two of `r`, `N`, `ω` and uses numbers | Recommendation with numbers but only one variable | No numbers | 15% |
