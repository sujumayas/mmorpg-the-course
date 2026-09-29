# MMO407 · Week 09 — Communication during crises

**Why this matters:** During an outage, the message is the only part of your game that players can still use. Most of the anger after a bad launch night is not about the minutes the servers were down. It is about the times players were told, the times those promises broke, and what was left unsaid. This week you learn to treat a promised time as a forecast you can compute, to see why "thirty more minutes" is almost always the wrong extension, and to write the updates players need when you do not know the answer yet.

**You will be able to:**
- Compute the cost-minimizing time to announce for an outage from a log of past durations and the relative cost of finishing late or early, using the critical ratio.
- Compute the average time still to go for an outage that has already lasted `t` minutes, and explain why it grows for the heavy-tailed durations real incidents have.
- Compare extension policies (fixed increments, re-forecasting from the log, update times only) by the expected number of broken promises.
- Write a crisis update that states what is known, what is not, what players should do and when the next update comes, and adapt it to outages, data loss, exploits and security breaches.

**Before class:** Read the Wikipedia article "2011 PlayStation Network outage," the timeline section (15 minutes). Read GitLab, "Postmortem of database outage of January 31" (10 February 2017), the section on how GitLab published the outage (5 minutes). Reread MMO308 week 13 section 4, "Talking to players." Its three rules are the starting point for this week and are not repeated.

**Prerequisites from earlier courses:** [MMO308 week 13, incident response](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md) (severity, roles, the communication cadence, the rule to promise update times rather than fix times, and the fix-forward survival curve; this week builds on all of them). [MMO302 week 14, observability](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md) (why the status page must not share a failure with the game). [DB201 week 13, privacy, GDPR and data retention](../../DB201-data-persistence-and-telemetry/lectures/w13-privacy-gdpr-and-data-retention.md) (breach notification duties). [DB201 week 14, backups and disaster recovery](../../DB201-data-persistence-and-telemetry/lectures/w14-backups-and-disaster-recovery.md) (the GitLab restore; this week looks only at how it was communicated). [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md).

**Interactive:** [examples/w09-eta-announcer.html](../examples/w09-eta-announcer.html). Keep it open during section 2.

---

## 1. What players need from you

A **crisis**, for this lecture, is any event that stops players playing or threatens what they own, and that they will hear about whether or not you tell them. An outage is the common case. Data loss, a rollback, an exploit in the economy and a security breach are the others. Each one raises the same three questions in every player's head:

1. **Is it me or you?** Players first check their own connection and their own account. A fast acknowledgement saves thousands of them from reinstalling the game.
2. **When can I play?** This is the question this week's model answers.
3. **Is my stuff safe?** Characters, items, progress, payment details. After a rollback or a breach, this outranks the second question.

MMO308 week 13 gave three rules for answering them: acknowledge fast, promise the next update and keep it, and never promise the fix time. The rules are right, and they leave a gap. Some crises come with a time you *must* announce. Scheduled maintenance has an end time on the launcher. A platform holder, an esports schedule or a marketing beat needs a date. A regulator needs a notification within a fixed window. And once you have said "we are working on it" three times, players will ask for a time whether or not you have one. When you give a time, you are making a forecast in public. This lecture is about making it well.

## 2. Worked example: which time do you announce?

### The hook

On 20 April 2011, Sony acknowledged on the PlayStation Blog that parts of the PlayStation Network were down. The next day it asked for patience and said full service might take "a full day or two." On 22 April it announced an external intrusion. On 25 April it said there was no estimated time of completion. On 26 April it said it had a clear path back and expected some services within a week. On 1 May it said some services would return in the first week of May. On 7 May it said it could not meet that one-week timeframe. Sign-in began coming back in North America on 14 May, 24 days after the first post.

Sony Online Entertainment's games went down too. SOE was the publisher of EverQuest, and its services were taken offline on 2 May after a related intrusion. SOE told players its games would not be available until some time after the weekend.

