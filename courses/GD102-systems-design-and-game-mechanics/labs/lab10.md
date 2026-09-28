# GD102 · Lab 10: Emergence audit

**Week:** 10, emergence vs progression ([lecture](../lectures/w10-emergence-vs-progression.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the Machinations models and exercises component (30%).

## Objective

Measure how much an emergent object set gives you and how much of it you can test. You build the interaction matrix for 16 systemic objects, count pairs and rules, estimate the untested share under two QA budgets, then playtest a paper version and write a policy for the surprising pairs your testers find.

## Starter materials

Everything you need is on this page. Copy the table into a spreadsheet (one row per object, one column per property, 1 for yes and blank for no).

**Properties (6).** burns, conducts, floats, heavy, wet, sharp.

**Starter property rules (8).** A rule fires when two objects meet and the condition holds.

| # | Condition | Effect |
|---|---|---|
| R1 | burns + burns, one of them lit | fire spreads to the other |
| R2 | burns + wet | fire goes out; the wet object loses "wet" |
| R3 | conducts + conducts, one of them electrified | current spreads |
| R4 | conducts + wet | current spreads into the wet object |
| R5 | heavy + floats | the floating object sinks if the heavy one is on top |
| R6 | sharp + burns | the burnable object is cut in two |
| R7 | heavy + sharp | nothing (the heavy object blunts the sharp one) |
| R8 | floats + wet | the floating object rides on the wet one |

**Objects (16).**

| # | Object | burns | conducts | floats | heavy | wet | sharp |
|---|---|---|---|---|---|---|---|
| 1 | wooden crate | 1 | | 1 | | | |
| 2 | rope | 1 | | 1 | | | |
| 3 | torch | 1 | | | | | |
| 4 | puddle | | 1 | | | 1 | |
| 5 | iron bar | | 1 | | 1 | | |
| 6 | balloon | | | 1 | | | |
| 7 | oil barrel | 1 | | 1 | 1 | | |
| 8 | grass patch | 1 | | | | | |
| 9 | stone block | | | | 1 | | |
| 10 | fan | | 1 | | | | |
| 11 | magnet | | 1 | | 1 | | |
| 12 | ice block | | | 1 | | 1 | |
| 13 | spear | 1 | | | | | 1 |
| 14 | copper wire | | 1 | | | | |
| 15 | glass shard | | | | | | 1 |
| 16 | raft | 1 | | 1 | | | |

Also bring: the [week 10 lecture](../lectures/w10-emergence-vs-progression.md) formulas, a printed copy of the object list cut into 16 cards, and a 10 × 10 grid sheet as a play area.

## Steps

1. **Counts by formula.** Compute `C(16, 2)`, `C(16, 3)` and the maximum property-rule count `R(6)`. Check: 120, 560 and 21.
2. **Interaction matrix.** Build a 16 × 16 sheet with the upper triangle filled. For each pair, list which of R1 to R8 can fire (use a formula that reads the property columns, not hand entry). Count the pairs where at least one rule can fire. Report that count and the share of 120.
3. **Rule coverage.** For each rule, count how many pairs it can fire on. Which rule does the most work? Which rule fires on fewest pairs? Would you cut it?
4. **QA budgets.** QA can test 40 pairs (budget A) or 90 pairs (budget B). Compute the untested share for each, both over all 120 pairs and over only the reacting pairs from step 2.
5. **Add one object.** Design a 17th object with at most three properties. Before you add it, predict how many new reacting pairs it will create. Add it and check.
6. **Paper playtest (in lab, 20 minutes).** In pairs, one student is the "game" and one is the player. The player gets a goal: "reach the top-right corner; a locked gate blocks column 8 until you find the key in the bottom-left." Place 10 of the objects on the grid. The player may move one square and combine two adjacent objects per turn. The game applies only rules R1 to R8. Record every pair the player tried and every outcome.
7. **Keep or patch.** For every pair your player used that you did not expect, decide "keep" or "patch" and give a one-line reason. At least one decision must mention whether the pair skips the locked gate.

## Deliverable

The spreadsheet (steps 1 to 5), the playtest log (step 6), and a memo of at most 400 words. The memo must give the reacting share, the untested share under both budgets, your 17th object and its predicted versus actual new pairs, and the keep/patch table with reasons.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Counts and formulas | 120, 560 and 21 correct; matrix filled by formula from the property columns | Correct counts, matrix partly by hand | Counts wrong | 20% |
| Rule coverage analysis | Every rule counted; a cut/keep decision justified by coverage | Counts given, weak justification | Missing | 20% |
| QA budget analysis | Both budgets, both denominators, interpretation of the difference | One denominator only | Missing or wrong | 20% |
| 17th object | Prediction written before adding, checked, gap explained | Prediction after the fact | Missing | 15% |
| Playtest and keep/patch policy | Complete log; every surprise has a reasoned decision; gate question addressed | Partial log or thin reasons | No playtest evidence | 25% |
