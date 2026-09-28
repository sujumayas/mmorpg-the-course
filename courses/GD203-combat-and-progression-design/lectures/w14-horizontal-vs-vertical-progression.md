# GD203 · Week 14 — Horizontal vs Vertical Progression

**Why this matters:** Every reward you give a player either raises their power or widens their options, and the mix decides whether veterans and newcomers can still play together a year after launch. You can compute that year in advance from one growth rate, and you should, before your content plan commits you to it.

**You will be able to:**
- Compute the power gap between two players under vertical and horizontal progression, and convert it into the health cost each pays in a shared encounter.
- Derive a content tier's shelf life from the per-tier growth rate and a tolerance band, and choose a growth rate that meets a target shelf life.
- Test whether a "sidegrade" is truly horizontal using dominance and expected value across situations.
- Critique a shipped game's progression as a mix of vertical and horizontal parts, and predict where its community will split.

**Before class:** Schreiber & Romero, *Game Balance* (2021), chapters "Progression in PvE Games" and "Progression in PvP Games". Schreiber, *Game Balance Concepts*, Level 6, "Situational Balance" (2010, free online).

**Prerequisites from earlier courses:** GD203 [week 8, power curves and level scaling](w08-power-curves-and-level-scaling.md) (power as offense times defense, the power ratio, squishes and downscaling), [week 13, difficulty modes and scaling](w13-difficulty-modes-and-scaling.md) (safety ratio as health cost), and [week 9, item budgets and stat weights](w09-item-budgets-and-stat-weights.md). This lecture sets up MMO307 weeks 2, 3, 5 and 6 (vertical progression, horizontal progression, stat squish, catch-up), in the [MMO307 syllabus](../../MMO307-game-balance-ii-pvp-progression-and-endgame/syllabus.md).

**Interactive:** [Power gap](../examples/w14-power-gap.html) (specified at the end of this lecture). Keep it open during section 2.

---

## 1. Two ways to get better

Think of the last reward that made you happy in an RPG. It probably did one of two things.

It made you stronger. A sword with a bigger number, a level that raised every stat, an item level that crept up after a raid. The new thing beats the old thing in every fight you will ever have. This is **vertical progression**. The word describes the picture on a chart. Power goes up.

Or it gave you something new to do. A second weapon type that handles armored enemies better and single targets worse. A glider that opens routes you could not take. A whole second class on the same character. The new thing is better than the old thing only in some situations. This is **horizontal progression**. On the chart, the line goes sideways. You have more choices, and your best-case power in any one situation has not moved much.

Most games mix the two. The design question is the ratio, and when to use each. To answer it with numbers we need two ideas from earlier weeks.

### Power, safety and the gap

In [week 8](w08-power-curves-and-level-scaling.md) you defined **power** as offense times defense, `P = a × h`, and saw that the safety ratio of a fight (time-to-die over time-to-kill, from week 4) equals the power ratio between the two sides. In [week 13](w13-difficulty-modes-and-scaling.md) you read the safety ratio as a health cost per fight, `1 / R`.

Now put two players against the same enemy, a veteran with power `P_A` and a newcomer with power `P_B`. Call the ratio of their powers the **power gap**:

```
G = P_A / P_B
```

Because each player's safety ratio is their power divided by the enemy's, the veteran's safety ratio is exactly `G` times the newcomer's. If the veteran is 1.5 times as strong, any fight that costs the newcomer 60% of their health costs the veteran 40%.

## 2. Worked example: how long can two players share an encounter?

### The hook

Two long-running MMOs answered "what does a player earn after the level cap?" in opposite ways.

World of Warcraft launched in 2004 with a level cap of 60 and raised it in most expansions, reaching 120 in Battle for Azeroth. In the Shadowlands pre-patch (patch 9.0.1, late 2020) Blizzard squished levels so that a level 120 character became level 50, with a new cap of 60. It had already squished stats twice before, in patch 6.0.2 (2014) and patch 8.0.1 (2018).

Guild Wars 2 launched in 2012 with a level cap of 80 and still has it. Its highest stat tier, ascended equipment, first arrived in November 2012. The official wiki lists ascended stats as 5% stronger than exotic gear, and legendary gear as equal to ascended. The Heart of Thorns expansion (2015) added masteries, an account-wide track of new abilities, instead of new levels.

