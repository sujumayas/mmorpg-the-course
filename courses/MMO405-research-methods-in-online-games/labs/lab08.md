# MMO405 · Lab 08: Linking a survey to logs

**Week:** 8 ([Mixed methods](../lectures/w08-mixed-methods.md))
**Time:** 2 hours in lab plus about 2 hours at home
**Counts toward:** methods labs (30%); the design memo becomes the mixed-methods section of your proposal (20%)
**Work:** in pairs; submit one folder per pair

## Objective

You will run an explanatory sequential analysis end to end on invented data. You link survey answers to server logs, decompose a group difference into the true difference and the reporting-bias difference, and apply a written connecting rule to choose interviewees. Then you build a statistics-by-themes joint display from supplied interview summaries and classify each meta-inference as confirmation, expansion or discordance. Along the way you will find that the answer to "who misreports?" depends on which logged measure you call the truth.

## Starter materials

All in [`lab08-starter/`](lab08-starter/README.md). Python 3.10 or later, standard library only.

- `gen_data.py` writes, from seed 808, `telemetry.csv` (1,200 accounts, with total logged hours and active hours excluding idle stretches) and `survey.csv` (respondents with cohort and self-reported hours). Some survey ids do not match any account.
- `interviews.csv` holds 20 short invented interview summaries with theme codes. They are for teaching only and describe no real players.
- `linkage.py` holds six functions to write: `link`, `discrepancy`, `group_summary`, `decompose`, `select_cases` and `theme_table`. Each docstring gives the exact rule. `main()` prints the whole analysis once they work.
- `check_lab08.py` prints PASS, FAIL or TODO per function, plus one check on the generated data.

```
python gen_data.py
python linkage.py
python check_lab08.py
```

## Steps

1. **Link (15 min).** Write `link`. How many respondents link? List the unmatched ids. In one sentence, say what you would do about unmatched records in a real study and what it could bias.
2. **Discrepancy and summary (20 min).** Write `discrepancy` and `group_summary`. Report each cohort's mean reported hours, mean logged hours and bias, first against `logged_total_h`, then against `logged_active_h`.
3. **Decompose (15 min).** Write `decompose`. For both measures, write out `survey gap = log gap + bias gap` with the numbers, and give the share of the logged gap the survey shows. Which cohort "misreports" depends on the measure. Explain in two or three sentences what that tells you about the construct each strand measures.
4. **Connect (20 min).** Write `select_cases` and run it with the default rule (four under-reporters and two accurate reporters per cohort) on `logged_total_h`. Before you run it on `logged_active_h`, predict whether the same people will be chosen. Run it and compare.
5. **Joint display (20 min).** Write `theme_table` and produce the statistics-by-themes table for the `logged_total_h` selection. Then build a side-by-side joint display in `RESULTS.md` with at least three rows (topic, quantitative result, qualitative result, fit, meta-inference), using the lecture's format. At least one row must be a discordance.
6. **Design memo (at home, 400 to 500 words).** For your own proposal topic, write the mixed-methods section. Give the design in Morse notation, the purpose (Greene and colleagues' term), both strands, the integration method and the exact step at which it happens, your connecting or building rule written in advance, the joint display you will produce, and one result from the first strand that would change the second. Add two sentences on the ethics of linking your data (consent and identifiability).

## Deliverable

One folder named `lab08-<name1>-<name2>` containing `linkage.py` (passing `check_lab08.py`), `RESULTS.md` with steps 1 to 5, and `memo.md` from step 6.

## Rubric (20 points)

| Criterion | Excellent (full) | Adequate (half) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Code passes the checker | All seven checks PASS | Five or six PASS | Four or fewer | 4 |
| Decomposition (steps 2 and 3) | Identity written out for both measures; shares computed; the measure-dependence explained as a construct mismatch | Numbers right, explanation missing or generic | Missing or wrong | 4 |
| Connecting (step 4) | Prediction stated before running; the change in selection explained by the measure | Selection shown without prediction or explanation | Missing | 3 |
| Joint display (step 5) | Participant counts correct; three or more rows each with a named fit; a real discordance identified and a next step proposed | Display present but fits unnamed or no discordance | Missing | 4 |
| Design memo (step 6) | Notation, purpose, strands, integration step and advance rule all present; the "what would change" result is specific; linking ethics addressed | One or two elements missing or vague | Missing | 5 |
