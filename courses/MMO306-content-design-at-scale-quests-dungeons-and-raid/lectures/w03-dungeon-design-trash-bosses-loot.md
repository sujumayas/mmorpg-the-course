# MMO306 · Week 03 — Dungeon Design: Trash, Bosses, Loot

**Why this matters:** Players judge a dungeon by its bosses and its loot, but they spend most of their time in it fighting trash. The numbers you give trash (health, damage, how tightly the packs sit) decide how players move through the space, how long a run takes, and whether the tank pulls one pack at a time or the whole corridor. If you can predict the pull size players will choose, you can design the dungeon they will actually play instead of the one on your whiteboard.

**You will be able to:**
- Compute kill time, tank survival time and clear time for a pull of `N` enemies, with and without an AoE target cap.
- Derive the largest safe pull from the tank's buffer and the healer's throughput, and predict how it shrinks as enemies scale up.
- Compare the trash rules of World of Warcraft's Mythic+, Diablo III's rifts and Guild Wars 2 by rewriting each in the same model.
- Design a dungeon's trash budget, boss spacing and loot so that the fastest route is also a route you intended.

**Before class:** Warcraft Wiki, "Mythic+" (15 minutes, the sections on completing a run and on loot). Diablo Wiki, "Nephalem Rift" (10 minutes, the progress bar and Greater Rifts). Reread MMO303 week 7's healer budget.

**Prerequisites from earlier courses:** [GD203 week 4, time to kill and time to die](../../GD203-combat-and-progression-design/lectures/w04-time-to-kill-and-time-to-die.md) set up the two clocks of a fight. This week runs them for a whole pack at once. [MMO303 week 7, healing throughput and mana economy](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w07-healing-throughput-and-mana-economy.md) defined healer throughput, and [MMO303 week 3, effective HP and effective DPS](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w03-effective-hp-and-effective-dps.md) the tank's buffer. We take both as given. [GD201 week 3, flow, pacing and intensity graphs](../../GD201-level-and-world-design/lectures/w03-flow-pacing-and-intensity-graphs.md) is the pacing tool for section 3. [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) and [MA102 week 10, pity timers](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w10-pseudo-random-distribution-and-pity-timers.md) cover the loot maths we use in section 4. From this course, [week 1](w01-the-content-treadmill-production-vs-consumption.md) introduced the replay multiplier that loot exists to raise.

**Interactive:** [`examples/w03-pull-size.html`](../examples/w03-pull-size.html). Keep it open during section 2.

---

## 1. Three parts of a dungeon

A **dungeon** here means an instanced area for a small group, usually five players, with a fixed layout, several bosses and a reward at the end. It has three parts, and each does a different job.

**Trash** is every enemy that isn't a boss. Designers use it to pace the space between bosses, to teach a mechanic the next boss will test, to wear down the group's resources, and to make the place feel inhabited. Trash comes in **packs**, groups of enemies standing together that fight as one when any of them is attacked. Engaging a pack is a **pull**. A tank who drags two or three packs into one fight is making a big pull.

**Bosses** are the named enemies with their own mechanics. They are the skill checks and the story beats. Weeks 4 to 6 are about bosses. This week treats a boss as a block of time and a place in the pacing.

**Loot** is what the dungeon pays. It is the reason players come back, which in week 1's terms is most of the replay multiplier `r`.

A useful first sketch of any dungeon is its time budget.

```
run time = trash time + boss time + travel time
```

Most players can tell you a dungeon's boss count. Few can tell you its trash time, and it is usually the biggest term. That is where the design decisions hide.

## 2. Worked example: how big should a pull be?

### The hook

World of Warcraft's Mythic+ system turns five-player dungeons into a timed challenge. The Warcraft Wiki describes the goal as defeating every boss and a set amount of trash before the timer runs out. The game tracks that trash as **enemy forces**, a percentage that fills as enemies die. Each keystone level makes enemies 8% tougher and 8% more damaging (as of The War Within). A death costs the group time on the clock.

Watch a Mythic+ group at a low keystone and the tank runs ahead, gathers two or three packs, and the group burns them down together. Watch the same dungeon at a high keystone and the tank pulls one pack at a time, carefully. Same dungeon, same players, very different run. Why does the best pull size shrink as the numbers rise? And what does that tell you, as the designer who placed the packs?

