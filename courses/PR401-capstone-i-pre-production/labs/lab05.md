# PR401 Lab 05: Test sizing sheet and greenlight evidence table

**Week:** 5 (Prototype 2). **Guide:** [week 5](../lectures/w05-prototype-2.md). **Team lab**, submitted once per team.

## Objective

Size prototype 2's tests so they can answer their questions, fit them in the hours you have, and turn both prototypes into the evidence table you will bring to the week 6 greenlight. You will label each question as discovery or decision, compute the testers and observer hours each needs with players tested in groups, choose between a clean answer and a split budget, and write a stop rule if you look at the data early. The checker confirms the sizing follows from your inputs and fits the budget.

## Starter materials

In [`labs/lab05-starter/`](lab05-starter/):

- `check_sizing.py`. Standard library only. Run it with `.venv/bin/python check_sizing.py sizing.csv`. It prints the sizing for each question and the total observer hours against your budget row.
- `sizing.csv`. *Emberfall*'s two prototype 2 questions and a budget row of 20 observer hours. Q1 is sequential with no stop rule and plans the full 96 testers, so the starter prints `NOT READY` on purpose.

Columns: `p` planning rate, `t` threshold, `lam` problem share (discovery only), `k` group size, `rho` intra-group correlation, `s` observed hours per group, `o` observers, `n_planned` testers you will actually recruit.

## Steps

1. **Warm-up (10 minutes).** Run the checker. Confirm `n₀ = 38.8`, `n = 94` and 12 groups for Q1, as in the guide. Apply the guide's option 3. Set Q1's `n_planned` to 48 (the first 6 groups), write the stop rule from the guide in `stop_rule`, and add a note saying the second 6 groups run only if the stop rule does not fire. The checker should print `PASS` with 15.75 of 20 hours planned.
2. **Update risks.** Rerun the lab 04 checker with prototype 1 results in `risks.csv`. Save the output.
3. **Your questions.** Write one row per prototype 2 question. Label each discovery or decision. A decision row needs a threshold that was committed in week 3 or week 4. Say which commit in `note`.
4. **Planning values.** Take `p` from prototype 1, and say so. Use `rho = 0.2` unless you have a reason. Set `k`, `s` and `o` to what you can run.
5. **Budget row.** Set `hours_available` to your week 5 budget minus build, recruitment, analysis and any other risk's prototype.
6. **Options.** In `options.md`, write at least two options (clean, split, sequential, or a design change) with the checker output for each. Choose one and say why.
7. **Brief.** Write `brief-p2.md` with the question, observable, threshold, the chosen option, and the stop rule if sequential. Commit it before the first group plays.
8. **Run and report.** Run the tests. For each decision question, report `n`, `k`, the Wilson interval at effective size `n / DE`, and the verdict. Estimate `rho` from your data if you have at least four groups, and say whether it was higher than planned.
9. **Evidence table.** Build `evidence.md` in the section 4 format of the guide. Its exposure column must sum to the lab 04 burn-down total after both prototypes.

## Deliverable

In `preproduction/week05/` in the team repository:

- `sizing.csv`, `check-output.txt`, `options.md`, `brief-p2.md`.
- Result reports with raw notes, and `timelog.csv` for prototype 2.
- `evidence.md`, the greenlight evidence table, and the rerun lab 04 checker output it reconciles with.

**Checkable output:** the instructor reruns `check_sizing.py sizing.csv`. It must print `PASS` and exit with code 0. The brief's commit must predate the first test session, and the evidence table's exposure total must equal the rerun burn-down.

## Rubric (25 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 3 | `PASS` on rerun; output saved |
| Question types | 3 | Every question labelled; no rate decided from a discovery sample |
| Sizing inputs | 4 | `p` from prototype 1; thresholds traced to earlier commits; `k`, `s`, `o` realistic |
| Options and choice | 4 | At least two options with numbers; the choice is argued against the budget |
| Stop rule | 3 | Written before the first group; covers every outcome at the look |
| Results | 4 | `n`, `k`, interval at effective size and verdict for each decision; `rho` checked where possible |
| Evidence table | 4 | Every load-bearing claim present; exposure reconciles with the burn-down |
