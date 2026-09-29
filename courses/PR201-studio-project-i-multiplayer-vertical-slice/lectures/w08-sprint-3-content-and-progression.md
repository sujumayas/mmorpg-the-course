# PR201 · Week 08 — Sprint 3: Content and Progression

**Why this matters:** After sprint 2 you have one room where combat works. A vertical slice needs a session: 15 to 25 minutes in which a new player fights, levels up and reaches an ending. That session is built from content, and content is where student teams most often run out of time, because nobody measured what one room costs before promising six.

**You will be able to:**
- Measure the cost of one unit of content from sprint 2, compare its estimate ratio with the team's, and correct content estimates only by the difference.
- Compute how much XP a progression curve demands and how much the planned content supplies.
- Build a content budget that balances XP, play time and production hours, and choose between cutting content and retuning the curve.
- Plan the server-side progression stories so XP and levels are authoritative and persistent.

**Before class:** Reread [GD203 week 7, section 4](../../GD203-combat-and-progression-design/lectures/w07-xp-curves.md) on designing an XP curve backwards from a play-time target. Bring your sprint 2 time log for the one room or area you finished, broken down by discipline, and your week 7 playtest findings with priorities.

**Prerequisites from earlier courses:** [PR101 week 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md) (vertical slice, cut lists and cut triggers). [PR101 week 6](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) (estimate ratios). [GD203 week 7](../../GD203-combat-and-progression-design/lectures/w07-xp-curves.md) (XP curves and income). [GD203 week 11](../../GD203-combat-and-progression-design/lectures/w11-spreadsheet-balancing-workshop.md) (balance spreadsheets). [DB201 week 5, transactions](../../DB201-data-persistence-and-telemetry/lectures/w05-transactions-and-acid.md) and [DB201 week 6, the duplication bug](../../DB201-data-persistence-and-telemetry/lectures/w06-race-conditions-and-the-duplication-bug.md).

---

## 1. Sprint 3's goal: from one room to one session

Sprint 3 runs over weeks 8 and 9 and ends at the week 9 review. The alpha milestone follows in week 10. A reasonable goal for the *Hollowmarch* sample team reads: **a party of three can play from the entrance to the boss in about 20 minutes, reach level 5 on the way, and log out and back in with their level intact.**

That sentence ties three plans together.

- A **content plan**: how many rooms, encounters and a boss.
- A **progression plan**: how much XP each level needs and where it comes from.
- A **production plan**: how many hours each piece costs and who builds it.

Most teams write the three separately. The designer writes a level list, a programmer writes the XP system and someone estimates hours at the end. The three rarely agree. This week's worked example makes them agree on one sheet, before anyone opens the editor.

The team also carries work in from week 7. The playtest produced P1 and P2 bugs, the ranged ability left out of sprint 2 is waiting, and so are the two sprint 1 tasks that week 6 moved here (enemy state packing and the R6 export spike). Reserve hours for the bugs first: at least the estimates of every P1 and P2 bug the playtest left open.

## 2. Progression is a server feature

In a single-player game, XP is a number in a save file. In your slice it is shared, persistent state, and three rules apply.

**The server awards XP.** Clients never send "I gained 60 XP". The server grants XP when it confirms the kill, exactly as it applied damage in sprint 2. Tag every grant with the reason (`kill`, `quest`, `boss`) so the telemetry you add in week 11 can count sources.

**Level-ups are transactions.** Writing the new XP total, the new level and any stat changes is one database transaction, as in [DB201 week 5](../../DB201-data-persistence-and-telemetry/lectures/w05-transactions-and-acid.md). A crash in the middle must leave the character at the old level or the new one, never at a mixture. Your week 3 TDD saved the character to a file with an atomic write, which already gives that guarantee for one file. This sprint moves the save into the database, because loot grants and level-ups now touch several records at once, and it becomes version 2 of TDD section 11, marked at alpha.

