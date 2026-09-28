# MA102 · Week 05 — Variance and Standard Deviation: 'Swingy' Designs

**Why this matters:** Two weapons with the same expected damage can feel completely different, and one of them can even kill slower on average. Players call the difference "swingy" or "consistent". Variance is the number behind that word, and it is the dial you turn when a system feels unfair even though its averages are balanced.

**You will be able to:**
- Compute the variance, standard deviation and coefficient of variation of a discrete random variable.
- Compute the distribution of hits-to-kill for a weapon with crits against a fixed health pool, and explain why equal expected damage does not mean equal expected kill time.
- Predict how the spread of total damage shrinks as a fight gets longer, using the rule that variances of independent hits add.
- Design two crit configurations with the same average and a chosen difference in swinginess.

**Before class:** Schreiber, *Game Balance Concepts* (blog course, 2010), Level 5 "Probability and Randomness Gone Horribly Wrong", the parts on how players perceive randomness; Schreiber & Romero, *Game Balance* (2021), the chapter on probability, the sections on variance and on randomness and player perception.

**Prerequisites from earlier courses:** MA101 week 2 (linear functions) and week 4 (exponents and powers), see the [MA101 syllabus](../../MA101-mathematics-for-games-i-algebra-functions-trigon/syllabus.md). From this course, [week 4, expected value](w04-expected-value-comparing-weapons.md), and [week 3, the complement rule](w03-complement-rule-chance-of-at-least-one-drop.md).

**Interactive:** [Swing meter](../examples/w05-swing-meter.html) (built from the spec at the end of this lecture). Keep it open during section 2.

---

## 1. Averages hide the story

Last week you learned to rank weapons by expected damage per second. Here is a pair that the expected value cannot tell apart.

- **Steady Blade:** 20 damage per hit, every hit. No crits.
- **Gambler's Axe:** 16 damage per hit, with a 25% chance to crit for double (32).

Expected damage per hit for the Axe is 16 × (1 + 0.25 × 1) = 20. Same as the Blade. Same swing speed, too. By last week's rules they are identical.

Hand them to a group of playtesters and they will not describe them as identical. The Axe players will tell you about the fight where they crit three times in a row and the one where they never crit at all. The Blade players will say the Blade is "boring" or "reliable", depending on temperament. What they are describing is **spread**: how far individual outcomes land from the average. This lecture puts a number on spread and then shows the surprising part: spread combined with a health pool changes the *average* kill time too.

### Deviation, variance and standard deviation

Let `X` be a random variable with expected value `μ = E[X]` (μ is the Greek letter mu, the usual symbol for a mean).

The **deviation** of an outcome is how far it is from the mean: `x − μ`. For the Axe, a normal hit deviates by 16 − 20 = −4 and a crit by 32 − 20 = +12.

You cannot just average the deviations. They always average to zero, because the mean is exactly the balance point. So square them first (squares are never negative), then average. That average of squared deviations is the **variance**:

```
Var(X) = E[(X − μ)²] = Σ (x − μ)² × P(x)
```

An equivalent form is often faster to compute:

```
Var(X) = E[X²] − μ²
```

"The average of the squares minus the square of the average."

Variance is measured in squared units (damage squared), which is hard to picture. Take the square root to get back to damage. That is the **standard deviation**:

```
SD(X) = σ = √Var(X)
```

σ (sigma) is roughly "the typical distance of an outcome from the average". It is not the maximum distance, and it is not exactly the average distance, but for everyday design reasoning it is the number that answers "how far off should I expect to be?"

### Worked numbers for the two weapons

Steady Blade: every outcome is 20, every deviation is 0. `Var = 0`, `σ = 0`. No spread at all.

Gambler's Axe:

| Outcome | Probability | Damage x | Deviation x − 20 | Squared deviation | Probability × squared |
|---|---|---|---|---|---|
| Normal | 0.75 | 16 | −4 | 16 | 12 |
| Crit | 0.25 | 32 | +12 | 144 | 36 |
| **Total** | 1.00 | | | | **48** |

`Var = 48`, `σ = √48 = 6.93`.

Check with the shortcut: `E[X²] = 0.75 × 256 + 0.25 × 1024 = 192 + 256 = 448`, and `448 − 20² = 448 − 400 = 48`. Same answer.

### Relative spread: the coefficient of variation