### The model

Take a pull of `N` identical enemies. The group damages them with area-of-effect (AoE) attacks, which hit every enemy in the pull at once.

```
kill time       t_kill(N) = H / A                  if N ≤ m
                          = H × N / (A × m)        if N > m
survival time   t_surv(N) = B / (N × d − Q)        if N × d > Q, otherwise the tank never drops
the pull works  when t_kill(N) ≤ t_surv(N)
clear time      = (M / N) × (t_kill(N) + w)
```

- `H` is each enemy's health.
- `A` is the damage per second the whole group's AoE deals to each enemy it hits.
- `m` is the **target cap**: the most enemies AoE can hit at full strength. Past the cap, the same total damage is shared among all `N`, so each enemy takes `A × m / N`.
- `d` is the damage per second one enemy deals to the tank after mitigation.
- `Q` is the healer's sustained healing per second on the tank (MMO303 week 7).
- `B` is the tank's buffer, the health the tank can lose before dying (MMO303 week 3's effective HP, spent down).
- `M` is the total number of trash enemies the group must kill, and `w` the seconds of walking and waiting between pulls.

The model assumes all `N` enemies die together, which is close to right when they have the same health and all take AoE. It ignores crowd control and cooldowns, which you add in the lab.

### Numbers you can check

Invented numbers for one trash type: `H = 1,000`, `A = 50`, `d = 30`, `Q = 150`, `B = 3,200`, `w = 10` seconds, and `M = 120` enemies in the dungeon. Two target caps, 5 and 20.

| Pull `N` | `t_kill`, cap 20 (s) | `t_kill`, cap 5 (s) | `t_surv` (s) | Clear, cap 20 (min) | Clear, cap 5 (min) |
|---|---|---|---|---|---|
| 1 | 20 | 20 | never | 60.0 | 60.0 |
| 3 | 20 | 20 | never | 20.0 | 20.0 |
| 5 | 20 | 20 | never | 12.0 | 12.0 |
| 6 | 20 | 24 | 106.7 | 10.0 | 11.3 |
| 8 | 20 | 32 | 35.6 | 7.5 | 10.5 |
| 10 | 20 | 40 | 21.3 | 6.0 | wipe |
| 12 | 20 | 48 | 15.2 | wipe | wipe |

Check the `N = 8`, cap 5 row by hand. Past the cap each enemy takes `50 × 5 / 8 = 31.25` damage per second, so `t_kill = 1,000 / 31.25 = 32` seconds. The tank takes `8 × 30 = 240` per second and is healed for 150, so it loses 90 per second and lasts `3,200 / 90 = 35.6` seconds. The pack dies first, with 3.6 seconds to spare. The run needs `120 / 8 = 15` pulls of `32 + 10 = 42` seconds, 630 seconds, or 10.5 minutes.

Now read the cap-20 column. Kill time doesn't change with `N` at all while `N` is under the cap. AoE hits every enemy at once, so eight enemies die as fast as one. Every extra enemy in the pull is free time saved, and clear time falls as `1 / N`, from an hour at one enemy per pull to six minutes at ten. **Under the cap, the only thing that stops a bigger pull is the tank dying.** The healer and the tank set the pull size, not the damage dealers.

The cap-5 column shows what a target cap changes. Past five enemies, kill time grows with `N`, and the saving from bigger pulls shrinks. At `N = 10` the pack now takes 40 seconds to die while the tank lasts 21. A low target cap pushes the best safe pull down, from 10 to 8 here, and it makes the gain from pulling big much smaller (10.5 minutes against 6.0).

Here is the table from code:

