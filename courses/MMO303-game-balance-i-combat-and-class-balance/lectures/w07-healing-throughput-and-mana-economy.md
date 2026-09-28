# MMO303 · Week 07 — Healing Throughput and Mana Economy

**Why this matters:** A healer runs out of two things during a fight. They run out of time to cast, and they run out of mana. Which one runs out first depends on how long the fight is, and if you tune healing spells without knowing that, you will build encounters that one healer finds trivial and another finds impossible with the same gear.

**You will be able to:**
- Compute heal per second (HPS), mana per second (MPS) and heal per mana (HPM) for any healing spell, and the time a healer takes to run out of mana.
- Derive the sustainable HPS of a two-spell healer as a function of fight length, and locate the fight lengths where the binding constraint switches.
- Design a healer spell list on the efficient frontier and explain why a spell below the frontier is a dead button.
- Critique a regeneration rule (five-second rule, cooldown-based regen, flat regen) by predicting how it changes healer behaviour.

**Before class:** Schreiber & Romero, *Game Balance* (2021), chapter 8 (Resources) and chapter 10 (Combat); GD203 week 5 (DPS, burst and sustain).

**Prerequisites from earlier courses:** GD203 [week 4, time-to-kill and time-to-die](../../GD203-combat-and-progression-design/lectures/w04-time-to-kill-and-time-to-die.md) and [week 5, DPS, burst and sustain](../../GD203-combat-and-progression-design/lectures/w05-dps-burst-and-sustain.md). [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md). From this course, [week 2](w02-armor-and-damage-mitigation.md) (effective HP) and [week 3](w03-effective-hp-and-effective-dps.md) (effective HP and effective DPS).

**Interactive:** [Mana budget: spell plane and sustainable HPS](../examples/w07-mana-budget.html). Keep it open during section 2.

---

## 1. Healing is a rate problem with a fuel tank

In week 3 you met time-to-die (TTD): how long a character lasts under a stream of damage. Written with effective health (EHP) and damage taken per second (DTPS):

```
TTD = EHP / DTPS
```

Healing enters this formula as a rate that fights the damage rate. If a healer restores `HPS` health per second on the target, the target's health drops at `DTPS − HPS`, so

```
TTD = EHP / (DTPS − HPS)      when HPS < DTPS
TTD = infinite                when HPS ≥ DTPS
```

That second line is the healer's whole job. While healing keeps up with damage, the tank never dies. When it falls short, even by a little, the tank dies on a clock. A 20,000 EHP tank taking 1,000 DTPS dies in 20 seconds with no healer. With a healer doing 900 HPS the tank lasts 20,000 / 100 = 200 seconds. The healer did not need to match the damage exactly to change the outcome by a factor of ten.

So far healing looks like DPS pointed the other way. It is not, because healers spend a pool of fuel. Most MMO healers pay for spells with mana, a resource with a maximum (the pool) and a refill rate (regeneration). Damage dealers in many games also spend a resource, but a DPS player who runs dry does less damage and the fight takes longer. A healer who runs dry stops healing, and the group dies. That asymmetry is why mana economy is a healer design problem first.

Three rates describe every healing spell. Define them once and use them for the rest of the lecture:

- **HPS (heal per second)** is healing divided by cast time. It measures throughput, how fast the spell turns casting time into health.
- **MPS (mana per second)** is mana cost divided by cast time. It measures how fast the spell burns the tank of fuel.
- **HPM (heal per mana)** is healing divided by mana cost. It measures efficiency, how much health you get out of the fuel.

Notice that `HPS = HPM × MPS`. A spell can be fast because it is efficient or because it burns mana quickly. Players often treat "big heal" and "good heal" as the same thing. They are different axes, and a good healer kit gives the player a real choice between them.

One more term. **Overhealing** is healing that lands on a target who is already at full health. It restores nothing. A 2,000-point heal on a target missing 1,200 health overheals by 800, so its effective HPM is 1,200 divided by the mana cost, not 2,000. Healers pick spells partly to fit the size of the hole, which is why big slow heals are riskier than they look on a tooltip.