A standard deviation of 6.93 means a lot on a 20-damage hit and very little on a 2,000-damage hit. To compare swinginess across systems of different scale, divide by the mean. The result is the **coefficient of variation**:

```
CV = σ / μ
```

For the Axe, CV = 6.93 / 20 = 0.346, or about 35%. This is the number I will use for "swinginess" in the rest of the lecture. A CV of 0 is perfectly consistent; a CV near 1 means outcomes routinely land a whole average away from the average.

### A formula for any crit

A hit that does base damage `b` normally and `m × b` on a crit with chance `c` has

```
μ  = b × (1 + c(m − 1))
σ² = b² × (m − 1)² × c(1 − c)
CV = (m − 1) × √(c(1 − c)) / (1 + c(m − 1))
```

You can derive the variance line from the table method. The term `c(1 − c)` is the variance of a single yes-or-no event with probability `c`. It is largest when `c = 0.5` and zero when `c = 0` or `c = 1`. So for a fixed multiplier, crits are swingiest at 50% chance and perfectly consistent at 100%, when every hit is a crit.

## 2. Worked example: same average, slower kill

### The hook

Competitive Pokémon players talk about damage "rolls". Since Generation III, every damage calculation multiplies by a random whole number from 85 to 100, then divides by 100. That gives 16 equally likely damage values for each attack. Community damage calculators such as Pokémon Showdown's list all 16 and report results like "guaranteed 2HKO" or "chance to OHKO". The average roll is 92.5%. But whether you knock out the opponent this turn depends on which roll you get, and one missed knockout can decide a match.

Take a simplified attack whose maximum roll would deal 110 damage to a target with exactly 100 HP. The average damage is 110 × 0.925 = 101.75, more than the target's health. Yet the attack only knocks out on rolls of 91 or higher (110 × 0.91 = 100.1). That is rolls 91 through 100, 10 of 16, a 62.5% chance. The average says "knockout". The roll says "about five times in eight". (Real Pokémon damage rounds down at several steps, so exact thresholds can differ by one roll; this simplified version keeps the arithmetic visible.)

The general lesson: **when an outcome depends on crossing a threshold, spread matters as much as the average**. Health pools are thresholds. So let us put the Steady Blade and the Gambler's Axe against a 100-HP enemy.

### The model

Each hit deals `b` damage, or `m × b` on a crit with chance `c`, independently of other hits. The enemy dies on the first hit where cumulative damage reaches `H`. After `n` hits containing `k` crits, total damage is

```
total(n, k) = b × (n + k(m − 1))
```

The number of hits to kill, `T`, is the first `n` with `total(n, k) ≥ H`. With `b = 16`, `m = 2`, `c = 0.25`, `H = 100`, total damage is `16 × (n + k)`, and the kill needs `n + k ≥ 7`, because 16 × 6 = 96 falls short and 16 × 7 = 112 does not.

The Steady Blade needs exactly 5 hits, every time: 5 × 20 = 100.

### Numbers you can check

For the Axe, work out the probability that the enemy is dead **by** hit `n`, then subtract to get the probability it dies **on** hit `n`.

- **By hit 3.** Even three crits give 16 × 6 = 96. Impossible.
- **By hit 4.** Needs at least 3 crits in 4 hits. Exactly 3 crits can happen in 4 arrangements (the normal hit can be any one of the four), each with probability 0.25³ × 0.75 = 0.01172, so 4 × 0.01172 = 0.04688. All 4 crits has probability 0.25⁴ = 0.00391. Total 0.05078.
- **By hit 5.** Needs at least 2 crits in 5 hits. Use the complement (week 3). Zero crits: 0.75⁵ = 0.23730. Exactly one crit: 5 arrangements × 0.25 × 0.75⁴ = 0.39551. So the probability of 2 or more is 1 − 0.23730 − 0.39551 = 0.36719.
- **By hit 6.** Needs at least 1 crit in 6 hits: 1 − 0.75⁶ = 1 − 0.17798 = 0.82202.
- **By hit 7.** Seven normal hits give 112. Certain.

| Hits to kill T | P(dead by hit T) | P(T exactly) | T × P |
|---|---|---|---|
| 4 | 0.0508 | 0.0508 | 0.203 |
| 5 | 0.3672 | 0.3164 | 1.582 |
| 6 | 0.8220 | 0.4548 | 2.729 |
| 7 | 1.0000 | 0.1780 | 1.246 |
| **Expected** | | 1.0000 | **5.76** |

