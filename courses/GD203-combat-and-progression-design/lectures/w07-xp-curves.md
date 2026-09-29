# GD203 · Week 07 — XP curves: linear, polynomial, exponential

**Why this matters:** The experience table is the clock of an RPG. Its shape decides where the player's hours go, when the game feels fast, and when it starts to feel like a chore, long before anyone tunes a single monster.

**You will be able to:**
- Compute cumulative XP, per-level cost and the "halfway level" for linear, polynomial and exponential XP curves.
- Rewrite a shipped game's XP table into one of these families and name its growth rate.
- Derive an XP table backwards from a target play time (for example 40 hours over 30 levels) and an XP income curve.
- Critique an XP curve by predicting where players will stall, grind or skip content.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapter on progression and advancement curves; Schreiber, *Game Balance Concepts*, level 7 ("Advancement, Progression and Pacing"). Skim your MA101 notes on exponentials and logarithms.

**Prerequisites from earlier courses:** MA101 week 4, [exponentials and the XP curve](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md), and week 5, [logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md). GD102 week 9, progression systems ([GD102 week 9 lecture](../../GD102-systems-design-and-game-mechanics/lectures/w09-progression-systems-skill-vs-power.md)). GD203 week 4, [time-to-kill and time-to-die](w04-time-to-kill-and-time-to-die.md), because XP income depends on how fast you kill things.

**Interactive:** [XP curve shapes](../examples/w07-xp-curve-shapes.html) (built from the spec at the end of this lecture). Keep it open during section 2.

---

## 1. Three numbers every XP table hides

An XP table looks like a list of big numbers. Each row says how much total experience a character needs to reach a level. Designers and players read it in different ways, so start by naming the three quantities you can pull out of it.

- **Cumulative XP, `T(n)`.** The total experience needed to reach level `n` from level 1. This is the number the table usually prints, and the number a full XP bar represents.
- **Per-level cost, `c(n)`.** The experience needed to go from level `n − 1` to level `n`. It is the difference between two rows, `c(n) = T(n) − T(n − 1)`. This is what the player feels when watching the bar fill after a level-up.
- **Time per level, `t(n)`.** How long level `n` takes to earn. It equals per-level cost divided by XP income, `t(n) = c(n) / I(n)`, where `I(n)` is the XP the player earns per hour at that level. This is what actually paces the game.

The first two come straight from the table. The third needs a second curve, the income curve, which comes from your combat numbers (TTK from week 4, monster XP, quest rewards). Most arguments about "grindy" levels are really arguments about `t(n)`, even when people point at `T(n)`.

One more term. The **cap** `N` is the highest level. A game with levels 1 to 20 has `N = 20` and 19 level-ups.

## 2. Worked example: where does the XP live?

### The hook

Old School RuneScape skills go from level 1 to 99. Players have a saying about them that sounds like a joke and is exactly true: level 92 is half of 99. The game's own wiki lists 6,517,253 total XP for level 92 and 13,034,431 for level 99. Seven levels at the end take as much experience as the first 91 put together.

If you have played the game, you have felt this. The skill levels up every few minutes early on, then a single late level can take a whole evening. The question for a designer is not "is this bad?" It is "what shape of curve produces that, and what would other shapes do?"

### One model, four families

Write the per-level cost `c(n)` for levels `n = 2 … N`. The cumulative total is the sum of all costs so far. Four families cover almost every shipped XP table.

```
Flat:         c(n) = a                    T(n) = a × (n − 1)
Linear:       c(n) = a × (n − 1)          T(n) = a × n(n − 1) / 2       (quadratic total)
Polynomial:   T(n) = a × n^p              c(n) grows like n^(p−1)
Exponential:  c(n) = a × r^(n − 2)        T(n) = a × (r^(n−1) − 1) / (r − 1)
```

- `a` is a scale constant. It sets the size of the numbers and nothing else. Doubling `a` doubles every row and changes no ratios.
- `p` is the polynomial power. `p = 2` is a quadratic total, `p = 3` a cubic total.
- `r` is the exponential growth ratio. Each level costs `r` times the previous one. `r = 1.10` means each level costs 10% more than the last.

