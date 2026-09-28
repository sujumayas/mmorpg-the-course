# MA102 · Lab 09: Loot table from targets

Assigned in week 9 ([lecture](../lectures/w09-weighted-tables-and-loot-table-design.md)). Due at the start of week 10. Counts toward the problem-set grade, and your table is the starting point for the loot design assessment.

## Objective

Design a two-tier weighted loot table for a raid boss by working backward from player-facing targets, verify every number, and then make a seasonal change that leaves protected items exactly where they were.

## Starter materials

- `lab09_starter.xlsx` (on the course page). Sheet "Brief" holds the design targets below. Sheet "Table" has columns for tier, entry, weight, probability within tier, overall probability, rolls-adjusted per-kill chance, kills to 50%, kills to 95%, value and EV contribution. The formula cells are empty.
- `lab09_starter.ipynb` for Python users: a `pick(table, rng)` function using the cumulative-walk algorithm from the lecture, and an empty `simulate_kills(table, kills, rolls, rng)` function.
- The week 9 interactive, `examples/w09-loot-weights.html`, and the week 7 interactive, `examples/w07-kills-until-drop.html`, for checking values.

### The brief

The boss is killed once per week per player and rolls its table **2 times per kill**. Rewards:

| Reward | Job | Target |
|---|---|---|
| Raid tokens | Income | Always drops 3 per kill (not part of the weighted table) |
| Gold | Income | Expected 120 gold per kill from the table |
| Tier armour piece | Progression | 95% of players have at least one within 12 kills |
| Raid weapon | Progression | 95% of players have it within 30 kills |
| Mount | Trophy | Median player gets it around kill 150 (within ±10) |

Use two tiers: a top table (Nothing, Gold, Gear tier, Trophy tier) and a gear sub-table (armour, weapon).

## Steps

1. **Per-kill targets.** For each progression and trophy reward, compute the required per-kill chance using the week 7 formulas. Convert each to a per-roll chance, remembering the table is rolled twice: solve `1 − (1 − p_roll)² = p_kill`.
2. **Build the tiers.** Choose the top-table weights and the gear sub-table weights so that each item's overall per-roll chance (tier chance times in-tier share) matches step 1. Use a top-table total of at least 1,000.
3. **Set the gold value.** Choose a gold amount per Gold drop so that the table's expected gold per kill is 120 (two rolls).
4. **Verify.** Fill every formula column. Show that each target in the brief is met. Then simulate 10,000 players for 200 kills each and compare simulated percentiles to your formulas.
5. **Seasonal change.** For four weeks the live team adds a "Festival cloak" with a per-kill chance of 10%, and doubles expected gold. The weapon and armour chances are protected and must not change, and the mount must stay within its target. Make the change by taking weight from specific entries. Show before-and-after weights and probabilities.
6. **Critique.** A teammate proposes putting the cloak into the gear sub-table "because it is gear." Compute what that does to the weapon's 95th-percentile wait and explain in two sentences why you would reject it.

## Deliverable

The spreadsheet or notebook, plus a one-page PDF (at most 400 words) with the final table, a checklist showing each target met (with the number), the seasonal before-and-after table, and your answer to step 6.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Targets to chances | All per-kill and per-roll chances correct, including the two-roll adjustment | One or two errors, or rolls ignored | Mostly incorrect | 20% |
| Table construction | Two tiers, weights produce every target, totals large enough that rounding does not break a target | Most targets met | Fewer than half met | 25% |
| Verification | Every formula column correct; simulation agrees with formulas and differences are explained | Formulas correct, simulation missing or unexplained | Numbers not checked | 20% |
| Seasonal change | Cloak and gold change applied, protected items unchanged to 0.01 points, mount still in range | Change applied with a small unintended shift | Protected items moved | 25% |
| Critique and write-up | Correct numeric critique, plain and short memo | Critique without numbers | Missing | 10% |
