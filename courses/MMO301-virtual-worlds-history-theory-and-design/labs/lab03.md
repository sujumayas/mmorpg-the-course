# MMO301 · Lab 03: The closed loop and the faucet

**Week:** 3 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** feeds case study 1 (part of the case-studies assignment, 40%)

## Objective

Build the week 3 resource model yourself, reproduce Ultima Online's closed-loop collapse in numbers, show what a hoarding minority does to everyone's supply, and design a drain package for the faucet version that keeps stored items under a database budget without punishing ordinary players.

This lab uses [week 3](../lectures/w03-ultima-online-the-simulation-dream-and-its-limits.md): the three stocks `B`, `W`, `H`, the daily update, the closed-loop steady supply `s* = d × R`, and the faucet steady hoard `σ(1 − d)/d`.

## Starter materials

- A spreadsheet or Python 3 (standard library only; any plotting tool).
- Parameter block. Put these in named cells or a dictionary:

| Parameter | Meaning | Base value |
|---|---|---|
| `R` | Total resources (closed mode) | 200,000 |
| `σ` | Spawn capacity per day | 6,000 |
| `N` | Active players | 1,500 |
| `c` | Demand per player per day | 4 |
| `d` | Return rate per day | 0.005 |
| `days` | Days simulated | 365 |

- Spreadsheet layout, one row per day from 0 to `days`. Row 0 holds the starting stocks (`Bank = R`, `W = 0`, `H = 0`); every later row uses the row above:

| Column | Header | Formula for row `t` (closed mode) |
|---|---|---|
| A | `t` | previous `t` + 1 |
| B | `s` spawned | `MIN(σ, Bank of row t−1)` |
| C | `h` harvested | `MIN(W of row t−1 + s, c × N)` |
| D | `W` world | `W of row t−1 + s − h` |
| E | `H` before return | `H of row t−1 + h` |
| F | `r` returned | `d × E` |
| G | `H` held | `E − F` |
| H | `Bank` | `Bank of row t−1 − s + r` |

  For faucet mode, set column B to `σ` and column H to a constant (the bank is unused), since returns are destroyed.

- Python skeleton:

```python
def simulate(R=200_000, sigma=6_000, N=1_500, c=4, d=0.005, days=365, mode="closed"):
    B, W, H = float(R), 0.0, 0.0
    rows, dry = [], None
    for t in range(1, days + 1):
        s = min(sigma, B) if mode == "closed" else sigma
        if mode == "closed":
            B -= s
        W += s
        h = min(W, c * N); W -= h; H += h
        r = d * H; H -= r
        if mode == "closed":
            B += r
        if dry is None and h < 0.5 * c * N:
            dry = t
        rows.append((t, B, W, H, s, h, r))
    return rows, dry
```

## Steps

1. **Build and verify.** On day 1 of the base case you must get `B = 194,030`, `H = 5,970`, `s = 6,000`. On day 37 you must get `s = 2,862`, and from day 38 on `s = 1,000`.
2. **Reproduce the lecture tables.** Run the return-rate table (`d` = 0.005, 0.01, 0.02, 0.03, 0.05) and the added-resources table (`R` = 200,000, 400,000, 1,200,000 at `d = 0.005`). Your steady supply and dry days must match the lecture exactly.
3. **Check the formula.** For each run in step 2, compare day-365 supply with `min(σ, d × R)`. Explain in one sentence the one run where `σ` is the binding limit.
4. **Hoarding minority.** Split `H` into two stocks. Casual players take 70% of each day's harvest and return `d_c = 0.02` per day. Hoarders (10% of players) take 30% and return `d_h = 0.002`. Both returns go to the bank. Run 3,000 days. Record steady supply and the dry day, and compare with everyone at `d = 0.02`. Derive the closed-form steady supply `s* = R / (1 + Σ ηᵢ(1 − dᵢ)/dᵢ)`, where `ηᵢ` is each group's share of harvest, and check it against your simulation.
5. **Switch to faucet.** Keep the two groups. Run faucet mode for 365 days and to steady state. Record each group's held stock.
6. **Design a drain package.** Your database budget is 400,000 held units at steady state. You may add at most two drains of your own design, each described as an in-game mechanism (for example, "house storage beyond 500 items decays at 1% per day", or "crafting upgrades consume stored materials"). Translate each into a change in `d_c`, `d_h` or both. You may not change `σ`, `N`, `c` or the 70/30 harvest split. Meet the budget.
7. **Price it for players.** For each drain, compute how many units per day a typical casual player and a typical hoarder lose to it at steady state (divide the group's daily return by its head count, 1,350 casual players and 150 hoarders). Say which players pay and whether they would accept it at launch or only if it were there from day one.

## Deliverable

The sheet or script; three plots (the base closed run's `B` and `H` over 365 days, supply per day for the hoarding run versus the all-casual run, and held stock by group in your final faucet design); and a memo of about 400 words. The memo must give your drain package, its effect on `d_c` and `d_h`, the steady held stock, per-player daily costs by group, and one reason a player might hate each drain.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Model correctness | Day-1 and day-37 checks pass; all step-2 values match | One value off | Checks fail | 25% |
| Formula and explanation | `min(σ, dR)` checked for every run; `σ`-limited case explained | Checked, explanation thin | Missing | 10% |
| Hoarding analysis | Two-group simulation and closed form agree; effect on supply stated as a number | Simulation only | Missing or wrong | 20% |
| Drain package | Meets the 400,000 budget; targets the group that causes the hoard; mechanisms are concrete | Meets budget with blunt changes that hit casual players hardest | Misses budget | 25% |
| Memo | Numbers from the model, per-player costs by group, honest downsides, launch timing discussed | Some numbers, thin on costs or timing | Opinion without numbers | 20% |

<details>
<summary>Instructor check values</summary>

- Step 2: see the lecture's tables. Dry days: `d = 0.005` day 37, `d = 0.01` day 42, others never. `R = 400,000` day 82.
- Step 3: at `d = 0.05`, `d × R = 10,000 > σ`, so supply is capped at 6,000 and the bank keeps a large balance (86,000 on day 365).
- Step 4: steady supply `200,000 / (1 + 0.7 × 49 + 0.3 × 499) = 200,000 / 185 ≈ 1,081` per day (the simulation reads 1,225 on day 365, still settling, and 1,081 by day 3,000). Dry day 46. With everyone at `d = 0.02` supply is 4,000 and never dry. The hoarders are 10% of players and cut everyone's supply by about 73%.
- Step 5: faucet steady held stock is `0.7 × 6,000 × 0.98 / 0.02 = 205,800` casual plus `0.3 × 6,000 × 0.998 / 0.002 = 898,200` hoarders, 1,104,000 in total. Day 365: 205,671 casual and 465,666 hoarders.
- Step 6: with `d_c` unchanged, hoarders must hold at most 194,200, which needs `d_h ≥ 1,800 / 196,000 ≈ 0.0092`, about 4.6 times their base rate. Raising `d_c` alone cannot meet the budget, since the hoarders' 898,200 is already over it. Good packages target stored quantity (upkeep or decay above a storage threshold, consumables that use stored goods) rather than a flat rate on everyone.
- Step 7: at steady state each group returns exactly what it harvests, so hoarders lose 1,800 per day (12.0 per hoarder) and casual players 4,200 per day (about 3.1 per casual player) whatever the rates. The drain changes how much each group holds, not how much it loses per day. At `d_h = 0.0092` hoarders hold about 193,900. Strong memos notice this and argue about fairness in terms of stock held, not daily loss.

</details>
