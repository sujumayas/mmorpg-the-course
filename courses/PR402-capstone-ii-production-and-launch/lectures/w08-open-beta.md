# PR402 · Week 08 — Open Beta

**Why this matters:** This weekend, anyone with the link can play your game. It is the last time you can learn something about your build before launch without paying launch prices for it. An open beta that is too small finds nothing your closed beta did not. One that is bigger than your server can hold becomes a login queue with a Discord channel attached. This week you size the beta from two numbers you can compute, the play you need to see rare bugs and the players your server can hold, and then you run it.

**You will be able to:**
- Compute the player-hours an open beta needs to catch bugs above a chosen rate, and the sign-ups that produce them.
- Turn sign-ups into a peak concurrency forecast and compare it with the safe capacity from your sprint 4 load test.
- Choose a lever (cap, waves, a second shard, fewer invites) when the forecast and the capacity disagree.
- Run the beta weekend with a rota, kill switches, a bug intake path and the targeted tests from week 6.
- Write open-beta exit criteria that feed next week's launch go or no-go.

**Before class:** Bring the sprint 4 load-test report with the latency knee (the concurrency where tick time starts climbing steeply), your closed-beta show-up rate (testers who played at least once divided by testers invited) and hours played per active tester, the open-beta test list from week 6, and your sign-up count so far. Re-read [MMO407 week 3](../../MMO407-launch-scaling-and-post-mortems/lectures/w03-beta-strategies.md), sections 2 and 4 (25 minutes), and skim [MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md), section 2, on finding the knee (10 minutes).

**Prerequisites from earlier courses:** [MMO407 week 3, beta strategies](../../MMO407-launch-scaling-and-post-mortems/lectures/w03-beta-strategies.md) (exposure and the rule of three, applied here without re-deriving). [MMO302 week 1, scale targets and CCU](../../MMO302-mmo-server-architecture/lectures/w01-scale-targets-ccu-messages-and-n-squared.md). [MMO302 week 11, load testing with bots](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md). [MMO302 week 13, cloud deployment and autoscaling](../../MMO302-mmo-server-architecture/lectures/w13-cloud-deployment-and-autoscaling.md) (headroom). [MMO308 week 4, funnels and churn](../../MMO308-live-operations-analytics-and-experimentation/lectures/w04-funnels-and-churn.md). [MMO305 week 12, community management](../../MMO305-social-systems-and-online-behaviour/lectures/w12-community-management.md). [MMO309 week 9, account security and takeovers](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w09-account-security-and-takeovers.md). From this course, the [week 6 guide](w06-telemetry-and-balance-review.md) (targeted tests) and [week 7 guide](w07-production-sprint-4.md) (readiness checklist).

**Interactive:** reuse MMO407's [beta exposure model](../../MMO407-launch-scaling-and-post-mortems/examples/w03-beta-exposure.html) with your own numbers.

---

## 1. What an open beta is for

Your closed beta answered "does the game work for people who are not us?" The open beta answers four different questions, and you should know which ones you are asking before you invite anyone.

1. **Rare bugs.** Bugs that fire once in hundreds of player-hours. Your closed beta did not produce enough play to see them.
2. **Strangers' first hour.** Closed-beta testers were friends, classmates and people who replied to a recruiting post. Open-beta players found a link and have no reason to be patient. Their tutorial funnel is the one launch will look like.
3. **Load and operations.** Sign-up spikes, login storms at the start of the weekend, and your team's ability to run a live server for 72 hours.
4. **The targeted tests.** The week 6 "can't decide" rows need more players than the closed beta had. The open beta is where they get them.

An open beta is not a launch. Keep that visible: label the build, tell players that progress will be wiped (or that it will not, and then keep that promise), and state the dates. MMO407 week 3 argued that the last beta before launch behaves like a launch whether you call it one or not; press coverage and first reviews often start here.

## 2. How much play you need

MMO407 week 3 gave the model. A bug that fires at rate `r` per player-hour has a chance `1 − e^(−r × E)` of appearing at least once in `E` player-hours. To see it with 95% probability, you need:

```
E ≥ 3 / r
```

Pick the rate by asking which bugs you cannot afford to meet first at launch. For a small MMO, a reasonable choice is "any bug that fires once per 400 player-hours or more often", because at launch you expect to run a few thousand player-hours in the first week, which would turn a once-per-400 bug into a dozen public incidents. The choice is a team decision. Write it down with the reason.

Then turn exposure into sign-ups with the rates your closed beta measured:

```
E = sign-ups × show-up rate × hours per active player
```

Show-up rate for an open beta is usually lower than for a closed one, since sign-up costs a stranger nothing. If you have no better number, use your closed-beta rate and treat the result as an upper bound.