**Rewards are granted once.** A quest turn-in that two party members trigger in the same tick, or a boss kill that a reconnecting client reports again, is the duplication bug from [DB201 week 6](../../DB201-data-persistence-and-telemetry/lectures/w06-race-conditions-and-the-duplication-bug.md) in a new costume. Give each grant an id and make the server ignore a grant it has already applied.

Put these rules in the acceptance criteria of the progression stories. They are the difference between a level-up that works at the review and one that survives the alpha week's reconnect tests.

## 3. The unit of content, and what it really costs

To plan content you need a unit, a thing you build many times with roughly the same steps. For a dungeon slice the natural unit is the **encounter room**. It is a greyboxed space, dressed with art, populated with two enemy packs, scripted, given ambient sound and tested in a networked build.

Sprint 2 built one room for the combat loop. That room is your best estimate for every other room, far better than a guess, because it went through every step of your real pipeline. [PR101 week 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md) made the same point about dressing the first jam level.

Log the room's cost by step and discipline, then compare with the estimate:

| Step | Discipline | Estimate (h) | Actual (h) |
|---|---|---|---|
| Greybox layout | Design | 1.5 | 2 |
| Set dressing | Art | 3 | 4 |
| Pack placement and tuning | Design | 1.5 | 2 |
| Ambient sound and triggers | Audio | 0.5 | 0.5 |
| Networked test pass | All | 1 | 1.5 |
| **Total** | | **7.5** | **10** |

The room's **estimate ratio** is `r_content = 10 / 7.5 = 1.33`. [PR101 week 6](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w06-estimation-and-why-it-fails.md) showed that teams are consistently wrong in the same direction. What you do with the ratio depends on the unit you plan in, which the next subsection settles.

Two other units are worth defining.

- A **remix room** reuses a finished room's art set with a new layout and new pack placement. The team estimates 3.75 hours.
- The **boss room** is a one-off, estimated at 9 hours.

Remixing is the cheapest content most teams have. It is the standard way to stretch a small art set. A slice does not need six unique rooms. It needs rooms that each teach or test something different.

### Units: estimate-hours, as in every other week

Weeks 4 to 6 planned in estimated hours against `f × U`. Sprint 3 does the same. There are two ways to turn a ratio into a capacity, and they don't agree.

```
ratio route:  capacity = U / r                    every useful hour lands on a task
focus route:  capacity = f × U,  f = (A_done / U) / r
```

The focus route is the one sprint 1 measured. Of 75 useful hours, only `A_done = 55` were logged on tasks that finished, a share of 0.733. The rest went to meetings, blocked time and tasks that carried over. So `f = 0.733 / 1.28 = 0.573`, the week 5 figure. The ratio route keeps the 1.28 and drops the 0.733. For sprint 3 it offers `81 / 1.28 = 63` estimate-hours, while the focus route offers 46. The 17-hour difference is time that never lands on a finished task, and the ratio route pretends it does.

`f` already contains the team's average overrun, `r_team = 1.28` from week 5. So don't multiply content estimates by the full 1.33. Multiply them only by how much worse content overruns than everything else:

```
k = r_content / r_team = 1.33 / 1.28 = 1.04
```

For *Hollowmarch* content overruns about like the rest of the work, and `k` barely moves the numbers. For a team whose room took 12 hours against 7.5 (`r_content = 1.6`), `k = 1.25`, and ignoring it would hide a quarter of the content bill.

## 4. Worked example: the curve writes a content bill

### The hook

In *Old School RuneScape*, reaching level 99 in a skill takes 13,034,431 XP. Level 92 takes 6,517,253, almost exactly half. The last seven levels hold as much XP as the first ninety-one, because the curve roughly doubles the XP per level every seven levels. Players know this as "92 is half of 99".

