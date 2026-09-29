# PR402 Lab 14: Post-mortem evidence workbook

**Week:** 14 (Post-mortem). **Guide:** [week 14](../lectures/w14-post-mortem.md). **Team lab**, submitted once per team.

## Objective

Build the evidence base for your post-mortem before anyone writes a paragraph of it. You will compute your estimate ratio and commitment rate for every sprint and the patch, check the week-12 forecast, build the two plan-against-actual tables, and compute lesson recurrence against your PR401 review. The post-mortem document then cites this workbook line by line.

## Starter materials

- Your sprint boards, labs 11 to 13, the patch release record, incident postmortems, and the PR401 production plan and pre-production review.
- The script in section 3 of the guide. Save an adapted copy as `production/postmortem/sprints.py` that reads `production/postmortem/sprints.csv` (columns `sprint,kind,estimated_h,actual_h,committed,delivered`, where `kind` is `feature` or `live`) and prints the Part A table, the ratio for each kind, and the forecast check.
- Copy this template into `production/postmortem/lab14.md`:

```markdown
## Part A. Sprints and forecast
(paste the output of sprints.py)
Ratio for feature work: __   Ratio for live work: __
Week-12 forecast: predicted __ h with R = __; actual __ h; error __ %
Claim about planning, in one or two sentences, citing rows: __
Sample-size caveat: __

## Part B. Plan against actual
| Milestone | Planned week (PR401) | Actual week | Reason for any slip |
|---|---|---|---|

| Feature or item | In PR401 plan? | Shipped at launch / in patch / cut | Note |
|---|---|---|---|
Planned: __  Shipped: __ (__ %)  Cut: __  Unplanned shipped: __ (of which ops tooling or live fixes: __)

## Part C. Recurrence
PR401 categories C1: __
Action items (category, change, closed yes/no, evidence): __
This project's categories C2: __
Recurrence R = |C1 ∩ C2| / |C1| = __   Closure = __
For each recurring category, one sentence on why it came back: __

## Part D. Lessons and action items
| Lesson | Evidence (Part and row) | Owner | Change | Check |
|---|---|---|---|---|
```

## Steps

1. **Warm-up (10 minutes).** Put the Emberfall rows from the guide into `sprints.csv` and confirm the script prints `r = 1.296` and `q = 75%` for sprint 3 and a forecast error of `-5.1%`. Replace them with your data.
2. **Part A.** Fill `sprints.csv` from the boards. Count only items committed at sprint planning. Tag the patch, and any other live-work sprint, as `live`. Write the planning claim only after the table exists, and add the caveat.
3. **Part B.** Start from the PR401 production plan, not from memory. List every unplanned item that shipped, and mark which were operations tooling or live fixes.
4. **Part C.** Code both "what went wrong" lists with the same categories (PR101 week 14). Compute recurrence and closure. Explain every recurring category, including any that recurred after its action item closed.
5. **Part D.** Write at most six lessons. Each cites a Part and row. Each action item has one owner, one change and one check.
6. **Pair critique.** Swap Part D with another team. For each lesson they write what would have to be true for it to be wrong. Keep their notes in the file and answer them.

## Deliverable

`production/postmortem/lab14.md`, `sprints.csv`, `sprints.py` and its saved output `sprints-output.txt`. The post-mortem document is submitted separately under its assessment brief and must cite this workbook.

**Checkable output:** the instructor runs `.venv/bin/python production/postmortem/sprints.py`. Its output must match `sprints-output.txt` and Part A. Counts in Part B must match the rows of its tables, and `R` and closure in Part C must follow from the listed categories.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Sprint table and script | 5 | Script runs; every sprint and the patch present; feature and live ratios separated; forecast error correct |
| Planning claim | 2 | Cites rows, uses both `r` and `q`, states the sample-size caveat |
| Plan against actual | 5 | Both tables start from the PR401 plan; counts correct; unplanned items listed and classified |
| Recurrence | 4 | Same categories used for both lists; `R` and closure correct; every recurring item explained |
| Lessons and critique | 4 | Six or fewer lessons, each with evidence, owner, change and check; the other team's critique answered |
