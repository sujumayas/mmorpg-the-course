# MMO307 · Lab 10: Queue time vs match fairness

**Assigned:** week 10 ([lecture](../lectures/w10-matchmaking-quality-vs-queue-time.md), [interactive](../examples/w10-queue-fairness-curve.html)). **Due:** start of week 11 class. **Feeds:** the rating lab assessment (30%) and [lab 11](lab11.md), which reuses your matchmaker.

## Objective

Implement the lecture's closed-form model of wait and fairness, then build a second-by-second queue simulation where waiting players match each other with expanding windows. Use the two together to measure waits by rating band and to tune a matchmaker against a written wait target and fairness ceiling, at peak and off-peak.

## Starter materials

The folder [`lab10-starter/`](lab10-starter/) contains:

- [`queue_model.py`](lab10-starter/queue_model.py). Part A holds the closed-form functions `share_in_window`, `mean_wait` and `mean_favourite_score`. Part B holds the simulation: `window`, `match_pool`, `simulate_queue` and `summarise`. The arrival loop (Poisson arrivals, normal ratings, a seeded `random.Random`) is written for you. Four functions are stubs that raise `NotImplementedError`. The file runs as shipped and prints a `TODO` line for each missing part.
- [`test_queue_model.py`](lab10-starter/test_queue_model.py). Five tests. From the repository root, run `.venv/bin/python courses/MMO307-game-balance-ii-pvp-progression-and-endgame/labs/lab10-starter/test_queue_model.py` (or `python3 test_queue_model.py` inside the folder). All five fail on the starter and must pass on your solution. The script exits with status 1 if any test fails.

Standard library only. The population defaults are `μ = 1500`, `σ = 200`, `λ = 12` players per minute, as in the lecture.

## Steps

1. **Closed form (30 min).** Implement `share_in_window`, `mean_wait` and `mean_favourite_score` from lecture section 2. Run the file and check that your Part A output matches the lecture's table to the printed precision.
2. **The matching rule (45 min).** Implement `match_pool`. Its docstring gives the rule. Sort by rating, walk upward, pair neighbours whose gap fits inside the smaller of their two current windows. Run the tests until all five pass.
3. **Model vs simulation (30 min).** Run `simulate_queue` for 2 hours of queue time (`seconds=7200`) with a fixed window (set `growth=0`, `w0=w_max=50`) and seed 1. Compare the simulated mean wait of players rated 1450 to 1550 with the model's 25.3 seconds. Explain the difference in two or three sentences. (Hint: which opponents does the model ignore?)
4. **Waits by band (45 min).** Change `simulate_queue` or write a wrapper so that it records each matched player's rating and wait. With the default expanding window (`w0 = 25`, `growth = 5`, `w_max = 400`), report the median and 90th-percentile wait, and the mean favourite score, for five bands: below 1300, 1300 to 1500, 1500 to 1700, 1700 to 1830, above 1830 (roughly the top 5%). Use at least three seeds and report the spread.
5. **Tune for peak (30 min).** Targets: the 90th-percentile wait of the top band is at most 120 seconds, and the population's mean favourite score is at most 0.60. Try `growth` in {1, 2, 5, 10, 20} at `λ = 12`. Report which values meet both targets and pick one.
6. **Off-peak (30 min).** Repeat step 5 at `λ = 3`. You will probably find no single `growth` meets both targets. Propose a rule that does something sensible anyway (for example a growth rate that depends on `λ` or on the player's band, or a merged queue for the top band). Implement it, rerun, and report its numbers.
7. **Write it up.**

## Deliverable

A zip or repository link containing:

- Your completed `queue_model.py` and `test_queue_model.py`, with the test output pasted into your report.
- `report.md` (700 to 1,000 words) with: the step 3 comparison and explanation; the step 4 band table with seeds; the step 5 and step 6 tuning tables; your off-peak rule, stated as a spec a programmer could implement; and one paragraph naming the player your rule treats worst and what they experience in seconds and win probability.
- The command lines and seeds for every table.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Weight |
|---|---|---|---|---|
| Closed-form model | All Part A values match the lecture; code is clear | Values match with minor rounding differences or unclear code | Values wrong | 20% |
| Simulation correctness | All tests pass; both-windows rule applied; step 3 difference explained by waiting-pool opponents | Tests pass, explanation missing or vague | Tests fail | 25% |
| Band analysis | Five bands, percentiles and fairness, several seeds with spread | Bands reported for one seed only | Population averages only | 20% |
| Tuning and off-peak rule | Peak choice justified against both targets; off-peak rule implemented, measured and stated as a spec | Rule proposed but not implemented, or measured without targets | No tuning | 25% |
| Judgment and reproducibility | Worst-off player named with numbers; every table reproducible from given commands | One of the two done well | Neither | 10% |
