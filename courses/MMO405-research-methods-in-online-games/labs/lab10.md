# MMO405 · Lab 10: A randomized response study and its ethics application

**Week:** 10 ([lecture](../lectures/w10-ethics-and-irb.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish the application.
**Work mode:** individual. You may discuss Part B with your proposal partner, but each student submits their own application.
**Counts toward:** methods labs (30% of the course grade). Part B becomes the ethics section of your course proposal (20%).

## Objective

Implement randomized response, show on simulated data that a noisy but honest method beats a precise but dishonest one, and write a complete ethics application for your own course project.

## Starter materials

- [`lab10-starter/rr.py`](lab10-starter/rr.py), Python 3, standard library only. It loads the survey and prints a report. Five stubs:
  - `p_yes` (TODO 1), the chance of a "yes", `q = tπ + (1 − t)/2`.
  - `estimate` (TODO 2), the estimate and its standard error.
  - `epsilon` (TODO 3), the privacy level `ln((1 + t)/(1 − t))`.
  - `posterior` (TODO 4), the chance a respondent is a buyer given their answer.
  - `n_for_margin` (TODO 5), the sample-size planner.
- [`lab10-starter/responses.csv`](lab10-starter/responses.csv), an invented survey of 3,000 adult players split at random into two halves. Half answered "have you ever bought gold?" directly (`t = 1`). Half answered with randomized response at `t = 0.5`. [`gen_responses.py`](lab10-starter/gen_responses.py) regenerates it and documents the hidden truth, but do not read the parameters until step 4.
- [`lab10-starter/test_rr.py`](lab10-starter/test_rr.py), eight tests. All fail on the starter and pass on a correct solution. From inside `lab10-starter/`, run `python -m unittest test_rr.py` (from the repository root, `.venv/bin/python` is the course Python).
- The interactive [`examples/w10-randomized-response.html`](../examples/w10-randomized-response.html), once it is built.
- The application template in section 3 of the lecture.

## Steps

### Part A: the estimator (60 min)

1. Implement TODOs 1 to 5 until all eight tests pass. Then run `python rr.py` and paste the report into your results sheet.
2. Compare the two estimates. Which interval is narrower? Do the two intervals overlap? Write two sentences on what a reader who saw only the direct result would conclude.
3. Using `n_for_margin`, fill in this table for a planning value `π = 0.12`: the sample size for a ±2-point and a ±4-point margin at `t` = 1.0, 0.75, 0.5 and 0.25. Add a column with `epsilon(t)`.
4. Now open `gen_responses.py` and read the true share and the honesty rate. Compute the bias of the direct method and the root-mean-square error `sqrt(bias² + SE²)` of each method at `n = 1,500`. Which method is closer to the truth? At what sample size per arm would the direct method's RMSE equal that of randomized response if its bias stayed the same? (Hint: the direct RMSE can never fall below its bias.)
5. Write a 150-word paragraph for a studio producer who says "we'll just ask directly, it's cheaper." Use your numbers.

### Part B: the ethics application (60 min in the lab, then at home)

6. For your own course project, write an application with the sections from lecture section 3: summary and question; recruitment (with the exact recruitment text); consent (the five-sentence key information opening, then the full elements); any waiver you request, arguing each of the five criteria of §46.116(f)(3) separately; data management (what, where, who, pseudonymization, key destruction, deletion date); distress and incidental-findings protocol.
7. Classify your study's review level (not human-subjects research, exempt with the category, expedited, full board) and justify it with the regulation's wording. If you study in the UK or EU, also name the committee at your university that would review it.
8. Name one feature of your design that is both an ethical and a validity problem, and the change you made to fix both. If your project asks anything sensitive, say whether you considered randomized response or an item count and why you did or did not use it.

## Deliverable

- `rr.py` passing all eight tests.
- A results sheet (one page): the report from step 1, answers to steps 2 to 4 with the table from step 3, and the paragraph from step 5.
- The ethics application (1,500 to 2,500 words) with the classification from step 7 and the paragraph from step 8.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code (step 1) | All tests pass; report matches | Tests pass with minor output errors | Tests fail | 15 |
| Analysis (steps 2 to 5) | Correct table, bias and RMSE; crossover reasoning right; producer paragraph uses the numbers | Numbers mostly right, reasoning thin | Missing or wrong | 25 |
| Consent and recruitment | Key information first and complete; recruitment text neutral; minors screened; incentives justified | Present but one element missing or vague | Missing or misleading | 20 |
| Waivers and classification | Each criterion argued separately; review level correct with citation | Classification right but justification loose | Wrong level or waiver unargued | 15 |
| Data and distress protocols | Pseudonymization, key destruction and deletion dated; distress steps concrete; incidental-findings promise realistic | Present but generic | Missing | 15 |
| Double problem (step 8) | Real design flaw found and fixed on both sides | Named but fix addresses only one side | Missing | 10 |
| **Total** | | | | **100** |
