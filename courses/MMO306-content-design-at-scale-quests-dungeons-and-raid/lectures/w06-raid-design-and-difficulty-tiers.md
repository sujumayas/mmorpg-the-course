# MMO306 · Week 06 — Raid Design and Difficulty Tiers

**Why this matters:** A raid is the most expensive content an MMO team builds, and modern games sell each one several times over: as a story mode, a matchmade tier, one or two organised tiers and a hardest tier. Every tier has to be fair to groups of different sizes and to players who test different things. If you scale boss health with group size and stop there, you will build a raid that quietly favours large guilds on damage and small guilds on mechanics, and nobody on the team will have decided that.

**You will be able to:**
- Compute the per-player damage requirement of a flexible-size boss under different health-scaling rules, and derive the rule that makes it neutral to group size.
- Compute how raid-wide and targeted mechanics change a group's clean-pull chance as group size grows, and explain why health scaling and mechanic scaling push in opposite directions.
- Design a difficulty ladder for one boss by choosing, per tier, its health, mechanic tax, failure outcomes and telegraph lengths, and justify what each tier tests.
- Critique catch-up tools (stacking wipe buffs, level sync, tuning buffs on old content) by computing how far each moves the damage requirement.

**Before class:** Ion Hazzikostas, "It's called flex for a reason..." (World of Warcraft forums, December 2013), quoted on the Warcraft Wiki's "Flexible Raid" page. Naoki Yoshida, "Behind the Realm Reborn" (GDC 2014, GDC Vault), for how Final Fantasy XIV's team rebuilt and relaunched the game in two years and nine months. Reread your notes on MMO305 week 5 (raid rosters).

**Prerequisites from earlier courses:** [GD203 week 13, difficulty modes and scaling](../../GD203-combat-and-progression-design/lectures/w13-difficulty-modes-and-scaling.md) (a difficulty setting as multipliers on time-to-kill and time-to-die; not re-taught here). [MMO303 week 5, the holy trinity](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w05-the-holy-trinity-tank-healer-dps.md) (role counts and why raids need few tanks). [MMO305 week 5, raiding as organization](../../MMO305-social-systems-and-online-behaviour/lectures/w05-raiding-as-organization-dkp.md) (rosters, attendance and the bench). [GD202 week 13, shared vs personal story](../../GD202-narrative-and-quest-design/lectures/w13-shared-vs-personal-story.md) (for story-only tiers). From this course: [week 1, tiers target percentiles](w01-the-content-treadmill-production-vs-consumption.md), [week 4, the enrage line](w04-encounter-mechanics-tank-and-spank-to-dance-fights.md), [week 5, the raid multiplier](w05-telegraphing-and-readability.md), and [week 7, the kill-rate curve](w07-tuning-encounters-with-logs.md), which picks up where this week stops.

**Interactive:** [`examples/w06-flex-scaling.html`](../examples/w06-flex-scaling.html). Keep it open during section 2.

---

## 1. What a raid is, and what a tier is

A **raid** is instanced group content for more players than a standard party, built as a sequence of boss encounters with trash (weaker enemies) between them. In World of Warcraft a raid holds up to 30 players on its flexible difficulties. In Final Fantasy XIV a standard raid is 8 players, and alliance raids put 24 players in three parties of 8.

A **difficulty tier** is one version of the same raid tuned for a different audience. The expensive parts (the environment, the boss models, the scripting framework) are built once and the tuning is built per tier. Week 1 showed why that matters for production: tiers multiply replay for a fraction of the cost of new content, and each tier aims at a different percentile of the player population.

This week asks two questions that week 1 left open.

1. **What should differ between tiers?** Not only the numbers. GD203 week 13 showed that a difficulty setting in a single-player game is mostly a set of multipliers on health and damage. In group content, tiers can also change the mechanic tax (week 4), the telegraphs and failure outcomes (week 5), and the group size. Section 3 builds a tier ladder from those knobs.
2. **How do you tune a tier that allows different group sizes?** The worked example.

Week 7 then covers what happens after launch: reading logs and moving a tier's kill rate.

## 2. Worked example: flex scaling and the two-way pull

### The hook

In patch 6.0.2 (2014, for Warlords of Draenor), World of Warcraft made its Raid Finder, Normal and Heroic difficulties **flexible**: the raid scales its difficulty to the number of players present, between 10 and 30. Below 10 it stops scaling. Mythic, the hardest difficulty, stayed fixed at 20 players.

