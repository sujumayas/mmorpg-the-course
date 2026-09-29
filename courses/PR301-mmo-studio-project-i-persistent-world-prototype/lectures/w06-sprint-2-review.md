# PR301 · Week 06 — Sprint 2 Review

**Why this matters:** Sprint 2 is putting combat and mobs on your world server, and this week you are halfway through it. In PR201 a review asked whether three players could fight. Here it has to ask whether a hundred bots can, while every mob on the map thinks on the same server. Most student worlds pass the first question in the review room and fail the second on the alpha weekend, because nobody measured what one more mob costs.

**You will be able to:**
- Inspect the sprint 2 increment under bot load at the midpoint, and again at the sprint 2 review at the start of week 7, not only in a hand-played demo.
- Measure tick time as a distribution and state it against the week 2 budgets.
- Fit a four-run cost model of tick time in players and mobs, and compute the largest mob count your server can hold at the load-test crowd.
- Choose between cutting content, changing the simulation and revisiting the architecture, and put the choice into the sprint 3 backlog with a size.

**Before class:** Reread [MMO302 week 5](../../MMO302-mmo-server-architecture/lectures/w05-tick-rate-for-mmos-vs-shooters.md) on tick budgets and [MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) on bot load tests. Reread your week 2 decision record, especially the trigger you wrote for the single-process decision. Bring the midpoint sprint 2 server build, your bot client and the tick-time log from at least one run.

**Prerequisites from earlier courses:** [PR201 week 7](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w07-sprint-2-review-and-playtest.md) (the review as a working session). [MMO302 week 1](../../MMO302-mmo-server-architecture/lectures/w01-scale-targets-ccu-messages-and-n-squared.md) (why pairwise work grows as a product). [MMO302 week 3](../../MMO302-mmo-server-architecture/lectures/w03-area-of-interest-grids-radius-hysteresis.md) (spatial grids). [MMO302 week 14](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md) (percentiles, not averages). [CS203 week 6](../../CS203-artificial-intelligence-for-games/lectures/w06-finite-state-machines.md) (the mob state machine). [MMO303 week 13](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w13-combat-simulators.md) (simulating fights before players do).

---

## 1. What this review has to settle

Sprint 2 runs from the week 5 session to the week 7 session. Its review takes the first part of week 7. This week's session is the midpoint: a stand-up, the load runs below, a hand playtest by the paired team and a burn-down check. The load runs come now because their result changes what sprint 3 plans, and the grid fix needs a place in that plan.

The *Saltmarsh* sprint 2 goal from week 5 read: "Twenty bots and three humans hunt the Reedbank wolf camp at once, and every kill, drop and death is decided and saved by the server." The review at the start of week 7 answers it with yes or no, counts only the stories that meet the definition of done in the tagged build, and ends with backlog changes. That part is the same as PR201. Three things are new.

**The review is not done until the server has been loaded.** A hand-played demo with seven people proves the combat rules. It says nothing about the course outcome, a world that holds 50 or more concurrent players. Week 2 set the load test at twice the target, 100 bots. Your definition of done for any server story now includes "measured at 100 bots". A combat story that works for seven players and has never seen a hundred is not done.

**Mobs are the first content that costs server time with nobody watching.** A player costs you work because they send input. A mob costs you work every tick. It checks for targets, walks paths and regenerates health. Week 5 asked for an idle state so that a wolf with nobody near costs almost nothing. This review measures whether it does.

**The focus factor gets its second data point at the review.** The sprint 1 review measured 0.46. For sprint 2, *Saltmarsh* committed the 38.2 hours that review forecast. Today's burn-down showed the combat chain ahead of plan, and in the second week the team pulled backlog stories estimated at 6.6 hours into the sprint, starting with the real authentication stubbed in sprint 1. At the review, stories estimated at 44.8 hours had met the definition of done out of 83 available, so `f = 44.8 / 83 = 0.54`. Week 7 plans sprint 3 with the range 0.46 to 0.54, not a single number.

## 2. The budgets from week 2

Your world server runs a fixed-rate loop. At `f_tick` ticks per second, each tick has

```
tick_ms = 1000 / f_tick
```

At *Saltmarsh*'s 10 Hz that is 100 ms. Week 2 set two limits on it, and this review holds the build to both.

