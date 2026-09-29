# MMO307 · Lab 11: Simulating a season end

**Assigned:** week 11 ([lecture](../lectures/w11-seasonal-structures-and-resets.md), [interactive](../examples/w11-soft-reset.html)). **Due:** start of week 12 class. **Feeds:** the rating lab assessment (30%) and the final season design project (week 15).

## Objective

Simulate a whole population through a season end. Measure, round by round, how far shown ratings sit from true skill and how many matches are lopsided, under a hard reset, soft resets and a visible-only reset. Compare the population result with the single-player model from the lecture, then propose and defend a reset rule with numbers.

## Starter materials

The folder [`lab11-starter/`](lab11-starter/) contains:

- [`season_sim.py`](lab11-starter/season_sim.py). A population of players with fixed true skills drawn from `N(1500, 200)` plays rated games. `run_season` warms the ladder up for 300 rounds from a flat start, applies a reset with compression `alpha`, then plays 100 more rounds and records the mean absolute rating error and the share of lopsided games (true skill gap above 200) each round. The driver, the command-line interface and `expected` are written. Five functions are stubs: `elo_update`, `soft_reset`, `play_round`, `mean_abs_error` and `lopsided_share`. As shipped, the script runs and prints a `TODO` line.
- [`test_season_sim.py`](lab11-starter/test_season_sim.py). Five tests. From the repository root, run `.venv/bin/python courses/MMO307-game-balance-ii-pvp-progression-and-endgame/labs/lab11-starter/test_season_sim.py` (or `python3 test_season_sim.py` inside the folder). All five fail on the starter and must pass on your solution. The script exits with status 1 on any failure.

The matchmaker in `play_round` sorts players by shown rating plus a random jitter of up to ±150 and pairs neighbours. The jitter is a stand-in for the search window you built in [lab 10](lab10.md). Standard library only; one run of 1,000 players takes a few seconds.

## Steps

1. **Complete the functions (45 min).** Implement the five stubs from their docstrings and the week 8 update rule. Run the tests until all pass. Then run `season_sim.py --alpha 0` and `--alpha 1` and check that the hard reset starts with a much larger error.
2. **The control run (20 min).** A season simulation needs a control. Run `--alpha 1` (no reset) for seeds 1 to 5 and record the mean error and lopsided share at rounds 0, 20 and 100. This is your baseline. Every later result is reported as a difference from it.
3. **Reset sweep (45 min).** For `alpha` in {0, 0.25, 0.5, 0.75, 0.9} and `K` in {32, 64}, run seeds 1 to 5. For each setting report: the round at which mean error returns to within 5 points of the control, and the total excess lopsided games over the 100 rounds (sum over rounds of the lopsided share minus the control's, times 500 games per round).
4. **Model check (30 min).** The lecture predicts games to settle as `τ × ln(e₀ / ε)` for one player. Pick the players whose true skill is above 1,900. Track their average error (shown minus true, with sign) round by round after a hard reset and compare it with the model and with the lecture's single-player simulation. Explain any gap in two or three sentences.
5. **A surprise to explain (20 min).** You should find that after a light reset (`alpha` around 0.8) the mean error right after the reset is *lower* than in the control. Find out why. Measure the standard deviation of shown ratings after the warm-up and compare it with the true 200. Then rerun the warm-up with `--jitter 10` and `--jitter 300` and see what happens to that spread. Connect what you find to the "rating drift" paragraph of lecture section 4.
6. **Visible-only reset (30 min).** Add a second number per player, a visible rank measured in stars, that resets to 0 at the season end while the hidden rating is kept (`alpha = 1`). Wins give `b` stars and losses cost 1, never below 0. Choose `b` as a function of the hidden rating so that a player at 1,900 true skill reaches 150 stars within 60 rounds. Report the rounds needed for players at 1,500, 1,700, 1,900 and 2,100.
7. **Write it up.**

## Deliverable

A zip or repository link containing:

- Your completed `season_sim.py` and `test_season_sim.py` with the test output pasted into the report.
- `report.md` (800 to 1,200 words) with: the control table; the step 3 sweep as a table with spreads across seeds; the step 4 comparison plot or table; your explanation of the step 5 surprise; the step 6 bonus rule and its results; and a closing recommendation stating `alpha`, `K` (with any provisional rule) and whether you reset hidden rating, visible rank or both, justified with at least two numbers from your tables.
- Commands and seeds for every table.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Weight |
|---|---|---|---|---|
| Correctness | All tests pass; control run reproduces; zero-sum preserved | Tests pass, control run missing or unstable | Tests fail | 20% |
| Reset sweep | Full grid, five seeds, excess measured against the control with spreads | Grid incomplete or single seed | No sweep | 20% |
| Model check | Model, single-player simulation and population compared; gap explained (curve bending, opponents who are themselves misplaced) | Comparison shown, explanation thin | Missing | 15% |
| Step 5 explanation | Spread measured; link between local matching, scale drift and compression explained with numbers | Correct idea without measurement | Missing or wrong | 15% |
| Visible track | Bonus rule meets the target at 1,900 and is reported for all four bands | Rule works for one band only | Missing | 15% |
| Recommendation | Specific rule, justified by numbers from the tables, names who pays the cost | Rule given with weak justification | Missing | 15% |
