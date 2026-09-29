# PR402 · Milestone 3 brief: closed beta

**Weight:** 7% of the course grade, inside the milestones component (40%).
**Assigned:** week 4. **Due:** the beta plan and tester pages at the end of the week 5 meeting; the beta report at the start of week 6.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide:** [week 5, closed beta](../lectures/w05-closed-beta-recruiting-and-stress-windows.md). **Lab:** [05](../labs/lab05.md).

## What this milestone proves

That the team can put enough real players on its server at the same moment to test the launch-evening peak, and can run a week of outside testing with consent, a feedback channel and a daily triage loop. The closed beta has three questions to answer ([week 5, section 1](../lectures/w05-closed-beta-recruiting-and-stress-windows.md)): does the server hold the evening peak, do the systems hold together over days, and which of the team's guesses were wrong.

The mark rewards an honest report more than a good-looking one. A window that reached 35 players, reported as 35 with the reason, scores better than a window reported as 60 with 25 bots mixed in.

## Gates

- **G1. Consent before invites.** The consent notice, code of conduct and wipe notice are live in the launcher before the first invite batch goes out. Telemetry uses game-generated player IDs only, and the invite list with contact details is stored in one restricted place ([week 5, section 3](../lectures/w05-closed-beta-recruiting-and-stress-windows.md)). A beta that fails this gate scores 0 for the milestone until it is fixed, and the instructor may pause the beta.
- **G2. Humans and bots apart.** Every concurrency figure in the report states real players and bots separately.

## Deliverables

1. **Beta plan** in the lab 05 format: target concurrency tied to your week 3 evening peak, funnel rates with sources, invite batches, two stress windows on different days. Checker `PASS`, with `check-output-plan.txt`.
2. **Tester pages**: consent notice, code of conduct, wipe notice and FAQ, with links.
3. **Invite text** showing the window times.
4. **Triage rota** naming who runs the morning triage each day, and the single feedback channel.
5. **Beta report**, one or two pages, due at the start of week 6: measured `p_start` and `p_window` (with `check-output-measured.txt`), peak CCU in each window with server metrics at that moment, total player-hours and the rule-of-three bound, the updated bug list, and the measured ops tax for week 5.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Funnel | Invite log, first-session query, per-window login query | Recomputes `p_start` and `p_window` from the raw queries |
| Window telemetry | Dashboard export for each window: CCU, tick time, memory, queue length | Checks the reported peak against the export and the time of any tick spike |
| Exposure | Session table query | Recomputes player-hours and the bound `3 / E` |
| Builds | Tags and deploy log for every build tested in the beta | Checks that every mid-beta deploy went through staging |
| Bug data | Tracker export with filing dates, reach telemetry from week 4 | Compares one S2's alpha reach guess with its measured reach |
| Tester mix | Recruitment log (source per batch, no personal data in the repo) | Checks at least half the planned testers were not friends or classmates |
| Ops tax | Time log for week 5 | Recomputes measured `t` |

## How it is marked

The instructor checks the plan and the pages at the end of the week 5 meeting, watches at least one window's dashboard live or from its export, and marks the report at the start of week 6. The lab 05 rubric is the detailed scoring guide for rows 1 to 3.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Target and funnel | 15 | Target tied to the week 3 forecast; rates sourced, then replaced by measured values after 24 hours | Target picked from thin air; guesses never updated |
| Batches and windows | 15 | Batch 2 sized from measured `p_start`; two announced windows on different days, 60 to 120 minutes | One batch; a single window; windows not announced |
| Tester pages and conduct | 15 | Consent, conduct and wipe notices live before batch 1; report command in game; at least half strangers | Pages added after testers joined; all friends |
| Window operations | 15 | One person on dashboards and one on chat in each window; peak CCU and tick-time spikes recorded with times | Nobody watching; spike found in logs days later |
| Daily triage | 10 | Morning triage each day by rota; gate bugs fixed through staging the same day where possible | Triage skipped; hotfixes pushed straight to production |
| Beta report | 20 | Measured rates, window peaks with metrics, player-hours, the bound and what it means for launch week, updated bug list, measured tax | "Stable" with no bound; bots counted as testers |
| Honesty about the gap | 10 | Any window short of target is reported with the shortfall, its cause and what was done | Shortfall hidden or blamed on testers |
| **Total** | **100** | | |

## Builds on

- [PR401 week 13, vertical slice sprint 2](../../PR401-capstone-i-pre-production/lectures/w13-vertical-slice-sprint-2.md) (exposure and the soak plan) and [PR401 week 8, economy and balance design](../../PR401-capstone-i-pre-production/lectures/w08-economy-and-balance-design.md) (the targets the beta starts to test).
- [PR101 week 10, bug tracking and QA basics](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md).
- [MMO302 week 11, load testing with bots](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) and [week 14, observability](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md).
- [MMO308 week 5, A/B testing design](../../MMO308-live-operations-analytics-and-experimentation/lectures/w05-ab-testing-design.md) (players as people) and [week 10, player feedback loops](../../MMO308-live-operations-analytics-and-experimentation/lectures/w10-player-feedback-loops-forums-surveys-polls.md).
- [MMO407 week 3, beta strategies](../../MMO407-launch-scaling-and-post-mortems/lectures/w03-beta-strategies.md) (exposure and the rule of three).
