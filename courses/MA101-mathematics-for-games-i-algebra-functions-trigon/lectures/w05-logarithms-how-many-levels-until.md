# MA101 · Week 05 — Logarithms: "how many levels until…"

**Why this matters:** Players ask "how many more?" all the time. How many more levels until my next unlock, how many more upgrades can I afford, how many more wins until I rank up. When the thing they are counting grows exponentially, the answer is a logarithm. Logarithms also explain why doubling a player's wealth buys the same small handful of upgrades every time, and why a volume slider that works in decibels feels right when one that works in raw amplitude does not.

**You will be able to:**
- Convert between exponential and logarithmic form and compute logarithms in any base with the change-of-base rule.
- Solve "how many steps until" problems for exponential costs, including the number of purchases a budget affords.
- Explain, with a computed table, why each doubling of a budget adds a fixed number of purchases or levels.
- Recognize logarithmic scales in rating systems and audio, and critique when a designer should show a log scale to players.

**Before class:** OpenStax, *College Algebra 2e*, sections 6.3 (Logarithmic Functions), 6.5 (Logarithmic Properties) and 6.6 (Exponential and Logarithmic Equations). Reread section 2 of [last week's lecture](w04-exponentials-and-the-xp-curve.md).

**Prerequisites from earlier courses:** [MA101 week 4, exponentials](w04-exponentials-and-the-xp-curve.md). You need `y = a · b^x`, the doubling interval and the geometric series formula. Inverse functions come from [week 1](w01-functions-as-machines.md).

**Interactive:** [`examples/w05-afford-curve.html`](../examples/w05-afford-curve.html). Keep it open during section 2.

---

## 1. Running an exponential backward

Last week you computed forward. Give the function a level and it tells you the XP. This week you run it backward. Give it the XP and ask which level that is.

A function that undoes another is its **inverse**. The inverse of "raise `b` to the power `x`" is the **logarithm base `b`**, written `log_b`. The two statements below say exactly the same thing:

```
b^x = y        ⇔        x = log_b(y)
```

Read `log_b(y)` as "the power I must raise `b` to in order to get `y`", or more usefully in games, "how many multiplications by `b` it takes to reach `y`". A logarithm **counts multiplications**.

Some values you can compute in your head:

- `log_2(8) = 3`, because `2 · 2 · 2 = 8`.
- `log_10(1,000,000) = 6`, because a million is six multiplications by ten. For whole powers of ten, the log is the number of zeros.
- `log_b(1) = 0` for any base, because zero multiplications leave you at 1.
- `log_2(0.5) = −1`. Halving is one multiplication run backward.

The logarithm is only defined for positive inputs. No number of multiplications by 2 gets you to 0 or to −5.

### Three bases you will meet

- **Base 10**, written `log` or `log10`. Used when people count digits: orders of magnitude, decibels, rating scales.
- **Base 2**, written `log2`. Used when things double: XP curves, binary search, texture mip levels.
- **Base `e ≈ 2.718`**, written `ln` and called the **natural logarithm**. It comes from calculus. You will meet it in MA201, and most code libraries use it as the default (`Math.log` in JavaScript, `math.log` in Python, `Mathf.Log` in Unity with one argument).

### Change of base

Your calculator or engine gives you `ln` and probably `log10`. To get any other base, divide:

```
log_b(y) = ln(y) / ln(b)       (or log10(y) / log10(b), same result)
```

Example: how many times must you multiply by 1.15 to reach 2? That is `log_1.15(2) = ln(2) / ln(1.15) = 0.6931 / 0.1398 = 4.96`. You have now computed exactly the Cookie Clicker doubling interval that last week you could only estimate with the rule of 70.

### The three rules that do all the work

Because a log counts multiplications, it turns multiplying into adding:

```
log(x · y) = log(x) + log(y)
log(x / y) = log(x) − log(y)
log(x^k)   = k · log(x)
```

These hold in any base. The first rule is the one to remember. If you multiply your gold by 8, you add `log_2(8) = 3` to its base-2 log. A function that turns "times" into "plus" is exactly what you want when players think in "how many more".

## 2. Worked example: double your cookies, five more buildings

### The hook

In Cookie Clicker, suppose you have saved 1,000,000 cookies and own no Grandmas. You can buy 52 of them. Save up 2,000,000 instead and you can buy 57. With 4,000,000 you get 62. With 10,000,000, only 68.

Doubling your savings buys five more Grandmas. Doubling again buys five more. Ten times the savings buys about sixteen more. Players feel this as the game running away from them: a huge pile of cookies, and the building count barely moves. Is Cookie Clicker stingy, or is this built into the math? It is built in, and one line of logarithms shows why.

### The model

From last week, the price of the next building when you own `M` is `p · 1.15^M`, where `p` is the base cost (100 for a Grandma). Buying `N` buildings starting from zero costs a geometric series:

```
total(N) = p · (1.15^N − 1) / 0.15
```

Now run it backward. You have `C` cookies. What is the largest `N` with `total(N) ≤ C`? Set them equal and solve for `N`:

```
p · (1.15^N − 1) / 0.15 = C
1.15^N − 1 = 0.15 · C / p
1.15^N     = 1 + 0.15 · C / p
N          = log_1.15(1 + 0.15 · C / p)
           = ln(1 + 0.15 · C / p) / ln(1.15)
```

Round down, because you cannot buy part of a building:

```
N(C) = floor( ln(1 + 0.15 · C / p) / ln(1.15) )
```

- `C` is the cookies you have.
- `p` is the base cost of the building.
- `0.15` is the growth rate, and `1.15` is the growth factor.
- `N` is how many buildings you can afford, starting from none.

When `C` is large, the `1 +` barely matters, and the log rules let you split the expression:

```
N ≈ log_1.15(C) + log_1.15(0.15 / p)
```

The first term is the only one that depends on your cookies. Double `C` and it goes up by `log_1.15(2) = 4.96`. **Every doubling of your cookies adds about five buildings, whatever you started with.** Multiply `C` by 10 and it goes up by `log_1.15(10) = 16.5`.

The second term depends only on the building. A Farm costs 11 times what a Grandma costs, so its count sits `log_1.15(11) ≈ 17.2` buildings lower at every budget. The base cost slides the curve sideways and never changes its shape.

### Numbers you can check

Computed from the formula with Cookie Clicker's base costs. Check two rows on a calculator.

| Cookies C | Cursors (p = 15) | Grandmas (p = 100) | Farms (p = 1,100) |
|---|---|---|---|
| 1,000 | 17 | 6 | 0 |
| 10,000 | 33 | 19 | 6 |
| 100,000 | 49 | 35 | 19 |
| 1,000,000 | 65 | 52 | 35 |
| 2,000,000 | 70 | 57 | 40 |
| 4,000,000 | 75 | 62 | 45 |
| 10,000,000 | 82 | 68 | 51 |

Read down any column. Each row with ten times the cookies adds 16 or 17. Each doubling adds 5. Read across a row: the Grandma column is the Cursor column shifted by about 13 (`log_1.15(100/15) ≈ 13.6`), and the Farm column is the Grandma column shifted by 17.

The same idea works if you already own some. With `M` owned, replace the `1` inside the log with `1.15^M`. If you own 20 Grandmas and hold 1,000,000 cookies, you can afford `floor(log_1.15(1.15^20 + 1,500)) − 20 = 32` more.

### Seeing it move

Open [`examples/w05-afford-curve.html`](../examples/w05-afford-curve.html). The left panel plots buildings affordable against cookies on an ordinary axis from 0 to 10 million. It rockets up at first and then crawls. That view suggests the game is getting stingier. The right panel plots the same thing with cookies on a log axis, where each gridline is double the one before. There the staircase climbs by the same five buildings at every gridline. The game is not getting stingier; it charges the same "price per doubling" the whole way.

Drag the cookies slider and watch both markers. Then change the growth rate from 15% to 7%. The staircase gets steeper on the log view: each doubling now buys `log_1.07(2) ≈ 10.2` buildings. The insight to take away: **for an exponential price, what a doubling of wealth buys is fixed, and the designer sets it with the growth rate.**

### Cross-game recognition

**RuneScape (levels from XP).** Last week's model said total XP is about `720.5 · 2^(L/7) − 796`. Invert it the same way:

```
L ≈ 7 · log_2( (xp + 796) / 720.5 )
```

Every doubling of your XP adds 7 levels. Check against the real table: 1,000,000 XP is level 73, 2,000,000 is level 80, 4,000,000 is level 87. The formula gives 73.1, 80.1 and 87.1. The Cookie Clicker rule with a different constant: five buildings per doubling there, seven levels per doubling here.

**Elo ratings (chess, and many online games).** The Elo rating system, designed for chess, predicts the expected score of player A against player B from the rating gap `D = R_A − R_B`:

```
E = 1 / (1 + 10^(−D/400))
```

Rearrange for the odds, meaning expected wins divided by expected losses:

```
E / (1 − E) = 10^(D/400)
D = 400 · log_10(odds)
```

So the rating gap is a logarithm of the odds. Every 400 points multiplies the odds by 10. A 400-point favorite is expected to score about 0.91 (10 to 1). An 800-point favorite is expected to score 0.99 (100 to 1). The same shape again: a fixed step in the displayed number means a fixed multiplication in the underlying quantity. Note that FIDE, the chess federation, uses a lookup table of rating differences from Elo's original work rather than this exact logistic formula, so treat the formula as the common textbook form.

**Decibels (every game's audio mixer).** Audio engineers measure gain in **decibels (dB)**. For amplitude, the conversion is:

```
dB = 20 · log_10(amplitude)          (amplitude 1 is 0 dB)
```

Halving the amplitude subtracts 6.02 dB. Dividing it by 10 subtracts 20 dB. Unity's Audio Mixer, for example, lets each group's attenuation run from −80 dB, which it treats as silence, up to +20 dB of gain. An options-menu slider usually runs from 0 to 1, and the mixer wants decibels, so a common line of code converts with `20 · log10(v)`, clamping `v` at 0.0001 so the bottom gives −80 dB instead of negative infinity. That treats the slider as amplitude. The top half of such a slider covers only 6 dB, while the bottom tenth covers 60 dB. Some designers instead map the slider linearly onto a decibel range, say −40 to 0 dB, so each tenth of travel changes the level by the same 4 dB, and snap the lowest position to silence. Which one feels better is a playtest question. You can only reason about it once you see that the two choices differ by a logarithm.

Four contexts, one principle. When the thing you care about grows by multiplication, its logarithm grows by addition, and a player-facing number that counts "how many" is usually a logarithm of some hidden quantity.

### Design judgment with eyes open

The five-buildings-per-doubling rule is a design choice with trade-offs you should make on purpose.

- **Strength: it prevents runaway snowballs.** If buildings were priced linearly, a player with 10 times the cookies would buy about 10 times the buildings, which then produce more cookies, and the economy would explode. Exponential prices turn "10 times the cookies" into "16 more buildings", which keeps the count in the dozens or hundreds for years of play.
- **Strength: every budget has a next target.** Because the gap per doubling is constant, there is always a purchase within reach of a few more minutes' saving.
- **Cost: late purchases feel small.** A player who waits all night to double their bank gets five buildings. Idle games answer this with other systems (upgrades that multiply output, prestige resets) that give a multiplicative reward to match the multiplicative cost. If your game has only additive rewards against exponential prices, it will feel like a treadmill.
- **Cost: the displayed number hides a log.** Players compare "I have 52 Grandmas, you have 57" as if it were a small gap. It is a factor of two in spending. When the ranking matters (leaderboards, matchmaking), consider showing the underlying quantity or explaining the scale.
- **Decision: pick the "per doubling" number first.** Decide how many purchases (or levels, or rating points) one doubling of the player's resources should buy. Then the growth rate follows: `b = 2^(1/k)`, where `k` is that number. That is a better starting point than copying 15% from Cookie Clicker.

Questions 1, 2 and 4 in "Check yourself" use this model.

## 3. Solving "how many until" problems

Almost every logarithm question in game design has the same shape. Something is multiplied by `b` every step, it starts at `a`, and you want to know when it reaches a target `T`.

```
a · b^n = T
n = log_b(T / a) = ln(T / a) / ln(b)
```

Then round in the direction that answers the question. For "when does it first reach `T`", round up. For "how many can I afford", round down.

### Exact doubling intervals

Last week's rule of 70 was an estimate. The exact doubling interval of a growth factor `b` is:

```
d = ln(2) / ln(b)
```

| Growth per step | b | Rule of 70 | Exact d |
|---|---|---|---|
| 5% | 1.05 | 14 | 14.2 |
| 10% | 1.10 | 7 | 7.27 |
| 15% | 1.15 | 4.67 | 4.96 |
| 25% | 1.25 | 2.8 | 3.11 |
| 50% | 1.50 | 1.4 | 1.71 |

The rule is good below 15% and drifts after that. For a design document, use the exact form.

The rule of 70 comes from `ln(2) ≈ 0.693` and the fact that `ln(1 + r) ≈ r` when `r` is small. That approximation is why it fails for large rates.

### Last week's two-point problem, finished

Last week you designed a curve where level 1 costs 100 XP and level 50 costs 1,000,000, and got stuck at `b^49 = 10,000`. Take logs of both sides:

```
49 · ln(b) = ln(10,000)
ln(b) = 9.2103 / 49 = 0.18797
b = e^0.18797 = 1.2068
```

The doubling interval is `ln(2) / 0.18797 = 3.69` levels. Every step is a log or its inverse.

### A time problem: rank decay

Suppose a rank-points system removes 3% of a player's points each day they don't play. A player at 2,000 points stops logging in. When do they fall below 1,000?

```
2,000 · 0.97^n < 1,000
0.97^n < 0.5
n > ln(0.5) / ln(0.97) = 22.76
```

They cross 1,000 on day 23. This is a half-life. Notice the division flips signs twice, because both `ln(0.5)` and `ln(0.97)` are negative; if your answer comes out negative, you have divided a negative by a positive somewhere.

### How many levels until a stat hits a target

Suppose a monster's health is `200 · 1.08^L` at level `L`, and your weapon one-shots anything under 5,000 health. From which level does it stop one-shotting?

```
200 · 1.08^L ≥ 5,000
L ≥ ln(25) / ln(1.08) = 41.8
```

From level 42 onward. You can now answer this for any stat curve in seconds, which is exactly what a balance designer does in a spreadsheet all day.

## 4. Logarithmic scales in tools and UI

A **logarithmic scale** places values so that equal distances mean equal ratios. On a log axis, 1 to 10 takes the same space as 10 to 100 and 100 to 1,000. You have already used two: the right panels in this week's and last week's interactives.

Use a log axis whenever the data spans several orders of magnitude and you care about ratios.

- **Balance plots.** Plot monster HP or item prices across 60 levels on a log axis. An exponential curve becomes a straight line, and any level where the designer broke the pattern shows up as a kink. On a linear axis the first 40 levels would be a flat line on the floor.
- **Big-number display.** Idle games display numbers like "1.52 quadrillion". Choosing the suffix is a base-10 logarithm: `floor(log10(x) / 3)` tells you how many groups of three zeros to strip, which picks thousand, million, billion and so on.
- **Audio and brightness sliders.** Human hearing and vision both respond roughly to ratios rather than differences, which is why these sliders often work in log units such as decibels.
- **Sensitivity settings.** A mouse-sensitivity slider that runs from 0.1 to 10 is more usable when the midpoint is 1 (a log mapping) than when it is 5.05 (a linear mapping).

The trade-off: players do not read log axes well. On a log chart, a gap of one gridline might be a factor of 10. For designers' tools, log axes are the default. For players, prefer a derived number that is already logarithmic, like a level or a rank, and label it plainly.

## In-class activity (25 minutes)

Work in groups of three. You are pricing upgrades for a single weapon in a small idle game. The weapon can be upgraded without limit. Players earn resources that roughly double every 30 minutes of play once the game is running.

1. Decide how many upgrades one doubling of resources should buy. Justify your number in one sentence about how often you want the player to press the upgrade button.
2. From that number `k`, compute the growth factor `b = 2^(1/k)` and the growth rate.
3. With a base cost of 50, write `N(C)` for the number of upgrades a budget `C` affords from zero. Fill in a five-row table for `C` = 1,000, 10,000, 100,000, 1,000,000 and 10,000,000.
4. Estimate how many upgrades a player will own after 2 hours and after 6 hours of play, assuming they start with 1,000 and always spend everything.
5. Present your table in 60 seconds. The class votes on which pacing they would rather play, and each group names the rule it used.

**Expected output:** a table, the formula with your `b`, and one sentence of rationale.

## Common misconceptions

- **"log(a + b) = log(a) + log(b)."** The rule is for products: `log(a · b) = log(a) + log(b)`. There is no simple rule for a log of a sum. This is why the `1 +` in the affordability formula had to be dropped as an approximation rather than split off exactly.
- **"Logarithmic growth means it stops growing."** A logarithm grows forever, just slowly. Cookie Clicker's building count never caps. It only needs doubling budgets to keep climbing.
- **"A 400-point Elo gap means the stronger player always wins."** It means expected score about 0.91. The weaker player is still expected to score about 1 in 11.
- **"Halving the volume slider halves the loudness."** Halving amplitude is −6 dB. What people hear as "half as loud" is a larger drop, closer to −10 dB. If your slider is linear in amplitude, the halfway position still sounds nearly as loud as the top.

## Check yourself

1. In Cookie Clicker, a Mine has base cost 12,000. How many Mines can you afford from zero with 50,000,000 cookies? How many more would you get with 200,000,000?
2. You change a game's building price growth from 15% to 10%. How many buildings does one doubling of wealth buy now? Is that more generous or less?
3. A monster's damage is `30 · 1.06^L`. At what level does it first deal at least 300 damage?
4. Using `L ≈ 7 · log_2((xp + 796) / 720.5)`, what RuneScape level does 500,000 XP correspond to? How much XP do you need for 7 levels more than that?
5. Player A is rated 1,700 and player B is rated 1,500. What is A's expected score under the logistic Elo formula?

<details>
<summary>Answers</summary>

1. `N = floor(ln(1 + 0.15 · 50,000,000 / 12,000) / ln(1.15)) = floor(ln(626) / 0.13976) = floor(46.08) = 46`. Two doublings (four times the cookies) add about `2 × 4.96 ≈ 10`, so about 56. (Exact: `floor(ln(2,501)/0.13976) = floor(55.99) = 55`. The approximation overshoots by one because of rounding down; always check the exact formula near a boundary.)
2. `ln(2) / ln(1.10) = 7.27` buildings per doubling. More generous per doubling, since the same savings buy more buildings. The economy will also snowball faster, because output grows with building count.
3. `1.06^L ≥ 10`, so `L ≥ ln(10) / ln(1.06) = 39.5`. First at level 40.
4. `7 · log_2(500,796 / 720.5) = 7 · log_2(695.1) = 7 · 9.44 = 66.1`, so level 66 (the exact table agrees: level 66 starts at 496,254 XP and level 67 at 547,953). Seven more levels needs about double, roughly 1,000,000 XP.
5. `E = 1 / (1 + 10^(−200/400)) = 1 / (1 + 0.316) = 0.76`.

</details>

## Lab hook

**Lab 05: The "how many until" calculator.** You build a spreadsheet that inverts three exponential curves (an XP table, a building price and a decaying rank) and answers player questions with logarithms, then check every answer against brute-force counting. See [`labs/lab05.md`](../labs/lab05.md). Next week, [rational functions](w06-rational-functions-and-asymptotes.md), introduces a third curve family that approaches a limit instead of growing forever.

## Sources

- The Cookie Clicker Wiki (wiki.gg), "Buildings" (current web version, accessed September 2026). Price formula `base cost × 1.15^M` and base costs (Cursor 15, Grandma 100, Farm 1,100, Mine 12,000).
- Old School RuneScape Wiki, "Experience" (accessed September 2026). XP table used to check the inverted formula.
- Wikipedia, "Elo rating system" (accessed September 2026). Logistic expected-score formula with base 10 and scale 400; the statement that each 400 points multiplies the expected-score ratio by ten; the note that FIDE uses Elo's rating-difference table.
- Unity Manual, "AudioGroup Inspector" (Unity 6 documentation, accessed September 2026). Attenuation range from −80 dB (silence) to +20 dB gain.
- OpenStax, *College Algebra 2e* (2021), sections 6.3, 6.5 and 6.6, for logarithm definitions and rules.
- Every other number in this lecture is computed from the formulas above.

## Interactive spec: examples/w05-afford-curve.html

**The one insight:** with exponential prices, a doubling of the player's budget always buys the same number of purchases. On a linear axis the curve looks like it is flattening out; on a log axis it is an even staircase.

**Layout.** Two linked plots, side by side on desktop and stacked on mobile.

- **Left, "Cookies as players count them":** horizontal axis is budget `C` from 0 to `Cmax` on a linear scale. Vertical axis is purchases affordable `N(C)`, drawn as a step function.
- **Right, "Cookies as the math counts them":** same data with `C` on a log2 axis from 1 to `Cmax`, gridlines at every power of 2 (labels every other gridline to avoid crowding). Draw a light bracket between two adjacent gridlines labeled "+X per doubling", where `X = ln(2) / ln(1 + r)` shown to two decimals.
- A vertical marker at the selected budget on both plots.

**Controls (all labeled and keyboard accessible):**

1. Budget slider controlling `log2(C)` from 0 to `log2(Cmax)` in steps of 0.05, so the slider moves evenly in ratios. Display `C` rounded to the nearest whole number with thousands separators. Default `C = 1,000,000`.
2. Growth rate `r`, slider from 2% to 30% in steps of 1%, default 15%.
3. Base cost `p`, select with presets 15 (Cursor), 100 (Grandma, default), 1,100 (Farm), 12,000 (Mine), plus a free number input.
4. Already owned `M`, number stepper 0 to 200, default 0.
5. Buttons "×2" and "÷2" next to the budget slider that double or halve `C`, so students can see the count change by the same amount each press.

**Formulas.**

- Affordable from `M` owned: `N(C) = floor( ln( (1+r)^M + r · C / p ) / ln(1 + r) ) − M`, clamped at 0.
- Cost of the next one: `p · (1 + r)^(M + N)`.
- Per doubling: `ln(2) / ln(1 + r)`.
- `Cmax = 10^9`.

**Readouts (copyable text):** `N(C)`, the price of the next purchase, the per-doubling number, and a row "×2 budget gives N = …" computed live.

**Test values (r = 15%, M = 0):**

| C | p = 15 | p = 100 | p = 1,100 |
|---|---|---|---|
| 1,000 | 17 | 6 | 0 |
| 1,000,000 | 65 | 52 | 35 |
| 2,000,000 | 70 | 57 | 40 |
| 10,000,000 | 82 | 68 | 51 |

With `p = 100`, `M = 20`, `C = 1,000,000`, `N` must read 32. Per doubling must read 4.96 at 15% and 10.24 at 7%.

**First screen:** Grandma preset, `C = 1,000,000`, `N = 52` highlighted, the log panel showing the even staircase with the "+4.96 per doubling" bracket.