## 2. Worked example: the healer's two budgets

### The hook: healers who cast weaker spells on purpose

In classic World of Warcraft (the original 2004 game, and the Classic servers that recreate it), every healing spell came in ranks. A level 60 priest knew the rank 1 heal they learned early and several stronger ranks learned later. Experienced raid healers often cast a lower rank on purpose. This was called downranking. A lower rank healed for less but cost much less mana, and with +healing gear it could heal very efficiently. Healers downranked because long raid fights ran them out of mana before they ran out of casting time.

Blizzard treated this as a balance problem. In a November 2006 post ahead of The Burning Crusade, a Blizzard representative said players were using low ranks and +healing gear to heal almost indefinitely, and announced that low ranks would get only a fraction of the +healing bonus, scaled by how far the rank's level trailed the caster's level. Spell ranks were later removed from the game altogether.

Why would a player ever choose the smaller heal? Because the question "which heal is better?" has no answer until you say how long the fight lasts.

### The model

Give a healer a mana pool `M`, a regeneration rate `r` (mana per second), and two spells. Call the slow efficient one Mend and the fast expensive one Surge. For each spell `i` you know its heal `H_i`, cost `C_i` and cast time `t_i`, so you know its three rates:

```
HPS_i = H_i / t_i       MPS_i = C_i / t_i       HPM_i = H_i / C_i
```

The healer casts without pause for a fight of length `T`. The only question is what fraction `f` of the casting time goes to Surge, with the rest going to Mend.

Over the whole fight, the healer may spend at most the starting pool plus everything regenerated. Divide that by `T` and you get a **mana budget per second**:

```
B(T) = M / T + r
```

Casting a mix costs `(1 − f) × MPS_Mend + f × MPS_Surge` mana per second, and that must fit inside `B(T)`. Throughput is the same mix of HPS. Maximise throughput subject to the budget and you get three regions:

```
Region 1 (short fight, B ≥ MPS_Surge):
    f = 1,  HPS = HPS_Surge

Region 2 (middle, MPS_Mend ≤ B < MPS_Surge):
    f = (B − MPS_Mend) / (MPS_Surge − MPS_Mend)
    HPS = HPS_Mend + f × (HPS_Surge − HPS_Mend)

Region 3 (long fight, B < MPS_Mend):
    cast Mend only, and only a fraction B / MPS_Mend of the time
    HPS = B × HPM_Mend
```

Look at region 3. When the fight is long, healing output equals mana income times the efficiency of the best spell per mana. Cast speed has dropped out of the formula. As `T` grows without limit, `B` shrinks to `r`, and the healer's long-run output settles at `r × HPM_Mend`.

Look at region 2 as well. Each second of casting you move from Mend to Surge buys `HPS_Surge − HPS_Mend` extra healing for `MPS_Surge − MPS_Mend` extra mana. That ratio is the **marginal HPM** of the upgrade, and it is usually far worse than either spell's own HPM. Fast heals are expensive in a way their tooltip does not show.

### Numbers you can check

Use these values for a generic healer. They are invented for teaching, so every figure is checkable by hand.

| Spell | Heal | Cost | Cast time | HPS | MPS | HPM |
|---|---|---|---|---|---|---|
| Mend | 2,000 | 250 | 2.5 s | 800 | 100 | 8 |
| Surge | 1,500 | 375 | 1.5 s | 1,000 | 250 | 4 |

Pool `M = 10,000`, regeneration `r = 20` mana per second.

Two quick facts first. Spamming Surge burns 250 mana per second and regains 20, so the healer runs out of mana (goes OOM, "out of mana") after 10,000 / 230 = 43.5 seconds. Spamming Mend lasts 10,000 / 80 = 125 seconds. Those two times are the region boundaries.

