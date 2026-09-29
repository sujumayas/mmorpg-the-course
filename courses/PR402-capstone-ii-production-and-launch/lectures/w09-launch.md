# PR402 · Week 09 — Launch

**Why this matters:** This week your game goes public and stays public. Everything you have practised (sizing, rotas, kill switches, severity tables) now runs for real, and the first 48 hours set the reviews, the Discord mood and the retention curve you will be reading for the rest of the term. Launches rarely fail because a team did not work hard enough. They fail because a decision that should have been made on Monday with a spreadsheet gets made at 21:00 on Friday by whoever is still awake. This week you make those decisions in advance: go or no-go, how many shards, when to merge them, who does what, and what you tell players when something breaks.

**You will be able to:**
- Run a go or no-go review against criteria written before the review, with a named owner and evidence for each line.
- Forecast launch-day login demand from your open-beta actuals and their measured error.
- Choose a shard count that keeps the launch queue short without leaving the world empty a week later, and write the merge trigger in advance.
- Write a launch run sheet from T−24 hours to T+48 hours with roles, update times and a rollback plan.

**Before class:** Bring the open-beta exit review and the forecast-against-actual table from lab 8, the week 7 readiness checklist, the latest load-test report, and your PR401 social systems plan with its minimum population target. Re-read [MMO407 week 2](../../MMO407-launch-scaling-and-post-mortems/lectures/w02-capacity-planning-and-login-queues.md), sections 2 and 4 (25 minutes), and [MMO407 week 9](../../MMO407-launch-scaling-and-post-mortems/lectures/w09-communication-during-crises.md), section 2 (10 minutes).

**Prerequisites from earlier courses:** [MMO407 week 1, launch day anatomy](../../MMO407-launch-scaling-and-post-mortems/lectures/w01-launch-day-anatomy.md). [MMO407 week 2, capacity planning and login queues](../../MMO407-launch-scaling-and-post-mortems/lectures/w02-capacity-planning-and-login-queues.md) (the queue model this guide applies at capstone scale). [MMO407 week 9, communication during crises](../../MMO407-launch-scaling-and-post-mortems/lectures/w09-communication-during-crises.md). [MMO407 week 13, launch plan workshop](../../MMO407-launch-scaling-and-post-mortems/lectures/w13-launch-plan-workshop.md) (triggers decided in advance). [MMO302 week 2, shards, realms, zones, instances and layers](../../MMO302-mmo-server-architecture/lectures/w02-shards-realms-zones-instances-layers.md). [MMO302 week 9, login and gateway services](../../MMO302-mmo-server-architecture/lectures/w09-login-character-select-gateway-services.md). [MMO308 week 9, patch management and hotfixes](../../MMO308-live-operations-analytics-and-experimentation/lectures/w09-patch-management-and-hotfixes.md) (rollback). [MMO308 week 13, incident response](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md). [PR101 week 13, builds and release checklists](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md). From this course, the [week 8 guide](w08-open-beta.md).

**Interactive:** reuse MMO407's [launch queue model](../../MMO407-launch-scaling-and-post-mortems/examples/w02-launch-queue-hour-three.html) with your own caps and arrivals.

---

## 1. What launch means in this course

Launch is the moment your game becomes available to anyone, with no end date, on the platform your PR401 plan named (itch.io, a Steam playtest, your own site). From that moment, player progress is permanent unless you announce otherwise, and you are operating a service. The live-ops weeks that follow are graded on how you run it.

Treat launch as a process that lasts about 72 hours, not as a moment.

- **T−24 h**: go or no-go review; release candidate built and tagged; announcements scheduled.
- **T−2 h**: final smoke test on production, kill switches checked, rota starts.
- **T**: doors open.
- **T to T+6 h**: the login spike, the first incidents, the first status updates.
- **T+6 h to T+48 h**: the first evening peak, the first hotfix decision, the first day-1 retention number.

The build that launches is the one that passed the open-beta exit review, plus fixes. No new systems and no new content. Content lock from week 7 still holds.

## 2. Go or no-go

A go or no-go review is a meeting where each criterion, written before the meeting, gets a named owner, evidence and a pass or fail. It is not a vote on the team's mood. MMO407 week 13 argued for triggers decided in advance, because a team under a deadline will read ambiguous evidence as good news.

Useful criteria for a capstone launch:

| Criterion | Evidence | Owner |
|---|---|---|
| No open SEV1 or SEV2 bugs | Tracker query at T−24 h | QA lead |
| Crash rate below threshold per 100 player-hours | Open-beta final day, same build family | Tech lead |
| Load test passes at forecast peak × 1.5 | Test report on the release candidate | Server owner |
| Every kill switch drilled on production | Drill log from T−2 h | On-call primary |
| Rollback tested: previous build restored with data intact | Staging log | Server owner |
| Status page and announcement channel live, off the game's own servers | Link check | Community lead |
| Rota filled for the first 72 hours | Calendar | Producer |

A no-go does not have to mean "delay a week". Decide in advance what each failure means. A failed load test can mean "launch with a lower login cap". An open SEV2 in trading can mean "launch with trading switched off". A failed rollback test means no-go, because without it every later decision is riskier.

## 3. Forecasting launch demand

Your open beta gave you a forecast and an actual for every demand number. Use the ratio. If you forecast a peak of 78 CCU and saw 101, your method underestimates by a factor of 1.3; apply the same correction to the launch forecast until you have a reason not to.

Then build the arrival profile. For login planning you need the rate at which players try to log in, per minute, across the first hours. Launch arrivals typically come in three phases: a spike when the doors open and the announcement goes out, a shoulder over the next few hours as word spreads and time zones wake up, and a lower steady rate after. Estimate each phase from your open beta's first-wave logs, scaled by the ratio of launch audience to beta audience (mailing list, wishlists, followers).

## 4. Shards, caps and the merge trigger

MMO407 week 2 showed the launch trade-off at the scale of New World: more worlds shorten the queue on launch night and leave each world emptier a month later. The same trade-off applies to a student MMO with 100 players per shard. The model from MMO407 week 2, applied without re-deriving it:

```
while filling:  admissions per minute = min(arrivals, entry rate)
once full:      admissions per minute = cap / session length
queue grows while arrivals exceed admissions
wait at the back ≈ queue / admissions
```

The population side comes from your PR401 social systems plan: the peak concurrency at which one shard feels alive (groups form within a few minutes, the market has sellers, towns have people in them). Call it the **alive threshold**. A shard below it for a week loses players who came for other players.

Every extra shard at launch needs a **merge trigger**: a written, measurable condition under which you merge it back, and a merge you have tested on staging before launch. Without a tested merge, a second shard is a permanent decision disguised as a temporary one.

## 5. The run sheet, roles and messages

Write the launch as a run sheet, one line per step with a time, an owner and a check. Use MMO308 week 13's roles: an incident commander who does not debug, one person who touches production, one who writes to players. On a team of seven, give each role a primary and a backup for every four-hour block of the first 72 hours.

Prepare the messages before launch. MMO407 week 9 set the rules: acknowledge within 15 minutes, promise the time of the next update and keep that promise, never promise a fix time. Draft the templates now: queue is long, servers restarting, trading paused, known issues. At 21:00 on launch night, nobody writes a good paragraph from scratch.

The rollback plan is one line on the run sheet with a trigger: "If the crash rate exceeds X per 100 player-hours for 30 minutes after a deploy, revert to build N−1." MMO308 week 9 covered why you decide the trigger before the deploy.

## 6. Worked example: one shard or two on launch day?

### The hook

New World released on 28 September 2021 with over 700,000 concurrent players on Steam on the first day. Each server held 2,000 players, and queues on the most popular servers reached their 25,000-player limit. World of Warcraft Classic launched on 26 August 2019 with larger servers than the original game and temporary layering to spread the first crowd, and some servers still had extreme queues, so Blizzard created more servers in every region. Both teams faced the question you face this week, at a thousand times your scale: how much capacity to open for launch day when the population you need to keep lives a week later.

### The model

Apply MMO407 week 2's queue model per shard, with arrivals split evenly across shards, and then compare each shard's day-7 peak with the alive threshold.

```
per-shard arrivals  = total arrivals / shards
queue(t)            = arrivals so far − admissions so far
wait at the back    = queue / (cap / session length)
day-7 peak per shard = forecast day-7 total peak / shards
```

A plan passes if the worst wait at the back is under your wait limit and every shard's day-7 peak is at or above the alive threshold, or if a tested merge trigger restores the threshold before day 7.

### Numbers you can check

Emberfall, the seven-person team used as the running example in this course, is launching. Its release-candidate load test of one shard (two zone servers, as in week 8) put the shared knee at 143 CCU, a little above the open beta's 140 after the open-beta fixes. By week 8's model the shard knee is `min(2 × 80, 143) = 143`, so with 30% headroom the cap is `143 × 0.7 ≈ 100` per shard. A shard loads at most 10 characters a minute. Open-beta logs show launch-evening sessions of about 50 minutes, so a full shard frees `100 / 50 = 2` places a minute. After correcting with the open-beta error ratio, the forecast is 2.5 login attempts a minute in the first hour, 2.25 a minute in hours 1 to 3 (the evening crowd arriving after class and work), and 0.8 a minute after that. Attempts include relogs after disconnects, so they add up to more than the number of distinct players. Emberfall's PR401 plan sets the alive threshold at 40 CCU per shard and the wait limit at 15 minutes. The day-7 evening peak forecast is 60 CCU in total. All values are invented teaching values.

