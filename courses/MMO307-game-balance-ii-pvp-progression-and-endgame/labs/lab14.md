# MMO307 · Lab 14: Does the ladder hide an overpowered class?

**Assigned:** week 14 ([lecture](../lectures/w14-measuring-balance-with-win-rates-and-pick-rates.md), [interactive](../examples/w14-rating-absorbs-advantage.html)). **Due:** one week after week 14 class. **Time:** 2 hours in lab, plus up to 3 hours at home. **Feeds:** the rating lab (30%) and the rating simulation in the final season design (40%).

## Objective

Build the pieces of an Elo ladder, then use a simulator to watch a rated ladder hide a class's advantage from its win rate. Measure where the advantage went, compare the simulation with the lecture's closed forms, and turn what you learn into a dashboard rule that would catch an overtuned class within a week of a patch.

## Starter materials

All in [`lab14-starter/`](lab14-starter/). Standard-library Python (3.10 or later), run with `.venv/bin/python` or any Python 3.

- [`ladder.py`](lab14-starter/ladder.py), with four functions to complete: `expected_score`, `elo_update`, `class_win_rate` and `top_share`. The rest is complete. `simulate_ladder` runs a ladder where a share of players main a strong class, and the matchmaker pairs neighbours by rating each round. `window_win_rate` and `representation` read its output. The command line is `python ladder.py --delta 60 --f 1.0 --seed 1`, with `--start patch` (default, ratings already match skill and the buff lands at round 0) or `--start reset` (everyone starts at 1,500).
- [`test_ladder.py`](lab14-starter/test_ladder.py), five tests. Four check your functions against the lecture's tables. One runs a 2,000-player ladder and checks that the class wins more than 55% of games in the first ten rounds, within 2 points of 50% in rounds 150 to 199, and is over-represented in the top 10%. All five fail on the starter.
- The [interactive](../examples/w14-rating-absorbs-advantage.html) for checking closed-form values.

## Steps

1. **Complete the functions (30 min).** Implement the four functions until all five tests pass. `top_share` uses `statistics.NormalDist` for `Φ` and `Φ⁻¹`.
2. **Watch the signal move (30 min).** Run the default ladder (`δ = 60`, `f = 1`) for five seeds. Plot the class win rate per 10-round window against rounds, averaged over seeds. Fit or eyeball the time constant in rounds, and compare it with week 8's `1/(K·g) ≈ 29` games at `K = 24`.
3. **Vary `f` (30 min).** Run `f = 0.1, 0.25, 0.5, 0.75, 1.0` (five seeds each). For each, report the late win rate (rounds 150 to 199) with a 95% interval from MA102 week 13, next to the closed form `E((1 − f)δ)`. Explain any value outside its interval.
4. **Representation (30 min).** For `f = 1`, report the top-10% and top-1% representation per seed, their mean and their spread. Compare with the closed forms (1.63 and 2.14). The simulation reads low. Find out why in two steps. First, drop the small-share assumption. The class is 20% of the ladder, so solve for the cutoff `c` where `0.8 × (1 − Φ(c/σ)) + 0.2 × (1 − Φ((c − 60)/σ))` equals the top fraction, and recompute the ratio (the lecture gets 1.47 for the top 10%). Second, widen the spread to `√(σ² + noise²)` with week 8's settled noise `√(K/(8g))`. Report how much of the gap each step explains.
5. **Season reset (20 min).** Rerun step 2 with `--start reset`. Explain why the first-window win rate is lower than under `--start patch`, even though the class is just as strong. (Hint: what does the matchmaker know in round 0?)
6. **Estimate `δ` blind (20 min).** Ask a partner to run the simulator with a secret `δ` between −80 and +120 and `f = 1`, and to give you only the per-round win and game counts plus the final ratings and main flags. Estimate `δ` two ways: from the early-window win rate and from top-10% representation. Report both with your reasoning, then check against the secret.
7. **Dashboard rule (20 min).** Write one rule, with a threshold and a sample-size condition, that would flag an overtuned class on a per-spec ladder within seven days of a patch. Test it on your runs for `δ = 0`, `+30` and `+60`. Report how often it fires.

## Deliverable

A zip or repository link containing:

- Your completed `ladder.py`, with the output of `test_ladder.py` in the report showing five passes.
- The plots from steps 2 and 4.
- `report.md` (800 to 1,200 words) with the tables from steps 3 and 4, the explanation from steps 4 and 5, the blind estimate from step 6, and the dashboard rule from step 7 with its hit rates. Close with one paragraph saying which rating structure (per spec or per player) you would choose for a new MMO arena mode, and what it would cost your balance team.
- The seeds and command lines for every number, so a reviewer can reproduce it.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Weight |
|---|---|---|---|---|
| Correct functions | All five tests pass | Four closed-form tests pass, simulation test fails | Three or fewer pass | 20% |
| Absorption and `f` sweep | Time constant measured and compared with week 8; `f` sweep with intervals; departures explained | Sweep done without intervals, or time constant missing | Not attempted | 20% |
| Representation and noise | Simulated and closed-form ratios compared; the gap split between the class-share effect and rating noise, both computed | Gap noted, explanation qualitative | Not attempted | 20% |
| Blind estimate | Both estimates with working; the direction of each bias explained | One method with working | No estimate | 15% |
| Dashboard rule | Rule has a threshold, a sample-size condition and measured hit rates for all three `δ` | Rule given, hit rates partial | No rule | 15% |
| Reproducibility and writing | Seeds and commands complete; plain, number-backed prose within length | Mostly reproducible | Cannot be rerun | 10% |
