# MMO304 · Lab 02: Pricing the three kinds of value

**Week:** 2 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the Models assignment (30%)

## Objective

Separate an item's price into functional, hedonic and social parts using a price history, test whether the `log2` social-value model from week 2 fits better than a simple alternative, and forecast what a planned patch will do to five items.

This lab uses [week 2](../lectures/w02-functional-hedonic-and-social-value.md): `V(t) = F(t) + H + S(t)`, `S = s × log2(1/f)` and the ownership update `f(t+1) = f(t) + q(1 − f(t)) − c f(t)`.

## Starter materials

- A spreadsheet or Python 3 (standard library, plus any plotting tool you like).
- The invented price history below, from a test server with constant population and weekly churn `c = 2%`. Prices are weekly averages in gold. `f` is the measured share of active players who own each item.

| Week | Glacier mount price | Glacier mount `f` | Ember mount price | Ember mount `f` | Tier-2 blade price | Tier-2 blade `f` |
|---|---|---|---|---|---|---|
| 0 | 10,140 | 0.50% | 10,140 | 0.50% | 23,140 | 0.50% |
| 10 | 7,320 | 3.55% | 10,440 | 0.41% | 19,250 | 7.44% |
| 20 | 6,570 | 5.95% | 10,730 | 0.33% | 18,480 | 12.66% |
| 30 | 6,170 | 7.84% | 11,020 | 0.27% | 4,890 | 16.60% |
| 40 | 5,920 | 9.33% | 11,310 | 0.22% | 4,650 | 19.56% |

- Notes supplied by the "live team": the Glacier and Ember mounts are two recolours of the same model with no functional use. The Ember mount was event-only and can no longer be obtained. The Tier-2 blade was the best weapon until the Tier-3 patch, which landed at week 25.
- The planned patch for the forecast in step 5: Tier 4 releases; the Ember mount returns to the store for two weeks; the Glacier mount's drop chance doubles.

## Steps

1. **Fit `s` and `H` from the recolours.** The two mounts share `F = 0` and should share `H`. For each row, compute `log2(1/f)` for each mount. Fit a straight line of price against `log2(1/f)` using all ten mount observations. The slope is your estimate of `s` and the intercept is `H`.
2. **Check the fit.** Plot price against `log2(1/f)` with the fitted line. Report the largest error in gold.
3. **Test an alternative.** Fit the same data with `S = s' × (1 − f)` instead. Compare the largest error. Write two sentences on which model you would trust for an item with `f` near 0.01% and why.
4. **Split the blade.** Using your `s`, compute the blade's `S` each week, then `F + H = price − S`. Estimate `F0` before the patch, `F0 × r` after it, and `r`. Assume the blade's `H` is 500.
5. **Forecast the patch.** Predict each item's value two weeks and twenty weeks after the planned patch. State every assumption (for example, how far `f` rises while the Ember mount is in the store).
6. **Who complains.** For each change in the patch, name the group of players who lose value and estimate how much per player.

## Deliverable

The sheet or script with both fits, the plot from step 2, and a one-page patch forecast table with a paragraph of about 250 words arguing for or against the Ember mount's return, using your numbers.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Fit of `s` and `H` | Both parameters within 10% of the check values, method shown | Parameters roughly right, method unclear | Missing or wrong | 25% |
| Model comparison | Both fits, errors reported, reasoned choice for very rare items | Fits done, weak reasoning | One model only | 20% |
| Blade split | `F0`, `r` and weekly `S` correct and consistent | Minor arithmetic errors | Missing | 20% |
| Forecast | All three changes forecast with stated assumptions and numbers | Forecast without assumptions | Missing | 20% |
| Argument | Uses the forecast numbers, names losers and amounts | Opinion with some numbers | Opinion only | 15% |

<details>
<summary>Instructor check values</summary>

The table was generated with `H = 2,500`, `s = 1,000`, blade `F0 = 15,000`, `r = 0.12` (so `F0 × r = 1,800`), blade `H = 500`, then rounded to the nearest 10 gold.

- Ownership paths: Glacier `q = 0.35%` a week, Ember `q = 0`, blade `q = 0.8%`, all starting at 0.5%, churn 2%.
- Mount fit: slope near 1,000, intercept near 2,500. Example: Glacier week 0, `log2(1/0.005) = 7.64`, price `2,500 + 7,644 ≈ 10,140` after rounding.
- Linear alternative `s'(1 − f)` fits poorly: mount prices vary by about 5,400 gold while `1 − f` changes by under 9 percentage points, so it needs an enormous `s'` and still misses the curvature.
- Blade week 0: `S = 7,644`, so `F + H = 15,496`, `F0 ≈ 15,000`. Week 30: `S = 1,000 × log2(1/0.166) = 2,591`, `F + H = 2,299`, `F ≈ 1,800`, so `r ≈ 0.12`. Accept 0.11-0.13 with a stated method.
- Ember mount forecast: if its `f` rises from 0.22% to 1.2% in the store window, social value falls by `log2(1.2/0.22) ≈ 2.4` halvings, about 2,400 gold per owner.

</details>
