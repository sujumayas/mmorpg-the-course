# PR301 · Week 12 — Sprint 5: Group Encounter

**Why this matters:** The course brief promises at least one group encounter, and next week 50 people will try it at once. An encounter is the feature in your world that fails most visibly. A boss that never resets, loot that goes to the wrong player, or a mechanic nobody can see will be the first thing every beta tester mentions. It is also the feature teams most often finish late, because the last 20% of it (reset logic, loot, edge cases when a player disconnects mid-fight) only shows up once people pull the boss. This week you build the encounter, tune it with a model before you tune it with pulls, and read your burn-down on Wednesday while there is still time to cut.

**You will be able to:**
- Define the smallest encounter that meets the milestone, and name its coordination mechanic.
- Set boss health and an enrage timer from simulated party damage, so that test pulls check mechanics and readability, not numbers.
- Budget test pulls as a scarce resource and say what a clean run of pulls does and does not prove.
- Project a mid-sprint burn-down two ways, and cut scope on day 3 by the amount the slower projection says.

**Before class:** Bring your sprint 4 review notes and the party build from last week. Re-read MMO306 week 4 on encounter mechanics (20 minutes) and week 5 on telegraphing (15 minutes). Skim MMO303 week 13 on combat simulators (15 minutes) and MMO407 week 3, section 2 on the rule of three (10 minutes).

**Prerequisites from earlier courses:** [MMO306 week 3, dungeon design](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w03-dungeon-design-trash-bosses-loot.md), [week 4, encounter mechanics](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w04-encounter-mechanics-tank-and-spank-to-dance-fights.md), [week 5, telegraphing and readability](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w05-telegraphing-and-readability.md) and [week 7, tuning encounters with logs](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w07-tuning-encounters-with-logs.md). [MMO303 week 5, the holy trinity](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w05-the-holy-trinity-tank-healer-dps.md) and [week 13, combat simulators](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w13-combat-simulators.md). [MMO302 week 2, shards, zones and instances](../../MMO302-mmo-server-architecture/lectures/w02-shards-realms-zones-instances-layers.md). [PR101 week 7, task tracking](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md) (burn-down charts). From this course, [week 11](w11-sprint-4-social-systems.md) (the party system and the one-week sprint rule). Looking ahead, [MMO407 week 3, beta strategies](../../MMO407-launch-scaling-and-post-mortems/lectures/w03-beta-strategies.md) (year 4) derives the rule of three.

**Interactive:** [Burn-down projection](../examples/w12-burndown-projection.html). Use it in the studio session when you project your own burn-down.

---

## 1. The smallest encounter that meets the milestone

The brief asks for "at least one group encounter". For marking purposes that means:

- **A fight built for a party,** not for one player with friends watching. A solo player at the party's level should lose.
- **One coordination mechanic.** Something the party must do together or in agreed roles: spread out, stack, interrupt in turn, swap the tank. MMO306 week 4 catalogues them. One clear mechanic beats three muddy ones.
- **A readable telegraph** for that mechanic (MMO306 week 5). If testers die to it without knowing why, it is a bug in the telegraph, not a skill check.
- **Correct reset and reward.** The boss resets on a wipe and when pulled too far. Loot goes to one party member by a stated rule, through the transactional item path your economy sprint built.
- **Telemetry.** Pull start, wipe, kill and deaths by ability, so that week 13 can tell you where parties failed.

Anything beyond that is optional. Second phases, add waves and bespoke death animations are what teams cut when the burn-down turns. Decide in planning which items are in the minimum and which are not, so that the cut on Wednesday is already agreed.

Use a light party as the unit: one tank, one healer and two damage dealers, the shape Final Fantasy XIV uses for its four-player content. Four is small enough that a team of seven can fill a party with people to spare for observing, and it means 50 beta testers can run up to 12 parties at once, which matters for section 2.

## 2. Where the encounter lives on the server

You have two choices, and MMO302 week 2 covers both.

- **Instanced.** Each party gets its own copy of the boss room. Clean ownership, easy reset, no griefing. Each copy is a small simulation on your server, so 12 parties means 12 of them running at once.
- **Open world.** One boss in the shared world. Cheap to build, but you now need rules for tagging (who owns the kill), for a second party arriving mid-fight, and for respawn timers. Those rules are where the bugs are.

