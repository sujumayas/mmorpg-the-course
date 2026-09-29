# MMO407 · Lab 06: Exploit discovery and reopening

**Week:** 6 ([lecture](../lectures/w06-case-duplication-exploits-after-launch-new-world-2021.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs for the code, individual for the case analysis.
**Counts toward:** case analyses (50% of the course grade). The reopening rule from Part B also goes into the incident section of your final launch plan.

## Objective

Build the week 6 discovery curve, learn how far a fit from a short find log can be trusted, and write a reopening rule a live-ops lead could defend. Then analyse New World's first two months against the lecture's response kit.

## Starter materials

- [`lab06-starter/discovery.py`](lab06-starter/discovery.py), Python 3.10 or later, standard library only. It provides `sse`, `simulate_log` (one random find log from known `a` and `b`) and `load_log`, and five stubs:
  - `fit_two_points` (TODO 1), the lecture's hand fit.
  - `remaining` (TODO 2) and `next_week` (TODO 3), hidden exploits and next-week risk, with releases.
  - `reopen_week` (TODO 4), the first week the risk is below a limit.
  - `fit_least_squares` (TODO 5), a fit to a whole log using a grid over `b` and the closed-form best `a` for each.
- [`lab06-starter/test_discovery.py`](lab06-starter/test_discovery.py) has six tests. All fail on the starter and pass on a correct solution. Run them from inside `lab06-starter/` with `python -m unittest test_discovery.py`.
- [`lab06-starter/find_log.csv`](lab06-starter/find_log.csv), an invented eight-week find log for a launch: cumulative value-path exploits found by the end of each week.
- `python discovery.py` prints the lecture's table once TODOs 1 to 4 are done.
- The interactive `examples/w06-exploit-discovery-curve.html`, once it is built.

## Steps

### Part A: the library and its limits (45 min)

1. Implement TODOs 1 to 5 and run the tests until all pass. Check `python discovery.py` against the lecture's table.
2. Load `find_log.csv`. Fit it three ways: two points at weeks 2 and 4, two points at weeks 4 and 8, and least squares on all eight weeks. Tabulate `a`, `b` and the hidden count at week 8 for each. (A correct solution gives about `a = 24.5` and `a = 18.0` for the two-point fits, and about `a = 19.1`, `b = 0.24` for least squares.)
3. How much does a two-point fit wander? Use `simulate_log(12, math.log(2) / 2, [2, 4], seed)` for seeds 0 to 499 and fit each with `fit_two_points`, counting the logs it cannot fit. Report the share unfittable, the median `a`, and the 10th and 90th percentiles. Then repeat with eight weeks of data and `fit_least_squares`. Write two sentences on what this means for a team deciding on day 28.
4. Plot the find log as steps with the least-squares curve over it and the ceiling `a` as a dashed line.

### Part B: the reopening rule (35 min)

5. Trading closed at the end of week 8 after a dupe. Using the least-squares fit, find the reopening week for risk limits of 5%, 10% and 20%, starting the search at week 8.
6. The roadmap puts a guild bank in week 10, estimated to hold 3 exploits. Find the new reopening weeks. (At 10%, a correct solution moves reopening from about week 15.2 to about week 19.4.) Then consider shipping the guild bank in the week after trading reopens instead. Compute the chance of at least one new exploit in its first week live, and say what caps and switch it should ship with.
7. Write a reopening rule of at most 60 words that a communications lead could post. It must name the risk limit, the data it is based on, a second condition that does not depend on the fit (for example, days of clean conservation ledger), and who owns the decision.

### Part C: case analysis (at home, 600 words, individual)

8. Using the lecture's sources and at least two more contemporary reports (dated October to December 2021), build a dated timeline of New World's exploit and value incidents from launch to the end of November 2021. For each, note the value path involved and the response.
9. Score New World against the lecture's section 4 response kit, row by row, with the evidence for each score. Name the row where the evidence is thinnest and say what document you would want to see.
10. Explain why you cannot honestly fit `a` and `b` to New World's public record, and what the public record does let you conclude. End with one transferable lesson written as an instruction to a future launch team.

## Deliverable

- `discovery.py` passing all six tests, plus your code for steps 2 to 6.
- A results sheet with the tables from steps 2, 3, 5 and 6, and the plot from step 4.
- The reopening rule (step 7).
- The 600-word case analysis (steps 8 to 10) with a dated source list.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Library (step 1) | All six tests pass | Minor numeric drift | Tests fail | 15 |
| Fits and their spread (steps 2 to 4) | Three fits tabulated; simulation spread and unfittable share reported for both methods; clear conclusion; plot labeled | Fits right, spread missing or unexplained | Missing | 25 |
| Reopening rule (steps 5 to 7) | Weeks correct; both guild-bank timings compared; rule within 60 words with limit, data, second condition and owner | Rule missing one element | Missing | 20 |
| Case analysis: timeline and scoring (steps 8 and 9) | Dated, sourced timeline; every kit row scored with evidence; thinnest row named | Timeline or scoring incomplete | Unsourced | 20 |
| Case analysis: limits and lesson (step 10) | States why a fit is not possible and what can be concluded; lesson is a concrete instruction | Vague on limits or lesson | Missing, or a fitted "New World a" presented as fact | 15 |
| Code quality | Readable, seeded, runs first time | Runs with minor fixes | Does not run | 5 |
| **Total** | | | | **100** |
