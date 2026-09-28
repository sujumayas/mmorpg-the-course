# UX201 · Heuristic evaluation brief

**Weight:** 20% of the course grade.
**Group size:** four or five students. One group report, plus each member's individual findings list, which is marked individually.
**Assigned:** week 9. **Report due:** start of week 12.
**Labs that feed it:** [lab 09](../labs/lab09.md) is the practice run and uses the same method, templates and `capture.py` script. [Lab 11](../labs/lab11.md) supplies the accessibility guidelines and `contrast.py` for the accessibility pass. [Lab 10](../labs/lab10.md) supplies the glance-cost model and `hud_glance.py` for the information pass. [Lab 01](../labs/lab01.md) and [lab 02](../labs/lab02.md) supply the search and keystroke-level models for screens the player reads rather than glances at.
**Related briefs:** [usability-test-brief.md](usability-test-brief.md) and [final-study-brief.md](final-study-brief.md). If you evaluate a screen of the game you plan to use for the final study, this evaluation can become the final study's inspection module.

## What this component is for

The course outcome behind this component is "run usability tests and heuristic evaluations". A heuristic evaluation finds problems without players, cheaply and early. Done alone it misses most of what is there. Done with independent evaluators, it can also estimate how much it missed. This assignment grades three things. Did each of you inspect the screen properly on your own? Did the group turn the lists into findings a producer could act on? And did you say honestly what the method can't see?

## What to evaluate

One screen or flow of a shipped game that players use often: an inventory, crafting screen, group finder, raid or party interface, shop, map, settings menu or combat HUD. Write the scope as "screen, player, task", for example "the group finder, for a player in their first week, joining a dungeon group". The scope must differ from your lab 09 scope (a different screen of the same game is fine). Record the game's version, platform and the dates you evaluated it.

Get the scope approved in the week 9 lab session.

## Method

Follow the four steps of week 9, section 1, with the additions below.

1. **Training round (15 minutes, as a group).** Evaluate a practice screen from a different game, compare notes, then stop talking about the target screen.
2. **Independent evaluation (60 to 90 minutes each).** Nielsen's ten heuristics with the game translations from the lecture, plus one game-specific set chosen by the group: HEP, PLAY, the mobile playability heuristics for a mobile game, or Pinelle, Wong and Stach. First pass to learn the screen, second pass to record problems. Every evaluator also tries the group's **three reach scenarios**, unusual states the screen can be in (for example inventory full, connection lost, a colour-vision simulator applied). Screenshot every problem. No sharing until everyone has finished.
3. **Consolidation.** One clear description per problem, from the player's side. Give each a `problem_id`. Fill `findings.csv` with one row per evaluator per problem found.
4. **Severity.** Send the consolidated list to every member. Each rates every problem 0 to 4 on their own, without discussion. Fill `severity.csv` and report the mean of all raters.
5. **Specialist passes.** After consolidation, two members each run one specialist pass on the same scope. These use measurement rather than judgment, and their new findings are added to the consolidated list marked "specialist".
   - **Accessibility pass.** Measure contrast for at least six text or HUD elements on the worst-case backgrounds you can reach, with `contrast.py`. Check the in-scope items among the twelve lab 11 guidelines. For any colour-coded element, compute the luminance contrast between the colours that must be told apart and check for a second channel.
   - **Information pass.** If the screen is used during real-time play, run the glance model on its three most-checked elements with `hud_glance.py` and a measured setup. If it is a menu the player reads, estimate the cost of the most frequent task with the search model (week 1) or the keystroke-level model (week 2), and name the `M`s and `S`es that are not the game.
6. **Estimation.** Run `capture.py` with `--all-splits` on the non-specialist findings only. Specialist passes used a different method, so their findings break the capture-recapture assumption that evaluators work the same way. Report the number found, the Chao estimate and the range of Lincoln-Petersen estimates across splits, and explain why they differ.
7. **Deliberate challenge.** For every problem with mean severity 2 or more, decide whether it is a usability problem or part of the intended challenge. Justify each "deliberate challenge" call with the design reason, using intrinsic against extraneous load (week 2).
8. **Link to testing.** Choose the three findings you are least sure about and write one usability test task for each that would confirm or reject it (week 8).