The shape parameter (`p` or `r`) is the design decision. The scale constant `a` is bookkeeping.

### The halfway level

Here is the question that makes the families easy to compare. At what level has the player earned half of all the XP in the game? Call it the **halfway level**, `n½`, the first level where `T(n) ≥ T(N) / 2`.

For polynomial totals `T(n) = a × n^p`, solve `n^p = N^p / 2`:

```
n½ = N / 2^(1/p)
```

For exponential costs, the total at level `n` is roughly proportional to `r^n` once `n` is large. Halving it means going back `log_r 2` levels:

```
n½ ≈ N − log(2) / log(r)
```

Look at the two results side by side. For a polynomial, the halfway level is a fixed **fraction** of the cap. For an exponential, it is a fixed **number of levels** before the cap, however high the cap is.

Now apply it to RuneScape. The skill formula adds a term `300 × 2^(ℓ/7)` per level, so the dominant part of the cost doubles every 7 levels. That means `r = 2^(1/7) ≈ 1.104`, and `log_r 2 = 7` exactly. Halfway is `99 − 7 = 92`. The saying is the formula.

### Numbers you can check

Take a 20-level game (`N = 20`) and build one table per family. The table lists per-level cost at a few levels, the total to level 20, the halfway level and the share of all XP spent on the last five level-ups (levels 16 to 20).

| Family | `c(2)` | `c(10)` | `c(20)` | `T(20)` | Halfway level | Share in last 5 levels |
|---|---|---|---|---|---|---|
| Flat, `a = 1,000` | 1,000 | 1,000 | 1,000 | 19,000 | 11 (10.5 exactly) | 26% |
| Linear cost, `a = 1,000` | 1,000 | 9,000 | 19,000 | 190,000 | 15 | 45% |
| Cubic total, `T = n³ − 1` | 7 | 271 | 1,141 | 7,999 | 16 | 58% |
| Exponential, `a = 1,000`, `r = 1.25` | 1,000 | 5,960 | 55,511 | 273,556 | 17 | 68% |

Check two rows by hand. Linear cost: `T(20) = 1,000 × 20 × 19 / 2 = 190,000`, half is 95,000, and `T(14) = 91,000` while `T(15) = 105,000`, so the halfway level is 15. Exponential: `log(2) / log(1.25) = 3.1`, so `n½ ≈ 20 − 3.1 = 16.9`, which rounds up to 17. The formula and the table agree.

Read down the last column. The same 20 levels can put a quarter of the XP in the last five levels, or two thirds. That column is the real personality of the curve.

Now open the interactive. The left view plots per-level cost as bars. Every family starts small, and on a linear axis they all look like "numbers go up." The right view plots the share of total XP earned by each level, with a marker at the halfway level. Switch families and watch the marker slide from the middle of the game toward the end. Then drag the cap from 20 to 99 with the exponential family selected. The halfway marker stays exactly `log_r 2` levels from the end. With a polynomial family it stays at the same fraction of the cap.

### Cross-game recognition

**Old School RuneScape (current, skills 1 to 99).** Total XP for level `L` is one quarter of the sum, over `ℓ = 1 … L − 1`, of `ℓ + 300 × 2^(ℓ/7)`, rounded down. The linear `ℓ` term matters for the first few levels and then disappears next to the doubling term. Rewritten in our form it is exponential with `r = 2^(1/7) ≈ 1.104`. Level 2 needs 83 XP and level 99 needs 13,034,431. The last level alone, 98 to 99, costs 1,228,825 XP, about 9.4% of everything.

**Dungeons & Dragons 3.5 edition (core rules, levels 1 to 20).** The advancement table follows `T(n) = 500 × n × (n − 1)`, so level 2 needs 1,000 XP, level 6 needs 15,000 and level 20 needs 190,000. Each level costs 1,000 more than the one before, which is our linear-cost family with `a = 1,000`. It is the second row of the table above, exactly.

