# PR402 · Week 10 — Live-Ops Week 1

**Why this matters:** Your game has been live for a few days. The launch spike is over, and now the work changes shape. Bugs arrive from players you will never meet, the first cohort's retention number lands every morning, and every fix competes for the same few hours with every other fix. A team that treats this week as "keep fixing until it's quiet" burns out by week 12 and ships its worst patches when it is most tired. This week you set up the routine that will run the game for the rest of the term: a daily review, a triage rule written in player-hours, an on-call load the team can sustain, and a hotfix decision you can defend.

**You will be able to:**
- Run a 30-minute daily live review from a fixed dashboard: health, the first cohort, the bug queue and the economy.
- Report day-1 and day-3 retention for the launch cohort with an interval, and say what the number can and cannot tell you yet.
- Triage live issues by severity first, then by harm avoided per developer-hour, and decide which go into a hotfix and which wait for the scheduled patch.
- Size the team's weekly fix capacity from the rota, net of incident follow-up, and keep on-call load within a sustainable limit.
- Close the loop with players through a known-issues post and patch notes.

**Before class:** Bring the lab 9 first-48-hours numbers, your live dashboard, the bug tracker export since launch, the incident log, and the rota for the coming week. Re-read [MMO308 week 9](../../MMO308-live-operations-analytics-and-experimentation/lectures/w09-patch-management-and-hotfixes.md), section 3, on hotfix now or wait (10 minutes), and [MMO308 week 13](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md), sections 3 and 4 (20 minutes).

**Prerequisites from earlier courses:** [MMO308 week 1, what live ops is](../../MMO308-live-operations-analytics-and-experimentation/lectures/w01-what-live-ops-is.md). [MMO308 week 2, KPIs](../../MMO308-live-operations-analytics-and-experimentation/lectures/w02-kpis-dau-mau-stickiness-arpdau.md). [MMO308 week 3, cohorts and retention curves](../../MMO308-live-operations-analytics-and-experimentation/lectures/w03-cohorts-and-retention-curves.md). [MMO308 week 9, patch management and hotfixes](../../MMO308-live-operations-analytics-and-experimentation/lectures/w09-patch-management-and-hotfixes.md) (the hotfix cost model this guide applies). [MMO308 week 10, player feedback loops](../../MMO308-live-operations-analytics-and-experimentation/lectures/w10-player-feedback-loops-forums-surveys-polls.md). [MMO308 week 12, economy monitoring](../../MMO308-live-operations-analytics-and-experimentation/lectures/w12-economy-monitoring.md). [MMO308 week 13, incident response](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md). [MMO309 week 11, exploit response: rollback against ban](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w11-exploit-response-rollback-vs-ban.md). [MMO302 week 14, observability](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md). [PR101 week 12, crunch: causes, costs and alternatives](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w12-crunch-causes-costs-alternatives.md). [MMO303 week 14, communicating balance changes](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w14-communicating-balance-changes.md). From this course, the [week 9 guide](w09-launch.md).

---

## 1. The shape of a live week

A live week has a fixed rhythm, and the rhythm is what keeps a small team from reacting to every message as an emergency. Set it now and keep it until the course ends.

- **Daily live review, 30 minutes, same time every day.** One person drives the dashboard; everyone on the week's rota attends. Section 2 lists what is on it.
- **Triage straight after the review.** New issues get a severity and, if they are not SEV1, a place in the ranked queue (section 4).
- **Fix windows.** Work on the queue happens in scheduled blocks, not whenever someone feels guilty.
- **One scheduled patch per week.** Pick a day and publish it, for example Thursday at 18:00. Players plan around a known patch day; MMO308 week 9 covered why a predictable cadence costs less than ad hoc deploys.
- **Hotfixes only by the rule.** A hotfix outside patch day happens when section 4's calculation says so, or when the severity table says SEV1.
- **Weekly retro, 30 minutes, after the patch.** What broke, what the numbers did, what changes in the routine.

Everything that is not on this schedule is an interruption, and the rota decides who absorbs it.

## 2. The daily dashboard

Keep it to one screen. If the review takes longer than 30 minutes, the dashboard has too much on it.