## Deliverables

- **Individual findings list** from each member, exactly as submitted before consolidation, with evaluator code, location, description, heuristics violated and screenshot reference. Marked individually.
- **Group report**, at most three pages plus appendices, in this order.
  1. Summary paragraph: scope, problems found, estimated range still hidden, count at mean severity 3 or more, whether the screen can ship, and what to test next.
  2. Evaluators: who they were (genre experience, any relevant perspective) and which heuristic set you used.
  3. Findings table in the week 9, section 3 format, sorted by severity then by how many evaluators found each, with a found-by column and a recommendation or "deliberate challenge" note on every row. Specialist findings are marked.
  4. Estimation output and your reading of it, as a range.
  5. Specialist passes: measured values, pass or fail against the stated threshold, and what they found that the heuristic passes didn't.
  6. The three test tasks.
- **Appendices:** `findings.csv`, `severity.csv`, script outputs, `contrast.py` and `hud_glance.py` inputs and outputs, annotated screenshots cropped to the interface.

## Milestones

| When | Milestone | Graded? |
|---|---|---|
| Week 9 lab session | Lab 09 run as practice; scope approved; reach scenarios written | Lab 09 is graded as a lab |
| End of week 10 | Individual lists submitted to the course site before consolidation. The timestamp shows they were independent | Yes, as the individual part |
| Week 11 lab session | Consolidated list and severity ratings complete; specialist passes started. The course team checks that the scope still matches | No |
| Start of week 12 | Group report and appendices | Yes |

## Rubric (100 points)

Each member's mark is the group score out of 80 plus their individual list score out of 20.

| Criterion | Points | Excellent | Good | Adequate | Weak or missing |
|---|---|---|---|---|---|
| Individual findings list (individual) | 20 | 18-20: submitted on time before consolidation; each row one problem, described from the player's side, correct heuristic, screenshot; all three reach scenarios tried | 14-17: one or two bundled or label-only rows | 9-13: several rows are heuristic names without a problem, or a reach scenario skipped | 0-8: late, copied, or not independent |
| Consolidated findings | 20 | 18-20: one problem per row, clear descriptions, observation kept apart from prediction ("a new player may not notice"), evidence attached | 14-17: minor bundling or wording that asserts player behaviour | 9-13: several bundled rows, weak evidence | 0-8: list is labels, or findings duplicated |
| Severity and estimation | 20 | 18-20: independent ratings from every member, means reported; Chao and Lincoln-Petersen computed on the right findings and reported as a range with the reason they differ; independence assumption stated | 14-17: numbers right, explanation thin | 9-13: one estimator only, or specialist findings included in the estimate | 0-8: single rater, or an estimate reported as fact |
| Specialist passes | 10 | 9-10: measurements on true worst cases, thresholds stated, results change or add to the findings | 7-8: measurements present, one pass thin | 4-6: measurements on average backgrounds or guessed positions | 0-3: missing |
| Design judgment | 15 | 13-15: every severity 2+ problem classified; deliberate-challenge calls justified with intent and load; recommendations specific and directional | 10-12: most calls justified | 6-9: calls asserted without reasons | 0-5: every violation marked "fix", or no recommendations |
| Summary and link to testing | 15 | 13-15: a producer could decide from the summary alone; three test tasks that would settle the uncertain findings | 10-12: summary clear, tasks loose | 6-9: summary buries the ship decision or the hidden range | 0-5: no summary or no tasks |

## Late work

Individual lists must arrive before consolidation starts. A late list scores at most 8 of 20, because the group can no longer treat it as independent. The group report may be up to 48 hours late for a 10-point penalty. After that it scores 0 unless an extension was agreed before the deadline.

## Academic integrity

Your individual list is your own work, done before you see anyone else's. Everything after consolidation is group work. The heuristic sets are published research. Cite the set you used and don't copy its text into the report beyond the heuristic names.
