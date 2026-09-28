# MMO401 · Lab 09: Haulers between two regions

**Week:** 9 ([lecture](../lectures/w09-regional-economies-and-logistics.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** pairs.
**Counts toward:** ABM labs (40% of the course grade). The final project can reuse this module for its regional layer.

## Objective

Write hauler agents for a two-region market, confirm that prices settle inside the transport-cost band from the lecture, then stress the route with a war and design a logistics rule that keeps frontier prices within a target.

## Starter materials

- [`lab09-starter.py`](lab09-starter.py): Python 3, standard library only. It contains
  - the two regional markets from the lecture, cleared each day from the flow of goods (`clear_region_a`, `clear_region_b`);
  - a `Route` with trip time, capacity, loss chance, toll and wage, and its `tau()`;
  - `analytic(tau)` and `lecture_tau(route)`, the lecture's closed-form answers;
  - `simulate(route)`, a 600-day loop with 120 haulers that smooths prices (half old, half new) each day;
  - two stubs to write, `decide` (the entry and exit rule, fully described in its docstring) and `run_trip`.
- Running the starter prints the analytic prices for four routes and "Simulation: not run yet".
- Flow in the simulation is measured in the lecture's units: one 200-unit trip adds 0.5 to the daily flow `F`.

## Steps

### Part A: haulers and verification (45 min)

1. Implement `decide` and `run_trip` as their docstrings describe.
2. Run the four scenarios. For each, report the analytic and simulated `P_A`, `P_B` and gap (the starter prints the mean of the last 200 days). Every simulated gap must be within 1.0 gold of the lecture's `τ`: 1.50, 6.00, 7.14 and 11.43.
3. Plot `P_A` and `P_B` against days for the "long_danger" route. Mark `τ` as a band around the price lines.
4. In two sentences, explain why the simulated gap sits slightly off the analytic one. (Look at how entry and exit work, and at what happens to lost cargo.)

### Part B: a war on the route (40 min)

5. Add a `schedule` to `simulate` so the route can change mid-run. From day 200 to day 350, raise the loss chance on the highway route from 0 to 25% (a war). Return it to 0 afterwards.
6. Plot both prices and the number of active haulers across the whole run. Report the frontier price before, during (mean of days 300 to 350) and after the war (mean of days 500 to 600), and compare the "during" value with the analytic answer for `λ = 25%`.
7. Measure how many days the frontier price takes to return within 1 gold of its pre-war level after day 350.

### Part C: design for a target (35 min)

8. Your lead wants the frontier price to stay at or below 64 even during the war. You may change exactly one of: capacity, trip time, a toll (it may be negative, a subsidy paid per unit delivered), or add an escort rule that halves `λ` at the cost of adding 0.5 hours to the trip.
9. Use `lecture_tau` to test each of the four options analytically. Some cannot reach the target at any setting; say which and why, using the parts of `τ`. Pick one that can, then confirm it with the simulation. Report the frontier price during the war and the cost of your rule (gold per day paid out for a subsidy, or hours added for an escort).

## Deliverable

- Your completed script, runnable with `python3`, plus the CSVs it writes.
- A report of up to 2 pages: the Part A table, chart and two sentences; the Part B chart, three prices and recovery time; the Part C choice with its analytic and simulated numbers; and a 200-word recommendation to the lead that names who gains and who loses from your rule.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Hauler agents and verification (Part A) | All four gaps within 1.0 of `τ`; chart shows the band; explanation correct | Three of four within tolerance, or explanation vague | Simulation does not run | 30 |
| War scenario (Part B) | Schedule works, three prices and recovery time reported, comparison with analytic answer | Prices reported without the analytic comparison or recovery time | Missing | 25 |
| Design for a target (Part C) | Analytic choice confirmed by simulation, cost computed | Choice made by trial and error without the analytic step, or cost missing | Missing | 25 |
| Recommendation | Uses own numbers, names winners and losers | Plausible but not tied to the runs | Missing | 15 |
| Code quality | Parameters in one place, readable, runs first time | Runs with minor fixes | Does not run | 5 |
| **Total** | | | | **100** |
