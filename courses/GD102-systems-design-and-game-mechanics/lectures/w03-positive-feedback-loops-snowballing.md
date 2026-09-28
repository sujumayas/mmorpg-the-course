# GD102 · Week 03 — Positive Feedback Loops (Snowballing)

**Why this matters:** "Snowballing" is one of the most common complaints in competitive games, and one of the most misdiagnosed. A small lead that grows by itself can make a game decisive and exciting, or it can make the last twenty minutes a formality. To tune it you need to know which part of the loop actually decides the game, and it is usually not the part players point at.

**You will be able to:**
- Identify a reinforcing loop in a game, write its loop gain `r`, and compute its doubling time.
- Compute, for two players on the same loop, how the absolute gap, the ratio and the time lead change over turns.
- Distinguish independent loops from zero-sum (coupled) loops and predict which one ends games.
- Critique a snowball mechanic by naming the knob (gain, cap, coupling, delay) you would turn and what it costs.

**Before class:** Donella Meadows, *Thinking in Systems: A Primer* (2008), chapter 1, the section on reinforcing loops, and chapter 2, the population and industrial-economy examples. Adams and Dormans, *Game Mechanics: Advanced Game Design* (2012), chapter 3, the section on positive feedback.

**Prerequisites from earlier courses:** [GD102 week 1](w01-systems-thinking-parts-relationships-emergence.md) for loop signs and [GD102 week 2](w02-stocks-and-flows.md) for stocks, flows and flows that depend on stocks. Exponential growth and the doubling interval from [MA101 week 4](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md), and "how many steps until" logarithms from [MA101 week 5](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md). GD101's Monopoly simulation is the first snowball you met ([GD101 week 4, MDA](../../GD101-introduction-to-game-design/lectures/w04-mda-mechanics-dynamics-aesthetics.md), and its [runaway leader simulator](../../GD101-introduction-to-game-design/examples/w04-monopoly-feedback.html)).

**Interactive:** [Snowball: gap vs ratio](../examples/w03-snowball.html). Keep it open during section 2.

---

## 1. The loop that feeds itself

Last week ended with a flow that depends on its own stock: settlers who attract more settlers. Draw it with week 1's signs. More population (+) more arrivals. More arrivals (+) more population. Zero minus signs, so the loop is **reinforcing**. Game designers call it a **positive feedback loop**, and players call what it does **snowballing**.

Every reinforcing loop in a game has the same three parts.

- A **stock** that the player owns: gold, workers, territory, levels, items.
- A **flow into that stock** whose size depends on the stock: income per turn, experience per kill, reinforcements per turn.
- A **conversion** that turns the flow back into more stock: buying workers with gold, conquering territory with armies.

The strength of the loop is its **loop gain** `r`: the fraction by which the stock grows each step when the player reinvests everything. If each worker earns 5 minerals per turn and a new worker costs 50 minerals, then 10 workers earn 50 minerals per turn and buy 1 more worker, a growth of 10% per turn. So `r = 5 / 50 = 0.10`. In general, for a reinvestment loop,

```
r = (income per unit of stock per step) / (cost of one more unit of stock)
```

Two warnings before we go on. First, "positive" means the direction of the loop, not its value to players. The same loop drives a leader ahead and a struggling player further behind, because a loss of stock shrinks the flow that would have replaced it. Second, a reinforcing loop does not run forever in any real game. Something always limits it: a cap, a running-out resource, the end of the match. Where that limit sits turns out to decide more than the loop does.

## 2. Worked example: two economies, one loop

### The hook

In Risk (Parker Brothers rules, 1993 edition), at the start of each turn you count your territories, divide by three and drop the fraction, and receive that many new armies. You never get fewer than 3. A player holding 30 territories gets 10 armies a turn. A player holding 12 gets 4. Armies conquer territories, and territories bring armies. Anyone who has played Risk knows how this feels: once a player gets ahead, every turn seems to widen the gap, and the rest of the table starts talking about ganging up on the leader.

So here is the question for this section. Is the leader pulling away because of the loop that turns territory into armies? Or is something else going on? Answer it with a model small enough to compute by hand, and the answer is surprising.

### The model

Strip the loop down to an RTS-style worker economy. Each player owns a stock of workers and reinvests all income into more workers. With loop gain `r` per turn:

```
S[t+1] = S[t] × (1 + r)          so   S[t] = S[0] × (1 + r)^t
```

