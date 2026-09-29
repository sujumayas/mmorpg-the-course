# MMO307 · Lab 08: Build and tune an Elo ladder

**Week:** 8, Elo and expected score ([lecture](../lectures/w08-elo-and-expected-score.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the rating lab (30%), with labs 09, 10, 11 and 14 (20 of its 100 points).

## Objective

Implement Elo, run it on a simulated ladder of 500 players whose true strength you know, and choose a K rule that meets two targets, placing new players quickly and keeping established ratings steady. Then measure what your rule does to the rating pool.

## Starter materials

- [`lab08-starter/elo.py`](lab08-starter/elo.py), standard-library Python. Empty: `expected`, `update` (with separate K for each player), `time_constant`, `settled_sd` and `calibration`. Provided: `make_players` (500 hidden true strengths, normal with mean 1,500 and standard deviation 200, all starting at 1,500), `play_round` (pairs neighbours by rating, decides results from true strength, updates ratings and can log predictions), `k_rule_flat`, and `rating_error` (root-mean-square gap between rating and truth after removing the average offset).
- [`lab08-starter/test_elo.py`](lab08-starter/test_elo.py) with the lecture's values: `E(400) = 10/11`, the 2,300 against 1,500 table row, the 1,700 pair exchanging 16, the unequal-K case (+20/−5), `τ(32) = 21.7`, `σ(32) = 52.7`, `σ(16) = 37.3`, calibration buckets, and a zero-sum check on a 100-player ladder. All tests fail on the starter. Run from the starter folder with `../../../../.venv/bin/python test_elo.py`, or with pytest.
- The [Elo interactive](../examples/w08-elo-expected-score.html), tab 2, for checking single-player climbs.

## Steps

1. **Core.** Implement `expected` and `update`. Each player applies their own K to their own surprise, so unequal K is not zero-sum.
2. **Speed and noise.** Implement `time_constant` and `settled_sd` from the lecture. Tests must pass before you continue.
3. **Flat K sweep.** For K in 8, 16, 24, 32, 48, run 300 rounds with a fixed seed. Plot `rating_error` against round for each K on one chart. Report the round at which each K first gets below 120, and its average error over rounds 200 to 300.
4. **Calibration.** For K = 24, log predictions over rounds 100 to 300 and run `calibration`. Make the bucket table. For each bucket, compute a 95% margin with MA102 week 13's `1.96 × sqrt(p(1 − p)/n)` and say whether the win rate is inside it.
5. **Two-stage K.** Write a `k_rule` that uses a high K for a player's first N games and a low K after. Choose N and both values so that average error falls below 120 by round 30 and stays below 90 over rounds 200 to 300. Show that it beats every flat K from step 3 on the combined goal, or explain why none can.
6. **Pool audit.** With your two-stage rule, track the sum of all ratings each round. Report the total drift over 300 rounds and explain its sign from the lecture's unequal-K argument.
7. **Newcomers.** From round 150, replace the 10 lowest-true-strength players every 10 rounds with fresh players (new true strengths from the same distribution, rating 1,500, 0 games). Report what happens to the average rating and to `rating_error`. Propose one fix and test it.

## Deliverable

The completed `elo.py` with all tests passing, your experiment script, the charts from steps 3 and 5, the calibration table, and a memo of at most 400 words to a ladder designer. The memo must recommend a K rule with its numbers, state the expected wobble a settled player will see on the public ladder, and name the pool effect your rule creates.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Implementation and tests | All tests pass; update uses per-player K correctly | Tests pass with a small spec mismatch noted | Tests fail | 20% |
| K sweep and calibration | Clear charts; calibration table with margins and a correct reading | Charts or table incomplete | Missing or misread | 25% |
| Two-stage rule | Meets both targets, compared fairly against flat K with the same seed | Meets one target | No working rule | 25% |
| Pool and newcomer analysis | Drift measured and explained; fix proposed and tested | Measured, thin explanation | Missing | 15% |
| Memo | Plain, numeric recommendation with wobble and pool effect, within limit | Recommendation with missing numbers | Hard to act on | 15% |
