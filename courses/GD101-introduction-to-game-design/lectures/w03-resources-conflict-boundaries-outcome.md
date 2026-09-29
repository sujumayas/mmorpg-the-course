# GD101 · Week 03 — Formal elements II: resources, conflict, boundaries, outcome

**Why this matters:** The number of lives you start with, the gold in your bag and the timer in the corner are all resources, and each one quietly decides who wins. This week you learn the other four formal elements and a small model that shows exactly how a resource like lives turns a player's skill into a win or a loss.

**You will be able to:**
- Identify the resources, sources of conflict, boundaries and outcome type of any game.
- Compute the chance of finishing a run from the number of stages, the number of lives and the chance of clearing a stage, using a table you fill in by hand.
- Explain how changing the starting lives moves the band of players for whom the outcome is uncertain.
- Critique a boundary between a game and the real world, such as a real-money exchange, by naming what crosses it.

**Before class:** Fullerton, *Game Design Workshop* (4th ed., 2018), chapter 3, the sections on resources, conflict, boundaries and outcome. Salen & Zimmerman, *Rules of Play* (2003), the chapter "The Magic Circle". Ian Schreiber, *Game Design Concepts* (2009), "Level 3: Formal Elements of Games", sections on resources and game state.

**Prerequisites from earlier courses:** None. From this course, [week 1](w01-what-is-a-game.md) (Juul's variable outcome, the magic circle) and [week 2](w02-players-objectives-procedures-rules.md) (players, objectives, procedures, rules). You need fractions and multiplication only. MA102 later treats the probability here formally in [week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md).

**Interactive:** [Lives and the win curve](../examples/w03-lives-and-outcome.html). Keep it open during section 2.

---

## 1. Resources: what is scarce and useful

A **resource** is anything in a game that is useful to the players and in short supply. Both parts matter. Air in a platformer is useful but unlimited, so it is not a resource. Air in an underwater level with a breath meter is a resource. A pile of useless tokens is scarce but not useful, so it is not a resource either.

Fullerton lists common resource types, and Schreiber adds a few. Together:

- **Lives.** Attempts you can fail before the game ends.
- **Health.** How much damage you can take before losing a life or the fight.
- **Currency.** Gold, money, points you can spend.
- **Actions.** Moves per turn, action points, stamina.
- **Units and territory.** Pieces on the board, land on the map.
- **Items and power-ups.** Weapons, potions, keys.
- **Time.** A clock that runs down, or turns that run out.
- **Information.** What you know that others don't. In Clue, the suspects you have ruled out are a resource.

Three questions tell you most of what you need to know about a resource:

1. **How does it enter the game?** A source that adds a resource is called a **faucet** in economy design: coins from enemies, a life every 100 coins.
2. **How does it leave?** A drain that removes a resource is a **sink**: repair costs, lives lost on death.
3. **What can it be turned into?** Gold becomes a sword. Time becomes actions. A resource that converts into winning is the one players fight over.

Faucets and sinks are the core of virtual economies, and you will use them for years in this program: in GD102 week 7 on [internal economies, sources and drains](../../GD102-systems-design-and-game-mechanics/lectures/w07-internal-economies-sources-drains-converters.md) and in MMO304 week 3 on [faucets, sinks and transformations](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md). This week you look at the simplest resource of all, the one that decides whether you get to keep playing.

## 2. Worked example: how many lives?

### The hook

In Super Mario Bros. (NES, 1985), collecting 100 coins gives you an extra life. So does a green 1-Up Mushroom. When you run out of lives, the game is over, although holding the A button on the game-over screen restarts you at the first level of the world where you died. The NES version even breaks at the top end: the counter can hold 127 lives, and going above that causes a Game Over on the next death because the number overflows.

Celeste (2018) has no lives at all. When you die, you reappear at the start of the current screen. The game is famous for being hard, yet you cannot "lose" it.

Old School RuneScape's Hardcore Ironman accounts get exactly one life. One unsafe death and the account turns into a regular Ironman and its HiScores entry is locked. Minecraft's Hardcore mode does the same thing to a whole world: one death and it is over.

Four games, four answers to one design question: how many times may a player fail? Is the lives counter a difficulty setting, a reward, or something else? The model below answers with numbers.

### The model

Picture a **run**: a sequence of `n` stages you must clear in order. Each time you attempt a stage, you clear it with probability `p` and fail with probability `1 − p`. Think of `p` as the match between your skill and the stage's difficulty: 0.9 means you clear it 9 times in 10.

You start with `L` lives. Clearing a stage moves you to the next one and costs nothing. Failing costs one life and you retry the same stage. With zero lives the run is over.

Let `W(n, L)` be the chance of finishing a run of `n` stages when you have `L` lives. Two edge cases are obvious:

- `W(0, L) = 1`. With no stages left, you have won.
- `W(n, 0) = 0`. With stages left and no lives, you have lost.

Every other case splits on your next attempt. With chance `p` you clear it, leaving `n − 1` stages and the same `L` lives. With chance `1 − p` you fail, leaving `n` stages and `L − 1` lives. So:

```
W(n, L) = p × W(n − 1, L) + (1 − p) × W(n, L − 1)
```

That one line is the whole model. Every cell of the table is built from the cell above it and the cell to its left. You need no formula beyond multiplication and addition.

The model makes two simplifying assumptions, and you should keep them in view. Every stage has the same `p`, and attempts do not get easier as you learn. Real players improve, so real runs are a bit kinder than the model. That turns out not to matter for the lesson.

### Numbers you can check

**A small table by hand, `p = 0.8`.** Rows are stages left (`n`), columns are lives (`L`).

| n \ L | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| 0 | 1 | 1 | 1 | 1 |
| 1 | 0 | 0.8 | 0.96 | 0.992 |
| 2 | 0 | 0.64 | 0.896 | 0.9728 |
| 3 | 0 | 0.512 | 0.8192 | 0.9421 |
| 4 | 0 | 0.4096 | 0.7373 | 0.9011 |

Check one cell yourself. `W(2, 2) = 0.8 × W(1, 2) + 0.2 × W(2, 1) = 0.8 × 0.96 + 0.2 × 0.64 = 0.768 + 0.128 = 0.896`. The column for `L = 1` is just `0.8` multiplied by itself `n` times, because one life means no mistakes: `0.8⁴ = 0.4096`.

**A full-length run, `n = 8` stages.** Same method, extended by the interactive or a spreadsheet:

| Skill `p` | L = 1 | L = 2 | L = 3 | L = 4 | L = 5 | Average failures in a finished run |
|---|---|---|---|---|---|---|
| 0.7 | 5.8% | 19.6% | 38.3% | 57.0% | 72.4% | 3.43 |
| 0.8 | 16.8% | 43.6% | 67.8% | 83.9% | 92.7% | 2.00 |
| 0.9 | 43.0% | 77.5% | 93.0% | 98.1% | 99.6% | 0.89 |

The last column is how many failures a player of that skill makes on average while clearing all 8 stages. It equals `n × (1 − p) / p`. For `p = 0.8`, that is `8 × 0.2 / 0.8 = 2`. Read along the `p = 0.8` row: the win chance crosses 50% between 2 and 3 lives. A useful rule of thumb follows. **A player tends to finish when they have about one more life than the failures they would make on an average run.**

**The skill band.** Now fix the lives and ask which players find the outcome uncertain, meaning their chance of finishing sits between 20% and 80%. (Recall Juul's "variable outcome" from week 1. This is where it lives.)

| Starting lives | Skill `p` at 50% win | Uncertain band (20% to 80% win) | Band width |
|---|---|---|---|
| 1 | 0.917 | 0.818 to 0.972 | 0.154 |
| 3 | 0.741 | 0.619 to 0.842 | 0.223 |
| 5 | 0.621 | 0.503 to 0.731 | 0.228 |

This is the key result. Lives do not simply make a game "easier". They choose **which players get a close contest**. With 1 life, only near-experts (`p` above about 0.82) ever face an uncertain ending. Everyone below that nearly always loses, which tells them nothing. With 5 lives, the uncertain band moves down to mid-skill players, and experts nearly always win.

**The faucet.** Give one extra life after clearing stage 4, like a 1-up earned mid-run. At `p = 0.8`:

| Start | Win chance, no 1-up | Win chance, 1-up after stage 4 |
|---|---|---|
| L = 1 | 16.8% | 30.2% |
| L = 2 | 43.6% | 61.1% |
| L = 3 | 67.8% | 81.2% |

The earned life helps, but less than a starting life: 1 life plus the 1-up gives 30.2%, while simply starting with 2 lives gives 43.6%. The reason is that the earned life only reaches players who already got halfway. It is a reward for doing well, so it helps the players who needed it least. You will meet this "the leader gets more" pattern again next week as a feedback loop, in [Monopoly's runaway leader](w04-mda-mechanics-dynamics-aesthetics.md).

### A visual you can move

Open [`examples/w03-lives-and-outcome.html`](../examples/w03-lives-and-outcome.html). The left panel is the `W(n, L)` table as a heat map, with each cell's number printed. Hover a cell to see the two cells it was built from. The right panel plots win chance against skill `p` for several starting lives, with the 20% to 80% band shaded.

Drag the lives slider from 1 to 5 and watch the S-shaped curve slide left along the skill axis. The curve barely changes shape. It moves. That is the picture of "lives choose who gets the close contest". Then switch on "1-up after stage k" and watch the curve lift mostly at the high-skill end.

### Cross-game recognition

Rewrite each game from the hook as the same model: what are `n`, `L` and `p`?

**Super Mario Bros. (1985).** `n` is 32 levels (8 on the warp route from week 1). `L` is your starting lives plus a faucet: every 100 coins and every 1-Up Mushroom adds one. The continue on the game-over screen is a second layer. It refills your lives but sends you back to the first level of the current world, so it trades a life resource for a time cost. The 127-life overflow shows the designers did not expect players to stockpile that many. The faucet was generous enough that some did.

**Celeste (2018).** `L` is infinite and each stage is a single screen. Plug `L = ∞` into the model and `W = 1` for any `p` above zero. Everyone finishes. The uncertain quantity is no longer *whether* you finish but *how many attempts* it takes: on average `1 / p` per screen, so 10 attempts on a screen you clear 10% of the time. The outcome changed type, from win or lose to a count. Celeste's Assist Mode goes further and lets players change `p` itself, with options such as slower game speed or invincibility.

**Old School RuneScape Hardcore Ironman, and Minecraft Hardcore.** `L = 1`, and `n` has no fixed end: it is every risky moment for the life of the account or world. Then `W = pⁿ`, which always heads to zero as `n` grows. For illustration only (these are not real game figures): a player who survives each risky encounter with `p = 0.999` has `0.999¹⁰⁰⁰ ≈ 0.37`, a 37% chance of surviving 1,000 of them. That is why one-life modes feel tense forever. The run never gets safe. It only gets longer.

Same model, three shapes: a finite run with a faucet, an infinite-lives run where the outcome becomes a count, and a one-life run with no end. When you meet a new game's failure rules, ask the same three questions: how many stages, how many lives, and what is the chance of clearing one?

### Eyes-open design judgment

Lives are a design decision with trade-offs, not a leftover from arcades.

- **Lives set the audience for tension.** Pick `L` for the skill band you want to have close finishes. Pick it by reflex (three lives because arcades had three) and you may be giving tension to nobody. Measure `p` in playtests, then use the table.
- **Game over costs content.** When a run ends, the player replays stages they already beat. That repetition is the real cost of losing a life, and it lands hardest on the weakest players. Checkpoints (Celeste's per-screen respawn) shrink `n` so failure costs seconds. Your decision is really about how much repetition failure should cost.
- **Earned lives reward the leader.** A 1-up faucet mostly helps players who were already likely to win. If you want to help struggling players, give lives at the start, or after failures, not after successes. Many games do both, on purpose.
- **Infinite lives change the outcome, not the challenge.** Removing lives does not make stages easier. It changes what the player tracks, from "will I make it" to "how many tries". Some players prefer the first kind of tension, some the second. Offer a choice (Minecraft ships both Survival and Hardcore) when your audience is broad.
- **Persistent worlds need a different sink.** An MMO cannot end your game on death without deleting months of progress. Most instead charge time (walking back to your body) or currency (repair bills). That keeps death meaningful without a game over, but it turns lives into an economy question. That is the MMO304 thread.

### Check the model

1. Compute `W(3, 2)` for `p = 0.5` by hand, building the table from `W(0, ·)` and `W(·, 0)`.
2. A designer wants a 10-stage game where a player with `p = 0.9` finishes about half the time. Use the average-failures rule of thumb to guess `L`. How many failures does that player make on average?
3. Your 1-life hard mode has a band from `p = 0.818` to `0.972` (for 8 stages). If you cut the run to 4 stages, does the band move up or down the skill axis? Explain without computing.

Answers are in the Check yourself section.

## 3. Conflict: what stands in the way

Conflict is what stops players from reaching the objective straight away. Recall Suits from week 1: the obstacles are unnecessary, and chosen. Fullerton sorts the sources of conflict into three kinds:

- **Obstacles.** Things in the world: a gap to jump, a locked door, a maze. They do not think.
- **Opponents.** Other players or AI that act against you and adapt.
- **Dilemmas.** Choices where every option costs something. Spend the gold on armor or on a faster mount? Heal now or attack now?

Most good games mix all three. A raid boss in an MMO is an opponent that uses obstacles (fire on the floor) and forces dilemmas (dodge now and lose damage, or stay and risk dying).

The three kinds break in different ways. Obstacles become trivial once solved; a platform you can jump once, you can jump forever. Opponents stay interesting because they adapt, but human opponents also bring the week-2 problems of implicit rules and player structure. Dilemmas collapse the moment one option is clearly best. A dilemma only exists if the costs are close, which is why balance, a later topic in this course, is mostly about keeping dilemmas alive.

Resources and conflict connect directly. In the lives model, `p` measures the conflict (how hard each stage is) and `L` measures how much conflict you can afford to lose to. Tuning a game is usually tuning both at once.

## 4. Boundaries: where the game stops

**Boundaries** separate the game from everything else. Some are physical: the edge of the board, the lines of a pitch, the invisible wall of a level. Others are conceptual: the start and end of a match, the agreement that the plastic money is not real money.

Johan Huizinga's *Homo Ludens* (1938) described play as happening inside a space marked off from ordinary life, where special rules hold. Eric Zimmerman and Frank Lantz named this idea the **magic circle** in 1999, and Salen & Zimmerman made it widely known in *Rules of Play* (2003). Inside the circle, taking your friend's queen is a good move. Outside, taking your friend's things is theft. The circle is what makes Juul's "negotiable consequences" possible.

For online worlds, the circle leaks. The economist Edward Castronova argued in *Synthetic Worlds* (2005) that the boundary around virtual worlds is a porous membrane. Players sell gold and items for real money, argue about game balance on outside forums, and take disputes over virtual property to real courts.

Designers can also cut a deliberate door in the membrane. World of Warcraft added the WoW Token in patch 6.1.2 (March 2015). You buy a token with real money in the in-game shop and sell it on the Auction House for gold at a market price the game sets from supply and demand. The buyer can redeem it for 30 days of game time or Battle.net balance. In boundary terms, real money now crosses into the game as gold, and gold crosses out as game time. The designers did not remove the boundary. They chose exactly what may cross it, and at what rate. That is a boundary decision, and it is also an economy decision, one you will analyse properly in MMO304 (see [week 11, real-money trade and gold farming](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w11-real-money-trade-and-gold-farming.md)).

When you describe a game's boundaries, answer three questions. Where does play happen (space)? When does it start and stop (time)? What crosses in or out (stakes, money, information, relationships)?

## 5. Outcome: how it ends, if it ends

The **outcome** is the result of play. Fullerton's point is that outcomes should be uncertain until the end, or players stop caring. That is Juul's variable outcome again, and the lives model showed how to measure it.

Outcomes come in several types:

- **Win or lose.** One or more players win; others lose. Chess, Super Mario Bros.
- **Ranking or score.** Everyone gets a position or a number. Racing games, arcade high scores.
- **Count.** How many attempts, how long, how many deaths. Celeste's model, speedruns.
- **Zero-sum or not.** In a **zero-sum** game, one player's gain is exactly another's loss (chess, poker among players). In a **non-zero-sum** game, players can all gain or all lose together (co-op games, trading in an MMO market).
- **No final outcome.** Persistent worlds rarely end. They offer many small outcomes (a boss killed, a quest done, a rank reached) inside a world that keeps going. Minecraft Survival shows the pattern even offline. You can defeat the Ender Dragon and watch the credits, then keep playing the same world.

The type of outcome shapes behaviour. Zero-sum outcomes push players against each other. Non-zero-sum outcomes allow cooperation, and in MMOs they create economies. Score outcomes invite replay to beat your number. Count outcomes, like attempts in Celeste, let every player finish while still measuring skill.

## In-class activity (25 min)

**Dice run.** Pairs. Materials: two six-sided dice per pair, the table template on the board, a pencil.

1. (3 min) Each stage is cleared by rolling a total of 6 or more on two dice. That happens in 26 of 36 outcomes, so `p = 26/36 ≈ 0.722`. A run is 6 stages.
2. (7 min) Play 10 runs with 2 lives and 10 runs with 4 lives. Record wins.
3. (8 min) Fill in the `W(n, L)` table for `n` up to 6 and `L` up to 4 with `p = 0.722`, using the recurrence. Round to 3 decimals. Your model values should be `W(6, 2) ≈ 0.378` and `W(6, 4) ≈ 0.779`.
4. (7 min) Compare your 10-run results with the model. Pool the class's runs on the board. With about 150 runs per setting, the pooled rates should usually land within 8 percentage points of the model. Ten runs per pair will scatter much more.

**Expected output:** a filled table, the pair's tallies, and a one-line answer to "how many lives would you give a first-time player of this dice game, and why?"

## Common misconceptions

- **"More lives just makes it easier."** More lives move the band of players who get a close finish. They make it easier for some players and remove tension for others.
- **"An earned 1-up is as good as a starting life."** It only reaches players who survive long enough to earn it. At `p = 0.8`, 1 life plus a 1-up after stage 4 wins 30.2% of the time, but starting with 2 lives wins 43.6%.
- **"Infinite lives means no challenge."** Celeste has infinite lives and hard stages. The outcome changes from win or lose to a count of attempts.
- **"The magic circle is a wall."** For online games it is a membrane. Designers decide what crosses it, as the WoW Token shows.

## Check yourself

1. A game has 5 stages, `p = 0.6`, and 1 life. What is the chance of finishing? How many lives does the rule of thumb suggest for a 50% finish rate?
2. Name one resource in chess. What is its faucet and what is its sink?
3. Describe the boundaries of a World of Warcraft raid in space, time and what crosses them.
4. Answer the three "Check the model" questions in section 2.

<details>
<summary>Answers</summary>

1. `0.6⁵ = 0.078`, about 7.8%. Average failures in a finished run are `5 × 0.4 / 0.6 ≈ 3.3`, so the rule of thumb suggests about 4 lives. (The exact values are `W(5, 3) ≈ 0.42` and `W(5, 4) ≈ 0.59`, so 4 lives is the first count above 50%.)
2. Pieces. Chess has no faucet for pieces except pawn promotion, which converts a pawn into a stronger piece. The sink is capture. Time on the clock is another resource, with increments (if used) as a faucet.
3. Space: the raid instance, which only group members can enter. Time: from entering the instance to the weekly reset that clears boss kills. Crossing in: players' gear, consumables bought with gold, and real-world schedules (people must be online together). Crossing out: loot, achievements, and social reputation in the guild.
4. (a) `W(1, 1) = 0.5`, `W(1, 2) = 0.5 × 1 + 0.5 × 0.5 = 0.75`. `W(2, 1) = 0.25`, `W(2, 2) = 0.5 × 0.75 + 0.5 × 0.25 = 0.5`. `W(3, 1) = 0.125`, `W(3, 2) = 0.5 × 0.5 + 0.5 × 0.125 = 0.3125`. (b) Average failures `10 × 0.1 / 0.9 ≈ 1.1`, so about 2 lives. (The exact value is `W(10, 2) ≈ 0.70`, and with 1 life it is `0.9¹⁰ ≈ 0.35`, so the 50% point sits between 1 and 2 lives.) (c) The band moves down. A shorter run means fewer chances to fail, so a less skilled player reaches the same finish chance. With 1 life, `W = p⁴` instead of `p⁸`, and `p⁴ = 0.5` at `p ≈ 0.84` instead of `0.917`.

</details>

## Lab hook

**Lab 03, Tune the lives.** Build the `W(n, L)` table in a spreadsheet, test it with a paper dice run, and choose starting lives and a 1-up rule for two difficulty modes. See [labs/lab03.md](../labs/lab03.md).

## Sources

- Fullerton, T. (2018). *Game Design Workshop*, 4th ed. CRC Press, chapter 3. Resources, conflict (obstacles, opponents, dilemmas), boundaries and outcome.
- Schreiber, I. (2009). *Game Design Concepts*, "Level 3: Formal Elements of Games". Resource examples including time and information; game state.
- Salen, K. & Zimmerman, E. (2003). *Rules of Play*. MIT Press, the chapter "The Magic Circle" (cited by title; chapter number not checked).
- Wikipedia, "Magic circle (games)" (accessed September 2026). Huizinga (1938); the term coined by Zimmerman and Lantz in 1999; Castronova's porous membrane.
- Castronova, E. (2005). *Synthetic Worlds: The Business and Culture of Online Games*. University of Chicago Press.
- Wikipedia, "Super Mario Bros." (accessed September 2026). Extra lives from 100 coins and 1-Up Mushrooms; holding A on the game-over screen restarts at the first level of the current world (NES, 1985).
- Super Mario Wiki, "Extra life" (accessed September 2026). 100-coin extra life introduced in Super Mario Bros.; NES version holds up to 127 lives before an overflow causes a Game Over.
- Wikipedia, "Celeste (video game)" (accessed September 2026). Released January 2018; chapters divided into single-screen challenges with checkpoints between screens; Assist Mode options (slower game speed, unlimited dashes, invincibility).
- Old School RuneScape Wiki, "Ironman Mode" (accessed September 2026). Hardcore Ironman has one life; an unsafe death converts the account to a regular Ironman.
- Wikipedia, "Minecraft" (accessed September 2026). Hardcore mode adds permadeath; Survival continues after the Ender Dragon and credits.
- Warcraft Wiki, "WoW Token" (accessed September 2026). Added in patch 6.1.2 (24 March 2015); bought with real money, sold for gold at a market price set from supply and demand, redeemable for 30 days of game time or Battle.net balance.
- All `W(n, L)` values, skill bands and 1-up comparisons were computed for this lecture with the recurrence in section 2. The Hardcore example uses illustrative numbers, not game data.

## Interactive spec: examples/w03-lives-and-outcome.html

**The one insight.** Starting lives do not reshape the win curve, they slide it along the skill axis. Lives choose which players get an uncertain, close finish.

**Layout.** Two linked panels. Panel A (table) left on desktop, Panel B (curves) right; on mobile, Panel B first.

**Model.** `W(0, L) = 1`; `W(n, 0) = 0`; `W(n, L) = p·W(n−1, L) + (1−p)·W(n, L−1)`. With the 1-up option at stage `k`, clearing stage `k` (moving from `k−1` cleared to `k` cleared) adds one life before continuing. Implement as a function `f(cleared, lives)`: returns 1 if `cleared = n`; 0 if `lives = 0`; else `p·f(cleared+1, lives + bonus) + (1−p)·f(cleared, lives−1)` where `bonus = 1` if the 1-up is on and `cleared + 1 = k`, else 0. Memoize.

**Panel A, the table.** Heat map of `W(n, L)` without the 1-up (the 1-up version is shown only as a value in the readout), rows `n = 0..N` (N = the stages slider), columns `L = 0..8`. Each cell prints its value to 3 decimals and is shaded by value (sequential lightness scale). Hovering or focusing a cell outlines the two source cells (above-left logic: `W(n−1, L)` and `W(n, L−1)`) and shows the arithmetic, e.g. "0.8 × 0.960 + 0.2 × 0.640 = 0.896". The cell for the current (n, L) slider values is ringed.

**Panel B, win chance vs skill.** X-axis `p` from 0.40 to 1.00. Y-axis win chance 0% to 100%. Draw `W(n, L)` as a curve for L = 1, 3, 5 (thin, muted) and the currently selected L (thick). Shade the horizontal band 20% to 80%. Mark and label where the selected curve crosses 20%, 50% and 80% (the uncertain band and its midpoint). Vertical cursor at the current `p` with the value printed. When the 1-up toggle is on, draw a second thick dashed curve for the selected L with the 1-up.

**Controls.**
- Skill `p` slider: 0.40 to 0.99, step 0.01, default 0.80.
- Stages `n` slider: 1 to 12, default 8.
- Starting lives `L` slider: 1 to 8, default 3.
- "1-up after stage k" toggle (default off) with `k` select 1 to n−1 (default 4).
- "Simulate 200 runs" button: runs Monte Carlo with the current settings and shows the observed win rate next to the model value; under reduced motion, show the result without animation.
- Readout line: "Average failures in a finished run: n(1 − p)/p = X".

**Test values (must match to the shown precision).**

| p | n | L | 1-up | W |
|---|---|---|---|---|
| 0.8 | 2 | 2 | off | 0.896 |
| 0.8 | 4 | 3 | off | 0.9011 |
| 0.8 | 8 | 1 | off | 0.1678 |
| 0.8 | 8 | 3 | off | 0.6778 |
| 0.8 | 8 | 5 | off | 0.9274 |
| 0.7 | 8 | 4 | off | 0.5696 |
| 0.9 | 8 | 2 | off | 0.7748 |
| 0.8 | 8 | 1 | after 4 | 0.3020 |
| 0.8 | 8 | 2 | after 4 | 0.6107 |
| 0.8 | 8 | 3 | after 4 | 0.8120 |
| 26/36 | 6 | 2 | off | 0.3784 |
| 26/36 | 6 | 4 | off | 0.7787 |

Band markers for n = 8 (to 3 decimals): L = 1 → 20% at p ≈ 0.818, 50% at 0.917, 80% at 0.972; L = 3 → 0.619, 0.741, 0.842; L = 5 → 0.503, 0.621, 0.731. Find crossings by bisection on `p`.

**Accessibility and style.** Curves are distinguished by line style and direct labels as well as colour. All sliders keyboard operable with visible values. Use `templates/interactive-tokens.css`. No game characters or art; stages are drawn as plain numbered blocks if shown at all.
