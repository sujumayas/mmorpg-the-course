# MMO308 · A/B report brief: one experiment, designed and then read honestly

**Weight:** 20% of the course grade.
**Assigned:** week 5, with Lab 05. **Milestone:** the Lab 05 plan (end of week 5) is marked as a lab and returned with written feedback on its design. **Final submission:** start of week 9, followed by a 10-minute viva in the week 9 lab session.
**Work mode:** the same pair as Labs 05 and 06, with a signed contribution statement. In the viva each partner answers alone.
**Lectures:** [week 5, A/B testing: design](../lectures/w05-ab-testing-design.md) and [week 6, statistics and pitfalls](../lectures/w06-ab-testing-statistics-and-pitfalls.md) most directly, plus [week 3](../lectures/w03-cohorts-and-retention-curves.md) (complete cohorts, standard errors), [week 4](../lectures/w04-funnels-and-churn.md) (time to reach a metric) and [week 7](../lectures/w07-segmentation.md) (pre-registered segments).

## What this component is for

It assesses the course outcome "run and analyze A/B tests correctly". The labs test each tool alone. This report asks for the whole chain, from the question to the decision, done twice. Once as the designer of a test for a change you chose, before any data exists. Once as the analyst who inherits someone else's test, with a peeked win, a broken split and a producer who wants to ship.

A report that says "B won with `p = 0.03`" earns little here. A report that states the unit and why, the design effect, the MDE the test can actually see, the stopping rule and its simulated error rate, the SRM result before any metric, and what the team should do next, earns a lot.

## What you hand in

One report, `ab-report.pdf`, of at most 3,000 words plus tables and figures, and a code folder that reproduces every number in it.

### Part 1: the plan (your change)

Start from your Lab 05 plan and revise it with the feedback you received. It keeps the eight parts of the week 5 plan: hypothesis, variants, unit, population and trigger, primary metric, guardrails, MDE and duration, and decision rule. Three things are required beyond Lab 05.

1. **The unit argued from interference.** Name the path by which a treated player could change a control player's outcome in your game (trade, grouping, a shared market, chat, a leaderboard). Choose the smallest unit that contains it. If the only honest unit is the whole game, say so and propose a switchback or a before-and-after design with its weaknesses listed.
2. **Sizing with the design effect.** Use your own estimate of `ρ` (from Lab 05's `icc_from_clusters`, or a stated assumption with a range) to compute `deff`, `n_eff`, the MDE and the duration in whole weeks, plus the time the last cohort needs to reach the metric. Give the MDE for your chosen unit and for the next smaller one.
3. **A stopping rule you have tested.** Choose one of the three honest options from week 6: one planned analysis, `K` planned looks with a boundary you found by simulation, or an always-valid method with its reference. If you plan looks, find your boundary by simulation with your own code, and report its false-positive rate and its power at your MDE from at least 50,000 simulated tests each, with the seed. Do not copy published boundary constants. Show the numbers your code produced.

### Part 2: the analysis (the Lab 06 experiment)

Start from your Lab 06 write-up for the crafting-station test in `experiment_daily.csv` and turn it into the analysis a producer can act on.

1. **Checks before results.** The SRM test on the totals and day by day, with `chi²` and `p`, and your explanation of the cause. State whether the test is readable at all.
2. **Three readings of the same data.** The day a naive daily peek would have stopped, what your sequential boundary from Lab 06 says at each look, and the planned single analysis at day 14. Show them on one chart of `z` by day with the 1.96 line and your boundary drawn.
3. **The mechanism.** Explain, with numbers from the data, how the missing players in one arm produced the apparent lift and why the bias favoured B.
4. **Metrics that lie.** Say whether novelty or whale effects could matter for this metric, and what you would plot to check.

### Part 3: the decision and the rerun

1. **Recommendation.** One paragraph to the producer who asked "B was significant on day 4, why haven't we shipped it?". It must answer that question with numbers and say what the team should do now.
2. **Rerun plan.** A short plan (the eight parts, one line each) for rerunning the crafting-station test, with the changes to the plan and to the client that would prevent the same failure. Size it with Lab 05's functions.
3. **What you would read by segment.** At most three pre-registered segments for the rerun, each defined by an attribute fixed before exposure, with the chance that at least one shows a false win.

### Code folder

Your Lab 05 and Lab 06 code, the simulation for Part 1 step 3, and a `README.md` with the exact command behind every number, table and figure. Everything runs with `.venv/bin/python` and the standard library. Every random process takes a seed.

## Milestone

The Lab 05 plan is marked as Lab 05 in the [analytics labs](analytics-labs-brief.md) and returned with design feedback by the end of week 6. The feedback names the two weakest parts of your plan. The final report is marked on whether those parts were fixed, so keep the feedback and answer it in a short "Changes since Lab 05" table at the start of Part 1.

## Rubric

| Criterion | Excellent (full marks) | Adequate (about half) | Weak (little or none) | Points |
|---|---|---|---|---|
| Unit, trigger and hypothesis | Interference path named and the unit follows from it; trigger happens the same way in both arms and before the outcome; hypothesis names change, metric and direction; Lab 05 feedback answered | Unit reasonable but not argued from interference, or trigger could differ between arms | Unit by habit (player) where interference is obvious, or trigger is the outcome | 15 |
| Metrics, MDE and duration | Primary and guardrails defined exactly; `ρ` estimated or bounded; `deff`, `n_eff` and MDE correct for two units; whole weeks plus the metric window | Sizing correct but ignores clustering, or duration not in whole weeks | No sizing, or MDE from the raw `n` of a clustered test | 15 |
| Stopping rule tested by simulation | Rule stated in advance; boundary found with own code; false-positive rate and power reported with run count, seed and margin | Rule stated, simulation thin or run count too small to support the claim | Peeking with no rule, or constants copied without a check | 15 |
| Checks and three readings (Lab 06 data) | SRM overall and by day with the cause identified; naive stop day, sequential decision and planned result all correct and on one chart | Two of the three readings correct, or SRM computed without a cause | Metric read before the split, or naive stop day reported as the result | 20 |
| Mechanism and metric traps | The path from missing players to a biased lift explained with the data's own numbers; novelty and heavy-tail risks assessed for this metric | Mechanism described in words only | Missing | 10 |
| Decision and rerun plan | Clear recommendation the producer can follow; rerun plan sized and fixing the cause in both plan and client; segments pre-registered with the false-win chance | Recommendation clear, rerun plan vague or unsized | No decision, or "ship B" | 15 |
| Writing and reproducibility | Plain, numeric, within the word limit; every number reproducible from the README commands with stated seeds; help acknowledged | Some numbers without a command, or over length | Numbers cannot be reproduced | 10 |
| **Total** | | | | **100** |

## Viva

In the week 9 lab session each student gets 10 minutes and three questions in the style of the [exam bank](exam-bank.md) week 5 and 6 sections, rewritten with the report's own numbers. For example, "Your plan randomizes by guild with `ρ = 0.04`. What happens to your MDE if guilds are twice as large?" or "Your boundary gives 5.1% in simulation. How many runs would you need to tell it apart from 5.5%?" The viva confirms authorship. It can move the mark down by at most 20 points if a student cannot explain their own report, using the same Full, Partial, Weak and None scale as the lab spot checks.

## Late work and integrity

The report is accepted up to 7 days late and marked out of 60. After that it is marked for feedback only. Extensions follow university policy. You may use lecture and lab code freely and must acknowledge any other help in one line. Simulated rates, boundaries and power figures must come from your own runs, with seeds.
