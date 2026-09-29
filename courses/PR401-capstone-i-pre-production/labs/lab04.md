# PR401 Lab 04: Risk sheet, prototype briefs and result report

**Week:** 4 (Prototype 1). **Guide:** [week 4](../lectures/w04-prototype-1.md). **Team lab**, submitted once per team.

## Objective

Choose your two prototypes by the exposure each one removes per hour, then build and test the first. You will turn load-bearing claims into risks, have someone other than each risk's owner estimate its probability and cost, let the picker choose within your hour budget, write a brief with a kill criterion for each prototype 1 item, and report the result against that criterion. The checker confirms your choices follow from your numbers, or that you have said why they don't.

## Starter materials

In [`labs/lab04-starter/`](lab04-starter/):

- `check_risks.py`. Standard library only. Run it with `.venv/bin/python check_risks.py risks.csv`. Use `--budget` for a different weekly budget and `--skip` to let the picker skip a risk that doesn't fit and try the next one.
- `risks.csv`. The *Emberfall* risks from the guide. R3 was estimated by its own owner and R2 is marked for the wrong prototype, so the starter prints `NOT READY` on purpose.

Also use the interactive [prototype picker](../examples/w04-prototype-picker.html) to try other budgets and estimates.

## Steps

1. **Warm-up (10 minutes).** Run the checker on the starter file. Confirm the guide's ratios and the burn-down totals 224, 140 and 104. The 104 is a forecast; week 6 re-rates it with the prototype results. Fix R3's `estimated_by` and R2's `chosen` column. The checker should print `PASS`.
2. **Risks from claims.** Every load-bearing claim in your claims sheet and every pillar test line from week 3 becomes a row. Add a proposed prototype and its cost `c`, including running the test.
3. **Blind estimates.** Each discipline's primary estimates `p` and `L` for risks owned by another discipline. Commit the numbers before anyone fills the `chosen` column.
4. **Budget.** Compute your team's weekly budget as `n × (8 − 0.25 × (n − 1))` hours unless your charter says otherwise. Pass it with `--budget`.
5. **Pick.** Run the checker. Fill `chosen` to match, or write a reason in `note` for each deviation. Save the output as `check-output.txt`.
6. **Briefs.** For each prototype 1 item, write `brief-Rn.md` with the six parts from section 3 of the guide. Commit it before the build starts.
7. **Build and test.** Keep a time log per item. Book tester sessions on the first day.
8. **Report.** For each item, write `result-Rn.md` using the section 4 format, with raw notes attached. State supported, refuted or unclear.
9. **Update.** Change evidence levels in the claims sheet and add any new risks to `risks.csv`. Rerun the checker and save it as `check-output-after.txt`. The prototype 2 choice may change.

## Deliverable

In `preproduction/week04/` in the team repository:

- `risks.csv`, `check-output.txt`, `check-output-after.txt`.
- `brief-Rn.md` and `result-Rn.md` for each prototype 1 item, and `timelog.csv` with columns `risk,discipline,hours`.
- The prototype itself in `prototypes/p1/` with a README saying how to run it and what was faked.

**Checkable output:** the instructor reruns `check_risks.py risks.csv` with your budget. It must print `PASS` and exit with code 0. Each brief's commit must predate the first build commit for that item.

## Rubric (25 points)

| Criterion | Points | Full marks when |
|---|---|---|
| Checker passes | 3 | `PASS` on rerun; outputs saved before and after |
| Risk coverage | 4 | Every load-bearing claim and pillar test line appears; costs include the test |
| Blind estimates | 3 | `estimated_by` differs from owner throughout; numbers committed before choices |
| Briefs | 5 | One question each; observable; kill criterion; fidelity justified; "will not build" list |
| Result reports | 6 | Result stated against the criterion; raw notes attached; surprises recorded; honest "unclear" when it is |
| Time log | 2 | Actual hours by discipline against `c`, with the gap noted |
| Update | 2 | Claims sheet and risk sheet changed as a result |
