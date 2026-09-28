# GD102 · Week 02 — Stocks and Flows

**Why this matters:** Gold, health, lives, energy, rested bonus, cards in hand. Most of the numbers on a game's screen are things that pile up and drain away. If you can separate the pile from the rate that fills it, you can predict how a system behaves over hours or weeks with a spreadsheet, and you can see what a cap on the pile is really asking players to do.

**You will be able to:**
- Classify any game quantity as a stock or a flow by its units, and draw a stock-and-flow diagram for a small system.
- Simulate a stock over time with the update rule `S[t+1] = S[t] + inflow − outflow`, including a cap.
- Compute a capped stock's time to fill and the share of inflow a player wastes for a given return interval.
- Compute the equilibrium level of a stock whose outflow is proportional to its size.

**Before class:** Donella Meadows, *Thinking in Systems: A Primer* (2008), chapter 1, the sections on stocks, flows and dynamic equilibrium (the bathtub examples). Adams and Dormans, *Game Mechanics: Advanced Game Design* (2012), chapter 4, the section on internal economy elements (resources, sources, drains).

**Prerequisites from earlier courses:** [GD102 week 1](w01-systems-thinking-parts-relationships-emergence.md) for elements, relationships and loop signs. Rates and units from [MA101 week 2](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md). Caps written with `min` from [MA101 week 7](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w07-piecewise-caps-and-floors.md).

**Interactive:** [Rested pool: stock and flows](../examples/w02-rested-pool.html). Keep it open during section 3.

---

## 1. Two kinds of number

Look at a character sheet and you will find two kinds of number mixed together.

A **stock** is an amount that exists at a moment. You could freeze the game and count it. Gold in your bag, current health, workers in a base, lives remaining. Its unit is a plain thing: gold, hit points, workers.

A **flow** is a rate at which a stock changes. You cannot see a flow in a single frozen frame. You need two moments and the difference between them. Gold per hour, damage per second, health regenerated per tick. Its unit is a thing per unit of time.

The unit test settles every argument. If the unit has "per second," "per hour" or "per turn" in it, it is a flow. If it does not, it is a stock. [MA101 week 2](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md) drilled you on rates and their units. Here they get a job.

Some common pairs:

| Stock | Inflows | Outflows |
|---|---|---|
| Health (HP) | healing per second, regeneration | damage per second |
| Gold | loot, quest rewards, sales per hour | repairs, purchases, taxes per hour |
| Workers in an RTS base | workers trained per minute | workers killed per minute |
| Lives in a mobile puzzle game | lives restored per half hour | lives lost per failed level |
| Cards in hand | cards drawn per turn | cards played or discarded per turn |

Two words from economics that MMO designers use all the time belong here. A **faucet** is an inflow that creates a resource from nothing, like a monster dropping gold. A **sink** (or drain) is an outflow that destroys it, like a repair bill. Week 7 of this course and the whole of MMO304 (start with its [week 3, faucets, sinks and transformations](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md)) are about balancing faucets and sinks across a player population. This week works with one stock at a time.

## 2. The bathtub rule

Meadows explains stocks with a bathtub. Water flows in through the tap and out through the drain. The water level is the stock. Three facts about a bathtub are true of every stock in every game.

**The stock only changes through its flows.** There is no other way. If you want to know why a player's gold went up, you must find an inflow that was larger than the outflows. Written as a rule you can put in a spreadsheet, with one row per time step:

```
S[t+1] = S[t] + inflow[t] − outflow[t]
```

- `S[t]` is the stock at step `t` (for example, gold at the start of hour `t`).
- `inflow[t]` and `outflow[t]` are the total amounts that flowed in and out during that step.

**The slope of the stock is the net flow.** When inflow exceeds outflow, the stock rises, however large or small it is. When they are equal, the stock is flat, even if huge amounts pass through. A tank holding steady at 50% health while taking 1,000 damage per second and receiving 1,000 healing per second is in a very different situation from a tank at 50% with no damage and no healing, yet the health bar looks identical. The bar shows the stock. The danger is in the flows.

