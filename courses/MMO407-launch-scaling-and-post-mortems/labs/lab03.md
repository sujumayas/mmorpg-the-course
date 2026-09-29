# MMO407 · Lab 03: Beta exposure planner

**Week:** 3 ([lecture](../lectures/w03-beta-strategies.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs.
**Counts toward:** the launch plan (50% of the course grade). Your risk-to-exposure table becomes the testing section of your final launch plan.

## Objective

Turn the lecture's exposure arithmetic into a small planning library, then use it to design a beta program for a given launch: how many testers, for how long, in which phases, with what caps, and which risks it deliberately leaves to launch.

## Starter materials

- [`lab03-starter/beta_exposure.py`](lab03-starter/beta_exposure.py), Python 3, standard library only. It provides `exposure`, `expected_firings` and Apple's phased-release fractions, and five stubs:
  - `p_seen` (TODO 1), the chance a bug fires at least once.
  - `rule_of_three` (TODO 2), the 95% bound after a clean beta.
  - `hours_needed` (TODO 3), the exposure needed for a given confidence.
  - `path_exposure` (TODO 4), exposure split across content paths.
  - `phased_ladder` (TODO 5), the chance of seeing a bug by each day of a phased launch.
- [`lab03-starter/test_beta_exposure.py`](lab03-starter/test_beta_exposure.py) has five tests. All fail on the starter and pass on a correct solution. Run them from inside `lab03-starter/` with `python -m unittest test_beta_exposure.py`.
- `python beta_exposure.py` prints the lecture's section 2 table once TODOs 1 and 2 are done.
- The interactive `examples/w03-beta-exposure.html`, once it is built.

## Steps

### Part A: the library (40 min)

1. Implement TODOs 1 to 5. Run the tests. `test_seen_and_expected` and `test_rule_of_three` must reproduce the lecture's table and its bound of 90 launch firings.
2. `hours_needed(n)` uses the exact `−ln(1 − confidence)`, while the lecture used 3. For confidences of 90%, 95% and 99%, print the exact multiplier and the percentage error of using 3. Say when the rule of three is good enough for planning.
3. Write a Monte Carlo check (MA102 week 11): simulate 10,000 betas of 100,000 player-hours for a bug that fires once per 200,000 hours, drawing each beta's firing count from a Poisson distribution (use the inverse-transform method with `random.random()`). Compare the share of betas that see the bug with `p_seen`.

### Part B: exposure has a shape (35 min)

4. A beta of 250,000 player-hours has these play shares: tutorial 25%, zones 1 to 20 40%, zones 21 to 40 25%, zones 41 to 50 8%, raids 2%. For each path, report the exposure and the rule-of-three bound. Which paths have a bound weaker than once per 5,000 player-hours?
5. The design lead proposes a level cap of 40. Rerun step 4 with the last two shares set to 0 and the rest renormalised. Write two sentences on what the team gives up and one alternative that keeps the endgame fresh but tests it.
6. Your starting zone will peak at 2,800 players at launch. The beta's busiest hour put 650 there. Explain, using the lecture's three exposure types, why adding more beta testers over more weeks will not close this gap, and specify a stress test that will (players, zone, duration, level cap).

### Part C: the beta program (45 min)

7. Plan the beta for this launch. Launch week is forecast at 250,000 players playing 14 hours each. You must see, with 95% confidence, any client crash that fires once per 150,000 player-hours or more often. You have up to 10 weeks and can recruit up to 40,000 testers in total across phases. The weekly reset runs every 7 days.
   - Give each phase (name, dates in weeks, testers, hours each, caps, wipe or not, NDA or not) and its exposure.
   - Show that the total meets the crash target using `hours_needed`.
   - Show which phase gives the weekly-reset exposure and which gives crowd exposure.
8. For the same launch, use `phased_ladder` to find the day of a 7-day phased launch by which a bug firing once per 500,000 player-hours has at least a 50% chance of having been seen. Compare it with a launch that goes to 100% on day 1.
9. Write the risk-to-exposure table for your plan with at least six risks, one of which you choose not to cover. For that one, write the launch-night response (kill switch, patch, or accept).

## Deliverable

- `beta_exposure.py` passing all five tests, plus your code for steps 2 to 8.
- A results sheet with the outputs of steps 2 to 6 and 8.
- A two-page beta program: the phase plan from step 7, the numbers that show it meets the target, and the risk-to-exposure table from step 9.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Library (step 1) | All five tests pass | Minor numeric drift | Tests fail | 20 |
| Checks (steps 2 and 3) | Multipliers and errors correct; Monte Carlo within 1 point of `p_seen`, difference explained | One check missing | Both missing | 15 |
| Exposure shape (steps 4 to 6) | Per-path bounds correct; cap trade-off stated; stress test specified with numbers | Numbers right, reasoning thin | Missing | 20 |
| Beta program (steps 7 and 8) | Meets the crash target within the tester budget; reset and crowd exposure both covered; phased-launch day found and compared | Target met but one exposure type ignored | Target not met or not shown | 30 |
| Risk table (step 9) | Six or more risks, each mapped to a phase or a named launch response | Fewer risks or vague responses | Missing | 10 |
| Code quality | Readable, runs first time | Runs with minor fixes | Does not run | 5 |
| **Total** | | | | **100** |
