# GD203 · Week 05 — DPS, burst and sustain

**Why this matters:** "Which weapon is better?" has no answer until you say how long the fight lasts. A single DPS number hides that question, and most arguments about balance are really arguments about fight length that nobody has named.

**You will be able to:**
- Compute alpha damage, burst DPS, sustained DPS and clip damage for a weapon or ability rotation.
- Plot cumulative damage over time for two weapons and find the fight length at which the better one changes.
- Compute time-to-kill against a target that heals or regenerates, and find the healing rate at which a weapon can never kill.
- Critique a weapon or class kit by naming which fight lengths it wins and which it loses.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapter on combat, sections on damage over time and resource pacing; Schreiber, *Game Balance Concepts*, level 6 (situational balance). Re-read your notes from GD203 week 4.

**Prerequisites from earlier courses:** Time-to-kill and breakpoints from [GD203 week 4](w04-time-to-kill-and-time-to-die.md). Stocks and flows from [GD102 week 2](../../GD102-systems-design-and-game-mechanics/syllabus.md), because health under regeneration is a stock with an inflow and an outflow. Expected value from [MA102 week 4](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md).

**Interactive:** [examples/w05-burst-vs-sustain.html](../examples/w05-burst-vs-sustain.html) (specified at the end of this lecture). Keep it open during section 2.

---

## 1. What one DPS number hides

**Damage per second (DPS)** is total damage divided by time. It sounds like one number. It is at least four, and good designers keep them apart.

- **Alpha damage** is the damage of the very first hit, delivered at time zero. The name comes from "alpha strike," an opening volley.
- **Burst DPS** is the rate while everything is firing, before any reload, cooldown or resource runs out. For a weapon that hits for `d` every `Δ` seconds, burst DPS is `d / Δ`.
- **Clip damage** is how much damage you can deal before you must stop. For a gun it is magazine size times damage. For a caster it is what a full mana bar or a set of cooldowns delivers.
- **Sustained DPS** is the long-run average, including reloads, cooldowns and resource refills. It is the number that matters in a fight that lasts much longer than one burst.

The tooltip in most games shows one of these, usually burst DPS, and calls it DPS. Players then compare two weapons by that number and are surprised when the one with the lower number wins. They are not wrong to be surprised. They were given the wrong number for the fight they were in.

Week 4 gave you the tool to see this. Against a target with few hits-to-kill, alpha damage and breakpoints decide the result. Against a target with many hits-to-kill, sustained DPS decides it. Burst sits in between. This week makes that transition visible.

## 2. Worked example: which weapon wins depends on how long the fight lasts

### The hook

In Minecraft (Java Edition, after the 1.9 combat update), a diamond sword lists 7 damage at 1.6 attacks per second, so 11.2 damage per second on paper. A diamond axe lists 9 damage at 1.0 attack per second, so 9.0 per second. By the DPS number the sword is 24% better. Many players still open fights with an axe. Why?

Because the axe's first swing hits for 9 and the sword's for 7. If the target has 9 health or less left, the axe finishes it one swing earlier. Java Edition axes also disable a raised shield for 5 seconds, which is a burst-window effect. It opens a short period where your damage lands. Against a zombie, which takes three hits from either weapon, the sword finishes in 1.25 seconds and the axe in 2.0 seconds. The sword wins the long game and the axe wins the first moment.

Team Fortress 2 shows the same split with a magazine. The rocket launcher deals 90 base damage per rocket, fires every 0.8 seconds, and holds 4 rockets. That is 360 damage in 2.4 seconds, a burst rate of 112.5 per second. Then it has to reload. The wiki lists 0.92 seconds for the first rocket and 0.8 for each after, so refilling the clip takes about 3.3 seconds. Plug those timings into this week's model and a long fight averages about `360 / (3.2 + 3.32) ≈ 55` damage per second, roughly half the burst rate. Treat that as an estimate. It assumes every rocket hits at base damage and that the Soldier empties the clip before reloading, and real play does neither. A Soldier player knows this without doing the arithmetic. They try to finish a fight inside one clip.

### The model

Describe any repeating attack with four numbers:

- `d`, damage per hit.
- `n`, hits before a forced pause (clip size, charges, or casts before a cooldown). Use `n = ∞` for a weapon that never pauses.
- `Δ`, the time between hits while firing.
- `R`, the length of the pause (reload or cooldown) after the clip is empty.