```python
def kill_time(N, H, A, cap):
    """Seconds to kill a pull of N mobs with H health each, all hit by AoE."""
    per_target = A if N <= cap else A * cap / N   # past the cap, damage is shared
    return H / per_target

def survive_time(N, d, Q, B):
    """Seconds until the tank's buffer B runs out (None means never)."""
    net = N * d - Q
    return None if net <= 0 else B / net

def clear_minutes(M, N, H=1000, A=50, cap=20, d=30, Q=150, B=3200, walk=10):
    tk, ts = kill_time(N, H, A, cap), survive_time(N, d, Q, B)
    if ts is not None and ts < tk:
        return None                               # the tank dies first: a wipe
    return M / N * (tk + walk) / 60

for cap in (5, 20):
    cells = []
    for N in (1, 3, 5, 6, 8, 10, 12):
        m = clear_minutes(120, N, cap=cap)
        cells.append(f"N={N}: " + ("wipe" if m is None else f"{m:.1f}"))
    print(f"cap {cap:2d} |", " | ".join(cells))
```

It prints:

```
cap  5 | N=1: 60.0 | N=3: 20.0 | N=5: 12.0 | N=6: 11.3 | N=8: 10.5 | N=10: wipe | N=12: wipe
cap 20 | N=1: 60.0 | N=3: 20.0 | N=5: 12.0 | N=6: 10.0 | N=8: 7.5 | N=10: 6.0 | N=12: wipe
```

### Why the pull shrinks as enemies scale

Now scale every enemy's health and damage by the same factor, the way a keystone level does. At 8% per level, five levels multiply both by `1.08⁵ ≈ 1.47`, and ten levels by `1.08¹⁰ ≈ 2.16`. Keep the group's damage, healing and buffer fixed, and search every `N` for the fastest pull that doesn't wipe (cap 20).

| Scaling | Enemy `H` | Enemy `d` | Largest safe pull | Clear time (min) |
|---|---|---|---|---|
| ×1.00 | 1,000 | 30.0 | 10 | 6.0 |
| ×1.47 (5 levels) | 1,469 | 44.1 | 5 | 15.8 |
| ×2.16 (10 levels) | 2,159 | 64.8 | 3 | 35.5 |

Both numbers grew by the same 47% at five levels, but the pull halved and the clear time more than doubled. Scaling hits the run twice. Each enemy takes longer to kill, so the tank must survive longer. Each enemy hits harder, so the tank survives for less time. The two effects multiply, and the only way out is a smaller pull. That is the behaviour players show at high keys, and the model produces it from nothing but health, damage and healing.

In practice, players' gear also grows as they climb, so real groups shrink their pulls more slowly than this table. The direction is the same.

### A visual you can move

Open the interactive. The left view plots clear time against pull size `N`, from 1 to 20, as a curve that ends in a shaded "wipe zone" where the tank dies before the pack. A marker sits on the fastest safe pull. The right view shows one pull as a race between the tank's health falling over time and the pack's health falling over time, on the same axis. The pull works if the pack's line reaches zero first.

Start with cap 20. Drag `N` up from 1. On the left the curve falls steeply, and on the right the pack's line doesn't move while the tank's line tilts down faster. At `N = 11` the tank's line crosses zero first, and the left view shades that `N` as a wipe. Now switch the cap to 5. The pack's line on the right starts tilting too, once `N` passes 5. Finally drag the "enemy scaling" slider up. Both lines on the right steepen together, and the marker on the left walks back toward small pulls.

### Cross-game recognition

**World of Warcraft, the area damage cap (Mists of Pandaria, patch 5.2.0, 2013).** The Warcraft Wiki documents the rule our model uses for `m`. From patch 5.2.0, most AoE damage spells dealt full damage to up to 20 targets. Against more, the total was capped at 20 targets' worth and split evenly, so each target took `damage × 20 / N`. That is our cap formula with `m = 20`. Later expansions gave many individual abilities their own target limits, so check current values before relying on 20. The principle holds whatever the number. Where the cap sits above the pulls a five-player group can survive, kill time is flat in `N` and the tank and healer set the pull size. That matches the big pulls Mythic+ groups make at low keystones.

**Guild Wars 2 (2012 onward).** Most AoE skills affect at most 5 targets, the 5 closest to the centre of the area, per the Guild Wars 2 Wiki. That is a hard cap rather than a shared one. In our model it is `m = 5` with the extra enemies taking nothing from that skill, which is harsher than the table's shared cap. Past five, big pulls barely speed up the kill and still raise incoming damage. A low cap makes pulling one or two packs the sensible default and takes away much of the incentive to gather a room.

