# PR301 · Week 13 — Beta: Open Class Playtest

**Why this matters:** This week your world meets the number the course is built around. The outcome says "a persistent multiplayer world supporting 50+ concurrent test players", and the beta is where you show it with people, not bots. At the week 9 alpha most teams learned that the invitation model worked in shape and missed in size, because recruiting or the show rate fell short of the guess. Now you have measured rates instead of guesses, and they come from small samples. This week you set an invitation target that still works at the low end of what the alpha measured, re-run the load test with the social systems and the encounter switched on, and run the beta with the week 9 operations plan plus a peak-hour crew and a restart drill that proves the world persists.

**You will be able to:**
- Take the week 10 invitation count from measured alpha rates, and set an invitation target with a 90% modelled chance of 50 humans online at the event, including at the low end of the show rate's interval.
- Re-run the headroom load test with every system from sprints 4 and 5 active, and find capacity from a stepped test against both the week 6 rule and the week 2 headroom convention.
- Run a beta peak hour with named roles, a go/no-go list and a restart drill that includes a change made seconds before the save.
- Collect the evidence the stabilization sprint and the final post-mortem will need.

**Before class:** Bring your week 10 telemetry review with its measured show rate, event attendance and beta invitation count. Re-read [week 9](w09-alpha-first-persistent-weekend.md), sections 2 and 4 (20 minutes). Re-read MMO302 week 11, section 2 on finding the knee (15 minutes). Skim MMO407 week 3, sections 1 and 4 on what a beta can show and who you invite (15 minutes), and PR201 week 11, section 3 on the Wilson interval (10 minutes).

**Prerequisites from earlier courses:** [MMO302 week 11, load testing with bots](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) and [MMO302 week 14, observability](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md) (how to test and how to watch; this guide applies them). [MMO302 week 3, area of interest](../../MMO302-mmo-server-architecture/lectures/w03-area-of-interest-grids-radius-hysteresis.md). [MMO308 week 13, incident response](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md). [PR201 week 11, playtest and telemetry review](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w11-playtest-and-telemetry-review.md) (the Wilson interval and the unit of analysis). From this course, [week 2](w02-technical-architecture-review.md) (headroom of 2), [week 6](w06-sprint-2-review.md) (the p99 tick rule), [week 9](w09-alpha-first-persistent-weekend.md) (the invitation model and the operations plan), [week 12](w12-sprint-5-group-encounter.md) (the encounter instance count) and the [syllabus](../syllabus.md). Looking ahead, [MMO407 week 3, beta strategies](../../MMO407-launch-scaling-and-post-mortems/lectures/w03-beta-strategies.md) (year 4) covers beta tests in depth.

**Interactive:** [Beta turnout model](../examples/w13-beta-turnout.html). Use it in section 2 and when you set your invitation target.

---

## 1. What the beta has to show

The beta milestone checks one outcome with three parts. Read the beta milestone brief for the exact marking. This guide follows the rule week 9 set for the alpha: humans and bots are counted separately, and the concurrency claim is about humans.

- **Concurrency.** At least 50 human players online at once, shown by the server's own player-count metric with bots excluded, not by a screenshot of a busy market square.
- **Support.** While they are online, the tick holds the week 6 rule (on a 10 Hz server, mean tick at or under 60 ms and p99 at or under 80 ms), and disconnects stay rare. Your beta plan states the disconnect threshold.
- **Persistence.** The world survives a planned restart during the peak hour. Characters, inventories, guild rosters and the economy's ledger come back as they were. This is what makes it a persistent world rather than a lobby.

Everything else in the beta (the encounter, the economy, the social features) is being tested too, and week 14 will triage all of it. But the three points above decide the milestone. Plan for them first.

## 2. From measured rates to a plan

Week 9 built the invitation model from guesses. Week 10 put the alpha's measured rates back into it and got an invitation count for the beta:

