# PR301 · Milestone 2 brief: technical architecture review

**Weight:** 6% of the course grade, inside the milestones component (50%).
**Assigned:** week 1. **Reviewed:** in the week 2 session. **Due:** the final pack before the week 3 session, in `docs/architecture/`.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide:** [week 2, technical architecture review](../lectures/w02-technical-architecture-review.md). **Lab:** [lab 02](../labs/lab02.md).
**Builds on:** [MMO302 week 1](../../MMO302-mmo-server-architecture/lectures/w01-scale-targets-ccu-messages-and-n-squared.md) (deliveries and the square term), [MMO302 week 2](../../MMO302-mmo-server-architecture/lectures/w02-shards-realms-zones-instances-layers.md) (shards, zones and instances), [MMO302 week 4](../../MMO302-mmo-server-architecture/lectures/w04-zone-servers-and-handoff.md) (what handoff costs), [MMO302 week 7](../../MMO302-mmo-server-architecture/lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md) (persistence strategies), [MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) (the latency knee and the 0.6 budget), [DB201 week 5](../../DB201-data-persistence-and-telemetry/lectures/w05-transactions-and-acid.md) (transactions) and [DB201 week 6](../../DB201-data-persistence-and-telemetry/lectures/w06-race-conditions-and-the-duplication-bug.md) (the duplication race), and [PR201 week 3](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w03-technical-design-document.md) (spikes and the walking skeleton).

## What this milestone proves

That the design carries twice the concurrency target in the worst crowd it allows, keeps every line of the persistence promise, and contains nothing the numbers do not justify. The review is also where machinery gets cut. The *Saltmarsh* team in the week 2 guide cut zone servers, a Redis cache and a separate login machine because one process held 111 players at 60% of a core. A review that removes 60 hours of handoff work is a good review.

## Deliverables

1. **Architecture diagram**, one page: processes, database, and what talks to what.
2. **Capacity sheet**: `capacity.csv` with the measured `e`, the worst crowd and host budgets, and the saved `check_capacity.py` output showing `PASS` at `headroom = 2`.
3. **Spike note**: code, machine, number of runs and the result for `e`, measured on the host the alpha will use.
4. **`N_max`**, the largest crowd within the CPU budget, compared with the load-test crowd.
5. **Persistence map**: the M1 promise with a strategy and a transaction boundary for every row, and the source of truth for each.
6. **Decision record**: five to ten decisions, each with a reason and a measurable revisit trigger; the deferred list; and the sprint 1 proof as one testable sentence that includes a restart.
7. **Review notes** from the other team's questions, with how each was answered or turned into a decision.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Spike measurement | Spike code and raw timings in the repository | Reruns the spike once on the alpha host, or reads the run log |
| Capacity | `capacity.csv` and `capacity-output.txt` | Reruns `check_capacity.py`; checks `N_max` by hand from the stated `u`, `u_m`, `m` and `e` |
| Commit rate | Row in the capacity sheet | Checks that write-through rows stay under what the team measured on its database |
| Transaction boundaries | Persistence map | Picks two actions (a trade and a craft) and asks the team to name every row each one changes |
| Decision triggers | `decisions.md` | Checks each trigger names a measurement and a threshold, for example "p99 tick above 80 ms at 100 bots" |
| Review conduct | Reviewer team's question sheet | Confirms the team was reviewed and reviewed the other team |

## How it is marked

The review in the week 2 session is 20 minutes of presentation and 20 of questions from a paired team and an instructor. The instructor marks the final pack against the rubric and uses the session notes for the review conduct row. The decision record is reused at weeks 6 and 13. A trigger written in week 2 that fires later and is honoured then scores well in [M3](m3-sprint-reviews-brief.md), not here.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Capacity passes | 12 | `PASS` at headroom 2 or more on rerun; output file matches | Fails on rerun, or headroom lowered to pass |
| Measured cost | 12 | `e` from a spike on the alpha host, with method and runs recorded | `e` guessed or taken from the internet |
| Worst crowd | 10 | The most crowded place the design allows is named and used, usually the town or the encounter | An average or spread crowd |
| Ceiling and bandwidth | 8 | `N_max`, outbound bandwidth and commit rate computed and compared with host limits | Only CPU checked |
| Persistence map | 18 | Every "None" loss maps to write-through with a named transaction boundary and one source of truth | Items held in memory and database with no rule for which wins |
| Justified components | 12 | Every box on the diagram is justified by the capacity sheet or the map; cuts recorded with their hours | Textbook architecture copied from MMO302 |
| Decision record | 14 | Each decision has a reason and a measurable trigger; deferred machinery listed | "Revisit if slow"; no deferred list |
| Sprint 1 proof | 6 | One sentence a bot test can answer, including a restart | Vague or untestable |
| Review conduct | 8 | Questions answered with numbers; the team's questions to the other team were specific | Defensive answers; no questions asked |
| **Total** | **100** | | |

## Late and missing work

The review happens in the session and cannot be moved without an agreed extension. The written pack is capped at 70 if it arrives up to 48 hours late. Sprint 1 planning in week 3 goes ahead with whatever proof sentence the team has.
