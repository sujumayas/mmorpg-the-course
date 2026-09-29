# MMO407 · Week 07 — Case: Classic and legacy servers

**Why this matters:** A classic server is a launch where you already know the content, the players already know the answers, and the old game's social problems come back at a scale the old game never had. The launch-night queue is the part everyone plans for. The part that decides whether the realm is alive in a year is slower and quieter: one faction gets a little bigger, new players follow it, the other side leaves, and six months later a "PvP realm" has nobody to fight. This week you learn to model that tip, to see it coming in the first weeks, and to choose between fighting it and finishing it.

**You will be able to:**
- Compute the weekly faction shares on a realm from a bandwagon model with joining and leaving rules, and predict how many weeks a small imbalance takes to reach 70/30 and 90/10.
- Explain why an even split is an unstable balance point when newcomers follow the crowd, and name the parameter that makes it stable.
- Compare balancing levers (creation locks, transfer prices and caps, periodic team reshuffles) by what each one costs in turned-away players and in broken friendships.
- Critique a legacy-server plan (frozen, progression or fresh-start) by the promise it makes to players and the operational problems that promise creates.

**Before class:** Read the Wowhead news post "Free Character Transfers to Mega Realms Coming Next Week" (16 September 2025), which reproduces Blizzard's forum announcement for Mists of Pandaria Classic in full (10 minutes). Read the Guild Wars 2 Wiki pages "World" (the sections on transferring and linked worlds) and "World Restructuring" (15 minutes). Reread GD102 week 3 on positive feedback loops.

**Prerequisites from earlier courses:** [GD102 week 3, positive feedback loops](../../GD102-systems-design-and-game-mechanics/lectures/w03-positive-feedback-loops-snowballing.md) (a loop that feeds itself runs away from where it started). [MMO302 week 2, shards, realms and layers](../../MMO302-mmo-server-architecture/lectures/w02-shards-realms-zones-instances-layers.md) (WoW Classic's 2019 launch and layering; this week does not repeat them). [MMO301 week 13, worlds that died](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w13-worlds-that-died-shutdowns-and-their-lessons.md) (the empty-shard spiral, which is about a realm's size; this week is about the split inside it). [MMO308 week 14, sunsetting content and servers](../../MMO308-live-operations-analytics-and-experimentation/lectures/w14-sunsetting-content-and-servers.md) (when a declining realm stops paying). [Week 2 of this course](w02-capacity-planning-and-login-queues.md) (how many realms to open on launch night).

**Interactive:** [examples/w07-faction-tipping.html](../examples/w07-faction-tipping.html). Keep it open during section 2.

---

## 1. Why studios reopen the past

A **legacy server** runs an older version of a live game next to the current one. Players ask for them because every expansion removes something. Old zones get rebuilt, old rules get simplified, and items that once mattered become unobtainable. Studios agree to run them because the content already exists, and because the demand is proven. Old School RuneScape and World of Warcraft Classic are the two largest cases, and they took different routes.

**Old School RuneScape (February 2013 onward).** Jagex rebuilt the game from an August 2007 backup of RuneScape found in its archives. It put the idea to a subscriber poll first. The poll drew 449,351 votes, enough for the project to go ahead, and the game opened on 22 February 2013. Jagex promised that new content would be polled, and it still is: updates other than balance and integrity fixes ship only if enough players vote yes. The pass threshold was 75% until 2022, when Jagex lowered it to 70%. The game broke its own concurrency record in August 2025, with a reported peak of 241,016 players. A legacy server that started as a restoration has become its own game.

**World of Warcraft Classic (August 2019 onward).** Blizzard launched Classic worldwide at one moment, 3 p.m. PDT on 26 August 2019 in the Americas and midnight CEST on 27 August in Europe, as a recreation of patch 1.12.1 from 2006. MMO302 week 2 covered its launch layering, and week 2 of this course covered the forecast Blizzard got wrong. Since then Blizzard has run several kinds of legacy realm side by side. **Progression** realms moved through re-releases of the next expansions in order. **Seasonal** realms changed the rules on purpose: Season of Mastery (November 2021), Hardcore realms with permadeath (August 2023) and Season of Discovery (November 2023). **Fresh** realms restarted the original game from level 1, as the 20th Anniversary Edition did on 21 November 2024. That edition moved on to The Burning Crusade on 5 February 2026.

