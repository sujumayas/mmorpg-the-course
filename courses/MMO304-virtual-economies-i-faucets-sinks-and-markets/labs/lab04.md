# MMO304 · Lab 04: The real value of every gold number

**Week:** 4 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the Models assignment (30%)

## Objective

Extend your week 3 simulator with a price level, a daily inflation rate and a real-value column for every gold amount in a design document. Then decide, for each amount, whether it should stay fixed, follow money per player, or become a percentage, and defend the policy with numbers from your sheet.

This lab uses [week 4](../lectures/w04-money-supply-per-capita-and-inflation.md): `m(t + 1) = m(t) + n − σ × m(t)`, the price level `P = m × V / q`, the inflation rate `π(t) = P(t)/P(t − 1) − 1`, real value `X / P` and weight `L / m`. It builds on [lab 03](lab03.md).

## Starter materials

- Your lab 03 spreadsheet or Python simulator. If you did not finish it, start a new sheet; this lab only needs the per-player update above.
- Parameter block (named cells or a dictionary):

| Parameter | Meaning | Base value |
|---|---|---|
| `m0` | Money per player on day 0 | 2,000 |
| `n` | Net faucet per player-day, `h(g − r)` in week 3 notation | 40 |
| `σ` | Stock sink share per day, `τ × v` in week 3 notation | 0 |
| `V` | Velocity, share of money spent per day | 0.05 |
| `q` | Potions sold per player-day | 1 |
| `days` | Horizon | 730 |

- The design document to audit. Every team uses the same table:

| # | Rule | Amount | Who mostly pays or receives it |
|---|---|---|---|
| 1 | Level 5 quest reward | 60 gold | Newcomers receive |
| 2 | Level 30 quest reward | 400 gold | Mid-level players receive |
| 3 | Starter armour set, NPC vendor | 900 gold | Newcomers pay |
| 4 | Repair after a dungeon wipe | 150 gold | Everyone pays |
| 5 | Fast-travel fee | 25 gold | Everyone pays |
| 6 | Guild creation | 10,000 gold | Organisers pay |
| 7 | Bank tab 5 | 50,000 gold | Veterans pay |
| 8 | Luxury mount | 200,000 gold | Veterans pay |
| 9 | Auction house cut | 5% of sale price | Sellers are charged |
| 10 | Maximum gold per character | 2,000,000 gold | Veterans are limited |

## Steps

1. **Price level.** Add columns for `P(t) = m(t) × V / q` and `π(t)`. With the base values, reproduce the week 4 lecture's first table at days 1, 30, 60, 180, 365 and 730, to the stated rounding.
2. **Stock sink.** Set `σ = 0.01` and reproduce the second table, including the steady state `m* = n / σ = 4,000`.
3. **Real value columns.** For each rule 1 to 8 and rule 10, add a column with its real value in potions, `X / P(t)`. For rules 6 to 8 and 10, also add the weight `X / m(t)`. Explain in one line why rule 9 needs no column.
4. **When does each rule stop working?** For each of rules 1 to 8, choose a threshold below which it no longer does its job (for example, "the level 5 reward must buy at least a quarter of a potion," or "the mount must cost at least 5 average balances"). Record the first day each rule crosses its threshold with `σ = 0`, and whether it ever crosses with `σ = 0.01`.
5. **The cap.** A top veteran's balance is 40 times `m`. On what day does that veteran hit the rule 10 cap with `σ = 0`? With `σ = 0.01`?
6. **Policy.** Classify every rule as fixed, indexed to `m`, or percentage. For each indexed rule, write the index formula (for example, `mount price = 100 × m(t)`). Rerun steps 3 and 4 with your policy in place.
7. **One faucet trap.** Add a version where rule 2 is indexed to `P(t)`. Model it as `n` rising by the same proportion as `P` above 100, so `n(t) = 40 × P(t) / 100`. Plot `m(t)` for 365 days next to the base run and describe the shape.

## Deliverable

The spreadsheet or notebook, and a memo of 400 to 500 words to your lead designer. The memo recommends the policy from step 6, quotes at least four numbers from your sheet (including one threshold day from step 4 and the cap day from step 5), and explains the result of step 7 in two or three sentences.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Model and reproduced tables | Both lecture tables reproduced to the stated rounding; steady state shown | One table off or rounding errors | Tables not reproduced | 20% |
| Real value and threshold analysis | All nine columns correct; every threshold stated and its crossing day found for both `σ` values | Columns correct, thresholds vague or missing for some rules | Columns missing or wrong | 25% |
| Cap analysis | Both cap days correct with working shown | One correct | Missing | 10% |
| Policy with formulas | Every rule classified, each indexed rule has a formula, and the rerun shows the policy holds | Classified without formulas, or no rerun | Missing | 20% |
| Faucet trap | Correct plot and a clear explanation of the positive feedback | Plot without explanation | Missing | 10% |
| Memo | Recommendation argued from the sheet's numbers, trade-offs named, within length | Recommendation made, weakly supported | Opinion without numbers | 15% |

<details>
<summary>Instructor check values</summary>

- Base run: `P(365) = 830`, `π(365) = 0.24%`; `σ = 0.01`: `P(365) = 197.45`, `m* = 4,000`.
- Rule 1 real value at day 0 is 0.60 potions; at `P = 240` (day 70) it reaches 0.25. With `σ = 0.01` the long-run value is `60 / 200 = 0.30`, so a 0.25 threshold is never crossed.
- Rule 8 weight at day 0 is 100 average balances. With `σ = 0` it reaches 5 when `m = 40,000`, on day 950, beyond the horizon. With a stricter threshold of 20 balances (`m = 10,000`) it crosses on day 200.
- Cap: the veteran holds `40 × m`, so the cap binds when `m = 50,000`, day `(50,000 − 2,000) / 40 = 1,200`, beyond the two-year horizon. With `σ = 0.01` the veteran's balance levels off near `40 × 4,000 = 160,000` and never binds. Students who model the veteran with their own higher `n` get earlier days; accept any consistent method.
- Step 7: with `n(t) = 40 × P / 100 = 40 × m / 2,000`, the update is `m(t + 1) = 1.02 × m(t)`, exponential growth of 2% a day. `m(365) ≈ 2,000 × 1.02^365 ≈ 2.7 million`.

</details>