That is a design choice about the curve. It is also a promise about content. Somewhere in the game there must be enough things to do to hand out thirteen million XP, and the top of the curve needs as much of them as the bottom. Every XP curve writes a bill that content has to pay. Your curve is five levels long and your content is a handful of rooms, but the bill is the same kind of number, and you can compute it this afternoon.

### The model

Three balances must all hold on one sheet.

```
XP balance:     Σ XP from content      ≥  XP to reach target level
Time balance:   Σ minutes of content   ≈  target session length (± 10%)
Hours balance:  Σ build hours of new content  ≤  content capacity
```

The XP side comes from the curve and the rewards:

```
XP to reach level L = Σ (XP to next level) for levels 1 to L − 1
XP from content     = packs × XP per pack + quest XP + boss XP
```

Every hour on this sheet is an estimated hour. Content build hours are raw estimates times `k` from section 3. Content capacity is what is left of the sprint forecast after the bug reserve and the system stories, both at their estimates:

```
forecast         = f × U                  (yesterday's weather, week 6)
content capacity = forecast − bug reserve − system stories
content hours    = k × Σ estimates of new content
```

If the three balances cannot all hold, you have exactly three levers. You can cut content, cheapen content (remix instead of new), or retune the curve or rewards. The first two act on hours. The third acts on XP, and it costs a spreadsheet edit.

### Numbers you can check

The designer's curve for *Hollowmarch* multiplies each step by about 1.5:

| Level | XP to next level | Cumulative XP to reach next level |
|---|---|---|
| 1 → 2 | 100 | 100 |
| 2 → 3 | 150 | 250 |
| 3 → 4 | 225 | 475 |
| 4 → 5 | 340 | 815 |

Reaching level 5 takes 815 XP. Rewards: 60 XP per pack (each player receives the full amount), 120 XP for the quest turn-in, 200 XP for the boss. A pack takes about 2 minutes to clear and walk past, the boss about 3 minutes, and the quest giver and travel about 3 minutes.

Capacity for sprint 3, in estimated hours:

| Item | Estimate-hours |
|---|---|
| Forecast: `f = (43 + 46) / (75 + 81) = 0.571` over sprints 1 and 2, times `U = 81`, is 46.2, rounded down | 46 |
| Bug reserve: the three P1 and P2 bugs from the week 7 playtest, at their estimates | −5 |
| XP grants and level-up with fixed stat gains, on the server | −4 |
| Persistence of level and XP, transactional | −4 |
| XP bar, level-up UI and sound | −2 |
| Ranged bolt (C6), thin version with no lag compensation, re-estimated from 10 | −5 |
| **Content capacity** | **26** |

The three progression stories total 10 hours, the figure week 5 gave F6 when talent choice became fixed stat gains. The sprint 1 carry-over (enemy packing, 4, and the R6 spike, 2) waits below the line. One grunt type fits the default synchronizer, and the lab server runs windowed.

**Plan A, the designer's first list.** Five encounter rooms (room 1 exists from sprint 2, so four are new) and a boss room.

```
XP:     10 packs × 60 + 120 + 200 = 920      ≥ 815   holds
Time:   10 × 2 + 3 + 3            = 26 min   target 20, +30%   fails
Hours:  1.04 × (4 × 7.5 + 9)     = 40.6 h   capacity 26       fails
```

Plan A overshoots the session by six minutes and the budget by 15 hours, more than half again what the team has. Built anyway, it ends week 9 with two undressed rooms and no boss.

**Plan B, remix and retune.** Keep room 1. Build one new room and two remixes, and the boss room.

```
Hours:  1.04 × (7.5 + 2 × 3.75 + 9) = 25.0 h  capacity 26      holds
Time:   8 × 2 + 3 + 3             = 22 min   target 20, +10%   holds
XP:     8 × 60 + 120 + 200        = 800      need 815          short by 15
```

Plan B misses level 5 by 15 XP. The party would reach the boss at level 4 with 800 of 815. There are two cheap fixes:

