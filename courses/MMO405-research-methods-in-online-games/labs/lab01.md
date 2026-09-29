# MMO405 · Lab 01: Question cards and a selection audit

**Week:** 1 ([lecture](../lectures/w01-research-questions-in-game-studies.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish.
**Work mode:** individual code; question cards may be drafted in pairs but each student submits their own.
**Counts toward:** methods labs (30% of the course grade). Your better question card becomes page 1 of the course proposal (20%).

## Objective

Measure how much of a dashboard's "guild members stay longer" gap is selection, show that stratifying on a coarse proxy removes only part of it, and turn your own research interest into two question cards with explicit claim types.

## Starter materials

- [`lab01-starter/selection_audit.py`](lab01-starter/selection_audit.py), Python 3, standard library only. It loads the data and computes a retention rate, and has three stubs:
  - `observed_gap` (TODO 1), the dashboard comparison.
  - `stratified_gap` (TODO 2), the within-stratum comparison weighted by stratum size.
  - `selection_term` (TODO 3), the lecture's `(r_H − r_L) × (s_T − s_U)`.
- [`lab01-starter/players.csv`](lab01-starter/players.csv), an invented log of 2,000 new accounts with four columns: `account_id`, `week1_band` (low, mid or high play time in week one), `in_guild_d7` and `active_d30`. [`make_players.py`](lab01-starter/make_players.py) regenerates it.
- [`lab01-starter/test_selection_audit.py`](lab01-starter/test_selection_audit.py) has eight tests. All fail on the starter and pass on a correct solution. Run them from inside `lab01-starter/` with `python -m unittest test_selection_audit.py` (from the repository root, `.venv/bin/python` is the course Python).
- The interactive [`examples/w01-selection-gap.html`](../examples/w01-selection-gap.html), once it is built.

## Steps

### Part A: the selection audit (60 min)

1. Implement `observed_gap` (TODO 1). Report guild and non-guild 30-day retention and the gap to one decimal place.
2. Implement `stratified_gap` (TODO 2) and `selection_term` (TODO 3). Run all eight tests. Then run `python selection_audit.py` and copy its report into your results sheet.
3. Using your numbers, state how many points of the observed gap are selection and how many are the guild effect, assuming week-one play time captures everything that drives selection.
4. Real proxies are coarser than this one. Merge `mid` and `high` into one band called `engaged` (write a few lines that relabel the rows, do not edit the CSV) and rerun the stratified gap. Report the new estimate. Explain in three sentences why a coarser stratifier leaves some selection behind, pointing to the rows of your per-stratum output that show it.
5. Pick one of the three bands and compute its `r_H − r_L`-style contrast yourself. In the full data, treat `high` as H and `low` as L, ignore `mid`, and use their non-guild retention rates and their shares among guild and non-guild accounts (restricted to those two bands). Compute the selection term with your function and compare it to the observed gap for those 1,400 accounts. Say whether the two-kind formula accounts for the whole gap and why.

### Part B: question cards (50 min)

6. Choose the topic you are most likely to study for your course proposal. Write **two** question cards using the lecture's template (all eleven fields), with different claim types. At least one must be answerable with data you could realistically get this term: public data, a game you can observe, players you can interview, or a studio partner your instructor has approved.
7. Score both cards on FINER (1 to 3 per letter) and write one sentence justifying each score.
8. For any associational or causal card, write a selection audit: the most likely variable driving selection, the sign you expect for each bracket of the selection term, and one design (stratification, within-person comparison, randomized encouragement, natural experiment) that would shrink it. For an interpretive card, instead name whose voices your sampling would miss.

## Deliverable

- `selection_audit.py` passing all eight tests, plus your code for steps 4 and 5.
- A results sheet (one page) with the step 2 report and your answers to steps 3 to 5.
- Two question cards with FINER scores and the audit from step 8 (two pages at most).

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code (steps 1 and 2) | All tests pass; report matches | Tests pass with minor output errors | Tests fail | 20 |
| Selection reasoning (steps 3 to 5) | Correct coarse-stratifier estimate; residual selection explained with the per-stratum numbers; two-kind check done and interpreted | Numbers right, explanation vague | Missing or wrong | 25 |
| Question cards (step 6) | Both cards complete; claim types match the proposed data; constructs operationalized precisely | Cards complete but one measure or unit is vague | Missing fields or claim type mismatched to data | 30 |
| FINER and audit (steps 7 and 8) | Scores justified; selection variable plausible with signed brackets and a fitting design | Scores given without real justification | Missing | 20 |
| Code quality | Readable, runs first time | Runs with minor fixes | Does not run | 5 |
| **Total** | | | | **100** |
