# GD203 · Simulation brief

**Weight:** 20% of the course grade, in two parts of 10% each.
**Part A:** [Lab 12, duel simulator](../labs/lab12.md). Assigned week 12, due at the start of week 13.
**Part B:** encounter simulation, specified below. Assigned week 13, due at the end of week 14.
**Lecture:** [Week 12, simulation-driven balance](../lectures/w12-simulation-driven-balance.md). Part B also uses [week 10](../lectures/w10-enemy-design-by-the-numbers.md) (encounter cost and kill order) and [week 13](../lectures/w13-difficulty-modes-and-scaling.md) (difficulty multipliers).

## What this component is for

Your spreadsheets report averages. Players live through distributions. This assessment asks you to build a simulator you can trust, then use it to answer a question the sheet cannot: how often does a room you designed kill the player, and how much does that change across difficulty settings and builds?

Part A proves you can build and validate a one-on-one duel simulator. Part B extends it to a multi-enemy encounter from your own balance sheet. The results of part B go into the simulation evidence section of your [final spec](final-spec-brief.md).

## Part A: duel simulator (lab 12)

Follow [lab 12](../labs/lab12.md) as written. It is marked out of 100 with the rubric in the lab, converted as described in the [spreadsheet labs brief](spreadsheet-labs-brief.md) (`weight × band points / 4`). Part A is worth 10% of the course. Lab 12 cannot be dropped.

## Part B: encounter simulation

### The question

Room D from lab 10 (three soldiers and two casters at level 22, budget 70% of player health) was tuned in your sheet with the smooth cost formula `Σ d_i × T_i`. With discrete hits, attack intervals, crits and a real kill order, what does the room actually cost, how often does it kill the player, and where is it balanced?

### Starter materials

- Your part A code. Keep its structure (state, rules, policy, loop, recorder) and its seeded generator.
- Your [lab 11](../labs/lab11.md) sheet, level 22 row: the soldier and caster stat blocks (health, damage per hit, attack interval) and the player's weapon (damage per hit, interval, health). If you changed role targets in lab 11, use your final values. The [lab 10 reference sheet](../labs/lab10-reference.md) gives the untuned level 22 blocks and room D's untuned costs (122.4% best order, 210.0% worst, 127.5% AoE) if you need to check your starting point.
- Your [lab 13](../labs/lab13.md) ladder: the `(p, e, h)` multipliers for Normal and Hard.

### Rules of the encounter

Use these so that everyone's results can be compared.

- Real time with an event queue. The player's first hit lands at `t = 0`. Each enemy's first attack lands at half its attack interval, then every interval after that.
- When a player hit and an enemy attack are scheduled at the same moment, resolve the player's hit first.
- Enemies attack only while alive. The player attacks one enemy at a time and switches target the moment it dies.
- Player hits can crit with chance `c` for 2× damage. Enemy hits are fixed.
- A difficulty rung multiplies player damage by `p`, enemy damage by `e` and enemy health by `h`.
- The fight ends when every enemy is dead or the player's health reaches 0. Record the health lost as a share of the player's health (it can pass 100%, which is a death).

### Validation targets

Before you simulate room D, your code must reproduce these exact results. Set crit chance to 0. The player deals 20 per hit every 1.0 s, and each goblin has 40 health and hits for 4 every 1.0 s.

| Goblins | Enemy hits landed | Damage taken | Smooth formula `c × n(n + 1)/2` |
|---|---|---|---|
| 1 | 1 | 4 | 8 |
| 3 | 9 | 36 | 48 |
| 5 | 25 | 100 | 120 |

Explain in two sentences why the discrete result is lower than the smooth formula here. Then add a crit chance of 25% to the one-goblin case and check that the goblin never lands a hit when the player's first strike crits (a 40-damage opening hit kills it at `t = 0`).

### Steps

1. **Validate.** Reproduce the table above and the crit check. Keep the validation script in your submission so it runs from a clean start.
2. **Three policies.** Simulate room D on Normal for three players: focus fire in best priority-ratio order (`d/h`, highest first), focus fire in worst order, and the AoE class from lab 10 (every hit strikes all enemies for `a = 0.4` of its damage). Use `c = 0.15`. Run 10,000 fights each.
3. **Report the distribution.** For each policy give the mean health cost, the 5th and 95th percentiles, the share of fights that end in death with a 95% interval, and the mean fight length.
4. **Compare with the sheet.** Put your sheet's `Σ d_i × T_i` prediction next to the simulated mean for each policy. Explain the gap in terms of first hits, attack offsets, breakpoints and crits.
5. **Difficulty.** Repeat the best-order run on Hard. Compare the change in mean cost and death rate with what the safety-ratio model predicts (`R` scales by `p / (h × e)`).
6. **Sweep.** Sweep player crit chance from 0% to 40% and soldier health from 70% to 130% of its sheet value, at least 8 × 8 cells, 2,000 fights per cell, with common random numbers. Colour each cell by death rate and mark the region where the death rate is at most 5% and the mean cost is inside the 70% budget.
7. **Recommend.** Propose one change to one role target that moves the best-order player into that region on Normal while keeping the worst-order player outside the budget, so kill order still matters. Show the before and after numbers.

### Deliverables

- Source code (Python standard library, `matplotlib` optional), with a README line that says how to run the validation and each step. Reruns with the same seed must print the same numbers.
- A results file with the validation table, the three-policy table, the sheet comparison, the Hard comparison and the sweep chart.
- A report of about 800 words. Answer: how far is the simulated room from the sheet's prediction and why; how often does each policy die; how fragile is the room (steepness of the sweep around your marked region); and what change you recommend. Every claim needs a number from your results.

## Milestones

| When | Milestone | Graded? |
|---|---|---|
| Start of week 13 | Part A (lab 12) submitted | Yes, 10% of the course |
| Week 13 lab session | Show the part B validation table running. The marker signs it off or tells you what is wrong. | No, but required before the part B deadline |
| End of week 14 (Friday) | Part B submitted | Yes, 10% of the course |
| Week 15 | Part B results appear in the simulation evidence section of the final spec | Graded in the final spec |

Late work follows the rules in the [spreadsheet labs brief](spreadsheet-labs-brief.md). Free extensions may be used for part A but not for part B, because the final spec depends on it.

## Part B rubric

Part B is marked out of 100.

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Validation and reproducibility | 20 | 18-20: all three cases and the crit check reproduced, gap explained, seeded reruns identical | 14-17: cases reproduced, explanation thin or one rerun differs | 10-13: one case wrong, or unseeded | 0-9: no validation, or code does not run |
| Encounter model | 20 | 18-20: event queue, offsets, tie rule, target switching, AoE and multipliers all as specified | 14-17: one rule implemented differently and documented | 10-13: fixed-tick approximation or a missing policy | 0-9: duel only, not an encounter |
| Results and sheet comparison | 20 | 18-20: all distribution statistics with intervals for three policies, every gap to the sheet explained by a named cause | 14-17: statistics complete, explanation partial | 10-13: means only, no intervals | 0-9: no comparison with the sheet |
| Difficulty and sweep | 20 | 18-20: Hard compared with the model's prediction, 8 × 8 or larger sweep with common random numbers, region marked, cliffs linked to breakpoints | 14-17: sweep complete, Hard or cliffs thin | 10-13: small grid or no common random numbers | 0-9: missing |
| Recommendation and report | 20 | 18-20: one targeted change with before and after numbers that meets both conditions, every claim backed by a result | 14-17: change proposed, one condition unchecked | 10-13: vague recommendation | 0-9: no recommendation |

The component grade is the average of part A and part B, each out of 100.
