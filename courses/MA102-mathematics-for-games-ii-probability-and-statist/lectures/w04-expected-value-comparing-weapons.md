# MA102 · Week 04 — Expected value: comparing weapons

**Why this matters:** Every time a player asks "which weapon is better?", they are asking for an average over outcomes they cannot predict one swing at a time. Expected value is the tool that answers that question, and it is also the number your game prints on the tooltip, so you need to know what it includes and what it quietly leaves out.

**You will be able to:**
- Compute the expected value of a discrete random variable from an outcome table.
- Derive expected damage per second for a weapon from damage range, speed, miss chance, crit chance and crit multiplier.
- Find the break-even stat value at which two weapons have equal expected damage.
- Critique a tooltip number by listing which random factors it averages and which it ignores.

**Before class:** Schreiber, *Game Balance Concepts* (blog course, 2010), Level 4 "Probability and Randomness"; Schreiber & Romero, *Game Balance* (2021), the chapter on probability, the sections on expected value.

**Prerequisites from earlier courses:** MA101 [week 2, linear functions and rates](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md) and [week 6, rational functions](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w06-rational-functions-and-asymptotes.md). From this course, [week 1, sample spaces](w01-sample-spaces-and-events.md), [week 2, independence](w02-independent-events-and-the-gamblers-fallacy.md) and [week 3, the complement rule](w03-complement-rule-chance-of-at-least-one-drop.md).

**Interactive:** [w04-expected-dps.html](../examples/w04-expected-dps.html) (built from the spec at the end of this lecture). Keep it open during section 2.

---

## 1. The number on the tooltip is already an average

In classic World of Warcraft, the two-handed axe Arcanite Reaper lists "153 - 256 Damage", "Speed 3.80" and, underneath, "(53.8 damage per second)". No single swing ever does 53.8 damage per second. A swing does some whole number between 153 and 256, and swings arrive every 3.8 seconds. So where does 53.8 come from?

Try it yourself. The middle of the damage range is (153 + 256) / 2 = 204.5. Divide by the swing time: 204.5 / 3.8 = 53.8. The tooltip is showing you the **average damage per swing, spread over the time between swings**. That is an expected value, printed on the item so players can compare a slow axe with a fast sword without doing algebra.

That is a design decision. Blizzard chose one number to summarize a random process, and players spent years comparing weapons by it. This lecture teaches you to compute that number, to extend it to the things the tooltip leaves out (misses and critical hits), and to spot when ranking weapons by it gives the wrong answer.

### Random variables

A **random variable** is a number whose value depends on the outcome of a random process. "The damage of the next swing" is a random variable. So is "the face of a d6" and "the gold dropped by the next goblin". We write random variables with capital letters, like `X`, and the values they can take with lowercase, like `x`.

A random variable has a **distribution**: the list of values it can take and the probability of each. For a fair d6 the distribution is six values, 1 through 6, each with probability 1/6. In week 1 you listed sample spaces; a distribution is the same idea after you have attached a number to each outcome.

### Expected value

The **expected value** of `X`, written `E[X]` and read "the expectation of X", is the probability-weighted average of its values:

```
E[X] = x1 × P(x1) + x2 × P(x2) + ... + xn × P(xn)
```

Every value gets multiplied by how likely it is, then everything is added up.

For a d6:

```
E[X] = 1(1/6) + 2(1/6) + 3(1/6) + 4(1/6) + 5(1/6) + 6(1/6) = 21/6 = 3.5
```

Two things about this result deserve attention.

First, 3.5 is not a face on the die. The expected value does not have to be a possible outcome. It is the **long-run average**: roll the die 10,000 times, add the results, divide by 10,000, and you will land very close to 3.5. That long-run reading is the one designers care about. It tells you what happens across thousands of swings, kills or loot rolls, which is the scale an MMO lives at.

Second, when the values are evenly spaced whole numbers from `a` to `b`, each equally likely, the expected value is simply the midpoint:

```
E[X] = (a + b) / 2
```

