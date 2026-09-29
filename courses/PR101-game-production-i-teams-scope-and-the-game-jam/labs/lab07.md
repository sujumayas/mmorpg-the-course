# PR101 · Lab 07: A board that tells the truth

**Week:** 7 ([Task tracking and definitions of done](../lectures/w07-task-tracking-and-definitions-of-done.md))
**Time:** one 2-hour lab session plus about 1 hour at home
**Work:** in your jam teams

## Objective

Build the task board your team will use in the jam next week. By the end you have a card list split into tasks of four person-hours or less, each with acceptance criteria someone else can check; a written definition of done; a WIP limit you can justify with the lecture's model; and the first rows of the jam log that lab 08 fills and lab 09 analyses. A checker script tells you when the list and the DoD meet the minimum standard.

## Starter materials

- Python 3.10 or later, standard library only. In this repository use `.venv/bin/python`.
- [`lab07-starter/check_board.py`](lab07-starter/check_board.py). It reads a task CSV and a DoD file, reports the hours per tier, and fails if any card is larger than 4 person-hours, lacks a checkable acceptance sentence, has a duplicate ID or an unknown tier, if the DoD has fewer than four checklist items, or if the WIP limit is above people + 1. With `--seed` it writes the hour-0 rows of your jam log.
- [`lab07-starter/tasks_template.csv`](lab07-starter/tasks_template.csv): an eight-card example with columns `task, tier, estimate_hours, owner, acceptance`. Tiers are `must`, `should`, `could` (MVP, slice, polish in week 4's terms).
- [`lab07-starter/dod_template.md`](lab07-starter/dod_template.md): the five-item jam DoD from the lecture, as a Markdown checklist.
- Your team's week 4 scope sheet (lab 04) and one-pager.
- The interactive [`examples/w07-wip-limit.html`](../examples/w07-wip-limit.html).
- A board: sticky notes on a wall, a shared spreadsheet, or a tracker such as GitHub Projects. Choose one.

From the `lab07-starter` folder, this runs the checker on the templates and passes:

```
python check_board.py tasks_template.csv dod_template.md --people 4 --wip 4
```

## Steps

### Part A: split (45 minutes)

1. Take your week 4 task list. Mark every task estimated above 4 person-hours.
2. Split each marked task with the three tests from lecture section 1: at most four person-hours, a visible change in a build, checkable by someone else. Keep the tier of the parent task unless a slice can move lower. Record which parent each new card came from.
3. Write one acceptance sentence per card, in the form "In a build, [observable result] when [player action or condition]." Avoid "works", "feels good" and "is done".
4. Save the list as `tasks.csv` in the template's format. Give every card a unique ID (`T01`, `T02`, ...) and one owner.
5. Run `check_board.py` on it with your team size. Fix every problem it reports.

### Part B: define done and set the limit (35 minutes)

6. Copy `dod_template.md` to `dod.md` and edit it for your engine and your team. Delete items that don't apply. Add at least one item that comes from something that went wrong in your lab 02, 03 or 05 work, and write that incident in one sentence as a comment under the item.
7. Open the interactive. Enter your team size, your number of must and should cards, and their average estimate. Set the playtest at hour 12 (week 4's first cut trigger). Record how many cards are done at hour 12 with no limit, with `w = n` and with `w = n + 1`, at `c = 0` and `c = 0.1`.
8. Choose your WIP limit. Write two sentences: why this number, and what the team does when Doing is full.
9. Run the checker with your `--wip`. It must pass.

### Part C: the board and the log (40 minutes)

10. Put every card on your board in To do. Write the DoD at the top of the Done column. Write the WIP limit on the Doing column.
11. Run the checker with `--seed ../jam_log.csv --team <your team code>` to write the hour-0 rows of your jam log. Open the file and confirm one row per card with `spent = 0` and `remaining_est` equal to the estimate.
12. Commit `tasks.csv`, `dod.md` and `jam_log.csv` to your team repository. Tag the commit `jam-plan`.
13. Swap boards with another team for 10 minutes. They pick the three cards whose acceptance sentences they could not check without asking you. Rewrite those three and rerun the checker.

### Part D: at home

14. Each person answers, in no more than 150 words: which card on the board are you least sure about, what could make it take twice its estimate, and what would you do at the hour-12 checkpoint if it had?

## Deliverable

A link to your team repository at the `jam-plan` tag, containing `tasks.csv`, `dod.md` and `jam_log.csv`, all passing `check_board.py`; a photo or screenshot of the board; a one-page PDF with the numbers from step 7, the WIP justification from step 8, the before-and-after of the three rewritten cards from step 13, and each person's answer to step 14.

## Rubric

| Criterion | Excellent (4) | Good (3) | Partial (2) | Missing (0-1) |
|---|---|---|---|---|
| Task splitting (30%) | Every card passes all three tests; parents recorded; splits are vertical (each card visible in a build) | All cards pass the checker; a few splits are horizontal (code-only layers) | Checker passes only after the swap step; several cards not visible in a build | Checker fails |
| Acceptance criteria (25%) | Every sentence is observable and specific; swap step found at most one unclear card | Most sentences checkable; swap found two or three | Many sentences restate the title | Missing or not checkable |
| Definition of done (20%) | Fits the engine and team; includes an item traced to a real past incident; checkable in two minutes per card | Sensible, mostly the template | Template copied unchanged | Fewer than four items |
| WIP limit (15%) | Justified with the step 7 numbers, including switching cost and blocked cards | Justified with numbers, one factor missing | Stated without numbers | Missing |
| Log and repository (10%) | Seeded log matches the card list; tagged commit contains all three files | Minor mismatch | Log missing or untagged | Nothing committed |
