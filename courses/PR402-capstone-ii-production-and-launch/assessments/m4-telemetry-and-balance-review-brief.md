# PR402 · Milestone 4 brief: telemetry and balance review

**Weight:** 7% of the course grade, inside the milestones component (40%).
**Assigned:** week 5. **Due:** before the week 7 studio meeting, in `production/week06/`.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide:** [week 6, telemetry and balance review](../lectures/w06-telemetry-and-balance-review.md). **Lab:** [06](../labs/lab06.md).

## What this milestone proves

That the team turns closed-beta telemetry into a short list of balance changes the data can defend, and says "we cannot tell yet" where the data is silent. The review is marked on method, not on whether your game turned out balanced. A team whose classes all come out "can't decide", with the open-beta tests to settle them planned and instrumented, can earn full marks.

Three things are checked above all ([week 6, sections 2 to 4](../lectures/w06-telemetry-and-balance-review.md)): the export was cleaned before anything was computed, every `n` counts players or parties and never events, and every change predicts a number that open beta will test.

## Deliverables

1. **Cleaning log**: internal accounts removed by ID, events split by build, count checks with numbers. The cleaning is a script in the repository.
2. **Balance review sheet** (`balance-review.csv`, lab 06 format): one row per numeric target in your PR401 balance document that the closed beta touched, with unit, `n`, interval, band, the date the band was set, and verdict. At least one party-level row.
3. **Balance change log**: for every `act` row, the lever, old and new value, the formula or simulator run, and the predicted metric. One lever per class.
4. **Targeted-test list for open beta**: every `cant_decide` row with the units needed, the telemetry event it requires and an owner. These items appear in the sprint 4 backlog.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Raw telemetry | Closed-beta export, unchanged | Repeats one count check from the raw export |
| Cleaning script | Code in the repository | Runs it on the raw export and compares event counts with the cleaning log |
| Build tags | Build number on every event | Checks that balance rows use one build only, or say how they were split |
| Targets | PR401 balance document, with dates | Checks every band against the document; bands set after the beta are marked `after-beta` |
| Intervals | `balance-review.csv` | Recomputes two rows to two decimals |
| Predictions | Change log, simulator commit or run ID | Recomputes one prediction from its formula or reruns the simulator |
| Backlog link | Sprint 4 board | Finds each targeted test as a backlog item with the same owner |

## How it is marked

The instructor marks the folder before the week 7 meeting and asks each team to defend one unit, one band and one change size in the pair review block. The lab 06 rubric is the detailed scoring guide for rows 2 to 5.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Question sorting | 10 | Questions sorted into answerable now, answerable per party with wide intervals, and not reached by the beta, with the last group moved to open beta or live ops | Every target treated as answerable |
| Cleaning | 15 | Accounts removed by ID, builds split, count checks balance; cleaning is a script that will run unchanged on week 8 data | Manual spreadsheet edits; developers left in the data |
| Units and arithmetic | 25 | Every `n` counts players or parties; per-player medians before means; two random rows recompute exactly | Kills or hits used as `n`; intervals that do not recompute |
| Bands and verdicts | 15 | Bands dated from PR401, none moved after the data; verdicts follow the act, leave, can't decide rule | Bands adjusted to fit the result; "can't decide" read as "leave" |
| Sized changes | 20 | Every `act` row has a lever, a model or simulator run and a predicted value inside the band; one lever per class; the choice of target within the band is argued | Changes sized by feel; several levers on one class |
| Targeted tests | 15 | Every `cant_decide` row has units needed, an event that fires, and an owner; items on the sprint 4 board | Test list with no sample sizes or no instrumentation |
| **Total** | **100** | | |

## Builds on

- [PR401 week 8, economy and balance design](../../PR401-capstone-i-pre-production/lectures/w08-economy-and-balance-design.md) (where your targets and bands come from).
- [PR101 week 13, builds and release checklists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md) (build identity on every event).
- [MMO302 week 14, observability](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md) (the event and log pipeline the export comes from).
- [MMO308 week 4, funnels and churn](../../MMO308-live-operations-analytics-and-experimentation/lectures/w04-funnels-and-churn.md) and [week 6, A/B testing statistics and pitfalls](../../MMO308-live-operations-analytics-and-experimentation/lectures/w06-ab-testing-statistics-and-pitfalls.md) (why the targeted tests stop at their planned sample).
- [MMO407 week 3, beta strategies](../../MMO407-launch-scaling-and-post-mortems/lectures/w03-beta-strategies.md) (what a closed beta can and cannot show).