**Pokémon (Generation III onward, "Medium Fast" group).** The total XP to reach level `n` is `n³`, so level 100 needs 1,000,000. The "Fast" and "Slow" groups multiply the same cubic by 0.8 and 1.25, giving 800,000 and 1,250,000 at level 100. Only the scale constant `a` changes, so the shape is identical. The halfway level is `100 / 2^(1/3) ≈ 79.4`, and you can check it: `79³ = 493,039` falls short of 500,000 and `80³ = 512,000` passes it.

Three games, three families, one question. When you meet a new XP table, compute the ratio of consecutive per-level costs. If the ratio is constant, the curve is exponential and `log_r 2` tells you where the halfway point is. If the difference between costs is constant, it is linear cost and quadratic total. If neither, try a power law and fit `p`.

### Eyes-open design judgment

No family is correct. Each one buys something and costs something.

- **Flat cost** makes every level feel the same size. It suits games where levels are rewards in themselves and there are many of them, such as account or battle-pass levels. Its cost is that the power you get per level must also stay flat, or later levels become the cheapest power in the game.
- **Linear cost (quadratic total)** grows slowly and predictably. D&D chose it for a tabletop game where the group advances together and the referee paces sessions. It rarely produces a wall, but it also barely stretches the endgame, so it needs content that scales in XP reward to keep late levels from flying by.
- **Polynomial totals** with `p = 3` put the halfway point around 80% of the cap. That is a strong late stretch without an exponential wall, and the curve is easy to explain.
- **Exponential cost** gives the designer one knob, `r`, and a clean promise that the last `log_r 2` levels hold half the XP. It creates a long, prestigious final stretch, which RuneScape uses on purpose. Level 99 means something because it costs as much as the whole road to 92. The cost is that the final levels can feel like a wall, and any mistake in `r` compounds. At `r = 1.15` over 60 levels, the last level costs `1.15^58 ≈ 3,300` times the first.

The judgment call is where you want the player's hours to go. Decide the halfway level first, as a design statement ("half the XP lives in the last 10% of levels"), then pick the family and parameter that deliver it. Do not pick "exponential because RPGs are exponential."

## 3. XP is only half the clock: income curves

The table alone does not tell you how long a level takes. Players earn more XP per hour as they level, because higher-level monsters and quests pay more. Time per level is the ratio

```
t(n) = c(n) / I(n)
```

Suppose both cost and income grow exponentially, cost by `r` per level and income by `q` per level. Then time per level grows by `r / q` per level. Three cases follow.

- `r = q`. Every level takes the same time. The numbers grow, but the clock is flat.
- `r > q`. Levels take longer as you go. This is the usual choice for a campaign.
- `r < q`. Levels get faster. Almost nobody wants this, and it usually happens by accident when late monsters are given generous XP rewards to feel "epic."

This is why a steep XP table does not prove a game is grindy. RuneScape's late levels cost 10% more XP each, but players also unlock faster training methods, so the time per level grows more slowly than the XP per level. When you critique an XP curve, ask for the income curve before you judge.

It also explains a common tuning accident. A designer doubles the XP a boss gives "as a reward." If bosses are a large share of XP income at that level band, `I(n)` jumps, `t(n)` drops, and players skip the next zone's content because they out-level it. The XP table did not change, yet the pacing broke.

## 4. Designing backwards from a play-time target

A course outcome for GD203 is to build curves that pace a 40-hour game. The safe way to do this is to start from time, not from XP.

**Step 1. Choose the time curve.** Decide how long each level should take. A common choice is exponential time with a modest ratio `g`:

```
t(n) = t₂ × g^(n − 2)          for n = 2 … N
Total time = t₂ × (g^(N−1) − 1) / (g − 1)
```

Set the total to the target and solve for `t₂`, the time of the first level-up.

**Step 2. Choose the income curve.** From your combat numbers, estimate XP per hour at each level. Here we assume `I(n) = I₂ × q^(n − 2)`.

**Step 3. Multiply.** The XP table's per-level cost is `c(n) = t(n) × I(n)`. Sum it for `T(n)`.