- lower the last step of the curve from 340 to 325, so level 5 needs exactly 800; or
- raise pack XP from 60 to 62, so content supplies `8 × 62 + 320 = 816`.

Both are a one-cell edit. The team picks the curve change, because players will hit the level-up at the boss kill, which is the moment the designer wanted. The alternative, a fifth room to find 15 XP, would cost 4 to 8 estimate-hours the team does not have.

| | Plan A | Plan B (retuned) |
|---|---|---|
| Rooms (new + remix) | 4 + 0 | 1 + 2 |
| XP supplied / needed | 920 / 815 | 800 / 800 |
| Session minutes | 26 | 22 |
| Build estimate-hours / capacity | 40.6 / 26 | 25.0 / 26 |

Plan B leaves 1 hour of slack, which is thin. The team writes a cut trigger in advance, in the style of [PR101 week 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md). If the new room is not dressed by the end of week 8, the second remix is cut, and pack XP rises to 75 so that six packs still supply `6 × 75 + 320 = 770`. The curve's last step then drops to 295 to match (`100 + 150 + 225 + 295 = 770`). The cut and the retune are decided now, while nobody is tired.

### Cross-game recognition

The same bill appears elsewhere. In PR101 week 4, the jam team learned that dressing its first level took 7 hours and used that to decide whether levels 2 and 3 fitted. That is section 3's unit cost at jam scale. In GD203 week 7, the XP curve was designed backwards from a play-time target, which is the time balance above written as a curve. And content that is promised before it is costed has a famous failure mode. Blizzard announced a Dance Studio for *World of Warcraft: Wrath of the Lich King* at BlizzCon 2007, postponed it several times over 2008 and 2009, and in 2013 described it as shelved rather than cancelled. A curve, a feature list or an announcement is a bill. Somebody has to pay it in hours.

### Eyes-open judgment

The model is deliberately simple. It assumes every pack gives the same XP, every room takes two minutes, and all three players stay together. A party that wipes on a pack spends longer and earns nothing, so real sessions run long, not short. Keep the time balance a little under target for that reason.

Retuning the curve is cheap, but it is not free. A slice's curve is a sample of the full game's curve, and a curve bent to fit four rooms may not scale. Write the retune down as a slice decision in the GDD, so nobody later mistakes it for the intended long-term shape. And remixing has a limit. Players notice the same art set by the third room. Two remixes of one set is usually fine. Four is a corridor.

The deeper point is where the capacity comes from. Suppose the team had planned in actual hours by the ratio route: every content and system estimate times 1.33, against all 81 useful hours. The bug reserve and systems cost `20 × 1.33 = 26.7` actual hours, leaving 54.3, and plan A costs `39 × 1.33 = 52`. Plan A fits with 2 hours spare, and the team builds five rooms. The focus route says plan A is 15 estimate-hours over. Sprint 1 already showed which route is right: a quarter of the useful hours never reached a finished task. Planning in the same unit as weeks 4 to 6 is what makes the problem visible in week 8 instead of week 9.

## 5. Running content in a sprint

Content has a different rhythm from features, so run it differently.

**Pipeline, not handoffs.** Rooms move through greybox, dress, populate, sound and test. Put each room on the board as one story with those steps as subtasks, and limit rooms in progress to two. A room is done when it plays in a networked build, not when it is dressed.

**Greybox all rooms first.** Playable greyboxes let the designer check the time balance in week 8 with real walking and real fights. If the session runs 28 minutes in greybox, cut before the artist dresses a room that will not ship.

**Content lock before alpha.** Agree now that no new rooms enter after the week 9 review. Week 10 is for making what exists work, not adding more.

## Studio session plan

