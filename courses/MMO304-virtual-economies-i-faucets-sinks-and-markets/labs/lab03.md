# MMO304 · Lab 03: Build the faucet/sink simulator

**Week:** 3 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the Models assignment (30%)

## Objective

Implement the week 3 money-supply model yourself, reproduce the lecture's five scenarios exactly, and then design a sink package that keeps prices inside a target band for two years on a server whose new-player numbers fall. You will leave with a working simulator you can extend in weeks 4, 5 and 12.

This lab uses [week 3](../lectures/w03-faucets-sinks-and-transformations.md): the daily update for `N` and `M`, the price index `P = 100 × m / 1,000`, and the steady states `m* = h(g − r) / (c + τv)` (constant population) and `m* = h(g − r) / (τv)` (no new players).

## Starter materials

- A spreadsheet or Python 3 (standard library only for the model; any plotting tool).
- Parameter block. Put these in named cells or a dictionary so every formula refers to them:

| Parameter | Meaning | Base value |
|---|---|---|
| `N0` | Starting players | 1,000 |
| `m0` | Starting gold per player | 1,000 |
| `J` | New players per day | 5 |
| `c` | Share of players quitting per day | 0.005 |
| `h` | Hours played per player per day | 2 |
| `g` | Faucet, gold per hour | 100 |
| `r` | Flow sink, gold per hour | 60 |
| `τ` | Trade tax | 0 |
| `v` | Share of money traded per day | 0.05 |

- Column layout for the spreadsheet version, one row per day from 0 to 730:

| Column | Header | Row 0 | Row `d+1` |
|---|---|---|---|
| A | `d` | 0 | `A_d + 1` |
| B | `N` | `N0` | `B_d + J − c × B_d` |
| C | `M` | `N0 × m0` | `C_d + B_d × h × (g − r) − τ × v × C_d − c × C_d` |
| D | `m` | `C / B` | `C / B` |
| E | `P` | `100 × D / 1,000` | same |
| F | Faucet today | `B × h × g` | same |
| G | Flow sink today | `B × h × r` | same |
| H | Tax today | `τ × v × C` | same |
| I | Quitters today | `c × C` | same |

- Python skeleton, if you prefer code:

```python
def simulate(N0=1000, m0=1000, J=5, c=0.005, h=2, g=100, r=60, tau=0.0, v=0.05, days=730):
    N, M = N0, N0 * m0
    rows = []
    for d in range(days + 1):
        rows.append((d, N, M, M / N, 100 * (M / N) / 1000))
        M = M + N * h * (g - r) - tau * v * M - c * M   # uses today's N
        N = N + J - c * N
    return rows
```

## Steps

1. **Build and verify.** Implement the model. On day 1 of the base case you must get `M = 1,075,000` and `m = 1,075`.
2. **Reproduce the five scenarios.** Run scenarios A to E from the lecture (base; 5% tax; `r = 80`; `J = 0`; `J = 0` with 5% tax). Your `m` at days 30, 90, 180, 365 and 730 must match the lecture's table to within 1 gold.
3. **Check the steady states.** For each scenario that has one, compute `m*` from the formula and confirm your simulation approaches it. For scenario A, compute the day `m` is halfway to `m*` with `ln 0.5 / ln(1 − c − τv)` and check it against the sheet.
4. **Flow chart.** For scenario B, plot the four daily flows (faucet, flow sink, tax, quitters) over two years. Mark the day on which tax plus quitters first exceeds half of the net faucet.
5. **The decline scenario.** Replace constant `J` with a falling one: `J(d) = 5 × (1 − d / 365)` for the first year and 0 after. Run it with base values and no tax, and plot `N`, `m` and `P`.
6. **Design a sink package.** Your target is that `P` stays between 100 and 1,000 for all 730 days of the decline scenario. You may change `r`, `τ`, and add at most one new sink of your own design (for example a housing upkeep of `u` gold per player per day, or a wealth fee of `k` per day on `M`). You may not change `g`, `h`, `c` or `J(d)`. Find a package that meets the target and record its parameters.
7. **Player cost.** For your package, compute how much a typical player pays per day in each sink on day 30 and on day 700. Write which players pay most.

## Deliverable

The sheet or script, the plots from steps 4 and 5, your final package's `P` curve with the 100-1,000 band drawn on it, and a design memo of about 400 words. The memo must give your package's parameters, the `P` values at days 180, 365 and 730, the daily cost to a typical player at days 30 and 700, and one reason a player might hate each sink you chose.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Model correctness | Day-1 check and all five scenarios within 1 gold | One scenario off | Two or more off, or day-1 check fails | 25% |
| Steady states | Formula values correct, convergence and halfway day shown | Formula values correct, no convergence check | Missing | 15% |
| Flows and decline | Both plots correct and labelled, crossing day marked | Plots present, labels or mark missing | Missing | 15% |
| Sink package | Meets the band for all 730 days, uses at least one stock sink, parameters justified | Meets the band but only by extreme values (for example a tax above 20%) | Misses the band | 25% |
| Memo | Numbers from the model, costs by player type, honest downsides | Some numbers, thin on downsides | Opinion without numbers | 20% |

<details>
<summary>Instructor check values</summary>

- Scenario values are in the week 3 lecture table. Day 1 base: `M = 1,075,000`.
- Scenario A halfway day: `ln 0.5 / ln 0.995 ≈ 138.3`.
- Scenario B flows on day 0: faucet 200,000, flow sink 120,000, tax 2,500, quitters 5,000. Net faucet 80,000, so tax plus quitters (7,500) starts far below half the net (40,000) and crosses it when `M` passes about 5.33 million, on day 79.
- Decline scenario with no tax: `P` passes 1,000 on day 157, reaches about 2,116 on day 365 and 5,050 on day 730, with about 74 players left (73.8). Some stock sink is required.
- A reference package that meets the band: `r = 75` plus a wealth fee of 0.5% of `M` per day. `P` is about 479 on day 180, 688 on day 365 and 950 on day 730, its maximum. Raising `r` alone cannot meet the band, since on a closed server only a stock sink creates a ceiling. Check any student package by rerunning it; do not require this one.

</details>