Every forecast in that timeline was reasonable on the day it was made, and nearly every one was wrong in the same direction. Here is the puzzle. If each estimate was a team's honest best guess, why did the guesses keep falling short? And what should the team have said instead?

### The model

You need two things. The first is a **duration log**: how long your past incidents of this kind lasted. The second is a judgment about **what a missed promise costs compared with an early finish**.

Announce "back at minute `T`." The outage actually lasts `D` minutes.

- If `D > T`, you are late. Players who came back at `T` wait, refresh and lose trust for `D − T` minutes. Call the cost per player per late minute `c_late`.
- If `D < T`, you are early. Players who believed you went elsewhere and come back at `T`, so the game sits idle for `T − D` minutes it could have been played. Call that cost `c_early`.

```
expected cost(T) = c_late × E[max(0, D − T)] + c_early × E[max(0, T − D)]
best T:  P(D ≤ T) = c_late / (c_late + c_early)          the critical ratio
```

- `D` is the outage's length, uncertain, described by your log.
- `T` is the announced time, counted from the start of the outage.
- `P(D ≤ T)` is the share of past outages that were over by `T`.

The second line is the result. Nudge `T` one minute later. With probability `P(D ≤ T)` you add a minute of early-finish cost, and with probability `P(D > T)` you save a minute of lateness. The cost stops falling when the two balance, which is when `P(D ≤ T)` equals the **critical ratio** `c_late / (c_late + c_early)`. Operations researchers know this as the newsvendor problem: how many papers to print when unsold ones and missed sales cost different amounts.

The critical ratio says something that sounds wrong until you check it. **If a late minute costs more than an early one, the right announcement is later than the median.** With `c_late = 2 × c_early`, the ratio is 2/3, so you announce the time by which two thirds of past outages were over, not half.

### Numbers you can check

Here is an invented log of a studio's last 20 unplanned outages, in minutes, sorted:

```
15  20  25  30  30  35  40  45  50  60
60  75  90  105 120 150 180 240 360 600
```

The median is 60 minutes (between the 10th and 11th values). The mean is 116.5, pulled up by a few long ones. Take `c_late = 2` and `c_early = 1`. A late minute costs twice an early one, because players who come back to a closed door are angrier than players who come back to an open one.

Check one cost by hand. Announce `T = 60`. Nine outages ran past 60, by 15, 30, 45, 60, 90, 120, 180, 300 and 540 minutes, a total of 1,380, so the lateness cost is `2 × 1,380 / 20 = 138.0`. Nine outages finished before 60, by 45, 40, 35, 30, 30, 25, 20, 15 and 10 minutes, a total of 250, so the early cost is `250 / 20 = 12.5`. The total is 150.5.

```python
import math

# Minutes each of the studio's last 20 unplanned outages lasted, sorted.
LOG = [15, 20, 25, 30, 30, 35, 40, 45, 50, 60,
       60, 75, 90, 105, 120, 150, 180, 240, 360, 600]

def cost(T, log, c_late=2, c_early=1):
    """Average cost per player of announcing 'back at minute T'."""
    return sum(c_late * max(0, d - T) + c_early * max(0, T - d) for d in log) / len(log)

def quantile(log, q):
    """Smallest logged duration with at least a share q of the log at or below it."""
    s = sorted(log)
    return s[math.ceil(q * len(s)) - 1]

def mean_left(log, t):
    """Average minutes still to go, for outages that have already lasted t."""
    rest = [d - t for d in log if d > t]
    return sum(rest) / len(rest)

for T in (60, 90, 105, 120, 150, 240):
    late = sum(d > T for d in LOG) / len(LOG)
    print(f"announce {T:3d} min: miss {late:4.0%}  cost {cost(T, LOG):6.1f}")
print("critical ratio 2/3 ->", quantile(LOG, 2 / 3), "min")
for t in (0, 60, 120, 240):
    print(f"down for {t:3d} min: {mean_left(LOG, t):5.1f} min still to go on average")
```

Output:

```
announce  60 min: miss  45%  cost  150.5
announce  90 min: miss  35%  cost  142.2
announce 105 min: miss  30%  cost  141.5
announce 120 min: miss  25%  cost  143.0
announce 150 min: miss  20%  cost  150.5
announce 240 min: miss  10%  cost  195.5
critical ratio 2/3 -> 105 min
down for   0 min: 116.5 min still to go on average
down for  60 min: 153.3 min still to go on average
down for 120 min: 186.0 min still to go on average
down for 240 min: 240.0 min still to go on average
```

The cost is lowest at 105 minutes, exactly the value the critical ratio picks out, the 14th of 20 durations. The median, 60 minutes, misses 45% of the time and costs as much as announcing 150. Notice also how flat the bottom is. Anything from 90 to 120 is within about 1% of the best. You do not need the exact number. You need to stop announcing the median.

### The longer it lasts, the longer it lasts

Now look at the last four lines. At the start, an outage has 116.5 minutes to go on average. After an hour, the ones still running have 153 minutes to go, more than at the start. After two hours, 186. After four hours, 240.

This is the fact that broke Sony's timeline, and it breaks most extension policies. An outage that has already outlasted your estimate is, by that fact, more likely to be one of the hard ones. The easy ones are over. What remains is the tail of the log, and the tail is long. Statisticians call this an increasing **mean residual life**, and it is typical of **heavy-tailed** durations, where a few cases last many times longer than the median.

MMO308 week 13 modelled diagnosis as rounds that each find the cause with probability `p`. That model is **memoryless**. However long you have been diagnosing, the expected time left is the same `r/p` as at the start. Even in that friendly model, a miss tells you nothing encouraging. Real logs are worse than memoryless, as this one is, because hard incidents are a different kind of incident, not unlucky easy ones.

### Extending after a miss

Suppose the outage runs past the announced time. Compare two policies on every outage in the log.

- **Policy A, "median, then thirty more."** Announce 60 minutes. On each miss, announce 30 more.
- **Policy B, "re-forecast."** Announce the 2/3 quantile, 105 minutes. On a miss, look only at past outages that lasted longer than your last announcement, and announce their 2/3 quantile.

| Actual outage | Policy A announcements | Misses | Policy B announcements | Misses |
|---|---|---|---|---|
| 45 min | 60 | 0 | 105 | 0 |
| 90 min | 60, 90 | 1 | 105 | 0 |
| 150 min | 60, 90, 120, 150 | 3 | 105, 240 | 1 |
| 360 min | 60, 90, …, 360 | 10 | 105, 240, 600 | 2 |
| 600 min | 60, 90, …, 600 | 18 | 105, 240, 600 | 2 |
| Average over the 20 logged outages | | 2.35 | | 0.4 |

Policy A breaks 18 promises on the worst outage, one every half hour for nine hours. Policy B breaks two. The reason is the growing residual. After a miss at 105 minutes, the outages still running in the log are 120, 150, 180, 240, 360 and 600. Their 2/3 quantile is 240, so the right extension is more than two hours, not thirty minutes. Fixed small increments assume the end is always near, and in a heavy-tailed world it rarely is.

Policy B has a price. On the 360-minute outage it announces 600 after the second miss, and finishes 240 minutes early. That is the `c_early` cost at work, and the critical ratio has already weighed it.

### Move it yourself

Open the interactive. The left view shows the log as a sorted bar chart with the announced time as a draggable horizontal line across the bars, bars past it coloured "late" and bars before it coloured "early," and the expected cost printed above. The right view plays one outage at a time as a timeline of announcements, with each broken promise marked as a red tick. Drag the cost ratio from 1:1 to 4:1 and watch the best announcement slide from the median to the long end of the log. Then pick the 600-minute outage and switch between Policies A and B. Count the red ticks.

### Cross-game recognition