Three kinds of promise, then:

| Kind | The promise | Example | The operational problem it creates |
|---|---|---|---|
| Frozen | "The game as it was." | Classic Era realms after progression moved on | Population only falls. Nothing new brings players back. |
| Progression | "The old game, then its sequels, in order." | WoW Classic moving through its expansions | Every expansion launch is a mini-launch, and players who liked one era leave at the next. |
| Fresh or seasonal | "Start again, together, from zero." | Hardcore, Season of Discovery, Anniversary realms | Every fresh start is a full launch: queues, then a tip, then consolidation. |

A legacy realm is never finished launching. Each fresh start re-runs the first months of an MMO, when the population inside each realm settles into its long-run shape. That shape is this week's subject.

### What is different about a legacy launch

Three things make a legacy realm behave differently from a new game's realm.

- **Players arrive informed.** They have read the guides, they know which class is strongest, and they know which faction had the better raid tools in 2006. Choices that were spread out in the original game now cluster.
- **Players arrive in groups.** Guilds reform before launch and pick a realm together, and communities that follow the same streamer or website often pick the same realm. The unit of arrival is often a guild of fifty, which makes the realm and faction choice lumpy.
- **The scale is modern.** The original realms were sized for the hardware and the audience of 2004. Legacy realms are sized for today's, and they concentrate harder.

All three strengthen the same effect, the tendency of new players to join whichever side is already bigger. Section 2 turns that tendency into a model.

## 2. Worked example: the realm that tipped

### The hook

On 16 September 2025, Blizzard announced free character transfers for Mists of Pandaria Classic in the Americas. Characters on a long list of realms, including Faerlina, Benediction and Whitemane, could move for free to one destination realm, Pagle. The same post re-flagged the region's PvP realms as PvE realms, and said the change would better reflect their current faction war status. A realm is flagged PvP so that the two factions can fight in the open world. Re-flagging it PvE says there was no longer much of a war to have. One side had taken over.

The same post kept a single realm for world PvP, Grobbulus, and put it under forced faction balancing. Transfers to Grobbulus could be halted for either faction without warning. Two years earlier, Blizzard had launched Season of Discovery with a similar rule from day one: on imbalanced realms, players could not create new characters of the dominant faction.

So the question is this. Every one of those PvP realms opened with two factions. Nobody set out to make them one-sided. How does a realm that starts at 55/45 end up at 95/5, and why did Blizzard's newer realms need a lock from the first day?

### The model

Take one realm with two factions, A and B. Count players who are active in a given week. Step forward one week at a time.

```
s        = A / (A + B)                          A's share of the realm
p        = s^k / (s^k + (1 − s)^k)              share of this week's newcomers who pick A
gap      = |2s − 1|                             0 when even, 1 when one-sided
A_next   = A × (1 − c − leave_A) + J × p
B_next   = B × (1 − c − leave_B) + J × (1 − p)
leave    = e × gap for the smaller faction, 0 for the bigger one
```

- `A` and `B` are the active players of each faction this week.
- `J` is the number of newcomers per week: new players, returning players and transfers in.
- `c` is the ordinary weekly churn, the share of players who leave for reasons that have nothing to do with factions.
- `k` is the **bandwagon strength**. At `k = 1`, newcomers split in the same proportion as the realm, so the share never moves. At `k = 2`, a faction with 55% of the realm attracts about 60% of the newcomers. At `k < 1`, newcomers favour the underdog.
- `e` is the **outnumbered penalty**, the extra weekly leaving rate on the smaller faction when the gap is total. The smaller side loses fights, loses contested resources and waits longer for groups, so some of its players leave or reroll.

The newcomer rule is the heart of it. A bigger faction offers more groups, faster raids and safer questing, so newcomers lean toward it. The rule `s^k / (s^k + (1 − s)^k)` is the simplest form that gives 50% at an even split, treats both factions alike, and lets `k` set how hard the crowd pulls.

The constants in this lecture are invented for teaching: `J = 1,000` per week, `c = 5%`, `k = 2` and `e = 0.2`. No studio publishes faction-choice curves. The shape of the result does not depend on the exact values, and the interactive lets you change every one.

