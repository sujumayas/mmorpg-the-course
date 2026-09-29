# PR301 · Viva and reflection bank

**Used by:** the week 15 viva in the [post-mortem brief](post-mortem-brief.md). Each student answers four questions: two about systems they owned, one about a system a teammate owned, and one from the reflection section. The examiners pick questions that fit the team's world and the student's role.
**How to read the guidance:** every question is about the student's own persistent-world prototype. The marking guidance says what a full answer contains and what separates a strong answer from a weak one. Where it quotes numbers, they are the *Saltmarsh* figures from the session guides, given so examiners can calibrate. A student answers with their own team's numbers, not these.
**Marking each question:** 0 to 10. Eight or more needs the team's own numbers, the model behind them and one trade-off or failure. Five needs a correct account of the concept with the team's world named. Below five means the student cannot connect the concept to what they built.

Linked lectures: [MMO302](../../MMO302-mmo-server-architecture/lectures/w01-scale-targets-ccu-messages-and-n-squared.md) for server architecture, [DB201](../../DB201-data-persistence-and-telemetry/lectures/w05-transactions-and-acid.md) for persistence and telemetry, [MMO304](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md) for economies, [MMO308](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md) for live operations, [MMO309](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w04-duplication-exploits-and-transactional-design.md) for exploits, and [PR201](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w01-pitch-and-team-formation.md) for the studio method.

## Pitch, scope and planning

1. Your pitch passed the week 1 budget at some load. Walk us through the numbers: supply, platform, systems, authored content and replay factor. Which estimate turned out furthest from reality?

<details><summary>Marking guidance</summary>

A full answer states supply from `n × (1 − b) × (H − c(n − 1)) × W`, the three demand terms and the load, and says what change got the pitch under 0.9 (for *Saltmarsh*, crafting cut to two tiers, `F` 200 to 160, load 0.99 to 0.88). The strong answer names the worst estimate with evidence from the sprint records, for example `k` or `r`, and says how the error showed up. A weak answer recites the formula without the team's numbers or cannot say which estimate was wrong.

</details>

2. What replay factor did you assume, and what did the alpha weekend tell you about it?

<details><summary>Marking guidance</summary>

The student gives the assumed `r` and the loop sentence behind it (week 1 required a loop connecting two systems for any `r` above 3). A full answer compares it with weekend evidence: repeat visits to camps or gathering routes, sessions per player, hours per player. It also says what the difference means for load (at *Saltmarsh*, `r` from 4 to 3 pushes the load from 0.88 to 0.94). Credit honesty that `r` was hard to measure, if the student says what they would log to measure it next time.

</details>

3. Pick one of your three pillars. Name a feature it ruled out, and say whether ruling it out was right by the end of the course.

<details><summary>Marking guidance</summary>

A full answer quotes the pillar, the feature it killed and who wanted it, and judges the decision with evidence from play (telemetry, observer notes) rather than taste. Strong answers admit a pillar that did no work, or one the team quietly broke. Weak answers name a pillar that rules out nothing, such as "fun combat".

</details>

4. Your sprint 1 plan fitted the team's total hours. Did it fit every person? Show how you checked.

<details><summary>Marking guidance</summary>

Expect the week 3 per-person load: `capacity_i = f × (H_i − c(n − 1)) × w`, charges with the cross-discipline factor, and `load_i` for each owner. The student should know the team-total trap (*Saltmarsh* was 1.12 overall but Ben was at 2.36) and name which of the four moves the team used (narrow the goal, move work at a price, stub, mob the contract). Full marks need the drop order and whether it was used.

</details>

5. How did your focus factor change across sprints 1 to 3, and how did you use it to plan the one-week sprints?

<details><summary>Marking guidance</summary>

A full answer gives the measured values (for *Saltmarsh*, 0.46 and 0.54), explains the definition (estimated hours of done stories over hours actually available) and says why the first server sprint is low (integration). For sprints 4 and 5, the student should describe converting to weekly velocity and committing at the low end minus the bug reserve (week 11). Deduct if the student averaged the values or counted stories that finished after the review build was tagged.

</details>

6. Which feature did you rescope rather than cut, and what did the smaller version leave out?

<details><summary>Marking guidance</summary>

Expect a concrete rescope such as the week 11 "guild lite" (roster, invite and guild chat, no ranks) with the reason, the estimate made from scratch and what was left out. A strong answer says whether players missed the part that was left out, citing beta notes. A weak answer describes a cut as a rescope or subtracts estimates.

