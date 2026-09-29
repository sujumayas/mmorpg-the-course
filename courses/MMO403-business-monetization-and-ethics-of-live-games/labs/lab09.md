# MMO403 · Lab 09: The spending curve of a live game

**Week:** 9, whales and spending distributions ([lecture](../lectures/w09-whales-and-spending-distributions.md)).
**Time:** 2 hours in the lab, plus up to 2 hours to finish the memo.
**Work mode:** pairs.
**Counts toward:** models (40% of the course grade).

## Objective

Measure how concentrated one month of spending is, without being fooled by the non-payers. Then test whether a Pareto model fitted to one top share predicts another, and price a spending protection from the data rather than from a formula.

## Starter materials

All in [`lab09-starter/`](lab09-starter/). Standard-library Python.

- [`spend.py`](lab09-starter/spend.py): a provided CSV loader and stubs for `payer_rate`, `gini`, `lorenz`, `top_share`, `gini_identity`, `alpha_from_top_share`, `pareto_top_share` and `cap_effect`.
- [`spend_month.csv`](lab09-starter/spend_month.csv): one synthetic month for 20,000 accounts (`account_id`, `spend_usd`). The data is invented for this lab.
- [`test_spend.py`](lab09-starter/test_spend.py): five tests built from the lecture's 20-player server, its Pareto figures and the CSV. All five fail on the starter. Run them from the repository root:

```
.venv/bin/python courses/MMO403-business-monetization-and-ethics-of-live-games/labs/lab09-starter/test_spend.py
```

- The interactive `examples/w09-spend-lorenz.html`, for comparing your curves with the Pareto model.

## Steps

1. **The toy server.** Implement `payer_rate`, `gini`, `lorenz`, `top_share` and `gini_identity`. Reproduce the lecture's 20-player numbers (0.672, 0.918, top 5% holds 80%).
2. **Pareto helpers and the cap.** Implement `alpha_from_top_share`, `pareto_top_share` and `cap_effect`. Run the tests until all five pass.
3. **Two curves.** For the CSV, plot the Lorenz curve of all accounts and of payers only (any plotting tool, or by hand from 20 evenly spaced points of `lorenz`). Report `p`, `G_all`, `G_pay` and check the identity.
4. **Fit and test.** Fit `α` from the top 10% of payers' share. Use it to predict the top 1% and top 20% shares, and compare with the data. Then fit from the top 1% and repeat. Write three sentences on what the disagreement tells you about the shape of this month's top tail, and which fit you would trust for a cap decision.
5. **Price protections from the data.** Using `cap_effect` on the payer list, tabulate payers affected and revenue lost for caps of $25, $50, $100, $200. Compare each row with the Pareto formula from section 3 of the lecture using both of your fitted `α` values (take `A` as the data's ARPPU).
6. **A softer option.** Model a player-set limit: assume only 20% of payers above a cap would ever set one, chosen at random with a fixed seed. Compute the revenue cost at $100 and compare it with the hard cap.

## Deliverable

Your completed `spend.py` with all tests passing; a one-page results sheet (the two curves, the fit table, the cap table); and a memo of at most 400 words to the game's director recommending a hard cap, a player-set limit, or neither. The memo must give the revenue cost and the payers affected from the data, say which fitted model (if any) you would use for next month and why, and cite one piece of evidence from the lecture on who the high spenders may be, with its limits.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Code correctness | All five tests pass; clean, readable functions | Tests pass with special cases | Tests fail | 30% |
| Curves and identity | Both curves drawn and labelled; identity checked numerically | One curve or unlabelled | Missing | 15% |
| Model testing | Two fits compared against held-out shares; tail shape explained | Fits done, comparison thin | Single-point fit used uncritically | 25% |
| Protection pricing | Data-based cap table, formula comparison, soft-limit estimate | Cap table only | Numbers missing or wrong | 15% |
| Memo | Numeric, balanced, evidence with its limits, within 400 words | Correct but vague or one-sided | Hard to act on | 15% |
