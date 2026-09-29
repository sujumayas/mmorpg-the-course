# MMO303 · Week 09 — Intransitivity and Counters

**Why this matters:** When you buff a class, you expect to see more of it. In a game built on counters, you often see less of it, and more of the class that beats it. Designers who don't know why end up chasing their own patches around a circle.

**You will be able to:**
- Distinguish transitive from intransitive relationships, and hard from soft counters, using matchup win rates.
- Compute the stable population mix of a three-class counter triangle from its matchup win rates.
- Predict how a buff to one matchup moves the stable mix, and explain why the counter class gains.
- Design an n-class counter graph with no dominant option, and critique when counters make a game feel unfair.

**Before class:** Schreiber & Romero, *Game Balance* (2021), chapter 25 (Intransitive Mechanics and Payoff Matrices); Sirlin, "Balancing Multiplayer Games, Part 1: Definitions" (a companion article to his GDC 2009 talk).

**Prerequisites from earlier courses:** MA102 [week 4](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md) (expected value) and [week 11](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md) (Monte Carlo simulation). GD102 Systems Design, [week 3](../../GD102-systems-design-and-game-mechanics/lectures/w03-positive-feedback-loops-snowballing.md) and [week 4](../../GD102-systems-design-and-game-mechanics/lectures/w04-negative-feedback-loops-rubber-banding.md) (feedback loops). From this course, [week 2](w02-armor-and-damage-mitigation.md) (the habit of rewriting a formula into one form), [week 1](w01-what-balanced-means.md) (fairness, viability, diversity) and [week 8](w08-crowd-control-and-diminishing-returns.md) (CC as a counter tool). [Week 10](w10-game-theory-payoff-matrices-and-nash-equilibria.md) formalizes today's "stable mix" as a Nash equilibrium.

**Interactive:** [Counter triangle](../examples/w09-counter-triangle.html). Keep it open during section 2.

---

## 1. Transitive and intransitive

A relationship is **transitive** if "A beats B" and "B beats C" always gives "A beats C". Level, item level and raw stat budgets are usually transitive. A level 60 character beats a level 50 who beats a level 40, and the 60 beats the 40 too. Transitive systems have a best option, and the player's job is to get it.

A relationship is **intransitive** if it can loop: A beats B, B beats C, and C beats A. Rock-paper-scissors is the smallest loop. No option is best in general. The best option depends on what the opponent picks.

Balance in a multiplayer game, in David Sirlin's framing, means that many options are viable at high-level play. Transitive systems work against that, because the best option crowds out the rest. Intransitive systems are one of the main tools for keeping several options alive. Each option has a reason to exist, which is the thing it beats.

Two words you will use all semester:

- A **counter** is an option with a favorable matchup against another. "Mage counters Knight" means a Mage wins more than half of their fights against Knights, all else equal.
- A **matchup win rate** `w(X, Y)` is how often X beats Y. It is a number from 0 to 1, and `w(Y, X) = 1 − w(X, Y)` when draws are rare.

Counters come in strengths:

- A **hard counter** wins most of its matchup, say 75% or more. Pick the wrong class into it and you mostly lose regardless of skill.
- A **soft counter** has an edge, say 55% to 60%. Skill and circumstance still decide most fights.

A game can be intransitive and still badly balanced. The shape of the loop is one question. How strong each link is and how the population responds are separate ones, and those are where the surprises live.

## 2. Worked example: buff the Knight, get more Mages

### The hook

The Fire Emblem series has used a weapon triangle since *Genealogy of the Holy War*. Swords beat axes, axes beat lances, lances beat swords. In the Game Boy Advance entries (*The Blazing Blade*, *The Sacred Stones*), the unit with the advantage gets +15 hit rate and +1 weapon might, and the other unit gets the matching penalty. Pokémon's starter types do the same thing with damage. Fire moves deal double damage to Grass, Grass to Water and Water to Fire, and a not-very-effective move deals half.

