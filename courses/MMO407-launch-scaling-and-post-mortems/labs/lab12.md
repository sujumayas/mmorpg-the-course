# MMO407 · Lab 12: A launch post-mortem that survives a comparison

**Assigned:** week 12 ([lecture](../lectures/w12-writing-a-post-mortem.md)). **Due:** start of week 13 class. **Feeds:** the case analyses (50%) and the post-mortem analysis in the final (week 15).

## Objective

Write a launch post-mortem whose lessons are graded by evidence. You will compute contrast ratios for six factors over 40 invented launches, show how the ranking by frequency differs from the ranking by contrast, and then write a full post-mortem for one troubled launch using the lecture's section 3 template, with every lesson checked against the comparison set.

## Starter materials

The folder [`lab12-starter/`](lab12-starter/) contains:

- [`launches.csv`](lab12-starter/launches.csv), 40 invented launches (20 troubled, 20 smooth) with six yes/no factor columns. "Troubled" means day-30 players below 70% of forecast or a severity-1 incident longer than four hours.
- [`contrast.py`](lab12-starter/contrast.py), your file. It loads the data and has three TODOs: `counts`, `contrast` (with the add-one-half option) and `rank`. `biggest_rank_change` is provided.
- [`test_contrast.py`](lab12-starter/test_contrast.py), four tests. All four fail on the starter.
- [`launch_T01.md`](lab12-starter/launch_T01.md), the case file for launch T01: the plan's forecasts, what happened, a UTC timeline and the team's raw retrospective notes.

Standard library only. Run everything with the course Python from inside the starter folder:

```
cd labs/lab12-starter
../../../../.venv/bin/python -m unittest test_contrast.py
../../../../.venv/bin/python contrast.py
```

When the TODOs are done, the report prints a table of six factors with `a / n_T`, `b / n_S`, `f_T`, `f_S` and `L`, the two rankings, and the factor whose rank changes most. The first four rows match the lecture's table.

## Steps

1. **Contrast library (30 min).** Implement TODOs 1 to 3. All four tests should pass. In the report, check one row by hand and explain in two sentences why `biggest_rank_change` returns the factor it does.
2. **Noise (20 min).** For the factor with the highest `L`, recompute `L` after moving one smooth launch into or out of the factor (so `b` changes by one) in each direction. Do the same for the factor with `L` closest to 1. Which verdicts from the lecture's teaching thresholds (below 1.5, 1.5 to 3, above 3) survive a one-launch change?
3. **Sort the notes (20 min).** Take the eight raw notes at the end of `launch_T01.md`. For each, write whether it is a choice made before launch, a symptom during it, or not a factor at all (a feeling or an instruction). Map every choice to a column in `launches.csv` where one exists.
4. **Plan against actual (30 min).** Build the plan-against-actual table for T01 with an error column and the model each forecast came from. For the peak-queue row, use week 2's model in words to say which two input errors explain most of the gap, and in which direction each pushed.
5. **Counterfactuals (30 min).** For three contributing factors, write a counterfactual with a number. At least one must use week 1's pipeline model (the account service saturating at about 700 per minute while 1,450 per minute arrived). Example of the form: "Had the account service been load-tested and sized to 1,500 per minute, the first-hour backlog in front of it would have been about ... instead of ...; the bottleneck would have moved to ..."
6. **Write the post-mortem (60 min).** Use the lecture's section 3 template in full: scope and sources, plan against actual, timeline (trimmed to the decisions), what went right and wrong, contributing factors with counterfactuals, at least four lessons each graded A, B or C with the counts from step 1 where they apply, and at least three actions with owner role, date and metric. Keep it blameless, and note one place where hindsight could mislead a reader and how you guarded against it.

## Deliverable

A zip or repository link containing:

- Your `contrast.py` with all tests passing (paste the test output in the report).
- `report.md`, 400 to 600 words: the step 1 check and explanation, the step 2 noise table and verdicts, and the step 3 sorting.
- `postmortem-T01.md`, 1,200 to 1,800 words, the full post-mortem from steps 4 to 6.
- Every number reproducible from a command you list or a row in the case file.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing or wrong (0) | Weight |
|---|---|---|---|---|
| Tests and contrast table | All four pass; hand check correct | Three pass | Two or fewer | 15% |
| Noise analysis | One-launch changes computed both ways for both factors; verdicts judged correctly | Computed, verdicts not discussed | Not done | 10% |
| Causes and symptoms | All eight notes classified defensibly; choices mapped to data columns | Most classified; mapping partial | Notes copied as lessons | 10% |
| Plan against actual | Every forecast row with error and source model; queue gap traced to arrivals and session length | Table complete, gap not traced | Table incomplete | 15% |
| Counterfactuals | Three with numbers, one from the week 1 model, each changing one thing | Numbers on two | No numbers | 15% |
| Lessons and actions | Four lessons graded honestly, counts cited, a factor with `L` near 1 explicitly not promoted to a lesson; three owned actions with metrics | Lessons graded but grades generous, or actions lack metrics | Ungraded lessons or "be more careful" actions | 25% |
| Blameless and clear | No blame; hindsight note present; reads as one document | Minor lapses | Blames individuals | 10% |
