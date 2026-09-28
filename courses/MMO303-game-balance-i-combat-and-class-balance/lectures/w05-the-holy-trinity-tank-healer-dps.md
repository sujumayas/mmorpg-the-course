# MMO303 · Week 05 — The Holy Trinity: Tank, Healer, DPS

**Why this matters:** Most MMO group content assumes some mix of tanks, healers and damage dealers, and players spend a lot of their time waiting for the missing role. Roles are not a genre habit you inherit. They come out of three numbers every encounter sets, and once you can compute them you can decide which roles your game needs and how scarce each one will be.

**You will be able to:**
- Compute an encounter's three demands (damage check, healing check, spike check) from its numbers.
- Test every group composition of a given size against those demands and find which ones pass.
- Explain, with numbers, what a tank slot is worth in healing saved.
- Critique a shipped game's role structure (WoW, Final Fantasy XIV, Overwatch, Guild Wars 2) in terms of the demands its content sets.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapter on characters and classes (asymmetric balance). Sirlin, "Balancing Multiplayer Competitive Games" (GDC 2009), the parts on viable options.

**Prerequisites from earlier courses:** [MMO303 week 2, armor and effective HP](w02-armor-and-damage-mitigation.md). [MMO303 week 4, stacking mitigation](w04-stacking-mitigation-multiplicative-layers.md). GD203 [week 4, time-to-kill and time-to-die](../../GD203-combat-and-progression-design/lectures/w04-time-to-kill-and-time-to-die.md) and [week 5, DPS, burst and sustain](../../GD203-combat-and-progression-design/lectures/w05-dps-burst-and-sustain.md).

**Interactive:** [`examples/w05-role-composition.html`](../examples/w05-role-composition.html). Keep it open during section 2.

---

## 1. Three jobs, three demands

A **role** is a job a group needs done, filled by a player whose character is built for that job. The classic MMO split has three.

- A **tank** takes the boss's attention and absorbs its attacks. Tanks have high health and high mitigation, and deal modest damage.
- A **healer** restores health. Healers deal little damage and are fragile.
- A **DPS** (damage per second, used as a noun for the role) removes the boss's health. DPS characters are the most numerous role and are moderately fragile.

Players call this the **holy trinity**. The name suggests something fixed and sacred. It isn't. Each role exists because an encounter sets a **demand**, a minimum the group must meet or it fails. There are three demands that nearly every boss fight sets, whether the designer states them or not.

1. **Damage check.** The group must deal the boss's health `H` before some deadline `T`. The deadline can be a hard enrage timer (the boss kills everyone at `T`) or a soft one (the group runs out of healer mana). Required group damage is `H / T`.
2. **Healing check.** Incoming damage per second must not exceed healing per second for long, or the group dies. We count damage after mitigation.
3. **Spike check.** Some single attacks, or short bursts, are larger than a fragile character's health. Whoever the boss targets must be able to survive the largest spike before healers can react.

The trinity appears when these three demands are strong enough that no single character type can meet all of them. Each role is a specialist for one demand. If your encounters set weak demands, roles blur. If they set strong ones, roles harden.

## 2. Worked example: why a 5-player group has exactly one tank

### The hook

In World of Warcraft's Dungeon Finder, a random 5-player dungeon group is formed as 1 tank, 1 healer and 3 DPS. By the Cataclysm expansion, DPS players were facing long queues because too few tanks, and to a smaller degree healers, were queuing. In patch 4.1 (April 2011) Blizzard added a system called Call to Arms. It checks which role is least represented in the queue and pays players of that role a bonus reward bag for completing a random heroic dungeon.

So a game company built a system to pay players to take a role. Why would one role be so scarce that it needs a subsidy? And why does the group need *exactly* one tank? The answer is in the encounter's numbers.

### The model

Describe an encounter with five numbers.

- `H`, the boss's health.
- `T`, the enrage time in seconds.
- `B`, the boss's sustained raw damage per second against its current target.
- `R`, raid damage per second after mitigation, spread across the group.
- `S`, the largest single raw hit the boss's target must survive.

Describe each role with a few stats.

| Role | Damage per second `p` | Healing per second `q` | Mitigation `m` | Health `HP` |
|---|---|---|---|---|
| Tank | 400 | 0 | 60% | 6,000 |
| Healer | 100 | 700 | 20% | 3,000 |
| DPS | 1,000 | 0 | 20% | 3,000 |

A group has `t` tanks, `h` healers and `d` DPS, with `t + h + d = 5`. The boss attacks a tank if the group has one; otherwise it attacks whoever it likes, which here means a 20%-mitigation character.