The designers' stated goal was neutrality. In a December 2013 forum post, Ion Hazzikostas wrote that the flexible system should never encourage a raid to turn away willing players of matching skill and gear, and should never make a raid feel it has to recruit extra bodies. In the same post he acknowledged that the system, as it stood, slightly favoured larger groups, because boss health and damage grew more slowly than raid throughput. The Warcraft Wiki's summary of the system adds that, with a few exceptions, each extra player adds a 20% chance for a boss ability to hit one more target.

Mythic stayed at a fixed 20 for more than a decade. In patch 12.0.7 (2026) the Sporefall raid became the first with a flexible Mythic difficulty, scaling from 15 to 25 players, meant to bridge the gap between Heroic and Mythic.

Why is neutrality so hard that the hardest tier went without it for so long? Because a boss tests two things that scale in opposite directions when the group grows.

### The model

Fix the boss's enrage `T` and its mechanic tax, so a group at the target execution has uptime `u` (week 4). A raid of `N` players has:

- 2 tanks, whatever its size. The boss hits one target at a time, so tanks don't scale (MMO303 week 5, section 4).
- `h(N) = N / 5` healers, one per five players, a common rule of thumb for raid rosters.
- `d(N) = N − 2 − N / 5` damage dealers.

To keep the arithmetic readable, assume tanks and healers deal no damage to the boss and each damage dealer brings the same paper DPS `D`. The raid's effective DPS is then `d(N) × D × u`.

**The damage side.** The boss's health follows a scaling rule `H(N)`. The damage each damage dealer must bring to kill at the enrage is

```
r(N) = H(N) / (T × u × d(N))
```

A rule is **neutral on damage** if `r(N)` is the same for every `N`.

**The execution side.** A raid-wide mechanic targets all `N` players, `k` times per pull. A targeted mechanic hits `N / 5` players, `k` times per pull (the 20% per extra player rule). With per-player success `p` from week 5, the clean-pull chances are

```
raid-wide:  P_clean(N) = p ^ (N × k)
targeted:   P_clean(N) = p ^ ((N / 5) × k)
```

### Numbers you can check

An invented boss with `T = 300` s, tax 0.2 and a target group at `x = 1`, so `u = 0.8`. At the reference size of 20 players the boss has `H(20) = 5,040,000`. Its one wipe mechanic is cast `k = 5` times per pull with a 1,100 ms telegraph, which with week 5's assumptions gives `p = 0.99617`.

First try the rule most people would write: **linear health**, `H(N) = H(20) × N / 20`, the same health per player at every size.

| Players `N` | Healers | Damage dealers `d` | Health, linear rule | Per-dealer requirement `r`, linear | Health, neutral rule | Clean pull, raid-wide | Clean pull, targeted |
|---|---|---|---|---|---|---|---|
| 10 | 2 | 6 | 2,520,000 | 1,750 | 2,160,000 | 82.5% | 96.2% |
| 15 | 3 | 10 | 3,780,000 | 1,575 | 3,600,000 | 75.0% | 94.4% |
| 20 | 4 | 14 | 5,040,000 | 1,500 | 5,040,000 | 68.1% | 92.6% |
| 25 | 5 | 18 | 6,300,000 | 1,458 | 6,480,000 | 61.9% | 90.9% |
| 30 | 6 | 22 | 7,560,000 | 1,432 | 7,920,000 | 56.2% | 89.1% |

Check the 10-player row by hand. Linear health `5,040,000 × 10/20 = 2,520,000`. Effective DPS per damage dealer must be `2,520,000 / (300 × 0.8 × 6) = 1,750`. At 20 players the same sum gives `5,040,000 / (240 × 14) = 1,500`. The 10-player group must bring 16.7% more damage per damage dealer than the 20-player group. The reason is the two tanks: they are a fixed overhead, 20% of a 10-player raid and under 7% of a 30-player one.

Now make the damage side neutral. Set `r(N)` equal to the 20-player value, 1,500, and solve for health:

```
H(N) = r × T × u × d(N) = 1,500 × 240 × (0.8 N − 2) = 288,000 N − 720,000
```

That is the "neutral rule" column. Health still grows linearly with `N`, but it no longer passes through zero: it has a negative intercept, so small groups get proportionally less health. The linear rule overcharges a 10-player group by `2,520,000 / 2,160,000 − 1 ≈ 17%`.