</details>

7. Show your day-3 burn-down for the encounter sprint. What did the two projections say, and what did you cut?

<details><summary>Marking guidance</summary>

The student computes `r_avg = (commit + added − remaining) / days` and `r_recent` over the last two days, uses the slower projection and cuts at least that much from items marked non-minimum at planning. *Saltmarsh* projected 6 hours left and cut 6.5 (phase 2 adds, need/greed UI, death VFX). Full marks need a comparison of the day-3 projection with the day-5 result. Deduct for projecting from the best day.

</details>

## Architecture and capacity

8. At what crowd size does your server run out of CPU budget, and how did you find that number?

<details><summary>Marking guidance</summary>

Expect the week 2 model, `deliveries = u × N × (N − 1) + m × u_m × N`, `cpu = deliveries × e`, solved for `cpu = 0.6` to give `N_max` (111 for *Saltmarsh* at `e = 8` µs). The student must say where `e` came from (a spike on the alpha host) and compare `N_max` with the 100-bot load test. Strong answers also compare the week 6 measured player cost with the week 2 prediction (38.0 ms against 39.6 ms).

</details>

9. Why does doubling the players more than double the server's delivery work? Use your own world.

<details><summary>Marking guidance</summary>

The player-to-player term grows with `N²`, so doubling `N` roughly quadruples it, while the mob term grows only with `N`. At *Saltmarsh*, 50 to 100 players multiplied deliveries by 3.37 (player part by 4.04, mob part by 2). A full answer connects this to the worst crowd (the market square or the encounter) and to [MMO302 week 1](../../MMO302-mmo-server-architecture/lectures/w01-scale-targets-ccu-messages-and-n-squared.md).

</details>

10. Name one piece of machinery your architecture review cut or deferred, and say whether you ever needed it.

<details><summary>Marking guidance</summary>

Expect a named component (zone servers and handoff, a cache, area of interest), the number that justified cutting it, and the revisit trigger written in the decision record. A strong answer says whether the trigger fired and what the team did. At *Saltmarsh* the deferred grid became a sprint 3 story when the week 6 trigger fired. [MMO302 week 4](../../MMO302-mmo-server-architecture/lectures/w04-zone-servers-and-handoff.md) is where handoff's duplication risk comes from.

</details>

11. Your week 6 tick model had terms for players, mobs and their product. Where did the product term come from in your code, and what did you do about it?

<details><summary>Marking guidance</summary>

The student explains `t = a + g + c·M + d·P·M`, how four runs in a 2 × 2 design fix the coefficients, and that `d` comes from idle mobs checking every player to decide whether to wake. A full answer gives `M_max` and the option chosen (grid wake checks, content cut or zones) with its fallback. Deduct if the student cannot say why run D is needed.

</details>

12. Why does the course hold you to p99 tick time rather than the mean? Give an example from your own logs.

<details><summary>Marking guidance</summary>

A mean inside budget can hide stalls that players feel as rubber-banding. At 10 Hz, one tick in a hundred over budget is a stall every ten seconds. The *Saltmarsh* beta load test had a mean of 58 ms at 100 bots (inside the 60 ms limit) and a p99 of 138 ms, against the week 6 limit of 80 ms. Full marks need a real example from the team's per-tick log and the limit it was checked against. Strong answers mention [MMO302 week 14](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md).

</details>

13. How did you find your server's capacity in the beta load test, and why did you not extrapolate past your last step?

<details><summary>Marking guidance</summary>

Expect stepped loads (25, 50, 75, 100 bots), ten minutes per step after warm-up, and capacity interpolated between the two steps either side of the point where p99 crosses the 80 ms limit (*Saltmarsh*: 78.4 players before the fix, headroom 1.57). The student should explain that response time turns a corner near saturation ([MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md)), so a line through good steps says nothing about where the corner is. Full marks need the team's own capacity and headroom, and the fix if headroom was below 2.

</details>

14. How much of your tick budget does the group encounter cost at beta load, and how did you decide between an instance and an open-world boss?

<details><summary>Marking guidance</summary>

A full answer gives the cost per copy and the maximum simultaneous copies (for example 12 parties of four from 50 testers) and adds them to the load test. It explains the trade-off from [MMO302 week 2](../../MMO302-mmo-server-architecture/lectures/w02-shards-realms-zones-instances-layers.md): instances give clean ownership and reset but multiply simulation cost, and open-world bosses need tagging rules. Deduct for an encounter that was never load-tested with its copies.

