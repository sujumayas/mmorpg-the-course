# UX201 · Lab 03: Flow playtest and dropout report

Assigned in week 3 ([lecture](../lectures/w03-flow-and-difficulty.md)). Due at the start of week 4. Groups of two or three; each group submits one report.

## Objective

Run a moderated playtest of a short, level-based game with three to five testers. Log deaths, time, a one-word rating and any stop per level. Estimate each tester's challenge ratio, apply the week 3 strain rule, and compare the testers it predicts will quit with what your testers actually did. The point is to report the players who leave, and why, instead of an average.

## Starter materials

**1. Analysis script.** [`lab03-starter/flow_strain.py`](lab03-starter/flow_strain.py), standard-library Python 3. It reads a CSV log and prints, for each tester, `R_hat` per level, zone, strain, predicted quit level and actual stop level. It then prints a pooled estimate per level with an approximate standard error. Options: `--q` (quit threshold, default 3), `--lo` and `--hi` (band edges, default 0.8 and 1.25), `--intended` (the deaths per clear you consider "about right" for this game, default 1).

**2. Log template and example.** [`lab03-starter/flow_log.csv`](lab03-starter/flow_log.csv) holds invented data for three testers, so you can run the script before your session. Keep the header row and replace the data with yours. Columns: `tester, level, deaths, cleared, minutes, rating, stopped_here`. `rating` is the tester's answer to the post-level question (`easy`, `right` or `hard`). `stopped_here` is 1 on the level where the tester stopped or asked to stop.

**3. Game choice.** Pick any free game with short, numbered levels and visible failure, for example a browser platformer or puzzle game, or a game from your own GD101 or GD102 work. It must have at least eight levels that a new player can reach in 30 minutes. Get your choice approved in the week 3 lab session. Before testing, write down your **intended deaths per clear**. Play the first three levels yourself and ask what death count you think the designer wanted.

**4. Session script (read it word for word).**

> Thanks for helping. I'm testing the game, not you. Please play for up to 30 minutes, as far as you like. You can stop at any point, for any reason, and that's useful information for me, not a problem. After each level I'll ask one question. Please think aloud while you play.

**5. Post-level question (ask it exactly, after every cleared level).** "Was that level easy, about right, or hard?"

**6. Observation log (by hand, alongside the CSV).** Time, level, what happened, and quotes in "quotes". Tag `S` for stuck more than 30 seconds, `Q` for a question, `B` for bored remarks or behaviour (checking phone, sighing, rushing), `A` for anxious remarks or behaviour (swearing, "one more try", tense posture). Keep observation and interpretation in separate columns, as in GD101 week 7.

## Steps

1. **Pilot** the game and the logging on one classmate. Fix anything in your setup that made logging slow.
2. **Recruit three to five testers** who have not played the game. Include at least one who plays the genre often and one who rarely plays games at all.
3. **Run the sessions.** One moderator talks and times. One observer fills the CSV and the observation log. No hints unless the tester is stuck for three minutes; log any hint as `ASSIST`.
4. **Run the script** with `--intended` set to your number from starter item 3. Save the output.
5. **Compare prediction and behaviour.** For each tester, did the strain rule predict their stop (or their finish)? Where it was wrong, use the observation log to say why: noise in death counts, confusion rather than difficulty, or a reason unrelated to the game.
6. **Sensitivity.** Rerun with `--q 2` and `--q 5`, and with `--intended` halved and doubled. Which conclusions survive all four runs?
7. **Draw the channel.** Plot each tester's levels on a challenge-against-skill chart. Use `C_k = 1` for every level and `S = 1 / R_hat` if you have no better scale, which is equivalent to plotting `R_hat` against the band. Mark stops with a cross. Hand-drawn is fine.
8. **Recommend.** For each tester who stopped, name the fix from lecture section 4 that targets their pattern, and say what it would cost the testers who finished.

## Deliverable

A report of at most two pages plus appendices.

- The game, your intended deaths per clear and why, and tester profiles (no names).
- The channel plot with crosses.
- A table per tester: levels played, predicted quit, actual stop, and the evidence that explains any mismatch.
- One paragraph on what the pooled per-level estimate says, with its standard errors, and why you should or shouldn't trust it at your sample size.
- The sensitivity results in two or three sentences.
- Recommendations, one per tester who stopped, each with a named cost.
- Appendices: the CSV, the script output and the observation logs.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Session method | Script and question used verbatim, mixed tester profiles, assists logged, observation kept separate from interpretation | Minor slips, mostly documented | Coaching, or no observation log | 20% |
| Data and model | Clean CSV, intended deaths justified, script run correctly, channel plot with crosses | Minor errors in data or plot | Model not applied or data unusable | 20% |
| Prediction vs behaviour | Every tester compared, mismatches explained with evidence from the log | Comparison made, thin explanations | No comparison | 25% |
| Uncertainty and sensitivity | Standard errors read correctly, sample-size limits stated plainly, conclusions sorted into robust and fragile | Uncertainty mentioned but not used | Treats one tester's death count as fact | 15% |
| Recommendations | Each fix matched to a dropout pattern, with its cost to other testers | Fixes plausible but generic | Missing, or "make it easier" for everyone | 20% |