One cycle lasts `L = n × Δ + R` and delivers `n × d`. So:

```
alpha         = d
burst DPS     = d / Δ
clip damage   = n × d
sustained DPS = n × d / (n × Δ + R)
```

The quantity that decides fights is **cumulative damage**, `D(t)`, the total damage dealt by time `t`, with the first hit at `t = 0`. For a weapon that never pauses, `D(t) = d × (floor(t / Δ) + 1)`. For a clip weapon, count the full cycles completed, then the hits in the current cycle, capped at `n`.

Time-to-kill is the first moment `D(t)` reaches the target's health. Two weapons can be compared at every fight length by plotting both `D(t)` curves on one chart. Wherever one curve is above the other, that weapon has dealt more damage so far.

### Numbers you can check

Two made-up weapons, chosen so the arithmetic stays clean.

| Weapon | d | n | Δ (s) | R (s) | Alpha | Burst DPS | Clip damage | Sustained DPS |
|---|---|---|---|---|---|---|---|---|
| Cannon | 90 | 4 | 0.8 | 4.0 | 90 | 112.5 | 360 | 50 |
| Repeater | 15 | ∞ | 0.2 | 0 | 15 | 75 | — | 75 |

Check the cannon's sustained rate. One cycle is `4 × 0.8 + 4.0 = 7.2` seconds and deals 360, so `360 / 7.2 = 50`.

Cumulative damage at selected times:

| Time (s) | Cannon D(t) | Repeater D(t) | Leader |
|---|---|---|---|
| 0 | 90 | 15 | Cannon |
| 0.8 | 180 | 75 | Cannon |
| 2.4 | 360 | 195 | Cannon |
| 4.0 | 360 | 315 | Cannon |
| 4.6 | 360 | 360 | Tie |
| 6.0 | 360 | 465 | Repeater |
| 9.6 | 720 | 735 | Repeater |
| 15.0 | 810 | 1,140 | Repeater |
| 30.0 | 1,620 | 2,265 | Repeater |

The cannon leads for the first 4.6 seconds, then the repeater leads for good. Now turn that into time-to-kill against targets of different health, which is what the player feels:

| Target health | Cannon TTK (s) | Repeater TTK (s) | Faster |
|---|---|---|---|
| 90 | 0.0 | 1.0 | Cannon |
| 180 | 0.8 | 2.2 | Cannon |
| 300 | 2.4 | 3.8 | Cannon |
| 360 | 2.4 | 4.6 | Cannon |
| 400 | 7.2 | 5.2 | Repeater |
| 720 | 9.6 | 9.4 | Repeater |
| 1,000 | 16.8 | 13.2 | Repeater |
| 3,000 | 58.4 | 39.8 | Repeater |

Check one row by hand. The repeater against 300 health needs `ceil(300 / 15) = 20` hits, and the 20th hit lands at `19 × 0.2 = 3.8` seconds.

Look at the jump between 360 and 400 health. The cannon's TTK goes from 2.4 seconds to 7.2 seconds, tripling, for 11% more target health. That is a **clip breakpoint**. If the target survives the clip, the cannon has to sit through a whole reload before it can finish. It is week 4's staircase with one very tall step. Clip damage relative to target health is the single most useful number for a burst weapon.

### See it move

Open `w05-burst-vs-sustain.html`. The top panel plots `D(t)` for both weapons from 0 to 30 seconds, with a horizontal line at the target's health. The bottom panel plots TTK against target health for both weapons, so you can read off which weapon wins for every enemy in your game at once.

Drag the target health slider from 300 to 400 and watch the cannon's TTK marker leap. Then drag the cannon's reload from 4.0 down to 1.0 seconds. The crossover point in the top panel moves right, and at a reload of about 1.6 seconds the cannon's sustained rate reaches 75 and the two long-run lines run parallel. Every weapon tuning decision is visible here as a move of that crossover.

### Cross-game recognition

Rewrite each case as alpha, burst, clip and sustained.