The three checks become three inequalities.

```
Damage:  400 t + 100 h + 1000 d  ≥  H / T
Healing: 700 h                    ≥  B × (1 − m_target) + R
Spike:   HP_target                >  S × (1 − m_target)
```

The spike check is strict. A character left at exactly 0 health is dead, so the hit must leave at least 1 point. That is why a DPS with 3,000 health survives any hit below `S = 3,750` but not a hit of exactly 3,750.

`m_target` and `HP_target` belong to whoever the boss is hitting: 60% and 6,000 with a tank, 20% and 3,000 without.

### Numbers you can check

Use this encounter: `H = 600,000`, `T = 180 s`, `B = 1,000`, `R = 200`, `S = 5,000`.

The damage check requires `600,000 / 180 = 3,333` group DPS.

The healing check depends on the target. With a tank, the boss's 1,000 raw DPS becomes `1,000 × 0.4 = 400` after mitigation, plus 200 raid damage, so 600 HPS is needed. Without a tank it becomes `1,000 × 0.8 + 200 = 1,000` HPS.

The spike check also depends on the target. A tank takes `5,000 × 0.4 = 2,000` from the big hit and has 6,000 health. A DPS takes `5,000 × 0.8 = 4,000` and has 3,000. The DPS dies.

Now test compositions. There are 21 ways to split 5 slots among three roles. Here are the ones worth looking at.

| Tanks | Healers | DPS | Group DPS | Needed HPS | Group HPS | Spike | Result |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 3 | 3,500 | 600 | 700 | pass | **passes** |
| 0 | 1 | 4 | 4,100 | 1,000 | 700 | fail | fails heal, spike |
| 0 | 2 | 3 | 3,200 | 1,000 | 1,400 | fail | fails damage, spike |
| 1 | 0 | 4 | 4,400 | 600 | 0 | pass | fails heal |
| 1 | 2 | 2 | 2,600 | 600 | 1,400 | pass | fails damage |
| 2 | 1 | 2 | 2,900 | 600 | 700 | pass | fails damage |
| 0 | 0 | 5 | 5,000 | 1,000 | 0 | fail | fails heal, spike |

Check one row by hand. For 1-1-3, damage is `400 + 100 + 3 × 1,000 = 3,500`, which clears 3,333. Healing is 700, which clears 600. The tank survives the spike. Every other composition fails at least one check. You can verify the remaining 14 in the interactive.

One composition out of 21. The trinity was not assumed anywhere in the model. It came out of the numbers.

### What a tank slot is worth

Look at what the tank does in the table. It deals 600 less damage than a DPS would. In exchange, it changes the boss's target from a 20% character to a 60% one. That cuts the boss's damage after mitigation from 800 to 400. The tank is worth

```
healing saved = B × (m_tank − m_other) = 1,000 × (0.60 − 0.20) = 400 HPS
```

That is 57% of a healer. The tank also turns a lethal spike into a survivable one, which no amount of healing can do, because a dead character cannot be healed. So a tank's value has two parts. One part converts into healing and can be traded. The other part, spike survival, cannot be bought any other way.

This is why the group needs exactly one tank. The first tank saves 400 HPS and passes the spike check. A second tank saves nothing more, because the boss only hits one target at a time. It costs 600 DPS and fails the damage check. One target, one tank.

### The visual

The interactive draws all 21 compositions on a triangle. Each corner is a pure group (5 tanks, 5 healers, 5 DPS), and each dot is one composition. A dot is colored by which checks it passes. The encounter sliders move the boss numbers, and the role sliders move the role stats.

Start with the default encounter. One dot is green, at 1-1-3. Now drag `S` below 3,750, where `3,000 / 0.8 = 3,750` is the largest hit a DPS can survive. Then drag `B` down to 500. With `B = 500`, the tankless group needs `500 × 0.8 + 200 = 600` HPS, which one healer provides. The 0-1-4 dot turns green alongside 1-1-3. With low boss damage and no big spike, the tank has become optional. Drag `B` back up and the island shrinks to one dot again. The encounter numbers decide whether your game has a trinity.

### Cross-game recognition

Every game in this list sets the same three demands. They differ in how large each demand is, which changes the composition that passes.

**World of Warcraft.** Five-player dungeons use 1 tank, 1 healer and 3 DPS, the composition our model found. Boss damage is aimed at one target, spikes are large, and damage checks are tight enough that extra support costs a kill. The Call to Arms bonus in patch 4.1 is a direct sign that the demand for tanks (1 in 5 slots, 20%) was higher than the share of players choosing to tank.

