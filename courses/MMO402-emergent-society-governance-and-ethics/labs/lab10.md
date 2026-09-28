# MMO402 · Lab 10: Pacing audit

**Week:** 10 ([lecture](../lectures/w10-addiction-wellbeing-and-responsible-design.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs.
**Counts toward:** case analyses (30% of the course grade).

## Objective

Run the lecture's four pacing rules (flat, rested, fatigue, daily reward) over a synthetic population of 500 players with different schedules. Find out who each rule rewards and who it penalizes. Then design a weekly reward that keeps the daily reward's retention purpose with a lower obligation cost, and recommend one design to a studio.

## Starter materials

- [`lab10-starter.py`](lab10-starter.py): a Python 3 script (standard library only). It contains:
  - the lecture's constants (`B = 10`, `A = 0.625`, `CAP = 150`, `D = 10`), all in percent of a level;
  - `simulate(sessions, rule)`, an hour-by-hour simulator that runs 6 weeks and returns the last week's experience, so rested pools reach a steady state;
  - `rule_gain(rule, hours_today, pool)` with the flat rule done and the rested, fatigue and daily rules left as `TODO`;
  - `self_test()`, which checks your rules against the lecture's table (light, daily, weekend and binge schedules);
  - `population(n=500, seed=402)`, which generates four archetypes: evening regulars (about 30%), weekenders (30%), irregular players (25%) and marathoners (15%);
  - `audit(players)`, which returns one row per player with hours, days played and the weekly total under each rule, and an optional `--csv` export.
- The pacing rules interactive, `examples/w10-pacing-rules.html`, once built, for checking single schedules. Until then, the lecture's section 2 table is the reference.
- A spreadsheet program for the charts, or `matplotlib` if you prefer.

## Steps

### Part A: implement the rules (25 min)

1. Fill in the three `TODO` branches of `rule_gain`. Rested earns `B + min(pool, B)`. Fatigue earns `B` for the first 3 hours of the calendar day, `B/2` until hour 5, then 0. Daily earns `B` plus `D` on the first played hour of the day.
2. Run the script. All 16 self-test lines must print `ok`. If one fails, explain the bug in one sentence in your write-up.

### Part B: who wins, who loses (35 min)

3. Run the audit on the default population. For each archetype, report mean hours per week and, for each rule, mean weekly experience as a ratio of the flat rule. Present this as a 4 × 3 table.
4. Plot experience per hour played (vertical) against hours per week (horizontal), one scatter per rule, with points colored by archetype.
5. In three or four sentences, say which archetype each rule favors, and connect each finding to the clock the rule reads (time offline, time in session, presence on the day).

### Part C: design a weekly reward (35 min)

6. Add a `weekly` rule. It pays `B` per played hour, plus a weekly bonus `W` split into up to `m` claims: the first played hour of each of the first `m` distinct days in the week earns `W / m`. Choose `W` and `m` so that the evening regulars' mean weekly total is within 5% of what the daily rule gives them.
7. Run the obligation test from the lecture on three players of your choice (one per archetype other than marathon): move one day's hours onto the next played day and compute each rule's loss. Report the losses for daily and weekly.
8. Compare daily and weekly across the whole population: mean ratio to flat per archetype, and the share of players who lose more than 5 experience from a moved day.

### Part D: sensitivity (15 min)

9. Change the population seed three times. Report whether your Part B and Part C conclusions hold. If a conclusion flips, say which archetype share or rule parameter drives it.

## Deliverable

- The completed script, runnable, with the `weekly` rule.
- A PDF of at most 3 pages: the Part B table and chart, the Part C design with its parameters and results, the Part D check, and a 400-word recommendation memo to a studio producer choosing between the daily reward and your weekly reward. The memo must name the clock each design reads, give at least two numbers from your audit, and state one risk of your recommendation.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Rules implemented (Part A) | All 16 self-tests pass | 12 or more pass, failures explained | Fewer than 12 pass | 15 |
| Population analysis (Part B) | Correct table and chart; each finding tied to the clock the rule reads | Table and chart present, explanation generic | Missing | 25 |
| Weekly design (Part C) | Parameters meet the 5% target; obligation test done and compared with daily across the population | Design works but comparison incomplete | Missing | 25 |
| Sensitivity (Part D) | Three seeds, conclusions checked, any flip explained | Seeds run, no explanation | Missing | 10 |
| Recommendation memo | Clear choice, two or more audit numbers, clock named, a real risk stated | Choice made with weak support | Missing | 25 |
| **Total** | | | | **100** |
