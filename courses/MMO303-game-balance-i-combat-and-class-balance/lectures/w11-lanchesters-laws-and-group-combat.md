# MMO303 · Week 11 — Lanchester's Laws and Group Combat

**Why this matters:** An MMO battle is many duels happening at once, and the players who die early stop dealing damage. That single fact makes numbers count far more than intuition says, and it decides whether your world-PvP, battlegrounds and raid adds reward headcount, gear or tactics.

**You will be able to:**
- Derive Lanchester's square law from two attrition equations and compute survivors and fight length.
- Compute how much per-player power a smaller group needs to tie a larger one.
- Explain which game rules (chokepoints, area damage, target caps, focus fire) push a fight toward the linear law or the square law.
- Critique a group-PvP design by predicting how it rewards blobbing.

**Before class:** Lanchester's laws overview (any operations-research text, or the summary in Washburn's Naval Postgraduate School notes "Lanchester Systems", sections 1 and 2); Schreiber & Romero, *Game Balance* (2021), the chapter on combat, pages on time-to-kill.

**Prerequisites from earlier courses:** time-to-kill and DPS from GD203 [week 4](../../GD203-combat-and-progression-design/lectures/w04-time-to-kill-and-time-to-die.md) and [week 5](../../GD203-combat-and-progression-design/lectures/w05-dps-burst-and-sustain.md); effective HP and effective DPS from [MMO303 week 3](w03-effective-hp-and-effective-dps.md); the effective-HP derivation in [MMO303 week 2](w02-armor-and-damage-mitigation.md); rates of change from [MA101 week 2](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md).

**Interactive:** [examples/w11-lanchester-battle.html](../examples/w11-lanchester-battle.html) (built from the spec at the end of this lecture). Keep it open during section 2.

---

## 1. Group fights are not sums of duels

In GD203 you computed time-to-kill for one attacker against one target. A group fight looks like a pile of those calculations, and it is tempting to add them up. Ten players with 100 damage per second (DPS) each deal 1,000 DPS. Eight players deal 800. So the ten should win by about 25%, right?

They win by far more, and the reason is **attrition**, the steady loss of units during a fight. When one of the eight dies, the eight become seven, and their damage drops to 700. The bigger side kills faster, so the smaller side loses damage sooner, so the bigger side takes less damage, so it keeps its own numbers longer. The advantage feeds itself.

Frederick Lanchester, an English engineer, wrote this feedback loop down as a pair of equations in *Aircraft in Warfare* (1916), while trying to understand air combat in the First World War. His equations are still the starting point for military combat models, and they fit MMO group combat surprisingly well because MMO combat is closer to his assumptions than real war is. Every player has exact HP, exact DPS and a tab-target that lets them shoot anyone in range.

A few terms, used throughout:

- **Force size** `A` and `B`: how many combatants are alive on each side at time `t`. `A₀` and `B₀` are the starting sizes.
- **Kill rate per unit** `α` (alpha): how many enemies one member of side A kills per second. For a player with DPS `d_A` shooting targets with HP `H_B`, `α = d_A / H_B`. A 100 DPS player against 1,000 HP targets has `α = 0.1` kills per second.
- **Kill rate** `β` (beta): the same for side B.
- **Aimed fire**: each attacker picks one target and all its damage goes into that target. Tab-target MMO combat is aimed fire.
- **Focus fire**: the whole side aims at the same target until it dies, then switches.

## 2. Worked example: why 10 players beat 8 by far more than 25%

### The hook

In *Guild Wars 2*'s World vs. World mode, most area-of-effect skills hit at most 5 targets, and the game picks the 5 closest to the center of the area. A group of 30 players standing in one spot therefore takes the same total damage from a single area skill as a group of 5. Players have a name for the resulting tactic: the "blob," a large group moving and fighting as one tight mass.