</details>

## Persistence and transactions

15. Take one line of your persistence promise marked "None" for acceptable loss. What strategy delivers it, and where is the transaction boundary?

<details><summary>Marking guidance</summary>

Expect write-through with a named boundary, for example "one transaction per trade, loot or craft", and the rows it changes. The student should say why position was allowed a periodic save (1,000 commits a second at 100 players if written through). Full marks need the source of truth named. Links: [MMO302 week 7](../../MMO302-mmo-server-architecture/lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md), [DB201 week 5](../../DB201-data-persistence-and-telemetry/lectures/w05-transactions-and-acid.md).

</details>

16. A player crafts one net from three reeds. List every row that changes, and say what happens if the server dies halfway.

<details><summary>Marking guidance</summary>

Three reeds removed, one net added, the crafting fee deducted with its ledger event, all in one transaction. If the server dies before commit, nothing happened. If the changes were split, a crash could destroy the reeds without the net or create the net without spending the reeds. A strong answer adds the week 13 restart-drill finding at *Saltmarsh*: a craft made seconds before a save was lost, which means the craft was not in its own transaction.

</details>

17. Explain how a mail dupe can occur when sending is saved periodically and collecting is written through. Did your world have one?

<details><summary>Marking guidance</summary>

The sender's balance changes in memory; the receiver collects and is saved at once; the server crashes; the sender is restored from the last periodic save from before the send. The ledger is right and the saved balances are not. The fix is both sides of every transfer in one transaction. Full marks need the student to say whether their world was exposed, how they checked, and the class-of-bug fix. [DB201 week 6](../../DB201-data-persistence-and-telemetry/lectures/w06-race-conditions-and-the-duplication-bug.md) and [MMO309 week 4](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w04-duplication-exploits-and-transactional-design.md) are the references.

</details>

18. Which of your social features persist across a restart and which do not? Why?

<details><summary>Marking guidance</summary>

Parties are in memory and dissolve on restart. Guilds and friends persist, and losing them is a data-loss bug. Chat history is not in the character database. Party loot uses the transactional item path. A full answer explains the reasoning (players regroup easily; a vanished guild is lost progress) and how the team tested guild survival across a restart.

</details>

19. Describe your restart drill at the beta. What made it a good test, or a weak one?

<details><summary>Marking guidance</summary>

A strong drill runs during peak load and checks named characters, a guild and at least one change made seconds before the save, before and after. Idle check characters cannot reveal a race between a write in flight and the save. Full marks need the team's actual result and what was filed. At *Saltmarsh* the late craft was lost and filed as S1.

</details>

20. How long did your restore from backup take, and what does that number mean for your world?

<details><summary>Marking guidance</summary>

The student gives the measured restore time from the week 9 drill and the week 14 candidate restore, and relates it to recovery time and recovery point from [DB201 week 14](../../DB201-data-persistence-and-telemetry/lectures/w14-backups-and-disaster-recovery.md). A full answer says what a player would lose if the database failed at the worst moment, given the backup schedule. Deduct for a backup that was never restored.

</details>

## Soak testing and evidence

21. What failure rate did your login path have to beat, and how many clean attempts did you need to show it?

<details><summary>Marking guidance</summary>

Expect `p* = k / E` from the alpha exposure (at *Saltmarsh*, 2 failures tolerated over 200 logins, so 1%) and `n = ⌈2.996 / p*⌉` (300). The student should explain the rule of three and why 50 clean logins only bounds the rate below 6%. Full marks need the threshold set before the soak ran.

</details>

22. Why did your soak test keep cycled, burst and one-shot conditions separate?

<details><summary>Marking guidance</summary>

Failures are not independent. Concurrency bugs such as the week 4 session race appear only under overlap, so a large clean total from an easy condition hides a failing hard one. A full answer names the bug each condition was designed to trigger and says which condition found the team's real failure, if any.

</details>

23. After a soak run with a few failures, how did you decide whether the story was done?

<details><summary>Marking guidance</summary>

The Wilson upper bound at 95% compared with the threshold (at *Saltmarsh*, 2 in 400 gives 1.80% against 1%, not done). The student should show the calculation roughly and explain why the point estimate of 0.5% is not enough. Credit an answer that mentions finding the cause from the failures' timing.

</details>

24. Fifteen clean pulls of your boss with no deaths to its mechanic. What can you claim?

