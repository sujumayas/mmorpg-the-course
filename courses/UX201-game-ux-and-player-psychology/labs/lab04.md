# UX201 · Lab 04: A free-choice experiment

Assigned in week 4 ([lecture](../lectures/w04-self-determination-theory.md)). Due at the start of week 5. Groups of three or four; each group submits one report. Two groups may pool data if both run the identical protocol.

## Objective

Run a small version of Deci's free-choice paradigm. One group of participants earns a points reward for each puzzle solved and one doesn't. Then you measure how long each person keeps playing when the reward is gone and nobody is asking them to. You compute the effect size with its uncertainty and compare it with the meta-analysis values from lecture section 2. The goal is to learn the method and to see, with your own numbers, how much a sample of 12 can and can't tell you.

## Starter materials

**1. Analysis script.** [`lab04-starter/free_choice.py`](lab04-starter/free_choice.py), standard-library Python 3. It reads your data file and prints group means and standard deviations for the final free-choice time, the change from baseline and self-reported interest, each with Cohen's `d` (reward minus control) and a bootstrap 95% interval. It ends by listing the meta-analysis effect sizes. Options: `--boot` (resamples, default 2000) and `--seed`.

**2. Data template with invented example data.** [`lab04-starter/free_choice_data.csv`](lab04-starter/free_choice_data.csv). Columns: `participant, group, baseline_s, free_choice_s, interest_1to7`. The 12 rows are invented so you can run the script before your session. Delete them and enter your own. The invented effect is much larger than real studies find, so don't copy its conclusion.

**3. The task.** Any free browser puzzle game with short, self-contained puzzles that a new player can solve in one to three minutes each (for example a nonogram, sliding-block or logic-grid site). Get it approved in the week 4 lab session. It must run on the lab machines and must not show ads that pull attention away.

**4. The free-choice room.** A desk with the puzzle game open and, within reach, two alternatives of similar effort: a few recent magazines or comics and a second device with a video site muted (or a set of paper puzzles of a different kind). The alternatives must be real options, or the free-choice time means nothing.

**5. Session protocol (read it word for word).**

> Thanks for taking part. This study is about how people solve puzzles. It takes about 25 minutes. You can stop at any time without giving a reason, and your data will be deleted if you ask. Nothing you do will be graded or shared with your name.

Then, in order:

1. **Practice (3 min).** The participant solves one puzzle while you watch, to learn the controls.
2. **Baseline free period (5 min).** Say: "I need to set up the next part. It'll take about five minutes. Do whatever you like in the meantime." Leave the room. The timer, sitting outside or watching through a door window or a video call with the camera pointed at the screen, records the seconds spent on the puzzle game.
3. **Work period (8 min).** Reward group: "For this part, you'll earn 10 points for each puzzle you solve, and the points will go on a class leaderboard with a small prize for the top score." Control group: "For this part, please solve as many puzzles as you can." Both groups solve puzzles for 8 minutes.
4. **Withdrawal.** Reward group: "That's the end of the points part. There are no more points from here on." Control group: "That's the end of that part."
5. **Final free period (8 min).** Same words as step 2. Leave. Time the seconds on the puzzle game.
6. **Questionnaire.** "How interesting did you find the puzzles?" from 1 (not at all) to 7 (very).
7. **Debrief.** Explain the real purpose, the reward manipulation and why you left the room. Give the reward group's points as promised. Ask them not to discuss the study with classmates who haven't taken part yet.

**6. Ethics.** This is a minimal-risk classroom exercise. Participants must be adult classmates or friends who agree to take part, and they may stop at any time. Record no names in the data file, only participant codes. If your institution requires registration of class projects with human participants, your instructor has done this for the course. Don't run the study on anyone under 18.

## Steps

1. **Assign groups.** Recruit 12 or more participants. Assign each to reward or control by coin flip or a shuffled list prepared in advance, not by who arrives first.
2. **Pilot** the protocol on one person outside your sample. Fix any wording that confused them or any timing that ran over.
3. **Run the sessions.** One person reads the protocol, one times. Keep a notes column for anything unusual, such as a participant who used their phone the whole time or asked whether the points were still running.
4. **Enter the data** and run the script. Save the output.
5. **Compare** your `d` for the change from baseline with the meta-analysis values. Is your interval wide enough to include both −0.36 and 0?
6. **Power check.** For `d = −0.36`, about 120 participants per group are needed to detect the effect reliably at the usual thresholds. Say in one sentence what your sample could have detected.
7. **Interpret.** Which of these could explain your result: the reward's meaning (a leaderboard is partly performance-contingent), the task's initial interest, the alternatives in the room, or noise? Use your notes column.

## Deliverable

A report of at most two pages plus appendices.

- The task, the reward, the room setup and any departures from the protocol.
- A table of group results for all three measures, with `d` and its interval.
- One paragraph comparing your effect with the meta-analysis, and saying what your sample size lets you conclude.
- One paragraph classifying your reward by the four contingency types and predicting how a purely informational version ("your best time so far") might have differed.
- Appendices: the data file, the script output and the session notes.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Protocol and ethics | Random assignment, protocol read verbatim, genuine alternatives in the room, debrief done, no names recorded | Minor departures, documented | Assignment by convenience, no debrief, or identifiable data | 25% |
| Data and analysis | Clean data, script run correctly, all three measures reported with intervals | Minor errors or one measure missing | Wrong groups or no effect sizes | 20% |
| Comparison with the literature | Effect compared with the correct meta-analysis category, interval read correctly, power stated plainly | Comparison made, uncertainty mentioned but not used | Treats one small-sample `d` as a finding | 25% |
| Interpretation | Alternative explanations weighed with evidence from notes; reward correctly classified | Plausible but thin | Missing or unsupported | 20% |
| Writing | Clear, within length, tables readable | Some padding or unclear tables | Hard to follow | 10% |