**Diablo III (Nephalem and Greater Rifts, patch 2.1 onward).** A rift has a progress bar that fills as monsters die, with stronger monsters worth more. When it reaches 100%, a Rift Guardian boss spawns. Elite packs drop progress orbs worth 1% each. Greater Rifts add a 15-minute timer. This is Mythic+'s "enemy forces" with a different skin. The designer sets how much each enemy is worth, and the player chooses which enemies to kill. Diablo characters are built to kill whole screens at once, so kill time is nearly flat in `N` and density becomes the thing players optimise. They look for rift layouts packed with enemies, because denser packs mean bigger pulls.

Three games, one trade. Everywhere, `t_kill` is flat in `N` until something caps it, and `t_surv` falls with `N`. The target cap, the enemy's damage and the healer's throughput decide where those lines cross, and players find that point within days.

### Eyes-open design judgment

- **Decide the pull size you want, then set `d`, `H` and `m` to produce it.** If you want careful single-pack play, give trash high damage relative to the healer's throughput, so `t_surv` falls fast. If you want big, exciting pulls, keep trash fragile and the target cap high. Don't expect players to pull the way you imagined unless the numbers reward it.
- **A high target cap makes the tank and healer the pacing roles.** Under the cap, damage dealers can't speed up a pull by pressing harder, only by allowing a bigger one. That can be a good identity for tanks. It can also make damage dealers feel like passengers in trash.
- **A low target cap protects packs but flattens the reward for skill.** GW2's cap of 5 makes AoE predictable and keeps big pulls from trivialising content. It also removes a way for skilled groups to go faster.
- **Scaling punishes big pulls twice.** Any difficulty system that multiplies enemy health and damage together shrinks the best pull faster than either factor alone. If you want high-difficulty runs to feel different, that's a gift. If you want them to feel like the same run with bigger numbers, scale one of the two, not both.
- **Players will route around you.** Once trash counts as a total, players choose which packs to kill. Section 3 is about making the fastest route one you intended.

### Check yourself (worked example)

1. With the base numbers and cap 20, a healer upgrade raises `Q` to 210. What is the largest safe pull now, and the clear time at that pull?
2. With cap 5, why does raising `Q` help less than with cap 20? Use `N = 10` to show it.

<details>
<summary>Answers</summary>

1. `t_kill = 20` for any `N ≤ 20`. The pull works while `3,200 / (30N − 210) ≥ 20`, so `30N − 210 ≤ 160` and `N ≤ 12.3`. The largest safe pull is 12, and clear time is `120 / 12 × (20 + 10) / 60 = 5.0` minutes.
2. With cap 5, `N = 10` has `t_kill = 40` seconds. With `Q = 210` the tank lasts `3,200 / 90 = 35.6` seconds, still under 40, so the pull still wipes. Past the cap, kill time grows with `N`, so the tank must survive longer for every extra enemy, and healing has to grow much faster to keep up.

</details>

## 3. Trash budgets, routes and boss spacing

### Forces and slack

A Mythic+ dungeon asks for 100% enemy forces, not for every enemy. When the enemies on the map add up to more than 100%, players choose which to kill. Call the ratio **forces slack**, by analogy with GD201 week 10's gate slack.

```
forces slack = total forces available / forces required
```

With a slack of 1.0, players kill everything, and the route is fixed. With a slack of 1.4, players can skip nearly a third of the trash, and they will skip whatever is slowest per percent of forces. Your job is to know which packs those are. Rank every pack by **forces per second**, its forces value divided by its kill time (plus the walk to it). The fastest route takes the highest-rate packs until it reaches 100%.

This is where the pull model comes back. A pack worth 3% that dies in 20 seconds is worth 0.15% per second on its own. Pull it together with a neighbour and both die in the same 20 seconds, so the pair is worth twice that. Packs that sit close together are worth more per second than the same packs spread out, because players can pull them together. **The distance between packs is a trash-value decision.**

Blizzard added a tool in patch 12.0.5 that shows how seriously it takes this. An optional feature called Lindormi's Glow, switched on by the tank, highlights the enemies that will help complete the enemy forces requirement. In effect the designer publishes a suggested route, so that groups who don't want to plan one can follow it. You may not want to go that far. But you should always know what your intended route is, and check that it is not much slower than the fastest one players will find.

