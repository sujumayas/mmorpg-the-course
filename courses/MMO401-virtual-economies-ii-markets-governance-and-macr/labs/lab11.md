# MMO401 · Lab 11: A token market in an agent-based economy

**Week:** 11 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the ABM labs (40%)

## Objective

Run a token market inside a small agent-based economy and test the claim from [week 11](../lectures/w11-premium-currencies-and-exchange-rates.md) that a token's gold price is a noisy inflation gauge. You will add a money ledger and a fee, trigger three shocks (a faucet increase, a store sale and a new token use), and find out which of them the token price can tell apart and which it cannot.

## Starter materials

- [`lab11-starter.py`](lab11-starter.py), a standard-library Python 3 script. It simulates 300 cash-rich players and 3,000 time-rich players for 360 days.
  - Each day each cash-rich player buys one token from the store with probability 5% (20 dollars each) and offers it for gold.
  - Each time-rich player earns about 40,000 gold a day and bids 3% of their gold balance on tokens.
  - The market is a daily call auction. The price is total gold bid divided by tokens offered, `P = B / Q`, the week 11 model at agent level. Buyers redeem tokens at once for game time.
  - Three events are switched on by default: income per hour rises 25% from day 120, a store sale triples buying on day 200 only, and a new token use raises the bid share by half from day 280.
- The places you must edit are marked `TODO`.

Run it once with `python3 lab11-starter.py`. With seed 11 the first monthly average price should be about 4,953,194 gold and the last about 11,150,803.

## Steps

1. **Predict first.** Before changing any code, use `P = B / Q` to predict the long-run token price before day 120 and between days 120 and 199. Hint: in the long run, what must a time-rich player's daily bid equal, if their balance stops growing? Write your two predictions down.
2. **Money ledger.** Record the money supply `M` (all gold held by both groups) each day. Add a daily check of `M(end) = M(start) + faucet − sinks` with an assertion. Plot `M` and the token price on one chart with two y-axes.
3. **Add a fee.** Set `FEE = 0.05` on the seller's proceeds, count the destroyed gold as a sink in your ledger, and rerun. Report the total gold destroyed over the year and the change in the average price in the last 60 days compared with `FEE = 0`. Explain why it moved, or why it did not.
4. **Implied rates.** For each month print the implied gold per dollar `e = P / 20` and the implied wage in dollars per hour for a player earning `GOLD_PER_HOUR`. Mark the months of each event.
5. **Tell the shocks apart.** Run four versions with the same seed: no events, faucet only, sale only, new use only. For each, report the average price in the 30 days after the event and in days 330-360. Which shocks leave a permanent change in the price and which fade? Explain the fading one using your answer to step 1.
6. **Noise.** With no events, run 10 seeds and report the standard deviation of the daily price and of the 30-day average. How large a change in the 30-day average would you need to see before calling it inflation? Compare with the faucet shock from step 5.

## Deliverable

1. Your modified script.
2. The chart from step 2 and a table for steps 5 and 6.
3. A memo of about 400 words to your studio's economy lead, titled "Can we read inflation from the token price?". Answer yes, no or partly, and support it with at least four numbers from your runs. Include one recommendation on what else the team should track alongside the token price.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Prediction (step 1) | Both prices predicted from the steady state with working shown, close to the simulation | One predicted, or reasoning unclear | Missing | 15% |
| Ledger and fee (steps 2-3) | Identity asserted daily, fee counted as a sink, price change explained | Ledger kept, fee effect unexplained | Missing | 20% |
| Implied rates (step 4) | Monthly `e` and wage correct, events marked | Values printed, events not marked | Missing | 10% |
| Shock separation (step 5) | Four runs, permanent vs fading shock identified and explained from the model | Runs done, explanation vague | Fewer than four runs | 25% |
| Noise (step 6) | Ten seeds, a clear detection threshold compared with the faucet shock | Seeds run, no threshold | Missing | 15% |
| Memo | Clear answer backed by numbers, a sensible extra indicator | Answer given, few numbers | Opinion without numbers | 15% |

<details>
<summary>Instructor check values</summary>

- Step 1: in the long run a time-rich player's bid equals their income, since balance stops growing when `0.03 × balance = income`. So `B ≈ 3,000 × 40,000 = 120` million gold per day. Tokens offered average `300 × 0.05 = 15` per day, so `P ≈ 8.0` million before day 120 and `P ≈ 150M / 15 = 10.0` million after the faucet rise.
- Unmodified starter, seed 11 (tested on Python 3.13): monthly averages start at about 4.95 million, reach about 8.6 million by month 4, swing between about 9.2 and 12.8 million in months 5 to 12 after the faucet change, and end at 11.2 million in the last month.
- The new use (higher bid share) produces a spike that fades, because in steady state bids return to income whatever the share. Students who expected a permanent doubling have applied `B = s × Y` without noticing that here `Y` is paid out of a balance. That is the key discovery of the lab and should be credited in the memo.
- Daily prices are very noisy because only about 15 tokens trade a day (binomial). Good answers show the 30-day average is needed before any inflation claim.
- With `FEE = 0.05` the price series is identical to the no-fee run, because the fee comes out of cash-rich players' gold and they never bid. Sellers receive 5% less. The fee destroys 2,400,746,420 gold over the year with seed 11. Strong answers point out that in a fuller model sellers would list fewer tokens when proceeds fall, which would raise the price.

</details>
