# MMO304 · Question bank

MMO304 has no written exam. The course grade is the Models assignment (30%), the telemetry lab (20%) and the final economy spec (50%). This bank feeds those three components in three ways.

- **Models questions.** Each lab that counts toward the Models assignment adds two or three questions from this bank, issued with new numbers (see [models-brief.md](models-brief.md)). The worked solutions here are the marking guide. Keep this file on the instructor side.
- **Quizzes.** Some lab sessions open with an ungraded ten-minute quiz of two questions, to check the class before the lab starts.
- **Vivas.** The telemetry lab ends with a short incident briefing and the final spec ends with a viva. Examiners pick questions from this bank that touch the student's own submission and change the numbers on the spot (see [telemetry-lab-brief.md](telemetry-lab-brief.md) and [final-spec-brief.md](final-spec-brief.md)).

Every question carries a tag with the week or weeks it draws on and one of four types.

- **compute**: apply a lecture model to new numbers and get a number out.
- **explain**: say why a model behaves as it does, in words, with at least one number.
- **design**: choose values or rules that meet a stated goal.
- **critique**: judge someone else's claim, proposal or dashboard reading against a model.

All game settings are invented unless the question names a shipped game. Facts about shipped games are the ones cited in the matching lecture, with the same version or era. Answers were recomputed for this bank. Rounding follows the lectures, usually to whole gold or three significant figures. Instructors changing numbers for a viva should rerun the arithmetic, not scale the old answer.

---

## Week 1: Why virtual economies exist, artificial scarcity

1. **[W01 · compute]** In an invented game the farming wage is `w = 800` gold per hour. A charm drops with chance 2% from a monster that takes 90 seconds to find and kill. Compute the expected hours per copy, the long-run price, and the median and 95th-percentile waits in kills and hours. How much gold is the 95th-percentile player's time worth?

   <details>
   <summary>Answer</summary>

   `t = 90 / 3,600 = 0.025` h. `T = t / p = 0.025 / 0.02 = 1.25` h, so `P = w × T = 800 × 1.25 = 1,000` gold. Median kills `ceil(ln 0.5 / ln 0.98) = ceil(34.3) = 35`, which is 0.875 h. 95th percentile `ceil(ln 0.05 / ln 0.98) = ceil(148.3) = 149` kills, which is 3.73 h. At 800 gold an hour that player spent about 2,980 gold of time on a 1,000-gold charm. The market pays the mean. The unlucky player pays three times it.

   </details>

2. **[W01 · compute]** A sword trades at 9,000 gold. Farmers earn about 1,200 gold per hour elsewhere, and a kill takes 4 minutes. What drop chance is the market implying?

   <details>
   <summary>Answer</summary>

   Read the model backwards. `T = P / w = 9,000 / 1,200 = 7.5` h. `t = 4 / 60 = 0.0667` h. `p = t / T = 0.0667 / 7.5 = 0.0089`, about 0.89%. If the design document says 1%, either the wage is lower than you think or players spend more time per kill than the spreadsheet assumes.

   </details>

3. **[W01 · compute · explain]** A raid can be run once a week. A run takes 2.5 hours and a trinket drops with chance 12% per run. The server has 800 raiders. Compute the hours cost, the mean wait in weeks, the 95th-percentile wait in weeks, and the most copies the server can produce per week. Explain why, if the trinket were tradeable, its price could sit above `w × T` for months.

   <details>
   <summary>Answer</summary>

   `T = 2.5 / 0.12 = 20.8` hours. Mean wait `1 / 0.12 = 8.3` weeks. 95th percentile `ceil(ln 0.05 / ln 0.88) = 24` weeks. Supply is at most `800 × 0.12 = 96` copies a week however hard anyone plays. The pull toward `w × T` works only when farmers can answer a high price by farming more. A weekly lockout caps supply in calendar time, so a high price cannot call out more copies, and the price is set by demand until enough weeks pass.

   </details>

4. **[W01 · critique]** Use the lecture's rare sword (`p = 0.5%`, 2 minutes per kill, `w = 600`). A designer adds a pity rule that guarantees the sword on kill 300 and writes: "Pity only helps unlucky players, it does not change the economy." Test the claim. Then say what a pity rule at 600 kills would do.

   <details>
   <summary>Answer</summary>

   With a guarantee at kill `k`, the mean kills are `(1 − (1 − p)^k) / p`. At `k = 300` that is `(1 − 0.995^300) / 0.005 = (1 − 0.222) / 0.005 = 155.5` kills, against 200 without pity. The long-run price falls from 4,000 to `600 × 155.5 × 2 / 60 ≈ 3,110` gold, a 22% cut. The claim is wrong at this cap. The tail also shrinks from 598 kills (19.9 h) to 300 (10 h). At `k = 600` the mean is 190.1 kills, a price near 3,800 (about 5% lower), and only players beyond the 95th percentile are touched. A pity cap near the 95th percentile changes the tail and barely moves the price. A cap near the mean changes both.

   </details>

## Week 2: Value, functional, hedonic and social

5. **[W02 · compute]** With `S = s × log2(1 / f)` and `s = 1,200` gold per halving, what is the social value of an item owned by 1 in 512 active players? What is it after ownership rises to 1 in 32?

   <details>
   <summary>Answer</summary>

   `log2(512) = 9`, so `S = 10,800`. `log2(32) = 5`, so `S = 6,000`. Ownership rose 16-fold, four halvings undone, and every owner lost `4 × 1,200 = 4,800` gold of social value.

   </details>

6. **[W02 · compute]** A retired title (`q = 0`) is held by 0.4% of active players. Weekly churn is 1.5%. How many weeks until its social value has risen by `2s`?

   <details>
   <summary>Answer</summary>

   Each halving of `f` adds `s`. With `q = 0` the share shrinks by 0.985 a week, so one halving takes `ln 2 / −ln 0.985 = 45.9` weeks. Two halvings take 91.7 weeks, about 21 months. The starting share does not matter, only the churn does.

   </details>

7. **[W02 · compute]** A store mount stays on sale. Each week 5% of non-owners buy it (`q = 0.05`) and churn is 2.5%. With `s = 900` and `H = 1,800`, what ownership share does it approach, and what value does it settle at?

   <details>
   <summary>Answer</summary>

   `f* = q / (q + c) = 0.05 / 0.075 = 66.7%`. `S = 900 × log2(1 / 0.667) = 900 × 0.585 = 526`. `V ≈ 1,800 + 526 = 2,326` gold. The mount ends up worth mostly its looks.

   </details>

