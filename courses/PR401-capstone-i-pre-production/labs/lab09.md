# PR401 Lab 09: Content inventory and yield plan

**Week:** 9 (Content plan). **Guide:** [week 9](../lectures/w09-content-plan.md). **Team lab**, submitted once per team.

## Objective

Choose the content your team will build with numbers a reviewer can rerun. You will list every candidate content unit with its measured cost, first-pass length, replay multiplier and evidence, fill the content budget with must-haves first and the rest by yield, compute the median player's drought, and find the one replay claim the plan depends on most.

## Starter materials

In [`labs/lab09-starter/`](lab09-starter/):

- `content_yield.py`. Standard library only. Run `python content_yield.py content.csv params.csv`. It lists every unit by yield, marks the included ones, prints spent hours, `Σ E`, the median drought in days, and the drought if the included assumed unit with the largest `E` has its `r` halved. It checks budget, must-haves, yield order and your declared values, then prints `PASS` or `NOT READY`.
- `content.csv`. *Emberfall*'s six candidate units from the guide, with the first-pass plan (dungeon at 60 hours, `r = 10`).
- `params.csv`. Budget, median weekly hours and live weeks, with the declared values blank.

An excluded unit that outranks an included optional unit, or that still fits the budget, needs a `note` explaining why (for example "held for the PR402 patch week").

## Steps

1. **Warm-up (15 minutes).** Apply the guide's final plan to the starter: dungeon at 70 hours with `r = 14`, the ash-storm event held for the patch week, and a note on the rumour quests. Fill the four declared values. Run until the checker prints `PASS`.
2. **Measured `k`.** For each content type in your prototypes, divide team hours by the median tester first-pass time. Record hours, play time and tester count in `docs/content-plan.md`.
3. **Inventory.** Replace `content.csv` with every candidate unit. Cost units the way they will ship, including art and test. Use tester medians for `first_pass_h`. Every unit needs evidence or the word `assumed`.
4. **Budget.** Set `budget_h` to the estimated hours your production plan gives content (estimates, not actuals; the plan ratio is applied in week 11). Set weekly hours and weeks from your week 1 median player.
5. **Fill.** Include must-haves, then units in descending yield until the next one does not fit. Every departure from yield order gets a note.
6. **Sensitivity.** Read the checker's sensitivity line. Name the unit in `sensitivity_unit`, declare the drought, and write the vertical slice sprint 1 test that will measure its `r` (who plays, how long, what counts as a repeat).
7. **Calendar.** Place every included unit in a sprint in `docs/content-plan.md`, with dependencies, and name the unit held for the patch week.

## Deliverable

In `preproduction/week09/` and `docs/content-plan.md` in the team repository:

- `content.csv`, `params.csv` and the checker output saved as `check-output.txt`.
- `docs/content-plan.md` with the measured `k` table, the sensitivity test and the calendar.

**Checkable output:** the instructor reruns `content_yield.py` on your two files. It must print `PASS` and exit with code 0.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun; saved output matches |
| Measured `k` | 4 | Every prototyped content type measured from real hours and tester medians |
| Inventory | 4 | All candidates listed, costed as shipped, with honest evidence labels |
| Selection | 3 | Must-haves in; yield order followed or departures explained |
| Sensitivity test | 3 | Load-bearing claim named; its test is specific and scheduled in sprint 1 |
| Calendar | 2 | Every unit in a sprint with dependencies; one unit held for the patch week |