**Stocks are buffers and delays.** Because a stock accumulates, it keeps working after the flows change. A player with 10,000 gold can keep buying for a while after their income stops. A tank with a full health bar survives a few seconds after the healer dies. That delay is what gives players time to react, and it is often the thing a designer is really tuning when they change a maximum.

One consequence surprises new designers. You can raise a stock by reducing its outflow just as well as by increasing its inflow. If players feel poor, doubling loot drops and halving repair costs can produce the same gold level. They do not produce the same game, because the flows are what players experience minute to minute. This is why the design question is almost never "what should the stock be?" but "what flows should produce it?"

### Drawing stocks and flows

The standard notation is simple enough to sketch on a whiteboard.

- A **box** is a stock. Label it with its name and unit.
- A **thick arrow with a valve** (drawn as a small bow-tie or circle on the arrow) is a flow. Label it with its rate.
- A **cloud** at the end of an arrow means "outside the system boundary." A faucet starts at a cloud. A sink ends at one.
- A **thin arrow** from a stock to a valve means "this stock affects this flow." That thin arrow is a relationship from week 1, and it is how loops enter the picture in section 4.

In week 5 you will meet the Machinations notation, where a stock is called a pool and a flow is a resource connection ([week 5](w05-machinations-diagrams-i.md) and [week 6](w06-machinations-diagrams-ii-converters-traders-gates.md)). The ideas are the same. The drawings differ.

## 3. Worked example: the rested pool

### The hook

In World of Warcraft, a character who logs out inside an inn or a capital city comes back with a **rested** bonus. While rested, the character earns double experience from killing monsters and from several gathering activities, and the bonus drains as it is used. The bonus stops growing at one and a half levels' worth of experience. Players quickly learn two habits: always log out in an inn, and do not stay away too long, because past a certain point waiting earns nothing.

That second habit comes from a cap on a stock. Every "energy," "lives" or "stamina" system on a phone uses the same structure. Once you can write the model you can compute the exact return time a design is asking for.

### The model

Measure rested experience in percent of the character's current level. Current retail WoW gives one "bubble," 10% of a level, for every 16 hours logged off in a rest area, and one bubble per 64 hours logged off elsewhere. The cap is 15 bubbles, 150% of a level.

```
while logged off:   R[t+1] = min(Cap, R[t] + i)
while playing:      bonus[t] = min(R[t], X[t]);   R[t+1] = R[t] − bonus[t]
```

- `R[t]` is the rested pool (a stock) at the start of step `t`, in percent of a level.
- `i` is the inflow per step while logged off. With one step = one day, `i = 10% × 24/16 = 15%` per day in a rest area and `10% × 24/64 = 3.75%` per day elsewhere.
- `Cap` is 150%.
- `X[t]` is the base experience the player earns from kills that step. The bonus doubles it, but only up to what is left in the pool.

Two numbers fall straight out of the model and they are what a designer is really choosing.

```
time to fill from empty   T_fill = Cap / i
wasted share of inflow    W(N) = max(0, 1 − Cap / (i × N))   for a player who returns every N steps and drains the pool
```

With `Cap = 150%` and `i = 15%` per day, `T_fill = 10 days`. Outside a rest area it is `150 / 3.75 = 40 days`.

### Numbers you can check

A character logs off in an inn with an empty pool.

| Days logged off | Inflow so far | Rested pool R | Inflow lost to the cap |
|---|---|---|---|
| 0 | 0% | 0% | 0% |
| 1 | 15% | 15% | 0% |
| 2 | 30% | 30% | 0% |
| 4 | 60% | 60% | 0% |
| 6 | 90% | 90% | 0% |
| 8 | 120% | 120% | 0% |
| 10 | 150% | 150% | 0% |
| 12 | 180% | 150% | 30% |
| 14 | 210% | 150% | 60% |

Now compare players who each come back on a fixed schedule and play long enough to use up the whole pool.

| Returns every N days | Inflow per cycle | Stored | Wasted | Wasted share W(N) |
|---|---|---|---|---|
| 3 | 45% | 45% | 0% | 0% |
| 7 | 105% | 105% | 0% | 0% |
| 10 | 150% | 150% | 0% | 0% |
| 14 | 210% | 150% | 60% | 28.6% |
| 20 | 300% | 150% | 150% | 50.0% |
| 30 | 450% | 150% | 300% | 66.7% |