**One shard.**

- Minutes 0 to 40: arrivals of 2.5 a minute are below the entry rate of 10, so everyone gets in. The shard is full at minute 40 (`2.5 × 40 = 100`).
- Minutes 40 to 60: the queue grows by `2.5 − 2 = 0.5` a minute, reaching `0.5 × 20 = 10`.
- Minutes 60 to 180: arrivals drop to 2.25, which still exceeds 2. The queue grows by 0.25 a minute, to `10 + 30 = 40` at minute 180.
- After minute 180 it shrinks by `2 − 0.8 = 1.2` a minute and empties about 33 minutes later.

The wait at the back at minute 180 is `40 / 2 = 20` minutes, over the 15-minute limit. The first hour looks fine, and the worst wait comes at hour 3, the same shape MMO407 week 2 found for New World.

**Two shards.** Each receives 1.25 a minute, then 1.125, then 0.4. By minute 60 each holds 75 players, and each fills at about minute 82. From then on, arrivals of 1.125 a minute are below the 2 places a minute that finishing sessions free, so no real queue forms. The simulation's worst queue is under one player, a rounding effect of stepping whole minutes.

| Plan | Worst queue | Wait at the back | Day-7 peak per shard | Alive (≥ 40)? |
|---|---|---|---|---|
| 1 shard | 40 at minute 180 | 20 min | 60 | yes |
| 2 shards, permanent | under 1 | 0 min | 30 | no |
| 2 shards, merge when combined peak < 80 on two evenings | under 1 | 0 min | 60 after the merge | yes, from the merge |

Neither fixed plan meets both limits. The third row does, if the merge is real: the second shard exists to absorb launch day and is merged as soon as the combined evening peak would fit in one shard with 20 places to spare (`100 − 20 = 80`) on two evenings in a row. The merge must have run on staging before launch, with character data from the open beta, and players on shard 2 must be told on day 1 that it is temporary.

This simulation reproduces both launch-day cases.

```python
CAP, ENTRY, SESSION = 100, 10, 50   # players per shard, logins loaded per minute, session length (min)

def arrivals(t):
    """Login attempts per minute across the whole game, t minutes after the doors open."""
    return 2.5 if t < 60 else 2.25 if t < 180 else 0.8

def launch_day(shards, minutes=480):
    online = queue = 0.0
    worst = (0, 0.0)
    for t in range(minutes):
        queue += arrivals(t) / shards
        if online < CAP:                          # filling: limited by the entry rate
            admit = min(queue, ENTRY, CAP - online)
        else:                                     # full: a place frees as a session ends
            admit = min(queue, CAP / SESSION)
        online = min(CAP, online + admit)
        queue -= admit
        if queue > worst[1]:
            worst = (t + 1, queue)
    return worst

for s in (1, 2):
    minute, q = launch_day(s)
    print(f"{s} shard(s): worst queue {q:.1f} at minute {minute}, "
          f"wait at back {q / (CAP / SESSION):.0f} min, day-7 peak per shard {60 / s:.0f}")
```

It prints:

```
1 shard(s): worst queue 40.0 at minute 180, wait at back 20 min, day-7 peak per shard 60
2 shard(s): worst queue 0.9 at minute 83, wait at back 0 min, day-7 peak per shard 30
```

### Move it yourself

Open MMO407's [launch queue model](../../MMO407-launch-scaling-and-post-mortems/examples/w02-launch-queue-hour-three.html) and enter one shard with a cap of 100, an entry rate of 10 and a 50-minute session, with the arrival phases above. Watch the queue keep growing after the spike has passed. Then set the cap to 200, which approximates two shards, and see the queue collapse. The population cost does not show on that chart. Write it next to it.

### Cross-game recognition

The launch-then-merge pattern is the small-scale version of what MMO407 week 2 called layering: WoW Classic ran temporary layers and New World offered transfers off full worlds. MMO302 week 2 described the cost of layers to players, friends split across copies. At your scale, a temporary second shard is the same tool, with the same cost, and the same need to switch it off on a date or a trigger rather than when someone remembers.

### Eyes-open design judgment

