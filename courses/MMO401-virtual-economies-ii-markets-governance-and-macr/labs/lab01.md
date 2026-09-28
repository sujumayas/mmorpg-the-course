# MMO401 · Lab 01: Reading a real economic report

**Week:** 1 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the ABM labs (40%)

## Objective

Do the measure job of an in-house economist on real data. You rebuild headline numbers from the raw files behind CCP's EVE Online Monthly Economic Report for October 2024, find where the published flows and stocks disagree, and compute price indices on a small basket. Then you turn what you found into a one-page memo.

This lab uses [week 1](../lectures/w01-the-in-house-economist-role.md): Laspeyres, Paasche and Fisher indices, stocks and flows, and the five-part memo.

## Starter materials

**1. CCP's raw data (real).** Download `https://web.ccpgamescdn.com/aws/community/EVEOnline_MER_Oct2024.zip` (linked from the October 2024 report on eveonline.com). Unzip it. You need four CSV files. Do not open `kill_dump.csv` (88 MB) unless you want to.

| File | Columns you need | What one row is |
|---|---|---|
| `money_supply.csv` | `history_date`, `character_isk`, `corporation_isk`, `total_isk` | ISK held on one day, 2017-01-01 to 2024-10-31 |
| `sinks_and_faucets_history.csv` | `history_date`, `entry_name`, `entry_sink_value`, `entry_faucet_value` | One faucet or sink category on one day (sinks are negative) |
| `index_baskets.csv` | `type_name`, `primary_index`, `sub_index` | Which item belongs to which index |
| `economy_indices_details.csv` | `history_date`, `primary_index`, `sub_index`, `price_change`, `total_value`, `price_change_weighted` | One sub-index in one month |

**2. An invented basket (fictional game, three months).** Copy this table into your sheet.

| Good | Price m0 | Price m1 | Price m2 | Units m0 | Units m1 | Units m2 |
|---|---|---|---|---|---|---|
| Ore | 10 | 15 | 12 | 1,000 | 700 | 900 |
| Health potion | 20 | 22 | 25 | 300 | 320 | 280 |
| Mid-tier sword | 500 | 400 | 380 | 20 | 30 | 32 |
| Mount | 5,000 | 4,000 | 4,200 | 2 | 3 | 3 |
| Dungeon key | 50 | 80 | 60 | 100 | 60 | 90 |

**3. Tools.** A spreadsheet, or Python with `csv` or `pandas`. Either is fine. Save your work so the marker can rerun it.

## Steps

1. **Money supply.** From `money_supply.csv`, report total ISK on 2017-01-01, 2023-10-01, 2024-10-01 and 2024-10-31, in trillions. Compute the growth from 1 October 2023 to 1 October 2024 as a percentage, and the share of ISK held by corporations (rather than characters) on 2024-10-01.
2. **October flows.** From `sinks_and_faucets_history.csv`, sum `entry_faucet_value` and `entry_sink_value` over every row dated in October 2024. Report both totals in trillions and as a percentage of the 1 October money supply. List the top five faucets and top five sinks with their shares.
3. **Classify by shape.** For each of your ten top entries, decide whether it behaves as flat (the same amount per player or per action) or proportional (scales with what the player owns or trades). Write one line of reasoning each. Mark "unsure" where the name does not tell you, and say what you would need to know.
4. **Reconcile.** Compare net October flows (faucets minus sinks) with the change in `total_isk` between 2024-10-01 and 2024-10-31. They will not match. Write at least three testable hypotheses for the gap, and for each one name the check you would run if you had CCP's internal data. Then run any check you can do with the files you have (for example, do the dates line up, does a different end date shrink the gap?).
5. **Index structure.** From `index_baskets.csv`, count how many item types sit in each primary index and list the sub-indices of the Consumer Price Index. From `economy_indices_details.csv`, show for one month that `price_change_weighted` equals `(price_change − 1)` times the sub-index's share of `total_value` within its primary index. State the formula you confirmed.
6. **Your own indices.** On the invented basket, compute for months 1 and 2 (base month 0): Laspeyres, Paasche and Fisher. Then compute a *chained* Laspeyres for month 2 (month 0 to 1 using month-0 quantities, times month 1 to 2 using month-1 quantities). Compute a new-player index (ore, potion, dungeon key) with Laspeyres weights.
7. **Memo.** Write a one-page memo in the week 1 five-part format about the invented economy, month 0 to month 2. It must quote at least three of your index values, name each basket, and say which result would make you change your recommendation.

