# UX201 · Week 14 — UX Research Reporting

**Why this matters:** A study nobody acts on changed nothing. Your playtest produced a notebook of observations. The team has a week of engineering time and a producer who reads the first page. What you put first, how sure you say you are, and how you word each finding decide which problems reach players. This week you learn to turn observations into a ranked, honest report that a team can act on the same day.

**You will be able to:**
- Write a finding that separates observation, evidence, interpretation, impact and recommendation, and rewrite a weak finding into that form.
- Compute an impact interval for each finding from its frequency, its Wilson interval and a severity weight, and sort findings into fix now, investigate and backlog tiers.
- Explain why sorting findings by how many testers hit them buries rare, severe problems, and show it with numbers.
- Design a report structure and a findings tracker for a team, including how to report a fix that was retested.

**Before class:** Jakob Nielsen, "Severity Ratings for Usability Problems" (Nielsen Norman Group, 1994, short web article). Ken Birdwell, "The Cabal: Valve's Design Process for Creating Half-Life" (Game Developer, 1999), the section on play-testing. Reread MA102 week 13, section 3, on the Wilson interval, and the RITE paragraph in GD101 week 7, section 2.

**Prerequisites from earlier courses:** [MA102 week 13, sampling, confidence and why n=5 lies](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md). This week uses its Wilson interval and rule of three as tools and does not re-derive them. [GD101 week 7, playtesting](../../GD101-introduction-to-game-design/lectures/w07-playtesting-observe-dont-explain.md), for the discovery curve, the RITE method and observation kept apart from interpretation. Looking ahead, [MMO303 week 14, communicating balance changes](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w14-communicating-balance-changes.md) (year 3) does for patch notes what this week does for research reports. [GD102 week 13, systems documentation](../../GD102-systems-design-and-game-mechanics/lectures/w13-systems-documentation.md), for writing documents a team maintains. From this course, [week 3](w03-flow-and-difficulty.md) (report the players who leave) and [week 13](w13-biometrics-and-eye-tracking.md) (what a signal can support). [Week 8](w08-usability-testing-methods.md) (usability testing), [week 9](w09-heuristic-evaluation-for-games.md) (heuristic evaluation) and [week 12](w12-surveys-and-interviews.md) (surveys and interviews) produce the findings you report here.

**Interactive:** [examples/w14-findings-triage.html](../examples/w14-findings-triage.html). Use it during section 2.

---

## 1. A report is a decision tool

A **UX research report** is the document that turns a study into decisions. It has readers with different needs. The designer who owns a feature wants to know exactly what went wrong and see the evidence. The producer wants to know what to schedule this sprint. The lead wants to know whether the build is on track. A report that serves one of them and loses the others doesn't get acted on.

The unit of a report is the **finding**, one problem (or one success) with its evidence. A good finding has five parts, and keeping them apart is most of the craft.

- **Observation.** What testers did or said, without interpretation. "4 of 5 testers opened the map while standing next to the second objective."
- **Evidence.** Where the reader can check it. Session codes and timestamps, clip links, quotes in quotation marks.
- **Interpretation.** Why you think it happened, labelled as your inference. "The quest tracker shows one objective at a time, so testers didn't know a second one existed."
- **Impact.** What it costs the player and the game, with a severity rating.
- **Recommendation.** What you suggest, framed as a direction the owner can reject. "Show all active objectives in the tracker, or add a counter such as '1 of 2'."

GD101 week 7 taught you to keep observation and interpretation in separate columns in your notes. The report keeps them in separate sentences. A reader who disagrees with your interpretation can still accept your observation, and that keeps the meeting about the game rather than about you.

Most findings in a study are not problems. Include what worked. It tells the team what not to break, and it's easier to hear the rest of the report after it.

## 2. Worked example: the blocker at the bottom of the list

### The hook

Ken Birdwell's account of how Valve made Half-Life (1998) reports that a typical two-hour playtest produced about 100 "action items," things to fix, change, add or delete. Valve ran more than 200 such sessions. Even allowing for repeats, that is thousands of items for one game. Observers were not allowed to say anything, and Birdwell describes how humbling it is to watch a tester stumble around your level for 20 minutes.

