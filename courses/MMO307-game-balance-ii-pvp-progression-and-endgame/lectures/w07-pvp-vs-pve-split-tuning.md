# MMO307 · Week 07 — PvP Balance vs PvE Balance: Split Tuning

**Why this matters:** An MMO ships two games in one client. Raids reward damage over five minutes against a script, and arenas reward damage in the first ten seconds against a person who fights back. One set of numbers can rarely satisfy both, and the moment you split them you have doubled what players must learn and what you must maintain.

**You will be able to:**
- Compute a class's PvE throughput and PvP time to kill from the same two numbers, and show when one change moves both.
- Derive the "clone" constraint, the single class shape that meets a PvE target and a PvP target at once without a split.
- Design a split at the right grain (global, time-based, per class, per ability) and compute the multiplier it needs.
- Critique a real game's split policy by counting what it costs players and developers.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapters on PvP and on PvE progression. Skim the Guild Wars 2 Wiki notes for the May 8, 2018 and July 10, 2018 balance updates and count how often the phrase "split between game modes" appears.

**Prerequisites from earlier courses:** [GD203 week 4, time to kill and time to die](../../GD203-combat-and-progression-design/lectures/w04-time-to-kill-and-time-to-die.md) (TTK measured in decisions). [GD203 week 5, DPS, burst and sustain](../../GD203-combat-and-progression-design/lectures/w05-dps-burst-and-sustain.md) (why burst beats its DPS in short fights). [MMO303 week 3, effective HP and effective DPS](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w03-effective-hp-and-effective-dps.md) (the TTK matrix for duels). [MMO303 week 11, Lanchester's laws](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w11-lanchesters-laws-and-group-combat.md) (the healing threshold that stalls group fights). [MMO303 week 2, armor](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md) (the divisive formula that resilience later copied).

**Interactive:** [`examples/w07-split-tuning.html`](../examples/w07-split-tuning.html). Keep it open from section 2 on.

---

## 1. Two games, one set of numbers

Start with what each mode measures, because balance only means something against a metric.

In **PvE** (player versus environment), the enemy is a script. A raid boss has a health pool and an enrage timer, and the question a raid leader asks of a class is "how much damage does it add over the whole fight?" Fights last minutes. Cooldowns come back several times. What matters is **throughput**, damage per second averaged over the fight. MMO303 called this effective DPS.

In **PvP** (player versus player), the enemy is a person who reacts. The question a PvP player asks is "can I kill my target before they can respond, and can they kill me first?" Fights are decided in seconds. What matters is **time to kill (TTK)**, and TTK in the first seconds is dominated by **burst**, damage delivered in a short window by stacking cooldowns. GD203 week 4 argued that a TTK shorter than a player's reaction window removes the defender's decisions entirely.

These two metrics weigh the same class differently. A class with modest steady damage and one huge cooldown looks average on a five-minute meter and lethal in a ten-second duel. When one number, say the damage of that cooldown, feeds both metrics, the two modes are **coupled**. Any change you make for one mode also lands in the other.

**Split tuning** means giving a value a separate number in each mode. The ability does 24,000 damage to monsters and 19,200 to players. The rune gives 50 endurance in dungeons and 25 in arenas. A useful way to write every split in this lecture is

```
value in mode m = base value × multiplier for mode m
```

where the multiplier might apply to one field of one ability, to one class, or to everyone. Most real splits fit this form, and seeing that is half of this week.

## 2. Worked example: the class that tops no meter and wins every duel

### The hook

In July 2018, a Guild Wars 2 balance update cut the Rune of the Adventurer's endurance bonus to 25 in PvP while keeping 50 in the other game modes. Six weeks later another update raised one skill's cooldown from 60 to 75 seconds "in PvP only". Yet two months before either change, on May 8, 2018, the same developer had shipped an update whose notes contain 86 lines saying a skill was no longer split between game modes. The team was adding splits and removing them in the same summer.

Why would a studio do both? Because a split solves a real problem and creates a new one. This worked example shows the problem with numbers you can check, and section 4 shows the cost.

### The model

Take one damage dealer described by two numbers.

- `s` is sustained DPS, the damage per second of the steady rotation.
- `B` is burst, the damage of one big cooldown that comes back every `C` seconds.

For PvE, measure throughput over a long fight. If the fight lasts a whole number of cooldowns and the burst is used on cooldown,

```
PvE DPS = s + B / C
```

For PvP, measure the time to kill a standard target with `H` effective health, opening with the burst and finishing with the rotation:

```
TTK = (H − B) / s          (0 if B ≥ H)
```

Use `C = 60` seconds and `H = 30,000`. This ignores healing, control and the target hitting back. MMO303 week 3 built the full duel matrix; here one target is enough, because the point is the gap between the two metrics.

### Numbers you can check

Three invented classes, each tuned by a careful PvE designer to exactly 1,100 DPS on a long fight.

| Class | `s` | `B` | PvE DPS `s + B/60` | PvP TTK `(30,000 − B)/s` |
|---|---|---|---|---|
| Duelist | 900 | 12,000 | 1,100 | 20.0 s |
| Ravager | 700 | 24,000 | 1,100 | 8.6 s |
| Channeler | 1,050 | 3,000 | 1,100 | 25.7 s |

The PvE meter shows a perfect tie. The duel shows the Ravager killing a target almost three times faster than the Channeler. In a game where you want at least a few seconds to react, 8.6 seconds of which the first instant removes 80% of your health is a loss you watch rather than play.

### One knob moves both games

Try the obvious fix. Cut the Ravager's burst by a quarter, from 24,000 to 18,000.

| Ravager | `s` | `B` | PvE DPS | PvP TTK |
|---|---|---|---|---|
| Before | 700 | 24,000 | 1,100 | 8.6 s |
| Burst −25% | 700 | 18,000 | 1,000 | 17.1 s |
| Burst −25%, sustain raised to 800 | 800 | 18,000 | 1,100 | 15.0 s |

The first fix repairs PvP and costs the Ravager 9% of its raid damage, which in a raid where groups compete for spots is the difference between being invited and being benched. So the designer compensates by raising sustained DPS to 800. PvE is back at 1,100 and PvP TTK is 15 seconds. It worked. But look at what the Ravager now is. It is a class with 800 sustain and 18,000 burst, much closer to the Duelist than to the class its players chose.

### The clone constraint

That drift is not bad luck. With two targets and two numbers per class, the targets pick the numbers. Set PvE DPS to a target `D` and PvP TTK to a target `T`:

```
s + B / C = D
(H − B) / s = T
```

Solve the second for `B = H − T·s`, substitute into the first, and

```
s = (C·D − H) / (C − T)
B = H − T·s
```

With `D = 1,100`, the only class that hits `T = 20` seconds exactly is `s = 900, B = 12,000`, the Duelist. Every class you tune to both targets becomes the same class. Call this the **clone constraint**. You can loosen it by asking for a band instead of a point, but not by much:

| Target TTK | `s` | `B` |
|---|---|---|
| 15 s | 800.0 | 18,000 |
| 20 s | 900.0 | 12,000 |
| 22 s | 947.4 | 9,158 |

If PvP should sit in a 15 to 22 second band, every class must carry between about 9,200 and 18,000 burst. The Ravager's 24,000 and the Channeler's 3,000 are both outside. Those two class identities, "the one big hit" and "the steady pressure", cannot exist in a coupled game that meets both targets. That is the real reason MMOs split. It is not that PvP and PvE players disagree about numbers. It is that two metrics over one set of numbers leave no room for difference.

Run it yourself:

```python
H = 30_000   # EHP of the standard PvP target
C = 60       # burst cooldown in seconds
classes = {"Duelist": (900, 12_000), "Ravager": (700, 24_000), "Channeler": (1_050, 3_000)}

def pve_dps(s, B):
    return s + B / C

def pvp_ttk(s, B, p=1.0, q=1.0, h=1.0):
    """Open with the burst, finish with sustained damage. p scales burst in PvP,
    q scales sustained damage in PvP, h scales every player's PvP health."""
    return max(0.0, h * H - p * B) / (q * s)

def clone(D, T):
    """The only (s, B) that hits PvE DPS D and PvP TTK T at once."""
    s = (C * D - H) / (C - T)
    return s, H - T * s

for name, (s, B) in classes.items():
    print(f"{name:9}  PvE {pve_dps(s, B):6.0f}  TTK {pvp_ttk(s, B):5.1f} s  "
          f"h=2: {pvp_ttk(s, B, h=2):5.1f} s  h=4.35: {pvp_ttk(s, B, h=4.35):5.1f} s")
for T in (15, 20, 22):
    s, B = clone(1_100, T)
    print(f"clone for TTK {T}: s = {s:.1f}, B = {B:,.0f}")
print(f"Ravager p=0.80: {pvp_ttk(700, 24_000, p=0.8):.1f} s, "
      f"Channeler q=1.20: {pvp_ttk(1_050, 3_000, q=1.2):.1f} s")
```

It prints:

```
Duelist    PvE   1100  TTK  20.0 s  h=2:  53.3 s  h=4.35: 131.7 s
Ravager    PvE   1100  TTK   8.6 s  h=2:  51.4 s  h=4.35: 152.1 s
Channeler  PvE   1100  TTK  25.7 s  h=2:  54.3 s  h=4.35: 121.4 s
clone for TTK 15: s = 800.0, B = 18,000
clone for TTK 20: s = 900.0, B = 12,000
clone for TTK 22: s = 947.4, B = 9,158
Ravager p=0.80: 15.4 s, Channeler q=1.20: 21.4 s
```

The `h` columns belong to section 3. Ignore them for now.

### The split fix

Now add PvP-only multipliers. Let `p` scale burst against players and `q` scale sustained damage against players. PvE DPS does not contain `p` or `q`, so it stays at 1,100 for everyone. Solving for the multiplier that lands a class on a target is one line each:

```
p = (H − T·s) / B          (burst multiplier for target TTK T)
q = (H − B) / (T·s)        (sustain multiplier for target TTK T)
```

For the Ravager at `T = 15`, `p = (30,000 − 10,500) / 24,000 = 0.81`. Round to 0.80 and TTK becomes 15.4 seconds. For the Channeler at `T = 22`, `q = 27,000 / 23,100 = 1.17`. Round to 1.20 and TTK becomes 21.4 seconds. All three classes now sit inside the band, all three still deal 1,100 on the raid meter, and the Ravager is still the class whose opener takes most of your health bar. It just takes 64% instead of 80%.

Notice what was split. Not the whole class, and not the whole ability. One field, the burst's damage against players, for one class. This is the finest grain available, and section 3 walks up to the coarser ones.

### The visual

Open [`examples/w07-split-tuning.html`](../examples/w07-split-tuning.html). The left panel is the raid meter, three bars with a ±3% target band around 1,100. The right panel is the duel, three TTK bars with a 15 to 22 second band. Below them, a third view plots every class as a dot in the `(s, B)` plane, with the PvE line `s + B/60 = 1,100` and the PvP band drawn as a strip. The two lines cross in a short segment. That segment is the clone constraint, visible.

Drag the Ravager's burst slider with "Split" off. Both panels move, and the dot slides along a line that can reach the PvP band only by leaving the PvE line. Now switch "Split" on. The PvP multipliers appear, and dragging them moves only the right panel. The dot's PvE position stays put while a ghost dot shows where it sits for PvP. One class, two positions, one per mode.

### Cross-game recognition

Every example below is `value in mode m = base × multiplier for m`, at a different grain.

**Guild Wars (2008 onward).** The May 22, 2008 update introduced separate PvP versions of skills. In PvP areas the altered skill carries "(PvP)" in its name and behaves differently. The Guild Wars Wiki category for these versions held 188 entries in September 2026. Grain: the whole ability, every field. The multiplier is a second copy of the skill.

**Guild Wars 2 (2018 balance updates).** Splits are per field, across three modes, PvE, structured PvP and World versus World. Rune of the Adventurer went to 25 endurance in PvP and kept 50 in other modes (July 10, 2018). Prime Light Beam's cooldown went from 60 to 75 seconds in PvP only (August 28, 2018). Grain: one field of one ability, exactly like our `p`.

**World of Warcraft, resilience (The Burning Crusade through Battle for Azeroth).** Resilience was a stat that reduced damage taken from players and did nothing against monsters. It arrived with patch 2.0.1. Until patch 4.0.1 it reduced the chance to be critically hit, and from 4.0.1 it reduced all player damage. In patch 4.1.0 its scaling changed so that each point added the same survival, the effective-health linearity you derived for armor in MMO303 week 2. In Mists of Pandaria every level-90 character received base resilience, 65% in patch 5.3.0, raised to 72% in 5.4.0 and 77% in 5.4.7. At 77%, player damage is multiplied by 0.23, which is the same as multiplying every player's health by `1/0.23 ≈ 4.35` against other players. Base resilience was removed in 6.0.2. Grain: global, the `h` in our code.

**World of Warcraft, Dampening (arena, from the December 2020 Shadowlands hotfix).** Dampening is a stacking debuff in arenas that reduces healing received and absorbs by 1% per stack. Per Warcraft Wiki, it applies from the start in 2v2 and after five minutes in 3v3, and each player gains a stack every 10 seconds. Ten minutes into a 3v3 match, healing is down by about 30%. Grain: global, but the multiplier is a function of time. It is aimed at the stalemate MMO303 week 11 found when healing sits near the threshold that stops deaths.

**League of Legends, ARAM modes (2026 patches).** ARAM is a single-lane mode. Riot gives individual champions mode-specific modifiers for incoming damage, outgoing damage and healing. In patch 26.06, for example, Swain's ARAM: Mayhem modifiers moved from +15% to +5% incoming damage, from −5% to 0% outgoing damage, and from −20% to −10% healing. Grain: per champion, per mode, three multipliers. Here the "other mode" is not PvE at all. The same logic applies to any two contexts that weigh a character differently.

Five games, one form. When you read a patch note that says "in PvP only", find the base, the mode and the multiplier, and ask at which grain it was applied.

### Design judgment, eyes open

- **Split late and narrow.** Try to meet both targets with shared numbers first. The clone constraint tells you when that is impossible, so compute it before splitting, not after players complain.
- **Split the field that differs between the metrics.** Here PvE counts burst once per minute and PvP counts it once per fight, so burst damage is the field to split. Splitting sustained damage for the Ravager would have fixed its TTK too, but it would also have made its long PvP fights weaker, which nobody asked for.
- **Prefer multipliers that players can read.** "Deals 20% less damage to players" is one line on a tooltip. A second copy of the whole skill, as in Guild Wars, is two skills to learn.
- **Every split is a promise to maintain it.** Once split, a value can drift in two directions. Guild Wars 2's 2018 un-splitting of 86 values is what paying that debt looks like.

## 3. The grain of a split: global, timed, class, ability

Section 2 used the finest grain. Designers have four, from coarsest to finest.

### Global multipliers change pace, and they are not neutral

A global PvP multiplier applies to every player. The simplest is `h`, a multiplier on every player's health against other players (or equivalently a divisor on all player damage, as resilience was). It is tempting to think a global multiplier only changes pace, making every fight longer by the same factor. It does not, because burst is a fixed amount while sustained damage scales with time. Read the `h` columns from the code:

| Class | TTK at `h = 1` | TTK at `h = 2` | TTK at `h = 4.35` |
|---|---|---|---|
| Duelist | 20.0 s | 53.3 s | 131.7 s |
| Ravager | 8.6 s | 51.4 s | 152.1 s |
| Channeler | 25.7 s | 54.3 s | 121.4 s |
| Slowest / fastest | 3.0 | 1.06 | 1.25 |

Doubling health nearly erases the spread, because the Ravager's opener now covers 40% of the target instead of 80%. At the resilience-era factor of 4.35 the order flips. The Ravager, the burst class, is now the slowest killer, because a long fight is a sustain contest. A global lever meant only to slow PvP down has quietly moved power from burst classes to sustain classes. Any time you touch `h`, recompute the whole roster.

Global levers are still valuable. They are one number, easy to explain, and they solve pace problems that per-class splits cannot. Just treat them as balance changes, not as neutral dials.

### Time-based multipliers target stalemates

Dampening is a global multiplier on healing that grows with match length. It exists because some fights have no natural end. In MMO303 week 11's reference fight, healing above a threshold stopped deaths entirely. A ramp pushes every team below that threshold eventually, so every match ends, while leaving the first minutes untouched. The design question is the ramp's start and slope. Start too early and healers are weak in every fight. Start too late and players sit through ten-minute stalemates first.

### Per-class multipliers fix fairness

A per-class aura ("deals 10% less damage to players") is the coarsest lever that can change relative strength between classes. It is simple to communicate and cheap to maintain, one number per class. Its weakness is bluntness. A class that is fine in sustained fights and too strong in openers gets weaker at both.

### Per-ability fields fix identity problems

The `p` in section 2 is a per-field split. It targets exactly the part of the class that the two metrics weigh differently. It costs the most, because every such split is a number players must know and a number designers must keep in sync.

A quick rule for choosing the grain. Fix pace with global, fix stalemates with time, fix fairness with class, and fix identity with fields. Work from coarse to fine, and stop at the first grain that meets both targets.

## 4. What splits cost

Splits are not free. Name the costs and you can budget them.

### The count

If a game has `A` abilities, each with `F` tunable fields, across `M` modes, the number of values a designer can tune is at most `A × F × M`. With 40 abilities per class, 4 fields each and 3 modes, that is 480 numbers per class, of which 320 are copies. Most will be identical. Each one that is not identical is a fact someone must know. Guild Wars 2's May 2018 update unified 86 split values in one patch, which tells you how many had built up.

### Knowledge and transfer

Players learn a class in one mode and carry expectations to the other. If the Ravager's burst takes 80% of a target in the open world and 64% in arenas, a player who learned in one will misjudge the other. Tooltips must say which number they show. The MMO303 week 2 rule applies here too. Distinguish "the tooltip shows X" from "the game computes X". Guild Wars solved the display problem by renaming the skill, "(PvP)", which is honest and costs a second name.

### Legitimacy

Splits change what "strong" means. When a class is weak in PvP after a PvP-only nerf, its players cannot point to the raid meter to argue it is fine. Some players read split tuning as the developer admitting that one mode is second priority. Communicate splits the way MMO303 week 14 taught for any balance change, with the metric that motivated them.

### Drift

Split values drift apart as each mode's designers tune their own copy. After enough patches the two versions of a class can differ in ways nobody chose deliberately. Budget a periodic audit that asks, for every split value, "does the reason for this split still exist?" If not, unsplit it.

## 5. A decision procedure

When a class is out of line in one mode, work through these steps in writing.

1. **Name the two metrics.** For example, PvE DPS over a 300-second fight, and PvP TTK against a standard target.
2. **Find the coupled numbers.** Which fields feed both metrics? For our model, `s` and `B` both do.
3. **Test for a shared fix.** Solve the clone constraint for your targets. If the class's intended shape lies inside the feasible band, fix it with shared numbers and do not split.
4. **Choose the coarsest grain that works.** Global for pace, timed for stalemates, class for fairness, field for identity.
5. **Compute the multiplier.** Use the one-line inverses from section 2. Round to a value players can read.
6. **Price the split.** Add it to the split register, a list of every split value with its reason and the date it was added.
7. **Schedule the audit.** Decide when you will check whether the split is still needed.

## In-class activity (25 minutes)

Pairs. Use the interactive or a spreadsheet with the section 2 model.

1. Add a fourth class, the Assassin, with `s = 600` and `B = 30,000`. Compute its PvE DPS and PvP TTK. (Hint: its burst equals `H`.)
2. The PvE lead says the Assassin must deal 1,100 DPS. What `s` does that force if `B` stays at 30,000? What is its TTK then?
3. Find a split that puts the Assassin inside the 15 to 22 second PvP band without touching PvE. Say which field you split and give the multiplier.
4. Now try the global lever. Find the smallest `h` that puts all four classes inside a band whose slowest-to-fastest ratio is at most 1.3. What does the average TTK become?
5. Write two sentences for the patch notes that explain your chosen fix to Assassin players.

Expected output: the four-class table with and without your split, your `h` result, and the two sentences. For step 2, `s = 600` already gives `600 + 30,000/60 = 1,100`. The Assassin's TTK is 0 seconds, a one-shot. For step 3, `p = (30,000 − 15 × 600) / 30,000 = 0.70` gives 15 seconds.

## Common misconceptions

- **"If the raid meter says two classes are equal, they are balanced."** Equal throughput over a long fight says nothing about the first ten seconds. Two classes with the same `s + B/C` can differ threefold in TTK.
- **"A global PvP health or damage multiplier is neutral."** It changes the weight of burst relative to sustain. In our roster, `h = 4.35` turned the fastest killer into the slowest.
- **"Splitting is always better than compromise."** Each split adds a number to learn and a number to maintain. The clone constraint tells you when you have no choice. Before that point, shared numbers are cheaper.
- **"PvP-only changes don't affect PvE players."** They do when PvE players do world PvP, when they switch modes, or when the change alters which class groups recruit because players read a class as "nerfed".

## Check yourself

1. A class has `s = 750` and `B = 21,000` with `C = 60` and `H = 30,000`. Compute its PvE DPS and PvP TTK. Is it inside a 15 to 22 second band?
2. For `D = 1,100`, find the clone shape for `T = 18` seconds.
3. The Channeler (`s = 1,050`, `B = 3,000`) gets a PvP burst multiplier instead of a sustain multiplier. What `p` puts it at 22 seconds? Is that a sensible split? Why or why not?
4. During a 3v3 arena match under the Dampening rule described in section 2, how much is healing reduced 8 minutes in? A healer's 5,000 HPS was enough to hold off 4,500 incoming DPS at the start. Does it still hold?
5. A designer proposes `h = 1.5` for all PvP. Using the table in section 3 or the code, which class gains the most relative to the others, and why?

<details>
<summary>Answers</summary>

1. PvE DPS `750 + 21,000/60 = 1,100`. TTK `(30,000 − 21,000)/750 = 12` seconds. Below the band. Too fast.
2. `s = (60 × 1,100 − 30,000)/(60 − 18) = 36,000/42 = 857.1`, `B = 30,000 − 18 × 857.1 = 14,571`.
3. `p = (30,000 − 22 × 1,050)/3,000 = 6,900/3,000 = 2.3`. It works on paper, but multiplying a tiny burst by 2.3 in PvP only would give the Channeler a burst identity in one mode and not the other. Players would learn two different classes. The sustain multiplier keeps the class's shape.
4. Eight minutes is 480 seconds, three minutes after dampening starts, so about 18 stacks and 18% less healing. 5,000 × 0.82 = 4,100 HPS, below the 4,500 incoming. The healer no longer holds.
5. At `h = 1.5` the TTKs are 36.7 (Duelist), 30.0 (Ravager) and 40.0 (Channeler) seconds. The Ravager went from 3.0× faster than the Channeler to 1.33× faster, so relative to the others it lost the most. The Channeler gains the most relative ground, because sustain matters more in longer fights.

</details>

## Lab / assignment hook

[Lab 07, split register](../labs/lab07.md). You will implement the model, solve the clone constraint, and write a split solver that finds the fewest, coarsest splits that put a six-class roster inside both target bands. Deliverable: the passing tests, a split register and a 300-word memo to the PvP and PvE leads.

## Sources

- Guild Wars 2 Wiki, "Game updates/2018-05-08" (May 8, 2018 balance update). The notes contain 86 lines stating a skill or trait value is no longer split between game modes. https://wiki.guildwars2.com/wiki/Game_updates/2018-05-08
- Guild Wars 2 Wiki, "Game updates/2018-07-10" (July 10, 2018). Rune of the Adventurer split to 25 endurance in PvP, 50 in other game modes.
- Guild Wars 2 Wiki, "Game updates/2018-08-28" (August 28, 2018). Prime Light Beam cooldown split, 60 to 75 seconds in PvP only.
- Guild Wars Wiki, "PvP (effect)" and "List of PvE and PvP versions of skills" (accessed September 2026). Altered skills carry "(PvP)" in their names; added in the May 22, 2008 update; the category held 188 entries.
- Warcraft Wiki, "PvP Resilience" (accessed September 2026). Introduced in patch 2.0.1; reduced crit chance until 4.0.1; linear scaling from 4.1.0 "in the same way armor and magic resistances do"; base resilience 65% in 5.3.0, 72% in 5.4.0, 77% in 5.4.7; base removed in 6.0.2; removed from remaining items in 8.3.0.
- Warcraft Wiki, "Dampening" (accessed September 2026). 1% healing and absorb reduction per stack; December 14, 2020 hotfix applying it immediately in 2v2 and after 5 minutes in 3v3; a stack every 10 seconds.
- League of Legends Wiki, "V26.06" (patch 26.06, 2026). ARAM: Mayhem mode-specific modifiers for Swain: incoming damage +15% to +5%, outgoing damage −5% to 0%, healing −20% to −10%.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.

## Interactive spec: examples/w07-split-tuning.html

**The one insight:** with shared numbers, the PvE target and the PvP target meet in a single narrow shape (the clone constraint), so fixing one mode breaks the other or erases class identity. A PvP-only multiplier on the right field decouples them.

**Layout (two linked views plus a plane):**

- Top left, "Raid meter (PvE DPS)". Horizontal bars for Duelist, Ravager, Channeler. Value `s + B/60`. A shaded band from 1,067 to 1,133 (±3% of 1,100). Bars inside the band use the palette's positive token; outside use negative plus a text marker "out of band".
- Top right, "Duel (PvP TTK vs 30,000 EHP)". Horizontal bars, value `max(0, h·H − p·B)/(q·s)` in seconds, axis 0 to 60 s (extend to 160 s automatically if any bar exceeds 60). Shaded band 15 to 22 s. Same in/out colouring and text marker.
- Bottom, "Shape plane". x axis `s` from 400 to 1,200, y axis `B` from 0 to 32,000. Draw the PvE line `B = 60·(1,100 − s)` and the PvP band as the strip between the curves `B = 30,000 − 15·s` and `B = 30,000 − 22·s` (these are straight lines). Highlight the segment of the PvE line inside the strip and label it "clone segment". Plot each class as a labelled dot at `(s, B)`. When Split is on and a class has `p ≠ 1` or `q ≠ 1`, draw a hollow ghost dot at its PvP-effective position `(q·s, p·B)` joined to the real dot by a dashed line.

**Controls:**

- Class selector (three buttons, keyboard accessible). For the selected class, sliders for `s` (400 to 1,200, step 10) and `B` (0 to 32,000, step 500).
- Toggle "Split PvP from PvE" (off by default). When on, show per-class sliders `p` (0.3 to 2.5, step 0.05) and `q` (0.5 to 1.5, step 0.05). These affect only the TTK panel and the ghost dots.
- Slider `h`, global PvP health multiplier (1.0 to 5.0, step 0.05), visible only when Split is on.
- Reset button restoring the lecture defaults.

**Numbers panel:** a table with, per class, `s`, `B`, PvE DPS (1 decimal), TTK (1 decimal), `p`, `q`, and a line "Slowest / fastest TTK ratio: x.xx". Also print the clone for the current TTK band ends: "Clone at 15 s: s = 800.0, B = 18,000; at 22 s: s = 947.4, B = 9,158" computed from `s = (60·1,100 − 30,000)/(60 − T)`.

**Test values (must match exactly):**

- Defaults: Duelist (900, 12,000) PvE 1,100.0, TTK 20.0; Ravager (700, 24,000) PvE 1,100.0, TTK 8.6; Channeler (1,050, 3,000) PvE 1,100.0, TTK 25.7.
- Ravager B = 18,000, Split off: PvE 1,000.0, TTK 17.1.
- Ravager s = 800, B = 18,000: PvE 1,100.0, TTK 15.0.
- Split on, Ravager p = 0.80: TTK 15.4, PvE unchanged 1,100.0. Channeler q = 1.20: TTK 21.4.
- Split on, h = 2.0, all p = q = 1: TTK 53.3, 51.4, 54.3; ratio 1.06. h = 4.35: 131.7, 152.1, 121.4; ratio 1.25.

**First screen:** defaults loaded, Split off, with the Ravager's TTK bar visibly out of band while all three PvE bars sit inside theirs. A one-line caption above: "Same raid meter. Very different duels."