```
online per invite = s × a,   where a = e + (1 − e) × L/P
I = 50 / (s × a)
```

`s` is the show rate, `e` the event attendance and `L/P` the share of players online in a normal evening hour, all from week 9. `a` is the share of players who are online at the event. This guide calls the beta's sign-ups **invitations**. `I` counts people who said yes to the invitation list, exactly as week 9 counted sign-ups.

That count is the right starting point, and it needs two corrections before it is a plan.

**The rates are small samples.** A show rate measured on 40 sign-ups has a Wilson interval about 28 points wide (PR201 week 11). Plan so that the target still holds near the low end of that interval, not only at its centre.

**The expected value is a coin flip.** Each invitation either ends with a person online at the event or it doesn't, so the number online is roughly binomial with `n = I` invitations and `p = s × a`. Setting `I = 50 / p` gives an expected 50, and about an even chance of reaching it. Plan for a 90% chance instead.

The levers are the ones week 9 named, now with numbers behind them. A stronger event raises `e`, and `a` with it. Reminders raise `s` a little. Recruiting beyond the class raises `I`. Only the first is cheap. CCP has long run mass tests of EVE Online on its Singularity test server and usually rewards participants on that server, often with millions of skill points per character. The reward exists to put testers online at the announced hour. Your version is a title, a cosmetic, or the showcase credits.

## 3. The load test, again

Week 2 set the course's headroom convention: load-test at twice the target, so 100 players. Week 6 set the tick rule at that crowd: mean tick at or under 60 ms (the 0.6 CPU budget) and p99 at or under 80 ms (the D3 trigger). The beta applies the same two numbers to the beta build, with no new rule. Your last full load test was probably in week 6 or 8. Since then you have added chat, parties, guilds and an encounter that runs in instances. Re-run it before the beta.

- **Test what the beta will do.** Bots must walk, fight, chat, form parties and run the encounter. Use the instance count from week 12: if 50 testers can form 12 parties, the bots run 12 instances.
- **Step and read the tail.** Run steps of 25 bots up to 100, holding each for ten minutes after warm-up, and record p99 from the per-tick log (week 6). The mean will look fine long after players feel stalls (MMO302 week 14).
- **Two checks.** At 100 bots, the mean must be at or under 60 ms. Capacity is the player count at which p99 crosses the 80 ms limit, interpolated between the two steps either side of it, and headroom is capacity over 50. Headroom must be at least 2, which is the same as p99 holding 80 ms at 100 bots. Capacity also tells you how far short you are when it doesn't.

If no step crosses 80 ms, capacity is "at least" the largest step. Never extrapolate past it. Response time turns a corner near saturation (MMO302 week 11), and a line through two good steps says nothing about where the corner is.

## 4. Running the peak hour

Keep the week 9 operations plan: runbook, dashboard, alarms, on-call rota and hotfix policy. It already covers the unattended hours. The peak hour adds four named roles and a drill.

- **Lead** (the incident commander in MMO308 week 13). Makes the go/no-go call, decides on restarts, rollbacks and kill switches, and is the only person who does.
- **Operator.** Watches the dashboard, runs the restart drill and takes any action the lead calls.
- **Comms.** Posts in the beta channel: doors open, event start, restart warning, incidents, close. Players forgive downtime they were told about.
- **Observers.** Everyone else plays, with a note sheet, as in the week 10 review.

The **restart drill** is planned for the peak hour, because an idle restart proves little. At a set time comms warns players, the operator saves and restarts the world server, and the team checks five named characters and one guild before and after. One of the checks must involve a change made a few seconds before the save, such as an item crafted or traded. If anything differs, it is an S1 bug and the first item in week 14.

The **go/no-go** check happens 30 minutes before the event. It is a list with yes or no answers, like the week 8 alpha list. Section 5 gives the *Saltmarsh* one.

## 5. Worked example: the *Saltmarsh* beta

### The hook

