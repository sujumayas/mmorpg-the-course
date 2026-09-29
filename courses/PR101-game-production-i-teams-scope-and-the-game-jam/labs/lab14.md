# PR101 · Lab 14: Coding post-mortems and closing the loop

**Week:** 14, post-mortems as a practice ([lecture](../lectures/w14-post-mortems-as-a-practice.md)).
**Time:** 2 hours in lab, plus up to 2 hours with your team before week 15.
**Weight:** feeds the final post-mortem (20%). The coded data, Pareto tables and action items from this lab are required sections of that post-mortem.

## Objective

Finish a small tool that turns coded post-mortem problems into Pareto tables, a recurrence rate and an action-item closure rate. Check it against the published counts from Politowski and colleagues, then code your own team's jam and final-project problems with two independent coders, and write action items that someone can check. By the end you can say, with your team's own numbers, which lessons from the jam stuck and which came back.

## Starter materials

All in [`lab14-starter/`](lab14-starter/). Standard-library Python 3.10 or later, no packages. From the repository root the course uses `.venv/bin/python`.

- [`postmortem_tools.py`](lab14-starter/postmortem_tools.py). The CSV loaders and the `report` function are complete. `count_by_category`, `pareto`, `vital_few`, `recurrence` and `closure` are stubs with docstrings that state the rule. Run `python postmortem_tools.py`. On the starter the tables have zero shares, `k_80` is the number of categories, and recurrence is 0%.
- [`politowski_types.csv`](lab14-starter/politowski_types.csv). The 20 problem types and counts from the paper's Figure 3b (927 problems from 200 post-mortems, 1997 to 2019).
- [`example_team.csv`](lab14-starter/example_team.csv). The invented team from lecture section 4: six jam problems with action items, five final-project problems. One row per problem with columns `project, category, problem, action_item, owner, done`.
- [`test_lab14.py`](lab14-starter/test_lab14.py). Six tests. Run `python test_lab14.py`. On the starter it reports `0/6 tests passed`.

## Steps

1. **Run everything first.** Run the tool and the tests. Look at the stubbed Pareto table for the 20 types and write down, before coding anything, what `k_80` you expect from the lecture.
2. **Count and sort.** Implement `count_by_category` and `pareto`. Watch the tie rule. `bugs` and `scope` both have 34 and must appear in alphabetical order. Check your first four rows against the lecture table (12.5%, 24.6%, 33.7%, 41.6% cumulative).
3. **The vital few.** Implement `vital_few` with a small tolerance, so that a cumulative share of exactly 80% counts. The lecture's example team reaches exactly 80.0% at `k = 4`, and if you add up shares instead of counts, floating-point rounding can land a hair below it.
4. **Recurrence and closure.** Implement `recurrence` and `closure`. Run `python postmortem_tools.py` and confirm the example team gives `R = 40%`, repeated `['communication', 'planning']`, and 60% of jam action items closed. Run the tests until you see `6/6 tests passed`.
5. **Code your own problems, twice.** Two people on your team each take your week 9 jam post-mortem and your sprint retrospective notes from the final project, and separately code every problem into one of Politowski's 20 types. Record your **percent agreement** (matching items divided by all items) before discussing. Then agree on one type per item.
6. **Build your team's file.** Put the agreed coding in `my_team.csv`, same columns as the example. For the jam rows, fill in the action items you actually wrote in week 9 and whether they were done. Be honest: an item nobody did is `no`.
7. **Run it.** Run `python postmortem_tools.py my_team.csv`. Record both Pareto tables, both `k_80` values, `R` and the jam closure rate.
8. **Open your biggest bucket.** For your team's top category in the final project, list its problems and give each a narrower root cause of your own (for example, "planning" into "art estimates" and "save-system estimates"). Rerun with the split categories and note what happens to the top of the chart.
9. **Write the next action items.** For each category in the final project (not only the top one), write at most one action item with an owner, a change and a check, as in lecture section 4. Any problem that escaped into a release also gets a new line in your week 13 `RELEASE_CHECKLIST.md`.

## Deliverable

- Your edited `postmortem_tools.py` with `python test_lab14.py` reporting `6/6 tests passed` (individual).
- Team: `my_team.csv` committed in your repository.
- Team: a note of at most 500 words with your percent agreement from step 5 and the category you disagreed on most; both Pareto tables and `k_80` values; `R` and the closure rate with two sentences interpreting them (remember the sample is tiny); the step 8 split and what it changed; and the step 9 action items as a table (category, action, owner, check).
- This note becomes the "lessons and next steps" section of your week 15 post-mortem.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Tests pass | 6/6 | 4-5 | 3 or fewer | 20% |
| Coding quality | Two independent coders, agreement reported before discussion, disagreements resolved and explained | Coded by one person, or agreement not reported | Categories inconsistent or missing | 20% |
| Numbers and interpretation | Both Pareto tables, `k_80`, `R` and closure rate correct, with a sentence on sample size | Numbers correct, interpretation thin | Numbers wrong or missing | 20% |
| Opening the bucket (step 8) | Top category split into root causes, rerun, and the change in the chart explained | Split done without rerun or explanation | Missing | 15% |
| Action items | Every final-project category has one action item with owner, change and check; blameless wording; checklist updated | Most items checkable | Vague items ("communicate better") or blame | 25% |
