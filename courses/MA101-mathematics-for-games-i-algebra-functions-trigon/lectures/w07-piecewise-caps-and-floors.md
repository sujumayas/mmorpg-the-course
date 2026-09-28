# MA101 · Week 07 — Piecewise Functions, Caps and Floors

**Why this matters:** Almost every stat in a shipped game stops behaving like one clean formula somewhere. It hits a cap, bottoms out at a floor, or changes slope at a "soft cap" that players argue about on forums. Those are piecewise functions, and if you can read and write them you can predict where players will stop investing in a stat before you ship it.

**You will be able to:**
- Write a piecewise function in math notation and in code, with correct boundary conditions.
- Build `clamp`, `min` and `max` caps and floors, and compute the effective value of a stat after them.
- Compute the per-point gain of a stat on each piece and locate its soft caps and hard caps.
- Critique a cap and propose a curve-based alternative when the cap creates a dead zone.

**Before class:** Schreiber & Romero, *Game Balance* (CRC Press, 2021), the chapter "Numeric Relationships"; skim the Fextralife Elden Ring wiki page "HP" (the table only).

**Prerequisites from earlier courses:** MA101 has no prerequisite course. This week uses slope from [MA101 week 2](w02-linear-functions-and-rates.md) and the rational curve `A / (A + K)` from [MA101 week 6](w06-rational-functions-and-asymptotes.md). The armor cap discussion builds on [MMO303 week 2, Armor and damage mitigation](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md), which you will meet in year 3.

**Interactive:** [Soft cap curve](../examples/w07-soft-cap-curve.html). Keep it open during section 2.

---

## 1. One rule is rarely enough

So far in this course every function has had one rule. Feed in `x`, apply the rule, get `y`. A line `y = 12x + 40`. A curve `y = A / (A + 100)`. One rule for every input.

Games break this all the time. A health regeneration rule might be "5 HP per second, but nothing while you are in combat." A damage rule might be "full damage up to 20 meters, then less." A movement rule might be "half gravity near the top of a jump if you are holding the button." Each of these is one function built from several rules, with the input deciding which rule applies. That is a **piecewise function**.

In math notation you write one rule per line, each with a condition:

```
         ⎧ 5      if not in combat
regen =  ⎨
         ⎩ 0      if in combat
```

For numeric inputs the conditions are usually ranges:

```
       ⎧ 2x          if x < 10
f(x) = ⎨ 20          if 10 ≤ x < 30
       ⎩ 20 + (x−30) if x ≥ 30
```

Each range is called a **piece**, and the input values where one piece hands over to the next (here 10 and 30) are **breakpoints**. Two rules for writing pieces well:

1. **The pieces must cover every input, and must not overlap.** Look at the `<` and `≤` signs above. At exactly `x = 10`, only the middle piece applies. If you wrote `x ≤ 10` on the first line and `10 ≤ x` on the second, the value at 10 would be ambiguous. In code this ambiguity does not show up as an error. The first `if` that matches wins, silently, and you get whatever order you happened to type.
2. **Check what happens at each breakpoint.** Plug the breakpoint into both neighbouring rules. Here the first rule gives `2 × 10 = 20` and the second gives `20`. They agree, so the graph has no jump. At 30 the second gives `20` and the third gives `20 + 0 = 20`. They agree again. A function whose pieces agree at every breakpoint is **continuous**: you can draw it without lifting the pen.

Continuous does not mean smooth. The graph of `f` above has two corners, one at each breakpoint, because the slope changes from 2 to 0 and then from 0 to 1. A corner like that is called a **kink**. Kinks are where most of the design action happens in stat curves, as you are about to see.

In code the same function is an if-chain:

```python
def f(x):
    if x < 10:
        return 2 * x
    elif x < 30:
        return 20
    else:
        return 20 + (x - 30)
```

