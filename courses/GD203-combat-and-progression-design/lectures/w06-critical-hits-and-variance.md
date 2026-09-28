# GD203 · Week 06 — Critical hits and variance

**Why this matters:** Critical hits are the most common source of randomness in combat, and the one players argue about most. Two builds with the same average damage can kill at different speeds, and whether a crit feels exciting or unfair depends on numbers you choose. This week you learn to choose them.

**You will be able to:**
- Compute the expected damage and the standard deviation of a hit with crit chance `c` and crit multiplier `m`.
- Derive the distribution of hits-to-kill for a crit build and predict whether crits speed up or slow down the average kill against a given target.
- Compute how variance shrinks with the number of hits in a fight, and use that to decide where randomness belongs in a design.
- Price crit chance against crit damage and explain why they reinforce each other.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapter on probability and randomness; Schreiber, *Game Balance Concepts*, level 4 and level 5 (probability and randomness), as a refresher. Official TF2 Wiki, "Critical hits."

**Prerequisites from earlier courses:** Expected value from [MA102 week 4](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md), variance from [MA102 week 5](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w05-variance-and-swingy-designs.md), the binomial distribution ("crits over a fight") from [MA102 week 6](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w06-binomial-crits-over-a-fight.md), and pseudo-random distribution from [MA102 week 10](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w10-pseudo-random-distribution-and-pity-timers.md). Breakpoints and hits-to-kill from [GD203 week 4](w04-time-to-kill-and-time-to-die.md). Fight length from [GD203 week 5](w05-dps-burst-and-sustain.md).

**Interactive:** [w06-crit-hits-to-kill.html](../examples/w06-crit-hits-to-kill.html) (specified at the end of this lecture). Keep it open during section 2.

---

## 1. The average and the spread

A **critical hit** (crit) is a hit that deals more than normal damage. In most games a crit happens at random with **crit chance** `c` and multiplies damage by the **crit multiplier** `m`. With base damage `d`, one hit deals `d` with probability `1 − c` and `m × d` with probability `c`.

MA102 gave you the two numbers that describe a random quantity. The **expected value** is the long-run average. The **standard deviation** measures how far typical results land from that average. For one hit:

```
expected damage   E = d × (1 + c × (m − 1))
variance          V = d² × c × (1 − c) × (m − 1)²
std deviation     σ = d × (m − 1) × sqrt(c × (1 − c))
```

- `d` is base damage per hit.
- `c` is crit chance, from 0 to 1.
- `m` is the crit multiplier. A crit that deals double damage has `m = 2`.

The term `1 + c × (m − 1)` is the **expected crit multiplier**. It is the factor by which crits raise average damage. With `c = 0.25` and `m = 2`, it is `1.25`. Crits add 25% to average damage.

To compare randomness across weapons of different sizes, divide the standard deviation by the mean. That ratio is the **coefficient of variation (CV)**:

```
CV (one hit) = σ / E = (m − 1) × sqrt(c × (1 − c)) / (1 + c × (m − 1))
```

A CV of 0.35 means a typical hit lands about 35% away from the average. A CV of 0.05 means hits are nearly predictable.

That is the whole toolkit. The rest of the lecture shows that the average alone misleads you about the thing players feel, which is how many hits a kill takes.

## 2. Worked example: same average damage, different kill speed

### The hook

In Team Fortress 2, most weapons have a random chance to crit. The official wiki gives a base chance of 2%, rising to at most 8% for a player who has dealt a lot of damage in the last 20 seconds. A crit deals three times base damage and ignores the usual distance falloff and random spread.

Two percent sounds tiny. Yet random crits are one of the most debated mechanics in the game, and the community's standard competitive format switches them off entirely, while keeping non-random crits such as Sniper headshots.

Why would a 2% effect matter so much? Put week 4's numbers next to it. A base rocket deals 90. A crit rocket deals 270. A Soldier has 200 health, which normally takes three rockets. A crit rocket kills a Soldier in one. A 2% roll does not add 4% to average damage in the way players experience it. It turns a three-hit fight into a one-hit fight. Randomness at low hit counts hits the staircase, and the staircase is what players feel.

This worked example asks a sharper question. Suppose two builds deal exactly the same average damage per hit. Do they kill at the same speed on average?

### The model

