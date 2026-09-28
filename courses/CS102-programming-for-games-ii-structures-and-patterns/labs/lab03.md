# CS102 · Lab 03: The chemistry engine

**Week:** 3 · **Time:** 2 hours in the lab plus up to 2 hours at home · **Weight:** one of the weekly labs (labs are 40% of the course)

**Lecture:** [Week 03, interfaces and polymorphism](../lectures/w03-interfaces-and-polymorphism.md)

## Objective

Grow a small element-and-material system twice: once with polymorphism (a class per material) and once as a data table. Count the existing code you had to edit each time, and use those counts to recommend a design for a given content plan.

## Starter materials

All in [`lab03/`](lab03/):

- `chemistry.py`: the lecture's Design B. A `Material` base class with a do-nothing `react`, four materials (Grass, Wood, Metal, Stone), three elements, the allowed `STATES`, and `apply(element, targets)`, which must never be edited. The module docstring states the `react` contract.
- `test_contract.py`: a contract test that finds every `Material` subclass automatically and runs it through every pair of probe elements, including unknown ones like `"wind"` and `"FIRE"`. It checks that `react` returns `str` or `None`, never raises, and leaves `state` in `STATES`. Plus two tests of the starter reactions.
- `scenario.py`: prints what a sequence of elements does to one of every material. Try `python scenario.py fire water`.
- `chemistry_table.py`: a stub for Design C with one table row filled in and a small `TableMaterial` class that reads the table.
- `test_table_agrees.py`: one test that fails on the starter. For each starter material and every pair of starter elements, it requires the class and the `TableMaterial` to return the same description and reach the same state. It passes once `REACTIONS` holds the starter reactions (the first half of step 5).

You need Python 3.11 or later. From the `lab03` folder, run `python -m unittest -v`. On the starter code the contract and starter-reaction tests pass and `test_table_agrees` fails, because the table has one row. Keep `test_contract.py` green at every step; `test_table_agrees` goes green in step 5.

## Steps

1. **Predict (10 min).** You will add three materials (Ice, Oil, Cloth) and one element (Wind). Before writing code, draw the extended grid on paper with every cell filled or marked empty. Using the lecture's table, predict how many existing code units Design A, Design B and Design C would edit.
2. **Design B, materials (30 min).** Add `Ice` (fire melts it to state `"melted"`; nothing else), `Oil` (fire makes it burn, water does nothing to burning oil), and `Cloth` (fire burns it, water wets it, wet cloth doesn't burn). Add any new state to `STATES`. Run the contract test after each class. Record which existing classes or functions you opened.
3. **Design B, element (20 min).** Add `"wind"` to `ELEMENTS`. Wind makes burning grass report "fire spreads faster" and blows dry cloth away (state unchanged, description "is blown away"). Record which existing classes you opened.
4. **Break the contract on purpose (10 min).** Make one `react` raise `KeyError` for unknown elements. Run the contract test and copy the failing subtest name into your notes. Then fix it.
5. **Design C (30 min).** Fill `REACTIONS` in `chemistry_table.py` so that `TableMaterial` reproduces every reaction from steps 2 and 3. You'll need to decide how the table expresses conditions like "not wet". Start with the four starter materials until `test_table_agrees.py` passes, then add your own rows. Write a test file `test_table.py` that extends the shipped check to every material, including Ice, Oil and Cloth, and to sequences that include `"wind"`.
6. **Recommend (at home).** A studio's plan for the next year is 30 new materials, each reacting to 2 elements, and 1 new element that affects 12 materials. A second studio plans 4 new materials and 5 new elements, each affecting 6 materials. Compute existing-unit edits for Designs A, B, B′ and C for each studio and recommend one design per studio.

## Deliverable

A zip or repository link with:

- `chemistry.py` with the three new materials and the new element; `test_contract.py` unchanged and passing.
- `chemistry_table.py` and `test_table.py`, passing, with `test_table_agrees.py` unchanged and passing.
- `NOTES.md`, at most 500 words: your step 1 predictions next to the actual counts from steps 2 and 3; the failing subtest name from step 4; how your table expresses conditions and one reaction it could not express without code; the step 6 calculations and your two recommendations with one reason each.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Design B additions | Three materials and wind work as specified; `apply` untouched; contract test passes unchanged | One reaction wrong, or `apply` edited | Several missing or contract test edited to pass | 30% |
| Design C table | Class and table versions agree on every material and sequence, shown by `test_table.py` | Agree on most; small gaps named | Table incomplete or untested | 25% |
| Edit counts | Predicted and actual counts for both changes, with a sentence on each mismatch | Counts present, mismatches unexplained | Missing | 15% |
| Recommendation | Correct A, B, B′ and C totals for both studios and a recommendation tied to which axis grows | Minor arithmetic errors, sound reasoning | Missing or no reasoning | 20% |
| Contract awareness | Failing subtest recorded and the principle it violates named | Recorded, no principle | Step skipped | 10% |