8. **[W02 · critique]** A retired event mount is owned by 0.08% of active players. `s = 1,000`, churn is 2% a week. The producer wants to sell it in the store for one week, expects 1.5% of active players to buy, and writes: "New players get something fun and nobody loses anything." Critique this with numbers, including how long owners wait to recover.

   <details>
   <summary>Answer</summary>

   After the sale `f` goes from 0.08% to 1.58%, a factor of 19.75. Social value falls by `log2(19.75) = 4.30` halvings, about 4,300 gold for every existing owner. When the sale ends `q` returns to 0 and `f` halves every `ln 2 / −ln 0.98 = 34.3` weeks, so recovering 4.3 halvings takes about 148 weeks, close to three years. Owners lose value at once and get it back slowly. A good answer also names the alternative: sell a new cosmetic, whose `f` starts near zero, and nobody's existing item loses value.

   </details>

9. **[W02 · compute · explain]** A raid axe's price drops from 18,000 to 5,000 gold in the week the next tier releases. Its ownership share barely moved, and its `H + S` is about 2,000. Estimate `F0` and `r`. Explain why a paper hat from a fixed-supply event can gain value over the same period.

   <details>
   <summary>Answer</summary>

   Before the patch `F0 + 2,000 = 18,000`, so `F0 = 16,000`. After it `F0 × r + 2,000 = 5,000`, so `F0 × r = 3,000` and `r = 0.1875`. The axe kept about 19% of its functional value. The hat has `F = 0`, so a patch cannot take functional value away. With `q = 0` its `f` falls every week through churn, so its `S` rises by `s` each halving. Functional value runs on the developer's calendar. Social value runs on the population.

   </details>

## Week 3: Faucets, sinks and transformations

10. **[W03 · compute]** A server has constant population. Players play `h = 3` hours a day, earn `g = 90` gold per hour and spend `r = 55` per hour on repairs and consumables. Churn is 0.4% a day, the trade tax is 4% and 6% of all money trades each day. Compute the steady state `m*`. What would it be if new players stopped arriving?

    <details>
    <summary>Answer</summary>

    Net income `h(g − r) = 3 × 35 = 105` gold a day. `τv = 0.04 × 0.06 = 0.0024`. `m* = 105 / (0.004 + 0.0024) = 16,406`. On a closed server churn cancels, so `m* = 105 / 0.0024 = 43,750`, 2.7 times higher. The newcomers were doing most of the braking.

    </details>

11. **[W03 · compute]** For the server in question 10, how many days does it take `m` to get halfway from its starting value to `m*`?

    <details>
    <summary>Answer</summary>

    The gap shrinks by `(1 − c − τv) = 0.9936` a day. Halfway when `0.9936^d = 0.5`, so `d = ln 0.5 / ln 0.9936 = 108` days.

    </details>

12. **[W03 · design]** Start from the lecture's scenario B (`h = 2`, `g = 100`, `r = 60`, `c = 0.5%`, `τ = 5%`, `v = 5%`, `m* = 10,667`). The lead wants `m*` at 6,000. Find the repair rate `r` that does it with the tax unchanged. Then find the tax rate that does it with `r = 60`. Recommend one.

    <details>
    <summary>Answer</summary>

    Changing `r`: need `h(g − r) = 6,000 × (0.005 + 0.0025) = 45`, so `g − r = 22.5` and `r = 77.5`. Changing the tax: need `c + τv = 80 / 6,000 = 0.01333`, so `τv = 0.00833` and `τ = 16.7%` at 5% volume. A 17% trade tax pushes trade off the market (week 6 deadweight loss, week 14 on `v`), so the repair change is the safer lever while the server is growing. A good answer adds that on a closed server only the tax gives a ceiling, so the package should keep some stock sink for when growth stops.

    </details>

13. **[W03 · critique]** On a server where new players have stopped arriving (`h = 2`, `g = 100`, no trade tax), a designer raises repairs from `r = 60` to `r = 90` and writes: "This will stop inflation." Critique it.

    <details>
    <summary>Answer</summary>

    Net income falls from 80 to `2 × 10 = 20` gold a day, which is still positive. Repairs are a flow sink. They change the numerator of `m* = h(g − r) / (τv)` and do nothing to the denominator, which is zero with no stock sink. Money per player still rises every day, by `20 / (1 − c)`, a little over 20 gold, forever. The change slows inflation to a quarter of its old speed and leaves it with no ceiling. To get a ceiling, add a stock sink such as a trade tax or upkeep.

    </details>

14. **[W03 · explain]** Classify each rule for money and for items, and for each money sink say whether it is a flow sink or a stock sink: (a) an NPC buys wolf pelts for 3 gold each; (b) a player pays another player 1,000 gold for a cloak through the auction house, which keeps 3%; (c) housing upkeep of 1% of the owner's balance per week; (d) a tailor turns 20 pelts into a cloak; (e) gold sent by mail between two alts.

    <details>
    <summary>Answer</summary>

    (a) Money faucet, item sink. (b) The 970 gold is a transfer, the 30 gold fee is a money sink, the cloak is an item transfer. The fee scales with trade volume and so with the money stock, a stock sink. (c) Money sink, stock sink, since it scales with wealth held. (d) Item transformation: pelt sink and cloak faucet, no money effect. (e) Transfer, no change to `M`. Only (b) and (c) can put a ceiling on money per player.

    </details>

## Week 4: Money supply per capita and inflation

15. **[W04 · critique]** A dashboard shows money supply rising from 150 million to 162 million gold in a month. Active players fell from 50,000 to 45,000. A producer says: "Money supply is up 8%, so prices will rise about 8%." Use `P = m / 20` to test the claim.

    <details>
    <summary>Answer</summary>

    `m` goes from 3,000 to 3,600, so `P` goes from 150 to 180, a rise of 20%, not 8%. Money grew while the population shrank. Always divide by `N`. Week 12 adds a second caution: players who left often keep their gold, so the active supply per active player can differ again.

    </details>