**EVE Online's daily downtime (current).** Every day at 11:00 UTC the cluster goes offline for maintenance. The EVE University wiki records that the window is nominally 15 minutes, shortened from 30 in May 2016, and that on most days it is over after a few minutes. That is a promise set at a very high quantile. CCP announces the time that almost always holds, and finishing early costs little because players know the window. When a patch needs longer, CCP announces an extended downtime in advance on its status page, its status account on X and the launcher. An extension announced before the window starts is not a broken promise.

**GitLab.com (31 January 2017).** DB201 week 14 covered what failed. The communication is this week's example. GitLab's post-mortem says the team kept its progress notes in a publicly visible document and streamed the recovery live on YouTube, with a peak of around 5,000 viewers, while a status account on Twitter carried short updates. The restore copy alone took around 18 hours. GitLab rarely needed an end time, because anyone could watch the work and see where it stood. Showing the work instead of forecasting it is the extreme version of MMO308's rule to promise updates, not fixes.

**Outside games: the planning fallacy.** Psychologists Roger Buehler, Dale Griffin and Michael Ross asked students to predict when they would finish their theses. The average prediction was 33.9 days, the average "if everything goes as poorly as it possibly could" was 48.6 days, and the average actual time was 55.5 days. In a later study, only 45% of students finished by the date they had given a 99% probability. People's gut quantiles are not quantiles. That is why the model starts from a log and not from the on-call engineer's feeling. The engineer's "probably an hour" is a median at best, and usually lower.

Three cases, one idea. A promised time is a quantile of a duration distribution. Choose the quantile on purpose, measure the distribution from records, and when a promise breaks, re-forecast from the cases that are still running.

### Eyes-open design judgment

- **Prefer no fix time at all.** MMO308's rule stands. Promising the next update is a promise at the 100% quantile, because you control it. Use this model only when a time is required or when players need one to plan their evening.
- **The cost ratio is a judgment, so write it down.** A studio whose players leave for other games when told "four hours" has a high `c_early`. A studio with a history of broken promises has a high `c_late`. Agree the ratio before the incident, not at 02:00.
- **The log must match the incident.** A database restore and a bad deploy have different distributions. Keep separate logs by kind, and when you do not know the kind yet, use the whole log and say so.
- **Round up, and say it is an estimate.** Players remember the number, not the hedge. "We expect to be back by 21:00 UTC and will update at 20:00" beats "we hope for 19:45."
- **The model says nothing about honesty.** Announcing a late time to look good when you finish early is a pattern players learn. The critical ratio works because it is honest about its cost ratio.

### Check this example

1. With `c_late = 3` and `c_early = 1`, what is the critical ratio, and which logged duration does it pick?
2. An outage has lasted 120 minutes. Using the log, what share of the outages still running will be over by 240?
3. Your team says "we'll be back in an hour" at every incident. How often is that promise broken, according to the log?

<details>
<summary>Answers</summary>

1. `3 / 4 = 0.75`. The 15th of 20 values, 120 minutes.
2. Outages longer than 120 are 150, 180, 240, 360 and 600. Three of the five are over by 240, so 60%.
3. Nine of 20 outages lasted longer than 60 minutes, so the promise breaks 45% of the time.

</details>

## 3. The rest of the message

The time is one line. The update around it does most of the work.

### The anatomy of an update

Every crisis update, whatever its channel, answers five things in this order.

1. **What is happening, in player terms.** "Players in Europe cannot log in" beats "authentication service degradation."
2. **Who is affected.** Regions, platforms, features. Players who are not affected stop worrying, and the ones who are stop wondering.
3. **What players should do.** Usually nothing, and saying so stops a wave of reinstalls and password resets. Sometimes something specific: do not trade, change your password, stay logged out.
4. **What you do not know yet.** Say it plainly. "We do not yet know whether any items were lost" is better than silence, and far better than a reassurance you take back later.
5. **When the next update comes.** A clock time in UTC and in the main local time zone, kept even if the update says "no change."

### Channels that survive the crisis