Build A deals a fixed `d₀` per hit, no crits. Build B has crits, with its base damage lowered so its average matches A:

```
d_B = d₀ / (1 + c × (m − 1))
```

Build B kills within `n` hits if the damage from `n` hits, with `k` of them crits, reaches the target's health `H`:

```
d_B × (n + k × (m − 1)) ≥ H
```

The number of crits `k` in `n` hits follows the binomial distribution you met in MA102 week 6:

```
P(k crits in n hits) = C(n, k) × c^k × (1 − c)^(n − k)
```

So the probability that B has killed by hit `n` is the sum of `P(k)` over every `k` large enough to satisfy the damage inequality. The probability that B kills on exactly hit `n` is the difference between "killed by `n`" and "killed by `n − 1`."

### Numbers you can check

Build A: 25 damage, no crits. Build B: 25% crit chance, 2× multiplier, so `d_B = 25 / 1.25 = 20`. Both average exactly 25 per hit.

For B, each crit adds one extra 20, so B kills within `n` hits when `20 × (n + k) ≥ H`, that is when `n + k ≥ H / 20`.

**Target with 80 health.** Build A needs `ceil(80 / 25) = 4` hits, always. It deals 100, wasting 20 on overkill. Build B needs `n + k ≥ 4`.

- Kill by hit 2 needs both hits to crit: `0.25² = 0.0625`.
- Kill by hit 3 needs at least one crit in three: `1 − 0.75³ = 0.578`.
- Kill by hit 4 is certain, since four normal hits deal 80.

| Hits | Build A | Build B |
|---|---|---|
| 2 | 0% | 6.3% |
| 3 | 0% | 51.6% |
| 4 | 100% | 42.2% |
| Average hits | 4.00 | 3.36 |

Build B kills 16% faster on average with the same average damage.

**Target with 100 health.** Build A needs exactly 4 hits and wastes nothing. Build B needs `n + k ≥ 5`.

- Kill by hit 3 needs at least two crits in three: `3 × 0.25² × 0.75 + 0.25³ = 0.156`.
- Kill by hit 4 needs at least one crit in four: `1 − 0.75⁴ = 0.684`.
- Kill by hit 5 is certain.

| Hits | Build A | Build B |
|---|---|---|
| 3 | 0% | 15.6% |
| 4 | 100% | 52.7% |
| 5 | 0% | 31.6% |
| Average hits | 4.00 | 4.16 |

Now Build B is 4% slower on average, and in almost a third of fights it needs a whole extra hit.

Same weapons, same average damage, opposite answers. The difference is where the target's health sits relative to A's breakpoints. At 80 health, A is just past a breakpoint and wastes a fifth of its last hit. B's variance lets it sometimes skip that wasted hit. At 100 health, A lands exactly on a breakpoint with zero waste, and B's variance can only make things worse on the downside than it makes them better on the upside.

Sweep the target's health from 50 to 150 and the pattern is regular:

| Target health | A average hits | B average hits | Faster on average |
|---|---|---|---|
| 55 | 3 | 2.56 | B |
| 75 | 3 | 3.36 | A |
| 80 | 4 | 3.36 | B |
| 100 | 4 | 4.16 | A |
| 105 | 5 | 4.96 | B |
| 125 | 5 | 5.76 | A |
| 130 | 6 | 5.76 | B |

**Crits speed up the average kill when the fixed build sits just past a breakpoint, and slow it down when the fixed build sits exactly on one.** Averaged over many target health values, the two builds come out close, but for any single enemy they do not.

### See it move

Open `w06-crit-hits-to-kill.html`. The left panel is a histogram of hits-to-kill for Build B, with Build A's single fixed bar drawn as an outline beside it. The right panel plots average hits-to-kill against target health. Build A is week 4's staircase. Build B is a softer, rounder staircase that weaves across it.

Drag the health slider from 75 to 80. A's bar jumps from 3 to 4 and B's histogram barely moves, so B goes from behind to ahead. Now raise crit chance to 50% while keeping the average fixed. B's histogram widens and its curve on the right flattens toward a smooth line. Finally, set crit chance to 2% and the multiplier to 3 (TF2's numbers). B's histogram is almost a single bar, with a tiny sliver one or two hits to the left. That sliver is the TF2 complaint. It is rare, and when it happens it is a whole hit or more.

### Cross-game recognition