Work it through for a 30-level campaign (29 level-ups) of 40 hours, with `g = 1.08`, `I₂ = 600` XP per hour and `q = 1.12`.

`(1.08^29 − 1) / 0.08 = 103.97`, so `t₂ = 2,400 minutes / 103.97 = 23.1` minutes.

| Level `n` | Time `t(n)` (min) | Income `I(n)` (XP/h) | Cost `c(n)` (XP) | Cumulative `T(n)` |
|---|---|---|---|---|
| 2 | 23.1 | 600 | 231 | 231 |
| 5 | 29.1 | 843 | 409 | 1,256 |
| 10 | 42.7 | 1,486 | 1,058 | 5,004 |
| 15 | 62.8 | 2,618 | 2,739 | 14,708 |
| 20 | 92.2 | 4,614 | 7,094 | 39,836 |
| 25 | 135.5 | 8,131 | 18,369 | 104,905 |
| 30 | 199.2 | 14,330 | 47,565 | 273,397 |

Check one row. At level 10, `t = 23.08 × 1.08^8 = 42.7` minutes, `I = 600 × 1.12^8 = 1,486` XP per hour, so `c = 42.7 / 60 × 1,486 = 1,058` XP.

Notice two things. First, the XP per level grows by `1.08 × 1.12 = 1.21` per level, much steeper than the time curve. A reader who sees only the XP table would think the game gets 21% grindier per level. It gets 8% longer per level. Second, half of the 40 hours are used up by level 23 of 30. That is a design statement you can defend or change. If playtesters complain the last seven levels drag, lower `g`, and the XP table follows automatically.

The interactive has a "pacing" tab that runs this exact procedure. Enter hours, levels, `g`, `I₂` and `q`, and it prints the table.

## 5. Caps, walls and what the bar tells the player

Three practical issues come up in every XP design review.

**The session unit.** Players experience levels through sessions. If a typical session is 60 minutes, then in the plan above a level-up happens two or three times per session at the start and once every three sessions at level 30. Designers often add sub-level rewards (new ability ranks, talent points, milestone quests) where `t(n)` exceeds one session, so the player still sees something change every time they play. This is a pacing decision, and UX201 returns to it under reinforcement schedules ([UX201 week 5](../../UX201-game-ux-and-player-psychology/lectures/w05-reinforcement-schedules-and-ethics.md)).

**The cap and what happens after it.** At the cap, XP stops meaning anything unless you convert it. Games handle this with prestige systems, alternative advancement, or by letting XP overflow into another currency. MMO307 covers these under alternative advancement ([MMO307 week 12](../../MMO307-game-balance-ii-pvp-progression-and-endgame/lectures/w12-alternative-advancement-and-account-progression.md)). For now, notice that an exponential curve makes the final levels feel like a prestige system already.

**Visible numbers.** Players read the bar, not the table. A bar that resets to zero each level hides `T(n)` and shows only `c(n)`. That is kind to exponential curves because every bar looks the same size. A bar that shows lifetime XP makes the wall visible. RuneScape shows both, and its "92 is half of 99" folklore exists because players can see the totals.

## In-class activity (25 minutes)

Work in pairs. You are pacing a 25-level single-player RPG for 30 hours.

1. Write one sentence stating where half the play time should fall (for example "by level 18").
2. Use the pacing tab of the interactive, or a spreadsheet, to find `g` that puts half the time at your chosen level. Record `g` and `t₂`.
3. Assume income grows by `q = 1.10` per level with `I₂ = 500` XP per hour. Produce the XP table and write down `c(25)` and `T(25)`.
4. Swap tables with another pair without showing them your sentence from step 1. They compute the halfway level in XP and the halfway level in time from your table. Do both match what you intended? Explain any gap in two sentences.

Expected output is one table per pair, one sentence of intent, and a short note on why the XP halfway level and the time halfway level differ.

## Common misconceptions