No team fixes 100 things a session. The report decides which few get fixed, and the most common way reports decide is to sort findings by how many testers hit them. Three of five testers struggled with the map icon, so it goes near the top. One tester lost the quest forever, so it goes near the bottom. This worked example shows why that ordering is wrong, and what to use instead.

### The model

You have `n` testers. For each finding:

- `x` is the number of testers who hit it, and `p̂ = x / n` the observed share.
- `[lo, hi]` is the Wilson 95% interval for the true share of players who would hit it (MA102 week 13). At `n = 5` the intervals are fixed and worth memorizing: 0 of 5 gives 0% to 43.4%, 1 of 5 gives 3.6% to 62.4%, 2 of 5 gives 11.8% to 76.9%, 3 of 5 gives 23.1% to 88.2%, 4 of 5 gives 37.6% to 96.4%, 5 of 5 gives 56.6% to 100%.
- `s` is the **severity**, on Nielsen's scale adapted for games. 1 is cosmetic (noticed, no cost). 2 is minor (costs seconds, or mild annoyance). 3 is major (costs minutes, causes a wrong decision, or strong frustration). 4 is a blocker (the player can't continue, loses progress, or quits).
- `w(s)` is a **severity weight** that says how many times worse one level is than the one below. We use `w = 1, 3, 10, 30` for `s = 1, 2, 3, 4`, roughly three times per step. The team writes these down before the study.

The **impact** of a finding is the share of players it hits times how much it hurts each one. You don't know the share, so compute the range:

```
L = lo × w(s)        (impact we are fairly sure of)
U = hi × w(s)        (impact we can't rule out)
P = p̂ × w(s)         (point estimate, for reference only)
```

Pick a **bar** `T`, the impact worth a fix this sprint. We use `T = 1`, which means "as bad as a cosmetic flaw every player sees." Then sort each finding into a tier.

- **Fix now** if `L ≥ T`. Even the optimistic reading is worth fixing.
- **Investigate** if `U ≥ T > L`. It might be serious and you don't know yet. Get more evidence (a targeted test, telemetry, a reproduction by QA) before spending on it, unless the fix is cheap.
- **Backlog** if `U < T`. Even the pessimistic reading is below the bar.

The interval width reflects how little five testers can tell you. The weight reflects what the team values. The tiers keep the two apart, so a meeting can argue about one without muddling the other.

### Numbers you can check

Five testers play the starter zone of a fictional MMO, 45 minutes each. The team logs six problems.

| Finding | `x / n` | `s` | `w` | Wilson interval | `P` | `L` | `U` | Tier |
|---|---|---|---|---|---|---|---|---|
| F1 Quest tracker hides the second objective | 4 / 5 | 2 | 3 | 37.6% to 96.4% | 2.40 | 1.13 | 2.89 | Fix now |
| F2 Selling the quest item to a vendor softlocks the quest | 1 / 5 | 4 | 30 | 3.6% to 62.4% | 6.00 | 1.09 | 18.73 | Fix now |
| F3 Talent points spend without confirmation and can't be refunded | 2 / 5 | 3 | 10 | 11.8% to 76.9% | 4.00 | 1.18 | 7.69 | Fix now |
| F4 Mailbox icon on the minimap is unreadable | 3 / 5 | 1 | 1 | 23.1% to 88.2% | 0.60 | 0.23 | 0.88 | Backlog |
| F5 Tutorial pop-up covers the boss's ground warning | 1 / 5 | 3 | 10 | 3.6% to 62.4% | 2.00 | 0.36 | 6.24 | Investigate |
| F6 System messages flood chat and hide party invites | 2 / 5 | 2 | 3 | 11.8% to 76.9% | 1.20 | 0.35 | 2.31 | Investigate |

Check two cells by hand. F2: `L = 0.036 × 30 = 1.09`, which clears the bar, so fix now. F5: `L = 0.036 × 10 = 0.36`, below the bar, and `U = 0.624 × 10 = 6.24`, far above it, so investigate.

Now sort the same six by frequency, the way many first reports do: F1 (4 of 5), F4 (3 of 5), F3 and F6 (2 of 5), then F2 and F5 (1 of 5). **The softlock is fifth of six.** The cosmetic mailbox icon is second. A producer who reads the top three and schedules them fixes a minor annoyance, a cosmetic flaw and one major problem, and ships the blocker.

