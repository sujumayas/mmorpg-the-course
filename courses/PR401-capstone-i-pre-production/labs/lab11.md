# PR401 Lab 11: Capacity and load per discipline

**Week:** 11 (Production plan). **Guide:** [week 11](../lectures/w11-production-plan.md). **Team lab**, submitted once per team.

## Objective

Turn your technical design, content plan and social systems plan into a staffed backlog for PR402, and prove that each discipline can do its share by each milestone. The checker computes capacity and cumulative load per discipline, finds the constraint and flags dependencies that point forwards in time.

## Starter materials

In [`labs/lab11-starter/`](lab11-starter/):

- `check_plan.py`. Standard library only. Run it with `.venv/bin/python check_plan.py team.csv backlog.csv`. It prints capacity and cumulative load at each milestone for every discipline, the team load (for comparison only), the constraint, then `PASS` or `NOT READY`. It exits with code 1 when anything fails.
- `team.csv`. The *Emberfall* team from the guide: four disciplines, seven people, 12 h a week in PR402, focus factor 0.75 and plan ratio 1.30 from week 6.
- `backlog.csv`. Sixteen *Emberfall* items, in raw estimated hours, with one missing owner, one dependency that points forwards, and the art overload from the guide.

Milestones are `S1`, `S2` and `S3` (PR402 sprints in weeks 1, 2 and 3, all before alpha) and `S4` (weeks 4 to 8, alpha fixes through open beta). Capacity is `people × hours_per_week × weeks × focus_factor`. Demand is the raw estimate times `plan_ratio`. The checker tests **cumulative** load. Work due by `S2` must fit in the capacity of weeks 1 and 2 together, because work can be done early but not late. `absence_hours` is the total scheduled hours the discipline loses over the eight weeks; the checker applies the focus factor and spreads it evenly.

## Steps

1. **Warm-up (20 minutes).** Run the checker on the starter files and read the three problems. Then fix them the way the guide did. Give A3 to the artist. Let P2 run on stub recipes until D3 lands: remove its dependency and name the stub in `constraint-log.md`. Relieve art with the guide's two moves. Move 20 h of imports, LODs and VFX to the tech-art student (A2 from 30 to 20, A3 from 35 to 25, and a new row T3 of 30 h in `S4` that depends on T1). Buy the prop kit for the dungeon (A2 from 20 to 10, and a new art row A4 "Integrate licensed prop kit" of 2 h in `S3`). The checker must print `PASS` with art at 0.94 and audio and tech art at 0.90.
2. **Your team.** Replace `team.csv` with your own disciplines. Split a person who covers two disciplines as a fraction (0.5 and 0.5). Use hours from your team charter (12 in PR402 unless it says otherwise), the focus factor and plan ratio from your week 6 fit sheet, and absences you know about. Write the source of each number in `inputs.md`.
3. **Your backlog.** Merge your week 7, 9 and 10 estimates into `backlog.csv`. Every row has one discipline, a named owner, a milestone and its dependencies. Anything your alpha definition names must be in `S1` to `S3`.
4. **First run.** Save the checker output as `run-1.txt` before you change anything. This is the starting load table for the constraint log.
5. **Relieve the constraint.** Use move, buy, cut and reorder. For every move, record in `constraint-log.md` the hours changed, the conversion factor if work moved between disciplines, who pays, and the pillar it touches if it is a cut. Rerun after each move.
6. **Leave room.** If programming is above 0.90 at `S4`, move or cut until it is at 0.90 or below, so the post-alpha bug wave has somewhere to go. Explain your target in one sentence if you choose a different one.
7. **Final run** until the checker prints `PASS`. Save the output as `check-output.txt`.

## Deliverable

In `preproduction/week11/` in the team repository:

- `team.csv`, `backlog.csv`, `inputs.md`, `run-1.txt`, `constraint-log.md` and `check-output.txt`.
- `production-plan.md`, as described in the guide's Deliverables section, which references these files.

**Checkable output:** the instructor reruns `check_plan.py` on your `team.csv` and `backlog.csv`. It must print `PASS` and exit with code 0, and the output must match `check-output.txt`.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun, output file matches |
| Inputs sourced | 3 | Every capacity input cites the charter, the week 6 fit sheet or a marked assumption; `f` and `R` are the measured values |
| Backlog complete | 3 | Every item from weeks 7, 9 and 10 is present or explicitly cut; alpha items are in `S1` to `S3` |
| Constraint log | 5 | Starting table saved; each move states hours, conversion, who pays and any pillar touched; the log shows at least one constraint identified and relieved |
| Slack where it matters | 2 | Programming at or below 0.90 at `S4`, or a stated reason for another target |
| Dependencies | 3 | No forward dependencies; at least one long cross-discipline chain broken with a stub, and the stub named |