Read the second table as a message from the designer. Anyone who returns within 10 days gets all of it. A player who returns every two weeks loses more than a quarter, and a monthly player loses two thirds. The cap does not punish anyone who plays weekly. It only bites for the occasional player, and it tells them exactly how occasional they can be.

Notice also the playing side of the model. The pool is a buffer that doubles the next stretch of play. A player who returns with 150% and earns 30% of a level per hour of kills uses the bonus up in 5 hours (`min(R, X)` takes 30% per hour from the pool). The cap sets the length of the reward, not only the return time.

### A visual you can move

Open `examples/w02-rested-pool.html`. The top panel plots the pool `R` over 60 days for a player who logs in every `N` days and plays a set number of hours each visit. The flat tops where the line sits on the cap are shaded as "wasted." The bottom panel is a bar chart of the flows each day: inflow above the axis, outflow (bonus used) below it, and inflow lost to the cap in a second color. Drag the return interval from 3 days to 30 and watch the shaded area appear exactly at `N = 10`. Then drag the cap. The top panel changes shape and the bottom panel shows you why: the flows are the same, only the part of the inflow that the stock can hold has changed.

### Cross-game recognition

Rewrite each of these into the same three numbers: inflow `i`, cap, and `T_fill = Cap / i`.

**Candy Crush Saga (King, 2012).** Players begin with five lives, lose one on each failed level, and get one back every half hour. In our form, `Cap = 5 lives`, `i = 2 lives per hour`, `T_fill = 2.5 hours`. The appointment it asks for is much shorter than WoW's. A player who fails five levels in a row and comes back after 6 hours has let 3.5 hours of refill, seven lives' worth, go to waste. The game also sells lives or the currency to buy them, and lets players ask friends for lives. Both are extra inflows added to the same stock, which is exactly where the diagram would tell a designer to put them.

**Catan (Kosmos, 1995).** A player's hand of resource cards is a stock. The inflow is production on each dice roll. The outflows are building and trading. There is no hard cap, but when anyone rolls a 7, every player holding eight or more cards discards half, rounded down. That is a soft cap: an outflow that only switches on when the stock is large. With a 7 on 6 of 36 rolls, a player sitting on 8 cards loses 4 of them about once every six rolls, an expected 0.67 cards per roll. The rule pushes players to spend rather than hoard, which is what a cap usually exists to do. You will meet this kind of outflow again in section 4.

**World of Warcraft outside an inn.** The same stock with a quarter of the inflow gives `T_fill = 40 days`. Designers kept one stock and one cap and used the location of logout to offer two appointment lengths. A player who forgot to find an inn still gets something.

Three games, one model. When you meet a timer-based system, ask for the cap and the inflow and divide. The quotient is the return interval the design is quietly asking for.

### Design judgment, with eyes open

- **A cap turns a stock into an appointment.** `T_fill` is the longest a player can stay away without losing anything. Choose it on purpose, based on how often you want your target player to return. WoW's 10 days suits a weekly player. Candy Crush's 2.5 hours suits someone who plays in short breaks during a day.
- **Waste feels like loss.** A full pool with inflow still arriving shows the player that the game is throwing value away. Some players respond by returning more often, which may be what you want. Others respond with resentment, especially when the inflow is something they could have bought. Decide which reaction you are designing for before choosing the cap.
- **The cap also bounds the reward.** A larger cap gives longer bonus sessions after long absences. That helps players who return after a break catch up with friends. It also makes the bonus larger relative to normal play, which changes how leveling feels for everyone.
- **Framing is part of the design.** The rested pool is presented as a bonus for time away. The same numbers could be presented as a penalty for playing too long (normal speed while rested, half speed once "tired"). Players read those two framings very differently even when the stock and flows are identical.

### Check yourself (worked example)

