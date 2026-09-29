# PR401 · Week 12 — Vertical Slice Sprint 1

**Why this matters:** The vertical slice is the evidence your week 14 panel uses to decide whether your project goes into production. It is also the only chance before PR402 to measure what one unit of your game costs to make. Teams that don't track their hours in these two sprints walk into the review with a slice and no numbers, and then plan PR402 with the same guesses they had in week 9. This week you start the slice, log every hour by kind, and decide which tools are worth building before production starts.

**You will be able to:**
- Plan a one-week slice sprint from per-discipline capacity and a single playable sprint goal.
- Tag logged hours as one-time, per-unit, fix or overhead, and compute a per-unit cost that excludes the one-time work.
- Compute the break-even count for a content tool, and check what the tool does to each discipline's load.
- Decide whether to build a tool now, later or never, and defend the decision with numbers.

**Before class:** Bring your lab 11 files (`team.csv`, `backlog.csv`, the constraint log) and your week 9 content plan with its unit counts (quests, bounties, towns, encounters). Make sure your tracker has a field for hours logged per task and a tag field; if it doesn't, add both before the meeting. Reread [PR201 week 6, section 4](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w06-sprint-2-core-combat.md) on yesterday's weather and dependency chains (15 minutes). Skim [MMO306 week 12](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w12-content-tooling-and-pipelines.md), section 1, on content as data flowing through a pipeline (10 minutes).

