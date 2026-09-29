# MMO405 · Lab 12: The review lottery and a real review

**Week:** 12 ([lecture](../lectures/w12-peer-review.md))
**Time:** 2 hours in the lab, plus up to 3 hours for the review and response letter.
**Work mode:** individual code and review. The response letter answers a classmate's review of your proposal draft, assigned by your instructor.
**Counts toward:** methods labs (30% of the course grade). The peer review of your classmate's draft also counts toward the final paper's process mark.

## Objective

Simulate two review committees, confirm the lecture's formula against the simulation, and use it to answer a design question for a venue. Then write a full review of an invented game-research manuscript, and a point-by-point response to the review your own draft received.

## Starter materials

- [`lab12-starter/committee.py`](lab12-starter/committee.py), Python 3, standard library only. Five stubs:
  - `spearman_brown` (TODO 1) and `reviewers_needed` (TODO 2), from week 4 and the lecture.
  - `both_accept` (TODO 3), the lecture's bivariate normal formula.
  - `simulate` (TODO 4), two committees scoring the same papers with independent noise.
  - `summarize` (TODO 5), precision and inconsistency from a table.
- [`lab12-starter/test_committee.py`](lab12-starter/test_committee.py), seven tests. All fail on the starter and pass on a correct solution. From inside `lab12-starter/`, run `python -m unittest test_committee.py` (from the repository root, `.venv/bin/python` is the course Python).
- [`lab12-starter/manuscript.md`](lab12-starter/manuscript.md), a short invented manuscript, "Voice Chat Makes Guilds Last". It contains several problems of the kinds covered in weeks 1 to 11, and some strengths.
- Your [lab 11](lab11.md) `grim_audit.py`, for checking the manuscript's numbers.
- The interactive [`examples/w12-review-lottery.html`](../examples/w12-review-lottery.html), once it is built.

## Steps

### Part A: the lottery (50 min)

1. Implement TODOs 1 to 5 until all seven tests pass. Run `python committee.py` and paste the output.
2. Run `simulate(166, 43.5 / 166, 0.55, seed)` for seeds 1 to 200. Report the mean and the 5th and 95th percentiles of precision. Is the NeurIPS 2014 precision of about 0.50 unusual under the model?
3. A game-research conference accepts 30% of papers with three reviewers each, and you estimate `ρ₁ = 0.3`. The organizers want at least 60% of accepted papers to survive a rerun. Using your functions, find the smallest number of reviewers that achieves it at 30% acceptance, and the highest acceptance rate that achieves it with three reviewers. Recommend one option in 100 words, with its costs.
4. Using `both_accept`, tabulate precision for acceptance rates 0.10, 0.20, 0.30 and 0.50 at `ρ = 0.55`. In two sentences, relate the table to the NeurIPS 2021 finding.

### Part B: the review (in the lab, then at home)

5. Review `manuscript.md` using the structure from lecture section 3: summary, strengths, numbered major concerns (each ending in a checkable request), minor concerns, recommendation and confidence. Use the week-by-week checklist. Run your lab 11 checker on every mean and p-value you can. Recompute the chi-square from the survival percentages and group sizes, and say whether it matches. 800 to 1,200 words.
6. Write the separate confidential comments to the editor (at most 100 words). Declare any conflict you would have if this were real, or state that you have none.

### Part C: the response letter (at home)

7. Your instructor sends you a classmate's review of your course-proposal draft. Write a point-by-point response letter: quote each comment, answer it, and say what you changed and where. Revise the draft to match.

## Deliverable

- `committee.py` passing all seven tests.
- A results sheet with the output of step 1 and your answers to steps 2 to 4.
- The review and the confidential comments (steps 5 and 6).
- The response letter and the revised proposal draft (step 7).

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code (step 1) | All tests pass; output matches | Tests pass with minor output errors | Tests fail | 15 |
| Lottery analysis (steps 2 to 4) | Simulation spread reported and compared with 0.50; both design options computed; recommendation weighs costs; 2021 link correct | Numbers right, interpretation thin | Missing or wrong | 20 |
| Review: major concerns (step 5) | Finds the design, sampling, claim, reporting and ethics problems that matter; every concern ends in a checkable request; number checks done and reported | Finds most problems; some requests vague | Lists minor points only, or requests nobody could act on | 30 |
| Review: summary, strengths, tone, confidentiality (steps 5 and 6) | Fair summary; real strengths named; criticizes the work, not the authors; conflicts addressed | One of these weak | Hostile or unfair | 15 |
| Response letter (step 7) | Every comment answered; changes located by section; disagreements argued with evidence; draft revised | Most comments answered; some changes not made | Missing | 20 |
| **Total** | | | | **100** |
