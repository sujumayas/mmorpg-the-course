# MMO309 · Lab 11: Dupe response, rollback, trace or ban

Assigned in week 11 ([lecture](../lectures/w11-exploit-response-rollback-vs-ban.md)). Due at the start of week 12. Part of the labs component (30% of the course). About 2 hours in lab and 2 at home.

## Objective

Implement the week 11 model of a dupe response, check it against an item-by-item simulation, and add what the lecture only described in words: refunding honest buyers from the ring's wallets and banning accounts worth a given amount. Then estimate the parameters of a new incident from its first four hours of ledger rows, as you would on the night, and write the runbook rule you would follow for it.

## Starter materials

All in [`lab11-starter/`](lab11-starter/). Standard-library Python 3 only.

- [`dupe_response.py`](lab11-starter/dupe_response.py). The module docstring states the model, including the `trace_refund` policy the lecture only sketched: the team debits up to `wallet` gold from the ring and refunds buyers. Five stub functions marked TODO: `respond`, `ring_net`, `crossover`, `simulate` and `estimate`. `PARAMS` holds the lecture's defaults.
- [`make_log.py`](lab11-starter/make_log.py). Do not edit. `incident_log(seed=11)` returns the ledger rows of a new 20,000-item dupe, 4 hours after it began: for each serial, the hour it left the ring (or `None`) and whether it was bought or is gone. The true `k` and `b` are inside the file. Estimate them from the rows instead of reading them.
- [`test_lab11.py`](lab11-starter/test_lab11.py). Five checks. `respond` must reproduce the lecture's table at `T` = 1/3, 1, 6 and 24 hours. `crossover` must give 23.5 hours for the defaults, about 7.1 with `k = 0.05`, about 14.1 with `b = 0.8`, and `None` when no crossover exists. `trace_refund` and `ring_net` must match the lecture's spec values. `simulate` must agree with the closed form over 20 runs. `estimate` must recover `k` and `b` from the incident log and from a four-row example. Run it from inside `lab11-starter/` with `../../../../.venv/bin/python test_lab11.py`. All five fail on the starter.

## Steps

1. **Closed form.** Implement `respond` and `ring_net`. Reproduce the lecture's table for all seven delays, including the ring-only column.
2. **The crossover and what moves it.** Implement `crossover`. Then halve and double each of `k`, `P`, `w` and `λ` in turn, try `b = 0.3` and `b = 0.9` (doubling a share past 1 makes no sense), and report the crossover each time in one table. Which parameters does your team control before an incident, and which are set by the exploiters or the economy?
3. **Simulate.** Implement `simulate`. At `T = 6`, run 200 seeds with the lecture's `D = 50,000`, then 200 seeds with a small dupe (`D = 500`, `M = 5,000,000`, the same 10% shock). For each, convert the counts into the trace's total harm and report the 10th and 90th percentiles as a share of the mean. Explain in two sentences why the closed form is enough for a large dupe and not for a small one.
4. **Refunds and bans.** Plot the trace-with-refund's honest hours and the ring's net against `wallet` from 0 to 40 million gold at `T = 6`, for `A = 0` and `A = 30` million. Find the smallest `wallet` that makes the ring's net zero when `A = 30` million. Then say where, in real logs, you would look for the ring's gold if it is not in the banned accounts.
5. **The new incident.** Implement `estimate` and apply it to `incident_log()`. Use your estimates with `D = 20,000`, `P = 1,500` and the other defaults. Report the crossover and the three responses at `T = 4`. Would your decision change if your estimate of `b` were off by 0.1 in either direction?
6. **Runbook.** Write the rule you would put in this server's runbook: when to roll back, when to trace with refunds, and the sanction for each tier from the lecture's section 3, sized so that a tier-3 player's net is negative.

## Deliverable

1. Your completed `dupe_response.py`, with all five tests passing.
2. The table from step 2, the percentiles from step 3, the chart from step 4 and the numbers from step 5.
3. A runbook entry of about 300 words for the incident in step 5. State the decision rule with its crossover delay, the refund and debit rule, and the sanction ladder. Include one sentence players could read that explains why honest buyers lose the duped item but get their gold back.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Implementation | All tests pass, code follows the stated model and is readable | Tests pass, some logic unclear | Tests fail | 25% |
| Sensitivity (step 2) | Full table, control question answered with reasons | Table without interpretation | Missing | 15% |
| Simulation (step 3) | Both dupe sizes, percentiles, clear explanation of scale | One size or no explanation | Missing | 15% |
| Refunds and bans (step 4) | Chart, break-even wallet, concrete log sources for moved gold | Chart or number only | Missing | 15% |
| Estimation and decision (step 5) | Estimates, crossover, robustness to `b` discussed | Estimates without a decision | Missing | 15% |
| Runbook entry | Defensible rule with numbers, ladder sized to payoffs, good public sentence | Rule without numbers or sentence | Opinion only | 15% |

<details>
<summary>Instructor check values</summary>

Tested with Python 3.13 on the reference solution.

- `respond` reproduces the lecture: at `T = 6`, rollback 24,000 hours, trace 10,482 hours and 2.80% inflation (harm 66,387), ring-only 6.99%, keeps 34.9 million. `crossover()` returns 23.54. With `k = 0.05` it is 7.09, with `b = 0.8` it is 14.11, with `P = 2,000` about 47.5, and with `P = 1,000` there is none before 48 hours.
- Step 2 crossovers (halved, doubled): `k` 20.8 and 23.8; `P` 47.5 and 10.4; `w` 21.6 and 27.4; `λ` 12.7 and 43.8. `b = 0.3` gives 36.9 and `b = 0.9` gives 8.8. More traceable loot, cheaper items, a lower `λ` or more players online all move it earlier. Strong answers note that the team controls `b` (by logging vendors and crafting) and `λ` (by policy), and can cut `k` to zero with a freeze.
- Step 3: for `D = 50,000` the trace harm's 10th to 90th percentile band is within about 1% of the mean. For `D = 500` it is about ±9%.
- Step 4: at `T = 6` with `A = 30` million, the break-even `wallet` is about 4.94 million gold. With `wallet = 20` million, honest hours fall to about 482 and the net is about −15.06 million.
- Step 5: `estimate(incident_log(), 4)` gives about `k = 0.153`, `b = 0.710`. With `D = 20,000` and `P = 1,500` the crossover is about 19.1 hours. At `T = 4`: rollback 6,000 hours; trace 3,253 hours and 0.53% inflation, harm about 13,877; ring-only harm about 36,645; the ring keeps about 9.16 million. A rollback is the right call at 4 hours and stays so for `b` from 0.6 to 0.8.

</details>
