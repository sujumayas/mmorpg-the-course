# CS203 · Week 12 — MMO Mob AI: Leashing, Aggro, Threat Tables

**Why this matters:** A stealth guard faces one player. An MMO monster may face forty, most of whom it cannot see well and all of whom it must treat by rules they can learn. The mob needs to decide when to start a fight, whom to hit and when to give up, and those three rules shape how groups play together. The threat table in particular is the reason a tank role can exist at all.

**You will be able to:**
- Compute a mob's aggro radius from level difference and predict which players it engages.
- Implement a per-mob threat table with damage, split healing threat, taunt and a thresholded target rule, and trace it tick by tick.
- Derive the healer safety margin and the minimum tank threat multiplier that keeps a boss off the healer, and explain why it depends on boss damage rather than tank damage.
- Critique leash and evade rules for the exploits they prevent and the player escapes they allow.

**Before class:** Warcraft Wiki, "Threat", "Aggro radius", "Leash" and "Evade" (read September 2026; listed in Sources). Guild Wars 2 Wiki, "Aggro". Consolegameswiki (Final Fantasy XIV), "Enmity". Kevin Dill, "What Is Game AI?", *Game AI Pro* (2013), chapter 1, the passage on scripted encounters in World of Warcraft (reread from week 1).

**Prerequisites from earlier courses:** [CS203 week 6, finite state machines](w06-finite-state-machines.md) (commitment by margin: why a monster switches only when the new target leads by 10% or 30%; this week uses the rule and does not re-derive it). [CS203 week 10, perception](w10-perception-systems.md) (a per-target memory that rises and falls). [MA101 week 14, distances and ranges](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w14-distances-ranges-and-squared-distance.md) (aggro and leash radii as two squared-distance tests). [MA101 week 2, linear functions and rates](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md) (two lines and where they cross).

**Interactive:** [`examples/w12-threat-table.html`](../examples/w12-threat-table.html). Keep it open during section 2.

---

## 1. The life of a mob

A **mob** (from "mobile object", the old MUD word) is any AI-controlled creature in an MMO. Most of its life is spent in three states, which you can build with week 6's machinery.

| State | What it does | Leaves when |
|---|---|---|
| IDLE (or PATROL) | Stands at its spawn point or walks a route | A player enters its aggro radius, or damages it, or a nearby ally pulls it in |
| COMBAT | Picks a target from its threat table and fights | Every enemy on the table is dead or gone, or it is pulled past its leash |
| EVADE | Runs home, ignores damage, regenerates, clears its table | It reaches home; then back to IDLE |

Each transition hides a design rule. This lecture takes them in order: starting a fight (aggro), choosing whom to hit (threat), and giving up (leash and evade).

### Aggro radius depends on level

**Aggro** is a mob's hostile attention. A mob "aggros" on a player when it starts attacking them. The **aggro radius** is how close a player can come before an idle hostile mob notices and attacks.

World of Warcraft never published its formula. Community testing summarized on Warcraft Wiki reports a pattern for ordinary mobs: about 20 yards when mob and player are the same level, changing by about 1 yard per level of difference, never less than about 5 yards (melee range), and capped at 45 yards when the mob is 25 or more levels above the player. The page's examples mention level 70 characters, so treat it as describing the game from the classic era through The Burning Crusade. As a model:

```python
def aggro_radius(mob_level, player_level):
    """Warcraft Wiki's community-tested rule of thumb, in yards."""
    return max(5, min(45, 20 + (mob_level - player_level)))

for mob in (10, 15, 25, 30, 35, 55, 70):
    print(f"level 30 player, level {mob:>2} mob: {aggro_radius(mob, 30):>2} yd")
```

Output:

```
level 30 player, level 10 mob:  5 yd
level 30 player, level 15 mob:  5 yd
level 30 player, level 25 mob: 15 yd
level 30 player, level 30 mob: 20 yd
level 30 player, level 35 mob: 25 yd
level 30 player, level 55 mob: 45 yd
level 30 player, level 70 mob: 45 yd
```