That is why the WoW tooltip can compute average damage by averaging minimum and maximum. It assumes every integer in the range is equally likely. (A uniform range is the common implementation; if a game weighted the middle of the range, the midpoint rule would still hold as long as the weighting is symmetric.)

### Expected value per second

A weapon has two random-ish properties: damage per swing and swings per second. If the swing time `s` is fixed, the expected damage per second is

```
expected DPS = E[damage per swing] / s
```

The Arcanite Reaper computation is exactly this formula with `E[damage per swing] = 204.5` and `s = 3.8`.

## 2. Worked example: tooltip DPS versus expected DPS

### The hook

The Arcanite Reaper's 53.8 is honest about the weapon. It says nothing about the person holding it. A real swing can miss. A real swing can crit. Those chances come from the character, not the item, so the tooltip leaves them out. And that means two weapons can rank one way on the tooltip and the other way in a fight.

Here is a pair of invented weapons for an invented MMO. Every number is chosen to be easy to check by hand.

| Weapon | Damage | Speed | Special |
|---|---|---|---|
| Iron Maul | 90 to 150 | 3.0 s | none |
| Keen Rapier | 30 to 42 | 1.0 s | +25% crit chance while equipped |

Tooltip DPS: the Maul's average is (90 + 150) / 2 = 120, so 120 / 3.0 = **40.0**. The Rapier's average is (30 + 42) / 2 = 36, so 36 / 1.0 = **36.0**. The tooltip says the Maul wins by 4 DPS.

Now give both to the same character. Against the target we care about, this character misses 10% of swings, has a 5% base crit chance, and crits deal double damage.

### The model

Every swing lands in exactly one of three outcomes: a miss, a normal hit or a crit. Name the symbols once:

- `q` is the miss chance (0.10 here).
- `c` is the crit chance on a swing that does not miss (0.05 for the Maul, 0.05 + 0.25 = 0.30 for the Rapier).
- `m` is the crit multiplier (2 here).
- `D` is the average rolled damage, the midpoint of the range.
- `s` is the swing time in seconds.

The outcome table for one swing is

| Outcome | Probability | Damage |
|---|---|---|
| Miss | `q` | 0 |
| Normal hit | `(1 − q)(1 − c)` | `D` |
| Crit | `(1 − q) c` | `m × D` |

The three probabilities add to 1, which is your first sanity check whenever you build a table like this.

Multiply each damage by its probability and add:

```
E[damage per swing] = (1 − q)(1 − c) D + (1 − q) c m D
                    = (1 − q) × D × (1 + c(m − 1))

expected DPS = (1 − q) × D × (1 + c(m − 1)) / s
```

Read the final formula as three multipliers applied to the tooltip DPS `D / s`:

- `(1 − q)` is the hit multiplier. Missing 10% of the time keeps 90% of the damage.
- `1 + c(m − 1)` is the crit multiplier. Each crit adds `m − 1` extra copies of a normal hit, and crits happen a fraction `c` of the time.
- `D / s` is what the tooltip prints.

### Numbers you can check

Iron Maul, outcome by outcome:

| Outcome | Probability | Damage | Probability × damage |
|---|---|---|---|
| Miss | 0.10 | 0 | 0 |
| Normal hit | 0.9 × 0.95 = 0.855 | 120 | 102.6 |
| Crit | 0.9 × 0.05 = 0.045 | 240 | 10.8 |
| **Total** | 1.000 | | **113.4** |

Expected DPS = 113.4 / 3.0 = **37.8**.

Keen Rapier:

| Outcome | Probability | Damage | Probability × damage |
|---|---|---|---|
| Miss | 0.10 | 0 | 0 |
| Normal hit | 0.9 × 0.70 = 0.63 | 36 | 22.68 |
| Crit | 0.9 × 0.30 = 0.27 | 72 | 19.44 |
| **Total** | 1.00 | | **42.12** |

Expected DPS = 42.12 / 1.0 = **42.12**.

