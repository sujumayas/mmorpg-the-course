# MMO303 · Lab 04: Mitigation stack audit

**Week:** 4, stacking mitigation ([lecture](../lectures/w04-stacking-mitigation-multiplicative-layers.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the problem sets (30%).

## Objective

Build a damage pipeline that combines percentage layers, flat reductions and absorbs in a stated order, and use it to find runaway combinations in a tank's defensive kit before they ship.

## Starter materials

- A blank spreadsheet (Excel, LibreOffice or Google Sheets) with three tabs you create: `Pipeline`, `Kit`, `Audit`. On `Pipeline`, add one row per layer with the columns `Layer`, `Type`, `Value`, `Let-through fraction`, `Doublings` and `Cumulative let-through`. Copy the kit table below onto `Kit`. `Audit` starts empty.
- The "Ironwarden" tank kit, given on the `Kit` tab and repeated here:

| Effect | Type | Value | Uptime or duration |
|---|---|---|---|
| Plate armor | armor, `K = 2,000` | 3,000 armor | always |
| Bulwark Stance | percent | 15% | always |
| Iron Skin | percent cooldown | 40% | 12 s every 60 s |
| Last Stand | percent cooldown | 60% | 8 s every 180 s |
| Shield Block | flat per hit | 300 | 6 s every 12 s |
| Priest's Ward (external) | absorb | 5,000 | on demand |
| Raid aura (external) | percent | 10% | always |

- Tank HP: 40,000. Boss hits: 4,000 raw every 1.5 s, plus a 90,000 raw "Crush" every 30 s.
- The [interactive](../examples/w04-mitigation-layers.html) for checking your multiplicative totals.

## Steps

1. **Pipeline.** On `Pipeline`, implement the default order from lecture section 4: armor, then percentage layers multiplied, then flat reductions with a minimum of 1 damage, then absorb, then health. Each layer is a row with columns for its let-through fraction, doublings and cumulative let-through.
2. **Check against the lecture.** Enter the lecture's "classic warrior" stack (75% and 75%) and the five 20% layers. Your sheet must reproduce `M = 16` and `M = 3.052`.
3. **Kit totals.** For the Ironwarden, compute let-through, `M`, doublings and EHP in four states: passive only, passive plus Iron Skin, passive plus Last Stand, everything at once.
4. **Crush test.** For each state, compute the damage the Crush deals after all layers (with and without the Ward) and whether the tank survives from full health.
5. **Order test.** Move Shield Block to before the percentage layers. Recompute the damage from a normal 4,000 hit in the passive state. Report the difference per hit and per minute.
6. **Additive counterfactual.** On `Audit`, recompute the "everything" state as if all percentage layers (armor included) added in one pool. Report whether the tank becomes immune.
7. **Recommendation.** Decide whether the kit needs a rule (shared cooldown, total soft cap, or a Crush that ignores some layers). Justify it with doublings.

## Deliverable

The completed sheet and a memo of at most 400 words to the encounter team. The memo must state the Ironwarden's doublings in each state, whether Crush is survivable without cooldowns, and your recommended rule.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Pipeline correctness | Reproduces both lecture test values; order is explicit and editable | One test value off or order hard-coded | Test values not reproduced | 25% |
| Kit analysis | All four states correct with let-through, `M`, doublings, EHP | Minor arithmetic slips in one state | States missing or conceptually wrong | 25% |
| Order and additive tests | Both computed and the size of each effect stated in numbers | Computed but not interpreted | Missing | 20% |
| Recommendation | Rule chosen and justified in doublings, trade-off named | Rule chosen, weak justification | No clear recommendation | 20% |
| Memo writing | Plain, numeric, fits the word limit | Some vague claims | Hard to act on | 10% |