One game grew the numbers so far it had to shrink them. The other froze its numbers and grew something else. Here is a model that shows why each happened.

### The model

**Vertical progression.** Content arrives in tiers (a raid, a season, an expansion). Each tier multiplies the power of a player who completes it by a growth rate `r`. After `t` tiers:

```
P_v(t) = r^t
```

**Horizontal progression.** The game has `n` kinds of situation, each equally common (say, armored enemies, swarms, ranged casters, and so on). There are `n` tools, one suited to each situation. Holding the right tool multiplies your power by `1 + b` in that situation and does nothing elsewhere. A player who owns `k` of the `n` tools, and brings the right one when they have it, has expected power:

```
P_h(k) = 1 + b × k / n
```

**Sharing an encounter.** One encounter can only serve players whose safety ratios are fairly close. Call `F` the widest gap it can serve, meaning the veteran's safety ratio may be at most `F` times the newcomer's before the fight is either trivial for one or brutal for the other. Two players can share the encounter when:

```
G ≤ F
```

With `F = 2`, an encounter tuned so the newcomer loses half their health per fight leaves the veteran losing a quarter. That is about the widest spread a normal dungeon can take and still feel like the same fight to both. Tightly tuned content, like a hard raid, has a smaller `F`.

**Shelf life.** Under vertical progression, a newcomer at tier 0 and a veteran at tier `t` have `G = r^t`. The largest tier distance two players can have and still share content is:

```
t* = ln F / ln r
```

Read `t*` two ways. It is how far apart two friends can be and still play together. It is also how many tiers a piece of content stays relevant before new players outgrow it or veterans find it trivial. Call it the content's **shelf life**.

### Numbers you can check

Take `r = 1.10` (each tier adds 10% power) and `F = 2`.

| Tiers apart, t | Power gap G = 1.1^t | Veteran's health cost if newcomer's is 50% | Can share (G ≤ 2)? |
|---|---|---|---|
| 0 | 1.000 | 50.0% | yes |
| 1 | 1.100 | 45.5% | yes |
| 2 | 1.210 | 41.3% | yes |
| 3 | 1.331 | 37.6% | yes |
| 4 | 1.464 | 34.2% | yes |
| 5 | 1.611 | 31.0% | yes |
| 6 | 1.772 | 28.2% | yes |
| 7 | 1.949 | 25.7% | yes |
| 8 | 2.144 | 23.3% | no |
| 10 | 2.594 | 19.3% | no |

The formula gives `t* = ln 2 / ln 1.1 = 0.693 / 0.0953 ≈ 7.27`. Seven tiers apart still works; eight does not. At one tier per four months, that is about two and a half years.

Now vary the growth rate and hold `F = 2`:

| Growth per tier r | Shelf life t* = ln 2 / ln r (tiers) |
|---|---|
| 1.05 | 14.2 |
| 1.10 | 7.3 |
| 1.15 | 5.0 |
| 1.25 | 3.1 |
| 1.50 | 1.7 |

A designer who wants each tier to feel big (25% more power) buys that feeling with content that goes stale in three tiers. Nothing about this depends on any particular game. It follows from compounding.

Horizontal progression behaves differently. Take `n = 6` situations and `b = 0.3` (the right tool gives 30% more power in its situation).

| Tools owned k | Expected power P_h = 1 + 0.3k/6 | Gap vs a newcomer with k = 1 | Veteran's health cost if newcomer's is 50% |
|---|---|---|---|
| 1 | 1.05 | 1.000 | 50.0% |
| 2 | 1.10 | 1.048 | 47.7% |
| 3 | 1.15 | 1.095 | 45.7% |
| 4 | 1.20 | 1.143 | 43.8% |
| 5 | 1.25 | 1.190 | 42.0% |
| 6 | 1.30 | 1.238 | 40.4% |

The gap stops at `1.3 / 1.05 ≈ 1.24`, however long the veteran plays. Horizontal progression has a hard ceiling on the gap, `(1 + b) / (1 + b/n)`. Vertical progression has none.

### A visual you can move

Open the interactive. The left panel plots power against time (tiers played) for three players. A vertical veteran rises as `r^t`. A horizontal veteran climbs one tool per tier and then flattens. A newcomer starts at tier 0. On this panel the horizontal line looks like the weaker design, since its line flattens early and the vertical line keeps climbing.

