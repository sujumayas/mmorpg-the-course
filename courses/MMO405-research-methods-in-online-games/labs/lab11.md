# MMO405 · Lab 11: From output to page

**Week:** 11 ([lecture](../lectures/w11-writing-and-presenting-research.md))
**Time:** 2 hours in the lab, plus up to 2 hours to finish the writing.
**Work mode:** individual.
**Counts toward:** methods labs (30% of the course grade). The writing rubric below is the one used for the results and abstract of your final paper (50%).

## Objective

Build the checks a careful reader runs on a paper's numbers, use them on an invented game-study manuscript, then write your own project's results paragraph and abstract so that they pass the same checks.

## Starter materials

- [`lab11-starter/grim_audit.py`](lab11-starter/grim_audit.py), Python 3, standard library only. It provides an exact two-sided p-value for a t statistic (`t_two_sided_p`) and loaders for the manuscript tables. Four stubs:
  - `grim` (TODO 1), the lecture's GRIM check in whole-number arithmetic.
  - `nearest_possible` (TODO 2), the closest possible reported means on each side.
  - `p_consistent` (TODO 3), a statcheck-style comparison of a reported p-value with the one its statistic implies.
  - `audit_means` (TODO 4), which labels each mean consistent, inconsistent or untestable.
- [`lab11-starter/manuscript.md`](lab11-starter/manuscript.md), the method and results extract of an invented paper about one raiding guild, and its tables [`manuscript_means.csv`](lab11-starter/manuscript_means.csv) and [`manuscript_tests.csv`](lab11-starter/manuscript_tests.csv).
- [`lab11-starter/test_grim_audit.py`](lab11-starter/test_grim_audit.py), seven tests. All fail on the starter and pass on a correct solution. From inside `lab11-starter/`, run `python -m unittest test_grim_audit.py` (from the repository root, `.venv/bin/python` is the course Python).
- The interactive [`examples/w11-grim-check.html`](../examples/w11-grim-check.html), once it is built.
- Your own project's analysis output from earlier labs.

## Steps

### Part A: the checker (50 min)

1. Implement TODOs 1 to 4 until all seven tests pass. Run `python grim_audit.py` and paste the audit into your results sheet.
2. Explain why `test_float_edge` exists. Compute `0.29 * 100` in Python and say what a checker that used floating-point division would conclude for `grim(0.29, 100)`.

### Part B: audit the manuscript (40 min)

3. For each inconsistent or untestable mean, give the most likely innocent explanation, using the manuscript text.
4. Subgroup check. The officers' and members' means must combine, weighted by their `n`, into the overall mean. Compute the implied overall raid-enjoyment mean from M2 and M3, and the implied overall loot-fairness mean from M6 and M7. Which overall value is wrong, and by how much?
5. The method says two members skipped the loot-fairness item. Test M5 and M7 again with the `n` the method implies. What do the results say about which sentence of the manuscript is wrong?
6. One reported p-value is inconsistent with its statistic. Is it a small rounding difference or does it change the conclusion at the .05 level? How would you word the result correctly?
7. Write the query you would send the authors through the editor (150 to 250 words). Lead with the checkable facts, ask specific questions, and do not speculate about motives.

### Part C: your own page (30 min in the lab, then at home)

8. Write the results paragraph for your project's main finding (120 to 200 words). Each result: direction, size, interval in words, then statistics in parentheses, with the analyzed `n`.
9. Write a 200-word abstract answering the lecture's five questions.
10. Run the lecture's section 5 pass on both. Run your checker on every mean of integer data you report. Attach the audit output and list anything you changed because of it.

## Deliverable

- `grim_audit.py` passing all seven tests.
- A results sheet: the audit from step 1, and answers to steps 2 to 6.
- The query to the authors (step 7).
- Your results paragraph, abstract and self-audit (steps 8 to 10), two pages at most.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code (steps 1 and 2) | All tests pass; float issue explained with the actual value | Tests pass, explanation vague | Tests fail | 20 |
| Manuscript audit (steps 3 to 6) | Every flag explained; subgroup and skipped-item contradictions found with numbers; p-value issue classified correctly and reworded | Most flags found, reasoning thin | Flags listed without interpretation | 25 |
| Query (step 7) | Factual, specific, courteous; each question answerable by the authors | Specific but accusatory, or courteous but vague | Missing | 15 |
| Results paragraph (step 8) | Direction, size, interval and statistics for each result; `n` stated; no bare "significant" | One element missing in places | Numbers without meaning or meaning without numbers | 20 |
| Abstract and self-audit (steps 9 and 10) | Five questions in 200 words; numbers match the results; audit attached with changes listed | Abstract complete, audit missing | Topic only | 20 |
| **Total** | | | | **100** |