Both triangles are symmetric. Every link has the same strength. So here is the designer's question. Suppose you make one link stronger, for example raising the advantage of axes over lances. Players will carry more axes, right?

Work it out and the answer is no. In the long run players carry more swords, the weapon that beats axes. The axe's own share stays put or falls. This worked example shows why, with an MMO arena as the setting.

### The setting

A small arena game has three classes.

- **Knight** beats Ranger. Heavy armor shrugs off arrows.
- **Ranger** beats Mage. Range and interrupts shut down casting.
- **Mage** beats Knight. Magic ignores armor and roots stop the Knight from closing in.

Players choose a class before they queue and do not see their opponent's class. Over weeks, players drift toward classes that are winning.

### The model

Turn each matchup win rate into a **net margin**, wins minus losses per fight:

```
margin(X, Y) = 2 × w(X, Y) − 1
```

A 60% matchup is a margin of +0.2. A 50% matchup is 0. Name the three favorable margins:

- `a` = margin of Knight over Ranger
- `b` = margin of Mage over Knight
- `c` = margin of Ranger over Mage

If the population plays Knight, Mage and Ranger with shares `k`, `m` and `r` (adding to 1), each class's expected margin against a random opponent is

```
E(Knight) = −b × m + a × r
E(Mage)   =  b × k − c × r
E(Ranger) = −a × k + c × m
```

A class's win rate against the whole population is `0.5 + E / 2`. A class with positive `E` wins more than half its games, and players drift toward it.

The population stops drifting when every class has `E = 0`, so all three win exactly half their games. Call this the **stable mix**. Setting all three expressions to zero and solving gives

```
k = c / (a + b + c)
m = a / (a + b + c)
r = b / (a + b + c)
```

Read it slowly, because it is strange. **Each class's share is set by the matchup it is not in.** Knight's share depends on how hard Ranger beats Mage. Mage's share depends on how hard Knight beats Ranger. So if you raise `a`, the Knight's edge over Rangers, the class that grows is Mage, the Knight's counter.

The logic in words: a stronger Knight punishes Rangers harder. The population must then hold fewer Knights for Rangers to break even, or more Mages to keep Knights in check. The system settles where Mages are common enough that Knights are no longer winning. Mages rise until they have soaked up the buff.

### Numbers you can check

Start symmetric: every favorable matchup is 60%, so `a = b = c = 0.2`. The stable mix is one third each.

Now the patch. Knight versus Ranger goes from 60% to 70%, so `a = 0.4`. The other two links stay at 60%.

| | Knight share | Mage share | Ranger share |
|---|---|---|---|
| Stable mix before patch (a = b = c = 0.2) | 33.3% | 33.3% | 33.3% |
| Stable mix after patch (a = 0.4) | 25.0% | 50.0% | 25.0% |

Check the new mix: `a + b + c = 0.8`, so `k = 0.2 / 0.8`, `m = 0.4 / 0.8`, `r = 0.2 / 0.8`.

Now look at win rates. In the first week after the patch, the population is still one third each. Win rate of each class against that population:

| Class | vs Knight | vs Mage | vs Ranger | Win rate, week 1 | Win rate at new stable mix |
|---|---|---|---|---|---|
| Knight | 50% | 40% | 70% | 53.3% | 50.0% |
| Mage | 60% | 50% | 40% | 50.0% | 50.0% |
| Ranger | 30% | 60% | 50% | 46.7% | 50.0% |

Check the Knight's week-1 number: `(0.50 + 0.40 + 0.70) / 3 = 0.533`. At the new mix it is `0.25 × 0.50 + 0.50 × 0.40 + 0.25 × 0.70 = 0.125 + 0.200 + 0.175 = 0.500`.

Here is the trap. The week after the patch, your dashboard says Knights win 53.3%, so Knights look overtuned. Players flock to Knight. Mages start winning. Mages flock in. Rangers get crushed and some leave. After a few weeks, if things settle, you see 25% Knights, 50% Mages, 25% Rangers, all at 50% win rate. The Knight buff made Knights rarer and Mages the most popular class in the game.