16. **[W04 · compute]** With `m(0) = 3,000`, `n = 60` gold per player-day and no stock sink, on which day does the daily inflation rate first fall below 1%? What is the potion price then, with `P = m / 20`?

    <details>
    <summary>Answer</summary>

    `π(t) = n / m(t − 1) = 60 / (3,000 + 60(t − 1))`. It equals 1% when `m(t − 1) = 6,000`, which is `t − 1 = 50`, so `π(51) = 1%` exactly and day 52 is the first day below. `m(52) = 3,000 + 60 × 52 = 6,120`, so `P = 306`. The rate halved from 2% while prices doubled.

    </details>

17. **[W04 · compute]** A server has `n = 50` and a stock sink `σ = 0.8%` a day, with `P = m / 20`. A quest reward of 250 gold bought 2.5 potions at launch (`P = 100`). What does it buy in the long run? A designer wants a luxury mount to cost 12 average balances once the economy settles. What price should they set?

    <details>
    <summary>Answer</summary>

    `m* = 50 / 0.008 = 6,250`, so the long-run `P = 312.5` and the reward buys `250 / 312.5 = 0.8` potions. The mount should cost `12 × 6,250 = 75,000` gold. Better, index it as `12 × m(t)`, so it keeps its weight on the way there.

    </details>

18. **[W04 · compute]** A fixed basket costs 12,000 gold on day 0 and 13,800 gold on day 45. Compute the index on day 45 and the average daily inflation rate.

    <details>
    <summary>Answer</summary>

    Index `= 100 × 13,800 / 12,000 = 115`. Daily rate `= 1.15^(1/45) − 1 = 0.31%`.

    </details>

19. **[W04 · critique]** A designer proposes: "Gold drops rise with the price index, so a new player's real income stays constant." The server has `m(0) = 2,000`, `P = m / 20`, and base net income `n = 50` at `P = 100`. Model the rule as `n(t) = 50 × P(t) / 100` and describe what happens to `m`. How long does it take `m` to double?

    <details>
    <summary>Answer</summary>

    `n(t) = 50 × (m / 20) / 100 = 0.025 × m`. So `m(t + 1) = 1.025 × m(t)`, exponential growth of 2.5% a day. `m` doubles every `ln 2 / ln 1.025 = 28.1` days and reaches about 8,800 by day 60 (`2,000 × 1.025^60 ≈ 8,800`). The rule turns a straight-line drift into a positive feedback loop (GD102 week 3). Even a 1% stock sink leaves 1.5% daily growth. Index sinks, never faucets.

    </details>

## Week 5: Deflation and hoarding

20. **[W05 · compute]** A server sells `Q = 1,200` potions a day. Newcomers: 800 players with 250 gold each, spending 25% a day. Regulars: 300 players with 2,000 each, spending 6%. Veterans: 100 players with 15,000 each, spending 0.4%. Compute `M`, spending `S`, effective velocity `V` and the price level `P = S / Q`.

    <details>
    <summary>Answer</summary>

    Balances 200,000, 600,000 and 1,500,000, so `M = 2,300,000`. Spending `50,000 + 36,000 + 6,000 = 92,000`. `V = 92,000 / 2,300,000 = 4.0%`. `P = 92,000 / 1,200 = 76.7`. Veterans hold 65% of the gold and produce 6.5% of the spending.

    </details>

21. **[W05 · compute]** On the server in question 20, compare two sinks that each remove 180,000 gold once: (a) every player pays a flat 150 gold; (b) 18 veterans buy a 10,000-gold mount. Compute `P` after each and the change.

    <details>
    <summary>Answer</summary>

    (a) Newcomers keep 100 each (80,000, spending 20,000), regulars 1,850 each (555,000, spending 33,300), veterans 14,850 each (1,485,000, spending 5,940). `S = 59,240`, `P = 49.4`, a fall of 35.6%. Newcomers lost 60% of their savings. (b) Only veterans change: 1,320,000, spending 5,280. `S = 91,280`, `P = 76.1`, a fall of 0.8%. Same gold removed, prices move 45 times as much under (a).

    </details>

22. **[W05 · compute]** Starting from question 20's server, compute `P` in two cases: (a) a returning-player campaign brings back 40 dormant veterans with 15,000 gold each, spending 3% a day; (b) no one returns, but a new raid lifts all current veterans' spending rate from 0.4% to 2%. Keep `Q = 1,200`.

    <details>
    <summary>Answer</summary>

    (a) Extra spending `40 × 15,000 × 0.03 = 18,000`. `S = 110,000`, `P = 91.7`, up 19.6%. (b) Veteran spending becomes `1,500,000 × 0.02 = 30,000`. `S = 116,000`, `P = 96.7`, up 26%. No gold entered the economy in (b). A hoard is inflation that has not happened yet.

    </details>

23. **[W05 · critique]** A live team reports: "Our sinks removed 180,000 gold on Monday and 180,000 on Tuesday, so they were equally effective." Monday's sink was a repair increase paid by everyone. Tuesday's was a guild-hall purchase by veterans. Critique the report and propose a better metric.

    <details>
    <summary>Answer</summary>

    Gold removed says nothing about prices. Using question 21's server, the flat sink cut `P` by about 36% and the veteran sink by under 1%. The effect depends on the spending rate of the players who paid. Report the change in spending `S` (or in the price index) per gold removed, and each cohort's share of balance taken. Repairs hit players who spend. The guild hall hits idle gold.

    </details>

## Week 6: Supply, demand and equilibrium in auction houses

24. **[W06 · compute]** Demand for a flask is `Q_d = 1,500 − 6P` and supply is `Q_s = 300 + 4P`. Find the no-fee equilibrium. Then add a 4% fee charged to sellers. Compute the price buyers pay, the price sellers receive, trades per day, the buyer's share of the wedge, gold removed per day and the deadweight loss.

    <details>
    <summary>Answer</summary>

    `P* = (1,500 − 300) / 10 = 120`, `Q* = 780`. With the fee, `P = 1,200 / (6 + 4 × 0.96) = 1,200 / 9.84 = 121.95`. `P_s = 121.95 × 0.96 = 117.07`. `Q = 1,500 − 6 × 121.95 = 768.3`. Buyer share `d / (b + d) = 4 / 10 = 40%` (check: `1.95 / 4.88`). Gold removed `0.04 × 121.95 × 768.3 ≈ 3,748` a day. Deadweight loss `≈ ½ × 4.88 × 11.7 ≈ 28.6` gold a day.

    </details>

