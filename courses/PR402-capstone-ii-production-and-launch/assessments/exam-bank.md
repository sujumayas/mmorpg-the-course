# PR402 · Exam bank: viva and reflection questions

PR402 has no written exam. Each student sits a 15-minute viva in week 15 or the exam period, worth 25 of the 100 points in the [post-mortem brief](post-mortem-brief.md). The same questions are prompts for the individual reflection, for the weekly live review and for sprint retrospectives.

## How the bank is used

- **In the viva.** Two examiners pick five or six questions and rewrite them with the team's own numbers: its lab sheets, dashboards, incident log, ledger and sprint records. At least two questions must be about a part of the game the student did not build. The repository, the dashboard and the live game are open, and the student may look things up. Knowing where to look is part of the answer.
- **For practice.** Answer each question for your own launched game before week 15. If you need a teammate to answer one, ask them now, not in the viva.
- **Types.** Each question is tagged **explain** (say why, with a number from your game), **compute** (redo a calculation with your data), **critique** (find the weakness in a decision) or **reflect** (what you would do differently, as a checkable change).

## Marking scale for every question

Each question is marked 0 to 5. The viva row is `total / (5 × questions asked) × 25`.

| Mark | Meaning |
|---|---|
| 5 | Correct concept, applied with the team's real numbers or records, trade-off stated, limits of the evidence acknowledged |
| 4 | Correct and specific, but one of numbers, trade-off or limits is missing |
| 3 | Correct in general terms; could be about any game |
| 2 | Partly correct, or correct only for the part the student built |
| 1 | Vague, or relies on a teammate's explanation the student cannot extend |
| 0 | Wrong, or no answer |

The guidance under each question says what a 5 contains and what usually drags an answer down. Model numbers come from the course's constructed Emberfall team (continued from PR401) unless the question says otherwise. In the viva, the examiner replaces them with yours.

---

## A. Capacity, the ops tax and the content pipeline

Links: [week 1](../lectures/w01-production-sprint-1-the-ops-tax.md), [week 2](../lectures/w02-production-sprint-2-content-pipeline.md), [week 3](../lectures/w03-production-sprint-3-feature-complete-and-server-budget.md), [PR401 week 11](../../PR401-capstone-i-pre-production/lectures/w11-production-plan.md), [PR101 week 6](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md), [PR101 week 7](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md).

1. *Compute.* Take your team's rate `r` from the PR401 slice sprints and your weekly hours `H`. What feature budget did your week 1 tax schedule give for weeks 1 to 3, and how many feature points did you cut to fit it?

<details>
<summary>Marking guidance</summary>

The formulas are `r = done points / available hours`, `v = r × H`, `c_w = v × (1 − t_w)`, and `F = c_1 + c_2 + c_3`. Emberfall: `r = 32 / 92 = 0.348`, `v = 29.2`, taxes 0.10, 0.15, 0.20, `F = 74.5` against 106 feature points, a cut of 31.5. A 5 gets the team's own arithmetic right, names the largest cut and its pillar, and says whether the cut held until alpha. A 3 has the formula without the team's numbers. Anyone who counts half-done stories in `r` scores at most 2, because every later number inherits the inflation.

</details>

2. *Explain.* What was your measured ops tax in the week of closed beta, and how far was it from the value you planned in week 1? What did the team change because of the gap?

<details>
<summary>Marking guidance</summary>

A 5 gives planned and measured `t` for that week from the tagged time log (Emberfall planned 0.55), states whether the gap exceeded the 0.1 replanning threshold, and names the replan: the cut line moved, a trigger item dropped, or an ops-reducing story pulled forward. It also says how bugs in a story's own code were tagged, since tagging them `ops` makes velocity look better than it is. A student who cannot say where the measured value came from scores at most 2.

</details>

3. *Critique.* The deploy script, the crash reporter and the admin tools are often the first things a team cuts. Did yours cut any of them? Use your interrupt log from week 10 or 11 to say what that decision cost or saved.

<details>
<summary>Marking guidance</summary>

The argument from week 1 is that ops-reducing stories cost points once and repay them every week from alpha to the showcase. A 5 names the story, its cost in points or hours, and a measured effect from the interrupt log (for example deploy hours per week before and after, or restart hours removed by a watchdog). If the team cut one, a 5 estimates what it cost using the log. A 3 repeats the argument without numbers.

</details>

4. *Compute.* Which stage of your content pipeline was the bottleneck in week 2? Show its capacity `m_s = h_s / k_s`, the throughput, and the forecast number of items by content lock.

<details>
<summary>Marking guidance</summary>

