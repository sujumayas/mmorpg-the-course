# PR301 · Milestone 5 brief: telemetry review

**Weight:** 7% of the course grade, inside the milestones component (50%).
**Assigned:** week 9. **Due:** 48 hours after the week 10 studio session, in `production/week10/`.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide:** [week 10, telemetry review](../lectures/w10-telemetry-review.md). **Lab:** [lab 10](../labs/lab10.md).
**Builds on:** [DB201 week 10](../../DB201-data-persistence-and-telemetry/lectures/w10-telemetry-design-events-and-properties.md) (event design), [DB201 week 11](../../DB201-data-persistence-and-telemetry/lectures/w11-pipelines-collect-store-query.md) (where pipelines lose events), [DB201 week 12](../../DB201-data-persistence-and-telemetry/lectures/w12-dashboards-and-kpis.md) (dashboards and KPIs), [MMO304 week 4](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w04-money-supply-per-capita-and-inflation.md) (money supply), [MMO304 week 12](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w12-economic-telemetry-and-dashboards.md) (economic telemetry), [MMO308 week 3](../../MMO308-live-operations-analytics-and-experimentation/lectures/w03-cohorts-and-retention-curves.md) (retention), [MMO308 week 12](../../MMO308-live-operations-analytics-and-experimentation/lectures/w12-economy-monitoring.md) (economy monitoring), [MMO309 week 11](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w11-exploit-response-rollback-vs-ban.md) (exploit response), [MMO302 week 7](../../MMO302-mmo-server-architecture/lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md) (what a periodic save loses, or gains) and [PR201 week 11](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w11-playtest-and-telemetry-review.md) (count checks and Wilson intervals).

## What this milestone proves

That the team can read what its world did over a weekend and tell a measurement from a hope. The centre of the review is the ledger equation from week 7. The residual `(M_end − M_start) − (Σ faucets − Σ sinks)` is either zero or fully explained, by time and by character, with each explanation predicting its own size. The *Saltmarsh* residual of 8,177 copper broke down into 620 of unlogged starter copper, 7,500 from a mail dupe opened by crashes, and 57 of rounding. That is the standard.

## Deliverables

1. **Telemetry review report** with, in this order: count checks (sequence gaps, sessions closed at crash time, bots excluded); stability (every restart with cause, loss window and whether the runbook worked; p99 tick by hour); concurrency (measured `I`, `s`, `k`, `W` and `e` beside the week 9 plan, and the beta sign-up estimate that follows); return rate with its Wilson interval; the economy section.
2. **Ledger reconciliation** in the lab 10 format, passing `check_ledger.py`: money supply over every place currency lives, the residual by hour and by character, and each cause with its predicted size.
3. **Budget against actuals** per player-hour, every line outside 0.75 to 1.25 of plan with a finding.
4. **Ranked sprint 4 input list** with ticket IDs, evidence and sizes, class-of-bug fixes above instance fixes.
5. **Exploit response record**: what was found, what was corrected (as logged ledger lines), and what happened to the players involved under the policy published before the weekend.
6. **The queries** used, in `production/week10/queries/`.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Telemetry export | The untouched M4 export | Recounts sequence gaps and bot accounts |
| Final backup | Database backup from Sunday 18:00 | Reruns one per-character query against it |
| Ledger | Ledger export and `check_ledger.py` output | Reruns the checker; recomputes the total residual by hand |
| Server logs | Weekend logs with crash times | Matches steps in the hourly residual to crashes or patches |
| Session data | Logins and logouts, humans only | Recomputes `s`, `k` and `W` |
| Playtest notes | Bug channel, report channel, observer notes | Checks that the earliest report of each finding is cited |

## How it is marked

The instructor reads the report and reruns the lab. The readout at the end of the session is not marked, but a team that shares a failure pattern there helps the whole cohort, and the instructor notes it for the peer rating's shared-work criterion. A report whose residual is not fully explained can still score well if the open items are named and each has a test that would settle it.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Count checks first | 10 | Sequence gaps, closed sessions and bot exclusion reported before any total, with what each means for trust | Charts before counts; bots mixed in |
| Stability | 10 | Every restart with cause, loss window and runbook outcome; p99 by hour against the week 6 limits | Crashes missing or unexplained |
| Concurrency and beta estimate | 12 | Measured rates from session telemetry; model rerun; beta sign-up estimate stated as an expected value to be corrected in week 13 | Plan figures reused; no link to the beta |
| Return rate | 5 | Reported with its Wilson interval and without comparison to shipped games | A bare percentage compared with a commercial game |
| Money supply | 10 | Every place from the lab 07 list, taken from the final backup | Character balances only |
| Residual decomposition | 20 | By time and by character; every cause's size predicted independently and matching; residual explained or open items named with a test | "Probably rounding" without a predicted size |
| Budget findings | 10 | Every out-of-band line explained; guesses replaced by measurements | Misses blamed on players |
| Ranked input list | 13 | Class-of-bug fix (for example, write-through on both sides of every transfer) ranked above instance fixes; ticket IDs and sizes | Symptoms listed; no ranking |
| Exploit response | 10 | Corrections logged as ledger lines (a correction sink); player response follows the published policy | Silent edits to balances, or a response invented after the fact |
| **Total** | **100** | | |

## Late and missing work

Up to 48 hours late is capped at 70. A team whose weekend evidence was wiped submits the review with the data it has, and the rows that depend on the missing data score 0.
