# PR401 · Week 09 — Content Plan

**Why this matters:** In week 1 you checked that your pitch could hold the median player for four weeks, using one authoring ratio and one replay multiplier for the whole game. Now you have measured costs from two prototypes, and they differ by a factor of four between content types. This week you turn "enough content" into a costed list, choose what to build by what each team hour buys in play, and find out which one claim the whole live period depends on.

**You will be able to:**
- Build a content inventory in units (quests, recipes, encounters, events) with a measured cost, a first-pass length and a replay multiplier for each.
- Compute the yield of each unit, hours of play per team hour, and fill a content budget in yield order after the must-haves.
- Compute the drought for each player type from the chosen mix, and its sensitivity to the replay claims.
- Schedule content between launch and the PR402 patch week so the drop lands before the median player runs out.

**Before class:** Reread [MMO306 week 1](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w01-the-content-treadmill-production-vs-consumption.md), section 1 (the two clocks), 10 minutes. Read [MMO306 week 13](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w13-content-budgets-and-cadence-planning.md), sections 1 and 2 (budgets in team-days and the date you can promise), 25 minutes. Pull the actual hours spent on every content piece in prototypes 1 and 2 from your tracker, and the play time testers spent on each.

**Prerequisites from earlier courses:** [Week 1 of this course](w01-pitch-development.md) (`C`, `r`, `k` and the locust ratio for the pitch). [Week 6](w06-greenlight-review.md) (the plan ratio `R` and the cut list). [MMO306 week 9](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w09-procedural-and-systemic-content.md) (systemic content). [MMO306 week 12](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w12-content-tooling-and-pipelines.md) (content pipelines). [GD202 week 6](../../GD202-narrative-and-quest-design/lectures/w06-quest-anatomy-hook-objective-complication-reward.md) (quest anatomy). Looking ahead, [MMO406 week 10](../../MMO406-worldbuilding-and-lore-for-persistent-worlds/lectures/w10-expansion-planning.md) (next semester) covers planning lore across drops.

---

## 1. From one ratio to a content inventory

Week 1 used one **authoring ratio** `k`, team hours per hour of play, and one **replay multiplier** `r` for the whole pitch. That was right for comparing pitches. It is wrong for planning, because content types differ so much. A fetch quest and a boss encounter can both hold a player for 15 minutes. The boss costs several times as much to build and gets played ten times as often.

So list the content as **units**. A unit is a piece a designer can build, test and ship on its own: a quest, a set of recipes, a bounty rotation, an encounter, an event. For each unit record:

- **Cost** in estimated team hours, including art, design, scripting and test.
- **First-pass length** `c`, the hours a median player spends on it the first time. Measure it from playtests, not from the designer's own run, which is always faster.
- **Replay multiplier** `r`, how many first-pass lengths a median player will spend on it in the live period. A story quest is 1. A dungeon with a loot table might be 10.
- **Evidence** for `c` and `r`: a prototype number with its tester count, a comparable, or "assumed".
- **Must-have** or not. Onboarding content is a must-have whatever its yield, because every player passes through it.

## 2. Measure your authoring ratios

The prototypes built in weeks 4 and 5 are the best cost data you have. For each content type the team built, divide team hours by the median first-pass play time. *Emberfall*'s numbers, from prototypes 1 and 2 and the R6 quest-area test in week 4:

| Content type | Team hours | Median first pass | Measured `k` (team h per play h) |
|---|---|---|---|
| Tutorial step (one, with dialogue and a crafting goal) | 6 | 12 minutes | 30 |
| Recipe set and gathering nodes | 40 | 1 hour | 40 |
| Bounty rotation (12 bounties) | 30 | 30 minutes | 60 |
| Dungeon (a collapsed mine, one guardian) | 60 | 30 minutes | 120 |