**Final Fantasy XIV.** Four-player dungeons use 1 tank, 1 healer and 2 DPS. Eight-player trials use 2 tanks, 2 healers and 4 DPS. The second tank exists because those fights include tank swaps, where a boss debuff forces the main target to change. That is a spike check that one tank cannot pass alone, so the fight's demand creates the second slot. Same model, different `S` rule.

**Overwatch.** When Blizzard added Role Queue in August 2019, teams were locked to 2 tanks, 2 damage and 2 support. Overwatch 2 launched in October 2022 as 5 against 5 with 1 tank, 2 damage and 2 support. Removing a tank slot is a statement about the damage and spike checks in that game's fights. With one fewer body absorbing damage, the remaining tank had to be tuned to absorb more, and every one of the four other slots got more space to deal damage.

**Guild Wars 2.** At launch in August 2012, ArenaNet built its game without a dedicated healing class or a dedicated tank. Every profession has one healing skill slot for self-sustain. Open-world encounters set weak spike checks and spread damage across many players, so no specialist was required. When the game's first raid, Spirit Vale, arrived in November 2015 with the Heart of Thorns expansion, several of its bosses target the player with the highest toughness stat. That is a deliberate spike check pointed at one player, and it produced tank and dedicated-healer builds in organized raiding.

Put them in one form. Where the boss concentrates damage on one target with large spikes, a tank appears. Where damage is spread and the fight is long, a healer appears. Where both are soft, roles blur. Guild Wars 2 is the clearest test, because the same game produced both outcomes from different encounter numbers.

### Eyes-open design judgment

The trinity is a set of trade-offs. Choose it knowingly.

- **Strength.** Specialists make encounters readable. Each player has a clear job and can tell when they failed at it. Designers can write a mechanic for one role at a time.
- **Strength.** The tank concentrates boss damage on one well-mitigated target, which makes healing efficient. Our example saved 400 HPS per fight with one slot.
- **Cost.** Role scarcity becomes a queue problem. If the content needs 20% tanks and 10% of players want to tank, half the DPS waits. Section 3 does this math. No balance change inside the fight fixes it, because the problem is the player population.
- **Cost.** Hard demands make compositions brittle. In our example, exactly one of 21 compositions works. A group without a healer cannot even attempt the fight. Designers can soften this by leaving slack in each check, so near-miss groups can win with better play.
- **Cost.** Without strong demands, the removal of the trinity can simply relocate the problem. Guild Wars 2's open world works without roles. Its raids brought them back the moment bosses concentrated damage.

The decision for a designer is not "trinity or no trinity." It is how hard each of the three checks should be, per piece of content, and how much slack to leave.

## 3. Role supply: the queue math

A matchmaking queue is a small economy. Each group consumes a fixed recipe of roles, and the scarcest role, relative to its recipe, sets how many groups form.

```
groups formed = min( tanks / t, healers / h, dps / d )
```

Suppose, as a made-up illustration, a queue holds 100 tanks, 150 healers and 750 DPS, with the recipe 1-1-3.

```
tanks / 1   = 100
healers / 1 = 150
dps / 3     = 250
groups formed = 100
```

One hundred groups use 100 tanks, 100 healers and 300 DPS. Fifty healers and 450 DPS wait. The DPS wait is the sign of a tank shortage, not a DPS surplus.

A designer has four levers, and each has a cost.

1. **Pay the scarce role.** Call to Arms does this. It raises the reward for tanking without changing the fight. It costs reward budget and can feel unfair to players who already chose to tank.
2. **Make the scarce role more attractive.** Lower the stress of tanking with clearer boss telegraphs, more forgiving threat (week 6), or better tools. This changes the fight, so it is a balance change.
3. **Change the recipe.** Fewer tanks per group, as Overwatch 2 did going from 2 to 1. This is the biggest lever and it rewrites every encounter's spike and healing checks.
4. **Let hybrids switch roles.** If a class can tank or deal damage, some of the DPS surplus can convert. That works only if the class is competitive in both roles.

Week 7 studies healer throughput and mana in detail, and MMO306 covers dungeon and raid content pacing. For now, keep one idea. Every time you add a hard demand, you add a role your queue must supply.

## 4. Scaling to raids

A raid is a larger group, and it is not five-player content multiplied up. Two things change.

**Damage checks scale with group size, spike checks do not.** A 25-player boss has roughly five times the health of a 5-player one, because there are five times as many DPS. But the boss still hits one target at a time. Its single-target spike does not need five times as many tanks. That is why raids tend to run 2 or 3 tanks, not 5.

