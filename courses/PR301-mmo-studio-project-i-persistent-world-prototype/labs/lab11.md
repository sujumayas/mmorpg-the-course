# PR301 Lab 11: One-week sprint plan for social systems

**Week:** 11 (Sprint 4: social systems). **Guide:** [week 11](../lectures/w11-sprint-4-social-systems.md). **Team lab**, submitted once per team.

## Objective

Plan sprint 4 so that the commit fits the team you have this week, the party system the week 12 encounter needs is never at risk, and at least one social feature is rescoped rather than cut whole. The checker tells you whether the plan follows the capacity rule from section 2 of the guide and whether every committed item's dependencies are in the sprint.

## Starter materials

In [`labs/lab11-starter/`](lab11-starter/):

- `check_sprint.py`. Standard library only. Run it with `.venv/bin/python check_sprint.py velocity.csv availability.csv backlog.csv`. It prints the weekly velocities, availability, `capacity_low`, `capacity_mean`, the bug reserve, the commit and the stretch, then `PASS` or `NOT READY`. It exits with code 1 when anything breaks the rule.
- `velocity.csv`. Estimated hours of done stories and sprint length in weeks for the *Saltmarsh* team's sprints 1 to 3.
- `availability.csv`. Full and available days per person for the *Saltmarsh* team.
- `backlog.csv`. The *Saltmarsh* backlog after the rescope in the guide, with the `status` column blank for the features.

Statuses are `done`, `commit`, `stretch`, `bug` (the bug reserve), `deferred` and `cut`. `depends_on` lists item IDs separated by semicolons.

## Steps

1. **Warm-up (15 minutes).** Fill in the statuses in the starter `backlog.csv` to match option B in the guide. Add notes for the deferred and cut items, and a note starting with `rescoped` on guild lite. Run the checker until it prints `PASS` with a commit of 11 and a stretch of 1.
2. **Velocity.** Replace `velocity.csv` with your own sprints 1 to 3 from the tracker. Use estimated hours of stories that met the definition of done only. Items that were "nearly done" at the review count as zero.
3. **Availability.** Replace `availability.csv` with this week's real figures for each team member. Exams, other deadlines and planned absences all count. Nobody is at more than 5 days.
4. **Bug reserve.** Add the must-fix bugs from your week 10 input list as rows with status `bug`, estimated in hours.
5. **Social backlog.** Add your social backlog with estimates from planning poker. Include dependencies.
6. **Rescope.** Pick at least one feature that doesn't fit whole. Split it into a smaller version that keeps its purpose, estimate the smaller version from scratch, and mark it with a note starting `rescoped` that says what was left out.
7. **Commit and stretch.** Set statuses. Run the checker until it prints `PASS`.
8. **Sequence.** In `sprint4-order.md`, list the committed items in the order work starts, with the owner and the day each starts. The item the encounter depends on starts first.
9. **Worst case.** In the same file, write the worst-case chat delivery rate and login presence burst at 50 players, as in the guide's worked example.

## Deliverable

In `production/week11/` in the team repository:

- `velocity.csv`, `availability.csv` and `backlog.csv` that pass `check_sprint.py`, with the output saved as `check-output.txt`.
- `sprint4-order.md` with the sequence and the worst-case numbers.

**Checkable output:** the instructor reruns `check_sprint.py` on your three CSV files. It must print `PASS` and exit with code 0, and the velocities must match the tracker for one sprint chosen at random.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun; output file matches |
| Velocity and availability | 4 | Taken from the tracker and from each person; converted to weekly figures |
| Bug reserve | 3 | Week 10 must-fix bugs included with estimates |
| Rescope | 4 | At least one feature split into a smaller version, estimated from scratch, with what was left out |
| Sequence | 3 | Dependency first; owners and start days named |
| Worst case | 2 | Delivery rate and presence burst computed with a stated rate limit |
