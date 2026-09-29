# PR401 · Milestone 7 brief: technical design document

**Weight:** 6% of the course grade, inside the pre-production package component (50%).
**Assigned:** week 7. **Due:** at the start of week 8, in `docs/tdd.md` and `preproduction/week07/`. Spike results are due at the end of week 9. **Reviewed:** at the week 8 stand-up.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide and lab:** [week 7, technical design](../lectures/w07-technical-design.md) with [lab 07](../labs/lab07.md).
**Builds on:** [PR201 week 3, technical design document](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w03-technical-design-document.md) (spikes and a bandwidth budget), [PR301 week 2, technical architecture review](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w02-technical-architecture-review.md) (the persistence promise and decision records), and [PR301 week 13, beta](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w13-beta-open-class-playtest.md), section 3 (the load test).

## What this milestone proves

That the server design survives twice the expected crowd standing in one place. The week 7 guide showed *Emberfall*'s uncapped hub at 120 players spending 71.4 ms of each 100 ms tick on replication. An interest cap of 40 brought it to 24 ms. The TDD is marked on whether the worst case is inside budget, or has a named change or an accepted risk, and on whether the risky inputs are measured.

## Deliverables

1. **Technical design document** (`docs/tdd.md`), eight to twelve pages, with the eight sections from week 7 section 2: targets, process map, authority table, data model and persistence, message catalog, budgets, build and deploy and observe, and decisions and spikes.
2. **Budget sheet** (`budget.csv`) in the lab 07 format with at least the spread, hub and 2× load-test cases, and `net_budget.py` printing `PASS`.
3. **Spike plan** (`spikes.md`): at least three spikes, each with an owner, a time box, the input it measures and the decision it feeds.
4. **Updated risk register** from week 6, with each technical risk linked to a spike or a design change.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Targets | TDD section 1 | Launch CCU and a load-test CCU at least twice as high |
| State ownership | Process map | Every process owns named state; no state is owned twice |
| Authority | Authority table | No empty cell for actions that change items, currency or health |
| Persistence | TDD section 4 | Save interval stated; transactional writes named |
| Budgets | Checker output | Reruns `net_budget.py`; spread, hub and 2× rows present |
| Measured inputs | Method notes for `s` and `t` | Measured from the real build, or a spike with owner and time box |
| Egress | One paragraph | Weekend gigabytes, the host's price and the date checked |

## How it is marked

The instructor reruns the checker and reads the TDD. At the week 8 stand-up any member may be asked who owns a given piece of state, or which cell of the budget sheet fails without the cap.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Targets and load cases | 10 | Launch and 2× CCU stated; hub case uses a realistic crowd for your world | Only the spread case |
| Process map and ownership | 15 | Every process with its state and what it may never do | Boxes and arrows with no state |
| Authority table | 15 | Complete for every action that changes items, currency or health | Empty cells, or "client decides" for trades |
| Persistence | 10 | Save interval, transactional writes and restart behaviour stated | "We use a database" |
| Budget sheet | 20 | `PASS` on rerun; every over-budget row has a design change or a reasoned accepted risk; player-facing cost of any cap named | Fails, or failing rows with no response |
| Measured inputs and spikes | 15 | `s` and `t` measured with method stated, or three or more spikes each tied to an input and a decision | Inputs copied from the guide's sample team |
| Decisions log | 10 | Three or more decisions with rejected alternatives | Decisions with no alternatives |
| Team ownership | 5 | Any member explains a budget row | Only the server programmer can |
| **Total** | **100** | | |

## Late and missing work

Up to 48 hours late is capped at 70. Spike results that miss the end of week 9 are recorded as open risks in the production plan, and the measured inputs row is marked on what was delivered on time.