Read it as a perception rule with a designer's intent. A high-level character can walk through a low-level area without being bothered, because the radius shrinks to melee range. A low-level character who wanders into a dangerous zone is attacked from far away, which teaches them where they do not belong before they get deep into it. This is week 10's sensing filter with the fill time set to zero, where being in range means aggro. MMOs can afford the instant rule because the radius is readable (players learn "about 20 yards") and because an MMO fight starts slowly anyway.

### Aggro spreads

Mobs rarely stand alone. Warcraft Wiki describes three ways a fight grows.

- **Co-aggro (social aggro).** A mob in combat that comes within the aggro radius of an idle mob may pass its aggro on, especially if they share a faction or creature type. The newcomer joins with zero threat on everyone but still attacks. Running away, or fearing a mob into its friends, is the classic way to pull a second group by accident.
- **Group aggro.** Designers link specific mobs so that attacking one engages all, whatever the distances. It can be one-sided. Pulling an elite brings its friends, but a friend can be pulled alone with a ranged attack.
- **Shouts.** Some mobs have an ability that calls every monster in a large area. Players learn to interrupt or disable them first.

For you as the AI programmer, co-aggro is a proximity query between mobs, and group aggro is a list of links set by the level designer. For the designer, these are the rules that decide how big a **pull** (a deliberately started fight) is, and so how hard a dungeon corridor plays. They are tuning knobs as important as mob health.

## 2. Worked example: why the tank's multiplier keeps the boss off the healer

### The hook

In classic World of Warcraft, a warrior tanking a boss in Defensive Stance had a threat multiplier of 1.3, and a fully talented one about 1.5. Later expansions raised tank threat step by step. In the Cataclysm era, a hotfix on August 16, 2011 raised tank threat to 500%, up from 300%. The usual reading is that this freed damage dealers from watching threat meters.

But ask a different question. Who does a boss turn to when the tank's threat is too low? Often not a damage dealer. It is the healer, who never touches the boss. The healer's threat does not depend on the healer's choices at all. It depends on how hard the boss hits the tank. So the multiplier is really a rule about the ratio of *boss damage* to *tank damage*, and the numbers say a multiplier near 1 was always going to break as bosses hit harder.

### The model

Each mob keeps a **threat table**: one number per enemy it is in combat with. Warcraft Wiki's current rules, which match the long-standing classic-era rules:

- Damage adds 1 threat per point of damage, times the attacker's threat multiplier `m`.
- Healing adds 0.5 threat per point of effective healing (overhealing does not count), **divided by the number of mobs** that observed the heal.
- A taunt sets the taunter's threat equal to the highest on the table and forces the mob's attention.
- The mob switches to a new target only if that unit exceeds the current target's threat by 10% while in melee range, or by 30% while outside it. Week 6 explained why the margin exists. It is commitment, so the mob does not flip back and forth.

Now name the quantities for one boss fight.

- `B` is the boss's damage per second on the tank. The healer must heal `B` per second to keep the tank alive, so healing per second is `H = B`.
- `d` is the tank's own damage per second, and `m` its threat multiplier. The tank's threat per second is `m × d`.
- `N` is the number of mobs in combat. The healer's threat per second on each mob is `0.5 × B / N`.
- The healer stands at range, so it takes the boss only when its threat exceeds `1.3 ×` the tank's.

Both threats grow in straight lines. The healer never takes the boss if its line grows no faster than `1.3 ×` the tank's line. Define the **healer safety margin**:

```
S = 1.3 × m × d / (0.5 × B / N) = 2.6 × m × d × N / B

S > 1   the boss never turns to the healer
S < 1   it always does, eventually; a head start only delays it
```

Set `S = 1` to get the smallest multiplier that is safe:

```
m* = B / (2.6 × d × N)
```

Look at what is in that formula. The tank's multiplier must scale with **boss damage divided by tank damage**. Tanks trade damage for survival, so `d` stays modest, while `B` climbs with every tier of content. The healer's own skill and gear do not appear at all. A healer cannot hold back healing to stay safe, because healing less than `B` kills the tank.

Here is the table in code. Threat is kept in whole numbers and thresholds in tenths, so the comparisons are exact.

