# PR402 · Launched game brief 4: economy review

**Weight:** 6% of the course grade, inside the launched game component (40%).
**Assigned:** week 12. **Due:** before the week 14 studio meeting, in `production/week13/`.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide:** [week 13, economy review](../lectures/w13-economy-review.md). **Lab:** [13](../labs/lab13.md).

## What this milestone proves

That the team reads its live currency ledger per active player, checks its model against the database, and turns four weeks of data into one decision with a number attached. The economy review is operations work on the launched game, so it sits in the launched game component. It is marked on reading and deciding, not on whether your economy turned out healthy.

"We measured it and chose not to change it" is a legitimate outcome ([week 13, section 3](../lectures/w13-economy-review.md)) if the argument is written down with the level of growth at which the team would act.

## Gates

- **G1. Ledger from queries.** Faucet, sink, active-account and active-held figures come from queries the team can run in front of the instructor. Figures typed in from a dashboard screenshot do not count.
- **G2. Configuration only.** Any change shipped is a parameter in configuration (a reward amount, a fee rate), not a new system. Week 13 is too late for new systems.

## Deliverables

1. **Lab 13 worksheet**, parts A to D, with `ledger.csv`, `review.py` and `review-output.txt`.
2. **The economy review**, at most two pages: the weekly table per active player, the model check against active-held currency, the growth target `g` with its reason, at least three costed options (one with a behavioural response), and the decision.
3. **The decision in intervention-spec form**: the change and its values, who pays (checked against the week 11 cohort table), the announcement text, the metric with its expected value and check date, and the rollback. Or no change, with the action level.
4. **If shipped**: the configuration diff, the patch note and the build tag.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Ledger | Currency event table grouped by week and source | Reruns the faucet and sink query for one week |
| Denominator | Weekly active accounts query, with bot and alt handling stated | Checks accounts, not characters, are counted |
| Model check | `active_held` query per week | Compares `m × N` with `active_held`; any gap over 10% must be explained |
| Prices | Median stall price for three traded items per week | Reruns one price query |
| Script | `review.py` | Runs it; output must match `review-output.txt` and the worksheet |
| Cohorts | Week 11 cohort table | Checks the "who pays" claim against which cohorts still earn from the lever |
| Build | Tag and configuration diff, if a change shipped | Checks the diff matches the spec values and the patch note |

## How it is marked

The instructor marks the folder before the week 14 meeting and asks each team for its headline number, decision and reason in the two-minute stand-up at the end of the week 13 meeting. The lab 13 rubric is the detailed scoring guide for rows 1 to 4.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Ledger table and script | 20 | Every week since launch; `F`, `S`, net, `S / F`, `N`, net per player, `m`, total stock and prices; script runs and matches | Weeks missing; table typed by hand |
| Per-player reading | 15 | The review states the change in wealth per active player and explains any gap between that and the totals | Only totals and the sink ratio read; "the economy is settling" |
| Model check | 15 | `m × N` compared with `active_held` for every week; gaps over 10% explained with evidence | Model trusted without a check |
| Target and options | 20 | `g` set with a reason before options were run; three or more options costed; one with trade lost to the fee or a similar named reaction | Fee sized as if nobody reacts |
| Decision | 20 | Change, values, who pays, announcement, metric with expected value and check date, rollback; or no change with an action level | Decision with no metric or no rollback |
| Clarity | 10 | Two pages or fewer; a reader outside the team can follow it | A data dump with no decision on page one |
| **Total** | **100** | | |

## Builds on

- [PR401 week 8, economy and balance design](../../PR401-capstone-i-pre-production/lectures/w08-economy-and-balance-design.md) (the design numbers the ledger is read against).
- [PR101 week 13, builds and release checklists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md) (a configuration change still goes through the checklist).
- [MMO302 week 7, persistence strategies](../../MMO302-mmo-server-architecture/lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md) and [week 8, item ownership and transactional integrity](../../MMO302-mmo-server-architecture/lectures/w08-item-ownership-and-transactional-integrity.md) (why the ledger can be trusted, or why a gap may be a duplication bug).
- [MMO308 week 3, cohorts](../../MMO308-live-operations-analytics-and-experimentation/lectures/w03-cohorts-and-retention-curves.md) and [week 12, economy monitoring](../../MMO308-live-operations-analytics-and-experimentation/lectures/w12-economy-monitoring.md).
- [MMO407 week 6, duplication exploits after launch](../../MMO407-launch-scaling-and-post-mortems/lectures/w06-case-duplication-exploits-after-launch-new-world-2021.md) (what a ledger gap can mean).
- Also [MMO304 week 12](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w12-economic-telemetry-and-dashboards.md) and [MMO401 week 14](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w14-intervention-design.md) for the ledger and the intervention spec.
