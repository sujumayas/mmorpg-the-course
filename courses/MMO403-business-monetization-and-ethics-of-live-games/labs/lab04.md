# MMO403 · Lab 04: Measure a paid edge

**Week:** 4 ([Cosmetics vs power](../lectures/w04-cosmetics-vs-power.md))
**Time:** 2 hours in lab plus up to 3 hours at home
**Counts toward:** ethics analysis (20%); the store policy is also reused in the final business plan
**Work:** in pairs; submit one folder per pair

## Objective

You will turn a purchased stat edge into a win chance, a rating-point value and a share of the top of a ladder, confirm with a full Elo simulation that matchmaking hides the edge from win rates, and write a store policy whose limit is stated in rating points.

## Starter materials

All in [`lab04-starter/`](lab04-starter/README.md). Python 3.10 or later, standard library only.

- `edge.py` holds five functions to write: `win_prob`, `rating_gap`, `top_cutoff`, `payer_share_on_top` and `unranked_win_rates`. Each docstring gives the exact formula from lecture 04. `main()` prints the lecture's table once they work.
- `ladder_sim.py` is given and complete. It runs an Elo ladder of 4,000 players and 1,000,000 matches with matchmaking, in which a share of players buy an edge. It imports your `win_prob` and `rating_gap`. One run takes about 4 seconds.
- `check_lab04.py` prints PASS, FAIL or TODO per function.
- `policy-template.md`, the store policy you hand in.

```
python check_lab04.py
python edge.py
python ladder_sim.py 0.10 0.2 0.25 404
```

## Steps

1. **The chain (25 min).** Write `win_prob` and `rating_gap`, then run `edge.py`. Your table must match lecture 04 section 2. In `RESULTS.md`, show by hand the calculation for `b = 0.05`, `σ = 0.25`: `z`, `p`, `Δ`.
2. **The ladder, analytically (20 min).** Write `top_cutoff` and `payer_share_on_top`. For `f = 0.2` and `s = 200`, make a table of payer share in the top 10% and top 1% for `Δ` = 0, 25, 50, 75, 100, 150. At what `Δ` do payers hold twice their population share of the top 1%?
3. **The ladder, simulated (30 min).** Run `ladder_sim.py` for edges 0, 0.05, 0.10 and 0.20 at `f = 0.2`, each with seeds 401 to 405. Average each output over the five seeds. Put the averages next to your step 2 predictions. Answer in `RESULTS.md`:
   - How close are buyers' and non-buyers' win rates in the second half of the run? Why are they not exactly 50%?
   - How do the simulated top-10% and top-1% shares compare with the analytic ones? Name two reasons they differ (hint: a sample of 40 players in the top 1%, and Elo ratings that carry noise of their own).
4. **Without matchmaking (10 min).** Write `unranked_win_rates`. For `b = 0.10`, `σ = 0.25`, `f = 0.2`, report both win rates. In two sentences, explain to a producer why the same item looks harmful in unranked play and harmless in ranked play, and why both views describe the same edge.
5. **Noise from data (15 min).** A telemetry export for your team's game says that in equal-rating duels between players with identical gear, the log of the kill time has a standard deviation of 0.18 per player. Compute `Δ` for edges of 2%, 5% and 10% at that noise. Which of the lecture's in-class items (A to D) would stay under a limit of 10 rating points?
6. **Store policy (at home).** Fill in `policy-template.md` for your team's game (or the fantasy MMO from the in-class activity). Your limit must be in rating points and computed from a stated `σ`. Review at least four items with the who-loses test. Name the ladder metric you will monitor, its threshold, and what happens when it trips.

## Deliverable

One folder named `lab04-<name1>-<name2>` containing your `edge.py` (passing `check_lab04.py`), `RESULTS.md` with steps 1 to 5, and `policy.md` from step 6.

## Rubric (20 points)

| Criterion | Excellent (full) | Adequate (half) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code passes the checker | All five PASS | Three or four PASS | Two or fewer | 4 |
| Chain and analytic ladder (steps 1 and 2) | Hand calculation correct; table complete; doubling point found and explained | Numbers right, no explanation | Missing or wrong | 4 |
| Simulation vs theory (step 3) | Averages over five seeds; win-rate gap explained by convergence; two valid reasons for differences in top shares | One seed only, or reasons missing | Missing | 4 |
| Ranked vs unranked (steps 4 and 5) | Both win rates right; producer explanation links rank and win rate as two views of one edge; step 5 values right and applied to the items | Numbers right, explanation generic | Missing or wrong | 4 |
| Store policy (step 6) | Limit in rating points from a stated `σ`; four items reviewed with who loses, `b` and `Δ`; monitoring metric with threshold and action; player-facing sentence plain and accurate | Complete but limit in percent, or no threshold | Missing | 4 |