When ArenaNet scaled up Guild Wars 2's testing in March and April 2012, it opened its beta tests to anyone who had pre-purchased the game, after small closed tests in 2011 and a press beta in February. Opening the tests to buyers was a turnout decision as much as a marketing one: it gave the load tests a large population with a reason to log in on the announced weekends. The *Saltmarsh* team can't sell pre-purchases. It has an invitation list, a class rota and its alpha numbers, and it needs an invitation target that holds up.

### What the alpha measured

Week 10 recorded the *Saltmarsh* alpha against the week 9 plan:

```
signed up                    40
logged in at least once      26     s = 26 / 40 = 0.650   Wilson 95%: 49.5% to 77.9%
attended the event           17     e = 17 / 26 = 0.654   Wilson 95%: 46.2% to 80.6%
evening share                       L/P = 2.69 × 0.0472 × 2.1 = 0.267
event share                         a = e + (1 − e) × L/P = 0.746 (from the unrounded e)
online per invite                   p = 0.650 × 0.746 = 0.485
```

The model predicted `40 × 0.485 = 19.4` humans at the event, and the team saw 19, with 81 bots on top. Week 10 concluded that the beta needs `50 / 0.485 = 103.1`, so 104 invitations.

### The naive answer

104 invitations give an expected 50 humans at the event. With `p = 0.485`, the binomial chance of 50 or more is 57.3%. That is barely better than a coin flip.

### The 90% answer

For each case, the team finds the smallest `I` with at least a 90% binomial chance of 50 or more humans online at the event:

| Show rate `s` | Event attendance `e` | `a` | `p` | Invitations for 90% |
|---|---|---|---|---|
| 0.650 (alpha) | 0.654 (alpha) | 0.746 | 0.485 | 117 |
| 0.495 (low end of interval) | 0.654 (alpha) | 0.746 | 0.369 | 155 |
| 0.650 (alpha) | 0.75 (stronger event) | 0.817 | 0.531 | 106 |
| 0.495 (low end) | 0.75 (stronger event) | 0.817 | 0.404 | 141 |

Read it by rows. With the alpha's own rates, 90% needs 117 invitations, not 104. If the true show rate is as low as the interval allows, it needs 155. The low end is the unrounded Wilson bound, 0.4951. Forty sign-ups is a small sample, so that bound sits far below the measured 0.65.

The event is the lever. At the alpha, 9 of the 26 players who logged in never came to the event, and the ones who came had no reason to stay for the whole hour. For the beta, the class rota gives *Saltmarsh* a peak hour with no clash. The team opens the Drowned Warden only during that hour, with a title for every party that kills it, and sends reminders the day before and an hour before. The team assumes that lifts `e` to 0.75. That is an assumption, and it is written down as one.

With `e = 0.75`, 141 invitations give 90% even at the low end of the show rate. The team sets a target of 145, recruiting from its own class, PR201 and first-year volunteers through the course's shared sign-up, so that no student is invited to two worlds in the same hour. It checks the plan against each case:

```
I = 145, s = 0.650, e = 0.75:    P(≥ 50) > 99.9%
I = 145, s = 0.495, e = 0.75:    P(≥ 50) = 94.0%
I = 145, s = 0.650, e = 0.654:   P(≥ 50) > 99.9%
I = 145, s = 0.495, e = 0.654:   P(≥ 50) = 75.7%
```

Only the last row misses, and it needs both the show rate and the event to disappoint. The team writes a trigger: if fewer than 85 people have confirmed for the peak hour in the shared sign-up two days before, it asks the instructor to pair its hour with a neighbouring team's for a shared event, and reports whatever it gets honestly.

### The load test

Monday's stepped test ran on the beta build with 12 encounter instances from the 50-bot step up, chat and parties active. At 10 Hz the week 6 rule asks for a mean at or under 60 ms and a p99 at or under 80 ms at 100 bots.