The right panel shows the question that matters for a live game, "can the veteran and the newcomer share an encounter?" It plots the power gap `G` with the band `F` drawn as a shaded ceiling. The vertical gap crosses the ceiling at `t*`. The horizontal gap never reaches it. Drag `r` up to 1.25 and watch the crossing move from tier 7 to tier 3. Drag `F` down to 1.5 (a game where encounters are tightly tuned, like a hard raid) and watch shelf life fall to `ln 1.5 / ln 1.1 ≈ 4.3` tiers. The same growth that looked like "more reward" on the left is "fewer people you can play with" on the right.

### Cross-game recognition

**World of Warcraft (vertical, with resets).** Each raid tier and expansion raises item level, which is `r^t` growth. As week 8 showed, stat squishes divide every number in the game by the same factor, veteran and newcomer alike. Divide both `P_A` and `P_B` by 10 and `G` does not change at all. A squish fixes numbers that have become too big to read or compute. It does not close a gap. What closes gaps in a vertical game is a **catch-up mechanic**, which raises the newcomer's `t` directly (MMO307 week 6). Expansions work the same way at a larger scale. New gear makes old gear obsolete, which resets every player's `t` near zero, so everyone lands inside `F` again.

**Guild Wars 2 (vertical, capped).** At level 80, the best gear is 5% better than exotic gear, which is widely available. In our model the vertical part stops after one step with `r = 1.05`, so `G = 1.05`, and a fight that costs a fresh level-80 player 50% of their health costs a fully geared veteran about 48%. That sits deep inside any sensible band. Masteries then add the horizontal part. They are new abilities (gliding, from Heart of Thorns, is the best-known one), each useful in particular zones and routes, which is exactly a tool with a situational `b`. Week 8's downscaling example shows the same pattern below the cap. A veteran in a low-level zone keeps skills, traits and gear but has raw stats cut to near the zone's level. Numbers are pushed together; options remain.

**Final Fantasy XIV (horizontal breadth over vertical jobs).** The game's Armoury system lets one character take any class or job by equipping that job's weapon or tool. Each job still levels vertically, and gear still rises in item level. At the character level, though, a new job is a new tool in our sense. A healer job is worthless when your group needs a tank and invaluable when it needs a healer. A veteran with every job has more `k`, and so more situations where they can fill the gap, without being more powerful in any single role than a newcomer who levelled that one job.

Three games, one model. For any progression system, ask two questions. What is `r`, and does it stop? What are the situations, and what is `b`?

### Eyes-open design judgment

Neither direction is correct. Each is a set of costs you choose.

Vertical progression is easy to read. Every reward is visibly better, the player's safety ratio grows (week 8), and new content can gate old content cleanly ("you need item level X"). Its costs follow from `t* = ln F / ln r`. Content has a shelf life. Veterans and newcomers drift apart. Numbers inflate until you squish them, and you will need catch-up systems forever.

Horizontal progression keeps the community together and keeps old content playable. Its costs are subtler.

- **Rewards can feel small.** If `b` is low, a new tool does not feel like a reward. Guild Wars 2's masteries work partly because traversal abilities feel large even with no stat attached.
- **It needs situations.** If your game has one kind of fight, there is nothing for a situational tool to be good at. Horizontal progression is mostly an encounter design problem ([week 10](w10-enemy-design-by-the-numbers.md)).
- **The balance workload multiplies.** With `n` tools and `m` situations, you tune `n × m` cells instead of one power curve.
- **It leaks into vertical.** The moment one "sidegrade" is better everywhere, it is vertical progression with a different label. Section 3 gives you a test.

Decide `r`, `F` and `b` on purpose, write them in your design document, and compute the shelf life before you plan a content calendar.

## 3. Is it really a sidegrade?

Designers often announce horizontal rewards that players quickly identify as vertical. You can check before shipping.

### The dominance test

Option X **dominates** option Y if X is at least as good as Y in every situation and strictly better in at least one. A dominated option is dead. No informed player will choose it. If a new reward dominates an old one, the reward is vertical, whatever its tooltip says.

Here are four swords, scored by damage per second in three situations.

