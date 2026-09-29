# PR101 · Lab 12: Recovery plan

**Week:** 12, crunch: causes, costs, alternatives ([lecture](../lectures/w12-crunch-causes-costs-alternatives.md)).
**Time:** 2 hours in lab, plus up to 1 hour at home with your team.
**Work mode:** your final-project team.
**Weight:** part of the final team game (40%). The overtime policy you write here is added to your working agreement from [lab 11](lab11.md) and checked at the week 15 release.

## Objective

Measure the real gap between your remaining work and your remaining capacity for the final game. Build two plans that close it, one with overtime only and one that cuts first. Compare them with the week 12 crunch ledger over the deadline and the weeks after it. Commit to one plan and write a bounded overtime policy into your working agreement.

This is a production exercise. The script only does the arithmetic. The decisions are yours.

## Starter materials

All in [`lab12-starter/`](lab12-starter/). Standard-library Python 3.10 or later.

- [`crunch_ledger.py`](lab12-starter/crunch_ledger.py) runs the lecture's model and prints a week-by-week ledger with the lead over a 40-hour schedule. Run with no arguments and it reproduces the lecture's four-week table, ending `lead at week 12: +4.0`. `--schedule 50,40,50` takes your own week-by-week hours. `--f`, `--g` and `--emin` change the parameters.
- [`remaining_work.csv`](lab12-starter/remaining_work.csv) is a template with three example rows. Replace them with your tasks.
- Your task board, your cut list from [week 4](../lectures/w04-scope-mvp-vertical-slice-cut-lists.md), your week 11 contribution record (for real hours per week) and your lab 10 stability forecast.
- The [interactive](../examples/w12-crunch-ledger.html).

Run from inside the folder:

```
cd lab12-starter
python crunch_ledger.py --schedule 50,40,50 --horizon 6 --deadline 3
```

That example prints a lead of +18.0 at the deadline and a return of 0.80 per extra hour.

## Steps

### Part A: the gap (25 min)

1. Fill `remaining_work.csv` with every open task for the final game, including bug fixing from your lab 10 forecast as one line per week. Mark which tasks are on the cut list and their cut order.
2. Compute capacity: for each member, the hours per week they actually worked over the last two weeks (from the contribution record, not from hope), times weeks left. Sum.
3. Gap = total estimate − capacity. Week 6 showed that estimates run low. Add a buffer of at least 20% to the estimates and recompute. Record both gaps.

### Part B: plan A, overtime only (20 min)

4. Find the weekly hours and number of weeks that close the buffered gap by overtime alone. Run the ledger with those numbers and `--horizon` set to the deadline plus four weeks (your exam period).
5. Record the lead at the deadline, the lead at the horizon, and the return per extra hour. Run it again with `--g 0.05` (slower recovery) and record the same three numbers.

### Part C: plan B, cut first (30 min)

6. Cut tasks from the bottom of the cut list until the remaining gap is no more than 10 hours per person. List the cuts and the hours each saves.
7. Close what remains with at most one 50-hour week per person, never two in a row and never in the final week. Run the ledger with that schedule.
8. For each cut, write one sentence on what the player loses and why the game still meets its pillars (week 4).

### Part D: decide and write the policy (25 min)

9. Put plan A and plan B side by side in one table: hours worked, features shipped, lead at the deadline, lead at the horizon, return per extra hour, and one risk each.
10. Choose. Write a 400-word justification that uses at least three numbers from the table and names the parameter (`f`, `g` or your estimates) your decision is most sensitive to.
11. Replace the "Overtime policy" placeholder in your working agreement with a policy of at most six rules. It must cover the maximum hours per week, how often overtime can happen, who can ask for it and who can refuse it, how it is logged in the contribution record, and the recovery week after the deadline. All members sign again.

## Deliverable

One PDF or shared page containing:

- The completed `remaining_work.csv` and the gap calculation, with and without buffer.
- The ledger output for plan A (both `g` values) and plan B, pasted as text.
- The comparison table and the 400-word justification.
- The cut list for plan B with the player-impact sentences.
- The updated, re-signed working agreement with the overtime policy.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Gap | Tasks complete; capacity from recorded hours, not plans; buffered and unbuffered gap | Gap computed from planned hours or without buffer | Missing | 20 |
| Plan A | Closes the buffered gap; ledger run at both `g` values; three numbers recorded for each | One run, or numbers incomplete | Missing | 15 |
| Plan B | Cuts follow the cut list order; remaining overtime obeys the rule; player impact stated for each cut | Cuts present, rule broken or impact vague | Missing | 20 |
| Decision | Comparison table complete; justification uses at least three numbers and names the most sensitive parameter | Decision made, argued mainly from opinion | Missing | 25 |
| Overtime policy | Six or fewer rules covering all five required points; re-signed | Policy present, a required point missing | Missing | 20 |
| **Total** | | | | **100** |

<details>
<summary>Instructor notes</summary>

- Expect plan A to show a large lead at the deadline and a small or negative lead four weeks later. Teams that choose plan A anyway can still earn full marks for the decision if they argue it with numbers and bound the damage (for example, because the deadline is immovable and they plan a light exam period). The rubric rewards reasoning, not the "right" answer.
- Watch for capacity copied from the week 1 charter rather than from the contribution record. That is the most common error, and it hides the real gap.
- Reference numbers: the default run gives +44.0 at week 4, +4.0 at week 12 and 0.05 per extra hour. `--schedule 50,40,50 --horizon 6 --deadline 3` gives +18.0 at the deadline, +16.0 at week 6 and 0.80 per extra hour.

</details>
