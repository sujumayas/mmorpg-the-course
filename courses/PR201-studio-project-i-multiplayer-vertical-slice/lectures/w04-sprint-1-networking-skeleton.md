# PR201 · Week 04 — Sprint 1: Networking Skeleton

**Why this matters:** Sprint 1 turns your TDD into running code. At the end of it, two people on two machines should see each other move and hit an enemy that only the server controls. Every later feature hangs on that skeleton. This week also starts the habit that decides whether you hit alpha, which is a daily chart that shows the truth about progress, including the work you didn't know about when you planned.

**You will be able to:**
- Write a sprint goal that a stranger can check on two machines in under five minutes.
- Compute each person's commitment limit from availability, coordination and focus, and check a sprint backlog against it.
- Keep a daily burn-down and burn-up, and compute the day-10 forecast from each.
- Explain why the two forecasts disagree when scope grows mid-sprint, and decide what to stop starting.

**Before class:** [PR101 week 5](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w05-agile-and-scrum-adapted-for-games.md), section 1 (Scrum in one page) and section 5 (standups). [PR101 week 7](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md), sections 1 and 3 (task splitting and definitions of done). The Scrum Guide (November 2020), sections "Sprint Planning" and "Sprint Goal" (about 10 minutes, scrumguides.org).

**Prerequisites from earlier courses:** [CS202 week 4](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w04-server-authority-never-trust-the-client.md) for intent-only input. [CS202 week 10](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w10-entity-interpolation.md) for interpolating remote players. [CS202 week 8](../../CS202-networking-fundamentals-for-multiplayer-games/lectures/w08-client-side-prediction.md) for prediction, which this team deferred to sprint 2. [PR101 week 13](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md) for reproducible builds. [GD201 week 2](../../GD201-level-and-world-design/lectures/w02-blockout-and-greyboxing.md) for the graybox arena.

**Interactive:** [Burn-down and burn-up for the same sprint](../examples/w04-burndown-burnup.html), built from the spec at the end of this guide.

---

## 1. What "skeleton" means

Last week you met Alistair Cockburn's **walking skeleton**: the thinnest version of the real system that runs end to end, built to production habits and kept. For a networked RPG slice, "end to end" means input on one machine, a decision on the server and a visible result on another machine. The skeleton for *Hollowmarch* is:

1. A headless or windowed server starts from a build.
2. A second machine joins by IP address.
3. Each player spawns, and disappears when they leave.
4. A client sends only input. The server moves the body. Both screens agree.
5. Remote players move smoothly between snapshots.
6. One enemy exists only on the server's authority. A player's attack is a request. The server applies the damage and the death, and both screens show it.
7. The build shows its version in the title bar.

Nothing here is fun yet, and nothing here should look good. Every item is load-bearing, though. Combat in sprint 2 sits on items 4 and 6, and every playtest from week 7 needs item 7.

The skeleton has no client prediction. The team's risk register (week 3) deferred the prediction spike to the first day of sprint 2. Until then, local movement waits for the server, and on the lab network that delay is under a frame. Deferring a feature on purpose, with a date, is not the same as forgetting it.

## 2. Worked example: the chart that lies, and the one that doesn't

### The hook

The Scrum Guide lists burn-downs, burn-ups and cumulative flow as forecasting practices that teams have found useful. In the same passage it warns that they don't replace empiricism, meaning decisions based on what has actually happened. Teams misread burn-downs all the time, and the usual cause is one line doing two jobs. It goes down when work is finished and up when work is discovered, so a flat day could mean nothing happened or that both things happened at once. On day 4 of sprint 1 the *Hollowmarch* chart went up by six hours, and half the team decided the sprint had failed. It hadn't. The chart couldn't tell them which half of the story they were looking at.

### The model: planning the sprint

Sprint 1 is two weeks, ten working days. For each member `i` with `A_i` available hours this sprint, coordination cost `c` per channel per week over `w` weeks, and a **focus factor** `f`, the share of useful hours that turns into finished estimated work:

```
limit_i  = f × (A_i − c × (n − 1) × w)
limit    = Σ limit_i
```

A sprint backlog passes when every person's committed estimates are at or below `limit_i`, and every task is 4 hours or less with an owner and an acceptance test (PR101 week 7). With no history, use `f = 0.7`, the same as the week 1 buffer. Week 5 replaces it with a measured number.

For *Hollowmarch*, `c = 0.25`, `n = 6`, `w = 2`. Each person spends 2.5 hours on coordination. Five people have 16 hours available and the artist has 10, because of an exam. Each of the five has `0.7 × 13.5 = 9.45`, the artist has `0.7 × 7.5 = 5.25`, and the team limit is 52.5 hours.

