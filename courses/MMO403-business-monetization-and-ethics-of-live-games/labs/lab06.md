# MMO403 · Lab 06: Cost of a collection and a disclosure page

**Week:** 6 ([Loot boxes and probability disclosure](../lectures/w06-loot-boxes-and-probability-disclosure.md))
**Time:** 2 hours in lab plus up to 3 hours at home
**Counts toward:** ethics analysis (20%); the disclosure is also an appendix of the final business plan if your game sells random items
**Work:** in pairs; submit one folder per pair

## Objective

You will compute exactly what a set of randomly sold items costs, including the unlucky tail, measure how duplicate protection and pity change that cost, and write a purchase-screen disclosure that answers the four questions from lecture 06 section 3.

## Starter materials

All in [`lab06-starter/`](lab06-starter/README.md). Python 3.10 or later, standard library only.

- `lootbox.py` gives the lecture's `terms` helper and holds eight functions to write: `expected_boxes`, `p_complete`, `protected_cdf`, `mean_from_cdf`, `percentile_from_cdf`, `simulate`, `summarize` and `box_price_in_money`. Each docstring states the rule exactly. `main()` prints the lecture's cost table once they work.
- `check_lab06.py` prints PASS, FAIL or TODO per function. The simulation checks compare your means with the exact values within 3%, so any correct implementation passes whatever order it draws random numbers in. It takes about 10 seconds.
- `disclosure-template.md`, the disclosure you hand in.

```
python check_lab06.py
python lootbox.py
```

## Steps

1. **Exact cost, no protection (20 min).** Write `expected_boxes` and `p_complete`. Reproduce the lecture's 71.95 boxes for 20 equal items and 120.55 for the 15/4/1 set. Then find the median and 90th percentile of the 15/4/1 set with `p_complete`. In `RESULTS.md`, explain in two sentences why the 90th percentile of the whole set equals that of the Legendary alone.
2. **Duplicate protection (25 min).** Write `protected_cdf`, `mean_from_cdf` and `percentile_from_cdf`. Reproduce 103.22 / 70 / 230. Explain, using the DP states, why protection cannot shorten the wait for the last Legendary.
3. **Pity by simulation (25 min).** Write `simulate` and `summarize`. Run 10,000 trials for each of the four rules in the lecture's table and compare your means with the exact values (69.70 and 36.61 for the pity rows). How many trials would you need for the simulated mean of the "no protection, no pity" row to be within 0.5 boxes of 120.55 with 95% confidence? Use the sample standard deviation of your 10,000 runs.
4. **A second currency (20 min).** Add a crafting rule to a copy of `simulate`: every duplicate Common gives 5 dust, Rare 20, Legendary 400, and you may craft any missing item for 40, 100 or 1,600 dust (Hearthstone's values for normal cards). Craft as soon as you can afford the most expensive missing item. Report mean, median and 90th percentile. Which part of the cost distribution does crafting move, and how does that compare with pity?
5. **Real money (10 min).** Write `box_price_in_money`. A box costs 150 gems; bundles are 500 gems for $4.99, 1,000 for $9.99 and 2,800 for $24.99. Report the price of one box at each bundle rate and explain which rate your disclosure should show and why.
6. **Your box and its disclosure (at home).** Design a box for your team's game, or use the mount set from the in-class activity (8 Common at 9%, 3 Rare at 8%, 1 Mythic at 4%). Choose at least one of protection, pity or crafting, and justify it with numbers from steps 1 to 4. Fill in `disclosure-template.md` completely, including median and 90th-percentile cost in money for the most wanted item and the full set. In the design notes, estimate how much revenue per 1,000 buyers your rule gives up, assuming buyers stop once they complete the set.

## Deliverable

One folder named `lab06-<name1>-<name2>` containing your `lootbox.py` (passing `check_lab06.py`), your crafting variant, `RESULTS.md` with steps 1 to 5, and `disclosure.md` from step 6.

## Rubric (20 points)

| Criterion | Excellent (full) | Adequate (half) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code passes the checker | All eight PASS | Six or seven PASS | Five or fewer | 4 |
| Exact and protected costs (steps 1 and 2) | Values reproduced; tail explained by the single rarest item; DP argument for why protection leaves the tail | Values without explanation | Missing or wrong | 4 |
| Simulation and crafting (steps 3 and 4) | Four rules compared with exact values; sample-size calculation from the observed standard deviation; crafting results with a clear comparison to pity | Results without the sample-size or comparison | Missing | 4 |
| Money (step 5) | Three rates right; recommendation tied to the FTC exchange-rate requirement or to the most common purchase | Rates right, no recommendation | Missing | 3 |
| Disclosure and design notes (step 6) | All four questions answered on one screen with correct numbers; rule justified; revenue given up estimated with stated assumptions; language plain and accurate | Complete but cost shown only in boxes, or no revenue estimate | Missing | 5 |
