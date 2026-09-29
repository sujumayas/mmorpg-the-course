# MMO404 · Lab 14: Case study teardown

**Week:** 14 · **Time:** 2 hours in lab plus about 5 hours of group work at home · **Weight:** part of the labs (40%)

## Objective

Use the [week 14 lecture](../lectures/w14-case-study-presentations.md) method on your group's case. You implement the inversion that turns a headline into an implied constant, bracket it with a sensitivity sweep, test your hypotheses against sources, and deliver a 12-minute teardown with 5 minutes of questions.

## Starter materials

Folder [`lab14-starter/`](lab14-starter/README.md). Standard library Python only. Run it with `.venv/bin/python` from the repository root or any Python 3.10+.

- `teardown.py`: the lecture's cases, default assumptions and ranges, Norvig's reference costs, and TODOs for `implied_pair_ns`, `implied_player_us`, `speedup_needed`, `nearest_reference`, `sensitivity` and `dominant_assumption`. It has `--check`, `--cases` and `--sweep` modes.
- Your case from the instructor's list, with its primary source.

## Steps

1. **The inversion.** Implement the six TODO functions and run `python teardown.py --check` until it prints `all checks passed`. Then run `--cases` and confirm the lecture's table.
2. **Your headline.** Write your case's headline in one line with its source and era. Add it to `CASES` with its player count, tick rate and game speed. If your case is dominated by per-player work (few players, high tick rate), use `implied_player_us` instead and say why in one sentence.
3. **The bound.** Compute the implied constant and its nearest reference cost. Show the calculation by hand once, with units at each step.
4. **Sensitivity.** Run `--sweep "<your case>" sweep.csv`. Plot the bound against each assumption on a log-scale chart (any tool). Name the dominant assumption and the range you can defend for it from your sources.
5. **What must be true.** List at least three hypotheses that would make the headline possible. For each, cite the evidence and mark it supported, contradicted or open. At least one piece of evidence must come from a primary source.
6. **The talk.** Build your 12-minute presentation using the six-part structure in section 3 of the lecture. Every number on a slide carries its source and era, and every computed number shows its formula.
7. **Peer questions.** During other groups' talks, write down one question for each group from section 5 of the lecture. Hand them in with your deliverable.

## Deliverable

Your finished `teardown.py` with your case added, `sweep.csv`, the chart from step 4, your slides (PDF), and a one-page handout with the headline, the formula, the sensitivity table, the hypotheses with evidence, and a full source list with eras. Submit slides and handout before your presentation slot; submit peer questions at the end of the week.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Inversion code | `--check` passes; hand calculation matches the code; the right term (pair or player) chosen and justified | Passes, but the choice of term is not justified | Fails the check | 15% |
| Bound and sensitivity | Log-scale chart; dominant assumption named with a defended range from the sources | Chart present, range asserted without a source | No sensitivity analysis | 20% |
| Hypotheses and evidence | Three or more hypotheses, each marked with cited evidence, at least one primary source | Hypotheses present, evidence thin or secondary only | Summary of the source with no hypotheses | 25% |
| Sources and accuracy | Every number carries source and era; facts, model results and judgment kept separate; no invented quotes | Minor gaps in eras or labelling | Unsourced numbers or invented quotes | 15% |
| Delivery and answers | On time; formulas visible on slides; answers to questions name the kind of claim and use the sensitivity table | Slightly over time or answers vague | Over by more than 3 minutes, or cannot answer about own numbers | 15% |
| Peer questions | One sharp question per group, aimed at an assumption or a source | Questions present but generic | Missing | 10% |