**Prerequisites from earlier courses:** [PR201 week 2, pre-production pillars and scope](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w02-pre-production-pillars-and-scope.md) (what a vertical slice is and why it is built at final quality). [PR201 week 6](../../PR201-studio-project-i-multiplayer-vertical-slice/lectures/w06-sprint-2-core-combat.md) (yesterday's weather, `q^k`). [PR101 week 7, task tracking and definitions of done](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w07-task-tracking-and-definitions-of-done.md) (WIP limits, levels of done). [PR101 week 6](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) (plan ratios, used here on tool estimates). [MMO306 week 9, procedural and systemic content](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w09-procedural-and-systemic-content.md) and [week 12, content tooling and pipelines](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w12-content-tooling-and-pipelines.md). From this course, [week 11, production plan](w11-production-plan.md) (per-discipline capacity and load, and the *Emberfall* sample team).

---

## 1. What the slice has to prove

PR201 defined a vertical slice as a small piece of the game at shipping quality, cutting through every layer. At capstone scale, for an MMO-scope project, the slice has a longer checklist, because the thing that makes an MMO different is the loop that runs across sessions and players. A capstone slice contains:

- **One town** at final art and audio quality, with its navigation, lighting, crafting station and set dressing done.
- **One quest chain** that starts at a hub and ends in a reward, using the real quest data format. Take it from your week 9 content plan. For *Emberfall* it is the tutorial quest chain, the one quest chain the plan keeps.
- **One group encounter** for the party size your design targets, with telegraphs, tuning and loot.
- **The persistent loop.** A player logs out and back in with their progress, items and currency intact, on the real server, not a local save.
- **One social system** from your week 10 plan working end to end, such as a guild roster, a party finder or trade.

The slice has two jobs. The obvious one is to show the panel the game is good. The less obvious one is to **measure the cost of making it**. Your week 11 production plan rests on estimates like "5 hours of art per town". The slice is the first time you build a town at final quality, so it is the first time that number can be checked. Week 14 uses what you measure in weeks 12 and 13 to redo the plan. If you don't log hours now, week 14 has nothing to work with.

## 2. Planning the sprint

Weeks 12 and 13 are one slice sprint each, and the slice is reviewed in week 14. Plan it the way PR201 taught you, with two changes for capstone scale.

- **Plan per discipline, at PR401 hours.** The slice runs at the PR401 convention of `H = 8` hours a week, not PR402's 12. With `f = 0.75`, the *Emberfall* artist has 6 hours of real work a week, and the team 42. Use the lab 11 method with those numbers, not the team total. If the art load for the slice is 1.3, the slice will ship with grey boxes whatever the team total says.
- **One playable goal.** The sprint 1 goal is a sentence a stranger can test, for example "two players log in, walk from the hub to the dungeon entrance, finish the first tutorial quest and log out, and their quest state survives a server restart." Order the backlog so the chain that makes that sentence true is committed first, then widen. PR201 week 6's `q^k` warning applies: the persistent loop is a chain of client, server and database work, and every link has to land.

Keep a WIP limit per discipline (PR101 week 7). On a capstone team the usual failure is five people each with three items "in progress" on day 6 and nothing merged. The slice build must be playable from the main branch every day from day 2 onward, even if most of it is grey.

## 3. Tag every hour

Log hours on every task, and give each log entry one tag.

- **One-time.** Work you do once no matter how many units you make: a shader, a material library, export presets, a quest data format, a server schema, learning a new tool.
- **Per-unit.** Work you repeat for every unit: building and dressing one town, scripting one bounty, tuning one encounter.
- **Fix.** Bug fixing and rework after something was called done.
- **Overhead.** Meetings, builds, reviews, playtests.

The tags matter because the slice total mixes one-time and per-unit work, and only the per-unit part scales with production. Suppose the *Emberfall* artist logs 14 hours on the slice's town across the two sprints. Four of those went into the material library, the terrain export presets and learning the foliage painter. If you plan PR402's three further towns at 14 hours each, you plan 42 hours. At the per-unit 10 hours, it is 30. The 12-hour difference is a sixth of the artist's whole PR402 capacity of 72. Get the tag wrong in the other direction and you plan 30 hours for work that costs 42.

Tag at the time you log, not at the end of the sprint. Nobody remembers on the last day which of Tuesday's four hours were the shader and which were the rocks.

## 4. Worked example: is the bounty tool worth building?

### The hook

At GDC 2017, Jaap van Muijden of Guerrilla Games presented the procedural placement system behind *Horizon Zero Dawn* (2017). Instead of artists placing every plant, rock and animal by hand, the system assembles the environment around the player as they move, from rules and data the artists author, including effects, sounds and wildlife. Building such a system is a one-time cost. Once it exists, covering more ground costs rules and data rather than hand placement, object by object.

You are not building an open world. You are about to decide something with the same shape. Your slice sprint 1 made bounties by hand, and your content plan wants many more. Should a programmer spend part of the next sprint building a bounty tool instead of more slice?

### The model

Every content decision like this compares two cost lines.

```
Manual:  T_m(n) = n × u_m
Tool:    T_t(n) = F + n × u_t
Break-even:  n* = F / (u_m − u_t)
```

- `n` is the number of units still to make, from the content plan.
- `u_m` is the per-unit cost without the tool, from your tagged hours.
- `F` is the one-time cost of building the tool, an estimate.
- `u_t` is the per-unit cost with the tool.
- `n*` is the **break-even count**. Below it, the tool costs more than it saves.

Then do the step the break-even formula leaves out. A tool usually moves per-unit work from one discipline to another. Recompute the loads from week 11 with the tool in place. A tool that saves hours in total can still push a discipline over 1.0.

### Numbers you can check

*Emberfall*'s week 9 content plan has a bounty rotation of 12 bounties before launch, and a second rotation of 12 for the PR402 patch week. The team built 3 bounties by hand in slice sprint 1. For each, the content designer wrote the target, the text and the reward, about 1 hour. That writing happens whichever way the bounty is built, and it is already in the plan, so it drops out of the comparison. The tools and UI programmer then scripted each one, 4.5 hours for the three, so `u_m = 1.5` programmer hours per bounty, tagged per-unit.

The programmer proposes a bounty tool. The designer's sheet becomes a data file with fields for target, count, zone and reward, and the server loads it directly. The estimate is `F = 12` programmer hours. With the tool, the designer spends about 0.4 extra hours per bounty entering and testing the data, and a programmer about 0.1 hours on the odd special case, so `u_t = 0.5`. Both costs are on top of the writing, the same as `u_m`.

`n* = 12 / (1.5 − 0.5) = 12` bounties.

Bounties still to make: 9 for the launch rotation (12 minus the 3 in the slice), and 12 for the patch week, 21 in all.

| Bounties `n` | Manual, h | Tool, h | Saved by tool | Programmer h with tool | Designer h with tool |
|---|---|---|---|---|---|
| 6 | 9.0 | 15.0 | −6.0 | 12.6 | 2.4 |
| 9 (launch rotation only) | 13.5 | 16.5 | −3.0 | 12.9 | 3.6 |
| 12 | 18.0 | 18.0 | 0.0 | 13.2 | 4.8 |
| 21 (launch and patch week) | 31.5 | 22.5 | 9.0 | 14.1 | 8.4 |
| 33 (plus one more live rotation) | 49.5 | 28.5 | 21.0 | 15.3 | 13.2 |

Check the 21-bounty row. Manual `21 × 1.5 = 31.5`. Tool `12 + 21 × 0.5 = 22.5`. Programmer `12 + 21 × 0.1 = 14.1`. Designer `21 × 0.4 = 8.4`.

The answer depends entirely on `n`. For the launch rotation alone the tool loses 3 hours. It pays only because the content plan has a patch-week rotation, and it pays well only if live operations keep adding rotations.

Two more checks before committing.

- **Tool estimates run late.** `F` and `u_t` are estimates, so scale them by *Emberfall*'s `R = 1.30`. That gives `F = 15.6`, `u_t = 0.65`, and `n* = 15.6 / (1.5 − 0.65) = 18.4`. `u_m` is a measured actual, so it is not scaled. At 21 bounties the tool now saves 2.25 hours. It still pays, barely.
- **What it does to the loads.** Put the scaled numbers into the week 11 load table. Programming loses the 31.5 hours of manual scripting and gains `15.6 + 21 × 0.13 = 18.3`, so its demand falls from 169 to 155.8 of 216, a load of 0.72 instead of 0.78. Design gains `21 × 0.52 = 10.9`, from 104 to 114.9 of 144, a load of 0.80 instead of 0.72. Neither discipline is near 1.0, so the move is safe. On a team where design was the constraint, the same tool would save hours in total and push the constraint over the line.

The team decides to build it, in slice sprint 2 (week 13), so that the slice's own bounties are made with it and `u_t` is measured, not guessed, by week 14. A tool built in PR402 sprint 3 would arrive after the launch rotation is made by hand, and `n` would fall to 12, exactly break-even at best.

### Cross-game recognition

**Horizon Zero Dawn, rewritten.** `F` is the placement system. `u_m` is an artist placing vegetation by hand per area. `u_t` is authoring rules per biome, which covers huge areas at once. With an open world, `n` is so large that `n*` hardly matters. The interesting question, for Guerrilla as for you, is who does the per-unit work afterwards: people writing placement rules instead of people placing objects.

**"Is It Worth the Time?" (xkcd 1205).** Randall Munroe's chart tabulates how long you can spend automating a routine task before you lose time over five years, by how often you do it and how much you shave off. It is `n* = F / (u_m − u_t)` solved for `F`, with `n` set by frequency times five years. The chart has the same blind spot as the formula. It counts total time and ignores whose time it is.

**Your own pipeline in MMO306.** MMO306 week 12 treated content as data moving through validation stages. A bounty tool is the first stage of that pipeline. Once the format exists, the validators MMO306 describes become cheap to add, which is a second saving the break-even table doesn't count.

### Eyes-open design judgment

- **Measure `u_m` before deciding.** The bounty decision turned on sprint 1's measured 1.5 hours. Build the first few units by hand. They tell you what the tool has to beat and what it must do.
- **Recompute loads, not just totals.** Every tool moves work. Check the constraint after the move.
- **Count units after launch if you will make them.** A live game keeps making content. A tool whose break-even sits above your launch content can still pay for itself in live ops, and PR402 has live-ops weeks.
- **Don't build tools for units you might cut.** If the week 9 plan's rumour quests are the first thing you would add or cut, `n` is uncertain, and the tool's value is uncertain with it. Build the tool for the units you are sure of.

### Check this example

1. A tool costs 30 hours and cuts a unit from 6 hours to 1.5. What is the break-even count?
2. The same team has 12 units left. How many hours does the tool save, and how many if `F` runs over by `R = 1.4`?
3. The tech-art student proposes a town-dressing brush for *Emberfall*: `F = 10` tech-art hours, and it cuts the artist's per-unit work on a town from 10 hours to 7 while adding 1 tech-art hour per town. With three more towns planned, does it save hours in total, and which discipline should you check?

<details>
<summary>Answers</summary>

1. `n* = 30 / 4.5 = 6.7` units.
2. Manual `72`, tool `30 + 18 = 48`, saving 24 hours. At `R = 1.4`, `F = 42`, tool `60`, saving 12 hours.
3. Per unit the saving is `10 − (7 + 1) = 2` hours, so `n* = 10 / 2 = 5` towns. With 3 towns it loses `10 + 24 − 30 = 4` hours in total. But it moves 9 hours of work off the artist, the constraint, and adds 13 to audio and tech art. Check audio and tech art first: at 0.90 in week 11, 13 more hours at `R = 1.3` would push it to about 1.14. Losing hours in total can be worth it to relieve a constraint, but not by creating a new one.

</details>

## 5. The slice quality bar and the daily build

Final quality means final for the slice, and nothing outside it. Write the quality bar as a short list the team signs before day 1, one line per discipline. For example: environment art dressed to the week 3 art direction page (the start of the art bible) with no placeholder materials in camera view; every player action with hit, sound and UI feedback; server persistence surviving a restart with no lost items; the frame time target from the technical design met on the lab machines. Anything not on the list is allowed to be rough.

Protect the build. The slice is an integration exercise, and the most common way to lose sprint 1 is to discover on the last day that the client and server branches no longer agree. Merge to main at least daily. Run a two-player smoke test on every merge that touches networking: log in, move, fight, log out, log in. Keep the result in the tracker. MMO306 week 12's point about catching defects early is doubly true here. A persistence bug found on day 1 costs an hour, and the same bug found at the review costs the review.

## Studio session plan

Week 12 meeting, 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:15 | Briefing: what the slice must prove, hour tags, the tool decision | |
| 0:15-0:40 | Teams write the slice quality bar and the sprint 1 goal sentence | Signed quality bar |
| 0:40-1:15 | Sprint planning per discipline from lab 11 capacity; commit the goal chain first, set WIP limits | Sprint 1 backlog |
| 1:15-1:25 | Break | |
| 1:25-1:55 | Tag setup: add the tag field, tag last week's hours as practice, agree edge cases (learning a tool is one-time) | Tracker ready |
| 1:55-2:30 | Tool decisions: list candidate tools, fill the break-even and load table for each (lab 12) | Tool decisions |
| 2:30-2:50 | Instructor round, 5 minutes per team, on the goal sentence and the tool decision | Sign-off |
| 2:50-3:00 | First merge of the day; smoke test on main | Build playable from main |

## Deliverables

Due at the end of the week 12 meeting, in `preproduction/week12/`:

1. **Slice quality bar and sprint 1 goal** (`slice-plan.md`), signed by every team member.
2. **Tool decisions** in the lab 12 format ([`labs/lab12.md`](../labs/lab12.md)): each candidate tool with `F`, `u_m`, `u_t`, `n`, break-even, the load effect and the decision. Checked by running `unit_cost.py`, which must print `PASS`.

Due at the start of the week 13 meeting: the tagged time log for sprint 1 so far (`timelog.csv`) and the per-unit cost report that `unit_cost.py` produces from it.

## Common failure modes

- **A slice without numbers.** The team builds a good slice and logs nothing. Week 14 then has no evidence to replan with.
- **One-time work booked as per-unit.** The first unit looks three times more expensive than it is, and production is overplanned or the project is killed for the wrong reason.
- **Per-unit work booked as one-time.** The opposite error, and more common, because people like to think the hard part is over.
- **Tools that move the constraint.** Always rerun the load table after a tool decision.
- **Tools built too late.** A tool that arrives after most units are made saves nothing.
- **Slice scope creep.** "While we're at final quality, let's add a second zone." The slice is small on purpose.
- **Integration on the last day.** Merge daily and smoke-test on every networking change.

## Review checklist

The instructor checks, at the end of the week 12 meeting and again at the week 14 review:

- [ ] The sprint 1 goal is one testable sentence that includes the persistent loop.
- [ ] Sprint 1 is planned per discipline, and no discipline is above 1.0 for the sprint.
- [ ] The quality bar exists, is signed, and has one line per discipline.
- [ ] Every logged hour has one of the four tags; the team has written down its edge-case rules.
- [ ] Each tool decision shows break-even, the load effect on each discipline and the decision, and `unit_cost.py` prints `PASS`.
- [ ] Main has been playable every day since day 2 of the sprint, with smoke-test results in the tracker.

## Sources

- van Muijden, J. "GPU-Based Run-Time Procedural Placement in 'Horizon: Zero Dawn'." GDC 2017. Guerrilla Games publication page "GPU-Based Procedural Placement in Horizon Zero Dawn" (dated 1 March 2017, with the GDC 2017 slides as PDF and PPT, read 29 September 2026). The page summary describes a GPU-based system that builds the world around the player at run time, including sounds, effects, wildlife and gameplay elements, from data artists can modify. No figures on time saved are claimed here.
- Munroe, R. "Is It Worth the Time?" xkcd comic 1205 (read September 2026). A table of how long you can spend making a routine task more efficient before you lose time over five years, by task frequency and time saved.
- The *Emberfall* hours, the bounty tool estimate and the brush tool are a constructed teaching example continuing weeks 6, 9 and 11. They are not data from a real team. `H = 8` for PR401 is the course convention from week 1.