**Minecraft (Java Edition, 1.9 onward).** Axe: alpha 9, sustained 9.0. Sword: alpha 7, sustained 11.2. No clip or reload. At `t = 0` the axe leads 9 to 7. At 0.625 seconds the sword has swung again and leads 14 to 9. The lead then swaps a few times, because both weapons hit in steps (the axe is ahead 18 to 14 at 1.0 seconds and 36 to 35 at 3.0 seconds). From 3.125 seconds on, the sword leads for good. With discrete hits, a crossover is a region, not a point. The axe's shield-disabling effect is a separate burst tool: it removes the target's mitigation for a short window, which raises your effective burst without changing any number on the weapon.

**Team Fortress 2.** Rocket launcher: alpha 90, burst 112.5, clip 360, sustained about 55 by our model's estimate, roughly half of burst. Put the class health values from week 4 next to the clip damage. A full clip of base-damage rockets, 360, is more than any class's base health (the Heavy has 300). So the launcher is designed to finish one full-health opponent per clip at base damage, if every rocket lands. That is a clip breakpoint chosen on purpose. An overhealed Heavy, whose health can reach 450, pushes past it.

**World of Warcraft (retail and classic eras).** A damage-dealing class usually has a steady rotation plus a few major cooldowns, abilities that raise damage for a short window and then lock out for minutes. That is our model with abilities in place of bullets. The rotation is sustained DPS. The cooldowns are burst. In a fight that lasts seconds, such as a PvP kill window, the burst decides the outcome. In the classic Naxxramas fight against Patchwerk, which has about 3,850,000 health and a 7-minute enrage, the raid needs a sustained rate of at least about 9,170 DPS for 420 seconds, and a cooldown that is up for a small fraction of that window changes the total only a little. The same class can be strong in one of those fights and middling in the other, and neither ranking is wrong.

Three games, one question. When you see a new weapon or kit, write down its alpha, burst, clip and sustained numbers, then ask how long the fights it will be used in actually last.

### Design judgment

- **Name the fight length.** Every DPS comparison should say "over a T-second fight." When someone on your team says a weapon is overpowered, ask which fight length they mean. They may both be right.
- **Burst is stronger than its DPS suggests in short fights and in PvP.** Burst can end a fight before the target reacts. Week 4's time-to-die argument applies here. If the burst window is shorter than a player's reaction time plus a defensive action, the victim gets no decisions. Many games cap burst for that reason, even when the sustained numbers look fine.
- **Sustain is stronger than it looks in long fights and PvE.** Over a 7-minute boss, the weapon with the higher sustained rate wins, whatever its tooltip says.
- **Clip damage is a design lever.** Set clip damage just above a common target's health and you create a strong, legible goal ("kill one per clip"). Set it just below and the weapon feels frustrating, because it almost works.
- **Give the two roles different costs.** If a burst weapon also has the best sustained DPS, it dominates everywhere. Pay for burst with a long reload, a resource cost, a wind-up, or a positional risk. Pay for sustain with low alpha, so it cannot finish targets quickly.

## 3. Sustain: healing, regeneration and the stalemate

**Sustain** is the ability to keep going over a long fight. On the defensive side, it means healing or regenerating health. A regenerating target adds a second flow to the fight. Health is now a stock with damage flowing out and healing flowing in, the same stock-and-flow picture you drew in GD102.

In the smooth view, if the attacker deals `DPS` and the target heals `HPS` (healing per second), the target loses health at the net rate `DPS − HPS`:

```
TTK ≈ H / (DPS − HPS)     if DPS > HPS
TTK = never                if DPS ≤ HPS
```

This is not a straight line. It is a hyperbola, and it goes to infinity as healing approaches damage. Take `H = 1,000` and `DPS = 100`:

| Target HPS | Net DPS | TTK (s) | Change vs no healing |
|---|---|---|---|
| 0 | 100 | 10 | — |
| 25 | 75 | 13.3 | +33% |
| 50 | 50 | 20 | +100% |
| 75 | 25 | 40 | +300% |
| 90 | 10 | 100 | +900% |
| 95 | 5 | 200 | +1,900% |
| 99 | 1 | 1,000 | +9,900% |

The first 50 points of healing double the fight. The next 40 multiply it by five more. Near the stalemate line, every point of healing is worth enormous amounts of time.

This has three consequences you should design for.