Notice the chain only tests the upper bound of each piece. That works because each `elif` already knows the earlier tests failed. It also means the order of the branches is part of the definition. Swap two branches and you have written a different function.

## 2. Worked example: Elden Ring's Vigor soft caps

### The hook

In Elden Ring (FromSoftware, 2022), the Vigor stat sets your maximum HP. Every player guide tells you the same thing: get Vigor to 40, then think hard before going past 60. Why those numbers?

Look at what one level-up buys you. According to the community formula on the Fextralife wiki (current as of 2026, after the Shadow of the Erdtree expansion), raising Vigor from 39 to 40 adds 48 HP. Raising it from 40 to 41 adds 26 HP. Nearly half the value vanished in one step. From 60 to 61 you get 6 HP. The stat did not change its name or its menu entry. The rule behind it changed.

### The model

Here is the simplest honest model. We keep the three breakpoint values that many sources agree on (Vigor 40 gives 1,450 HP, Vigor 60 gives 1,900 HP, Vigor 99 gives 2,100 HP) plus Vigor 25 at 800 HP, and connect them with straight lines. That gives a **piecewise-linear** function:

```
           ⎧  800 + 43.3 × (V − 25)    if 25 ≤ V ≤ 40
HP(V)  ≈   ⎨ 1450 + 22.5 × (V − 40)    if 40 < V ≤ 60
           ⎩ 1900 + 5.13 × (V − 60)    if 60 < V ≤ 99
```

- `V` is the Vigor stat, an integer from 1 to 99.
- `HP(V)` is maximum health at that Vigor.
- The slope on each piece is the **per-point gain**: how much HP one more point of Vigor buys. It is the rise over the run between two breakpoints, for example `(1450 − 800) / (40 − 25) = 650 / 15 = 43.3`.

The breakpoints at 40 and 60 are the game's **soft caps**. A soft cap is a breakpoint where the per-point gain drops but stays above zero. You can keep investing. You just get less.

The actual game does not use straight lines between the breakpoints. The Fextralife wiki lists a curved rule for each piece, for example `1450 + 450 × (1 − (1 − (V − 40)/20)^1.2)` for Vigor 41 to 60, rounded down. We use the straight-line version as our model because it has one number per piece that you can reason about. The interactive shows both so you can see how close they are.

### Numbers you can check

First, the per-point gain on each piece, straight from the model:

| Piece | Vigor range | HP gained over the piece | Levels spent | Per-point gain |
|---|---|---|---|---|
| 1 | 25 to 40 | 650 | 15 | 43.3 |
| 2 | 40 to 60 | 450 | 20 | 22.5 |
| 3 | 60 to 99 | 200 | 39 | 5.1 |

Then the model against the wiki's curved formula at a few points:

| Vigor | Model HP (straight pieces) | Wiki formula HP | HP from last point (wiki) |
|---|---|---|---|
| 25 | 800 | 800 | 31 |
| 30 | 1,016.7 | 994 | 43 |
| 40 | 1,450 | 1,450 | 48 |
| 41 | 1,472.5 | 1,476 | 26 |
| 50 | 1,675 | 1,704 | 24 |
| 60 | 1,900 | 1,900 | 13 |
| 61 | 1,905.1 | 1,906 | 6 |
| 80 | 2,002.6 | 2,015 | 5 |
| 99 | 2,100 | 2,100 | 3 |

Check one row by hand. At Vigor 50 the model uses piece 2: `1450 + 22.5 × (50 − 40) = 1450 + 225 = 1,675`. The wiki's curved formula gives 1,704. The model is off by 29 HP, under 2%, and it agrees exactly at every breakpoint. That is good enough to reason about where the caps are.

Now read the table the way a player does. Vigor 20 to 40 buys 798 HP (the wiki gives 652 at Vigor 20). Vigor 40 to 60 buys 450. Vigor 60 to 99, which is 39 levels, buys 200. A level-up in Elden Ring costs the same runes whichever stat you raise, so after 60, those levels almost certainly do more for you in a damage stat.

