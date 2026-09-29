# MMO309 · Lab 12: A sanction policy with an error budget

Assigned in week 12 ([lecture](../lectures/w12-legal-and-ethical-considerations.md)). Due at the start of week 13. Part of the labs component (30% of the course), and a building block for the threat model assessment. About 2 hours in lab and 2 at home.

## Objective

Measure three detection signals on labelled data, find out whether they are independent, and write a four-rung sanction policy whose cost ratios are stated in writing and whose expected innocent sanctions per million players you can defend. The lecture assumed independence. This data breaks that assumption for one pair, and your policy has to cope.

## Starter materials

All in [`lab12-starter/`](lab12-starter/). Standard-library Python 3 only.

- [`make_accounts.py`](lab12-starter/make_accounts.py). Do not edit. `make_accounts(n=200_000, seed=12)` returns labelled accounts with three boolean signals: `aim` (aim-snap detector), `reports` (three or more player reports) and `hash` (known cheat file). About 1% of accounts cheat. The rates are close to the lecture's.
- [`policy.py`](lab12-starter/policy.py). Six stub functions marked TODO: `rates`, `dependence`, `posterior`, `threshold`, `allowed` and `rule_rates`. The docstring states the model. Running it prints a summary once the stubs work.
- [`test_lab12.py`](lab12-starter/test_lab12.py). Four checks: the lecture's posterior values and ladder, measured rates in the expected range, the dependence ratios, and rule rates that expose the double counting. Run it from inside `lab12-starter/` with `../../../../.venv/bin/python test_lab12.py`. All four fail on the starter.

## Steps

1. **Implement the model.** Fill in the six functions until the tests pass. Run `policy.py`.
2. **Measure.** Report TPR, FPR and LR for each signal, with the count of accounts behind each rate. Which rate rests on so few events that you would not trust its second digit?
3. **Test independence.** Compute the dependence ratio for every pair of signals, separately for cheaters and honest players. Name the pair that is not independent and say which group it matters for, and why that group is the one that decides false positives.
4. **See the damage.** For the rule "aim and reports", compare the innocents per million the lecture's independence formula predicts (`990,000 × FPR_aim × FPR_reports`) with what `rule_rates` measures. Compute the effective LR of the pair from the data (TPR and FPR of the combined rule) and compare with the product of the separate LRs.
5. **Write the ladder.** Define four sanctions of your choice, from a reversible restriction to a permanent ban, and set `C` for each in writing with one sentence of justification. For each sanction, list which signal combinations clear its threshold using the measured combined rates, not the independence product.
6. **Budget.** Report, for each rung, cheaters caught and innocents hit per million players. Set an error budget for the permanent ban (for example, at most 1 innocent per million per season) and check your rule against it. With 200,000 accounts, how confident can you be about a rate near 1 per million? Say what you would need to measure it.
7. **Base-rate shift.** Rerun your posterior calculations for a population where only 0.2% cheat (a casual queue). Which rungs does each combination still clear?

## Deliverable

1. Your completed `policy.py`, with all tests passing.
2. The tables from steps 2 to 6.
3. A policy memo of about 400 words that a lawyer and a community manager could both read. It states the four sanctions and their `C` values, the evidence each requires, the expected innocents per million at each rung, the human review and appeal route for the top two rungs, and what data you keep and for how long.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Implementation | All tests pass, functions short and correct | Tests pass, some awkward code | Tests fail | 20% |
| Measurement and independence (steps 2-3) | Rates with counts, weak rates flagged, dependent pair found and explained for the right group | Pair found, explanation thin | Pair missed | 20% |
| Double counting (step 4) | Predicted vs measured compared, effective LR computed and interpreted | Comparison without effective LR | Missing | 15% |
| Ladder and budget (steps 5-6) | Written `C` values with reasons, rungs mapped to measured combinations, budget checked with an honest note on sample size | Ladder without reasons or budget | Missing | 25% |
| Memo | Readable by both audiences, includes review, appeal and retention | Covers the ladder only | Unclear or missing | 20% |

<details>
<summary>Instructor check values</summary>

Seed 12, 200,000 accounts, reference solution, Python 3.13.

- Measured rates: aim TPR 0.904, FPR 0.0097, LR about 93. Reports TPR 0.480, FPR 0.0504, LR about 10. Hash TPR 0.617, FPR 0.0010, LR about 590. The hash FPR rests on about 200 honest accounts and the combined rules below rest on far fewer, so students should flag them.
- Dependence of aim and reports: about 6.2 among honest players, about 1.05 among cheaters. It matters for honest players, because false positives are drawn from them.
- Rule "aim and reports": about 4,470 cheaters caught and 2,980 innocents per million, against the independence prediction of about 495 innocents per million. The effective LR of the pair is about 150 (TPR about 0.45, FPR about 0.003), not the product of about 900. At a 1% base rate that gives P(cheat) of about 0.60, so under the lecture's ladder the pair justifies only the lowest rung, not the 7-day suspension the lecture computed.
- Rules that include the hash show 0 innocents in the sample. Good answers say that 0 in about 198,000 honest accounts does not show a rate of 0, and that bounding a rate near 1 per million needs millions of labelled honest accounts or a separate audit.

</details>