- **"Exponential XP means the game gets exponentially grindier."** Only if income is flat. Time per level grows by `r / q`, not by `r`. Always ask for the income curve.
- **"Doubling every number makes the curve steeper."** Multiplying every row by a constant changes `a` only. The halfway level and every ratio stay the same.
- **"A higher cap makes the ending feel longer."** For polynomial curves the halfway level stays at the same fraction of the cap. For exponential curves the last `log_r 2` levels always hold half the XP, so a higher cap makes the early game longer and leaves the prestige stretch the same length.
- **"The table is the pacing."** The table is XP. Pacing is time. They are linked by income, which you tune in combat and quest design.

## Check yourself

1. A game uses exponential per-level costs with `r = 1.06` and a cap of 80. Estimate the halfway level. How many levels hold the second half of the XP?
2. A game's XP table has `T(10) = 10,000`, `T(20) = 80,000` and `T(40) = 640,000`. Which family is it, and what is `p`? Where is the halfway level if the cap is 40?
3. Per-level XP cost grows 12% per level and XP income grows 9% per level. By roughly what percentage does time per level grow? After 20 levels, how many times longer is a level?
4. A designer wants a 50-level game where every level takes exactly 45 minutes. XP income is `I(n) = 400 × 1.1^(n − 2)` XP per hour. Write `c(n)`.

<details>
<summary>Answers</summary>

1. `log(2) / log(1.06) = 11.9`, so `n½ ≈ 80 − 11.9 = 68.1`, which is level 69 in practice. About 12 levels, the last 15% of the level range, hold half the XP.
2. Doubling the level multiplies `T` by 8 each time, so `T = a × n^p` with `2^p = 8`, `p = 3`. The halfway level is `40 / 2^(1/3) = 31.7`, so level 32.
3. Time per level grows by `1.12 / 1.09 = 1.0275`, about 2.75% per level. After 20 levels, `1.0275^20 ≈ 1.72` times longer.
4. `c(n) = t × I(n) = 0.75 h × 400 × 1.1^(n − 2) = 300 × 1.1^(n − 2)` XP. The XP table is exponential with `r = 1.1` even though time per level is flat.

</details>

## Lab / assignment hook

**Lab 07, XP curve and 40-hour pacing sheet** ([labs/lab07.md](../labs/lab07.md)). You build the section 4 procedure as a spreadsheet, fit two shipped XP tables to families, and write a pacing memo. Week 8 extends the same sheet with power curves.

## Sources

- Old School RuneScape Wiki, "Experience" (current game, accessed September 2026). XP formula, table values for levels 2, 10, 50, 92 and 99, and the explanation that seven levels near the top double the total. https://oldschool.runescape.wiki/w/Experience
- Dungeons & Dragons 3.5 edition *Player's Handbook* (2003), character advancement table; formula `500 × n × (n − 1)` as summarised by the d20 community tools and EN World thread "3.5 XP Table". https://www.enworld.org/threads/3-5-xp-table.105812/
- Bulbapedia, "Experience" (Generation III onward), and Serebii, "Experience Points". Medium Fast group `n³`, Fast `0.8 n³`, Slow `1.25 n³`, and level 100 totals of 800,000, 1,000,000 and 1,250,000. https://bulbapedia.bulbagarden.net/wiki/Experience and https://www.serebii.net/games/exp.shtml
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Chapters on progression and curves.
- Schreiber, I. (2010). *Game Balance Concepts*, level 7, "Advancement, Progression and Pacing" (online course). https://gamebalanceconcepts.wordpress.com/

## Interactive spec: examples/w07-xp-curve-shapes.html

**The one insight.** The shape parameter decides where the XP lives. Polynomial curves put the halfway point at a fixed fraction of the cap. Exponential curves put it a fixed number of levels (`log_r 2`) before the cap, whatever the cap is.

**Layout.** Two linked charts side by side on desktop, stacked on mobile, plus a second tab "Pacing".