**Raid damage `R` becomes the dominant healing demand.** In a 5-player group, most healing goes to the tank. In a 25-player raid with heavy spread damage, most healing goes to the raid. The number of healers in a raid is then set by `R`, while the number of tanks is set by the number of simultaneous targets and swap mechanics.

A quick check with round numbers. A 20-player raid boss deals `R = 3,000` spread HPS after mitigation and `B = 2,000` raw DPS on its target. Two tanks at 60% mitigation take turns. Healing needed is `2,000 × 0.4 + 3,000 = 3,800`. At 700 HPS per healer, you need 6 healers (4,200 HPS). That leaves 12 DPS slots. If you want more DPS slots, you must lower `R`, not `B`.

## In-class activity (25 minutes)

In groups of three, design a 4-player dungeon boss for a game with roles that match the table in section 2.

1. Pick `H`, `T`, `B`, `R` and `S` so that exactly two compositions pass. Show all passing and failing compositions in a table.
2. Name the composition you want players to bring most often. Explain which check makes it better than the other passing one.
3. Change one number so the tank becomes optional. Say which one and by how much.
4. Hand your encounter to another group. They must find a composition you missed, or confirm your table.

Expected output: one page per group with the encounter numbers, the composition table and a two-sentence rationale.

## Common misconceptions

- **"The trinity is a tradition MMOs copy."** The compositions come out of encounter demands. Set different demands and a different composition passes, as the interactive shows.
- **"More healers is always safer."** Every healer slot costs damage. In the example, 1-2-2 heals twice as much as it needs and fails the damage check.
- **"A tank is worth the healing it saves."** That is half of it. The other half is spike survival, which cannot be traded for healing at any rate.
- **"Long DPS queues mean too many people play DPS."** They mean too few people play the scarcest role relative to the recipe. The fix is on the scarce side.

## Check yourself

1. Using the section 2 roles and encounter, a new boss has `B = 1,500` and everything else unchanged. How much HPS does a tanked group need? Does 1-1-3 still pass? If not, which composition does?
2. A tank's mitigation is buffed from 60% to 70%. How much healing does one tank slot now save against `B = 1,000`? Express it as a fraction of a healer.
3. A queue holds 80 tanks, 60 healers and 400 DPS, and the recipe is 1-1-2 (a 4-player light party). How many groups form, and which role is the bottleneck?
4. A designer wants to remove dedicated healers from their game but keep one tank per group. Which of the three checks must change, and in which direction?

<details>
<summary>Answers</summary>

1. With a tank: `1,500 × 0.4 + 200 = 800` HPS. One healer gives 700, so 1-1-3 fails the healing check. 1-2-2 heals 1,400 but deals `400 + 200 + 2,000 = 2,600`, failing damage. No 5-player composition passes. The boss needs a lower `H`, a longer `T`, or a stronger healer.
2. Saved healing `= 1,000 × (0.70 − 0.20) = 500` HPS, which is `500 / 700 = 71%` of a healer.
3. `min(80/1, 60/1, 400/2) = min(80, 60, 200) = 60` groups. Healers are the bottleneck. Twenty tanks and 280 DPS wait.
4. The healing check must become passable without a healer. Either sustained damage after mitigation (`B × (1 − m) + R`) must fall to what self-heals and the tank can cover, or the fight must be short enough that nobody runs out of health before `T`. The spike check can stay, because the tank passes it.

</details>

## Lab hook

**Lab 05, composition solver** ([`labs/lab05.md`](../labs/lab05.md)). You write a small solver (spreadsheet or Python) that enumerates every composition for a given group size, applies the three checks, and reports the passing set. You then tune three encounters to produce a target set of compositions.

## Sources