Before you decide whether that cap is good or bad, answer a simpler question. Why would players want to stack numbers in the first place? If ten players really were only 25% stronger than eight, bringing extra players would be a modest advantage. Experienced PvP players treat a few extra bodies as decisive. Lanchester's square law says they are right, and tells you by how much.

### The model

Assume aimed fire, identical players within each side, and that dead players stop fighting. Each surviving member of side B kills `β` players of side A per second, so A shrinks at a rate proportional to B's size. The same holds the other way:

```
dA/dt = −β · B
dB/dt = −α · A
```

Divide the first equation by the second. Time cancels:

```
dA/dB = (β · B) / (α · A)
α · A · dA = β · B · dB
```

Integrate both sides from the start of the fight:

```
α · (A₀² − A²) = β · (B₀² − B²)
```

Rearranged, the quantity `α · A² − β · B²` never changes during the fight. That is **Lanchester's square law**:

```
α · A₀² − β · B₀²  =  α · A² − β · B²   at every moment
```

The side with the larger `α · N²` wins. When B hits zero, A's survivors are:

```
A_final = sqrt( A₀² − (β/α) · B₀² )
```

and when both sides have the same kill rate `k = α = β`, the fight lasts until

```
t_end = artanh(B₀ / A₀) / k
```

(Here `artanh` is the inverse hyperbolic tangent, available in any spreadsheet as `ATANH`. You do not need to derive it; you need to be able to use it.)

**Fighting strength is `α × N²`.** Quality counts once. Numbers count twice.

### What "quality" means for players

Substitute the per-player values. `α = d_A / H_B` and `β = d_B / H_A`. The tie condition `α · A₀² = β · B₀²` becomes

```
(d_A / H_B) · A₀² = (d_B / H_A) · B₀²
d_A · H_A · A₀²   = d_B · H_B · B₀²
```

So a side's fighting strength is **N² × DPS × HP**. The per-player quality term is DPS times HP. In week 3 you met effective DPS and effective HP; plug those in and the law covers armor, healing buffs and damage modifiers too. This is also why a 25% gear gap and a 25% headcount gap are not equivalent. To offset 25% more players, the smaller side needs `1.25² = 1.5625` times the DPS × HP per player. That is exactly 25% more DPS **and** 25% more HP per player, together.

### Numbers you can check

Every player has 1,000 HP and 100 DPS, so `α = β = 0.1` kills per second. Side B has 8 players. We vary side A.

| A₀ | Strength ratio A₀² : B₀² | Survivors, square law | Survivors, linear law (for comparison) | Fight length, square law |
|---|---|---|---|---|
| 8 | 64 : 64 | 0 (both wiped) | 0 | never ends cleanly |
| 9 | 81 : 64 | 4.12 | 1 | 14.2 s |
| 10 | 100 : 64 | 6.00 | 2 | 11.0 s |
| 12 | 144 : 64 | 8.94 | 4 | 8.0 s |
| 16 | 256 : 64 | 13.86 | 8 | 5.5 s |

Check the headline row by hand. `sqrt(10² − 8²) = sqrt(36) = 6`. Ten players beat eight and lose only four people. If the fight were a sum of duels, the ten would lose eight. The fight length is `artanh(0.8) / 0.1 = 1.0986 / 0.1 ≈ 11.0` seconds.

The column labeled "linear law" is what you get when fights really are a set of one-on-one duels, and section 3 explains when that happens.

Now compare with a discrete simulation. In the reference simulation for this lecture, each player is an individual with 1,000 HP, damage is applied every 0.01 seconds, and both sides focus fire. The ten win with 6 survivors in 10.5 seconds, one of them damaged. The continuous equations and the discrete players agree on survivors. The small difference in time comes from players dying in whole units instead of fractions.

### A visual you can move

Open the [Lanchester battle interactive](../examples/w11-lanchester-battle.html). The top panel is a battlefield of two groups of dots. The bottom-left panel plots each side's alive count over time, with the continuous square-law curve drawn as a thin line behind the discrete simulation. The bottom-right panel shows two bars for fighting strength, `N² × DPS × HP`, so you can see 100 against 64 before the fight starts.