Look at three more things in the table.

- **F2 is fix now with one tester.** Its lower bound is tiny, 3.6%, but a blocker weighted 30 clears the bar even at 3.6%. Rare and catastrophic beats common and cosmetic.
- **F4 can never reach fix now.** Its weight is 1, so even at 100% of players its impact is exactly 1. With five testers its upper bound is 0.88. A cosmetic finding belongs in the report, in the backlog.
- **F5 and F2 have identical frequency.** Only the severity separates them, and it separates them by a whole tier. That's why severity ratings deserve care. Nielsen recommends that three evaluators rate severity independently and that you use the mean, because one person's rating is too unreliable.

### A visual you can move

Open `examples/w14-findings-triage.html`. The left chart is the report most teams write first, one bar per finding, sorted by how many testers hit it. It looks clean and ordered. The right chart shows the same findings as horizontal interval bars from `L` to `U` on a log scale, with the point estimate as a dot, a vertical line at the bar `T`, and each bar coloured by tier.

On first load, the finding at the bottom of the left chart, F2, has the longest bar on the right, reaching past 18. Drag the number of testers from 5 to 20, keeping each finding's share fixed. The intervals shrink, but F5 and F6 stay in "investigate." More testers narrow an interval slowly. F5 (1 in 5, severity 3) first reaches "fix now" at 28 testers, and F6 (2 in 5, severity 2) is still "investigate" at 40, the slider's maximum, because its point estimate of 1.20 sits just above the bar. That's why check-yourself question 2 runs a targeted test and then lets cost decide. Then change the weights to `1, 2, 4, 8`. Almost everything slides into "investigate," and the report stops making decisions. Change them back and try `T = 2`.

### Cross-game recognition

**Valve, Half-Life (1998) and after.** Birdwell writes that Valve worked the playtest feedback back into its design process to remove designs that didn't work and build on those that did. Late in the project it added automatic logging to find problem areas objectively. Ambinder's 2009 GDC talk on Valve's playtesting shows a heatmap of where players died on a Team Fortress 2 map (with simulated numbers) and warns that averages hide extreme examples. In our terms, the heatmap is a frequency chart. It shows where many players suffered, and it needs a severity column before it can say what to fix first.

**Microsoft Games User Research, the RITE method (2002).** Medlock, Wixon, Fulton, Terrano and Romero defined Rapid Iterative Testing and Evaluation. The team changes the build as soon as a problem is identified and a solution is clear, sometimes after a single participant. In our model, that's a finding whose lower bound clears the bar at `n = 1`, which happens when severity is high, or when the fix is so cheap that the bar for it is near zero. RITE adds the cost of the fix to the decision, and section 2's model should too. GD101 week 7 introduced RITE as a way to discover more problems. Here it is also a triage rule.

**Bug trackers.** Bugzilla, and trackers modelled on it, record **severity** (how bad the problem is, from "blocker" to "trivial") separately from **priority** (when the team will fix it). Game studios' QA databases work the same way. Keeping the two fields apart is the same move as keeping `w(s)` apart from the tier. Severity is a fact about the problem. Priority is a decision that also depends on frequency and cost.

**Election polls.** A poll of about 1,000 people reports "48%, margin of error ±3 points." That's the same interval, at a sample size where it's narrow. Your five-tester report has a margin of error of about ±30 points on every frequency. Nobody would schedule an election recount on a poll of five, and nobody should rank findings on five testers' frequencies alone.

### Eyes-open design judgment

- **Set weights and the bar before the study.** If you choose them after seeing the data, you will choose the ones that rank your favourite finding first. The flat weights `1, 2, 4, 8` put five of six findings in "investigate." A report with flat weights looks careful and decides nothing.
- **Deterministic bugs skip the sampling question.** F2 is a softlock. Once QA can reproduce it every time, its frequency among testers matters less than its reproducibility. File it as a bug with steps. The frequency interval is for problems that depend on player behaviour and perception.
- **Cost belongs in the decision.** A one-line text change for F6 can go in today even though it's "investigate." A week of UI engineering for F3 should wait for a clear "fix now." Add a cost column in the tracker and let the producer weigh it.
- **"Investigate" is a plan, not a shrug.** Every investigate finding gets a named next step: which test, how many testers, which telemetry event. Otherwise it is a backlog item with extra words.
- **Report the counts, never bare percentages.** Write "2 of 5 testers (Wilson 95%: 12% to 77%)." Writing "40% of players" invites a decision the data can't support.

