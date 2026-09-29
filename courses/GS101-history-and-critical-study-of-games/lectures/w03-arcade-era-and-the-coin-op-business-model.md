# GS101 · Week 03 — Arcade era and the coin-op business model

**Why this matters:** The way a game earns money shapes the game. Arcade machines were paid by the play, and that one fact pushed designers toward short sessions, rising difficulty and lives you could lose. You will meet the same pressure again in free-to-play and live-service games, so learning to trace a design choice back to a business model starts here.

**You will be able to:**
- Compute a coin-op machine's revenue per hour, plays per day and payback time from price, session length and utilization.
- Explain, with the model, why pay-per-play games favour short sessions and difficulty that rises over time.
- Compare Galaxy Game and Computer Space (1971) as two business designs for the same idea, and explain why one reached a market.
- Critique a historical revenue figure by asking who measured it, how, and what it leaves out.

**Before class:** Donovan, *Replay: The History of Video Games* (2010), the pages on Nutting Associates, the founding of Atari and Pong, and the arrival of Space Invaders. The course reader lists the pages. Wikipedia's "Golden age of arcade video games" as an overview, read with the source-checking questions from section 4 in mind.

**Prerequisites from earlier courses:** None formally. From this course, [week 2](w02-early-computer-games.md) (Spacewar!, the PDP-1's cost, and why no one could sell it). The revenue model in section 2 is a rational function. If you are taking MA101 alongside, [MA101 week 6, rational functions and asymptotes](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w06-rational-functions-and-asymptotes.md) explains the shape of `1 / L`. Difficulty that rises over time returns as a design tool in [GD203 week 13, difficulty modes and scaling](../../GD203-combat-and-progression-design/lectures/w13-difficulty-modes-and-scaling.md). Business models for live games are the subject of MMO403 week 1 (see the [MMO403 week 1 lecture](../../MMO403-business-monetization-and-ethics-of-live-games/lectures/w01-business-models-box-subscription-f2p-hybrid.md)).

**Interactive:** [The quarter clock](../examples/w03-quarter-clock.html). Keep it open during section 2.

---

## 1. Two ways to sell Spacewar! (1971)

Last week ended with a problem. Spacewar! was a great game on a machine that cost $120,000. In 1971 two teams tried to solve that problem, a few kilometres apart in California, and chose opposite answers.

### Galaxy Game: keep the computer, charge a dime

Bill Pitts and Hugh Tuck built Galaxy Game and installed it in November 1971 at the Tresidder student union at Stanford University. It was Spacewar!, gravity star and all, running on a DEC PDP-11/20 minicomputer with a Hewlett-Packard display. The prototype cost about $20,000, of which the computer was $14,000 and the display $3,000. Players paid 10 cents a game or 25 cents for three, and the winner of a match got a free game.

A second version in June 1972 could drive several consoles from one computer, though only two were installed. It stayed popular at the student union until 1979, when the display hardware failed. The whole project cost about $65,000.

Galaxy Game was faithful to Spacewar! and it worked. But it could not be copied cheaply. Every new site needed another minicomputer.

### Computer Space: throw the computer out

Nolan Bushnell and Ted Dabney took the other route. Computer Space, built by their company Syzygy Engineering and sold by Nutting Associates from late 1971, had no processor at all. Its logic was a fixed circuit of standard 7400-series chips, with the graphics stored in diode arrays. A circuit like this can do only one thing, but it costs a tiny fraction of a computer and can be mass-produced.

To fit that budget they cut the gravity star and made the game single-player against two computer-controlled saucers. Players paid a quarter. Each game lasted a fixed time that the operator could set between 60 and 150 seconds, 90 by default.

Nutting ordered 1,500 units and sold between 1,300 and 1,500 by mid-1972. That made it the first commercially sold video game. It still disappointed Nutting. Bushnell later said the game was loved by his friends, but his friends were engineers, and it was a little too complicated for the average player in a bar. It did well on college campuses and poorly in the working-class bars where coin-op machines mostly lived.

### Pong: the same business, a simpler game

Bushnell and Dabney founded Atari in 1972 and hired Allan Alcorn, whose first project was a simple tennis game. It became Pong. The prototype went into Andy Capp's Tavern, a bar in California, in August 1972. When the bar called to say it had stopped working, Alcorn found that the coin mechanism was overflowing with quarters.

Pong kept Computer Space's business design, a dedicated circuit and a quarter per game, and fixed its audience problem. It had one knob and a goal anyone could grasp. Bushnell reported that a Pong machine earned $35 to $40 a day, which at 25 cents a play is 140 to 160 plays. Atari filled 2,500 orders by 1973 and sold more than 8,000 units by the end of 1974.

Put the three machines side by side and you have the first lesson of this lecture. Galaxy Game had the best game and the worst unit cost. Computer Space had a sellable unit cost and a hard game. Pong had both a cheap unit and a game a stranger could learn in seconds. The business model did not only decide who made money. It decided which game design survived.

## 2. Worked example: the quarter clock

### The hook

A Pong game ends when one player reaches 11 points. Designers could have made it 21, or unlimited. Alcorn also made the ball speed up the longer a rally lasted, and reset the speed after a miss. Space Invaders (Taito, 1978) speeds its aliens up as fewer of them remain. Computer Space simply let the bar owner set a timer. Three games, three mechanisms, one effect: the game ends sooner. Why would designers work so hard to end their own games?

### The model

An arcade machine earns money only when a coin goes in. Name the parts:

- `p` is the price per play, in dollars.
- `L` is the average session length, in minutes, from coin in to game over.
- `u` is the **utilization**, the fraction of opening hours in which someone is playing. A machine with a queue has `u` near 1. A machine in a quiet corner has `u` near 0.
- `H` is the number of hours the location is open per day.
- `s` is the operator's share of the cash box. In this model an operator owns the machine and shares the takings with the bar or arcade that hosts it. This lecture assumes `s = 0.5`. Real splits were negotiated case by case.

Then:

```
plays per day      = u × H × 60 / L
revenue per hour   = p × u × 60 / L
operator per day   = s × p × u × H × 60 / L
payback in days    = cabinet price / (operator per day)
```

The whole lecture sits in one feature of these formulas. **Revenue is proportional to `1 / L`.** Halve the session length and, if the machine stays busy, you double the money. This is the rational-function shape from MA101 week 6: it climbs steeply as `L` shrinks and flattens as `L` grows.

### Numbers you can check

Take `p = $0.25`, `u = 0.75` and `H = 10` hours. This is one invented combination that happens to reproduce Bushnell's reported Pong figure at `L = 3` minutes. It is not a measurement of any real bar.

For the payback column, use a cabinet price of $2,400. Wikipedia's article on the golden age gives this as the price of a Pac-Man cabinet around 1981. Pong was cheaper, so treat the column as a later-era illustration.

| Session length `L` | Plays per day | Revenue per hour | Cash box per day | Operator share per day | Payback on $2,400 |
|---|---|---|---|---|---|
| 1.5 min | 300 | $7.50 | $75.00 | $37.50 | 64 days |
| 3 min | 150 | $3.75 | $37.50 | $18.75 | 128 days |
| 5 min | 90 | $2.25 | $22.50 | $11.25 | 213 days |
| 10 min | 45 | $1.13 | $11.25 | $5.63 | 427 days |

Check the 3-minute row. `0.75 × 10 × 60 / 3 = 150` plays. `150 × $0.25 = $37.50`, inside Bushnell's $35 to $40. Half of that is $18.75, and `$2,400 / $18.75 = 128` days.

A 10-minute game earns less than a sixth of a 1.5-minute game on the same machine. For the operator, that is the difference between a machine that pays for itself in two months and one that takes over a year.

### Where session length comes from: skill and ramps

`L` is not a number the designer types in. It comes from how long players survive. Build a small model of that.

Suppose the game's difficulty starts at `d₀ = 1` and rises by `r` units per minute. A player with skill `S` survives until the difficulty passes their skill, so their session lasts `(S − d₀) / r` minutes. Add two limits. A session lasts at least half a minute, since even the worst player needs time to lose. And a player who is never challenged leaves after 30 minutes out of boredom.

Take a bar where half the players are novices (`S = 2`), 35% are regulars (`S = 5`) and 15% are experts (`S = 12`). Keep `p = $0.25` and `u = 0.75`.

| Ramp `r` per minute | Novice session | Regular | Expert | Average `L` | Revenue per hour |
|---|---|---|---|---|---|
| 0.25 | 4.0 min | 16.0 min | 30 min (bored) | 12.1 min | $0.93 |
| 0.5 | 2.0 min | 8.0 min | 22.0 min | 7.1 min | $1.58 |
| 1 | 1.0 min | 4.0 min | 11.0 min | 3.55 min | $3.17 |
| 2 | 0.5 min | 2.0 min | 5.5 min | 1.78 min | $6.34 |

Check the `r = 1` row. The novice lasts `(2 − 1) / 1 = 1` minute, the regular 4 and the expert 11. The average is `0.5 × 1 + 0.35 × 4 + 0.15 × 11 = 3.55`. Revenue per hour is `0.25 × 0.75 × 60 / 3.55 ≈ $3.17`.

Look at the expert column. With a gentle ramp, the 15% of experts hold the machine for 22 to 30 minutes on one coin, and they drag the average up. A steeper ramp cuts every session in proportion, but it matters most for the players who were occupying the most time. Doubling the ramp roughly doubles revenue per hour.

Now look at the novice column. At `r = 2` a novice pays a quarter for thirty seconds. That is the cost of the ramp, and section 3 comes back to it.

### A visual you can move

Open `examples/w03-quarter-clock.html`. The left panel plots revenue per hour against average session length, the `1 / L` curve, with a dot for the current settings. The right panel shows the three player groups as bars of session length under the current ramp. Drag the ramp slider. The expert bar shrinks the most, and the dot on the left races up the curve. Then drag the novice share up to 90% and watch the ramp matter less. A bar full of beginners ends its own games quickly. The ramp exists for the experts.

### Cross-game recognition

Write each of these as a way of controlling `L` or `p` in the same formula.

- **Pong (Atari, 1972).** A game ends at 11 points, which caps `L`. The ball speeds up the longer a rally lasts, which is a ramp inside each rally, reset after every miss so that rallies cannot run forever.
- **Space Invaders (Taito, 1978).** The aliens move faster as fewer remain. The designer, Tomohiro Nishikado, found that the hardware drew the remaining aliens faster when there were fewer of them, and he kept the effect because it made the game more exciting. A hardware accident became a ramp.
- **Computer Space (1971).** No ramp needed. The operator set `L` directly with a timer, between 60 and 150 seconds.
- **Dragon's Lair (Cinematronics, 1983).** It changed `p` instead. It was the first video arcade game to charge 50 cents a play, justified by its laserdisc animation.
- **Atari's Lunar Lander (1979).** It sold more of the game's resource, fuel, for more coins. That lets `p` grow with `L`, so a long session still pays.

The same variables appear in later business models. A game sold once for a fixed price has no `p` per session, so it has no reason to cut `L`, and home games grew longer. A free-to-play game can charge for continuing, which puts `p` back on the session. MMO403 treats that case, and its ethics, in detail.

### Eyes-open design judgment

- **Short sessions and fair sessions pull against each other.** A steep ramp raises revenue per machine, but a novice who pays for thirty seconds may never come back. Computer Space showed what happens when a game is too hard for its audience. The operator's cash box filled slowly because strangers would not put in a second coin.
- **Ramp the experts, protect the novices.** The model shows that experts create the long sessions. Designs that start gently and escalate hard target them while giving beginners a fair first minute. Space Invaders' speed-up is a good example, since it only becomes severe late in a wave.
- **Change `p` instead of `L` when the game needs length.** Dragon's Lair and Lunar Lander raised the price rather than cutting the game short. That keeps the experience whole for players willing to pay.
- **Remember the queue.** The model assumes `u` stays fixed as `L` changes. If short games leave the machine idle between players, cutting `L` stops paying. Revenue comes from sessions that are short when there are people waiting, not short in themselves.

### Check the model

1. A machine charges $0.50 with an average session of 4 minutes, `u = 0.6`, open 12 hours. How many plays a day, and how much in the cash box?
2. In the ramp table, what ramp makes the expert session exactly 5 minutes? What is the novice session at that ramp?
3. An operator can choose between a game with `L = 2` at $0.25 and one with `L = 5` at $0.50. Which earns more per hour at the same `u`?

<details>
<summary>Answers</summary>

1. `0.6 × 12 × 60 / 4 = 108` plays, `108 × $0.50 = $54`.
2. `(12 − 1) / r = 5` gives `r = 2.2` per minute. The novice's `(2 − 1) / 2.2 ≈ 0.45` minutes is below the floor, so they get the minimum 0.5 minutes.
3. Revenue per hour is proportional to `p / L`. `0.25 / 2 = 0.125` against `0.50 / 5 = 0.10`, so the short, cheap game earns 25% more.

</details>

## 3. The design traits the coin box selected

Step back from the formula. Over roughly a decade, pay-per-play pushed arcade video games toward a family of traits. None was compulsory, and every one has exceptions, but together they explain why "arcade game" names a style as well as a place.

- **Learnable in seconds.** A stranger in a bar decides in moments whether to put in a coin. Pong's one-knob design is the clearest case, and Computer Space the clearest counter-example.
- **A ramp inside the session.** Difficulty rises until the player fails, so sessions stay short whatever the skill. Pong's rally speed-up and Space Invaders' accelerating aliens are the early models.
- **Loss built into the structure.** Lives, timers and point limits guarantee an end.
- **A reason to put in another coin.** The game must make failure feel like the player's fault and near success. Galaxy Game's free replay for the winner is an early, explicit version, a price cut for skill.
- **Scale.** Once the formula worked, it worked everywhere. By the end of 1979 about 750,000 Space Invaders machines were installed worldwide, 400,000 of them in Japan. Pac-Man (Namco, 1980) is reported to have sold over 400,000 cabinets at $2,400 each and grossed over $1 billion by 1981.

Notice that this list is a claim about causes. A critic could push back. Perhaps short, hard games were simply what the hardware of the time could manage, with its tiny memory and no room for long adventures. Both causes probably operated together. A good essay separates them. The hardware limited what a game could contain. The business model decided how long a player should be allowed to stay.

## 4. Reading the numbers critically

Arcade history is full of big round numbers. Wikipedia's overview of the golden age, drawing on period reports, says that in 1982 arcade video games took in $8 billion in quarters in the United States, more than pop music and Hollywood films combined, and that North America had about 1.5 million arcade machines in operation. Space Invaders is reported to have grossed $3.8 billion by 1982.

These figures may be right. As a historian you still need to ask four questions before using one.

1. **Who counted?** A manufacturer, a trade magazine, an industry body or a government statistics office? Each has different reasons to round up.
2. **What was counted?** Quarters in the cash box (gross takings), money to the manufacturer (sales of cabinets), or profit? A cabinet sold for $2,400 and the quarters it collected are both "revenue" to someone.
3. **Over what period?** "By 1982" can mean a four-year total. Comparing it with a one-year music figure mixes units.
4. **Compared with what?** "More than Hollywood" depends on whether you compare cash-box takings with box-office takings, or with studio revenue.

Do the same with Bushnell's $35 to $40 a day. It is a founder's recollection, reported later, about his own product. It is plausible, and it fits the model, but it is one person's number. Section 2 used it as a calibration point, not as proof.

The questions matter for next week. The golden age ended in 1983, and the figures around that collapse are even more contested. When you study the crash in [week 4](w04-home-consoles-and-the-1983-crash.md), the numbers will carry the argument, and you will need to know where each one came from.

## In-class activity (25 min)

In groups of three, you are an arcade operator in 1981 choosing between two invented cabinets for one spot in a busy bar.

- Cabinet A costs $2,400, charges $0.25 and has a gentle ramp. Playtests show an average session of 6 minutes.
- Cabinet B costs $3,000, charges $0.25 and has a steep ramp. The average session is 2.5 minutes, but a third of first-time players do not play a second game.

1. Compute revenue per hour and payback days for both, with `u = 0.75`, `H = 10` and `s = 0.5`.
2. Estimate what happens to `u` for cabinet B if the players who give up are not replaced. Recompute with your estimate.
3. Pick one cabinet and write a three-sentence recommendation that names the variable you think matters most.
4. Swap recommendations with another group and find one assumption in theirs that the numbers do not support.

Expected output: a four-row calculation table, a recommendation paragraph, and one written challenge to another group.

## Common misconceptions

- **"Arcade games were hard because the hardware was primitive."** Hardware limited content. Difficulty ramps and short sessions follow from pay-per-play, as the model shows. Both causes operated.
- **"Computer Space failed."** It sold between 1,300 and 1,500 units and was the first commercial video game. It disappointed its maker, mainly because bar customers found it too complicated.
- **"Shorter games always earn more."** Only while the machine stays busy. If short sessions drive players away, utilization falls and so does revenue.
- **"The $8 billion figure measures the size of the games business."** It is reported quarters taken in by arcade machines in one country and one year. It says nothing about manufacturer profit, home games or other countries.

## Check yourself

1. Using the model, Pong's $35 to $40 a day and a 25-cent price, how many plays a day does Bushnell's figure imply? If the bar was open 12 hours and each game lasted 4 minutes, what utilization does that imply?
2. Explain in two sentences, using the ramp model, why Pong resets ball speed after a miss rather than keeping it high.
3. Galaxy Game charged 10 cents a game or 25 cents for three, with a free game for the winner. Rewrite the winner's free game in terms of `p`. Which players does it favour, and what does it do to `L` per coin?
4. Wikipedia reports Space Invaders at about $3.8 billion gross by 1982. Write the four source questions from section 4 for this figure, and answer the ones you can from the lecture.

<details>
<summary>Answers</summary>

1. `$35 / $0.25 = 140` to `$40 / $0.25 = 160` plays. At 150 plays of 4 minutes, the machine is busy 600 minutes out of 720, so `u ≈ 0.83`.
2. If the speed stayed high, the next rally would start at a speed the novice could not handle and end at once, making the game frustrating without earning more. Resetting makes each rally a fresh ramp, so every point is winnable at first and ends sooner the longer it lasts.
3. The winner's effective price per game falls: two games for one coin halves `p` for a player who wins once. It favours skilled players and lengthens their time per coin, the opposite of a ramp. It trades revenue per hour for a reason to come back.
4. Who counted is not stated in the lecture. What was counted is "gross," likely money taken in, not profit. The period is cumulative from the 1978 release to 1982, not one year. The comparison class is not given. A careful writer would find the underlying report before using it.

</details>

## Lab / assignment hook

[Lab 03, the operator's spreadsheet](../labs/lab03.md). You will build the quarter-clock model in a spreadsheet, fit it to the provided session log from an invented arcade, and write a 500-word memo that recommends a difficulty ramp and justifies it with numbers and with one historical precedent. The memo is practice for the timeline project's "cause" entries.

## Sources

- Wikipedia, "Galaxy Game" (accessed September 2026). Tresidder Union, Stanford, November 1971; Pitts and Tuck; PDP-11/20 ($14,000) and HP display ($3,000), prototype about $20,000; 10 cents a game or 25 cents for three, free game to the winner; June 1972 multi-console version; in service until 1979; total about $65,000.
- Wikipedia, "Computer Space" (accessed September 2026). Nutting Associates, late 1971; Bushnell and Dabney; no microprocessor, 7400-series logic, graphics in diode arrays; 1,500 ordered and 1,300 to 1,500 sold by mid-1972; 25 cents; timer 60 to 150 seconds, default 90; Bushnell's remark on it being too complicated for bar customers.
- Wikipedia, "Pong" (accessed September 2026). Alcorn; Andy Capp's Tavern prototype, August 1972, coin mechanism overflowing; release 29 November 1972; first to 11 points; ball accelerates during a rally and resets on a miss; Bushnell's $35 to $40 a day, 140 to 160 plays; 2,500 orders by 1973 and over 8,000 units by the end of 1974.
- Wikipedia, "Space Invaders" (accessed September 2026). Taito, July 1978, Nishikado; alien speed-up from rendering speed, kept deliberately; about 750,000 machines by end of 1979, 400,000 in Japan; $3.8 billion gross by 1982.
- Wikipedia, "Dragon's Lair (1983 video game)" (accessed September 2026). June 1983; first video arcade game to cost 50 cents; laserdisc.
- Wikipedia, "Lunar Lander (video game genre)" (accessed September 2026). Atari's 1979 arcade game let players buy more fuel with coins.
- Wikipedia, "Golden age of arcade video games" (accessed September 2026). About 1978 to 1983; $8 billion in quarters in 1982; 1.5 million machines in North America; Pac-Man cabinets at $2,400, over 400,000 sold, over $1 billion grossed by 1981.
- Donovan, T. (2010). *Replay: The History of Video Games*. Yellow Ant, East Sussex (xiv + 501 pp.).

## Interactive spec: examples/w03-quarter-clock.html

**Purpose.** Show that pay-per-play revenue is proportional to `1 / L`, and that a difficulty ramp controls `L` mainly by cutting expert sessions.

**The one insight the visual must make obvious.** Dragging the ramp steeper shrinks the expert bar far more than the novice bar in minutes, and the revenue dot climbs the `1 / L` curve. Long sessions come from the few experts.

**Layout.** Two linked views, side by side on desktop, stacked on mobile, plus a numbers panel.
- Left, "Revenue per hour vs average session": x axis `L` from 0.5 to 30 minutes, y axis revenue per hour. Draw the curve `p × u × 60 / L` for the current `p` and `u`. A dot marks the current average `L`. A faint second curve shows `p = $0.50` for comparison.
- Right, "Session length by player group": three horizontal bars (novice, regular, expert), bar length = session minutes, bar thickness or label showing the group's share. Mark the 0.5-minute floor and the 30-minute boredom cap with thin vertical lines.
- Numbers panel: each group's session, average `L`, plays per day, revenue per hour, cash box per day, operator share per day and payback days.

**Controls.**
- Ramp `r`: slider 0.1 to 3.0 per minute, step 0.05, default 1.0.
- Price `p`: select $0.10, $0.25, $0.50, default $0.25.
- Utilization `u`: slider 0.1 to 1.0, step 0.05, default 0.75.
- Hours open `H`: slider 4 to 16, default 10.
- Operator share `s`: slider 0.3 to 0.7, default 0.5 (label "assumption").
- Cabinet price: number input, default 2400.
- Group mix: three linked sliders for novice, regular and expert share that always sum to 100% (default 50 / 35 / 15). Skills fixed at 2, 5 and 12; an "advanced" disclosure lets the user edit them (1 to 20).
- Start difficulty `d₀` fixed at 1, editable under "advanced".
- Preset button "Pong calibration": sets `p = 0.25`, `u = 0.75`, `H = 10`, and a fixed `L = 3` override (a checkbox "set L directly" that bypasses the ramp model), showing 150 plays and $37.50 a day.

**Formulas.**
- Session for skill `S`: `L(S) = min(30, max(0.5, (S − d₀) / r))`.
- Average `L = Σ share × L(S)`.
- `plays/day = u × H × 60 / L`; `revenue/hour = p × u × 60 / L`; `cash/day = revenue/hour × H`; `operator/day = s × cash/day`; `payback = cabinet / operator/day`.

**Test values** (`p = 0.25`, `u = 0.75`, `H = 10`, `s = 0.5`, cabinet $2,400, mix 50/35/15, skills 2/5/12, `d₀ = 1`).
- `r = 0.25`: sessions 4.0 / 16.0 / 30.0, average 12.1, revenue/hour $0.93.
- `r = 0.5`: 2.0 / 8.0 / 22.0, average 7.1, $1.58.
- `r = 1`: 1.0 / 4.0 / 11.0, average 3.55, $3.17, plays/day 126.8, payback 151 days.
- `r = 2`: 0.5 / 2.0 / 5.5, average 1.775, $6.34.
- Direct `L = 3`: 150 plays/day, $3.75/hour, $37.50/day, $18.75 operator, payback 128 days.
- Direct `L = 1.5`: 300 plays, payback 64 days. `L = 10`: 45 plays, payback 427 days.

**Style.** Shared tokens. Draw generic cabinet icons only, no game logos or screenshots. First screen shows `r = 1` with the expert bar visibly longest and the revenue dot labelled, so the insight appears before any input.
