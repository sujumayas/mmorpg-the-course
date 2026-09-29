# PR401 · Week 13 — Vertical Slice Sprint 2

**Why this matters:** Next week the review panel plays your slice. If the server falls over in the first ten minutes, the panel learns nothing about your game and a great deal about your build. Most teams judge stability by feel ("it hasn't crashed in a while"). This week you put a number on how much stability evidence your playtests actually give you, find out why they say almost nothing about the server, and spend the sprint collecting the evidence the review needs.

**You will be able to:**
- Compute client and server exposure from a playtest log, counting player-hours and server-hours at load separately.
- Compute a 95% upper bound on a crash rate from zero or a few crashes, and the chance the review demo runs clean.
- Plan the soak testing needed to reach a target, and choose between collecting more evidence and making a failure cheaper.
- Prepare a tagged review build with a demo script and a fallback.

**Before class:** Bring your slice sprint 1 playtest log with, for every session, the start and end time, the number of players connected over time, and every client crash and server crash or restart. Bring your lab 12 time log. Reread [PR201 week 13, beta milestone](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w13-beta-milestone.md), section 3, on crash-free soak hours and the upper bound after `k` crashes (20 minutes). Skim [MMO302 week 11, load testing with bots](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md), section 1 (10 minutes).

**Prerequisites from earlier courses:** [MA102 week 13, sampling](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md) (the rule of three, `3/n` after zero events). [PR201 week 13, beta milestone](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w13-beta-milestone.md) (crashes as a Poisson process and the 95% upper bound `U(k)` after `k` crashes). [MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) (bot fleets, soak and stress tests). [PR101 week 10, bug tracking and QA basics](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md) (severity, priority, regressions). [PR101 week 13, builds and release checklists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md). [PR201 week 7, sizing the playtest](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w07-sprint-2-review-and-playtest.md) (finding problems, as opposed to measuring rates). [PR201 week 12, the polish budget](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w12-sprint-4-polish.md) (fix load before polish). From this course, [week 12](w12-vertical-slice-sprint-1.md) (the slice checklist and the *Emberfall* team). Looking ahead, [MMO407 week 3](../../MMO407-launch-scaling-and-post-mortems/lectures/w03-beta-strategies.md) (next semester) applies the same bound to bugs per player-hour in a public beta, and [MMO405 week 3, telemetry as research data](../../MMO405-research-methods-in-online-games/lectures/w03-telemetry-as-research-data.md) covers the unit problem, which is the exposure problem below.

---

## 1. What sprint 2 has to finish

Slice sprint 2 ends in a build the panel plays in week 14. By the end of the week:

- **Every item on the slice checklist from week 12 meets the quality bar.** Not most items. An item that can't meet the bar is cut from the slice and listed as cut, not shown half-done.
- **Every `build_now` tool from lab 12 exists and has made at least one slice unit.** That measures its per-unit cost `u_t`, which week 14 needs.
- **The build has stability evidence.** How many hours of play it has survived, of which kind, and what that says about the demo. That is this week's worked example.
- **The review build is tagged**, with a demo script and a fallback plan.

The sprint is short, and fixing always comes first. Before planning any new work, reserve fix hours the way PR201 week 12 showed, from your sprint 1 bug find rate and regression rate. On a capstone team in the last slice sprint, it is normal for half the programming hours to go to fixes.

## 2. Two kinds of crash, two kinds of exposure

An online game can fail in two places, and they fail differently.

- **A client crash** ends one player's session. The others keep playing. If your reconnect works, that player is back in a minute.
- **A server crash** ends everyone's session at once. In an MMO-scope game it can also lose recent progress for everyone if persistence was mid-write.

Each kind has its own **exposure**, the amount of running the evidence covers.

- **Client exposure** is **player-hours**: for each session, players connected times hours. Eight players for 1.5 hours is 12 player-hours. Each player's client is a separate chance to crash.
- **Server exposure** is **server-hours at load**: hours during which the server carried at least the load you care about. One server running for 1.5 hours with eight players is 1.5 server-hours at a load of eight, however many players there were.

This asymmetry is the whole problem. A class playtest piles up client exposure fast and server exposure slowly. Ten students for an hour is ten player-hours of client evidence and one server-hour. MMO405 week 3 (next semester) calls this the unit problem in telemetry: count the wrong unit and your sample looks ten times bigger than it is.

## 3. Worked example: will the slice survive the review?

### The hook