| Panel | What you read | Where it comes from |
|---|---|---|
| Health | Peak CCU, p99 tick time at peak, crashes and disconnects per 100 player-hours | MMO302 week 14 |
| First cohort | Launch-day accounts: day-1, day-3, day-7 return, each with `n` | MMO308 week 3 |
| New players | Tutorial funnel for accounts created yesterday | MMO308 week 4 |
| Bug queue | New, fixed, open by severity; oldest open SEV2 | PR101 week 10 |
| Economy | Faucet and sink totals per player-hour against the week 8 baseline; any alarm | MMO308 week 12 |
| Incidents | Open incidents, time to mitigate for any closed since yesterday | MMO308 week 13 |

Read retention with the same care as any small-sample rate. A launch cohort of 260 accounts is large for a capstone and small for a statistic. Report it with a Wilson interval (PR201 week 11), and compare it with the target in your PR401 plan only when the interval is clear of the target. Day-7 retention cannot exist until day 7, so do not let the team read meaning into day-3 swings of a few points.

## 3. On-call load you can sustain

Google's *Site Reliability Engineering* book (2016) sets limits that are a useful starting point even for a team of seven students. It caps on-call at no more than 25% of an engineer's time. It aims for at most two incidents per 12-hour on-call shift, because it finds that each incident takes about six hours of follow-up (root cause, fix, postmortem) on average. Those numbers come from a large company's service teams, not from games or students. What transfers is the principle: incidents cost far more time than the minutes spent fighting them, and a rota that ignores the follow-up will run out of hours by midweek.

Compute your week's fix capacity from the rota, not from goodwill.

```
fix capacity = people on the fix rota × fix hours per person per day × days
             − expected incidents × 6 hours of follow-up
```

Take the expected incident count from the launch weekend's log. Keep each person's on-call blocks within the limits your team agreed in week 8. If the capacity is smaller than the queue, the queue waits; section 4 decides which part.

## 4. Triage in player-hours

Triage in a live game has two stages, and the order matters.

**Stage 1: the severity rule.** Give every issue its level with the mapping from [week 4](w04-alpha-review-and-bug-triage.md), section 2. SEV1 issues bypass the queue. MMO308 week 13 put economy integrity at SEV1 even when servers are healthy, because a duplication exploit grows every minute it runs. Flip the kill switch first, then fix. MMO309 week 11 covers what to do with the items and accounts afterwards.

**Stage 2: harm per developer-hour.** For everything else, MMO308 week 9 gave the hotfix model in player-hours.

```
wait cost   = h × T           h = harm per hour (player-hours), T = hours to the scheduled patch
hotfix cost = D + r × H       D = restart disruption, r = chance the hotfix breaks something, H = harm if it does
```

This is the [week 4](w04-alpha-review-and-bug-triage.md) ranking (impact per fix hour, with gate bugs first) in a unit you can now measure. Before launch you weighted sessions by severity because you had no live harm data. Now telemetry gives harm in player-hours directly, and week 4's gate bugs (data loss, value-path exploits) are SEV1 here.

Two refinements matter at student scale. First, a hotfix bundles several fixes into one restart, so `D` is paid once per hotfix, not once per fix. The per-issue question becomes "is `h` above the break-even rate `(D + r × H) / T`?" Second, developer-hours are the real limit. Rank issues that clear break-even by `h × T / fix hours`, the harm avoided per hour of work, and fill the fix capacity from the top.

Estimate `h` from telemetry wherever you can. "Players who hit it per hour × time each loses" is usually enough. When you cannot measure it, write your estimate and its basis; the retro checks it next week.

## 5. Talking to players in week 1

The launch messages from week 9 now become a routine.

- **Known-issues post**, pinned, updated after each daily review. Each line says what players see, whether there is a workaround, and whether the fix is in the next hotfix or on patch day. Players who see their bug listed stop reporting it and start waiting for it.
- **Patch notes** for every hotfix and patch, written for players. MMO303 week 14 covered how to write balance lines so players can tell a buff from a nerf. The Hexer change from week 6 belongs in your launch notes if it shipped.
- **Closing the loop.** When a player-reported bug is fixed, say so where they reported it. MMO308 week 10 showed why players who see their reports acted on keep reporting.

