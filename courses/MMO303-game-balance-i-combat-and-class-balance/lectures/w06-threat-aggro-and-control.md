# MMO303 · Week 06 — Threat, Aggro and Control

**Why this matters:** Last week's tank only works if the boss actually hits the tank. Threat is the system that decides who the boss attacks, and it quietly sets a speed limit on every damage dealer in the group. Get it wrong and your DPS players spend fights holding back, or your tank has nothing to do.

**You will be able to:**
- Compute when a damage dealer will pull aggro from a tank, from threat rates, head start and the switch threshold.
- Derive the maximum sustainable damage for a melee and a ranged attacker given a tank's threat rate.
- Explain what a taunt does to the threat race, and why it buys less time than players expect.
- Compare threat tables, stat-based aggro and fixed targeting rules, and choose one for a given design goal.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapter on combat and AI-driven opponents. Read the Warcraft Wiki "Threat" article for the classic-era rules (listed in Sources).

**Prerequisites from earlier courses:** [MMO303 week 5, the holy trinity](w05-the-holy-trinity-tank-healer-dps.md) (why a tank must be the target). [CS203, AI for games](../../CS203-artificial-intelligence-for-games/syllabus.md) (target selection as a decision rule). [MA101 week 2, linear functions and rates](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md) (lines and where two of them cross).

**Interactive:** [`examples/w06-threat-race.html`](../examples/w06-threat-race.html). Keep it open during section 2.

---

## 1. Who does the boss hit?

Week 5 showed that a tank saves healing and survives spikes, but only if the boss attacks the tank. Every game with a tank role needs a rule for this. The rule is called **aggro** (short for aggravation): the enemy's current choice of target. A character "has aggro" when the enemy is attacking them. "Pulling aggro" means taking it from someone else, usually by accident.

There are three broad families of aggro rules.

- **Threat tables.** Each enemy keeps a running score, called **threat** (or hate, or enmity), for every character in combat. Actions add threat. The enemy attacks whoever leads, with rules for when the lead changes hands. World of Warcraft and Final Fantasy XIV both use this.
- **Stat-based rules.** The enemy attacks whoever has the most of some stat, or is closest. Guild Wars 2 uses proximity as the main factor for ordinary enemies, and some raid bosses target the player with the highest toughness.
- **Scripted rules.** The encounter picks a target by script: a random player, the farthest player, a player marked with a debuff. Many modern boss mechanics layer these on top of threat.

Each family answers the same design question differently. How much work should holding a boss's attention take, and who should do the work?

## 2. Worked example: the threat race

### The hook

In classic World of Warcraft, a tank and a mage can both be hitting a boss, and the mage can be ahead in threat without the boss turning. The boss switches only when someone in melee range exceeds the current target's threat by 10%, or someone at range exceeds it by 30%. Players learn the rule of thumb "ranged can do more damage before pulling." But a mage with 20% more threat than the tank can still pull aggro if it happens to step into melee range. The same number, a different threshold.

So how long can a DPS player go all-out before the boss turns on them? And is there any damage they can sustain forever?

### The model

Classic WoW's rules, which we will use as the base model, work like this.

- Each point of damage adds 1 threat, times the attacker's **threat modifier**. Warriors in Defensive Stance have a 1.3 modifier. Most DPS play at 1.0.
- Healing adds 0.5 threat per point of effective healing, split equally across all enemies in combat.
- The boss switches target when a player in melee range has more than 110% of the current target's threat, or a player at range has more than 130%.

Assume each character adds threat at a constant rate, called **threat per second** (TPS), after an initial lead. Then threat is a straight line in time.

```
threat_tank(t) = L + τT × t
threat_dps(t)  = τD × t
pull when       threat_dps(t) > k × threat_tank(t)
```

- `L` is the tank's head start, the threat built before the DPS begins attacking.
- `τT` is the tank's TPS. `τD` is the DPS player's TPS.
- `k` is the switch threshold, 1.1 in melee and 1.3 at range.

Set the two sides equal and solve for time.

```
τD × t = k × (L + τT × t)
t_pull = k L / (τD − k τT)          if τD > k τT
t_pull = never                       if τD ≤ k τT
```

That is the whole model. Two facts come straight out of it.