**Healing near enemy DPS creates stalemates.** A fight where a healer out-heals the damage never ends. Designers break stalemates with mechanics that change one side of the equation over time. Enrage timers raise the boss's DPS after a set time, which is what Patchwerk's 7-minute limit does. Healing-reduction effects cut `HPS` on demand. Resource limits (mana) force healing to stop eventually, which turns sustain into a clip with a very long reload.

**Burst beats regeneration.** Regeneration only matters over time. A burst weapon that deals the target's health before much regeneration happens barely notices it. Run the cannon and repeater from section 2 against targets that regenerate continuously, with regeneration capped at full health (computed by simulating each hit):

| Target health | Regen per second | Cannon TTK (s) | Repeater TTK (s) |
|---|---|---|---|
| 200 | 0 | 1.6 | 2.6 |
| 200 | 60 | 2.4 | 12.4 |
| 300 | 0 | 2.4 | 3.8 |
| 300 | 60 | never | 19.0 |
| 1,000 | 30 | 38.4 | 22.0 |
| 1,000 | 60 | never | 65.8 |

Against the 200-health target, 60 regeneration per second makes the repeater almost five times slower and the cannon only 1.5 times slower. The cannon wins because it deals 360 in 2.4 seconds, before the target can heal back. But against the 300-health target with the same regeneration, the cannon's clip falls short (360 dealt minus 144 healed during the burst is 216), the target heals to full during the reload, and the cannon never wins. Its sustained 50 DPS is below the 60 regeneration. The repeater grinds it down at a net 15 per second.

So regeneration splits attackers into two groups. Those who can kill inside one burst window mostly ignore it. Those who cannot need sustained DPS above the regeneration rate, and they slow down along the hyperbola as they approach it.

**Attacker sustain is the mirror image.** Lifesteal, self-healing and damage shields on the attacker slow their own time-to-die clock. The same hyperbola applies from the other side. A character whose self-healing nearly matches incoming damage is almost impossible to kill without burst, which is why lifesteal-heavy builds are usually countered by burst, and burst is countered by mitigation that is strongest against big hits.

## 4. From paper DPS to effective DPS

The numbers so far assume every hit lands at full value and the attacker never stops. Real fights leak damage in four places. You can fold them into one expression:

```
effective DPS = paper DPS × uptime × hit rate × (1 − mitigation) × (1 − overkill share)
```

- **Uptime** is the share of the fight you are actually attacking. Moving out of a fire patch, running between targets, or being stunned all cut uptime. A melee class with 70% uptime and a ranged class with 95% uptime are not equal even if their paper DPS is.
- **Hit rate** is the share of attacks that connect, from accuracy, dodge or miss chances. Diablo II's defense works entirely through this term, as you will see in [MMO303 week 2](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md).
- **Mitigation** is [week 3](w03-mitigation-curves-and-effective-hp.md)'s topic. It enters here as a multiplier.
- **Overkill share** is week 4's wasted damage on the last hit. In a fight against many small targets, overkill can be a large share of damage. A 90-damage rocket that kills a 20-health target wastes 78% of itself.

Each term is a design lever. Encounter designers control uptime through movement demands. Class designers trade burst for uptime (a ranged class with low burst and high uptime versus a melee class with high burst and low uptime). When a class seems strong in one encounter and weak in another, one of these terms usually explains it.

## In-class activity (25 minutes)

Groups of three. Each group designs a pair of weapons for a fantasy RPG, a "greataxe" and a "twin daggers," with these rules.

1. Both weapons must have sustained DPS within 5% of 40.
2. The greataxe must win against any single target with 120 health or less. The twin daggers must win against any single target with 400 health or more.
3. Choose `d`, `n`, `Δ` and `R` for each. You may give the greataxe a cooldown-style pause (`n = 1` hit, then a pause) or a clip.
4. Fill a TTK table for target health 60, 120, 200, 400 and 800. Mark the crossover.
5. Add a regenerating troll: 300 health, 20 regeneration per second. Which weapon kills it faster? Did you expect that answer?

Expected output: parameter table for both weapons, a five-row TTK table, and a one-paragraph note on the troll. Two groups present, and the class checks their crossover with the interactive.

## Common misconceptions