Marginal HPM of switching from Mend to Surge: (1,000 − 800) / (250 − 100) = 200 / 150 = 1.33 healing per mana. Surge on its own heals 4 per mana, but the extra 200 HPS it gives you over Mend costs mana at a rate of 1.33, six times worse than Mend's 8.

Now the sustainable HPS at several fight lengths:

| Fight length T | Budget B = M/T + r | Region | Surge share f | Sustainable HPS |
|---|---|---|---|---|
| 30 s | 353.3 | 1 | 1.00 | 1,000.0 |
| 60 s | 186.7 | 2 | 0.578 | 915.6 |
| 90 s | 131.1 | 2 | 0.207 | 841.5 |
| 120 s | 103.3 | 2 | 0.022 | 804.4 |
| 180 s | 75.6 | 3 | 0 | 604.4 |
| 300 s | 53.3 | 3 | 0 | 426.7 |
| 600 s | 36.7 | 3 | 0 | 293.3 |
| very long | 20.0 | 3 | 0 | 160.0 |

Check the 60-second row yourself. `B = 10,000 / 60 + 20 = 186.7`. That is between 100 and 250, so region 2. `f = (186.7 − 100) / 150 = 0.578`. `HPS = 800 + 0.578 × 200 = 915.6`.

Read the table from top to bottom. For fights under 43.5 seconds, the healer's limit is casting time and Surge is the right button. Between 43.5 and 125 seconds, the healer blends. Past 125 seconds, the limit is mana, the healer casts only Mend, and even Mend has to pause. Output keeps falling as fights get longer, toward 160 HPS, which is just `20 × 8`.

### The design consequence: the healer's clock

Encounter designers set damage. Suppose a boss deals 700 DTPS to the tank after mitigation. How long can this healer keep up? Solve `HPS(T) = 700`. At 125 seconds the healer still does 800, so the answer is in region 3: `8 × B = 700`, so `B = 87.5`, so `M / T = 67.5`, so `T = 148` seconds. Past about two and a half minutes the tank starts losing health and dies on the TTD clock from section 1.

This is a hidden enrage timer. The boss has no timer on it, but the group's mana economy gives it one. Every raid encounter in a mana-based game has this clock whether the designer drew it or not. Better to draw it on purpose.

### A visual the student can move

Open the [mana budget interactive](../examples/w07-mana-budget.html). The left view plots each spell as a point on a plane: MPS across, HPS up. The budget line `B(T)` is a vertical line you drag with the fight-length slider. The healer can reach any point on the segment between Mend and Surge that lies left of the budget line, and the best reachable point is marked.

The right view plots sustainable HPS against fight length, from 10 seconds to 10 minutes, with the same marked point. Drag the slider from 30 to 300 seconds. On the left, the budget line sweeps across the Surge point, then the Mend point, and the best point slides down the segment and then down toward the origin. On the right, the curve holds flat, bends, and then decays. The same numbers, two views. The first one shows why the curve on the second bends where it does.

The "Add third spell" control drops in a spell you define. If it lands above the Mend-Surge segment, the frontier changes shape. If it lands below, the healer never casts it in any fight length.

### Cross-game recognition

Healer mana systems look different across games. Rewrite each one into `M`, `r` and the spell rates, and they turn into the same model.

**Classic World of Warcraft: the five-second rule.** In classic WoW, a character's regeneration from the Spirit stat stopped for five seconds after they spent mana. Gear with the MP5 stat (mana per five seconds) kept regenerating regardless. Before patch 1.4.0, regeneration stopped while casting. The rule was removed in patch 4.0.1. In model terms, the rule makes `r` depend on how often you cast. A healer who casts continuously gets only the MP5 part of `r`. A healer who pauses gets Spirit regeneration too. That rewards the gaps region 3 already asks for, so the rule deepens the gap between long-fight and short-fight play. Downranking was a way to move a spell up the HPM axis, and the Burning Crusade penalty moved it back down.

