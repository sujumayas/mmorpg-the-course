# MMO304 · Lab 05: Sink targeting

**Week:** 5 · **Time:** 2 hours in lab plus about 2 hours at home · **Weight:** part of the Models assignment (30%)

## Objective

Compare four sink packages on a realistic server snapshot, measuring each by what it does to prices and to each group of players, not only by the gold it removes. Then design a package that meets a producer's brief and test it against a returning-player event.

This lab uses [week 5](../lectures/w05-deflation-and-hoarding.md): spending `S = Σ B_i × v_i`, money supply `M = Σ B_i`, effective velocity `V = S / M` and the price level `P = S / Q`.

## Starter materials

- A spreadsheet or Python 3.
- The server snapshot below. Treat each cohort as identical players. `Q` is one potion per active player per day, so `Q = 9,200`.

| Cohort | Players | Balance each | Share of balance spent per day `v` |
|---|---|---|---|
| New (first two weeks) | 3,000 | 250 | 25% |
| Levelling | 2,500 | 900 | 12% |
| Casual, max level | 2,000 | 3,000 | 5% |
| Raiders | 1,200 | 8,000 | 3% |
| Traders | 300 | 40,000 | 1.5% |
| Collectors | 200 | 120,000 | 0.3% |

- The four sink packages. Each is applied once to the snapshot, then prices are recomputed.

| Package | Description | How to model it |
|---|---|---|
| A. Repair increase | Repairs cost 20 more gold per player-day for a week | Each player pays `min(balance, 140)` |
| B. Auction cut | A 5% cut on all spending for a week | Each player pays `0.05 × 7 × balance × v` |
| C. Luxury mount | A 100,000-gold mount, bought by 40% of collectors and 10% of traders | Collectors' balance each falls by 40,000 on average, traders' by 10,000 |
| D. Balance tax | 2% of every balance, once | Each balance is multiplied by 0.98 |

## Steps

1. **Baseline.** Compute each cohort's total balance and spending, then `M`, `S`, `V` and `P`. Compute the share of gold and the share of spending held by the top two cohorts.
2. **Four packages.** For each package, compute the gold removed, the new `M`, `S`, `V` and `P`, and the percent change in `P`.
3. **Incidence.** For each package, compute the percent of each cohort's balance it took. Present a table with packages as rows and cohorts as columns.
4. **Efficiency.** For each package, compute "percent fall in `P` per 1% fall in `M`." Rank the packages.
5. **The brief.** Your producer asks for a package that removes at least 10% of `M` while lowering `P` by no more than 3% and taking no more than 5% of any newcomer's or levelling player's balance. Design one, from these four or your own, and show it meets all three conditions.
6. **Returning players.** A campaign brings back 150 dormant traders with 40,000 gold each, spending 3% a day for their first week. Compute `P` with and without your step 5 package. Propose one change to the campaign (not to the sink) that limits the price jump, and compute its effect.

## Deliverable

The spreadsheet or notebook and a one-page brief (about 400 words) for your producer. The brief recommends the step 5 package, shows the incidence table from step 3 for it and for the package you rejected, and states the returning-player risk from step 6 with a number.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Baseline and four packages | All values correct to 1 decimal place of `P` | One package wrong | Two or more wrong | 25% |
| Incidence table | Complete and correct, and the pattern described in a sentence | Complete, not interpreted | Missing | 15% |
| Efficiency ranking | Ratios correct and the ranking explained with spending rates | Ranking without explanation | Missing | 15% |
| Package meets the brief | All three conditions met and shown | One condition missed or not shown | Missing | 20% |
| Returning-player analysis | Both prices correct, mitigation modelled with a number | Prices correct, mitigation not modelled | Missing | 10% |
| Brief | Clear recommendation, both incidence tables, risk stated with a number | Recommendation weakly supported | Opinion without numbers | 15% |

<details>
<summary>Instructor check values</summary>

- Baseline: `M = 54,600,000`, `S = 1,297,500`, `V ≈ 2.38%`, `P ≈ 141.03`. Traders and collectors (500 players) hold 66% of gold and produce 19.4% of spending.
- A: removes 1,288,000 (2.4% of `M`), `S = 1,130,746`, `P ≈ 122.91` (−12.9%). Newcomers lose 56% of their balance.
- B: removes 454,125 (0.8%), `P ≈ 137.01` (−2.9%). Newcomers lose 8.75%.
- C: removes 11,000,000 (20.1%), `P ≈ 133.53` (−5.3%). Newcomers lose nothing.
- D: removes 1,092,000 (2.0%), `P ≈ 138.21` (−2.0%). Every cohort loses 2%.
- Efficiency (percent fall in `P` per 1% fall in `M`): A about 5.5, B about 3.5, D 1.0, C about 0.26.
- Step 5: C meets the removal and incidence conditions but lowers `P` by 5.3%. Scaling C down so collectors lose 25,000 each on average and traders 5,000 removes 6,500,000 (11.9%) and gives `S = 1,260,000` and `P ≈ 136.96` (−2.9%), which meets all three, narrowly. Other valid designs exist.
- Step 6: returning traders add `150 × 40,000 × 0.03 = 180,000` to spending. With no sink, `P ≈ (1,297,500 + 180,000) / 9,350 ≈ 158.0` if they also count in `Q` (one potion each), or 160.6 if `Q` stays 9,200. Accept either with the assumption stated.

</details>
