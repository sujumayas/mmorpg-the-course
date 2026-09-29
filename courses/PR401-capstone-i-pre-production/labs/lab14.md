# PR401 Lab 14: Replan from the slice, and the review decision record

**Week:** 14 (Pre-production review). **Guide:** [week 14](../lectures/w14-pre-production-review.md). **Team lab**, submitted once per team.

## Objective

Replace the week 11 estimates with what the vertical slice measured, project production costs with a learning rate you can defend, and show that every discipline still fits at every milestone. Then record the review panel's decision as checkable action items. The checker recomputes the lab 11 loads with your measured unit costs in place.

## Starter materials

In [`labs/lab14-starter/`](lab14-starter/):

- `reconcile.py`. Standard library only. Run it with `.venv/bin/python reconcile.py team.csv backlog.csv replan.csv`. For each replaced item it prints the old planned hours, the projection at your learning rate and the flat projection, then the cumulative load per discipline at each milestone, then `PASS` or `NOT READY`. It exits with code 1 when anything fails.
- `team.csv` and `backlog.csv`. The *Emberfall* plan as it passed lab 11.
- `replan.csv`. One row replacing A1 (three more towns) with the slice measurement from the guide: `u1 = 10` actual hours, units 2 to 4, planned at `LR = 0.95`.

Rules the checker applies. A replaced item's hours are `Σ u1 × n^(log2 LR)` over the production units, in actual hours, so they are **not** multiplied by the plan ratio. Other items keep their raw estimate times the plan ratio. A learning rate below 0.9 needs either at least two measured units of that type or a note with the evidence.

## Steps

1. **Warm-up (10 minutes).** Run the checker on the starter files. Art is at 1.05. Make the guide's decision: two more towns instead of three (`units` from 3 to 2). Rerun and confirm art at 0.93 and `PASS`. Then try `lr = 0.85` with three towns and read the message the checker gives you.
2. **Your measurements.** From your lab 12 and lab 13 time logs, take the per-unit cost `u1` of every content type the slice built at the quality bar, with one-time hours removed. Include tool-made units, using the measured `u_t`.
3. **Replace estimates.** Copy your lab 11 `team.csv` and `backlog.csv`. For every backlog item that the slice measured, add a `replan.csv` row. Set `first_n` to the number of units already built plus 1.
4. **Choose learning rates.** Plan at 0.95 unless you have two or more measured units of that type, or evidence you can write in the note. Run the checker at your rates, and once with every `lr` at 1.0. Save both outputs.
5. **Make it fit.** If any discipline is above 1.0, cut units, move work or reorder, as in lab 11. Record each move in `replan-log.md` with the pillar it touches. Do not lower the slice quality bar to fit.
6. **Triggers.** For each learning rate you planned with, add a risk register entry: the hours unit 2 must come in under for the hopeful case, the hours above which you take your reserve cut, and the response for each. Use `u1 × 2^(log2 LR)` to get the lines.
7. **Final run** until `PASS`. Save the output as `check-output.txt`.
8. **After the review.** Fill in `review-decision.md` from the template below during the last 15 minutes of the meeting.

### Review decision template

```
Decision: go / go with conditions / rework / pivot
Panel members:
Date:

Conditions (one row each)
| # | Condition as stated by the panel | Owner | Due | Observable result that shows it is met |

Questions we could not answer, and how we will answer them
| Question | What we will measure or build | Owner | Due |

Peer panel questions and our answers
```

## Deliverable

In `preproduction/week14/` in the team repository:

- `team.csv`, `backlog.csv`, `replan.csv`, `replan-log.md`, the flat-rate output as `flat-output.txt`, and `check-output.txt`.
- The updated `production-plan.md` with the new load table and the learning-rate triggers in its risk register.
- `review-decision.md`, completed at the meeting.

**Checkable output:** the instructor reruns `reconcile.py` on your three CSV files. It must print `PASS` and exit with code 0, and the output must match `check-output.txt`.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun, output file matches |
| Measured costs | 4 | Every content type the slice built is replaced; `u1` traces to tagged per-unit hours with one-time hours removed |
| Learning rates | 3 | 0.95 or flat unless two measured units or written evidence; flat run saved and discussed |
| Replan log | 3 | Every change recorded with hours and the pillar touched; no quality-bar reductions |
| Triggers | 3 | Each planned rate has numeric lines for unit 2 and a pre-chosen response for each direction |
| Decision record | 3 | Every condition has an owner, a date and an observable result; open questions have a plan |