Week 1 assumed `k = 20` for everything. The measured values are all higher, and the dungeon is six times higher. Week 4's R6 test measured the first row, and the claim of 20 did not survive it. That is normal. Designers estimate the build and forget the tuning, the bugs and the second pass after testers get lost. PR101 week 6 showed the same effect on tasks. Use the measured values from now on, and scale estimates by your plan ratio `R` from week 6 when you compare them with capacity.

## 3. Worked example: what should the content hours buy?

### The hook

Two long-running MMOs show the two ends of content planning.

Guild Wars 2's first Living World season ran from January 2013 to March 2014 as small story and event releases arriving every two weeks. Most of it was temporary: when the next release came, the previous one left the game, so a player who missed two weeks missed the story.

Final Fantasy XIV, since its Endwalker expansion, has released major patches on a 4.5-month (19-week) interval. Each is large and much of its end-game is gated per week, so players stretch a big drop across months.

Both studios were solving the same equation with different terms. One chose a small `c` and a short cadence. The other chose a large `c`, large `r` and a gate. Your capstone has one launch and one patch week. Which terms can you afford?

### The model

```
effective hours of a unit     E_i = c_i × r_i
yield of a unit               y_i = E_i / cost_i                  play hours per team hour
content the median needs      E_need = h × weeks                  hours of play in the live period
drought for a player type     D = max(0, h × weeks − Σ E_i) / h    weeks with nothing new
```

Fill the budget in this order: every must-have first, then the rest in descending yield until the next unit would not fit. `h` and weeks come from week 1: the median plays 5 hours a week for 4 weeks, so `E_need = 20` hours.

### Numbers you can check

Week 6's feature lines mixed system work with content, and put the dungeon's instance and combat in the foundation line. Split out, the content part of *Emberfall*'s plan (tutorial steps, recipes, contracts, encounters) comes to 180 estimated team hours. That is the content budget. The candidates:

| Unit | Cost (h) | `c` (h) | `r` | `E` (h) | Yield `y` | Evidence for `r` |
|---|---|---|---|---|---|---|
| Tutorial quest chain (6 steps), must-have | 36 | 1.2 | 1 | 1.2 | 0.033 | Played once |
| Recipe set and gathering nodes | 40 | 1.0 | 8 | 8.0 | 0.200 | Assumed in the week 1 pitch; prototype 1 showed 5 of 8 testers repeating the loop twice, not how many times it holds |
| Waystation contract rotation (12) | 30 | 0.5 | 6 | 3.0 | 0.100 | Prototype 2, testers repeated contracts 3 times in one session |
| Dungeon, one guardian | 60 | 0.5 | 10 | 5.0 | 0.083 | Assumed from loot table size |
| Ash-storm event (valley-wide) | 30 | 0.25 | 8 | 2.0 | 0.067 | Assumed |
| Town rumour quests (10) | 60 | 2.0 | 1 | 2.0 | 0.033 | Played once |

Fill the budget:

```
tutorial quest chain (must-have)  36 h    E = 1.2    running 36,  E total 1.2
recipes and nodes   (y = 0.200)   40 h    E = 8.0    running 76,  E total 9.2
contract rotation   (y = 0.100)   30 h    E = 3.0    running 106, E total 12.2
dungeon             (y = 0.083)   60 h    E = 5.0    running 166, E total 17.2
ash-storm event    (y = 0.067)   30 h    would reach 196 > 180, skip
town rumour quests  (y = 0.033)   60 h    skip
```

The median needs 20 hours and gets 17.2. Drought: `(20 − 17.2) / 5 = 0.56` weeks, about 3.9 days at the end of the live period.

The team has 14 hours left. Two options:

- **Add 10 hours of loot table depth to the dungeon**, raising its `r` from 10 to 14 (another claim to test). `E` for the dungeon becomes 7.0, the total 19.2, and the drought `(20 − 19.2) / 5 = 0.16` weeks, about 1.1 days. Budget used: 176 of 180.
- **Build the ash-storm event in PR402 for the patch week** (week 12 of PR402, the fourth week of the live period). It adds 2.0 hours of play for the median player, just as they would run out, and its cost comes out of the live-ops budget, not the pre-launch one.

