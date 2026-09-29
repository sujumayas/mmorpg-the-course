# PR402 Lab 11: Interrupt budget and support queue worksheet

**Week:** 11 (Live-ops week 2). **Guide:** [week 11](../lectures/w11-live-ops-week-2-operating-rhythm.md). **Team lab**, submitted once per team.

## Objective

Measure how much of your week live operations took in week 10, how long players waited for support, and which one-off fixes buy back the most planned time. The output is a worksheet whose every number can be recomputed from the raw data in it, plus a rota the team actually follows.

## Starter materials

Copy this template into `production/week11/lab11.md` and fill every blank. Keep the raw data tables; the instructor recomputes from them.

```markdown
## Part A. Interrupt budget (week 10)
Team size: __   Hours per person: __   C = __
Interrupt line (set before analysis, date): __% (__/__/____)

| Category | Hours | Log entries | Main driver |
|---|---|---|---|
| Incidents and hotfixes | | | |
| Player support | | | |
| Moderation | | | |
| Monitoring | | | |
| Deploys and restarts | | | |
| Total I | | | |

i = I / C = __     P = C − I = __     Planned hours assumed in the week-10 plan: __

## Part B. Support queue (week 10)
Open tickets at the same time each day (7 values): __, __, __, __, __, __, __
L = __   Tickets arrived in the week: __   λ = __ per day   W = L / λ = __ days
Wait target W_target = __ days   L_target = λ × W_target = __

| Ticket cause | Count | Share |
|---|---|---|
| | | |

## Part C. Buy-back plan
| One-off job | Cost h | Interrupt hours removed per week s | Payback h/s | Owner | Tracker ID |
|---|---|---|---|---|---|

Steady-state I' = __   i' = __   P' = __
Week-11 planned hours = C − I − sum of chosen costs = __
Cumulative planned hours weeks 11-14, with and without the plan: __ / __

## Part D. Operating rhythm
On-call rota (one name per day to end of week 14):
Daily triage time and length:
Weekly live review day, time and four agenda items:
```

## Steps

1. **Warm-up (10 minutes).** Fill Part A and B with the Emberfall numbers from the guide and check you get `i = 54.8%`, `W = 4.50` days and a payback of 1.55 weeks. Then delete them.
2. **Set the interrupt line** before you open the log. Write the date next to it.
3. **Tag the log.** Every week-10 entry gets exactly one tag: planned, or one of the five interrupt categories. Entries without a tag count as interrupts. Fill Part A.
4. **Count the queue.** Use your ticket system's history to reconstruct the open count at one fixed time each day, or use the counts you took. Fill Part B, including the cause breakdown from ticket labels.
5. **List candidate fixes.** At least three, each with a cost estimate and the weekly interrupt hours it removes, taken from a specific row of Part A. Include the top ticket cause. Compute payback and choose. Create a tracker ticket for each chosen fix.
6. **Project four weeks** of cumulative planned hours with and without the plan, as in the guide's script. State the week in which the plan pulls ahead, if it does.
7. **Write the rhythm** (Part D) and post the rota where every team member sees it.

## Deliverable

`production/week11/lab11.md`, complete, with tracker IDs.

**Checkable output:** the instructor recomputes `C`, `I`, `i`, `P`, `L`, `λ`, `W`, `L_target` and every payback from the raw numbers in the sheet. All must match the sheet to one decimal place. The row totals in Part A must equal `I`, and the cause counts in Part B must sum to the week's arrivals.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Arithmetic | 5 | Every recomputed number matches; totals add up |
| Honest log | 3 | Every entry tagged; interrupt line dated before analysis |
| Queue | 4 | Seven daily counts, correct `W`, a stated target and `L_target`, causes sum to arrivals |
| Buy-back plan | 5 | At least three candidates, each tied to a Part A row; top ticket cause addressed or explicitly deferred with a reason; owners and tracker IDs |
| Rhythm | 3 | Rota covers every day to week 14; triage and review slots are fixed times |
