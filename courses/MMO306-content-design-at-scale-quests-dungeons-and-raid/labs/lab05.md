# MMO306 · Lab 05: Telegraph tuning from measured data

**Week:** 5, telegraphing and readability ([lecture](../lectures/w05-telegraphing-and-readability.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the encounter designs (40%).

## Objective

Tune telegraphs for a 20-player raid from measured response times instead of an assumed bell curve. You will fit the lecture's normal model to a data set, show where its tail disagrees with the data, and set telegraph lengths and failure outcomes for three mechanics so the raid reaches a stated clean-pull target.

## Starter materials

All in [`lab05-starter/`](lab05-starter/). Standard-library Python 3.10 or later.

- [`reaction_times.csv`](lab05-starter/reaction_times.csv): 400 measured response times (`player, trial, needed_ms`), 20 trials from each of 20 players. The times are the full budget from GD101 week 12 (see, decide, act) plus an 80 ms round trip. The data set is synthetic but shaped like real response-time data: a bell with a long slow tail.
- [`telegraph.py`](lab05-starter/telegraph.py): a CSV loader and eight functions marked TODO: `fit_normal`, `p_normal`, `p_empirical`, `p_clean`, `expected_misses`, `required_normal`, `required_empirical` and `shift`.
- [`test_telegraph.py`](lab05-starter/test_telegraph.py): the lecture's values (97.7% per player and a 10% clean pull at 1,000 ms for 20 players × 5 casts; 1,193 ms for a 95% clean pull) and the data set's values (mean 698.3 ms, sd 153.6 ms; 99.0% of responses by 1,200 ms). Run it with `python test_telegraph.py`. Every test fails on the starter.
- The [interactive](../examples/w05-raid-telegraph.html), which can overlay the same data set.

## Steps

1. **Implement and test.** Fill in the eight functions until all tests pass.
2. **Model versus data.** For `T_tel` from 900 to 1,400 ms in steps of 50, tabulate `p_normal` (fitted), `p_empirical`, and the clean-pull chance for 20 players × 5 casts under each. Mark the telegraph length where the two clean-pull columns differ most.
3. **Per-player spread.** Compute each player's own mean. Which three players are slowest? What share of all responses over 1,100 ms come from them? Write two sentences on what this means for a raid that recruits by average skill.
4. **Latency.** Use `shift` to add 170 ms for one player (a 250 ms connection instead of 80 ms). Recompute the clean-pull chance at 1,100 and 1,200 ms for a raid of 19 players drawn from the data plus that one player. Compare with the lecture's section 4 figure.
5. **Tune three mechanics.** For a 20-player raid, design (a) a raid-wide wipe mechanic cast 3 times, (b) a mechanic that targets 4 players and kills them, cast 6 times, (c) a raid-wide mechanic that applies a debuff on failure, cast 8 times. Set each telegraph from the empirical data so that (a) has a 95% clean pull, (b) averages at most 0.5 deaths per pull, and (c) averages at most 3 misses per pull. Report each telegraph length, and say where the 400-sample data set is too small to answer (step 2's last rows will show you).
6. **Readability plan.** For mechanic (a), write its shape, colour, timer, target marker and sound using the lecture's section 3 table, and name one redundancy you added for a player who would otherwise sit in the slow tail.

## Deliverable

`telegraph.py` with all tests passing, the step 2 table, and a memo of at most 600 words covering steps 3 to 6. Include one sentence on how many more samples you would need to set mechanic (a) with confidence, and why.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Implementation | All tests pass; functions short and readable | Tests pass, code repetitive | Tests fail | 25% |
| Model versus data | Table complete; tail disagreement located and explained | Table complete, explanation thin | Missing or wrong | 20% |
| Latency and spread | Both analyses correct, raid consequence stated | One analysis correct | Missing | 15% |
| Three tuned mechanics | All three meet targets from empirical data; sample-size limit named | Targets met from the normal model only | Targets not met | 25% |
| Readability plan | Every channel specified, redundancy aimed at a named group | Channels listed without reasons | Missing | 15% |