### How the population gets there

Players do not jump to the stable mix. They drift. A simple rule captures this: each week, each class's share grows in proportion to how far its margin is above zero:

```
share_next = share × (1 + η × E)
```

where `η` (eta) is how quickly players switch. Because every win for one class is a loss for another, the shares still add to 1 after the update. This is a discrete version of what biologists call **replicator dynamics**.

Run one step from one third each with `η = 1`. The Knight's `E` is `(0 − 0.2 + 0.4) / 3 = +0.067`. The Mage's is `(0.2 + 0 − 0.2) / 3 = 0`. The Ranger's is `(−0.4 + 0.2 + 0) / 3 = −0.067`. The new shares are Knight 35.6%, Mage 33.3%, Ranger 31.1%. Knights rise first, exactly as your week-1 dashboard predicted. Keep stepping and Mages rise next, then Rangers recover as Mages crowd out Knights, and the shares spiral around the stable mix.

In a pure counter triangle, the spiral does not settle by itself. The population cycles around the stable mix forever, and the size of the loop depends on where it started. Real populations settle more because of friction. Many players stick with a class they like, and new players arrive with their own preferences. But the cycle is real, and it is one reason metas in counter-based games rotate even without patches.

### A visual the student can move

Open the [counter triangle interactive](../examples/w09-counter-triangle.html). The left view is a triangle. Each corner is a population of all one class, and each point inside is a mix. The stable mix is a marked point. From the current population, a line traces the drift, week by week.

The right view shows the stable-mix shares as bars and each class's win rate against the current population.

Drag the Knight versus Ranger slider from 60% to 70%. On the right, the Mage bar grows while the Knight bar shrinks. On the left, the stable point slides toward the Mage corner, and the drift line from the old mix loops around the new point. Press "Week 1 view" to see the win rates the week after the patch, with Knights on top, and then "Run 20 weeks" to watch the population chase the new center.

### Cross-game recognition

**Fire Emblem, rewritten.** With equal triangle bonuses, the three weapons have equal `a`, `b`, `c`, and a player facing an unknown army should expect a third of each. Raise the axe's edge over lances (the "a" link, with axe as Knight and lance as Ranger) and the stable mix shifts toward swords. The series has also shown the other design lever. *Three Houses* removed the weapon triangle from its core rules, and *Engage* changed the advantage into a "break" status instead of a hit and damage bonus. That is a designer deciding that the loop's strength, not just its shape, is a choice.

**Pokémon type chart.** Eighteen types (since Fairy arrived in Generation VI) with multipliers of 2, 0.5 and 0. Fire, Grass and Water form a clean triangle with equal 2× links, and the full chart is a much bigger counter graph with many uneven links. The stable-mix idea still applies. A type that hits many popular types hard pushes up the use of whatever resists it. Adding Fairy, which is super effective against Dragon, changed the counter graph by giving Dragon a new counter, and every share in the stable mix moved with it.

**Dark Age of Camelot realms.** Dark Age of Camelot's realm versus realm war puts three realms, Albion, Midgard and Hibernia, against each other. The three-way structure has the same feedback as a counter triangle, at the scale of factions. When one realm pulls ahead, the other two both have reason to attack it, which pushes the lead to rotate. The link strengths are not fixed numbers. They come from population and coordination. But the rewrite is the same: three options, each pressed by the other two, and a population that drifts toward whoever is not being pressed.

In each case, write the relationships as a margin table, find the stable mix, and ask what a change to one link does to the mix. The answer is rarely "more of the thing you buffed".

### Eyes-open design judgment