**Final Fantasy XIV: fixed pool, cooldown regen.** Since patch 5.0 (Shadowbringers, 2019), every job's maximum MP is fixed at 10,000, and the Piety stat raises MP regeneration instead of the pool. So `M` is the same for every healer and gear moves only `r`. The role action Lucid Dreaming restores 550 MP every three seconds for 21 seconds, 3,850 MP in all, on a 60-second recast (values as of patch 6.1). Averaged over its recast that is 3,850 / 60 = 64.2 extra MP per second while it is used on cooldown. A cooldown that refills a resource is just a lumpy term added to `r`. It changes the long-fight plateau and leaves the short-fight plateau alone, because short fights never hit the mana constraint.

**Any energy or stamina bar.** Put an action game's stamina system or a rogue-style energy bar into the same form. Those bars usually have a small `M` and a large `r`, so `B(T)` is close to `r` after only a few seconds. That is the model's region 3 almost from the start. Such systems play as rate-limited rather than pool-limited, and players never plan a whole fight's spend. A mana healer has a large `M` relative to `r`, so fight length matters and players plan. Choosing the ratio `M / r` chooses which kind of resource game you are making.

The first move with any new game is the same as with armor in week 2: find `M`, find `r`, compute HPM and MPS for each spell, and ask where the budget line falls for a typical fight.

### Eyes-open design judgment

- **Short fights reward throughput, long fights reward efficiency.** If most of your content is 60-second dungeon pulls, your HPM tuning barely matters and HPS decides everything. If raid bosses last eight minutes, HPS barely matters. Tune for the fight lengths players actually meet, and look at your telemetry for them.
- **A spell on the frontier is a decision, and a spell off it is a trap.** The frontier is the upper edge of the region you can reach by mixing spells (the "upper convex hull" of the spell points in the MPS-HPS plane). Spells on it get cast in some fight length. A spell below it is never optimal and turns into a newcomer trap.
- **Regeneration rules shape moment-to-moment play.** The five-second rule taught healers to stop casting. Cooldown regen teaches them to plan around a timer. Flat regen asks nothing. Pick the behaviour you want.
- **Mana pools hide an enrage timer.** Every change to boss damage, fight length, healer `M` or `r` moves it. Compute it for each encounter instead of discovering it in testing.
- **Large pools make healers conservative early.** When running dry late costs the group, healers hoard, and fights feel slow at the start. Some designs hand back mana on specific events to push healers to spend.

## 3. Where the efficient frontier comes from

With two spells, the healer mixes along a straight segment. With more spells, the reachable region is the area under the upper edge of all the spell points. That edge is the **efficient frontier**, and it has a simple rule. Walking along it from left (cheap) to right (expensive), the slope must fall at every point. Each step right buys HPS at a worse marginal HPM than the step before.

Try it with a third spell, Quick: heals 900 for 150 mana in 1.0 second. Its rates are HPS 900, MPS 150, HPM 6.

| Segment | Extra HPS | Extra MPS | Marginal HPM |
|---|---|---|---|
| Mend to Quick | 100 | 50 | 2.0 |
| Quick to Surge | 100 | 100 | 1.0 |
| Mend to Surge (without Quick) | 200 | 150 | 1.33 |

The slope falls from 2.0 to 1.0, so Quick sits on the frontier. At MPS 150 the old Mend-Surge segment only reached `800 + 1.33 × 50 = 866.7` HPS. Quick reaches 900. Adding Quick raised the healer's output for every fight length whose budget falls between 100 and 250 mana per second. At the 90-second fight (`B = 131.1`), the healer now blends Mend and Quick for `800 + 2.0 × 31.1 = 862.2` HPS instead of 841.5.

Now try a spell called Flash: heals 1,000 for 300 mana in 1.25 seconds. HPS 800, MPS 240, HPM 3.3. It has Mend's throughput at more than double the mana rate. It sits far below the frontier and no fight length ever makes it right. A new player will cast it because the name sounds fast.

This is the healer version of the cost curves in Schreiber and Romero's transitive mechanics chapter. Every spell has a price (mana per second) and a benefit (healing per second), and a spell below the curve is overpriced.