The ranking flipped. The Maul led by 4.0 on the tooltip and trails by 4.3 in the fight. The shortcut formula gives the same answers: for the Maul, 0.9 × 120 × 1.05 / 3 = 37.8; for the Rapier, 0.9 × 36 × 1.30 / 1 = 42.12.

Notice what caused the flip. Both weapons lost the same 10% to misses, so misses cannot change the order. The crit multiplier is where they differ: 1.05 for the Maul, 1.30 for the Rapier. The Rapier's special adds 25 percentage points of crit, which at `m = 2` lifts its crit multiplier from 1.05 to 1.30, about 24% more damage. That is far more than the 10% tooltip gap.

### The break-even point

A designer rarely wants to know only who wins. You want to know **by how much, and where the lines cross**, because that is the number you can tune. Hold the Maul fixed at 37.8 and let the Rapier's total crit chance `c` vary:

```
0.9 × 36 × (1 + c) / 1.0 = 37.8
32.4 × (1 + c) = 37.8
1 + c = 1.1667
c = 0.1667
```

The Rapier ties the Maul when its total crit chance is 16.7%, which means its special only needs to grant about +11.7%. At +25% it is overbudget.

| Rapier total crit chance | Rapier expected DPS | Maul expected DPS | Leader |
|---|---|---|---|
| 5% | 34.02 | 37.80 | Maul |
| 10% | 35.64 | 37.80 | Maul |
| 15% | 37.26 | 37.80 | Maul |
| 20% | 38.88 | 37.80 | Rapier |
| 25% | 40.50 | 37.80 | Rapier |
| 30% | 42.12 | 37.80 | Rapier |
| 40% | 45.36 | 37.80 | Rapier |

The Rapier column climbs by exactly 1.62 DPS per 5 points of crit. Expected DPS is a **linear function** of crit chance, the same straight-line shape you met in [MA101 week 2](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md). Straight lines are easy to tune: one slope, one intercept, one crossing point.

### A visual you can move

Open the interactive. The left panel shows two pairs of bars: tooltip DPS and expected DPS for each weapon. The right panel plots expected DPS against the Rapier's crit bonus as two lines, a flat one for the Maul and a rising one for the Rapier, with the crossing point marked. Drag the crit bonus slider and watch the left panel's ranking flip exactly when the slider passes the crossing on the right. Then change the character's base crit chance. Both weapons gain the same number of crit points, but not the same percentage of damage. One extra point lifts the Maul's crit multiplier from 1.05 to 1.06, about 0.95%, and the Rapier's from 1.30 to 1.31, about 0.77%. The Maul gains proportionally more, so the crossing moves slightly to the right. Finally drag the miss chance: both bars shrink by the same fraction and the crossing does not move at all. That last behavior is the formula telling you that a shared multiplier cannot change a ranking.

### Cross-game recognition

The same three-multiplier structure appears in games that look nothing alike. Rewrite each into `hit multiplier × average × crit multiplier` and you see it is one idea.

**Dungeons & Dragons 5th edition.** The System Reference Document prints an average next to every monster's damage dice, in the form "7 (2d6)". The 7 is an expected value: a d6 averages 3.5, so two of them average 7. The average of one die with `n` faces is `(n + 1) / 2`, the midpoint rule from section 1. On a critical hit (a natural 20 on the d20), 5e rolls the damage dice twice but adds modifiers only once. So if a greatsword attack deals 2d6 + 3 and hits 65% of the time including the 5% crit chance, its expected damage per attack is

```
0.65 × (7 + 3) + 0.05 × 7 = 6.5 + 0.35 = 6.85
```

The crit term is small because only the dice double. Same structure as our weapons, with a crit that multiplies part of the damage instead of all of it.

**League of Legends.** A critical strike in League multiplies the hit by a crit damage value, so an attack's expected damage multiplier is `1 + c(m − 1)`, exactly our crit multiplier. The value of `m` has changed across patches. The League of Legends Wiki records base crit damage as 200% at launch, reduced to 175% in patch V10.23, and returned to 200% in V26.01. At 50% crit chance, that is an expected multiplier of 1 + 0.5 × 0.75 = 1.375 under the V10.23 to V25 rules and 1 + 0.5 × 1.0 = 1.5 from V26.01. A patch note that changes one constant moved every crit build's expected damage by about 9%. League also smooths crit streaks with a pseudo-random rule; that affects how streaky crits feel, which week 10 covers, and for this lecture we treat the listed crit chance as the long-run rate.

