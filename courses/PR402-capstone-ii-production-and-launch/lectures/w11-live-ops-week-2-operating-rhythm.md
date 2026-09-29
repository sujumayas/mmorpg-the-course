# PR402 · Week 11 — Live-ops Week 2: From Firefighting to an Operating Rhythm

**Why this matters:** Your game has been live for two weeks, and last week probably felt like one long emergency. That feeling has a number behind it. If crashes, tickets and restarts ate more than half of your team's hours, you cannot build the patch due in week 12, and the emergency will not end on its own. This week you measure how much of the week live operations takes, buy some of it back, and set up a rhythm the team can keep until the showcase.

**You will be able to:**
- Compute your team's interrupt fraction from a week-10 time log and the planned hours it leaves for patch work.
- Apply Little's law to your support queue to get the average time a player waits for an answer, and the queue length that meets a wait target.
- Rank one-off fixes by how many weekly interrupt hours they remove, and compute their payback time.
- Set up an on-call rota, a daily triage slot and a weekly live review that the team can run with the hours it has.

**Before class:** Export your week-10 time log (every entry tagged planned or interrupt) and your support tickets with open and close times. Read MMO308 week 1, section 1, on what live ops is (15 minutes), and MMO308 week 13, section 4, on running an incident response (15 minutes). Read *Site Reliability Engineering* (Beyer et al., 2016), chapter 5, "Eliminating Toil", free at sre.google (20 minutes). Bring the week-10 incident log.

**Prerequisites from earlier courses:** [MMO308 week 1, what live ops is](../../MMO308-live-operations-analytics-and-experimentation/lectures/w01-what-live-ops-is.md) (the live team's jobs). [MMO308 week 3, cohorts and retention curves](../../MMO308-live-operations-analytics-and-experimentation/lectures/w03-cohorts-and-retention-curves.md) (reading your launch cohort, section 4 below). [MMO308 week 8, event design and calendars](../../MMO308-live-operations-analytics-and-experimentation/lectures/w08-event-design-and-calendars.md) (whether to run a first event). [MMO308 week 13, incident response](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md) (severity levels, revert first, the incident postmortem). [MMO407 week 9, communication during crises](../../MMO407-launch-scaling-and-post-mortems/lectures/w09-communication-during-crises.md) (what you tell players during an outage). [PR101 week 10, bug tracking and QA basics](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w10-bug-tracking-and-qa-basics.md) (the open-bug stock model, which the support queue resembles). [MMO302 week 9, login and gateway services](../../MMO302-mmo-server-architecture/lectures/w09-login-character-select-gateway-services.md) (Little's law applied to a login queue). From this course, [week 1, the ops tax](w01-production-sprint-1-the-ops-tax.md) (the planned share `t` of each week lost to ops, which this week measures after launch), [week 9, launch](w09-launch.md) and [week 10, live-ops week 1](w10-live-ops-week-1.md) (the fix rota, on-call limits and triage in player-hours).

**Interactive:** [Live capacity: interrupts and the support queue](../examples/w11-live-capacity.html)

---

## 1. Launch mode and operating mode

A team runs in **launch mode** when every person drops planned work the moment something breaks. That is correct for the first days after launch. Players are arriving, you know little about how the servers behave under real load, and a crash left alone for an hour costs you players you will never see again (MMO407 week 10).

Launch mode does not scale past a week or two. Everyone is on call all the time, so nobody finishes anything. Planned work slips, and the patch that would remove the crashes never ships. The team ends up working longer hours to stand still, which PR101 week 12 calls the start of crunch.

**Operating mode** replaces "everyone reacts" with a small set of rules. One person is on call at a time. Player tickets are triaged once a day at a fixed time. The team reviews the live numbers once a week and decides what goes into the next patch. Everyone else works on planned tasks. The switch is not a mood. It happens when you can show, from your own log, that the interrupt load fits inside a budget.

## 2. Interrupts, toil and the time log

