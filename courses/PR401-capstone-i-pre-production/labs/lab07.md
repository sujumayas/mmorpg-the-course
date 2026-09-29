# PR401 Lab 07: Technical design budget sheet and spike plan

**Week:** 7 (Technical design). **Guide:** [week 7](../lectures/w07-technical-design.md). **Team lab**, submitted once per team.

## Objective

Size your launch server with numbers you measured, before you build on it. You will fill a budget sheet for at least three load cases (spread, hub and a 2× load test), check it against the course budget lines, decide what to change where it fails, and plan the spikes that measure the inputs you are still guessing.

## Starter materials

In [`labs/lab07-starter/`](lab07-starter/):

- `net_budget.py`. Standard library only. Run `python net_budget.py budget.csv`. For each row it prints the visible entities `e`, update size `u`, client kbit/s, egress Mbit/s, entity updates per second and replication milliseconds per tick. It then checks your declared values (2% tolerance), the budget lines, and that every over-budget row has a response. It prints `PASS` or `NOT READY`.
- `budget.csv`. The *Emberfall* rows from the guide's table. One row has its declared values blank, and the uncapped load-test row has no response.

Column notes. `kind` is `spread`, `hub` or `loadtest`. `aoi_cap` is a number or `none`. `source` is `measured` or `spike planned`. `response` is a design change or an accepted risk with a reason, required whenever a row breaks a budget line.

Budget lines: client downstream at most 128 kbit/s in every case, and replication at most half a tick in `loadtest` rows.

## Steps

1. **Warm-up (10 minutes).** Fill the blank declared values in the starter from the guide's table and write a response for the uncapped load-test row ("rejected design, replaced by the capped row" is acceptable here). Run the checker until it prints `PASS`.
2. **Targets.** Write your launch CCU and your load-test CCU (at least twice the launch figure) at the top of `docs/tdd.md`.
3. **Measure `s`.** Log the serialized size of one entity update for your most common entity in the current build. Use the median of at least 1,000 updates. If you cannot measure it this week, set `source` to `spike planned`.
4. **Measure `t`.** Time the replication step for one tick with bots in one place, and divide by the number of entity updates sent in that tick. Repeat for five ticks and take the median.
5. **Build your sheet.** Replace the starter rows with your own spread, hub and load-test cases, with and without your interest cap if you have one.
6. **Respond.** For every row over a line, write a design change (a cap, a lower rate, a smaller update, a priority rule) and add the changed row, or an accepted risk with the reason.
7. **Weekend egress.** Multiply your worst launch-case egress in MB/s by 172,800 seconds and write the gigabytes, your host's current price per GB and the date you checked it in `docs/tdd.md`.
8. **Spike plan.** In `spikes.md`, list at least three spikes, each with the input it measures, owner, time box, and what result would change the design.

## Deliverable

In `preproduction/week07/` and `docs/tdd.md` in the team repository:

- `budget.csv` and the checker output saved as `check-output.txt`.
- `spikes.md` with at least three spikes.
- The TDD with the targets, the budget table, the egress estimate and the decisions log.

**Checkable output:** the instructor reruns `net_budget.py` on your `budget.csv`. It must print `PASS` and exit with code 0, with at least one row of each kind.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun; saved output matches |
| Measured inputs | 5 | `s` and `t` measured from the real build with method stated, or a spike with owner and time box |
| Load cases | 3 | Spread, hub and 2× load test present; the hub case uses a realistic crowd for your world |
| Responses | 4 | Every over-budget row has a design change or a reasoned accepted risk; player-facing costs of any cap named |
| Egress | 2 | Weekend gigabytes computed; price and date recorded |
| Spike plan | 2 | Three or more spikes, each tied to an input and a decision |