Post where players look first, on infrastructure that does not fail with the game. MMO302 week 14 made this argument for monitoring. EVE's status page, X account and launcher messages, listed in the cross-game section, are an example of several channels carrying the same message. Pin one of them as the **source of truth**, and have every other channel link to it, so that a correction made in one place reaches everyone.

### Different crises, different first sentences

| Crisis | The question players ask first | What the first update must say | The trap |
|---|---|---|---|
| Outage | When can I play? | Scope, a next-update time, and a promised time only if you must | Announcing the median |
| Rollback or data loss | What did I lose? | The exact window being rolled back, in UTC, and what happens to purchases in it | Saying "minor" before you know |
| Exploit in the economy | Is my stuff worth less? | What is switched off (trading, a vendor), that the cause is known or not, and that you will not describe the exploit | Teaching the exploit in the patch notes |
| Security breach | Is my account or card at risk? | What data may be involved, what players should do now, and when you will know more | Waiting until the investigation is complete |
| Design backlash | Are you listening? | That you have read the feedback, what you will decide and when | Promising a reversal you have not agreed |

The breach row has a legal edge. Under the EU's GDPR, Article 33, a studio must notify the supervisory authority of a personal data breach without undue delay and, where feasible, within 72 hours of becoming aware of it (DB201 week 13 covers the rest). The Sony timeline shows the reputational side. Sony identified an intrusion on 19 April and told users on 26 April that personal data might have been taken. Government officials in several countries criticized the week's delay, and it featured in lawsuits. Sony's own explanation was that it needed several days of forensic analysis to know what had been taken. That is true of every breach, and it is exactly why the first update must say what you do not know yet, rather than wait until you do.

Exploits and design backlash have their own weeks: [duplication exploits in week 6](w06-case-duplication-exploits-after-launch-new-world-2021.md), [the Star Wars Galaxies NGE in week 5](w05-case-star-wars-galaxies-and-the-nge.md), and [recovery strategies in week 10](w10-recovery-strategies.md). Compensation after the crisis is MMO308 week 13's topic.

### Who speaks

A crisis update needs a voice. On a small team, the communications role from MMO308's incident roles writes the updates, and a named lead signs the one that matters most, usually the explanation after the crisis. A named person reads as accountable. An anonymous account reads as a wall. The trade-off is that a named person becomes the target, so the studio must stand behind them in public.

## In-class activity (25 minutes)

Groups of three. Scenario: your MMO's European login servers failed at 19:10 UTC on a Friday, one hour into a new content patch. Your on-call lead says the cause is not known yet. Use this lecture's log and a cost ratio your group agrees on.

1. Agree `c_late : c_early` and justify it in one sentence for a Friday-evening outage. Compute the time to announce, if any. (5 min)
2. Write the first update (posted 19:25) and the second (posted at the time the first promised). Each must have all five parts of section 3. (10 min)
3. It is now 21:30 and the announced time has passed. Write the third update with a re-forecast from the log. (5 min)
4. Swap updates with another group. Mark each of their updates for the five parts and for any promise that the log says is likely to break. (5 min)

Expected output: the ratio and time, three short updates, and the other group's marked copy.

## Common misconceptions

- **"Announce your best guess."** A best guess is roughly a median, and a median breaks half the time. If a late minute costs more than an early one, announce later than the median, at the critical ratio.
- **"Short extensions look more responsive."** They break more promises. In the log, "thirty more minutes" breaks 18 promises on the longest outage, while re-forecasting breaks two.
- **"If it has been down this long, it must be nearly fixed."** For heavy-tailed durations the opposite holds. In the log, an outage that has lasted two hours has 186 minutes still to go on average, more than a fresh one.
- **"Say nothing until you know."** Silence answers none of the three questions and invites rumours to fill the gap. "We do not know yet, next update at 20:30" answers two of them.

## Check yourself

