# MMO403 · Lab 11: A token for a subscription MMO

**Week:** 11 ([Subscription tokens](../lectures/w11-subscription-tokens.md))
**Time:** 2 hours in lab plus up to 2 hours at home
**Counts toward:** models (40%)
**Work:** in pairs; submit one folder per pair

## Objective

Your studio runs a subscription MMO at US$15 a month and is deciding whether to launch a token at US$20. You will build the lecture's revenue model, run it on a population of 50,000 players with different cash and time budgets, and find out how the gain depends on the token's gold price, on substitution and on a platform fee. You finish with a launch recommendation that names what gold should never buy.

## Starter materials

All in [`lab11-starter/`](lab11-starter/README.md). Python 3.10 or later, standard library only.

- `gen_players.py` writes `players.csv` (seed 1111): 50,000 players, each with `wtp_usd` (the most they would pay in cash for a month) and `gold_per_month` (gold earned in a month of normal play).
- `tokens.py` holds five functions to write: `token_gain`, `breakeven_sigma`, `blended_rate`, `classify` and `simulate`. Docstrings give exact definitions. `main()` prints a scenario table once they work.
- `check_lab11.py` prints PASS, FAIL or TODO per function. It fails on the starter and passes on a correct solution.

```
python gen_players.py
python tokens.py
python check_lab11.py
```

The population model is deliberately simple. A player pays with gold whenever half their monthly gold covers the token's gold price, otherwise pays cash if their willingness to pay reaches the subscription price, otherwise leaves. Token supply is assumed to come from cash-rich buyers outside the file. Say in your write-up where this simplification matters.

## Steps

1. **The formula (15 min).** Write `token_gain`, `breakeven_sigma` and `blended_rate`. Reproduce the lecture's table for `T = 100,000`, `s = 15`, `c = 20`.
2. **The population (25 min).** Write `classify` and `simulate`, then run `tokens.py`. For gold prices of 50,000, 100,000, 150,000 and 250,000, report the token players `T`, the measured `k`, the players kept who would otherwise leave, and `ΔR`. Explain why `k` rises as the gold price falls.
3. **Substitution (15 min).** At a gold price of 100,000, compute `ΔR` for `σ` = 0, 0.3 and 0.6, and the break-even `σ`. Which is the bigger risk for this population, cannibalization or substitution?
4. **A platform fee (15 min).** Suppose tokens are sold only through a store that keeps 30%, and subscriptions are sold directly. Rerun with net `c = 14` and `σ = 0`. Compare with step 3's `σ = 0.3` row and explain why the two match. Then find the lowest token price (to the nearest US$0.50) for which the platform version still gains at `σ = 0.3`.
5. **Pricing the token (15 min).** Holding the gold price at 100,000, try token prices from US$15 to US$30. The model has no demand response to `c`, so `ΔR` rises without limit. Name the effect the model leaves out, and use week 10's break-even idea to say what you would need to measure before raising `c`.
6. **Recommendation (at home).** One page to the producer. Recommend launch or no launch, the dollar price, the sales channel and one item or service gold must never buy once the token exists. Include the `(k, σ)` break-even line for your chosen price and fee, one sentence on players the token helps, and one on players it puts at risk (MMO402 weeks 10 and 11).

## Deliverable

One folder named `lab11-<name1>-<name2>` containing your `tokens.py` (passing `check_lab11.py`), `RESULTS.md` with the tables and answers from steps 1 to 5, and `recommendation.pdf` from step 6.

## Rubric (20 points)

| Criterion | Excellent (full) | Adequate (half) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code passes the checker | All five PASS | Four PASS | Three or fewer | 4 |
| Population results (step 2) | Full table; the rise of `k` with a falling gold price explained through who can afford the token | Table without explanation | Missing | 4 |
| Substitution and platform fee (steps 3 and 4) | Break-even `σ` correct; the fee and `σ` equivalence explained; lowest viable price found | Numbers right, no explanation | Missing | 4 |
| Model limits (step 5 and the simplifications) | Names the missing demand response and at least one population simplification, with how to measure each | One limit named | Missing | 3 |
| Recommendation (step 6) | Clear decision with price and channel; break-even line shown; a protected item justified; both player groups addressed fairly | Decision clear, ethics thin or one-sided | Missing | 5 |
