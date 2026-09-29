# PR401 Lab 06: Greenlight fit sheet

**Week:** 6 (Greenlight review). **Guide:** [week 6](../lectures/w06-greenlight-review.md). **Team lab**, submitted once per team.

## Objective

Show the panel, with numbers it can rerun, whether your pitched game fits your team in the build window, PR401 weeks 12 and 13 plus PR402 weeks 1 to 8. You will measure your focus factor and plan ratio from PR301, cost your five biggest risks, compute the fit ratio `F` and the tripwire `R*`, and order the cut list that brings `F` to 1.00 or below.

## Starter materials

In [`labs/lab06-starter/`](lab06-starter/):

- `greenlight_fit.py`. Standard library only. Run `python greenlight_fit.py team.csv plan.csv risks.csv`. It prints `C`, `S`, `D`, `E`, `F`, `R*`, the fit ratio if your biggest risk fires, and the model's fit verdict. Then it prints `PASS` or `NOT READY` and exits with code 1 when anything is blank, inconsistent or missing.
- `team.csv`. The *Emberfall* team from the guide, with `declared_F`, `declared_tripwire` and `fit_verdict` left blank.
- `plan.csv`. The *Emberfall* feature list after cuts. One kept feature is missing its pillar.
- `risks.csv`. The six-risk register after both prototypes, as in the guide.

Fit verdicts are `go` (`F ≤ 1.00`), `conditional go` (up to 1.15) and `no-go` (above 1.15). They describe the plan in the files. The panel's decision, which can add conditions, goes in the decision record.

## Steps

1. **Warm-up (10 minutes).** Fill the three blank values in `team.csv` from the guide's section 4 and give the market stall its pillars. Run the checker until it prints `PASS`.
2. **Measure `f` and `R`.** Export scheduled hours, logged task hours, estimated hours and actual hours for every PR301 sprint. Compute `f = logged task hours / scheduled hours` and `R = Σ actual / Σ estimated`. Write the totals in the `*_source` fields. If a sprint has no estimates, leave it out and say so. Keep the course weeks and hours (2 weeks at 8, 8 weeks at 12, so `H = 112`) unless your team agreement differs, and reduce them for any absence already known.
3. **Feature list.** Replace `plan.csv` with every feature your pitch promises, estimated in hours. Split any feature over 80 hours into parts. Mark each with the pillar it serves, or `core` for infrastructure that every pillar needs.
4. **Risk register.** Carry your week 4 and 5 risks into `risks.csv` with probabilities updated by the prototype results, and add any new ones, at least five in all. `loss_h` is the rework if the risk fires. Every trigger must be something the team can observe without opinion: a number, a date, an event.
5. **Compute and cut.** Run the checker with every feature kept. If `F > 1.00`, set `keep` to `no` on the features furthest from the pillars until `F ≤ 1.00`. Record the order in `cut-list.md`, with hours saved per cut.
6. **Worst case.** Read the "if the biggest risk fires" line. If it is above 1.00, name in `cut-list.md` which further cuts would cover it, or say that none can.
7. **Declare.** Enter `declared_F`, `declared_tripwire` and `fit_verdict` and run the checker until it prints `PASS`. For any risk whose full loss the cut list cannot cover, write in `cut-list.md` whether the answer is a cut or a pivot, and what the pivot would be.

## Deliverable

In `preproduction/week06/` in the team repository:

- `team.csv`, `plan.csv`, `risks.csv` and the checker output saved as `check-output.txt`.
- `cut-list.md`: ordered cuts with hours, and the worst-case cover from step 6.
- `decision-record.md`, written after the review: outcome, conditions, dates, owners, and the tripwire.

**Checkable output:** the instructor reruns `greenlight_fit.py` on your three CSV files. It must print `PASS` and exit with code 0.

## Rubric (20 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 4 | `PASS` on rerun; saved output matches |
| Measured inputs | 4 | `f` and `R` come from PR301 data with totals shown; exclusions stated |
| Feature list | 3 | Every pitched feature present, none over 80 h, every kept feature traced to a pillar or `core` |
| Risk register | 4 | Five or more risks, realistic probabilities, hours, owners and observable triggers |
| Cut list | 3 | Ordered by distance from the pillars; hours per cut; worst case covered or named as a pivot risk |
| Decision record | 2 | Every panel condition has a date and an owner; tripwire stated |