- **"The weapon with higher DPS is better."** Only for a stated fight length. Short fights reward alpha and burst. Long fights reward sustained DPS.
- **"Healing adds a fixed amount of survival."** Healing subtracts from the attacker's rate, so its effect on TTK grows without limit as healing approaches damage. The first and the fiftieth point of healing are not worth the same.
- **"Sustained DPS is just burst DPS minus a bit."** A long reload or cooldown can halve it or worse, as the TF2 launcher and our cannon show.
- **"Regeneration hurts every attacker equally."** It barely affects an attacker who kills inside one burst window, and it can make a low-burst attacker unable to kill at all.

## Check yourself

1. A crossbow deals 60 per shot, holds 1 bolt, fires instantly, and takes 2.4 seconds to reload. A shortbow deals 18 every 0.6 seconds and never reloads. Compute each weapon's alpha, burst and sustained DPS. Which kills a 60-health target faster, and which kills a 300-health target faster?
2. A boss has 50,000 health and heals 400 per second. Your raid deals 900 DPS. What is the TTK? How much does it shrink if you apply an effect that halves the boss's healing?
3. Using the cannon from section 2, what is the largest target health the cannon can kill inside its first clip? What reload time would make the cannon's sustained DPS equal to the repeater's?

<details>
<summary>Answers</summary>

1. Crossbow: alpha 60, burst DPS undefined (one shot, so treat burst as the alpha), sustained `60 / 2.4 = 25`. Shortbow: alpha 18, burst and sustained `18 / 0.6 = 30`. Against 60 health the crossbow kills at `t = 0` and the shortbow needs 4 hits, landing at `3 × 0.6 = 1.8` s. Against 300 health the crossbow needs 5 shots, landing at `4 × 2.4 = 9.6` s. The shortbow needs `ceil(300 / 18) = 17` hits, landing at `16 × 0.6 = 9.6` s. It is a tie. Change either weapon slightly and it tips.
2. Net rate `900 − 400 = 500`, TTK `50,000 / 500 = 100` s. With healing halved, net `900 − 200 = 700`, TTK about 71.4 s, a 29% cut from one debuff. The closer the healing was to the damage, the larger this cut would be.
3. One clip deals `4 × 90 = 360`, so 360 health. For sustained DPS of 75, `360 / (3.2 + R) = 75`, so `3.2 + R = 4.8` and `R = 1.6` s.

</details>

## Lab / assignment hook

**[Lab 05: Burst, sustain and the crossover](../labs/lab05.md).** Build a time-step spreadsheet that computes cumulative damage for three weapons and a regenerating target, find each crossover, and tune one weapon so it wins a stated fight-length band. The sheet extends your week 4 breakpoint table.

## Sources

- Minecraft Wiki, "Sword" (Java Edition, 1.9 combat update onward, 1.21 era): diamond sword 7 damage, attack speed 1.6. https://minecraft.wiki/w/Sword
- Minecraft Wiki, "Axe" (Java Edition, 1.21 era): diamond axe 9 damage, attack speed 1.0; axes disable a target's shield for 5 seconds. https://minecraft.wiki/w/Axe
- Official TF2 Wiki, "Rocket Launcher": base damage 90, clip of 4, attack interval 0.8 s, reload 0.92 s first and 0.8 s consecutive. https://wiki.teamfortress.com/wiki/Rocket_Launcher
- Official TF2 Wiki, "Health": class base health and overheal maximums (Heavy 300 base, 450 overhealed). https://wiki.teamfortress.com/wiki/Health
- Warcraft Wiki, "Patchwerk (Classic)" (40-player Naxxramas, patch 1.12): about 3,850,000 health, 7-minute enrage. https://warcraft.wiki.gg/wiki/Patchwerk_(Classic)
- Warcraft Wiki, "Cooldown" (retail era): distinction between the global cooldown and individual ability cooldowns. https://warcraft.wiki.gg/wiki/Cooldown
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.
- Schreiber, I. (2010). *Game Balance Concepts*, level 6. https://gamebalanceconcepts.wordpress.com/

## Interactive spec: examples/w05-burst-vs-sustain.html

**The one insight the visual must make obvious:** which weapon is better flips at a specific fight length. Burst leads early, sustain leads late, and a clip that falls just short of a target's health triples the time to kill.

**Layout.** Two stacked panels sharing a control column (column on the right on desktop, above the panels on mobile).

