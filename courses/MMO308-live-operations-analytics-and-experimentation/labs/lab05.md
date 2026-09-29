# MMO308 · Lab 05: Design an experiment for a shared world

**Week:** 5 ([A/B testing: design](../lectures/w05-ab-testing-design.md))
**Time:** 2 hours in lab plus up to 3 hours at home
**Counts toward:** analytics labs (40%); the finished plan is also the design section of the A/B report (20%)
**Work:** in pairs; submit one folder per pair

## Objective

You will build the three tools an experiment designer needs (salted hash assignment, the design effect, and an intraclass-correlation estimate from history), use them to size player, guild and server versions of the same test, and write a complete plan for a change of your choice.

## Starter materials

All in [`lab05-starter/`](lab05-starter/README.md). Python 3.10 or later, standard library only.

- `gen_servers.py` writes `server_history.csv` from seed 505: last month's new players and day-7 retained players on each of 40 servers (60,518 new players in all).
- `design.py` holds six functions to write: `bucket`, `variant`, `design_effect`, `effective_n`, `mde` and `icc_from_clusters`. Each docstring gives the exact formula. `main()` prints a player, guild and server design table once they work.
- `check_lab05.py` prints PASS, FAIL or TODO per function.
- `plan-template.md`, the nine-part plan you hand in.

```
python gen_servers.py
python design.py
python check_lab05.py
```

## Steps

1. **Assignment (20 min).** Write `bucket` and `variant`. Assign player ids 0 to 49,999 to experiment `lab05-test` and count B. Is the split within two standard deviations of 25,000? Then assign the same players to a second experiment name and cross-tabulate. Finally, assign them to two experiments with the **same** name and cross-tabulate again. Record all three results in `RESULTS.md` and explain the last one in one sentence.
2. **Ramping (10 min).** For `lab05-test`, list which of players 0 to 19 are in B at `share_b` = 0.05, 0.2 and 0.5. Show that every player in B at a lower share is still in B at a higher one. Why does this matter when you ramp a test that crashed at 5%?
3. **Design effect (15 min).** Write `design_effect`, `effective_n` and `mde`. Reproduce the lecture's table row for servers with `ρ = 0.01`.
4. **Estimate ρ (25 min).** Write `icc_from_clusters` and run it on `server_history.csv`. Report the baseline, the between-server variance, the binomial noise term and `ρ`. Then run `design.py` and copy the table into `RESULTS.md`. In two sentences, say what the estimate means for a test that must be randomized by server.
5. **How many servers? (15 min).** Using your `ρ` and 5,000 players per server, find the smallest number of servers per arm that detects a 2-point change in D7 at 80% power. Your game has 40. What would you tell the producer who wants a server-level test of a new world boss?
6. **The plan (at home).** Choose one change for an MMO, either your PR301 project or one of the four from the in-class activity. Fill in `plan-template.md` completely. Use your functions for step 7 of the plan and show the arithmetic. Your unit choice must be justified by the interference the change could cause, and your trigger must be an event that happens the same way in both arms.

## Deliverable

One folder named `lab05-<name1>-<name2>` containing your `design.py` (passing `check_lab05.py`), `RESULTS.md` with steps 1 to 5, and `plan.md` from step 6.

## Rubric (20 points)

| Criterion | Excellent (full) | Adequate (half) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code passes the checker | All six PASS | Four or five PASS | Three or fewer | 4 |
| Assignment and ramping (steps 1 and 2) | Split checked against its standard deviation; salt and same-name results explained; ramp monotonicity shown and tied to crash safety | Results without explanation | Missing | 4 |
| ICC and server sizing (steps 4 and 5) | `ρ` estimated with its parts shown; servers needed computed; advice to the producer follows from the numbers | Numbers right, advice missing or generic | Missing or wrong | 4 |
| Plan: unit and trigger | Unit justified by a named interference path; trigger valid in both arms and before the outcome | One of the two weak | Missing | 4 |
| Plan: metrics, sizing and ethics | Primary and guardrails defined exactly; sizing uses `deff`; duration in whole weeks with the metric window added; a real fairness check | Complete but sizing ignores clustering or duration is not whole weeks | Missing | 4 |
