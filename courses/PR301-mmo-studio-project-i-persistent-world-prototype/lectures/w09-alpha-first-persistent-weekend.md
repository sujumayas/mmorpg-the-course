# PR301 · Week 09 — Alpha: The First Persistent Weekend

**Why this matters:** This weekend your world stops being a demo. It runs for 48 hours, through the night, with players you did not sit next to, and everything they do is saved. Most of what can go wrong in an MMO shows up for the first time now: the 3 am crash, the save that did not happen, the evening when nobody logs in. A team that plans the weekend like an operation learns from it. A team that plans it like a playtest spends Sunday apologising.

**You will be able to:**
- Write an operations plan for an unattended weekend: runbook, dashboards, alarms, on-call rota and hotfix policy.
- Compute how many sign-ups you need to reach a concurrency target, from show rate, sessions per player, session length and event attendance.
- Explain why headcount and concurrency differ by a factor of five or more, and use a scheduled event to close the gap.
- Collect the numbers during the weekend that let you size the week 13 beta from your own data.

**Before class:** Reread [MMO308 week 13](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md) (incident response) and [MMO302 week 14](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md) (dashboards and alarms). Skim [DB201 week 13](../../DB201-data-persistence-and-telemetry/lectures/w13-privacy-gdpr-and-data-retention.md) on consent and retention. Bring the freeze candidate build, your lab 08 go/no-go list and a draft tester list.