Now look at the two right-hand columns. With the damage side neutral, a raid-wide wipe mechanic still gets harder as `N` grows, from an 82.5% clean pull at 10 players to 56.2% at 30. The chance of a clean pull for the 30-player group is two thirds of the 10-player group's. Targeted mechanics grow more gently, from 96.2% to 89.1%, because they add one target per five players rather than one per player.

So the two sides pull in opposite directions. **Health that scales per player favours large groups on damage. Mechanics that scale per player favour small groups on execution.** Neutrality needs both sides tuned together, and the numbers are different for every mechanic.

### A visual you can move

Open [`examples/w06-flex-scaling.html`](../examples/w06-flex-scaling.html). The left view plots the per-dealer damage requirement `r(N)` against group size from 10 to 30, for the linear rule (falling curve) and the neutral rule (flat line), with a horizontal line at your group's actual per-dealer DPS. The right view plots the clean-pull chance against group size for a raid-wide and a targeted mechanic.

Start with the linear rule and your group's DPS at 1,550. The left view shows 10- and 15-player groups failing and 20 and above passing. The right view shows the smallest group has the best clean-pull chance. Switch to the neutral rule: the left view goes flat and every size passes. The right view doesn't change at all. Then move the "wipe mechanic" selector to "penalty" (week 5, section 5) and watch the right view flatten into expected misses per pull. That is the insight to take away: **you can make a flexible boss neutral on damage with one formula, but execution neutrality needs a decision about each mechanic.**

### Cross-game recognition

**World of Warcraft, flexible raids (patch 6.0.2 onward) and fixed Mythic.** Hazzikostas's 2013 remark that health and damage scaled more slowly than raid throughput is the linear-rule row of the table seen from the player side: bigger groups found the boss easier. His stated goal, never turning away or needing extra players, is the neutral rule. Keeping Mythic fixed at 20 removed the problem entirely for the tier where small biases matter most. Week 7 shows why: near the top of the field, a few percent of difficulty moves the kill rate a lot. Sporefall's flexible Mythic in 12.0.7, limited to 15 to 25 players, narrows the range over which neutrality has to hold, which is a sensible way to take on the problem.

**Final Fantasy XIV, fixed party sizes.** Final Fantasy XIV avoids flex scaling. Its raids are fixed at 8 players (or 24 in three parties of 8 for alliance raids), each party built from a fixed role recipe. In this week's model that sets `N` once, so the designers can tune `H`, the tax and every mechanic's exposure for exactly one group shape. The cost is roster rigidity: a static group missing one player can't raid, which is the scheduling burden MMO305 week 5 described.

**World of Warcraft, Raid Finder, 25 players.** Raid Finder is fixed at 25 on its matchmade side. The wiki says its bosses remove or modify mechanics that make the raid depend on a single player's performance. With 25 strangers, a raid-wide wipe mechanic has `N × k` of 125 or more, which week 5 showed is brutal. Raid Finder's answer is the one this model suggests: change the failure outcome rather than the telegraph.

### Eyes-open design judgment

- **Decide what "neutral" means before you tune.** Neutral per damage dealer, per player, or per raid? The table shows these give different health curves. Write the definition into the design document so tuners and players share it.
- **Fixed overhead roles break linear rules.** Any role whose count doesn't scale with `N` (tanks, a dedicated interrupter, a player assigned to a side platform) makes small groups pay more per head under a linear rule. Put an intercept in the formula.
- **Scale mechanic exposure deliberately.** For each mechanic, choose whether its targets scale with `N` or stay fixed. Raid-wide mechanics are cheap to build and expensive for large groups. Fixed-target mechanics are neutral on exposure but change how often each player is chosen, which small groups feel as "it's always me."
- **Flex is a social feature.** Its main value is that a guild can bring whoever showed up. A small bias towards larger groups may be acceptable if it encourages inviting people. A bias against them is not, because it tells raid leaders to bench friends.
- **Fixed size buys precision at the top.** For the tier where tuning margins are a few percent, a fixed size lets you test one configuration properly. Relax it, as Sporefall did, only over a range narrow enough to test.

### Check yourself (worked example)