Every crit system can be written as `(c, m)` and put through the same formulas.

| Game (version) | Crit chance c | Multiplier m | Expected multiplier | CV per hit |
|---|---|---|---|---|
| Team Fortress 2 (current, ranged, base) | 0.02 | 3 | 1.04 | 0.27 |
| Pokémon (Gen VII onward, stage 0) | 1/24 | 1.5 | 1.02 | 0.10 |
| League of Legends (V26.01 onward, 25% from items) | 0.25 | 2.0 | 1.25 | 0.35 |
| Minecraft Java (jump attack) | player-controlled | 1.5 | — | — |

**Team Fortress 2.** A low chance with a large multiplier. The average gain is small (4%), but the CV per hit is high because the rare outcome is so large. That is the recipe for "rare and decisive," and it explains both the excitement and the complaint.

**Pokémon.** Since Generation VI, crits deal 1.5× rather than the 2× of earlier generations, and since Generation VII the base chance is 1 in 24 (it was 1 in 16 in Generation VI). Both changes shrink the crit's contribution to variance. Pokémon also rolls a random multiplier between 85% and 100% on every hit, so damage calculators report "percentage chance to 2HKO" rather than one number. That is our hits-to-kill distribution, computed for every matchup by the community.

**League of Legends.** Crit chance is bought through items and caps at 100%. Crit damage was 200% from launch, was cut to 175% in patch V10.23, and returned to 200% in V26.01. The wiki notes that League's crit rolls are pseudo-random, with a hidden modifier that makes a crit more likely the longer you go without one. That is a deliberate cut to the variance of `k`, the number of crits in `n` hits, without changing its average. You studied the same idea as pseudo-random distribution in MA102 week 10.

**Minecraft (Java Edition).** A critical hit deals 1.5× damage, but it is not random. It happens when the player attacks while falling, so it is a skill-and-timing crit. The multiplier is there, the randomness is not. Minecraft converts variance into a player decision (jump before you swing) that costs time and positioning.

Four games, one formula. Each design team chose a point on two dials, how often and how big. They also chose whether chance or the player decides.

### Design judgment

- **Variance lives at low hit counts.** A crit that changes a 3-hit kill to a 2-hit kill is a big event. The same crit in a 300-hit boss fight averages out. Section 3 puts a number on this.
- **Know where your breakpoints are.** If key enemies sit right on a breakpoint for a no-crit build, adding crits at equal average damage makes kills slower on average. If they sit just past one, crits make kills faster. You can tune this deliberately.
- **Rare and big feels decisive. Common and small feels like texture.** Low `c` with high `m` produces memorable swings and complaints about unfairness. High `c` with low `m` produces steady damage with a little sparkle. Pick the feel you want, then check the CV.
- **Randomness is a gift to the underdog and a tax on the skilled.** In a fight the better player usually wins, variance gives the weaker player some wins. That can be good in casual play and frustrating in competition. TF2's competitive format removed random crits. Minecraft made crits skill-based. League smoothed them. Each is a stance on this trade.
- **Show the player what happened.** Big crit numbers, sounds and screen effects tell the player why a fight ended early. Unexplained variance feels like a bug.

## 3. Variance shrinks with fight length

Over a fight of `n` independent hits, the average total damage grows as `n`, but the standard deviation grows only as `sqrt(n)`. So the CV of total fight damage falls as `1 / sqrt(n)`:

```
CV (n hits) = CV (one hit) / sqrt(n)
```

For a 25% crit chance at 2×, one hit has a CV of about 0.35:

| Hits in the fight | CV of total damage | Typical swing around the average |
|---|---|---|
| 1 | 0.346 | ±35% |
| 4 | 0.173 | ±17% |
| 16 | 0.087 | ±9% |
| 100 | 0.035 | ±3.5% |

Quadruple the fight length and you halve the randomness. A 100-hit fight is almost deterministic even with a 25% crit chance.

This gives you a design rule. Put randomness where you want surprise, and remove it where you want skill to decide. Short PvP exchanges and one-shot mechanics are low-`n`, so crits there are loud. Long raid fights are high-`n`, so crits there mostly raise the average and barely affect the outcome. A designer who wants a raid to have tension from randomness must add it some other way, such as random boss abilities, because crits will not do it.

