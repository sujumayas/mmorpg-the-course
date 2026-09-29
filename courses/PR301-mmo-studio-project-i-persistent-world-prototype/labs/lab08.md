# PR301 Lab 08: Freeze plan and kill-switch sheet

**Week:** 8 (sprint 3 mid-sprint session and the alpha go/no-go; the sprint 3 review is at the start of week 9). **Guide:** [week 8](../lectures/w08-sprint-3-review.md). **Team lab**, submitted once per team.

## Objective

Decide, from your own tracker, whether the bug work between the review and the alpha freeze fits your team's hours. Close any gap by cutting scope, test the plan against faster bug arrivals, and build and test the kill switches that let the world launch safely if an S1 is still open on Thursday.

## Starter materials

In [`labs/lab08-starter/`](lab08-starter/):

- `check_gonogo.py`. Standard library only. Run it with `.venv/bin/python check_gonogo.py tracker.csv plan.txt killswitches.csv`. It prints the forecast for the expected case and for arrivals × 1.5, with slack in hours and as a share of capacity, then `PASS` or `NOT READY` (exit code 1).
- `tracker.csv`. The guide's tracker numbers per severity, before any cuts.
- `plan.txt`. The guide's capacity inputs, before the cuts, with `bad_case_response` blank.
- `killswitches.csv`. Four value-moving systems with flag names, no owners and no test dates.

## Steps

1. **Warm-up (10 minutes).** Apply the guide's two cuts to the starter files (crafting UI to 1 hour; six S2s flagged off). Check that the expected slack is +2.6 h and the pessimistic slack is −6.4 h. The checker will still say `NOT READY` because of the kill switches and the blank response. That is expected.
2. **Your tracker numbers.** Export your tracker. For each severity, count open bugs now, bugs opened in the last two weeks divided by two, and mean hours logged per closed bug. Re-check every severity against the persistent-world table in the guide before you count. Enter your numbers in `tracker.csv`.
3. **Your capacity.** Fill `plan.txt` with your team size, available hours per person per week (as in week 3), weeks to the freeze, the middle of your two measured focus factors and at least 5 reserved hours for alpha operations. Put every unfinished committed feature in `feature_hours`.
4. **Cuts.** If the expected case does not fit, cut scope. Simplify a feature, or flag off features the alpha does not test. Record every cut in the backlog as cut or flagged, with the ticket ID, in `freeze-plan.md`. Do not change severities, fix times, hours per week or the focus factor to make it fit.
5. **Bad case.** Read the pessimistic line. In `bad_case_response`, write what the team will do if it happens (for example: "launch with the affected system behind its kill switch; if the S1 cannot be switched off, run Saturday only").
6. **Kill switches.** Implement a runtime flag for each value-moving system in your world. Add systems your world has that the starter lacks. Give each an owner. Flip each one both ways on a running server with at least two clients connected, and record the date in `tested_on`.
7. **Run the checker** until it prints `PASS`.

## Deliverable

In `production/week08/` in the team repository:

- `tracker.csv`, `plan.txt` and `killswitches.csv` that pass `check_gonogo.py`, with its output saved as `check-output.txt`.
- `freeze-plan.md`: the tracker export date, the cuts with ticket IDs, the bad-case response, and a short clip or log excerpt for each kill-switch test.
- The signed go/no-go list from the guide, section 5.

**Checkable output:** the instructor reruns `check_gonogo.py` on your three files. It must print `PASS` and exit with code 0. At the freeze on Thursday of week 9, the instructor flips one kill switch of their choice on your running server.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun, output file matches |
| Honest inputs | 4 | Counts, rates and fix times traceable to the tracker export; severities follow the persistent-world table |
| Cuts | 4 | Scope cuts only, each with a ticket ID; expected slack is positive |
| Bad case | 3 | Pessimistic slack reported and a concrete response written down |
| Kill switches | 5 | Every value-moving system covered, runtime flags, owners, tested both ways with clients connected, evidence attached |
