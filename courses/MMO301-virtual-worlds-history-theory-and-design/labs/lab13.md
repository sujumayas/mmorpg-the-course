# MMO301 · Lab 13: Sunset simulation and closure post-mortem

**Assigned:** week 13 ([lecture](../lectures/w13-worlds-that-died-shutdowns-and-their-lessons.md)). **Due:** start of week 14 class. **Feeds:** the case-studies assessment (40%) and the sunset chapter of your world bible (week 15).

## Objective

Use the week 13 density-churn model to tell the population story of one real closed world as far as public data allows, find where the model stops explaining the case, and write a post-mortem with a sunset plan the team could have used a year before the end.

## Starter materials

- [`lab13-starter.py`](lab13-starter.py), a standard-library Python script with the week 13 model: `churn`, `break_even`, `simulate` (with an optional merge) and `resting_population`. It prints the first months, the months below break-even and the resting population, and writes a CSV with `--csv`. Two functions are left as TODOs (`fit_to_timeline` and `sunset_month`).
- The interactive [`examples/w13-shard-spiral.html`](../examples/w13-shard-spiral.html), for quick what-if checks. The script is the source of truth for your numbers.
- Your chosen case's Wikipedia article and at least one other source (developer post, press coverage from the time, a maintained fan wiki). Allowed cases: Tabula Rasa, The Matrix Online, Star Wars Galaxies, City of Heroes, WildStar, or another closed MMO approved by your tutor.

Check your setup before you start. `python3 lab13-starter.py` must print a month-1 population of 188,571 and a first month below break-even of 14. `python3 lab13-starter.py --merge 6 --after 10` must print zero months below break-even and a resting population of 90,746.

## Steps

1. **Timeline (30 min).** Build a dated timeline for your case with at least six events: launch, major redesigns or business-model changes, merges or server closures, the closure announcement, the final day, and anything that happened after (emulators, licences). Cite a source for every row.
2. **Data points (20 min).** Collect every public population figure you can find (subscribers, concurrent players, server counts) with its date and source. Label each as subscribers, concurrency or server count. You may have only two or three. That is normal. Say so.
3. **Fit (45 min).** Implement `fit_to_timeline`. Search a grid of `A` (0 to 30,000, step 500) and `S` (1 to 60) with the other parameters at their defaults, and pick the pair that best matches your data points. Report the fit and the error. If your data are too thin to fit, fix `S` at the known server count and fit `A` alone.
4. **Sunset trigger (20 min).** Implement `sunset_month`, which returns the first month the world has spent six months in a row below break-even. Report it for your fitted run.
5. **Counterfactual (30 min).** Run one design change the team could have made (an earlier merge, a lower shard count at launch, a higher `A` from a free trial) and report how the sunset month moves. Then name one part of your case's story the model cannot represent (a licence, a studio closure, a redesign that changed who the game was for).
6. **Write-up (60 min).** A 600-word post-mortem with these parts: main cause and contributing causes (using the four families from the lecture), what the model shows, what it cannot show, and a five-line sunset plan answering the five questions in lecture section 4.

## Deliverable

One PDF or Markdown file with the timeline table, the data-point table, one chart of your fitted and counterfactual runs (players and break-even over time), and the 600-word post-mortem. Attach your completed `lab13-starter.py`.

## Rubric

| Criterion | Excellent (full marks) | Adequate (half marks) | Missing (0) | Weight |
|---|---|---|---|---|
| Timeline and evidence | Six or more dated events, each cited, with sources of different kinds | Six events, some uncited or all from one source | Fewer than six or uncited | 20% |
| Model use | Both TODOs work; fit and counterfactual are reproducible from the stated parameters; setup checks pass | Model runs but fit is by hand or undocumented | Model not used | 25% |
| Model limits | Names what the model cannot represent in this case and why, with evidence | Mentions limits in general terms | No limits discussed | 20% |
| Cause analysis | Main and contributing causes argued from evidence, with the four families used correctly | Causes named but weakly supported | Cause asserted without evidence | 20% |
| Sunset plan | All five questions answered with numbers and dates a team could act on | Plan present but vague on triggers or preservation | No plan | 15% |
