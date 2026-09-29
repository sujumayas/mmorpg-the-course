# PR301 Lab 03: Sprint 1 plan with per-person loads

**Week:** 3 (Sprint 1: world server and login). **Guide:** [week 3](../lectures/w03-sprint-1-world-server-and-login.md). **Team lab**, submitted once per team. Reused in week 5 for the sprint 2 plan.

## Objective

Produce a sprint plan that every person on the team can finish. You will estimate the sprint 1 stories, compute each person's capacity from a focus factor, find the people whose load is above 1, and reshape the plan with the four moves from the guide (narrow the goal, move, stub, mob) until the checker passes.

## Starter materials

In [`labs/lab03-starter/`](lab03-starter/):

- `check_sprint.py`. Standard library only. Run it with `.venv/bin/python check_sprint.py team.csv sprint.csv`. Options: `--focus` (default 0.62), `--weeks` (2), `--c` (0.25), `--studio` (3 hours of mob work allowed) and `--cross` (1.5). It prints each person's capacity, charged hours and load, lists every problem, then `PASS` or `NOT READY`.
- `team.csv`. The seven *Saltmarsh* members: `name`, `primary`, `hours_per_week`.
- `sprint.csv`. The *Saltmarsh* first draft from the guide. Columns: `id`, `story`, `discipline`, `owner`, `est_hours`, `deps` (IDs separated by spaces), `goal` (`y` if the sprint goal needs it), `status` (`committed`, `stretch`, `studio`, `later` or `done`).

## Steps

1. **Warm-up (15 minutes).** Run the checker on the starter files and confirm Ana 1.61, Ben 2.36 and Chen 1.86. Apply the four moves from guide section 2 (S5 and S13 to `later`; S8 to Dee and S9 to Gus; S3 at 3 hours with a new `later` story S14 for full authentication; S1 to `studio`; S7 to Ben). Confirm `PASS` at a team load of 0.90.
2. **Your team.** Replace `team.csv`. Use your PR201 median focus factor for `--focus` and record how you computed it.
3. **Your stories.** Write every story the sprint 1 proof needs, with the owner's estimate and its dependencies. Mark `goal` honestly.
4. **Run and reshape.** Apply the moves in order of cost. Every stub gets a `later` story with an owner.
5. **Drop order.** For everyone at a load of 0.95 or more, name which story drops first if they lose a day. Put the drop order at the top of the sprint board.
6. **Week 5 reuse.** For sprint 2, rerun with `--focus` set to the value measured at the sprint 1 review (start of week 5).

## Deliverable

In `production/sprint1/` (and `production/sprint2/` in week 5):

- `team.csv`, `sprint.csv` and the checker output saved as `plan-output.txt`, with the `--focus` value used written at its top.
- `plan-notes.md` with the focus factor calculation, the moves applied and the drop order.

**Checkable output:** the instructor reruns `check_sprint.py` with your stated `--focus`. It must print `PASS` and exit with code 0.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun with the stated focus factor; output file matches |
| Goal chain | 4 | Every story the sprint 1 proof needs is marked `goal` and is committed or studio |
| Estimates and owners | 3 | Each estimate made by the story's owner; cross-discipline stories charged at the factor |
| Stubs | 3 | Every stub has a `later` story with an owner and target sprint |
| Drop order | 3 | Named for everyone at 0.95 or more |
| Focus factor | 3 | Computed from PR201 records (week 3) or the sprint 1 review measurement (week 5), with inputs shown |
