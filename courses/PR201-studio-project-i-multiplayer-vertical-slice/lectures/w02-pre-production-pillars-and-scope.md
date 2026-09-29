# PR201 · Week 02 — Pre-production: Pillars and Scope

**Why this matters:** Last week you checked that a pitch fits your team in rough hours. This week you turn it into a feature list with a line across it. Everything above the line is the slice you promise, and everything below it is work you have agreed not to do. The line is cheap to move now and expensive in week 9, and your pillars decide where it goes.

**You will be able to:**
- Write three design pillars for a multiplayer slice, at least one of them about players together, and map every candidate feature to them.
- Rank features by pillar support per hour and place the cut line inside your plannable hours.
- Check every pillar's support after the cut, and repair a fragile pillar with a swap that keeps the total inside the budget.
- Compute how much estimate overrun the must tier survives, and shrink it if the answer is below 2.

**Before class:** [GD101 week 14](../../GD101-introduction-to-game-design/lectures/w14-design-documents-one-pagers-and-pitch.md), section 2 (the pillar-mechanic map, support and the swap test). [PR101 week 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md), sections 2 and 5 (the cut line, `m_max` and cut triggers). Bring your week 1 fit sheet and your team's plannable hours.

**Prerequisites from earlier courses:** [GD101 week 14](../../GD101-introduction-to-game-design/lectures/w14-design-documents-one-pagers-and-pitch.md) for pillars and the pillar-mechanic map. [PR101 week 4](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w04-scope-mvp-vertical-slice-cut-lists.md) for MoSCoW tiers and the overrun a plan survives. [PR101 week 5](../../PR101-game-production-i-teams-scope-and-the-game-jam/lectures/w05-agile-and-scrum-adapted-for-games.md), section 3, for pre-production versus production. [GD201 week 11](../../GD201-level-and-world-design/lectures/w11-shared-spaces-designing-for-many-players.md) if your zone is shared by several players at once.

---

## 1. What pre-production is for

**Pre-production** is the part of a project where the team is still finding out what the game is. **Production** is the part where the team knows and is making it. PR101 week 5 put it as "pre-production is for questions, production is for content". Mark Cerny's "Method", which he set out while consulting for Sony's first-party studios in 2002, ends pre-production with a "publishable first playable": a small piece of the game at shipping quality that proves the idea works. Only then does full production start.

Your course is too short for a long pre-production. You get three weeks, and they produce three documents that together answer "what is the game":

| Week | Document | Question it answers |
|---|---|---|
| 1 | Pitch and fit sheet | Is this game something our team can build? |
| 2 | Pillars and scope sheet | Which features, in which order, and which ones we won't build |
| 3 | Technical design document | How we will build it, and what might stop us |

The slice itself plays the role of Cerny's first playable. The scope sheet decides what goes into it.

## 2. Worked example: where the cut line goes, and what it leaves standing

### The hook

BioWare's *Anthem* was in development from 2012 and released in February 2019. Jason Schreier's 2019 report for *Kotaku*, summarized on Wikipedia, describes flying being added and removed several times, and developers saying most of the game was built in the year before release. Whatever else went wrong, a team that is still deciding whether its signature feature exists after five years has not finished pre-production. A cut line drawn late is drawn by the calendar.

You have fifteen weeks, not seven years, so the same mistake costs you a milestone instead of a studio's reputation. The fix is to decide in week 2, with numbers, and to write down the rule you used.

### The model

List every feature you might build. For each feature `f`, estimate its hours `e_f` across all disciplines, and mark which pillars it supports, as in GD101's map (`L[f, p] = 1` if feature `f` serves pillar `p`). Then:

```
value_f   = Σ over pillars p of L[f, p]          how many pillars f holds up
density_f = value_f / e_f                        pillar support per hour
room      = P − S_must                           hours left after the must tier
```

1. Put the **must tier** first. It is the core loop without which nobody can play the slice at all. It is not ranked, because nothing else works without it.
2. Rank every other feature by `density_f`, highest first. Features with `value_f = 0` go straight to the cut list.
3. Walk down the ranking and keep each feature if the running total still fits inside `room`. A feature that doesn't fit goes to the cut list, but keep walking, because a smaller feature further down may still fit. The **cut line** sits under the last feature kept.
4. Recompute `support(p) = Σ over kept features of L[f, p]` for each pillar. A pillar with support 1 is **fragile**. One cut or failed feature and it has nothing under it. Require `support(p) ≥ 2`.
5. Check the must tier against overrun, as in PR101 week 4: `m_max = C / S_must`, where `C` is useful hours before the buffer. For a first-time team, require `m_max ≥ 2`, meaning the must tier still finishes if every task takes twice its estimate.