### Numbers you can check

Start the realm at 5,500 players of A and 4,500 of B, a 55/45 split. Week 0:

- `s = 0.55`, so `s² = 0.3025` and `(1 − s)² = 0.2025`. Then `p = 0.3025 / 0.505 = 0.599`. Of 1,000 newcomers, 599 pick A and 401 pick B.
- `gap = 0.1`, so B's extra leaving rate is `0.2 × 0.1 = 0.02` and B loses 7% in total. A loses the ordinary 5%.
- `A = 5,500 × 0.95 + 599 = 5,824`. `B = 4,500 × 0.93 + 401 = 4,586`. The share is now 55.95%.

| Week | A | B | A's share | Newcomers to A | B's weekly loss |
|---|---|---|---|---|---|
| 0 | 5,500 | 4,500 | 55.0% | 599 | 7.0% |
| 1 | 5,824 | 4,586 | 55.9% | 617 | 7.4% |
| 2 | 6,150 | 4,630 | 57.0% | 638 | 7.8% |
| 3 | 6,481 | 4,630 | 58.3% | 662 | 8.3% |
| 4 | 6,819 | 4,582 | 59.8% | 689 | 8.9% |

Every column moves the same way. A bigger A attracts more newcomers, and a smaller B loses more players. Two loops push in one direction. By week 4 faction B has stopped growing, although the realm as a whole still grows.

Run it for a year and compare three realms, all starting at 55/45:

```python
def week(A, B, J=1000, c=0.05, k=2, e=0.2, lock=None, spill=0.5):
    """One week on a realm with factions A and B. Returns the new (A, B)."""
    s = A / (A + B)                          # A's share of the realm
    p = s**k / (s**k + (1 - s)**k)           # share of newcomers who pick A
    new_A, new_B = J * p, J * (1 - p)
    if lock is not None and s > lock:        # creation lock on the big faction
        new_B, new_A = new_B + spill * new_A, 0
    if lock is not None and 1 - s > lock:
        new_A, new_B = new_A + spill * new_B, 0
    gap = abs(2 * s - 1)                     # 0 when even, 1 when one-sided
    leave_A = c + (e * gap if s < 0.5 else 0)
    leave_B = c + (e * gap if s > 0.5 else 0)
    return A * (1 - leave_A) + new_A, B * (1 - leave_B) + new_B

for label, kw in [("bandwagon", {}), ("neutral", {"k": 1, "e": 0}),
                  ("lock at 55%", {"lock": 0.55})]:
    A, B = 5500, 4500
    row = []
    for w in range(53):
        if w in (0, 1, 4, 8, 12, 16, 26, 52):
            row.append(f"{100 * A / (A + B):.1f}")
        if w < 52:
            A, B = week(A, B, **kw)
    print(f"{label:12s}", " ".join(row), f"| minority at week 52: {min(A, B):,.0f}")
```

Output, with A's share at weeks 0, 1, 4, 8, 12, 16, 26 and 52:

```
bandwagon    55.0 55.9 59.8 68.1 79.8 90.7 99.4 100.0 | minority at week 52: 0
neutral      55.0 55.0 55.0 55.0 55.0 55.0 55.0 55.0 | minority at week 52: 8,688
lock at 55%  55.0 55.9 54.0 53.4 53.0 55.7 53.7 54.9 | minority at week 52: 7,121
```

The bandwagon realm crosses 70/30 in week 9 and 90/10 in week 16. By week 26 faction B has fewer than 100 active players. The realm did not shrink. It has more players than it started with, all of them on one side. On a PvP realm, that is a realm with no PvP.

The neutral realm never moves. With `k = 1` and no outnumbered penalty, 55/45 stays 55/45 for ever. Nothing about a 55/45 realm is doomed. The doom is in `k` and `e`.

The locked realm stays between 53% and 56% all year. The lock is not free. Half the newcomers who wanted to join A go to B instead, and the other half (the `spill` parameter) go somewhere else. Over the year the lock turns away about 3,650 players, and the realm ends with 15,785 active players against the bandwagon realm's 18,688. The designer traded about 16% of the realm's population for a realm that still has two sides.

### How small an imbalance is safe?

None, with `k > 1`. Run the model from other starting splits and count the weeks to 90/10:

| Starting split | Weeks to 90/10 |
|---|---|
| 51/49 | 27 |
| 52/48 | 22 |
| 55/45 | 16 |
| 60/40 | 12 |

Even a 51/49 realm is lopsided within six months. The even split is a balance point, since at exactly 50/50 nothing moves. But it is an **unstable** one. Like a pencil standing on its tip, any nudge grows. GD102 week 3 called this a positive feedback loop. Here you can see where the feedback lives: in `k > 1`, which makes the crowd's pull stronger than proportional, and in `e > 0`, which pushes the losing side out.

That tells you where to intervene. You can lower `k` (make the bigger side less attractive to newcomers), lower `e` (make the smaller side less miserable), or override the newcomer rule entirely with a lock. The model says the second matters more than it looks. With `e = 0.2`, even a strong underdog bonus (`k = 0.5`) tips the realm to 70/30 within about half a year, because a bonus reaches only newcomers while the penalty hits every player on the smaller side every week. With `e = 0`, any `k` below 1 pulls the realm back toward even. You cannot fix the tip by waiting, and the cheapest week to act is the first one, when a 1% nudge needs a 1% correction.

### Move it yourself

Open the interactive. The top chart shows A's share over 52 weeks, with a band from 45% to 55% marked "contested." The bottom chart shows the newcomer rule itself: the share of newcomers who pick A against A's share of the realm, with the diagonal `p = s` drawn for reference. Where the curve lies above the diagonal, the big faction gains every week. Drag `k` from 2 down to 1 and watch the curve flatten onto the diagonal while the top chart's line goes flat. Then set `k` to 0.7 and `e` to 0. The curve crosses the diagonal the other way, and the line in the top chart bends back toward 50%. Now raise `e` to 0.1 and watch the realm tip anyway, more slowly. An underdog bonus for newcomers does not help if the underdog's current players keep leaving. Turn on the creation lock and drag its threshold to see how late a lock can start and still hold.

### Cross-game recognition

The same loop appears wherever players choose a side and the sides compete. In each case, find `k`, `e` and the lever.

**World of Warcraft Classic (2023 to 2025).** Season of Discovery launched in November 2023 with a rule that locked character creation for the dominant faction on imbalanced realms. That is the model's `lock` from day one. In September 2025 Blizzard re-flagged the Mists of Pandaria Classic PvP realms in the Americas and Europe as PvE. In the Americas it kept one PvP realm, Grobbulus, under forced faction balance, and said transfers there could be halted for either faction at any time. A transfer halt is a lock applied to arrivals instead of new characters.

**Guild Wars 2, World versus World (2012 to 2024, then World Restructuring).** In Guild Wars 2's large-scale PvP mode, each "world" was a team, and players joined a world by picking a home world and paying gems to transfer. ArenaNet used three levers from the model, one after another. Transfer prices rose with the destination world's population (500, 1,000 or 1,800 gems for medium, high and very high), which lowers `k` by making the popular choice expensive. Worlds listed as Full could not accept transfers at all, which is a lock. From April 2016, low-population worlds were linked to larger ones and the links were redrawn every two months. On 14 June 2024 ArenaNet replaced worlds with World Restructuring. Teams are rebuilt about every four weeks from players' chosen guilds, aiming at even populations, and transfers between teams are closed during a match. That is the strongest lever of all. Instead of slowing the tip, it resets `s` to 50% every month.

**Outside games: Schelling's segregation model (1971).** The economist Thomas Schelling showed that residents with only a mild preference for neighbours like themselves could produce fully separated neighbourhoods, because each move made the next more likely. The sociologist Morton Grodzins had earlier called the moment a neighbourhood flips a "tipping point." Schelling's tolerance threshold plays the part of `k` and `e`. Small individual preferences plus feedback give extreme group outcomes that nobody wanted.

### Eyes-open design judgment