## 4. Effective healing: overheal, smart heals and the real HPM

The model so far assumes every point of healing is useful. Real healing is not, for three reasons.

**Overhealing.** Damage arrives in lumps. A big heal that lands after a small hit wastes most of itself. If a healer's Mend overheals by 30% on average, its effective HPM is `8 × 0.7 = 5.6`, and its effective HPS is 560. Big slow heals overheal more than small fast ones because they commit to a size before the damage is known. This is part of why the fast spell survives in players' kits even when the model says Mend is more efficient.

**Healing over time (HoT).** A HoT heals in ticks. It overheals less on a target taking steady damage and more on a target who is already full. It also frees the healer's cast time, which the two-budget model counts as spare throughput.

**Absorption shields.** A shield that absorbs the next `X` damage never overheals in the usual sense, because it waits for damage. But if the shield expires unused it is wasted mana. The designer's choice of expiry time sets how much a shield is worth.

The practical rule: measure effective HPS from combat logs, not raw HPS. Your balance spreadsheet should carry an overheal factor per spell. Expect it to vary by role and encounter, because a raid-wide pulse of damage and a single tank hit create different overheal patterns.

## 5. Healing in the holy trinity

Week 5 set up the three roles. Healing throughput ties them together.

The tank's EHP sets how much damage each hit takes out of a healer's budget. Week 2 showed that armor multiplies EHP. It also multiplies healing. A tank with 50% mitigation takes half the damage, so every heal is worth twice as many raw damage points absorbed. Healing and mitigation stack as multipliers on TTD.

DPS sets fight length. If the group's damage dealers kill the boss 20% faster, `T` drops 20%, `B(T)` rises, and the healer moves up the curve in the table. Weak DPS makes a healer's job harder for reasons that have nothing to do with healing gear. Healers notice this even when they cannot name it.

The encounter sets DTPS and its shape. A steady stream of damage lets healers use efficient spells. Spikes, where 5,000 damage lands in one second after a quiet period, force throughput spells, because a tank with 4,000 health left cannot wait for a 2.5-second cast. Spiky damage pushes healers to the right side of the frontier and drains mana faster. The same average DTPS can be easy or brutal depending on how it is spread over time. Week 13's combat simulator will let you test both shapes against the same kit.

## In-class activity (25 minutes)

In pairs, design a three-spell healer kit for a raid boss that deals 650 DTPS to the tank for a 4-minute fight.

1. Choose `M` and `r`. Justify the ratio `M / r` in one sentence.
2. Design three spells with heal, cost and cast time. Plot them on paper in the MPS-HPS plane and draw the frontier. All three must be on it.
3. Compute the sustainable HPS at 60, 120 and 240 seconds. Does the healer keep up with 650 DTPS for the full fight? If not, find the time the hidden enrage clock starts.
4. Swap kits with another pair. Find the fight length at which their kit's weakest spell stops being cast, and whether any spell is never cast at all.

Expected output: one sheet per pair with the plot, the three HPS values and the enrage time, if any.

## Common misconceptions

- **"The spell with the biggest number is the best heal."** Size and speed are throughput. Efficiency is a separate axis. The best spell depends on fight length, and in long fights the most efficient spell wins even if it is the smallest.
- **"Surge heals 4 per mana, so switching to it costs 4 per mana."** The switch trades Mend for Surge, so it costs the marginal rate, 1.33 per mana in our example. Marginal HPM is the number that decides the mix.
- **"More regeneration always helps the healer."** Regeneration only helps once the budget binds. In fights shorter than the pool-limited time (43.5 seconds for Surge in our example), extra `r` changes nothing.
- **"If average healing matches average damage, the tank is safe."** Only if damage arrives smoothly. Spiky damage forces throughput spells, and overheal raises the mana cost of every point of useful healing.

## Check yourself

