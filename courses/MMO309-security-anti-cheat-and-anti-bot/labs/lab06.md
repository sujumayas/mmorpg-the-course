# MMO309 · Lab 06: The bot farm ledger

Assigned in week 6 ([lecture](../lectures/w06-botting-economics.md)). Due at the start of week 7. Part of the labs component (30% of the course).

## Objective

Estimate how long bots live in a (synthetic) game from its ban log, turn that into the operator's profit per account, and recommend the cheapest set of changes that makes farming lose money. You will also find out how far the lecture's `W/2` shortcut is from the real wave lag in the data.

## Starter materials

All in [`lab06-starter/`](lab06-starter/):

- `make_ledger.py` writes `bots.csv`, a ban log for 2,000 bot accounts, with seed 309. Columns are `account`, `created_day`, `detected_day` and `banned_day`. Empty cells mean the event had not happened by day 120, when the log ends. The data is invented for practice. The generator's docstring says how it was made, but try the lab before reading it.
- `farm.py`, the file you edit. A CSV loader and five stubs: `margin`, `profit`, `breakeven_d`, `estimate_d` and `mean_wave_lag`. The docstrings give the formulas from the lecture.
- `check_lab06.py`, the checker. Ten checks use the lecture's numbers and a four-account log you can work by hand. Two run on `bots.csv`. Every check fails on the starter and passes on a correct solution.

Standard library only, Python 3.11 or later. From the `lab06-starter` folder run `python check_lab06.py` (in this repository, `../../../../.venv/bin/python check_lab06.py`).

## Steps

1. **The model (20 min).** Implement `margin`, `profit` and `breakeven_d`. Run the checker until the first eight checks pass. Reproduce the lecture's table of profit against `d` for `W = 0, 7, 14` with your own code.
2. **Detection from censored data (25 min).** Implement `estimate_d`. First work the four-account log in the checker by hand, and write down why simply averaging `detected_day − created_day` over detected accounts would overstate `d`. Then run it on `bots.csv`.
3. **The real wave lag (15 min).** Implement `mean_wave_lag`. The lecture assumed a detected bot waits `W/2` days for the next wave. Compare that with the measured lag. Explain the difference in one or two sentences, using how this studio's waves are scheduled.
4. **The farm's profit (10 min).** Run `farm.py`. Using the lecture's card for revenue and costs, and your estimated `d` with the measured lag, what does an operator make per account? Is the farm open?
5. **Levers (30 min).** Find the cheapest combination of changes that makes profit per account negative. You may change `d`, the wave schedule, `A`, `p` and `g`, each with a cost to your studio or its players that you state yourself in one line (for example "phone verification: raises `A` by $8, loses 3% of new players"). Present at least three options as a table with the new profit, and pick one.
6. **Adaptation (at home).** Pick your chosen option and describe how an operator would respond, using section 3 of the lecture. Estimate the operator's new profit after that response. If it is positive again, add a second lever.

## Deliverable

Your completed `farm.py` (checker output pasted into `RESULTS.txt`, all 12 checks passing) and a memo of at most 300 words plus tables to your producer. The memo gives the estimated `d` and lag, the current profit per account, your lever table from step 5, the option you chose, and the operator's likely response from step 6.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Correctness | All 12 checks pass without editing the checker | 9-11 pass | Fewer than 9 | 30% |
| Censoring and lag | Explains why naive averaging is biased and why the measured lag differs from `W/2`, with numbers | One of the two explained | Neither | 20% |
| Lever analysis | Three or more options, each with a stated cost and new profit; choice justified by cost to honest players, not only by profit | Options without costs, or only two | One option or none | 30% |
| Adaptation | Operator response named, re-costed with the model, second lever added if needed | Response named, not re-costed | Missing | 10% |
| Memo | Plain, numbers-first, fits the limit | Complete but long or vague | Missing | 10% |
