# GD203 · Lab 10 reference sheet

This is the instructor's reference for [lab 10](lab10.md), computed from the default player curve and role templates before any tuning. Release it at the start of week 11. Students whose own sheet is incomplete can start [lab 11](lab11.md) from these values.

All numbers come from the lab 10 definitions and the formulas in [week 10](../lectures/w10-enemy-design-by-the-numbers.md). Values are rounded for display. Keep full precision in the sheet.

## Player curve

`P(L) = 10 × 1.06^(L − 1)`, `H(L) = 100 × 1.05^(L − 1)`.

| Level | P (DPS) | H |
|---|---|---|
| 1 | 10.00 | 100.0 |
| 3 | 11.24 | 110.3 |
| 5 | 12.62 | 121.6 |
| 8 | 15.04 | 140.7 |
| 15 | 22.61 | 198.0 |
| 22 | 34.00 | 278.6 |
| 25 | 40.49 | 322.5 |
| 30 | 54.18 | 411.6 |

## Stat blocks

`h = P × t`, `d = s × H / t`, damage per hit `= d × interval`. Two columns do not depend on level, because every role is defined in player units.

| Role | Hit size (share of H) | Room-cost share alone (`s`) |
|---|---|---|
| Fodder | 1.6% | 2% |
| Soldier | 3.6% | 9% |
| Caster | 10.0% | 12% |
| Elite | 5.25% | 35% |

No default role hits above 25% of `H`, so the hit-size check is green everywhere before tuning.

Raw values at the room levels:

| Level | Role | h | d (DPS) | Damage per hit | Priority ratio d/h |
|---|---|---|---|---|---|
| 3 | Fodder | 16.9 | 1.47 | 1.76 | 0.087 |
| 8 | Soldier | 75.2 | 2.53 | 5.07 | 0.034 |
| 8 | Caster | 45.1 | 5.63 | 14.07 | 0.125 |
| 15 | Fodder | 33.9 | 2.64 | 3.17 | 0.078 |
| 15 | Elite | 452.2 | 3.46 | 10.39 | 0.0077 |
| 22 | Soldier | 170.0 | 5.01 | 10.03 | 0.029 |
| 22 | Caster | 102.0 | 11.14 | 27.86 | 0.109 |
| 30 | Fodder | 81.3 | 5.49 | 6.59 | 0.068 |
| 30 | Caster | 162.6 | 16.46 | 41.16 | 0.101 |
| 30 | Elite | 1,083.7 | 7.20 | 21.61 | 0.0066 |

The priority order is the same at every level: caster, fodder, soldier, elite.

## Breakpoint pass (step 3)

Assumed weapon: one hit every 0.8 s for `0.8 × P`. The soldier's untuned health is `5P`, so it takes `5P / 0.8P = 6.25`, rounded up to 7 hits, at every level. The 7-hit step is `4.8P < h ≤ 5.6P`, and its middle is `h = 5.2P`.

| Level | Hit | Untuned h (5P) | Centered h (5.2P) |
|---|---|---|---|
| 5 | 10.10 | 63.1 | 65.6 |
| 15 | 18.09 | 113.0 | 117.6 |
| 25 | 32.39 | 202.4 | 210.5 |

Margins, using week 4's rule that damage can range from `h / n` up to just under `h / (n − 1)`:

- Untuned (`h = 5P`): damage can fall 10.7% or rise 4.2% before the hit count changes.
- Centered (`h = 5.2P`): damage can fall 7.1% or rise 8.3%.

## Room costs before tuning

Because every stat is in player units, each room's cost as a share of `H` is the same at any level. The table uses focus fire for the best and worst orders and `a = 0.4` for the AoE class.

| Room | Best order | Best cost | Worst cost | AoE cost (a = 0.4) | Budget | Best order passes? |
|---|---|---|---|---|---|---|
| A | 5 fodder (any order) | 30.0% | 30.0% | 25.0% | 20% | No |
| B | caster, soldier, soldier | 49.8% | 79.0% | 75.0% | 40% | No |
| C | fodder ×3, elite | 54.9% | 127.0% | 102.5% | 60% | Yes |
| D | caster ×2, soldier ×3 | 122.4% | 210.0% | 127.5% | 70% | No |
| E | caster ×2, fodder ×2, elite | 108.7% | 314.3% | 157.5% | 90% | No |

Hand check for room B. The caster dies at 3 s, the soldiers at 8 s and 13 s. Cost share `= 0.12 × 3/3 + 0.09 × 8/5 + 0.09 × 13/5 = 0.120 + 0.144 + 0.234 = 0.498`.

AoE shortcut. Under AoE every enemy dies at `t / a`, so each costs `s / a` and the room costs `Σs / a`. Room A is `0.10 / 0.4 = 25%`.

Room D's best-to-worst gap is 87.6 points of player health (341 against 585 health at level 22). Both orders kill the untuned player, so before tuning the gap does not yet decide the fight. After tuning, a gap that spans the budget line is what makes kill order a real decision.

## What tuning should find

Four of five rooms fail, on purpose. The default targets are too expensive for packs, because pack cost grows with the square of pack size. There is no single correct tuned sheet. Look for these in student work:

- Changes made to role targets (`t`, `s` or interval), never to individual room cells.
- A lower caster or soldier cost share is the fastest route to passing rooms B and D. Room A needs a fodder share of at most 0.0133 (`0.2 / 15`).
- The AoE condition in step 7 (AoE cost at least a third of budget) holds for every untuned room.
- AoE at `a = 0.4` beats focus fire only in room A (25.0% against 30.0%). For a pack of 5 identical enemies the break-even is `a > 2/(5 + 1) = 0.33`, and 0.4 clears it. In the mixed rooms focus fire on the high-ratio casters is cheaper. Check that students read the comparison column this way.