## 6. Worked example: what goes into Tuesday's hotfix?

### The hook

The SRE book's limits (on-call at most 25% of time, at most two incidents per 12-hour shift, about six hours of follow-up per incident) exist because service teams kept running out of time for anything but incidents. A capstone team is the same problem at a smaller size. Seven students, a live game, a patch day on Thursday, and a queue that grows faster on Monday than it shrinks. The question every live team answers on its first Tuesday is which of today's issues are worth a restart now, and which of them fit in the hours the team actually has.

### The model

```
break-even harm   h* = (D + r × H) / T
fix capacity         = rota hours − expected incidents × 6
rank                 = h × T / fix hours, for issues with h ≥ h*
hotfix               = SEV1 fixes first, then ranked issues until capacity runs out
```

### Numbers you can check

It is Tuesday morning of week 10 for Emberfall, the seven-person team used as the running example in this course ([week 11](w11-live-ops-week-2-operating-rhythm.md) reviews its whole week). The scheduled patch is Thursday, `T = 48` hours away. A hotfix needs a 5-minute restart with about 40 players online on average, so `D = 40 × 5 / 60 = 3.3` player-hours. The team judges a 15% chance that a rushed hotfix breaks something costing about 30 player-hours, so `r × H = 4.5`. Four of the seven students are on the fix rota for two days at three fix hours each, 24 hours, and the launch weekend suggests one incident in those two days, costing 6 hours of follow-up. All values are invented teaching values.

```
hotfix cost   = 3.3 + 4.5         = 7.8 player-hours
break-even h* = 7.8 / 48          = 0.16 player-hours per hour
fix capacity  = 3 × 4 × 2 − 1 × 6 = 18 developer-hours
```

The queue after the daily review:

| Issue | Severity | Basis for `h` | `h` (ph per hour) | Fix hours |
|---|---|---|---|---|
| A: crafting duplicates items | SEV1 | economy integrity | not ranked | 0.5 switch + 4 trace and roll back |
| B: first town bounty does not complete, blocks progress | SEV2 | 6 new players an hour × 22% hit it × 0.5 h lost | 0.66 | 3 |
| C: crash when accepting a guild invite | SEV2 | 1 crash an hour at 40 CCU × 0.25 h lost | 0.25 | 6 |
| D: 40-second login delay for accounts with 5+ characters | SEV3 | 27 logins an hour × 40 s | 0.30 | 5 |
| E: wrong stat in an item tooltip | SEV3 | estimate | 0.02 | 1 |

Issue A goes first by the severity rule. The on-call engineer switches off crafting (0.5 hours), and two people spend 4 hours tracing the duplicated items and rolling them back (MMO309 week 11). The code fix itself is not urgent once the switch holds, so it waits for the week 12 patch, where it appears as a 4-hour candidate. That leaves `18 − 4.5 = 13.5` hours. Now rank the rest.

| Issue | `h × T` saved | Per fix hour | Decision | Hours left |
|---|---|---|---|---|
| B | 31.7 | 10.56 | hotfix | 10.5 |
| D | 14.4 | 2.88 | hotfix | 5.5 |
| C | 12.0 | 2.00 | Thursday: no capacity | 5.5 |
| E | 1.0 | 0.96 | Thursday: below break-even | 5.5 |

Check issue B by hand: `0.66 × 48 = 31.7` player-hours avoided, for 3 hours of work, 10.56 per hour. Issue E's harm of 0.02 per hour is below the break-even of 0.16, so it would not justify a restart on its own; it rides Thursday's patch. Issue C is worth hotfixing in principle, but at 6 hours it does not fit the 5.5 hours left. It waits two days, which costs 12 player-hours, and goes on the known-issues post with the workaround ("decline and re-send the invite from the guild panel").

The Tuesday hotfix bundles B and D. It avoids `31.7 + 14.4 = 46.1` player-hours of harm for one restart costing 7.8. Crafting stays switched off, and the known-issues post says so. The remaining 5.5 hours go to a regression test for the dupe and to the support queue, which week 11 shows was already backing up.