1. **The rates decide whether you pull. The head start decides when.** If a DPS player's TPS is at most `k` times the tank's, they never pull, no matter how long the fight. If it is higher, they always pull eventually, and the head start only delays it.
2. **The threshold sets a speed limit.** The largest TPS a DPS can sustain forever is `k × τT`. For a player with threat modifier `c`, the damage limit is `k × τT / c`.

### Numbers you can check

Take a tank with `τT = 500` TPS and a head start of `L = 1,500` (three seconds of solo tanking). Compare a melee and a ranged DPS doing the same raw damage with a threat modifier of 1.0.

Speed limits: melee `1.1 × 500 = 550` TPS, ranged `1.3 × 500 = 650` TPS.

| DPS rate `τD` | Melee pull time (k = 1.1) | Ranged pull time (k = 1.3) |
|---|---|---|
| 500 | never | never |
| 600 | `1,650 / 50 = 33 s` | never |
| 700 | `1,650 / 150 = 11 s` | `1,950 / 50 = 39 s` |
| 800 | `1,650 / 250 = 6.6 s` | `1,950 / 150 = 13 s` |
| 1,000 | `1,650 / 450 = 3.7 s` | `1,950 / 350 = 5.6 s` |

Check the 700 row by hand. Melee: `k L = 1.1 × 1,500 = 1,650`, and `τD − k τT = 700 − 550 = 150`, so 11 seconds. At that moment the tank has `1,500 + 500 × 11 = 7,000` threat and the DPS has `700 × 11 = 7,700`, which is exactly 110% of 7,000.

The same 700 damage per second pulls in 11 seconds from melee and 39 seconds from range. That is the hook, explained. The threshold is part of the speed limit, and it is a different limit for melee and ranged players.

Now change the head start. With `τD = 700` in melee, doubling `L` to 3,000 doubles the pull time to 22 seconds. Halving it halves the time. Head start scales pull time linearly, which is why tanks are told to get a few seconds of threat in before DPS starts. But no head start turns a "pull eventually" into a "never."

### Taunts

A **taunt** is a tank ability that forces the enemy's attention. In classic WoW, Taunt sets the tank's threat equal to the highest threat on the table and forces the boss to attack the tank for a short time. Suppose the DPS has pulled aggro with threat `X`. After the taunt, the tank also has `X`. The new race starts with the tank's head start being the DPS's own threat, and the DPS needs `k X`.

```
t_pull_after_taunt = (k − 1) X / (τD − k τT)
```

With the 700 TPS melee DPS, `X = 7,700` at the moment of the first pull, so the taunt buys `0.1 × 7,700 / 150 = 5.1` seconds. Less than half the original 11. A taunt resets who is on top. It does not change the slopes. If the DPS keeps going at 700, they take the boss again five seconds later.

That is a good lesson to design around. Taunts fix a mistake. They do not fix a rate problem.

### The visual

The interactive plots cumulative threat over 60 seconds. The tank's line is solid. A shaded band above it marks the switch zone, bounded by `1.1 ×` tank threat (melee) or `1.3 ×` (ranged). Each DPS is a line from the origin. Where a DPS line leaves the band's upper edge, a marker shows the pull time.

Load the default. The 700 TPS melee line crosses the 110% edge at 11 seconds. Toggle that DPS to ranged: the band widens to 130%, and the crossing moves to 39 seconds. Now drag the DPS rate down to 550. The DPS line runs parallel to the band's edge and never crosses. Press the taunt button to see a new race start from the DPS's threat level, and watch it end five seconds later. Every time, the answer is in the slopes.

### Cross-game recognition

Every tank game solves the same race. The differences lie in how large `k` is, how large the tank's multiplier is, and whether threat exists at all.

**World of Warcraft after Cataclysm.** Blizzard raised tank threat modifiers several times. An August 2011 hotfix set tank threat generation to 500% of normal, up from 300%. In the model, that multiplies `τT` by 5 for the same damage. A tank dealing 200 damage per second now produces 1,000 TPS, and the melee speed limit becomes 1,100 TPS. Threat went from a constant constraint on DPS in the classic era to something most groups can ignore. Same equation, different number.