Emberfall's plan A had scripting at `9 / 9 = 1.0` quest a week, so `X = 1.0` and four quests in the four production weeks. A 5 uses the team's measured touch hours, names the bottleneck, and explains why adding hours to another stage did not raise output (Emberfall's plan B added art hours and still shipped four). It also says which stage became the bottleneck after the fix. Answers that name the stage that "looked worst" without numbers score at most 2.

</details>

5. *Explain.* Use Little's law to explain what happened to the items your team started early in the pipeline. What WIP limit did you set, and what lead time did it give?

<details>
<summary>Marking guidance</summary>

`W = WIP / X`. Emberfall started eight quests with `X = 1.0`, a lead time of eight weeks, longer than the four production weeks; a WIP limit of 3 at `X = 1.5` gave two weeks. A 5 gives the team's own WIP, throughput and lead time, and says how many items were half-built at content lock. A 3 states the law correctly without the team's numbers. Confusing throughput with capacity at a non-bottleneck stage drops the mark to 2.

</details>

6. *Critique.* Your week 3 hosting budget split cost into lines that follow players and lines that follow the clock. Which dominated your actual bill by the showcase, and did your schedule changes hold?

<details>
<summary>Marking guidance</summary>

Emberfall's naive plan was $743.50, of which the player-driven lines (the peak zone server, the launch-week second shard and egress) were $133.90, about 18%. The fixed plan scheduled staging and pre-beta production to reach $448.30. A 5 compares the plan with the provider's billing history in `spend-log.md`, names the largest line, and mentions any forgotten resource (a bot fleet over a weekend). A student who says "players are the main cost" without evidence scores at most 2.

</details>

## B. Alpha and triage

Links: [week 4](../lectures/w04-alpha-review-and-bug-triage.md), [PR101 week 10](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md), [MMO302 week 8](../../MMO302-mmo-server-architecture/lectures/w08-item-ownership-and-transactional-integrity.md), [MMO407 week 6](../../MMO407-launch-scaling-and-post-mortems/lectures/w06-case-duplication-exploits-after-launch-new-world-2021.md).

7. *Explain.* Pick one line of your alpha exit criteria. Why is it a test a stranger could run, and which of the four meanings of "feature complete" does it check?

<details>
<summary>Marking guidance</summary>

The four meanings in week 3 are: every system in and connected, no placeholder logic, server authority on value paths, and running where testers will run it. A 5 reads the line, shows that it has an observable pass condition, names the meaning, and says whether it passed at the review. "Parties work" style lines score at most 2, because they cannot fail.

</details>

8. *Compute.* Take one non-gate bug from your alpha triage sheet. Compute its impact and its impact per fix hour. Where did it rank, and did it make the fix plan?

<details>
<summary>Marking guidance</summary>

`I = sessions × reach × weight(severity)`, weights S1 10, S2 4, S3 1, S4 0.2, then `I / hours`. Emberfall's B4: `450 × 0.25 × 4 = 450`, `450 / 8 = 56.25` per hour, ranked second and fixed. A 5 also compares the alpha reach guess with the reach measured by the telemetry event added for closed beta. Sorting by severity alone and calling it triage scores at most 2.

</details>

9. *Explain.* Why are exploits on value paths gates in this course, however rare they look? Point to one in your own game, or to the value path most at risk.

<details>
<summary>Marking guidance</summary>

The accidental reach of a duplication bug is tiny. Its real reach is everyone who hears about it, because exploits are found deliberately and spread by word of mouth (MMO407 week 6). A 5 names a specific value path (trade, bank, crafting, mail), how the server protects it (a single transaction with an idempotent grant, MMO302 week 8), and what the kill switch is. An answer that runs an exploit through the impact formula scores at most 2.

</details>

10. *Critique.* Did your team use a workaround to avoid fixing a bug before closed beta? What other bug's reach did it change?

<details>
<summary>Marking guidance</summary>

Week 4's example: scheduled restarts hid a memory leak (B7) and made a restart-during-trade data-loss bug (B2) routine. A 5 names the team's workaround, checks the bug list for interactions, and says what happened in the logs. If the team used none, a 5 names the workaround it was tempted by and the interaction that ruled it out. Generic answers score 3.

</details>

## C. Closed and open beta

Links: [week 5](../lectures/w05-closed-beta-recruiting-and-stress-windows.md), [week 8](../lectures/w08-open-beta.md), [MMO407 week 3](../../MMO407-launch-scaling-and-post-mortems/lectures/w03-beta-strategies.md), [MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md), [MMO308 week 5](../../MMO308-live-operations-analytics-and-experimentation/lectures/w05-ab-testing-design.md).

11. *Compute.* Work backwards from your closed-beta target concurrency to the invites you needed. Then give the measured `p_start` and `p_window`. How many invites would the measured rates have required?

<details>
<summary>Marking guidance</summary>

`invites = ceil(ceil(target / p_window) / p_start)`. Emberfall: target 60, `p_window = 0.40`, `p_start = 0.45`, so 150 active testers and 334 invites. A 5 recomputes with the team's measured rates, says how batch 2 was resized after 24 hours, and states the real peak in each window with humans and bots apart. A student who cannot separate bots from humans in the reported peak scores at most 2.

</details>

12. *Explain.* Why did your closed beta need scheduled stress windows? Use your own session data to show the concurrency you would have seen without them.

<details>
<summary>Marking guidance</summary>

Without windows, `average CCU = testers × sessions × hours / 168`. Emberfall's 150 testers at three 1.5-hour sessions gave 4.0 on average and about 12 at an evening peak, a fifth of launch-evening load. A 5 uses the team's own player-hours, compares that figure with the window peaks it measured, and names one problem that only appeared above the no-window peak. A 3 explains the idea without numbers.

</details>

13. *Compute.* What rate of bug could your closed beta rule out, and what did that mean for launch week?

<details>
<summary>Marking guidance</summary>

By the rule of three, a bug never seen in `E` player-hours has a rate below `3 / E` at 95%. Emberfall: `E = 675`, so below once per 225 player-hours, while launch week was forecast at 3,150 player-hours, so an unseen bug could still fire up to 14 times. A 5 uses the team's exposure and launch forecast and says what the team did about the gap (open beta sizing, rota, kill switches). "The beta was clean so the game is stable" scores at most 1.

</details>

14. *Explain.* What consent notice, data minimum and wipe policy did your betas use? Why is telemetry keyed on a game-generated ID and not an email?

<details>
<summary>Marking guidance</summary>

A 5 states what was collected, why, for how long and whom to contact, where the notice appeared before first play, and where the invite list with contact details was kept and when it is deleted. It explains that game IDs let the team analyse behaviour without holding personal data in the telemetry store, which limits the damage of a leak and the university's exposure. It also states the wipe policy and whether the team kept its promise. Vague answers ("we had a privacy page") score 2.

</details>

15. *Compute.* Size your open beta. What exposure target did you choose, how many sign-ups did it need, and what was the forecast peak against safe capacity?

<details>
<summary>Marking guidance</summary>

`E = 3 × (player-hours per firing)`, `sign-ups = E / (show-up × hours)`, `peak = E × busiest-day share × busiest-hour share × spike`, `safe = knee × (1 − headroom)`. Emberfall: 1,200 player-hours, 1,067 sign-ups, forecast peak 97.2 against safe capacity 98, cut to 77.8 with waves. A 5 uses the team's own inputs with sources and names the lever chosen. A student who cannot say which bug rate the target was built for scores at most 2.

</details>

16. *Critique.* Put your open-beta forecast beside the actuals. Which input had the largest error, and how did you carry that error into the launch forecast?

<details>
<summary>Marking guidance</summary>

A 5 reads the lab 08 section C table, names the input with the largest error ratio (often show-up rate or busiest-hour share), traces how it moved the peak forecast, and shows the same ratio applied to the launch arrival phases in lab 09. It also says whether the correction turned out right at launch. A student who treats the forecast as a target the team hit or missed, rather than a model to correct, scores at most 2.

</details>

## D. Telemetry and balance

Links: [week 6](../lectures/w06-telemetry-and-balance-review.md), [PR401 week 8](../../PR401-capstone-i-pre-production/lectures/w08-economy-and-balance-design.md), [MMO308 week 6](../../MMO308-live-operations-analytics-and-experimentation/lectures/w06-ab-testing-statistics-and-pitfalls.md), [MMO302 week 14](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md).

17. *Explain.* What three contaminations did your cleaning script check for, and what did it find in your closed-beta export?

<details>
<summary>Marking guidance</summary>

Internal accounts (removed by ID, not by name), stale builds (events tagged by build and split), and broken counts (sessions that start must end, quest completions cannot exceed starts). A 5 gives the before and after counts from the cleaning log and one thing the check caught. A student who removed developers by name, or never split builds, scores at most 2.

</details>

18. *Critique.* A teammate reports a class's kill time as "13.1 seconds across 400 kills, interval 12.7 to 13.5". What is wrong? Show the correct interval for one row of your own balance sheet.

<details>
<summary>Marking guidance</summary>

Kills cluster inside players, so `n` must count players. The 400-kill interval is about the square root of kills per player too narrow. Emberfall's Warden with nine players gives 11.26 to 14.94 s, which crosses the band edge, so the verdict is "can't decide", not "leave". A 5 recomputes one of the team's rows with `m ± t × s / √n` and the right `t`. Using 1.96 for `n = 6` loses a mark.

</details>

19. *Compute.* Size one balance change your team shipped. What damage multiplier did the formula give, what value did it predict, and what did the next data show?

<details>
<summary>Marking guidance</summary>

`multiplier = (current − approach) / (target − approach)`. Emberfall's Hexer: `(8.9 − 2.0) / (11.0 − 2.0) = 0.767`, a 23% cut aimed at 11 s. A 5 gives the team's own change, why it aimed where it did in the band, and compares the prediction with open-beta or live data with an interval (for example 11.4 s with `n = 40`, `s = 1.7` gives about 10.86 to 11.94 s, inside the band). Changing two levers on one class loses a mark, because the next review cannot separate them.

</details>

20. *Reflect.* Which balance question did your team leave as "can't decide", and was the targeted test in open beta big enough to settle it? What would you do with that question now?

<details>
<summary>Marking guidance</summary>

The players needed are roughly `(1.96 × s / gap)²`, where `gap` is the distance from the mean to the nearer band edge. Emberfall's Warden needed about 46 players. A 5 gives the team's test, its planned and reached `n`, the verdict, and whether the test stopped at its planned sample or was peeked at. If it did not reach its sample, a 5 says so and states the risk the team accepted. Reading "can't decide" as "leave" scores at most 2.

</details>

## E. Sprint 4 and the lock

Links: [week 7](../lectures/w07-production-sprint-4.md), [PR101 week 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md), [PR101 week 5](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w05-agile-and-scrum-adapted-for-games.md).

21. *Compute.* Rebuild your sprint 4 commitment: planning and conservative capacity, the interrupt buffer and its data source, and the commitment at each line.

<details>
<summary>Marking guidance</summary>

`capacity = velocity × availability`, rounded down; `buffer = expected must-fix bugs × mean points per bug`; `commitment = capacity − buffer`. Emberfall: 27 and 25 points (33 of 35 person-days), buffer `8 × 1.5 = 12`, commitments 15 and 13. A 5 uses completed points only, names the tracker query behind the buffer, and says how the buffer compared with the bugs that arrived. If the away teammate had been available all five days, Emberfall's planning capacity would be 29 and the commitment 17, still short of item D's running total of 18, so D stays stretch.

</details>

22. *Explain.* What did your burn-down show on day 3 of sprint 4, and what did the team do? Why does a cut on day 3 free more than a cut on day 5?

<details>
<summary>Marking guidance</summary>

The remaining line falls at the completion rate minus the bug rate. The day-3 threshold is the ideal line plus one average item (Emberfall: `6.0 + 3 = 9.0` for a 15-point commitment). A 5 reads the team's day-3 row, states the decision, and explains that a cut on day 5 frees nothing because the time has already been spent on the item. A team with no day-3 record scores at most 2.

</details>

23. *Critique.* Name one item that went to your post-launch list at the lock, and one that went to the cut list. Were those the right calls, judged by what players asked for after launch?

<details>
<summary>Marking guidance</summary>

A 5 names both items with the reasons written at the time, then uses post-launch evidence (tickets, requests, the patch candidate table) to judge them. Emberfall's fast travel and guild bank went to post-launch and came back as week 12 candidates; the cosmetic shop was cut. It also says whether anything slipped past the lock into the open-beta build. Hindsight without the dated reason scores 3 at most.

</details>

## F. Launch

Links: [week 9](../lectures/w09-launch.md), [MMO407 week 2](../../MMO407-launch-scaling-and-post-mortems/lectures/w02-capacity-planning-and-login-queues.md), [MMO407 week 9](../../MMO407-launch-scaling-and-post-mortems/lectures/w09-communication-during-crises.md), [MMO407 week 13](../../MMO407-launch-scaling-and-post-mortems/lectures/w13-launch-plan-workshop.md), [MMO302 week 2](../../MMO302-mmo-server-architecture/lectures/w02-shards-realms-zones-instances-layers.md), [MMO308 week 9](../../MMO308-live-operations-analytics-and-experimentation/lectures/w09-patch-management-and-hotfixes.md).

24. *Explain.* Walk through your go or no-go record. Which criterion was closest to failing, and what had the team decided in advance would happen if it failed?

<details>
<summary>Marking guidance</summary>

A 5 names the criterion, its evidence and owner, and the "if fail, then" line committed before the review (a lower cap, trading switched off, delay). It shows from the commit history that criteria predate the review. It explains why a failed rollback test means no-go while a failed load test can mean a lower cap. Criteria written during the review score at most 1.

</details>

25. *Compute.* Rerun your launch queue model for one shard. Where was the worst queue, and what was the wait at the back?

<details>
<summary>Marking guidance</summary>

While filling, admissions are the lesser of arrivals and entry rate; once full, admissions are `cap / session length`. Emberfall: cap 100, 50-minute sessions, so 2 places a minute; arrivals 2.5, then 2.25, then 0.8 a minute; the queue reached 40 at minute 180, a 20-minute wait, over the 15-minute limit. A 5 explains why the worst wait came at hour 3, not in the first hour, and compares the model with the queue observed at launch. Answers that treat the first hour as the peak score at most 2.

</details>

26. *Critique.* Did your team open more than one shard at launch? Judge the choice against your alive threshold and the day-7 peak you actually saw.

<details>
<summary>Marking guidance</summary>

Two permanent shards halve the day-7 population (Emberfall: 30 per shard against an alive threshold of 40), so a second shard needs a merge trigger tested on staging. A 5 gives the team's trigger, whether it fired, and the merge log, or explains why one shard with a cap and an honest queue message was the better risk. The smallest alive threshold at which two permanent Emberfall shards pass is 30. "More shards is safer" scores at most 2.

</details>

27. *Explain.* Show one player-facing message from launch week. When did the incident start, when did the message go out, and what did it promise?

<details>
<summary>Marking guidance</summary>

The rules from MMO407 week 9: acknowledge within 15 minutes, promise the time of the next update and keep it, never promise a fix time. A 5 reads the message and its timestamp against the incident log, and says whether the next-update promise was kept. It also says where the message was posted and why that channel stays up when the game is down. A message that promised a fix time loses at least two marks unless the student names that as the error.

</details>

28. *Compute.* Report day-1 retention for your launch cohort with a Wilson interval. Can you say it met your PR401 target?

<details>
<summary>Marking guidance</summary>

Emberfall's week 10 dashboard: 99 of 260 returned, 38.1%, Wilson 95% interval about 32.4% to 44.1%. A target of 35% sits inside it, so the honest report is "consistent with target, not yet above it". A 5 does the same with the team's cohort and says what a cohort of that size can and cannot distinguish. Reporting a percentage with no `n` scores at most 2.

</details>

## G. Live operations

Links: [week 10](../lectures/w10-live-ops-week-1.md), [week 11](../lectures/w11-live-ops-week-2-operating-rhythm.md), [MMO308 week 1](../../MMO308-live-operations-analytics-and-experimentation/lectures/w01-what-live-ops-is.md), [MMO308 week 3](../../MMO308-live-operations-analytics-and-experimentation/lectures/w03-cohorts-and-retention-curves.md), [MMO308 week 9](../../MMO308-live-operations-analytics-and-experimentation/lectures/w09-patch-management-and-hotfixes.md), [MMO308 week 13](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md), [MMO302 week 14](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md), [PR101 week 12](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w12-crunch-causes-costs-alternatives.md).

29. *Compute.* Compute the break-even harm for a hotfix in your game at a typical point in week 10. Which issue in your triage sheet sat closest to it, and what did you decide?

<details>
<summary>Marking guidance</summary>

`h* = (D + r × H) / T`, with `D` the restart disruption in player-hours. Emberfall: `D = 40 × 5 / 60 = 3.3`, `r × H = 0.15 × 30 = 4.5`, `T = 48`, so `h* = 0.16` player-hours per hour. A 5 uses the team's values, states the basis of `h` for the nearest issue, and explains why break-even is necessary but not enough: fix capacity decides. With a restart-free path (`D = 0`), Emberfall's break-even falls to about 0.09, and the tooltip issue at 0.02 still does not qualify.

</details>

30. *Explain.* Describe the worst SEV1 in your game after launch. What was mitigated first, by whom, and how long did the follow-up take?

<details>
<summary>Marking guidance</summary>

A 5 gives the timeline from the incident log: detection, the switch or revert that stopped the harm, the player message, the fix, the postmortem. It names the roles (incident commander who does not debug, one person on production, one writing to players) and the follow-up hours, compared with the six hours per incident used in week 10's capacity line. It explains why a duplication exploit is SEV1 even with healthy servers. Answers that start with the code fix score at most 2.

</details>

31. *Compute.* What was your team's interrupt fraction in week 10, and how many hours did it leave for planned work? How does it compare with the ops tax you planned in week 1?

<details>
<summary>Marking guidance</summary>

`i = I / C`, `P = C − I`. Emberfall: `46 / 84 = 54.8%`, 38 planned hours against 59 assumed. A 5 uses the team's tagged log, breaks `I` into the five categories, names the largest driver, and connects `i` to the week 1 `t` (they are the same quantity). A student whose log tagged interrupts as sprint tasks, and who does not notice it, scores at most 2.

</details>

32. *Compute.* Use Little's law on your support queue. What was the average wait, and what queue length would have met your wait target?

<details>
<summary>Marking guidance</summary>

`W = L / λ`, `L_target = λ × W_target`. Emberfall: `L = 27`, `λ = 6` a day, `W = 4.5` days; after the item-loss fix `λ = 3.86`, so about 4 open tickets for a one-day wait. A 5 uses daily open counts at a fixed time, not hand-timed tickets, and explains why the law holds whatever the mix of easy and hard tickets. It names the top ticket cause and its share. Recomputing Emberfall's week 11 (9 open, 30 a week) gives 2.1 days, which misses a one-day target.

</details>

33. *Critique.* Which one-off fix in your buy-back plan had the shortest payback? Did the week 12 log confirm the hours it was supposed to remove?

<details>
<summary>Marking guidance</summary>

`payback = cost / weekly hours removed`. Emberfall's plan cost 21.7 hours to remove 14 a week, 1.55 weeks. A 5 names the team's fix, its forecast and the measured change in the week 12 log, and says whether the savings arrived. A watchdog that restarts into the same crash loop saves nothing. Counting savings that were never measured scores at most 2.

</details>

34. *Explain.* A low day-1 cohort in your table: was it the tutorial or the calendar? How did you check?

<details>
<summary>Marking guidance</summary>

An outage on one day is a period effect. It shows up at a different install date in each Dn series. A 5 marks incident dates on the cohort table, checks whether the low cohort's day 1 fell on an outage day, and only then looks at the tutorial funnel. It reports the cohort with `n` and an interval (for example 70 of 260 at D7 is about 22% to 33%). Blaming the tutorial without the check scores at most 2.

</details>

35. *Reflect.* Was your on-call load sustainable? Use the rota and the time log to say who carried it, and what you would change in the rota for a second month of live operation.

<details>
<summary>Marking guidance</summary>

The SRE limits in week 10 are a reference, not a rule for students: on call at most 25% of time, at most two incidents per 12-hour shift. A 5 gives on-call hours per person against the team's agreed limit, names any imbalance, and proposes a checkable change (a rotation length, a paging rule, a watchdog). Answers that praise individual heroics score at most 2, since the rota exists so the person who makes the 03:00 decision has slept.

</details>

## H. The patch

Links: [week 12](../lectures/w12-patch.md), [PR101 week 6](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md), [PR101 week 13](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md), [MMO308 week 9](../../MMO308-live-operations-analytics-and-experimentation/lectures/w09-patch-management-and-hotfixes.md).

36. *Compute.* Rebuild your patch budget: `H`, release work `X`, `A`, your plan ratio `R`, and the estimate budget `E`.

<details>
<summary>Marking guidance</summary>

`A = H − X`, `R = Σ actual / Σ estimate`, `E = A / R`. Emberfall: `H = 68.3`, `X = 10`, `A = 58.3`, `R = 1.35`, `E = 43.2`. A 5 uses the team's figures, says which sprints `R` came from and why, and explains why release work stays out of the slack. Another team with `H = 50`, `X = 8`, `R = 1.6` would have `E = 26.3`. Comparing raw estimates with hours, as if `R` were 1, scores at most 2.

</details>

37. *Explain.* What was your patch's cut order, and did you use it? If a surprise had cost ten hours during the week, what would have left first?

<details>
<summary>Marking guidance</summary>

The cut order is the selection read from the bottom. Emberfall's first to leave was the ash-storm event, which freed `14 × 1.35 = 18.9` hours. A 5 gives the team's order, shows it was committed before feature freeze, and answers the ten-hour case with the items that would go and the hours freed at the team's `R`. It explains why an event is usually the riskiest item.

</details>

38. *Critique.* Did your patch ship on its announced date? Compare the expected actual hours with the actual hours, and say whether your choice of `R` was the safer one.

<details>
<summary>Marking guidance</summary>

Emberfall forecast 52.7 hours and took 50, an error of −5.1%; sprint 4's ratio alone would have forecast 47.1, 6.0% under. A 5 does the same with the team's numbers, states whether the patch hit its date, and names any cut made on the way with its reason. A no-go tied to a criterion and a new announced date is an acceptable answer. A silent slip is not.

</details>

39. *Explain.* Pick one item your patch shipped. What number did you expect it to move, and what did the number do a week later?

<details>
<summary>Marking guidance</summary>

A 5 names the metric written before release (tickets for item loss, D1 for a tutorial fix, a class pick rate), its before and expected values, the actual value with `n`, and whether the change can be told apart from noise at that sample. It mentions anything else that changed in the same week. An item with no expected number, or a claim that "players liked it", scores at most 2.

</details>

## I. The economy

Links: [week 13](../lectures/w13-economy-review.md), [PR401 week 8](../../PR401-capstone-i-pre-production/lectures/w08-economy-and-balance-design.md), [MMO308 week 12](../../MMO308-live-operations-analytics-and-experimentation/lectures/w12-economy-monitoring.md), [MMO302 week 8](../../MMO302-mmo-server-architecture/lectures/w08-item-ownership-and-transactional-integrity.md).

40. *Compute.* Take your latest full week of ledger data. What was the net flow per active player, and how much did wealth per active player change since launch?

<details>
<summary>Marking guidance</summary>

`m_t = m_(t−1) + (F_t − S_t) / N_t`. Emberfall's week 12: net 310k over 240 players, 1,291.7 per player, and `m` rose from 1,800 to 6,095 in four weeks. A 5 uses the team's ledger and denominator (weekly active accounts, bots removed, alts handled) and states it. Another team with `F = 900k`, `S = 810k`, `N = 150` gains 600 per player a week despite a sink ratio of 0.90.

</details>

41. *Explain.* Your total net inflow may have fallen every week since launch. Why does that not mean the economy is settling?

<details>
<summary>Marking guidance</summary>

When faucets and sinks scale with players, the weekly rise per player is `φ − σ`, which does not depend on `N`. Players leaving shrink every total but leave each remaining player's weekly gain where it was. Emberfall's total net inflow fell 57% while net per player fell only 28%. A 5 shows this with the team's own table and a price in the basket. An answer that uses the sink ratio as evidence of health scores at most 2.

</details>

42. *Critique.* Did your model's `m × N` match the currency actually held by active accounts? What explained the largest gap?

<details>
<summary>Marking guidance</summary>

The model assumes leavers hold average wealth and ignores new accounts. A 5 gives the gap per week from the direct query and explains any gap over 10% with evidence: poor tourists leaving (model too low), many new accounts, currency in mail or escrow, or a duplication bug. It says whether the gap changed the team's decision. A team that never ran the check scores at most 2.

</details>

43. *Compute.* What growth target `g` did you set, and how large a cut did it require? Why could a trade fee alone not deliver it in your game?

<details>
<summary>Marking guidance</summary>

`cut = (φ − σ) − g × m`. Emberfall: `1,291.7 − 0.03 × 6,095.4 = 1,108.8` marks per player per week. A stall fee rise alone would need `f = 1,108.8 / 8,750 = 12.7%` of stall sales, high enough to push trade off the stalls, so the real removal would be much smaller. A 5 gives the team's `g` with its reason, the cut, and at least one option with a behavioural response. Sizing a fee as if nobody reacts scores at most 2.

</details>

44. *Reflect.* Who paid for your economy decision? Use your cohort table to say which players felt it, and whether you would choose the same lever again.

<details>
<summary>Marking guidance</summary>

A faucet cut on quests hits levelling players, who may be the newest and most at risk of leaving. A fee hits traders and crafters. A 5 names the lever, the cohorts still earning from it, how the change was announced, the metric and check date, and the rollback. "No change" is a full-mark answer if the student gives the action level and the argument. A decision announced after it shipped loses at least one mark.

</details>

## J. Post-mortem and reflection

Links: [week 14](../lectures/w14-post-mortem.md), [PR401 week 14](../../PR401-capstone-i-pre-production/lectures/w14-pre-production-review.md), [PR101 week 14](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w14-post-mortems-as-a-practice.md), [MMO407 week 12](../../MMO407-launch-scaling-and-post-mortems/lectures/w12-writing-a-post-mortem.md).

45. *Compute.* Did your team get better at planning? Show `r` and `q` for each sprint and the patch, and say what the two columns together show.

<details>
<summary>Marking guidance</summary>

`r = actual / estimate`, `q = delivered / committed`, and the model predicts `q ≈ 1 / r`. Emberfall's `r` fell from 1.50 to 1.21 while `q` rose from 61% to 86%, tracking `1 / r` within 6 points: real improvement in estimating. The patch had `r = 1.28` and `q = 100%`, so better commitment, not better estimation. A 5 does this with the team's rows and gives the sample-size caveat. A team with `r` flat at 1.4 and `q` rising to 100% got better at committing, not at estimating.

</details>

46. *Explain.* Name one unplanned item your team shipped. Why was it missing from the PR401 production plan, and what would the next plan do about it?

<details>
<summary>Marking guidance</summary>

Emberfall shipped 7 unplanned items, all operations tooling or live fixes, and none had a line in the PR401 plan. A 5 names the team's item, shows its hours from the log, and turns it into an action: budget operations tooling as a feature, sized from lab 11's interrupt hours. Answers that call it "scope creep" without the classification score 3.

</details>

47. *Compute.* What were your recurrence and closure rates against the PR401 pre-production review? Explain one category that came back even though its action item was closed.

<details>
<summary>Marking guidance</summary>

`R = |C1 ∩ C2| / |C1|`, closure = closed action items / all. Emberfall: 3 of 6 recurred (50%), 4 of 6 closed (67%); planning came back because the buffer fixed feature sprints but live work had its own ratio. A 5 does this with the team's categories coded the same way both times, and explains the recurring closed item with a mechanism. A category list coded differently in the two reviews scores at most 2.

</details>

48. *Critique.* Read one lesson from your post-mortem aloud. What grade (A, B or C) does its evidence earn, and what would have to be true for it to be wrong?

<details>
<summary>Marking guidance</summary>

Grade A needs a mechanism plus a contrast; B has one of them; C is one case with no comparison (MMO407 week 12). A 5 grades the lesson honestly, names the record it cites, and states a concrete observation that would falsify it. It checks the lesson for hindsight: was the evidence available when the decision was made? Defending a C lesson as a rule scores at most 2.

</details>

49. *Reflect.* Describe the decision in your individual reflection. What did you know at the time, from which dated record, and what does the evidence say now?

<details>
<summary>Marking guidance</summary>

A 5 separates what was known then from what is known now, cites the dated record (a commit, a lab sheet, a triage row), and ends in a change someone could check on the next project. It avoids "we should have known". Examiners ask one follow-up that moves the decision to a different week and check the student can reason about it. A narrative with no record scores at most 2.

</details>

50. *Critique.* Find one sentence in your team's post-mortem that could be read as blame. Rewrite it blamelessly and name the process gap it points to.

<details>
<summary>Marking guidance</summary>

Blameless writing asks what in the process let the problem go unseen (PR101 week 14). A 5 picks a real sentence, or if none exists picks the sentence closest to blame, rewrites it around the process (no review step, no alert, an unowned queue), and names the action item that closes the gap. Rewrites that only swap a name for "someone" score 2.

</details>

## K. Team, players and ethics

Links: [peer assessment brief](peer-assessment-brief.md), [PR101 week 11](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w11-communication-and-conflict-in-teams.md), [PR101 week 12](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w12-crunch-causes-costs-alternatives.md), [MMO308 week 10](../../MMO308-live-operations-analytics-and-experimentation/lectures/w10-player-feedback-loops-forums-surveys-polls.md).

51. *Explain.* How did your team make on-call work visible in its records, so that it counted in reviews and peer ratings?

<details>
<summary>Marking guidance</summary>

A 5 describes the time log tags (`ops`, or the five interrupt categories from week 11), the rota file, and how incident postmortems were attributed. It explains why a rating that counts closed feature tickets undervalues a live-ops role, as in the peer brief's worked example. Answers that say "everyone knew who did it" score at most 2.

</details>

52. *Reflect.* Your real players outlast the course. What did your team decide about the game after the showcase: keep it running, hand it over, or shut it down? How did you tell players?

<details>
<summary>Marking guidance</summary>

A 5 states the decision with its reason (hosting grant, team availability, player count), the date, what happens to player data, and the message players received with enough notice to act on it. It connects the decision to promises made at launch (the wipe policy, "no end date"). Examiners accept any of the three choices. They mark the reasoning and the honesty to players. "We haven't thought about it" scores at most 1.

</details>

53. *Critique.* Pick one piece of player feedback your team acted on and one it chose not to act on. Was the second decision explained to the players who raised it?

<details>
<summary>Marking guidance</summary>

A 5 names both items with their source (feedback channel, ticket, survey), the evidence the team weighed, and how the loop was closed in each case (a patch note, a reply where it was reported, a known-issues line). It explains why players who see their reports acted on keep reporting (MMO308 week 10). Answers that treat all feedback as equal votes score at most 2.

</details>