1. A healer has 8,000 mana, regenerates 10 mana per second, and has one heal: 1,800 healing for 300 mana, 2-second cast. How long can they cast without pause before running out of mana? What is their long-run HPS once the pool is empty?
2. Using the Mend and Surge healer from section 2 (`M = 10,000`, `r = 20`), what is the sustainable HPS for a 240-second fight? The tank takes 550 DTPS. Does the healer keep up, and if not, how much extra regeneration per second would close the gap?
3. A designer adds Flash (1,000 healing, 300 mana, 1.25 s) to the Mend and Surge kit. Compute its HPS and MPS, and use the frontier to say whether any fight length makes it worth casting.
4. A patch cuts every boss's health by 25%, and DPS is unchanged. Which healers benefit more, those whose output is limited by casting time or those limited by mana? Use `B(T)` to explain.

<details>
<summary>Answers</summary>

1. MPS is 300 / 2 = 150. Net drain is 150 − 10 = 140 per second, so the pool lasts 8,000 / 140 = 57.1 seconds. HPM is 1,800 / 300 = 6, so once empty the healer sustains `10 × 6 = 60` HPS.
2. `B = 10,000 / 240 + 20 = 41.7 + 20 = 61.7`. That is below Mend's MPS of 100, so region 3. HPS is `8 × 61.7 = 493.3`. The tank needs 550, so the healer falls short by 56.7 HPS. They need `B = 550 / 8 = 68.75`, which is 7.08 more mana per second of regeneration.
3. Flash has HPS 1,000 / 1.25 = 800 and MPS 300 / 1.25 = 240. It matches Mend's HPS while burning 2.4 times the mana. Any budget that can afford 240 MPS can instead afford a Mend-Surge mix near 240 MPS with about `800 + 1.33 × 140 = 986.7` HPS. Flash is below the frontier at every fight length and is never worth casting.
4. Fights get shorter, so `T` falls and `M / T` rises, raising `B`. Healers who were already limited by casting time (region 1) gain nothing from a bigger budget. Mana-limited healers (regions 2 and 3) move up the curve. The patch helps mana-limited healers more.

</details>

## Lab hook

**Lab 07 (Healer mana budget).** Build a spreadsheet that takes a healer's `M`, `r` and spell list, draws the efficient frontier, and outputs sustainable HPS for fight lengths from 10 seconds to 10 minutes. Then use it to tune a three-spell kit so every spell is cast somewhere in a 1-to-6-minute range. See [`labs/lab07.md`](../labs/lab07.md).

## Sources

- Warcraft Wiki, "Five second rule" (accessed 2026). Spirit regeneration paused for five seconds after spending mana in classic-era World of Warcraft; MP5 unaffected; before patch 1.4.0 regeneration stopped while casting; removed in patch 4.0.1.
- Blizzard Entertainment forum post, "Change to Coefficient Bonuses on Spells", 7 November 2006, archived on BlueTracker. Announces reduced +healing bonuses for low spell ranks ahead of The Burning Crusade, explaining that downranking let healers heal almost indefinitely. Later wiki sources report a different constant in the final formula; this lecture relies only on the direction of the change.
- Final Fantasy XIV Online Wiki (consolegameswiki), "MP" (accessed 2026). Maximum MP fixed at 10,000 for all jobs from patch 5.0; Piety changed from raising maximum MP to raising regeneration. Also Square Enix, "Patch 5.0 Notes", The Lodestone.
- Final Fantasy XIV Online Wiki, "Lucid Dreaming" (accessed 2026). Potency 55 (since patch 6.0), 550 MP per 3-second tick for 21 seconds (3,850 MP total), 60-second recast, level 14 since patch 6.1.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Chapter 8 (Resources), chapter 10 (Combat), and the chapter on transitive mechanics and cost curves.
- All spell values in the worked example (Mend, Surge, Quick, Flash) are invented for teaching.

## Interactive spec: examples/w07-mana-budget.html

**The one insight:** a healer's output is capped by casting time in short fights and by mana in long fights, and the switch between them happens at fight lengths you can compute. The left view shows why the right view's curve bends where it does.

