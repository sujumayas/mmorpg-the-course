# MMO406 · Lab 07: Lore memory

**Week:** 7 ([lecture](../lectures/w07-lore-delivery-in-mmos.md))
**Time:** 2 hours in the lab, plus up to 3 hours to finish.
**Work mode:** individual code, then pairs for the audit review.
**Counts toward:** exercises (40%). The beat table and assumed-knowledge rule go into the continuity section of your world bible.

## Objective

Implement the knowledge-share model from the lecture, test where its single churn rate misleads, and use it to decide which beats of your own setting a first expansion may take for granted.

## Starter materials

All in [`lab07-starter/`](lab07-starter/). Standard-library Python 3, run with `.venv/bin/python` from the repository root or any Python 3.9+.

- [`lore_memory.py`](lab07-starter/lore_memory.py), a skeleton with seven functions to write: `knowledge`, `half_life`, `needed_r`, `steady_mix`, `two_group`, `load_beats` and `audit`. The `two_group` docstring states the exact monthly update rules.
- [`beats.csv`](lab07-starter/beats.csv), five invented beats with live reach `a` and catch-up reach `r`. Replace them with your own in Part C.
- [`test_lore_memory.py`](lab07-starter/test_lore_memory.py), seven tests using the lecture's numbers. All fail on the starter. Run them from the starter folder with `../../../../.venv/bin/python test_lore_memory.py`.
- The [interactive](../examples/w07-lore-memory.html) for spot checks.

## Steps

### Part A: the model (35 min)

1. Implement `knowledge`, `half_life` and `needed_r`. Check them against the table in section 2 of the lecture.
2. Implement `load_beats` and `audit`. Running `python lore_memory.py` must print one row per beat with its knowledge share at months 12 and 24 for 8% churn.
3. For the beat "The harbor city burns", find the smallest whole-number month at which its knowledge share falls below 25%, and the catch-up reach it would need to stay at 50% at month 18. Report both.

### Part B: two kinds of player (40 min)

4. Implement `steady_mix` and `two_group`. Run all tests.
5. Use short-stay churn 40% a month, long-stay churn 4% a month and `w_short = 0.5`. Compute the steady population's average churn (weight each group's churn by its share). Compare the knowledge share of a temporary beat (`a = 0.8`, `r = 0`) at months 6, 12 and 24 under `two_group` and under the one-rate `knowledge` with the average churn. Put both in one table.
6. Explain in at most 100 words why the two answers differ, using the words "release cohort" and "long-stay". Then say which answer a lore team should plan with and why.
7. Change one assumption in the two-group model that you think is wrong for a real MMO (for example, give long-stay players a higher live reach than short-stay players). Rerun step 5 and report the change in `K(12)`.

### Part C: audit your setting (45 min)

8. Replace `beats.csv` with the eight beats your first expansion depends on most. For each, write the delivery and permanence class from the lecture (temporary, replaced, gated, permanent), and estimate `a` and `r` with a one-line justification.
9. Your first expansion ships at month 18. Using 8% churn, or the two-group model if you can justify its parameters, compute `K(18)` for each beat.
10. Write the assumed-knowledge table: beat, delivery, `K(18)`, assumption (none, "has heard of it", "was there"), action. Every "was there" assumption below `K = 0.5` needs an action: retell, re-release or rewrite.
11. Swap tables with a partner. Each of you marks one beat where you think the other's `r` is too optimistic and says why. Revise if convinced.

## Deliverable

- The completed `lore_memory.py` with all tests passing, and your `beats.csv`.
- A report of at most 3 pages: the step 3 answers, the step 5 table and step 6 explanation, the step 7 change, and the assumed-knowledge table from step 10 with your partner's challenge and your response.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Model (Part A) | Tests for the model pass; step 3 answers correct and shown | Tests pass, step 3 wrong or unexplained | Tests fail | 25 |
| Two-group analysis (Part B) | Table correct; explanation names the release cohort and long-stay effect; a defensible changed assumption with its effect | Table correct, explanation vague or step 7 missing | Missing | 30 |
| Setting audit (Part C) | Eight beats with justified `a` and `r`; every low-`K` "was there" beat has a concrete action | Table complete, some estimates unjustified or actions generic | Missing | 35 |
| Peer challenge and clarity | Challenge recorded and answered; numbers traceable to code | Challenge recorded, no response | Missing | 10 |
| **Total** | | | | **100** |