### Check yourself (worked example)

1. Three evaluators re-rate F6 and agree on severity 3. Recompute its `L`, `U` and tier.
2. The team runs a targeted test of F5 with 20 new testers and 4 hit the problem. The Wilson interval for 4 of 20 is 8.1% to 41.6%. What is F5's tier now? What would you say in the report?
3. Use the flat weights `1, 2, 4, 8` and `T = 1`. Which findings are fix now? Explain in one sentence why a report built on those weights is less useful.

<details>
<summary>Answers</summary>

1. `w = 10`. `L = 0.118 × 10 = 1.18`, `U = 0.769 × 10 = 7.69`. Fix now. The severity rating, not the frequency, moved it.
2. `L = 0.081 × 10 = 0.81`, `U = 0.416 × 10 = 4.16`. Still investigate, even with 20 testers. The report should say "4 of 20 (8% to 42%) had the boss warning covered; at severity 3 this may cost up to about 4 units of impact, above our bar, and at least 0.8, just below it. The fix is cheap (move the pop-up), so we recommend doing it now." Cost decides what the data can't.
3. `L` values: F1 `0.376 × 2 = 0.75`, F2 `0.036 × 8 = 0.29`, F3 `0.118 × 4 = 0.47`, F4 0.23, F5 0.14, F6 0.24. None reaches 1, so nothing is fix now. With weights that barely separate a blocker from an annoyance, five testers can never be sure of anything, so the report pushes every decision back to the meeting.

</details>

## 3. Writing one finding well

Here is a finding as it often arrives in a first draft.

> Players found the talent system confusing and didn't like it. Consider redesigning.

It fails in every part. "Players" hides how many. "Confusing" is an interpretation with no observation behind it. "Didn't like it" is an opinion survey result with no question attached. "Consider redesigning" gives the owner nothing to do. Rewrite it in the five parts.

> **F3. Talent points are spent without confirmation and can't be refunded.** Severity 3 (major), 2 of 5 testers (Wilson 95%: 12% to 77%). Tier: fix now.
>
> *Observation.* P2 and P4 clicked a talent while reading its tooltip and spent the point. Both then tried to undo it, P2 by right-clicking and P4 by pressing Escape. Neither could. P4 said "wait, I didn't mean to take that" and restarted the character (P4, 31:40 to 34:10). P2 continued with a talent she said she didn't want (P2, 22:05).
>
> *Interpretation.* Hovering and clicking are the same gesture in this screen, so reading a talent risks buying it. Players expect a way back from a menu choice.
>
> *Impact.* One tester lost about 20 minutes of progress by restarting. Both made a character choice they didn't intend at level 10.
>
> *Recommendation.* Add a confirm step for spending, or a free refund until the player leaves the talent screen. Retest with the next build.
>
> *Evidence.* Clips F3-a and F3-b.

A few rules make this form work.

- **Title the finding with the problem, not the feature.** "Talent screen" says where. "Talent points are spent without confirmation" says what.
- **Put severity, count, interval and tier on one line** so a skimming reader gets all four.
- **Quotes are short and marked.** One sentence from a tester, in quotation marks, with a timestamp. Never paraphrase a tester into a quote.
- **The recommendation is a direction.** Offer one or two options and name the retest. The designer owns the solution. Researchers who prescribe exact UI changes get argued with about the UI instead of the problem.
- **No blame.** "The talent screen spends points on click," not "the designer forgot a confirm step."

## 4. The shape of the report

Teams read reports top-down and stop early. Structure the document for that.

