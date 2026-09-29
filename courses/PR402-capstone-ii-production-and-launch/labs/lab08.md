# PR402 Lab 8: Open-beta sizing sheet and operations log

**Week:** 8 (Open beta). **Guide:** [week 8](../lectures/w08-open-beta.md). **Team lab**, submitted once per team.

## Objective

Size your open beta from two targets that pull in opposite directions, run it with a rota and tested kill switches, and record forecast against actual so that next week's launch forecast starts from measured error rather than a fresh guess.

## Starter materials

Copy this template to `production/week08/sizing.md` and fill every blank before the weekend.

```
## A. Sizing (before the weekend)
Rarest bug to catch: once per ___ player-hours   Reason: ___
Exposure needed E = 3 × ___ = ___ player-hours
Show-up rate ___ (source ___)   Hours per active player ___ (source ___)
Sign-ups needed = E / (___ × ___) = ___      Sign-ups now: ___
Busiest-day share ___   Busiest-hour share ___   (source ___)
Peak-hour CCU = E × ___ × ___ = ___
Spike factor ___ (reason ___)   Forecast peak = ___
Load-test knee ___ CCU (report ___)   Headroom ___   Safe capacity = ___
Levers chosen: ___          Forecast peak after levers: ___
Login cap set to: ___

## B. Operations (during the weekend)
Rota: | Block | Primary | Backup |
Kill-switch drill: | Switch | Flipped at | Restored at | Worked? |
Incident log: | Time | Severity | What players saw | Action | Resolved at |

## C. Forecast against actual (after the weekend)
| Quantity | Forecast | Actual | Error (actual / forecast) |
| Sign-ups | | | |
| Show-up rate | | | |
| Exposure (player-hours) | | | |
| Busiest-hour share | | | |
| Peak CCU | | | |
| Tick time at peak (p99) | — | | |
| Crashes per 100 player-hours | — | | |

## D. Exit criteria
| Criterion | Threshold (written before the weekend) | Result | Pass/fail |
```

## Steps

1. **Warm-up (10 minutes).** Fill section A with the guide's worked-example values. You must get 1,200 player-hours, 1,067 sign-ups, 64.8 peak-hour CCU, 97.2 forecast peak, safe capacity 98, and 77.8 with waves. Save it as `warmup.md`.
2. **Size.** Fill section A from your closed-beta logs and the sprint 4 load-test report. Name the source of every rate.
3. **Choose levers.** If the forecast peak is above 90% of safe capacity, choose at least one lever from the guide's table and recompute. Set the login cap at or below safe capacity.
4. **Write exit criteria.** At least five, each with a threshold, written before the doors open. Include crash rate per player-hour, peak tick time, a tutorial-funnel step, and at least one targeted test.
5. **Drill.** Flip and restore every kill switch on staging. Log the times.
6. **Run.** Keep the incident log live during the weekend. Every incident gets a severity from your table.
7. **Close.** Fill sections C and D within 24 hours of the beta ending. Compute the error ratio for every forecast.

## Deliverable

In `production/week08/`: `warmup.md`, `sizing.md` with all four sections, and the raw peak-CCU and crash queries used for section C.

**Checkable output:** the instructor recomputes section A from its inputs (all derived values must match), checks that the exit thresholds in section D carry a timestamp before the beta started (commit history), and recomputes one error ratio in section C from the raw query.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Warm-up | 2 | All six values match |
| Sizing | 5 | Every rate sourced; arithmetic correct; levers applied when the margin is thin |
| Readiness | 4 | Login cap set; every kill switch drilled with times; rota in blocks of at most four hours |
| Operations log | 3 | Every incident has severity, times and action |
| Forecast against actual | 3 | Complete, with error ratios and raw queries |
| Exit criteria | 3 | Written before the weekend; results with evidence; pass or fail follows from the threshold |
