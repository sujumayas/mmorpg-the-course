# MMO304 · Final economy spec brief

**Weight:** 50% of the course grade.
**Week:** 15 (submission, presentation and viva), with milestones in weeks 11 and 14.
**Work mode:** individual. You may share a game concept with a classmate, but the numbers, workbook and spec must be your own.
**Tools:** your [Lab 14](../labs/lab14.md) workbook (or its Python version), your [Lab 13](../labs/lab13.md) simulation and memo, and any earlier lab tool you want to reuse.

## The job

Write the economy section of a game design spec for an MMO of your own design, and back every number in it with a simulation. Another designer should be able to implement your economy from the spec, and a live team should be able to tune it from your telemetry table without asking you anything.

This is the course in one document. Weeks 1 and 2 price your items and say what kind of value they carry. Weeks 3, 4, 5 and 14 size your money flows and sinks. Weeks 6, 7 and 8 set your markets, crafting chains and item lifecycles. Weeks 9, 10, 11 and 13 decide what can be traded, how, and what money players will really use. Week 12 decides what you will watch after launch.

## Constraints

- The game is fictional and must have player-to-player trade of at least some goods.
- At least one tradeable currency, at least one crafting chain of two or more stages, and at least one durable item category.
- Every faucet and sink names the player activity that produces it.
- Every number in the spec traces to a cell in your workbook or a line of your script. Do not type a result that the model should compute.
- Real-game facts appear only as supporting examples, cited with the version or era the course lectures give. Your design numbers are your own.
- No copyrighted names, art or characters from shipped games in your game's content.

## The spec: required sections

Length 10-14 pages plus appendices. Use these headings in this order so markers can find each part.

| # | Section | What it must contain | Course source |
|---|---|---|---|
| 1 | Game and money | The core loop, the core reward, and the two or three things money is for at the top level | Weeks 1, 13, 14 |
| 2 | Scarcity and value | A table of at least six items with lever (chance, effort, rate limit, fixed supply), `p`, `t`, expected hours `T`, price `w × T`, median and 95th-percentile wait, and the item's main value type (`F`, `H` or `S`). Say which items are bound and why | Weeks 1, 2 |
| 3 | Currency flows and steady state | The faucet and flat-sink ledger for a typical player, `N`, the proportional sinks and `s = τv + other rates`, target `W*` and half-life with a two-sentence justification each, and the server average for your expected stay | Weeks 3, 14 |
| 4 | Nominal or indexed | Every fixed gold number in the spec classified as fixed, indexed to money per player, or a percentage, with the index formula where one applies | Week 4 |
| 5 | Sinks and hoards | A cohort table (new, regular, veteran at least) with balances and spending rates, the price level `P = S / Q`, and the effect of each of your sinks on `P` and on each cohort. At least one sink must reach players with low trade velocity | Week 5 |
| 6 | Markets and fees | Per good class: scope, search cost, visibility (asks only or order book), fees and where they are charged. A fee-incidence estimate for one key good using straight-line curves, with the buyer's share and the gold removed per day | Weeks 6, 10 |
| 7 | Crafting and gathering | The bill of materials for one chain with `e = q(1 − r) / s` at each stage, the finished item's cost, the experience-crafter threshold `a − bC`, and the gathering price `W / u` | Week 7 |
| 8 | Item lifecycle | For each durable category, a destruction rate `d` derived from a coverage target, `S*`, mean lifetime, and the player-facing rule. Repair sinks priced per hour of play | Week 8 |
| 9 | Money that players might choose | The item most likely to become commodity money, scored against the week 9 properties, and your plan for its drop rate, sinks and duplication response | Week 9 |
| 10 | Market reach | The reach `m` for each item category, the core reward's `m`, and one number from your Lab 13 simulation | Week 13 |
| 11 | Real-money trade policy | Your policy family, and the black-market band from the week 11 model with your own token price, bot costs and ban time. Say which variable you push first | Week 11 |
| 12 | Telemetry and levers | At least six dashboard panels with metric, cadence and alert rule, and a levers table with at least four rows (metric, segment, target band, lever if above, lever if below). At least one row segmented by account age | Weeks 12, 14 |
| 13 | Stress tests and risks | The three Lab 14 stress tests with results and the lever you would pull, plus two risks your model cannot see | Lab 14 |

**Appendices:** the workbook or script, the Lab 14 charts, the Lab 13 plot, and a one-page summary sheet listing every target and its current modelled value.

## Milestones

| When | Milestone | Share of this 50% |
|---|---|---|
| End of week 11 | M1: one-page proposal. Game, core reward, currencies, first-guess `W*` and half-life, and the reach `m` you plan for the core reward. Feedback within four days | 5% |
| Week 14, due with the spec | M2: [Lab 14](../labs/lab14.md), scored with its own rubric (20 points, scaled) | 20% |
| Week 15, 48 hours before the session | M3: the full spec with appendices | 55% |
| Week 15 | M4: 8-minute presentation and 10-minute viva | 20% |

The Lab 13 memo is marked in the [Models assignment](models-brief.md). Here it counts only as evidence in section 10, so you may revise it for the spec.

## Presentation and viva (M4)

