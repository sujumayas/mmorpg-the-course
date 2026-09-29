# PR401 Lab 12: Tagged time log and tool decisions

**Week:** 12 (Vertical slice sprint 1). **Guide:** [week 12](../lectures/w12-vertical-slice-sprint-1.md). **Team lab**, submitted once per team.

## Objective

Log every slice hour with a tag, compute what one unit of each content type really costs with one-time work removed, and decide for each candidate tool whether to build it now, later or never. The checker computes per-unit costs from your log, the break-even for each tool, and checks that each decision is consistent with its numbers and states its effect on discipline loads.

## Starter materials

In [`labs/lab12-starter/`](lab12-starter/):

- `unit_cost.py`. Standard library only. Run it with `.venv/bin/python unit_cost.py timelog.csv units.csv tools.csv`. It prints hours by tag, per-unit cost by unit type and discipline, break-even and total saving for each tool, then `PASS` or `NOT READY`, and exits with code 1 when anything fails.
- `timelog.csv`. Eleven *Emberfall* sprint 1 entries from the guide, one of them untagged.
- `units.csv`. Units built so far, per unit type and discipline.
- `tools.csv`. The bounty data tool from the guide, with its note missing.

Tags are `one_time`, `per_unit`, `fix` and `overhead`. A `per_unit` row needs a `unit_type`. In `tools.csv`, `manual_discipline` names the discipline whose measured per-unit cost `u_m` is checked against. Decisions are `build_now`, `build_later` and `never`.

## Steps

1. **Warm-up (15 minutes).** Run the checker on the starter files. Tag the untagged row (a rework after a playtest is a fix). Write the bounty tool's note from the guide: programming load 0.78 to 0.72, design 0.72 to 0.80, and why it pays only because of the patch-week rotation. Rerun until `PASS`. Check that the town's per-unit cost is 10 hours, not the 14 the artist logged on it.
2. **Agree edge cases.** Before tagging your own hours, write `tag-rules.md` with at least five edge cases and how your team tags them. Examples: learning a tool (one-time), rework after review (fix), the first unit's extra experimentation (one-time if it produced a reusable asset or rule, per-unit otherwise).
3. **Your log.** Export your tracker's sprint 1 hours into `timelog.csv`, one row per log entry. Tag every row. Fill `units.csv` with units built to the slice quality bar only. Units still in progress count as zero.
4. **Candidate tools.** List every tool someone on the team has proposed, plus one you think is missing. For each, fill `tools.csv` with `F` from the person who would build it, `u_m` from the checker's per-unit output, `u_t` from a short trial or a written walkthrough, and `n_remaining` from the week 9 content plan.
5. **Load effect.** For each tool, recompute the lab 11 discipline loads with the tool in place (rerun `check_plan.py` on a copy of your backlog). Put the resulting loads in the tool's note.
6. **Late tool.** For your most expensive tool, recompute the break-even at your team's plan ratio from week 6 and write whether the decision survives.
7. **Run the checker** until it prints `PASS`. Save the output as `check-output.txt`.

## Deliverable

In `preproduction/week12/` in the team repository:

- `timelog.csv`, `units.csv`, `tools.csv`, `tag-rules.md` and `check-output.txt`.
- For every `build_now` tool, a backlog item in slice sprint 2 with an owner, so the tool's `u_t` can be measured by week 14.

**Checkable output:** the instructor reruns `unit_cost.py` on your three CSV files. It must print `PASS` and exit with code 0, and the output must match `check-output.txt`.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun, output file matches |
| Tagging | 5 | Every hour tagged; tag rules written with at least five edge cases; one-time and per-unit split is plausible on spot check |
| Unit counts | 2 | Only units at the slice quality bar are counted |
| Tool decisions | 5 | `F`, `u_m`, `u_t` and `n` sourced; break-even computed; decision consistent or explained |
| Load effect | 3 | Each note states the discipline loads with the tool, from a rerun of the lab 11 checker |
| Late-tool check | 1 | Break-even at the team's plan ratio computed for the most expensive tool |
