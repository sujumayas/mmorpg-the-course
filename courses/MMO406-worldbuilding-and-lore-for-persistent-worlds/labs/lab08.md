# MMO406 · Lab 08: Canon fit

**Week:** 8 ([lecture](../lectures/w08-player-agency-vs-canon.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** individual code, then pairs for the policy review.
**Counts toward:** exercises (40%). The canon policy becomes the canon section of your world bible.

## Objective

Implement the canon-fit model, see how player types change who carries the contradictions, and write a canon policy for your setting with a fit check for your first expansion.

## Starter materials

All in [`lab08-starter/`](lab08-starter/). Standard-library Python 3, run with `.venv/bin/python` from the repository root or any Python 3.9+.

- [`canon_fit.py`](lab08-starter/canon_fit.py), a skeleton with ten functions to write: `fit`, `expected_contradictions`, `distribution`, `dissonance_bits`, `best_honor_set`, `take_rates`, `mixture_distribution`, `mixture_fit`, `per_type_expected` and `load_choices`. Docstrings give the exact rules, including tie-breaking.
- [`choices.csv`](lab08-starter/choices.csv), the lecture's five invented choices and take rates. Replace them in Part C.
- [`test_canon_fit.py`](lab08-starter/test_canon_fit.py), seven tests using the lecture's numbers. All fail on the starter. Run them from the starter folder with `../../../../.venv/bin/python test_canon_fit.py`.
- The [interactive](../examples/w08-canon-fit.html) for spot checks.

## Steps

### Part A: fit and budget (35 min)

1. Implement `fit`, `expected_contradictions`, `distribution`, `dissonance_bits`, `best_honor_set` and `load_choices`. Running `python canon_fit.py` must print the lecture's fit (0.111), distribution and best honor set.
2. For the lecture's five choices, compute the fit for every possible honor set of size 2 (there are 10). Rank them. Confirm that `best_honor_set` picks the top one, and report how much worse the worst size-2 set is.
3. Prove in at most five lines, using the log view, that honoring the smallest `p_i` is always the best choice for a budget of one. Then explain why the same greedy rule is also best for any budget.

### Part B: player types (40 min)

4. Implement `take_rates`, `mixture_distribution`, `mixture_fit` and `per_type_expected`. Run all tests.
5. Use the lecture's population: 60% loyalists who pick each canon option with probability 0.9, 40% rebels who pick it with 0.3, five choices. Report the fit under independence (from the take rates), the real mixture fit, and each type's expected contradictions.
6. Now "mix the canon": canonize the loyalist-favored option on three choices and the rebel-favored option on two (the second test case in `test_per_type` shows the probabilities). Report the same three numbers. Fit falls. What rises? Write at most 120 words on which canon you would ship and why.
7. Find the honor set of size 2 that minimizes the *larger* of the two types' expected contradictions under the mixed canon from step 6. Is it the same as `best_honor_set`? Explain the difference in two sentences.

### Part C: your canon policy (45 min)

8. Replace `choices.csv` with the choices from your launch story that your first expansion will depend on (at least six). Estimate take rates and justify each in one line. If you believe your players split into types, define at most two and give their probabilities.
9. Assign each choice one of the five answers from the lecture (honor, canonize, absorb, reconcile, delegate) with a total honor budget of two. Report the fit and the distribution, and per-type expected contradictions if you defined types.
10. Write a one-page canon policy for your world bible: the canon layers (world, faction or class, personal), how later content refers to each, the answer for each choice from step 9 with one sentence on how the expansion refers to it, and the defaults a brand-new character inherits.
11. Swap policies with a partner. Each of you finds one choice where you think the other's answer will feel wrong to players, and says why. Revise if convinced.

## Deliverable

- The completed `canon_fit.py` with all tests passing, and your `choices.csv`.
- A report of at most 3 pages: the step 2 ranking, the step 3 argument, the step 5 to 7 results and discussion, and the canon policy from step 10 with your partner's challenge and your response.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Model and budget (Part A) | Tests pass; ranking correct; a correct short argument for the greedy rule | Tests pass, argument incomplete | Tests fail | 25 |
| Player types (Part B) | Numbers correct for both canons; a reasoned choice between fit and fairness; step 7 difference explained | Numbers correct, discussion thin | Missing | 30 |
| Canon policy (Part C) | Six or more choices with justified take rates; every choice has an answer and a concrete reference plan; new-character defaults stated | Policy complete but some answers unjustified | Missing | 35 |
| Peer challenge and clarity | Challenge recorded and answered; numbers traceable to code | Challenge recorded, no response | Missing | 10 |
| **Total** | | | | **100** |