This script reproduces the decisions.

```python
T = 48                       # hours until Thursday's scheduled patch
D = 40 * 5 / 60              # restart disruption: 40 players online, 5 minutes
RISK = 0.15 * 30             # 15% chance of a problem costing 30 player-hours
breakeven = (D + RISK) / T
print(f"hotfix cost {D + RISK:.1f} player-hours, break-even harm {breakeven:.2f} per hour")

hours = 3 * 4 * 2 - 1 * 6    # rota fix hours minus one incident's follow-up
left = hours - 4.5           # SEV1 dupe goes first: switch 0.5 h + trace and roll back 4 h
print(f"fix capacity {hours} dev-hours, {left} left after the dupe fix")

issues = [  # name, harm per hour (player-hours), fix hours
    ("B quest blocker", 0.66, 3),
    ("C guild-invite crash", 0.25, 6),
    ("D slow login", 0.30, 5),
    ("E wrong tooltip", 0.02, 1),
]
for name, h, dev in sorted(issues, key=lambda i: -i[1] * T / i[2]):
    if h < breakeven:
        where = "Thursday (below break-even)"
    elif dev <= left:
        left -= dev
        where = "hotfix"
    else:
        where = "Thursday (no capacity)"
    print(f"{name:21} saves {h * T:4.1f} ph, {h * T / dev:5.2f} per dev-hour -> {where}, {left} h left")
```

It prints:

```
hotfix cost 7.8 player-hours, break-even harm 0.16 per hour
fix capacity 18 dev-hours, 13.5 left after the dupe fix
B quest blocker       saves 31.7 ph, 10.56 per dev-hour -> hotfix, 10.5 h left
D slow login          saves 14.4 ph,  2.88 per dev-hour -> hotfix, 5.5 h left
C guild-invite crash  saves 12.0 ph,  2.00 per dev-hour -> Thursday (no capacity), 5.5 h left
E wrong tooltip       saves  1.0 ph,  0.96 per dev-hour -> Thursday (below break-even), 5.5 h left
```

The same morning's dashboard shows the launch cohort: 260 accounts created on launch day, 99 of them returned on day 1. That is 38.1%, with a Wilson 95% interval of 32.4% to 44.1%. If the PR401 target was 35%, the interval includes it, so the honest report is "consistent with target, not yet above it". The first-bounty blocker (issue B) sits in the first hour of play, which is one reason to expect day-3 retention of the next cohort to move after the hotfix.

### Move it yourself

Open PR101's [bug backlog model](../../PR101-game-production-i-teams-scope-and-the-game-jam/examples/w10-bug-backlog.html) and set the arrival rate to your team's new bugs per day since launch and the fix rate to your fix capacity divided by your mean fix hours. If the backlog grows, the ranking above is not optional: some issues will wait, and the only choice is which ones.

### Cross-game recognition

The break-even rule is MMO308 week 9's hotfix model with one change: shared restart cost across a bundle. MMO308 week 9 also noted that server-side hotfixes that need no restart drop `D` to zero and lower the break-even, which is why live teams invest in them. The severity-first rule is MMO308 week 13's table and MMO309 week 11's exploit logic. The capacity line is PR101 week 10's backlog model: if arrivals beat fixes, the queue grows no matter how you rank it.

### Eyes-open design judgment

The numbers in the `h` column are estimates, some of them rough. That is fine as long as they are written down, because the retro can check them against what happened after the fix. A ranking that nobody wrote down cannot be checked and will repeat its mistakes. Two judgment calls sit outside the arithmetic. First, some harms do not fit in player-hours: a bug that makes one group of players feel targeted, or a crash that hits streamers on camera. Raise their priority deliberately and write why. Second, the cheapest way to find capacity is to stop doing something. If issue C matters more than the team's planned week 11 content, move the content, not the rota.

### Check yourself

1. The team adds a restart-free hotfix path, so `D = 0`. What is the new break-even harm, and does issue E now qualify?
2. Two incidents happen on Tuesday instead of one. Recompute fix capacity. Which of B and D still make the hotfix?
3. Day-3 retention for the launch cohort is 65 of 260. Compute the rate and say, without an interval calculation, whether you could distinguish it from 25% with this `n`. Then check with the Wilson interval.