**Pokémon (Generation VII onward).** Damage is multiplied by a random integer from 85 to 100, divided by 100. Every integer is equally likely, so the average factor is (85 + 100) / 2 = 92.5%. A move's "average damage" is therefore 92.5% of its maximum roll. Critical hits at the base stage happen with probability 1/24 and deal 1.5 times damage, so the expected crit multiplier is 1 + (1/24)(0.5) = 1.021. Base-rate crits in modern Pokémon add about 2% to expected damage. They feel dramatic because each one is a 50% jump, but on average they barely move the needle. That gap between feel and average is next week's topic.

**Diablo II and armor.** The MMO303 lecture on [armor and damage mitigation](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md) shows that Diablo II's defense changes the *chance to be hit* rather than the damage. Our hit multiplier `(1 − q)` is the same idea from the attacker's side. The expected damage you take is the chance to be hit times the average hit, so a defense stat that lowers hit chance and one that lowers damage can be compared on one scale.

Four games, one structure: expected damage = chance to land × average size × crit adjustment. When a new game hands you a weapon, look for those three factors first.

### Eyes-open design judgment

Expected DPS is the right number for comparing weapons **over long fights against the same target**. It is the wrong number, or an incomplete one, in several situations you should plan for deliberately.

- **The tooltip describes the item, not the wielder.** Blizzard's choice to print weapon-only DPS keeps the tooltip stable when you swap characters, at the cost of misleading players whose crit or hit chance is unusual. If your game has large crit bonuses on items, a weapon-only tooltip will rank items wrongly for many players. Decide whether to show a character-aware number, and label it clearly if you do.
- **Expected value ignores thresholds.** An enemy with 100 HP dies to any hit of 100 or more. A crit for 240 on that enemy deals 100 useful damage and wastes 140. When targets have low health relative to hits, the extra damage from crits is partly wasted and expected DPS overstates the weapon. Next week you will compute exactly how much.
- **Expected value ignores timing.** A 3.0-second weapon in a 4-second fight swings twice at most, often once. Expected DPS assumes the fight is long enough that partial swings do not matter. For burst windows, count swings, not seconds.
- **Expected value hides spread.** The Maul and Rapier could have identical expected DPS and completely different feel. A weapon that deals 0 or 80 with equal chance and one that always deals 40 have the same average. Players do not experience averages. They experience streaks.
- **Crit and damage bonuses interact.** Because expected damage is a product, a point of crit is worth more on a weapon with high base damage, and a point of crit multiplier is worth more when crit chance is high. Price your stats with this in mind or players will discover the combination you underpriced.

So use expected value as the baseline, then ask which of these five conditions breaks it for the content you are designing.

### Check yourself (worked example)

1. The character in the example buys a ring that removes all misses. Compute both weapons' new expected DPS. Did the ranking change? Why or why not?
2. Keep the original character (10% miss, 5% base crit) but raise the crit multiplier to 3. What is the Rapier's crit bonus at which the two weapons tie now?
3. A designer wants the Rapier to tie the Maul at +25% crit without changing crit. Which single number on the Rapier would you change, and to what?

<details>
<summary>Answers</summary>