The Axe kills in 5.76 hits on average. The Blade kills in 5.00. **Same expected damage per hit, 15% slower kills.**

Where did the damage go? Into **overkill**, damage dealt past zero health. The Blade's 100 damage lands exactly on 100 HP. The Axe usually finishes with some damage to spare: 112 on a seven-hit kill, or more after a crit. That surplus counts in the Axe's expected damage and does nothing to the enemy. Spread plus a threshold turned into a lower average kill rate.

The Axe also has spread in the kill time itself. Its hits-to-kill has a mean of 5.76 and a standard deviation of about 0.80 (you can verify with `E[T²] − 5.76²`), while the Blade's is 0. Sometimes the Axe kills in 4, beating the Blade; 18% of the time it needs 7.

### A visual you can move

Open the interactive. The left panel shows the damage of one hit for both weapons as a bar chart, with a vertical line at the shared mean. The right panel shows the distribution of hits-to-kill against a health pool you choose, with each weapon's mean marked. Start with the lecture values. Now drag the enemy HP slider from 100 down to 96. The Blade still needs 5 hits, but the Axe's mean drops to 4.96, so the swingy weapon is now slightly faster. Slide up to 112. The Blade needs 6 hits (120 damage, 8 of it overkill), while the Axe's mean stays at 5.76, because 112 is exactly seven normal Axe hits. Now the Axe wins by about a quarter of a hit. Whether variance helps or hurts depends on where the health pool sits relative to the hit sizes, and the interactive lets you see that curve directly.

Then switch the lower panel to "long fight". It plots the coefficient of variation of total damage against fight length in hits. The curve falls fast, and section 3 explains why.

### Cross-game recognition

**Dungeons & Dragons 5th edition.** The greatsword deals 2d6, average 7. The greataxe deals 1d12, average 6.5. Their variances differ a lot: one d12 has variance (12² − 1) / 12 = 11.92, σ = 3.45; two d6 have variance 2 × 35/12 = 5.83, σ = 2.42. The greataxe has nearly twice the variance for a slightly lower average. Players who pick the greataxe for "big hits" are choosing spread. Week 8 explains why sums of dice pile up in the middle, which is where the smaller variance comes from.

**Pokémon.** The 85 to 100 roll is a uniform whole number with 16 values. For evenly spaced whole numbers taking `N` values, the variance is `(N² − 1) / 12` in steps of 1. Here that is 255 / 12 = 21.25, so σ = 4.61 percentage points on a mean of 92.5, a CV of about 5%. Pokémon deliberately keeps damage spread small. Its big swings come from separate events such as crits and accuracy, where a single roll changes the result far more than the damage roll does.

**League of Legends.** With crit damage at 200% (patch V26.01 onward) and 50% crit chance, the per-hit CV from our formula is 1 × √0.25 / 1.5 = 0.33, the same as the Gambler's Axe. Riot kept the formula and changed the *randomness*. The League of Legends Wiki describes a pseudo-random algorithm that raises the crit probability after streaks of non-crits, which cuts the longest droughts and streaks while keeping the average. Week 10 builds this kind of system from scratch.

Three games, one quantity. Each designer decided how much spread to allow per hit and where to put it: in the damage roll (Pokémon, small), in the dice choice (D&D, left to the player), or in crits with the streaks trimmed (League).

### Eyes-open design judgment

Variance is neither good nor bad. It buys some things and costs others, and you should buy it on purpose.

- **Variance creates stories.** The fight where you crit three times in a row is the one you tell your friends about. A game with zero variance per hit has no such moments. If your combat has few other sources of surprise, some spread keeps it from feeling mechanical.
- **Variance near a threshold wastes damage.** As the worked example shows, when targets die in a handful of hits, swingy damage kills slower on average than steady damage with the same mean. If you balance weapons by expected DPS alone, the swingy weapon is secretly weaker against trash mobs and PvP targets, and secretly stronger nowhere. Test kill times, not only damage.
- **Short fights amplify spread; long fights erase it.** A raid boss taking thousands of hits averages out almost all per-hit variance (section 3). A PvP duel decided in five hits does not. The same crit build can feel fair in a raid and unfair in a duel. MMOs often answer this with different rules per mode, and that is a deliberate choice you should make, not an accident you discover.
- **Players tolerate variance better when they chose it.** A greataxe the player picked for big hits feels different from a random crit that decides a match against them. If you add spread, give players ways to opt in or to plan around it.
- **You can change spread without changing the average.** Section 4 shows how. That makes variance one of the few balance levers that does not touch the DPS spreadsheet at all.

