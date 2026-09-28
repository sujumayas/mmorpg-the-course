# GD203 · Final spec brief: combat system spec and balance workbook

**Weight:** 40% of the course grade.
**Due:** week 15 (the final week), with a 10-minute viva in the same week.
**Builds on:** every lab, and most directly [lab 11](../labs/lab11.md) (the balance sheet), [lab 14](../labs/lab14.md) (the progression memo) and part B of the [simulation brief](simulation-brief.md).

## What you are making

A combat and progression specification for a small RPG of your own design, and the balance workbook behind it. The spec is the document a team would build from. The workbook is where every number in it comes from. Together they show that you can do what the course outcomes promise: design stats and damage formulas with predictable properties, tune time-to-kill and encounter length, pace a 40-hour game with XP and power curves, and prove it with spreadsheets and simulation.

You have been building the parts all semester. This assessment asks you to choose, reconcile and defend them as one system.

## Scope

Keep the game small so the numbers can be complete.

- One player character with at least **3 weapon kits or classes**.
- Levels **1 to 30**, about **40 hours** to the cap.
- At least **4 enemy roles** and **5 zones or dungeons** with encounters.
- At least **4 difficulty rungs**.
- Content after the cap: at least **4 tiers** of post-cap progression.

The setting, the names and the fiction are yours. Do not use characters, logos or art from existing games. You may cite shipped games as precedent, with the version or era, as the lectures do.

## Deliverables

### 1. The spec document

About 5,000 to 7,000 words, not counting tables. Use these sections in this order. Each names the week whose model it must use.

| Section | Must contain | Weeks |
|---|---|---|
| 1. Design promises | Three to five promises in plain sentences, each with a number that tests it. One must answer "what can a weak enemy do to a strong character?" | 1, 2 |
| 2. Stats | The stat graph with exchange rates per kit, the dead stats and why you kept or cut each, and your stacking policy (which bonuses are additive, which multiply, and how many multiplicative sources you allow) | 1 |
| 3. Damage pipeline | Formula and constants, floor policy, order of operations, and one hit traced end to end | 2 |
| 4. Mitigation | Mitigation model, EHP at levels 1, 15 and 30, prices for health and armor, and the tank build those prices lead to | 3 |
| 5. Time-to-kill | Target TTK and safety ratio bands per enemy role, the hits-to-kill matrix at level 15, and every matchup within 5% of a breakpoint with your decision on it | 4 |
| 6. Kits | Alpha, burst, clip and sustained numbers for each kit, and the band of fight lengths each kit wins | 5 |
| 7. Variance | Crit chance and multiplier, the CV at your game's typical PvE and PvP hit counts, and any other randomness | 6 |
| 8. XP and pacing | Time curve, income curve and XP table for levels 1 to 30, the time and XP halfway levels, and the session plan | 7 |
| 9. Power and scaling | Power curve, what a five-level gap means at level 10 and at level 30, the scaling scheme and `R` for every zone | 8 |
| 10. Item budget | Price list with its derivation from stat weights, budget growth with item level, and one audited 12-item loot table | 9 |
| 11. Enemies and encounters | Role templates in player units, stat blocks at levels 5, 15 and 25, and five encounters with best-order, worst-order and AoE costs | 10 |
| 12. Balance workbook summary | Tab map, the check columns and their red-cell count, the sensitivity table and what it means for future patches | 11 |
| 13. Simulation evidence | Part B results, rerun on your final numbers: death rates, the gap to the sheet, and the sweep | 12 |
| 14. Difficulty | The ladder with `(p, e, h)` per rung, the fight-length cap, the scaling exponent `α`, and any assist options kept apart from difficulty | 13 |
| 15. Progression after the cap | The lab 14 memo revised for your game: growth per tier, shelf life, horizontal rewards passing the dominance and expected-value tests | 14 |
| 16. Risks | The three numbers most likely to be wrong, what would reveal it in playtest or telemetry, and what you would change first | all |

### 2. The balance workbook

One workbook with at least these tabs: `Inputs`, `Levels`, `Checks`, `Scenarios`, `Rooms`, `Ladder`, `Tiers`, `Rewards`, `Export` and `Changelog`. You may add more. The rules from the [spreadsheet labs brief](spreadsheet-labs-brief.md) apply: named inputs, no typed constants in formulas, check columns with colour rules, charts of what the player feels.

Every number in the spec must trace to a named cell. Add a `Spec map` tab that lists each table in the spec and the cells it comes from.