An **interrupt** is any hour spent on work nobody planned at the start of the week: restarting a crashed zone server, answering a ticket, investigating a report of harassment, rolling back a bad deploy. The SRE book calls the repetitive, manual part of this **toil**. It is work that scales with the number of players or incidents and leaves nothing permanent behind.

To manage it you need three numbers from the week-10 log.

```
C = team hours available in the week
I = hours logged as interrupts
i = I / C              the interrupt fraction
P = C − I              hours left for planned work
```

The interrupt fraction `i` is the same quantity as the ops tax `t` you planned in week 1 and measured at every sprint review since. What changes after launch is its size. Week 1 planned for a tax of a few tenths. Live games can take more than half. Week 10 sized the fix rota from the incident log; this week puts every kind of interrupt in one budget.

Tag each log entry with one category. Five cover most student teams: incidents and hotfixes, player support, moderation, monitoring (checking dashboards by hand), and deploys and restarts. Keep the categories stable from week to week so the trend means something.

The log has to be honest to be useful. A team member who spent 40 minutes on a ticket and logged it as "sprint task" has hidden the cost you are trying to find. Tell the team up front that a high interrupt fraction is information, not a grade.

## 3. Worked example: the week that disappeared

### The hook

Google's Site Reliability Engineering organization publishes a rule for its own engineers. It advertises a goal of keeping operational work, which it calls toil, below 50% of each engineer's time. The other half goes to engineering that removes future toil or improves the service. The same chapter reports that Google's quarterly surveys found the average engineer spending about 33% of their time on toil, with some reporting none and others as much as 80%.

This is a team of specialists who run some of the largest services in the world, and they still found it necessary to write down a cap and measure against it. Your team has seven students, a few hundred players and no one whose only job is operations. Without a cap, interrupts will take whatever share of the week they want.

The Emberfall team, the constructed example that runs through this course, launched its small persistent game in week 9. In the week-10 plan they assumed live work would take about 30% of their time and planned 59 hours of patch work. They delivered 38. Where did the other 21 hours go?

### The model

Two formulas carry the whole example.

**The interrupt budget.** From section 2, `i = I / C` and `P = C − I`. The rule borrowed from the SRE book is that if `i > 0.5`, the first planned hours of the next week go to fixes that reduce `I`, before any new content.

**Little's law for the support queue.** For any queue that is roughly stable, where tickets arrive about as fast as they are closed:

```
L = λ × W
```

- `L` is the average number of open tickets.
- `λ` (lambda) is the arrival rate, in tickets per day.
- `W` is the average time a ticket stays open, in days.

The law holds whatever order you answer tickets in and whatever mix of easy and hard tickets you get (Little, 1961). You can measure `L` by counting open tickets once a day and `λ` from the ticket log. Then `W = L / λ` tells you how long players wait, without timing a single ticket. Turn it around and it gives the queue length you must keep to meet a wait target: `L_target = λ × W_target`.

**Payback of a one-off fix.** A fix that costs `h` hours once and removes `s` interrupt hours per week pays back in `h / s` weeks.

### Numbers you can check

Emberfall has seven students at 12 hours each, so `C = 7 × 12 = 84` hours. Their week-10 log:

| Category | Week 10 hours | What drove it |
|---|---|---|
| Incidents and hotfixes | 18 | 5 incidents; 3 were zone crashes restarted by hand, about 3 hours each including diagnosis |
| Player support | 14 | 42 tickets at about 20 minutes each |
| Moderation | 6 | Chat reports and one harassment case |
| Monitoring | 5 | Checking the dashboard by hand several times a day |
| Deploys and restarts | 3 | Two hotfix deploys |
| **Total `I`** | **46** | |

So `i = 46 / 84 = 0.548`, or 54.8%, and `P = 84 − 46 = 38` hours. That is where the 21 hours went. The plan assumed `i = 0.30`, which leaves `84 × 0.70 = 58.8`, about 59 hours.

Now the support queue. The team counted open tickets every evening at 18:00 during week 10: 22, 25, 31, 28, 30, 26, 27. The sum is 189, so `L = 189 / 7 = 27`. Tickets arrived at 42 per week, so `λ = 42 / 7 = 6` per day. Then:

```
W = L / λ = 27 / 6 = 4.5 days
```

The team answered as many tickets as arrived, so the queue was stable. It was also long, because nobody owned it. Tickets were answered in bursts when someone felt guilty. The average player waited four and a half days to hear back, which, for a player who lost an item, is longer than they will keep playing.

The ticket log also shows why they arrived. Of 42 tickets, 15 were "item lost after disconnect", 9 were account or login problems, 8 were bug reports, 6 were questions and 4 were harassment reports. One bug caused 36% of the support load.

The team proposed three one-off fixes and one queue clean-up:

| One-off job | Cost `h` | Weekly hours removed `s` | Effect |
|---|---|---|---|
| Fix the item-loss-on-disconnect bug | 8 | 5 | Tickets fall from 42 to 27 a week; support falls from 14 to 9 hours |
| Watchdog that restarts a crashed zone and pages the on-call person | 4 | 6 | Incidents fall from 18 to 12 hours |
| Alert rule on crash rate and queue length | 2 | 3 | Monitoring falls from 5 to 2 hours |
| Clear the ticket backlog down to target | 7.7 | 0 | One-time, sets `W` to about 1 day |

Check the support row. The bug caused 15 of the 42 tickets (36%, counted in whole tickets), so 27 remain. After the fix, `λ = 27 / 7 = 3.86` tickets a day, and 27 tickets at 20 minutes each is 9 hours, 5 fewer than 14.

Check the backlog row. For a one-day wait, `L_target = 3.86 × 1 = 3.86`, so keep about 4 tickets open. Clearing from 27 to 4 means answering 23 extra tickets, `23 × 20 / 60 = 7.7` hours. After that, a daily triage slot that answers each day's tickets keeps the queue near 4.

Add it up. Steady-state interrupts become `12 + 9 + 6 + 2 + 3 = 32` hours, so `i = 32 / 84 = 38.1%` and `P = 52` hours. The one-off jobs cost `8 + 4 + 2 + 7.7 = 21.7` hours and remove `46 − 32 = 14` hours a week, a payback of `21.7 / 14 = 1.55` weeks.

Now the uncomfortable part. Those 21.7 hours come out of week 11, while the old interrupt load is still running. If week 11's interrupts match week 10's, the team has `84 − 46 − 21.7 = 16.3` hours for patch work this week. From week 12 on, it has 52. Spending week 11 buying back time looks slow. The alternative is 38 hours every week until the course ends. Add up planned hours from week 11: without fixes, 76 by the end of week 12 and 114 by the end of week 13. With fixes, 68.3 and then 120.3. The team is behind for one week and ahead from week 13 on.

This script reproduces the numbers. Run it with `.venv/bin/python`.

```python
C = 7 * 12
week10 = {"incidents": 18, "support": 14, "moderation": 6, "monitoring": 5, "deploys": 3}
after = {"incidents": 12, "support": 27 * 20 / 60, "moderation": 6, "monitoring": 2, "deploys": 3}

def summary(log):
    I = sum(log.values())
    return I, I / C, C - I

for name, log in (("week 10", week10), ("after fixes", after)):
    I, i, P = summary(log)
    print(f"{name:12} I={I:5.1f}  i={i:5.1%}  P={P:5.1f}")

L = sum([22, 25, 31, 28, 30, 26, 27]) / 7
lam = 42 / 7
print(f"L={L:.1f}  lambda={lam:.2f}/day  W={L / lam:.2f} days")
lam2 = 27 / 7
clear = (round(L) - round(lam2 * 1)) * 20 / 60
one_off = 8 + 4 + 2 + clear
saved = summary(week10)[0] - summary(after)[0]
print(f"backlog clear={clear:.1f} h  one-off={one_off:.1f} h  saved={saved:.1f} h/week  "
      f"payback={one_off / saved:.2f} weeks  week-11 planned={C - 46 - one_off:.1f} h")
```

It prints:

```
week 10      I= 46.0  i=54.8%  P= 38.0
after fixes  I= 32.0  i=38.1%  P= 52.0
L=27.0  lambda=6.00/day  W=4.50 days
backlog clear=7.7 h  one-off=21.7 h  saved=14.0 h/week  payback=1.55 weeks  week-11 planned=16.3 h
```

### Cross-game recognition

**Login queues.** MMO302 week 9 uses the same law for the queue in front of a full world server. The number of players waiting equals the arrival rate times the wait. A studio that knows its login rate and its queue length knows the wait without timing anyone, which is what the "estimated wait" figure on a queue screen is built from.

**Abandoned houses.** MMO301 week 12 applies Little's law to player housing in Final Fantasy XIV. There the "queue" is the stock of abandoned houses, and the demolition timer plays the part of `W`. Change the timer and the stock changes in proportion. Your ticket queue works the same way. Change how long a ticket may sit before someone answers it and the pile changes in proportion.

**Open bugs.** PR101 week 10 treated open bugs as a stock with an inflow and an outflow. The support queue is the same bathtub, one step closer to the player. The difference is that a player on the other end of the ticket is deciding whether to keep playing while they wait.

### Eyes-open design judgment

- **Fix the source before you speed up the queue.** Clearing the backlog without the item-loss fix would bring `W` down for a few days, then 42 tickets a week would refill it. The largest single cause of tickets is usually a bug, and it belongs in the patch.
- **The 50% line is a rule of thumb, not a law.** Google chose it for engineers whose job includes operations. For a student team with a patch due, 40% may already be too much. Pick your line before you see the log, the same way PR201 week 11 asked you to set playtest thresholds in advance.
- **Some interrupt hours are the job.** Moderation and harassment reports should not be driven toward zero by making them harder to file. Budget them, and aim the cuts at toil that a script or a fix can remove.
- **Payback assumes the fix works.** A watchdog that restarts a zone into the same crash loop saves nothing. Check the week-12 log before you count the savings.

### Check this example

1. In week 11 Emberfall counts an average of 9 open tickets, with 30 tickets arriving over the week. What is the average wait? Does it meet a one-day target?
2. A team logs `C = 70` and `I = 28`. They plan a 10-hour fix that removes 4 interrupt hours a week, and the course has 4 weeks left. Is it worth doing, measured in planned hours by the end of the course?
3. Why can you use `W = L / λ` for a queue where some tickets take 5 minutes and others take 2 hours?

<details>
<summary>Answers</summary>

1. `λ = 30 / 7 = 4.29` per day. `W = 9 / 4.29 = 2.1` days. It misses the one-day target; the queue should hold about 4 tickets.
2. `i = 28 / 70 = 40%`. Without the fix, planned hours over 4 weeks are `4 × 42 = 168`. With it, week 1 has `42 − 10 = 32`, then 3 weeks at 46, for `32 + 138 = 170`. It gains 2 hours, so it barely pays inside the course. Do it only if the hours it removes are toil people hate, or if the problem grows with players.
3. Little's law needs only a stable queue and long-run averages. It says nothing about the distribution of service times or the order tickets are answered in. The mix changes which tickets wait longest, not the average.

</details>

## 4. Reading your first cohort

Week 10 was about keeping the servers up. Week 11 is the first week you can read retention for your launch cohort. Use MMO308 week 3 for the method: build a cohort table by install day and read D1, D7 and, when you have it, D14.

Two warnings apply to a student launch. First, your cohorts are small. With 260 accounts in the launch cohort ([week 10](w10-live-ops-week-1.md)), a D7 of 27% has a Wilson interval of roughly 22% to 33% (70 of 260) (MA102 week 13), so do not compare it with a published figure from a large game and conclude anything. Compare your own cohorts with each other. Second, week 10's incidents are a **period effect**. An outage on a single day shows up at a different install date in each Dn series. Before you blame the tutorial for a low D1 on one cohort, check whether that cohort's day 1 fell on an outage day.

Write the cohort table into the live review each week. By week 13 you will want it for the economy review, and in week 14 for the post-mortem.

## 5. The operating rhythm