**Layout.** Two linked views side by side on desktop, stacked on mobile (left view first). A number panel under them.

**Left view: the spell plane.**
- x-axis MPS (0 to 400), y-axis HPS (0 to 1,200).
- Each spell is a labeled dot. Draw the efficient frontier as a polyline through the upper convex hull of the spell dots plus the origin (0, 0). Draw spells below the frontier as hollow grey dots with the label "never cast".
- A vertical dashed line at `x = B(T)`, labeled "budget B = M/T + r".
- A filled marker at the best reachable point: the frontier's height at `x = min(B, max MPS on frontier)`. If B is below the lowest MPS on the frontier, the marker moves along the straight line from the origin to that spell (idle part of the time), height `B × HPM` of the leftmost frontier spell.

**Right view: sustainable HPS vs fight length.**
- x-axis fight length T from 10 s to 600 s (linear), y-axis HPS 0 to 1,200.
- Plot `HPS(T)` computed as below at 1-second steps. Mark the current T with the same filled marker. Draw vertical dotted lines at each region boundary, where `B(T)` equals the MPS of a frontier spell, labeled with T to one decimal.
- Optional horizontal line for incoming DTPS (control below). Where the curve crosses it, show "healer falls behind at T = ... s".

**Controls (all keyboard accessible, update both views immediately):**
- Fight length T slider, 10 to 600 s, step 1, default 60.
- Mana pool M, 2,000 to 30,000, step 500, default 10,000.
- Regeneration r, 0 to 100 mana/s, step 1, default 20.
- Spell table with editable heal, cost, cast time for Mend (2,000 / 250 / 2.5) and Surge (1,500 / 375 / 1.5).
- "Add third spell" toggle with editable heal, cost, cast time, default Quick (900 / 150 / 1.0). A preset button "Flash" sets it to 1,000 / 300 / 1.25.
- DTPS line toggle and slider, 0 to 1,200, default off, 700 when turned on.
- Overheal slider, 0 to 50%, default 0. Multiplies every spell's heal (and so HPS and HPM) by `1 − overheal`.

**Formulas.**
- `HPS_i = H_i / t_i`, `MPS_i = C_i / t_i`, `HPM_i = H_i / C_i`.
- `B(T) = M / T + r`.
- Frontier: sort spells by MPS, take the upper convex hull starting from the origin. Let the hull vertices be `(m_0, h_0) = (0, 0), (m_1, h_1), ..., (m_k, h_k)`.
- `HPS(T)`: if `B ≥ m_k`, `h_k`. Else find `j` with `m_j ≤ B < m_{j+1}` and interpolate linearly, `h_j + (B − m_j) × (h_{j+1} − h_j) / (m_{j+1} − m_j)`. Interpolating between the origin and the first spell gives the idle case `B × HPM_1`.

**Number panel** (live, copyable): `B(T)`, active region, fraction of time on each spell, sustainable HPS, time to OOM for each spell cast alone (`M / (MPS_i − r)` or "never" when `MPS_i ≤ r`), marginal HPM of each frontier segment, and the DTPS crossing time when that line is on.

**Test values (defaults, two spells, overheal 0):**
- T = 30: B = 353.3, HPS 1,000.0.
- T = 60: B = 186.7, Surge share 0.578, HPS 915.6.
- T = 90: B = 131.1, HPS 841.5.
- T = 120: HPS 804.4. T = 180: HPS 604.4. T = 300: HPS 426.7. T = 600: HPS 293.3.
- Region boundaries at T = 43.5 s and T = 125.0 s. Time to OOM: Surge 43.5 s, Mend 125.0 s.
- DTPS 700: healer falls behind at T = 148.1 s.
- With Quick added: T = 90 gives HPS 862.2. With Flash instead, Flash is drawn as "never cast" and HPS values match the two-spell case.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`. Frontier and curve in the primary color, budget line dashed. All values in the number panel also appear as text for screen readers. No game art or logos.