- **A lock is cheapest when it starts early.** In the interactive, a lock at 55% from week 0 holds the realm near balance and turns away about 3,650 newcomers over the year. The same lock switched on at week 16, when the realm is at 91/9, does pull the share back, to 70% by week 26 and 53.5% by week 52. That repair costs about 8,180 turned-away newcomers, more than twice as many, because for months almost every newcomer wants the big side. It also spends half a year as a realm with no PvP, and the B players who left do not come back. B is rebuilt from strangers. Season of Discovery's day-one lock is the model's advice.
- **Every lever breaks a social tie somewhere.** A creation lock tells a new player they cannot join their friends' faction. A transfer halt splits a guild that moves in stages, which Blizzard's own post acknowledged by advising groups to transfer at once. A monthly reshuffle, as in Guild Wars 2, breaks rivalries and server identity. Pick the tie your game can best afford to break.
- **Balance matters only where the sides compete.** On a PvE realm, a 90/10 split costs almost nothing, because the factions rarely interact. That is why re-flagging a tipped PvP realm as PvE is a legitimate move and not a surrender. The fight was over, so stop charging players for a war that no longer exists.
- **Decide what you are protecting.** If your game's promise is open-world faction war, `s` is a health metric. Put it on the live dashboard next to concurrency, with an alert at 55%. If your promise is a busy world, the realm's total size matters more, and section 3 shows the loop working in your favour.

### Check this example

1. With `k = 2`, a realm is at 60/40 this week. What share of newcomers picks the bigger faction?
2. With the lecture's constants, a realm is at 50/50 exactly. What happens next week? What happens if 100 extra players join A in one week?
3. A designer proposes `k = 0.8` by giving the smaller faction an experience bonus. Describe the long-run split and explain it with the newcomer rule.

<details>
<summary>Answers</summary>

1. `0.36 / (0.36 + 0.16) = 0.692`, so about 69% of newcomers.
2. Nothing moves: `p = 0.5` and `gap = 0`, so both factions change by the same proportion. After a nudge of 100 players to A, `s` is slightly above 0.5, so `p > s`, and the loop carries the realm away from 50%. The balance point is unstable.
3. For newcomers, `k < 1` puts the curve below the diagonal whenever `s > 0.5`, so the bigger faction attracts a smaller share of newcomers than it holds, which pulls toward 50%. But with the lecture's `e = 0.2` the realm still tips: the model gives 70% in week 19. The bonus acts only on newcomers, while the penalty removes smaller-side players every week. With `e = 0` the same bonus pulls the realm to about 52.6% by week 52 and closer to even after that. An experience bonus works only alongside changes that stop the smaller side's players from leaving.

</details>

## 3. The same loop picks realms

Replace "faction" with "realm" and the model still works. When players choose between several realms, a newcomer who wants a busy world picks the busiest one. That is the same rule with more than two options:

```
share of newcomers to realm i = pop_i^k / Σ pop_j^k
```

With `k > 1`, the biggest realm grows fastest and the smallest ones shrink. MMO301 week 13 showed what happens next to a realm that shrinks: it feels empty, so its churn rises, so it shrinks faster. The two models connect. Concentration across realms feeds the empty-realm spiral in the small ones.

Classic realms showed both. Some realms became far more popular than others. Blizzard's long-standing tool for that is the free one-way transfer, which the Warcraft Wiki describes being used both to relieve a crowded realm and to gather a community in one place. Its 2025 answer finished the concentration on purpose. The September 2025 post closed the source realms to new players, raised the caps on Pagle and Grobbulus to what it called effectively unlimited, and said Blizzard had seen overall increased satisfaction and engagement when players were on larger "mega realms," first in Season of Discovery and then on the Anniversary realms.

Here the model gives a clear rule. If players' `k` is above 1 and your technology can hold one very large realm, fighting concentration is fighting your players. Layering and modern hardware (MMO302 week 2) are what make "finish the tip" possible. A 2004 realm could not hold everyone. A 2025 realm can. If the technology cannot hold the crowd, you are back to week 2's plan: open enough realms for launch night, then merge before the small ones spiral.

The faction question is different, because a faction cannot be merged away. On a PvP realm the only fixes are the levers in section 2, applied early.

## 4. Running a legacy game: the promise problem

Every legacy server makes a promise about change, and the promise sets the operational problems.

### Frozen promises decay

"No changes" cannot be kept completely, because the old client's exploits and bot weaknesses will be found in days by a modern audience. A frozen realm also has a fixed amount of content, so once players finish it the only reason to log in is other players. MMO308 week 14's decline models apply directly.

### Change by vote