<details><summary>Marking guidance</summary>

About `3 / 15 = 20%` as a 95% upper bound on the per-pull failure rate, and the pulls were by people who know the fight. A full answer says the beta was the real test and reports what beta telemetry showed about deaths by ability.

</details>

## Combat, mobs and the camp faucet

25. At the alpha's busiest hour, what was the utilization of your busiest mob camp, and how did your respawn rule keep it in range?

<details><summary>Marking guidance</summary>

Expect `k = 60 / (TTK + t)`, `λ = P × k`, `μ = M × 60 / T`, `ρ = λ / μ` with the team's numbers, and the 0.8 target. A full answer explains why a fixed timer tuned with three players starves ten (the Reedbank camp went from 0.75 to 2.5) and what the dynamic rule `T(P) = clamp(M × 60 × 0.8 / λ, T_min, T_max)` does. Strong answers mention the floor and what happens beyond it.

</details>

26. How does your respawn rule change the money entering your economy?

<details><summary>Marking guidance</summary>

With a fixed timer, total camp output is capped, so income per player falls as crowds grow. With a dynamic timer the faucet scales with player-hours. The student should connect this to [MMO304 week 3](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md) and state their world's loot faucet per player-hour. Full marks need a comment on whether that choice matched the pillars.

</details>

27. What was your kill credit rule, and what did it do to how strangers behaved at camps?

<details><summary>Marking guidance</summary>

First-hit credit makes players race to tag mobs; shared credit lets strangers help each other and lowers demand per player. A full answer names the rule, whether it was chosen or happened by accident, and evidence from observer notes or telemetry. Link to MMO305 week 3 on voluntary grouping is a bonus.

</details>

28. Which parts of combat does your server decide, and how would a modified client try to cheat each one?

<details><summary>Marking guidance</summary>

The client sends intent, and the server resolves range, cooldown, damage, death and loot. A full answer names two attacks (range or cooldown spoofing, forged loot pickup) and the server check that stops each. [MMO302 week 6](../../MMO302-mmo-server-architecture/lectures/w06-simulation-authority-and-anti-cheat-by-design.md) and [MMO309 week 2](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w02-never-trust-the-client.md) are the references. Deduct for any client-decided outcome the student cannot justify.

</details>

## Economy and the ledger

29. State your world's net income per player-hour as planned, and how many hours a player needed for the first real purchase.

<details><summary>Marking guidance</summary>

Expect the faucet and sink lines with reason codes, `n = Σ f − Σ s`, the sink ratio and `h_G = G / n`, and the single-line change that moved `h_G` into the target band (*Saltmarsh*: 155 to 107 by cutting the wolf drop from 5 to 4 copper, giving 5.6 hours to a 600-copper charter). A strong answer explains who pays for each option, as week 7 did for repairs against loot.

</details>

30. Write the ledger equation for your world and explain what a non-zero residual means.

<details><summary>Marking guidance</summary>

`M_end − M_start = Σ faucets − Σ sinks`, with `M` over every place currency lives (balances, mail, escrow, guild banks). A non-zero residual means something changed a balance without going through the logging function or saved one side of a transfer. A full answer lists every place currency lived in the team's world and how the money-supply query covered it.

</details>

31. Your alpha residual was not zero, or was it? Decompose it the way you did in week 10.

<details><summary>Marking guidance</summary>

Expect decomposition by time (drift against steps, steps matched to crashes or patches) and by character (a few characters point to a dupe, all characters point to an unlogged faucet), with each cause predicting its own size. The *Saltmarsh* standard was 620 starter copper, 7,500 mail dupe and 57 rounding, summing to 8,177. A team with a zero residual should explain how it made sure the zero was real (per-character check, not a total that nets a leak against a dupe).

</details>

32. Did any crafting recipe in your world act as a hidden faucet? How would you find one?

<details><summary>Marking guidance</summary>

The arbitrage inequality `vendor_sell(output) > fee + Σ vendor_sell(inputs)`, where gathered inputs count at their sell value, often zero. The *Saltmarsh* reed mat made 8 copper from nothing, 430 times. A full answer says whether the team's check ran in the build pipeline, and how the vendor and crafting-fee lines moving together in telemetry reveal a leak. [MMO304 week 7](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w07-crafting-chains-and-gathering-professions.md) is the reference.

</details>

33. When you found duplicated currency, did you correct balances or roll back? Defend the choice.