1. A mobile game gives 1 energy every 6 minutes with a cap of 120. What is `T_fill`? What share of the inflow does a player waste who checks in twice a day, 12 hours apart, and spends all their energy each time?
2. A designer wants WoW-style rested experience that fills in exactly 7 days with the same 150% cap. What inflow per day, and per 16 hours, does that need?

<details>
<summary>Answers</summary>

1. `i = 10` energy per hour, so `T_fill = 120 / 10 = 12 hours`. With `N = 12` hours, `W = max(0, 1 − 120/(10 × 12)) = 0`. They waste nothing. Checking in every 16 hours would waste `1 − 120/160 = 25%`.
2. `i = 150% / 7 ≈ 21.4%` per day, which is `21.4 × 16/24 ≈ 14.3%` of a level per 16 hours, up from 10%.

</details>

## 4. When a flow depends on the stock

So far every flow in this lecture has been fixed: 15% per day, 2 lives per hour. In most interesting systems a flow depends on the stock itself. That is the thin arrow from section 2, from a box back to a valve, and it creates a loop.

There are two cases, and the rest of this course hangs on them.

**Outflow grows with the stock.** Suppose a town has 100 settlers arriving every day, and each day 5% of the current population leaves. The outflow is `0.05 × S`. A bigger town loses more people. The loop is: more population (+) more leaving, more leaving (−) less population. One minus sign, so by week 1's rule it is a balancing loop. The stock rises until the outflow equals the inflow and then stops. That level is the **equilibrium**:

```
S[t+1] = S[t] + I − r × S[t]
equilibrium: I = r × S*   →   S* = I / r
```

With `I = 100` and `r = 0.05`, `S* = 2,000`. Starting from an empty town:

| Day | Population | Inflow | Outflow (5%) |
|---|---|---|---|
| 0 | 0 | 100 | 0 |
| 1 | 100 | 100 | 5 |
| 2 | 195 | 100 | 9.75 |
| 3 | 285.3 | 100 | 14.3 |
| 7 | 603.3 | 100 | 30.2 |
| 14 | 1,024.7 | 100 | 51.2 |
| 30 | 1,570.7 | 100 | 78.5 |
| far future | 2,000 | 100 | 100 |

The stock approaches 2,000 but slows as it gets close, because the gap closes by 5% each day. It reaches half the equilibrium after about 13.5 days, since `0.95^13.5 ≈ 0.5`. Two things follow that a designer can use. The equilibrium depends only on the ratio `I / r`, not on where the stock started. And a proportional outflow is a soft cap with no hard wall, which is often friendlier than a `min` because nothing is ever visibly thrown away. Catan's discard rule is a lumpy version of the same idea. Week 4 takes this loop apart properly under the name negative feedback.

**Inflow grows with the stock.** Now suppose each settler attracts new settlers, so inflow is `g × S`. More population (+) more arrivals, more arrivals (+) more population. No minus signs, so the loop reinforces. There is no equilibrium. The stock grows by the same percentage every step, which is exponential growth, the subject of [MA101 week 4](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md). Next week studies this loop under its game-design name, snowballing.

Most real systems have both. A worker economy has an inflow that grows with workers and a cap from limited resources. A health bar has regeneration that some games scale with maximum health and damage that does not care. When you model a system, the first question after "what are the stocks?" is "which flows depend on which stocks?" The answer tells you which loops you have, and the loops tell you the behavior.

## 5. From diagram to spreadsheet

Every stock-and-flow diagram turns into a spreadsheet the same way, and you will do it in the lab.

1. One column per stock, one row per time step. Pick a step small enough that nothing important happens inside it (a day for rested experience, a second for combat, a turn for a board game).
2. One column per flow. Write each flow's formula using only values from the current row. If a flow depends on a stock, reference that stock's cell in the same row.
3. The next row's stock is this row's stock plus inflows minus outflows. Wrap it in `MIN(cap, ...)` or `MAX(0, ...)` if the stock has limits.
4. Chart the stocks as lines and the flows as bars. The stock line's slope should match the net flow bar in every row. If it does not, you have a bug.

The last step is worth doing every time. It is the bathtub rule used as a unit test.

