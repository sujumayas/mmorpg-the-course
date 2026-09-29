# MMO407 · Lab 04: Patch or rebuild

**Week:** 4 ([lecture](../lectures/w04-case-ffxiv-1-0-to-a-realm-reborn.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** pairs for the code, individual for the case analysis.
**Counts toward:** case analyses (50% of the course grade). The case analysis in Part C is one of the graded case analyses.

## Objective

Turn the week 4 model into a small library, add the one thing the lecture's formula leaves out (players leave while the visible game is bad), and use it to ask whether Final Fantasy XIV's choice to keep the old game running was worth its months. Then apply the model to a second relaunch from the public record.

## Starter materials

- [`lab04-starter/rebuild_model.py`](lab04-starter/rebuild_model.py), Python 3.10 or later, standard library only. It provides the lecture's reference values `REF`, a `patch_gap` helper and `print_lecture_table`, and five stubs:
  - `patch_months` (TODO 1), `rebuild_months` (TODO 2) and `crossover_m` (TODO 3), the lecture's formulas.
  - `old_game_gap` (TODO 4), the gap players of the old game see during a rebuild, when a share `s` of the team keeps patching it at the old-code price.
  - `players_after` (TODO 5), a month-by-month player count where each month a share `base + k × gap / G` leaves.
- [`lab04-starter/test_rebuild_model.py`](lab04-starter/test_rebuild_model.py) has five tests. All fail on the starter and pass on a correct solution. Run them from inside `lab04-starter/` with `python -m unittest test_rebuild_model.py`.
- `python rebuild_model.py` prints the lecture's section 2 and 3 tables once TODOs 1 to 3 are done.
- The interactive `examples/w04-patch-or-rebuild.html`, once it is built.

## Steps

### Part A: the library (35 min)

1. Implement TODOs 1 to 5 and run the tests until all pass. Run `python rebuild_model.py` and check it prints the lecture's six lines exactly.
2. Write a function that returns the crossover rebuild time, the `T_r` at which both paths take equally long for given `G`, `φ`, `m`, `F`. Check it against the lecture's first "check this example" question (60 months for game C).
3. Sensitivity. For game C, vary each of `G`, `φ`, `m`, `F` and `T_r` by ±25% one at a time and record the change in `T_patch − T_rebuild`. Rank the five parameters by how much they move the decision. One sentence on what the ranking means for where a team should spend its estimation effort.

### Part B: players during the wait (45 min)

The lecture's model finishes on the team's clock. Players leave on theirs. Use `players_after` with `P0 = 100,000`, `base = 0.02` and `k = 0.05`.

4. **Patch path.** Using `patch_gap` for game C, compute the players left at month 39 (the month the rebuild would finish with `s = 0`). You should get about 9,987.
5. **Rebuild path.** For `s` in 0, 0.1, 0.2, 0.25, 0.3 and 0.4, compute the build length and the players of the old game left at relaunch, using `old_game_gap`. Round the build length to whole months. Tabulate. Which `s` leaves the most players at relaunch under this model?
6. **The missing term.** The model in step 5 says keeping people on the old game only delays the relaunch. The lecture argued the old-game patches also buy proof, which lowers churn. Add a trust term: while `s > 0`, the base churn falls from `base` to `base × (1 − τ)`. Find the smallest `τ` for which `s = 0.25` leaves more players at relaunch than `s = 0`. Write two sentences on whether a value that large is plausible, citing what Final Fantasy XIV's team did in 2011 and 2012.
7. **Compare.** At month 39, how do the patch path (step 4) and the best rebuild plan compare? Both numbers are small against 100,000. State what that says about any studio in game C's position, whatever it chooses.

### Part C: case analysis (at home, 600 words, individual)

8. Choose **The Elder Scrolls Online (2014 to 2015)** or **No Man's Sky (2016 to 2018)**. From public sources (start with the Wikipedia articles cited in the lecture and at least one contemporary news report), estimate for your case:
   - the gap `G` and its structural share `φ`, from a list of at least six problems reviewers or players named at launch, each tagged structural or not;
   - whether the evidence suggests a high or low `m`;
   - what the studio actually did, and when, as a short dated timeline.
9. State which path the model recommends for your case, whether the studio took it, and one thing the model misses about the case (for example, a business-model gap, or players' trust). End with one transferable lesson written as an instruction to a future launch team.

## Deliverable

- `rebuild_model.py` passing all five tests, plus your code for steps 2 to 7.
- A results sheet with the sensitivity ranking (step 3), the step 5 table, the `τ` from step 6 and the step 7 comparison.
- The 600-word case analysis (steps 8 and 9) with a source list that gives the version or date of each source.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Library (step 1) | All five tests pass, table prints exactly | Minor numeric drift | Tests fail | 15 |
| Crossover and sensitivity (steps 2 and 3) | Crossover `T_r` correct; ranking computed and interpreted | One of the two missing or unexplained | Missing | 15 |
| Players during the wait (steps 4 to 7) | Table correct; `τ` found and judged against the case record; comparison stated | Numbers right, reasoning thin | Missing or wrong | 25 |
| Case analysis: evidence (step 8) | Six or more problems tagged and sourced with dates; timeline correct | Fewer problems or weak sources | Unsourced | 20 |
| Case analysis: judgment (step 9) | Clear recommendation from the model, honest about what it misses, a transferable lesson as an instruction | Recommendation without limits, or lesson vague | Missing | 20 |
| Code quality | Readable, runs first time | Runs with minor fixes | Does not run | 5 |
| **Total** | | | | **100** |