The sprint goal is: **two players on two lab machines join a server, move, and hit one server-owned enemy that dies for both.** The team committed 48 hours in 16 tasks. Nine of them, 27 hours, are the goal. The other seven are the four funded spikes from week 3 (15 hours: R4 3, R3 4, R1 3 + 3, R6 2), hit sounds and a connect screen.

| Member | Limit | Committed | Tasks |
|---|---|---|---|
| Ana (code) | 9.45 | 9 | R1 spike parts 1 and 2, remote interpolation |
| Ben (code) | 9.45 | 9 | Server start and join, spawn and despawn, authoritative movement |
| Cato (design) | 9.45 | 8 | Server-owned enemy, attack hit check |
| Dee (art) | 5.25 | 4 | R3 export spike |
| Eli (audio) | 9.45 | 9 | Graybox arena, hit and death sounds, connect screen |
| Fay (production) | 9.45 | 9 | R4 and R6 spikes, enemy death replication, build script |
| Team | 52.50 | 48 | |

Lab 04's `check_sprint.py` prints this table from the starter files.

### The model: tracking it

Each day, the owner of every unfinished task writes the hours they think remain on it. Sum them to get **remaining** `R[d]`. Keep a second number, **scope** `S[d]`, the total estimate of every task in the sprint, including tasks added since planning. Then:

```
done[d]  = S[d] − R[d]                               the burn-up line
burn-down forecast at day k:  R[k] − ((R[0] − R[k]) / k) × (D − k)
burn-up forecast at day k:    S[k] − done[k] − (done[k] / k) × (D − k)
```

`D = 10` is the sprint length in days. The burn-down forecast extends the net slope of the remaining line. The burn-up forecast extends the rate of finished work and assumes the scope stays where it is now.

### Numbers you can check

On day 4 the R4 spike answered its question. Home players can join, but only through a relay the team must set up (6 hours). The R1 spike found that the default synchronizer sends 30 enemies at about twice the budget, so enemy state must be packed by hand (4 hours). Both tasks entered the sprint, and scope went from 48 to 58.

| Day | Remaining `R` | Scope `S` | Done `S − R` |
|---|---|---|---|
| 0 | 48 | 48 | 0 |
| 1 | 45 | 48 | 3 |
| 2 | 41 | 48 | 7 |
| 3 | 40 | 48 | 8 |
| 4 | 46 | 58 | 12 |
| 5 | 42 | 58 | 16 |
| 6 | 37 | 58 | 21 |
| 7 | 32 | 58 | 26 |
| 8 | 26 | 58 | 32 |
| 9 | 20 | 58 | 38 |
| 10 | 15 | 58 | 43 |

Stand at day 6 and forecast day 10.

- **Burn-down:** the net slope is `(48 − 37) / 6 = 1.833` hours a day. At that rate, `37 − 1.833 × 4 = 29.7` hours remain on day 10.
- **Burn-up:** the team has finished `21 / 6 = 3.5` hours a day. If scope holds, done reaches `21 + 14 = 35` by day 10, leaving `58 − 35 = 23` hours.

The two charts agree that the sprint won't finish everything. They disagree about how badly, by almost 7 hours, and they disagree about *why*. The burn-down slope folds the 10 added hours into the team's speed, as if the team were slow. The burn-up shows a team working at a steady 3.5 hours a day whose target moved once. Those two stories call for different fixes. A slow team needs help or smaller tasks. A moved target needs a cut.

The team read the burn-up and made a decision at day 6. The goal needs 27 hours. The forecast says about 35 hours of work will be done by day 10, so the goal fits only if the goal tasks are finished first. From day 6, **nobody starts a non-goal task** until all goal tasks are done. The connect screen and the relay setup wait.

The actual day-10 result was 43 hours done and 15 remaining. The rate picked up to 5.5 hours a day in the second half, once the spikes stopped blocking people. Both forecasts were pessimistic. The burn-up was closer, but it was also the one that made the day-6 decision obvious. The goal was met. The relay, the enemy packing, the hit sounds and the R6 spike carried over, for 15 hours.

### Move it yourself

The interactive specified below shows both charts for the same sprint, one above the other. Drag the scope-change day and size, and watch the burn-down slope flatten while the burn-up rate line stays straight. Then set scope added to zero and watch the two forecasts meet.

### The same idea elsewhere

**Kanban cumulative flow.** A cumulative flow diagram stacks "done", "in progress" and "to do" over time. The top edge is scope and the bottom band is done, which is a burn-up with the middle drawn in. PR101 week 7's Little's law reads straight off it: the horizontal distance across the in-progress band is cycle time.