| Bots | Mean tick (ms) | p99 tick (ms) |
|---|---|---|
| 25 | 11 | 24 |
| 50 | 22 | 43 |
| 75 | 38 | 71 |
| 100 | 58 | 138 |

At 100 bots the mean is 58 ms, inside the 60 ms limit. The p99 is 138 ms, and the 80 ms limit is crossed between 75 and 100:

```
capacity = 75 + (80 − 71) / (138 − 71) × 25 = 75 + 3.4 = 78.4 players
headroom = 78.4 / 50 = 1.57
```

The convention asks for 2. The team is short. Notice that a team that read only the mean would call this a pass. At 100 bots one tick in a hundred takes longer than a whole 100 ms tick, and players feel every one of them.

### The fix and the retest

The profiler shows most of the growth in entity updates, which scale with how many players each player can see. The area-of-interest radius is 60 m, set in sprint 1 when the world held five players. In the market square, where parties gather before the encounter and guild members meet, nearly everyone sees nearly everyone. The team cuts the radius to 45 m with hysteresis (MMO302 week 3) and reruns the upper steps: mean 20, 32 and 44 ms and p99 36, 58 and 76 ms at 50, 75 and 100 bots. No step crosses 80 ms, so capacity is at least 100 and headroom at least 2. The team does not claim more than 100, because it did not test more.

### The go/no-go list

Thirty minutes before the peak hour, the lead (Gus) reads it out:

1. Load test at 100 bots on the build being deployed: yes, mean 44 ms and p99 76 ms at 100.
2. Dashboard shows humans and bots separately, p99 tick, disconnects and errors, and the ledger residual: yes, checked by the operator (Chen).
3. Backup of the world database in the last hour, restore tested this week: yes.
4. Restart drill at 20:40; five check characters, one guild, and one craft made by Dee ten seconds before the save: yes.
5. Roles named: yes.
6. Invitations sent: 145. Confirmed for the hour: 96, above the trigger of 85. Reminders sent.
7. Open S1 bugs: none. Kill switches tested on this build (week 8): yes.

Go.

### What happened

At 20:17 the dashboard showed 57 humans online and 0 bots, the peak of the beta. The p99 tick that minute was 47 ms. The 20:40 restart took 3 minutes 10 seconds. The five check characters and the guild matched. Dee's craft, made ten seconds before the save, did not: the reagents were gone and the crafted item was missing. That is an S1 data-loss bug, and it is the first item on the week 14 list. The milestone evidence is the player-count export for the hour, the tick export, the restart check table and the bug report.

### What the example shows

The expected value of a turnout funnel is a coin flip. A target that works comes from the low end of a small-sample interval and from the lever that moves event attendance, not from the average. On the server side, the mean hid a failure the p99 showed, and the fix was an old sprint 1 setting that only mattered once the social systems gathered everyone in one square.

### Check this example

1. With the stronger event and the alpha show rate, what is the expected number of humans online for 145 invitations? The team saw 57. What does that suggest?
2. Why does the team say "at least 100" instead of extrapolating a capacity from the retest?
3. The drill passed for all five check characters but lost Dee's craft. What does that say about how check characters should be chosen?

<details>
<summary>Answers</summary>

1. `a = 0.75 + 0.25 × 0.267 = 0.817`, so `145 × 0.650 × 0.817 = 77.0`. Seeing 57 suggests that `s`, `e` or both came in below the planning values. Compute both from the beta logs in week 14. They are better inputs for the showcase and for next year's team than the alpha ones.
2. A straight line through steps below the knee says nothing about where the knee is (MMO302 week 11). Only a step whose p99 crosses the 80 ms limit measures capacity.
3. The check characters were idle during the save, so they could not show a race between a write in flight and the save. At least one check must make a change seconds before the save.

</details>

## Studio session plan