**Prerequisites from earlier courses:** [MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md) (bots and Little's law). [MMO302 week 7](../../MMO302-mmo-server-architecture/lectures/w07-persistence-strategies-write-through-periodic-event-sourcing.md) (what a crash loses). [DB201 week 14](../../DB201-data-persistence-and-telemetry/lectures/w14-backups-and-disaster-recovery.md) (restore drills, RPO and RTO). [MMO308 week 9](../../MMO308-live-operations-analytics-and-experimentation/lectures/w09-patch-management-and-hotfixes.md) (hotfixes). [MMO305 week 8](../../MMO305-social-systems-and-online-behaviour/lectures/w08-griefing-typology-and-design-responses.md) (griefing and reporting). [MMO309 week 11](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w11-exploit-response-rollback-vs-ban.md) (rollback or ban).

**Interactive:** [Weekend concurrency model](../examples/w09-weekend-concurrency.html). Use it in section 4.

---

## 1. What a weekend tests that a class session cannot

A three-hour class playtest tests your game. A 48-hour weekend tests your world, and four things only show up over that length of time.

- **Time.** The server runs through the night. Memory grows, logs fill disks, periodic saves meet peak load, and a leak of 1 MB a minute becomes 2.8 GB.
- **Restarts.** Something will restart the server, whether a crash, a hotfix or the host. Each restart is a real test of persistence: do characters come back exactly as saved, within your loss window?
- **Real concurrency.** Players come and go on their own schedule. You will see what your world looks like with five players online, which is most of the weekend, not only at the event.
- **An economy with a history.** Copper accumulates. By Sunday there are rich players, and a market with prices. Week 10 reads what happened.

The alpha has one more job. It is a rehearsal for the week 13 beta, where the course outcome of 50 or more concurrent players is checked. Measure everything you will need to plan that.

## 2. The operations plan

Write it this week and keep it in the repository as `ops/alpha-weekend.md`. Five parts.

**Runbook.** Step-by-step instructions for every action someone might need at 3 am: start, stop, restart, restore from last night's backup, flip each kill switch, deploy a hotfix, and roll back a hotfix. Each step is a command to copy, not a description. Test each one on the freeze build. The person on call may be the teammate who never touched the server code.

**Dashboards.** One page, readable on a phone: concurrent players (humans and bots separately), p99 tick time against the week 6 rule, error and crash counts, and the ledger residual, recomputed every hour ([week 7](w07-sprint-3-economy-and-crafting.md), section 3). The residual is the economy's smoke alarm. It should be zero every hour.

**Alarms.** An alarm posts to the team's on-call channel when the server stops answering health checks for 60 seconds, when p99 tick exceeds the week 6 limit for five minutes, when the hourly ledger residual is not zero, or when any character's copper rises by more than a set amount in an hour. The last rule is how studios catch dupes early. [MMO308 week 12](../../MMO308-live-operations-analytics-and-experimentation/lectures/w12-economy-monitoring.md) covers better detectors.

**On-call rota.** Every hour from Friday 18:00 to Sunday 18:00 has a named person who will see an alarm within 15 minutes, plus a backup. Nobody does more than six hours in one stretch. Night hours can use "alarm wakes you" rather than "awake and watching", but the phone must be loud. Swap shifts in the rota file, never in a chat message.

**Hotfix policy.** During the weekend, only S1 fixes deploy, and only with a second person reading the diff. Every deploy and every kill-switch flip goes in the incident log with the time, the reason and the person. [MMO308 week 13](../../MMO308-live-operations-analytics-and-experimentation/lectures/w13-incident-response.md) gives the log format. If a hotfix makes things worse, roll it back first and think second.

## 3. Your testers

Testers are students and friends giving you their evening. Treat them the way a studio treats a closed test.

- **Consent and data.** Before the first login, show a short notice. It says what you collect (telemetry events, chat logs, IP addresses in server logs), why, who can see it, and when you delete it. Keep only what the week 10 review needs, and set the deletion date now ([DB201 week 13](../../DB201-data-persistence-and-telemetry/lectures/w13-privacy-gdpr-and-data-retention.md)). Never put testers' personal data in shared spreadsheets or bug reports. Use character IDs.
- **Conduct.** Publish the course code of conduct in the launcher or login screen, give players a way to report another player in game, and name who handles reports each shift ([MMO305 week 8](../../MMO305-social-systems-and-online-behaviour/lectures/w08-griefing-typology-and-design-responses.md)).
- **Exploits.** Tell testers that finding a dupe is welcome and using one is not. Give them a channel to report it privately. Decide now what you will do if someone uses one: rollback, removing the gold, or nothing ([MMO309 week 11](../../MMO309-security-anti-cheat-and-anti-bot/lectures/w11-exploit-response-rollback-vs-ban.md)).
- **Bots.** You may run bots to add load. Mark them in telemetry and report humans and bots separately. A concurrency number that mixes them is not evidence of anything.

## 4. Worked example: how many sign-ups for twenty online?

### The hook

The WoW Classic stress tests of 2019 did not run for weeks and hope people showed up. They ran on announced dates (22 to 23 May, 19 to 20 June and 25 to 26 July) with characters capped at level 5, which kept everyone in the starting areas. EVE Online does the same on its Singularity test server. CCP announces mass tests for a set time and usually rewards participants, often with skill points to use on the test server, according to the EVE University wiki. Both studios know that people who might play are not the same as people online at once. They create concurrency on purpose, with a clock and a reason to be there.

*Saltmarsh* wants twenty humans online together at the alpha's Saturday event, with bots filling the server to the week 2 load-test crowd of 100. The course outcome of 50 humans is checked at the week 13 beta. The alpha's job is to get the rates that make the beta plan honest. How many testers must sign up?

### The model

Four measured or estimated rates, and one scheduled event:

```
P = I × s                    players who log in at least once
S = P × k                    sessions over the weekend
λ = S × share_hour           sessions starting per evening hour
L = λ × W                    concurrent players in a steady evening (Little's law)
C_event = e × P + (1 − e) × L
```

where `I` is sign-ups, `s` the show rate (share of sign-ups who ever log in), `k` sessions per player, `W` mean session length in hours, `share_hour` the share of all weekend sessions that start in one evening hour, and `e` the share of players who attend the scheduled event. `L = λW` is Little's law, from [MMO302 week 11](../../MMO302-mmo-server-architecture/lectures/w11-load-testing-with-bots.md): the average number in a system equals the arrival rate times the time each one stays.

For `share_hour`, the team weighted each hour of the weekend by when students play: night (00:00 to 07:00) 0.1, morning (07:00 to 12:00) 0.5, afternoon (12:00 to 18:00) 1.0, evening (18:00 to 24:00) 2.0. The window from Friday 18:00 to Sunday 18:00 has 12 evening hours, 14 night hours, 10 morning hours and 12 afternoon hours, so the total weight is

```
12 × 2.0 + 14 × 0.1 + 10 × 0.5 + 12 × 1.0 = 24 + 1.4 + 5 + 12 = 42.4
share_hour (evening) = 2.0 / 42.4 = 4.72%
```

### Numbers you can check

Gus's first plan: `I = 60` sign-ups, `s = 0.55` (a guess for students recruited by other students), `k = 2.5`, `W = 1.5` hours, and a Saturday 20:00 hunt for the Reedbank alpha wolf with `e = 0.6`.

```
P = 60 × 0.55             = 33 players
S = 33 × 2.5              = 82.5 sessions
λ = 82.5 × 0.0472         = 3.89 sessions per evening hour
L = 3.89 × 1.5            = 5.8 online on a normal evening
```

Thirty-three players, six online. That ratio, about one in six, is what surprises every team the first time. Headcount is not concurrency, because each player is online for a small part of the weekend. Here that is 2.5 sessions of 1.5 hours, 3.75 hours out of 48.

The event changes the picture:

```
C_event = 0.6 × 33 + 0.4 × 5.8 = 19.8 + 2.3 = 22.1
```

Now solve for the sign-ups that reach a target. Note that `L / P = k × share_hour × W = 2.5 × 0.0472 × 1.5 = 0.177` does not depend on `I`:

```
online per sign-up = s × (e + (1 − e) × L/P) = 0.55 × (0.6 + 0.4 × 0.177) = 0.369
sign-ups for 20    = 20 / 0.369 = 54.2 → 55
sign-ups for 50    = 50 / 0.369 = 135.5 → 136
```

The interactive computes the same thing hour by hour. At 20:00 the evening crowd is only two hours old and has not reached its steady level (5.06 online, not 5.8), so it shows 21.8 at the event from 60 sign-ups. That makes it slightly more cautious: 55 sign-ups for 20, the same as the hand figure, and 138 for 50 instead of 136. The hand calculation is close enough to plan with.

Now the sensitivity, because `s` and `e` are guesses:

| Change | Online per sign-up | Sign-ups for 20 |
|---|---|---|
| Plan (`s` 0.55, `e` 0.6) | 0.369 | 55 |
| Show rate 0.40 | 0.268 | 75 |
| Event attendance 0.8 | 0.459 | 44 |
| Sessions of 3 h instead of 1.5 h | 0.408 | 50 |

Show rate moves the answer most, and it is the number you know least. Doubling session length changes it by only a tenth, because the event pulls people in whatever their normal habits. So the team's plan has three parts.

1. **Recruit 60 sign-ups**, a little above the hand figure.
2. **Raise `e`.** Announce the hunt in the sign-up message, give it a reward that matters in the world (a title, a discount on the guild charter), and coordinate the time with the other teams so that the same students are not asked to be in two worlds at 20:00. Stagger team events by an hour.
3. **Top up with bots to 100** during the event, marked as bots, so the server sees the week 2 load-test crowd with real humans in it. Report both numbers.

### Interactive

`examples/w09-weekend-concurrency.html` plots concurrent players over the 48 hours, with the event spike and a line at the target. Move the show rate and watch the sign-ups needed jump. Move session length and watch the evening plateau rise while the event spike barely changes.

### Cross-game recognition

Rewrite the hook games in the model's terms. The WoW Classic stress tests raised `share_hour` towards 1 for a few hours by announcing a window, and the level-5 cap kept those players in one area, which is what a load test needs. EVE's Singularity mass tests raise `e`: a reward for showing up at the announced time increases the share of possible participants who are online together. Neither studio could make `P` much bigger in a week. Both made the concurrency they needed by moving `e` and `share_hour`. That is your lever too.

### Eyes-open judgment

- **A spike is not a load test.** One hour at 22 humans tests the event. It does not test six hours at 22. Use bots for the plateau and humans for the spike.
- **Sign-ups have a cost.** Six teams each recruiting 60 means the same students are asked several times. Coordinate across the course, or every team's show rate falls.
- **Players are not independent.** Friends log in together, and a Discord ping moves ten people at once. That makes the real peak spikier than the model, which helps at the event and hurts your plan everywhere else.
- **Measure, don't guess, next time.** Log sign-ups, `s`, `k`, `W` and `e` from session telemetry this weekend. Week 13 sizes the beta from your own numbers, with their uncertainty, not from this guide's.

### Check yourself

1. Only 40 testers sign up. With the plan's rates, how many humans will be online at the event, and how many bots are needed to reach 100?
2. The event is moved to Sunday 10:00, a morning hour. With 60 sign-ups and the plan's rates, compute `L` and `C_event`.
3. Suppose the beta had no scheduled event. Using the plan rates, how many sign-ups would reach 50 online on a normal evening?

<details>
<summary>Answers</summary>

1. `40 × 0.369 = 14.8`, about 15 humans, so 85 bots. The interactive, hour by hour, shows 14.5 humans and asks for 86 bots. Plan for the larger figure.
2. Morning `share_hour = 0.5 / 42.4 = 1.18%`. `λ = 82.5 × 0.0118 = 0.97`, `L = 1.5`. `C_event = 19.8 + 0.4 × 1.5 = 20.4`. The event still carries it. The background crowd matters little once most players attend, but `e` itself would probably fall for a Sunday-morning event.
3. Without the event, online per sign-up is `s × L/P = 0.55 × 0.177 = 0.097`, so `50 / 0.097 = 514` sign-ups. That is why the beta needs its own event.

</details>

## 5. During the weekend

Keep it short and boring.

- **Friday 17:00.** Final go/no-go against the lab 08 list. Tag the build. Take a backup. Start the world at 18:00 with the team online.
- **Every shift.** Check the dashboard at the start and the end, write one line in the incident log even if nothing happened, and hand over in the rota channel.
- **Saturday 20:00.** Event. Whole team online, one person watching only the dashboard, one watching only chat and reports.
- **Sunday 18:00.** Announce shutdown 30 minutes ahead. Stop logins, take the final backup, export telemetry and the ledger, and stop the server. Do not wipe anything. Week 10 needs all of it.

## Studio session plan

Week 9 meeting, 3 hours, on the Tuesday before the weekend. The sprint 3 review opens it, and the rest is a dress rehearsal. The one-hour bot run for the review's ledger check starts before class.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:40 | Sprint 3 review, paired teams: goal answered yes or no on the tagged build, done hours, focus factor, the one-hour ledger reconciliation, retrospective (see week 8) | Sprint 3 review record |
| 0:40-0:55 | Status against the go/no-go list from week 8; open S1s and their switches | Updated list |
| 0:55-1:20 | Restore drill: restore last night's backup on a second machine, log in a character, time it | Measured restore time |
| 1:20-1:30 | Break | |
| 1:30-1:50 | Crash drill: `kill -9` the server with bots trading, restart from the runbook, run the ledger check | Loss window and residual after restart |
| 1:50-2:15 | Sign-up sizing (lab 09 part A); event times coordinated across all teams at the board | Sign-up target, staggered event schedule |
| 2:15-2:40 | Rota, alarms and consent notice (lab 09 parts B and C); one alarm triggered on purpose; runbook walk-through by the teammate who knows the server least | Rota passing the checker, alarm received on a phone, runbook fixes |
| 2:40-3:00 | Instructor check of the ops plan | Signed ops plan |

## Deliverables

The sprint 3 review record is due in this session (see week 8). The items below are due Thursday at the freeze, in `ops/` and `production/week09/`:

1. **Ops plan** (`ops/alpha-weekend.md`) with runbook, dashboard link, alarm list, hotfix policy and incident log template.
2. **Lab 09** ([`labs/lab09.md`](../labs/lab09.md)): sign-up sizing and rota, passing `check_weekend.py`.
3. **Drill evidence**: restore time, crash-restart loss window and post-restart ledger residual.
4. **Consent notice** as shown to testers, with the data deletion date.

Due Monday after the weekend: the incident log, the telemetry and ledger exports, and the final backup, all untouched.

## Common failure modes

- **An ops plan in someone's head.** The one person who knows how to restart is asleep. Every action is a command in the runbook, tested by someone else.
- **Alarms nobody hears.** Alarms go to a channel with notifications muted. Trigger one on purpose on Tuesday and check that phones buzz.
- **Counting bots as players.** The report says "62 concurrent" and 30 were bots. Report the two numbers separately, always.
- **Every team's event at 20:00.** Six worlds split the same testers six ways. Coordinate at the board.
- **Hotfixing tired.** A 2 am fix without a second reader turns a crash into a corruption. Flip a kill switch, write it down, and fix it in the morning.
- **Wiping on Sunday.** The world is reset for a clean beta, and the evidence for week 10 is gone. Export first, and keep the final backup.

## Review checklist

The instructor checks on Thursday and during the weekend:

- [ ] The go/no-go list from week 8 is all yes, or every no has its planned response in place.
- [ ] Runbook commands were executed by a teammate other than their author, including restore and a kill switch.
- [ ] The restore drill and crash drill were timed, and the post-restart ledger residual is zero.
- [ ] The dashboard shows humans and bots separately, p99 tick and the hourly ledger residual.
- [ ] At least one alarm was triggered on purpose and received.
- [ ] `check_weekend.py` prints `PASS`: sign-ups sized from stated rates, every hour covered, no shift over six hours.
- [ ] The consent notice names data, purpose, access and a deletion date.
- [ ] The event time is coordinated with the other teams.
- [ ] During the weekend: the incident log has an entry every shift.

## Sources

- Warcraft Wiki, "Stress test" (accessed September 2026). WoW Classic stress tests on 22 to 23 May, 19 to 20 June and 25 to 26 July 2019 (the third first planned for 18 to 19 July); level cap of five on stress-test realms. https://warcraft.wiki.gg/wiki/Stress_test
- EVE University Wiki, "Singularity" (accessed September 2026). CCP conducts mass tests on the Singularity test server, and participation usually brings rewards for use on that server, often skill points. https://wiki.eveuniversity.org/Singularity
- Little, J. D. C. (1961). "A Proof for the Queuing Formula L = λW." *Operations Research* 9(3), 383-387.
- The *Saltmarsh* team, its sign-up plan, show rates, session figures, hourly weights and event attendance are invented for teaching, continuing the example from weeks 1 to 8. The six-hour shift limit and the ops plan structure are this course's conventions.

## Interactive spec

**File:** `examples/w09-weekend-concurrency.html`

**The one insight:** headcount and concurrency are different numbers. Thirty-three players give about six online on a normal evening, and only a scheduled event brings the peak above twenty. Show rate moves the sign-ups needed far more than session length does.

**Layout.** Top: a chart of concurrent players over the 48-hour weekend. Below it on desktop, to the right on wide screens (≥ 1100 px): a number panel. Bottom: a small second chart, "Sign-ups needed for the target", against show rate. Stacked at 390 px with the top chart first.

**Top chart, "Online over the weekend".** x axis: hours from Friday 18:00 (0) to Sunday 18:00 (48), labelled with day and clock time every 6 hours. y axis: players online, 0 to max(60, 1.1 × peak). Draw the regular curve `R(T)` as a line and the event point `C(E)` as a marker joined to the line (a spike at `E`). Horizontal dashed line at the target (default 50) labelled "target". Shade night hours (00:00 to 07:00) lightly. If a bot top-up is on, draw a stacked band from humans up to `max(humans, bot_target)` at the event hour only, labelled "bots".

**Bottom chart, "Sign-ups needed".** x axis: show rate 0.2 to 0.9. y axis: sign-ups (0 to 400, clipped with an arrow). Line of `ceil(target / (s × (e + (1 − e) × R(E) / P1)))`, where `P1 = s` (one sign-up). Marker at the current `s`.

**Controls.**
- Sign-ups `I`: slider 10 to 300, default 60.
- Show rate `s`: slider 0.2 to 0.9, step 0.01, default 0.55.
- Sessions per player `k`: slider 1 to 6, step 0.5, default 2.5.
- Mean session length `W` (hours): slider 0.5 to 4, step 0.25, default 1.5.
- Event time `E`: select from every whole hour from 1 to 47, labelled by day and clock, default Saturday 20:00 (`E = 26`). Option "no event".
- Event attendance `e`: slider 0 to 1, step 0.05, default 0.6.
- Target: number input 5 to 200, default 20.
- Bot top-up: checkbox with a bot target input (default 100).
- Hour weights: four number inputs (night 0.1, morning 0.5, afternoon 1.0, evening 2.0), collapsed under "Advanced".

**Formulas (exact).**

```
hour-of-day of hour u (u = 0..47) = (18 + u) mod 24
w(h) = night if h < 7, morning if h < 12, afternoon if h < 18, evening otherwise
P = I × s ;  S = P × k
A(u) = S × w(u) / Σ_{v=0..47} w(v)          sessions starting uniformly within hour u
R(T) = Σ_{u=0..T−1} A(u) × W × ( exp(−(T − u − 1)/W) − exp(−(T − u)/W) )
                                             online at clock hour T (T = 0..48), R(0) = 0
C(T) = R(T) except at T = E, where C(E) = (1 − e) × R(E) + e × P
sign-ups needed = ceil( target / ( s × (e + (1 − e) × R1(E)/s) ) ) = ceil( target / ( s × e + (1 − e) × R1(E) ) )
                 where R1 is R computed with I = 1 (so R1(E) = R(E) / I, and R(E)/P = R1(E)/s)
Little's-law check shown in the panel: L = S × w_evening / Σw × W
```

Session lengths are exponential with mean `W`; say so in a footnote.

**Number panel (aria-live="polite").** `P`, `S`, `Σw`, evening `share_hour`, Little's-law `L`, `R(E)`, `C(E)`, the peak of `C` and its time, sign-ups needed, and, when the bot top-up is on, bots needed at the event (`max(0, bot_target − C(E))`).

**Test values (defaults unless stated).**
- `P = 33`, `S = 82.5`, `Σw = 42.4`, evening share 4.72%, Little's `L = 5.84`.
- `R(26) = 5.06`, `C(26) = 21.82` (shown 21.8), regular peak 5.78 at `T = 30` (Sunday 00:00). `R(6)` (Saturday 00:00) = 5.73. `R(12)` (Saturday 06:00) = 0.39.
- Sign-ups needed for 20: 55. With target 50: 138.
- `s = 0.40`: `C(26) = 15.87`, sign-ups for 20: 76.
- `e = 0.8`: `C(26) = 27.41`, sign-ups for 20: 44.
- `W = 3`: `R(26) = 8.46`, `C(26) = 23.18`, regular peak 10.83.
- `k = 4`: `R(26) = 8.10`, `C(26) = 23.04`.
- No event (`e = 0`): peak 5.78 at `T = 30`. Sign-ups for 20 measured at Saturday 20:00 (`R(26) = 5.06` from 60): 238. Measured at the Sunday 00:00 regular peak: 208. The page shows both.
- Bot top-up at 100 with defaults: bots needed 79 (100 − 21.82 = 78.18, rounded up).
- Week 10 check (`I = 40`, `s = 0.65`, `k = 2.69`, `W = 2.1`, `e = 0.654`): `C(26) = 18.92`. The hand model in week 10 gives 19.4.
- Check-yourself 1 (`I = 40`, other defaults): `C(26) = 14.55`, bots needed 86.

**First screen:** defaults, caption "33 players, 6 online on a normal evening. The Saturday event brings 22. Fifty would take 138 sign-ups."

**Accessibility and style.** Tokens from `templates/interactive-tokens.css` inline. Controls are native inputs with labels and visible focus. The spike and the target line carry text labels, not colour alone. Respect `prefers-reduced-motion` (no animated transitions) and `prefers-color-scheme`. No game names, logos or art in the graphic.
