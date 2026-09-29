# PR201 · Lab 01: Team charter, skill matrix and pitch fit

**Week:** 1 · **Time:** the last hour of the studio session plus about 3 hours as a team · **Weight:** part of [milestone 1, pitch and pre-production](../assessments/m1-pitch-and-preproduction-brief.md) (marked with lab 02)

## Objective

Form a team that covers every discipline with a primary and a backup, and show with numbers that your chosen pitch fits that team. You finish with a pitch whose largest discipline load is at or below 1, and a written record of every change you made to get there. The model is in section 2 of the [week 1 guide](../lectures/w01-pitch-and-team-formation.md).

## Starter materials

Folder `lab01-starter/`. Standard library Python only. Use the course interpreter (`.venv/bin/python` at the repository root) or any Python 3.10 or later.

- `team.csv`: one row per member with `member`, `hours_per_week`, `primary` and `backup`. Disciplines are `code`, `design`, `art`, `audio` and `production`. The starter holds the six-person *Hollowmarch* team.
- `pitch_demand.csv`: hours the pitch needs from each discipline. The starter holds the *Hollowmarch* pitch before its art fix.
- `check_fit.py`: prints supply, demand and load per discipline, checks primaries and backups, and ends with `PASS` or `NOT READY`. Options `--weeks`, `--c` and `--buffer` default to 11, 0.25 and 0.3.
- The team charter questions in [PR101 week 1](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w01-roles-on-a-game-team.md), section 5.

## Steps

1. **Reproduce the guide.** Run `python check_fit.py team.csv pitch_demand.csv`. Confirm the art load of 1.35 and the total of 0.85. Change art to 48 and confirm `PASS` with a largest load of 0.92.
2. **Skill matrix.** In a separate sheet, each member rates themselves 0 to 3 in the five disciplines. Assign a primary and a different backup for every discipline from the ratings. Record wishes in a separate column.
3. **Your team file.** Replace the starter `team.csv` with your team. Use each person's honest weekly hours outside the studio session.
4. **Your demand.** For your chosen pitch, each discipline's primary estimates that discipline's hours for the whole slice. Fifteen minutes, rough numbers, no one estimates another discipline.
5. **Run the check.** If it prints `NOT READY`, find the largest load and apply one of the three moves from the guide (cut, move, add supply). Rerun. Repeat until `PASS`.
6. **Record decisions.** For each change, write one line in `decisions.md`: what changed, the hours before and after, and what it now rules out for the design.
7. **Stress test.** Rerun with `--buffer 0.45`. Report the largest load. If it is above 1.1, name the task you would cut first.
8. **Charter.** Write the one-page charter, adding the build owner and the product owner.

## Deliverable

In `docs/` of your team repository: `team.csv`, `pitch_demand.csv`, the checker output from step 5 (pasted into `fit.md`) and from step 7, `decisions.md`, the skill matrix, the charter and the pitch one-pager. The instructor reruns `check_fit.py` on your files.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Coverage | Every discipline has a primary and a different backup, justified from the skill matrix | Coverage complete, matrix thin | A discipline without primary or backup | 20% |
| Fit | `check_fit.py` passes on submitted files; demand estimated by each discipline's primary | Passes, but estimates by one person | Does not pass | 30% |
| Decisions | Every change recorded with before and after hours and its design consequence | Changes listed without consequences | No record | 20% |
| Stress test | Buffer 0.45 result reported and a first cut named | Result reported, no cut | Missing | 10% |
| Charter and pitch | Charter answers every question with specific rules; pitch names a moment of interdependence | Charter generic or "why together" vague | Missing | 20% |
