# PR301 Lab 01: Persistent-world pitch budget

**Week:** 1 (Pitch and world pillars). **Guide:** [week 1](../lectures/w01-pitch-and-world-pillars.md). **Team lab**, submitted once per team.

## Objective

Decide which world your team can afford to build. You will estimate the platform, system and authored-content costs of two or three pitches, compute each pitch's load against your team's supply, find the break-even play time between them, and change the chosen pitch until its load is at or below 0.9. Each change becomes a written design constraint.

## Starter materials

In [`labs/lab01-starter/`](lab01-starter/):

- `check_budget.py`. Standard library only. Run it with `.venv/bin/python check_budget.py pitches.csv`. Options set the team: `--n`, `--hours`, `--c`, `--weeks`, `--buffer` and `--margin` (defaults 7, 8, 0.25, 12, 0.3 and 0.9). It prints supply, each pitch's authored hours, demand and load, the break-even play time for each pair, then `PASS` or `NOT READY`, and exits with code 1 when no pitch passes.
- `pitches.csv`. The two pitches from the guide, *Lantern Coast* and *Saltmarsh*, before the fix.

Columns: `name`, `target_play_hours` (`T`), `platform_hours` (`P`), `system_hours` (`F`), `cost_per_content_hour` (`k`), `replay` (`r`).

## Steps

1. **Warm-up (10 minutes).** Run the checker on the starter file. Confirm supply 382.2, loads 1.19 and 0.99, and break-even 3.05 hours. Change *Saltmarsh*'s `system_hours` to 160 and confirm `PASS` at 0.88.
2. **Team parameters.** Set `--n` and `--hours` for your team. If your PR201 team measured its own coordination cost, use it for `--c` and say where it came from.
3. **Measure `k`.** From your PR201 records, divide the team hours spent on content (levels, encounters, quests, with their art and audio) by the minutes of play they produced, times 60. Write the calculation in `budget-notes.md`. If you have no records, use 45 and say so.
4. **Estimate each pitch.** For every shortlisted pitch, each discipline's primary estimates their share of `P` and `F`. Set `T = 6` for the alpha weekend. Set `r` from the pitch's loop. Any `r` above 3 needs one sentence naming the loop that connects two systems.
5. **Run and fix.** Run the checker. Change the chosen pitch until it passes. Record each change as a constraint in the form "X is out of scope for PR301" or "X is limited to Y".
6. **Sensitivity.** Rerun the chosen pitch with `r` reduced by one. Record the load. If it goes above 1, name the first cut you would make in week 10.
7. **Discipline check.** Split the chosen pitch's demand by discipline and run the PR201 lab 01 checker on it. Record the largest discipline load.

## Deliverable

In `docs/pitch/` in the team repository:

- `pitches.csv` and the checker output saved as `budget-output.txt`.
- `budget-notes.md` with the `k` calculation, the loop sentence for any `r` above 3, the constraints, the sensitivity result and the largest discipline load.

**Checkable output:** the instructor reruns `check_budget.py` on your `pitches.csv` with the team parameters written at the top of `budget-notes.md`. It must print `PASS` and exit with code 0.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun with the stated parameters; output file matches |
| Estimates | 4 | `P` and `F` estimated by each discipline's primary; `P` includes login, persistence, grouping and the group encounter |
| `k` and `r` | 4 | `k` measured or honestly defaulted; every `r` above 3 backed by a named loop |
| Constraints | 4 | Every change written as a constraint a designer could apply |
| Sensitivity and discipline check | 4 | Load at `r − 1` reported with a named cut; largest discipline load reported and at or below 1 |
