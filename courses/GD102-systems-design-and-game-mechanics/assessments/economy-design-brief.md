# GD102 · Economy design brief

**Weight:** 30% of the course grade, in three parts.
**Part A:** [Lab 07, town economy spreadsheet](../labs/lab07.md). 6% of the course.
**Part B:** [Lab 09, skill and power table](../labs/lab09.md). 6% of the course.
**Part C:** economy design project, specified below. 18% of the course. Assigned in week 8, due at the start of week 12.
**Lectures:** mainly [week 7, internal economies](../lectures/w07-internal-economies-sources-drains-converters.md) and [week 8, core loops and meta loops](../lectures/w08-core-loops-and-meta-loops.md). Part C also uses [week 2](../lectures/w02-stocks-and-flows.md) (stocks, flows, caps), [week 5](../lectures/w05-machinations-diagrams-i.md) and [week 6](../lectures/w06-machinations-diagrams-ii-converters-traders-gates.md) (the diagram language) and [week 9](../lectures/w09-progression-systems-skill-vs-power.md) (where power comes from).

## What this component is for

The fourth course outcome is "design an internal economy for a small game". Labs 07 and 09 give you the two halves of that on fictional numbers. Lab 07 is the money side, where faucets, sinks and converters decide the price level. Lab 09 is the power side, where the rate at which the economy pays out power decides how much skill still matters. Part C asks you to put both into a game of your own and show, with a running model, that the economy does what you say it does.

The game you design here is the game your [final SDD](final-sdd-brief.md) documents. Choose one you are willing to spend the rest of the semester on.

## Parts A and B: labs 07 and 09

Follow each lab as written. Each is marked out of 100 with the rubric printed in the lab, and each is worth 20% of this component (6% of the course). Neither lab can be dropped, because Part C starts from both.

| Lab | Assigned | Due |
|---|---|---|
| [07](../labs/lab07.md) | Week 7 | Start of week 8 |
| [09](../labs/lab09.md) | Week 9 | Start of week 10 |

## Part C: economy design project

### The task

Design the internal economy of a small game and prove, with a spreadsheet model and a running Machinations diagram, that it settles where you intend, survives three stress tests, and gives its core loop a binding constraint you chose on purpose.

### Pick a premise

Choose one of these three, or propose your own at the week 9 milestone. Every premise is fictional. If you borrow a structure from a shipped game, cite the lecture that covers it and add no new facts about that game.

| Premise | Starting size | What makes it interesting |
|---|---|---|
| **Harbor town.** A small-server MMO town where players fish, craft and trade. | 500 players, one currency, two materials | A player market that needs a proportional sink, and crafters whose goods set prices |
| **Relay run.** A roguelite whose runs pay two currencies, one lost on death and one kept. | One player, 20-minute runs | A meta shop whose cadence must wind down near the end of the content |
| **Hollow farm.** A co-op farm for 4 players with shared silos and a seasonal market. | 4 players, 28-day seasons | A reinvesting core loop that must bend at a designed constraint, and shared stocks |

### Requirements

Your economy must contain all of the following. Name each in your design note where it appears.

1. **At least three resources**, at least one of them a currency. List each as a stock with its unit.
2. **At least one source, one flat drain, one proportional drain and one converter.** If your game has a player-to-player trade, draw it as a trader. If it has none, say why.
3. **One reinforcing and one balancing loop**, each drawn with a state connection and labelled with its count of minus links.
4. **A core loop with a binding constraint.** Write it as `n = min(limit 1, limit 2, ...)` as in week 8. Say which limit binds in the first hour and which binds after ten hours, and show the bend in your sheet.
5. **A meta loop** that spends core-loop output and moves a named constraint. Give its exchange rate and cadence for the first five purchases.
6. **One power source** from the economy (gear, levels, upgrades). Using the week 9 model or your own stated version of it, show the mistake budget for one representative challenge at the expected power and at the power a player would have after one extra hour of play.

### The model

- **Spreadsheet.** One inputs tab with every tunable number named and given a unit. One row per step (day, run or cycle). One checks tab. Run at least 180 days, or 100 runs or cycles if your step is not a day.
- **Equilibrium by formula and by sheet.** For each currency with a proportional drain, compute `M*` by formula (week 7) and show the sheet converging to it. Give the half-life of a gap. For any stock without a proportional drain, say so and say what happens when its faucet drifts.
- **Machinations diagram.** The same economy, drawn with the week 5 and 6 elements, with every rate labelled with the symbol used in your sheet. It must run in machinations.io for at least 50 steps. Include a screenshot of the pool chart and one line showing the conservation check for your main currency.