**Final Fantasy XIV.** Tanks have a stance that raises the enmity (FFXIV's name for threat) they generate. The Provoke action puts the tank at the top of the target's enmity list and adds extra enmity. That is a taunt that leaves a head start, not just a tie, which in the model means a positive `L` after the taunt instead of zero. Eight-player fights use Provoke for planned tank swaps, turning the taunt from an emergency fix into a scripted part of the encounter.

**Guild Wars 2.** Ordinary enemies choose targets mainly by proximity, with toughness, damage and other factors in the mix. Several raid bosses, including Vale Guardian and Gorseval, attack the player with the highest toughness, and switch if someone else's toughness becomes higher. There is no race at all. The tank's "head start" is a stat on their gear. `τT` and `τD` do not matter. The only question is whose toughness is highest.

Put them in one form. A threat table is a race between lines. Raising `k` or the tank's multiplier widens the gap. Stat-based aggro replaces the race with a sort. Scripted targeting replaces it with a rule the designer writes per fight.

### Eyes-open design judgment

- **Strength of a tight race (classic WoW).** Threat is a skill test for both roles. The tank must play well to raise `τT`. DPS must watch a threat meter and hold back near the speed limit. That creates cooperation and a visible reason for the tank to exist beyond soaking damage.
- **Cost of a tight race.** DPS players spend fights not pressing buttons, which feels bad. Your damage checks from week 5 become harder, because group DPS is capped at a multiple of the tank's TPS. In our numbers, three melee DPS at 550 each give 1,650 group DPS, far short of the 3,000 they could deal. If your damage check assumes full DPS, a tight threat race makes the fight impossible.
- **Strength of a loose race (post-2011 WoW).** DPS can go all-out. The damage check becomes the real test. Tanks focus on mitigation and positioning.
- **Cost of a loose race.** The tank loses a job. If threat never binds, a tank is only a mitigation stat block, and players ask why a tank needs its damage abilities at all.
- **Stat-based aggro.** Easy to read and zero-skill to maintain. It works well when you want targeting to be a gear decision and not a moment-to-moment one. It fails when two players' stats are close, because tiny changes flip the target.
- **Scripted targeting.** Full control for the encounter designer, and no threat math for players to learn. It is also the most work per fight.

A useful exercise before you pick is to write down the speed limit your threat rules impose, `k × τT / c`, and compare it with the DPS your damage check assumes. If the limit is below the assumption, the fight is impossible. If it is far above, threat does not exist in practice. The interesting space is between.

## 3. Healers and threat

Healing also adds threat. In the classic rules, each point of effective healing adds 0.5 threat, split equally across every enemy in combat. Overhealing (healing past full health) does not count.

Two consequences follow.

**Healers are safer on multi-enemy pulls.** A healer doing 800 HPS against one boss adds 400 TPS to that boss. Against four enemies, each enemy gets 100 TPS from the healer. The tank's threat is usually concentrated on one or two targets. So on a large pull, the enemies the tank ignores are the ones most likely to find the healer.

**Healers are at range.** Their threshold is `k = 1.3`. With a 500 TPS tank, the healer's limit on one boss is 650 TPS, or 1,300 HPS. That is well above what our week 5 healer produces. So in the default numbers, a healer only pulls aggro from a single boss if the tank is doing badly, or on adds that the tank has not touched.

This is why many games give tanks area-of-effect threat tools. The tool's job is to raise `L` on every enemy in the pull before the healer's split threat lands.

## 4. Control: beyond the threat table

**Control** is the broader set of tools that decide who gets attacked and when. Threat is one of them. Others:

- **Taunt and forced targeting.** Covered above. A single-target reset, often on a cooldown.
- **Fixate.** A boss or add ignores threat and chases one player for a fixed time. This is a scripted rule on top of a threat table, used to test a non-tank player.
- **Threat drops.** Abilities that reduce a player's own threat, by a percentage or to zero. In the model, a 50% threat drop halves the DPS player's line, which halves how far ahead they were and restarts the race from a better position.
- **Crowd control.** Stuns, roots and slows stop an enemy from acting on its choice. Week 8 treats crowd control and its diminishing returns in detail.

In PvP, none of this works the same way. Human opponents ignore threat. A PvP tank has no table to climb, so control tools (displacement, slows, abilities that punish the enemy for attacking someone else) become the tank's whole job. MMO307 takes this up for PvP balance. For now, note that a threat system is a PvE contract. It only binds opponents who agree to it, which is to say, AI-controlled ones.

## 5. Designing the threat budget

Put weeks 5 and 6 together into one design check. Given a tank's damage `p_T`, threat modifier `c_T`, and ability bonus threat, compute `τT`. Then compute each DPS's speed limit `k × τT / c_D`. Sum the limits for the planned composition. That sum is your **threat-limited group DPS**.

```
threat-limited group DPS = Σ over DPS of min(p_D, k_D × τT / c_D) + tank DPS + healer DPS
```

Compare it with the damage check `H / T`. Using week 5's tank (`p = 400`) with a 1.3 modifier and 180 TPS of bonus threat from abilities, `τT = 400 × 1.3 + 180 = 700` TPS. A melee DPS's limit is `1.1 × 700 = 770`, a ranged DPS's limit is `1.3 × 700 = 910`. A 1-1-3 group with three melee DPS has threat-limited DPS `400 + 100 + 3 × 770 = 2,810`. The week 5 damage check was 3,333. The fight fails.

With two ranged DPS and one melee, it is `400 + 100 + 910 + 910 + 770 = 3,090`. Still failing. The designer needs a tank with more threat, a longer enrage, or less boss health. Each fixes the same inequality, and each changes a different player's experience.

## In-class activity (25 minutes)

In pairs, tune the threat rules for a 5-player dungeon using week 5's default encounter (`H = 600,000`, `T = 180 s`, group 1-1-3, DPS at 1,000 raw damage each, all melee).

1. Choose `k` for melee and ranged, and the tank's threat modifier. Keep the tank's damage at 400.
2. Compute the tank's TPS and each DPS's speed limit. Does the threat-limited group DPS pass the 3,333 damage check?
3. Tune your choices so that the group passes only if DPS players hold back slightly (between 90% and 100% of their raw damage). Show the numbers.
4. Write a one-sentence patch note that explains your threat rule to players without showing the formula.

Expected output: a short table of `k`, modifiers, TPS, speed limits and group DPS, plus the patch note.

## Common misconceptions

- **"A big enough head start means the DPS will never pull."** Head start only delays. If the DPS rate exceeds `k` times the tank's rate, the DPS pulls eventually.
- **"Ranged players can do 30% more damage than the tank."** They can generate 30% more *threat* than the tank's total. The damage limit also depends on the tank's TPS, and on each player's threat modifier.
- **"Taunt fixes aggro problems."** Taunt ties the tank with the top player. The race restarts from a tie and ends sooner than the first one did.
- **"Removing threat makes tanks easier to design."** It removes one of their jobs. You must give the tank another reason to exist, or accept that the role is a mitigation stat block.

## Check yourself

1. A tank has 400 TPS and a 2,000 head start. A ranged DPS generates 600 TPS. When does the DPS pull aggro? What if they step into melee range at the start?
2. With the same tank, what is the most raw damage per second a melee DPS with a 0.8 threat modifier can deal forever without pulling?
3. A melee DPS pulls aggro at 12,000 threat while generating 900 TPS against a 700 TPS tank. The tank taunts. How long until the DPS pulls again if nothing changes?
4. A designer raises all tank threat modifiers from 1.3 to 5.0. Using the section 5 tank (400 damage, 180 bonus TPS), recompute the tank's TPS and a melee DPS's speed limit. Does threat still bind a DPS dealing 1,000 raw damage?

<details>
<summary>Answers</summary>

1. Ranged: `k τT = 1.3 × 400 = 520`, so `t = 1.3 × 2,000 / (600 − 520) = 2,600 / 80 = 32.5 s`. Melee: `k τT = 440`, so `t = 1.1 × 2,000 / (600 − 440) = 2,200 / 160 = 13.75 s`.
2. The threat limit is `1.1 × 400 = 440` TPS. With a 0.8 modifier, damage limit `= 440 / 0.8 = 550` damage per second.
3. `k τT = 1.1 × 700 = 770`. After the taunt both have 12,000, so `t = 0.1 × 12,000 / (900 − 770) = 1,200 / 130 = 9.2 s`.
4. `τT = 400 × 5 + 180 = 2,180` TPS. Melee limit `= 1.1 × 2,180 = 2,398` TPS. A 1,000 DPS player is far below it. Threat no longer binds, which matches what happened to WoW's threat game after the 2011 change.

</details>

## Lab hook

**Lab 06, threat budget simulator** ([`labs/lab06.md`](../labs/lab06.md)). You write a tick-based threat simulator for one boss and a 5-player group, confirm it matches the closed-form pull time, then add taunts, threat drops and a multi-enemy pull with split healing threat.

## Sources

- Warcraft Wiki, "Threat". Classic-era rules: 1 threat per damage, healing at 0.5 threat per point split across enemies, target switch at 110% in melee and 130% at range; tank threat raised to 500% from 300% in an August 2011 hotfix (Cataclysm era); patch 3.0.2 (October 2008) exposed threat to addons. https://warcraft.wiki.gg/wiki/Threat
- Warcraft Tavern, "WoW Classic Threat Guide & Reference Table". WoW Classic (1.12 rules): Defensive Stance ×1.3, Dire Bear Form ×1.3, Taunt sets threat equal to the highest on the table. https://www.warcrafttavern.com/wow-classic/guides/threat-guide-reference-table/
- Final Fantasy XIV Online Wiki (consolegameswiki), "Provoke". Current era: places the user at the top of the target's enmity list and adds enmity; used for tank swaps. https://ffxiv.consolegameswiki.com/wiki/Provoke
- Guild Wars 2 Wiki, "Aggro". Current era: proximity as the main factor, with toughness, damage and level; raid and strike bosses such as Vale Guardian and Gorseval target highest toughness. https://wiki.guildwars2.com/wiki/Aggro
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.

## Interactive spec: examples/w06-threat-race.html

**The one insight.** Whether a DPS ever pulls aggro depends only on the slopes (DPS threat rate vs `k` times tank threat rate). Head start and taunts only move the crossing point in time.

**Layout.**
- **Main chart, "Threat over time".** x-axis time 0 to 60 s. y-axis cumulative threat, auto-scaled. The tank line: `L + τT × t`, starting at `L` at t = 0. For each DPS, a shaded band from the tank line up to `k × tank line`, using that DPS's `k` (1.1 melee, 1.3 ranged); draw the band edge as a dashed line. Each DPS line: `τD × t` from the origin, in its own palette color. At the crossing, draw a marker and label "pulls at 11.0 s". If there is no crossing within 60 s but `τD > k τT`, label "pulls at X s (off chart)". If `τD ≤ k τT`, label "never pulls".
- **Side panel, "Speed limits".** For each DPS: its `k`, its threat limit `k × τT`, its damage limit `k × τT / c`, its current damage, and pull time. Numbers must be copyable.

**Controls.**
- Tank: TPS `τT` (100 to 3,000, step 10, default 500), head start `L` (0 to 6,000, step 100, default 1,500).
- Up to three DPS (default one visible, "Add DPS" button): raw damage (100 to 3,000, step 10, default 700), threat modifier `c` (0.5 to 1.5, step 0.05, default 1.0), melee/ranged toggle (default melee). `τD = damage × c`.
- "Taunt at pull" toggle. When on, at the first pull time `t1` the tank's threat jumps to the DPS's threat `X = τD × t1`, and the tank line continues from there with slope `τT`. Show the second pull time. Formula: `t2 = t1 + (k − 1) X / (τD − k τT)`.
- "Threat drop" button per DPS with a percent (default 50%) applied at a chosen time (default 8 s).
- Presets: "Default (melee 700)", "Same DPS at range", "At the speed limit (melee 550)", "Post-2011 tank (τT = 2,180)".

**Formulas.**
- Pull time: `t = k L / (τD − k τT)` if `τD > k τT`, else never.
- With a threat drop of fraction `f` at time `t0` (before pull): DPS threat becomes `(1 − f) τD t0` at `t0`, then grows at `τD`. Solve `(1 − f) τD t0 + τD (t − t0) = k (L + τT t)` for `t`.

**Test values (the build must reproduce these).**
- `τT = 500`, `L = 1,500`, melee `τD = 700`: pull at 11.0 s; tank threat 7,000, DPS 7,700.
- Same, ranged: 39.0 s.
- Melee `τD = 600`: 33.0 s. Ranged 600: never. Melee 550: never.
- Taunt at first pull, melee 700: second pull at `11 + 770 / 150 = 16.13 s`.
- Threat drop 50% at 8 s, melee 700: DPS threat 2,800 at 8 s; solve `2,800 + 700 (t − 8) = 1.1 (1,500 + 500 t)` gives `150 t = 4,450`, pull at 29.67 s.
- Check yourself Q1: `τT = 400`, `L = 2,000`, ranged 600: 32.5 s; melee 600: 13.75 s.

**First screen.** Default preset with one melee DPS at 700, the band visible, and the "pulls at 11.0 s" marker shown.
