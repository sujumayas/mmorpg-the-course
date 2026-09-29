# MMO307 · Lab 04: The season ladder

**Week:** 4, gear treadmills and item level ([lecture](../lectures/w04-gear-treadmills-and-item-level.md)).
**Time:** 2 hours in lab, plus up to 3 hours at home.
**Weight:** part of the progression analysis (30%).

## Objective

Read two real World of Warcraft seasons' upgrade-track tables, compute where each old item lands on the next season's ladder and how long it survives, convert item-level gaps into power under exponential and linear budgets, and then design a three-season ladder for a fictional MMO that meets targets you set for carry-over, growth and sharing.

## Starter materials

All in [`lab04-starter/`](lab04-starter/). Standard-library Python, run with `.venv/bin/python` or any Python 3.10+.

- [`tracks.csv`](lab04-starter/tracks.csv), the upgrade tracks of Midnight Seasons 1 and 2 and The War Within Seasons 2 and 3 (base ranks only, no event ranks), transcribed from the Warcraft Wiki tables cited in the lecture. One row per `season, track, rank, ilvl`.
- [`ladder.py`](lab04-starter/ladder.py), a loader that works and eight functions to write: `ladder`, `ranks_at`, `landing`, `survival`, `gap_exp`, `gap_linear`, `creep_for_landing` and `max_width`. Each docstring states the rule from the lecture. Running the file lists the seasons it loaded.
- [`test_ladder.py`](lab04-starter/test_ladder.py), tests built from the lecture's numbers: ladders (220, 289) and (266, 334) for Midnight; 289 is Veteran 4 in Season 2 and 678 is Veteran 4 in War Within Season 3; the landing table (−0.42, −0.04, 0.14, 0.33); survival 0, 0, 0, 1, 1; gaps 1.26, 1.58 and 1.99 at `g = 1%`; the linear-budget spread 1.28; `c = 46` for `x = 1/3`. Run `python test_ladder.py`. Every test prints `TODO` on the starter, and the script exits with status 1 until all pass.
- The [interactive](../examples/w04-season-ladder.html) for spot checks.

## Steps

1. **Read the data.** Implement `ladder` and `ranks_at`. For each of the four seasons print entry, top and width `W`. For both seams (Midnight 1 to 2, War Within 2 to 3) print the creep `c` and the carry-over ratio `W / c`.
2. **Landing table.** Implement `landing` and `survival`. For every track's top rank in the older season of each seam, print `x_1`, the new season's rank label at that item level (or "below the ladder"), and `n_max`. Confirm the lecture's table for Midnight and build the same table for The War Within.
3. **Gaps.** Implement `gap_exp` and `gap_linear`. For both seams, compute the patch-day gap, season growth and in-season spread under `g = 1%` and under the linear budget `0.6 i + 15.5`. Put all twelve numbers in one table.
4. **Tests.** Implement `creep_for_landing` and `max_width`, then run the tests until they all pass.
5. **A per-level curve from data (short).** Using `gap_linear`, plot the effective `g` per item level, `a / (a i + b)`, from item level 100 to 700. At what item level has it halved from its value at 146? Write two sentences on what that means for a game that keeps adding the same 45 levels per season on a linear budget.
6. **Design task.** Design three seasons for a fictional MMO with `g = 0.8%` per item level. Your targets:
   - the old top lands between 0.30 and 0.45 of the new ladder;
   - season growth at the top is at least 1.6;
   - the in-season spread fits inside `F = 2`;
   - the patch-day gap (old top against new entry) is at most 1.2.
   Show that the four targets cannot all be met exactly as written, relax the one you think matters least, and justify it. Then split each season into tracks (at least four, two-rank overlap) and write the result as a `tracks.csv` in the same format as the starter's. Your own functions must reproduce your targets from that file.
7. **Critique.** Pick one of the two real seams. In at most 200 words, say which kind of player it serves best and worst, using at least two numbers from your tables.

## Deliverable

Your completed `ladder.py` with passing tests, your design `tracks.csv`, and a report of at most 700 words with the step 1 to 3 tables, the step 5 plot and answer, the step 6 design with its four target values, and the step 7 critique.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Code correctness | All provided tests pass; functions reused for the design, no hard-coded answers | Tests pass, some values typed in by hand | Tests fail | 25% |
| Real-data tables | Both seams analysed, landing ranks labelled, gaps under both budgets | One seam complete, the other partial | Tables missing or wrong | 20% |
| Budget comparison | Plot correct, halving level found, consequence explained with numbers | Plot correct, explanation vague | Missing | 15% |
| Ladder design | Conflict shown algebraically, relaxation justified, CSV reproduces all targets | Design meets three targets, CSV present | Targets unchecked | 30% |
| Critique and report | Specific player types, numbers cited, within length | General but correct | Missing or over length | 10% |