- **CPU budget 0.6.** Week 2 kept one worker at or below 60% busy, because response time climbs steeply as a single worker nears full use ([MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md)). At 10 Hz that is a mean tick of at most 60 ms.
- **The D3 trigger.** The decision record said: one process for the whole world, *revisit if* the week 6 load test shows p99 tick time above 80 ms at 100 bots.

Together these are the course's **tick rule**. At 100 bots, the mean tick stays at or under 60 ms and p99 at or under 80 ms. It applies to every load test from here on, including the week 8 freeze and the week 13 beta. Notice the percentile in the second limit. A mean tick of 50 ms can hide one tick in a hundred at 150 ms. At 10 Hz that is a stall every ten seconds, and players feel it as rubber-banding. Your server should write one line per tick with the tick number, its duration, the player count and the mob count. Everything in this guide is computed from that log.

Week 2 also warned that its model left out the simulation itself: AI, combat and regeneration. "Week 6 measures it directly when the mobs think." This is that measurement.

## 3. Loading the review

A review run needs bots, because your class cannot supply a hundred players at 2 pm on a Tuesday. [MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) covers bot design. Dee's bot from sprint 2 needs three properties.

1. **It uses the real client protocol.** A bot that calls server functions directly skips the network layer and the input validation from sprint 1.
2. **It behaves like a player where it matters for cost.** It moves, picks targets, attacks, loots and dies. A bot standing still at spawn costs almost nothing and tells you nothing.
3. **It stands where week 2 said the worst crowd stands.** Week 2 costed the worst case, all players in one crowd in the market square. Run that layout first, then a spread layout, and record which each run used.

Run each configuration for at least ten minutes after the world has warmed up, and discard the first two minutes. Ten minutes at 10 Hz is 6,000 ticks, enough for a stable p99, since 60 ticks lie above it.

## 4. Worked example: how many mobs fit?

### The hook

EVE Online runs its server logic on a tick of one second. That sounds generous next to your 100 ms, until you read the rest. The EVE University wiki notes that a typical server node hosts hundreds of star systems, so each system may get a hundredth of a second or less of each tick. When a fleet fight overloads a node, EVE does not drop work. It slows the whole node's game clock with time dilation, down to 10% of normal speed. Minecraft makes the same deal at a different scale. A Java Edition server targets 20 ticks per second, 50 ms each, and when the machine cannot keep up, the tick rate falls and the whole world runs slow.

Both games fixed a budget per tick and then had to live with what happens when the work does not fit. *Saltmarsh* has to make the same decision about its wolves, with numbers.

### The model

Tick time grows with players, with mobs, and with their product. The product comes from the idle state's wake check. Every tick, each idle wolf asks whether any player is inside its aggro radius, and the sprint 2 code asks every player. That is the pairwise term from [MMO302 week 1](../../MMO302-mmo-server-architecture/lectures/w01-scale-targets-ccu-messages-and-n-squared.md). Mean tick time is modelled as

```
t(P, M) = a + g + c·M + d·P·M
```

