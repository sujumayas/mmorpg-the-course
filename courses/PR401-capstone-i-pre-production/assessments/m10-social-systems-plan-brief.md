# PR401 · Milestone 10 brief: social systems plan

**Weight:** 5% of the course grade, inside the pre-production package component (50%).
**Assigned:** week 10. **Due:** at the start of week 11, in `docs/social-plan.md`, `docs/code-of-conduct.md` and `preproduction/week10/`. **Reviewed:** at the week 11 stand-up.
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md).
**Session guide and lab:** [week 10, social systems plan](../lectures/w10-social-systems-plan.md) with [lab 10](../labs/lab10.md).
**Builds on:** [PR301 week 11, social systems](../../PR301-mmo-studio-project-i-persistent-world-prototype/lectures/w11-sprint-4-social-systems.md) (what social means for a 50-player prototype), [MMO405 week 10, ethics](../../MMO405-research-methods-in-online-games/lectures/w10-ethics-and-irb.md) (consent for any research use of player data), [MMO406 week 8, player agency vs canon](../../MMO406-worldbuilding-and-lore-for-persistent-worlds/lectures/w08-player-agency-vs-canon.md) (what the world records when players change it), and [PR101 week 11, communication and conflict](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w11-communication-and-conflict-in-teams.md) for the team's own rota.

## What this milestone proves

That every social system works at the population the team will really have, and that the safety features exist before strangers meet. *Emberfall*'s draft towns of 15 could field four defenders on about half of evenings, which made defending a coin flip. Four towns of about 22, a militia of two and a fixed raid window brought it to 99%. This milestone marks the arithmetic, the levers chosen and what they cost players, and the safety minimums with owners.

## Deliverables

1. **Social systems plan** (`docs/social-plan.md`) with the six parts from week 10 section 1 (grouping, long-lived groups, communication, trade and trust, conflict rules, safety), each tied to a pillar, and a low-population fallback rule.
2. **Liquidity and safety sheets** (`liquidity.csv`, `safety.csv`) in the lab 10 format, with `social_check.py` printing `PASS`.
3. **Code of conduct** (`docs/code-of-conduct.md`), one page, and the moderation rota with hours.
4. **Social backlog**: every social feature estimated and ready for the week 11 production plan.

## Evidence required

| Evidence | Format | How the instructor checks it |
|---|---|---|
| Coverage | `liquidity.csv` | Every system that needs several players at once has a row |
| Play-time inputs | Notes in the plan | `h`, window share and window length from data or labelled assumed |
| Levers | `response` column | Every row under 0.80 has a lever and its cost to players |
| Off-peak rule | `off_peak_rule` column | Decided for every conflict system |
| Safety minimums | `safety.csv` | All eight features from week 10 section 3 with owners and dates |
| Rota | Rota table | Every open hour of the live period covered |
| Fallback | One paragraph | Trigger, action and decision owner |

## How it is marked

The instructor reruns the checker and reads the plan. At the week 11 stand-up one member computes `P(defended)` for one row by hand or with the script, and another explains the sanction ladder in the code of conduct.

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Checker passes | 10 | `PASS` on rerun, output matches | Fails |
| Six parts tied to pillars | 15 | All six present; each names the pillar it serves | Social features with no pillar |
| Liquidity rows | 15 | Every multi-player system has a row with sourced inputs | Rows only for the systems that pass |
| Levers and costs | 15 | Every row under 0.80 has a lever and its player-facing cost; off-peak decided for all conflict systems | Levers chosen with no cost stated |
| Safety minimums | 20 | Eight features with owners and dates; rota covers every open hour | Missing report or block, or rota gaps |
| Code of conduct | 10 | One page, shown at sign-up, with a sanction ladder | A list of banned words |
| Fallback and backlog | 10 | Low-population trigger, action and owner; every social feature estimated | No trigger, or features unestimated |
| Team ownership | 5 | Any member explains a lever's cost | Only the systems designer can |
| **Total** | **100** | | |

## Late and missing work

Up to 48 hours late is capped at 70. The safety sheet must be complete before the week 14 review whatever this mark is, because PR402 cannot open to the public without it.