### Stress tests

Run each from the settled state, and write your prediction before you run it.

| Test | Change | Pass condition |
|---|---|---|
| Faucet | Main currency faucet +15% from day 0 | Price level (or cost of your reference good in currency) within 20% of its starting value after 180 days |
| Population | +50% players on day 60, joining with zero wealth (skip for single-player premises and use "+50% run length" instead) | Money per player returns to within 10% of its old equilibrium, or you explain why it should not |
| Converter | Output of your main converter +50% | You state the price change the model predicts and the group of players who pay for it |

A failing test is not a failing grade. A failed test that you explain and fix, with the fix shown in the sheet, earns full marks on that line.

### Deliverables

- The spreadsheet (file or view link) with Inputs, Simulation, Checks and a Scenarios tab holding the three stress tests.
- The Machinations file or link, and the pool-chart screenshot.
- A design note of 1,200 to 1,500 words with these headings.
  - *Premise and target player.* Who plays, how often, and what rhythm the economy should reward.
  - *Economy audit.* The five-step audit from week 7, section 4, as a table: stocks, every source, drain, converter and trader, each drain classified flat or proportional, the equilibrium, and money per player.
  - *Loops.* The reinforcing and balancing loops with signs, the core loop's `min`, the bend, and the meta loop's cadence.
  - *Power.* The mistake budget at expected and at +1 hour power, and one sentence on whether that exchange rate is what you want.
  - *Stress tests.* Prediction, result, and explanation for each.
  - *Who pays.* For each drain, the group of players it falls on most heavily.
  - *What the model leaves out.* At least two things, and which way each would push your numbers.

## Milestones

| When | Milestone | Graded? |
|---|---|---|
| End of week 8 | Lab 07 returned with feedback | Part A |
| Week 9 lab session | **Pitch.** One page: premise, target player, list of stocks with units, and a first Machinations sketch on paper. Five minutes with a marker, who approves the premise or asks for one change. | 10 points of Part C |
| Start of week 10 | Lab 09 submitted | Part B |
| Week 10 lab session | **Checkpoint.** The sheet runs 180 days (or 100 cycles) and the equilibrium cell matches the sheet's last row. The marker signs it off or names what is wrong. | No, but required before submission |
| Start of week 12 | **Part C submitted.** | 90 points of Part C |
| Week 13 | Feedback returned, in time to revise for the SDD | No |

## Part C rubric (100 points)

The pitch is worth 10 points: 10 for a pitch that meets the list above, 5 if a stock list or the sketch is missing, 0 if no pitch. The submission is marked out of 90.

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Economy structure and audit | 15 | 14-15: every requirement present, audit complete, drains classified, money per player given | 11-13: one requirement thin | 8-10: audit partial or a required element missing | 0-7: no audit, or several requirements missing |
| Machinations diagram | 15 | 14-15: runs 50 steps, every rate labelled with the sheet's symbol, activation modes right, conservation line holds | 11-13: runs, one label or mode wrong | 8-10: runs with several errors, or does not match the sheet | 0-7: does not run or not provided |
| Spreadsheet model | 15 | 14-15: inputs named with units, no numbers in formulas, checks tab works, reruns cleanly | 11-13: one or two hard-coded numbers | 8-10: several hard-coded numbers, or checks missing | 0-7: sheet does not run the stated model |
| Equilibrium and feedback | 15 | 14-15: `M*` and half-life by formula match the sheet, loops signed with minus counts, flat-only stocks named with their drift | 11-13: equilibrium right, one loop unsigned | 8-10: equilibrium by sheet only | 0-7: no equilibrium, or loops misread |
| Core loop, constraint and power | 10 | 9-10: `min` with real limits, bend shown in the sheet, meta cadence for five purchases, mistake budget at both power levels | 7-8: one of those missing | 5-6: loop described in words, no bend | 0-4: missing |
| Stress tests | 10 | 9-10: all three run with predictions before results, every failure explained and fixed | 7-8: all three run, one prediction or explanation missing | 5-6: two run | 0-4: one or none |
| Design judgment | 10 | 9-10: who pays is named for every drain, limits of the model push the numbers in a stated direction, choices defended against an alternative | 7-8: who pays named, alternatives thin | 5-6: judgment generic, could fit any economy | 0-4: missing |

## Late work

Part C submitted up to 48 hours late loses 10 of its 100 points. After that it is marked for feedback only and scores 0. Free lab extensions (see the [Machinations models brief](machinations-models-brief.md)) cannot be used on Part C, because the SDD depends on it. Labs 07 and 09 follow the lab late rules in that brief and may use its free extensions.