Take two players, A and B, on exactly the same loop, with A starting slightly ahead. Three quantities describe the race.

```
gap         G[t] = A[t] − B[t] = (A[0] − B[0]) × (1 + r)^t
ratio       A[t] / B[t] = A[0] / B[0]                         (constant)
time lead   Δt = ln(A[0] / B[0]) / ln(1 + r)                  (constant)
doubling time  t_2 = ln 2 / ln(1 + r)  ≈  0.7 / r  for small r
```

- `S[t]` is a player's workers after `t` turns. `A[0]` and `B[0]` are the starting stocks.
- The **gap** is the lead in workers, the number players see on the scoreboard.
- The **ratio** says how many times bigger A's economy is than B's.
- The **time lead** is how many turns behind A player B is. B will have A's current stock after exactly `Δt` more turns.

### Numbers you can check

Let `r = 0.10`, `A[0] = 12`, `B[0] = 10`.

| Turn | A | B | Gap | Ratio A/B |
|---|---|---|---|---|
| 0 | 12.0 | 10.0 | 2.0 | 1.20 |
| 5 | 19.3 | 16.1 | 3.2 | 1.20 |
| 10 | 31.1 | 25.9 | 5.2 | 1.20 |
| 15 | 50.1 | 41.8 | 8.4 | 1.20 |
| 20 | 80.7 | 67.3 | 13.5 | 1.20 |
| 25 | 130.0 | 108.3 | 21.7 | 1.20 |
| 30 | 209.4 | 174.5 | 34.9 | 1.20 |

The doubling time is `ln 2 / ln 1.1 = 7.27` turns, so the gap doubles roughly every 7 turns: 2, then about 4 around turn 7, about 8 by turn 15, about 16 by turn 22. On the scoreboard this looks exactly like a snowball. After 30 turns A has almost 35 more workers than B, from a start of 2.

But the ratio never moves. A's economy is 1.2 times B's at turn 0 and at turn 30. And the time lead is `ln 1.2 / ln 1.1 = 1.91` turns from start to finish. B is always less than two turns behind A. If the game is "first to 200 workers," A gets there at turn 29.5 and B at turn 31.4. That is the same 1.9 turns.

So a pure, independent reinforcing loop **does not make the leader pull away**. It stretches the absolute gap and keeps everything else fixed. The snowball players feel in the scoreboard is real in absolute numbers and absent in relative ones.

Now add a cap. Real worker economies saturate. A base can only use so many workers. Put a cap of 100 on both players.

| Turn | A | B | Gap |
|---|---|---|---|
| 20 | 80.7 | 67.3 | 13.5 |
| 22 | 97.7 | 81.4 | 16.3 |
| 23 | 100 | 89.5 | 10.5 |
| 24 | 100 | 98.5 | 1.5 |
| 25 | 100 | 100 | 0 |

A's biggest lead ever, 16.3 workers, appears just before the cap and is gone three turns later. An independent loop with a cap hands the trailing player a free catch-up. The lead is only worth something if A spends it on something else before B arrives.

Finally, **couple** the two players. Suppose that each turn, each player takes from the other an amount equal to 10% of their own stock. Raiding, combat or conquest, whatever one side gains, the other loses.

```
A[t+1] = A[t] + c × A[t] − c × B[t]
B[t+1] = B[t] + c × B[t] − c × A[t]
```

With `c = 0.10`, the total `A + B` stays at 22 forever (it is zero-sum), and the gap grows by `2c = 20%` per turn: `G[t] = 2 × 1.2^t`.

| Turn | A | B | Gap | Ratio A/B |
|---|---|---|---|---|
| 0 | 12.00 | 10.00 | 2.00 | 1.20 |
| 2 | 12.44 | 9.56 | 2.88 | 1.30 |
| 4 | 13.07 | 8.93 | 4.15 | 1.46 |
| 6 | 13.99 | 8.01 | 5.97 | 1.75 |
| 8 | 15.30 | 6.70 | 8.60 | 2.28 |
| 10 | 17.19 | 4.81 | 12.38 | 3.58 |
| 12 | 19.92 | 2.08 | 17.83 | 9.56 |
| 13 | 21.70 | 0.30 | 21.40 | 72.2 |