A queue is not only a cost. A visible queue tells players the game is popular, and a short one on launch evening can be acceptable. A 20-minute wait at hour 3, when friends of the first players are arriving, is not: many players close the client and do not return (MMO407 week 1 on launch funnels). On the other side, an empty shard is quieter and worse, because players who leave an empty world rarely post about it. Also weigh what the merge costs your team: name collisions, guild membership, housing plots, auction listings. If your game has any of these, the merge needs rules you publish before launch. If you cannot build a safe merge in time, a single shard with a hard cap and an honest queue message is a defensible choice. Write down which risk you are taking.

### Check yourself

1. The open beta's error ratio suggests launch arrivals will be 20% higher than the forecast in every phase. Does one shard still empty its queue by the end of the day? What is its worst wait?
2. With two shards, what is the smallest alive threshold at which the permanent two-shard plan would pass?
3. On day 3 the combined evening peak is 76, then 83, then 74. Under the stated trigger, when do you merge?

## Studio session plan

The studio meeting runs 180 minutes with one break. It takes place about 24 hours before the doors open.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:10 | Instructor briefing: go or no-go rules, shard decision, run sheet | — |
| 0:10-0:50 | Go or no-go review: each criterion presented by its owner with evidence | Signed go or no-go record |
| 0:50-1:25 | Launch forecast and shard decision (lab 9, parts A and B) | Shard plan with merge trigger |
| 1:25-1:35 | Break | — |
| 1:35-2:10 | Write the run sheet from T−24 h to T+48 h, with owners and checks | Run sheet |
| 2:10-2:35 | Draft message templates; check the status channel from off-network | Templates, link check |
| 2:35-3:00 | Rollback drill on staging, timed; instructor walk-round | Drill log, final sign-off |

## Deliverables

Due at the week 10 studio meeting, in `production/week09/`.

1. **Go or no-go record**: criteria, owners, evidence links, results, the decision and its time. Checked against the commit history (criteria written before the review).
2. **Launch capacity plan** (lab 9): forecast with its correction, the shard plan, queue and population figures, the merge trigger. Checked by recomputing one plan's worst queue.
3. **Run sheet as run**: each step with its actual time and any deviation.
4. **Incident and message log** for the first 48 hours: every incident with severity and times, every player-facing message with its time and the promised next-update time.
5. **First numbers**: peak CCU, worst queue observed, crash rate per 100 player-hours, and day-1 retention of the launch cohort (accounts created on launch day who return the next day).

## Common failure modes

- **Criteria written during the review.** A criterion written after seeing the evidence always passes.
- **Treating no-go as all or nothing.** Decide in advance which failures mean a lower cap or a switched-off feature, and which mean delay.
- **Launch forecast from the pitch deck.** Use the open-beta actuals and their error, not the number that made the pitch look good.
- **A temporary shard with no merge.** Without a tested merge and a written trigger, it stays, and both shards die slowly.
- **Status updates on the game's own servers.** When the server is down, so is your explanation.
- **Promising fix times.** Promise the next update time instead.
- **The whole team awake at T+20 hours.** The rota exists so that the person who makes the 03:00 decision slept.

## Review checklist

The instructor checks, at the week 10 meeting:

- [ ] Go or no-go criteria were committed before the review, and each has evidence and an owner.
- [ ] The launch forecast applies a correction from the open-beta forecast-against-actual table.
- [ ] The shard plan shows worst queue, wait at the back and day-7 peak per shard, with correct arithmetic for at least one plan.
- [ ] Any temporary shard has a written merge trigger and a staging merge log from before launch.
- [ ] The run sheet has owners and checks, and the as-run version records deviations.
- [ ] The first player-facing message after each incident went out within 15 minutes, and every promised update time was kept or its miss explained.
- [ ] A rollback was drilled before launch, with its time recorded.
- [ ] Day-1 retention of the launch cohort is reported with its `n`.

## Sources

- Wikipedia, "New World (video game)" (read September 2026; "New World: Aeternum" redirects there). Global release on 28 September 2021; over 700,000 concurrent players recorded on Steam on release day; 2,000 players per server; queues on the most popular servers reaching the 25,000-person limit.
- Warcraft Wiki, "World of Warcraft: Classic" (read September 2026). Global launch on 26 August 2019 (Pacific time, so 27 August in Europe); larger server sizes than the original and temporary layering; extreme login queues and rapid creation of additional servers in all regions.
- MMO407 week 2 (this program) for the cumulative-curve queue model and the launch-night against day-30 trade-off, with its sources.
- All caps, rates, session lengths, thresholds and forecasts in sections 3 to 6 are invented teaching values.