1. Maul: 1.0 × 120 × 1.05 / 3 = 42.0. Rapier: 1.0 × 36 × 1.30 = 46.8. The ranking stays the same. The hit multiplier `(1 − q)` multiplies both weapons by the same factor, so it scales both lines and cannot move the crossing.
2. With `m = 3`, the crit multiplier is `1 + 2c`. Maul: 0.9 × 120 × (1 + 2 × 0.05) / 3 = 0.9 × 120 × 1.1 / 3 = 39.6. Rapier: 0.9 × 36 × (1 + 2c) = 39.6 gives 1 + 2c = 1.2222, so c = 0.1111. The Rapier's total crit only needs to be 11.1%, a bonus of about +6.1%. A higher multiplier makes each point of crit chance worth more.
3. Change the average damage `D`. The Rapier needs 0.9 × D × 1.30 = 37.8, so D = 32.3. Any range with midpoint about 32.3 works, for example 27 to 38 (midpoint 32.5, close enough for a playtest) or 26 to 38.6 if you allow decimals.

</details>

## 3. Linearity of expectation

The shortcut that turned the three-row outcome table into one formula is a general rule, and it is the most useful fact in this course.

**Linearity of expectation.** For any random variables `X` and `Y` and any constants `a` and `b`:

```
E[X + Y] = E[X] + E[Y]
E[aX + b] = a E[X] + b
```

This holds whether or not `X` and `Y` are independent. That freedom is rare in probability, and designers exploit it constantly.

Three consequences you will use all semester:

- **Expected damage over a fight is expected damage per swing times the number of swings.** If a fight lasts 20 swings, the Rapier's expected total is 20 × 42.12 = 842.4. You do not need to enumerate the millions of possible sequences of misses and crits.
- **Flat bonuses add straight through.** If a buff adds 5 damage to every hit that lands, expected damage per swing rises by `(1 − q) × 5 × (1 + c(m − 1))` if crits double the bonus, or by `(1 − q) × 5` if they do not. Either way it is a separate term you can add.
- **Expected loot is a sum over the table.** If a goblin drops 10 gold with probability 0.5, a 50-gold gem with probability 0.1 and nothing otherwise, expected gold per kill is 0.5 × 10 + 0.1 × 50 = 10. Over 300 kills, the expected haul is 3,000 gold. MMO economy designers (MMO304) use exactly this to estimate how much currency a zone injects per hour.

A warning to carry into next week. Linearity works for averages. It does **not** say that the variance, or the chance of a lucky streak, adds up the same way. Averages are the easy part of randomness.

## 4. Expected value of a decision

Expected value also answers "should I?" questions, which is where it meets game design most directly.

Suppose a crafting system lets players upgrade a weapon from +5 to +6. The attempt costs 100 gold. It succeeds with probability 0.6 and adds 3 DPS. On failure the weapon is unchanged. Is it worth it?

The expected DPS gain per attempt is 0.6 × 3 = 1.8. The expected number of attempts until the first success is 1 / 0.6 = 1.67 (you will derive that formula in week 7, the geometric distribution), so the expected cost of the upgrade is about 167 gold. Now the player can compare "167 gold for 3 DPS" with other ways to spend 167 gold.

Change the rule so that failure **destroys** the weapon, and expected value alone stops being enough. The average cost goes up, and there is now a painful outcome players will remember. Many MMOs with enhancement systems built exactly this, and much of the player anger around them comes from the tail outcomes, not from the average. When you design a decision with a harsh failure state, compute the expected value, then compute the probability of the worst outcome, and ask whether you are comfortable with that number of angry players. Week 5 gives you the tool for the second question.

## In-class activity (25 minutes)

Work in pairs. Each pair gets three weapon cards (printed or on screen):

| Card | Damage | Speed | Special |
|---|---|---|---|
| A: Warhammer | 60 to 100 | 2.5 s | Crits deal ×2.5 instead of ×2 |
| B: Twin Blades | 12 to 18 | 0.6 s | none |
| C: Longbow | 40 to 60 | 2.0 s | Never misses |

Use the character from section 2 (10% miss, 5% base crit, ×2 crits unless the card says otherwise).

1. Compute tooltip DPS for all three (5 minutes).
2. Build the outcome table (miss, hit, crit) for each and compute expected DPS (10 minutes).
3. Rank the cards both ways. Write one sentence explaining any ranking change in terms of the three multipliers.
4. Choose one card and change **one** number so all three have expected DPS within 1 of each other. Swap with another pair and check their arithmetic (5 minutes).

