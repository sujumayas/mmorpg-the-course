# GD101 · Lab 07: Silent playtest and observation log

Assigned in week 7 ([lecture](../lectures/w07-playtesting-observe-dont-explain.md)). Due at the start of week 8. This is playtest report 1 of 3 (part of the 30% playtest-report grade). Your findings list is the input to lab 08.

## Objective

Run three silent playtests of your week 6 paper prototype with testers who have never seen it, keep timed observation logs, and turn them into a ranked findings list. The point is method: by the end you should be able to run a session without explaining your game and to separate what you saw from what you think it means.

## Starter materials

Everything below is included in this file. Print or copy it.

**1. Intro script (read word for word to every tester).**

> Thanks for helping. I'm testing this game, not you, so there are no wrong moves. The rules are on this sheet. During play I won't answer questions about the rules, because I want to see how the game works without me. If you get stuck, tell me what you're thinking and try what seems right. Please think aloud as you play: say what you're looking at and what you're deciding. I'll take notes [and audio, if agreed]. You can stop at any time. Any questions before we start?

**2. Consent line (tester signs or says yes on audio).** "I agree to play a prototype game for about 30 minutes. I understand the designer will take written notes [and an audio recording], that my name will not appear in the report, and that I can stop at any time."

**3. Allowed prompts during play.** "What are you thinking right now?" / "What are you looking for?" / "What do you expect will happen?" / Deflection for rules questions: "What do you think the rules say?" Nothing else.

**4. Observation log template (one sheet per tester).**

| Time | What happened (actions, direct quotes in "quotes") | Why I think it happened (optional) | Tag |
|---|---|---|---|
| 00:00 | | | |

Tags: `Q` tester asked a question, `S` stuck (more than 30 seconds without acting), `M` misread a rule, `ASSIST` you intervened, `+` surprising success or delight.

**5. Rescue rule.** Set your threshold before the first session (for example, three minutes stuck with no progress). If crossed, give the smallest possible hint and log `ASSIST` with the exact words you used.

**6. Debrief questions (after play only, in this order).** Tell me about that game in your own words. What was the most interesting moment? The most frustrating? Was there anything you wanted to do but couldn't? Then up to two questions about your test goals.

**7. Findings sheet template.**

| # | Finding (observation, not fix) | Testers (k of 3) | Severity (1 to 3) | Evidence (log refs) | Possible fix (optional) |
|---|---|---|---|---|---|

Severity: 3 blocker (needed ASSIST or game broke), 2 major (played a different game than designed), 1 minor (friction only).

## Steps

1. **Write test goals.** One to three questions a silent session can answer. Get them signed off by your lab instructor before recruiting.
2. **Prepare the prototype.** Rules sheet, components, a clock or phone timer. Play it once alone to confirm it can be finished in 30 minutes.
3. **Recruit three testers** who have not seen your game and are not in your project group. At least one should be from outside this course. Record, for each, how often they play board or card games (never, sometimes, weekly).
4. **Run three sessions** with the intro script, the allowed prompts only, and a fresh log sheet each time. If you have a partner, one of you observes and tallies every rule break by the facilitator.
5. **Debrief** each tester with the questions in order.
6. **Cluster and count.** Put every log line on a sticky note or spreadsheet row. Group them into findings. Count testers per finding (k of 3).
7. **Rate and rank.** Assign severity, then sort by severity and count, as in lecture section 5.
8. **Coverage check.** Pick your two highest-ranked findings. For each, estimate a plausible frequency `p` from your counts and compute `1 − (1 − p)^3`. Then name one problem you suspect exists but did not see, and compute how many testers you would need for a 90% chance of seeing it if `p = 0.10`.

## Deliverable

A PDF of at most four pages plus the three raw log sheets as an appendix (photos are fine).

- Test goals and tester profiles (one short paragraph).
- The ranked findings list, at least six findings, each with evidence.
- A section "Where I broke the rule": every explanation, leading prompt or ASSIST, with what it may have hidden. Zero is suspicious; be honest.
- The coverage check from step 8 with working.
- A one-paragraph answer to each test goal, supported by counts.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Session method | Script used verbatim, only allowed prompts, rescues logged with exact words, rule breaks reported honestly | Minor slips, mostly reported | Explained rules during play or no evidence of method | 25% |
| Observation quality | Logs are timed observations with quotes, interpretation kept separate | Mix of observations and conclusions | Mostly conclusions ("confused by X") | 25% |
| Findings | Six or more findings, clustered correctly, counts and severity justified, problems separated from fixes | Findings present but thin evidence or mixed with fixes | Fewer than four findings or unsupported | 25% |
| Coverage check | Correct calculations, sensible `p` estimates, clear statement of what three testers can and cannot show | Minor calculation errors | Missing or wrong | 15% |
| Writing | Numbers first, plain, at most four pages | Readable but padded | Hard to follow | 10% |