### Boss spacing

A dungeon's intensity graph (GD201 week 3) has one peak per boss and one smaller bump per pull. Place bosses so that the trash between them does a job.

- **Teach before you test.** A trash pack that uses the next boss's mechanic, in a gentler form, is a free tutorial.
- **Leave a valley after each boss.** A short walk with no trash lets the group recover resources, check loot and reset. GD201 week 3's calm time.
- **Keep trash time per boss roughly even, or rising.** A dungeon with 12 minutes of trash before the first boss and 2 before the last feels front-loaded, even if the total is fine.

A simple budget for a 30-minute dungeon with four bosses might be four boss fights of about 3 minutes, about 15 minutes of trash split into three stretches of about 5, and 3 minutes of walking. Write the budget before building the layout, then check it against the pull model. If the pull model says players will clear your 15 minutes of trash in 8, your dungeon is a 23-minute dungeon.

## 4. Loot: what the dungeon pays

Loot is the replay engine. It decides how many times a player runs the dungeon, and it is the only part of the dungeon they take home.

Here is how Mythic+ pays out, according to the Warcraft Wiki (The War Within and Midnight eras). A chest at the end always holds one item, and a second if the group beat the timer. Items are awarded at random as personal loot, each fits the receiving player's class and specialization, and a player can trade an item to a party member if it isn't an upgrade for them. The Great Vault adds a weekly choice from any dungeon's table.

Turn that into a waiting time. Suppose a dungeon's table has `m` items a given player can use, the chest holds `i` items shared among 5 players, and every item on the table is equally likely. The chance that a run gives this player one specific item is `i / (5 × m)`, and the expected number of runs is the geometric mean from MA102 week 7:

```
expected runs for one specific item = 5 × m / i
```

With 12 usable items and a timed run (`i = 2`), that is 30 runs. Untimed (`i = 1`), it is 60. At about 30 minutes a run, a player chasing one item plays 15 to 30 hours for it. That is a large share of week 1's replay multiplier, from one line of loot rules.

Three design choices move that number.

- **Table size `m`.** Every item you add to a dungeon's table stretches the wait for every other item on it. Adding items is not free content. It is a longer grind for the items already there.
- **Items per run `i`.** A reward for beating the timer raises `i` for skilled groups. It turns skill into loot speed, which is motivating, and widens the gap between groups.
- **Deterministic paths.** A currency earned per run, spent on chosen items, puts a ceiling on the wait. World of Warcraft's crests and Final Fantasy XIV's weekly-capped tomestones both do this. MA102 week 10's pity timers are the random version of the same guarantee. Each shortens the worst-case wait and, by week 1's maths, the time until the player is done.

MMO305 week 5 covers how groups share loot among themselves when the game lets them. Here, the question is only how long the dungeon keeps each player coming back.

## In-class activity (25 minutes)

Groups of three. You are designing the trash for one wing of a dungeon: 40 enemies worth 1% forces each, in packs you choose, with 30% forces required from this wing. Use the base numbers from section 2 (cap 20).