25. **[W06 · compute]** Same curves, no fee. An NPC buys flasks without limit at 130 gold. What happens to the market price, how many flasks go to the NPC each day, and what does it do to the money supply?

    <details>
    <summary>Answer</summary>

    The market price of 120 is below the floor, so the price rises to 130. Buyers want `1,500 − 780 = 720`. Sellers offer `300 + 520 = 820`. The NPC takes 100 a day and pays `100 × 130 = 13,000` gold of new money a day. The NPC buy price is a faucet that switches on when supply outruns demand.

    </details>

26. **[W06 · compute · explain]** Same curves. A patch adds a raid that raises `a` from 1,500 to 1,700. Compute the new equilibrium. In the same patch a herb buff raises `c` from 300 to 500. Compute the equilibrium with both changes and say what a price-only dashboard would report.

    <details>
    <summary>Answer</summary>

    Raid only: `P* = (1,700 − 300) / 10 = 140`, `Q* = 1,700 − 840 = 860`. Both: `P* = (1,700 − 500) / 10 = 120`, `Q* = 980`. The price is back at 120 while volume is up 26% on the baseline. A price-only panel reports "no effect". Watch volume next to price.

    </details>

27. **[W06 · design]** With the curves in question 24, the economy lead wants the flask market to remove 6,000 gold a day. Find the fee (to the nearest 0.1%) and state what buyers and sellers each pay and the lost trades.

    <details>
    <summary>Answer</summary>

    Solve `t × P(t) × Q(t) = 6,000` with `P(t) = 1,200 / (6 + 4(1 − t))`. At `t = 6.4%`, `P = 123.15`, `P_s = 115.27`, `Q = 761.1`, removal about 6,000. Buyers pay 40% of the 7.88-gold wedge (3.15 per flask) and sellers 60% (4.73). Trades fall by about 19 a day, a deadweight loss near 75 gold a day, small next to the 6,000 removed. A first estimate from the 4% row, `3,748 × 6.4 / 4 ≈ 6,000`, is close because removal is nearly proportional to `t` at these rates.

    </details>

28. **[W06 · critique]** A community manager proposes: "Players hate the seller fee. Charge the same 5% to buyers instead and sellers will be better off." Critique it with the week 6 model.

    <details>
    <summary>Answer</summary>

    The economic incidence depends on the slopes, `d / (b + d)` for buyers and `b / (b + d)` for sellers, not on who is charged. Moving the charge to buyers shifts the demand line instead of the supply line, and `P`, `P_s`, `Q` and the split come out the same. With question 24's curves sellers bear 60% either way. The proposal changes which receipt shows the fee, which may be worth doing for clarity, but it gives sellers nothing.

    </details>

## Week 7: Crafting chains and gathering professions

29. **[W07 · compute]** A bow needs 3 planks per attempt, succeeds 90% of the time, and a crafter stat refunds 10% of inputs on that stage. A plank is cut from 2 logs with 80% success. Compute the effective ratio for each stage, the logs per bow and the material cost at 12 gold per log. How far off is the recipe card?

    <details>
    <summary>Answer</summary>

    Plank stage `e1 = 2 / 0.8 = 2.5` logs per plank. Bow stage `e2 = 3 × (1 − 0.1) / 0.9 = 3` planks per bow. `R = 2.5 × 3 = 7.5` logs, cost 90 gold. The recipe card says `2 × 3 = 6` logs (72 gold), so the real chain uses 25% more. The refund and the failure on the bow stage cancel exactly here, which is a coincidence worth pointing out to players.

    </details>

30. **[W07 · compute]** The bow from question 29 costs `C = 90`. Demand is `Q_d = 2,000 − 10P` a day, and a vendor floor sits at 30. Find the experience-crafter volume where price leaves cost. Give the price and value destroyed per bow when `X` is 600, 1,500 and 1,800 a day.

    <details>
    <summary>Answer</summary>

    Threshold `a − bC = 2,000 − 900 = 1,100`. `X = 600`: Case 1, price 90, profit crafters make 500, nothing destroyed. `X = 1,500`: Case 2, `P = (2,000 − 1,500) / 10 = 50`, 40 gold destroyed per bow. `X = 1,800`: `(2,000 − 1,800) / 10 = 20` is below the floor, so the price sticks at 30. Buyers take 1,700, and the 100 surplus bows go to the vendor, which creates 3,000 gold a day. The chain ends in a faucet.

    </details>

31. **[W07 · compute]** The best alternative activity pays 3,000 gold per hour. A miner gathers 150 ore per hour in a quiet zone. Estimate the long-run ore price. On expansion day a zone's nodes produce 3,600 ore per hour in total and 40 gatherers share them. What price is needed before gathering pays there?

    <details>
    <summary>Answer</summary>

    Quiet zone: `p ≈ W / u = 3,000 / 150 = 20` gold. Crowded zone: `u = 3,600 / 40 = 90` per hour, so `p ≈ 3,000 / 90 = 33.3`. Crowding raises the break-even price by two thirds, which is why fresh materials sell high in the first days.

    </details>

32. **[W07 · compute]** In EVE Online (current rules, as cited in the lecture), a blueprint at Material Efficiency 10 cuts materials by 10%, rounds up after multiplying by runs, and never goes below one unit per run. An input is listed at 4 units per run. How many units do 1, 5 and 10 runs need?

    <details>
    <summary>Answer</summary>

    1 run: `4 × 0.9 = 3.6`, rounded up to 4, no saving. 5 runs: `20 × 0.9 = 18`, saving 2. 10 runs: `40 × 0.9 = 36`, saving 4. The formula is `ceil(runs × q × (1 − r))`, which rewards batching.

    </details>

33. **[W07 · critique]** Using question 30's market with `X = 1,500`, a designer proposes removing experience from bow crafting "so bows sell at cost and gatherers earn more." Estimate the change in daily log demand and critique the claim.

    <details>
    <summary>Answer</summary>

    Today 1,500 bows a day are made, pulling `1,500 × 7.5 = 11,250` logs. Without experience crafters, only profit crafters remain and they make what the market takes at cost, 1,100 bows, which is 8,250 logs. Log demand falls by 27%. Bows do sell at cost, which helps crafters, but experience crafters were the gatherers' best customers. Gatherers lose a quarter of their bow-driven sales, and the log price drifts down until gathering pays no better than `W / u`.

    </details>