<details><summary>Marking guidance</summary>

With a trustworthy ledger, a targeted correction removes exactly the duplicated amount and nobody else loses play. Without one, a rollback is the only safe tool. Corrections should be logged as a sink (for example `S_GM_CORRECTION`). The player response follows the policy published before the weekend. Full marks need the student to separate the economic fix from the decision about the players. [MMO309 week 11](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w11-exploit-response-rollback-vs-ban.md) is the reference.

</details>

34. Which budget line was furthest from your plan after the alpha, and what did you change because of it?

<details><summary>Marking guidance</summary>

Expect the actual-to-budget ratio for the line, the cause, and the update. A strong answer treats a miss as a measurement replacing a guess (the *Saltmarsh* market cut came in at 0.59 because players traded less than guessed) and does not "fix" players. Deduct if the student changed several lines at once and cannot say which change did what.

</details>

## Operations and the alpha weekend

35. Walk us through your on-call rota and one incident from the alpha weekend, from alarm to resolution.

<details><summary>Marking guidance</summary>

A full answer gives the rota rules (every hour covered with a backup, no stretch over six hours, swaps in the rota file), then an incident with times from the log: alarm, acknowledgment, first action from the runbook, kill switch or hotfix, second reader, and close. Link to [MMO308 week 13](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md). Strong answers say what the log helped them reconstruct afterwards.

</details>

36. Which of your alarms fired during the weekend, and was any of them muted? What does that teach?

<details><summary>Marking guidance</summary>

The student names the alarms (health check, p99 tick, hourly ledger residual, per-character copper jump) and what fired. The lesson from the week 10 guide: an alarm that fires on a known, harmless cause gets muted and then misses the real one, so remove the cause and keep the alarm. Full marks need the team's own example or a clear account of how they avoided it.

</details>

37. Which systems in your world had kill switches, and did you ever use one?

<details><summary>Marking guidance</summary>

Expect every value-moving system (trade, market, mail attachments, crafting) with a runtime flag, an owner and a test with clients connected, both ways. A full answer explains why a switch is better than shipping with an open S1 (the New World and Old School RuneScape cases in week 8) and describes any real flip. Deduct for switches that needed a restart.

</details>

38. How many sign-ups did you plan for the alpha, and why was concurrency so much lower than headcount?

<details><summary>Marking guidance</summary>

Expect `P = I × s`, sessions `S = P × k`, Little's law `L = λW` for the evening crowd and `C_event = e × P + (1 − e) × L`. Each player is online for a small part of a 48-hour weekend (3.75 hours at *Saltmarsh*), so headcount is about six times concurrency. A full answer says which rate moved the answer most (show rate) and which lever the team used (a scheduled event).

</details>

39. What did your consent notice tell testers, and what did you delete, and when?

<details><summary>Marking guidance</summary>

Data collected, purpose, who can see it, and the deletion date, shown before first login. Character IDs, not names, in bug reports. A full answer says whether the deletion happened on the date, and names one piece of data the team decided not to collect. [DB201 week 13](../../DB201-data-persistence-and-telemetry/lectures/w13-privacy-gdpr-and-data-retention.md) is the reference.

</details>

## Telemetry and the beta

40. Before you drew any chart from the weekend data, what checks did you run, and what did they find?

<details><summary>Marking guidance</summary>

Sequence gaps (expected around crashes, a pipeline problem elsewhere), sessions without logouts closed at crash time, and bots filtered out and counted against the bot plan. A full answer gives the team's numbers and says what the checks meant for trust in later figures. [DB201 week 11](../../DB201-data-persistence-and-telemetry/lectures/w11-pipelines-collect-store-query.md) covers where events get lost.

</details>

41. How did you set your beta invitation target, and why was the expected-value answer not enough?

<details><summary>Marking guidance</summary>

Setting `I = 50 / (s × a)` gives about an even chance of 50. The number online is roughly binomial, so the team finds the smallest `I` with a 90% chance, and checks it at the low end of the show rate's Wilson interval. A full answer names the lever used to raise event attendance and whether it worked, from the beta turnout review.

</details>

42. How many humans were online at your peak, and how do you know that number excludes bots?

<details><summary>Marking guidance</summary>

The number from the server's own metric with humans and bots in separate columns, the minute of the peak, and how bots were marked in telemetry. A shortfall answered honestly with recomputed `s` and `e` earns more than an inflated claim. Deduct heavily for a screenshot or a mixed count.

