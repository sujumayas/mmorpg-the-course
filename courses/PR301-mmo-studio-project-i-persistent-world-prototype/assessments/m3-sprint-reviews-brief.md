# PR301 · Milestone 3 brief: sprint reviews 1 to 5

**Weight:** 14% of the course grade, inside the milestones component (50%). Sprint 1, 2 and 3 reviews are worth 3% each. Sprint 4 and 5 reviews are worth 2.5% each, because they are one-week sprints.
**Reviewed:** each two-week sprint runs from one planning session to the next, and its review takes the first part of that next session. Sprint 1 at the start of week 5, sprint 2 at the start of week 7, sprint 3 at the start of week 9, sprint 4 at the start of week 12, sprint 5 (the group encounter) at the start of week 13.
**Work mode:** team. One team mark per review, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guides:** [week 3](../lectures/w03-sprint-1-world-server-and-login.md) and [week 4](../lectures/w04-sprint-1-review.md), [week 5](../lectures/w05-sprint-2-combat-and-mobs.md) and [week 6](../lectures/w06-sprint-2-review.md), [week 7](../lectures/w07-sprint-3-economy-and-crafting.md) and [week 8](../lectures/w08-sprint-3-review.md), [week 11](../lectures/w11-sprint-4-social-systems.md), [week 12](../lectures/w12-sprint-5-group-encounter.md). **Labs:** [03](../labs/lab03.md) to [08](../labs/lab08.md), [11](../labs/lab11.md) and [12](../labs/lab12.md).
**Builds on:** [PR201 week 6](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w06-sprint-2-core-combat.md) (yesterday's weather and chain risk), [PR201 week 7](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w07-sprint-2-review-and-playtest.md) (the review as a working session), [PR201 week 9](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w09-sprint-3-review.md) (scope cuts and the freeze), [MMO302 week 5](../../MMO302-mmo-server-architecture/lectures/w05-tick-rate-for-mmos-vs-shooters.md) (tick budgets), [MMO302 week 9](../../MMO302-mmo-server-architecture/lectures/w09-login-character-select-gateway-services.md) (login and session tickets), [MMO302 week 10](../../MMO302-mmo-server-architecture/lectures/w10-chat-guild-and-social-services.md) (fan-out and token buckets), [MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) (bot load tests), [MMO302 week 8](../../MMO302-mmo-server-architecture/lectures/w08-item-ownership-and-transactional-integrity.md) (item ownership), [DB201 week 5](../../DB201-data-persistence-and-telemetry/lectures/w05-transactions-and-acid.md) and [week 6](../../DB201-data-persistence-and-telemetry/lectures/w06-race-conditions-and-the-duplication-bug.md) (transactions and races), [DB201 week 10](../../DB201-data-persistence-and-telemetry/lectures/w10-telemetry-design-events-and-properties.md) (event design), [MMO304 week 3](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md), [week 7](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w07-crafting-chains-and-gathering-professions.md) and [week 12](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w12-economic-telemetry-and-dashboards.md) (faucets, crafting and economic telemetry), and [MMO309 week 4](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w04-duplication-exploits-and-transactional-design.md) (why a rare dupe is S1).

## What this milestone proves

That the team builds a persistent world one increment at a time and can tell, with evidence, whether each increment works. Every review answers the sprint goal yes or no on the test host from a tagged build. A goal answered "no" with honest evidence can still earn most of the marks. A "yes" that the evidence does not support earns few.

## Deliverables at every review

1. **Review record**: the goal read aloud and answered yes or no, stories done and not done, and the demo on the test host from the tagged build, deployed by script.
2. **Velocity**: estimated hours of stories that met the definition of done, available hours, and the focus factor (sprints 1 to 3) or weekly velocity (sprints 4 and 5).
3. **Retrospective note** with one change, an owner and a check date, and the result of the previous one.
4. **Tagged input list** for the next sprint: defects with reproducing conditions, stubs coming due and discoveries, each sized.
5. **The sprint's lab**, with its checker output saved: lab 04 (sprint 1), lab 06 (sprint 2), lab 08 (sprint 3), lab 11 plus the sprint 4 review notes (sprint 4), lab 12 (sprint 5).

## Evidence required

| Sprint | Evidence | Format | How the instructor checks it |
|---|---|---|---|
| 1 | Soak data | `soak.csv` with cycled and burst conditions, bot logs, threshold with its exposure calculation | Reruns `check_soak.py`; traces two counts to the bot logs; checks the threshold was committed before the run |
| 1 | Restart result | Server log of the kill and restart, positions before and after | Watches another team kill the server in the session; compares positions with the persistence map |
| 2 | Tick logs | One line per tick for runs A to D (and E, spread), ten minutes each after warm-up | Reruns `check_tick.py`; recomputes `M_max` and compares `g` with the week 2 prediction |
| 2 | Kill transaction | Code path and a restart test | Kills the server during a loot and checks there is no pelt without a kill |
| 3 | Ledger reconciliation | Money-supply and by-reason queries on a one-hour bot run of a fresh world | Reruns both queries; the residual must be 0 |
| 3 | Tracker export | Every bug with severity, opened, closed and hours | Reruns `check_gonogo.py`; checks severities against the week 8 table |
| 3 | Kill switches | Flag names, owners, test dates, a log excerpt of each flip with clients connected | Flips one switch on the running server at the week 9 freeze |
| 4 | Social bot test | Server log of a 50-client bot test that used each merged feature | Forms a party, joins a guild and chats in the build; restarts and checks the guild roster |
| 4 | Worst-case chat numbers | Delivery rate and presence burst with the stated rate limit | Recomputes them from the token bucket |
| 5 | Encounter telemetry | Pull, wipe, kill and deaths by ability | Matches two rows of the pull log to telemetry |
| 5 | Live encounter check | The build at the start of week 13 | A party of the instructor's choosing runs a wipe, a leash and a kill |

Playtest notes from the paired team (the hand-played part of weeks 6 and 8, and the week 12 pull sessions) go in the review record.

## How it is marked

Each review is marked on the same 100-point rubric. Half the points are common to every sprint. The other half are the sprint's own evidence, broken down in the second table. A story counts in the sprint in which it met the definition of done, never in the sprint it was started. The instructor recomputes velocity for one review from the tracker export.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Goal answered honestly | 12 | Yes or no on the test host from the tagged build; "yes" supported by the sprint evidence | Laptop demo, or "yes" the evidence contradicts |
| Definition of done | 10 | Only stories meeting every line counted (test host, restart, bot check at the stated load) | Unfinished or untested stories counted |
| Velocity and forecast | 10 | Measured from done stories and actual availability; next sprint planned from it (range from sprint 3, low end for one-week sprints) | Borrowed or average figures; plan above capacity |
| Retrospective | 8 | One owned change, and the previous change checked | No change, or the same change every sprint |
| Next-sprint input | 10 | Defects have reproducing conditions; items sized and tagged; class-of-bug fixes ranked first | Unsized wish list |
| Sprint evidence | 50 | See the breakdown for the sprint below | |
| **Total** | **100** | | |

### Sprint evidence breakdown (50 points)

| Sprint | Evidence row | Points |
|---|---|---|
| 1 | Threshold set from alpha exposure before the soak ran | 12 |
| 1 | Cycled and burst conditions kept separate, each at the threshold, `check_soak.py` agrees | 14 |
| 1 | Restart by another team, persistent state matches the map | 14 |
| 1 | Protocol document versioned; every stub has a backlog story | 10 |
| 2 | 100 bots through the real protocol in the worst-case layout, bots that move and fight | 12 |
| 2 | Four-run 2 × 2 design, p99 reported, `check_tick.py` agrees | 14 |
| 2 | Content and engineering options modelled before any architecture change; chosen option has a story and fallback | 12 |
| 2 | Kill, drop and experience in one transaction, proven by a restart test | 12 |
| 3 | Ledger reconciles to zero on the one-hour bot run | 16 |
| 3 | Severities follow the persistent-world table; forecast with the pessimistic case | 12 |
| 3 | Kill switch for every value-moving system, read at runtime, tested both ways | 12 |
| 3 | Go/no-go list signed, every item checkable on Thursday | 10 |
| 4 | Party works in the build (invite, accept, leave, frames, party chat) | 16 |
| 4 | Guild data survives a restart; parties are in memory only | 12 |
| 4 | Chat rate limit merged with the channel; worst case written down | 10 |
| 4 | Rescope note for each rescoped or deferred item; bug reserve closed or carried | 12 |
| 5 | Encounter meets the five points of week 12 section 1, checked live | 18 |
| 5 | Boss health and enrage from a saved simulator run, margin as a percentage of simulated DPS | 10 |
| 5 | Leash, wipe reset and disconnect each have a recorded pull | 10 |
| 5 | Day-3 burn-down with both projections; cut at least as large as the slower one, from items marked non-minimum | 12 |

Each sprint's rows total 50.

## Late and missing work

Reviews happen in the session. A team that cannot demo from the test host answers the goal "no" and is marked on its evidence. Written records are capped at 70 for their rows if they arrive up to 48 hours after the stated deadline. The sprint 5 live check at the start of week 13 cannot be repeated later in the week, because the beta uses the same build.
