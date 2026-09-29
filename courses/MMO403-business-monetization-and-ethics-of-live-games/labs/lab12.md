# MMO403 · Lab 12: The revenue waterfall

**Week:** 12 ([Publishing, platforms and fees](../lectures/w12-publishing-platforms-and-fees.md))
**Time:** 2 hours in lab plus up to 3 hours at home
**Counts toward:** models (40%); the waterfall is reused in the final business plan (40%)
**Work:** in pairs; submit one folder per pair

## Objective

You will turn the week's fee schedules into a small library, run one invented year of a game's sales through four channels, and compare two publishing deals that differ only in how they recoup. At the end you will know how much of a player's dollar reaches the studio in each channel, and you will have a waterfall you can reuse for your business plan.

## Starter materials

All in [`lab12-starter/`](lab12-starter/README.md). Python 3.10 or later, standard library only.

- `channels.json` holds the fee schedules from the lecture (Steam, Epic, Google Play remaining markets, Apple Small Business Program, and a direct store with card fees), each with the date it was checked. The schedules are for teaching. Check every one against the platform's current terms before using it in a real plan.
- `forecast.csv` is one invented year: consumer spend and number of purchases per channel, and whether the developer was eligible for Apple's program last year.
- `fees.py` holds seven functions to write: `bracket_take`, `status_take`, `card_fees`, `tax_from_inclusive`, `channel_take`, `publisher_split` and `waterfall`. Docstrings give exact definitions. `main()` prints the channel table and two publishing deals once they work.
- `check_lab12.py` prints PASS, FAIL or TODO per function. It fails on the starter and passes on a correct solution.

```
python fees.py
python check_lab12.py
```

## Steps

1. **Schedules (25 min).** Write `bracket_take`, `status_take`, `card_fees` and `tax_from_inclusive`. Reproduce the lecture's table of Steam and Epic takes at US$1M to US$100M, and the card fee on baskets of US$0.99 to US$99.99.
2. **The channel table (20 min).** Write `channel_take` and `waterfall`, then run `fees.py` with a 10% tax rate and 4% refunds. For each channel report net revenue, fee, average fee rate and payout. Why is Epic's average rate below 12%? Why is Apple's below 30%?
3. **Marginal thinking (15 min).** The studio can earn US$1M more net revenue on one channel with a DLC. For each channel, compute the extra payout from that US$1M using the marginal rate at this year's revenue. Where should the DLC's marketing go, if reach were equal?
4. **Next year (15 min).** Rerun Apple with `eligible_last_year = 0`, as it would be next year given this year's revenue. How much more does Apple take on the same revenue? Explain the difference between a bracket and a status rule in two sentences.
5. **Publishing deals (20 min).** Write `publisher_split`. The publisher advanced US$4M (development plus marketing) and splits payouts 50/50. Compare recoupment from the studio's half with recoupment from all payouts. Then find the studio share, to the nearest 5%, at which recouping from the studio's half gives the studio the same year-one money as the "all payouts" deal at 50/50.
6. **Channel memo (at home).** One page to your studio head. Recommend which channels to launch on, and whether to take the publisher deal and under which recoupment clause. Show the full waterfall for your recommended set as a chart, with each step's share of consumer spend. State every fee assumption with its date, and name one platform rule other than the fee (payments, pricing or exclusivity) that could change your recommendation.

## Deliverable

One folder named `lab12-<name1>-<name2>` containing your `fees.py` (passing `check_lab12.py`), `RESULTS.md` with the tables and answers from steps 1 to 5, and `memo.pdf` from step 6.

## Rubric (20 points)

| Criterion | Excellent (full) | Adequate (half) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code passes the checker | All seven PASS | Five or six PASS | Four or fewer | 4 |
| Channel table and average rates (steps 1 and 2) | Correct table; each average rate explained from its schedule | Correct table, weak explanation | Missing | 4 |
| Marginal and status reasoning (steps 3 and 4) | Marginal payouts correct; bracket and status rules contrasted in numbers | One of the two correct | Missing | 4 |
| Publishing deals (step 5) | Both clauses computed; equivalent share found and interpreted | Clauses computed, no equivalent share | Missing | 3 |
| Memo (step 6) | Clear recommendation; waterfall chart with shares; every assumption dated; a non-fee platform rule and its risk named | Recommendation clear, assumptions undated or chart missing | Missing | 5 |