B is eliminated during turn 14. The formula agrees. B reaches zero when the gap equals the total, `2 × 1.2^t = 22`, so `t = ln 11 / ln 1.2 = 13.2` turns. Now the ratio explodes. This is the snowball players complain about, and it comes from the coupling, not from the growth loop. A never grew faster than B in the first model. Here, the richer player is taking from the poorer one, so every step the leader's gain is also the trailer's loss.

That answers the Risk question. Risk's reinforcement loop, by itself, is the first model. What makes Risk leads decisive is that territories are zero-sum. Every territory the leader adds is one someone else loses, along with the armies it would have produced for them.

### A visual you can move

Open `examples/w03-snowball.html`. The left chart plots A and B on an ordinary axis, with the gap shaded between them. The right chart plots the same two lines on a logarithmic axis, where a constant ratio shows up as two parallel lines. In "independent" mode, drag the turn slider forward: the shaded gap on the left swells while the lines on the right stay perfectly parallel. Switch on the cap and watch the gap close. Switch to "zero-sum" mode and the right chart changes character. The lines stop being parallel and B's line dives. Same starting numbers, same growth rate, different coupling.

### Cross-game recognition

Write each game's loop in the same form: what is the stock, what is `r`, and is the loop independent or coupled?

**Risk (1993 rules).** Stock: territories. Flow: `max(3, floor(territories / 3))` armies per turn, plus continent bonuses (Asia 7, North America and Europe 5, Africa 3, South America and Australia 2). The loop is coupled, since territory is taken from other players. Two more rules push it further. When you eliminate a player you take their Risk cards. And the armies for trading in a card set rise for everyone as the game goes on (4, 6, 8, 10, 12, 15, then 5 more for each later set), so each turn's conquest is worth more than the last. The minimum of 3 armies is the one rule working the other way. It props up a player below 9 territories, a small balancing element inside a big reinforcing loop.

**Catan (Kosmos, 1995).** Stock: settlements and cities. A settlement produces one resource card when its number is rolled, a city produces two, and resources buy more settlements and cities. The loop is mostly independent, because building never takes production away from another player. By our model, Catan leads should stay proportional, and players can race for 10 victory points with a real chance to catch up. The coupling Catan does have is small and deliberate: the robber, moved on a 7, blocks one hex's production and lets the mover steal a card. Players commonly aim it at the leader. It turns a little of the coupling against the snowball.

**StarCraft II.** Stock: workers. Flow: minerals gathered per worker. Conversion: minerals buy more workers. That is close to the model in section 2, up to the point where a base saturates, which is the cap. Legacy of the Void (2015) changed the economy by giving players more workers at the start and fewer resources per base. In model terms the first change raises `S[0]`, which skips the early doublings when little happens. With a pure reinforcing loop, doubling the starting stock saves exactly one doubling time. The second change makes bases run out sooner, so players must expand to keep the loop going, and expanding means taking map space an opponent also wants. The designers converted part of an independent loop into a coupled one.

**Monopoly.** In GD101 you simulated wealth concentration. The loop there is money buys properties, properties charge rent, rent brings money. Rent is paid by other players, so it is coupled from the first purchase. That is why Monopoly games end in bankruptcy rather than a close finish.

Four games, one pair of models. When you meet a snowball, ask two questions. What is the loop gain? And does the leader's gain come out of the trailer's stock?

### Design judgment, with eyes open

- **Independent loops are fair and forgiving.** A small lead stays small in relative terms. Players who fall behind can race back. The cost is that early skill matters less than players expect, and games can feel like parallel solitaire. Catan leans this way and adds a little coupling.
- **Coupled loops end games.** They turn small leads into eliminations. That is valuable when the game needs a clear ending, and it is why many strategy games have them on purpose. The cost is the long, joyless tail for the trailing player, who is still playing a game they cannot win. Risk's table talk about the leader is players building a balancing loop the rules did not provide.
- **Caps give catch-up for free.** A cap on an independent loop erases leads. If your game has a saturation point, the leader must convert the lead into a different stock before the cap (army, tech, map control), and that conversion is where skill shows. If you add a cap without a conversion outlet, you have removed the reward for the early lead.
- **Watch the gain, not only the structure.** With `r = 0.02` per turn the doubling time is 35 turns, which may be longer than a match. The loop exists on paper and never matters in play. With `r = 0.3` it doubles every 2.6 turns and the first few turns decide everything. Compute `t_2` and compare it with your match length before you argue about whether a loop is too strong.

