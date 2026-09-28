# MMO401 · Final brief: agent-based economy and policy memo

**Weight:** 60% of the course grade.
**Due:** end of week 15, with a 15-minute viva during week 15.
**Builds on:** every lab, and most directly [lab 03](../labs/lab03.md) (the calibrated model), [lab 07](../labs/lab07.md) (the market module), [lab 13](../labs/lab13.md) (the report decomposition) and [lab 14](../labs/lab14.md) (the intervention spec).
**Lectures:** the model follows [weeks 2](../lectures/w02-agent-based-modeling-i.md) and [3](../lectures/w03-agent-based-modeling-ii.md). The memo follows [week 13](../lectures/w13-reading-an-economic-report.md) for the diagnosis and [week 14](../lectures/w14-intervention-design.md) for the spec.

## What you are making

You are the in-house economist of an invented MMO. The producer hands you a problem, in numbers. You build an agent-based model of the economy, check it, use it to test interventions, and write the one-page memo that tells the producer what to ship, what it will do, who pays, and what would make you reverse it. Then you defend both in a viva.

This is the week 1 job description done end to end. Measure, diagnose, advise. The model is the evidence. The memo is the decision.

## The problem you choose

In week 9 the course team publishes four [scenario cards](scenario-cards.md). Each card describes an invented game with a ledger, a price basket, a player count and six months of report data in the week 13 format, and ends with the producer's question. Choose one by the week 10 milestone.

| Card | The producer's question |
|---|---|
| A. Starter squeeze | New players say they cannot afford their first gear. Is the economy inflating, and what do we change? |
| B. The top pulls away | The money supply is flat but the richest accounts keep growing. Do we need a new sink, and what shape? |
| C. Frontier shortage | Frontier prices sit far above the hub since the border war started. Is hauling broken, and what do we change? |
| D. The token climb | The token's gold price rose 40% in two quarters. Is that inflation, and should we act? |

You may propose your own scenario instead. It must be an invented game with invented numbers, come with a ledger and six months of report data you write yourself, and be approved by the week 10 milestone. Do not base the numbers on a real game's data. You may cite shipped games as precedent, with version or era, only for facts the lectures already cite.

## Deliverables

### 1. The model (code)

A Python agent-based model, runnable with `python3` and the standard library (`matplotlib` allowed for charts). It must contain:

- **Agents.** At least 1,000 player agents with their own wallets, and at least two player types that differ in behavior (for example gatherers and traders, or cash-rich and time-rich players).
- **Money flows.** At least two faucets and two sinks, including at least one flat and one proportional rule (week 3). Every flow is logged by category.
- **A market.** The lab 07 clearing model with a tax and a bypass channel, or the lab 05 order book. Players trade through it at prices it sets.
- **One scenario module** that fits your card. Card A usually needs a price basket and new-player agents joining over time. Card B needs a proportional faucet and a wealth observer. Card C needs the lab 09 regions and haulers. Card D needs the lab 11 token market. Other modules from the course (lab 06 manipulation agents, lab 08 bank, lab 10 loss rules) are welcome if they bear on the question.
- **A ledger check.** `M_end = M_start + faucets − sinks`, asserted at every tick, with `M` counted from wallets, not from the flows (week 12).
- **Observers.** Money supply, money per active player, at least one price index on a named basket (week 1), velocity, the Gini, the median balance, and whatever your card's question needs.
- **Seeds.** A private generator per run, one place in the file for the seed list, and common random numbers across policies.

A README of at most one page says how to run the verification tests, the baseline, each policy experiment and each chart, and how long each takes.

### 2. The model report

At most 8 pages plus tables, in the four-part format from week 3 section 5.

1. **Overview.** Purpose in one sentence. Agents, their state and types. What one tick means in game time, and why.
2. **Rules.** Every rule as an equation or pseudocode, with each parameter's value and its status: calibrated (from the card, with the row it came from), assumed (with a reason), or swept (with the range).
3. **Tests.**
   - Verification: the ledger check, and at least two unit tests with known answers, such as the week 3 four-player tick or the week 7 discrete-book count.
   - Validation: with every policy switched off, the settled Gini is near the random-exchange baseline of about 0.5. Also show that the calibrated model reproduces at least two patterns from the card's six months of data (for example money growth and the direction of the price index).
4. **Results.**
   - Baseline and at least three interventions, using at least two different lever types from the week 14 table.
   - Each result as a mean with a 95% interval, from at least 20 replications with common random numbers.
   - For each intervention, the path of the target metric at 30, 90 and 180 days, under at least two values of the behavioral parameter your lever depends on (for example the tax elasticity `ε`, the bypass cost `E`, or the token-use share `s`).
   - A one-at-a-time sensitivity sweep on at least three parameters, and one structural test that changes a rule's shape (week 3 section 4).
   - One sentence for every finding that would change the recommendation.

### 3. The policy memo

One page, in the seven-part spec format from week 14 section 5. Add these to what that format already asks for.

