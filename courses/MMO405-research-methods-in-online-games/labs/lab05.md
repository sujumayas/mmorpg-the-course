# MMO405 · Lab 05: Difference-in-differences on a synthetic policy change

**Week:** 5 ([Experiments and quasi-experiments](../lectures/w05-experiments-and-quasi-experiments.md))
**Time:** 2 hours in lab plus up to 2 hours at home
**Counts toward:** methods labs (30%); the design critique becomes the threats-to-validity section of your proposal (20%)
**Work:** in pairs; submit one folder per pair

## Objective

You will estimate the effect of a playtime rule for under-18 accounts in an invented MMO three ways: from pooled telemetry, from minors alone, and by difference-in-differences against two possible comparison groups. You will use a placebo test to decide which comparison group is valid, and then check your estimates against the true model, which you can only do because the data is simulated.

## Starter materials

All in [`lab05-starter/`](lab05-starter/README.md). Python 3.10 or later, standard library only.

- `gen_panel.py` writes `panel.csv` from seed 505: 60,000 invented accounts over weeks −8 to 7, one row per account per week, with `age_band` (`under18`, `18-24`, `25plus`) and `heavy` (1 if the account played more than 4 hours a day on 6 days that week, the definition Zendle and colleagues used). The rule for under-18 accounts starts in week 0, the same week as an expansion for everyone.
- `did.py` holds five functions to write: `weekly_share`, `window_mean`, `did`, `placebo_did` and `odds_ratio`. The windows are fixed at the top of the file: early-pre weeks −8 to −5, pre weeks −4 to −1, post weeks 0 to 3.
- `check_lab05.py` prints PASS, FAIL or TODO per function.

```
python gen_panel.py
python did.py
python check_lab05.py
```

## Steps

1. **Functions (35 min).** Write the five functions until the checker passes.
2. **What a pooled dataset shows (10 min).** Run `did.py`. Record the pooled pre and post heavy-play shares, the change and the odds ratio. Write the one-sentence conclusion analyst 1 from the lecture would draw.
3. **Minors alone (5 min).** Record the minors-only change. Which threat to internal validity makes it unreliable here?
4. **Two comparison groups (20 min).** Record the DiD against `18-24` and against `25plus`, and the placebo DiD for each. Plot (by hand, spreadsheet or any tool) the weekly series for all three bands from week −8 to 7. In three sentences, say which comparison group you trust and why, using the placebo numbers and the plot.
5. **Dilution (15 min).** Using the pooled series, compute what the pooled change would have been if the rule had had no effect at all. (Hint: you can reconstruct the minors' counterfactual from your trusted DiD.) How big is the gap between the actual and counterfactual pooled change, and why is it so much smaller than the effect on minors?
6. **Check against the truth (10 min).** Now open `gen_panel.py` and read `prob()`. Write down the true effect of the rule and the true pre-trend of each band. How close was each of your estimates, and which gap is noise and which is bias?
7. **Design critique (at home).** Write one page (400 to 600 words) as a reviewer of a paper that claims "the rule had no effect" using only the pooled series. Name the design flaw, estimate how large an effect could hide in their data using your step 5 result, and propose a design that would identify the effect with data a studio could realistically collect. State what that design assumes and how the authors should test it.

## Deliverable

One folder named `lab05-<name1>-<name2>` containing `did.py` (passing `check_lab05.py`), `RESULTS.md` with steps 2 to 6 and your plot, and `critique.md` from step 7.

## Rubric (20 points)

| Criterion | Excellent (full) | Adequate (half) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code passes the checker | All five PASS | Four PASS | Three or fewer | 4 |
| Pooled and naive estimates (steps 2 and 3) | Numbers correct; analyst 1's conclusion stated; history named as the threat to the minors-only change | Numbers right, reasoning missing | Missing | 3 |
| Comparison group choice (step 4) | Trusted group chosen from both the placebo and the plot; the other group's failure explained as non-parallel trends | Choice made from one kind of evidence only | Missing or wrong | 5 |
| Dilution and truth check (steps 5 and 6) | Counterfactual pooled change computed; gap explained by group share; noise and bias told apart | Computation right, explanation weak | Missing | 4 |
| Design critique (step 7) | Flaw named precisely; hidden-effect size estimated; proposed design stated with its assumption and a test for it | Critique without a quantitative estimate or without a test | Missing | 4 |