```python
MELEE_K, RANGED_K = 11, 13        # switch thresholds in tenths: 110% and 130%

class ThreatTable:
    """One mob's memory of who has hurt it, and its rule for whom to attack."""

    def __init__(self, thresholds=True):
        self.threat = {}          # unit -> threat, kept as whole numbers
        self.target = None
        self.thresholds = thresholds

    def add(self, who, amount):
        self.threat[who] = self.threat.get(who, 0) + round(amount)

    def choose(self, in_melee):
        """Keep the current target unless someone beats it by 10% (melee) or 30% (ranged)."""
        if self.target is None:
            self.target = max(self.threat, key=self.threat.get)
            return self.target
        current = self.threat[self.target]
        def beats(who):
            k = 10 if not self.thresholds else MELEE_K if who in in_melee else RANGED_K
            return self.threat[who] * 10 > current * k
        challengers = [w for w in self.threat if w != self.target and beats(w)]
        if challengers:
            self.target = max(challengers, key=self.threat.get)
        return self.target

def healer_pull(multiplier, boss_dps=600, tank_dps=200, mobs=1, seconds=600):
    """Second at which the boss first turns to the healer, or None."""
    table = ThreatTable()
    for t in range(1, seconds + 1):
        table.add("tank", multiplier * tank_dps)
        if t >= 2:                                   # healer starts one second late
            table.add("healer", 0.5 * boss_dps / mobs)
        if table.choose(in_melee={"tank"}) == "healer":
            return t
    return None

for m in (1.0, 1.1, 1.15, 1.2, 1.3, 5.0):
    margin = 1.3 * m * 200 / (0.5 * 600)
    print(f"multiplier {m:>4}: margin {margin:.3f}, healer pulls at {healer_pull(m)}")
print("two mobs, multiplier 1.0:", healer_pull(1.0, mobs=2))
```

Output:

```
multiplier  1.0: margin 0.867, healer pulls at 8
multiplier  1.1: margin 0.953, healer pulls at 22
multiplier 1.15: margin 0.997, healer pulls at 301
multiplier  1.2: margin 1.040, healer pulls at None
multiplier  1.3: margin 1.127, healer pulls at None
multiplier  5.0: margin 4.333, healer pulls at None
two mobs, multiplier 1.0: None
```

### Numbers you can check

Start with the pull times. The tank adds `m × 200` from second 1. The healer adds `0.5 × 600 = 300` from second 2, so after `t` seconds the healer has `300 (t − 1)` and the tank `200 m t`. The healer pulls when `300 (t − 1) > 1.3 × 200 m t`.

- `m = 1.0`: `300t − 300 > 260t`, so `t > 7.5`. First whole second: 8. At `t = 8` the healer has 2,100 and the tank 1,600, and `1.3 × 1,600 = 2,080 < 2,100`.
- `m = 1.1`: tank rate 220, `1.3 × 220 = 286`. `14t > 300` gives `t > 21.4`, so 22.
- `m = 1.15`: tank rate 230, `1.3 × 230 = 299`. `t > 300`, so 301. Five minutes in, which on a real raid night is the middle of the fight, or the start of the next pull if the boss died first. A margin just under 1 hides the problem until it is expensive.
- `m = 1.2`: `1.3 × 240 = 312 > 300`. Never.

The break-even multiplier is `m* = 600 / (2.6 × 200 × 1) = 1.154`. With two mobs in combat, the healer's threat on each halves to 150 per second, the margin doubles to 1.733, and even `m = 1.0` is safe. Healing threat is split, tank threat is not.

Now hold the tank fixed at `d = 200` and let the content get harder. Margin `S = 2.6 × m × 200 / B`:

| Boss DPS on tank `B` | `S` at `m = 1.0` | `S` at `m = 1.3` (classic stance) | `S` at `m = 5.0` (from August 2011) | Minimum safe `m*` |
|---|---|---|---|---|
| 400 | 1.300 | 1.690 | 6.500 | 0.769 |
| 600 | 0.867 | 1.127 | 4.333 | 1.154 |
| 800 | 0.650 | 0.845 | 3.250 | 1.538 |
| 1,200 | 0.433 | 0.563 | 2.167 | 2.308 |

Check the 800 row. `S = 2.6 × 1.3 × 200 / 800 = 676 / 800 = 0.845`. The classic multiplier holds the boss off the healer against a boss hitting for 600, and fails against one hitting for 800. Nothing about the healer changed. A tank's own damage has to keep pace with the boss's damage, or the multiplier has to grow. The five-fold multiplier keeps the margin above 2 even at triple the boss damage. These numbers are invented to show the shape; real tank and boss damage varied by tier and by fight, and the community reverse-engineered the threat rules because Blizzard did not publish them.