### 3. Simulation code

Your part B simulator, updated to read its stats from the workbook's `Export` tab, and the command that reproduces section 13.

### 4. Viva

A 10-minute oral defense in week 15.

- **3 minutes.** You walk through the one decision in the spec you are most confident in, with its numbers.
- **7 minutes.** The examiners ask three questions. One changes an input in your workbook in front of you and asks you to predict two outputs before it recalculates. One is a compute question in the style of the [exam bank](exam-bank.md), rewritten with your game's numbers. One asks you to defend the weakest part of the spec.

## Milestones

| When | Milestone | Points | What you hand in |
|---|---|---|---|
| End of week 6 | Pitch | 5 | One page: the game in two sentences, the design promises with target numbers, the damage and mitigation model you intend to use, and the level and hour targets |
| End of week 11 | Draft checkpoint | 10 | The workbook with `Inputs`, `Levels` and `Checks` working, and draft sections 1 to 5 and 11 of the spec. You get written feedback within a week |
| Week 15 | Final submission | 70 | The spec, the workbook, the simulation code |
| Week 15 | Viva | 15 | Nothing extra. Bring the workbook open on a laptop |

Milestone points are awarded for a complete, on-time submission that meets the description. A late pitch or checkpoint scores 0 for that milestone but still gets feedback. The final deadline is fixed, and free lab extensions do not apply to it.

## How the final submission is checked

Before reading the spec closely, the marker does three things.

1. **Trace test.** Picks ten numbers from the spec at random and finds them in the workbook through the `Spec map`. Each number that does not trace, or does not match, is noted under "Workbook and traceability."
2. **Change test.** Changes one growth rate on `Inputs` by 10% and checks that `Levels`, `Checks`, `Rooms` and `Ladder` all update and that the red-cell count changes in a way your sensitivity table predicts.
3. **Rerun test.** Runs the simulation command and checks that it reproduces the numbers in section 13.

## Rubric

The final submission is marked out of 70 and the viva out of 15. Milestones add up to 15 more, for 100 in total.

### Final submission (70 points)

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Design promises and coherence | 8 | 7-8: each promise has a test number, and later sections visibly serve the promises | 6: promises clear, one not tested | 5: promises stated, rarely referenced | 0-4: missing, or contradicted by the numbers |
| Combat math (sections 2 to 7) | 18 | 16-18: every model applied correctly, breakpoints and variance addressed with decisions, one hit traced end to end | 13-15: one section thin or one model misapplied | 10-12: several sections thin, or averages used where hit counts matter | 0-9: sections missing or wrong |
| Progression math (sections 8 to 10 and 15) | 18 | 16-18: pacing, power, scaling, budget and post-cap growth consistent with each other, shelf life computed, sidegrades tested | 13-15: one inconsistency between curves, or one test missing | 10-12: curves chosen without their consequences shown | 0-9: sections missing or wrong |
| Enemies, encounters and difficulty (sections 11 and 14) | 10 | 9-10: roles in player units, kill order a real decision, AoE checked, ladder separates danger from duration | 7-8: one of those missing | 5-6: stat blocks without encounter costs, or ladder without a length cap | 0-4: missing |
| Workbook and traceability (section 12) | 10 | 9-10: trace test and change test pass, sensitivity table drives stated patch advice | 7-8: one or two numbers fail to trace | 5-6: several numbers typed into the spec, change test partly fails | 0-4: workbook does not support the spec |
| Evidence and risks (sections 13 and 16) | 6 | 6: simulation reruns, results change at least one decision, risks are specific and testable | 5: reruns, decisions unchanged or risks generic | 3-4: results pasted without interpretation | 0-2: no simulation evidence |

### Viva (15 points)

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Walkthrough | 4 | 4: one decision explained with its numbers and its alternative | 3: decision clear, alternative missing | 2: describes rather than defends | 0-1: not prepared |
| Change prediction | 4 | 4: both outputs predicted in the right direction with a reason from the model | 3: one right, reasoning sound | 2: guesses, reasons after seeing the result | 0-1: cannot follow the workbook |
| Compute question | 4 | 4: correct answer with the model named | 3: right method, arithmetic slip | 2: partial method | 0-1: no method |
| Defending the weakest part | 3 | 3: names the weakness, its cost in numbers and a fix | 2: names the weakness and a fix | 1: defends without evidence | 0: no answer |