Old School RuneScape's answer is to let players vote on every content change. A proposal passes only with a supermajority, 70% since 2022 and 75% before that. A supermajority is a deliberate bias toward the status quo. With a 70% threshold, a change that 65% of voters want fails. That protects the game's identity, and it is also why some broadly popular ideas never ship. Lowering the threshold from 75% to 70% was Jagex choosing to let a little more change through. The threshold is a design parameter, like `k`.

### Fresh starts are launches

WoW Classic's seasonal and anniversary realms take the other route. They keep the old game but restart it on a schedule, which brings back lapsed players because everyone starts at level 1 on the same day. Each restart is also a full launch, with week 1's pipeline, week 2's queue and this week's tip. Season of Discovery's day-one faction lock is a studio applying its own post-mortem. When you plan a fresh start, plan its first 16 weeks, not just its first night.

### When the studio says no

Where a studio will not run the old version, players sometimes run it themselves on unofficial servers. [Week 11](w11-shutdowns-and-emulation-communities.md) covers emulation communities. Demand for a legacy version exists whether or not the studio serves it.

## In-class activity (25 minutes)

Groups of three. You are launching a fresh legacy realm for a two-faction MMO with open-world PvP. Your telemetry team can report faction shares daily.

1. Using the interactive, find the smallest starting split that reaches 70/30 within 12 weeks with the lecture's constants. (5 min)
2. Choose one lever: a creation lock (pick the threshold), a transfer price that rises with faction share, or a scheduled reshuffle. Write one sentence on which social tie it breaks. (5 min)
3. Model your lever in the interactive or by hand for 16 weeks from a 55/45 start. Record A's share at week 16 and the players turned away. (10 min)
4. Write the alert rule for your live dashboard: the metric, the threshold, and who acts when it fires. (5 min)

Expected output: the split from step 1, your lever with its week-16 share and cost, and a one-line alert rule. Two groups present; the class compares costs.

## Common misconceptions

- **"A 55/45 realm is close enough to even."** The number today matters less than which way it is moving. With `k > 1`, 55/45 is a realm on its way to 90/10. Watch the trend, not the level.
- **"Imbalance comes from one faction being better."** A stronger faction helps, but the model tips from pure chance. Even at 51/49 with identical factions, the bandwagon carries the realm to 90/10 in about half a year.
- **"Balancing levers are free if players can still play."** Every lever turns someone away or splits a group. The lock in section 2 cost about 16% of the realm's year-end population. Count the cost before you choose.
- **"Consolidation means the game is dying."** Mega realms can be a response to `k > 1` in a healthy game. A merge because of decline and a merge because players want crowds look the same on the realm list and mean opposite things in the telemetry.

## Check yourself

1. A realm is at 58/42 with the lecture's constants. Compute next week's newcomers to each faction and the smaller faction's total weekly leaving rate.
2. Two realms each start at 55/45. One has `k = 2, e = 0`. The other has `k = 1, e = 0.2`. Which one tips, and why? (Use the model, not the interactive.)
3. A Guild Wars 2-style reshuffle resets every team to 50/50 every four weeks. With the lecture's constants, roughly how far from 50% can a team drift before the next reshuffle, starting from 51/49? Use the weeks-to-threshold table and the week-by-week growth rate to estimate.
4. Your fresh realm launches with 10,000 players at 50/50, but a famous guild of 400 joins faction A in week 1. Estimate the week at which A's share passes 70%.

<details>
<summary>Answers</summary>

1. `s = 0.58`: `s² = 0.3364`, `(1 − s)² = 0.1764`, `p = 0.3364 / 0.5128 = 0.656`. So 656 newcomers to A and 344 to B. `gap = 0.16`, so B loses `5% + 0.2 × 0.16 = 8.2%` per week.
2. Both tip, and the penalty realm tips faster. With `k = 2, e = 0`, newcomers favour A but B loses only the ordinary 5%, so the realm drifts slowly and reaches 90/10 around week 50. With `k = 1, e = 0.2`, newcomers split exactly by share, so they never push the realm. But B loses extra players every week, which lowers its share and widens the gap, which raises its losses. That realm reaches 90/10 in week 27. Either parameter alone is enough to make the even split unstable.
3. From 51/49 the share grows by less than one point per week at first (the 51/49 row takes 27 weeks to reach 90%). In four weeks the team drifts only to roughly 52 to 53%. That is why a four-week reset holds: it acts while the imbalance is still in its slow phase.
4. After the guild joins, the realm is about 52/48. Reading from the table, a 52/48 start takes 22 weeks to 90/10, so 70/30 comes somewhat past halfway. Running the model gives 70% in week 17 and 90% in week 24. One guild at launch is enough to tip a realm within a season, which is why fresh realms need a balancing rule before launch.