Week 8 meeting, 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:20 | Briefing: sections 1 to 3; the three balances | |
| 0:20-0:50 | Measure the unit: each team fills the room cost table from its sprint 2 log and computes the estimate ratio | Ratio and corrected unit costs |
| 0:50-1:30 | Content budget: fill the lab 08 sheet with your curve, rewards, rooms and capacity; run `check_content_budget.py` | A plan that passes all three balances, or a list of the levers you will pull |
| 1:30-1:40 | Break | |
| 1:40-2:10 | Sprint 3 planning: bug reserve first, then system stories with the section 2 rules, then content to the line | Ordered backlog, line drawn |
| 2:10-2:25 | Write the cut trigger and its retune in advance | Trigger in the sprint plan |
| 2:25-2:50 | Instructor round: 5 minutes per team on the budget sheet | Notes |
| 2:50-3:00 | Greybox the first new room | First commit |

## Deliverables

Due at the end of the week 8 meeting:

1. **Content budget** in the lab 08 format ([`labs/lab08.md`](../labs/lab08.md)): the unit cost table with the estimate ratio, the curve, the reward table, the capacity table, and the chosen plan with all three balances. Checked with `check_content_budget.py`, which must report all three balances holding.
2. **Sprint 3 plan**: ordered backlog with bug reserve, system stories and content stories, the line, the sprint goal and the cut trigger.
3. **Progression acceptance criteria**: server-awarded XP with reason tags, level-up as one transaction, grant ids for idempotent rewards.

All rooms should be greyboxed and playable by the end of week 8. The sprint 3 increment is due as a tagged build at the week 9 review.

## Common failure modes

- **Estimating rooms from imagination.** Nobody built a real room first, so nobody knows whether content overruns more than the rest. Measure one, and compute `k`.
- **Mixing units.** Content in actual hours, capacity in estimated hours, or estimates times the ratio against all useful hours. Plan in estimate-hours against `f × U`, as every other week.
- **Curve and content designed apart.** The level cap is unreachable, or reached in room 2. Put both on one sheet.
- **Building to fill hours instead of the goal.** A sixth room because the artist had time, while the boss has no death sound. Content serves the session goal.
- **Client-side XP.** Level-ups work in the demo and duplicate on reconnect. Apply DB201's rules.
- **Dressing before the time check.** Rooms get polished, then the greybox session turns out to run 30 minutes. Greybox everything first.
- **No trigger.** The new room runs late, nobody decides, and week 9 arrives with half of everything. Write the cut and its retune now.

## Review checklist

The instructor checks at the week 8 meeting and at the week 9 review:

- [ ] The unit cost is measured from sprint 2's real log, with an estimate ratio, and `k = r_content / r_team` is applied to every new content estimate.
- [ ] Capacity is the forecast `f × U` in estimate-hours, and every system story is at its estimate.
- [ ] The budget sheet shows the XP, time and hours balances with numbers, and the checker reports all three holding.
- [ ] Where a balance failed, the team names the lever it pulled and why (cut, remix or retune).
- [ ] Bug reserve is set before content, and the playtest's P1 bugs are on the committed list.
- [ ] Progression stories state server authority, one transaction per level-up and idempotent grants.
- [ ] A cut trigger with its retune is written with a date.
- [ ] At the week 9 review: every committed room plays in the networked build, and a fresh character reaches the target level in the planned session.

## Sources

- Old School RuneScape Wiki, "Experience" (current game, accessed September 2026). 13,034,431 XP for level 99, 6,517,253 for level 92, and the "92 is half of 99" rule; XP per level roughly doubling every seven levels from about level 30.
- Warcraft Wiki, "Dance Studio" (warcraft.wiki.gg, accessed September 2026), as cited in PR101 week 4. Announced at BlizzCon 2007 for *Wrath of the Lich King*; postponement statements in 2008 and 2009; described as shelved, not cancelled, in August 2013.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Chapters on progression and curves.
- Keith, C. (2020). *Agile Game Development: Build, Play, Repeat* (2nd ed.). Addison-Wesley. Background on production phases and content planning in agile game teams.
- The *Hollowmarch* curve, rewards, room costs and capacity table are invented for teaching.