- **Buffs move the counter, not the class.** In a pure triangle, buffing a class's favorable matchup raises its counter's share. If you want more Knights, strengthen the Ranger-over-Mage link (the one Knight is not in), or make Knights better against their counter.
- **Early win rates lie.** A patch changes win rates before it changes populations. A 53% class in week 1 may be a 50% class in week 6 at a lower pick rate. Wait for the population to move before you patch again, or you will chase your own changes around the triangle. MMO307 week 14 goes further on reading win and pick rates together.
- **Hard counters make class choice a coin flip.** When the opponent is unknown at pick time, a 75% counter means a quarter of your fights are decided before they start. That is acceptable when players can switch between fights, and much worse in an MMO where a class takes months to level.
- **Soft counters keep skill in charge.** A 55% link still creates rotation and viability, and it leaves most fights to the players.
- **Groups dilute counters.** In a five-player team the counter relationships average out across the members. Group PvP can tolerate harder individual counters than 1v1 duels.
- **A loop can hide a dominant option.** If one class beats one class and ties the rest, while others win some and lose some, the tying class is never worse and often better. Check each class's worst matchup, not just the loop's direction.

## 3. Counter graphs with more than three classes

With `n` classes, draw a **counter graph**: one node per class, an arrow from X to Y when X beats Y. A healthy graph has no **dominant** class (one that beats or ties everything) and no **dominated** class (one that loses to or ties everything).

The cleanest balanced graph is one where every class beats exactly half of the others and loses to the other half. Graph theorists call this a **regular tournament**. It exists only when `n` is odd, because each class plays `n − 1` others and must beat `(n − 1) / 2` of them. Rock-paper-scissors-lizard-Spock, with five options each beating two, is the popular example.

With an even number of classes, such as four, each class plays three others and cannot beat exactly half. Designers fix this in three ways:

1. **Allow even matchups.** Some links are 50%. Each class beats one, loses to one, ties one.
2. **Make links uneven in strength.** A class beats two others softly and loses to one hard. The expected margins can still balance.
3. **Use roles instead of a loop.** In a group game, classes do not fight each other one to one. Counters happen between compositions, and the graph is over teams, not classes.

For three classes you found the stable mix by hand. For five or more, the same indifference conditions give a system of linear equations, one per class, and week 10 solves them with payoff matrices. The rule survives: a buff to one link shifts shares around the graph, often away from the class you touched.

## 4. Where counters come from in an MMO

MMO classes rarely say "Mage beats Knight" on a tooltip. Counters emerge from mechanics you already know.

- **Range against gap-closing.** A ranged class wins if it keeps distance. A melee class wins if it closes. Roots and slows (week 8) decide which happens.
- **Mitigation type.** Week 2's armor helps against physical damage and not against magic. A class stacking armor counters physical attackers and is countered by casters.
- **Interrupts against casters.** Silences and interrupts punish classes with long cast times. The healer spells from week 7 with 2.5-second casts are exactly what an interrupt class counters.
- **Healing against burst.** A class with strong sustained healing beats one with steady damage and loses to one with burst that kills through a heal.
- **CC against CC-breakers.** A class whose power is chain CC is countered by a class with immunities and breaks.

Each is a lever. When you need to change a matchup, name which of these mechanics decides it, and change that, instead of adding flat damage that shifts every matchup at once.

## In-class activity (25 minutes)

In pairs, you are balancing the three-class arena from section 2. Current matchups: Knight beats Ranger 65%, Mage beats Knight 60%, Ranger beats Mage 55%.

1. Compute `a`, `b`, `c` and the stable mix.
2. Your community wants "more Rangers". Find the one link to change and the new win rate that puts Rangers at 40% of the stable mix. Keep the other two links fixed.
3. Name the mechanic from section 4 you would change to get that win rate, and one side effect it has on another matchup.
4. Predict the class win rates in the first week after your patch, with the population still at the old stable mix. Which class will players complain about?

Expected output: the stable mix before and after, the patched win rate, the week-1 win rates, and a two-sentence patch note.

## Common misconceptions