The week 13 studio meeting is the class-wide beta session. The instructor publishes a rota of peak hours so that no two teams hold their event at the same time and no tester is invited to two worlds in one slot. Worlds stay open for the whole beta weekend under the week 9 operations plan.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:20 | Instructor briefing; each lead confirms the team's slot, go/no-go time and restart drill time | Rota confirmed |
| 0:20-0:50 | Go/no-go checks by team (lab 13, part C), with the instructor visiting each lead | Signed go/no-go sheets |
| 0:50-1:50 | Peak slot 1: the first group of teams hosts; everyone else plays in the hosting worlds as testers and observers | Dashboards recorded, notes |
| 1:50-2:00 | Break | None |
| 2:00-2:50 | Peak slot 2: the second group hosts | Dashboards recorded, notes |
| 2:50-3:00 | Hosting teams export the hour's metrics and write first incident notes while they are fresh | Metric exports |

Teams whose peak hour falls in the weekend run the same go/no-go and roles then, and hand in the same evidence.

## Deliverables

Due at the start of the week 14 studio meeting, in the team repository under `production/week13/`.

1. **Beta plan** (lab 13) that passes `check_beta.py`: alpha rates with Wilson intervals, the invitation target and its cases, the load-test steps, capacity and headroom. Checked by rerunning the checker.
2. **Go/no-go sheet**, signed by the lead with the time. Checked against the run sheet.
3. **Peak evidence**: the server's player-count export (humans and bots separately) and p99 tick export for the peak hour, with the peak marked. Checked by reading the peak from the export.
4. **Restart drill record**: before-and-after values for the check characters, the guild and the late change, and the restart duration.
5. **Beta telemetry export** and observer notes, in the week 10 format, ready for week 14 triage.
6. **Turnout review**: invitations, logins and event peak, with `s` and `e` recomputed and compared with the plan.

## Common failure modes

- **Planning to the expected value.** It gives about an even chance of reaching 50. Plan to a 90% chance.
- **Trusting the centre of a small sample.** Use the low end of the show rate's interval and see whether the plan survives.
- **An event that clashes.** Two teams' events in one hour split the same testers. Use the rota.
- **Load-testing the week 6 build.** Chat, parties and 12 encounter instances were not there in week 6. Re-run on the beta build.
- **Reading the mean tick.** It stays under budget long after players feel stalls. Record p99 at every step.
- **Extrapolating capacity.** Capacity is where a measured step crosses the 80 ms p99 limit.
- **Counting bots as players.** The concurrency claim is about humans. Report both, separately.
- **Nobody owns the call.** Two people restart the server at once, or nobody does. Name the lead.
- **Restart drill with idle characters.** It can't find the race you are most likely to have.

## Review checklist

The instructor checks, at the week 14 meeting:

- [ ] Alpha `s` and `e` come from the server logs (as in the week 10 report), with Wilson intervals.
- [ ] The invitation target gives at least a 90% modelled chance at the low end of `s` under the planned event attendance, and any raised `e` is explained by a lever.
- [ ] The load test ran on the beta build with chat, parties and encounter instances, stepped to 100, with p99 at every step.
- [ ] At 100 bots the mean and p99 meet the week 6 rule (headroom at least 2), or the team fixed and retested.
- [ ] The go/no-go sheet was completed before the peak hour and names every role.
- [ ] The server's own metric shows at least 50 humans online at once, or the shortfall is reported with the turnout numbers.
- [ ] The restart drill includes a change made seconds before the save, with before-and-after values.
- [ ] Beta telemetry and observer notes are exported in the week 10 format.

## Sources