The presentation covers your targets, your flow table, the steady-state chart and your three most important levers. Keep numbers on screen.

In the viva, the examiner changes one number in your workbook (for example, raises one faucet by 30% or halves your trade velocity) and asks you to predict by hand the new `W*`, half-life and server average before you rerun the sheet. Then the examiner asks two questions from the [question bank](exam-bank.md), weeks 3, 4, 5, 6, 11, 13 or 14, with new numbers, chosen to touch your own design. Finally, you defend one design choice against an alternative you rejected.

## Rubric

M3 is scored out of 100, M4 out of 100. The marker picks the band that fits best within each criterion.

**M3: the spec**

| Criterion | Points | Excellent | Good | Weak | Missing |
|---|---|---|---|---|---|
| Targets and steady state (sections 1, 3) | 20 | 18-20: targets justified in player terms, `W*` and half-life hit within 5% in the simulation, server average reported for the expected stay | 12-17: targets hit, justification thin or server average missing | 5-11: targets stated but not hit, or `s` not split into its sources | 0-4: no steady state |
| Coverage of the course models (sections 2, 4-11) | 25 | 22-25: every section present with its required numbers, each computed by the right model | 15-21: one section thin or one model misapplied | 7-14: two or three sections missing or number-free | 0-6: most sections missing |
| Internal consistency | 15 | 13-15: numbers agree across sections (the same `N`, `τ`, `v`, prices and populations everywhere), every number traces to the workbook | 8-12: one or two mismatches | 3-7: several mismatches or typed results | 0-2: numbers do not trace |
| Sinks aimed at the right players (sections 5, 8) | 10 | 9-10: each sink's effect on `P` and on each cohort shown, at least one sink reaches low-velocity players, newcomers protected with a number | 6-8: incidence shown for most sinks | 2-5: sinks sized by gold removed only | 0-1: missing |
| Markets, reach and RMT (sections 6, 10, 11) | 10 | 9-10: per-class market choices tied to search cost and fees, core reward's `m` justified with the Lab 13 number, black-market band computed with your own inputs | 6-8: choices made, one part without numbers | 2-5: one market for everything, or RMT policy without the model | 0-1: missing |
| Telemetry and levers (section 12) | 10 | 9-10: six or more panels with alert rules, four or more lever rows with owners, age-segmented row present, each lever has an expected effect | 6-8: table complete, levers vague | 2-5: metrics listed without thresholds or levers | 0-1: missing |
| Stress tests and risks (section 13) | 10 | 9-10: all three scenarios with results and a named lever, two specific risks the model cannot see | 6-8: two scenarios, or generic risks | 2-5: one scenario | 0-1: missing |
| **Total** | **100** | | | | |

**M4: presentation and viva**

| Criterion | Points | Excellent | Good | Weak | Missing |
|---|---|---|---|---|---|
| Presentation | 25 | 22-25: within 8 minutes, every claim has a number on screen, the steady-state chart explained | 15-21: clear, a few unsupported claims or slight overrun | 7-14: hard to follow or mostly text | 0-6: not given |
| Hand prediction | 35 | 31-35: correct model, `W*`, half-life and server average within 2% of the rerun | 21-30: correct model, one arithmetic slip | 9-20: needs prompting to choose the model | 0-8: cannot predict |
| Bank questions | 20 | 18-20: both correct by hand, linked to the student's own design | 12-17: one correct, one with a slip | 5-11: one correct | 0-4: neither |
| Defending a choice | 20 | 18-20: names the rejected alternative and why, with numbers from the workbook | 12-17: defends the choice, alternative vague | 5-11: restates the choice | 0-4: cannot defend |
| **Total** | **100** | | | | |

The final spec grade is `0.05 × M1 + 0.20 × M2 + 0.55 × M3 + 0.20 × M4`, with M1 marked out of 100 on completeness (every item on the proposal list present) and M2 as the Lab 14 score scaled to 100.

## Rules

- Your workbook must reproduce the Lab 14 Tidewater check values when loaded with the starter inputs. Keep a copy of that sheet in the appendix.
- Every number in the spec and slides must trace to a cell or a script output.
- Late M3 submissions lose 10% per day and cannot be presented in the main session; you present in a make-up slot instead.
- If you use an AI tool or a classmate's code for any part, say which part in the appendix.

<details>
<summary>Marker checklist for internal consistency</summary>

- `N` in section 3 equals faucets minus flat sinks in the ledger, and `W* = N / s` with `s` equal to the sum of the proportional rates listed.
- The half-life is `ln 2 / s`. The server average uses `W* × (1 − (1 − e^(−sL)) / (sL))` with the same `L` as the Lab 14 `stay_days`.
- The fee in section 6 equals the `τ` in section 3, and the `v` used for `s` is plausible for the market design in section 6 (a high fee with high velocity is a warning sign, since a high fee lowers `v`).
- The farming wage `w` in section 2 is consistent with the faucet income in section 3 for the same play time.
- The coverage targets in section 8 use the same player population as the cohort table in section 5.
- The black-market band in section 11 uses a token gold price stated next to its ratio to a settled player's daily net income `N`, so the marker can judge whether it is plausible.

</details>