- **"Buffing a class makes it more popular."** In a counter loop, it makes its counter more popular in the long run. The buffed class may even become rarer.
- **"A 50% win rate means the class is balanced."** At the stable mix, every class in a pure loop wins 50%, at any link strengths. The pick rates, not the win rates, show what the links are doing.
- **"Rock-paper-scissors is balanced, so any triangle is."** Only if the links are equal. Uneven links give an uneven stable mix, and some classes end up rare.
- **"Hard counters create more strategy."** They create more counter-picking when picks are visible. When picks are blind, they create more games decided at character select.

## Check yourself

1. Matchups: Knight beats Ranger 70%, Mage beats Knight 55%, Ranger beats Mage 60%. Compute the stable mix. Which class is rarest, and which link would you change to raise it?
2. With Knight over Ranger and Ranger over Mage both at 60%, what win rate must Mage have over Knight for Rangers to make up 40% of the stable mix?
3. A four-class game has classes W, X, Y, Z. W beats X, X beats Y, Y beats Z, Z beats W, and the two remaining pairs (W vs Y, X vs Z) are even. All favorable links are 60%. Is there a dominant class? What is the stable mix?
4. A designer sees Mage at 52% win rate the week after a patch that only changed Ranger versus Mage. Did the patch make Rangers stronger or weaker against Mages? Explain using `E(Mage)` at the old mix.

<details>
<summary>Answers</summary>

1. `a = 0.4`, `b = 0.1`, `c = 0.2`, total 0.7. Knight `c / 0.7 = 28.6%`, Mage `a / 0.7 = 57.1%`, Ranger `b / 0.7 = 14.3%`. Ranger is rarest. Its share is set by `b`, so strengthen Mage against Knight.
2. `a = c = 0.2`. Need `b / (0.4 + b) = 0.4`, so `b = 0.16 + 0.4 b`, `0.6 b = 0.16`, `b = 0.267`. Win rate `= (1 + 0.267) / 2 = 63.3%`. To get more Rangers, you buff Mage against Knight.
3. No class is dominant: each beats one class, loses to one, and ties one. By symmetry every class has `E = 0` at 25% each, so the stable mix is one quarter each. (Other mixes are also stable here, for example W and Y only; week 10 covers games with many equilibria.)
4. The old mix had `E(Mage) = 0`. Only `c` changed, and `E(Mage) = b × k − c × r`. A 52% win rate means `E(Mage) = +0.04 > 0`, so `c` must have fallen. Rangers got weaker against Mages.

</details>

## Lab hook

**Lab 09 (Patch the triangle).** Build a replicator-dynamics sheet or script for a three-class and a five-class counter graph. Predict the week-1 win rates and the long-run stable mix for three proposed patches, then run 30 simulated weeks to check your predictions. See [`labs/lab09.md`](../labs/lab09.md).

## Sources

- Fire Emblem Wiki, "Weapon triangle" (accessed September 2026). Swords beat axes, axes beat lances, lances beat swords, since *Genealogy of the Holy War*; +15 hit and +1 might in *The Blazing Blade* and *The Sacred Stones*; removed in *Echoes* and *Three Houses*; changed to a break effect in *Engage*.
- Pokémon type chart as summarized by Pokémon Database, "Pokémon type chart" and Bulbapedia, "Fairy (type)" (accessed September 2026). 18 types, multipliers 2, 0.5 and 0; Fire, Grass, Water triangle; Fairy added in Generation VI and super effective against Dragon.
- Broadsword Online Games, "Three Realms", darkageofcamelot.com, and Wikipedia, "Dark Age of Camelot" (accessed September 2026). Three realms, Albion, Midgard and Hibernia, in a realm versus realm war.
- Sirlin, D. (2009). "Balancing Multiplayer Competitive Games", GDC 2009 (GDC Vault), and "Balancing Multiplayer Games, Part 1: Definitions", sirlin.net. A game is balanced when many options are viable at expert play.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Chapter 25, Intransitive Mechanics and Payoff Matrices.
- The Knight, Mage and Ranger arena and all its win rates are invented for teaching.