The step size matters more than it looks. With one step per day, the town example above takes the 5% from the population at the start of each day. With one step per hour and a matching hourly rate, you get a slightly different curve with the same equilibrium. If two versions of your model disagree only in the early rows but agree on the long-run level, the step size is the cause and it usually does not matter. If they disagree on the long-run level, something else is wrong.

## In-class activity (25 minutes)

In groups of three, pick one system from a game you all know: a survival game's hunger, a shooter's ammunition, a card game's mana, a mobile game's energy.

1. (5 min) List every stock and every flow. Put the unit next to each one and apply the unit test.
2. (8 min) Draw the stock-and-flow diagram. Mark each flow as fixed or as depending on a stock. Draw the thin arrows for the ones that depend.
3. (5 min) Find the cap if there is one. Estimate the inflow and compute `T_fill`. Say in one sentence what appointment it asks players for.
4. (5 min) Find one loop. Give its sign by counting minus links. Predict whether the stock settles or runs away.
5. (2 min) One group presents; another group checks their units.

**Expected output:** a labeled diagram, a list of stocks and flows with units, one computed `T_fill` and one signed loop with a prediction.

## Common misconceptions

- **"Income and wealth are the same thing."** Income is a flow (gold per hour). Wealth is a stock (gold). A player can have high income and low wealth if their sinks are large. Designers who tune one while measuring the other get surprising results.
- **"A flat stock means nothing is happening."** A flat stock means inflow equals outflow. Both can be enormous. The health bar of a tank being healed through heavy damage is flat and in constant danger.
- **"To raise a stock, raise its inflow."** Lowering the outflow works equally well on the stock. It changes a different experience. Choose based on what players should feel, not on which number is easier to find.
- **"A cap is a neutral limit."** A cap on a stock with a steady inflow sets an appointment and creates waste for anyone who misses it. That is a behavioral design decision, not a technical one.

## Check yourself

1. Classify each as a stock or a flow and give its unit: a character's mana, mana regeneration, a guild bank's gold, a raid's damage per second, the number of players online, logins per day.
2. A stamina system restores 1 point every 5 minutes, up to 60. A player logs in at 8:00 with 0 stamina and spends nothing until 15:00. How much stamina do they have, and how much inflow did they waste?
3. A kingdom earns 300 gold per day and pays upkeep of 2% of its treasury per day. What is the equilibrium treasury? If the designer wants an equilibrium of 10,000 gold with the same upkeep, what income is needed?
4. A designer says "players complain there is too much gold, so we'll halve the gold drop rate." Name one other flow change that lowers the gold stock, and one way the two changes would feel different to players.

<details>
<summary>Answers</summary>

1. Mana: stock (mana points). Mana regeneration: flow (mana per second). Guild bank gold: stock (gold). Raid DPS: flow (damage per second). Players online: stock (players). Logins per day: flow (logins per day).
2. Inflow is 12 per hour. `T_fill = 60/12 = 5 hours`, so they reach 60 at 13:00. They have 60 at 15:00 and wasted 2 hours of inflow, which is 24 points.
3. `S* = I / r = 300 / 0.02 = 15,000` gold. For 10,000: `I = 0.02 × 10,000 = 200` gold per day.
4. Add or raise a sink, such as repair costs, a marketplace fee or a consumable players must buy. Halving drops makes every kill feel less rewarding. A sink leaves kills feeling the same but makes spending feel more frequent. Players usually notice lower drops more than a small fee.

</details>

## Lab hook

**Lab 02: Stock-and-flow spreadsheet** ([labs/lab02.md](../labs/lab02.md)). Build the rested-pool model and the town-population model from this lecture as spreadsheets, verify them against the tables, then design a capped energy system for a target player and justify its `T_fill` with numbers.

## Sources