1. **(8 min)** Split the 40 enemies into packs and place them on a corridor sketch with distances in seconds of walking. Mark which packs players can pull together (within 5 seconds of each other).
2. **(7 min)** Compute forces per second for each pack alone and for each pair that can be pulled together. Find the fastest route to 30%.
3. **(5 min)** Change one thing (a distance, a pack size or one pack's damage `d`) so that the fastest route passes through a pack you want every group to see, for example one that teaches the next boss's mechanic.
4. **(5 min)** Swap with another group. Find a faster route through their wing than the one they intended.

Expected output: a pack sketch, a forces-per-second table, the fastest route before and after your change, and the other group's counter-route.

## Common misconceptions

- **"Bigger AoE damage makes bigger pulls."** Under the target cap, AoE damage sets how fast every pull dies, not how big it can be. The tank's buffer and the healer's throughput set the size. More AoE damage shortens `t_kill` and so allows a slightly bigger pull, but healing is the main lever.
- **"Scaling enemies by 50% makes the dungeon 50% harder."** Scaling health and damage together shrinks the safe pull, so clear time grows much faster than 50%. The table in section 2 shows 47% scaling more than doubling the run.
- **"Trash is filler."** Trash is most of the run time, it sets the tank's and healer's pace, and its layout decides which route players take. It is the part of the dungeon players play most.
- **"Adding items to a loot table adds content."** It lengthens the wait for every item already on the table. Sometimes that's what you want. Decide it on purpose.

## Check yourself

1. A pack of 6 enemies has `H = 1,500` each. The group deals `A = 60` AoE damage per second to each target with cap 20. Each enemy deals `d = 25` to the tank, the healer heals `Q = 120`, and the tank's buffer is `B = 4,000`. Does the pull work?
2. The same pack sits 8 seconds of walking from a second, identical pack. Should the group pull both together? Compute both options' time per enemy.
3. A dungeon's packs add up to 125% forces with 100% required. A designer adds three more packs worth 5% each at the far end of a side corridor. What is the new slack, and will players kill the new packs?
4. A dungeon table has 15 items usable by a player, and the chest holds one item for the party (two if timed). How many runs does a player expect for one specific item if the group always times the run? What if the designer adds 5 more items?

<details>
<summary>Answers</summary>

1. `t_kill = 1,500 / 60 = 25` seconds. Incoming is `6 × 25 = 150`, net `150 − 120 = 30` per second, so the tank lasts `4,000 / 30 = 133` seconds. The pull works easily.
2. Alone: two pulls of `25 + 8` seconds (the walk counts once per pull), 66 seconds for 12 enemies, 5.5 seconds per enemy. Together: `N = 12`, `t_kill` is still 25 seconds (under the cap), incoming `300 − 120 = 180`, the tank lasts `4,000 / 180 = 22.2` seconds, which is less than 25. The double pull wipes. They should pull the packs one at a time, or bring more healing.
3. `140 / 100 = 1.4`. Players will kill the new packs only if their forces per second, including the walk down the corridor and back, beats the slowest packs on the current route. Far packs on a side corridor usually lose, so the new packs are likely to be skipped. Adding forces far from the path adds slack without changing routes.
4. Timed, `i = 2`: `5 × 15 / 2 = 37.5` runs. With 20 items: `5 × 20 / 2 = 50` runs. Five more items made the wait for each existing item a third longer.

</details>

## Lab / assignment hook

[Lab 03, pull planner](../labs/lab03.md). You implement the pull model, a search for the fastest safe pull, and a route planner that picks packs to reach a forces target in the least time. You then lay out the trash for the first wing of your final dungeon and show that the fastest route passes through the packs you meant players to fight.

## Sources

- Warcraft Wiki, "Mythic+" (The War Within and Midnight eras, retrieved September 2026). Defeat all bosses and a set amount of trash before the timer expires; enemies deal 8% more damage and have 8% more health per keystone level; death penalty (Challenger's Burden) of 5 seconds, 15 at level 12 and above; Challenger's Cache holds one item plus one if timed, awarded as personal loot and tradeable if not an upgrade; Lindormi's Glow added in patch 12.0.5 to highlight enemies that complete the enemy forces requirement; crest rewards scale by keystone level (patch 11.0.7). https://warcraft.wiki.gg/wiki/Mythic%2B
- Warcraft Wiki, "Area of Effect" (Mists of Pandaria, patch 5.2.0; later per-ability limits not covered). Area damage cap of 20 targets; beyond it, damage per target is `DamagePerTarget × 20 / NumberOfTargets`. https://warcraft.wiki.gg/wiki/Area_of_Effect
- Guild Wars 2 Wiki, "Area of effect" (game version as of 2026). An AoE skill affects at most 5 targets, the closest to the centre of the area. https://wiki.guildwars2.com/wiki/Area_of_effect
- Diablo Wiki (Fandom), "Nephalem Rift" (Diablo III, patch 2.1 onward). Progress bar filled by kills, stronger monsters worth more; Rift Guardian at 100%; progress orbs worth 1% from elites; Greater Rifts added in patch 2.1 with a 15-minute timer. https://diablo.fandom.com/wiki/Nephalem_Rift
- Final Fantasy XIV Online Wiki (consolegameswiki), "Raids" (Dawntrail era, 2026). Weekly-capped tomestone gear alongside raid drops. https://ffxiv.consolegameswiki.com/wiki/Raids
- All trash, healing, buffer, walking and loot-table numbers in the worked example and activities are invented for teaching.

## Interactive spec: examples/w03-pull-size.html

**The one insight.** Under the target cap, a pack dies just as fast whether it holds one enemy or ten, so bigger pulls are free time until the tank's survival line crosses the kill line. The student must see the pack's health line stay put while the tank's line steepens as `N` rises.

**Layout.** Two linked views, side by side on wide screens, stacked on phones (race first on phones, since it carries the insight).

- **Left view, "Clear time vs pull size".** Line chart, x axis `N` from 1 to 20 (integers), y axis clear time in minutes (0 to 60, log scale toggle). Points for each `N`; points where the pull wipes are replaced by a shaded "wipe zone" band. A highlighted marker on the fastest safe `N`, labelled with its clear time. A vertical dashed line at the target cap `m`, labelled "target cap".
- **Right view, "One pull as a race".** Two lines over time, 0 to 60 seconds: the pack's remaining health as a share of `N × H` (it falls linearly and reaches zero at `t_kill`), and the tank's remaining buffer as a share of `B` (falls at `N × d − Q` per second, or stays flat if that is not positive). Label the crossing of zero for each. Banner above: "Pack dies first, with X s to spare" or "Tank dies first, X s before the pack".
- **Readout.** `t_kill`, `t_surv`, pulls needed `M / N`, time per pull, clear time, forces per second (with every enemy worth `100 / M` percent), and the largest safe `N`.

**Controls.**
- Pull size `N`: slider 1 to 20, default 1.
- Target cap `m`: segmented control 3, 5, 10, 20, "none". Default 20.
- Enemy scaling: slider 1.00 to 2.50, step 0.01, with tick labels for `1.08^L` at L = 0, 5, 10 (1.00, 1.47, 2.16). Multiplies `H` and `d`.
- Healing `Q`: slider 0 to 400, step 10, default 150.
- Tank buffer `B`: slider 1,000 to 8,000, step 100, default 3,200.
- Group AoE `A`: slider 10 to 150, step 5, default 50.
- Fixed values shown as text, editable in an "advanced" panel: `H = 1,000`, `d = 30`, `w = 10` s, `M = 120`.

**Formulas.**
- `t_kill = H / A` if `N ≤ m`, else `H × N / (A × m)`. With "none", always `H / A`.
- `t_surv = B / (N × d − Q)` if `N × d > Q`, else infinite.
- The pull works if `t_kill ≤ t_surv`.
- Clear time (minutes) `= (M / N) × (t_kill + w) / 60`, shown only when the pull works.

**Test values** (base numbers, scaling 1.00).
- Cap 20: `N = 1` 60.0 min; `N = 5` 12.0; `N = 8` 7.5; `N = 10` 6.0 (`t_surv = 21.3` s); `N = 11` wipes (`t_surv = 17.8` s against `t_kill = 20` s). Fastest safe `N = 10`.
- Cap 5: `N = 6` 11.3 min (`t_kill = 24` s); `N = 8` 10.5 min (`t_kill = 32` s, `t_surv = 35.6` s); `N = 9` wipes (`t_kill = 36` s, `t_surv = 26.7` s). Fastest safe `N = 8`.
- Cap 20, scaling 1.47 (`1.08⁵`): fastest safe `N = 5`, 15.8 min. Scaling 2.16 (`1.08¹⁰`): fastest safe `N = 3`, 35.5 min.
- Cap 20, `Q = 210`: fastest safe `N = 12`, 5.0 min (check yourself Q1).

**First screen.** Cap 20, `N = 1`, with a one-line prompt "Drag N up" next to the slider. The race view already shows the pack's line reaching zero at 20 seconds and the tank's line flat, so the first drag shows the pack line staying still while the tank line tilts.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Pack and tank lines differ by dash pattern as well as colour. The wipe zone uses a hatch pattern. All controls keyboard operable. No animation under `prefers-reduced-motion`.