where `t` is mean tick time in ms, `P` is players (bots) online, `M` is mobs spawned, `a` is the fixed cost of an empty world, `g` is the player cost at the load-test crowd (mostly week 2's deliveries), `c` is the cost per mob, and `d` is the cost per player-mob pair.

The player cost `g` is measured at one crowd size, 100 in the market square, because week 2 showed it grows with `P²`. Use this model at `P = 100` only. For other crowd sizes, scale `g` with week 2's delivery formula.

Four bot runs, arranged as a 2 × 2 design, pin down the four coefficients. The alpha world as designed has 240 mobs: the Reedbank camp's 18 wolves, the 60 critters of the market square, and the other camps.

| Run | Bots `P` | Mobs `M` | Mean tick (ms) | p99 tick (ms) |
|---|---|---|---|---|
| A | 0 | 0 | 3.0 | 4.1 |
| B | 100 | 0 | 41.0 | 55.2 |
| C | 0 | 240 | 15.0 | 20.3 |
| D | 100 | 240 | 65.0 | 88.4 |

Because the D3 trigger is a p99 limit, you also need the ratio of p99 to mean at load. Take it from run D, the run closest to the real weekend: `k = 88.4 / 65.0 = 1.36`.

### Numbers you can check

Solve for the coefficients one at a time.

```
a = t_A                              = 3.0 ms
g = t_B − a                          = 38.0 ms at 100 bots
c = (t_C − a) / 240                  = 12.0 / 240     = 0.05 ms per mob
d = (t_D − a − g − 240c) / (100 × 240)
  = (65.0 − 3.0 − 38.0 − 12.0) / 24,000
  = 12.0 / 24,000                    = 0.0005 ms per pair
```

First, check week 2. Its model predicted `5 × 100 × 99 = 49,500` player deliveries per second at 8 µs each, which is 39.6% of a core, or 39.6 ms of every 100 ms tick. The measured `g` is 38.0. The architecture review's arithmetic held.

The mobs are the problem. Run D fails both limits: a mean of 65.0 against 60, and a p99 of 88.4 against 80. The D3 trigger has fired. To find the largest mob count that fits, take the tighter of the two limits as a mean:

```
mean allowed  = min(60, 80 / 1.36) = min(60, 58.8) = 58.8 ms
cost per mob  = c + d·P = 0.05 + 0.0005 × 100   = 0.10 ms
M_max         = (58.8 − 3.0 − 38.0) / 0.10      = 178 mobs
```

The design has 240. Each wolf costs as much in wake checks (0.05 ms) as in everything else it does (0.05 ms). Before anyone reaches for zone servers, model the cheaper options.

**Option 1: cut content.** Drop to 170 mobs by thinning the outer camps.

**Option 2: grid wake checks.** Each idle mob checks only players in its own and neighbouring grid cells ([MMO302 week 3](../../MMO302-mmo-server-architecture/lectures/w03-area-of-interest-grids-radius-hysteresis.md)). In the worst-case layout, 100 bots in the market square, only the square's 60 critters have any player nearby. The other 180 mobs find empty cells and check nobody, so the pair term becomes `0.0005 × 100 × 60 = 3.0` ms instead of 12.0. Week 2 deferred a grid "with a trigger", and this is it.

**Option 3: revisit D3 and split into zone servers.** Week 2 estimated handoff at 60 hours and named it as the place items get duplicated. Model it only if options 1 and 2 fail.

| Option | Mobs | Mean tick (ms) | p99 est. (ms) | Both limits |
|---|---|---|---|---|
| As built | 240 | 65.0 | 88.4 | fails |
| 1. Cut to 170 | 170 | 58.0 | 78.9 | passes, 1.1 ms spare |
| 2. Grid wake checks | 240 | 56.0 | 76.2 | passes, 3.8 ms spare |
| 2 + a 40-mob world boss in the square | 280 | 60.0 | 81.6 | fails |

Check two rows yourself. Option 1: `3.0 + 38.0 + 170 × 0.05 + 0.0005 × 100 × 170 = 3.0 + 38.0 + 8.5 + 8.5 = 58.0`, times 1.36 is 78.9. Option 2: `3.0 + 38.0 + 240 × 0.05 + 3.0 = 56.0`, times 1.36 is 76.2.

Both options pass, and neither passes by much. The last row is the warning. Week 2's first check-yourself question added a world boss with 40 extra mobs to the square. With the grid in place, those 40 are near the crowd, so each costs the full 0.10 ms. That adds 4 ms, and the build fails again. The group encounter in week 12 has to run in an instance or bring its own budget.

*Saltmarsh* took option 2 as a 6-hour story for Ana in sprint 3, with option 1 as the fallback. If the grid is not done and measured by the week 8 mid-sprint session, the spawn table drops to 170 before the alpha freeze. D3 stays as written, with its trigger updated to "p99 above 80 ms at 100 bots *after* the grid".

### A visual you can move

No separate interactive ships this week, because the model is linear at a fixed crowd and fits in the lab 06 checker. Put your four runs in [`labs/lab06-starter/runs.csv`](../labs/lab06-starter/runs.csv), change the planned mob count and rerun. If your team wants a picture for the review, plot mean tick against mobs for the as-built and grid versions. Both are straight lines, and the grid line is half as steep for mobs away from the crowd.

### Cross-game recognition

Rewrite the two hook games in the same form. EVE's tick is 1,000 ms, shared by hundreds of systems on a node, so each system's budget is of the order of 10 ms, and `a` for one system competes with every other system on the node. When a fight pushes `t` past the budget, EVE stretches the tick instead of dropping work. Time dilation is a controlled way of lowering `f_tick` so that `1000 / f_tick` grows to fit `t`. Minecraft's rule is ours with `f_tick = 20` and a 50 ms budget. When the world's entities and block updates exceed it, the tick rate falls, and the game slows for everyone on that server.

The WoW Classic stress tests of May to July 2019 are the third case, from the testing side. According to the Warcraft Wiki, the stress-test realms capped characters at level 5, and Blizzard's announcement said the caps were there to bring many players close together. Crowding raises the number of players near each creature, which is the `P·M` term. The test was built to hit the expensive term on purpose, the same reason your run D uses the market-square crowd.

### Eyes-open judgment

- **The worst case is not the only case.** In a spread layout, fewer players hear each other, so `g` falls. But more mobs have a player nearby, so the grid saves less. Run a fifth configuration with bots spread over the world and report both.
- **The p99 ratio is not a law.** 1.36 came from one run. Wolves waking in bursts when a crowd walks into the camp can raise it. Remeasure after the grid lands.
- **Cutting content is a real option.** 170 mobs may be plenty for an alpha with twenty humans. If your pillars do not need a dense world, the cheapest story is a spawn-table edit. Engineering stories cost sprint 3 hours that the economy needs.
- **The linear model breaks near the budget.** Once ticks overrun, work queues up and the next tick starts late. Do not extrapolate past the budget. Measure instead.

### Check yourself

1. A team runs its server at 15 Hz with week 2's CPU budget of 0.6. What is the largest acceptable mean tick?
2. With the grid in place and the 100 bots in the square, how many mobs can the team add *away from the crowd* before the mean reaches 58.8 ms?
3. A teammate says run D is redundant because "we can add runs B and C." What does run D measure that B and C cannot?

<details>
<summary>Answers</summary>

1. The tick is `1000 / 15 = 66.7` ms, so the mean must stay at or under `0.6 × 66.7 = 40` ms.
2. With the grid, the 60 square mobs cost 0.10 ms each and far mobs cost only `c = 0.05`. `3.0 + 38.0 + 60 × 0.10 = 47.0`, leaving 11.8 ms, which is `11.8 / 0.05 = 236` far mobs. That is 296 mobs in all, 56 more than today's 240.
3. The interaction coefficient `d`. B and C each have one factor at zero, so the product `P·M` is zero in both. Only a run with both players and mobs can show the 12 ms that neither alone predicts.

</details>

## 5. Turning the review into sprint 3 input

Today's session drafts the backlog changes, and the review at the start of week 7 finalizes them. From a combat-and-mobs sprint they usually fall into three groups.

- **Performance stories** with a model behind them, like the grid, each sized and each with a measurement that proves it done ("p99 at or under 80 ms at 100 bots in the square layout").
- **Combat bugs** found in the hand-played part of the review, triaged with the severity scale from [PR101 week 10](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md).
- **Balance notes** that are not stories yet. "The wolf pack kills a fresh character in 6 seconds" is a number to check against your combat simulator from [MMO303 week 13](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w13-combat-simulators.md), not an opinion to argue about.

Sprint 3 is economy and crafting. Performance work you take now competes with it for the same hours, so size it honestly and write down the fallback.

## Studio session plan

Week 6 meeting, 3 hours, in the middle of sprint 2. Two teams are paired and load and play each other's builds. The sprint 2 review itself opens the week 7 session.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Setup: both servers up from midpoint builds, bot clients ready, tick logging on | Both servers accept a client |
| 0:15-0:35 | Team A stand-up and burn-down check: goal-chain status, drop order, hours done so far | Burn-down decision |
| 0:35-1:05 | Team B plays team A's world by hand while team A runs configuration D behind them | Combat issue log, tick log for run D |
| 1:05-1:15 | Break and swap | |
| 1:15-1:35 | Team B stand-up and burn-down check | Burn-down decision |
| 1:35-2:05 | Team A plays team B's world while team B runs configuration D | Combat issue log, tick log |
| 2:05-2:40 | Each team alone: runs A to C (5 minutes each if not done before class), fit the model, compute `M_max`, draft the options table | Lab 06 parts A and B |
| 2:40-3:00 | Draft backlog changes, D3 trigger reviewed | Draft sprint 3 input list, updated decision record |

If runs A to C were done before class, spend 2:05-2:40 on the spread-layout run instead.

At the sprint 2 review (first part of the week 7 session): goal read aloud and answered yes or no on the tagged build, a 100-bot run in the worst-case layout, done hours counted, the sprint 2 focus factor, and the retrospective with one change for sprint 3.

## Deliverables

In `production/week06/` in the team repository.

Due 48 hours after this meeting:

1. **Tick budget report** in the lab 06 format ([`labs/lab06.md`](../labs/lab06.md)): the four runs with their tick logs, the fitted coefficients, the comparison of `g` with your week 2 prediction, `M_max`, the options table and the team's decision. `check_tick.py` must print `PASS`.
2. **Decision record update**: the D3 trigger result and what the team decided.

Due at the sprint 2 review, start of week 7:

3. **Sprint 2 review record**: goal met (yes or no), hours committed and done, the sprint 2 focus factor, and the list of backlog changes.
4. **Sprint 3 input list**: performance stories with sizes and measurable done conditions, triaged combat bugs, balance notes with the number that prompted them.

## Common failure modes

- **Reviewing with seven humans only.** The room has fun and the server has never seen a hundred clients. Every server story's done condition names a load.
- **Reporting the average tick.** A 50 ms mean with 150 ms spikes looks fine on a slide. Report p99 and the worst tick.
- **Bots that stand still.** Idle bots cost nothing, and the model's `g` comes out tiny. Bots must move, fight and die.
- **One run at full load.** Without runs B and C you cannot tell whether players, mobs or their product is the problem, and you cannot say which fix will help.
- **An idle state that still looks at everyone.** The wolf skips pathfinding but still scans every player to decide whether to wake. That is the `d` term. Measure idle cost with players online, not only in an empty world.
- **Jumping to zone servers.** The trigger fired, so the team splits the world, which costs 60 hours and brings handoff bugs. Model the cheap options first.

## Review checklist

The instructor checks at this meeting, in the submission, and at the sprint 2 review at the start of week 7:

- [ ] The review ran from the tagged build at the start of week 7, and the sprint goal was answered yes or no.
- [ ] At least one run reached 100 bots through the real protocol, in the week 2 worst-case layout, with bots that move and fight.
- [ ] The tick log is per tick, and the report states p99, not only the mean.
- [ ] Four runs in a 2 × 2 design, coefficients fitted, `g` compared with week 2, `M_max` computed, and `check_tick.py` agrees.
- [ ] The options table models at least one content option and one engineering option before any architecture change.
- [ ] The chosen option has a sprint 3 story with a size, a measurable done condition and a fallback.
- [ ] The sprint 2 focus factor is recorded with its inputs.
- [ ] A spread-layout run exists or is scheduled before the alpha freeze.

## Sources

- EVE University Wiki, "Server tick" (accessed September 2026, current mechanics). The server aims for one tick per second; a typical node handles hundreds of systems, so a single grid may get a hundredth of a second or less of each tick. https://wiki.eveuniversity.org/Server_tick
- EVE University Wiki, "Time dilation" (accessed September 2026). Time dilation slows in-space actions on an overloaded node, to a minimum of 10% speed; introduced in 2011 (see the MMO302 week 12 sources for the CCP dev blog of 22 April 2011). https://wiki.eveuniversity.org/Time_dilation
- Minecraft Wiki, "Tick" (accessed September 2026, Java Edition). A fixed rate of 20 ticks per second, 50 ms per tick; ticks per second fall when the computer cannot keep up. https://minecraft.wiki/w/Tick
- Warcraft Wiki, "Stress test" (accessed September 2026). WoW Classic stress tests on 22 to 23 May, 19 to 20 June and 25 to 26 July 2019; level cap of five on stress-test realms. https://warcraft.wiki.gg/wiki/Stress_test
- Blizzard Entertainment, "Mark Your Calendars: WoW Classic Launch and Testing Schedule" (World of Warcraft news, 14 May 2019, archived copy of 3 July 2019 on web.archive.org, as cited in MMO302 week 11). Stress tests meant to push the technology to its limit, with level caps to bring many players close together.
- Schwaber, K. and Sutherland, J. (2020). *The Scrum Guide*, November 2020 edition. The sprint review as a working session that inspects the increment.
- The *Saltmarsh* team, its runs, coefficients, mob counts and hours are invented for teaching, continuing the example from weeks 1 to 5. The CPU budget of 0.6 and the D3 trigger come from the week 2 guide.
