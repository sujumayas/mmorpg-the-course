# UX201 · Lab 09: Heuristic evaluation of a game interface

Assigned in week 9 ([lecture](../lectures/w09-heuristic-evaluation-for-games.md)). Due at the start of week 10. Groups of four or five; each group submits one report, and each member submits their individual findings list. This lab is the practice run for the graded heuristic evaluation assignment (20%).

## Objective

Run a heuristic evaluation of one screen or flow of a shipped game with independent evaluators. Consolidate the findings, collect severity ratings, and estimate how many problems your group did not find. Write a findings report a producer could act on. The point is to find problems without players, to be honest about what the method missed, and to separate usability problems from deliberate challenge.

## Starter materials

**1. Heuristic sheets.** Nielsen's ten heuristics with the game translations from lecture section 1, and one game-specific set chosen by your group: HEP (Desurvire, Caplan and Toth, 2004), PLAY (Desurvire and Wiberg, 2009), the mobile playability heuristics (Korhonen and Koivisto, 2006) for a mobile game, or Pinelle, Wong and Stach (2008). The papers are in the course reading list. Print one sheet per evaluator.

**2. Findings template.** One row per problem, with columns `evaluator, problem_id, location, description, heuristics, screenshot`. Use your own evaluator code (E1, E2 ...). Leave `problem_id` blank until consolidation.

**3. Analysis script.** [`lab09-starter/capture.py`](lab09-starter/capture.py), standard-library Python 3. It reads `findings.csv` (columns `evaluator, problem_id`, one row per evaluator per consolidated problem) and prints the union as evaluators are added, the found-by histogram, the Chao estimate, the Lincoln-Petersen and Chapman estimates for a split (`--a E1,E2`) or for every split (`--all-splits`), and mean severities from an optional `severity.csv` (columns `problem_id, rater, severity`).

**4. Example data.** [`lab09-starter/findings.csv`](lab09-starter/findings.csv) and [`lab09-starter/severity.csv`](lab09-starter/severity.csv) hold the lecture's Tidefall data. Run `python3 capture.py findings.csv --a E1,E2 --all-splits --severity severity.csv` and check that it prints Lincoln-Petersen 12.86 and Chao 15.12 before you use it on your data.

**5. Scope and game.** Choose one screen or flow that a player uses often: an inventory, a crafting screen, a group finder, a raid or party interface, a shop, or a settings menu. Write the scope as "screen, player, task," for example "the crafting screen, for a player in their first two hours, crafting a potion." Get it approved in the week 9 lab session. Record the game version and platform.

**6. Reach scenarios.** Before evaluating, the group writes three unusual states the screen can be in (for example, inventory full, connection lost, a colour-vision filter applied with a free simulator). Every evaluator must try all three in their second pass.

## Steps

1. **Train (15 min).** As a group, evaluate a practice screen from a different game for ten minutes and compare notes, so everyone applies the heuristics the same way. Then stop talking about the target screen.
2. **Evaluate alone (60 to 90 min each).** First pass to learn the screen. Second pass to record problems, including the three reach scenarios. Screenshots for every problem. Do not share lists until everyone has finished.
3. **Consolidate.** Merge the lists into one, write one clear description per problem, and give each a `problem_id`. Fill `findings.csv` with one row per evaluator per problem they found.
4. **Rate severity.** Send the consolidated list to every member. Each rates every problem 0 to 4 on their own, without discussion. Fill `severity.csv`.
5. **Estimate.** Run the script with `--all-splits`. Report the found count, the Chao estimate, the range of Lincoln-Petersen estimates across splits, and a sentence on why they differ.
6. **Deliberate challenge.** Go through every problem rated 2 or above and decide whether it is a usability problem or part of the intended challenge. Justify each "deliberate" call with the design reason (intrinsic against extraneous load, week 2).
7. **Recommend what to test.** Choose the three findings you are least sure about and write one usability test task (week 8) that would confirm or reject each.

## Deliverable

A report of at most two pages plus appendices.

- Scope, game version, platform, the heuristic sets used, and who the evaluators were (experience with the genre, any relevant perspective).
- A summary paragraph: problems found, the estimated range still hidden, the count at mean severity 3 or above, and whether the screen can ship.
- The findings table from lecture section 3, sorted by severity, with the found-by column and a recommendation or "deliberate challenge" note per row.
- The estimation output and your reading of it.
- The three test tasks.
- Appendices: each evaluator's original list, `findings.csv`, `severity.csv`, script output and screenshots.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Method | Clear scope, training round, independent evaluation shown by the individual lists, reach scenarios used | Mostly independent, scope loose | Evaluated together, or one person did most of it | 20% |
| Findings quality | Each row one problem, described from the player's side, correct heuristics, evidence attached | Some bundled or label-only rows | Findings are heuristic names without problems | 25% |
| Severity and estimation | Ratings independent from at least three raters; both estimators computed and their difference explained; range reported | Numbers computed, weak explanation | Single rater, or one estimate reported as fact | 20% |
| Design judgment | Deliberate-challenge calls justified with load and intent; recommendations specific | Some calls unjustified | Every violation marked "fix" | 20% |
| Link to testing | Three precise test tasks that would settle the uncertain findings | Tasks vague | Missing | 15% |
