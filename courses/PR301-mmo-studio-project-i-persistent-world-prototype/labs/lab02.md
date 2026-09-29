# PR301 Lab 02: Architecture capacity sheet and decision record

**Week:** 2 (Technical architecture review). **Guide:** [week 2](../lectures/w02-technical-architecture-review.md). **Team lab**, submitted once per team.

## Objective

Show with numbers that your architecture carries a load test at twice the concurrency target in the worst crowd your world allows, and cut every component the numbers do not require. You will measure the cost of one delivery in a spike, fill a capacity sheet, find the largest crowd one process can hold, and write a decision record with measurable revisit triggers.

## Starter materials

In [`labs/lab02-starter/`](lab02-starter/):

- `check_capacity.py`. Standard library only. Run it with `.venv/bin/python check_capacity.py capacity.csv`. It prints deliveries per second, CPU share, outbound bandwidth, database commits and the largest crowd within the CPU budget, then `PASS` or `NOT READY`. It exits with code 1 when a budget is exceeded or a value is missing.
- `capacity.csv`. The *Saltmarsh* values from the guide, with a note column explaining each key.

## Steps

1. **Warm-up (10 minutes).** Run the checker on the starter file. Confirm 61,500 deliveries per second, 49.2% CPU and a largest crowd of 111. Set `headroom` to 2.4 and confirm `NOT READY`.
2. **Spike.** On the machine that will host the alpha, time how long your server takes to build and queue one state update for one client. Run at least 100,000 deliveries and divide. Record the code, machine and result in `spike-note.md`.
3. **Worst crowd.** Name the place in your world where the most players and mobs can be at once. Count its mobs for `mobs`.
4. **Fill the sheet.** Replace every value with your own. Take `u` and `tick_hz` from your design, `bytes_per_delivery` from your protocol, `changes_per_player_s` from your persistence map, and the two budgets from your host and database.
5. **Run.** If the sheet fails, change the design (fewer updates, a smaller crowd, area of interest), not the budgets. Record each change as a decision.
6. **Decision record.** Write five to ten decisions, each with its reason and a revisit trigger someone could measure. List deferred machinery. End with the sprint 1 proof sentence.

## Deliverable

In `docs/architecture/` in the team repository:

- `capacity.csv` with your values, and the checker output saved as `capacity-output.txt`.
- `spike-note.md`.
- `decisions.md` with the decisions, the deferred list and the sprint 1 proof.
- The architecture diagram and the persistence map with strategy and transaction boundary columns.

**Checkable output:** the instructor reruns `check_capacity.py` on your `capacity.csv`. It must print `PASS` with `headroom` at least 2 and exit with code 0.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun at headroom 2 or more; output file matches |
| Measured cost | 4 | `cost_us` comes from a spike on the alpha host, with method recorded |
| Worst crowd | 3 | The sheet uses the most crowded place the design allows, named and justified |
| Persistence map | 3 | Every "None" loss maps to write-through with a named transaction boundary |
| Decision record | 4 | Each decision has a reason and a measurable revisit trigger; deferred machinery is listed |
| Sprint 1 proof | 2 | One testable sentence that includes a restart |
