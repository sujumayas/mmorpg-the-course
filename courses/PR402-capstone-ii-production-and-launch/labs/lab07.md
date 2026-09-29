# PR402 Lab 7: Sprint 4 plan with an interrupt buffer

**Week:** 7 (Production sprint 4). **Guide:** [week 7](../lectures/w07-production-sprint-4.md). **Team lab**, submitted once per team.

## Objective

Plan the last sprint before open beta from measured numbers. You will compute capacity at two velocities, size a buffer for arriving bugs from your closed-beta data, draw a conservative and a planning cut line through one ranked backlog, and track a burn-down that shows arriving bugs separately.

## Starter materials

Copy this template to `production/week07/sprint-plan.md` and fill every blank.

```
## A. Capacity
Completed points: sprint 1 ___  sprint 2 ___  sprint 3 ___
Measured ops tax t: sprint 1 ___  sprint 2 ___  sprint 3 ___
Untaxed velocities (points / (1 − t)): ___  ___  ___
Planning velocity (mean)       = ___
Conservative velocity (min)    = ___
Person-days this sprint ___ / normal ___ = availability ___
Planning capacity     = ___ × ___ = ___  → rounded down ___
Conservative capacity = ___ × ___ = ___  → rounded down ___

## B. Buffer
Closed-beta must-fix bugs filed: ___ over ___ days  (source: tracker query ___)
Expected must-fix bugs this sprint: ___  (reasoning in one line)
Mean points per fixed must-fix bug: ___  (from ___ fixed bugs)
Buffer = ___ × ___ = ___

## C. Commitment
Planning commitment     = ___ − ___ = ___
Conservative commitment = ___ − ___ = ___

## D. Ranked backlog
| Rank | Item | Serves (readiness / balance / instrumentation / onboarding / other) | Points | Running total | Lands |

## E. Day-3 threshold
Ideal line at day 3 = commitment × (D − 3) / D = ___
Mean committed item size = ___
Cut if remaining on day 3 > ___

## F. Burn-down log
| Day | Planned work remaining | Bug points added today | Total remaining | Note |
```

## Steps

1. **Warm-up (10 minutes).** Fill sections A to C with Emberfall's numbers from the guide (27, 26 and 20 points at taxes of 0.10, 0.15 and 0.25; 33 of 35 person-days; 8 bugs at 1.5). You must get capacities of 27 and 25, a buffer of 12, and commitments of 15 and 13. Then open the [interactive](../examples/w07-sprint-buffer-burndown.html) with velocity 29.1 and confirm a commitment of 27 leaves about 11.6 points, as in the guide. Keep the warm-up in `warmup.md`.
2. **Capacity.** Fill section A from your tracker and your week 1 to 3 ops-tax measurements. Use completed points only. If a sprint had carry-over, count it in the sprint where it was finished.
3. **Buffer.** Query your tracker for closed-beta bugs marked must-fix before open beta. Record the count, the days, and the mean size of the ones you have already fixed. State in one line why you expect more or fewer this sprint.
4. **Rank.** Put every candidate item in one list: week 6 change log items, open-beta test instrumentation, readiness items, open bugs, and any features still in the plan. Tag what each serves. Every readiness item must sit above the conservative line; if it does not fit, cut something above it until it does.
5. **Lines.** Mark each item `core`, `planned edge`, `stretch`, `post-launch` or `cut`. Write `post-launch.md` and `cut-list.md`, one reason per item.
6. **Threshold.** Fill section E before the sprint starts.
7. **Track.** Each day, fill one row of section F from the tracker. Add bug points in their own column. On day 3, compare with the threshold and record the decision, even if the decision is "no cut".

## Deliverable

In `production/week07/`: `warmup.md`, `sprint-plan.md` with all six sections, `post-launch.md`, `cut-list.md`.

**Checkable output:** the instructor recomputes sections A, B, C and E from the numbers you entered; all must match. The instructor then checks that the running total at the planning line is at most the planning commitment, and that the day-3 row of section F records a decision consistent with the threshold.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Warm-up | 2 | All five numbers match the guide |
| Capacity | 3 | Completed points only; both capacities correct and rounded down |
| Buffer | 4 | Count, days and sizes come from a named tracker query; expectation reasoned |
| Ranking and lines | 5 | One list; readiness above the conservative line; totals fit commitments |
| Lists | 2 | Post-launch and cut lists exist with reasons |
| Tracking | 4 | Daily rows with bug points separate; day-3 decision recorded and consistent with the threshold |