- Warcraft Wiki, "Call to Arms (dungeon)". Added in WoW patch 4.1.0 (April 26, 2011, Cataclysm era); detects the least represented role and awards a bonus bag for completing a random level-85 heroic; stated goal was shorter DPS queues caused by too few tanks and healers. https://warcraft.wiki.gg/wiki/Call_to_Arms_(dungeon)
- Blizzard Entertainment, "4.1 Preview: Dungeon Finder: Call to Arms" (2011). https://worldofwarcraft.blizzard.com/en-gb/news/10002882/41-preview-dungeon-finder-call-to-arms
- Final Fantasy XIV Online Wiki (consolegameswiki), "Party". Current era: light party 1 tank, 1 healer, 2 DPS for dungeons; full party 2 tanks, 2 healers, 4 DPS for trials. https://ffxiv.consolegameswiki.com/wiki/Party
- Overwatch Wiki, "August 13, 2019 Patch" (patch 1.39.1.0.60993). Role Queue with 2-2-2 went live. https://overwatch.fandom.com/wiki/August_13,_2019_Patch
- PC Gamer, "Overwatch 2 PvP will be 5v5 with only one Tank per team" (2021), and Wikipedia, "Overwatch 2" (release October 4, 2022). https://www.pcgamer.com/overwatch-2-pvp-will-be-5v5-with-only-one-tank-per-team/
- Ten Ton Hammer, "Guild Wars 2: No More Healers" (pre-launch coverage), and Guild Wars 2 Wiki, "Guild Wars 2" (release August 28, 2012). https://wiki.guildwars2.com/wiki/Guild_Wars_2 No dedicated healing profession; each profession has a healing skill slot. https://www.tentonhammer.com/articles/guild-wars-2-no-more-healers
- Guild Wars 2 Wiki, "Spirit Vale" and "Guild Wars 2: Heart of Thorns". Spirit Vale, the first raid wing, released November 17, 2015; Heart of Thorns released October 23, 2015. https://wiki.guildwars2.com/wiki/Spirit_Vale
- Guild Wars 2 Wiki, "Aggro". Several raid and strike bosses (Vale Guardian, Gorseval and others) target the player with the highest toughness. https://wiki.guildwars2.com/wiki/Aggro
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.
- Sirlin, D. (2009). "Balancing Multiplayer Competitive Games." Game Developers Conference.

## Interactive spec: examples/w05-role-composition.html

**The one insight.** Roles are not assumed. For a given encounter, only a small island of compositions passes all three checks, and moving the encounter's numbers moves or grows the island. The trinity appears when single-target damage and spikes are high.

**Layout.**
- **Main view, composition triangle.** A triangular grid for group size `N` (default 5). Corners are labeled "all tanks", "all healers", "all DPS". Each composition `(t, h, d)` with `t + h + d = N` is a dot at barycentric position `(t, h, d) / N`. For `N = 5` there are 21 dots. Dot fill: green if all three checks pass; otherwise a neutral fill with up to three small marks showing which checks fail (D for damage, H for healing, S for spike). The dot for 1-1-3 is labeled when visible.
- **Side panel, selected composition.** Clicking or keyboard-selecting a dot shows its three checks as horizontal bars, each with the requirement drawn as a vertical line and the group's value as the bar: group DPS vs `H/T`, group HPS vs needed HPS, target HP vs spike damage after mitigation. Numbers shown next to each bar.

**Controls.**
- Encounter sliders: `H` (100,000 to 1,500,000, step 10,000, default 600,000), `T` (60 to 600 s, step 10, default 180), `B` (0 to 3,000, step 50, default 1,000), `R` (0 to 1,500, step 50, default 200), `S` (0 to 10,000, step 250, default 5,000).
- Group size `N`: 4, 5, 8, 10.
- Collapsible "Role stats" with sliders for each role's `p`, `q`, `m`, `HP`, defaulting to the lecture table.
- Presets: "Default dungeon", "Soft boss (B = 500, S = 3,500)", "Check yourself Q1 (B = 1,500)".

**Formulas.**
- Group DPS `= Σ p_role × count_role`.
- Target: if `t ≥ 1`, the target is a tank (`m = m_tank`, `HP = HP_tank`). Otherwise the target is the non-tank role present with the highest `HP`, ties broken by highest `m`, then DPS before healer.
- Needed HPS `= B × (1 − m_target) + R`. Group HPS `= Σ q_role × count_role`.
- Spike damage `= S × (1 − m_target)`. Spike passes if `HP_target > spike damage`.
- Damage passes if group DPS `≥ H / T`.

**Test values (default roles).**
- Default encounter, `N = 5`: only (1,1,3) passes. (0,1,4): DPS 4,100, needed HPS 1,000, HPS 700, spike 4,000 vs 3,000 HP, fails healing and spike. (1,2,2): DPS 2,600 fails damage (needs 3,333.3).
- Soft boss, `B = 500`, `S = 3,500`: (1,1,3) and (0,1,4) pass. For (0,1,4): needed HPS 600, spike 2,800 vs 3,000.
- `B = 1,500`, other defaults: no composition passes at `N = 5`.
- `N = 4`, default encounter: no composition passes (max tanked DPS is 1-1-2 = 2,500).

**First screen.** Default encounter, `N = 5`, with the single green dot at 1-1-3 and its three bars shown in the side panel.