**Tab 1, "Where the XP lives".**
- Left chart, "Per-level cost `c(n)`". Bar chart, x = level 2 … N, y = XP cost (linear axis). Toggle for log y-axis.
- Right chart, "Share of total XP reached by level". Line chart, x = level 1 … N, y = `T(n) / T(N)` from 0 to 100%. Horizontal guide at 50%. A vertical marker at the halfway level `n½` labelled "Halfway: level X". Shade the region from `n½` to N and label it "Second half of all XP: N − n½ + 1 levels" (or the equivalent count of level-ups).
- Controls.
  - Family radio buttons: Flat, Linear cost, Polynomial total, Exponential.
  - `N` (cap) slider 10 … 120, default 20.
  - `p` slider 1.5 … 4.0, step 0.1, default 3 (visible for Polynomial).
  - `r` slider 1.02 … 1.40, step 0.01, default 1.25 (visible for Exponential).
  - Preset buttons: "RuneScape skill (1 to 99)", "D&D 3.5 (1 to 20)", "Pokémon Medium Fast (1 to 100)".
- Readouts under the charts: `T(N)`, `c(N)`, `c(N) / c(2)`, halfway level (exact integer by search, plus the closed-form estimate), share of XP in the last 5 levels.

**Formulas.**
- Flat: `c(n) = 1000`.
- Linear cost: `c(n) = 1000 × (n − 1)`.
- Polynomial: `T(n) = n^p − 1` for n ≥ 1 (so `T(1) = 0`), `c(n) = T(n) − T(n − 1)`.
- Exponential: `c(n) = 1000 × r^(n − 2)`.
- `T(1) = 0`, `T(n) = T(n − 1) + c(n)`.
- Halfway level: smallest `n` with `T(n) ≥ T(N) / 2`. Closed-form estimate: polynomial `N / 2^(1/p)`, exponential `N − ln 2 / ln r`.
- RuneScape preset uses the exact formula `T(L) = floor( (1/4) × Σ_{ℓ=1}^{L−1} floor(ℓ + 300 × 2^(ℓ/7)) )`, N = 99.
- D&D preset: `T(n) = 500 × n × (n − 1)`, N = 20.
- Pokémon preset: `T(n) = n³`, N = 100 (use `T(1) = 1` exactly as the game table; the share chart uses `T(n)/T(N)`).

**Test values (must match exactly).**
- Flat, N = 20: `T(20) = 19,000`, halfway level 11.
- Linear cost, N = 20: `T(20) = 190,000`, `c(10) = 9,000`, halfway level 15, last-5 share 44.7%.
- Polynomial p = 3, N = 20: `T(20) = 7,999`, halfway level 16.
- Exponential r = 1.25, N = 20: `c(20) = 55,511`, `T(20) = 273,556`, halfway level 17, estimate 16.9.
- RuneScape preset: `T(2) = 83`, `T(10) = 1,154`, `T(92) = 6,517,253`, `T(99) = 13,034,431`, halfway level 92.
- Pokémon preset: `T(79) = 493,039`, `T(80) = 512,000`, halfway level 80.

**Tab 2, "Pacing".**
- Inputs: total hours H (default 40), cap N (default 30), time ratio g (1.00 … 1.20, default 1.08), income at level 2 `I₂` (default 600 XP/h), income ratio q (1.00 … 1.25, default 1.12).
- Computes `t₂ = 60H × (g − 1) / (g^(N−1) − 1)` minutes (use `t₂ = 60H / (N − 1)` when g = 1), `t(n) = t₂ × g^(n−2)`, `I(n) = I₂ × q^(n−2)`, `c(n) = t(n)/60 × I(n)`, cumulative T.
- Chart: two lines on a shared x-axis, "minutes per level" (left axis) and "XP per level" (right axis, log scale option). Mark the level where cumulative time first reaches H/2.
- Table below the chart with columns n, t(n), I(n), c(n), T(n), copyable.
- Test values with defaults: `t₂ = 23.1` min, `t(10) = 42.7`, `c(10) = 1,058`, `c(30) = 47,565`, `T(30) = 273,397` (sum of unrounded values, rounded at display), half the time reached at level 23.

**Accessibility.** All sliders keyboard operable with visible labels and live numeric readouts. Charts have text summaries (halfway level and last-5 share) in an `aria-live` region. Respect reduced motion (no animated transitions).
