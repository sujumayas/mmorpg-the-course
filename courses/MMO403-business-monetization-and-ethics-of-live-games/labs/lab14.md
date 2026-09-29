# MMO403 · Lab 14: Stage-gate funding plan and pitch

**Week:** 14, pitching to publishers and investors ([lecture](../lectures/w14-pitching-to-publishers-and-investors.md)).
**Time:** 2 hours in lab, plus up to 4 hours at home.
**Weight:** part of the Models strand (40%). The funding plan and deck become the funding section of your final business plan (week 15).

## Objective

Implement the week 14 gate model, the stage-1 design chooser and the valuation arithmetic, check them against the lecture, then turn your lab 13 budget into a staged funding plan with a written go/no-go gate and a ten-slide pitch. By the end you should be able to say how much your first stage costs, what it proves, the false-go rate at which your plan stops being worth funding, and what you will do after a "stop".

## Starter materials

All in [`lab14-starter/`](lab14-starter/). Standard-library Python 3.10 or later.

- [`stage_gate.py`](lab14-starter/stage_gate.py), with an options loader and nine empty functions: `ev_all_in`, `ev_gated`, `kill_rate`, `posterior_hit`, `breakeven_f`, `best_stage1`, `post_money`, `pre_money` and `founder_share`. Each docstring gives the exact rule.
- [`stage1_options.csv`](lab14-starter/stage1_options.csv), the lecture's three stage-1 designs (prototype, vertical slice, soft launch).
- [`test_stage_gate.py`](lab14-starter/test_stage_gate.py), eight tests from the lecture: the −5.00 all-in value and +8.50 perfect gate, the realistic-gate table and kill rates, the rule that a funder never continues at a loss, `P(hit | go)`, the break-even false-go rate (including check-yourself question 2), the best stage-1 design before and after the soft launch's price rises to $6M, the Cloud Imperium valuation, and dilution across rounds. Every test fails on the starter.
- Your completed lab 13 budget.
- The interactive [`examples/w14-stage-gate.html`](../examples/w14-stage-gate.html) for spot checks.

Run the tests from inside the folder with `python3 test_stage_gate.py` (or `pytest`). From the repository root use `.venv/bin/python courses/MMO403-business-monetization-and-ethics-of-live-games/labs/lab14-starter/test_stage_gate.py`. The script exits with status 0 only when all eight pass.

## Steps

### Part A: the model (40 min)

1. Implement `ev_all_in`, `ev_gated` and `kill_rate`. Compute the `f = 0.2` row of the lecture table by hand before you run the tests.
2. Implement `posterior_hit` and `breakeven_f`. Derive the break-even formula on paper from `EV_gate = 0`.
3. Implement `best_stage1`, `post_money`, `pre_money` and `founder_share`. Run until all eight tests pass.

### Part B: sensitivity (20 min)

4. For the lecture pitch (`p = 0.25`, `V = 60`, `C2 = 18`), make a grid of `EV_gate` over `p` in {0.10, 0.15, 0.20, 0.25, 0.30} and `f` in {0.05, 0.10, 0.20, 0.30, 0.40} with `C1 = 2`, `s = 0.8`. Mark the cells below zero. Describe the boundary in one sentence.
5. Extend the model with a salvage value `L` for a killed project (tools, tech, a team that can move to another game), added as `k × L`. How large must `L` be for the `f = 0.6` row to break even? Name one real kind of salvage from the lecture's cross-game cases.

### Part C: your funding plan (60 min)

6. From your lab 13 budget, define stage 1 (its cost `C1`, its length and what it builds) and stage 2 (`C2`). State `V` as a range with its source (your week 1 and 2 models).
7. Write the gate. Name one primary metric, its threshold and the date it will be measured, and say who decides. Estimate `s` and `f` for your gate and justify each in two sentences, using MA102 week 14's language of false positives and power.
8. Using a pessimistic, middle and optimistic `p`, report `EV_all`, `EV_gate`, the kill rate and `f*`. Say whether your plan is fundable at each.
9. Propose one alternative stage-1 design (cheaper or more thorough) and compare it with `best_stage1`.
10. If you raise equity, show a two-round table (pre-money, investment, post-money, share sold, founders' share) and explain what the stage-1 result must show to justify the step-up in valuation. If you plan a publisher deal or crowdfunding instead, explain which funder makes the go/no-go decision and when.
11. Write your "stop" plan. What happens to the team, to any players in a test, and to any money players have paid, if the gate says stop.

### Part D: the pitch (at home)

12. Build a deck of at most 12 slides following lecture section 4, including the ask for stage 1 only and a gate slide. Use your own art or plain shapes; no copyrighted game art or logos.
13. Record or rehearse a 5-minute pitch. You will deliver it in the week 15 session.

## Deliverable

- The completed `stage_gate.py` with all eight tests passing.
- A PDF of at most 4 pages: the Part B grid and salvage answer, the Part C numbers in one table, the gate definition, the dilution or funder table, and the stop plan.
- The pitch deck (PDF, at most 12 slides).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Implementation (Part A) | All eight tests pass; hand check and break-even derivation shown | Tests pass, working missing | Tests fail | 20% |
| Sensitivity (Part B) | Correct grid with the boundary described; salvage computed and tied to a real case | Grid correct, interpretation or salvage missing | Missing or wrong | 10% |
| Gate design (steps 7 and 11) | One metric fixed in advance with threshold, date and decider; `s` and `f` justified; humane stop plan covering team, testers and money | Gate present, estimates or stop plan thin | No real gate | 25% |
| Funding numbers (steps 6, 8 to 10) | All three scenarios computed and interpreted; alternative stage 1 compared; dilution or funder logic correct | Middle case only | Numbers missing or wrong | 20% |
| Pitch deck (Part D) | Every slide supports one of the four funder numbers; honest ranges and sources; monetization and regulatory risks stated | Complete but promotional, ranges missing | Incomplete | 20% |
| Honesty | Low-end case shown; comps' survivorship bias acknowledged; no wishful numbers presented as forecasts | Some numbers unsupported | Misleading claims | 5% |
