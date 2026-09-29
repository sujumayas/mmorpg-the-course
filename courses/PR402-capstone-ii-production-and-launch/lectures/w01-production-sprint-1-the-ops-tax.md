# PR402 · Week 01 — Production sprint 1: the plan meets the ops tax

**Why this matters:** Your PR401 production plan assumed the whole team builds features every week until launch. From week 4 on, you will be running a live build for testers, and every hour spent on crashes, deploys and tester questions is an hour not spent on the backlog. Teams that plan without that cost discover it in week 6, when cutting is most expensive.

**You will be able to:**
- Compute a weekly velocity from your PR401 vertical slice sprints and turn it into a capacity forecast for alpha and content lock.
- Apply a week-by-week ops tax to that forecast and state how many backlog points must be cut.
- Split the backlog into a feature budget (due at alpha) and a content budget (due at content lock) and draw the cut line in each.
- Set up tracker tags that measure the real ops tax every week.

**Before class:** Bring your PR401 pre-production package: the production plan, the backlog with estimates, and the board export for both vertical slice sprints (done points and available hours). Read "Eliminating Toil", chapter 5 of Beyer et al., *Site Reliability Engineering* (O'Reilly, 2016, free at sre.google), about 20 minutes. Reread section 5 of [PR101 week 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md) on cut lists and cut triggers.

**Prerequisites from earlier courses:** [PR401 weeks 11 to 14](../../PR401-capstone-i-pre-production/lectures/w11-production-plan.md) (production plan, vertical slice sprints, pre-production review). [PR101 week 6, estimation](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md). [PR101 week 7, task tracking and definitions of done](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md). [PR201 week 6](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w06-sprint-2-core-combat.md) (yesterday's weather and the dependency rule). [MMO308 week 1, what live ops is](../../MMO308-live-operations-analytics-and-experimentation/lectures/w01-what-live-ops-is.md).

**Interactive:** [Ops tax burn-up](../examples/w01-ops-tax-burnup.html)

---

## 1. The shape of the semester

PR402 is fifteen weeks, and the calendar is fixed before you write a line of code:

| Week | Milestone | What the build must be |
|---|---|---|
| 1-3 | Production sprints 1 to 3 | Features land |
| 4 | Alpha | Feature complete: every system in, content may be placeholder |
| 5 | Closed beta | Invited testers on your servers |
| 6 | Telemetry and balance review | Data drives the next sprint |
| 7 | Production sprint 4 | Content lock at the end of the week |
| 8 | Open beta | Anyone can join |
| 9 | Launch | Public, persistent, supported |
| 10-13 | Live ops, patch, economy review | Operate what you shipped |
| 14-15 | Post-mortem and showcase | Reflect and present |

Two dates carry the plan. **Feature complete** at the week 4 alpha means every system your game needs exists and works end to end, even if it looks rough. **Content lock** at the end of week 7 means no new quests, zones or items go in before open beta. The feature list closed at alpha, and content lock closes the content list too. After content lock, the build takes only bug fixes, balance values and polish until launch. Every guide in this course calls it content lock.

Every production sprint in this course is one week long, five working days, with the team's full weekly hours. Sprints 1 to 3 are weeks 1 to 3, and sprint 4 is week 7. When a later guide gives hours or points per sprint, it means per week.

So you have three sprints to finish features and four more weeks, 4 to 7, to produce content. Before alpha, content gets only a pilot item and the tools that make content cheaper (week 2). The rest of this guide is about how much of those seven weeks you really have.

## 2. What changes when the build is live

In PR401 your build ran on a laptop in a studio. From week 4 it runs on a server that testers can reach at 11 pm. That brings work that never appears in a pre-production backlog:

- **Bug fixing from outside reports.** Testers find bugs you would not, and some block them.
- **Builds and deploys.** Each build that reaches testers passes the release checklist from [PR101 week 13](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w13-builds-and-release-checklists.md). A clean deploy takes an hour. A broken one takes an evening.
- **Server operations.** Restarts, database backups, watching dashboards, reading logs ([MMO302 week 14](../../MMO302-mmo-server-architecture/lectures/w14-observability-logs-metrics-traces.md)).
- **Tester support.** Answering the Discord, sending keys, collecting surveys.
- **Playtest sessions.** Running them, watching them, writing them up.

Call the share of team hours that goes to this work the **ops tax**, written `t`. A week with `t = 0.4` means 40% of available hours went to keeping the game running and 60% went to the backlog. Google's site reliability engineers deal with the same thing under the name **toil**. Their book defines toil as manual, repetitive operational work that grows with the service, and it sets a cap: at most 50% of an engineer's time, because toil left alone will fill all of it.

Your ops tax will not be constant. Before alpha it is mostly your own bug fixing, around 10% to 20%. In the week of alpha and closed beta it jumps, because outside testers arrive and every system is new to them. It falls a little as you automate deploys and write a tester FAQ, then rises again at open beta and launch.

## 3. Features and content have different deadlines

Your PR401 backlog mixes two kinds of work, and they are due on different dates.

A **feature** is a system: trading, parties, the crafting station, the quest framework, the login queue. Features are due at alpha, because closed beta testers need every system present to find the bugs between them.

A **content item** is an instance that a system plays: one quest, one dungeon, one set of items. Content can keep arriving until content lock, because adding a quest to a working quest framework is lower risk than adding the framework.

The split matters because the ops tax is small while features are due and large while content is due. If you treat the backlog as one pile, the weeks with the most capacity get spent on whatever is at the top, and content week capacity looks bigger than it is. Keep two budgets and two cut lines.

## 4. Worked example: the plan that fits until you tax it

### The hook

Valheim entered Steam early access on 2 February 2021. It was made by a five-person team at Iron Gate Studio, and a month after release it had sold over five million copies. Its first major content update, Hearth & Home, arrived on 16 September 2021, about seven and a half months later. The next large one, the Mistlands biome, came in December 2022.

We do not know how Iron Gate split its time, and this example does not depend on it. What is plain is the situation. Five people went from building a game to running one for millions of players, and the same five people had to build the next update. That is your situation at a far smaller scale in week 4. The cost of running the game comes out of the hours you planned to spend making it.

### The model

Start from yesterday's weather, as in [PR201 week 6](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w06-sprint-2-core-combat.md):

```
rate          r   = points done in the last sprints / available hours in them
nominal       v   = r × H                         (points per week, H = available hours per week)
week w        c_w = v × (1 − t_w)                 (backlog points in week w)
feature cap   F   = Σ c_w over weeks 1 to 3
content cap   C   = Σ c_w over weeks 4 to 7
cut           max(0, backlog − cap) in each budget
```

- `r` uses done points only, measured at the review, and the hours people really had.
- `H` is the team's available hours in a normal PR402 week, after other courses and absences.
- `t_w` is the ops tax planned for week `w`, between 0 and 1.
- `F` and `C` are the two budgets from section 3.

The naive plan is the same model with every `t_w = 0`.

### Numbers you can check

The sample team for this course is Emberfall, the seven-person team from PR401, a constructed example that runs through the whole semester. It has three programmers (server, gameplay, tools and UI), two designers (systems and economy, content), one artist and one student who covers audio and technical art. They are building a small co-op world where players make every tool and weapon and small groups hold towns. PR401 week 14 approved their vertical slice and replanned art to two more towns, with a third on the cut list behind a trigger. The slice sprints were one week each, at PR401's 8 hours a week per person, so 56 scheduled team hours a sprint before absences:

| Sprint | Points done | Available hours |
|---|---|---|
| Vertical slice 1 | 14 | 44 |
| Vertical slice 2 | 18 | 48 |
| Total | 32 | 92 |

`r = 32 / 92 = 0.348` points per hour. In PR402 each member has the 12 hours a week that PR401 week 11 planned with, so the team has `H = 7 × 12 = 84` hours a week and `v = 0.348 × 84 = 29.2` points per week.

Their remaining backlog from the PR401 production plan, pointed after the slice, is 106 points of features, spread over 30 features, and 89 points of content, 195 in all. PR401 week 11 found the same backlog fitted in hours at a team load of 0.80, with no hours set aside for running a live build.

**Naive plan.** Seven weeks at 29.2 is 204.5 points against a backlog of 195. The plan fits with room to spare, and the team feels fine.

**Taxed plan.** The team sets the ops tax from its own history and the calendar. Their PR401 slice sprints spent about 10% of hours on bug fixing, so weeks 1 to 3 start there and rise as the build hardens for alpha. Weeks 4 to 7 are planning guesses to be replaced with measured values each week.

| Week | Milestone | Tax `t_w` | Backlog points `c_w` |
|---|---|---|---|
| 1 | Sprint 1 | 0.10 | 26.3 |
| 2 | Sprint 2 | 0.15 | 24.8 |
| 3 | Sprint 3 | 0.20 | 23.4 |
| | **Feature budget `F`** | | **74.5** |
| 4 | Alpha | 0.45 | 16.1 |
| 5 | Closed beta | 0.55 | 13.1 |
| 6 | Telemetry review | 0.50 | 14.6 |
| 7 | Sprint 4, content lock | 0.45 | 16.1 |
| | **Content budget `C`** | | **59.9** |

Check one row. Week 5: `29.2 × (1 − 0.55) = 13.1`.

Now compare:

| | Naive | Taxed |
|---|---|---|
| Capacity, weeks 1-7 | 204.5 | 134.4 |
| Feature points to cut (of 106) | none | 31.5 |
| Content points to cut (of 89) | none | 29.1 |
| Total cut | none | 60.6 |

The naive plan cuts nothing. The taxed plan cuts 60.6 points, almost a third of the backlog. On the feature side that is about 30% of the feature points, roughly 9 of the 30 features. The difference is not pessimism. It is the cost of work the team already knows it will do.

The model also shows a trap. In the naive plan, the team would carry 106 points of features into weeks 1 to 3, which only have room for 74.5. The last 31.5 points of features slip past alpha into the high-tax weeks and push content out. That is the most common way capstone alphas fail. The features are "nearly done" in week 4, and closed beta testers meet half-built systems.

This program reproduces the table. Run it with `.venv/bin/python`:

```python
done_points = 14 + 18            # PR401 vertical slice sprints 1 and 2
done_hours = 44 + 48             # available hours in those sprints
rate = done_points / done_hours  # points per available hour
hours = 84                       # available team hours per PR402 week: 7 x 12

tax = {1: 0.10, 2: 0.15, 3: 0.20, 4: 0.45, 5: 0.55, 6: 0.50, 7: 0.45}
feature_weeks, content_weeks = [1, 2, 3], [4, 5, 6, 7]

naive = rate * hours * len(tax)
feat = sum(rate * hours * (1 - tax[w]) for w in feature_weeks)
cont = sum(rate * hours * (1 - tax[w]) for w in content_weeks)
print(f"rate {rate:.3f} pt/h, nominal {rate * hours:.1f} pt/week")
print(f"naive weeks 1-7: {naive:.1f} pts")
print(f"feature capacity to alpha: {feat:.1f} pts (low {feat * 0.8:.1f})")
print(f"content capacity weeks 4-7: {cont:.1f} pts (low {cont * 0.8:.1f})")
print(f"total with ops tax: {feat + cont:.1f} pts")
backlog = {"feature": 106, "content": 89}
print(f"cut features {backlog['feature'] - feat:.1f}, cut content {backlog['content'] - cont:.1f}")
```

It prints:

```
rate 0.348 pt/h, nominal 29.2 pt/week
naive weeks 1-7: 204.5 pts
feature capacity to alpha: 74.5 pts (low 59.6)
content capacity weeks 4-7: 59.9 pts (low 47.9)
total with ops tax: 134.4 pts
cut features 31.5, cut content 29.1
```

The "low" values apply a 20% band, as in PR201. Commit to the middle value. Put the points between the low and middle values on a trigger list, so you know in advance what goes first if week 2 comes in slow.

### Cross-game recognition

The same arithmetic appears wherever one group builds and operates the same thing.

- **Google SRE, 2016.** The 50% toil cap is an ops tax ceiling. Google's rule is the reverse of our plan. Instead of forecasting `t` and cutting scope, they fix the maximum `t` and move operational work back to the product developers when it goes over. In weeks 5 and 6 your planned `t` is at or above their ceiling. That is acceptable for two weeks of beta. It is a warning if it stays there after launch.
- **Valheim, 2021.** Five people, millions of players, and the next update built by the same five. The gap between early access and the first major update is what running a hit costs in development time, whatever the exact split was.
- **Your own PR201 and PR301 projects.** Look at your old boards. The sprint with an external playtest almost always has a lower done count than the sprint before it. That drop is the ops tax, measured on you.

### Eyes-open judgment

The tax values are guesses until week 4. Two errors are common, and they point in opposite directions.

Setting `t` too low is the naive plan with extra steps. If you cannot justify a number, start at 0.5 for the weeks with outside testers and correct it with your measured value.

Setting `t` too high hides a different problem. A team that plans `t = 0.7` in closed beta has usually not automated its deploys or written its tester FAQ. The fix there is to spend feature points in sprints 1 to 3 on the things that lower the tax: a one-command deploy, a crash reporter that files tickets, an admin command to restore a character. Those stories cost points now and repay them every week from week 4 to week 13. Put at least one of them above the line in sprint 1.

Finally, the tax is a planning number, not a target. Nobody should skip fixing a crash to protect the feature budget. Measure `t` honestly every week and replan with the measured value.

## 5. Measuring the ops tax

The forecast is only useful if you replace guesses with data. Set this up in sprint 1, before the tax is large:

- **Tag every ticket** `feature`, `content` or `ops`. Ops covers bugs found by anyone outside the story's own work, deploys, server work, tester support and playtest running.
- **Log hours against tickets**, even roughly. Half-hour resolution is enough.
- **Compute `t` at each sprint review:** ops hours divided by logged hours. Enter it in the lab 01 sheet next to the planned value.
- **Replan when the measured `t` misses the planned one by more than 0.1.** Rerun the checker with the measured value for past weeks and the new guess for future ones, and move the cut line.

A bug in a story's own code, found before the story is done, is part of that story, not ops. Tagging it as ops makes velocity look better than it is.

## 6. Sprint 1 itself

With the cut line drawn, plan sprint 1 as in PR201: commit the forecast (26.3 points for Emberfall), order by dependency, and put stretch stories below the line. Three extra rules apply in production:

- **Longest feature chain first.** Features have three sprints. A chain that needs all three must start today.
- **One ops-reducing story.** Deploy script, crash reporter or admin tools, as argued in section 4.
- **A server build from day 1.** The sprint 1 increment runs on the server you will use for alpha, not only on a laptop. Environment setup is covered in week 3, but the first deploy should happen now.

## Studio session plan

Week 1 meeting, 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:20 | Briefing: the semester calendar and sections 1 to 3 | Every team member can name the alpha and content lock dates |
| 0:20-0:50 | Teams compute `r` and `v` from PR401 data; agree the tax schedule (lab 01, part A) | `history.csv` and `plan.csv` filled |
| 0:50-1:30 | Split the backlog into feature and content; draw both cut lines and the trigger list (lab 01, part B) | `backlog.csv` with every item marked keep, trigger or cut |
| 1:30-1:40 | Break | |
| 1:40-2:00 | Run `check_capacity.py`; fix what it flags | `PASS` output |
| 2:00-2:30 | Instructor round, 5 minutes per team: the biggest cut and its pillar check | Notes on the board |
| 2:30-3:00 | Sprint 1 planning: commit the forecast, pick the ops-reducing story, set up ticket tags | Sprint 1 board live |

## Deliverables

Every week's deliverables go in `production/weekNN/` in the team repository, `production/week01/` this week. The post-mortem and the showcase use `production/postmortem/` and `production/showcase/`.

Due at the end of the week 1 meeting:

1. **Capacity plan** in the lab 01 format ([`labs/lab01.md`](../labs/lab01.md)): history, week-by-week tax schedule, and the backlog with keep, trigger and cut marks. The instructor reruns `check_capacity.py`. It must print `PASS`.
2. **Cut memo**, one page: the five largest cuts, which pillar each touches, and what the player loses. Signed off by the whole team.
3. **Sprint 1 board** with ticket tags in place and one ops-reducing story above the line.

Due at the start of week 2: the sprint 1 increment deployed to the team server, with the measured ops tax for week 1 entered in `plan.csv`.

## Common failure modes

- **One backlog, one line.** Features and content share a cut line, so feature work drifts into weeks 4 to 7. Keep two budgets.
- **Tax of zero "until beta starts".** Weeks 1 to 3 have bug fixing too. Your PR401 data shows how much.
- **Cutting the invisible work.** The deploy script and the admin tools are the first things cut because players never see them. They are the things that lower `t` for ten weeks.
- **Counting half-done stories in velocity.** An 80% story counts zero. Otherwise `r` inflates and every later number with it.
- **Cuts nobody owns.** A cut that is not written down and agreed comes back as "we'll squeeze it in". The cut memo exists to stop that.
- **Never replanning.** A tax schedule written in week 1 and never updated is a guess with a spreadsheet around it.

## Review checklist

The instructor checks at the end of week 1:

- [ ] `r` is computed from done points and available hours of the PR401 slice sprints, with the source board exports in the repo.
- [ ] A tax is set for every week 1 to 7, at least 0.1 in weeks 1 to 3 and at least 0.3 in weeks 4 to 7, with one sentence of justification for each phase.
- [ ] Kept feature points do not exceed the feature budget; kept content points do not exceed the content budget (checker `PASS`).
- [ ] Trigger items cover the gap between the low and middle forecast in each budget.
- [ ] Every cut names the pillar it touches.
- [ ] At least one ops-reducing story is committed in sprint 1.
- [ ] Ticket tags `feature`, `content`, `ops` exist and are used on the sprint 1 board.

## Sources

- Wikipedia, "Valheim" (read September 2026). Early access release on Steam on 2 February 2021; five-person team at Iron Gate Studio; over five million copies sold a month after release; Hearth & Home update on 16 September 2021; Mistlands update in December 2022.
- Beyer, B., Jones, C., Petoff, J. and Murphy, N. R. (eds.) (2016). *Site Reliability Engineering: How Google Runs Production Systems*. O'Reilly. Chapter 5, "Eliminating Toil", read at sre.google, September 2026. Definition of toil and the 50% cap on operational work, with the rationale that toil left unchecked expands to fill everyone's time.
- Fowler, M. "Yesterdays Weather." martinfowler.com, 12 May 2004. Planning an iteration from the last one's output.
- Keith, C. (2020). *Agile Game Development: Build, Play, Repeat* (2nd ed.). Addison-Wesley. Background on release planning across alpha and beta in game teams.
- The Emberfall team continues the constructed PR401 example (PR401 weeks 6 and 11 to 14). Its slice sprint history, backlog and tax schedule here are constructed for teaching and continue in weeks 2 to 14. They are not data from any real team.

## Interactive spec: examples/w01-ops-tax-burnup.html

**The one insight:** a backlog that fits the untaxed capacity line can miss the taxed line by a third, and the gap opens in the weeks after alpha, when outside testers arrive.

**Layout.** Two linked views, stacked below 900px and side by side above.

- **Left, burn-up chart.** X axis: weeks 0 to 7. Y axis: cumulative points, 0 to 220. Three lines. (1) Naive capacity, dashed: `v × w`. (2) Taxed capacity, solid: cumulative `Σ v × (1 − t_i)` for `i ≤ w`. (3) Scope, horizontal: backlog total, with a second horizontal step showing the feature backlog up to week 3. Shade the band from 0.8 to 1.0 times the taxed line. Mark week 3 (alpha, feature complete) and week 7 (content lock) with vertical rules and labels.
- **Right, tax bars.** Seven vertical bars, one per week, height `t_w` from 0 to 0.8. Each bar is draggable (pointer) and adjustable by keyboard (focus a bar, arrow up and down in steps of 0.05). A horizontal line at 0.5 labelled "SRE toil cap".

**Controls.** Number inputs for done points (default 32), done hours (92), weekly hours `H` (84), feature backlog (106), content backlog (89). A button "Reset to Emberfall". A toggle "Show naive line".

**Readouts, next to the chart.** `r`, `v`, feature budget `F`, content budget `C`, low values at 80%, feature cut and content cut, each to one decimal. When a cut is positive, show it in the warning color.

**Test values (defaults).** `r = 0.348`, `v = 29.2`, `F = 74.5`, `C = 59.9`, total 134.4, naive 204.5, feature cut 31.5, content cut 29.1. Setting every tax to 0 gives `F = 87.7`, `C = 116.9` and a feature cut of 18.3: the feature budget is too small even with no tax, because features have only three weeks. That is worth a caption.

**Formulas.** `r = done_points / done_hours`; `v = r × H`; `c_w = v × (1 − t_w)`; `F = c_1 + c_2 + c_3`; `C = c_4 + ... + c_7`; cut = `max(0, backlog − budget)`.

**Accessibility.** All values also in a table below the charts. Respect `prefers-reduced-motion` (no animated transitions). Colors from `templates/interactive-tokens.css`.