Expected output: a filled table with six DPS values, two rankings and one balance change per pair. For reference, the tooltip values are 32.0, 25.0 and 25.0, and the expected values are 30.96, 23.63 and 26.25. Twin Blades and Longbow tie on the tooltip and separate by 2.6 DPS in the fight.

## Common misconceptions

- **"The expected value is the most likely result."** It is the long-run average, and it may not be possible at all (3.5 on a d6). For a weapon that crits for double, you will never see a hit of exactly the expected damage.
- **"Tooltip DPS includes my crits."** A weapon-only tooltip cannot know your crit chance. Check what your game's tooltip averages before trusting it, and when you design one, say which factors it includes.
- **"10% more crit chance means 10% more damage."** It adds `0.10 × (m − 1)` to the crit multiplier. At `m = 2` that is +0.10 on a multiplier that is already above 1, so the relative gain is less than 10% and shrinks as you stack crit. At `m = 1.5`, it adds only +0.05.
- **"Linearity of expectation needs independence."** It does not. `E[X + Y] = E[X] + E[Y]` holds for any two random variables. Independence matters for variance, which you meet next week.

## Check yourself

1. A loot table gives 1 gold with probability 0.7, 20 gold with probability 0.25 and 200 gold with probability 0.05. Compute expected gold per kill. Which row contributes most to the average?
2. Using the League of Legends crit damage values from section 2, how much crit chance does a champion need under the V10.23 to V25 rules (175%) to match the expected crit multiplier of a champion with 30% crit under the V26.01 rules (200%)?
3. A d20 attack hits on 11 or higher (so 50% including a natural 20) and deals 1d8 + 4, with dice doubled on a natural 20. Compute expected damage per attack. By how much does the champion fighter's "crit on 19 or 20" raise it?

<details>
<summary>Answers</summary>

1. 0.7 × 1 + 0.25 × 20 + 0.05 × 200 = 0.7 + 5 + 10 = 15.7 gold. The rare 200-gold row contributes 10 of the 15.7, almost two thirds. Rare, large rewards dominate averages, which is why a small change to a rare drop can move an economy.
2. Target multiplier: 1 + 0.30 × 1.0 = 1.30. Under 175%: 1 + c × 0.75 = 1.30, so c = 0.40. The old rules needed 40% crit to match 30% under the new ones.
3. Average 1d8 = 4.5. Expected damage = 0.50 × (4.5 + 4) + 0.05 × 4.5 = 4.25 + 0.225 = 4.475. Critting on 19 or 20 raises the crit chance to 0.10 (both still hit), so the crit term becomes 0.10 × 4.5 = 0.45. New expected damage is 4.25 + 0.45 = 4.70, a gain of 0.225 per attack, about 5%.

</details>

## Lab hook

**Lab 04: Expected-DPS spreadsheet** ([`labs/lab04.md`](../labs/lab04.md)). You build a sheet that computes tooltip DPS and expected DPS for a set of weapons, plots expected DPS against crit chance, finds the break-even points and writes a balance recommendation. The sheet is reused in Lab 05 to add variance.

## Sources

- Warcraft Wiki, "Arcanite Reaper" (World of Warcraft classic era, patch 1.x item data): 153 to 256 damage, speed 3.80, 53.8 damage per second, required level 58. https://warcraft.wiki.gg/wiki/Arcanite_Reaper
- Wizards of the Coast, *System Reference Document 5.1* (D&D 5th edition, 2016), Combat chapter: natural 20 always hits; on a critical hit, roll all damage dice twice and add modifiers once; monster stat blocks list average damage with dice in parentheses. Also the Champion subclass, Improved Critical (crit on 19 or 20 from 3rd level).
- League of Legends Wiki, "Critical strike" (accessed September 2026): base crit damage 200% at release, 175% from patch V10.23, 200% again from V26.01; crits use a pseudo-random algorithm. https://wiki.leagueoflegends.com/en-us/Critical_strike
- Bulbapedia, "Damage" (Pokémon, Generation III onward): random factor is an integer from 85 to 100 divided by 100. https://bulbapedia.bulbagarden.net/wiki/Damage
- Serebii.net, "Critical Hits" (Pokémon): base crit chance 1/24 (about 4.17%) from Generation VII, crit damage 1.5× from Generation VI. https://www.serebii.net/games/criticalhits.shtml
- Schreiber, I. (2010). *Game Balance Concepts*, Level 4, "Probability and Randomness". https://gamebalanceconcepts.wordpress.com/
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.

