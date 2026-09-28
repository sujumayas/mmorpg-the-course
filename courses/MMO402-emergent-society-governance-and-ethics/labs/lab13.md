# MMO402 · Lab 13: Shutdown policy memo

**Assigned:** week 13 ([lecture](../lectures/w13-shutdown-ethics.md)). **Due:** start of week 14 class. **Time:** 2 hours in lab plus about 3 hours at home. **Feeds:** the case analyses (30%) and the week 14 debate on shutdown obligations.

## Objective

Price a shutdown plan for an invented live-service world with the week 13 stranded-value model, using a purchase history with three item types that have different useful lives. Then write the announcement and a policy memo that defends your notice period, refund rule and currency policy with numbers, and states which losses your numbers cannot capture.

## Starter materials

- [`lab13-starter.py`](lab13-starter.py). A standard-library Python script. It loads a purchase history, computes stranded value by item type for any notice period with `stranded()` and `stranded_by_category()`, and adds running cost with `total_cost()`. The useful lives are set in the `LIFETIME` table: cosmetics 12 months, season passes 3 months, the expansion 24 months. Two functions are left as TODOs: `best_notice()` and `refund_window()`.
- [`lab13-purchases.csv`](lab13-purchases.csv). The purchase history of the invented world "Harrowmere," 49 rows with header `age_months,category,spend_usd`. For each of the 24 months before the announcement (ages 0.5 to 23.5) it holds $150,000 of cosmetics and $40,000 of season passes. It also holds one $600,000 row of expansion sales at age 8.5. Every figure is invented.
- The interactive `examples/w13-stranded-value.html` once built, for quick what-if checks with the single-item-type model. The script is the source of truth for your numbers.
- Extra facts for the scenario: running the world costs $150,000 a month during notice. Players hold $400,000 of unspent premium currency. The server build uses licensed middleware that cannot be redistributed without a new agreement (estimated three months of legal work).

Check your setup before you start. `python3 lab13-starter.py lab13-purchases.csv` must print $2,880,000 spent in the last 12 months and a stranded value of $1,347,500 at 0 months' notice. With `--notice 3` the cosmetic line must read $506,250 and the season-pass line $0.

## Steps

1. **Read the baseline (15 min).** Run the script at notice 0, 3 and 6. For each item type, explain in one sentence why its stranded value falls at the rate it does. Why is the season pass gone by month 3, while the expansion falls slowly?
2. **Best notice (30 min).** Implement `best_notice()`. Search `N` from 0 to 24 months in steps of 0.25 and return the `N` with the lowest total cost, taking the shorter `N` on ties. Report `N*` and the total at running costs of $150,000, $50,000 and $300,000 a month. Explain why the answer is not `L × (1 − C / s)` for any single `L`.
3. **Refund window (30 min).** Implement `refund_window()`. It refunds the full price of every purchase younger than `W` months at the announcement and returns the cash paid and the value still stranded on everything else. Report both numbers for `W = 1` and `W = 3`, at notice 0 and at notice 3. Which pairing of notice and window leaves the least value stranded for each dollar spent?
4. **Change an assumption (20 min).** Suppose the store page said the expansion was "yours to keep." Argue for a new expansion life, change `LIFETIME["expansion"]`, and rerun step 2. How far does `N*` move? What does that tell you about where the ethical weight sits in this model?
5. **The currency (10 min).** Decide what happens to the $400,000 balance: refund, conversion to items, or nothing. Give the cost and one argument against your choice.
6. **Write-up (at home).** Produce the two documents in the deliverable.

## Deliverable

One Markdown or PDF file with:

- A results table: `N*` at the three running costs, the step 3 refund-window results, and the step 4 rerun.
- A shutdown announcement to players of at most 250 words. It must give the closing date, the day sales stop, the refund rule, the currency policy, what players can keep, and what happens to their data.
- A policy memo to the publisher of about 700 words. It must defend the plan with at least four numbers from your results, say which weight you gave player losses against operator cost and why, name one loss from the four-row table in lecture section 1 that the model cannot price, and say what you would do about the middleware licence.
- Your completed `lab13-starter.py`.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing (0) | Weight |
|---|---|---|---|---|
| Model code | Both TODOs correct; setup checks and instructor values reproduce | One TODO correct, or results not reproducible | Model not used | 25% |
| Use of numbers | Plan argued from at least four results, with trade-offs stated in dollars and months | Numbers present but not tied to decisions | Opinion without numbers | 20% |
| Useful life and weighting | Step 4 argued from what buyers were told; player-loss weight chosen and defended | Assumptions changed without argument | Assumptions not discussed | 20% |
| Losses beyond money | Names a loss the model cannot price and proposes a concrete remedy (export, event, archive, licence) | Mentions such losses in general terms | Absent | 15% |
| Announcement | Clear and complete in 250 words; a player could act on it | Missing one required element | Missing two or more | 20% |

<details>
<summary>Instructor check values</summary>

- Notice 0: cosmetic $900,000, season pass $60,000, expansion $387,500, total $1,347,500.
- Notice 3: total stranded $818,750 (cosmetic $506,250, season pass $0, expansion $312,500).
- `best_notice()` with steps of 0.25: at $150,000 a month, `N* = 2.5` and total $1,262,500. At $50,000, `N* = 9.5` and total $662,500. At $300,000, `N* = 0` and total $1,347,500.
- `refund_window()`: `W = 1, N = 0` gives $190,000 paid and $1,170,417 left. `W = 1, N = 3` gives $190,000 and $712,500. `W = 3, N = 0` gives $570,000 and $893,750. `W = 3, N = 3` gives $570,000 and $537,500.
- The single-`L` formula fails because the three item types have different lives. The season pass stops contributing after 3 months, so beyond that point the marginal relief comes only from cosmetics and the expansion.

</details>