### The visual

Open [`examples/w07-soft-cap-curve.html`](../examples/w07-soft-cap-curve.html). The left panel plots HP against Vigor. It looks like a gently bending hill, and the kinks at 40 and 60 are easy to miss. The right panel plots the per-point gain against Vigor. On that panel the same data is a staircase: a tall step up to 40, a middle step to 60, a low step after. Drag the Vigor slider and a marker moves on both panels at once.

That is the point of the two views. A soft cap is hard to see on the total and obvious on the gain. When players say "Vigor falls off at 40," they are reading the right-hand panel, even if they never drew it.

### Cross-game recognition

Soft caps, hard caps and floors are the same object in different clothes: a piecewise function whose slope drops at a breakpoint. The difference is only how far it drops.

**League of Legends, cooldown reduction (before patch 10.23, November 2020).** For years League gave a stat called cooldown reduction (CDR) that cut ability cooldowns by a percentage, capped at 40% (45% with one rune). Written as a piecewise function of the CDR on your items, `c`:

```
                    ⎧ c      if c < 0.40
effective CDR  =    ⎨
                    ⎩ 0.40   if c ≥ 0.40
```

That is a **hard cap**: the slope on the last piece is exactly zero. Past 40%, each extra point of CDR bought nothing. Players built to exactly 40% and treated anything beyond as wasted gold. In patch 10.23 Riot replaced CDR with **ability haste**, where `cooldown = base × 100 / (100 + haste)`. That is the rational curve from week 6. Casts per minute become `(60 / base) × (1 + haste/100)`, a straight line in haste with no dead zone. The designers removed a kink by changing the whole function family.

**Diablo II: Lord of Destruction, resistances.** Your effective fire resistance is your listed resistance minus a difficulty penalty (0 in Normal, 40 in Nightmare, 100 in Hell in the expansion), then clamped between a floor of −100% and a ceiling of 75%. Some unique items raise the ceiling, to at most 95%. So:

```
effective = clamp(listed − penalty, −100, 75 + bonus_max)
```

This one has a floor and a hard cap in the same line. A player with 120% listed fire resistance sees 75% in Normal (the cap cuts off 45 points) and 20% in Hell (the penalty eats 100 points and the cap no longer applies). The same gear is "overcapped" in one difficulty and badly short in another.

**Celeste (Maddy Makes Games, 2018), the jump apex.** The developers published the player movement code in 2018. Gravity there is piecewise. If the vertical speed is below 40 pixels per second and the jump button is held, gravity is multiplied by 0.5. Otherwise it is multiplied by 1. Two pieces, a jump at the breakpoint rather than a kink, and the result is a small floaty moment at the top of every held jump. Same idea, different stat.

**World of Warcraft (classic era).** Armor mitigation is `A / (A + K)` capped at 75%, which [MMO303 week 2](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md) turns into an effective-HP multiplier of at most 4.

Four games, one form. The question to ask of any new stat: *where are the breakpoints, and what is the per-point gain on each side?*

### Design judgment

A soft cap is a decision about where you want players to stop. Elden Ring's Vigor curve pushes most builds toward 40 to 60 Vigor. That leaves room for a glass-cannon build with low Vigor and a very tanky build near 99, both as deliberate choices with visible costs. That is a healthy use of a soft cap: it shapes the common case without forbidding the odd one.

A hard cap is blunter. It creates a dead zone where the stat is worth zero, and players will find the exact edge. Riot's move from capped CDR to ability haste is the standard fix. If you want diminishing percentage returns without a dead zone, use a curve whose slope shrinks but never reaches zero.

Kinks also have a cost for players. They are invisible on a stat screen that shows only the total. If your soft caps matter, show the per-point gain in the level-up menu ("+26 HP") so players do not need a wiki to find them. Decide on purpose whether the breakpoint is something players should discover or something you tell them.

