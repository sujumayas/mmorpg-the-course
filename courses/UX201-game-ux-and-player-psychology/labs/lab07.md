# UX201 · Lab 07: Onboarding timeline audit

Assigned in week 7 ([lecture](../lectures/w07-onboarding-and-tutorials.md)). Due at the start of week 8. Pairs; each pair submits one audit.

## Objective

Record the opening of a shipped game, log when each core mechanic is taught, practised and first needed, and compute recall at every moment of need with the week 7 model. Find the two worst forgetting gaps and redesign the schedule to close them, naming what the redesign costs. The point is to judge a tutorial by what the player can do when it matters, not by what the tutorial covered.

## Starter materials

**1. Analysis script.** [`lab07-starter/onboarding_recall.py`](lab07-starter/onboarding_recall.py), standard-library Python 3. It reads an event log and prints, for every moment of need, the practice uses before it, the stability `s`, the gap since last use and the recall `e^(−gap/s)`. It then prints all-ready recall and expected mechanics missing for each moment of need. Options: `--s0` (default 20), `--g` (default 2.5) and `--target` (recall below which a need is flagged `LOW`, default 0.8). An unprompted need counts as a practice use for later needs. A `prompt` row at the same minute as a `need` row marks the need as prompted, and recall is reported as 1.0.

**2. Event log template and example.** [`lab07-starter/onboarding_events.csv`](lab07-starter/onboarding_events.csv) holds schedule A from the lecture, so the script's output should match the lecture table (0.549 per ability, all-ready 0.091). Columns: `mechanic, event, minute, note`. `event` is one of `teach`, `use`, `need`, `prompt`. Keep the header and replace the rows with yours.

**3. Game choice.** Any shipped game with at least four core mechanics taught in its first 45 minutes. Good candidates are action-adventure, action RPG, platformer or MMO starting zones. Do not use a game you have played through in the last year, because you need to watch the opening with fresh eyes. Get the choice approved in the week 7 lab session.

**4. Coding rules (use these exactly so that pairs can compare).**

- `teach`: the first time the game shows the mechanic *and* the player performs it, prompted or not. Record the minute of the performance.
- `use`: an unprompted use of the mechanic by the player at least 2 minutes after the previous event for that mechanic. Uses closer together than 2 minutes count as one (massed practice).
- `need`: the first time, and every later time, that progress requires the mechanic and the game does not show a prompt for it. Record the minute the requirement starts.
- `prompt`: the game shows a hint or button prompt for the mechanic at a `need`. Log it at the same minute.
- Round minutes to the nearest whole minute from the start of play (first input after the title screen).

**5. Recording.** Screen-record the session (OS recorder or OBS). Play as you normally would, or recruit a player who has not played the game and record them. A recorded new player gives better data, and it is good practice for week 8.

## Steps

1. **Record** 30 to 45 minutes of the opening.
2. **Code the video.** Both partners code it independently with the rules above. Then compare logs, and resolve disagreements by rewatching. Keep a count of disagreements before resolution.
3. **Run the script** with the defaults. Save the output.
4. **Sensitivity.** Rerun with `--s0 10 --g 2` and with `--s0 40 --g 3`. Which moments of need are flagged `LOW` in all three runs? Those are your robust findings.
5. **Draw the timeline.** Minutes across, one row per mechanic, dots for teach, ticks for use, vertical lines for need, as in the lecture's interactive. Hand-drawn and scanned is fine.
6. **Redesign.** Choose the two worst robust gaps. For each, propose a change from the lecture's toolkit (a practice use at a named place, a gate, a fading prompt, a contextual prompt at the need, or moving the need). Edit a copy of your log to reflect the change and rerun the script.
7. **Cost.** For each change, name what it costs in pace, autonomy, screen space or content, and which player (new, veteran, returning) it helps most.

## Deliverable

An audit of at most two pages plus appendices.

- The game, the platform and version, and who played.
- The timeline figure.
- A table of every moment of need with recall under the three parameter sets, robust `LOW` rows marked.
- The two redesigns, each with before and after recall, and its cost.
- One paragraph on the tutorial's checklist view against your recall view. When did the game finish *teaching* its core mechanics, and when were players first reliably ready to *use* them?
- Appendices: both original coded logs, the disagreement count, the resolved log and the script outputs.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Coding quality | Rules applied exactly, independent coding, disagreements counted and resolved from the video | Rules mostly followed, one coder did most of the work | Events guessed from memory or rules ignored | 25% |
| Model use | Script run correctly, sensitivity runs done, robust findings separated from fragile ones | Script run, sensitivity thin | Model not applied or misapplied | 20% |
| Timeline figure | Clear, complete, readable at a glance, needs visible | Complete but hard to read | Missing or incomplete | 15% |
| Redesigns | Two targeted changes, rerun with new logs, recall gains reported | Changes plausible but not rerun | Generic advice ("add more tutorial") | 25% |
| Costs and judgment | Each change priced in pace, autonomy or content, and matched to a player type | Costs mentioned briefly | No costs named | 15% |