1. **One-page summary.** The goal of the study in one sentence, what was tested and with whom, the three to five fix-now findings in one line each, and what is working. If the producer reads only this page, the right things still get scheduled.
2. **Findings by tier.** Fix now, then investigate (each with its next step), then backlog. Inside each tier, sort by `U`, then by cost.
3. **What worked.** Positive findings in the same format, briefly.
4. **Method and limits.** Build number, tasks, tester profiles (no names), `n`, how severity was rated and by how many raters, the weights and bar. State what the study can't tell you. Five testers can't give you frequencies, and recruited testers may differ from your players.
5. **Appendix.** Full observation log, task results, survey responses, clips index.

### Tracking findings across builds

A report is a snapshot. A **findings tracker** is the living version, a table with one row per finding: ID, title, severity, tier, owner, status (open, fixed in build X, retested, closed), and the evidence for each status change.

Retests need the same honesty as the first test. After the F3 fix, you retest with six new testers and nobody hits the problem. Write "0 of 6 after fix (Wilson 95%: 0% to 39%)," not "fixed." Zero of six is good news. It still leaves room for up to about 39% of players to hit it. MA102 week 13's rule of three gives a rougher bound of `3 / 6 = 50%`. Whether that's enough depends on severity. For a cosmetic problem, close it. For a blocker, confirm by reproduction and keep watching telemetry after launch.

### Presenting it

Most reports are delivered in a meeting before anyone reads them. Keep to the order of the summary. Show one clip per fix-now finding, 20 to 40 seconds long, because watching a tester struggle persuades faster than any number. Then stop and let the owners respond. Your job in the meeting is to make sure the problems are understood. The solutions are the team's job. When a designer says "that tester just wasn't paying attention," answer with the count and the clip, not with an argument about the tester.

### Ethics of reporting

Testers trusted you with their time, faces and voices. Report codes, never names. Show clips only if the consent form covered it, and crop or blur faces when a clip goes beyond the immediate team. Don't report anything that makes a tester look foolish when the lesson is about the game. The finding is always about the design.

## In-class activity (25 minutes)

Groups of three. Each group receives an observation log from a 5-tester session of a small platformer (about 40 raw notes, with timestamps and tester codes) and a severity-rating sheet.

1. **Cluster (8 min).** Group the notes into findings. Aim for six to ten. Give each a problem-first title.
2. **Rate independently (4 min).** Each group member rates every finding's severity alone on the 1 to 4 scale. Then take the mean, rounded to the nearest whole level. Note any finding where your ratings differed by 2 or more.
3. **Triage (8 min).** Count testers per finding, look up the Wilson interval from the `n = 5` list in section 2, and compute `L` and `U` with weights `1, 3, 10, 30` and `T = 1`. Sort into tiers.
4. **Write one (5 min).** Write your top fix-now finding in the five-part form.

Expected output: the findings list with counts, three severity ratings each, `L`, `U` and tier, plus one finding written in full. Discuss the findings where raters disagreed. They are usually the ones where you disagree about who the player is.

## Common misconceptions

- **"The most common problem is the most important."** Frequency is half the impact. A blocker seen once can outrank a cosmetic flaw everyone saw. Sort by impact interval, not by count.
- **"With five testers, 3 of 5 means 60% of players."** It means somewhere between 23% and 88%. Report the count and the interval.
- **"A good report recommends exact solutions."** A good report makes the problem undeniable and suggests directions. The owner designs the fix, and the next test checks it.
- **"Not seen in the retest means fixed."** 0 of 6 still allows up to 39%. Say what the retest covered, and confirm deterministic bugs by reproduction.

## Check yourself

1. A finding hit 3 of 5 testers and has severity 2. With weights `1, 3, 10, 30` and `T = 1`, compute `L`, `U` and its tier.
2. The team changes the bar to `T = 2` after seeing the table in section 2. Which findings change tier? Why is changing the bar after seeing the data a problem?
3. Rewrite this finding in the five-part form, inventing plausible evidence: "The map is bad. Players get lost."
4. After a fix for F1, a retest with 8 testers shows 0 of 8 missing the second objective. The Wilson upper bound for 0 of 8 is 32.4%. What do you write in the tracker, and would you close the finding?

<details>
<summary>Answers</summary>