| Sword | Single target | Swarm (cleave) | Armored | Expected DPS (50/30/20) |
|---|---|---|---|---|
| A | 100 | 60 | 50 | 78.0 |
| B | 80 | 90 | 50 | 77.0 |
| C | 85 | 65 | 75 | 77.0 |
| D (new) | 105 | 70 | 55 | 84.5 |

Compare D to each older sword.

- D vs A. D is higher in all three columns (105 ≥ 100, 70 ≥ 60, 55 ≥ 50). D dominates A. For anyone holding A, D is a vertical upgrade.
- D vs B. B wins swarms (90 > 70). No dominance.
- D vs C. C wins armored (75 > 55). No dominance.

So D is vertical relative to A and horizontal relative to B and C. The design fix, if you wanted D to be a true sidegrade, is to give it a weakness somewhere A is strong.

### The expected-value test

Dominance is not the whole story. Suppose single-target fights happen 50% of the time, swarms 30% and armored 20%. Weight each sword's DPS by those frequencies (this is the situational-balance method from Schreiber's Level 6). A, B and C land between 77 and 78. D lands at 84.5, about 8% ahead of A. D dominates nothing except A, and yet most players will use D almost everywhere, because it wins the most common situation and loses little elsewhere.

A true sidegrade needs to pass both tests. No option may dominate another. Expected values across realistic situation frequencies must stay within a tolerance you choose, for example 3%. If the frequencies change (a new raid full of armored enemies), the expected values change, and yesterday's sidegrade becomes today's best-in-slot. Horizontal balance is always conditional on the content mix.

## 4. Where hybrid designs put each part

Real progression systems stack both kinds. A useful way to read one is by layer.

**Inside a tier: vertical.** Within a season or a raid tier, most games let power rise. It gives short-term goals and a clear signal of success, and the tier is short enough that `t` stays small.