### Check yourself (worked example)

1. Replace the Axe's crit chance with 50% and its base damage with `b` chosen so the mean stays 20. What is `b`? What is the per-hit CV?
2. Against a 32-HP enemy, how many hits does the Steady Blade need? What is the probability the original Gambler's Axe kills in one hit, and what is its expected number of hits?
3. A designer says "the Axe and Blade have the same DPS, so they are balanced." Give one situation where the Axe is better and one where it is worse, with numbers.

<details>
<summary>Answers</summary>

1. `b × (1 + 0.5) = 20`, so `b = 13.33`. CV = 1 × √(0.5 × 0.5) / 1.5 = 0.5 / 1.5 = 0.333. The CV is slightly lower than at 25% (0.346), even though 50% maximizes `c(1 − c)`, because the mean multiplier also grew.
2. The Blade needs 2 hits (40 damage). The Axe kills in one hit only on a crit (32 ≥ 32), probability 0.25. Otherwise the second hit always finishes it (16 + 16 = 32). Expected hits = 1 × 0.25 + 2 × 0.75 = 1.75, faster than the Blade's 2. Here the threshold sits exactly at a crit, so variance helps.
3. Better: the 32-HP enemy from question 2 (1.75 hits versus 2). Worse: the 100-HP enemy from the worked example (5.76 hits versus 5). The weapons are balanced in average damage, not in average kill time, and kill time is what players experience.

</details>

## 3. Variance of a whole fight

A single hit's spread is only half the story. Players feel the spread of **total damage over a fight**, and that behaves very differently.

**Variances of independent random variables add.** If `X` and `Y` are independent,

```
Var(X + Y) = Var(X) + Var(Y)
```

Unlike linearity of expectation, this one needs independence. If one hit's outcome changed the next hit's chances, as in League's pseudo-random crits, the rule breaks, and that is exactly how pseudo-random systems reduce spread.

For `n` independent hits, each with mean `μ` and variance `σ²`:

```
mean of total = n μ
Var of total  = n σ²
SD of total   = √n × σ
CV of total   = (√n × σ) / (n μ) = CV of one hit / √n
```

The mean grows like `n`. The standard deviation grows like `√n`, which is much slower. So the relative spread shrinks like `1 / √n`.

For the Gambler's Axe (μ = 20, σ² = 48):

| Hits in fight n | Mean total | SD of total | CV of total |
|---|---|---|---|
| 1 | 20 | 6.93 | 34.6% |
| 5 | 100 | 15.49 | 15.5% |
| 20 | 400 | 30.98 | 7.7% |
| 50 | 1,000 | 48.99 | 4.9% |
| 100 | 2,000 | 69.28 | 3.5% |

A five-hit PvP exchange has a 15% typical swing in total damage. A hundred-hit boss fight has 3.5%. Quadrupling the fight length halves the relative swing. This is the math behind the design rule "long fights are fair, short fights are swingy", and it is the reason MMO raid encounters can carry large crit multipliers that would be unbearable in a duel.

The `1 / √n` rule also explains a playtest trap you will meet in week 13: small samples are swingy for the same reason short fights are.

## 4. Tuning spread without touching the average

Because the mean of a crit hit depends on `c(m − 1)` only, any pair of crit chance and multiplier with the same product has the same average. Hold the mean multiplier at 1.25 and see what happens to swinginess:

| Crit chance c | Crit multiplier m | c(m − 1) | Mean multiplier | Per-hit CV |
|---|---|---|---|---|
| 100% | 1.25 | 0.25 | 1.25 | 0 |
| 50% | 1.5 | 0.25 | 1.25 | 0.200 |
| 25% | 2 | 0.25 | 1.25 | 0.346 |
| 12.5% | 3 | 0.25 | 1.25 | 0.529 |
| 6.25% | 5 | 0.25 | 1.25 | 0.775 |

Every row deals the same expected damage. The top row is a flat 25% damage bonus with no randomness. The bottom row is a rare, huge crit. Rare-and-big is the swingy end; frequent-and-small is the steady end.

