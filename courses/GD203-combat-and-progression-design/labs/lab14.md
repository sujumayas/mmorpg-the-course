# GD203 · Lab 14: Progression audit

**Assigned:** week 14. **Due:** with the final combat system spec (week 15). **Weight:** part of the spreadsheet labs (40% of the course); the redesign feeds the progression section of the final spec.
**Lecture:** [Week 14, horizontal vs vertical progression](../lectures/w14-horizontal-vs-vertical-progression.md).

## Objective

Audit a two-year progression plan for a small MMO. Measure how far apart its players drift, how long each tier's content stays shareable, and which of its "sidegrade" rewards are secretly vertical. Then redesign it to hit a shelf-life target without losing the feeling of reward.

## Starter materials

Create these yourself from the definitions below. Any spreadsheet tool works. Keep every input on one `Inputs` tab.

**Tier plan (one tier every three months).** Each value is the power growth a player gets from completing that tier.

| Tier | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Growth r | 1.10 | 1.10 | 1.15 | 1.10 | 1.20 | 1.10 | 1.10 | 1.15 |

**Tolerance.** `F = 2` for dungeons, `F = 1.5` for raids. The [power gap](../examples/w14-power-gap.html) interactive draws the gap and shelf life for a constant `r`, and its Sidegrade checker tab runs the dominance and expected-value tests on up to six options.

**Reward table.** DPS of eight weapons in four situations. The tier column says when each weapon enters the game.

| Weapon | Tier | Single target | Swarm | Armored | Ranged |
|---|---|---|---|---|---|
| Longsword | 0 | 100 | 60 | 50 | 70 |
| Greataxe | 0 | 80 | 95 | 55 | 60 |
| Warpick | 0 | 75 | 55 | 100 | 55 |
| Longbow | 0 | 70 | 60 | 45 | 100 |
| Runeblade | 3 | 110 | 65 | 55 | 72 |
| Twin daggers | 3 | 105 | 70 | 40 | 75 |
| Halberd | 5 | 95 | 100 | 70 | 65 |
| Stormbow | 5 | 72 | 62 | 48 | 104 |

**Content mixes.** Share of fights in each situation.

| Mix | Single target | Swarm | Armored | Ranged |
|---|---|---|---|---|
| A (open world) | 40% | 30% | 15% | 15% |
| B (armored raid) | 20% | 20% | 50% | 10% |

## Steps

1. **Cumulative power.** On a `Tiers` tab, compute `P(t)` for tiers 0 to 8 as the running product of the growth rates. Add a column for the power gap between each tier and tier 0.
2. **Gap matrix.** Build a 9 × 9 matrix of `G = P(i) / P(j)` for every pair of tiers. Colour cells green when `G ≤ F` and red otherwise, with `F = 2` read from `Inputs`. Make a second copy with `F = 1.5` for raids.
3. **Shelf life.** For each tier, count how many later tiers can still share its content at `F = 2` and at `F = 1.5`. Compare with the lecture's formula `t* = ln F / ln r` using the plan's average growth (geometric mean of the eight rates).
4. **Dominance matrix.** On a `Rewards` tab, build an 8 × 8 matrix that reads "dominates" when the row weapon is at least as good as the column weapon in every situation and strictly better in at least one. List every pair where a newer weapon dominates an older one. Those rewards are vertical.
5. **Expected value.** Compute each weapon's expected DPS under mix A and mix B. Flag any weapon more than 3% above the median of the weapons available at the same tier. Note which weapon becomes the default when the content moves from mix A to mix B.
6. **Redesign.** Change the plan so that any two players within four tiers can share dungeon content (`F = 2`), keeping total growth over eight tiers at least 1.6. You may change growth rates, add a cap, or add a catch-up rule that raises new players to a given tier. Then edit at most three weapons so that no newer weapon dominates an older one and no weapon is more than 3% above its tier's median under mix A. Log every change on a `Changelog` tab with the reason.

## Deliverable

- The spreadsheet file, with tabs `Inputs`, `Tiers`, `Rewards`, `Changelog`.
- A 500-word memo written as a section of your final combat system spec. State the original and redesigned shelf life, what a tier 8 veteran and a tier 4 newcomer each lose in health in a shared dungeon fight before and after, which weapons were vertical in disguise and how you fixed them, and one risk your redesign creates.

## Rubric

| Criterion | Excellent (4) | Good (3) | Needs work (2) | Missing (0-1) |
|---|---|---|---|---|
| Power and gap matrix (20%) | Cumulative power and both matrices correct, colours driven by `F` on `Inputs` | One error that propagates | Matrix built but thresholds hardcoded | Missing |
| Shelf life (15%) | Counts correct at both tolerances and compared with `t*` from the geometric mean, with the difference explained | Counts correct, comparison missing | Counts off by one or more | Missing |
| Dominance and expected value (25%) | Every dominance pair found, expected values correct under both mixes, flags and mix change explained | One missed pair or one wrong value | Several errors | Missing |
| Redesign (25%) | Meets both shelf-life and growth constraints; weapon edits remove all dominance and EV outliers within three edits; changelog complete | Meets one constraint fully | Constraints not met, or edits not logged | Missing |
| Memo (15%) | Every question answered with numbers from the sheet; the stated risk is specific and follows from the model | Complete but one claim unsupported | Vague or mostly qualitative | Missing |