1. Using the log, compute the expected cost of announcing 120 minutes by hand with `c_late = 2`, `c_early = 1`. Confirm the value in the table.
2. A studio's players say a late minute is only as bad as an early one. What should it announce, and how often will it be late?
3. Your log for database restores has five entries: 90, 120, 150, 240 and 900 minutes. A restore has been running for 150 minutes. What is the average time still to go, and what does that tell you about your next announcement?
4. A producer proposes to always announce twice the engineer's estimate. Using the planning fallacy results, explain when this helps and why it is still worse than using the log.

<details>
<summary>Answers</summary>

1. Five outages ran past 120 (150, 180, 240, 360, 600), late by 30, 60, 120, 240 and 480, total 930, so lateness is `2 × 930 / 20 = 93`. Fifteen finished before or at 120, early by 105, 100, 95, 90, 90, 85, 80, 75, 70, 60, 60, 45, 30, 15 and 0, total 1,000, so the early cost is `1,000 / 20 = 50`. Total 143.0, matching the table.
2. With a ratio of 1/2, it announces the median. `ceil(0.5 × 20) = 10`, so the 10th value, 60 minutes. It is late 45% of the time (nine outages ran longer than 60).
3. The restores still running after 150 minutes are 240 and 900, with 90 and 750 minutes to go, an average of 420 minutes. One very long restore dominates. With so few records the forecast is shaky, so the next announcement should be an update time, not a new end time, and the update should say that the restore is in its slow case.
4. Doubling helps when estimates are consistently too low by about half, as in the thesis study (33.9 days predicted, 55.5 actual). But a fixed multiplier ignores the tail. It moves every estimate up by the same factor, while the log shows most outages are short and a few are very long. It over-announces short incidents and still under-announces long ones. The log's quantile does neither.

</details>

## Lab / assignment hook

[Lab 09, the crisis communications kit](../labs/lab09.md). You build the ETA forecaster from this week's model, test extension policies on a larger log of outages, and write a communications kit: update templates for four kinds of crisis, a channel plan and a cost ratio your team signs off before launch. The kit becomes the "communications" section of your final launch plan.

## Sources

- Wikipedia, "2011 PlayStation Network outage" (accessed September 2026). Intrusion 17-19 April 2011; acknowledgement on 20 April; "a full day or two" on 21 April; external intrusion announced 22 April; no estimated completion time on 25 April; expectation of some services within a week on 26 April, with the disclosure that personal data may have been compromised; first-week-of-May estimate on 1 May; SOE services offline 2 May; the one-week timeframe missed on 7 May; services returning in North America from 14 May; criticism of the week's delay by government officials; Sony's explanation of the forensic analysis.
- Wikipedia, "EverQuest" (accessed September 2026). Published by Sony Online Entertainment from 1999 until SOE became Daybreak Game Company in 2015.
- GitLab, "Postmortem of database outage of January 31" (10 February 2017). Progress kept in a publicly visible document; recovery streamed on YouTube with a peak of about 5,000 viewers; Twitter status account; copying the data took around 18 hours. https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/
- EVE University Wiki, "Downtime" (accessed September 2026). Daily downtime at 11:00 UTC, nominally 15 minutes since May 2016 (previously 30), usually over after a few minutes; extended downtime announced through developer posts, the status page, the status account on X and the launcher.
- Buehler, R., Griffin, D. & Ross, M. (1994). "Exploring the 'planning fallacy': Why people underestimate their task completion times." *Journal of Personality and Social Psychology* 67(3), 366-381. Thesis predictions of 33.9 days, worst case 48.6, actual 55.5.
- Buehler, R., Griffin, D. & Ross, M. (1995). "It's about time: Optimistic predictions in work and love." *European Review of Social Psychology* 6, 1-32. 13%, 19% and 45% of students finished by their 50%, 75% and 99% dates. Both studies as summarized in Wikipedia, "Planning fallacy" (accessed September 2026).
- Regulation (EU) 2016/679 (GDPR), Article 33, via gdpr-info.eu (accessed September 2026). Notification of a personal data breach to the supervisory authority without undue delay and, where feasible, within 72 hours.
- The outage log and cost ratios are invented for teaching.