**Across tiers: reset or cap.** Between tiers, the game must stop `t` from growing without limit. Three tools do this. A cap freezes the vertical part (Guild Wars 2). A reset makes old power obsolete so everyone restarts near zero (a new expansion's gear). A catch-up mechanic raises the newcomer's `t` directly. A squish does none of these. It rescales `P` and leaves `G` alone.

**Across the account: horizontal.** Unlocks that belong to the account (masteries, jobs, mounts, collections) give long-term goals that never widen the gap between players in a single encounter.

**Cosmetics: outside power.** Appearances have `b = 0`. They are a reward track that costs no balance at all, which is why so many live games lean on them. They are not horizontal progression in our sense, because they give no new options in play. Treat them as a third category.

A shelf-life worked in reverse gives you a budget. Suppose you plan ten tiers over five years and want any two players within four tiers of each other to share content at `F = 2`. Then `r^4 ≤ 2`, so `r ≤ 2^(1/4) ≈ 1.19`. Every tier's rewards together may raise power by at most 19%. That is a number your item budget from week 9 can enforce.

## In-class activity (25 minutes)

Work in groups of three. You are handed a one-page plan for a small MMO's first two years: six tiers, each adding 20% power, with `F = 2`.

1. Compute the shelf life `t*`. Which pairs of tiers can share an encounter?
2. The producer wants tier 6 players to be able to help tier 2 players through old dungeons. Propose two different fixes. One must change `r`. The other must keep `r` and add a cap, reset, catch-up or downscaling rule. Show the resulting gap for a tier 6 and a tier 2 player under each.
3. Redesign tier 4's rewards as horizontal. Write three new tools with DPS in three situations, and situation frequencies for tier 4's content. Run the dominance test and the expected-value test against the existing best tool (DPS 100, 70, 60).
4. Present your best fix in two minutes. The other groups try to find a dominated option or an expected-value gap above 3%.

Expected output: one table of gaps and shelf lives, one table of tools with expected values, and a two-sentence recommendation.

## Common misconceptions

- **"Horizontal progression means no power."** A horizontal tool gives real power, `1 + b`, in its situation. What it lacks is power *everywhere*. The gap it can create is bounded by `(1 + b) / (1 + b/n)`.
- **"A stat squish fixes power creep."** A squish divides everyone's numbers by the same factor, so the gap `G` is unchanged. It fixes readability and overflow, not the distance between players.
- **"A sidegrade with a niche is balanced."** It also has to avoid a large expected-value lead in common situations. Sword D above loses two niches and still wins most fights.
- **"Players only want vertical rewards."** Players want rewards that change what they can do. Vertical rewards are the easiest way to deliver that, and horizontal rewards with a large `b` in a memorable situation (a glider, a new job) can deliver it too.

## Check yourself

1. A game grows power by 15% per tier. With `F = 2`, how many tiers apart can two players be and still share an encounter?
2. A horizontal system has `n = 4` situations and `b = 0.5`. What is the largest power gap between a newcomer with one tool and a veteran with all four? If a shared fight costs the newcomer 60% of their health, what does it cost the veteran?
3. A veteran is 12 tiers ahead of a newcomer at `r = 1.1`. The studio divides every stat in the game by 10. What is the power gap before and after?
4. Add sword E (DPS 90, 92, 76) to the table in section 3. Which swords does it dominate? Which sword, if any, is horizontal to E?
5. You want a shelf life of at least 5 tiers at `F = 1.5`. What is the largest `r` you can use?

<details>
<summary>Answers</summary>

1. `t* = ln 2 / ln 1.15 ≈ 0.693 / 0.140 ≈ 4.96`. At 5 tiers apart the gap is `1.15⁵ ≈ 2.01`, just over 2, so up to 4 tiers apart.
2. `P_h(4) = 1.5`, `P_h(1) = 1.125`. Gap `1.5 / 1.125 ≈ 1.33`. The veteran pays `60% / 1.33 = 45%`.
3. `1.1¹² ≈ 3.14` before and after. Dividing both players by 10 cancels in the ratio.
4. E dominates B (90 ≥ 80, 92 ≥ 90, 76 ≥ 50) and C (90 ≥ 85, 92 ≥ 65, 76 ≥ 75). It does not dominate A or D, because both beat it on single target (100 and 105 against 90) while E beats both in the other columns. A and D are horizontal to E. E's expected DPS is `45 + 27.6 + 15.2 = 87.8`, which beats D's 84.5, so D stops being the default.
5. `r^5 ≤ 1.5`, so `r ≤ 1.5^(1/5) ≈ 1.084`. About 8% per tier.

</details>

## Lab / assignment hook

**Lab 14, progression audit** ([`labs/lab14.md`](../labs/lab14.md)). You receive a two-year content plan and an eight-weapon reward table. You compute the power gap across tiers, the shelf life, a dominance matrix and expected values under two content mixes, then write a redesign memo. It feeds directly into the progression section of your final combat system spec.

## Sources

- Warcraft Wiki, "Stat squish". WoW stat squishes in patch 6.0.2 (2014) and 8.0.1 (2018); level, item level and stat squish in patch 9.0.1, with level 120 characters becoming level 50; level cap history from 60 (2004) to 120 (Battle for Azeroth).
- Wikipedia, "World of Warcraft: Shadowlands", and Blizzard Watch, "We finally know exactly what level your character will be in Shadowlands" (September 2020). Pre-patch 9.0.1 released October 2020; new cap of 60.
- Guild Wars 2 Wiki, "Ascended equipment". Introduced from The Lost Shores (16 November 2012) onward; 5% stronger stats than exotic, equal to legendary.
- Guild Wars 2 Wiki, "Level". Maximum character level 80 (current live game).
- ArenaNet, "Reimagining Progression: The Mastery System" (guildwars2.com, 2015), and Guild Wars 2 Wiki, "Mastery". Heart of Thorns kept the level cap at 80 and added account-wide masteries.
- Guild Wars 2 Wiki, "Dynamic level adjustment". Downscaling keeps skills, traits and gear.
- Massively Overpowered, "Wisdom of Nym: Classes, job, and the Armoury System in Final Fantasy XIV" (2017), and Gamer Escape FFXIV wiki, "Armoury". One character can change class or job by changing equipped weapon or tool (A Realm Reborn onward).
- Schreiber, I. (2010). *Game Balance Concepts*, Level 6, "Situational Balance". Expected value of situational options weighted by encounter frequency.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Chapters "Progression in PvE Games" and "Progression in PvP Games".

## Interactive spec: examples/w14-power-gap.html

**The one insight.** Vertical progression looks like the stronger design on a power-over-time chart, and it is the one that splits players apart on a "can we play together?" chart. The crossing point is `t* = ln F / ln r`, and horizontal progression never crosses.

**Layout.** Two linked panels, side by side at 1280px and stacked at 390px, with controls below. A second tab holds the sidegrade checker.

**Left panel, "Power over time."** Line chart, x-axis tiers played 0 to 15, y-axis power multiplier, linear, auto-scaled with a minimum top of 2.
- Vertical veteran, `P_v(t) = r^t`, drawn in blood.
- Horizontal veteran, `P_h(t) = 1 + b × min(t + 1, n) / n`, in steel (starts with one tool at tier 0, gains one per tier, caps at `n`).
- Newcomer reference, a flat dashed ink line at the power of a tier-0 player in the chosen mode (1 for vertical, `1 + b/n` for horizontal).
- A vertical cursor at the selected tier `t` with values labelled.

**Right panel, "Can a veteran at tier t and a newcomer share an encounter?"** Line chart, same x-axis. y-axis power gap `G`, log scale from 1 to 8.
- Vertical gap `G_v(t) = r^t`.
- Horizontal gap `G_h(t) = P_h(t) / (1 + b/n)`.
- A shaded region above `G = F` labelled "outside the band". The crossing point of `G_v` with `F` is marked with a dot and a label "shelf life t* = {value}".

**Readout (exact numbers).** Table for the selected `t` with rows Vertical and Horizontal and columns Veteran power, Newcomer power, Gap G, Veteran health cost when the newcomer's is 50% (`50% / G`), Inside band?. Plus a line "Shelf life t* = ln F / ln r = {value} tiers" and "Horizontal ceiling (1 + b)/(1 + b/n) = {value}". Show 3 decimals for powers and gaps, 2 for margin gaps and `t*`.

**Controls.**
- `r` slider 1.00 to 1.50, step 0.01, default 1.10.
- `F` slider 1.2 to 4.0, step 0.1, default 2.0.
- `b` slider 0 to 1.0, step 0.05, default 0.30.
- `n` stepper 2 to 12, default 6.
- `t` slider 0 to 15, default 8.
- Button "Stat squish ÷10": divides all plotted powers on the left by 10 (and relabels the axis), leaves the right panel unchanged, and shows the caption "Gap unchanged: a squish rescales, it does not close gaps." Press again to undo.
- All controls keyboard operable with visible labels and live values; respects `prefers-reduced-motion` (no animated transitions).
- If `r = 1.00`, display shelf life as "unlimited".

**Formulas.**
```
Pv(t)   = r^t
Ph(t)   = 1 + b * min(t + 1, n) / n
Gv(t)   = r^t
Gh(t)   = Ph(t) / (1 + b/n)
tStar   = ln(F) / ln(r)          // r > 1
ceiling = (1 + b) / (1 + b/n)
```

**Test values.**
- `r = 1.10, F = 2`: `t* = 7.27`. At `t = 7`, `G_v = 1.949`, veteran cost 25.7%, inside. At `t = 8`, `G_v = 2.144`, veteran cost 23.3%, outside.
- `r = 1.25, F = 2`: `t* = 3.11`. `r = 1.05`: `t* = 14.21`. `r = 1.15`: `t* = 4.96`.
- `r = 1.10, F = 1.5`: `t* = 4.25`.
- `b = 0.3, n = 6`: ceiling 1.238; at `t = 2` (k = 3), `P_h = 1.150`, `G_h = 1.095`.
- `b = 0.5, n = 4`: ceiling 1.333.
- Squish at `r = 1.1, t = 12`: left panel shows 0.314 instead of 3.138; right panel still shows `G_v = 3.138`.

**Second tab, "Sidegrade checker."** An editable table of up to 6 options by 3 situations (default rows are swords A to D from section 3), plus three frequency inputs that must sum to 100% (default 50/30/20; normalise if they do not). Output 1: a dominance matrix where a cell reads "dominates" if the row option is ≥ the column option in every situation and > in at least one. Output 2: expected value per option, with any option more than a chosen tolerance (default 3%) above the median highlighted. Test: with defaults, D dominates A only; expected values A 78.0, B 77.0, C 77.0, D 84.5; D highlighted. Adding E (90, 92, 76) gives E dominates B and C, E expected value 87.8.
