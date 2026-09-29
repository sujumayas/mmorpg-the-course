# MMO407 · Lab 05: Redesign break-even

**Week:** 5 ([lecture](../lectures/w05-case-star-wars-galaxies-and-the-nge.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs for the code, individual for the case analysis.
**Counts toward:** case analyses (50% of the course grade). The case analysis in Part C is one of the graded case analyses.

## Objective

Build the week 5 redesign model, then face its weakness head on. The break-even month depends most on two inputs nobody can measure in advance, new-player retention and the decline without the change. You will turn those guesses into ranges, compute the chance a redesign has paid off by a given month, and use the result to critique the NGE and propose what Sony Online Entertainment could have done instead.

## Starter materials

- [`lab05-starter/redesign.py`](lab05-starter/redesign.py), Python 3.10 or later, standard library only. It holds the lecture's invented game (`S0`, `SEGMENTS`, `HUBS`, `A`, `G_NEW`, `G_OLD`), a `print_lecture_tables` helper, and five stubs:
  - `departure_share` (TODO 1), `break_even` (TODO 2), `compound` (TODO 3) and `second_round` (TODO 4), the lecture's formulas.
  - `chance_by_month` (TODO 5), a Monte Carlo over `r`, `g_old` and each segment's `d`, seeded for repeatable results.
- [`lab05-starter/test_redesign.py`](lab05-starter/test_redesign.py) has five tests. All fail on the starter and pass on a correct solution. Run them from inside `lab05-starter/` with `python -m unittest test_redesign.py`.
- `python redesign.py` prints the lecture's break-even table once TODOs 1 and 2 are done.
- The interactive `examples/w05-redesign-break-even.html`, once it is built.

## Steps

### Part A: the library (35 min)

1. Implement TODOs 1 to 5 and run the tests until all pass. Check `python redesign.py` against the lecture's table.
2. Add the second round to the break-even. With `h = 0.5`, compute the total loss and the new break-even at `r = 25%`. You should get about 67,186 players and 11.2 months.
3. Derive and implement the retention `r` needed to break even by a target month `T`. Check it against the lecture's answer of 19.2% for `T = 12`.

### Part B: the chance it pays (40 min)

4. Run `chance_by_month(12, 10_000, 1, (0.10, 0.35), (0, 6_000), 0.1)`. Report the chance the redesign has broken even by month 12. With a correct solution this is close to 45%.
5. Tornado. Starting from the ranges in step 4, collapse one input at a time to its lecture value (`r = 0.25`, `g_old = 4,000`, `d_spread = 0`) and rerun. Which collapse changes the chance the most? Tabulate and plot the three changes as a bar chart.
6. Research is worth something. Suppose a two-week test server and survey would cut `d_spread` from 0.1 to 0.03, and a telemetry study would narrow `g_old` to 3,000 to 5,000. Compute the chance under each. In two sentences, recommend which study to fund first and why.
7. Compounding. Add a first change with `D₁ = 0.10` six months before the main one, and assume its players do not come back. Rerun step 4 with the main change applied to the smaller base (`S0 × 0.9`) and the same `g_old` measured against the original path. Explain in one sentence why the chance falls, or why it does not.

### Part C: case analysis (at home, 600 words, individual)

8. Build your own segment table for Star Wars Galaxies in November 2005, with at least four segments. Justify each segment's share and departure estimate qualitatively from the sources (the lecture's sources, the *New York Times* article of 10 December 2005, and at least one design essay by Raph Koster or another developer). Do not invent subscriber counts. Use shares and a symbolic `S₀`.
9. Write the counterfactual SOE claimed and what evidence you would have needed in 2005 to check it.
10. Recommend one alternative from lecture section 4 (split, stage, test on a copy, make it reversible, relaunch properly). State which parameters it changes and in which direction, and use your Part B results to argue why that direction matters most.

## Deliverable

- `redesign.py` passing all five tests, plus your code for steps 2 to 7.
- A results sheet with the numbers from steps 2 to 7 and the tornado chart.
- The 600-word case analysis (steps 8 to 10) with a source list giving each source's date.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Library (step 1) | All five tests pass | Minor numeric drift | Tests fail | 15 |
| Extensions (steps 2 and 3) | Second-round break-even and required `r` correct and derived | One missing | Both missing | 10 |
| Uncertainty (steps 4 to 7) | Chance reported; tornado correct and read; study recommendation justified with numbers; compounding explained | Numbers right, interpretation thin | Missing or wrong | 30 |
| Case analysis: evidence (steps 8 and 9) | Segments justified from dated sources, no invented counts, counterfactual stated with the evidence needed | Segments asserted without support | Invented numbers presented as fact | 20 |
| Case analysis: recommendation (step 10) | Alternative tied to specific parameters and to the Part B result | Alternative named, link to the model weak | Missing | 20 |
| Code quality | Readable, seeded, runs first time | Runs with minor fixes | Does not run | 5 |
| **Total** | | | | **100** |