### Move it yourself

Open [the interactive](../examples/w12-threat-table.html). The left view is the boss's threat table drawn as horizontal bars for the tank, the healer and a rogue, with the current target marked and two tick marks on the target's bar at 110% and 130%, showing what melee and ranged players must beat. Press Play and the bars grow second by second. The right view plots the time until the healer pulls against the tank multiplier from 0.5 to 6. It is a curve that shoots up to "never" at a vertical line labelled `m*`.

Start at `m = 1.0` and watch the healer's bar cross the 130% tick at 8 seconds. Drag the multiplier to 1.15 and the crossing moves off the chart to 301 seconds. Drag past 1.154 and the right-hand curve goes vertical. Now raise boss DPS from 600 to 800. The vertical line slides right to 1.538, past the classic 1.3 marker, and the healer is in trouble again with no change to the tank or the healer. Set mobs to 2 and watch the line jump left. Split healing threat is why healers are safest on big pulls of trash and most exposed on single bosses.

### Cross-game recognition

**World of Warcraft, classic era to Cataclysm.** The same equation with a moving `m`. Classic Defensive Stance at 1.3 (1.495 with the Defiance talent) and Dire Bear Form at 1.3, later 300% for tanks, then 500% from the August 16, 2011 hotfix, which covered warriors in Defensive Stance, death knights in Blood Presence, druids in Bear Form and paladins with Righteous Fury. Warcraft Wiki's history section says tanks got increasing passive boosts until threat became relatively unimportant. A tank either has aggro or does not, and keeps it easily once it does. In our table, `S` went from about 1 to about 4.

**Final Fantasy XIV (current).** Enmity is FFXIV's name for threat. Attacks and healing both generate it, which puts healers on the same table. All tank jobs have a stance that, in the wiki's words, drastically increases the enmity they generate, and it is meant to be on at all times. Provoke puts the tank at the top of the target's enmity list and adds more enmity on top, which is a taunt that leaves a lead rather than a tie. The game also shows the table. Party list numbers give each player's enmity order and an "A" marks who has aggro. Rewritten in our form, `m` is large and the healer's `S` is comfortably above 1 by design. The same wiki notes that DPS and healer jobs once had enmity-reducing actions that were later removed, which is what you would expect once `S` no longer needs help.

**Guild Wars 2 (current).** Generic enemies choose targets mainly by range, so the closest character or pet holds their attention. The wiki still describes a threat table, but as a priority queue fed by conditions such as proximity, damage over time, and for many raid and strike bosses, the highest toughness. In our form, a proximity rule replaces accumulated threat with a value recomputed every tick, so there is no slope to race. The healer is safe if they stand farther away than the tank, and a toughness boss asks "whose stat is highest?" instead. The designer moved the question from "how fast do you generate threat" to "where do you stand" or "what did you equip".

Three games ask one question. How much of a lead does the character meant to be hit have over the character not meant to be hit, and does that lead grow or shrink with time? A slope ratio answers it for accumulated threat. A distance or stat comparison answers it for the others.

### Eyes-open design judgment

- **Compute `m*` for every tier, not once.** `m* = B / (2.6 d N)` rises with boss damage. If you tune the multiplier on the first dungeon, your last raid breaks it. Either scale tank damage with boss damage, or set the multiplier high enough that `S` stays above about 2 through the whole game.
- **A tight margin makes threat a skill; a loose one removes it.** With `S` near 1, tanks must play well and healers feel the pressure; groups coordinate around a threat meter. With `S` near 4, threat stops mattering and the tank loses a job. In year 3, [MMO303 week 6](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w06-threat-aggro-and-control.md) works out what that does to damage dealers and group damage budgets. This lecture's point is narrower. The healer is the first casualty of a low margin, and the one player who cannot fix it.
- **Split healing threat is a design choice.** Dividing by `N` makes healers safe on large pulls, where the tank's threat is spread thin across many mobs. That can surprise players. The same healer is safer against ten weak mobs than against one strong boss.
- **Show the table, or make it irrelevant.** Warcraft Wiki records that threat was a hidden value in early WoW, reverse-engineered by addon authors, until patch 3.0.2 exposed it to addons. A tight threat system that players cannot see is week 1's unfair hidden rule. FFXIV shows enmity order in the party list. Guild Wars 2 mostly uses a rule players can see, distance.