`P` is plannable hours from week 1. `S_must` is the must tier's estimate.

### Numbers you can check

The *Hollowmarch* team from week 1 has `C = 445.5` useful hours (six people at 74.25) and `P = 311.85`, rounded to 312. Their pillars are:

- **P1, Hold the line together.** Each role protects the others, and a fight is lost by the group, not by one player.
- **P2, Every fight reads.** Players can see an attack coming and tell whether their own hit landed.
- **P3, Leave stronger.** Players leave the slice with something they chose.

The must tier is the core loop: join a server, move, attack, one enemy type, die and respawn, one graybox zone. It is estimated at 150 hours across all disciplines. So `room = 312 − 150 = 162` hours, and `m_max = 445.5 / 150 = 2.97`, which passes.

The candidate features, ranked by density:

| Rank | Feature | Hours | P1 | P2 | P3 | Density | Running total | Greedy result |
|---|---|---|---|---|---|---|---|---|
| 1 | F3 Attack telegraphs (ground decal and audio cue) | 22 | 1 | 1 | 0 | 0.0909 | 22 | keep |
| 2 | F7 Revive a downed ally | 12 | 1 | 0 | 0 | 0.0833 | 34 | keep |
| 3 | F8 Hit feedback (hitstop, flash, sound) | 14 | 0 | 1 | 0 | 0.0714 | 48 | keep |
| 4 | F1 Tank taunt | 18 | 1 | 0 | 0 | 0.0556 | 66 | keep |
| 5 | F4 Two-phase boss | 40 | 1 | 1 | 0 | 0.0500 | 106 | keep |
| 6 | F5 Loot drops with rarity | 20 | 0 | 0 | 1 | 0.0500 | 126 | keep |
| 7 | F2 Healer class | 30 | 1 | 0 | 0 | 0.0333 | 156 | keep |
| 8 | F9 Crafting | 30 | 0 | 0 | 1 | 0.0333 | 186 | cut |
| 9 | F6 Talent choice at level 2 | 35 | 0 | 0 | 1 | 0.0286 | | cut |
| 10 | F11 Second zone | 45 | 0 | 0 | 1 | 0.0222 | | cut |
| | F10 Day and night cycle | 16 | 0 | 0 | 0 | 0 | | cut |
| | F12 Emotes | 10 | 0 | 0 | 0 | 0 | | cut |

Ties keep the order of the original list. The greedy pass keeps 156 hours inside 162. Now count support among the kept features.

| Pillar | Kept features supporting it | Support |
|---|---|---|
| P1 Hold the line together | F3, F7, F1, F4, F2 | 5 |
| P2 Every fight reads | F3, F8, F4 | 3 |
| P3 Leave stronger | F5 | **1, fragile** |

This is the result the ranking hides. P3 features happen to be expensive, so the greedy pass fills the budget with cheap P1 features and leaves "leave stronger" standing on loot drops alone. If loot slips in sprint 3, the slice has no progression, and progression is one of the course's fixed requirements.

### The repair

Take a feature away from the pillar with the most support and give its hours to the fragile one. P1 has 5. The lowest-density P1 feature is F2, the healer, at 30 hours. Swap it for the best-value P3 feature that fits:

- F9 crafting (30 hours) fits exactly: 156 − 30 + 30 = 156.
- F6 talent choice (35 hours) also fits: 156 − 30 + 35 = 161 ≤ 162.

The team chose F6. A single talent choice at level 2 gives each player one visible decision in a 15-minute session. Crafting needs a loop of gather, craft and use that doesn't fit into 15 minutes. After the swap the kept tier is 161 hours, with support P1 = 4, P2 = 3, P3 = 2. Every pillar is at 2 or more. One hour of slack is left inside the budget.

Lab 02's `check_scope.py --greedy` reproduces the first table and prints `FAIL: pillar P3 has support 1`. Edit the tiers to the repaired set and it prints `PASS`.

