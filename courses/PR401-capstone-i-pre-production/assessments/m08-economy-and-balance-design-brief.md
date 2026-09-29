# PR401 · Milestone 8 brief: economy and balance design

**Weight:** 6% of the course grade, inside the pre-production package component (50%).
**Assigned:** week 8. **Due:** at the start of week 9, in `docs/economy.md`, `data/` and `preproduction/week08/`. **Reviewed:** at the week 9 stand-up.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide and lab:** [week 8, economy and balance design](../lectures/w08-economy-and-balance-design.md) with [lab 08](../labs/lab08.md).
**Builds on:** [PR301 week 7, economy and crafting](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w07-sprint-3-economy-and-crafting.md) (the ledger rule and crafting leaks), [PR301 week 10, telemetry review](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w10-telemetry-review.md) (tracing where currency came from), [MMO403 week 4, cosmetics vs power](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w04-cosmetics-vs-power.md), and [MMO403 week 8, dark patterns](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w08-dark-patterns.md) if your capstone sells anything.

## What this milestone proves

That every price in the game is reachable by the player it is meant for, inside the four-week live period. *Emberfall*'s draft house plot at 5,000 marks was never reached by three players in four. Its revised plot at 1,200 marks falls in week 3 for the median player. The milestone also checks that the team knows who holds the money: keen and heavy players are a quarter of *Emberfall*'s launch players and hold about 55% of the marks.

## Deliverables

1. **Economy one-pager** (`docs/economy.md`) with the five parts from week 8 section 1 (currencies, faucets, sinks, transformations, trade), a source label on every rate, the player shares, and the money-split paragraph.
2. **Price and flow tables** (`flows.csv`, `prices.csv`, `players.csv`) in the lab 08 format, with `economy_check.py` printing `PASS`.
3. **Balance targets** (`data/balance.csv`), six or more rows, each with a value, a unit and a reason.
4. **Telemetry list**: one event per faucet and sink, with the properties needed to compute currency per hour per player.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Rates with sources | `flows.csv` | Every faucet and sink has a rate per hour and a source label |
| Target week | `prices.csv` | Every saved-for item has a target player type and week |
| Key purchase | Checker output | The median reaches it inside the live period, or the team explains why not |
| Money split | Paragraph in the one-pager | Recomputed from `players.csv` |
| Data, not code | A data file the build reads | The instructor changes one price and restarts; no rebuild needed |
| Telemetry | Event list | One event per faucet and sink |

## How it is marked

The instructor reruns the checker, changes one value in `data/balance.csv` on the build, and asks one member to compute a purchase's week for the light player.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Checker passes | 10 | `PASS` on rerun, output matches | Fails |
| One-pager | 15 | Five parts, one currency or a reason for a second, every trade channel tied to a pillar | Parts missing, or trade channels no pillar needs |
| Flows with sources | 15 | Every faucet and sink with a rate and a source label | Rates with no source |
| Prices against the live window | 20 | Every saved-for item has a type and week; misses have a reasoned response; the light player has a goal | Key purchase out of reach with no comment |
| Money split and scaling sink | 15 | Split computed; a sink that scales with activity targets the top holders and costs light players little | Only flat sinks |
| Balance targets | 10 | Six or more with values, units and reasons | Targets as adjectives |
| Data and telemetry | 10 | The game reads the files at start; every flow has an event | Values hard-coded, or no events |
| Team ownership | 5 | Any member computes a target week | Only the economy designer can |
| **Total** | **100** | | |

## Late and missing work

Up to 48 hours late is capped at 70. After that it scores 0 but must still be handed in, because the vertical slice reads these data files.