## Week 8: Item decay, durability and destruction as sinks

34. **[W08 · compute]** A breastplate is created at `F = 150` a day and destroyed at `d = 1.5%` a day. `N = 16,000` players want one, `P_max = 1,200`. Compute the steady stock, mean lifetime, days to half the steady stock from zero, coverage and long-run price with `P ≈ P_max × (1 − S / N)`.

    <details>
    <summary>Answer</summary>

    `S* = 150 / 0.015 = 10,000`. Mean lifetime `1 / 0.015 = 66.7` days. Half after `ln 0.5 / ln 0.985 = 45.9` days. Coverage `10,000 / 16,000 = 62.5%`. Price `1,200 × 0.375 = 450` gold.

    </details>

35. **[W08 · design]** A mid-level helmet should be owned by 30% of the 12,000 players who want one. Players create 90 a day. Choose `d`, then turn it into a per-death destruction chance if the average holder dies 5 times a day.

    <details>
    <summary>Answer</summary>

    `d = F / (c × N) = 90 / (0.3 × 12,000) = 2.5%` a day, a mean lifetime of 40 days. Per death: `(1 − x)^5 = 0.975`, so `x = 1 − 0.975^(1/5) = 0.505%`. The shortcut `0.025 / 5 = 0.5%` is close because `x` is small. A good answer adds a tooltip line so players know zero durability means loss.

    </details>

36. **[W08 · compute]** (a) In Old School RuneScape (current, as cited in the lecture), a fully degraded Barrows set costs 330,000 coins at a non-player repairer, an armour stand charges `NPC price × (1 − Smithing level / 200)`, and the set lasts 15 hours of combat. What does a Smithing 80 player pay per hour of combat? (b) In an invented game, a full repair costs 120 gold and each death costs 10% durability. What is the sink per hour for a player dying 6 times an hour?

    <details>
    <summary>Answer</summary>

    (a) `330,000 × (1 − 80/200) = 198,000` coins, so `198,000 / 15 = 13,200` coins per hour. (b) `6 × 0.10 × 120 = 72` gold per hour. Both are flow sinks that scale with play, so they pace income but cannot cap money per player (week 3).

    </details>

37. **[W08 · explain]** World of Warcraft charges durability on death but never destroys the item. EVE Online destroys a lost ship. Using `S* = F / d`, explain what each rule feeds, and what WoW uses instead to keep gear demand alive.

    <details>
    <summary>Answer</summary>

    WoW's rule sets `d = 0` for gear, so the stock of any item grows as `F × t` until everyone who wants one owns one, and after that new copies sell at the floor. The rule feeds a gold sink, the repair bill. EVE's rule gives `d > 0`, so stock levels off at `F / d` and every destroyed ship is a new sale for builders. It feeds the item economy and crafters. WoW keeps gear demand alive by obsolescence (new tiers remove value on a schedule), by binding, and by consumables whose use supplies the `d`.

    </details>

## Week 9: Commodity money

38. **[W09 · compute]** A game has 25 kinds of tradable goods and no accepted money. How many meetings does a trader expect before one barter trade? How many with money? How many prices does each system need?

    <details>
    <summary>Answer</summary>

    Barter `(G − 1)² = 576` meetings, money `2(G − 1) = 48`. Barter needs `G(G − 1) / 2 = 300` exchange rates, money needs `G − 1 = 24` prices. Barter is 12 times as slow here, and the gap grows with `G`.

    </details>

39. **[W09 · compute]** A money item drops at `F = 60` a day and players consume `d = 0.3%` of the stock a day. Compute the steady stock. A duplication exploit adds 100 extra copies a day for 20 days before it is fixed. How large is the excess when the fix lands, how much are prices quoted in the item raised, and how much excess is left 180 days later?

    <details>
    <summary>Answer</summary>

    `S* = 60 / 0.003 = 20,000`. The excess after 20 days is `100 × (1 − 0.997^20) / 0.003 ≈ 1,944`, a little under 2,000 because the sink removes some. That is 9.7% of the stock, so prices in the item rise about 9.7%. The excess decays by 0.997 a day, halving every `ln 0.5 / ln 0.997 = 231` days. After 180 more days about 1,132 remain, still 5.7% above normal. Twenty days of exploit cost more than a year of raised prices.

    </details>

40. **[W09 · explain]** In Diablo II: Lord of Destruction on Battle.net realms (as cited in the lecture), dying cost a share of all gold carried and stashed equal to character level in percent, capped at 20%. A level-15 player holds 400,000 gold and a level-60 player holds the same. What does one death cost each? Use the answer to explain which of money's three jobs gold failed, and why a ring did not.

    <details>
    <summary>Answer</summary>

    Level 15: 15%, so 60,000 gold. Level 60: capped at 20%, so 80,000. Gold failed as a store of value, because holding it meant losing a share at every death. Rings are not subject to that penalty and never need repair, so a ring in the stash kept its value. The same player who was losing a fifth of their gold per death lost nothing by holding their savings in Stones of Jordan.

    </details>

41. **[W09 · design]** Players can trade these items: (a) a ring with fixed stats that never wears out and is consumed by one rare recipe; (b) a crafting orb that stacks to 20, has one fixed effect, and is destroyed when used; (c) a gem that takes one inventory slot, is destroyed when used to upgrade gear, and whose quality rolls from 1 to 100. Score each against the week 9 properties (durable, uniform, widely wanted, scarce with steady supply, easy to trade, has sinks) at 0, 1 or 2 per row. Which becomes money? Propose one rule that makes the gem usable as money.

    <details>
    <summary>Answer</summary>

    A reasonable scoring: ring 2, 2, 1 or 2, 2, 2, 1 (total 10 or 11); orb 2, 2, 2, 2, 2, 2 (12); gem 2, 0, 2, 2, 1, 2 (9). The orb scores highest because it is uniform, stacks, is wanted by every crafter and destroys itself when used, which gives the money a built-in sink, as in Path of Exile. The ring is a close second and is the money if orbs are cheap. The gem fails "uniform", since every unit needs inspection. Fixing quality to a few grades (for example 1, 2 and 3), each stacking separately, turns it into three uniform goods. Accept other scorings that are argued row by row.

    </details>