**Top panel: "Damage dealt so far."**
- x axis: time `t` from 0 to `T_max` (default 30 s, selectable 10 / 30 / 120).
- y axis: cumulative damage.
- Weapon A (blood red) and weapon B (steel) as step functions `D(t)`. First hit at `t = 0`.
- Horizontal ochre line at target health `H`. Mark each weapon's kill time where its curve first reaches `H` (a dot plus a label "A kills at 2.4 s").
- Shade the band between the two curves in the color of whichever weapon leads. Label each crossover time.
- When regeneration `r > 0`, instead plot the target's remaining health for each weapon, `h(t)`, falling on each hit and rising at `r` per second, capped at `H`. Provide a toggle "show damage dealt / show target health" and switch to target health automatically when `r > 0`.

**Bottom panel: "Time to kill by target health."**
- x axis: target health from 1 to `H_max` (default 1,000; selectable 500 / 1,000 / 5,000).
- y axis: TTK in seconds.
- Both weapons as step curves. Show "never" as a line at the top edge with a label when a weapon cannot kill (only possible with `r > 0`).
- A vertical cursor at the current `H`.

**Model (exact).**
- Weapon parameters: `d`, `n` (integer, or "no reload" checkbox meaning infinite), `Δ`, `R`.
- Hit times: cycle length `L = n × Δ + R`; hits at `c × L + k × Δ` for `c = 0, 1, 2, ...` and `k = 0 .. n − 1`. With no reload, hits at `k × Δ`.
- Without regeneration: TTK is the time of the first hit at which cumulative damage `≥ H` (use a tolerance of 1e-9).
- With regeneration: simulate hit by hit. Start `h = H`, `last = 0`. For each hit time `t`: `h = min(H, h + r × (t − last))`, `last = t`, `h = h − d`. Kill when `h ≤ 1e-9`. Declare "never" if there is no kill by `t = 600` s.
- Readouts for each weapon: alpha, burst DPS `d / Δ`, clip damage `n × d`, sustained DPS `n × d / L`, TTK at current `H`, and average DPS over the kill `H / TTK` (show "instant" when TTK = 0).

**Controls.** Sliders plus numeric inputs for each weapon's `d` (1-500), `n` (1-50 or no reload), `Δ` (0.05-5 s), `R` (0-15 s); target `H` (1-5,000); regeneration `r` (0-200 per second). Presets:
- "Cannon vs repeater" (default): A = (90, 4, 0.8, 4.0), B = (15, no reload, 0.2, 0), H = 360, r = 0.
- "Axe vs sword (Minecraft Java)": A = (9, no reload, 1.0, 0), B = (7, no reload, 0.625, 0), H = 20. Add a note that mitigation is ignored in this preset.
- "Troll": cannon vs repeater, H = 300, r = 60.

**Test values (must match exactly).**
| Preset / input | A TTK (s) | B TTK (s) |
|---|---|---|
| Cannon vs repeater, H 90 | 0.0 | 1.0 |
| Cannon vs repeater, H 360 | 2.4 | 4.6 |
| Cannon vs repeater, H 400 | 7.2 | 5.2 |
| Cannon vs repeater, H 1,000 | 16.8 | 13.2 |
| Cannon vs repeater, H 200, r 60 | 2.4 | 12.4 |
| Troll (H 300, r 60) | never | 19.0 |
| Cannon vs repeater, H 1,000, r 30 | 38.4 | 22.0 |
| Axe vs sword, H 20 | 2.0 | 1.25 |

Axe vs sword lead changes in the top panel (H set high): axe leads on [0, 0.625), sword on [0.625, 1.0), axe on [1.0, 1.25), sword on [1.25, 3.0), axe on [3.0, 3.125), sword from 3.125 on.

Crossover in the top panel for the default preset at H off-screen: A leads for `t < 4.6`, tie at 4.6 (360 each), B leads from 4.8 on. Sustained DPS readouts: cannon 50.00, repeater 75.00.

**First screen:** default preset with `H = 360` and the kill markers visible, plus a one-line caption: "Cannon kills 360 health in 2.4 s. Add 40 health and it takes 7.2 s." A single "Try 400" chip sets `H = 400`.

**Style:** program palette; weapon A in blood red, weapon B in steel, target health and regeneration in ochre, positive change in moss. No game art. Respect `prefers-reduced-motion`.
