# MMO304 · Telemetry lab brief

**Weight:** 20% of the course grade.
**Week:** 12 (lab session and checkpoint), with the submission and incident briefing in week 13.
**Work mode:** individual. The checkpoint may be done in pairs in the lab room, but the submission and briefing are your own.
**Tools:** Python 3 with pandas (or numpy) and matplotlib. A spreadsheet is accepted for the checkpoint only.

## The job

You are the economist on the live team of a fictional MMO server. Fifty-six days of ledger data, balance snapshots and auction prices have landed on your desk. The patch notes list two content updates. The data hold three more events that nobody documented. Build the dashboard from the [week 12 lecture](../lectures/w12-economic-telemetry-and-dashboards.md), section 5, find the incidents, estimate what each cost the economy in gold, and brief the producer so that the right team acts on each one.

The task and data are in [Lab 12: Economy telemetry](../labs/lab12.md): [`lab12-ledger.csv`](../labs/lab12-ledger.csv), [`lab12-snapshots.csv`](../labs/lab12-snapshots.csv) and [`lab12-prices.csv`](../labs/lab12-prices.csv). This brief adds the milestones, the briefing and the full rubric.

It draws on week 3 (faucets, sinks and transfers), week 4 (money per player and price indices), week 5 (velocity and hoards), week 11 (bots are a faucet) and week 12 (reconciliation, indices, denominators and concentration).

## Deliverables

1. **Notebook or script** that runs from the three CSV files with one command and regenerates every number and chart. Put the command in a README.
2. **Dashboard,** one page, five panels (steps 1-5 of the lab): supply and reconciliation gap, faucets and sinks with the sink/faucet ratio, supply and flows per active player, faucet concentration, and price indices with the average transaction price. Under each panel write its metric, cadence and alert rule, and annotate the day 15 and day 29 patches.
3. **Incident report,** 600-900 words, for the live producer. One section per incident with the days it covers, the panel that shows it first, the numbers that prove it, the estimated gold impact with the method, the most likely cause, and one action with a named owner (a team, not "the studio"). End with one change to the telemetry itself that would have caught the incidents sooner.
4. **Alert log,** a table listing every day on which any of your alert rules fired, with the rule and the value. False alarms stay in the table with a one-line note.

## Milestones

| When | Milestone | Share of this 20% |
|---|---|---|
| End of the week 12 lab session | M1 checkpoint: ledger-predicted supply, daily reconciliation gap and the faucets-and-sinks panel for all 56 days, shown to the lab tutor | 10% |
| Start of week 13 | M2 submission: all four deliverables | 75% |
| Week 13 lab session | M3 incident briefing, 8 minutes per student | 15% |

The M1 checkpoint is marked pass (full 10%), partial (5%) or not shown (0%). A pass needs the day 1 supply of 404,449,262 and a gap series that first exceeds 0.1% of supply on the correct day. Tutors give feedback on the spot, so a student who is stuck on reconciliation leaves the room unstuck.

## The incident briefing (M3)

You brief the examiner, playing the live producer, for 8 minutes.

1. **Three minutes of briefing.** Walk through your three incidents in order of cost. One number per incident, one action per incident.
2. **Day 57 card.** The examiner hands you a card with a new day of data and asks what your dashboard says about it. The standard card is below. Examiners may change its numbers.
3. **Two bank questions.** One from weeks 4 or 5 and one from week 12 of the [question bank](exam-bank.md), with new numbers, answered by hand.

**Standard day 57 card**

| Item | Value |
|---|---|
| Snapshot, end of day 56 | 885,866,185 |
| Ledger faucets, day 57 | 44,900,000 |
| Ledger sinks, day 57 | 38,100,000 |
| Snapshot, end of day 57 | 894,166,185 |
| `ah_fees`, day 57 | back to its days 15-46 level |
| Mob-loot `top1pct_share`, day 57 | 0.06 |