### The same idea elsewhere

**Knapsack problems.** Choosing items by value per unit of weight until the bag is full is the standard greedy method for the knapsack problem. It is fast and usually good. It can also be badly wrong when a constraint exists that the ratio doesn't see, which here is "every pillar needs two supports".

**MoSCoW.** Dai Clegg's MoSCoW tiers (1994) from PR101 week 4 map directly onto this sheet: must is the core loop, should is everything above the cut line, and won't is the cut list. The density ranking is a way of deciding the order inside should, which MoSCoW itself leaves to judgment.

**GD101's swap test.** The repair above is the GD101 swap test run in the other direction. There you removed a mechanic and checked whether any pillar fell. Here you check which pillar is closest to falling and add a feature under it.

### Eyes-open judgment

The density score treats every pillar as equally important and every support as equally strong. Neither is true. A two-phase boss supports "every fight reads" far more than emotes would, even if both got a 1. Use the ranking to start the argument, then override it where the team can say why in one sentence. Write that sentence on the scope sheet.

Watch features that depend on each other. Talent choice needs levelling, and levelling needs experience from kills. If a kept feature depends on a cut one, you have either hidden cost or hidden breakage. PR101 week 4's dependency column exists for this reason.

Finally, `m_max ≥ 2` protects the must tier and nothing else. The should tier has almost no margin at 161 of 162 hours. That is fine as long as the team treats should as "planned, in this order" and not as "promised". Cut triggers, below, make that explicit.

### Check yourself

1. The artist re-estimates F4 at 55 hours. Rerun the greedy pass by hand from rank 5. Which features are kept, and is any pillar fragile?
2. The must tier grows to 230 hours after the team adds a lobby and character select. Compute `m_max` and `room`. What should the team do first?

<details><summary>Answers</summary>

1. F4's density becomes `2 / 55 = 0.0364`, so it drops to rank 6, after F5. Running totals: F3 22, F7 34, F8 48, F1 66, F5 86, F4 141. F2 would reach 171, which doesn't fit, and neither do F9 (171) or F6 (176). F11 at 45 is also too big. Kept: F3, F7, F8, F1, F5, F4, with 21 hours of slack. Support is P1 = 4, P2 = 3, P3 = 1. P3 is fragile again. Swap F1 (18) for F6 (35): 141 − 18 + 35 = 158, which fits.
2. `m_max = 445.5 / 230 = 1.94`, below 2, and `room = 312 − 230 = 82`. First, shrink the must tier. A lobby and character select are not the core loop. Players can join by IP with a fixed class until sprint 4. Move them to should, where they compete on density like everything else.

</details>

## 3. Writing pillars that decide things

A pillar is a short promise about the experience that lets you say no to a feature. GD101 covered the form. For a multiplayer slice, add three rules.

- **At least one pillar is about players together.** If every pillar would hold in a single-player game, your networking hours support nothing on the sheet.
- **Each pillar can be tested in a playtest.** "Every fight reads" can be tested. Ask a player after a fight what hit them. "Epic adventure" can't be tested.
- **Each pillar rules something out.** "Hold the line together" rules out a class that solos the boss. If a pillar rules out nothing, it doesn't do any work.

Three pillars is typical. Two can work. Five is usually two pillars written five ways.

## 4. The scope sheet

The scope sheet is one CSV and one page of prose. The CSV has one row per feature: id, name, tier, hours, one column per pillar, and a "player loses" line for anything cut. The prose page records:

- **The must tier**, as a list of player-visible steps, from "launch the build" to "see the victory screen".
- **Overrides**, meaning every place the team moved a feature against its density rank, with one sentence each.
- **Dependencies** between kept features and cut ones.
- **Cut triggers** for the should tier, as in PR101 week 4. Write them against milestones, not hours. "At the sprint 2 review, if telegraphs are not in the build, cut F1 and move its hours to F3."

The sheet is locked at the end of week 3, together with the technical design document. After that, one-in-one-out applies. A new feature enters only with an estimate and a matching cut.

## 5. The slice from the player's side

Before you lock scope, walk the kept features as a player would. Write the 15 minutes as a timeline. Minute 0, three players join. Minute 2, the first enemy telegraphs its swing. Minute 6, someone goes down and gets revived. Minute 12, the boss changes phase. Minute 14, loot drops and each player picks a talent.