### Check yourself (worked example)

1. A game has loop gain `r = 0.05` per minute and matches last 30 minutes. How many doublings happen in a match? Would you expect players to feel a snowball?
2. A starts with 15 workers, B with 10, both on independent loops with `r = 0.2`. What is the time lead? What is the gap after 10 turns?

<details>
<summary>Answers</summary>

1. `t_2 = ln 2 / ln 1.05 = 14.2` minutes, so about 2.1 doublings in 30 minutes. The stock grows about 4.3 times. The absolute gap grows the same 4.3 times, which players may notice, but the ratio and time lead do not change. If there is coupling it will be felt more, since the gap would grow at about `2c`.
2. Time lead `= ln 1.5 / ln 1.2 = 2.22` turns. Gap after 10 turns `= 5 × 1.2^10 = 5 × 6.19 = 31.0` workers.

</details>

## 3. Where snowballs come from

Once you know the shape, you will find reinforcing loops in almost every genre. Some common structures:

- **Reinvestment.** Resources buy producers of resources. Workers, farms, gold mines, idle-game generators. The gain is income per producer divided by producer cost.
- **Kill rewards.** Defeating an enemy gives experience or gold, which makes you stronger, which makes the next kill easier. Most online battle arenas have this loop at the center of the match.
- **Map control.** Holding space gives access to resources or vision, which lets you hold more space. This one is almost always coupled, since space you hold is space the opponent does not.
- **Information.** A player who is ahead often sees more of the map, scouts more, and makes better decisions. It is rarely drawn on a diagram and often matters most.
- **Social loops.** In an MMO, a guild that clears content attracts stronger players, which helps it clear more content. A busy server attracts new players because it is busy. These loops sit outside any single match and can decide which guilds and servers survive a whole expansion.

Two properties to check for every loop you find.

**Delay.** How many steps between gaining stock and getting its extra flow? A worker that starts mining the instant it spawns has no delay. A farm that produces nothing for five turns has a long one. Delay lowers the effective gain and makes the loop feel slower, because the player invests now and sees the return later. Meadows spends much of chapter 2 on delays, and you will see them in week 4 as the cause of overshoot.

**Conversion rate.** Many loops pass through a player decision. Gold becomes workers only if the player chooses to buy workers. A skilled player keeps the loop running at full gain. A distracted player lets gold pile up in a stock that produces nothing. That means some of what looks like snowballing is really a difference in how well players run the same loop. This is the part of the loop that rewards skill, and it is often the part you most want to keep.

## 4. Taming a snowball

Next week covers balancing loops in detail ([GD102 week 4](w04-negative-feedback-loops-rubber-banding.md)). Here is the menu of knobs a designer has for the loop itself, in the terms of this lecture's model.

| Knob | What it changes | Effect on the race | Cost |
|---|---|---|---|
| Lower the gain `r` | slower doubling | gap grows more slowly; ratio still constant | the game feels slower; investment feels less rewarding |
| Add a cap | growth stops at a level | independent leads erased at the cap | leaders need a conversion outlet or early play stops mattering |
| Remove coupling | leader's gain no longer comes from trailer | ratio stays constant | less interaction; games may not end decisively |
| Add delay | returns arrive later | effective gain drops; mistakes cost less | slower feedback to the player's decisions |
| Add a timer or end condition | the game ends before the loop dominates | limits how far any loop can run | a race to the timer instead of a contest |
| Add a balancing loop | trailer gets extra flow, leader loses some | ratio pulled toward 1 | can feel unfair to the leader; the subject of week 4 |

No knob is free. The most common mistake is reaching for a balancing loop (week 4) to fix a snowball that is really coming from coupling. You can often get more by making the loop less zero-sum. For example, give players separate resource sites instead of shared ones, and the ratio stops exploding without any rule that punishes the leader.

Group combat has its own version of this loop, and MMO303 takes it apart with Lanchester's laws. In a fight, the side with more units deals more damage, which kills more enemy units, which reduces the enemy's damage. It is the coupled model with the extra twist that both damage and losses scale with numbers ([MMO303 week 11](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w11-lanchesters-laws-and-group-combat.md)).

## In-class activity (25 minutes)

In pairs, use paper and a calculator, or a spreadsheet if you have one open.

