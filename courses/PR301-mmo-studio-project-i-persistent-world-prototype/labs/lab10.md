# PR301 Lab 10: Ledger reconciliation sheet

**Week:** 10 (Telemetry review). **Guide:** [week 10](../lectures/w10-telemetry-review.md). **Team lab**, submitted once per team.

## Objective

Prove where every coin in your world came from. You compare the weekend's ledger with the week 7 budget per player-hour, compute the money supply from every place currency can live, and explain the residual between the two until nothing of any size is left. Every explanation must carry evidence and predict its own size.

## Starter materials

In [`labs/lab10-starter/`](lab10-starter/):

- `check_ledger.py`. Standard library only. Run it with `.venv/bin/python check_ledger.py ledger.csv snapshot.txt explanations.csv findings.csv`. It prints the budget table with ratios, flags every line outside 0.75 to 1.25 of budget, computes money supply and the residual, subtracts your explanations and prints what is left. The tolerance is 10 or 0.1% of the money supply, whichever is larger. Then it prints `PASS` or `NOT READY` (exit code 1).
- `ledger.csv`, `snapshot.txt`. The *Saltmarsh* weekend from the guide.
- `explanations.csv`. Two of the three causes, one of them without evidence.
- `findings.csv`. One finding filled in, one blank, one missing.

## Steps

1. **Warm-up (15 minutes).** Run the checker on the starter files. It reports four problems. Complete the explanations and findings from the guide, including the rounding and its size check (`sales × 0.475`), until it prints `PASS`.
2. **Count checks first.** On your own exports, count sequence gaps per server, sessions closed at crash time and bot accounts excluded. Write them at the top of `reconciliation.md`. Exclude bot characters' ledger lines before you total anything.
3. **Your ledger.** Sum the ledger by reason code for human characters and enter the totals in `ledger.csv` with your week 7 budget rates. Enter human player-hours from session telemetry in `snapshot.txt`.
4. **Your money supply.** From the final backup, sum currency in every place it can live (your lab 07 list) and enter each as a `place.` line.
5. **Decompose the residual.** Compute it by hour and by character (a query per character: final balance minus the sum of that character's ledger deltas). Look for drift, steps and outlier characters. Enter each cause in `explanations.csv` with its amount and the evidence that sizes it: a query result, a timestamp match, a count times a unit amount.
6. **Findings.** For every budget line outside 0.75 to 1.25, write one finding: a bug, a design leak, or a guess replaced by a measurement.
7. **Run the checker** until it prints `PASS`. If a residual cannot be explained, do not force it. Leave it, say so in `reconciliation.md`, and open an S1.
8. **Response.** In `reconciliation.md`, record what you corrected (with `S_GM_CORRECTION` ledger lines), what you fixed, and what happened to any players involved under your week 9 policy.

## Deliverable

In `production/week10/` in the team repository:

- `ledger.csv`, `snapshot.txt`, `explanations.csv` and `findings.csv` that pass `check_ledger.py`, with its output saved as `check-output.txt`.
- `reconciliation.md`: count checks, the residual by hour and by character (tables or charts), the reasoning for each explanation, and the response.
- The queries you used, in `production/week10/queries/`.

**Checkable output:** the instructor reruns `check_ledger.py` on your four files. It must print `PASS` and exit with code 0. The instructor also reruns one of your per-character queries against the final backup.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 3 | `PASS` on rerun, output file matches |
| Count checks | 3 | Sequence gaps, closed sessions and bot exclusion reported before any total |
| Money supply | 3 | Every place from the lab 07 list is included, from the final backup |
| Decomposition | 5 | Residual shown by time and by character; each cause's size predicted independently and matching |
| Findings | 3 | Every out-of-band line explained; guesses replaced by measurements in the updated budget |
| Response | 3 | Corrections logged as ledger lines; class-of-bug fix ranked above instance fixes; player response follows the week 9 policy |