**Bug backlogs.** PR101 week 10 tracked open bugs with `B[t] = B[t−1] + found[t] − fixed[t]`. Open bugs are a burn-down with two causes mixed together, just like this one. That lecture separated find rate from fix rate for the same reason this one separates scope from done.

**Release burn-ups in games.** A studio tracking content to a milestone (levels dressed, quests scripted) has scope that grows as the game is designed. A burn-up keeps "we're slow" and "we added a zone" apart, which a producer needs when talking to a publisher.

### Eyes-open judgment

Burn-up is not always better. It trusts the scope line, and a team can hide trouble by quietly lowering estimates so that scope shrinks. A burn-down is simpler to keep and fine when scope really is stable, as in a polish sprint. Keep both for your first two sprints, compare their forecasts, and then keep the one your team reads correctly.

Neither chart knows *which* work is done. Forty-three hours done could mean the goal is complete or that every spike and sound is done and the enemy still doesn't die. Always read the chart next to the goal tasks. Mark goal tasks on the board so that "goal remaining" is one glance away.

Finally, remaining hours are guesses made each morning by tired people. A task that says "1 hour left" three days running is stuck, not almost done. The standup exists to catch that.

### Check yourself

1. Suppose the 10 added hours had arrived on day 1 instead of day 4, with the same done column. Compute both day-6 forecasts. Which one changes?
2. A teammate proposes absorbing added work by not updating the scope line ("we'll just work harder"). What happens to the burn-up forecast, and what information does the team lose?

<details><summary>Answers</summary>

1. Scope is 58 from day 1, so `R[6] = 58 − 21 = 37`, the same as before, and `R[0] = 48`. The burn-down forecast is unchanged at 29.7, since it only uses `R[0]` and `R[6]`. The burn-up forecast is also unchanged at 23. Neither changes, which shows that the forecasts only see the totals at day 6, not when the scope arrived. The charts look different, but the day-6 numbers are the same.
2. The scope line stays at 48, so the burn-up reports `48 − 21 − 14 = 13` hours left on day 10 instead of 23. The forecast looks 10 hours better than reality, and the team loses the record that the spikes found work. That record is what makes next sprint's plan honest.

</details>

## 3. Running the sprint

Sprint 1 follows the Scrum shape from PR101 week 5, adapted to a studio that meets once a week.

- **Sprint planning** happens in this week's studio session, timeboxed to 90 minutes. The Scrum Guide caps planning at 8 hours for a one-month sprint and says shorter sprints usually need less.
- **Standups** are 10 minutes, at least three times a week, in the team channel if not in person. Each person answers one question: what is blocking the sprint goal? Update remaining hours before the standup, not during it.
- **The board** has four columns (to do, doing, review, done) and a WIP limit of one "doing" card per person (PR101 week 7).
- **Definition of done** for sprint 1: merged to `main`, builds from a clean checkout, tested on two machines, acceptance line checked by someone other than the author.
- **Branching** follows the TDD. Short-lived feature branches, spikes on `spike/…` branches that are never merged.

Programmers pair on the first networked task (server start and join). Everyone who touches networking later should see how the connection is made once, with the person who made it.

## Studio session plan

| Time | Activity | Output |
|---|---|---|
| 0:00 to 0:15 | TDD feedback. Instructor returns one question per team about authority or rates | Questions logged in the TDD change log |
| 0:15 to 0:35 | Sprint goal. The product owner proposes it, and the team rewrites it until a stranger could test it on two machines in five minutes | Goal on the board |
| 0:35 to 1:25 | Sprint planning. Split must-tier and spike work into tasks of 4 hours or less, assign owners, write acceptance lines, run `check_sprint.py` | Backlog at `PASS` |
| 1:25 to 1:35 | Break | |
| 1:35 to 2:35 | Build time. Programmers pair on server start and join. Art runs the export spike. Audio builds the graybox. Producer sets up the build script and the daily log | First commit on `main`, day-0 row in `daily.csv` |
| 2:35 to 2:55 | Two-machine check. Can a second machine run the build at all? | Pass or a blocking task |
| 2:55 to 3:00 | Standup schedule and chart owner confirmed | Calendar entries |

## Deliverables

At the start of next week's studio session (the sprint 1 review):

- **Sprint backlog** (`backlog.csv`) and **availability** (`availability.csv`) as planned, with the `check_sprint.py` output from planning day.
- **Daily log** (`daily.csv`) with one row per working day, and the burn-down and burn-up chart for the sprint.
- **A tagged build** `sprint-1` that the instructor can run on two lab machines.
- **Risk register** updated with the answers from every spike.

