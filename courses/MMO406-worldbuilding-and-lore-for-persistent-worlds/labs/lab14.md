# MMO406 · Lab 14: The question test

**Week:** 14, bible workshop ([lecture](../lectures/w14-bible-workshop.md), [interactive](../examples/w14-lore-desk.html)).
**Time:** 2 hours in lab, plus about 4 hours at home.
**Weight:** the last of the exercises (40%). The revision you make here is the final check before you submit the world bible (60%) in week 15.

## Objective

Implement the lore desk model and a scorer for question logs, and run them on a *Thornmere* log. Then run two question tests on your own bible with a revision in between, and show with numbers whether the revision moved your bible out of the "never clears" region for a realistic team, and whether it would survive the team doubling for an expansion.

## Starter materials

All in [`lab14-starter/`](lab14-starter/). Standard-library Python, run with `.venv/bin/python`.

- [`lore_desk.py`](lab14-starter/lore_desk.py) has the model in its docstring, a working `load_log`, and six empty functions: `escalated_rate`, `wait_days`, `min_answer_rate`, `answer_rate_for_wait`, `score_questions` and `gap_ranking`. It also has a `report` function and a command line with `--lam` and `--mu` options. As shipped it prints a TODO and exits with status 1.
- [`thornmere_questions.csv`](lab14-starter/thornmere_questions.csv) is a question test of the *Thornmere* bible: 40 questions from two askers, each tagged with the chapter it concerns and one of the five statuses from lecture section 3.
- [`test_lore_desk.py`](lab14-starter/test_lore_desk.py) holds six tests. They check the lecture's wait table, the expansion table, the thresholds and edge cases, the scoring of the Thornmere log, input validation and the gap ranking.

### The question log format

```
id,asker,chapter,question,status
Q05,asker1,history,When were the Tidewardens founded?,contradicted
```

`status` is one of `answered`, `derivable`, `missing`, `contradicted` or `reserved`. `chapter` uses the chapter names of your bible. Use pseudonyms like `asker1` for askers, not names.

Run the tests and the report from the repository root:

```
.venv/bin/python courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab14-starter/test_lore_desk.py
.venv/bin/python courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab14-starter/lore_desk.py courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab14-starter/thornmere_questions.csv --lam 48 --mu 20
```

On the starter all six tests report `TODO` and the script exits with status 1.

## Steps

1. **The desk (20 min).** Implement `escalated_rate`, `wait_days`, `min_answer_rate` and `answer_rate_for_wait` from the lecture's formulas. `wait_days` returns `math.inf` when the escalated rate is at least `μ`. `answer_rate_for_wait` returns `None` when even a perfect bible can't reach the target (the lead's capacity alone is too small) and never returns less than 0. The first three tests pass.
2. **The scorer (25 min).** Implement `score_questions` (counts for all five statuses, `a` and its 95% margin) and `gap_ranking` (score `missing + 2 × contradicted` per chapter, only chapters above zero, highest first, ties alphabetical). Raise `ValueError` for an unknown status or an empty log. Run the tests until all six pass.
3. **Read the Thornmere report (15 min).** Run the report with `--lam 48 --mu 20`, then with `--lam 96`. Answer in writing: is the Thornmere bible stable for 12 writers? Can you be sure, given the margin? Which chapter do you fix first, and which single question in it would you fix first? What happens when the team doubles?
4. **First test of your bible (in class, 40 min).** Run the workshop's first pass (lecture section 4) in your group. Collect at least 30 questions from at least two askers who have not read your bible, each working from a writing task you give them. Classify every question with the askers watching and record the log as `test1.csv`.
5. **Revise (at home, 2 hours).** Fix the chapters at the top of your gap ranking. For each fix, record the fact ids you added or changed and add them to your lab 11 canon graph, then run its `validate`. Run the consistency pass from lecture section 4 (tension ledger, timeline, canon graph, names) and fix what it finds. Write the one-page front, the reserved list and the change log.
6. **Second test (at home, 45 min).** Recruit two new askers (classmates from another group, or anyone who hasn't seen your world), give them a different writing task, and collect at least 30 new questions. Do not reuse test 1's questions. Record `test2.csv`.
7. **Decide (30 min).** Assume a launch team of 12 writers at 4 questions a week and a lead at 20 a week, and an expansion team of 24. Run both logs for both teams. Write the verdict in one paragraph: for which team is your bible stable, taking the margin into account, and what would you do next with one more week?

## Deliverable

A zip or repository link containing:

- `lore_desk.py` with all six tests passing (paste the test output into the report).
- `test1.csv` and `test2.csv`.
- `lab14.md`, 800 to 1,200 words, with: the step 3 answers; a table of both tests (questions, counts by status, `a`, margin, gap ranking); a list of the revisions with their fact ids; the four desk results from step 7 (two logs, two team sizes); and the verdict paragraph.
- The revised bible, with its one-page front, reserved list and change log.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Model correctness | All six tests pass; infinity, `None` and validation handled as specified | Four or five pass | Three or fewer | 20% |
| Reading the Thornmere report | Stability judged against the margin, not the point estimate; first fix named with a reason; expansion result explained | Numbers right, judgment thin | Report pasted without reading | 10% |
| Test design | Two tests of 30+ questions each, fresh askers and fresh questions for test 2, realistic writing tasks, honest classification | Tests run but small, or test 2 reuses askers | One test, or questions written by the author | 20% |
| Revision | Fixes follow the gap ranking; every fix has fact ids in the canon graph; consistency pass run and its findings fixed; front, reserved list and change log present | Fixes made, traceability partial | Cosmetic changes only | 30% |
| Verdict | Four desk results computed; conclusion uses both `a_min` and the margin; next step follows from the numbers | Results computed, conclusion ignores the margin | Missing or unsupported | 20% |

<details>
<summary>Instructor check values</summary>

- Lecture table (`λ = 48`, `μ = 20`): wait in days 6.25, 1.56, 0.89, 0.48, 0.39, 0.33 at `a` = 60%, 65%, 70%, 80%, 85%, 90%; never clears at 55% and below. `a_min = 58.3%`; one-day wait needs 68.75%.
- Expansion (`λ = 96`): never clears at 70%; 0.89 days at 85%; `a_min = 79.2%`; one-day wait needs 84.4%.
- Thornmere log: 40 questions; answered 20, derivable 6, missing 8, contradicted 3, reserved 3; `a = 65.0%`, margin 14.8 points (50.2% to 79.8%). Gap ranking: religion 5, factions 3, history 3, geography 2, community 1. For 12 writers: 1.56 days at the estimate, never clears at the low end, 0.49 days at the high end. For 24 writers: never clears at the estimate; 8.47 days even at the high end.
- Good step 3 answers: the point estimate is stable, but the low end of the margin is below `a_min`, so one test can't show stability. Fix religion first, because its two contradictions (whether the Drowned King is a god; whether the gods caused the Drowning) mislead writers who don't know to ask; the Tidewardens' founding date (Q05) is the week 11 conflict between the core fact and the tie-in, which the tier rule already settles, so the fix is to state the winner in the history chapter. The three reserved questions are the week 10 hooks and should stay reserved.
- Watch for: students reusing test 1's questions in test 2 (the rise in `a` then measures memory, not the bible); authors classifying generously (a "derivable" answer must follow from a stated rule without judgment); reserved lists that have grown to hide missing answers.

</details>
