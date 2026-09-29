# MMO306 · Lab 09: Measuring a dungeon generator

**Week:** 9, procedural and systemic content ([lecture](../lectures/w09-procedural-and-systemic-content.md)).
**Time:** 2 hours in the lab, plus up to 2 hours at home.
**Work mode:** pairs.
**Counts toward:** final dungeon (60%). Any generated element in your dungeon must state its `M_eff` and `n_50` from this lab's tools.

## Objective

Measure how much variety an invented dungeon generator really has, check the birthday-problem model against a simulation, see what validation does to the distribution, and redesign the generator to meet a first-repeat target at the lowest authoring cost.

## Starter materials

All in [`lab09-starter/`](lab09-starter/). Python 3, standard library only.

- [`generator.py`](lab09-starter/generator.py). The generator is given: `AXES` (5 layouts weighted 3 : 3 : 2 : 1 : 1, 4 bosses even, 5 modifiers weighted 4 : 3 : 1 : 1 : 1), a 32-bit decoration seed and a torch count, a validation rule (the Hydra cannot appear in the Library or the Garden) and `generate_valid` with a fallback. Ten functions are yours to write, each with a docstring that states its rule. `report()` prints the lab's numbers once they work.
- [`test_lab09.py`](lab09-starter/test_lab09.py): seven checks, all failing on the starter. Run `python test_lab09.py` inside the folder.
- The [oatmeal meter interactive](../examples/w09-oatmeal-meter.html) for spot checks.

## Steps

### Part A: the model (40 min)

1. Implement `signature`, `effective_variety`, `perceived_and_effective`, `p_repeat`, `p_repeat_uniform_exact` and `n50`. The checks reproduce the lecture: `M_eff = 85.7` for the lecture generator, 61.8% for five giant bounties, `n_50 = 13.4` for `M = 120`.
2. For the lab's generator, compute `M`, `M_eff` and `n_50` from its inputs. You should get `M = 100`, `M_eff ≈ 59.5`, `n_50 ≈ 9.6`. The raw output count is about `100 × 2^32 × 23`. Write one sentence on why that number doesn't belong in a patch note.

### Part B: simulation and validation (40 min)

3. Implement `measured_m_eff`, `expected_attempts`, `p_more_than` and `first_repeat_median`. Run `report()`.
4. The validator removes 10 of the 100 signatures. Compare the measured `M_eff` of accepted outputs (about 53) with the input value (59.5). Explain the drop in two sentences, naming which signatures lost probability and which gained it.
5. Compare the simulated median first repeat (about 10) with `n_50` computed from the measured `M_eff`. Which input to the formula gives the right answer, and why?
6. Change the validator so the Hydra is also barred from the Mine. Recompute the pass rate, expected attempts, `P(more than 5 attempts)` and measured `M_eff`. Would you now add a fallback layout? Say why with the numbers.

### Part C: redesign on a budget (40 min)

7. Your target: the simulated median first repeat must be at least 16 runs, with no memory rule. Authoring costs, in design-days: a new layout 3, a new boss 5, a new modifier 2, a new salient axis with `v` even values `2v + 2`. Changing weights costs nothing. Find the cheapest design that meets the target. Show `M_eff`, `n_50` and the simulated median for it and for at least two alternatives. (Hint: when you add an axis, pass the new `axes` dict to `first_repeat_median`, so the signature includes it.)
8. Now allow a memory rule. Find the smallest `k` for "not one of the last `k` signatures" that meets the target for the original generator with flattened weights. Write two sentences on what the memory rule costs players, even though it costs no design-days.

## Deliverable

- `generator.py` passing all seven checks.
- A one-page design note to the content lead: the variety table (inputs, accepted, simulated), the validation finding from step 6, your cheapest redesign with its cost and numbers, and your recommendation on the memory rule.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Model functions | All checks pass; lecture values reproduced | One check failing with a diagnosed cause | Several checks failing | 25% |
| Simulation and validation | Measured and input `M_eff` compared correctly; step 6 numbers correct and a fallback decision justified | Numbers right, explanation thin | Validation effect not measured | 25% |
| Redesign | Cheapest design found with cost and three numbers, alternatives compared | Target met but not the cheapest, or numbers missing | Target not met | 30% |
| Memory rule | Smallest `k` found; cost to players named concretely | `k` found, cost vague | Missing | 10% |
| Design note | Plain, numeric, one page | Some vague claims | Hard to act on | 10% |