1. Under the linear rule, what per-dealer DPS must a 12-player raid (2 tanks, 2 healers after rounding down `12/5`) bring? Compare it with the 20-player requirement.
2. Derive the neutral health for a 25-player raid if the tanks become 3 at 25 players and above.
3. A mechanic targets exactly 3 players whatever the raid size, `k = 5`, `p = 0.99617`. What is the clean-pull chance at 10 and at 30 players?

<details>
<summary>Answers</summary>

1. `d = 12 − 2 − 2 = 8`. Health `5,040,000 × 12/20 = 3,024,000`. `r = 3,024,000 / (240 × 8) = 1,575`, which is 5% above the 20-player requirement of 1,500.
2. `d = 25 − 3 − 5 = 17`. `H = 1,500 × 240 × 17 = 6,120,000`, lower than the 6,480,000 of the two-tank neutral rule, because one more player is overhead.
3. `0.99617^15 ≈ 0.944` at both sizes. Fixed-target mechanics are neutral on exposure.

</details>

## 3. Building a difficulty ladder

A tier is a setting of several knobs at once. Treat them as a table you fill in per tier, and ask of each column: what does this tier test?

| Knob | What it tests | From |
|---|---|---|
| Health and damage multipliers | Gear and rotation | GD203 week 13 |
| Mechanic tax | Execution speed (hidden health) | Week 4 |
| Mechanics present | Knowledge and coordination | Week 4, section 4 |
| Telegraph length and exposure `N × k` | Reading under pressure | Week 5 |
| Failure outcome | Tolerance for mistakes | Week 5, section 5 |
| Group size and whether it flexes | Organisation | This week |

Here is one invented boss as a five-tier ladder. The numbers are illustrative. The pattern is the point.

| Tier | Health (× Normal) | Tax | Mechanics | Telegraph | Wipe mechanics | Group |
|---|---|---|---|---|---|---|
| Story | 0.3 | 0.05 | 2 of 6 | 1,600 ms | None | Solo or small, with AI allies |
| Matchmade | 0.8 | 0.10 | 4 of 6 | 1,400 ms | None; misses cost a debuff | 25, strangers |
| Normal | 1.0 | 0.15 | 6 of 6 | 1,250 ms | None; misses cost a death | 10 to 30, flex |
| Heroic | 1.3 | 0.20 | 6 of 6, faster cycles | 1,150 ms | 1 | 10 to 30, flex |
| Mythic | 1.8 | 0.25 | 6 + 2 new | 1,050 ms | 3 | 20, fixed |

Read the ladder by column and you can see the design intent. Health rises steadily. The tax rises more slowly, so the lower tiers are mostly a test of showing up with the right gear. Wipe mechanics appear only once groups are organised and fixed. Telegraph lengths shrink as the audience gets more practised.

Three rules keep a ladder healthy.

**Each step should add one new test.** If Heroic is Normal with more health, it tests only gear, and the players who find Normal easy will find Heroic a longer version of it. Week 1 described tiers as aimed at percentiles of the population. The best ladders also aim each tier at a different skill.

**Each tier should teach the next.** Mechanics introduced at Mythic should be rare, because players have no lower tier to practise them on. Final Fantasy XIV's Savage is built on this idea: the community wiki describes Savage as the same boss as Normal with harder mechanics, more health and higher damage, and every Savage boss has an enrage. Players learn the boss's shape in Normal and its full demands in Savage. The Story tier in the ladder is there for players who want the narrative without a group; World of Warcraft's Story Mode, available from the raid's second week, is a vastly simplified version of the final boss that gives no loot. GD202 week 13 covered how shared stories reach players who never see the hardest content.

**The step sizes should not be even.** Week 7 shows that a group's chance of meeting a damage check depends on where the check sits in the distribution of groups. Equal multipliers between tiers do not give equal steps in the share of groups that clear. Place tiers by the audience you want each to reach, not by round multipliers.

## 4. Catch-up: moving the requirement after launch

A tier's difficulty is not fixed for its whole life. Groups get stronger as they collect gear, and designers often lower the requirement deliberately so that later players can see content that the first wave cleared. Three shipped tools do this, and each is easy to price with week 4's model.