Start at 10 against 8 and press Fight. Watch the curves. For the first few seconds both sides lose players at similar speed, then the smaller side's losses accelerate while the bigger side's slow down. Now drag side B's DPS up by 25% (to 125) and HP up by 25% (to 1,250). The strength bars become equal and the fight ends in a near mutual wipe: side B wins with 1 player left. Reset, then raise only side B's DPS. The slider moves in steps of 5, so you cannot hit the exact 56% (156). At 150 side A still wins with 2 survivors. At 155 side B wins with 1. The tipping point sits where the square law puts it. That is the insight made visible. A group's power is quadratic in its size, and per-player quality has to grow as the square to keep up.

### Cross-game recognition

**Iwo Jima, 1945.** J. H. Engel's 1954 paper "A Verification of Lanchester's Law" took the daily casualty records from the battle of Iwo Jima and fitted Lanchester's aimed-fire equations, with a term for American reinforcements landing over the first days. The computed American troop strength tracked the recorded numbers closely over the campaign. It remains the standard example that the square law describes real attrition and not only a thought experiment. When you tune an MMO fight with Lanchester's equations, you are using the same tool Engel checked against real battle data.

**Area damage and *Guild Wars 2*'s target cap.** Go back to the hook. Area damage behaves differently from aimed fire. An area attack hits every enemy in the circle, so its kills per second grow with how many enemies are packed in. Write that into the equations:

```
aimed fire:           dB/dt = −α · A
uncapped area fire:   dB/dt = −α · A · B     (each attacker hits all of B)
```

With area fire on both sides, dividing the equations gives `dA/dB = β/α`, a constant, and the conserved quantity becomes `α · A − β · B`. That is the **linear law**. Numbers count once, not twice. Uncapped area damage cancels the advantage of a blob. A 5-target cap undoes that the moment the blob is bigger than 5: each area skill hits a fixed number of people, which is aimed fire again, and the square law returns. *Guild Wars 2*'s cap is a design decision about which of Lanchester's laws governs large fights. It favors large groups on purpose or by side effect, and players respond by blobbing.

**Chokepoints in real-time strategy and dungeon design.** Lanchester's linear law was first described for ancient battles, where each soldier could fight only the enemy directly in front. Any game that forces one-on-one contact recreates it: a corridor one unit wide, a bridge, a doorway held by melee units. With `n` fighters meeting at a time, the numbers advantage shrinks to what you see in the linear column above. This is why RTS players pull a bigger army back through a narrow ramp, and why an outnumbered MMO group defending a keep wants to fight at the gate rather than in the courtyard. The map is choosing the law.

Three contexts, one idea. Ask of any group fight, "does killing an enemy reduce the damage coming back, and can every one of my players shoot at once?" If both answers are yes, numbers count squared.

### Eyes-open design judgment

The square law is not good or bad. It is a strong force you should decide about deliberately.

- **If you want big groups to win big, you already have it.** Tab-target combat with capped area damage produces the square law by default. Territorial PvP where organized guilds bring numbers may want exactly that. Expect players to blob, and expect small-group play to be crushed unless you give it separate objectives.
- **If you want outnumbered groups to have a chance, move fights toward the linear law.** Uncapped or softly capped area damage, chokepoints on the map, and objectives that only a few players can contest at once all reduce the value of headcount. Each has a cost. Uncapped area damage makes ten mages delete any group, and chokepoints make fights static.
- **Do not fix numbers with raw stat buffs.** An "outnumbered" bonus has to grow with the square of the gap to matter. A 20% damage bonus for a side outnumbered 10 to 8 closes less than half of the 56% gap. A buff large enough to close big gaps (a 2-to-1 gap needs 4×) makes small groups invulnerable against evenly matched opponents when the numbers swing.
- **Watch for snowballing in team games.** In a 5-versus-5 match, one early death turns 25 : 25 into 25 : 16 in strength terms, a 56% edge. That is why a single pick often decides a MOBA or battleground teamfight. If that is more decisive than you want, shorten time-to-kill less, or give the losing side a way to disengage.