42. **[W09 · critique]** For a holiday, a producer proposes doubling the drop rate of the server's money item from 60 to 120 a day for 7 days "as a gift to players." With `d = 0.3%` and `S* = 20,000`, critique the proposal with numbers.

    <details>
    <summary>Answer</summary>

    Extra copies arrive at 60 a day for 7 days. With the sink, the excess at the end is `60 × (1 − 0.997^7) / 0.003 ≈ 416`, about 2.1% of the stock. Prices quoted in the item rise about 2%, and the excess halves only every 231 days. Every player receives more units, but each unit buys less, and savers lose 2% of their wealth. A drop-rate change on a money item is monetary policy. A better gift is a consumable or cosmetic that does not add to the money stock.

    </details>

## Week 10: Market design

43. **[W10 · compute]** Asks for an item are spread evenly from 200 to 260 gold. What price does a buyer expect to pay after checking 5 sellers?

    <details>
    <summary>Answer</summary>

    `E[price] = L + (H − L) / (k + 1) = 200 + 60 / 6 = 210` gold.

    </details>

44. **[W10 · compute]** Same market, with a search cost of 2.5 gold per check. How many sellers should the buyer check, and what is their total expected cost?

    <details>
    <summary>Answer</summary>

    Gain from check `k + 1` is `60 / ((k + 1)(k + 2))`: 10, 5, 3, 2 for the 2nd to 5th checks. The 4th check gains 3, more than 2.5, so take it. The 5th gains 2, less than 2.5, so stop at `k = 4`. Price `200 + 60 / 5 = 212`, total `212 + 4 × 2.5 = 222`. Check: `k = 3` gives 222.5 and `k = 5` gives 222.5.

    </details>

45. **[W10 · compute · explain]** Same market. A seller asks 230. What is the chance they win a buyer who checked them when buyers check 1 seller, and when they check 4? Explain what the difference does to sellers' pricing.

    <details>
    <summary>Answer</summary>

    `P(sale) = ((H − p) / (H − L))^(k − 1)`. At `k = 1` it is 1, so a high ask sells as often as a low one. At `k = 4` it is `(30 / 60)^3 = 12.5%`. When buyers see more sellers, high asks stop selling, and sellers who want sales cut toward `L`. That is the undercutting of a central auction house.

    </details>

46. **[W10 · compute]** A trader buys an item at 400 and can resell it at 450. Using the fee schedules cited in the lecture, compute the break-even resale price and the profit or loss on Guild Wars 2's Trading Post (15% in total) and on Old School RuneScape's Grand Exchange (2% since 29 May 2025, ignore the cap).

    <details>
    <summary>Answer</summary>

    Break-even `s = b / (1 − f)`. Guild Wars 2: `400 / 0.85 = 470.6`. Selling at 450 returns `382.5`, a loss of 17.5. Old School RuneScape: `400 / 0.98 = 408.2`. Selling at 450 returns 441, a profit of 41. The same 12.5% gap is arbitrage in one game and a loss in the other.

    </details>

47. **[W10 · design]** A sailing MMO has 12 commodities and about 400 kinds of ship parts. The designers want new players to pay fair prices for ship parts, and they want a trader career that profits from carrying commodities between four ports. Write the market design as values for search cost, scope, visibility and fees for each good class, and predict one number.

    <details>
    <summary>Answer</summary>

    One sound design. Ship parts: one server-wide order book with bids and asks, reachable in any port, 5% fee on sale. Search cost near zero, so asks bunch near cost and new players pay about `L`. Commodities: one order book per port, visible only in that port, 2% fee. Search cost between ports is the voyage, so prices differ between ports by up to the hauling cost. The trader earns that gap. The predicted number: with a 2% fee, a trader profits on any gap above `1 / 0.98 − 1 = 2.04%`, so a commodity bought at 100 in one port and sold above 102.04 in another pays. Mark down answers that give one design for both good classes, since the brief asks for different outcomes.

    </details>

## Week 11: Real-money trade and gold farming

48. **[W11 · compute]** (a) Your item sits at the 98th percentile of the drop distribution. How many drops do you expect to need for the next upgrade? (b) A player finds 500 items in a season, in a game with market multiplier `M = 20`. How many self-found upgrades do they expect, and how many without a market?

    <details>
    <summary>Answer</summary>

    (a) `1 / (1 − 0.98) = 50` drops. (b) `H(500) = 6.79`, so about 6.8 without a market and `6.79 / 20 = 0.34` with it. The market turned seven "found it myself" moments into one in three seasons.

    </details>

49. **[W11 · compute]** A token costs US$20 and sells for 200,000 gold. Buyers on the black market carry a risk cost of `r = 0.4`. A bot costs $0.25 an hour to run, farms 25,000 gold an hour, and a fresh account costs $40. What is the black-market ceiling per 100,000 gold? What is the longest average account lifetime at which bots can no longer undercut the token? Is the black market alive if bans take 500 hours?

    <details>
    <summary>Answer</summary>

    `p_s = 20 / 200,000` dollars per gold, $10.00 per 100k. Ceiling after risk `10 / 1.4 = $7.14`. The bot makes 0.25 units of 100k per hour, so its hourly cost must reach `7.14 × 0.25 = $1.79` to be priced out. `0.25 + 40 / t ≥ 1.79` gives `t ≤ 26.0` hours. At 500 hours the cost is `(0.25 + 0.08) / 0.25 = $1.32` per 100k, far below the ceiling, so the black market thrives. Speed of detection matters more than thoroughness.

    </details>

50. **[W11 · critique]** A producer says: "Once we sell a gold token, gold sellers are finished, and the token will inflate the economy because people can buy gold." Critique both halves with the week 11 models.

    <details>
    <summary>Answer</summary>

    First half: the token sets a ceiling on the black-market price, `p_s / (1 + r)`. Sellers whose cost per gold is below it keep selling (question 49 shows costs of $1.32 against a $7.14 ceiling). The studio still needs fast bans, account costs or buyer risk to push the floor up. Second half: a token moves existing gold from the player who sells it to the player who buys it. No new gold is created. Bots create gold, since they are an extra faucet. So the inflation risk comes from farming, which the token may reduce, not from the purchase.

    </details>