## Interactive spec: examples/w04-expected-dps.html

**Purpose.** Show that tooltip DPS and expected DPS can rank two weapons differently, and that the flip happens at one computable crossing point.

**The one insight the visual must make obvious.** Shared multipliers (miss chance) scale both weapons and never change the ranking; the crit bonus changes one weapon's line and flips the ranking exactly at the crossing.

**Layout.** Two linked panels, side by side at desktop width, stacked at 390px.

- Left panel, "Tooltip vs fight": a grouped bar chart. Two groups (Iron Maul, Keen Rapier), two bars each (tooltip DPS in a muted tone, expected DPS in the accent tone). Exact values printed on or above each bar to two decimals. A one-line verdict above the chart: "Tooltip leader: Maul. Fight leader: Rapier."
- Right panel, "Expected DPS vs Rapier crit bonus": x axis is the Rapier's crit bonus from 0% to 50%; y axis is expected DPS from 0 to 60. A horizontal-ish line for the Maul (constant in the Rapier's bonus) and a rising line for the Rapier. Mark the crossing with a dot and a label "tie at +X%". Draw a vertical marker at the current slider value.
- Below both, an outcome table for each weapon (miss, normal, crit rows with probability, damage, probability × damage, total), updated live, matching section 2 of the lecture.

**Controls** (all keyboard accessible range inputs with visible numeric values):

- Miss chance `q`: 0% to 40%, step 1%, default 10%.
- Base crit chance `c0`: 0% to 30%, step 1%, default 5%.
- Rapier crit bonus `b`: 0% to 50%, step 1%, default 25%.
- Crit multiplier `m`: 1.5 to 3.0, step 0.05, default 2.0.
- A "Reset to lecture values" button.

**Formulas.**

- Maul: `D = 120`, `s = 3.0`, `c = min(1, c0)`.
- Rapier: `D = 36`, `s = 1.0`, `c = min(1, c0 + b)`.
- Tooltip DPS = `D / s`.
- Expected DPS = `(1 − q) × D × (1 + c × (m − 1)) / s`.
- Crossing (Rapier bonus at which the two tie): solve `(1 − q) × 36 × (1 + (c0 + b)(m − 1)) = (1 − q) × 120 × (1 + c0(m − 1)) / 3` for `b`, which gives `b* = ((40/36) × (1 + c0(m − 1)) − 1) / (m − 1) − c0`. If `b*` is outside 0 to 50%, show "no tie in range" instead of the dot.

**Test values** (defaults must reproduce the lecture):

| q | c0 | b | m | Maul tooltip | Maul expected | Rapier tooltip | Rapier expected | Tie at |
|---|---|---|---|---|---|---|---|---|
| 0.10 | 0.05 | 0.25 | 2.0 | 40.00 | 37.80 | 36.00 | 42.12 | +11.67% |
| 0.00 | 0.05 | 0.25 | 2.0 | 40.00 | 42.00 | 36.00 | 46.80 | +11.67% |
| 0.10 | 0.05 | 0.25 | 3.0 | 40.00 | 39.60 | 36.00 | 51.84 | +6.11% |
| 0.10 | 0.05 | 0.10 | 2.0 | 40.00 | 37.80 | 36.00 | 37.26 | +11.67% |

Note that rows 1 and 2 share the same tie point. The visual should make that invariance visible: when the miss slider moves, both lines scale and the dot slides vertically but not horizontally.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`, light and dark themes, `prefers-reduced-motion` disables transitions. No game art or logos; weapons are drawn as plain labeled bars.