Most teams should instance. Whichever you pick, write down the maximum number of simultaneous copies at beta and add it to the week 13 load test. An encounter that runs fine alone and costs 4 ms of tick time per copy costs 48 ms with 12 copies. Week 6 measured 41 ms of mean tick for 100 bots in an empty world, so those copies would push the mean far past the 60 ms that the week 6 rule allows on a 10 Hz server. Measure one copy's cost this week, not at the beta.

Three server behaviours need explicit code and a test each: **leash** (the boss resets if pulled beyond a distance), **wipe detection** (all party members dead or out of range, then reset after a delay), and **disconnect handling** (a player who drops mid-fight stays in the party and can rejoin the instance for a set time). The worked example shows what happens when a team forgets the first one.

## 3. Numbers before pulls

Test pulls are slow and noisy. A four-person pull tells you whether people understood the mechanic. It tells you very little about whether the boss has the right health, because four people's damage on one night varies more than any tuning change you'd make. So set the numbers with a model first, as MMO303 week 13 shows, and use pulls to check what a model cannot.

For a boss with health `H`, party damage per second `D` from the simulator, and a fraction `u` of the fight in which the party can actually deal damage (the rest is spent moving for mechanics):

```
kill time        T = H / (D × u)
health for a target kill time    H = D × T_target × u
enrage margin    m = T_enrage / T − 1
lowest party DPS that beats the enrage    D_min = H / (T_enrage × u)
```

The enrage timer is a design statement about how much worse than the simulated party a real party may be and still win. Write it as a percentage of simulated DPS, not as a number of seconds.

## 4. Test pulls are a budget

A test pull costs the fight length plus the time to run back, rebuff and talk about what went wrong. Every tuning change that needs a new server build costs a rebuild and deploy. With four to six people free at the same time for two sessions a week, you get about fifteen pulls. Spend them on questions a pull can answer:

- Did the party see the telegraph and react? Look at deaths by ability.
- Did the reset, leash and loot work every time?
- What happens when someone disconnects, on purpose, mid-pull?

When a question has a yes-or-no answer per pull, such as "did anyone die to the slam after the telegraph change?", a clean run still has an upper bound. MMO407 week 3 gives the rule of three: after zero failures in `n` independent trials, the 95% upper bound on the failure rate is about `3/n`. Fifteen clean pulls say the true rate is probably below 20%, not that it is zero. That is enough to take into beta, where 50 testers will run many more pulls than your team can.

## 5. Reading the burn-down on day 3

A burn-down chart plots remaining work against days. PR101 week 7 introduces it. In a one-week sprint it is only useful if someone reads it in the middle of the week and acts on it.

Two projections are worth computing on day 3:

```
average rate    r_avg    = (commit + added − remaining) / days elapsed
recent rate     r_recent = work completed in the last two days / 2
projected left  = remaining − r × days left
```

Use whichever projection leaves more work undone. If it is above zero, cut at least that much on day 3, from the items already marked non-minimum in planning. Cutting on Wednesday costs a conversation. Discovering the shortfall on Friday costs the item you most needed, because by then everything is half done.

## 6. Worked example: the *Saltmarsh* team's Wednesday

### The hook

Final Fantasy XIV's four-player duties use a fixed shape, one tank, one healer and two damage dealers, and its eight-player content doubles each role. A fixed party shape is a production tool as much as a design one. It lets encounter designers tune against one known party instead of every possible mix. The *Saltmarsh* team's encounter, the Drowned Warden in the cistern under the market square, uses the four-player shape for the same reason. Its simulated party is the unit every number below is built on.

### Setting the numbers

The team ran the combat simulator from sprint 2 on a party of one tank, one healer and two damage dealers at the level of the cistern. Simulated damage per second was 40 for the tank, 15 for the healer and 110 for each damage dealer.

```
D           = 40 + 15 + 110 + 110               = 275 DPS
u           = 0.85   (Tidal Slam forces a spread about every 30 s)
T_target    = 300 s  (a five-minute fight)
H           = 275 × 300 × 0.85                  = 70,125, set to 70,000
T           = 70,000 / (275 × 0.85)             = 299.5 s
T_enrage    = 360 s
m           = 360 / 299.5 − 1                   = 0.20, a 20% margin
D_min       = 70,000 / (360 × 0.85)             = 228.8 DPS, 83% of simulated
```

The design statement is "a party doing at least 83% of simulated damage beats the enrage". The pulls will not be used to move `H`.

### The pull budget

The team reserved two 90-minute pull sessions at sprint planning, outside the hour budget, on Thursday and Friday afternoons.