51. **[W11 · explain]** Name the four policy families from week 11 and give one real-game example of each that the lecture cites, with its date. For a loot-driven game whose core loop is "find better gear", which family damages the loop most, and why, in terms of `M`?

    <details>
    <summary>Answer</summary>

    Ban and enforce (the default in most MMOs, for example Old School RuneScape still bans gold sellers). Restrict trade (RuneScape's trade limit, applied 2 January 2008, removed 1 February 2011 after a 91% referendum vote). Sanction currency (WoW Token from patch 6.1.2, Americas 7 April 2015; EVE's PLEX; Old School RuneScape bonds from 30 March 2015). Sanction items (Diablo III's real-money auction house, June 2012 to 18 March 2014). Sanctioning items does most damage to a gear loop, because it opens every tradable drop to a large pool, raising `M`, so self-found upgrades fall as `H(n) / M` for every player, buyers or not.

    </details>

## Week 12: Economic telemetry and dashboards

52. **[W12 · compute]** A snapshot shows 620,000,000 gold. The ledger logs 44,300,000 of faucets and 41,050,000 of sinks for the day. The next snapshot shows 624,050,000. Compute the reconciliation gap and say whether the week 12 alert (gap above 0.1% of supply) fires.

    <details>
    <summary>Answer</summary>

    Predicted `620.00 + 44.30 − 41.05 = 623.25` million. Gap `624.05 − 623.25 = 0.80` million, which is 0.128% of supply. The alert fires. Likely causes are an untagged faucet from new content, a duplication exploit, or dropped log events. Check whether the gap is concentrated in a few accounts.

    </details>

53. **[W12 · compute]** Base week: potions 12 gold (800 sold), herbs 3 gold (4,000 sold), rings 500 gold (6 sold). Next week: potions 15 (700 sold), herbs 3 (4,000 sold), rings 500 (20 sold). Compute the Laspeyres index, the Paasche index and the change in average transaction price.

    <details>
    <summary>Answer</summary>

    Base basket `12 × 800 + 3 × 4,000 + 500 × 6 = 24,600`. At new prices `15 × 800 + 12,000 + 3,000 = 27,000`, so Laspeyres is 109.8. New spending `15 × 700 + 12,000 + 500 × 20 = 32,500`. New quantities at old prices `12 × 700 + 12,000 + 10,000 = 30,400`, so Paasche is 106.9. Average price goes from `24,600 / 4,806 = 5.12` to `32,500 / 4,720 = 6.89`, up 34.5%. The average triples the real inflation because more rings sold.

    </details>

54. **[W12 · compute · critique]** Total gold held rose from 2.0 billion to 2.1 billion in a month. Monthly active players fell from 80,000 to 70,000. The team writes "supply up 5%, within target." Compute gold per active player and critique the note.

    <details>
    <summary>Answer</summary>

    Per active player: 25,000 to 30,000, up 20%. Part of the held gold belongs to players who left, and it can return with them. The note should report total supply, active supply and active supply per active player, with bots excluded and accounts, not characters, as the denominator.

    </details>

55. **[W12 · explain]** The mob-loot faucet rose 40% this week. Active accounts rose 6%, no patch shipped, and the faucet's top 1% share went from 5% to 30%. What is the most likely cause, which team do you call, and what does the cause do to your per-player metrics?

    <details>
    <summary>Answer</summary>

    Bots farming mob loot. A faucet rising far faster than accounts, concentrated in a few accounts, without a patch, is the bot signature. Call the anti-bot or security team. Bots count as active accounts, so they inflate the denominator. Per-player sink metrics appear to fall, and supply per player looks lower than it is for real players.

    </details>

56. **[W12 · design]** The auction fee sink silently breaks and collects about 5% of its normal amount. Which dashboard panel from week 12 catches it first, with what alert rule? Why do the concentration and reconciliation panels miss it?

    <details>
    <summary>Answer</summary>

    The faucets-and-sinks panel, with "any source moves more than 25% week on week without a patch note" (or a daily version on the 7-day average), catches the fee source dropping by 95%. The sink/faucet ratio line also drops. Reconciliation misses it because the ledger correctly logs the smaller fee, so snapshots and ledger still agree. Concentration misses it because no few accounts gain. The owner is the engineering team that owns the market service.

    </details>

## Week 13: Case studies, EVE, Diablo, RuneScape Grand Exchange

57. **[W13 · compute]** A self-found player has found 999 items. What is the chance their next drop is an upgrade, and how many drops should they expect to wait?

    <details>
    <summary>Answer</summary>

    With `K = 999`, the chance is `1 / (K + 1) = 0.1%`, and the expected wait is 1,000 drops.

    </details>

58. **[W13 · compute]** A game gives `d = 25` drops an hour, and a market has reach `m = 19`. At hour 40, estimate upgrades per hour from play with and without the market, and the hours between upgrades.

    <details>
    <summary>Answer</summary>

    `n = 25 × 40 = 1,000`. Self-found `25 / 1,001 = 0.025` per hour, one every 40 hours (about `1 / t`). Market `K = 20 × 1,000 = 20,000`, rate `25 / 20,001 = 0.00125` per hour, one every 800 hours. The market divides the rate by `1 + m = 20`.

    </details>

59. **[W13 · compute]** Until free trade returned on 1 February 2011, RuneScape's Grand Exchange limited offers to 5% above or below the market price (as cited in the lecture). If an item's true clearing price is 80% above its guide price, what is the fewest number of guide-price updates to reach it?

    <details>
    <summary>Answer</summary>

    Smallest `u` with `1.05^u ≥ 1.8`. `ln 1.8 / ln 1.05 = 12.05`, so 13 updates. Check: `1.05^12 = 1.796`, just short, and `1.05^13 = 1.886`. Throughout, sellers who know the real value hold back, so the item is scarce on the exchange.

    </details>

60. **[W13 · compute]** Under Old School RuneScape's rules since 29 May 2025 (2% tax, capped at 5 million coins per item), what tax is paid on an item selling for 180 million coins, and on one selling for 900 million? Give each as a percentage of the price.

    <details>
    <summary>Answer</summary>

    180 million: `0.02 × 180M = 3.6M`, below the cap, so 2%. 900 million: 2% would be 18M, so the cap applies and the tax is 5M, which is 0.56%. The cap binds above 250 million, so the richest trades pay the lowest rate.

    </details>

61. **[W13 · critique]** A producer says: "Players in our loot game complain they never find upgrades. Double the drop rate." There is no market. Use the self-found model to critique the proposal with numbers.

    <details>
    <summary>Answer</summary>

    Upgrades per hour from play are about `d / (d t + 1) ≈ 1 / t`, whatever `d` is. Doubling `d` gets players to good gear sooner, but at any given hour they still find about one upgrade per `t` hours. Counted by drops, upgrades are `H(n)`. Going from 500 to 5,000 drops only raises `H` from 6.79 to 9.09. More drops push gear quality up faster, which makes each later drop less likely to beat it. Real fixes change the loop: destruction or decay that resets `K`, new tiers, or targeted drops that widen what counts as an upgrade for this character.

    </details>

## Week 14: Designing an economy from scratch

62. **[W14 · compute]** A player earns `F = 15,000` gold a day and pays `S = 5,000` in flat sinks. You want them to settle near 500,000 gold. What proportional rate `s` do you need, and what is the half-life?

    <details>
    <summary>Answer</summary>

    `N = 10,000`. `s = N / W* = 10,000 / 500,000 = 0.02` a day. Half-life `ln 2 / 0.02 = 34.7` days.

    </details>

63. **[W14 · compute]** A market tax of 2.5% applies to players who sell 40% of their holdings a day, and a luxury sink takes 0.5% of holdings a day. With `N = 4,500`, compute `s`, `W*`, the half-life and the days to reach 90% of `W*`.

    <details>
    <summary>Answer</summary>

    `s = 0.025 × 0.4 + 0.005 = 0.015`. `W* = 4,500 / 0.015 = 300,000`. Half-life `ln 2 / 0.015 = 46.2` days. 90% after `ln 10 / 0.015 = 153.5` days.

    </details>

64. **[W14 · compute · explain]** Using question 63's economy (`s = 0.015`, `W* = 300,000`), compute the server average wealth when players stay 60 days and when they stay 120 days. Explain what a dashboard showing only the server average would report after a content update that doubles the typical stay.

    <details>
    <summary>Answer</summary>

    `server average = W* × (1 − (1 − e^(−sL)) / (sL))`. At `L = 60`, `sL = 0.9`, share `1 − 0.593 / 0.9 = 34.1%`, about 102,200 gold. At `L = 120`, `sL = 1.8`, share 53.6%, about 160,900. The average rises by a factor of 1.57 with no change to any faucet or sink. A server-average panel reports this as inflation. Segment wealth by account age before touching a sink.

    </details>

65. **[W14 · critique]** In question 62's economy (`F = 15,000`, `S = 5,000`, `s = 0.02`), a designer doubles every faucet and writes: "Players will now take twice as long to reach the ceiling." Compute the new `W*` and half-life, and the day a new player first holds 200,000 gold before and after.

    <details>
    <summary>Answer</summary>

    `F = 30,000`, `N = 25,000`, `W* = 1,250,000`. The half-life stays `ln 2 / 0.02 = 34.7` days, because it depends only on `s`. Before: solve `500,000 (1 − e^(−0.02t)) = 200,000`, so `t = ln(1 / 0.6) / 0.02 = 25.5` days. After: `1,250,000 (1 − e^(−0.02t)) = 200,000`, so `t = ln(1 / 0.84) / 0.02 = 8.7` days. The ceiling moved up 2.5 times, the approach speed stayed the same, and a fixed amount arrives three times sooner.

    </details>

66. **[W14 · design]** Your market tax is 1.5% of each sale, capped at 3 million gold per sale. Above what sale price does the tax stop being proportional? Propose one change that keeps a ceiling on the richest players' wealth without taxing every trade more.

    <details>
    <summary>Answer</summary>

    The cap binds at `3,000,000 / 0.015 = 200` million gold. Above that the effective `τ` falls as price rises, so the richest traders have the lowest `s` and the highest `W*`. One fix is to raise or remove the cap on the few very expensive trades. Another is a second proportional sink that reaches the top without touching ordinary trade, such as luxury goods priced near the 99th-percentile balance or property upkeep that scales with holdings. Either restores a working `s` at the top.

    </details>

## Cross-week questions

67. **[W03, W14 · explain]** Week 3's steady state is `m* = h(g − r) / (c + τv)` and week 14's is `W* = N / s`. Show that they are the same model, say what term week 14 leaves out, and explain why that makes week 14's `W*` a single player's ceiling while week 3's `m*` is a server's.

    <details>
    <summary>Answer</summary>

    Both have a fixed daily inflow (`h(g − r)` or `N = F − S`, faucets minus flow sinks) and an outflow proportional to the stock (`τv` or `s`, with `s = τv` plus any luxury rate). The ceiling is inflow divided by outflow rate in both. Week 3 adds churn `c` to the denominator, because newcomers arriving with zero gold dilute the average. Week 14 follows one player, who does not get diluted, so `c` is absent and the ceiling is higher. Week 14's section 3 brings the server back by averaging over account ages, which is where dilution reappears as a server average below `W*`.

    </details>

68. **[W05, W08, W12 · critique]** On a mature server, the price of a crafted breastplate has fallen 40% in two months while the potion price index rose 6%. A producer says: "The economy is deflating, so cut sinks." Use three course models to critique the diagnosis and say what data you would pull first.

    <details>
    <summary>Answer</summary>

    Two different price levels are moving in opposite directions, so "the economy" is not deflating. The potion index, a fixed-basket measure (week 12), rose 6%, which is mild inflation in money per player. The breastplate is a durable good. With `d = 0` or a small `d`, its stock grows toward saturation and its price falls toward the vendor floor (week 8). That is an item-stock problem, fixed with destruction or obsolescence, not by cutting money sinks. Cutting sinks would raise `m` and push the potion index up further. Week 5 adds a third check: falling durable prices can also mean veterans stopped buying (a falling `v`). Pull first the breastplate's stock and coverage `S / N`, its listings and volume, and effective velocity by cohort.

    </details>