## 3. Building the table

The class in section 2 is the core. A shipping version needs the rest of the rules, and each one is a small, testable method.

- **Entries start when combat starts.** Every unit joins the table at zero when it enters combat with the mob, and leaves when combat ends or it dies. Leaving and re-entering starts again at zero.
- **Splitting.** A heal or a buff is observed by every mob in combat with the healer's group. Add `0.5 × amount / N` to each of those `N` tables. Keep a per-group list of mobs in combat, so this is one loop, not a search.
- **Taunt.** Set the taunter's threat equal to the current maximum and force the target for a few seconds. In the code, a forced target ignores `choose()` until a timer runs out. Warcraft Wiki's ability table lists several variants: set to highest (Taunt, Growl), set to zero for a duration (Fade), and remove from all tables (Vanish, Feign Death).
- **Death and removal.** When the current target dies or leaves the table, pick the highest remaining unit with no threshold. There is nobody to commit to.
- **The switch rule.** Week 6 showed why the 10% and 30% margins exist. A table with no margin switches every time the lead changes sign. Two units with the same average threat rate and opposite rhythms (a tank and a rogue each averaging 300 per second, alternating big and small hits) make a mob with no margin switch every second of a 60-second fight. With the 110% rule it switches three times in the first three seconds and then stays put, because once totals pass about 1,000, a swing of 150 to 250 is under 10%. Lab 12 has you reproduce both counts.

A mob's threat table is also its memory, in week 10's sense. It is the per-target number that says how much the mob cares about each enemy. The stealth guard's meter rises with exposure and drains with time. The threat table rises with damage and healing and never drains during combat. Both are one number per target, updated by events, compared against thresholds.

## 4. Leashing and evading

A **leash** is the maximum distance a mob will chase before it gives up. When it leashes, the mob clears its threat table and enters EVADE. It runs back to its spawn point or patrol, ignores all attacks, regenerates health as if out of combat, and resets. MA101 week 14 built the two-radius version, which starts chasing at the aggro radius and gives up at the larger leash radius. The gap between the two is what stops a mob at the edge from flickering in and out of combat.

Warcraft Wiki describes several variations, and each one exists to block an exploit or allow an escape.

| Rule | What it prevents or allows |
|---|---|
| Open-world mobs leash back to spawn | Players can escape a losing fight by running. It also blocks **training**, luring mobs onto other players, because an evading mob ignores everyone it runs past |
| Classic era: hitting a mob resets its leash range | Players can deliberately drag a mob far away by attacking it now and then while walking. A known kiting technique; the modern rule removed it |
| Hardcore Classic: mobs do not follow between zones | Stops players on permadeath servers from escaping or griefing by crossing a zone line |
| Dungeon trash generally does not leash | Players cannot run away from a pull inside an instance; they must win, reset with an ability, or leave |
| A mob that cannot reach its target evades, and some **snap** (teleport) to the player | Stops players from standing on a ledge the mob cannot path to and killing it for free |
| Raid bosses leash to an area, and some despawn if pulled out of it | Keeps an encounter in the room it was designed for |

Look at the evade rule from the player's side. When a mob cannot reach you, it becomes immune and heals, which tells you the game has noticed the exploit. It is the AI version of week 1's cheat test. The mob's immunity is visible and consistent, so players accept it. A mob that simply stood still and died would reward the exploit. A mob that teleported without warning every time would feel like cheating. Snapping is used where the designers decided the exploit is worse than the surprise.

Guild Wars 2 states a similar reset. Enemies with no one left on their aggro list leave combat and either regenerate to full health or despawn until the encounter resets.

### Designing a leash

Three numbers decide how a leash feels.

