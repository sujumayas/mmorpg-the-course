# PR402 · Milestone 5 brief: open beta

**Weight:** 8% of the course grade, inside the milestones component (40%).
**Assigned:** week 7. **Due:** the sizing sheet, rota and kill-switch drill before the doors open in week 8; the full folder before the week 9 studio meeting, in `production/week08/`.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guides:** [week 7, production sprint 4](../lectures/w07-production-sprint-4.md) (readiness checklist) and [week 8, open beta](../lectures/w08-open-beta.md). **Lab:** [08](../labs/lab08.md).

## What this milestone proves

That the team sizes a public test from two numbers it can compute, the play needed to see rare bugs and the players its server can hold, and then runs a weekend the way it intends to run launch. The open beta is the last time you learn about your build without paying launch prices for it ([week 8](../lectures/w08-open-beta.md)). Its outputs are the inputs to launch: a forecast-against-actual table whose errors correct the launch forecast, and an exit review that recommends go or no-go.

## Gates

- **G1. Readiness evidence.** Every line of the week 7 open-beta readiness checklist has evidence attached before the doors open (load-test report at 1.5 times the open-beta peak target, rate-limit test log, kill-switch test), or an explicit fail with a plan the instructor accepted.
- **G2. Login cap.** A login cap at or below safe capacity is set and tested before the first wave.
- **G3. Personal data.** Accounts, reports and telemetry follow the same consent and minimum-data rules as the closed beta.

A beta run with a gate open has this milestone capped at 50.

## Deliverables

1. **Sizing sheet** (lab 08 section A): exposure target and the bug rate behind it, sign-ups needed, peak forecast, safe capacity, chosen levers, login cap.
2. **Beta operations log** (section B): rota as run in blocks of at most four hours with primary and backup; kill-switch drill with times; every incident with severity, times and actions; every kill-switch use.
3. **Forecast against actual** (section C): sign-ups, show-up rate, exposure, busiest-hour share, peak CCU, tick time at peak and crashes per 100 player-hours, each with its forecast and error ratio, and the raw queries.
4. **Targeted-test results**: each week 6 test with its `n` and verdict, or a statement that it did not reach its sample.
5. **Exit review** (section D): at least five criteria with thresholds committed before the weekend, results, evidence, and a one-paragraph launch recommendation.
6. **Known-issues post** and the code of conduct as published.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Build | Open-beta build tag and deploy log | Confirms no system or content item added after the week 7 content lock |
| Load test | Sprint 4 load-test report with the knee and latency threshold | Checks safe capacity uses this knee, not the bot maximum |
| Telemetry | Queries for sessions, peak CCU, tick time, crashes, tutorial funnel | Recomputes one error ratio in section C from the raw query |
| Incident log | Timestamped entries with severity | Picks one incident and matches it to server logs and the player-facing message |
| Kill switches | Drill log from staging | Checks every switch was flipped and restored before the doors opened |
| Playtest data | Targeted-test tables | Checks each test stopped at its planned `n` or says it did not reach it |
| Commit history | Exit thresholds and sizing | Checks both were committed before the beta started |

## How it is marked

The instructor walks the readiness checklist with the team at the end of the week 8 meeting and gives "go for the weekend" or names a blocker. The folder is marked before the week 9 meeting. The lab 08 rubric is the detailed scoring guide for rows 1, 3, 4 and 5.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Sizing | 20 | Bug rate chosen with a reason; exposure, sign-ups and peak forecast computed from named closed-beta and load-test sources; safe capacity from the knee with stated headroom | "As many as possible"; inputs with no source |
| Levers | 10 | When the margin under safe capacity is thin, at least one lever chosen before the weekend and its effect recomputed | Margin under 10% and nothing done |
| Weekend operations | 20 | Rota in blocks with primary and backup; severity table with names; every switch drilled; bug intake through the in-client button and tracker | One person on call all weekend; reports left in Discord |
| Forecast against actual | 15 | Every line has forecast, actual and error; raw queries attached; errors explained | Table missing lines, or forecasts written after the fact |
| Targeted tests | 15 | Each test reported at its planned `n` with a verdict, or marked as not reaching it; no early stopping | Tests stopped when the numbers looked good |
| Exit review | 15 | Five or more criteria written before the weekend; results with evidence; recommendation follows from the criteria | Recommendation contradicts the criteria, or thresholds added later |
| Player communication | 5 | Known-issues post kept current; wipe policy and dates stated and kept | Stale post; wipe policy changed without notice |
| **Total** | **100** | | |

## Builds on

- [PR401 week 11, production plan](../../PR401-capstone-i-pre-production/lectures/w11-production-plan.md) (the milestone dates the beta sits on).
- [PR101 week 12, crunch](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w12-crunch-causes-costs-alternatives.md) (why the rota has blocks) and [week 10, bug tracking](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md).
- [MMO302 week 1, scale targets and CCU](../../MMO302-mmo-server-architecture/lectures/w01-scale-targets-ccu-messages-and-n-squared.md), [week 11, load testing](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) and [week 13, headroom](../../MMO302-mmo-server-architecture/lectures/w13-cloud-deployment-and-autoscaling.md).
- [MMO308 week 4, funnels and churn](../../MMO308-live-operations-analytics-and-experimentation/lectures/w04-funnels-and-churn.md) and [week 13, incident response](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md).
- [MMO407 week 3, beta strategies](../../MMO407-launch-scaling-and-post-mortems/lectures/w03-beta-strategies.md) and its [beta exposure model](../../MMO407-launch-scaling-and-post-mortems/examples/w03-beta-exposure.html).