## 3. How many players at once

Exposure tells you total play. Your server cares about play at the same moment. Convert in three steps.

1. **Busiest day.** What share of the weekend's play falls on the busiest day? For a Friday-to-Sunday beta, Saturday typically carries the largest share. Use your closed-beta daily split if you have it.
2. **Busiest hour.** What share of that day's play falls in its busiest hour? Your closed-beta session logs give this directly. Player-hours in one hour equal the average concurrency in that hour.
3. **Spike.** The first hour after the doors open, and the hour after any announcement, run above the daily pattern. Multiply by a spike factor. With no data, 1.5 is a common starting point; your load test should already have tested at that level (week 7, item I).

[Week 3](w03-production-sprint-3-feature-complete-and-server-budget.md) estimated launch peak from DAU, session hours and a peak ratio, to size the fleet and its bill. For a beta weekend you already know the exposure you want, so work from it directly. Both routes should land within a few players of each other; if they do not, find out which input is wrong before the weekend.

Compare the result with **safe capacity**, which is the knee from your load test minus headroom. MMO302 week 13 explained why headroom must cover the time it takes you to react. For a student team whose reaction is "someone notices, wakes a teammate, and restarts with a bigger instance", 30% headroom is a reasonable default.

```
safe capacity = knee × (1 − headroom)
```

This is week 3's `knee × u` with `u = 0.7`.

## 4. Running the weekend

The beta weekend is a rehearsal for launch week. Run it the way you intend to run launch.

- **Rota.** Named people on call in blocks of at most four hours, a primary and a backup, written in the team calendar. Nobody is on call for the whole weekend. PR101 week 12 covered what fatigue does to the quality of decisions.
- **Severity table and roles.** Adopt MMO308 week 13's severity table as written, with your team's names in the roles, and give tracker bugs their level with the mapping in [week 4](w04-alpha-review-and-bug-triage.md), section 2. Decide in advance who may restart the server and who posts status updates.
- **Kill switches.** Trading, the market stalls, new sign-ups, and any system added in sprint 4 should each have a switch that the on-call person can flip without a deploy. Test each switch once before the doors open.
- **Waves.** Instead of opening to every sign-up at once, send invitations in waves (for example a third on Friday evening, a third on Saturday morning, the rest on Saturday afternoon). Waves turn one spike into three smaller ones and let you stop if the first wave breaks something.
- **Bug intake.** One path: the in-client report button from sprint 4, which attaches build number, position and last 60 seconds of logs. Discord reports are welcome, but someone copies them into the tracker within the shift.
- **Community.** A code of conduct, a moderator on every shift, and a pinned post with known issues. MMO305 week 12 covers moderation; MMO309 week 9 covers the basics of account security, which matter from the moment strangers have accounts.

## 5. What to measure

Collect the data you will need next week, not everything you can.

- **Crash and disconnect rate per player-hour**, by build. These feed the launch go or no-go.
- **The tutorial funnel for new accounts**, step by step (MMO308 week 4). Compare it with the closed beta's.
- **The week 6 targeted tests**, with the instrumentation from sprint 4. Stop each test when it reaches its players-needed count, not when the numbers look good (MMO308 week 6 on why peeking inflates false positives).
- **Peak concurrency and tick time at peak**, to compare with the forecast in section 3. Next week's launch forecast depends on how wrong this one was.
- **Server-side economy flows** per player-hour (MMO304 week 12), so launch starts with a baseline.

## 6. Worked example: how big should the open beta be?

### The hook

EA let players sign up for SimCity's closed betas from August 2012, and those betas ran in January and February 2013 with the stated aim of load-testing the servers. When SimCity launched in March 2013, the servers were overloaded, with outages, disconnections and lost save data. MMO407 week 3 used this case to show that a beta built to test load did not predict launch load, because a beta holds far less play than a launch. The same arithmetic applies to your weekend. You can size it to find what matters, or you can size it by accident.

### The model

```
exposure needed      E = 3 × (player-hours per firing of the rarest bug you must catch)
sign-ups needed        = E / (show-up rate × hours per active player)
peak-hour CCU          = E × busiest-day share × busiest-hour share
forecast peak          = peak-hour CCU × spike factor
safe capacity          = knee × (1 − headroom)
```

The beta is sized correctly when sign-ups meet the exposure target and the forecast peak stays under safe capacity. If both cannot hold, you choose which to give up, and you choose before the weekend.

### Numbers you can check

Emberfall, the running example team, wants a 95% chance of seeing any bug that fires once per 400 player-hours. Its closed beta had a 45% show-up rate and 2.5 hours of weekend play per active tester. Saturday carried 45% of the play, and the busiest hour held 12% of Saturday's play. The sprint 4 load test of the whole shard, two zone servers behind one login service and one database, put the knee at 140 CCU. That is less than twice [week 3](w03-production-sprint-3-feature-complete-and-server-budget.md)'s 80 per zone server, and the reason is the course's one capacity model for a shard:

```
shard knee = min(z × zone knee, shared knee)
```

Here `z` is the number of zone servers, the zone knee is week 3's 80 per zone server, and the shared knee is the load at which the login service and the database that all the zone servers use start to slow down. With two zone servers the zone limit is 160, so the 140 the test found is the shared limit. A third zone server would add nothing. Past about 140 players, only a second shard with its own login service and database, or a queue, adds room (week 9). Emberfall has 900 sign-ups. All values are invented teaching values.

```
exposure needed      E = 3 × 400                     = 1,200 player-hours
sign-ups needed        = 1,200 / (0.45 × 2.5)         = 1,066.7  → 1,067
exposure from 900      = 900 × 0.45 × 2.5            = 1,012.5 player-hours
Saturday play          = 1,200 × 0.45                = 540 player-hours
peak-hour CCU          = 540 × 0.12                  = 64.8
forecast peak          = 64.8 × 1.5                  = 97.2
safe capacity          = 140 × (1 − 0.30)            = 98
```

With 900 sign-ups the chance of seeing a once-per-400 bug is `1 − e^(−1,012.5 / 400) = 1 − e^(−2.53) = 92.0%`. That is close to the target but not at it. The team needs 167 more sign-ups. With 1,067, the forecast peak of 97.2 fits under the safe capacity of 98 with less than one player to spare.

That margin is too thin to trust, because every input is an estimate from one closed-beta week. The team has four levers, each of which moves one of the formulas.

| Lever | What it changes | Effect here |
|---|---|---|
| Invite in three waves | Spike factor falls from 1.5 toward 1.2 | Forecast peak `64.8 × 1.2 = 77.8`, 20 below safe capacity |
| Cap logins at 98 with a queue | Peak can no longer exceed capacity | Protects the server; costs some players a wait |
| Extend the beta to four days | Same exposure over more days, lower busiest-day share | Lower peak; costs a day of team time |
| Second shard | Doubles capacity | Costs the running cost and a merge; tests nothing launch needs if launch runs one shard |

Emberfall chooses waves plus a hard login cap at 98, and recruits 170 more sign-ups through its community channels. If the first wave's peak runs above forecast, the cap protects the server and the third wave is delayed.

This script reproduces the numbers.

```python
import math

EVERY = 400                 # rarest bug to catch: once per 400 player-hours
SHOW, HOURS = 0.45, 2.5     # closed-beta show-up rate, weekend hours per active player

need_E = 3 * EVERY
print(f"exposure needed: {need_E} player-hours, sign-ups needed: {math.ceil(need_E / (SHOW * HOURS))}")
for signups in (900, 1067):
    E = signups * SHOW * HOURS
    print(f"{signups} sign-ups: E = {E:,.1f} player-hours, "
          f"P(see 1-in-{EVERY} bug) = {1 - math.exp(-E / EVERY):.1%}")

peak_hour = 1200 * 0.45 * 0.12          # Saturday share, then busiest-hour share
safe = 140 * (1 - 0.30)                 # load-test knee with 30% headroom
for spike in (1.5, 1.2):
    print(f"spike {spike}: forecast peak {peak_hour * spike:.1f} CCU, safe capacity {safe:.0f}")
```

It prints:

```
exposure needed: 1200 player-hours, sign-ups needed: 1067
900 sign-ups: E = 1,012.5 player-hours, P(see 1-in-400 bug) = 92.0%
1067 sign-ups: E = 1,200.4 player-hours, P(see 1-in-400 bug) = 95.0%
spike 1.5: forecast peak 97.2 CCU, safe capacity 98
spike 1.2: forecast peak 77.8 CCU, safe capacity 98
```

### Move it yourself

Open MMO407's [beta exposure model](../../MMO407-launch-scaling-and-post-mortems/examples/w03-beta-exposure.html). Set the beta to 480 active testers at 2.5 hours (the 1,067 sign-ups at 45% show-up) and the launch audience to your launch-week forecast. Read off the rates a clean open beta still cannot rule out. That band is the risk you carry into launch, and your launch rota has to be able to handle it.

### Cross-game recognition

The same two-sided sizing runs through every large beta. MMO407 week 2 showed New World's launch-scale version, where one world's cap of 2,000 players and its queue limit were the capacity side. MMO407 week 3 used SimCity to show the exposure side. At your scale the numbers are a thousand times smaller and the shape is the same: one formula wants more players, the other wants fewer, and the levers (waves, caps, head starts, extra shards) exist to let both hold.