1. (5 min) Pick a competitive game you know. Write down one reinforcing loop in it as stock, flow and conversion. Estimate `r` per minute or per turn from rough numbers you know. Compute `t_2`.
2. (5 min) Decide whether the loop is independent or coupled. Write one sentence of evidence.
3. (8 min) Simulate 10 turns by hand for two players, one starting 20% ahead, under your loop. If it is coupled, use the zero-sum model with `c = r`. Record gap and ratio at turns 0, 5 and 10.
4. (5 min) Choose one knob from the table in section 4 that you would turn and predict its effect on your numbers.
5. (2 min) Trade with another pair and check one of their numbers.

**Expected output:** a loop written in three parts, `r` and `t_2`, a ten-turn table with gap and ratio, and one knob with a predicted effect.

## Common misconceptions

- **"A growing gap means the leader is pulling away."** In an independent loop the gap grows while the ratio and the time lead stay fixed. Ask which quantity decides the game before calling it a snowball.
- **"Positive feedback is good for players."** A reinforcing loop amplifies losses as readily as gains. The player on the wrong side of it is having a worse time every turn.
- **"Every snowball needs a catch-up mechanic."** Many snowballs come from coupling. Reducing the coupling, or adding a cap with a conversion outlet, can fix the problem without any rule that treats players differently by rank.
- **"Doubling the starting resources doubles the pace of the game."** In a reinforcing loop, doubling the starting stock saves one doubling time and nothing more. The game after that point runs exactly as before.

## Check yourself

1. Workers earn 4 minerals per turn each and cost 50 minerals. What is `r`? What is the doubling time? How many turns are saved by starting with 16 workers instead of 8?
2. Two players on an independent loop with `r = 0.15` start at 20 and 16. After how many turns does the trailing player reach 100? How far behind the leader are they at that moment, in turns?
3. The same two players are now coupled with `c = 0.1` (the zero-sum model). What is the total, and how many turns until the trailing player reaches zero?
4. A designer says "our strategy game has a snowball problem, so we'll give the losing player 20% more income." Using this lecture's model, what would you ask about the game first, and what alternative might you suggest?

<details>
<summary>Answers</summary>

1. `r = 4 / 50 = 0.08`. `t_2 = ln 2 / ln 1.08 = 9.0` turns. Starting at 16 instead of 8 is one doubling, so it saves 9.0 turns.
2. `t = ln(100/16) / ln 1.15 = 1.833 / 0.1398 = 13.1` turns. The time lead is `ln(20/16) / ln 1.15 = 0.223 / 0.1398 = 1.6` turns, the same as at the start.
3. Total `= 36`. Gap starts at 4 and grows by 20% per turn: `4 × 1.2^t = 36`, so `t = ln 9 / ln 1.2 = 12.1` turns.
4. Ask whether the loop is coupled: does the leader's gain come out of the trailer's stock? If it does, the ratio explodes because of the coupling, and reducing it (separate resource sites, less value from raiding) may fix the problem without a rank-based rule. If the loop is independent, check whether leads actually matter in time terms before adding a catch-up rule, since the ratio may already be stable.

</details>

## Lab hook

**Lab 03: Snowball simulator** ([labs/lab03.md](../labs/lab03.md)). Build the independent, capped and zero-sum models in a spreadsheet, reproduce this lecture's tables, then add random income and measure how often a 20% early lead wins, first on the independent loop and then on the zero-sum loop.

## Sources

- Parker Brothers (1993). *Risk* rules (Hasbro instruction PDF at hasbro.com/common/instruct/risk.pdf, rules copyright 1959 to 1993, accessed September 2026). Reinforcements equal territories divided by three with fractions dropped, minimum 3 per turn; continent bonuses as on the board; card-set trade-in values 4, 6, 8, 10, 12, 15, then 5 more per later set; eliminating a player gives you their cards.
- Wikipedia, "Risk (game)" (accessed September 2026). Continent bonus table for the standard board (North America 5, South America 2, Europe 5, Africa 3, Asia 7, Australia 2).
- Wikipedia, "Catan" (accessed September 2026). Kosmos, 1995. Settlements produce one resource card and cities two; ten victory points to win; on a 7 the robber moves to block a hex and its mover may steal a card from another player.
- Wikipedia, "StarCraft II: Legacy of the Void" (accessed September 2026). Blizzard, released 10 November 2015. The expansion decreased resource quantities and increased the number of workers at the start of the game. The exact counts are not used in this lecture.
- Meadows, D. H. (2008). *Thinking in Systems: A Primer*. Chelsea Green. Chapters 1 and 2, reinforcing loops, exponential growth and delays. Paraphrased.
- Adams, E. & Dormans, J. (2012). *Game Mechanics: Advanced Game Design*. New Riders. Chapter 3, positive feedback as a mechanism that amplifies differences and helps end games. Paraphrased.
- Wikipedia, "Positive feedback" (accessed September 2026). General definition of a loop in which a change is amplified.