</details>

## Lab / assignment hook

[Lab 07, faction balance simulator](../labs/lab07.md). You implement this week's model, reproduce the lecture's numbers, measure how the tip depends on `k` and `e`, and compare three levers on one fresh-realm launch. Deliverable: the simulator passing its tests and a one-page balance plan for a fresh realm, which becomes the "population health" section of your final launch plan.

## Sources

- Wowhead, "Free Character Transfers to Mega Realms Coming Next Week - Mists of Pandaria Classic" (16 September 2025), reproducing Blizzard's forum post. Free transfers from listed Americas realms (including Faerlina, Benediction, Whitemane) to Pagle from the 23 September maintenance, and EU transfers to Mirage Raceway from 24 September; PvP realms re-flagged PvE to reflect faction war status; Grobbulus kept as RP-PvP with forced faction balancing and transfer halts; Pagle and Grobbulus caps raised; source realms closed to new players; mega realms credited with higher satisfaction and engagement after Season of Discovery and Anniversary. https://www.wowhead.com/mop-classic/news/free-character-transfers-to-mega-realms-coming-next-week-mists-of-pandaria-378529
- Wikipedia, "World of Warcraft Classic" (accessed September 2026). Release 26 August 2019 (Americas; 27 August at midnight CEST in Europe) recreating patch 1.12.1; Season of Mastery from November 2021; Hardcore realms 24 August 2023; Season of Discovery with a creation lock on the dominant faction at launch (citing Blizzard's BlizzCon 2023 announcement); 20th Anniversary Edition 21 November 2024; move to The Burning Crusade on 5 February 2026; September 2025 mega realm transfers.
- Wikipedia, "Old School RuneScape" (accessed September 2026). Release 22 February 2013 from an August 2007 backup; the 2013 poll with 449,351 votes; content polls with the pass threshold lowered from 75% to 70% in 2022; concurrency record of 241,016 on 3 August 2025 as reported by GameSpot.
- Warcraft Wiki, "Character transfer" (accessed September 2026). Free one-way character migrations used to relieve highly populated realms or gather a community, for a fixed period and sometimes limited to one faction; Season of Mastery characters offered free transfers from 14 February 2023.
- Guild Wars 2 Wiki, "World" (accessed September 2026). Transfer fees by destination population (500, 1,000 and 1,800 gems); no transfers to Full worlds; world linking from 22 April 2016 to 14 June 2024, redrawn every two months.
- Guild Wars 2 Wiki, "World Restructuring" (accessed September 2026). Teams built from nominated guilds for even population; released 14 June 2024 after betas from September 2021; four-week matches with no transfers between teams during a match.
- Wikipedia, "Tipping point (sociology)" and "Schelling's model of segregation" (accessed September 2026). Grodzins' use of the term; Schelling's 1971 model in which mild preferences produce segregation.
- Schelling, T. C. (1971). "Dynamic models of segregation." *Journal of Mathematical Sociology* 1(2), 143-186.
- The model constants (`J`, `c`, `k`, `e`, the lock's `spill`) are invented for teaching. No studio has published faction-choice data in this form.

## Interactive spec: examples/w07-faction-tipping.html

**The one insight:** when newcomers follow the crowd (`k > 1`), an even split is an unstable balance point. A tiny imbalance grows by itself into a one-sided realm within months, and a lever works only if it acts before the tip.

**Layout (two linked views, stacked on mobile, side by side at 900px and wider):**

- View A, "the realm over a year": x is week 0 to 52. A line for A's share (0 to 100%) in `--blood`, with a shaded band from 45% to 55% labelled "contested" in `--moss`. A second, thinner line in `--steel` for total active players on a right-hand axis. A vertical cursor (default week 16) with a readout of A, B, share and newcomers that week. Mark the first week the share passes 70% and 90% with small labelled ticks.
- View B, "the newcomer rule": x is A's share of the realm `s` from 0 to 1, y is the share of newcomers who pick A `p(s)`. Draw the curve `p = s^k / (s^k + (1 − s)^k)` in `--blood` and the diagonal `p = s` dashed in `--ink-soft`. Shade the region where the curve is above the diagonal (for `s > 0.5`) in a light `--blood` wash labelled "big side gains," and below it in `--moss` labelled "small side gains." A dot on the curve at the current cursor week's `s`, linked to View A.

**Controls:**

- Starting share of A, 50% to 70%, step 1% (default 55%). Starting total 10,000.
- Bandwagon strength `k`, 0.5 to 3.0, step 0.1 (default 2.0).
- Outnumbered penalty `e`, 0 to 0.5, step 0.05 (default 0.2).
- Newcomers per week `J`, 0 to 3,000, step 100 (default 1,000).
- Base churn `c`, 1% to 15%, step 1% (default 5%).
- Lever selector: "none" (default), "creation lock", "reshuffle every N weeks".
  - Creation lock: threshold 51% to 80%, step 1% (default 55%); start week 0 to 40 (default 0); spill 0 to 1, step 0.1 (default 0.5).
  - Reshuffle: period 2 to 12 weeks (default 4). At the end of each period, set `A = B = (A + B) / 2`.
- Preset buttons: "Lecture realm" (defaults), "Neutral (k = 1, e = 0)", "Underdog bonus (k = 0.7, e = 0)", "Late lock (start week 16)", "51/49 start".
- Cursor week (draggable in View A, and a slider for keyboard users).

**Readout (always visible, `aria-live="polite"`):** share at the cursor, first week at 70% and at 90% (or "never"), minority size at week 52, total players at week 52, players turned away by the lock over the year, and a one-line verdict ("Tipped by week 16", "Held within 45-55%", "Tipped before the lock started").

**Formulas (one-week steps, `w = 0 … 51`):**

```
s = A / (A + B);  p = s^k / (s^k + (1 − s)^k)
newA = J × p;  newB = J × (1 − p)
if lock on and w ≥ lock_start and s > T:      turned += (1 − spill) × newA;  newB += spill × newA;  newA = 0
if lock on and w ≥ lock_start and 1 − s > T:  turned += (1 − spill) × newB;  newA += spill × newB;  newB = 0
gap = |2s − 1|
leaveA = c + (s < 0.5 ? e × gap : 0);  leaveB = c + (s > 0.5 ? e × gap : 0)
A = A × (1 − leaveA) + newA;  B = B × (1 − leaveB) + newB
reshuffle on and (w + 1) % N == 0:  A = B = (A + B) / 2
```

"Turned away" counts the locked-out newcomers who leave the realm instead of joining the other faction.

**Test values (must match, defaults unless stated):**

- Week 1: A = 5,824, B = 4,586, share 55.9%. Week 4: share 59.8%. Week 8: 68.1%. Week 16: 90.7%. First week at or above 70%: 9. First week at or above 90%: 16.
- Neutral preset: share 55.0% at every week.
- Lock at 55% from week 0: share at week 52 is 54.9%; minority at week 52 is 7,121; total 15,785; turned away about 3,653.
- Bandwagon (defaults): total at week 52 is 18,688; minority at week 52 below 1.
- Start 51/49: first week at or above 90% is 27. Start 60/40: 12.
- `p(0.6)` with `k = 2` is 0.692.
- Underdog bonus preset (`k = 0.7`, `e = 0`): share 51.9% at week 52. With `k = 0.8`, `e = 0.2`: first week at or above 70% is 19.

**First screen:** defaults with the cursor at week 16. Caption: "This realm started at 55/45. Nobody changed anything. It is now 91/9. Drag k to 1."

**Accessibility:** every control keyboard operable with visible focus; the cursor moves with arrow keys (1 week) and Shift plus arrows (4 weeks); readout in `aria-live="polite"`; the share line also listed in a collapsible table of weeks 0 to 52; respects `prefers-reduced-motion` (no animated transitions) and `prefers-color-scheme`; tokens from `templates/interactive-tokens.css` inline. Generic shapes only: two coloured banners for the factions, no game art, logos or faction emblems.