## 3. When the linear law applies

The square law needs every living unit to be able to fire at a target of its choice. Break either condition and the law changes.

**One-on-one contact.** If only matched pairs can fight (a single-file corridor, a formal duel tournament bracket), each pair is an even duel, and the bigger side simply has spare players waiting. Ten against eight becomes eight even duels plus two fresh players, so 2 survivors. This is the classic statement of the linear law.

**Area fire.** As shown with the target cap, when each attacker's kills scale with how many enemies are present, numbers count once. Artillery, fireball spam and cleave attacks without target limits all push toward this.

**Mixed cases.** Real games sit between the two. A melee brawl where each player can reach only two or three enemies behaves like a partial square law. You can measure where your game sits by simulating a fight at several sizes and fitting survivors against starting numbers. Lab 11 does this. If survivors of `A₀` versus `B₀` follow `A₀ − B₀`, you are linear; if they follow `sqrt(A₀² − B₀²)`, you are square.

A useful designer's shorthand is the exponent. Write fighting strength as `quality × N^e`. The square law has `e = 2`, the linear law `e = 1`, and many real game modes land somewhere between. Your map, your area-damage rules and your target caps together set `e`.

## 4. Focus fire, spread damage and why raids call targets

Lanchester's aimed-fire equations assume each shot helps kill someone. Real players often waste damage by spreading it across many targets. Spread damage keeps every enemy alive (and firing) until the very end.

The reference simulation runs 10 against 8 with identical players (1,000 HP, 100 DPS) under each combination of targeting rules.

| Side A (10 players) | Side B (8 players) | Winner | Survivors | Fight length |
|---|---|---|---|---|
| Focus | Focus | A | 6 of 10 | 10.5 s |
| Focus | Spread | A | 10 of 10, at 64% HP on average | 8.0 s |
| Spread | Spread | A | 10 of 10, at 36% HP each | 8.0 s |
| Spread | Focus | **B** | 8 of 8, at 14% HP on average | 12.5 s |

Look at the last row. The smaller side won without losing anyone, because the bigger side's spread damage never reduced the smaller side's output while the smaller side removed shooters one at a time. Focus fire is worth more than a 25% headcount advantage. That is why raid and PvP groups have a caller who names targets, and why "assist" and target-marking tools matter for balance. A game that makes coordinated focus fire easy is a game that runs on the square law. A game where targeting is hard (action combat, heavy crowd control, stealth) drifts toward spread damage, and the math of large fights changes with it.

There is a second lesson in the table. With spread damage on both sides, nobody on the winning side dies. The fight looks close on the health bars and then the losing side collapses at once. Players describe these fights as "we were winning until we weren't." That feeling comes from the math, not from luck.

## 5. Healers and sustained fights

MMO groups have healers, and Lanchester had nothing like them. Healing restores HP to living allies without reviving the dead. In aimed-fire terms, a side's healers reduce the rate at which the other side's damage turns into deaths.

The reference simulation keeps side A at 10 damage dealers and gives side B 6 damage dealers plus 2 healers. Everyone has 1,000 HP. Damage dealers deal 100 DPS, healers deal none, and each healer heals the lowest-health living ally. Both sides focus fire, and side A attacks side B's damage dealers first.

| Healing per healer | Winner | Survivors | Fight length |
|---|---|---|---|
| 0 | A | 8 of 10 | 9.2 s |
| 150 HP/s | A | 7 of 10 | 16.2 s |
| 200 HP/s | A | 5 of 10 | 37.1 s |
| 250 HP/s | B | 5 of 8 | 27.6 s |
| 400 HP/s | B | 8 of 8 | 16.7 s |