## Studio session plan

The studio meeting runs 180 minutes with one break. The game is live throughout; the on-call primary keeps the dashboard open and may leave the room.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:10 | Instructor briefing: live rhythm, triage stages, capacity | — |
| 0:10-0:40 | Run a real daily review from your dashboard, timed, with the instructor watching | Review notes; dashboard gaps listed |
| 0:40-1:20 | Triage the live queue (lab 10): severity, `h` with basis, fix hours, break-even, ranking | Ranked queue and hotfix decision |
| 1:20-1:30 | Break | — |
| 1:30-2:00 | Compute this week's fix capacity from the rota; check on-call limits | Capacity line and rota for the week |
| 2:00-2:30 | Write or update the known-issues post and the draft patch notes for patch day | Posts ready to publish |
| 2:30-3:00 | Instructor walk-round: each team defends one "wait" decision | Sign-off |

## Deliverables

Due before the week 11 studio meeting, in `production/week10/`.

1. **Daily review log**: one entry per day since the last meeting, with the dashboard values and the decisions taken. Checked against the dashboard's history for one day.
2. **Triage sheet** (lab 10): every live issue with severity, `h` and its basis, fix hours, break-even, rank and decision. Checked by recomputing the break-even and one rank.
3. **Hotfix and patch records**: for each deploy, the build number, the issues it closed, the restart time and whether anything regressed.
4. **Rota and capacity** for weeks 10 and 11, with on-call hours per person.
5. **Player-facing posts**: the known-issues post history and the patch notes.
6. **Retention report**: launch cohort day-1, day-3 and day-7 with `n` and Wilson intervals.

## Common failure modes

- **Fixing in arrival order.** The loudest or newest issue is not the most harmful. Rank.
- **One restart per fix.** Bundle fixes into one hotfix; the restart cost is shared.
- **Hotfixing everything above break-even.** Break-even is necessary, not sufficient. Capacity decides.
- **Ignoring the follow-up.** An incident fought in 20 minutes still costs hours of root cause and postmortem.
- **The same two people on call every night.** The rota exists so the whole team shares the load and nobody crunches (PR101 week 12).
- **Reading day-3 noise as a trend.** Report intervals; wait for day 7 and a second cohort.
- **A known-issues post that goes stale.** Update it after every daily review, or players stop trusting it.
- **Leaving a kill switch on with no plan.** A disabled crafting system is a mitigation, not a fix. Put the re-enable step on the run sheet.

## Review checklist

The instructor checks, at the week 11 meeting:

- [ ] A daily review ran every day with a log entry, and took 30 minutes or less.
- [ ] Every SEV1 was mitigated first by a switch or a revert, with times recorded.
- [ ] The triage sheet states `h` with a basis for every issue, and the break-even and one rank recompute correctly.
- [ ] Hotfixes bundled fixes, and each one's decision follows from the sheet.
- [ ] Fix capacity was computed from the rota net of incident follow-up, and no one exceeded the team's agreed on-call limit.
- [ ] The known-issues post was updated daily, and closed issues were announced where they were reported.
- [ ] Retention is reported with `n` and intervals, and the report does not claim a trend the intervals cannot support.

## Sources

- Beyer, B., Jones, C., Petoff, J. and Murphy, N. R. (eds.) (2016). *Site Reliability Engineering: How Google Runs Production Systems*. O'Reilly. Chapter 11, "Being On-Call" (read at sre.google, September 2026): no more than 25% of SRE time on-call; about six hours of follow-up per incident, including postmortem; a maximum of two incidents per 12-hour on-call shift.
- Wilson, E. B. (1927). "Probable inference, the law of succession, and statistical inference." *Journal of the American Statistical Association* 22(158), 209-212. The interval used for retention, as taught in MA102 week 13.
- MMO308 weeks 9 and 13 (this program) for the hotfix cost model and the severity table, with their sources.
- All issues, harm rates, restart times, rota hours and cohort counts in section 6 are invented teaching values.