- **Diagnosis** opens with a five-line reading of the card's latest month (week 13 section 4). It uses the stock-flow identity and the equation of exchange, and it quotes at least one index with its basket (week 1).
- **Prediction** comes from your model, with intervals, not from the closed-form formulas alone. Where the closed form exists (for example `M* = F / (τv)`), show that the model agrees with it or explain why not.
- **Incidence** has one line per player group and one line for at least one player-run institution the change touches. Examples are market makers and their break-even spread (week 5), a producer cartel (week 6), a player bank's honesty ceiling (week 8) or hauling corporations (week 9). Give a number for the institution line.
- **Kill criteria** are numeric and dated, and at least one of them tells apart the two behavioral parameter values you forecast under.

A memo longer than one page is marked on its first page only.

### 4. The viva

Fifteen minutes in week 15, with two examiners.

- **Five minutes, live run.** An examiner changes one parameter or seed in your model. Before it runs, you predict which way two outputs will move and roughly how far. Then you run it and explain any surprise.
- **Ten minutes, questions.** Two or three questions in the style of the [exam bank](exam-bank.md), rewritten with numbers from your own model and memo. Expect at least one compute question you answer on paper with a lecture model, and at least one critique of your own recommendation.

## Milestones

| When | Milestone | Graded? |
|---|---|---|
| Week 9 | [Scenario cards](scenario-cards.md) published | — |
| End of week 10 | Proposal, at most one page: chosen card (or your own, for approval), the scenario module you will add, the tick length, and the four-part overview in draft | No, but required. Feedback within a week |
| End of week 12 | Checkpoint. In a lab session, show the ledger check and the validation run passing on the calibrated baseline. A marker signs it off or tells you what is wrong | No, but required before the final deadline |
| Start of week 15 | [Lab 14](../labs/lab14.md) spec submitted as the memo's first draft | Graded in the ABM labs |
| End of week 15 | Model, README, model report and memo submitted | Yes |
| Week 15 | Viva | Yes |

The final deadline is fixed. Free extensions from the [ABM labs brief](abm-labs-brief.md) do not apply. A student who misses the week 12 checkpoint must book a make-up session before the end of week 13.

## Rules

- Work alone on the model, the report and the memo. You may reuse your own lab code and any course reference solution, and you must say which files.
- Every number in the memo must trace to a table or chart in the report, and every table in the report must be reproducible from the README.
- Use only invented data for the game. The scenario cards are fictional, and so is any scenario you write yourself.
- No copyrighted art, logos or characters in charts or documents.

## Rubric

Marked out of 100 and scaled to 60% of the course grade.

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Model structure and verification | 15 | 14-15: every required part present, ledger asserted every tick with `M` counted from wallets, two meaningful unit tests pass, seeded reruns identical | 11-13: all parts present, one test trivial or the ledger checked only at the end | 8-10: a required part missing, or tests weak | 0-7: ledger fails, code does not run, or the model is not agent-based |
| Calibration and validation | 10 | 9-10: every parameter tagged calibrated, assumed or swept with its source, baseline Gini near 0.5 with policies off, two card patterns reproduced | 7-8: calibration complete, one validation check missing | 5-6: several parameters untagged, validation thin | 0-4: no calibration table or no validation |
| Experiments and results | 15 | 14-15: baseline and three or more interventions of two lever types, 20 or more replications with common random numbers, intervals on every result, paths at 30, 90 and 180 days under two behavioral values | 11-13: all runs done, one comparison without intervals or one behavioral value missing | 8-10: fewer than three interventions, or single runs | 0-7: no policy comparison |
| Sensitivity and structural test | 10 | 9-10: three or more one-at-a-time sweeps and one structural test, with each finding that would flip the recommendation stated | 7-8: sweeps done, structural test missing or its impact unstated | 5-6: one or two sweeps, no decision impact | 0-4: none |
| Model report | 5 | 5: four parts complete, another student could rerun every table from the README | 4: one part thin | 3: two parts thin | 0-2: missing or unreproducible |
| Diagnosis | 10 | 9-10: five-line reading correct, both identities used, index quoted with its basket, residual addressed | 7-8: identities used, one line vague or the basket missing | 5-6: diagnosis from one chart, no decomposition | 0-4: no diagnosis, or it contradicts the card's numbers |
| Intervention and forecast | 10 | 9-10: lever sized from the model, alternatives rejected with numbers, model checked against the closed form, forecasts with intervals under two behavioral values | 7-8: lever sized, one alternative or one behavioral value missing | 5-6: lever chosen with a forecast from the closed form only | 0-4: lever without a size or a forecast |
| Incidence, institutions and kill criteria | 10 | 9-10: one line per player group, an institution line with a number, rollout dated, numeric kill criteria that separate the behavioral values | 7-8: incidence complete, kill criteria numeric but do not separate the values | 5-6: incidence partial or criteria not numeric | 0-4: missing |
| Viva | 15 | 14-15: live prediction right in direction and close in size, surprises explained from the model, bank-style questions answered with correct numbers | 11-13: prediction right in direction, one answer needs prompting | 8-10: prediction wrong but the reason found, answers partly correct | 0-7: cannot explain own model or numbers |

A submission whose memo contains a number that does not appear in the report, or whose report contains a table the README cannot reproduce, loses up to 5 points under the criterion that number belongs to.