### Eyes-open design judgment

Every input to this calculation is uncertain, and the uncertain ones are the ones strangers control: show-up rate and spike. Plan for being wrong in both directions. If only 30% show up, exposure falls to 800 player-hours and your 95% becomes about 86%, which you should report honestly in the exit review rather than rounding up. If 60% show up, your cap and waves carry the load. Do not solve a capacity problem by shrinking the beta below the exposure target unless you also accept, in writing, the bug rate you are no longer able to see.

### Check yourself

1. Your team decides it must catch bugs down to once per 600 player-hours. Recompute exposure and sign-ups with the same rates.
2. Saturday's busiest hour actually held 18% of the day's play, not 12%. With 1,067 sign-ups and waves (spike 1.2), does the forecast peak still fit under 98?
3. The beta ends with zero crashes of a particular kind in 1,150 player-hours. What is the highest rate of that crash the data can rule out at 95%?

## Studio session plan

The studio meeting runs 180 minutes with one break. The beta itself runs Friday evening to Sunday evening after this meeting.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Instructor briefing: exposure, peak forecast, levers, exit criteria | — |
| 0:15-0:50 | Fill the sizing sheet (lab 8, part A) from your closed-beta and load-test data | Sizing sheet with chosen levers |
| 0:50-1:20 | Build the weekend rota, fill the severity table with names, list kill switches | Rota and severity table |
| 1:20-1:30 | Break | — |
| 1:30-2:05 | Kill-switch drill: each switch flipped and restored on the staging server; one simulated SEV2 run end to end | Drill log with times |
| 2:05-2:30 | Write the exit criteria and the known-issues post; check the targeted-test instrumentation fires | Exit criteria, pinned post draft |
| 2:30-3:00 | Instructor walk-round: readiness checklist from week 7, evidence for each line | Go for the weekend, or a named blocker |

## Deliverables

Due before the week 9 studio meeting, in `production/week08/`.

1. **Sizing sheet** (lab 8): exposure target, sign-ups, peak forecast, safe capacity, chosen levers. Checked by recomputing the peak forecast.
2. **Beta operations log**: rota as run, every incident with severity, times and actions, every kill-switch use.
3. **Forecast against actual**: sign-ups, show-up rate, exposure, peak CCU and tick time at peak, each with its forecast next to it. This is the input to the launch forecast.
4. **Targeted-test results**: each week 6 test with its `n` and verdict, or a statement that it did not reach its sample.
5. **Exit review**: each exit criterion with pass or fail and its evidence, and a one-paragraph recommendation for the launch go or no-go.

## Common failure modes

- **Sizing by hope.** "As many as possible" is not a size. Without a peak forecast, the first sign of trouble is the login server falling over.
- **No cap.** A server without a login cap degrades for everyone at once. A queue annoys a few; a tick-time collapse annoys all.
- **Everyone on call all weekend.** Friday's heroes make Sunday's bad decisions. Rota in blocks.
- **Untested kill switches.** A switch that has never been flipped is a hypothesis.
- **Bug reports that live in Discord.** If it is not in the tracker with a build number, it will not be fixed before launch.
- **Stopping a targeted test when it looks good.** Stop at the planned sample, or say it did not reach it.
- **Forgetting the forecast.** If you do not write down what you expected, you cannot measure how wrong you were, and next week's launch forecast inherits the same error.

## Review checklist

The instructor checks, at the week 9 meeting:

- [ ] Exposure target and bug rate are stated with a reason; sign-ups needed are computed correctly.
- [ ] The peak forecast and safe capacity are computed from named sources (closed-beta logs, sprint 4 load-test report).
- [ ] At least one lever was chosen before the weekend and its effect is shown.
- [ ] Every kill switch was drilled before the doors opened, with times logged.
- [ ] The rota ran in blocks of at most four hours with a primary and a backup.
- [ ] The forecast-against-actual table is complete, with the error for each line.
- [ ] Every targeted test has a verdict at its planned `n` or is marked as not reaching it.
- [ ] The exit review gives a recommendation that follows from the criteria.

## Sources

- Wikipedia, "SimCity (2013 video game)" (read September 2026). Closed beta sign-ups from August 2012; closed betas in January and February 2013 to load-test the servers; release in early March 2013; network outages, disconnections and lost save data at launch.
- Wikipedia, "New World (video game)" (read September 2026; "New World: Aeternum" redirects there). Server capacity of 2,000 players each and queues reaching the 25,000-person limit at launch in September 2021, as used in MMO407 week 2.
- MMO407 week 3 (this program) for the exposure model and the rule of three, with its sources.
- All sign-up counts, rates, shares, knee values and headroom in sections 2 to 6 are invented teaching values.