**A stacking wipe buff (World of Warcraft Raid Finder).** Each time a Raid Finder group wipes on a boss, every player gains a buff called Determination that raises their health, damage dealt and healing received by 5%, stacking up to 10 times, until the boss dies. Treat the stacks as additive: after `w` wipes, damage is multiplied by `1 + 0.05 w`, up to 1.5. A group whose effective DPS is 80% of what it needs (it needs a factor of `1 / 0.8 = 1.25`) clears after 5 wipes. A group at 67% (needs 1.5) needs all 10. Any group below `1 / 1.5 = 67%` of the requirement can never clear, whatever it does. That is a clean design: the buff helps groups that are close, caps how much it can help, and leaves a floor.

**A flat buff on old content (Final Fantasy XIV's Echo).** When a Savage raid is no longer current, players entering it receive a buff called the Echo, and the wiki notes that its strength does not rise when a group wipes. It lowers the requirement for everyone, by the same fraction, forever. In week 7's terms it slides the damage check left along the whole field. It rewards nobody for failing, which suits content that is no longer the frontier.

**Level and item-level sync (Final Fantasy XIV Ultimate).** Each Ultimate raid has a strict item-level sync and cannot be run unsynced. This is the opposite tool: it stops the requirement from falling as gear improves. Paper DPS is capped, so the only way to move the enrage line is execution, `x` from week 4. Designers use sync when they want a fight to stay a test of play, not of time invested.

Each tool is a choice about who the tier is for once it is old. Price it before you ship it. "How many wipes until the median group clears?" is a question with a number for an answer.

## 5. The raid as a sequence

A raid is more than its bosses one at a time. Three structural decisions shape how groups experience a tier.

**Order and gating.** Bosses are usually fought in a set order, or in wings that unlock in sequence. Put a low-tax boss first (a gear check, week 4) so that groups learn early whether they belong in this tier. Put the hardest execution test last, so that groups meet it after they have practised the raid's mechanic language. Final Fantasy XIV's Savage tiers follow this pattern: the wiki describes the first two encounters of a tier as roughly comparable to an Extreme trial and the last two as much harder. The same source notes that, since Omega: Deltascape, the first Savage tier of each expansion has been tuned easier on purpose, to let players adjust to the expansion's class changes. That is a ladder across tiers inside the ladder across difficulties.

**Checkpoints.** A long raid lets groups keep progress: a boss killed this week stays dead until the weekly reset. Final bosses with two phases can add a checkpoint between them, which Final Fantasy XIV does for most final Savage floors. A checkpoint halves the cost of learning the second phase, because a wipe there no longer means redoing the first. Where you put checkpoints decides where groups spend their practice time.

**Group size and the roster.** A fixed-size tier asks the raid leader to choose exactly who plays, which MMO305 week 5 showed creates benches, attendance rules and loot politics. A flexible tier removes most of that. That is why flex went to the tiers aimed at casual and social groups, and fixed size stayed at the top where organisation is part of what the tier tests.

## In-class activity (25 minutes)

In groups of three, build a four-tier ladder for one boss. You may reuse your week 4 boss.

1. (8 min) Fill in the ladder table from section 3 for four tiers of your choice. For each tier, write one sentence naming the new test it adds.
2. (7 min) For your flexible tiers, derive the neutral health rule for your roster assumptions (tanks, healers per player). Show `H(10)`, `H(20)` and `H(30)`.
3. (5 min) Pick one raid-wide mechanic from your ladder. Compute its clean-pull chance at 10 and 30 players with your telegraph and `σ = 150 ms`. Propose one change (target count or failure outcome) that brings the two within 10 points of each other.
4. (5 min) Choose one catch-up tool from section 4 for when the tier is old. Compute how much it moves the requirement.

Expected output: the ladder table, the neutral health rule with three values, the two clean-pull numbers before and after your change, and the catch-up calculation.

## Common misconceptions

- **"Scale boss health per player and flex is fair."** Only if every role scales with group size. Fixed roles like tanks make a per-player rule overcharge small groups (17% at 10 players in the example).
- **"Harder tiers are the same fight with bigger numbers."** That makes a ladder that tests only gear. Good tiers change the tax, the mechanics, the telegraphs and the failure outcomes, so each step asks for something new.
- **"Mythic is fixed-size for tradition."** It is fixed because at the top tier small biases decide who clears, and one fixed configuration can be tuned and tested exactly.
- **"Catch-up buffs are free difficulty."** Each one moves the requirement by a computable amount and changes who the tier is for. A stacking wipe buff with a cap still leaves some groups below its floor.

## Check yourself

1. Using the section 2 model with 2 tanks and `N / 5` healers, a boss is tuned neutral at 1,800 per-dealer DPS with `T = 360` s and `u = 0.75`. Write `H(N)` and give `H(10)` and `H(30)`.
2. With the same roster rule and the linear rule `H(N) = H(20) × N / 20`, by what percentage does a 15-player group's per-dealer requirement exceed a 30-player group's?
3. A raid-wide mechanic with `p = 0.995` is cast 4 times per pull. What are the clean-pull chances at 10 and at 25 players? If you convert it to a targeted mechanic hitting `N / 5` players, what are they now?
4. A Raid Finder group has 70% of the effective DPS a boss needs. With Determination as described in section 4, how many wipes before it can clear? What about a group at 60%?
5. A designer proposes a ladder where Heroic is Normal with 1.3× health and nothing else changed. Name the test Heroic adds and one knob you would move to make it add a second.

<details>
<summary>Answers</summary>

1. `d(N) = 0.8 N − 2`. `H(N) = 1,800 × 360 × 0.75 × (0.8 N − 2) = 486,000 × (0.8 N − 2) = 388,800 N − 972,000`. `H(10) = 2,916,000`, `H(30) = 10,692,000`.
2. `r ∝ N / d(N)`. At 15: `15 / 10 = 1.5`. At 30: `30 / 22 ≈ 1.364`. Ratio `1.5 / 1.364 ≈ 1.10`, so 10% more.
3. Raid-wide: `0.995^40 ≈ 0.818` at 10, `0.995^100 ≈ 0.606` at 25. Targeted: `0.995^8 ≈ 0.961` at 10 (2 targets × 4 casts), `0.995^20 ≈ 0.905` at 25 (5 targets × 4 casts).
4. It needs a factor of `1 / 0.7 ≈ 1.43`. `1 + 0.05 w ≥ 1.43` gives `w ≥ 8.6`, so 9 wipes. At 60% it needs `1.67`, above the 1.5 cap, so it can never clear.
5. It adds only a gear test (a longer damage line). Raise the tax by shortening mechanic cycles (an execution test), or add one wipe mechanic with a shorter telegraph (a reading test).

</details>

## Lab / assignment hook

[Lab 06, a flexible tier ladder](../labs/lab06.md). You extend your lab 04 calculator with roster rules, health-scaling rules and mechanic exposure, find the neutral health formula for two roster assumptions, and fill in a four-tier ladder for your own boss with a one-page rationale. The ladder is the largest single piece of your encounter-design portfolio before the final dungeon.

## Sources

- Warcraft Wiki, "Flexible Raid" (current). Flexible scaling from 10 to 30 players on Raid Finder, Normal and Heroic since patch 6.0.2, bottoming out at 10; Mythic statically tuned for 20; each extra player adds a 20% chance for an ability to hit an extra target; Ion Hazzikostas's blue post of 10 December 2013 on neutrality with respect to group size and on health and damage scaling more slowly than raid throughput. https://warcraft.wiki.gg/wiki/Flexible_Raid
- Warcraft Wiki, "Instance difficulty" (current, through patch 12.0.7). The four raid difficulties since Warlords of Draenor, Mythic fixed at 20, Story Mode (simplified final boss, no loot, from week two), and Sporefall as the first flexible Mythic raid for 15 to 25 players in patch 12.0.7. https://warcraft.wiki.gg/wiki/Instance_difficulty
- Warcraft Wiki, "Raid Finder" (current). Raid Finder first released in patch 4.3.0; always 25 players; mechanics that depend on a single player's performance removed or modified; the Determination buff, 5% health, damage and healing received per wipe, stacking up to 10 times. https://warcraft.wiki.gg/wiki/Raid_Finder
- Final Fantasy XIV Online Wiki (consolegameswiki), "Raids" (accessed September 2026, covering A Realm Reborn through Dawntrail). Normal raids for 8 players; alliance raids for 24 in three parties of 8; Savage as the same boss with harder mechanics, more health, higher damage and an enrage; first Savage tier of each expansion tuned easier since Omega: Deltascape; checkpoints on final floors; the Echo on old Savage, not increasing on wipes; Ultimate's strict item-level sync. https://ffxiv.consolegameswiki.com/wiki/Raids
- Yoshida, N. "Behind the Realm Reborn." GDC 2014, GDC Vault. https://gdcvault.com/play/1020179/Behind-the-Realm
- The flex boss, its roster rule (2 tanks, one healer per five players), the five-tier ladder and all their numbers are invented for teaching. The Determination arithmetic treats stacks as additive.

## Interactive spec: examples/w06-flex-scaling.html

**Purpose.** Show that health scaling and mechanic scaling push in opposite directions as group size grows, and that a neutral health rule fixes only the damage side. The first screen must show the linear rule with a group at 1,550 per-dealer DPS: the left view with the 10- and 15-player points above the group's line (failing) and the right view with the raid-wide curve falling from 82.5% to 56.2%.

**Model (exact).** For integer `N` from 10 to 30: tanks `t(N) = tanks` (slider, default 2; optional "3 tanks at 25+" toggle), healers `h(N) = floor(N / 5)`, damage dealers `d(N) = N − t(N) − h(N)`. Reference health `H20` at `N = 20`. Linear rule `H(N) = H20 × N / 20`. Neutral rule `H(N) = r20 × T × u × d(N)` with `r20 = H20 / (T × u × d(20))`. Custom rule `H(N) = H20 × (a + b N)` with `a + 20 b = 1` (one slider for `a`, `b` derived). Per-dealer requirement `r(N) = H(N) / (T × u × d(N))`. Per-player success `p = Φ((T_tel − μ) / σ)` with `μ = 700` ms. Raid-wide `P_clean = p^(N k)`; targeted `P_clean = p^(floor(N/5) × k)`; fixed-target `P_clean = p^(m k)` with `m` a slider. In "penalty" mode show expected misses `N k (1 − p)` (raid-wide) and `floor(N/5) k (1 − p)` (targeted) instead.

**Left view, "Damage: what each dealer must bring."** x axis `N` 10 to 30; y axis per-dealer effective DPS 1,000 to 2,000. Linear rule as a steel line with circle markers at each `N`; neutral rule as a moss flat line; custom rule dashed when selected. Horizontal ochre line at the group's per-dealer DPS (slider). Points above the ochre line drawn hollow and labelled "fails" on hover or focus.

**Right view, "Execution: chance of a clean pull."** x axis `N` 10 to 30; y axis 0 to 100%. Raid-wide curve (blood red, thick), targeted curve (steel), fixed-target curve (ink, dashed) when enabled. In penalty mode the y axis becomes expected misses per pull, 0 to 5.

**Controls.** Rule selector (linear, neutral, custom). Sliders: `H20` 2,000,000 to 10,000,000 step 10,000 (default 5,040,000); `T` 180 to 600 (300); tax 0 to 0.4 (0.2) with `u = 1 − tax`; group per-dealer DPS 1,000 to 2,000 step 10 (1,550); `T_tel` 800 to 1,600 ms step 10 (1,100); `σ` 50 to 300 (150); `k` 1 to 10 (5); fixed targets `m` 1 to 10 (3). Toggles: "3 tanks at 25+", wipe/penalty. All keyboard operable with visible values.

**Readout table.** Rows `N` = 10, 15, 20, 25, 30; columns `d`, `H(N)` under the current rule, `r(N)`, pass/fail for the group, raid-wide and targeted clean pull.

**Test values.** Defaults: `d` = 6, 10, 14, 18, 22. Linear `H` = 2,520,000 / 3,780,000 / 5,040,000 / 6,300,000 / 7,560,000 and `r` = 1,750 / 1,575 / 1,500 / 1,458.3 / 1,431.8. Neutral `H` = 2,160,000 / 3,600,000 / 5,040,000 / 6,480,000 / 7,920,000 with `r` = 1,500 everywhere. `p = 0.99617`. Raid-wide clean pull 82.5 / 75.0 / 68.1 / 61.9 / 56.2%. Targeted 96.2 / 94.4 / 92.6 / 90.9 / 89.1%. Fixed 3 targets: 94.4% at every `N`. With group DPS 1,550 and the linear rule, `N` = 10 and 15 fail, 20 to 30 pass.

**The one insight.** Switching from linear to neutral must flatten the left view while the right view stays exactly as it was. Caption: "Health scaling can be made neutral with one formula. Mechanic scaling has to be decided one mechanic at a time."

**Style and accessibility.** Program tokens inline. Pass and fail shown by filled versus hollow markers as well as colour. Respect `prefers-reduced-motion` and `prefers-color-scheme`. At 390 px the two charts stack and the readout table scrolls inside its own container, not the page.