1. Interval 23.1% to 88.2%, `w = 3`. `L = 0.69`, `U = 2.65`. Investigate.
2. With `T = 2`: F1 (`L` 1.13) moves to investigate. F2 (`L` 1.09) moves to investigate. F3 (`L` 1.18) moves to investigate. F4 (`U` 0.88) stays backlog. F5 (`U` 6.24) stays investigate. F6 (`U` 2.31) stays investigate. Nothing is fix now. Changing the bar after seeing results lets the team make any finding disappear or appear. The bar is a statement of what the team can afford, and it must be set before the evidence arrives.
3. One good answer: "**F7. Players can't find the exit from the town hub.** Severity 3, 4 of 5 testers (38% to 96%). Fix now. *Observation.* P1, P2, P3 and P5 walked the hub perimeter for 2 to 6 minutes before finding the east gate; P3 asked 'is there a way out?' (P3, 08:12). *Interpretation.* The gate matches the wall texture and no path leads to it. *Impact.* 2 to 6 minutes lost at the start of the game, where week 3 says strain costs the most. *Recommendation.* A lit path or a landmark at the gate; retest next build. *Evidence.* Clips F7-a to F7-d."
4. "0 of 8 after fix in build X (Wilson 95%: 0% to 32%)." F1 is severity 2, so its impact upper bound after the fix is `0.324 × 3 = 0.97`, below the bar. Closing it is reasonable. Note that later telemetry (players opening the map near the objective) can confirm it at scale.

</details>

## Lab hook

[Lab 14, findings triage and research report](../labs/lab14.md). You turn a provided observation log from a five-tester session into a findings list, rate severity independently with two classmates, run the starter triage script, and write a report in the structure of section 4 with a one-page summary and a findings tracker. Deliverable: the report and the tracker. The lab is a dry run for the final UX study of a shipped game in week 15.

## Sources

- Birdwell, K. (1999). "The Cabal: Valve's Design Process for Creating Half-Life." Game Developer (Gamasutra), December 10, 1999. More than 200 play-test sessions; about 100 action items from a typical two-hour session; observers not allowed to speak; testers stumbling for 20 minutes; feedback worked back into the design process; later automated logging.
- Ambinder, M. (2009). "Valve's Approach to Playtesting: The Application of Empiricism." Game Developers Conference, March 2009. Slides from Valve's publications page. Death-concentration heatmap for Team Fortress 2's Dustbowl map (marked as simulated numbers); "averages hide extreme examples."
- Nielsen, J. (1994). "Severity Ratings for Usability Problems." Nielsen Norman Group, November 1, 1994. Frequency, impact and persistence as components of severity; the 0 to 4 scale from "not a usability problem" to "usability catastrophe"; independent ratings from about three evaluators, averaged.
- Wikipedia, "RITE Method" (accessed September 2026). Defined in 2002 by Medlock, Wixon, Fulton, Terrano and Romero; changes made as soon as a problem is identified and a solution is clear, sometimes after one participant; decision makers on the research team.
- Bugzilla documentation, "Understanding a Bug" (bugzilla.readthedocs.io, latest). Severity from "blocker" to "trivial"; priority as a separate field for scheduling.
- Wilson intervals are computed with `z = 1.96` as in MA102 week 13.
- The starter-zone study, the six findings, the severity weights `1, 3, 10, 30`, the bar `T = 1` and all tester quotes and timestamps are teaching examples, not data from any game.

## Interactive spec: examples/w14-findings-triage.html

**Purpose.** Show that a report sorted by frequency buries rare severe problems, and that interval-based impact tiers make the uncertainty and the team's values visible and separate.

**The one insight the visual must make obvious.** The finding at the bottom of the frequency-sorted chart (F2, the softlock, 1 of 5) has the longest impact bar on the right, reaching 18.7, and sits in "fix now."

**Layout.** Two charts side by side at 1280px, stacked at 390px (frequency chart first, so the reveal comes second). Controls and a findings table below.

- Left, "Sorted by how many testers hit it": horizontal bars of `x` (0 to `n`), findings sorted by `x` descending, ties broken by ID. Label each bar "F2 · 1 of 5". Neutral colour for all bars.
- Right, "Impact we're sure of to impact we can't rule out": one row per finding, same row order as the tier sort (fix now, investigate, backlog; within tier by `U` descending). Horizontal interval from `L` to `U` on a log-scale x axis from 0.1 to 50, a dot at `P`, and a vertical line at `T` labelled "bar". Bars are coloured and patterned by tier (fix now solid, investigate striped, backlog outline) with the tier name in text at the row end.
- Hovering or focusing a finding in either chart highlights it in both.