A rhythm is a short list of fixed slots. Keep it small enough that the team runs it in week 13 when everyone is tired.

- **On-call rota.** Keep the on-call limits your team set in week 10. One person per day holds the pager (a phone alert from the watchdog is enough). They handle incidents following MMO308 week 13 and post the player message using the MMO407 week 9 template. Everyone else ignores live noise unless paged for a SEV1 incident.
- **Daily triage, 20 minutes.** The on-call person answers or routes every new ticket and files bugs in the tracker with severity and priority (PR101 week 10). The goal is `L` near `L_target`.
- **Weekly live review, 30 minutes.** The whole team looks at four things: the interrupt log and `i`, the ticket queue (`L`, `λ`, `W`, top three causes), the cohort table, and the incident list. The output is a short list of items for the next patch.
- **A first event, only if you can afford it.** MMO308 week 8 shows that a live event mostly moves play forward in time. With `P` at 16 hours this week, most teams should defer. If you run one, make it a configuration change, not new code.

## Studio session plan

The studio meeting runs 180 minutes with one break.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Instructor briefing: the interrupt fraction, Little's law, payback | Notes |
| 0:15-0:50 | Teams tag their week-10 log and compute `C`, `I`, `i`, `P` (lab 11, part A) | Interrupt table |
| 0:50-1:20 | Support queue: daily open counts, `λ`, `W`, cause breakdown (lab 11, part B) | Queue sheet |
| 1:20-1:30 | Break | |
| 1:30-2:05 | List one-off fixes, estimate cost and hours removed, compute payback, choose (lab 11, part C) | Buy-back plan |
| 2:05-2:30 | Write the on-call rota and the weekly review agenda; set the interrupt line | Rhythm sheet |
| 2:30-3:00 | Instructor walk-round: each team shows `i`, `W` and its first buy-back item | Sign-off |

## Deliverables

Due before the week 12 studio meeting, in `production/week11/` in the team repository.

1. **Lab 11 worksheet**, parts A to D, complete. Checked by recomputing `i`, `W` and one payback from the raw numbers in the sheet.
2. **Buy-back plan.** The one-off fixes chosen, each a ticket in the tracker with an owner. Checked by opening two tickets.
3. **Rhythm sheet.** On-call rota to the end of week 14, triage time, review agenda, the team's interrupt line. Checked by asking a random team member who is on call today.
4. **Cohort table** for every install day since launch, with D1 and D7 where complete.

## Common failure modes

- **Logging interrupts as planned work.** The log then shows a low `i` and a missed plan with no explanation. Ask "was this on the board on Monday?"
- **Timing tickets by hand.** It is slow and nobody keeps it up. Count open tickets once a day and use Little's law.
- **Speeding up the queue instead of fixing its source.** More people on support treats the symptom. Put the biggest ticket cause in the patch.
- **Everyone on call.** If the whole team jumps at every alert, the rota exists only on paper. The on-call person handles it unless it is SEV1.
- **Counting savings that never arrived.** Payback is a forecast. Compare it with the week-12 log.
- **Starting an event with no hours to run it.** An event that needs a hotfix on day 2 turns into an incident.

## Review checklist

The instructor checks, at the week 12 meeting:

- [ ] `C`, `I`, `i` and `P` are computed from a log with stable categories, and recompute correctly.
- [ ] `W` comes from daily open-ticket counts and `λ`, and the team states a wait target and `L_target`.
- [ ] The top ticket cause is named with its share, and a fix for it is in the patch or has an explicit reason not to be.
- [ ] Every chosen one-off fix has a cost, hours removed per week and a payback, and a named owner.
- [ ] An on-call rota covers every day to the end of week 14, and one random team member can name today's on-call person.
- [ ] The cohort table exists and any low cohort is checked against the incident dates before it is blamed on design.
- [ ] The team's interrupt line was written before the log was analysed, or the change is explained.

## Sources