This table is a design tool. If playtesters say crits feel "irrelevant", move down the table. If PvP players complain about one-shots, move up it. Neither change needs a new DPS balance pass.

A second tuning knob is **where** the randomness sits. Pokémon puts a small spread on every hit (the 85 to 100 roll) and bigger spread on rare events. Some games remove damage ranges entirely and keep only crits. Others roll damage ranges but no crits. The per-hit CV tells you the size of the spread; the fight length tells you how much of it players will notice.

## In-class activity (25 minutes)

Groups of three. Each group gets two d6 and one d12 (or a dice app) and a 30-HP target.

1. Weapon X deals 2d6 per hit. Weapon Y deals 1d12 per hit. Compute each weapon's mean and standard deviation per hit, and note that Y's mean is half a point lower (5 minutes).
2. Roll to kill the 30-HP target 10 times with each weapon. Record hits-to-kill each time (12 minutes).
3. Pool results across the class on the board. Compare average hits-to-kill and the range of hits-to-kill for X and Y.
4. Write two sentences: which weapon would you give a player who complains that fights "feel random"? Which would you give a player who wants "big moments"? Use the standard deviations in your answer.

Expected output: two means (7 and 6.5), two SDs (2.42 and 3.45), a class tally showing that 1d12 has more fights at both extremes, and a two-sentence recommendation. Keep the class tally; week 8 returns to it.

## Common misconceptions

- **"Same average means same balance."** Only when fights are long and there are no thresholds. Near a health threshold, spread changes the average kill time, as the Axe's 5.76 hits show.
- **"Standard deviation is the biggest possible miss from the average."** It is a typical distance. The Axe's crit lands 12 above the mean, farther than one σ (6.93).
- **"Variances always add."** Only for independent events. Pseudo-random crits, pity timers and anything with memory break the rule, often on purpose.
- **"Longer fights make crits matter less."** Crits contribute the same share of the average in a long fight. What shrinks is their share of the *spread*: the relative swing falls like `1 / √n`.

## Check yourself

1. A loot box gives 0 gold with probability 0.9 and 100 gold with probability 0.1. Compute the mean, variance and standard deviation of one opening. Then compute the mean and SD of the total gold from 25 openings.
2. Two crit builds both have mean multiplier 1.3: build P is 60% crit at ×1.5, build Q is 15% crit at ×3. Which is swingier per hit? Compute both CVs.
3. A duel lasts 9 hits; a raid pull lasts 144 hits. By what factor is the raid's CV of total damage smaller than the duel's, for the same weapon?

<details>
<summary>Answers</summary>

1. Mean = 10. `E[X²] = 0.1 × 10,000 = 1,000`, so Var = 1,000 − 100 = 900 and SD = 30. For 25 openings: mean 250, Var = 25 × 900 = 22,500, SD = 150. The CV drops from 3.0 for one opening to 0.6 for 25.
2. P: (0.5) × √(0.6 × 0.4) / 1.3 = 0.5 × 0.490 / 1.3 = 0.188. Q: (2) × √(0.15 × 0.85) / 1.3 = 2 × 0.357 / 1.3 = 0.549. Q is almost three times as swingy.
3. √(144 / 9) = √16 = 4. The raid's relative spread is one quarter of the duel's.

</details>

## Lab hook

**Lab 05: Swing and overkill** ([`labs/lab05.md`](../labs/lab05.md)). Extend your Lab 04 spreadsheet with per-hit variance and CV, then compute the hits-to-kill distribution for the Steady Blade and Gambler's Axe across enemy HP from 20 to 200 and plot the expected kill time for both. You will find the HP values where the swingy weapon wins and where it loses.

## Sources

- Bulbapedia, "Damage" (Pokémon, Generation III onward): the random factor is a whole number from 85 to 100, inclusive, divided by 100; Generations I and II used a different range. https://bulbapedia.bulbagarden.net/wiki/Damage
- Pokémon Showdown damage calculator (accessed September 2026): lists the 16 possible damage values per attack and reports knockout chances. https://calc.pokemonshowdown.com/
- Wizards of the Coast, *System Reference Document 5.1* (D&D 5th edition, 2016), Equipment chapter, weapons table: greatsword 2d6 slashing, greataxe 1d12 slashing.
- League of Legends Wiki, "Critical strike" (accessed September 2026): crit damage 200% from V26.01; crit chance uses a pseudo-random algorithm that raises the chance after non-crit streaks. https://wiki.leagueoflegends.com/en-us/Critical_strike
- Schreiber, I. (2010). *Game Balance Concepts*, Level 5, "Probability and Randomness Gone Horribly Wrong". https://gamebalanceconcepts.wordpress.com/
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.