<details>
<summary>Examiner check values for the day 57 card</summary>

Ledger-predicted end of day 57 is `885,866,185 + 44,900,000 − 38,100,000 = 892,666,185`. The snapshot exceeds it by 1,500,000, about 0.17% of supply, so the reconciliation alert fires. The gap had been flat at 12,000,000 since day 39, so this is 1.5 million of fresh unlogged gold in one day, and the cumulative gap is now 13.5 million. A strong answer says the exploit from incident 3 has reopened or a second one has started, that concentration is normal so this is not bots, and that the fee sink looks repaired. The action is to page the engineering owner of the exploit fix and pull the accounts whose balances grew most since day 56.

</details>

## Rubric

M2 is scored out of 100 and M3 out of 100. The marker picks the band that fits best within each criterion. Lab 12's instructor check values are the reference for M2.

**M2: submission**

| Criterion | Points | Excellent | Good | Weak | Missing |
|---|---|---|---|---|---|
| Supply and reconciliation | 15 | 13-15: ledger supply correct to the gold on every day, gap computed daily, alert days listed and matched to incident 3 | 9-12: correct method, minor arithmetic error or plot missing | 4-8: gap computed on some days only, or against the wrong starting supply | 0-3: not attempted or wrong method |
| Dashboard panels | 25 | 22-25: all five panels correct and readable, patches annotated, metric, cadence and alert rule under each | 15-21: one panel unlabelled or one alert rule missing | 7-14: two panels missing or misleading | 0-6: fewer than three panels |
| Denominator analysis | 10 | 9-10: identifies the `ah_fees` per active player dip in days 29-42 as a denominator effect from bots counted as active, with numbers | 6-8: notices the effect, numbers thin | 2-5: mentions denominators in general only | 0-1: missing |
| Price indices | 15 | 13-15: average, Laspeyres and Paasche correct, week 5 read correctly as a mix shift on top of about 5% real inflation | 9-12: numbers correct, reading weak | 4-8: one index wrong | 0-3: wrong formulas |
| Incidents found | 20 | 18-20: all three found with correct days, first panel, proving numbers and cause | 12-17: all three found, one with weak evidence, or two found well | 5-11: one found well | 0-4: none |
| Report, damage estimates and alert log | 15 | 13-15: owner and action per incident, estimates with method shown and within about 10% of the check values, a sound telemetry change, complete alert log | 9-12: estimates present but method thin, or log incomplete | 4-8: actions vague and no estimates | 0-3: unusable for a producer |
| **Total** | **100** | | | | |

**M3: incident briefing**

| Criterion | Points | Excellent | Good | Weak | Missing |
|---|---|---|---|---|---|
| Briefing | 30 | 26-30: within 3 minutes, incidents ordered by cost, one number and one owner each | 18-25: clear, one incident without a number or owner | 8-17: runs long or reads the report aloud | 0-7: not given |
| Day 57 card | 40 | 35-40: computes the gap by hand, says the alert fires, separates exploit from bots using concentration, names an action and owner | 24-34: correct gap, diagnosis partly right | 10-23: needs prompting to reconcile | 0-9: cannot read the card |
| Bank questions | 30 | 26-30: both correct by hand with the model named | 18-25: one correct, one with a slip | 8-17: one correct | 0-7: neither |
| **Total** | **100** | | | | |

The telemetry grade is `0.10 × M1 + 0.75 × M2 + 0.15 × M3`, with M1 as 100, 50 or 0.

## Rules

- The notebook must run unchanged on the CSV files as shipped. Hand-edited data or typed numbers in the dashboard cost the reproducibility part of the relevant criterion.
- Every number in the report must appear in the notebook's output.
- The data are synthetic. Do not compare them with any real game. If you use a real-game example in the report to explain a point, cite it with the version or date from a course lecture.
- Late M2 submissions lose 10 points per day. A student who misses M3 briefs in a make-up slot within a week.