</details>

43. Your return rate from alpha to a second day came from a small sample. How did you report it, and why not compare it with a shipped game?

<details><summary>Marking guidance</summary>

A Wilson 95% interval (*Saltmarsh*: 17 of 26, 46% to 81%). Testers were recruited friends on a free weekend, so the population is nothing like a shipped game's players. A full answer says what the figure is good for (a baseline for the beta). Link to [MMO308 week 3](../../MMO308-live-operations-analytics-and-experimentation/lectures/w03-cohorts-and-retention-curves.md).

</details>

## Stabilization and release

44. How did you decide which beta bugs had to be fixed before the showcase, and how much work was that?

<details><summary>Marking guidance</summary>

The week 8 persistent-world scale, frequency from telemetry for every S2 and S3, and the week 14 budget: must-fix work from tracker fix times, expected arrivals from internal testing, divided by `1 − q` for reopens, against capacity after release work is reserved. A full answer gives the team's demand, capacity and margin. Deduct for estimates made in the meeting.

</details>

45. Did you switch any system off or reclassify any bug for the showcase? What were you not allowed to do?

<details><summary>Marking guidance</summary>

A switch-off uses a week 8 kill switch already tested, leaves the world meeting the brief, is noted in the showcase notes, and keeps the bug open on main. Reclassification needs telemetry and is never allowed for S1, data loss or crashes. A strong answer explains why closing a bug as "disabled" is wrong: anyone who turns the system back on reintroduces the exploit.

</details>

46. What did your two-hour soak on the release candidate show that a ten-minute test would not?

<details><summary>Marking guidance</summary>

Slow growth in memory or p99 tick (leaks, growing caches, log files), and periodic work such as saves meeting load. A full answer shows the team's memory and p99 curves and says whether any growth was filed. Credit a connection to the alpha's "time" failures in week 9, section 1.

</details>

## Reflection

47. Which number you computed during the course changed a decision most? What would have happened without it?

<details><summary>Marking guidance</summary>

A specific number, the calculation, the decision and the counterfactual, for example the per-person load that moved the bot client to the designer, or the day-3 projection that cut phase 2. Strong answers say whether the decision held up. Weak answers name a number with no decision attached.

</details>

48. Name a prediction your team made that the world proved wrong. What was wrong with the model or its inputs?

<details><summary>Marking guidance</summary>

The student distinguishes a bad model (for example assuming independent failures) from a bad input (a guessed show rate, a borrowed focus factor), with evidence. Full marks need a change the student would make to the model or to how the input is measured.

</details>

49. Describe a moment when the team disagreed about a technical or scope decision. How was it settled, and was the process fair?

<details><summary>Marking guidance</summary>

A specific disagreement, the evidence each side used, the decision rule (product owner, decision record, pull request review) and the outcome. Strong answers judge the process separately from the outcome, and link to [PR101 week 11](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w11-communication-and-conflict-in-teams.md). Deduct for blame without evidence.

</details>

50. Explain a system a teammate built that you did not work on: what it does, what it costs the server and how it failed or held.

<details><summary>Marking guidance</summary>

Used as the teammate-system question. A full answer covers purpose, the data it reads and writes, its cost (tick, bandwidth or commits) and one real failure or test result. Five points for purpose and data alone. Below five if the student cannot say what the system stores.

</details>

51. Your on-call shifts: what did you learn about running a live world that you could not have learned from building one?

<details><summary>Marking guidance</summary>

Expect a concrete observation from the student's own shifts (an alarm at 3 am, a runbook step that did not work for a non-author, a quiet shift that still needed a log entry) and the practice it changed. Strong answers connect it to a PR401 plan. Weak answers are general statements about teamwork.

</details>

52. If your team started PR401 with this world tomorrow, what would you fix first, and why that before anything else?

<details><summary>Marking guidance</summary>

A ranked choice backed by evidence: an open S1 on main (such as a dupe behind a switch), a persistence gap, a capacity limit, or a process failure. Full marks need the reason it outranks the alternatives, in the same terms the course used (value created or destroyed, data lost, players affected).

</details>

53. What practice from this course will you keep, and how will you know it worked next time?

<details><summary>Marking guidance</summary>

A named practice (thresholds set before tests, per-person load checks, reason codes on every balance change, rota swaps in the file) and a measurable check (fewer reopened fixes, residual zero every hour, no one above load 1). Weak answers name a virtue ("communicate more") with no check.

</details>