Finally, prefer continuous functions for anything players invest in over time. A jump in the function at a breakpoint (like Celeste's gravity) is fine for moment-to-moment feel. A jump in a progression stat creates a **breakpoint hunt**, where players race to one exact value and nothing near it matters.

### Check yourself (worked example)

1. Using the straight-line model, how much Vigor does a player at 40 need to add to gain 300 HP? Using the same model, how much would a player at 60 need?
2. A designer wants a Vigor curve where the per-point gain halves at each soft cap, starting at 40 HP per point from Vigor 25, with soft caps at 40 and 60. Write the piecewise function and compute HP at Vigor 60.

<details>
<summary>Answers</summary>

1. From 40, the gain is 22.5 per point, so `300 / 22.5 = 13.3`, which rounds up to 14 points (Vigor 54). From 60 the gain is 5.13 per point, so `300 / 5.13 = 58.5` points. That would need Vigor 118.5, past the maximum of 99, so it is impossible. The whole piece above 60 only holds 200 HP.
2. `HP = 800 + 40(V − 25)` for 25 ≤ V ≤ 40, giving 1,400 at 40. Then `1400 + 20(V − 40)` for 40 < V ≤ 60, giving 1,800 at 60. Then `1800 + 10(V − 60)` above 60.

</details>

## 3. The three building blocks: min, max, clamp

You can write almost every cap and floor with three functions that every language and engine provides.

- `min(a, b)` returns the smaller value. `min(x, 100)` is a **cap** at 100. It passes `x` through until `x` reaches 100, then holds at 100.
- `max(a, b)` returns the larger value. `max(x, 0)` is a **floor** at 0. It stops a value from going negative.
- `clamp(x, lo, hi)` does both: `clamp(x, lo, hi) = min(max(x, lo), hi)`.

Each of these is a piecewise function in disguise. `min(x, 100)` is exactly:

```
            ⎧ x     if x < 100
min(x,100)= ⎨
            ⎩ 100   if x ≥ 100
```

You will see them in shipped code constantly. In Celeste's published player code, the wall-slide timer drains with `wallSlideTimer = max(wallSlideTimer − dt, 0)`. That is a floor that stops the timer going negative. The same code base has a helper called `Approach(value, target, maxMove)`. It moves a value toward a target by at most `maxMove`, and it is built from exactly one `min` or `max` depending on direction. You will use it again next week.

### Order matters

Once you chain operations, the position of the clamp changes the answer. Take Diablo II's resistance rule and swap the order by mistake:

| Listed fire res | Hell penalty | Correct: clamp(listed − 100, −100, 75) | Wrong: clamp(listed, −100, 75) − 100 |
|---|---|---|---|
| 120 | 100 | 20 | −25 |
| 175 | 100 | 75 | −25 |
| 60 | 100 | −40 | −40 |
| −50 | 100 | −100 | −150 |

The wrong version caps first. So no amount of extra resistance ever helps in Hell, and the floor stops working. In the real game, stacking resistance above 75% is exactly how players prepare for Hell. The order of the clamp is the difference between a working progression and a broken one. When you write a spec, say where each cap applies.

### Caps on the output versus caps on the input

There are two places to cap a stat, and they feel different to players.

- **Cap the output.** Let the stat grow as high as players like, but clamp the effect. Diablo II does this: you can stack 175% listed resistance, but the effect caps at 75%. Players can see they are "overcapped" and trade the extra for something else, or keep it as a buffer against penalties.
- **Cap the input.** Stop the stat itself from rising. Elden Ring does this at 99: you cannot raise Vigor further at all.

Output caps give players room to plan around penalties and debuffs. Input caps are simpler and stop runaway stacking, but they make the last points before the cap feel like the end of a road.

## 4. Continuity, kinks and jumps

Go back to the breakpoint test from section 1. At each breakpoint, compare the two neighbouring pieces.

- **Same value and same slope.** Smooth. The player cannot feel the breakpoint.
- **Same value, different slope.** A kink. The total is continuous but the per-point gain jumps. Soft caps and hard caps live here. Players feel it as "this stat fell off."
- **Different value.** A jump, or **discontinuity**. The total itself leaps. Players feel it as a threshold: "you need exactly 50 to do this."

Jumps are not automatically bad. Celeste's half-gravity rule is a jump in the gravity multiplier from 0.5 to 1, and it works because players never see the number. They feel a slight hang at the top of the jump. Jumps in visible, invested stats are riskier. Suppose a crafting skill jumps from 70% to 100% success at skill 50. Now skill 49 is nearly worthless and skill 50 is mandatory. Every player will grind to 50, stop, and never care about 51.

Here is a quick check you can run on any piecewise stat. Compute the value one unit on each side of every breakpoint. If the difference between those two values is much larger than the per-point gain on either side, you have a jump, and you should decide whether you meant it.

### Smoothing a kink

If you like a soft cap's shape but not its sharp corner, blend the two pieces over a small range instead of switching instantly. The curved formulas on the Elden Ring wiki are one way to do that. Look at the "HP from last point" column. Inside the 40 to 60 piece the gain starts at 26 and tapers to 13 by Vigor 60. So the step down at 61 is from 13 to 6, a drop of 7 HP per point. With straight pieces the same step is from 22.5 to 5.1, a drop of more than 17. The curved piece spreads the falloff across the range instead of saving it all for one breakpoint. Weeks 8 and 9 give you the tools for this: interpolation and easing curves let you blend any two rules smoothly.

## 5. Replacing a cap with a curve

The League of Legends change in patch 10.23 is worth studying because it shows a general fix. The old design used `cooldown = base × (1 − min(c, 0.4))`. Tabulate it for a 10-second ability:

| CDR on items | Effective CDR | Cooldown (s) | Casts per minute |
|---|---|---|---|
| 0% | 0% | 10.0 | 6.0 |
| 20% | 20% | 8.0 | 7.5 |
| 40% | 40% | 6.0 | 10.0 |
| 50% | 40% | 6.0 | 10.0 |

Now ability haste, `cooldown = base × 100 / (100 + h)`:

| Ability haste | Cooldown (s) | Casts per minute |
|---|---|---|
| 0 | 10.0 | 6.0 |
| 25 | 8.0 | 7.5 |
| 50 | 6.67 | 9.0 |
| 100 | 5.0 | 12.0 |
| 150 | 4.0 | 15.0 |

Casts per minute rise by exactly 0.6 for every 10 haste, forever. This is the same move as armor in week 6: the percentage view shows diminishing returns, while the "how much more do I get to act" view is a straight line. The 40% dead zone disappeared because the new function never needs a cap to stay below 100%. It approaches zero cooldown without reaching it.

This is not free. Without a low cap, very high-haste builds become possible, and the designers now have to watch the top end with item prices and item limits. The current wiki does list a hard cap of 500 haste (83.3% cooldown reduction), but it sits far above normal builds; the wiki puts the highest reachable total in a normal match below 300. That cap is a safety rail for exotic cases, not a breakpoint players build toward. A cap is a single, cheap safety rail. A curve is a better experience that needs more ongoing tuning.

Caps also move. League's attack speed cap sat at 2.5 attacks per second from the game's 2009 release until patch 25.S1.3 (February 2025), when Riot raised it to about 3.0. A cap is a number in a data table. Treat it as a live tuning value, not a law of nature.

## In-class activity (25 minutes)

Work in pairs. You are designing a "Stamina" stat for a small action RPG. Stamina can be raised from 10 to 60, and total stamina points (SP) should land between 100 and 300.

1. Choose two soft-cap breakpoints and write a continuous piecewise-linear function for SP. The per-point gain must fall at each breakpoint and must never be zero.
2. Fill a table of SP and per-point gain at Stamina 10, 20, 30, 40, 50 and 60. Verify continuity by computing both neighbouring pieces at each breakpoint.
3. Add a debuff, "Exhausted: −40 SP, minimum 20 SP." Write it as a clamp and decide whether it applies before or after any cap you have. Show one number where the order matters.
4. Trade sheets with another pair. Mark where you think most players will stop investing, and write one sentence on why.

Expected output: one sheet per pair with the function, the table, the debuff rule, and the other pair's annotation.

## Common misconceptions

- **"A soft cap means the stat stops working."** A soft cap only lowers the per-point gain. Elden Ring Vigor still adds HP after 60, about 5 per point. A hard cap is the one where the gain drops to zero.
- **"If the pieces meet at the breakpoint, the curve is smooth."** Meeting only removes jumps. The slope can still change, and a kink is exactly what players feel as falloff.
- **"Order doesn't matter, clamp is just a safety check."** As the Diablo II table shows, clamping before a penalty and clamping after it give different results and different optimal builds.
- **"`<` versus `≤` is a detail."** At the breakpoint itself, the two choices give different values if the function has a jump. Players stand at breakpoints on purpose, so it is the most-tested value in your game.

## Check yourself

1. A game defines `crit = min(0.02 × agility, 0.5)`. At what agility is the cap reached? What is the per-point gain just below and just above it?
2. Write `clamp(x, 0, 100)` as a three-piece function with explicit conditions.
3. A Diablo II character has 140% listed cold resistance and an item that adds +5% to maximum cold resistance. What is their effective cold resistance in Nightmare (penalty 40) and in Hell (penalty 100)? What fraction of cold damage do they take in each?
4. A function is `f(x) = 3x` for `x < 20` and `f(x) = 50 + x` for `x ≥ 20`. Is it continuous at 20? If not, how big is the jump, and which side do players want to be on?

<details>
<summary>Answers</summary>

1. The cap is reached when `0.02 × agility = 0.5`, so agility 25. Below 25 each point adds 0.02 (2 percentage points). Above 25 each point adds 0.
2. `clamp(x, 0, 100) = 0` if `x < 0`, `x` if `0 ≤ x ≤ 100`, `100` if `x > 100`.
3. The cap is `75 + 5 = 80`. Nightmare: `140 − 40 = 100`, clamped to 80, so they take 20% of cold damage. Hell: `140 − 100 = 40`, below the cap, so they take 60%.
4. Left side at 20 gives `3 × 20 = 60`. Right side gives `50 + 20 = 70`. It is not continuous. It jumps by 10 at the breakpoint, so players want to be at exactly 20 or above. Value 19 gives 57, and one point more gives 70, a gain of 13 compared with 1 per point after that.

</details>

## Lab hook

**Lab 07, Stat curves with caps and floors.** Build a spreadsheet that reproduces the Elden Ring Vigor model and the wiki formula side by side, graphs total and per-point gain, and then re-tunes the curve to a brief. See [labs/lab07.md](../labs/lab07.md).

## Sources

- Fextralife, *Elden Ring Wiki*, "HP" and "Vigor" pages (retrieved September 2026, covering the game after the Shadow of the Erdtree expansion). Community formula for HP by Vigor range, HP values at Vigor 1, 10, 25, 40, 60 and 99, and the note that results round down. The formula is community-derived, not published by FromSoftware.
- PC Gamer, "Elden Ring: How much Vigor you need and soft caps explained." Soft caps at 40 and 60.
- League of Legends Wiki, "V10.23" and "Haste" pages (retrieved September 2026). Replacement of cooldown reduction by ability haste in patch 10.23 (preseason 2021, November 2020), the old 40% cap (45% with Cosmic Insight), the formula `base × 100 / (100 + haste)`, and the current hard cap of 500 haste.
- League of Legends Wiki, "Attack speed" and "V25.S1.3" (retrieved September 2026). Attack speed cap of 3.003 after patch 25.S1.3 (February 2025), previously 2.5 since release.
- Diablo Wiki (Fandom archive), "Resistances (Diablo II)" and "Difficulty (Diablo II)." Maximum resistance of 75% (raisable to 95%), minimum of −100, and Lord of Destruction penalties of 0, −40 and −100.
- NoelFB/Celeste repository on GitHub, `Source/Player/Player.cs` (published 2018, MIT licence for the code files only). Half-gravity rule below 40 px/s vertical speed with jump held, and the wall-slide timer floor.
- Warcraft Wiki, "Armor." Classic-era armor formula with a 75% cap, as summarised in MMO303 week 2.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press.

## Interactive spec: examples/w07-soft-cap-curve.html

**Insight the visual must make obvious:** a soft cap is nearly invisible on the total-HP curve and unmistakable on the per-point-gain chart. The student should see a gentle hill on the left and a staircase on the right, driven by the same slider.

**Layout.** Two linked panels side by side on desktop, stacked on mobile (total on top).

- Left panel, "Total HP": x-axis Vigor 1 to 99, y-axis HP 0 to 2,200. Plot two series. (a) "Straight-line model": the piecewise-linear function through (25, 800), (40, 1450), (60, 1900), (99, 2100); below 25 draw it dashed and label it "outside model". (b) "Wiki formula": the four-piece curved formula below, floored to an integer. Draw faint vertical guide lines at Vigor 40 and 60, labelled "soft cap".
- Right panel, "HP from one more point": x-axis Vigor 2 to 99, bars or a step line showing `HP(V) − HP(V − 1)` for the wiki formula, and the three flat model slopes (43.3, 22.5, 5.13) as a step line overlay.

**Controls.**
- Slider "Vigor" (1 to 99, step 1, default 40), keyboard accessible with arrow keys. A marker moves on both panels.
- Toggle "Show wiki formula" (default on) and "Show straight-line model" (default on).
- Mode switch "Curve family": "Elden Ring (soft caps)" (default), "Hard cap (League CDR style)". In hard-cap mode, replace both panels with `effective = min(c, 40)` for c = 0 to 80 (%), showing total as a line with a flat tail and gain as a step from 1 to 0. Include a second series for ability haste converted to casts per minute on a 10 s base, `6 × (1 + h/100)` for h = 0 to 150, on its own y-axis, so students see the cap removed.
- Readout box next to the charts: "Vigor V: model HP = …, wiki HP = …, last point gave +… HP, next point gives +… HP."

**Exact formulas.**
- Model: `800 + (650/15)(V − 25)` for 25 ≤ V ≤ 40; `1450 + 22.5(V − 40)` for 40 < V ≤ 60; `1900 + (200/39)(V − 60)` for 60 < V ≤ 99.
- Wiki (floor the result): V 1 to 25, `300 + 500((V − 1)/24)^1.5`; V 26 to 40, `800 + 650((V − 25)/15)^1.1`; V 41 to 60, `1450 + 450(1 − (1 − (V − 40)/20)^1.2)`; V 61 to 99, `1900 + 200(1 − (1 − (V − 60)/39)^1.2)`.

**Test values (the builder must match these exactly).** Wiki HP: V=1 → 300, 10 → 414, 20 → 652, 25 → 800, 30 → 994, 39 → 1402, 40 → 1450, 41 → 1476, 50 → 1704, 59 → 1887, 60 → 1900, 61 → 1906, 80 → 2015, 99 → 2100. Per-point gain: V=40 → +48, 41 → +26, 60 → +13, 61 → +6. Model: V=30 → 1016.7, 50 → 1675.0, 80 → 2002.6. Hard-cap mode: c=50 → effective 40; haste h=100 → 12.0 casts per minute.

**Constraints.** Draw generic shapes only, no game logos, fonts or icons. Label the wiki formula "community formula (Fextralife, 2026)".
