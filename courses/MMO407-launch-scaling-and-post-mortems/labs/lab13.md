# MMO407 · Lab 13: Launch risk register

**Week:** 13 ([lecture](../lectures/w13-launch-plan-workshop.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** your launch plan group (3 or 4 people).
**Counts toward:** the launch plan (50% of the course grade). This lab produces sections 4 to 6 of the plan: the risk register, the mitigations and the triggers.

## Objective

Implement the exact loss distribution for a launch-week risk register, reproduce the lecture's table, choose mitigations under a budget with three explicit rules, measure how a correlated cause changes the tail, and then apply all of it to your own group's launch.

## Starter materials

- [`lab13-starter/launch_risk.py`](lab13-starter/launch_risk.py), Python 3, standard library only. It holds the lecture's register (`LECTURE_RISKS`), mitigations (`LECTURE_FIXES`) and disaster line (`LECTURE_D = 300`), with `expected_loss` and `apply_fixes` done and four stubs:
  - `loss_distribution` (TODO 1), the exact distribution `{loss: probability}` over all `2ⁿ` combinations.
  - `exceedance` (TODO 2), `P(L > x)`.
  - `choose` (TODO 3), the best set of fixes under the rules `"expected"`, `"penalty"` and `"limit"`.
  - `scenario_distribution` (TODO 4), a hidden cause that fires several risks together while keeping each risk's overall rate.
- [`lab13-starter/test_launch_risk.py`](lab13-starter/test_launch_risk.py), eight tests. All fail on the starter and pass on a correct solution. Run them from inside `lab13-starter/` with `python -m unittest test_launch_risk.py` (from the repository root, use `.venv/bin/python`).
- `python launch_risk.py` prints the lecture's plan table once TODOs 1 and 2 are done.
- The interactive `examples/w13-risk-register-tail.html`, once it is built.
- Your group's outputs from labs 1 to 3 and the register from the in-class activity.

## Steps

### Part A: the model (40 min)

1. Implement `loss_distribution` and `exceedance` (TODOs 1 and 2). Run the tests. `test_lecture_table` must reproduce `E = 115.0` and `P(L > 300) = 0.069` with no fixes, and the M1+M2, M1+M3 and M3+M4 rows.
2. Plot the exceedance curve `P(L > x)` for x from 0 to 1,700 for "none", M1+M2 and M3+M4 on one chart, as step lines. Draw the disaster line at 300. In two sentences, say what M1+M2 changes and what it does not.
3. Add a fifth risk to the lecture register: "store and entitlement outage", `p = 0.15`, `I = 220`. Recompute `E` and `P(L > 300)` for the seven plans. Which combinations now cross the line that did not before?

### Part B: choosing under a budget (30 min)

4. Implement `choose` (TODO 3) and run the tests.
5. For the lecture register, find the break-even penalties `B` between every pair of plans that is ever the cheapest as `B` goes from 0 to 2,000. Present them as a table like the lecture's "your rule, plan you buy" table and check it against a sweep of `choose` in steps of 10.
6. Raise the budget to 3 fixes and repeat step 5. Does the expected-loss rule ever buy a set with zero disaster chance?

### Part C: correlated risks (20 min)

7. Implement `scenario_distribution` (TODO 4) and run all tests.
8. For the lecture register with the scenario "demand three times forecast" forcing `queues` and `auth`, sweep `s` from 0 to 0.3 and plot `P(L > 100)` and `P(L > 300)`. Explain in two sentences why one moves and the other does not.
9. Invent a second scenario, "a rushed day-3 patch", that forces `dupe` and `data loss` together with `s = 0.01`. What does it do to `P(L > 300)` with no fixes and with M3+M4? Is your chosen plan still the right one?

### Part D: your launch (30 min)

10. Enter your group's register: at least six risks, at least one scenario row, and at least five candidate mitigations with a cost in engineer-weeks. State where each `p` and `I` comes from, and label guesses as guesses.
11. Agree the disaster line `D` and write down who agreed it and why, before you run `choose`.
12. Choose your mitigations with a budget you justify. Report the plan each rule picks, the break-even `B` between them, and the plan you buy.
13. Write at least four contingency triggers in the lecture's table form (signal, threshold, action, owner, lead time, stand-down). For each, check `t_s + T ≤ t_h` using your lab 2 queue model or an estimate you state.

## Deliverable

- `launch_risk.py` passing all eight tests, plus your code and plots for steps 2 to 13.
- Sections 4 to 6 of your launch plan, at most 4 pages: the register with sources for each number, the exceedance chart for your chosen plan and the expected-loss plan, the rule and budget you used with the break-even penalty, and the trigger table.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Model (steps 1 to 3) | Tests pass; exceedance plot correct with the disaster line; fifth-risk crossings identified | Tests pass; plot or step 3 incomplete | Tests fail | 20 |
| Budget rules (steps 4 to 6) | Tests pass; break-even table matches the sweep; budget-3 question answered with numbers | Table present but not checked by sweep | Tests fail | 20 |
| Correlation (steps 7 to 9) | Tests pass; both sweeps plotted and explained; second scenario analysed with and without fixes | Sweeps without explanation | Tests fail | 15 |
| Group register (steps 10 to 12) | Six or more risks with sourced numbers; `D` agreed in advance; rule, budget and break-even stated | Register present, sources or `D` reasoning thin | Missing | 25 |
| Triggers (step 13) | Four or more complete triggers, each with a lead-time check | Triggers missing owner, stand-down or lead-time check | Missing | 15 |
| Code quality | Readable, runs first time | Runs with minor fixes | Does not run | 5 |
| **Total** | | | | **100** |