1. **Leash distance.** Short leashes make running away easy and pulls small. Long leashes make fleeing dangerous and co-aggro likely, because the fleeing player drags the mob past other groups.
2. **What resets it.** Resetting on damage (classic) lets players kite on purpose. Resetting on a timer since the mob last saw its target lets stealth abilities work as escapes. Fixed distance from spawn is the most predictable.
3. **What evade restores.** Full health and a cleared table is the standard. Restoring health slowly instead would let players wear a mob down by pulling it back and forth, which is usually not what you want.

Scale is its own problem. A zone with thousands of mobs cannot run every mob's perception and threat logic every tick. [MMO404 week 12, AI at scale](../../MMO404-advanced-networked-simulation/lectures/w12-ai-at-scale.md) computes that cost from player positions, and [CS203 week 14](w14-performance-ai-lod-and-time-slicing.md) covers AI level of detail and time-slicing. Idle mobs are the cheap state. Most of the cost is in COMBAT and in the aggro checks near players.

## In-class activity (25 minutes)

Groups of four, each member playing one role: tank, healer, damage dealer, boss. The boss holds a printed threat table and a pencil.

1. **Play it (10 min).** Use the section 2 numbers: tank `d = 200`, boss `B = 600`, one boss. The tank announces `200 × m` each second with `m = 1.1`, the healer announces 300 from second 2, and the boss updates the table and says whom it attacks. Run until the boss turns or 25 seconds pass. Compare the turn second with the formula.
2. **Retune (7 min).** The next boss hits for 900. Compute `m*`. The designer refuses to raise the multiplier above 1.3. Find two other changes that bring `S` back above 1.2, with the numbers (for example, the tank's damage, or adds that split healing threat).
3. **Leash (5 min).** Your mob can be pulled across a zone line in a normal zone. Pick one rule from section 4's table to adopt, and write the exploit it prevents and the escape it removes.
4. **Share (3 min).** One group reads its retune; the class checks `S`.

Expected output: the filled table with the turn second, two retunes with margins, and one leash rule with its two consequences.

## Common misconceptions

- **"The healer pulls aggro because they healed too much."** The healer heals what the boss deals. Their threat per second is set by boss damage, so the fix is on the tank's side (`m` or `d`) or in the encounter (`B` or `N`).
- **"If the boss hasn't turned after a minute, it never will."** With a margin just under 1, the pull can come minutes later. At `m = 1.15` in section 2 it comes at 301 seconds. Compute `S`; do not wait for it.
- **"Aggro radius is a fixed distance."** In World of Warcraft it depends on level difference, from about 5 yards for much weaker mobs to 45 for much stronger ones. That is how the game tells players where they belong.
- **"Evade is a bug players run into."** It is a deliberate anti-exploit rule that also stops griefing by training. Its visibility (the mob turns immune and heals) is what makes it accepted.

## Check yourself

1. A level 42 player approaches a level 38 mob and a level 50 mob. Using the rule of thumb, what are the two aggro radii?
2. A tank deals 250 damage per second with a multiplier of 1.5. The boss hits the tank for 1,100 per second, and there is one boss. What is the healer margin `S`? Does the boss ever turn to the healer? What multiplier would make `S = 1.5`?
3. Same tank and boss, but the boss fight adds three adds that stay in combat all fight (so `N = 4`). Recompute `S`. What is the catch?
4. In section 2's setup with `m = 1.0`, the tank taunts at the moment the boss turns to the healer (second 8), setting its threat equal to the healer's. The tank is in melee. Using the rates, does the tank keep the boss after the taunt ends, or does the healer take it again? Explain with slopes.
5. A designer wants players to be able to escape any open-world fight by running, but also wants to stop kiting mobs across the map. Propose a leash rule and give one case it handles badly.

<details>
<summary>Answers</summary>

1. Level 38: `20 + (38 − 42) = 16` yards. Level 50: `20 + 8 = 28` yards.
2. `S = 2.6 × 1.5 × 250 / 1,100 = 975 / 1,100 = 0.886`. Below 1, so yes, eventually. For `S = 1.5`: `m = 1.5 × 1,100 / (2.6 × 250) = 1,650 / 650 = 2.54`.
3. `S = 0.886 × 4 = 3.55`. Safe from the boss. The catch: the tank's threat is on the boss, but the healer's threat also lands on each add. If the tank is not also generating threat on the adds, the adds turn to the healer at once, because the healer has threat on them and nobody else does. Splitting helps with the boss only if the tank holds the adds too.
4. After the taunt, both start from the same threat, 2,100. The healer then gains 300 per second and the tank 200. The healer needs 130% of the tank's threat: `2,100 + 300s > 1.3 × (2,100 + 200s)` gives `40s > 630`, `s > 15.75`. So the boss turns back to the healer about 16 seconds after the taunt. A taunt resets who is on top. It does not change the slopes, and `S < 1` means the healer wins every race eventually.
5. For example: leash at a fixed distance from spawn, measured from spawn and never reset by damage. Running always escapes, and kiting is capped at the leash distance. It handles badly a mob whose spawn is near a narrow path, where a player running past is chased back and forth by several mobs in turn, or a quest that needs the player to lead a mob somewhere. Any rule with a clearly named bad case is correct.

</details>

## Lab / assignment hook

[Lab 12, the mob brain](../labs/lab12.md). Implement aggro radius, a threat table with split healing, taunt and removal, the thresholded target rule, and a leash with evade, until the provided checker passes. Then run the provided three-tier raid and find the smallest tank multiplier that keeps each boss off the healer, and compare it with the formula. Deliverable: the passing code, a tier table and a 300-word note.

## Sources

- Warcraft Wiki, "Threat" (read September 2026; the page is marked partly outdated). One threat per damage; healing at 0.5 threat per point of effective healing, divided by the number of observing NPCs, overheal excluded; switch at 110% in melee and 130% outside melee; current tank multipliers of 5.0; taunt, Fade, Vanish and Feign Death effects; threat hidden and reverse-engineered by addons until patch 3.0.2; hotfix of August 16, 2011 raising tank threat to 500% from 300%. https://warcraft.wiki.gg/wiki/Threat
- Warcraft Tavern, "WoW Classic Threat Guide & Reference Table" (read September 2026). WoW Classic: Defensive Stance ×1.3, with Defiance ×1.495; Dire Bear Form ×1.3; healing threat 0.5 per point divided equally among mobs in combat; notes that Blizzard never listed the numbers. https://www.warcrafttavern.com/wow-classic/guides/threat-guide-reference-table/
- Warcraft Wiki, "Aggro radius" (read September 2026). Community testing: about 20 yards at equal level, about 1 yard per level of difference, minimum about 5 yards, cap of 45 yards at 25 or more levels above; co-aggro, group aggro and shouts. https://warcraft.wiki.gg/wiki/Aggro_radius
- Warcraft Wiki, "Leash" and "Evade" (read September 2026). Leash clears the aggro list and sends the mob home in evade mode; leashing prevents training; instance trash generally does not leash; snapping; raid boss area leashes; in Classic, hitting a mob resets its leash range; in Hardcore, mobs do not follow between zones; evade makes the mob immune and regenerate. https://warcraft.wiki.gg/wiki/Leash and https://warcraft.wiki.gg/wiki/Evade
- Guild Wars 2 Wiki, "Aggro" (read September 2026, current game). Generic enemies target mainly by range; threat table as a priority queue including proximity, damage and toughness; raid and strike bosses with toughness or fixate mechanics; enemies with no aggro regenerate or despawn. https://wiki.guildwars2.com/wiki/Aggro
- Final Fantasy XIV Online Wiki (consolegameswiki), "Enmity" and "Provoke" (read September 2026, current patches). Enmity from attacks and healing; tank stances that drastically increase enmity; the party list enmity order and "A" marker; historical enmity-reducing actions; Provoke places the user at the top of the list with additional enmity. https://ffxiv.consolegameswiki.com/wiki/Enmity
- Dill, K. (2013). "What Is Game AI?" In S. Rabin (ed.), *Game AI Pro*, chapter 1. World of Warcraft's heavily scripted, predictable encounters, as cited in CS203 week 1.
- Tank damage, boss damage, the level examples and the activity numbers are invented for teaching.

## Interactive spec: examples/w12-threat-table.html

**The one insight:** the healer's threat is set by how hard the boss hits, so whether the boss ever turns to the healer depends on one ratio, `S = 2.6 × m × d × N / B`. Below 1 the healer always pulls eventually (and the pull can come minutes later); above 1 never. Dragging the multiplier shows a cliff at `m* = B / (2.6 d N)`, and raising boss damage slides that cliff past the classic 1.3 multiplier.

**Layout.** Two linked views, side by side at 1280 px, stacked at 390 px (table on top).

- **Left, "The boss's threat table":** three horizontal bars, labelled "Tank (melee)", "Healer (ranged)" and "Rogue (melee)", with exact threat values printed at the end of each bar. A marker (text "TARGET" plus an outline) on the current target's bar. On the target's bar, two tick marks at 110% ("melee must beat") and 130% ("ranged must beat") of its value. Below the bars, a 60-second timeline strip coloured by who the boss targets, with the switch times printed.
- **Right, "When does the healer pull?":** x-axis tank multiplier `m` from 0.5 to 6 (linear), y-axis first pull second from 0 to 120 s. Above the plot sit two labelled bands: ">120 s" for runs that pull after 120 s but by 600 s (the dot is drawn there and labelled with its time, for example "301 s, off chart"), and "never" for runs with no pull by 600 s. A vertical dashed line at `m*` labelled with its value, plus fixed reference markers at 1.3 ("classic stance") and 5.0 ("from Aug 2011"). A dot marks the current `m`. Readouts: `S`, `m*`, first pull second.

**Controls (keyboard accessible, labelled):**

1. Tank multiplier `m` slider, 0.5 to 6, step 0.05, default 1.0.
2. Boss DPS on tank `B`, 200 to 1,500, step 50, default 600.
3. Tank DPS `d`, 50 to 500, step 10, default 200.
4. Mobs in combat `N`, 1 to 5, default 1.
5. Rogue toggle (default off). When on, the rogue deals a constant 250 threat per second from second 1 (melee, multiplier 1).
6. Play/Pause, Step (1 s), Reset. A "Taunt" button: sets tank threat equal to the current maximum and forces the target to the tank for 3 seconds.
7. "Thresholds" toggle (default on). Off makes every challenger need only to exceed 100%.

**Formulas.** Integer seconds `t = 1, 2, ...`. Each second: tank `+ round(m × d)`; healer `+ round(0.5 × B / N)` from `t = 2`; rogue `+250` from `t = 1` if on. Then the switch rule: a challenger replaces the current target if `10 × threat > k × current`, with `k = 11` for melee units, `13` for the healer, `10` if thresholds are off; among several challengers the highest threat wins. Initial target at `t = 1` is the highest threat. Right chart: first `t ≤ 600` at which the healer becomes the target in a run with the rogue off, else "never". `S = 2.6 m d N / B`, `m* = B / (2.6 d N)`.

**Test values (must match `healer_pull` in the lecture).**

- Defaults (`B = 600`, `d = 200`, `N = 1`): `m = 1.0` pulls at 8 (healer 2,100, tank 1,600 at `t = 8`); `m = 1.1` at 22; `m = 1.15` at 301 (drawn in the ">120 s" band as "301 s, off chart"); `m = 1.2`, 1.3 and 5.0 never. `m* = 1.154`. `S` at 1.0, 1.3, 5.0: 0.867, 1.127, 4.333.
- `B = 800`: `m* = 1.538`; at `m = 1.3`, `S = 0.845`.
- `N = 2`, `m = 1.0`: never; `S = 1.733`.
- Check yourself 2: `d = 250`, `m = 1.5`, `B = 1,100`: `S = 0.886`.
- Taunt at `t = 8` with `m = 1.0` (thresholds on): tank set to 2,100; after the 3-second force ends the healer retakes the boss at the first second where `2,100 + 300s > 1.3 × (2,100 + 200s)`, that is `s = 16`, so at `t = 24`.

**First screen.** Defaults with `m = 1.0`, the run already at `t = 8` showing the healer's bar just past the 130% tick and the TARGET marker on the healer; right chart with the dot at `m = 1.0` (8 s) and the `m*` line at 1.154. Caption: "The healer never hit the boss. The boss's damage did this."

**Accessibility.** All controls reachable by Tab with visible focus. A live region announces target changes ("boss turns to Healer at 8 s"). Respects `prefers-reduced-motion` (Play advances 1 s per step with no bar tweening) and `prefers-color-scheme`. Palette from `templates/interactive-tokens.css`. No game art or class icons: labelled bars only.