See [lab 04](../labs/lab04.md).

## Common failure modes

- **A goal nobody can test.** "Networking works." Fix: name the machines, the actions and what both screens show.
- **Commitment by total only.** The team fits 52.5 hours but one programmer holds 14. Fix: the per-person limit, same idea as week 1's discipline load.
- **Scope added silently.** Spikes find work, and it is done without a card. Fix: every discovered task gets a card, an estimate and a scope-line update the same day.
- **Spike code merged.** Fix: spikes stay on spike branches. Write the answer down, then rebuild properly.
- **The two-machine test at the end.** Everything works on one laptop with two windows, and the first real test is on review day. Fix: two machines from day 1, and the lab has them.

## Review checklist

The instructor checks at next week's review:

- [ ] Sprint goal written before work started, testable on two machines.
- [ ] Every task is 4 hours or less with owner and acceptance, and no person was committed over their limit.
- [ ] Daily log has a row for each working day, and scope changes are recorded on the day they happened.
- [ ] Both charts drawn, with the day-6 (or mid-sprint) forecast and the decision it led to.
- [ ] Tag `sprint-1` builds from a clean checkout and runs on two machines.
- [ ] Client sends only input for movement and attack. The server applies damage.
- [ ] Every spike's answer is in the risk register, and spike branches are not merged.

## Sources

- Schwaber, K. and Sutherland, J. (2020). *The Scrum Guide*, November 2020 edition. scrumguides.org. Sprints of one month or less; the Sprint Goal created during planning; Sprint Planning timeboxed to 8 hours for a one-month sprint and usually shorter for shorter sprints; burn-downs, burn-ups and cumulative flows named as useful forecasting practices that do not replace empiricism.
- Cockburn, A. "Walking skeleton" (alistair.cockburn.us, archived copy read September 2026). A tiny end-to-end implementation linking the main architectural parts, kept and grown.
- Keith, C. (2020). *Agile Game Development: Build, Play, Repeat* (2nd ed.). Addison-Wesley. Sprints, task boards and burn-down charts in game teams.
- The *Hollowmarch* team, backlog, availability and daily log are invented for teaching.

## Interactive spec: examples/w04-burndown-burnup.html

**Insight to make obvious:** a burn-down mixes finished work and added scope into one line, so it cannot tell a slow team from a moving target. A burn-up with a separate scope line can.

**Layout.** Two charts stacked, sharing the x-axis (day 0 to `D`). Top: burn-down, remaining hours `R[d]` with the ideal line from `R[0]` to 0. Bottom: burn-up, done hours and scope hours as two lines. A vertical cursor at the forecast day `k` runs through both. Right of or below the charts, a number panel shows both forecasts and their difference.

**Model.** Generate a sprint from parameters. Done work grows at `r1` hours a day up to day `m` and `r2` a day after it: `done[d] = r1 × min(d, m) + r2 × max(0, d − m)`, capped at scope. Scope is `S0` until day `a`, then `S0 + x`. `R[d] = S[d] − done[d]`. Forecasts use the formulas in section 2:
- burn-down: `R[k] − ((R[0] − R[k]) / k) × (D − k)`
- burn-up: `S[k] − done[k] − (done[k] / k) × (D − k)`

Draw each forecast as a dashed extension from day `k` to day `D` on its own chart.

**Controls.**
- Initial scope `S0`, 20 to 100, default 48.
- Scope added `x`, 0 to 30, default 10.
- Day added `a`, 1 to `D − 1`, default 4.
- Forecast day `k`, 1 to `D − 1`, default 6.
- Rate before and after the change point, `r1` and `r2`, 1 to 8 h/day, defaults 3.5 and 5.5, with change point `m` default 6.
- Sprint length `D`, fixed at 10 in the default view, with an option for 5 to 15.
- A toggle "use the *Hollowmarch* log", which replaces the generated series with the exact table from section 2.

**Test values** (with the *Hollowmarch* log toggle on, `k = 6`): burn-down slope 1.833 h/day and forecast 29.7 h left; burn-up rate 3.500 h/day and forecast 23.0 h left; difference 6.7 h. With `x = 0` and the generated model at defaults, the two forecasts must be equal at every `k`, since both then extend the same done rate (check: `k = 6` gives 48 − 21 − 14 = 13 on both).

**Display rules.** Show the numeric forecasts next to the charts at all times, to one decimal. Label the scope jump on the burn-down as "scope +x" so students see the rise is not negative work. Use the shared palette, keyboard-operable sliders, and text equivalents for both charts (a table of `d`, `R`, `S`, done).