It also explains a common playtest surprise. A crit-heavy build that looks fine in a boss-fight simulation can feel unfair in duels, because the simulation is high-`n` and the duel is low-`n`. Always test variance at the hit counts the player will actually see.

## 4. Crit chance and crit damage as stats

Many games let players buy crit chance and crit damage separately. The expected multiplier `1 + c × (m − 1)` tells you how to price them.

The gain from a little more crit chance is proportional to `(m − 1)`. The gain from a little more crit multiplier is proportional to `c`:

```
gain from +Δc   = Δc × (m − 1)
gain from +Δm   = Δm × c
```

The two stats reinforce each other. Crit chance is worth more when crits are bigger, and crit damage is worth more when crits are more frequent. They are worth the same per point when `c = m − 1`.

A worked comparison with `c = 0.30` and `m = 1.5`, so the expected multiplier is `1.15`:

- +5 points of crit chance: `0.05 × 0.5 = 0.025`, raising the multiplier to 1.175 (+2.2%).
- +10 points of crit damage: `0.10 × 0.30 = 0.030`, raising it to 1.180 (+2.6%).

Crit damage wins here. Change the starting point to `c = 0.10` and the same items give +0.025 and +0.010, and crit chance wins. The value of a stat depends on the build it goes into. [Week 9](w09-item-budgets-and-stat-weights.md) turns this into item budgets and stat weights.

Two structural cautions.

**Caps create cliffs.** If crit chance caps at 100% (League does this), then at the cap every further point of crit chance is worth zero and crit damage becomes plain damage. Builds rush to the cap and stop. You saw the same pattern with linear armor caps in [week 3](w03-mitigation-curves-and-effective-hp.md).

**Multiplying stats snowball.** Because the two crit stats multiply, a build that stacks both grows faster than a build that stacks either. That is the positive feedback loop from GD102. If your game lets players stack both without limit, the crit build will outgrow everything else late in progression. Many designers give crit damage a fixed value, or tie both stats to the same budget, to keep the product under control.

## 5. Other ways to shape variance

Crits are only one way to add randomness to damage. You have other tools, and each changes the distribution differently.

- **Damage ranges.** Each hit rolls uniformly between a minimum and maximum, as in Pokémon's 85-100% roll. This adds small, frequent variance with no rare spikes. It blurs breakpoints evenly.
- **Pseudo-random crits.** Keep the average crit rate and cut the streaks, as League does. This lowers the variance of crits over a fight without touching expected damage.
- **Skill crits.** Make the crit depend on player action, as Minecraft does. The multiplier stays, the randomness goes, and the decision becomes part of the skill ceiling.
- **Guaranteed crits on a counter.** "Every fourth hit crits." Same expected multiplier as `c = 0.25`, zero randomness, fully predictable breakpoints. Players can plan around it, which some games want and some do not.
- **Turn it off.** TF2's competitive format does exactly this for random crits.

Choose by asking two questions. At the hit counts your players see, how large is the CV you are adding? And does the player's skill or the dice decide who benefits?

## In-class activity (25 minutes)

Pairs. You are tuning a dagger for a small online RPG. The dagger averages 30 damage per hit. Common enemies have 60, 90, 100 and 150 health.

