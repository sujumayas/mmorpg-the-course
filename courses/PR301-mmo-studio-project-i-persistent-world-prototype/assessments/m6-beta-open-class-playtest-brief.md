# PR301 · Milestone 6 brief: beta, the open class playtest

**Weight:** 9% of the course grade, inside the milestones component (50%).
**Assigned:** week 10. **Run:** the week 13 session and the beta weekend. **Due:** at the start of the week 14 studio session, in `production/week13/`.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide:** [week 13, beta: open class playtest](../lectures/w13-beta-open-class-playtest.md). **Lab:** [lab 13](../labs/lab13.md).
**Builds on:** [MMO302 week 3](../../MMO302-mmo-server-architecture/lectures/w03-area-of-interest-grids-radius-hysteresis.md) (area of interest), [MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) (stepped load tests and the knee), [MMO302 week 14](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md) (tail latency), [MMO308 week 13](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md) (incident roles), [DB201 week 14](../../DB201-data-persistence-and-telemetry/lectures/w14-backups-and-disaster-recovery.md) (restores), [MMO309 week 4](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w04-duplication-exploits-and-transactional-design.md) (the race a late save exposes) and [PR201 week 11](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w11-playtest-and-telemetry-review.md) (Wilson intervals and the unit of analysis).

## What this milestone proves

The course outcome: a persistent multiplayer world supporting 50 or more concurrent test players. The beta checks it in three parts, as week 13 section 1 sets out.

- **Concurrency.** At least 50 human players online at once, shown by the server's own player-count metric with bots excluded.
- **Support.** While they are online, the tick holds the week 6 rule (mean at or under 60 ms, p99 at or under 80 ms on a 10 Hz server) and disconnects stay under the threshold in the beta plan.
- **Persistence.** The world survives a planned restart during the peak hour, including a change made seconds before the save.

A team that plans well and falls short of 50 humans because turnout disappointed can still pass this milestone, if it reports the shortfall with the turnout numbers. It cannot earn the concurrency row. The [final world brief](final-world-brief.md) gives one more chance to show 50 at the showcase.

## Deliverables

1. **Beta plan** (lab 13) passing `check_beta.py`: alpha rates from the server logs with Wilson intervals; the invitation target with at least a 90% modelled chance of 50 at the low end of the show rate; the lever behind any raised event attendance; the confirmation trigger and what happens if it fires.
2. **Load test** on the beta build with chat, parties and the encounter instances from week 12 active, stepped by 25 to 100 bots, ten minutes per step after warm-up, mean and p99 at every step, capacity interpolated only where a step's p99 crosses 80 ms, and any fix with its retest.
3. **Go/no-go sheet** completed 30 minutes before the peak hour, signed by the lead with the time, naming lead, operator, comms and observers.
4. **Peak evidence**: the server's player-count export (humans and bots separately) and the p99 tick export for the peak hour, peak marked.
5. **Restart drill record**: before-and-after values for five check characters, one guild and one late change, and the restart duration.
6. **Beta telemetry export and observer notes** in the week 10 format.
7. **Turnout review**: invitations, logins and event peak, `s` and `e` recomputed and compared with the plan.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Server metrics | Per-minute player count, humans and bots in separate columns | Reads the humans-only peak from the export |
| Tick log | Per-tick CSV for the peak hour | Recomputes p99 for the peak minute |
| Load test data | `loadtest.csv` and raw tick logs per step | Reruns `check_beta.py`; recomputes capacity by interpolation |
| Server logs | Restart drill window | Matches the save, stop and start times to the drill record |
| Database | Rows for the check characters before and after | Compares values; any difference must be filed as S1 |
| Telemetry | Beta export with encounter events | Checks pulls, wipes and kills are present from tester parties |
| Playtest notes | Observer note sheets | Checks they reach week 14 triage |

## How it is marked

The instructor watches the go/no-go and the peak hour for each team, then marks from the evidence at week 14. The restart drill is marked on whether it was designed to find a problem. The *Saltmarsh* drill in the week 13 guide lost a craft made ten seconds before the save. That drill scores full marks, because it found an S1 and the team filed it. A drill with five idle characters that finds nothing scores low.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| 50 humans online | 20 | Server metric shows 50 or more humans at once, bots excluded; or, for half marks at most, an honest shortfall report with recomputed `s` and `e` | Screenshot as evidence; bots counted |
| Invitation plan | 12 | Rates from alpha logs with intervals; target gives 90% at the low end of `s`; raised `e` tied to a named lever; trigger written | Expected value used as the target |
| Load test | 16 | Beta build with all systems and instance count; stepped to 100; p99 at every step; capacity only where measured; headroom at least 2 or fixed and retested | Week 6 build; mean only; capacity extrapolated |
| Tick at peak | 8 | Mean and p99 during the peak hour within the week 6 rule, from the per-tick log | Not measured |
| Restart drill | 14 | Planned in the peak hour; five characters, a guild and a late change checked before and after; any difference filed as S1 | Idle characters only; differences ignored |
| Run of the hour | 10 | Go/no-go signed before the hour; one lead makes calls; comms warned players before the restart | Nobody owns the call |
| Encounter at scale | 8 | Tester parties ran the encounter; telemetry records pulls, wipes and deaths by ability | Encounter closed, or no telemetry |
| Evidence for week 14 | 12 | Telemetry, observer notes and turnout review handed in the week 10 format | Notes missing or unsorted |
| **Total** | **100** | | |

## Late and missing work

The peak hour follows the instructor's rota and cannot be moved. A team whose slot fails for reasons outside its control (a campus network outage, for example) is given a weekend slot. Written evidence up to 48 hours late is capped at 70 for its rows.