In 2019, before World of Warcraft Classic launched, Blizzard ran three public stress tests (22 to 23 May, 19 to 20 June and 25 to 26 July). Stress test realms capped characters at level 5, so thousands of players crowded into the same starting areas, and the announcement said the aim was to push the technology to its limit. CCP does something similar for EVE Online. It runs mass tests on its public test server, Singularity, and rewards the pilots who show up, often with millions of skill points to use on that server.

Why recruit a crowd for a few hours instead of running a small group of testers for weeks? Because a server fails under load, and the only way to get server-hours at load is to put the load on the server. A small group piles up player-hours. It doesn't pile up server-hours at launch-like concurrency. Your capstone has the same problem at a smaller scale.

### The model

For each kind of crash, with `k` crashes observed over exposure `E`:

```
λ̂      = k / E                         point estimate, crashes per hour
λ_up    = U(k) / E                      95% upper bound
          U(0) = 3.00, U(1) = 4.74, U(2) = 6.30, U(3) = 7.75
P(clean demo) = exp(−(N × λ_c + λ_s) × t)
```

- `E` is player-hours for client crashes and server-hours at load for server crashes.
- `U(k)` is the one-sided 95% upper limit of a Poisson count. `U(0) = 3.00` is the rule of three from MA102 week 13. `U(1)` to `U(3)` are the factors from PR201 week 13's soak planner. The lab script computes any `k`.
- `λ_c` and `λ_s` are the client and server crash rates per hour.
- `N` is the number of players in the demo and `t` its length in hours.
- `P(clean demo)` is the chance of no crash of either kind, treating crashes as random in time (a Poisson process). Use `λ_up` for the rates to get the pessimistic answer the panel should plan around.

### Numbers you can check

The *Emberfall* team ran four playtests in slice sprint 1.

| Session | Players | Hours | Player-hours | Server-hours at load 8 | Client crashes | Server crashes |
|---|---|---|---|---|---|---|
| 1 | 8 | 1.5 | 12 | 1.5 | 1 | 0 |
| 2 | 8 | 1.5 | 12 | 1.5 | 1 | 0 |
| 3 | 4 | 1.5 | 6 | 0 | 0 | 0 |
| 4 | 4 | 1.5 | 6 | 0 | 0 | 0 |
| **Total** | | **6** | **36** | **3** | **2** | **0** |

The review demo is two parties of four panel members, `N = 8`, for 30 minutes, `t = 0.5`.

| Estimate | Rate | Expected crashes in demo | Chance of none |
|---|---|---|---|
| Client, point `2 / 36` | 0.056 per player-hour | `8 × 0.056 × 0.5 = 0.22` | 0.80 |
| Client, upper `6.30 / 36` | 0.175 per player-hour | `8 × 0.175 × 0.5 = 0.70` | 0.50 |
| Server, point `0 / 3` | 0 per hour | 0 | 1.00 |
| Server, upper `3.00 / 3` | 1.0 per hour | `1.0 × 0.5 = 0.50` | 0.61 |
| Both, upper | | `0.70 + 0.50 = 1.20` | 0.30 |

Read the server rows. The team's feeling was "the server has never crashed", and the point estimate agrees, at zero. The honest statement is that three server-hours at load cannot rule out a crash rate of one per hour. At that rate the demo has a 39% chance of losing the server. Sessions 3 and 4 added 12 player-hours of client evidence and nothing at all for the server, because the server never carried the demo load.

Now plan the sprint. How much evidence would bring the server upper bound down to a level the team can live with? With zero crashes, `λ_up = 3 / T_s`, so:

| Server-hours at load, zero crashes | `λ_up` per hour | Chance the server survives the demo |
|---|---|---|
| 3 | 1.00 | 0.61 |
| 8 | 0.375 | 0.83 |
| 16 | 0.19 | 0.91 |
| 30 | 0.10 | 0.95 |

Sixteen hours at load gets the server to 91%. No class can supply sixteen hours of eight humans in a week. A bot fleet can. MMO302 week 11 showed how to script bots that log in, move, fight and trade. Two overnight soaks of 8 hours each with eight or more bots gives the 16 hours, if nothing crashes. If something does, you found a server bug before the panel did, which is the better result.

The client side is harder. With zero crashes on the fixed build, the client upper bound falls only as player-hours grow:

| Player-hours on the fixed build, zero crashes | `λ_up` per player-hour | Chance no client crashes in the demo |
|---|---|---|
| 36 | 0.083 | 0.72 |
| 100 | 0.030 | 0.89 |
| 200 | 0.015 | 0.94 |

A hundred player-hours in one week is eight people for twelve and a half hours. Bots don't help much here, because headless bots skip rendering, audio and input, which is where most client crashes live. So the *Emberfall* team takes the other route. They make a client crash cheap instead of rare. The client reconnects automatically and the server restores position, inventory and quest state within a minute. With that in place, a client crash in the demo is a blemish, not a failure, and the number that decides the demo is the server's. The team logs 36 more player-hours on the fixed build during sprint 2 playtests to check that the fixes held, and puts its effort into the bot soak.

One more rule. **A fix resets the evidence for what it touched.** The 36 player-hours that saw two crashes were on the old build. Once the crash bugs are fixed, the build is different, and so is its rate. Count exposure on the build you will demo.

### Cross-game recognition

**WoW Classic, rewritten.** Level cap 5 put thousands of players in the starting zones. In the model, that raised the load on exactly the servers that would be busiest at launch, so each stress-test hour was a server-hour at launch-like load. A test with players spread evenly would have logged many player-hours and few server-hours at the load that mattered.

**EVE Online mass tests.** The skill point rewards buy concurrency. CCP needs server-hours with hundreds of pilots in one system, which internal testers can't produce. It is the same trade your team makes with bots, with players standing in for bots because EVE's worst case is how real pilots behave in a fight.

**Crash-free metrics in live games.** Crash reporting services such as Firebase Crashlytics report crash-free users and crash-free sessions, one minus the share of users or sessions that crashed. Those are client-side ratios. They say nothing about a shared server. An online game needs a second, server-side measure beside them, and your two exposures are that split.

### Eyes-open design judgment

- **Say "at most", not "never".** "Zero server crashes in 3 hours" means the rate could be up to one an hour. Report the upper bound in the review, with its exposure.
- **Count the unit the failure lives in.** Player-hours for clients, server-hours at load for servers. More players in the room doesn't raise server evidence unless it raises the load.
- **Rare or cheap.** When the evidence for "rare" would take more hours than you have, spend the hours making the failure cheap: reconnects, autosave, a fast server restart. PR402's launch will face the same choice with much larger numbers (MMO407 week 3).
- **The bound assumes a steady rate.** A memory leak that crashes the server after six hours never shows in 30-minute sessions. Long soaks find what short sessions can't, so make at least one soak longer than the longest session you expect in PR402.

### Check this example

1. A team logs 5 server-hours at demo load with one server crash. What is the 95% upper bound on the server crash rate, and the pessimistic chance a 30-minute demo keeps its server?
2. The same team runs a clean 20-hour bot soak on the fixed build. What are the new bound and chance?
3. Ten players for an hour, and the server stays up. How much client exposure and how much server exposure did that give, at a demo load of eight?

<details>
<summary>Answers</summary>

1. `λ_up = 4.74 / 5 = 0.95` per hour. `exp(−0.95 × 0.5) = 0.62`.
2. The fix resets the evidence, so only the soak counts. `λ_up = 3 / 20 = 0.15`, `exp(−0.075) = 0.93`.
3. Ten player-hours of client exposure and one server-hour at load eight or more.

</details>

## 4. Preparing the review build

The panel plays a build, not your branch. Follow PR101 week 13's release checklist, with four additions for an online slice.

- **Freeze 48 hours before the review.** The review build is tagged then. After the tag, only fixes for crashes found in the soak go in, each reviewed by a second person and followed by a new short soak.
- **Demo script.** One page, timed: who logs in on which machine, the route the parties take, the moments that show each pillar, and what the team says during loading. The panel may go off-script. The script is for the team, so nobody improvises the setup.
- **Fallback.** A second server instance ready to start, a recorded run of the full slice in case the network fails, and a known way to restore the database to a clean state. Rehearse the restore once.
- **Stability statement.** A short table for the review: build tag, client player-hours and crashes, server-hours at load and crashes, upper bounds, and the pessimistic chance of a clean demo. Panels trust teams that show this more than teams that say "it's stable".

## 5. Measuring the tool and the slice units

Week 14 replans production from what the slice cost. Two things must be in the log by the end of this sprint.