1. Version A: 30 damage, no crits. Compute hits-to-kill for each enemy.
2. Version B: 20% crit chance at 2.5×. Compute the base damage that keeps the average at 30.
3. For each enemy, compute B's probability of killing in fewer hits than A and in more hits than A. Use the binomial method from section 2 (or the interactive to check).
4. Decide which version to ship. Your design goal is "daggers feel spiky in PvP but fair against quest mobs." Justify it in three sentences using CV and hit counts.
5. Propose one change (to `c`, `m`, or an enemy's health) that makes B at least as fast as A on average against the 90-health enemy.

Expected output: a table with A's hits and B's distribution for four enemies, a recommendation, and the proposed change with its new numbers.

## Common misconceptions

- **"Same average damage means same kill speed."** Only for long fights. At low hit counts, crits can make the average kill faster or slower, depending on where the target's health sits relative to breakpoints.
- **"A 2% crit chance barely matters."** It barely changes average damage. With a large multiplier and low hit counts, it changes the outcome of the fights where it happens, and players remember those fights.
- **"Crits just add damage, so they're a DPS stat."** They add damage and variance. The variance matters as much as the damage in short fights and almost not at all in long ones.
- **"Crit chance and crit damage are separate stats with separate values."** Their gains multiply. Each one's value depends on the other's current level.

## Check yourself

1. A weapon has 40 base damage, 20% crit chance and a 2.5× multiplier. What is its expected damage per hit? What is the CV of one hit?
2. Build A deals 30 per hit with no crits. Build B has a 20% chance to deal 2× and the same average damage. Against a 120-health target, what is B's probability of killing in 3 hits? Of needing 5? Is B faster or slower on average than A?
3. A build has 30% crit chance and a 1.5× multiplier. Which item adds more expected damage, +5 points of crit chance or +10 points of crit damage? At what crit chance would the two items be equal?
4. A fight takes 9 hits and a single hit has a CV of 0.30. What is the CV of the fight's total damage? How many hits would the fight need to bring it to 0.05?

<details>
<summary>Answers</summary>

1. `E = 40 × (1 + 0.2 × 1.5) = 52`. `σ = 40 × 1.5 × sqrt(0.2 × 0.8) = 60 × 0.4 = 24`. CV `= 24 / 52 ≈ 0.46`.
2. B's base damage is `30 / 1.2 = 25`, and each crit adds another 25. B kills within `n` hits when `n + k ≥ 120 / 25 = 4.8`, so `n + k ≥ 5`. In 3 hits it needs at least 2 crits: `3 × 0.2² × 0.8 + 0.2³ = 0.104`. Killing by hit 4 needs at least 1 crit in 4: `1 − 0.8⁴ = 0.590`. So B needs 5 hits with probability `0.8⁴ = 0.410`. Average hits `= 3 × 0.104 + 4 × 0.486 + 5 × 0.410 ≈ 4.31`, slower than A's 4. The target sits exactly on A's breakpoint (`4 × 30 = 120`).
3. Crit chance: `0.05 × 0.5 = 0.025`. Crit damage: `0.10 × 0.30 = 0.030`. Crit damage wins. The items are equal when `0.05 × 0.5 = 0.10 × c`, that is at `c = 0.25`.
4. `0.30 / sqrt(9) = 0.10`. For 0.05 you need `sqrt(n) = 6`, so 36 hits.

</details>

## Lab / assignment hook

**[Lab 06: Crits, breakpoints and Monte Carlo](../labs/lab06.md).** Compute exact hits-to-kill distributions with the binomial method, check them against a 10,000-fight spreadsheet simulation, and redesign a crit system to hit a target CV at the hit counts your game uses. It extends your breakpoint table from Lab 04.

## Sources

- Official TF2 Wiki, "Critical hits" (current): base random crit chance 2% for most weapons, scaling to a maximum of 8% with damage dealt in the last 20 seconds; crits deal 3× base damage and ignore distance falloff and random spread; melee crit chance 15% base. https://wiki.teamfortress.com/wiki/Critical_hits
- Official TF2 Wiki, "Standard community competitive format": random crits disabled, non-random crits kept. https://wiki.teamfortress.com/wiki/Standard_community_competitive_format
- Official TF2 Wiki, "Rocket Launcher" and "Health": 90 base damage per rocket; Soldier 200 base health. https://wiki.teamfortress.com/wiki/Rocket_Launcher
- Pokémon Showdown, "Critical hit" article: multiplier 2× in Generations II-V (Generation I applied it through the level term, close to 2× at level 100) and 1.5× from Generation VI; stage-0 rate 1/16 in Generation VI and 1/24 from Generation VII. https://dex.pokemonshowdown.com/articles/criticalhit.md
- Smogon Forums, "Pokémon Damage Calculator Tutorial": the 16 random rolls from 85% to 100%, and KO-chance reporting. https://www.smogon.com/forums/threads/pok%C3%A9mon-damage-calculator-tutorial.3700836/
- League of Legends Wiki, "Critical strike": 200% crit damage from launch, 175% from V10.23, 200% again from V26.01; pseudo-random crit rolls; crit chance cap of 100%. https://wiki.leagueoflegends.com/en-us/Critical_strike
- Minecraft Wiki, "Sword" (Java Edition): critical hits deal 1.5× and occur when the player attacks while falling. https://minecraft.wiki/w/Sword
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.
- Schreiber, I. (2010). *Game Balance Concepts*, levels 4-5. https://gamebalanceconcepts.wordpress.com/

## Interactive spec: examples/w06-crit-hits-to-kill.html

**The one insight the visual must make obvious:** two builds with the same average damage per hit do not kill at the same average speed. Crits help when the fixed build is just past a breakpoint and hurt when it sits exactly on one.

**Layout.** Two linked panels, side by side on desktop, stacked on mobile.

**Left panel: "How many hits did it take?"**
- Histogram of Build B's hits-to-kill probability, bars in blood red, labelled with percentages (1 decimal).
- Build A's single outcome (probability 100%) drawn as a steel outline bar at its hit count.
- Vertical markers for A's hits and B's mean hits (ochre dashed), both labelled.

**Right panel: "Average hits to kill vs target health."**
- x axis: target health H from `d₀` to `8 × d₀`.
- Build A: `ceil(H / d₀)` as a steel staircase.
- Build B: exact mean hits-to-kill (computed as below) as a blood-red line, evaluated at every integer H.
- Shade regions where B is below A (B faster) in moss, and where B is above A in blood red at low opacity.
- Cursor at current H.

**Model (exact, no simulation).**
- Inputs: average damage per hit `d₀`, crit chance `c`, crit multiplier `m`, target health `H`.
- Build A deals `d₀` per hit. Build B base damage `d_B = d₀ / (1 + c × (m − 1))`.
- `P_by(n) = Σ_{k=0..n} C(n,k) c^k (1 − c)^(n−k)` over all `k` with `d_B × (n + k × (m − 1)) ≥ H − 1e-9`.
- `P_exact(n) = P_by(n) − P_by(n − 1)`, `P_by(0) = 0`. Iterate `n` up to `ceil(H / d_B)` (which always has `P_by = 1`).
- Mean hits `= Σ n × P_exact(n)`.
- Also show the probabilities that B is faster than A, same as A, and slower than A.
- Per-hit CV `= (m − 1) × sqrt(c(1 − c)) / (1 + c(m − 1))`, and fight CV at A's hit count `= CV / sqrt(hits_A)`.

**Controls.** Sliders plus numeric inputs: `d₀` (1-200, default 25), `c` (0-1, step 0.005, default 0.25), `m` (1-5, step 0.05, default 2), `H` (1-1,000, default 80). A "keep average fixed" note beside `c` and `m` (always on; B's base damage is shown and updates). Presets:
- "Just past a breakpoint" (d₀ 25, c 0.25, m 2, H 80).
- "Exactly on a breakpoint" (same, H 100).
- "TF2-style" (d₀ 90, c 0.02, m 3, H 200).
- "Pokémon-style crit" (d₀ 30, c 1/24, m 1.5, H 100).

**Readouts:** d_B (3 decimals), A hits, B distribution table, B mean (4 decimals), P(B faster / same / slower), per-hit CV (3 decimals), fight CV.

**Test values (must match exactly, 4 decimals).**
| Input | A hits | B distribution | B mean |
|---|---|---|---|
| d₀ 25, c 0.25, m 2, H 80 | 4 | 2: 0.0625, 3: 0.5156, 4: 0.4219 | 3.3594 |
| d₀ 25, c 0.25, m 2, H 100 | 4 | 3: 0.1563, 4: 0.5273, 5: 0.3164 | 4.1602 |
| d₀ 25, c 0.25, m 2, H 105 | 5 | 3: 0.0156, 4: 0.2461, 5: 0.5010, 6: 0.2373 | 4.9600 |
| d₀ 25, c 0.25, m 2, H 55 | 3 | 2: 0.4375, 3: 0.5625 | 2.5625 |
| d₀ 30, c 0.2, m 2, H 120 | 4 | 3: 0.1040, 4: 0.4864, 5: 0.4096 | 4.3056 |
Per-hit CV for c 0.25, m 2: 0.346. For c 0.02, m 3: 0.269.

**First screen:** "Just past a breakpoint" preset, with a caption: "Same average damage. With crits: 3.36 hits. Without: 4." One chip toggles to "Exactly on a breakpoint" so the reversal is one click away.

**Style:** program palette; Build A in steel, Build B in blood red, means in ochre, "B faster" regions in moss. No game art or logos. Respect `prefers-reduced-motion`.