- Meadows, D. H. (2008). *Thinking in Systems: A Primer*. Chelsea Green. Chapter 1, stocks and flows, the bathtub, dynamic equilibrium, stocks as buffers and delays, and raising a stock by lowering its outflow. Paraphrased.
- Adams, E. & Dormans, J. (2012). *Game Mechanics: Advanced Game Design*. New Riders. Chapter 4, internal economies, resources, sources and drains. Paraphrased.
- Warcraft Wiki, "Rest" (accessed September 2026; page reflects retail World of Warcraft through Dragonflight-era patches). One bubble of rested experience (10% of the current level) per 16 hours logged off in a rest area, one per 64 hours elsewhere, maximum 15 bubbles (150% of a level); double experience from killing monsters and some gathering while rested. The lecture's per-day rates are computed from these figures.
- Wikipedia, "Candy Crush Saga" (accessed September 2026). King, released 2012. Players begin with five lives, lose one on a failed level, and one is restored every half hour; lives can be requested from friends or bought.
- Wikipedia, "Catan" (accessed September 2026). Kosmos, 1995. When a 7 is rolled, players holding eight or more resource cards discard half, rounded down.

## Interactive spec: examples/w02-rested-pool.html

**The one insight:** a capped stock with a steady inflow wastes nothing until the return interval passes `T_fill = Cap / i`, then wastes a growing share `1 − Cap/(i × N)`. The stock line looks nearly the same either side of that point; the flows panel shows the waste appear.

**Layout.** Two linked panels sharing a horizontal axis "Day" from 0 to 60, stacked vertically at all widths (top panel taller).

- **Top panel, "The stock":** rested pool `R` in percent of a level, vertical axis 0 to `max(Cap, 150) + 10`. Draw the cap as a dashed horizontal line labeled "cap." Shade every interval where `R = Cap` while logged off and inflow is still arriving, labeled "full: inflow wasted." Mark each login day with a small tick on the axis.
- **Bottom panel, "The flows":** one bar per day. Inflow stored (above zero, primary color), inflow wasted (above zero, stacked on top, warning color), bonus used during play (below zero, secondary color). Vertical axis symmetric around zero.
- **Readout block (copyable text):** `T_fill` in days (one decimal), wasted share `W(N)` as a percent with one decimal, total inflow, total stored, total wasted over 60 days, and the sentence "A player who returns every N days loses W% of their rested bonus."

**Controls (keyboard accessible, labeled):**

1. Return interval `N`, slider 1 to 30 days, integer, default 14.
2. Cap, slider 30% to 300% in steps of 10, default 150.
3. Location toggle: "Rest area (15%/day)" default, "Elsewhere (3.75%/day)". Also a "Custom" option that reveals an inflow slider 1% to 50% per day, step 0.25.
4. Hours played per visit, slider 1 to 10, default 5, with base experience per hour fixed at 30% of a level.

**Simulation (one step per day, days 0 to 60).** Start `R = 0`, logged off in the chosen location. Login days are `N, 2N, 3N, ...`. On a non-login day: `stored = min(i, Cap − R)`, `wasted = i − stored`, `R = R + stored`. On a login day, first apply that day's inflow as above, then play: `X = 30% × hours`, `bonus = min(R, X)`, `R = R − bonus`. (Treat the play session as happening at the end of the login day.)

**Formulas for readouts:** `T_fill = Cap / i`; `W(N) = max(0, 1 − Cap/(i × N))` (analytic, shown next to the simulated waste share over complete cycles so students see they agree when the player drains the pool each visit).

**Test values (rest area, i = 15%/day, Cap = 150%, 5 hours per visit so X = 150%):**

| N | T_fill | W(N) | Simulated R at day N before play |
|---|---|---|---|
| 3 | 10.0 | 0.0% | 45% |
| 7 | 10.0 | 0.0% | 105% |
| 10 | 10.0 | 0.0% | 150% |
| 14 | 10.0 | 28.6% | 150% |
| 20 | 10.0 | 50.0% | 150% |
| 30 | 10.0 | 66.7% | 150% |

Elsewhere (3.75%/day), Cap 150%: `T_fill = 40.0`, `W(14) = 0.0%`. Custom inflow 21.43%/day, Cap 150%: `T_fill = 7.0`.

**First screen:** `N = 14`, rest area, cap 150%. The top panel shows four flat shaded stretches on the cap, the bottom panel shows the wasted bars in warning color, and the readout says "A player who returns every 14 days loses 28.6% of their rested bonus." Next to it, a one-line comparison "Return every 10 days: 0.0%."