## Deliverable

Your spreadsheet or notebook, and a PDF with: the numbers from steps 1-2 in a table, the classification from step 3, the reconciliation write-up from step 4 (about 300 words), the confirmed formula from step 5, the index table from step 6, and the memo from step 7 (at most one page).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Money supply and flows (steps 1-2) | All values within rounding of the check values, shares correct, units stated | One value wrong or units missing | Several wrong | 20% |
| Shape classification (step 3) | Every entry classified with a sound reason, unknowns flagged with what would resolve them | Classified with thin reasons | Missing | 10% |
| Reconciliation (step 4) | Three or more testable hypotheses, each with a concrete check, at least one check run and reported | Hypotheses given but vague or untestable | Missing or "the data is wrong" with no hypothesis | 25% |
| Index structure (step 5) | Counts correct, formula confirmed with a worked row | Formula stated without a check | Missing | 10% |
| Own indices (step 6) | All nine values correct, chained versus fixed difference explained | Minor arithmetic errors | Formulas wrong | 15% |
| Memo (step 7) | Five parts present, three values quoted with baskets, a reversal condition stated | Parts missing or values without baskets | Opinion without numbers | 20% |

<details>
<summary>Instructor check values</summary>

- Total ISK (trillions): 2017-01-01 1,018.1; 2023-10-01 1,889.4; 2024-10-01 2,206.0; 2024-10-31 2,335.8. Growth October 2023 to October 2024: 16.8%. Corporation share on 2024-10-01: 469.9 / 2,206.0 = 21.3%.
- October 2024 faucets about 170.8 trillion (7.7% of 1 October supply), sinks about 95.9 trillion (4.3%). Net about +74.9 trillion. Change in `total_isk` 1 to 31 October about +129.9 trillion.
- Top faucets: Commodity (Market) 27.8%, Bounty Prizes 26.8%, ESS Main Bank Autopayment 13.3%, Corporate Reward Payout (Triglavian Invasions) 12.0%, Corporate Reward Payout (Sansha Incursions) 9.6%.
- Top sinks: Transaction Tax 21.3%, LP Store 16.3%, Brokers Fee 11.3%, Skill Purchase 10.6%, Manufacturing 9.1%.
- Step 5: primary indices in the details file are Consumer Price Index, Mineral Price Index, Primary Producer Price Index and Secondary Producer Price Index. Example row: 2003-11-01, CPI, Implants, `price_change` 0.641805, weighted −0.037262, implying a value share of about 10.4%.
- Step 6: month 1 L 111.2, P 99.9, F 105.4. Month 2 L 101.2, P 95.7, F 98.4. Chained Laspeyres month 2: 105.6 (the fixed-base value is 101.2; the gap comes from reweighting to month-1 quantities). New-player Laspeyres: 141.0 (m1), 121.4 (m2).
- Sums for checking: `Σp0q0 = 41,000`, `Σp1q0 = 45,600`, `Σp2q0 = 41,500`, `Σp0q1 = 46,400`, `Σp1q1 = 46,340`, `Σp0q2 = 50,100`, `Σp2q2 = 47,960`, `Σp2q1 = 44,000`.
- Accept any reconciliation hypotheses that are testable. Good ones include flows missing from the category table, a timing offset between the stock snapshot and the daily flow totals, ISK moving to or from accounts not counted in `total_isk`, and category definitions that net some flows before reporting.

</details>
