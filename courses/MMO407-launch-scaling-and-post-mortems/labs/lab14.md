# MMO407 · Lab 14: Readiness review and presentation dry run

**Week:** 14 ([lecture](../lectures/w14-presentations.md))
**Time:** 2 hours in the lab, plus time to revise your slides before your presentation slot.
**Work mode:** your launch plan group, reviewed by one other group.
**Counts toward:** the launch plan (50% of the course grade). The scorecard and the revised slides are part of your final submission.

## Objective

Implement the lecture's three ways of combining readiness criteria and a gate report, find the smallest changes that flip a verdict, score your own launch plan honestly, and run a timed dry run of your presentation in front of a peer panel that uses the same scorecard.

## Starter materials

- [`lab14-starter/readiness.py`](lab14-starter/readiness.py), Python 3, standard library only. It holds the lecture's scorecard (`LECTURE_CRITERIA`, weights and gates) and plans A, B and C (`LECTURE_PLANS`), with `score_of` and `verdict` done and four stubs:
  - `weighted_score` (TODO 1), `S = Σ wᵢ sᵢ / W`.
  - `geometric_score` (TODO 2), `G = Π sᵢ^(wᵢ/W)`.
  - `failed_gates` (TODO 3), in scorecard order.
  - `smallest_fix` (TODO 4), the smallest total score increase that turns a plan into "go" under the gated rule.
- [`lab14-starter/test_readiness.py`](lab14-starter/test_readiness.py), eight tests. All fail on the starter and pass on a correct solution. Run them from inside `lab14-starter/` with `python -m unittest test_readiness.py` (from the repository root, use `.venv/bin/python`).
- `python readiness.py` prints the lecture's three-plan table once TODOs 1 to 3 are done.
- The interactive `examples/w14-readiness-gates.html`, once it is built.
- Your launch plan draft and the lab 13 register.

## Steps

### Part A: the scoring rules (35 min)

1. Implement TODOs 1 to 3 and run the tests. `python readiness.py` must print the lecture's table: A at 0.917, 0.000 and a failed low-end gate; B at 0.850; C at 0.867 and 0.863.
2. For plan A, sweep the low-end platform score from 0 to 1 in steps of 0.05 and plot `S`, `G` and the gated verdict on one chart. Mark the score at which each rule first says "go". Explain in two sentences why the geometric rule says "go" long before the gate does.
3. Keep plan A's scores and sweep the low-end weight from 0 to 6. At which weight does the weighted average first fall below 0.8? Check your answer against `1 − wₖ/W`.

### Part B: what would flip the verdict? (25 min)

4. Implement `smallest_fix` (TODO 4) and run all tests.
5. Build three invented plans of your own, each designed so that exactly two of the three rules agree. For each, report `S`, `G`, the failed gates, all three verdicts and the smallest fix.
6. The panel proposes one change to the lecture scorecard: gate beta exposure at 0.5. Which of plans A, B and C change verdict? Write two sentences on whether that gate is justified by week 3's argument.

### Part C: your own plan (30 min)

7. Build your group's scorecard. Keep the six lecture criteria, add at least two for your game (for example, a platform you sell on, or a region you open), and decide which are gates. For every gate, write one line linking it to a risk above your week 13 disaster line.
8. Score your plan with a measured value and one line of evidence per criterion. Anything without evidence is `None`. Report all three verdicts and the smallest fix.
9. If your plan is "no-go" under the gated rule, either do the fix (and update the evidence) or change your recommendation to "go with conditions" and write each condition as a week 13 trigger.

### Part D: dry run (30 min)

10. Present to the other group in 12 minutes, following the order in lecture section 3, then take 8 minutes of questions. Time it.
11. The reviewing group scores your plan on your own scorecard without seeing your scores, and asks at least one gate, one tail and one transfer question. Record the questions and your answers.
12. Compare the two sets of scores. For every criterion where they differ by more than 0.2, write one line on which evidence explains the difference and what you will change on the slide.

## Deliverable

- `readiness.py` passing all eight tests, plus your code and plots for steps 2 to 9.
- Your scorecard with weights, gates, scores and evidence lines (step 7 and 8), and your verdict under all three rules.
- A one-page dry-run report: the timing, the reviewers' scores next to yours, the questions asked with your answers, and the list of slide changes from step 12.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Scoring rules (steps 1 to 3) | Tests pass; sweep plot with all three thresholds marked and explained; weight sweep checked against `1 − wₖ/W` | Tests pass; plots or explanation incomplete | Tests fail | 20 |
| Verdict flips (steps 4 to 6) | Tests pass; three plans that split the rules as asked; beta-gate question answered with a reason | Plans present but do not split the rules as asked | Tests fail | 20 |
| Own scorecard (steps 7 to 9) | Every gate tied to a disaster-line risk; measured scores with evidence; no-evidence rows scored 0; no-go handled by a fix or triggered conditions | Scores present, evidence or gate reasoning thin | Missing | 30 |
| Dry run (steps 10 to 12) | Timed run; reviewer scores recorded blind; all three question types answered; concrete slide changes | Dry run done, report thin | Missing | 25 |
| Code quality | Readable, runs first time | Runs with minor fixes | Does not run | 5 |
| **Total** | | | | **100** |
