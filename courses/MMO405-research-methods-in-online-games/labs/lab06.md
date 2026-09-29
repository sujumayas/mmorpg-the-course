# MMO405 · Lab 06: From interview guide to reliable codes

**Week:** 6 ([Qualitative methods: interviews](../lectures/w06-qualitative-methods-interviews.md))
**Time:** 2 hours in lab plus up to 3 hours at home
**Counts toward:** methods labs (30%); the guide and consent text go into your proposal (20%)
**Work:** in pairs for coding (steps 3 to 6); the interview guide (steps 1 and 2) is individual

## Objective

You will write an interview guide for your own research question and pilot it in a role-play. Then, with a partner, you will code invented interview excerpts, measure your agreement with the statistics from the lecture, and revise a codebook until a rare code is applied reliably. You will see the week's worked example in your own numbers: two codes with the same percent agreement and very different kappas.

## Starter materials

All in [`lab06-starter/`](lab06-starter/README.md). Python 3.10 or later, standard library only.

- `interview-guide-template.md`: the structure for your guide, with consent and distress notes.
- `excerpts.csv`: 40 invented excerpts from interviews with former guild members of an invented MMO.
- `prior_codes.csv`: a previous team's codes for the same excerpts, from two coders (`_a`, `_b`) for two codes (`schedule`, `harassment`).
- `codebook-v1.md`: that team's codebook, with brief definitions only.
- `agree.py` holds five functions to write: `table_2x2`, `percent_agreement`, `cohen_kappa`, `specific_agreement` and `pabak`. `load_codes` and the report are written for you.
- `check_lab06.py` prints PASS, FAIL or TODO per function.

```
python agree.py
python check_lab06.py
```

## Steps

1. **Interview guide (30 min, individual).** Fill in `interview-guide-template.md` for the interpretive question in your project proposal. Your main questions must ask about specific episodes, not opinions. Name your sampling strategy and the bias of your recruitment route.
2. **Role-play pilot (15 min, pairs).** Interview your partner for 10 minutes using your guide. Your partner plays an invented player persona that they make up on the spot. Don't use real experiences, real names or real character names, so no personal data is collected. Swap. Afterwards, write down two questions that didn't work and how you changed them.
3. **Functions (25 min).** Write the five functions in `agree.py` until the checker passes.
4. **The previous team's agreement (10 min).** Run `python agree.py`. Record both codes' tables and statistics in `RESULTS.md`. In three sentences, explain why the two codes have the same `p_o` and different kappas, using `p_e` and `p_pos`.
5. **Revise the codebook (20 min).** Read the three excerpts on which the previous team disagreed about harassment (find them in `prior_codes.csv`). For each, decide what the right code is and why. Then write `codebook-v2.md` with a full entry for each code: name, brief definition, full definition, when to use, when not to use, example. Every harassment disagreement must be settled by a line in "when to use" or "when not to use".
6. **Code it yourselves (25 min).** Each partner codes all 40 excerpts independently with `codebook-v2.md`, without conferring. Put your codes in `mine.csv` with the same columns as `prior_codes.csv` (you are coder `a` and your partner is `b`). Run `python agree.py mine.csv`. Before you run it, write down the harassment kappa you will accept as adequate and one sentence saying why. Record the results next to the previous team's.
7. **Reliability report (at home).** Write 400 to 600 words for a methods section. Give both codes' tables, kappa, `p_pos` and `p_neg`, before and after your revision. Explain whether your study needs inter-rater reliability at all, citing the lecture's guidance, and what you would do with the harassment code if you were writing the full study (for example, how to build a reliability set with enough positive cases).

## Deliverable

One folder named `lab06-<name1>-<name2>` containing each partner's `interview-guide.md` with the pilot notes from step 2, `agree.py` (passing `check_lab06.py`), `codebook-v2.md`, `mine.csv`, `RESULTS.md` (steps 4 and 6) and `reliability.md` (step 7).

## Rubric (20 points)

| Criterion | Excellent (full) | Adequate (half) | Missing or wrong (0) | Points |
|---|---|---|---|---|
| Interview guide and pilot | Episode-based questions with probes; sampling strategy and recruitment bias named; consent and distress notes complete; two concrete revisions from the pilot | Guide complete but questions mostly opinion-based, or revisions vague | Missing | 5 |
| Code passes the checker | All five PASS | Four PASS | Three or fewer | 3 |
| Explaining the paradox (step 4) | Same `p_o`, different κ explained through `p_e` and `p_pos` with the numbers | Correct statement without numbers | Missing or wrong | 3 |
| Codebook revision (step 5) | Every disagreement settled by an explicit rule; entries complete in the lecture's format | Entries complete, some disagreements not addressed | Missing | 5 |
| Reliability report (steps 6 and 7) | Threshold set before measuring; before and after tables; a reasoned position on whether IRR fits the study; a plan for rare-code positives | Numbers reported without a position or plan | Missing | 4 |