With these rules, the outcome flips between 200 and 250 HP/s per healer. Two things are worth noticing. First, near the threshold fights get very long. Healing does not add linearly to a side's strength; it trades against incoming focus damage, and when the two nearly balance, deaths almost stop. That is the stalemate PvP players complain about when healers are strong. Second, the result depends on the targeting rule. If side A kills the healers first, the flip point moves a long way. Lab 11 asks you to find out how far.

This gives a designer two levers against stalled PvP fights: lower healing in PvP only, or give attackers an effect that reduces the healing their target receives. In Lanchester terms, both push healers below the threshold. MMO307 covers split PvP and PvE tuning in detail ([MMO307 syllabus](../../MMO307-game-balance-ii-pvp-progression-and-endgame/syllabus.md)).

## 6. A checklist for group-combat design

When you design a mode where groups fight groups, answer these in writing before you tune any numbers.

1. **Which law do you want?** Decide whether headcount should win (square) or whether organization and position should be able to beat numbers (closer to linear).
2. **What sets the exponent?** List the rules that push toward each law: target caps, area damage, reachable targets per player, map chokepoints, targeting assistance.
3. **What is the snowball speed?** Compute `t_end` for your standard group size with one player down. If a single early death decides the fight within seconds, players will feel fights are decided at the first pick.
4. **Where is the healing threshold?** Find the healing throughput at which your standard fight stalls, and make sure healers sit below it in PvP.
5. **How will players exploit it?** If numbers count squared, expect blobs and zerging. If position counts, expect turtling at chokepoints. Plan content that punishes the exploit you do not want.

## In-class activity (25 minutes)

Pairs. Materials: the interactive, or a spreadsheet with the square-law formulas.

1. Your world-PvP zone often sees fights of 12 attackers against 9 defenders. Compute the strength ratio and the attackers' expected survivors. (5 min)
2. Design an "outnumbered" buff that lets 9 defenders tie 12 attackers. Express it as a percentage bonus to DPS and HP. (Hint: the buff has to cover the ratio of squares.) (5 min)
3. Now apply your same buff to a fight of 12 defenders against 12 attackers where the buff is wrongly triggered for one side. What happens? (5 min)
4. Propose a non-stat alternative that pulls the fight toward the linear law instead, such as a map feature or an area-damage rule, and state its cost to other kinds of play. (10 min)

Expected output: the numbers for steps 1 to 3, and a 100-word design note for step 4.

## Common misconceptions

- **"10 against 8 is a 25% advantage."** In aimed-fire combat it is a 56% advantage in fighting strength (`100 : 64`), and the winner loses 4 players, not 8.
- **"Better gear can make up for fewer players, point for point."** Gear multiplies DPS × HP once; numbers count squared. Offsetting 25% more players takes 25% more DPS and 25% more HP per player together.
- **"Area damage is the natural counter to blobs."** Only if it is uncapped or softly capped. With a hard target cap below the group size, area damage is aimed fire again and the square law holds.
- **"Healing adds to a side's strength like extra HP."** Healing trades against the focused damage rate, so it has a threshold. Below it, healers delay deaths. Near it, fights stall. Above it, the healing side stops losing players.

## Check yourself

1. Side A has 15 players, side B has 12, all identical with 100 DPS and 1,000 HP. Compute A's survivors under the square law and under the linear law.
2. A guild of 6 veterans with 1.5 times the DPS and 1.2 times the HP of ordinary players fights 8 ordinary players. Who wins under the square law, and by how much fighting strength?
3. In a game with uncapped area damage, 10 players fight 8. What does the linear law predict for survivors? Now the designer adds a 5-target cap. Which law applies, and why?
4. You want a 5-versus-5 mode where losing one player early is not decisive. Name two rule changes that move the mode toward the linear law, and one cost of each.

<details>
<summary>Answers</summary>

