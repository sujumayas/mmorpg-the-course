# MMO307 · Lab 12: Designing an alternative advancement track

**Assigned:** week 12 ([lecture](../lectures/w12-alternative-advancement-and-account-progression.md), [interactive](../examples/w12-aa-gap.html)). **Due:** start of week 13 class. **Feeds:** the progression analysis assessment (30%).

## Objective

Implement the lecture's cost schedules and value rules, then search for an AA track that meets five targets at once for a light (5 hours a week) and a heavy (20 hours a week) player over three years. The targets conflict. The point of the lab is to show where they conflict, with numbers, and to make a defended choice about which one to relax or how to change the design so the conflict goes away.

## Starter materials

The folder [`lab12-starter/`](lab12-starter/) contains:

- [`aa_schedules.py`](lab12-starter/aa_schedules.py). A design is a dictionary with a cost schedule (`flat`, `linear` or `geometric`, plus parameters) and a value rule (`constant`, `decaying` or `capped`, plus parameters). `evaluate` is written for you. It plays both players through 156 weeks and returns the final gap, the peak gap, the light player's points at week 10 and the heavy player's average weeks per point in year 3. The three lecture designs are included as `LECTURE_DESIGNS`. Three functions are stubs: `cost_of_point`, `points_after` and `power`. As shipped, the script runs and prints a `TODO` line.
- [`test_aa_schedules.py`](lab12-starter/test_aa_schedules.py). Four tests. From the repository root, run `.venv/bin/python courses/MMO307-game-balance-ii-pvp-progression-and-endgame/labs/lab12-starter/test_aa_schedules.py` (or `python3 test_aa_schedules.py` inside the folder). All four fail on the starter and must pass on your solution. The script exits with status 1 on any failure.

Standard library only.

## The five targets

Your content serves a band of `F = 1.3`. Product has asked for these:

| Target | Measure | Requirement |
|---|---|---|
| A. Long-run gap | `G` at week 156 | at most 1.20 |
| B. Peak gap | largest `G` in weeks 1 to 156 | at most 1.30 |
| C. Early hook | light player's points at week 10 | at least 10 |
| D. Heavy cadence | heavy player's average weeks per point in year 3 | at most 1.0 |
| E. Meaningful late points | value of the heavy player's next point at week 156 | at least 0.5% power |

Target D averages over the whole third year, so the lecture's geometric design scores 6.5 weeks per point here (8 points in weeks 105 to 156), not the 7.7 weeks the lecture quotes for the single next point at week 156.

## Steps

1. **Implement (30 min).** Complete the three stubs from their docstrings and lecture sections 2 and 3. Run the tests until all pass. Run the script and check that the three lecture designs print the lecture's numbers.
2. **Add target E (20 min).** Extend `evaluate` to return the value of the heavy player's next point at week 156 (`v` for constant value, `v₀ × d^n` for decaying, 0 past the cap for capped). Add a test for it using a value from the lecture (the decaying design with `v₀ = 2%`, `d = 0.98` and flat 10-hour costs gives about 0.004%).
3. **Score the lecture designs (15 min).** Make a table of the three lecture designs and the lecture's decaying design against all five targets. Mark each pass or fail.
4. **Search (45 min).** Write a grid search over at least two schedules and two value rules, with at least 200 designs in total. Report how many meet each target on its own, how many meet A to D together, and how many meet all five.
5. **Find the conflict (30 min).** You should find that no design in the grid meets all five, while every pair of targets can be met together. Find the smallest set of targets that no design meets. (A grid of about 1,000 designs across all schedules and value rules points to a set of three.) Explain with the lecture's argument why that set cannot hold under a single number per point, in a short algebraic or numeric argument.
6. **Resolve it (45 min).** Choose one route and implement it in `aa_schedules.py`. Either (a) relax one target and argue for it as the designer, or (b) change the design so every target holds, for example a second, non-power reward track on a steady clock, a cost tied to a moving server line in the style of Diablo Immortal, or a hybrid schedule. If you choose (b), state precisely how target E is measured in your design and why that measure is honest.
7. **Account-wide share (15 min).** Using the lecture's alt-cost model with `T_c = 40` hours, decide what share `s` of your AA track is account-wide. Report the cost of four characters and one risk your choice creates for the band `F`.
8. **Write it up.**

## Deliverable

A zip or repository link containing:

- Your completed `aa_schedules.py` and `test_aa_schedules.py`, with the test output pasted into the report.
- `report.md` (800 to 1,200 words) with: the step 3 table; the step 4 counts; the step 5 argument; your step 6 design as a spec a programmer could implement, with its values on all five targets; a chart of `G` over 156 weeks for your design next to the flat lecture design; and the step 7 decision.
- The commands that produce every table and chart.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Weight |
|---|---|---|---|---|
| Implementation | All tests pass, target E added with its own test, lecture numbers reproduced | Tests pass, target E missing a test | Tests fail | 20% |
| Search | 200+ designs, counts per target and combined, clear table | Smaller grid or counts incomplete | No search | 20% |
| The conflict | Names the smallest conflicting set and proves it with a short argument tied to gap, cadence and value | Names the set without an argument | Missing or wrong | 20% |
| Resolution | Design or relaxation fully specified, measured on all five targets, honest about what E now means | Resolution given, partly measured | Missing | 25% |
| Account share and judgment | `s` chosen with numbers, a real risk to `F` named | Numbers without the risk, or the reverse | Missing | 15% |