- **Tool per-unit cost.** Every unit made with a `build_now` tool is logged with its hours, so `u_t` is measured. If the bounty tool's first bounty took 1.2 hours instead of the estimated 0.5, week 14 needs to know.
- **Slice units at the quality bar.** Each finished unit, with one-time and per-unit hours split as in week 12. For the town, week 14 uses the per-unit hours as the cost of the first unit, with production's towns as units 2, 3 and 4.

## Studio session plan

Week 13 meeting, 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Briefing: two exposures, upper bounds, rare or cheap | |
| 0:15-0:45 | Teams build the exposure table from the sprint 1 playtest log (lab 13, part A) | `sessions.csv` |
| 0:45-1:10 | Run `stability.py`; compute the demo's pessimistic chance; set the target | Stability report |
| 1:10-1:20 | Break | |
| 1:20-1:50 | Plan the evidence: bot soak schedule, reconnect or autosave work, the playtests on the fixed build; reserve fix hours | Sprint 2 plan |
| 1:50-2:20 | Supervised class soak: every team's slice with eight players from other teams for 25 minutes, logged | Session rows |
| 2:20-2:45 | Instructor round, 5 minutes per team, on the stability table and the fallback | Sign-off |
| 2:45-3:00 | Start the first overnight bot soak before leaving | Soak running |

## Deliverables

Due at the start of the week 14 meeting, in `preproduction/week13/`:

1. **Tagged review build**, with the build tag in `review-build.md` alongside the demo script and the fallback plan.
2. **Stability evidence** in the lab 13 format ([`labs/lab13.md`](../labs/lab13.md)): `sessions.csv` covering every playtest and soak on the tagged build, and the report from `stability.py`, which must print `PASS`, or `NOT READY` with the shortfall stated and a demo plan that allows for it.
3. **Updated time log** from lab 12 with every slice unit and every tool-made unit, tagged.

## Common failure modes

- **"It hasn't crashed."** Zero crashes over three hours is weak evidence. Report the bound.
- **Counting player-hours for the server.** A room full of players is one server.
- **Evidence from the old build.** Exposure before a fix doesn't count for the fixed build.
- **Short sessions only.** Leaks and slow corruption need long soaks.
- **Features in the last 48 hours.** Every late change is a regression chance with no soak behind it (PR101 week 10).
- **No fallback.** The one review where the network fails is the one where the recorded run saves the team.

## Review checklist

The instructor checks, at the start of the week 14 review:

- [ ] `stability.py` prints `PASS` on `sessions.csv` (or an honest `NOT READY` with a matching demo plan), and every row is on the tagged build or marked as older.
- [ ] Client and server exposure are counted separately, and server-hours are at the stated demo load.
- [ ] The stability statement reports upper bounds and the pessimistic chance of a clean demo.
- [ ] At least one soak is longer than the longest expected PR402 session.
- [ ] If client crashes are handled by reconnect, a logged test shows state restored.
- [ ] The build was tagged at least 48 hours before the review; later commits are crash fixes with a second reviewer.
- [ ] Demo script and fallback exist, and the database restore has been rehearsed.
- [ ] Every `build_now` tool has made at least one logged unit.

## Sources

- Blizzard Entertainment, "Mark Your Calendars: WoW Classic Launch and Testing Schedule" (World of Warcraft news, 14 May 2019), as cited in MMO302 week 11 of this program. Warcraft Wiki, "Stress test" (read September 2026): stress tests on 22 to 23 May, 19 to 20 June and 25 to 26 July 2019 (the third first scheduled for 18 to 19 July), level cap of five on stress-test realms.
- EVE University Wiki, "Singularity" (read September 2026). Singularity is CCP's public test server; CCP runs mass tests there, and participants are usually rewarded, often with millions of skill points for use on that server.
- Firebase, "Understand crash-free metrics" (Crashlytics documentation, read September 2026). Crash-free users and crash-free sessions defined as one minus the share of users or sessions with a crash.
- Hanley, J. A. & Lippman-Hand, A. (1983). "If nothing goes wrong, is everything all right? Interpreting zero numerators." *JAMA*, 249(13), 1743-1745. The rule of three, as used in MA102 week 13 and PR201 week 13.
- Wikipedia, "Poisson distribution", section "Confidence interval" (read September 2026). The exact interval from chi-squared quantiles, citing Garwood (1936); the one-sided 95% upper limits `U(k)` above are half the 0.95 chi-squared quantile with `2k + 2` degrees of freedom.
- The *Emberfall* sessions, crashes and soak plan are a constructed teaching example. They are not data from a real team.