## Interactive spec: examples/w09-eta-announcer.html

**The one insight:** a promised time is a quantile of the outage-length distribution. If a late minute costs more than an early one, the best promise is later than the median. And because long outages are more likely to keep going, the right extension after a miss is long, not "thirty more minutes."

**Layout (two linked views, stacked on mobile, side by side at 900px and wider):**

- View A, "the log": the 20 durations as a sorted bar chart (x is rank 1 to 20, y is minutes on a square-root scale with ticks at 15, 60, 120, 240, 600). A draggable horizontal line at the announced time `T`. Bars longer than `T` coloured `--blood` ("late"), bars shorter coloured `--steel` ("early"). Above the chart, the expected cost and miss rate at `T`, and a small cost curve (cost against `T` from 0 to 600) with its minimum marked and labelled with the critical ratio's pick.
- View B, "one outage, played out": a horizontal timeline from 0 to the chosen outage's length plus 60 minutes, widened when needed so the latest promised time also fits. Each announcement is a flag at the minute it was made pointing to the time it promised; broken promises get a red tick at the moment they break. The end of the outage is a `--moss` marker. Beneath it, the residual strip: for each 30-minute mark, the average minutes still to go among logged outages longer than that mark, as a small bar.

**Controls:**

- Cost ratio `c_late : c_early`, 1:4 to 6:1 on a log scale (default 2:1).
- Announced time `T`, 0 to 600 (drag in View A, and a slider). A "snap to best" button sets `T` to the critical-ratio quantile.
- Outage picker: any of the 20 logged durations (default 600).
- Extension policy: "median, then +X" with `X` from 10 to 120 in steps of 10 (default 30); "re-forecast at the critical ratio" (default comparison); "update times only, every U minutes" with `U` from 15 to 120 (default 30), which shows update flags but no promised end times.
- Log editor: a text field of comma-separated minutes, validated to 5-100 positive numbers; "Reset to lecture log."

**Readout (always visible, `aria-live="polite"`):** critical ratio, best `T`, cost and miss rate at the current `T`, mean time still to go at 0, 60, 120 and 240 minutes, and for the picked outage the number of broken promises under each policy, plus the average over the whole log.

**Formulas:**

```
cost(T) = (1/N) Σ [ c_late × max(0, d − T) + c_early × max(0, T − d) ]
ratio   = c_late / (c_late + c_early)
best T  = sorted(log)[ceil(ratio × N) − 1]
mean_left(t) = mean(d − t for d in log if d > t)
Policy A (median, +X): T0 = sorted(log)[ceil(0.5 × N) − 1]; while D > T: miss += 1; T += X
Policy B (re-forecast): T0 = best T; while D > T: miss += 1; T = quantile of {d in log : d > T} at ratio
```

**Test values (must match, lecture log unless stated):**

- Ratio 2:1: best `T` = 105; cost 141.5; miss 30%. Cost at 60 = 150.5, at 120 = 143.0, at 240 = 195.5.
- Ratio 3:1: best `T` = 120. Ratio 1:1: best `T` = 60, miss 45%.
- Mean still to go: 116.5 at 0, 153.3 at 60, 186.0 at 120, 240.0 at 240.
- Outage 600: Policy A (+30) breaks 18 promises; Policy B breaks 2 (announcements 105, 240, 600). Outage 150: A breaks 3, B breaks 1. Averages over the log: A 2.35, B 0.4.

**First screen:** defaults with the 600-minute outage picked and Policy A shown in View B. Caption: "Eighteen broken promises, one every half hour. Switch to re-forecast."

**Accessibility:** every control keyboard operable with visible focus; `T` moves with arrow keys (1 minute) and Shift plus arrows (15 minutes); the log and the cost table are available as a collapsible table; readout in `aria-live="polite"`; respects `prefers-reduced-motion` (announcements appear without animation) and `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline. No logos, launcher screenshots or platform branding.