*Emberfall* does both. On paper the median player now has something new all four weeks.

Now check the other players and the claims:

| Case | `Σ E` | Median drought (days) | Keen (12 h/week) runs out on day |
|---|---|---|---|
| Plan as above, before the patch | 19.2 | 1.1 | 11.2 |
| Recipe `r` is 4, not 8 | 15.2 | 6.7 | 8.9 |
| Recipe `r` is 4 and dungeon `r` is 10 | 13.2 | 9.5 | 7.7 |

Check one cell: with recipe `r = 4`, `Σ E = 19.2 − 4.0 = 15.2`. Median drought is `(20 − 15.2) / 5 = 0.96` weeks, or 6.7 days. Keen runs out at `15.2 / 12 = 1.27` weeks, day 8.9.

Read it.

- **One claim carries the plan.** The recipe set is 42% of the median player's content (8 of 19.2 hours) and its `r = 8` is assumed. If it is 4, the median has a week with nothing new. Testing that claim is the first job of vertical slice sprint 1 in week 12.
- **Keen players run out in week 2 whatever you do with 180 hours.** They need 48 hours of play. The plan offers 19.2. Only systems with very high `r` or a patch in week 2 can hold them. That is *Emberfall*'s real bet: town raids, bounties on players and trade at the stalls (pillars P2 and P3) have to hold keen players, because authored content cannot. Decide now whether you are designing for them, as week 1 asked, and say so in the plan.
- **Played-once content loses on yield, and you keep the tutorial anyway.** Every player passes through it. The rumour quests are the first thing to add if a claim fails in the good direction and hours free up.
- **The plan still has a quest chain.** The tutorial quest chain is six quests with dialogue, objectives and a reward (the player's first crafted tool). It is the only quest chain *Emberfall* launches with, so it is the quest chain the week 12 vertical slice builds, and it proves the quest data format for anything added later.

### Cross-game recognition

- **Guild Wars 2, Living World season 1.** In these terms each release had a small `E` and a two-week cadence, and was then removed. The studio chose to pay for many small drops instead of high `r`, which keeps a two-week drought from ever opening but needs a production line that never stops.
- **Final Fantasy XIV since Endwalker.** A 19-week cadence needs `Σ E` large enough to hold a median player for 19 weeks. Weekly gates on end-game loot raise the effective `r` of each encounter, as MMO306 week 1 showed, so a finite drop lasts until the next one.
- **MMO306 week 13's promise date** is the same model on the calendar: how late can a drop be before the median's drought opens? *Emberfall*'s ash-storm event in the patch week is a one-drop version of that plan.

### Eyes-open judgment

Yield ranks units by play hours, not by how good those hours are. Ten runs of a dungeon with a loot table count the same as ten hours of story. If the tenth run is a grind, `r` was not 10, it was a chore. Test `r` by watching whether testers choose to repeat, not whether they can.

Yield also ignores dependencies. The dungeon needs combat to be finished and its loot table needs the crafting pipeline, because in *Emberfall* the loot is materials, not gear. A unit with high yield that depends on a system at risk in the week 6 register is riskier than its yield suggests. Put the dependency in the plan.

And beware the unit that is cheap because it is unfinished. A recipe set costed at 40 hours with no art pass will cost 60 after one. Cost units the way they will ship.

## 4. Schedule the content

A content plan is a list and a calendar. Put each chosen unit into the sprints of weeks 12 and 13 and PR402 weeks 1 to 8, with its dependencies. Three rules keep it honest:

1. **Must-haves first.** The tutorial quest chain goes into vertical slice sprint 1, because the slice must be playable from the start and its quest chain element (week 12) is this unit.
2. **Test the riskiest `r` early.** The unit whose replay claim carries the most of `Σ E` gets built in a testable form first, even rough.
3. **Hold one unit for the patch week.** It is your insurance against the drought and your practice for PR402's patch.

## Studio session plan

Week 9 meeting, 3 hours.

| Time | Activity | Output |
|---|---|---|
| 0:00-0:25 | Measured `k` per content type from prototype data | Section 2 table for your team |
| 0:25-1:05 | Content inventory: every candidate unit with cost, `c`, `r`, evidence and must-have flag (lab 09) | `content.csv` draft |
| 1:05-1:15 | Break | |
| 1:15-1:45 | Fill the budget in yield order, compute droughts, run the checker | Checker output |
| 1:45-2:15 | Sensitivity: halve the largest assumed `r` and recompute; choose the test that would settle it | One named claim and its test |
| 2:15-2:45 | Calendar: units into sprints, dependencies drawn, one unit held for the patch week | Content calendar |
| 2:45-3:00 | Lore check with the narrative lead: does the order of drops tell the story in order? (MMO406 week 10) | Notes for the setting bible |

## Deliverables

Due at the start of week 10, in `docs/content-plan.md` and `preproduction/week09/`:

1. **Content inventory and plan** in the [lab 09](../labs/lab09.md) format. The checker `content_yield.py` must print `PASS`.
2. **Measured `k` table** for every content type you prototyped, with hours and play times.
3. **Sensitivity paragraph**: the claim that carries the most of `Σ E`, what the drought is if it halves, and the test in vertical slice sprint 1 that will settle it.
4. **Content calendar** across the build window with dependencies and the patch-week unit.

## Common failure modes

- **Costing from the pitch.** Using week 1's `k = 20` after measuring 30 to 120. The plan then promises three times the content the team can make.
- **Designer play time as `c`.** The designer finishes the dungeon in 12 minutes. Testers take 30. Use tester medians.
- **Replay by hope.** `r = 10` with no evidence. Mark it assumed and plan the test.
- **All story.** Quests are satisfying to write and the lowest yield on the list, and *Emberfall*'s anti-pillar rules out a solo campaign anyway. Keep the must-haves and let yield choose the rest.
- **No patch-week unit.** The live period has one planned drop. Without a unit ready for it, PR402's patch week will be bug fixes only.
- **Keen players ignored by accident.** Decide deliberately whether to hold them, and write the decision down.

## Review checklist

The instructor checks in the submission and at the week 10 stand-up:

- [ ] Every content type prototyped has a measured `k` with its hours and play time.
- [ ] Every unit has cost, `c`, `r`, evidence and a must-have flag.
- [ ] Must-haves are included, and the rest are chosen in yield order within budget, or departures are explained.
- [ ] `content_yield.py` prints `PASS` and the declared totals match.
- [ ] Median drought is computed, and the sensitivity case for the largest assumed `r` is shown.
- [ ] The test for the load-bearing `r` is scheduled in vertical slice sprint 1.
- [ ] The calendar places every unit in a sprint with its dependencies, and one unit is held for the patch week.

## Sources

- Guild Wars 2 Wiki, "Living World Season 1" (accessed September 2026). Ran from 28 January 2013 to 18 March 2014 in temporary, bi-weekly installments; key moments re-released as permanent content in 2022. https://wiki.guildwars2.com/wiki/Living_World_Season_1
- Final Fantasy XIV Online Wiki (consolegameswiki), "Patches" (accessed September 2026). Major patches on a 4.5-month (19-week) interval since Endwalker; Dawntrail patches 7.0 on 2 July 2024, 7.1 on 12 November 2024, 7.2 on 25 March 2025 and 7.3 on 5 August 2025. https://ffxiv.consolegameswiki.com/wiki/Patches
- MMO306 weeks 1 and 13 of this program, for the exhaustion-time model, weekly gates and cadence planning.
- The *Emberfall* costs, play times, replay values and the 180-hour budget are invented for teaching and continue weeks 1 to 8. The player types and the four-week live period come from week 1 of this course.