## Interactive spec: examples/w03-snowball.html

**The one insight:** on an independent reinforcing loop, the absolute gap between two players explodes while their ratio stays exactly constant (parallel lines on a log axis); only coupling (the leader's gain coming out of the trailer's stock) makes the ratio explode.

**Layout.** Two linked charts side by side on desktop, stacked on mobile (linear on top). Shared horizontal axis "Turn" from 0 to `T` (default 30).

- **Left chart, "What the scoreboard shows":** A and B on an ordinary vertical axis, the area between them shaded and labeled "gap." If the cap is on, draw it as a dashed line.
- **Right chart, "What actually changes":** the same A and B on a log10 vertical axis (clip values below 0.1 to 0.1 and mark elimination with an "X" on B's line). Under it, a small secondary line of the ratio A/B on its own axis (log scale, 1 to 100).
- A vertical cursor at the selected turn in both charts.
- **Readouts (copyable):** at the selected turn, A, B, gap, ratio (two decimals), time lead `Δt` (independent mode only, two decimals), doubling time `t_2` (two decimals), and in zero-sum mode "B eliminated at turn X.X" from `ln((A0+B0)/(A0−B0)) / ln(1+2c)`.

**Controls (keyboard accessible, labeled):**

1. Mode: "Independent" (default), "Zero-sum."
2. Loop gain `r` (independent) or raid rate `c` (zero-sum), slider 0.01 to 0.40, step 0.01, default 0.10. One slider relabeled by mode.
3. `A0` slider 1 to 50, default 12. `B0` slider 1 to 50, default 10.
4. Cap toggle (independent mode only), with a cap value slider 20 to 500, default 100.
5. Turn slider 0 to `T`, default 10. `T` stepper 10 to 60, default 30.

**Formulas (discrete, one step per turn).**

- Independent: `A[t+1] = min(Cap, A[t] × (1 + r))`, same for B (no min when the cap is off).
- Zero-sum: `A[t+1] = A[t] + c × A[t] − c × B[t]`, `B[t+1] = B[t] + c × B[t] − c × A[t]`. When a value would go below 0, set it to 0 and stop both series (show the elimination marker).
- `t_2 = ln 2 / ln(1 + r)`; `Δt = ln(A0 / B0) / ln(1 + r)` (show "n/a" when `A0 = B0`).

**Test values.**

Independent, `r = 0.10`, `A0 = 12`, `B0 = 10`, no cap:

| Turn | A | B | Gap | Ratio |
|---|---|---|---|---|
| 0 | 12.0 | 10.0 | 2.0 | 1.20 |
| 10 | 31.1 | 25.9 | 5.2 | 1.20 |
| 20 | 80.7 | 67.3 | 13.5 | 1.20 |
| 30 | 209.4 | 174.5 | 34.9 | 1.20 |

`t_2 = 7.27`, `Δt = 1.91`.

Independent with cap 100: turn 22 A = 97.7, B = 81.4; turn 23 A = 100, B = 89.5; turn 24 A = 100, B = 98.5; turn 25 both 100, gap 0.

Zero-sum, `c = 0.10`, `A0 = 12`, `B0 = 10`: turn 4 A = 13.07, B = 8.93, ratio 1.46; turn 10 A = 17.19, B = 4.81, ratio 3.58; turn 13 A = 21.70, B = 0.30; B eliminated during turn 14; formula readout "13.15". Total A + B stays 22.00 every turn.

**First screen:** independent mode, defaults, turn slider at 30, so the left chart shows a large shaded gap (34.9) and the right chart shows two parallel straight lines with the ratio line flat at 1.20. A one-line caption above both: "Gap: 2 → 34.9. Ratio: 1.20 → 1.20." Switching to zero-sum immediately redraws with the caption "Gap: 2 → 21.4. Ratio: 1.20 → 72.2."