1. Square law: `sqrt(15² − 12²) = sqrt(225 − 144) = sqrt(81) = 9` survivors. Linear law: `15 − 12 = 3` survivors.
2. Veterans' per-player quality is `1.5 × 1.2 = 1.8`. Strength `1.8 × 6² = 64.8` against `1 × 8² = 64`. The veterans win narrowly, by about 1.3%. Two more ordinary players (10) would give 100 and swamp them.
3. Linear law: `10 − 8 = 2` survivors. With a 5-target cap, each area attack hits at most 5 players whatever the group size, so each attacker's kill rate stops growing with the enemy count once the enemy has more than 5 alive. That is aimed fire, so the square law applies while both sides are above 5, giving a bigger win for the 10.
4. Examples: uncapped or softly capped area damage (cost: stacking tightly becomes suicide and a few area specialists can dominate); longer time-to-kill so a numbers edge has time to be reversed by play (cost: slower, less punchy fights); objectives that require splitting up (cost: less direct teamfighting); chokepoints (cost: static fights). Any two with a real cost earn full credit.

</details>

## Lab hook

**Lab 11: Battle simulator and the exponent of your game.** You build a small group-combat simulator in a spreadsheet or Python, confirm the 10-versus-8 results above, measure which law your rules produce, and find the healing threshold with and without healer focus. See [`labs/lab11.md`](../labs/lab11.md). The simulator you build here becomes the core of the week 13 combat-simulator assignment.

## Sources

- Lanchester, F. W. (1916). *Aircraft in Warfare: The Dawn of the Fourth Arm*. Constable. Origin of the linear and square laws. Summary in Wikipedia, "Lanchester's laws" (checked 2026). https://en.wikipedia.org/wiki/Lanchester%27s_laws
- Engel, J. H. (1954). "A Verification of Lanchester's Law." *Journal of the Operations Research Society of America* 2(2), 163–171. Fit of the aimed-fire equations with reinforcements to Iwo Jima casualty data.
- Washburn, A. "Lanchester Systems." Naval Postgraduate School lecture notes. https://faculty.nps.edu/awashburn/Files/Notes/Lanchester.pdf
- Guild Wars 2 Wiki, "Area of effect" (current game, checked 2026). Most area skills affect at most 5 targets, chosen by proximity to the center; many melee attacks hit up to 3. https://wiki.guildwars2.com/wiki/Area_of_effect
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Chapter on combat and time-to-kill.
- All simulation tables (10 against 8 with focus and spread targeting, and with healers) come from this course's reference simulation with the rules stated in each section; they are not measurements of a shipped game.

## Interactive spec: examples/w11-lanchester-battle.html

**The one insight:** a group's fighting strength grows with the square of its size. Ten beat eight with six survivors, and eight need 56% more DPS × HP per player to tie. Secondary insight: the targeting rule (focus or spread) and the area-damage rule decide whether the square law holds.

**Layout.** Three panels. Mobile: stacked. Desktop (≥ 1024px): battlefield on top across the full width, the two charts side by side below.

1. **Battlefield.** Two groups of circles, side A on the left in one palette color and side B on the right in another. Each circle is a player and has a thin health ring. Dead players fade to an outline. Draw a faint line from each living attacker to its current target when there are 20 or fewer players per side. No game art.
2. **Alive over time.** Line chart, x = time in seconds, y = players alive. Discrete simulation as stepped lines (one per side). The continuous square-law solution as thin smooth lines behind them. A vertical marker at the end of the fight.
3. **Fighting strength.** Two horizontal bars showing `N² × DPS × HP` for each side at the start of the fight, normalized so the larger bar is full width. Label each bar with its value in units of "ordinary player²" (one ordinary player = 100 DPS × 1,000 HP = 1). Show the ratio, e.g. "1.56 : 1".

**Readout (always visible, copyable text).** Winner, survivors (discrete sim), survivors predicted by the square law, survivors predicted by the linear law, fight length (discrete), fight length predicted by `artanh(B₀/A₀)/k` when both sides have equal kill rates.