## Interactive spec: examples/w09-counter-triangle.html

**The one insight:** in a counter triangle, strengthening one link moves the stable population toward the counter of the class you buffed. The week-1 win rates point one way and the long-run mix points another.

**Layout.** Two linked views side by side on desktop, stacked on mobile. Controls above the views, number panel below.

**Left view: population triangle (ternary plot).**
- Equilateral triangle with corners labeled Knight (top), Mage (bottom left), Ranger (bottom right). A point's barycentric coordinates are the shares `(k, m, r)`.
- A filled marker at the stable mix. A hollow marker at the current population (default: one third each). The student can drag the hollow marker to set a starting population, or use arrow keys to move it in 1% steps.
- When the student runs weeks, draw the drift path as a polyline from the current population, one vertex per week.
- Light arrows on a grid of about 30 interior points showing drift direction (the vector of `share × E` per class) so the rotation is visible without running.

**Right view: bars.**
- Grouped bars per class: stable-mix share (solid) and current share (outline).
- Below, a win-rate row per class against the current population, with a 50% reference line.

**Controls.**
- Three sliders for favorable win rates, 50% to 95%, step 1: Knight over Ranger (default 60), Mage over Knight (60), Ranger over Mage (60).
- Switch rate η slider, 0.1 to 3, step 0.1, default 1.
- Buttons: "Step 1 week", "Run 20 weeks" (animated at 4 weeks per second, instant when reduced motion is on), "Reset population to stable mix", "Reset population to one third each", "Week 1 view" (sets the population to the stable mix of the previous slider values and shows win rates there).
- Preset buttons: "Symmetric 60%", "Knight buff (70/60/60)", "In-class activity (65/60/55)".

**Formulas.**
- `a = 2 w_KR − 1`, `b = 2 w_MK − 1`, `c = 2 w_RM − 1`.
- `E_K = −b m + a r`, `E_M = b k − c r`, `E_R = −a k + c m`.
- Win rate of class X vs the population `= 0.5 + E_X / 2`.
- Stable mix `k = c / S`, `m = a / S`, `r = b / S`, `S = a + b + c`. If `S = 0` (all links at 50%), show "every mix is stable".
- Weekly step: `x_i ← x_i (1 + η E_i)`, then divide by the sum (the sum is 1 up to rounding) and clamp at 0.0001 to keep points inside the triangle. This weekly formula is the default mode and produces the lecture's numbers. An optional "Smooth orbit (RK4)" mode integrates the continuous version, `dx_i/dt = η x_i E_i`, with fourth-order Runge-Kutta using 10 substeps of 0.1 week, so the path stays on its closed orbit instead of spiraling outward. The two modes give slightly different weekly values; the drift arrows use the continuous field.

**Number panel.** `a`, `b`, `c`; stable mix to one decimal percent; current shares; each class's `E` and win rate against the current population; week counter.

**Test values.**
- Symmetric 60%: stable mix 33.3 / 33.3 / 33.3; all win rates 50.0%.
- Knight buff (70/60/60): stable mix Knight 25.0%, Mage 50.0%, Ranger 25.0%. With population at one third each: win rates Knight 53.3%, Mage 50.0%, Ranger 46.7%. One step with η = 1 from one third each: Knight 35.6%, Mage 33.3%, Ranger 31.1% in the default weekly mode (the lecture's formula); Knight 35.5%, Mage 33.5%, Ranger 31.1% in the RK4 mode.
- In-class preset (65/60/55): stable mix Knight 16.7%, Mage 50.0%, Ranger 33.3%.
- Mage over Knight at 63.3% with the other two at 60%: Ranger share 40.0%.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`. Classes distinguished by shape as well as color (circle, square, triangle). The ternary point is keyboard movable. No game art, weapon icons or logos.
