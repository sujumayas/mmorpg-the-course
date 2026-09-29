# GD202 · Lab 07: The drop-rate tax

**Week:** 7, quest types and redeeming them ([lecture](../lectures/w07-quest-types-and-redeeming-them.md)).
**Time:** 2 hours in lab, plus up to 2 hours at home.
**Weight:** part of the dialogue exercises (40%). The redesigned quest goes into your final quest chain.

## Objective

Build a calculator that prices a collect quest in kills and minutes, including its unlucky tail. Use it to audit a small starter zone, then redesign the worst quest twice: once with numbers, once with a different verb.

## Starter materials

All in [`lab07-starter/`](lab07-starter/). Standard-library Python.

- [`quest_effort.py`](lab07-starter/quest_effort.py), a skeleton with an argument checker, a CSV loader and five TODO functions: `expected_kills`, `sd_kills`, `prob_done_by`, `percentile_kills` and `same_mean_designs`.
- [`quests.csv`](lab07-starter/quests.csv), a five-quest starter zone with `n`, `p` and seconds per kill for each quest.
- [`test_quest_effort.py`](lab07-starter/test_quest_effort.py), tests built from the lecture tables: the five same-mean designs with their median, P90 and P99; mean and SD values; the exact binomial tail for small cases; argument checks.
- The [interactive](../examples/w07-drop-rate-tax.html) for spot checks.

Run the tests from inside the starter folder with `../../../../.venv/bin/python test_quest_effort.py`. They all fail on the starter. They all pass once your functions are correct.

## Steps

1. **Mean and spread.** Implement `expected_kills(n, p) = n / p` and `sd_kills(n, p) = sqrt(n(1 − p)) / p`. Call `check_args` first in both.
2. **The tail.** Implement `prob_done_by(k, n, p)`, the chance of at least `n` drops in `k` kills. Use `math.comb`. Return 0 when `k < n`.
3. **Percentiles.** Implement `percentile_kills(n, p, q)`, the smallest whole `k` with `P(K ≤ k) ≥ q`. Use the tolerance given in the docstring.
4. **Same-mean designs.** Implement `same_mean_designs(mean, ns)` and use it to regenerate the lecture's five-row table for a mean of 20 and then for a mean of 40.
5. **Tests.** Run the test file until every test passes.
6. **Audit the zone.** Run `quest_effort.py`. For each quest in `quests.csv`, record the mean time and the P90 time in minutes. Mark the quest with the largest gap between the two.
7. **Redesign A, numbers only.** Change `n` and `p` for the worst quest so that its mean time stays within 10% of the original and its P90 time falls by at least 30%. Report the new numbers.
8. **Redesign B, verb.** Keep the NPC's motivation, but change the atomic-action sequence (see the lecture's checklist). Write the new quest giver line (at most 40 words) and objective line, and give the new quest's expected time with a short justification of your estimate.
9. **Price it.** Your zone pays 1 reward point per minute of mean time. Compute how much the unlucky tenth of players is underpaid on the original worst quest (P90 time minus mean time, in points). State whether you would price from the mean or the P90 and why.

## Deliverable

Your completed `quest_effort.py` with passing tests, and a report of at most 600 words with the audit table (step 6), both redesigns (steps 7 and 8) and the pricing paragraph (step 9).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Calculator correctness | All tests pass; code is readable and uses the model's names | Tests pass with hard-coded shortcuts or unclear code | Tests fail | 30% |
| Zone audit | Table complete, worst quest identified by the mean-to-P90 gap | Table complete, reasoning for the worst quest missing | Table incomplete or wrong | 15% |
| Redesign A | Meets both targets, numbers shown and checked | Meets one target | Misses both | 20% |
| Redesign B | Motivation kept, verb changed, new cost named, line reads well aloud | Verb changed but motivation drifts or cost missing | Reworded only | 25% |
| Pricing argument | Uses the computed underpayment and takes a clear position | Position stated without numbers | Missing | 10% |