```
session time                2 × 90                      = 180 min
planned tuning builds       4, at 10 min each to build and deploy   = 40 min
time per pull               6 min fight + 3 min reset and discussion = 9 min
pulls                       (180 − 40) / 9              = 15.6, so 15 pulls
```

Fifteen pulls over four builds is about four pulls per build. The pull plan for Thursday is: two pulls to check the telegraph, one pull with a planned disconnect, one pull where the tank drags the boss out of the room to test the leash.

### The burn-down

The team planned sprint 5 with the week 11 rule. Sprint 4 finished its 15 committed hours (11 of features and the 4-hour bug reserve) but not its stretch, so the last three weekly velocities are 22.4, 17 and 15. With everyone available, `capacity_low` is 15 and `capacity_mean` is 18.1. The bug reserve is 3 hours, 20% of the low forecast. That allows a commit of up to 12 hours. The team committed 11, which leaves room for up to `18.1 − 3 − 11 = 4.1` hours of stretch, and put the 3-hour phase 2 adds in as stretch. The burn-down tracks all 14 planned hours, split into tasks of half an hour to two hours of estimate so the chart moves daily. In the burn-down formulas, "commit" means those 14 hours.

| Item | Hours | Minimum? |
|---|---|---|
| Encounter instance: spawn, entry, reset on wipe | 3 | Yes |
| Boss phase 1 with Tidal Slam telegraph | 3 | Yes |
| Encounter telemetry (pull, wipe, kill, deaths by ability) | 1 | Yes |
| Loot rule with need/greed roll UI (deferred from sprint 4, re-estimated) | 3 | Rule yes, UI no |
| Phase 2 add spawns | 3 | No |
| Boss death VFX and sound | 1 | No |

On Tuesday, the team's own first pull found that the boss followed the tank up the stairs and into the market square. Leash logic had not been on the plan. It went in as 2 hours of added scope, because without it the encounter can't reset and fails the minimum.

Remaining work at the end of each day:

| Day | Remaining | Note |
|---|---|---|
| 0 (plan) | 14 | |
| 1 Mon | 13 | |
| 2 Tue | 13 | 2 hours done, 2 hours of leash added |
| 3 Wed | 10 | Instance and phase 1 done |

The two projections on Wednesday evening:

```
r_avg       = (14 + 2 − 10) / 3        = 2.0 hours/day
r_recent    = (2 + 3) / 2              = 2.5 hours/day
projected left, average   10 − 2.0 × 2 = 6 hours
projected left, recent    10 − 2.5 × 2 = 5 hours
```

The slower projection leaves 6 hours undone. The ideal line would have had 5.6 hours left on Wednesday, and the team has 10. It is behind by more than a full day of work in a five-day sprint.

### The cut

The remaining 10 hours are leash (2), telemetry (1), loot rule with UI (3), phase 2 adds (3) and death VFX (1). Leash and telemetry are minimum. The team cuts at least 6 hours from the rest.

| Change | Hours saved |
|---|---|
| Cut phase 2 adds. Tidal Slam already gives the fight its coordination mechanic | 3 |
| Replace the need/greed UI with a server-side round-robin rule, announced in party chat (0.5 hours to build) | 3 − 0.5 = 2.5 |
| Cut death VFX and sound; the boss uses the generic death effect | 1 |
| **Total** | **6.5** |

After the cut, the remaining work is leash (2), telemetry (1) and round-robin loot (0.5), which is 3.5 hours. At the slower rate of 2.0 hours a day, two days give 4 hours of capacity. The margin is half an hour. That is thin, and the team says so in its stand-up note. If anything else is found in Thursday's pulls, the round-robin loot is the next thing to simplify (the killer's party leader receives the item).

Notice what was not cut. The team never considered dropping the telemetry hour, which is the least visible item on the list. Without it, the beta produces 50 players' worth of pulls and no record of where they died.

### Reading the pulls

By Friday evening the team had run 14 pulls (one build took longer to deploy). After the Thursday telegraph fix, which added a ground marker 1.5 seconds before the slam, 10 pulls ran on the fixed build and nobody died to Tidal Slam in them. By the rule of three, the per-pull rate of a Tidal Slam death on that build is probably below `3 / 10 = 30%`. That is a weak claim, and the team writes it as one. The beta will test it with many more parties.