The timeline catches two problems the CSV can't. The first is **dead minutes**, stretches where no kept feature is active. Those usually mean the zone is too big for the content, and [GD201 week 3](../../GD201-level-and-world-design/lectures/w03-flow-pacing-and-intensity-graphs.md) on pacing helps you fix them. The second is **features nobody reaches**. A talent choice at level 2 is worthless if players reach level 2 in minute 14 and the slice ends in minute 15.

## Studio session plan

| Time | Activity | Output |
|---|---|---|
| 0:00 to 0:15 | Instructor feedback on week 1 pitches, one concern per team | Concerns logged as risks |
| 0:15 to 0:50 | Pillars. Each person drafts three pillars alone for 10 minutes, then the team merges them and runs the three rules from section 3 | Three pillars on the wall |
| 0:50 to 1:30 | Feature list. Brainstorm every candidate feature, then each discipline's primary estimates their share of each feature | `features.csv` with hours |
| 1:30 to 1:40 | Break | |
| 1:40 to 2:20 | Cut line. Mark the pillar map, run `check_scope.py --greedy`, repair fragile pillars, record overrides | Tiers assigned, `PASS` |
| 2:20 to 2:45 | Player timeline. Walk the 15 minutes aloud and fix dead minutes and unreachable features | Timeline on one page |
| 2:45 to 3:00 | Cross-team read. Swap scope sheets with another team, and each team names one feature it would cut from the other's should tier | One written challenge per team |

## Deliverables

Due before next week's studio session, in `docs/` in your repository.

- **Pillars** (half a page), each with the playtest question that tests it and one thing it rules out.
- **Scope sheet** (`features.csv` in the lab 02 format) and the output of `check_scope.py` showing `PASS` with your chosen tiers.
- **Scope notes** (one page): must tier as player steps, overrides, dependencies and cut triggers.
- **Player timeline** of the 15-minute slice.

See [lab 02](../labs/lab02.md) for the format and rubric.

## Common failure modes

- **Pillars as genre labels.** "Co-op RPG" is a genre, not a pillar. Fix: write what the player feels or does, then test it with the three rules.
- **Everything is must.** The must tier holds 80% of the hours and `m_max` is 1.3. Fix: must means "the slice doesn't run without it". Anything a player could live without for a week of testing is should.
- **Estimates in one person's head.** Fix: every discipline estimates its own share of every feature, even if the share is zero.
- **Cutting by fatigue.** The last features estimated are the ones cut, because the team got tired. Fix: rank by density first, then argue.
- **No player-loses line.** The cut list is a list of names. Fix: for each cut, one line on what the player no longer gets. It makes the cut honest and makes it easy to reverse if time appears.

## Review checklist

- [ ] Three (or two) pillars, one about players together, each with a playtest question.
- [ ] Every feature has hours from every discipline and a pillar mapping.
- [ ] `check_scope.py` passes: should tier inside `room`, every pillar support at least 2, `m_max` at least 2.
- [ ] Every override of the density order has a one-sentence reason.
- [ ] Every cut feature has a player-loses line, and no kept feature depends on a cut one.
- [ ] The must tier is written as player-visible steps and includes the fixed course requirements.
- [ ] The 15-minute timeline has no dead stretch over two minutes, and every kept feature is reached.

## Sources

- Wikipedia, "Anthem (video game)" (accessed September 2026), summarizing Schreier, J., "How BioWare's Anthem Went Wrong", *Kotaku*, April 2019. Development from 2012, release on 22 February 2019, flying added and removed several times, and developers' account that most of the game was built in the year before release. The same facts are used in PR101 week 5.
- Wikipedia, "Mark Cerny" (accessed September 2026), section "The Method process". Set out in 2002 while consulting for Sony first-party studios; pre-production ending in a "publishable first playable".
- Wikipedia, "MoSCoW method" (accessed September 2026). Developed by Dai Clegg in 1994.
- Wikipedia, "Knapsack problem" (accessed September 2026). The greedy approximation that sorts items by value per unit of weight.
- Keith, C. (2020). *Agile Game Development: Build, Play, Repeat* (2nd ed.). Addison-Wesley. Pre-production and production in agile game development.
- The *Hollowmarch* pillars, features and hour estimates are invented for teaching.
