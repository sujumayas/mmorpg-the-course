# MMO306 · Lab 08: Rotations and caps

**Week:** 8, repeatable content ([lecture](../lectures/w08-repeatable-content-dailies-dungeons-rotations.md)).
**Time:** 2 hours in the lab, plus up to 2 hours at home.
**Work mode:** pairs.
**Counts toward:** final dungeon (60%). Your dungeon's repeat structure must use numbers from this lab.

## Objective

Measure how fast a rotation wears out, check the formula against a simulation, and size a pool for a freshness target. Then run hard and accumulating weekly caps against 16 weeks of play logs and find a cap that meets a two-sided design target.

## Starter materials

All in [`lab08-starter/`](lab08-starter/). Python 3, standard library only.

- [`repeatables.py`](lab08-starter/repeatables.py): eight functions to write, each with a docstring stating its exact rule, plus `load_hours` and a `report()` that prints the lab's numbers once the functions work.
- [`test_lab08.py`](lab08-starter/test_lab08.py): eight checks, all failing on the starter. Run `python test_lab08.py` inside the folder.
- [`hours.csv`](lab08-starter/hours.csv): 400 invented players, hours played in each of 16 weeks. About one week in ten is a missed week (0 hours).
- The [rotation interactive](../examples/w08-rotation-wear.html) for spot checks.

## Steps

### Part A: rotations (50 min)

1. Implement `expected_repeats`, `exposure` (both modes), `periods_to` and `pool_for_target`. Your numbers must match the lecture table: Tol Barad `X(3) = 61.5%`, 7.2 days to 90%; Firelands 5.8 days.
2. Implement `simulate_exposure`. With 3,000 trials, the simulated exposure for `S = 22`, `a = 6`, `d = 3` must land within one point of the formula. Explain in one sentence why a simulation is worth writing when a formula exists (hint: the next step has no clean formula).
3. Turn on `no_repeat_yesterday`. Simulate `S = 22`, `a = 6` for 1 to 7 days and plot it next to the random-draw and fixed-cycle curves. Where does the memory rule sit between the two?
4. Your hub offers 6 quests a day. Find the smallest pool that keeps random-draw exposure at or below 75% after 7 days (the check expects 34). Then find the smallest pool that meets the same target with the memory rule, by simulation. How many quests does the memory rule cost or save?

### Part B: caps (50 min)

5. Implement `weeks_to_goal` (hard, accumulating and no cap), `percentile` and `finish_weeks`. The checks replay section 4 of the lecture: the 30-hour player who misses three weeks finishes in week 11 under a hard cap and week 8 under an accumulating one.
6. Run `report()`. With `r_c = 60`, `G = 3,600` and `C = 450`, the finish-week percentiles should be p10 = 8 and p50 = 10 (hard) or p50 = 9 (accumulating), and 90 players never finish within 16 weeks. Note that a low finish-week percentile means a fast player.
7. Sweep `C` from 300 to 1,000 in steps of 50, both cap types. Tabulate p10, p25, p50 and p75 of finish week. Which percentile moves least as the cap changes (it sits at 15 for most caps)? Connect this to week 1's gate result in two sentences.
8. Design target: the fastest 10% must finish no sooner than week 8, and the median no later than week 9. Find every `(C, type)` pair in your sweep that meets it. Explain why only one cap type works.

## Deliverable

- `repeatables.py` passing all eight checks.
- A memo of at most 450 words to the live team with: the pool size for the daily hub and your random-versus-memory recommendation, the cap sweep table, your chosen `(C, type)` with its percentiles, and one sentence naming the chore your choice creates.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Rotation functions and simulation | All checks pass; memory-rule curve plotted and placed correctly between random and cycle | Checks pass, plot or placement missing | Checks failing | 25% |
| Pool sizing | Both pool sizes found, cost of the memory rule stated in quests | One pool size found | Missing | 15% |
| Cap functions | All checks pass; percentile direction handled correctly | Minor slip in percentiles | Checks failing | 20% |
| Cap design | Sweep complete, fixed percentile identified and explained, every qualifying pair found with a correct reason | Sweep done, reasoning thin | Target not checked | 30% |
| Memo writing | Plain, numeric, within the word limit | Some vague claims | Hard to act on | 10% |
