# MMO404 · Lab 13: The player-hour bill

**Week:** 13 · **Time:** 2 hours in lab plus about 3 hours at home · **Weight:** part of the labs (40%)

## Objective

Turn the [week 13 lecture](../lectures/w13-cost-engineering.md) cost model into a tool you can put in front of a producer. You price 1,000 player-hours from its three terms, check the share rule against direct computation, find where the tick rate makes compute the big term, add the spot fill limit, and rank real proposals by dollars saved and by what they cost players.

## Starter materials

Folder [`lab13-starter/`](lab13-starter/README.md). Standard library Python only. Run it with `.venv/bin/python` from the repository root or any Python 3.10+.

- `cost_model.py`: the week 1 capacity function (given, with the budget scaled to the tick rate), the lecture's baseline constants, and TODOs for `cost_terms`, `shares`, `lever_saving`, `ceiling`, `spot_fill_limit` and `blended_price`. It has `--check`, `--levers` and `--sweep` modes.

## Steps

1. **By hand first.** Before writing code, compute the network term for 6,000 B/s at $0.08 per GB and the compute term for 8 zones of 938 players at 50% fill on a $0.40 server. Write both in your report with units at every step.
2. **The model.** Implement the six TODO functions and run `python cost_model.py --check` until it prints `all checks passed`. Then run `--levers` and paste the table.
3. **The share rule.** For each of the four levers, compute the saving two ways: directly with `lever_saving`, and with `ceiling(share, factor)`. They agree exactly for the network levers and not for the speed-up. Explain the disagreement in at most three sentences. (Hint: does a 3× faster server give 3× the capacity? Look at week 1.)
4. **Where compute takes over.** Run `--sweep cost.csv` and plot the three terms against tick rate as a stacked area chart (any tool). Then find, by editing the call or writing a short loop, the bytes per client at which compute becomes the largest term at 128 Hz. Report the value to the nearest 100 B/s.
5. **Spot, honestly.** For the baseline, compute the total when 60% of the fleet runs on spot at a 70% discount, with fill at 50% and again at the spot limit for `q = 0.25`. Then do the same for the shooter from the lecture's check question 3. State in two sentences why spot is worth the engineering for one game and not the other.
6. **Your cost plan.** A free-to-play MMO has these measured numbers: 20 Hz tick, `h = 0.15` at evening peak, 9,000 B/s per client, $0.07 per GB egress, $0.40 per server-hour, 8 zones per server, 55% fill, $0.35 per 1,000 player-hours in services, and 30,000 average CCU. The team has three proposals: (a) a 2× server speed-up, (b) a 30% byte cut from field LOD, (c) a committed-use contract that cuts the server price by 35%. Write a one-page plan: monthly cost today, the saving of each proposal in dollars per month, your ranking, and the player price of each.

## Deliverable

Your finished `cost_model.py`, `cost.csv`, the chart from step 4, and a report (PDF or Markdown, at most three pages) with the hand calculations from step 1, the lever table, the answers to steps 3 to 5 and the plan from step 6. Submit before the week 14 lecture.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Model code | `--check` passes; hand calculations agree with the code to three decimals | Passes after patching a constant to fit a test | Fails the check | 20% |
| Share rule | Both methods reported; the speed-up gap explained with the square-root capacity law | Numbers present, explanation vague | Step skipped | 15% |
| Tick-rate analysis | Stacked chart; crossover byte rate found and checked by hand | Chart present, crossover missing or unchecked | No chart | 15% |
| Spot analysis | Both games priced; fill limit applied; the share of compute named as the reason | Numbers present for one game only | Step skipped | 15% |
| Cost plan | Monthly dollars for today and each proposal; ranking follows from the numbers; a player price named for each | Numbers present, ranking or prices partly unjustified | Plan missing or copied from the lecture | 30% |
| Writing | Plain, one idea per paragraph, units everywhere | Mostly clear | Hard to follow | 5% |
