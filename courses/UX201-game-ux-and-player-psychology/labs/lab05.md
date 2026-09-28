# UX201 · Lab 05: Reward schedule audit

Assigned in week 5 ([lecture](../lectures/w05-reinforcement-schedules-and-ethics.md)). Due at the start of week 6. Individual work, but you may play in pairs, with one playing and one logging, as long as each student writes their own audit.

## Objective

Find the reward schedules inside a real game by logging them, not by guessing. You play for 60 minutes, record every reward event, classify each reward stream as fixed or variable ratio or interval, apply the week 5 value model to locate the natural stopping points, and review the whole system with the seven-question ethics checklist. The finished audit should let a designer who has never played the game see where it lets players stop and where it doesn't.

## Starter materials

**1. Analysis script.** [`lab05-starter/schedule_audit.py`](lab05-starter/schedule_audit.py), standard-library Python 3. It reads your reward log and prints, for each stream, the number of rewards, the mean gap and its coefficient of variation, a schedule label (FR, VR, FI or VI), and, for ratio streams, the lecture's model: the value of the next action right after a reward on the fixed version, the value on the random version, whether a player with threshold `θ` stops, and the 5% dry streak. It also writes `cumulative_rewards.csv` for a cumulative-reward chart, and saves a PNG if matplotlib is installed and you pass `--plots`. Options: `--k` (discount, default 1) and `--theta` (default 12).

**2. Log template with invented example data.** [`lab05-starter/reward_log.csv`](lab05-starter/reward_log.csv). Columns: `time_s, stream, trigger, actions_since_last, paid, notes`. The example has three invented streams, a fixed "kill 10" quest, random chest drops and a herb node on a 10-minute timer. Run the script on it before your session, then replace the rows with your own.

**3. Game choice.** Any game with at least two reward sources you can observe in an hour. Good choices are an MMO or action RPG in its early levels, a mobile game with daily systems, or a free-to-play shooter with a battle pass and drops. If the game sells random items, you **must not spend money** for this lab. Log only what you can observe for free, and read the published odds where they exist.

**4. What counts as a reward.** Anything the game presents as a gain. Items, currency, experience jumps, level-ups, achievement pop-ups, unlocks, cosmetic drops. Count kills, pulls, harvests or matches as "actions" for the stream they feed. When unsure, log it and decide later.

**5. Observation habits.** Start a stopwatch when play begins. Log the time of each reward in seconds. Also log, in `notes`, every moment when you felt like stopping or actually paused, even if no reward was involved. Those notes are your data on stopping points.

## Steps

1. **Play and log** for 60 minutes. Keep one row per reward event.
2. **Clean the log.** Give streams consistent names. For count-triggered streams, fill `actions_since_last`. Mark `paid = 1` for any stream whose draws money can buy, directly or through a premium currency.
3. **Run the script** with the defaults, then with `--k 0.5` and `--theta 20`. Save all three outputs.
4. **Check the labels.** A stream with fewer than four gaps can't be classified by the script. Use published information (patch notes, wiki pages, in-game odds) to label it, and cite the source with its date.
5. **Chart** the cumulative rewards per stream against time, from the CSV or the PNG. Mark each moment from your notes when you paused or wanted to stop.
6. **Find the stopping points.** For each ratio stream, compare the model's prediction (does a fixed player stop after rewards?) with your notes. Did your own pauses fall right after rewards on fixed streams? Did random streams keep you going?
7. **Run the ethics checklist** from lecture section 3 on the game as a whole: stopping points, money in, disclosure, worst case, audience, exit, informational alternative.
8. **Propose one change** that adds a stopping point or removes a "yes" from the checklist, and estimate its cost to the game's engagement in one sentence.

## Deliverable

A two-page audit plus appendices.

- The game, platform, version or season, and date played.
- A table of streams: schedule label, mean gap, CV, paid or not, and model values for ratio streams.
- The cumulative-reward chart with your pause marks.
- A paragraph comparing the model's predicted stopping points with your own pauses.
- The seven checklist answers, each one line, with sources for any published odds.
- The proposed change and its cost.
- Appendices: the raw log and the script outputs.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Logging | 60 minutes, every reward logged with time and trigger, pauses noted | Gaps in the log or missing pause notes | Reconstructed from memory | 20% |
| Classification | Every stream labelled correctly, short streams labelled from cited sources | One or two doubtful labels | Labels guessed without data or sources | 20% |
| Model and stopping points | Model values correct, predictions compared honestly with own pauses, sensitivity runs discussed | Model run, comparison thin | Model not used | 25% |
| Ethics review | All seven questions answered with evidence; money and disclosure handled carefully; no money spent | Answers generic in places | Checklist missing or unsupported | 20% |
| Recommendation | One concrete change, tied to a checklist item, with a stated cost | Change plausible but cost missing | No change, or "remove all rewards" | 15% |