**Controls.**
- Side A size, 1 to 40, default 10. Side B size, 1 to 40, default 8.
- Side A DPS per player (50 to 300, step 5, default 100) and HP per player (500 to 3,000, step 50, default 1,000). Same for side B.
- Targeting for each side: "Focus" (default) or "Spread".
- Combat rule: "Aimed fire" (default), "Uncapped area fire", "Area fire, target cap 5".
- Healers (optional section, collapsed by default): number of side B players who are healers (0 to 4) and healing per healer in HP/s (0 to 500, step 10). Healers deal no damage and heal the lowest-health living ally. Checkbox "Side A kills healers first".
- Buttons "Fight", "Reset", and "Instant result" (runs the simulation without animation). Keyboard operable, visible focus.

**Simulation rules (discrete).**
- Time step `dt = 0.01` s. Each step, compute each side's total damage this step from its living damage dealers: `sum(DPS) × dt`.
- Aimed fire, Focus: all of a side's damage goes to the first living enemy in a fixed order (damage dealers first, healers last unless "kills healers first" is checked). Overkill damage is lost.
- Aimed fire, Spread: damage is divided equally among all living enemies.
- Uncapped area fire: each attacker's per-step damage `DPS × dt` is applied in full to every living enemy (so total damage scales with the enemy count). Area-fire damage uses a separate per-player area DPS equal to 10% of the DPS slider to keep fights watchable; label this in the UI.
- Area fire, target cap 5: as above, but each attacker's damage is applied only to up to 5 living enemies (the first 5 in order).
- Healing: after damage, each living healer adds `HPS × dt` to the lowest-health living ally, capped at max HP.
- The fight ends when one side has no living players, or at 300 s (show "stalemate").
- Deaths are applied simultaneously within a step, so equal forces can wipe each other.

**Continuous overlay.** Integrate `dA/dt = −β B`, `dB/dt = −α A` with `α = DPS_A / HP_B`, `β = DPS_B / HP_A` (Euler, `dt = 0.001`), stopping when either reaches 0. For "Uncapped area fire" use `dA/dt = −β' A B`, `dB/dt = −α' A B` with `α' = 0.1 × DPS_A / HP_B`. Hide the overlay when healers are present and label it "no closed form with healers".

**Test values (builder must reproduce).**
| A | B | Rule | Targeting A / B | Result |
|---|---|---|---|---|
| 10 | 8 | Aimed | Focus / Focus | A wins, 6 survivors, ≈ 10.5 s discrete; square law 6.00, 10.99 s |
| 10 | 8 | Aimed | Focus / Spread | A wins, 10 survivors, 8.0 s |
| 10 | 8 | Aimed | Spread / Spread | A wins, 10 survivors at 36% HP each, 8.0 s |
| 10 | 8 | Aimed | Spread / Focus | B wins, 8 survivors, ≈ 12.5 s |
| 15 | 12 | Aimed | Focus / Focus | A wins, square law predicts 9.00 |
| 8 | 8 | Aimed | Focus / Focus | mutual wipe |
| 10 | 8, B DPS 125 and HP 1,250 | Aimed | Focus / Focus | strength bars equal (100 : 100); near mutual wipe |
| 10 | 6 DPS + 2 healers at 150 HP/s | Aimed | Focus / Focus | A wins, 7 survivors, ≈ 16.2 s |
| 10 | 6 DPS + 2 healers at 250 HP/s | Aimed | Focus / Focus | B wins, 5 survivors, ≈ 27.6 s |

(Small differences of ±0.2 s from rounding are acceptable; survivor counts must match.)

**First screen.** Load at 10 against 8, aimed fire, focus on both sides, with the strength bars showing "100 : 64" and the readout already filled from an instant run. One-line caption: "25% more players, 56% more fighting strength."

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`, both color schemes, side colors also distinguished by shape (circles vs squares) for color-blind users. With reduced motion, "Fight" shows the final state and the full chart without animation.
