# MMO401 · Lab 08: The honesty ceiling

**Week:** 8 ([lecture](../lectures/w08-player-banks-loans-and-scams.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs.
**Counts toward:** ABM labs (40% of the course grade).

## Objective

Simulate a player-run bank week by week with random deposits, random lending demand and a banker whose interest fades. Find when the banker's best move flips from honest to theft, then test three enforcement rules and say which one a designer should ship.

## Starter materials

No code file is provided. Build the model in a spreadsheet or in Python (standard library plus `matplotlib` if you want charts). The model is fully specified here.

**State each week `w`** (start at `w = 0`):

| Variable | Start | Update each week |
|---|---|---|
| Deposits `D` (billion) | 20 | `D ← D × (1 + g_w)`, with `g_w` drawn uniform on [4%, 16%] (mean 10%) |
| Lending demand `L` (billion) | 60 | `L ← L × (1 + h_w)`, with `h_w` drawn uniform on [0%, 6%] (mean 3%) |
| Quit chance `δ` | 1% | `δ ← min(1, δ + 0.05 points)` (so 1.05% in week 1, 1.10% in week 2, ...) |
| Spread `s` | 2% | constant |
| Penalty `K` | 0 | set by the enforcement rule |

Each week compute `V = s × min(D, L) / δ` and `S = D − K`. The banker steals in the first week where `S > V`. Record that week and `D` at that week. Also stop at week 104 if no theft happens.

**Reference run (no randomness).** Set every draw to its mean (`g_w = 10%`, `h_w = 3%`) and keep `K = 0`. Use this order each week: update `D`, `L` and `δ` (skip the update in week 0), then compare `V` and `S`. Your model must reproduce these rows:

| Week | `D` | `L` | `δ` | `V` | `S` | Best move |
|---|---|---|---|---|---|---|
| 0 | 20.0 | 60.0 | 1.00% | 40.0 | 20.0 | Honest |
| 10 | 51.9 | 80.6 | 1.50% | 69.2 | 51.9 | Honest |
| 16 | 91.9 | 96.3 | 1.80% | 102.1 | 91.9 | Honest |
| 17 | 101.1 | 99.2 | 1.85% | 107.2 | 101.1 | Honest |
| 18 | 111.2 | 102.1 | 1.90% | 107.5 | 111.2 | Steal |

Theft happens in week 18.

**Seeds.** For random runs use 1,000 runs. In Python use `random.Random(seed)` with seeds 0 to 999 so your results are reproducible. In a spreadsheet use 200 runs with `RAND()` and paste values before you report.

## Steps

### Part A: build and verify (40 min)

1. Build the week-by-week model and reproduce the reference table.
2. Plot `V` and `S` against weeks for the reference run on one chart and mark the crossing.

### Part B: randomness (30 min)

3. Run 1,000 random runs (or 200 in a spreadsheet). Record the theft week of each.
4. Report the median theft week, the 10th and 90th percentiles, and the share of runs with no theft by week 104. Plot a histogram of theft weeks.

### Part C: three enforcement rules (40 min)

Test each rule on the same seeds.

5. **Ban risk.** `K = 0.3 × D` (the banker expects to lose 30% of the loot's value to bans and confiscation).
6. **Deposit cap.** The game refuses deposits above `1.5 × L`. Clamp `D` each week.
7. **Server collateral.** The banker must lock their own collateral equal to 40% of `D` in a server escrow that pays out to depositors on theft. Model it as `K = 0.4 × D`, and note that the banker must own that much ISK, so compute how many runs have `0.4 × D` above a banker wealth of 50 billion (those banks cannot operate under the rule).

8. For each rule, report the same statistics as step 4 and one cost to players (who can no longer do what).

## Deliverable

- The spreadsheet or script, with a short README (up to 10 lines).
- A report of up to 2 pages: the Part A table and chart, the Part B statistics and histogram, a table comparing the baseline and three rules, and a 250-word recommendation. Name the rule you would ship, cite your own numbers, and say which player group pays for it.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Model correctness (Part A) | Reference table reproduced, chart marks the crossing | Crossing within two weeks of the reference | Model wrong | 30 |
| Random runs (Part B) | 1,000 (or 200) seeded runs, percentiles and histogram correct | Statistics present with errors | Missing | 20 |
| Enforcement rules (Part C) | All three rules on the same seeds, statistics and a player cost for each | Two rules, or costs missing | Fewer than two rules | 25 |
| Recommendation | Uses own numbers, names who pays, links back to the lecture's `D*` | Plausible but not backed by the runs | Missing | 20 |
| Reproducibility | Seeds fixed, runs first time | Runs with small fixes | Does not run | 5 |
| **Total** | | | | **100** |
