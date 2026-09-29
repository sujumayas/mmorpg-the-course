# MMO404 · Lab 06: Battle budget

**Week:** 6 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the labs (40%)

## Objective

Put numbers on the [week 6 lecture](../lectures/w06-massive-battles.md). In part A you implement MMO302 week 12's work and speed functions and this week's event-stream model, then measure how many pilot pairs are really within weapon range in a seeded battle and see whether a dense fight is `n²`. You design an aggregation scheme and show what it saves. In part B you find and fix a determinism bug in a small lockstep simulation by comparing checksums from two processes that differ only in their hash seed.

## Starter materials

Folder [`lab06-starter/`](lab06-starter/README.md). Standard library Python only.

- `battle.py`: MMO302's node constants (`A`, `B`, `C`, `FLOOR`) and TODOs for `work`, `speed`, `stream_Bps` and `count_pairs`. Given code builds battles (`make_battle`), a brute-force pair counter and the `--run` sweep.
- `lockstep.py`: a 300-unit skirmish that prints one checksum per tick, a runner that starts two machines with different `PYTHONHASHSEED`, and a TODO for `first_divergence`. The simulation contains one determinism bug.

## Steps

1. **The model.** Implement `work`, `speed` and `stream_Bps`. Before running `--check`, compute by hand `work(2000)`, its speed and the full, dilated and aggregated streams in kbit/s. Then run `python battle.py --check` until only `count_pairs` fails.
2. **Pairs.** Implement `count_pairs` with a grid (cells of side `radius`, 3 by 3 neighbourhood). It must equal `brute_pairs`. Time both on 2,000 pilots and report the ratio. Then explain why the grid saves much less here than in CS202 lab 13's world. Use the `pair_share` column from step 3 in your answer.
3. **The sweep.** Run `python battle.py --run battle.csv`. Plot work per game-second and the two streams against pilots on log-log axes. Measure the slope of `pairs_in_range` between 1,000 and 4,000 pilots. What exponent does it show, and what does that say about spatial partitioning in a dense fight?
4. **Where it breaks.** The sweep charges MMO302's `b` for each ordered pair actually in range, so only a share of all pairs costs anything. At what battle size does the node first dilate, and where does it hit the 10% floor? Extend the sweep until you find both, to the nearest 250 pilots, and compare them with MMO302's 861 and 3,016, which assume every pair is in range.
5. **Your aggregation.** Replace the default `circle = 20, squad = 10, summary = 8` with a scheme you design for a 3,000-pilot fight at MMO302's speed for that size. State who is in the circle and what a summary holds. Keep each client under 32 kbit/s. Report the per-client and server totals.
6. **Find the desync.** Implement `first_divergence` and run `python lockstep.py --check`. It reports the first tick where the two machines disagree. `--check` always starts the two machines with `PYTHONHASHSEED=1` and `PYTHONHASHSEED=2`, so the desync reproduces on every run. If you run one machine yourself, set the seed explicitly (`PYTHONHASHSEED=1 python lockstep.py --machine`). Without it, Python picks a new random hash seed for each process, and two runs you meant to compare may or may not agree. Find the line that causes it. Explain in three sentences why the two processes compute different bits from the same inputs, and why the checksum sees it even though no unit's health differs visibly.
7. **Fix it.** Fix the bug so `--check` prints `all checks passed`. Then name two other ways the same kind of bug could enter a C++ lockstep game (think about compilers, instruction sets and containers) and how you would guard against each.

## Deliverable

Your finished `battle.py` and `lockstep.py`, `battle.csv`, the plot from step 3, and a report (PDF or Markdown, at most three pages) with the hand calculation from step 1, the timing and explanation from step 2, the answers to steps 3, 4, 6 and 7, and the aggregation design from step 5. Submit before the week 7 lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Model code | `battle.py --check` passes; hand calculation of `work`, speed and streams agrees | Passes, hand calculation missing | Fails | 15% |
| Pair counting | Grid matches brute force; timing ratio reported and explained with the pair share | Correct, explanation thin | Brute force only or wrong counts | 15% |
| Scaling analysis | Log-log plot; slope near 2 measured and interpreted; dilation and floor sizes found | Plot present, interpretation thin | Missing | 20% |
| Aggregation design | Circle and summary justified by player needs; totals under the cap with numbers | Numbers present, design unjustified | Missing | 15% |
| Desync | Divergence tick found; cause explained with float non-associativity and hash-seeded set order; fix passes | Fixed without a clear explanation | Not fixed | 25% |
| Writing | Plain, units everywhere | Mostly clear | Hard to follow | 10% |