- Wikipedia, "Guild Wars 2" (read September 2026). Small closed alpha and beta tests in 2011; a press beta in February 2012; beta tests made available to anyone who pre-purchased, with their size increased significantly, in March and April 2012; pre-purchasers playing from 25 August and launch on 28 August 2012. https://en.wikipedia.org/wiki/Guild_Wars_2
- EVE University Wiki, "Singularity" (read September 2026, current EVE Online test server). Mass tests often conducted by CCP; participation usually rewarded for use on Singularity, often with millions of skill points per participating character. https://wiki.eveuniversity.org/Singularity
- Wilson, E. B. (1927). "Probable inference, the law of succession, and statistical inference." *Journal of the American Statistical Association* 22(158), 209-212. As taught in MA102 week 13 and applied in PR201 week 11.
- MMO302 weeks 3, 11 and 14, MMO407 week 3 and MMO308 week 13 (this program) for area of interest, load testing, tail latency, beta design and incident roles, with their sources.
- The *Saltmarsh* team's alpha and beta turnout, load-test results, peak and restart outcomes are a constructed teaching example, not data from any real team. The event attendance of 0.75 is an assumption for the example. The alpha figures are those of the week 10 example.

## Interactive spec

File: `examples/w13-beta-turnout.html`.

**The one insight.** An invitation target set to the expected value gives about a coin-flip chance of 50 humans at the event. Raising event attendance moves the whole distribution further right than the same effort spent on invitations, and the plan must survive the low end of the show rate's interval.

**What is plotted.**

- **Chart 1, humans online at the event.** Bars for the binomial probability mass `P(X = k)`, with `X ~ Binomial(I, s × a)` and `a = e + (1 − e) × LP`. Show only the range where the mass is above 0.0005. A vertical line at the target (default 50). Bars at or above the target in the accent colour, the rest neutral. Label "P(≥ 50) = xx.x%".
- **Chart 2, invitations needed.** x axis: event attendance `e` from 0.3 to 1.0. y axis: smallest `I` with `P(X ≥ target) ≥ goal`, clipped at 400 with an arrow. Two lines, one for the alpha `s` and one for the Wilson lower bound of `s`. A dot at the current `e` on each.

**Controls.**

- Alpha sign-ups `n` (default 40), alpha logins `k_s` (default 26), alpha event attendees `k_e` (default 17), evening share `LP` (default 0.267), all from the week 10 report. These set `s = k_s / n`, `e_alpha = k_e / k_s`, and the Wilson interval for `s`.
- Toggle "Use low end of show rate" (default off).
- Event attendance `e`: slider 0.3 to 1.0, step 0.01, default `e_alpha`, with a marker at `e_alpha` and a button "Stronger event (0.75)".
- Invitations `I`: slider 50 to 400, default 104. Button "Team's plan: 145 invitations".
- Target (default 50) and goal probability (default 0.90).
- Button "Load worked example".

**Formulas.**

```
Wilson (z = 1.96): center = (p + z²/(2n)) / (1 + z²/n)
                   half   = z × sqrt(p(1 − p)/n + z²/(4n²)) / (1 + z²/n)
a = e + (1 − e) × LP,   p = s × a
P(X ≥ T) = Σ_{k=T..I} C(I, k) p^k (1 − p)^(I − k)
I_needed = smallest I ≥ T with P(X ≥ T) ≥ goal (search upward from T)
```

Compute the binomial in log space (`lgamma` or a running product) so that `I = 400` does not overflow.

**Test values.** `s = 0.650` with Wilson 49.5% to 77.9% (low end 0.4951 unrounded); `e_alpha = 0.654` (Wilson 46.2% to 80.6%); `a = 0.746`; `p = 0.485`. At `I = 104`, `e = e_alpha`: `P(X ≥ 50) = 57.3%`. At `I = 145`: over 99.9% (alpha `s`, `e = 0.75`), 94.0% (low `s`, `e = 0.75`), over 99.9% (alpha `s`, alpha `e`), 75.7% (low `s`, alpha `e`). `I_needed` for 90%: 117 (alpha, alpha), 155 (low, alpha), 106 (alpha, 0.75), 141 (low, 0.75).

**Accessibility.** Probabilities and `I_needed` are printed in a number panel, not only drawn. The two lines in chart 2 differ by dash pattern as well as colour. Charts stack vertically below 700 px.
