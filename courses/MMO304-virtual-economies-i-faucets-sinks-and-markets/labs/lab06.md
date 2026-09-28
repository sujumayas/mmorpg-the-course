# MMO304 · Lab 06: Estimating a market from auction data

**Week:** 6 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the Models assignment (30%)

## Objective

Fit straight-line supply and demand curves to a week of order-book data for one item, use them to predict what a fee change and a content patch will do, and check your predictions against what actually happened. You will see how close a two-line model gets, and where it misses.

This lab uses [week 6](../lectures/w06-supply-demand-and-equilibrium-in-auction-houses.md): `Q_d = a − b × P`, `Q_s = c + d × P × (1 − t)`, the equilibrium `P(t) = (a − c) / (b + d(1 − t))`, the buyer's share `d / (b + d)`, and the sink `t × P × Q`.

## Starter materials

- A spreadsheet (you will use `SLOPE` and `INTERCEPT`, or `LINEST`) or Python 3 with any least-squares routine.
- The item is a mid-level healing flask on one server of a fictional MMO. The market charges sellers a 2% fee during the data week.
- **Order-book schedules, averaged per day over the data week.** "Demand" is how many flasks buyers' standing offers would take per day at that price. "Supply" is how many flasks sellers would list per day if they received that price after the fee.

| Price (gold) | Demand (flasks per day) | Supply (flasks per day, at this net price) |
|---|---|---|
| 60 | 851 | 372 |
| 70 | 790 | 397 |
| 80 | 722 | 482 |
| 90 | 653 | 529 |
| 100 | 603 | 585 |
| 110 | 552 | 614 |
| 120 | 486 | 657 |
| 130 | 413 | 716 |
| 140 | 346 | 773 |
| 150 | 335 | 800 |
| 160 | 231 | 884 |
| 170 | 173 | 912 |
| 180 | 118 | 973 |

- **What actually happened.** Averages over each week, from the server's trade log.

| Week | Change | Average price buyers paid | Flasks traded per day |
|---|---|---|---|
| Data week | Fee 2% | 104.4 | 575 |
| Week 2 | Fee raised to 5% | 106.3 | 561 |
| Week 3 | Fee 5%, new raid requires the flask | 124.9 | 649 |

## Steps

1. **Fit the lines.** Fit demand as a line in price and report `a` and `b` (note the sign of the slope). Fit supply as a line in net price and report `c` and `d`. Plot both schedules with their fitted lines on one chart.
2. **Check the fit.** Compute the residual (actual minus fitted) for each row. Which three prices fit worst? Is there a pattern, or is it noise?
3. **Predict the data week.** Using your fit and `t = 0.02`, compute the equilibrium price, the seller's net price and the daily quantity. Compare with the data-week row.
4. **Predict the fee change.** Compute `P`, `P_s`, `Q`, the buyer's share of the wedge and the gold removed per day at `t = 0.05`. Compare with week 2. By how much did the fee change move the price that buyers paid, and how much of the extra fee fell on sellers?
5. **Explain the patch.** Assume the raid moved only `a` and left `b`, `c` and `d` unchanged. Use week 3's observed price and quantity to estimate the new `a`. Then predict the week 3 price from your supply curve and the new `a`, and compare.
6. **Deadweight loss.** Estimate the trades per day lost to the 5% fee in week 2, and the deadweight loss in gold per day, with the triangle rule from the lecture.
7. **Recommendation.** Your lead wants the flask market to remove 5,000 gold a day after the raid. Find the fee that does it with your week 3 curves, and state the buyer's and seller's parts of the wedge at that fee.

## Deliverable

The spreadsheet or notebook and a memo of about 350 words. The memo gives your fitted curves, reports how close your predictions for weeks 2 and 3 were (as percent errors), names one reason the model may miss, and makes the step 7 recommendation with its effect on buyers and sellers.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Fitted curves and chart | Parameters correct to 2 decimals, chart labelled, signs handled | Parameters close, chart missing labels | Wrong fit or no chart | 20% |
| Residual check | Worst rows identified, pattern discussed sensibly | Residuals computed, not discussed | Missing | 10% |
| Fee-change prediction | All five quantities correct, compared with week 2 with percent errors | Most quantities correct | Missing or wrong method | 20% |
| Patch estimate | New `a` estimated correctly and used to predict week 3 | Method right, arithmetic slips | Missing | 15% |
| Deadweight loss | Lost trades and loss computed with working | One of the two | Missing | 10% |
| Recommendation and memo | Fee found, incidence stated, one limitation named, within length | Fee found without incidence or limitation | Opinion without numbers | 25% |

<details>
<summary>Instructor check values</summary>

- Least-squares fits: demand `a ≈ 1,211.37`, `b ≈ 6.07`; supply `c ≈ 70.09`, `d ≈ 4.99`. The data were generated from `a = 1,200`, `b = 6`, `c = 60`, `d = 5` with noise, so answers near these are fine.
- Data week, `t = 0.02`: `P ≈ 104.10`, `P_s ≈ 102.02`, `Q ≈ 579`. Observed 104.4 and 575, errors under 1%.
- Week 2, `t = 0.05`: `P ≈ 105.55`, `P_s ≈ 100.27`, `Q ≈ 570`, buyer share `4.99 / 11.06 ≈ 45.1%`, gold removed about 3,010 per day. Observed 106.3 and 561. The price rose about 1.4 to 1.9 gold, and sellers' net fell about 1.8 gold.
- Week 3: from `649 = a' − 6.07 × 124.9`, `a' ≈ 1,407`. Predicted `P = (1,407 − 70.09) / (6.07 + 4.99 × 0.95) ≈ 123.7`, within about 1% of the observed 124.9.
- Deadweight loss at 5%, using the no-fee equilibrium (`P ≈ 103.17`, `Q ≈ 584.8`): about 14.5 lost trades per day and roughly `½ × 5.3 × 14.5 ≈ 38` gold per day.
- Step 7 with `a' ≈ 1,407`: the sink at 5% is about `0.05 × 123.7 × 656 ≈ 4,060`; a fee near 6.2% gives about 5,000 gold per day. Buyers still pay about 45% of the wedge.

</details>