## Interactive spec: examples/w05-swing-meter.html

**Purpose.** Show that two weapons with the same expected damage per hit can have different expected kill times, and that the relative spread of total damage shrinks like `1 / √n` as fights get longer.

**The one insight the visual must make obvious.** Equal mean damage does not mean equal mean kill time: overkill near a health threshold costs the swingy weapon, and the size of that cost depends on where the HP sits.

**Layout.** Two linked views on top, one switchable view below. Side by side at desktop, stacked at 390px.

- Top left, "One hit": bar chart of the per-hit damage distribution for both weapons (Steady: one bar at the mean; Swingy: two bars at `b` and `m × b` with heights `1 − c` and `c`). A vertical dashed line at the shared mean. Print mean, SD and CV for each weapon under the chart.
- Top right, "Hits to kill": grouped bar chart of `P(T = n)` for both weapons for `n` from 1 to the maximum possible. Mark each weapon's `E[T]` with a vertical line and print `E[T]` and `SD(T)` to two decimals. Show a one-line verdict: "Swingy kills X% slower" or "X% faster".
- Bottom, tab 1 "Kill time vs HP": x axis enemy HP from 10 to 300, y axis `E[T]`. Two lines: the Steady line is a staircase `ceil(H / μ)`; the Swingy line is smoother. Shade the regions where Swingy is faster. A dot follows the HP slider.
- Bottom, tab 2 "Long fight": x axis fight length `n` from 1 to 200 hits (log scale acceptable), y axis CV of total damage for the Swingy weapon. Print the table values at n = 1, 5, 20, 50, 100.

**Controls** (keyboard accessible, values visible):

- Crit chance `c`: 0% to 100%, step 1%, default 25%.
- Crit multiplier `m`: 1.0 to 5.0, step 0.05, default 2.0.
- Shared mean damage `μ`: fixed at 20 (display only). The Swingy weapon's base is recomputed as `b = μ / (1 + c(m − 1))`.
- Enemy HP `H`: 10 to 300, step 1, default 100.
- Tab toggle for the bottom view. Reset button.

**Formulas.**

- Steady: damage 20 per hit, `T = ceil(H / 20)`.
- Swingy per hit: mean `b(1 + c(m − 1))`, variance `b²(m − 1)²c(1 − c)`, CV as in the lecture.
- `P(T ≤ n) = Σ over k from 0 to n of C(n, k) c^k (1 − c)^(n − k) × [b(n + k(m − 1)) ≥ H]`, where the bracket is 1 when true, 0 otherwise. Use a tolerance of 1e-9 in the comparison. `P(T = n) = P(T ≤ n) − P(T ≤ n − 1)`. Stop when `P(T ≤ n) ≥ 1 − 1e-12`, or at `n = ceil(H / b)`, where it is certainly 1.
- `E[T] = Σ n P(T = n)`, `SD(T) = √(Σ n² P(T = n) − E[T]²)`.
- Long fight: CV of total over `n` hits = per-hit CV / `√n`.

**Test values.**

| c | m | H | b | P(T=4) | P(T=5) | P(T=6) | P(T=7) | Swingy E[T] | Steady T |
|---|---|---|---|---|---|---|---|---|---|
| 0.25 | 2.0 | 100 | 16 | 0.0508 | 0.3164 | 0.4548 | 0.1780 | 5.760 | 5 |
| 0.25 | 2.0 | 32 | 16 | — | — | — | — | 1.750 | 2 |
| 0.00 | any | 100 | 20 | 0 | 1 | 0 | 0 | 5.000 | 5 |

Per-hit values at defaults: mean 20, SD 6.93, CV 0.346. Long-fight CVs: n = 1: 0.346, 5: 0.155, 20: 0.077, 50: 0.049, 100: 0.035.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`, light and dark themes, reduced motion respected, no game art. Weapons are labeled "Steady" and "Swingy" in text; do not draw weapons.