**Data (defaults).** `n = 5`. Findings (ID, title, `x`, `s`): F1 "Quest tracker hides second objective" 4, 2. F2 "Selling quest item softlocks quest" 1, 4. F3 "Talent points spend without confirm" 2, 3. F4 "Mailbox minimap icon unreadable" 3, 1. F5 "Tutorial pop-up covers boss warning" 1, 3. F6 "System messages hide party invites" 2, 2.

**Controls.**

- Testers `n`: slider 1 to 40, default 5. Mode toggle: "keep counts" (x fixed, clamp to `n`) or "keep shares" (default; `x = round(p̂₀ × n)` where `p̂₀` is the default share).
- Per finding: `x` (number input 0 to `n`) and severity (select 1 to 4).
- Weights `w(1..4)`: four number inputs, defaults 1, 3, 10, 30. Preset buttons "Steep (1, 3, 10, 30)" and "Flat (1, 2, 4, 8)".
- Bar `T`: slider 0.25 to 5, step 0.25, default 1.
- Confidence: radio 90% (`z = 1.645`) or 95% (`z = 1.96`, default).
- Add finding (up to 10) with editable title; delete finding.
- Reset.

**Formulas.**

- `p̂ = x / n`. Wilson: `centre = (p̂ + z²/(2n)) / (1 + z²/n)`, `half = z × sqrt(p̂(1 − p̂)/n + z²/(4n²)) / (1 + z²/n)`, `lo = max(0, centre − half)`, `hi = min(1, centre + half)`.
- `L = lo × w(s)`, `U = hi × w(s)`, `P = p̂ × w(s)`.
- Tier: fix now if `L ≥ T`; investigate if `U ≥ T > L`; backlog if `U < T`.
- On the log axis, draw `L = 0` at the left edge (0.1) with an arrow showing it continues.

**Findings table.** Columns ID, title, `x / n`, severity, weight, Wilson interval (%, one decimal), `P`, `L`, `U` (two decimals), tier. Plus a summary line: "3 fix now, 2 investigate, 1 backlog. Frequency sort puts F2 in position 5 of 6."

**Test values.**

- Defaults: F1 37.6% to 96.4%, `L` 1.13, `U` 2.89, fix now. F2 3.6% to 62.4%, `L` 1.09, `U` 18.73, fix now. F3 11.8% to 76.9%, `L` 1.18, `U` 7.69, fix now. F4 23.1% to 88.2%, `L` 0.23, `U` 0.88, backlog. F5 `L` 0.36, `U` 6.24, investigate. F6 `L` 0.35, `U` 2.31, investigate. Frequency order F1, F4, F3, F6, F2, F5.
- Flat weights: `L` F1 0.75, F2 0.29, F3 0.47, F4 0.23, F5 0.14, F6 0.24; F4 backlog, all others investigate.
- `T = 2`, steep weights: no fix now; F4 backlog; others investigate.
- 90% confidence, defaults: F1 43.5% to 95.4% (`L` 1.31), F2 4.6% to 56.5% (`L` 1.38, `U` 16.94), F5 `L` 0.46, `U` 5.65.
- F6 severity changed to 3: `L` 1.18, `U` 7.69, fix now.
- F5 with `x = 4`, `n = 20` (keep counts): 8.1% to 41.6%, `L` 0.81, `U` 4.16, investigate.
- `x = 0`, `n = 6`: interval 0% to 39.0%.
- Keep shares, `n = 20`: F5 is 4 of 20 (`L` 0.81) and F6 is 8 of 20 (`L` 0.66), both still investigate. F5 first reaches fix now at `n = 28` (6 of 28, `L` 1.02). F6 is still investigate at `n = 40` (16 of 40, `L` 0.79).

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark. Tiers differ by pattern and text label as well as colour. All controls keyboard operable with visible focus; chart rows reachable by Tab with the highlight shown in both charts. The findings table is a real `<table>` with headers, and the summary line uses `aria-live="polite"`. Respect reduced motion (no animated bar transitions when set). No game art, logos or screenshots.
