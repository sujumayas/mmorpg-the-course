# MMO407 · Lab 07: Faction balance simulator

**Week:** 7 ([lecture](../lectures/w07-classic-and-legacy-servers.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs.
**Counts toward:** the launch plan (50% of the course grade). Your balance plan becomes the "population health" section of your final launch plan.

## Objective

Implement the lecture's bandwagon model of faction shares, reproduce its numbers, measure which parameters make a realm tip and how fast, and choose a balancing lever for a fresh legacy realm by comparing what each lever costs.

## Starter materials

- [`lab07-starter/realm_balance.py`](lab07-starter/realm_balance.py), Python 3, standard library only. It provides `simulate`, `share` and a `__main__` block that prints the lecture's year once the TODOs are done, plus four stubs:
  - `newcomer_share` (TODO 1), the rule `s^k / (s^k + (1 − s)^k)`.
  - `week` (TODO 2), one weekly step with the optional creation lock. It returns `(A, B, turned_away)`.
  - `first_week_at` (TODO 3), the first week a share threshold is reached.
  - `realm_choice` (TODO 4), the several-realm version from the lecture's section 3.
- [`lab07-starter/test_realm_balance.py`](lab07-starter/test_realm_balance.py) has six tests. All fail on the starter and pass on a correct solution. Run them from inside `lab07-starter/` with `python -m unittest test_realm_balance.py`.
- The interactive `examples/w07-faction-tipping.html`, once it is built.

## Steps

### Part A: the model (40 min)

1. Implement TODOs 1 to 3 and run the tests. `test_year` must reproduce the lecture: 68.1% at week 8, 90.7% at week 16, 70% first reached in week 9, a total of 18,688 players at week 52.
2. Plot A's share over 52 weeks for starting splits of 51/49, 52/48, 55/45 and 60/40 on one chart. Mark the week each crosses 90%, and check the lecture's table.
3. Plot the newcomer rule `p(s)` against `s` for `k = 0.7, 1, 2, 3`, with the diagonal. Write two sentences explaining, from this plot alone, why `k = 1` is neutral and `k = 0.7` pulls the realm back toward even.

### Part B: what makes a realm tip (35 min)

4. Sweep `k` from 0.6 to 3.0 in steps of 0.2 and `e` from 0 to 0.4 in steps of 0.05. For each pair, record the first week at 90% from a 55/45 start (or "never" within 104 weeks). Present it as a heat map or table.
5. With `e = 0.2`, does any `k` in your grid keep the realm below 70% for two years? Then fix `k = 1.2` and find the largest `e`, to two decimal places, that keeps the realm below 70% for two years. What does each answer mean for a designer who can influence only one of the two parameters?
6. Change `J` to 200 and then to 3,000 with the other constants at the lecture's values. Does a realm with many newcomers tip faster or slower? Explain with the model, not with the plot.

### Part C: choose a lever (45 min)

7. Implement `realm_choice` (TODO 4) and run all tests.
8. Your studio opens a fresh legacy PvP realm. Launch-week arrivals give a 53/47 split with 12,000 players; after launch, `J = 800`, `c = 6%`, `k = 2.2`, `e = 0.25`. Compare three levers over 26 weeks:
   - a creation lock at 55% from week 0, with `spill = 0.5`;
   - the same lock switched on only when the share first passes 60%;
   - a reshuffle every 4 weeks (add it to your own copy of `simulate`: after every 4th week, set both factions to half the total).
   For each, report the share at weeks 8, 16 and 26, the players turned away, and the total at week 26.
9. Three realms open at 4,000, 3,000 and 2,000 players with 1,500 newcomers per week, `c = 5%` and `k = 1.5`. Simulate 20 weeks of realm choice (no factions; each realm loses `c` and gains its newcomers). Report each realm's share of all players at weeks 5, 10 and 20, and the share of newcomers the smallest realm receives at week 20. Propose one intervention (for example a cap or a transfer incentive) and show its effect on those numbers.

## Deliverable

- `realm_balance.py` passing all six tests, plus your code for steps 2 to 9.
- The plots from steps 2, 3 and 4.
- A one-page balance plan for the step 8 realm: the lever you chose, its numbers against the alternatives, the social tie it breaks and how you will explain that to players, and the dashboard alert (metric, threshold, owner) that triggers it.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Model (steps 1 to 3) | Tests pass; plots correct; neutral and underdog cases explained from the newcomer rule | Tests pass; explanation vague | Tests fail | 25 |
| Sensitivity (steps 4 to 6) | Full grid; both thresholds found; the effect of `J` explained with the model | Grid present, one threshold or the `J` explanation missing | Missing | 20 |
| Lever comparison (step 8) | All three levers run with shares, turned-away counts and totals; late lock shown to fail or succeed with numbers | Two levers compared | Missing | 25 |
| Realm choice (steps 7 and 9) | Test passes; shares reported; intervention modelled | Shares reported without intervention | Missing | 10 |
| Balance plan | Every claim traced to a run; cost stated; alert rule concrete | Clear but partly unsupported | Missing | 15 |
| Code quality | Readable, runs first time | Runs with minor fixes | Does not run | 5 |
| **Total** | | | | **100** |