The leash worked in both pulls that tested it. The planned disconnect exposed one bug: the disconnected player could rejoin the instance, but their party frame stayed grey. It went into the tracker as a severity 3 bug for the stabilization sprint.

### What the example shows

Both burn-down projections said the sprint would miss, a day and a half before the end. Because the minimum had been marked at planning, the cut took one conversation and removed features no tester would have called missing. The encounter numbers came from the simulator, so the pulls were free to test the things only people can test: whether the telegraph reads, and whether reset, leash and disconnect work.

### Check this example

1. Suppose the healer's simulated DPS is 0 instead of 15. Keeping `H = 70,000`, what is the kill time and the enrage margin?
2. On Wednesday, a teammate says, "we did 3 hours today, so at 3 a day we finish with 4 left, cut 4". What is wrong with that?
3. The team runs 15 more clean pulls on the same build (25 in all). What can it now say about Tidal Slam deaths?

<details>
<summary>Answers</summary>

1. `D = 260`, `T = 70,000 / (260 × 0.85) = 316.7 s`, `m = 360 / 316.7 − 1 = 0.137`, a 13.7% margin. The design statement becomes "a party at 88% of simulated DPS beats the enrage". Decide whether that is still the fight you want before changing `H`.
2. One day's rate is the noisiest estimate available, and it happens to be the best day so far. The rule is to use the slower of the two projections, which asks for a 6-hour cut.
3. After 25 clean pulls, the 95% upper bound on the per-pull rate is about `3 / 25 = 12%`. Still not zero, and all 25 pulls were by the same four people who know the fight.

</details>

## Studio session plan

The studio meeting runs 180 minutes with one break. It falls on day 1 of sprint 5, so the burn-down part is practice on the worked example and on your sprint 4 data.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Instructor briefing: the minimum encounter, numbers before pulls, reading a day-3 burn-down | None |
| 0:15-0:45 | Sprint 4 review: done hours against commit, and the one planning change for sprint 5 | Review notes |
| 0:45-1:20 | Sprint 5 planning with the week 11 capacity rule; mark every item minimum or not | Sprint 5 backlog (lab 12, part A) |
| 1:20-1:30 | Break | None |
| 1:30-2:00 | Encounter numbers from your simulator: `D`, `u`, `H`, enrage and `D_min` | Numbers sheet (lab 12, part B) |
| 2:00-2:30 | Pull budget and pull plan; book the two pull sessions in everyone's calendar | Pull plan (lab 12, part C) |
| 2:30-3:00 | Practice: project the worked example's burn-down in the interactive, then set up your own burn-down log. Instructor walk-round | Burn-down log started |

## Deliverables

Due at the start of the week 13 studio meeting, in the team repository under `production/week12/`.

1. **Sprint 5 plan and burn-down log** (lab 12) that pass `check_burndown.py`, including the day-3 projection and any cut. Checked by rerunning the checker.
2. **Encounter numbers sheet** with `D`, `u`, `H`, `T_enrage`, the margin and `D_min`, and the simulator run it came from. Checked by recomputing `H` and `D_min`.
3. **Pull log**: one row per pull with build ID, question tested, outcome and deaths by ability. Checked against the encounter telemetry for two pulls.
4. **The encounter in the build**, meeting all five points of section 1. Checked live at the start of week 13 by a party of the instructor's choosing, including a wipe, a leash and a kill.
5. **Instance count for beta**: the maximum number of simultaneous encounter copies expected, handed to the week 13 load-test plan.

## Common failure modes

- **Tuning boss health from four people's pulls.** One evening of four players is too noisy to tune `H`. Set it from the simulator and use pulls for readability.
- **No leash, no wipe detection.** The boss follows the party into town, or never resets after a wipe. Test both on purpose in the first session.
- **Loot through a side door.** Awarding the drop with a direct inventory write instead of the transactional path from the economy sprint. This is how duplication bugs are born.
- **Reading the burn-down on Friday.** By then the cut is forced, and it falls on whatever is least finished rather than least needed.
- **Projecting from the best day.** Use the slower of the average and recent rates.
- **Cutting the telemetry.** It is invisible to testers and essential to the week 13 review.
- **Forgetting the instance cost.** Twelve copies of the encounter at beta is a load-test case, not a surprise.
- **Pulls without a question.** "Let's just try it" pulls produce opinions. Write the question for each pull before it starts.

## Review checklist

The instructor checks, at the week 13 meeting:

- [ ] The encounter needs a party, has one named coordination mechanic, and a solo player at party level loses.
- [ ] Boss health and enrage come from a simulator run, with the margin stated as a percentage of simulated DPS.
- [ ] Leash, wipe reset and mid-fight disconnect each have a recorded test.
- [ ] Loot goes to one player by a stated rule, through the transactional item path.
- [ ] Encounter telemetry records pull, wipe, kill and deaths by ability, and matches the pull log for two pulls.
- [ ] The burn-down log shows a day-3 projection by both rates, and a cut at least as large as the slower projection when it was positive.
- [ ] Cut items were marked non-minimum at planning, or the change is explained.
- [ ] The beta instance count has been passed to the load-test plan.

## Sources

- Final Fantasy XIV Online wiki (consolegameswiki), "Party" (accessed September 2026, current Final Fantasy XIV). Light party of four with one tank, one healer and two DPS; full party of eight with two, two and four; alliance of 24. https://ffxiv.consolegameswiki.com/wiki/Party
- MMO407 week 3 (this program) for the rule of three and its sources (Hanley and Lippman-Hand, 1983).
- MMO303 week 13 and MMO306 weeks 4, 5 and 7 (this program) for simulators, encounter mechanics, telegraphs and tuning, with their sources.
- The *Saltmarsh* team, the Drowned Warden, its damage figures, the burn-down, the pull times and the pull results are a constructed teaching example, not data from any real team.

## Interactive spec

File: `examples/w12-burndown-projection.html`.

**The one insight.** On day 3 of a five-day sprint, both projections already show the miss. A cut made on day 3 of the size the slower projection gives lands the sprint; the same shortfall found on day 5 cannot be cut, only failed.

**What is plotted.** One chart. x axis: sprint day 0 to 5, integer ticks labelled "Plan, Mon, Tue, Wed, Thu, Fri". y axis: remaining hours, 0 to `commit + total added + 2`.

- Ideal line: straight from `(0, commit)` to `(5, 0)`, dashed, neutral colour.
- Scope line: a step line showing `commit + cumulative added` per day, thin, neutral.
- Actual remaining: solid line with dots for days 0 to the current day.
- Average-rate projection: from the current day's remaining, slope `−r_avg`, dotted, to day 5.
- Recent-rate projection: same, slope `−r_recent`, dotted, second colour.
- After a cut: a vertical drop at the current day by the cut amount, then a solid projection at the slower rate. Colour the end hour green if it is at or below 0 and red otherwise.
- A shaded band between the two projections at day 5, labelled "projected left: a to b hours".

**Controls.**

- Commit (number, 5 to 40, default 14).
- Table of daily remaining (days 1 to 5) and added scope per day (0 by default), editable. Default rows: remaining 13, 13, 10, blank, blank; added 0, 2, 0, 0, 0.
- Current day (slider 1 to 4, default 3). Only days up to the current day are used.
- Cut (slider 0 to 10 in steps of 0.5, default 0).
- Button "Load worked example" to reset the defaults.

**Formulas.** With `R_d` the remaining at day `d`, `A` the cumulative added scope up to the current day `t`, and `C` the commit:

```
r_avg     = (C + A − R_t) / t
r_recent  = (R_{t−2} − R_t + added on days t−1 and t) / 2     (for t ≥ 2; for t = 1 use r_avg)
left_avg  = R_t − r_avg × (5 − t)
left_rec  = R_t − r_recent × (5 − t)
cut_needed = max(0, max(left_avg, left_rec))
after cut: left = R_t − cut − min(r_avg, r_recent) × (5 − t)
```

The number panel shows `r_avg`, `r_recent`, both projected-left values, `cut_needed`, and the margin after the cut.

**Test values.** With the defaults (`C = 14`, remaining 13, 13, 10, added 0, 2, 0, `t = 3`): `r_avg = 2.0`, `r_recent = 2.5`, `left_avg = 6.0`, `left_rec = 5.0`, `cut_needed = 6.0`. With cut 6.5, after-cut left is `10 − 6.5 − 2.0 × 2 = −0.5`, shown green with "margin 0.5 hours". With `t = 2` and no cut: `r_avg = (14 + 2 − 13) / 2 = 1.5`, `r_recent = (14 − 13 + 2) / 2 = 1.5`, `left = 13 − 1.5 × 3 = 8.5`.

**Accessibility.** Projection lines differ by dash pattern as well as colour. The number panel repeats every value shown on the chart. Works at 360 px wide with the table stacked under the chart.
