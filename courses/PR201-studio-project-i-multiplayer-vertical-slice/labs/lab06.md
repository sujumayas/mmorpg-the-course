# PR201 Lab 06: Sprint 2 plan, forecast and combat chain

**Week:** 6 (Sprint 2: core combat). **Guide:** [week 6](../lectures/w06-sprint-2-core-combat.md). **Team lab**, submitted once per team.

## Objective

Plan sprint 2 so that it ends with one playable combat loop. You will forecast the sprint from sprint 1's measured focus factor, order the combat backlog by dependency, mark the chain that makes the sprint goal playable, and state the chain's risk. The checker tells you whether the plan fits the forecast, whether every committed story's dependencies are committed, and whether the committed stories cover the whole loop.

## Starter materials

In [`lab06-starter/`](lab06-starter/):

- `check_sprint_plan.py`. Standard library only. Run `python check_sprint_plan.py forecast.csv backlog.csv`. It prints the focus factor, the forecast, the committed total, the chain and `q^k`, then `PASS` or `NOT READY`. It exits with code 1 when anything fails.
- `forecast.csv`. The *Hollowmarch* sprint 1 record from the guide, sprint 2's useful hours, the sprint goal and `required_roles`, the loop roles the sprint goal needs (here `attack;damage;death;feedback;target`).
- `backlog.csv`. The R2 spike, the guide's ten combat stories in the product owner's excitement order, and the two sprint 1 carry-over tasks, with plan A above the line. Columns: `id`, `story`, `estimate_h`, `depends_on` (story ids separated by `;`, or `sprint1` for work already done), `owner`, `loop_role`, `above_line` (y/n), `on_chain` (y/n), `acceptance`.

## Steps

1. **Warm-up (10 minutes).** Run the checker on the starter files. It reports `NOT READY` because plan A does not form the loop. Edit `above_line` and `on_chain` to make plan B from the guide and run it again until it prints `PASS`. Check that the forecast (46.4) and `q^k` (0.28) match the guide.
2. **Your sprint 1 record.** Replace the sprint 1 values in `forecast.csv` with your own from the week 5 review. Use estimated hours done (the sum of the original estimates of tasks that met your definition of done) and useful hours after illness, other deadlines and week 4's coordination cost.
3. **Your sprint 2 hours.** Ask each member for known absences in weeks 6 and 7 (exams, travel, other deadlines). Enter `s2_useful_h`.
4. **Your sprint goal and loop roles.** Write the sprint goal as one sentence a stranger can check on three machines. List the loop roles it needs in `required_roles`. Most combat goals need at least an attack, damage, a result (death or defeat) and feedback.
5. **Your backlog.** Replace the stories with your own. Split any story over 12 estimated hours. Give every story an owner, its dependencies, a loop role if it has one, and acceptance criteria that include server authority where it applies (CS202 week 4).
6. **Draw the line.** Commit the chain first, then add stretch stories only while the total stays within the forecast plus 10%. Run the checker until it prints `PASS`.
7. **Chain risk.** Record `q`, `k` and `q^k` from the checker output in `plan.md`. If `q^k` is below 0.5, list at least two concrete changes that raise `q` (WIP limit, thin first versions, daily integration, pairing on the riskiest link) and name who is responsible for each.
8. **Latency budget.** Add the predicted versus confirmed feedback table from guide section 3 to `plan.md`, with the RTT and tick rate your TDD assumes.

## Deliverable

In `production/week06/` in the team repository:

- `forecast.csv` and `backlog.csv` that pass `check_sprint_plan.py`, with the output saved as `check-output.txt`.
- `plan.md` with the sprint goal, the chain risk and your changes to raise `q`, the feedback table, and the enemy's tuning targets (time-to-kill and time-to-die) as numbers.

**Checkable output:** the instructor reruns `check_sprint_plan.py` on your two CSV files. It must print `PASS` and exit with code 0.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun, output file matches |
| Honest inputs | 4 | Sprint 1 values match the week 5 review record; useful hours account for real absences and coordination |
| Loop and dependencies | 4 | `required_roles` follows from the sprint goal; the chain is the shortest set that makes the goal playable; stretch stories sit below the line |
| Chain risk | 3 | `q`, `k` and `q^k` stated; if below 0.5, at least two owned changes to raise `q` |
| Acceptance criteria | 3 | Every committed story's criteria can be checked by someone else; server authority is explicit for attack, damage and death |
| Feedback table and tuning targets | 2 | Predicted and confirmed columns filled with RTT and tick stated; impact sound confirmed; TTK and TTD targets are numbers |

<details>
<summary>Instructor notes</summary>

- The warm-up fix is the R2 spike and C1 to C5 above the line, C1 to C5 on the chain, C6 and C8 below. Committed total 46, forecast 46.4. Plan A (44 hours) passes the hours check and fails only the loop check, which is the point.
- Watch for teams that pass the checker by listing very few `required_roles`. Compare the roles with the sprint goal sentence.
- Teams often count half-finished sprint 1 tasks in `s1_done_estimate_h`. Cross-check with the week 5 review record.

</details>