- Beyer, B., Jones, C., Petoff, J. & Murphy, N. R. (eds.) (2016). *Site Reliability Engineering: How Google Runs Production Systems*. O'Reilly. Chapter 5, "Eliminating Toil" (read at sre.google, September 2026). The advertised goal of keeping toil below 50% of each SRE's time, with the rest on engineering work; quarterly surveys finding an average of about 33% of time on toil, ranging from 0% to 80% for individuals.
- Little, J. D. C. (1961). "A Proof for the Queuing Formula: L = λW." *Operations Research* 9(3), 383-387. doi:10.1287/opre.9.3.383.
- The Emberfall team, its time log, ticket counts and fix estimates are a constructed example for teaching. They are not data from any real team.

## Interactive spec: examples/w11-live-capacity.html

**The one insight.** Interrupt hours and the support queue are the same problem seen twice. A single bug fix that removes the top ticket cause moves both views at once, and spending a week's hours on fixes returns more planned time by the end of week 13 than spending nothing.

**Layout.** Two linked views, side by side on desktop, stacked on mobile.

1. **Left view, the week as a bar.** One horizontal stacked bar of length `C`, split into the five interrupt categories (each with its own token color and a text label) and the remaining planned hours `P`. A vertical dashed line at the interrupt line (default 50% of `C`). Above the bar, large text: "Interrupts 54.8% of the week, 38.0 h left for planned work". Below it, a second bar for "after fixes" with the same scale.
2. **Right view, the queue.** A line chart of open tickets over 14 days (week 10 then week 11), with a horizontal dashed line at `L_target`. Readout: "λ = 6.00/day, L = 27.0, W = 4.50 days".
3. **Bottom strip, cumulative planned hours.** A line chart over weeks 10 to 14 of cumulative planned hours for "no fixes" and "fixes in week 11". Label the week where the lines cross.

**Controls.**
- Team size (3 to 8, default 7) and hours per person (8 to 20, default 12).
- Five sliders for week-10 interrupt hours by category (0 to 30, step 1; defaults 18, 14, 6, 5, 3).
- Tickets per week (0 to 80, default 42), minutes per ticket (5 to 60, default 20), share caused by the top bug (0 to 60%, default 36%, which gives 15 of 42).
- Checkboxes for each one-off fix: item-loss fix (8 h), watchdog (4 h, removes 6 incident hours), alert rule (2 h, removes 3 monitoring hours), clear backlog (cost computed).
- Wait target (0.5 to 5 days, default 1). Interrupt line (30% to 70%, default 50%).
All controls keyboard operable with visible focus.

**Formulas.**

```
C = team × hours
I = sum of category hours;  i = I / C;  P = C − I
λ = tickets / 7;  W = L / λ;  L_target = λ × W_target
item fix: removed = round(tickets × share);  tickets' = tickets − removed;  support' = tickets' × minutes / 60
backlog clear cost = max(0, round(L) − round(λ' × W_target)) × minutes / 60
one_off = sum of checked fix costs
saved = I − I'
payback = one_off / saved
week-11 planned = C − I − one_off;  weeks 12-14 planned = C − I'
no-fix planned = C − I every week
queue sim: L drops linearly to L_target over the first 2 days of week 11 when "clear backlog" is checked, else stays at L
```

Week-10 open counts are fixed data: 22, 25, 31, 28, 30, 26, 27.

**Test values** (must match the guide).
- Defaults, no fixes: C 84, I 46, i 54.8%, P 38.0, L 27.0, λ 6.00, W 4.50.
- All fixes checked: I' 32.0, i' 38.1%, P' 52.0, λ' 3.86, L_target 3.86, backlog clear 7.7 h, one-off 21.7 h, saved 14.0, payback 1.55 weeks, week-11 planned 16.3.
- Cumulative planned hours, weeks 11 to 14: no fixes 38, 76, 114, 152; with fixes 16.3, 68.3, 120.3, 172.3. The lines cross during week 13 (week 12: 76 against 68.3; week 13: 114 against 120.3).

**Behaviour.** Bars and lines animate over 200 ms, none under `prefers-reduced-motion`. Colors from `templates/interactive-tokens.css`; every segment has a text label, never color alone. No game art.
