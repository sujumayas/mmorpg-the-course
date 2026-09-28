# GD101 · Week 10 — Chance vs Skill: The Role of Randomness

**Why this matters:** Every game you design sits somewhere between a coin flip and chess, and players feel exactly where. Too much chance and good players stop trying because practice doesn't show. Too little and weaker players stop showing up because they never win. This week gives you a way to measure where your game sits and three dials that move it.

**You will be able to:**
- Compute a stronger player's chance to win a round when the result is "skill plus a die roll", by counting outcomes on a grid.
- Compute the chance that the stronger player wins a best-of-3 or best-of-5 match, and explain why longer matches reward skill.
- Classify a random element as input randomness or output randomness and predict how it changes player decisions.
- Critique a design's balance of luck and skill, and propose a change to one dial (die size, skill gap, or match length) with a number attached.

**Before class:** Ian Schreiber, *Game Balance Concepts* (blog course, 2010), Level 1 "Intro to Game Balance", the vocabulary sections on determinism, non-determinism and solvability. Elias, Garfield & Gutschera, *Characteristics of Games* (MIT Press, 2012), the chapter on luck and skill (skim). Bring two six-sided dice and one twenty-sided die, or a dice app.

**Prerequisites from earlier courses:** None outside GD101. From this course you need [week 2's formal elements](w02-players-objectives-procedures-rules.md) and [week 9's tests for an interesting decision](w09-choice-and-meaningful-decisions.md). The probability you need is taught here by counting. If you want the full theory later, MA102 covers [independent events](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w02-independent-events-and-the-gamblers-fallacy.md), [the binomial distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w06-binomial-crits-over-a-fight.md) and [dice sums](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w08-dice-sums-and-the-normal-curve.md).

**Interactive:** [The luck dial](../examples/w10-luck-dial.html). Keep it open during section 2.

---

## 1. Two ingredients in every result

Watch any game end and ask why the winner won. The answer always mixes two things. Some of it came from the players: what they knew, what they chose, how well their hands moved. Some of it came from outside the players: the dice, the shuffle, the spawn point, the enemy that happened to turn left.

We will call the first part **skill** and the second part **luck**. Here "luck" means any source of outcome that no player controls and no player can predict, and we will call the machinery that produces it **randomness** (dice, shuffled cards, a random number generator in code). A game with no randomness at all is **deterministic**: the same choices always give the same result. Chess and tic-tac-toe are deterministic. Candy Land, from Milton Bradley in 1949, is at the other end: players never make a choice, they draw a card and move to the color it shows. Its result is pure chance.

Most games you love sit between these ends, and designers disagree about where the right spot is. That disagreement is healthy. What isn't healthy is putting randomness in a game by reflex, or taking it out by reflex, without knowing what it does.

### What randomness buys you

- **Weaker players win sometimes.** If a beginner can never beat an expert, the beginner stops playing, and the expert runs out of opponents. A little luck keeps the losing side hopeful, and the chapter on luck and skill in this week's reading returns to this idea often.
- **Variety.** A shuffled deck makes every game of the same card game start differently. You get replay value without designing new content.
- **A game players can't solve.** Week 9 showed that tic-tac-toe stops being fun once you know the answer. Randomness keeps the answer changing, so there is always something to decide.
- **Stories.** The last-turn comeback on a lucky roll is the thing people retell. A game with no uncertainty has no suspense.

### What randomness costs you

- **It hides skill.** A good player who loses to a bad roll learns nothing about their play. Neither does the observer.
- **It slows learning.** If you try a new strategy and win, was it the strategy or the dice? The noisier the result, the more games you need before you can tell.
- **It can feel unfair.** Players forgive a loss they caused. They resent a loss the game caused, and they remember streaks of bad luck much longer than streaks of good luck. MA102 spends two weeks on this ([the gambler's fallacy](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w02-independent-events-and-the-gamblers-fallacy.md) and [pseudo-random distribution and pity timers](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w10-pseudo-random-distribution-and-pity-timers.md)).

So the question is never "should there be luck?" The question is "how much does luck move the result, compared with skill?" The worked example turns that question into a number.

## 2. Worked example: the luck dial

### The hook

Chess has no dice, but it still has upsets. The Elo rating system, used by FIDE for international chess, predicts that a player rated 200 points above their opponent will score about 76% against them. So even in a game with no randomness at all, the weaker player wins or draws a real share of games, because human performance varies from day to day.

Now look at Magic: The Gathering. Its official tournament rules say a match is played until one player has won a set number of games, usually two. That is a best-of-three. Why doesn't the tournament just play one game and move on? It would take a third of the time.

Both facts point at the same idea. Every result is skill plus some randomness, and the designer (or the tournament organizer) decides how much randomness gets through. Let's build the smallest possible model of that and play with it.

### The model: skill plus a die

Two players, A and B, play a round. Each has a fixed **skill score**. Each rolls one die with `d` faces, numbered 1 to `d`, and adds it to their skill score. The higher total wins the round. If the totals are equal, both roll again.

Call the difference in skill scores the **skill gap**, `g`. Say A is the stronger player, so A's skill is `g` points higher than B's. Then A wins a round when:

```
A's roll + g  >  B's roll
```

There are only three symbols:

- `g`, the skill gap, a whole number of points. This is the part players control over time, by practicing.
- `d`, the die size. This is the part the designer controls, and it is the **luck dial**. A bigger die means more randomness per round.
- `p`, the chance that A wins one round (with ties re-rolled). This is what we want.

Because ties are replayed, `p` is the number of winning roll pairs divided by the number of roll pairs that are not ties:

```
p = W / (W + L)
```

where `W` counts the pairs of rolls where A wins and `L` counts the pairs where B wins.

### Numbers you can check: counting the grid

With a six-sided die there are 6 × 6 = 36 pairs of rolls. Draw a 6 by 6 grid. A's roll goes along the rows, B's roll along the columns. For `g = 1`, mark each square W, T (tie) or L.

| A rolls \ B rolls | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 1 (total 2) | W | T | L | L | L | L |
| 2 (total 3) | W | W | T | L | L | L |
| 3 (total 4) | W | W | W | T | L | L |
| 4 (total 5) | W | W | W | W | T | L |
| 5 (total 6) | W | W | W | W | W | T |
| 6 (total 7) | W | W | W | W | W | W |

Count them: 21 W, 5 T, 10 L. So `p = 21 / 31 = 0.677`. A one-point edge on a d6 wins about two rounds in three.

Now swap the d6 for a d20. The grid has 400 squares and you don't want to count them by hand, but there's a shortcut. The tie squares sit on one diagonal, and there are `d − g` of them. The loss squares form a triangle in the corner with `(d − g − 1)(d − g) / 2` squares. Everything else is a win. Check it on the d6: ties `6 − 1 = 5`, losses `4 × 5 / 2 = 10`, wins `36 − 5 − 10 = 21`. It matches the grid.

For the d20 with `g = 1`: ties 19, losses `18 × 19 / 2 = 171`, wins `400 − 19 − 171 = 210`, so `p = 210 / 381 = 0.551`.

Here is the whole table. Every entry comes from the same three counts.

| Die | Skill gap g | Wins W | Ties | Losses L | p = W/(W+L) |
|---|---|---|---|---|---|
| d6 | 1 | 21 | 5 | 10 | 0.677 |
| d6 | 2 | 26 | 4 | 6 | 0.813 |
| d6 | 3 | 30 | 3 | 3 | 0.909 |
| d12 | 1 | 78 | 11 | 55 | 0.586 |
| d12 | 2 | 89 | 10 | 45 | 0.664 |
| d12 | 3 | 99 | 9 | 36 | 0.733 |
| d20 | 1 | 210 | 19 | 171 | 0.551 |
| d20 | 2 | 229 | 18 | 153 | 0.599 |
| d20 | 3 | 247 | 17 | 136 | 0.645 |

Read down a column and you see the design lesson. The same skill gap is worth much less on a bigger die. A three-point edge wins 91% of rounds on a d6 and only 64.5% on a d20. **What matters is the skill gap compared with the size of the randomness, not either one alone.** A d20 with a 3-point gap feels about as skillful as a d6 with a gap of less than one point.

### Turning rounds into matches

Now use the Magic idea. Instead of one round, play a best-of-3: the first player to win two rounds wins the match. A wins the match in three ways: win-win, win-lose-win, or lose-win-win. So:

```
P(A wins best-of-3) = p × p + p × (1 − p) × p + (1 − p) × p × p
                    = p² × (3 − 2p)
```

Check with the d20, `g = 2`, `p = 0.599`: `0.599² × (3 − 1.198) = 0.3588 × 1.802 = 0.647`. The best-of-3 turned a 60% round edge into a 65% match edge.

Longer matches follow the same logic with more paths. The general rule counts the ways to win a majority of `n` rounds, which is the binomial distribution you'll meet in [MA102 week 6](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w06-binomial-crits-over-a-fight.md). You don't need the formula today; the interactive computes it, and the table gives you the values to check against.

| Round edge p | Best of 1 | Best of 3 | Best of 5 | Best of 7 | Best of 15 |
|---|---|---|---|---|---|
| 0.55 | 0.550 | 0.575 | 0.593 | 0.608 | 0.654 |
| 0.60 | 0.600 | 0.648 | 0.683 | 0.710 | 0.787 |
| 0.65 | 0.650 | 0.718 | 0.765 | 0.800 | 0.887 |
| 0.70 | 0.700 | 0.784 | 0.837 | 0.874 | 0.950 |

Two things stand out. First, every extra round helps the stronger player, because luck in different rounds tends to cancel while skill shows up every time. Second, when the round edge is small, you need a lot of rounds. At `p = 0.55`, even fifteen rounds leave the weaker player winning about a third of matches. Counted one odd length at a time, the stronger player first reaches an 80% match win rate at a best-of-71.

So you now have **three dials**, and they trade off against each other:

1. **Die size `d`** (how much randomness per round).
2. **Skill gap `g`** (how much the game lets practice show, for example by giving choices that matter more).
3. **Match length `n`** (how many independent rounds decide the winner).

Want a game where a one-point edge wins 80% of matches? On a d6 that takes a best-of-5 (0.806). On a d20, where the exact round edge is `210/381 = 0.551`, it takes a best-of-67, which nobody will sit through. The d20 game needs a bigger skill gap or a smaller die.

### A visual you can move

Open [`examples/w10-luck-dial.html`](../examples/w10-luck-dial.html). The left panel is the roll grid from the table above, colored win, tie and loss, and it redraws as you change the die size and the skill gap. The right panel plots A's chance to win a match against match length. Start at d6 with `g = 1`, then slide the die up to d20. Watch the loss triangle on the left grow toward half the grid while the curve on the right flattens toward 50%. Then drag the match length up and watch the curve climb back. The insight to take away is that the same one-point edge can look decisive or invisible depending only on the die, and that match length buys the skill back at a cost in time.

### Cross-game recognition

**Chess ratings.** The Elo system assumes each player's performance in a game is their rating plus a random swing, the same "skill plus a die" structure. Its expected-score formula is `E = 1 / (1 + 10^(−D/400))`, where `D` is the rating difference. The number 400 plays the role of our die size: it sets how big the random swing is compared with the skill gap. Plug in `D = 200` and you get 0.76, the figure from the hook. You can also run it backwards. Our d20 with a one-point gap gives `p = 0.551`, which Elo would call a rating gap of about 36 points. A d6 with a one-point gap gives 0.677, about 129 points.

**Magic tournament matches.** Magic has a lot of randomness per game, because each player draws from a shuffled deck, and a player can lose to drawing too few or too many lands no matter how well they play. The tournament rules answer with match length: usually first to two game wins. From our table, a player who wins 60% of games wins about 65% of best-of-3 matches. The organizer can't shrink the die (the shuffle is the game), so they turn the third dial instead.

**Tennis.** Tennis nests the same idea several levels deep. A game goes to four points with a two-point margin. A set goes to six games with a two-game margin, with a tiebreak at six-all. A match is best of three or best of five sets. Each level is a longer "match" built from the level below, so by the same arithmetic as our table, a small edge on individual points grows at every level.

Three settings, one idea. When you look at any competitive structure, ask the same questions: how big is the random swing per round, how big is the typical skill gap, and how many independent rounds decide the result?

### Eyes-open design judgment

There is no correct amount of luck. There is a right amount for your players and your match length.

- **Short games can afford more luck.** A ten-minute party game with a big die is fine; if you lose, you play again. A four-hour strategy game that a single roll can decide is miserable, because the cost of a bad beat is four hours.
- **Mixed-skill groups need more luck.** Families and first-time players want everyone to have a chance. Tournament players want the better player to win. Some games serve both with two modes: casual play with one game, competitive play with a best-of structure.
- **Match length is expensive.** Every extra round costs time and attention. Before you add rounds, ask whether you can raise the skill gap instead by giving players decisions that matter more, which is week 9's topic.
- **Making the die smaller isn't free.** A tiny die means the stronger player almost always wins, and then the result feels decided before it starts. That removes the suspense, the week 9 problem from the opposite side.
- **Watch the loss triangle, not the average.** Two designs can give the same average and very different chances of an upset. Always ask what happens to the weaker player.

### Check yourself (worked example)

1. With a d8 and `g = 2`, count W, T and L using the shortcut and compute `p`.
2. A designer wants a one-roll game in which a 1-point skill edge wins at least 60% of rounds. What is the largest die from d6, d8, d10, d12 and d20 that achieves it? (Hint: compute `p` for d10 and d12.)
3. A game has round edge `p = 0.65`. How many rounds must a best-of-n have before the stronger player wins at least 80% of matches?

<details>
<summary>Answers</summary>

1. Ties `8 − 2 = 6`, losses `5 × 6 / 2 = 15`, wins `64 − 6 − 15 = 43`. `p = 43 / 58 = 0.741`.
2. d10, `g = 1`: ties 9, losses `8 × 9 / 2 = 36`, wins `100 − 45 = 55`, `p = 55 / 91 = 0.604`. d12: `p = 78 / 133 = 0.586`. The d10 is the largest that clears 60%.
3. From the table, best of 7 gives 0.800. Best of 5 gives only 0.765. So best of 7.

</details>

## 3. Where the randomness sits: input and output

The luck dial measures how much randomness there is. Just as important is *when* it arrives compared with the player's decision. Tabletop designers use two terms for this.

**Output randomness** comes after the decision. You choose to attack, then a roll decides if the attack hits. XCOM: Enemy Unknown (2012) is the familiar example: the interface shows your percentage chance to hit before you take the shot, you commit, then the game rolls. Your skill goes into choosing good odds. The roll then decides whether that choice pays off.

**Input randomness** comes before the decision. The game deals you a random situation and you decide how to handle it. In Slay the Spire (full release 2019), after most fights you are offered one of three randomly selected cards to add to your deck. The randomness picks the menu. You pick from it, and your pick is where skill enters.

The two feel different, for reasons you can predict from the model.

- Output randomness sits between the decision and the result, so it is exactly the "die" in our model. It adds noise to every decision and makes a good choice look bad some of the time. Players feel it as unfairness: "95% and I missed."
- Input randomness sits before the decision, so it creates new decisions instead of blurring old ones. A bad hand is still a problem you can play well or badly. Skill shows up in how you respond, and the result still tracks the quality of your play.

This doesn't make input randomness good and output randomness bad. Output randomness creates suspense at the moment of action, which is where drama lives. A sword fight in which every swing lands exactly as planned has no held breath before the roll. Many games mix both: a random hand (input), then a dice roll for combat (output). What you want to avoid is output randomness so large that it swamps the decision, which in our model is a die far bigger than any skill gap the game can create.

A practical test during playtesting: after a loss, ask the player "what would you do differently?" If they can name a decision, the game's luck is leaving room for skill. If they shrug and say "roll better," it isn't.

## 4. Many small rolls or one big roll

Our model had one roll per round. Real games usually have many random events inside one game: every attack, every draw, every spawn. How they combine matters as much as their size.

Think back to the match table. A best-of-15 made of 60% rounds gave the stronger player a 79% match. The same thing happens *inside* a single game if it contains many small random events whose effects add up. Each small roll is like a round. The more of them there are, the more they cancel, and the more the final result reflects the choices that stayed constant across them.

That gives you a fourth dial, hiding inside the other three. You can keep the same total amount of randomness but split it into more, smaller pieces. Here is the difference in one sentence. One d20 roll at the end of a game can swing anything; twenty small d20 rolls spread across the game mostly average out. MA102 shows why sums of dice pile up in the middle ([week 8](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w08-dice-sums-and-the-normal-curve.md)), but you can feel it without the math: roll one die and anything happens, roll ten and add them and you almost always land near the middle.

Designers use this in both directions:

- **Spread randomness thin** when you want skill to decide the game and luck to add texture. Many small rolls, small cards, small random events.
- **Concentrate it** when you want a dramatic late swing. A single high-stakes roll near the end gives every player a chance, which is exactly right for a party game and exactly wrong for a tournament.

Watch the **timing** too. A big random event early in a game gives players time to respond, so it acts more like input randomness. The same event on the last turn leaves no response, so it acts purely as output randomness. If a playtester says a loss "came out of nowhere," check where in the game your biggest random swings sit.

## 5. How players judge randomness

Players don't measure luck with a grid. They judge it with memory, and memory is biased.

- They remember losses to luck and forget wins from luck. So a system that is perfectly fair on paper will be described as "rigged" in reviews.
- They see streaks in truly random sequences and conclude the random number generator is broken. Three misses at 80% happen about once in 125 tries, and a player who makes a few hundred attacks will see it several times.
- They treat displayed percentages as promises. A 90% shot that misses feels like a broken promise, even though it should happen one time in ten.

Shipped games respond to this in several ways, from hiding the number to quietly bending the dice so streaks happen less often. MA102 [week 10](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w10-pseudo-random-distribution-and-pity-timers.md) covers those tools and their costs. For now, the design point is simpler: what players *feel* about your randomness is a design output too. You measure it the same way you measure anything else in week 7's playtests, by watching what players do and listening to what they say after a loss.

## In-class activity (25 minutes)

Work in pairs. You need one d6, one d20 (or a dice app) and a sheet of paper.

1. **Play the model (8 minutes).** Player A adds +1 to every roll. Play 20 rounds with the d6 and tally who wins each round, re-rolling ties. Then play 20 rounds with the d20. Write both win rates on the board.
2. **Pool the class data (5 minutes).** Add up all pairs' tallies for each die. Compare the class totals with the table: 0.677 for the d6 and 0.551 for the d20. How close did twenty rounds per pair get? How close did the whole class get?
3. **Design to a target (10 minutes).** Your design brief: "a strong player should win about 70% of best-of-3 matches, and a match should take no more than 3 rounds." Choose a die and a skill gap from the table that meet it, and show the numbers. Then write one sentence on what kind of player this game suits.
4. **Share (2 minutes).** Two pairs read their choice aloud. Did anyone pick a different die with a different gap and land on the same match rate?

Expected output: a tally sheet, a class comparison, and a one-paragraph design choice with numbers.

## Common misconceptions

- **"More randomness makes a game more balanced."** Randomness pulls every matchup toward 50%, which hides imbalance rather than fixing it. A game where one strategy is clearly better still has that strategy; luck just makes it slower to notice. Week 11 is about finding exactly those hidden problems.
- **"Skill games have no luck."** Chess has no dice, yet the Elo model still predicts that a 200-point underdog scores about a quarter of the time. Human performance varies, so every game has a random component. The question is its size compared with the skill gap.
- **"If a player wins more, they're more skilled."** Only after enough rounds. At `p = 0.55`, a stronger player loses about 35% of best-of-15 matches, so small samples can crown the wrong player. That is why tournaments play several games per match and several rounds per event.
- **"Input randomness is skillful, output randomness is luck."** Both are luck. The difference is whether a decision comes after the random event (input) or before it (output). Input randomness tends to leave more room for skill, but a deal can still be so bad that no decision saves it.

## Check yourself

1. Game X uses a d10 and a skill gap of 3. Game Y uses a d6 and a skill gap of 2. Which gives the stronger player a larger round edge? Show the counts.
2. A designer halves the die size of their game from d20 to d10 while keeping the skill gap at 2. Compute `p` before and after, and describe in one sentence how the game will feel different to a weaker player.
3. A tournament uses one game per match, and the stronger player wins 65% of games. Organizers want the stronger player to win at least 75% of matches. What is the shortest best-of-n that achieves it?
4. Classify each random element as input or output randomness: (a) a card game deals each player five cards at the start; (b) a strategy game rolls a die after you declare an attack to decide whether it succeeds; (c) a racing game randomly picks the track before players choose their cars.

<details>
<summary>Answers</summary>

1. X: ties `10 − 3 = 7`, losses `6 × 7 / 2 = 21`, wins `100 − 28 = 72`, `p = 72 / 93 = 0.774`. Y: from the table, `p = 26 / 32 = 0.813`. Y gives the larger edge, even though X has the bigger gap, because Y's die is smaller.
2. d20, `g = 2`: `p = 0.599`. d10, `g = 2`: ties 8, losses `7 × 8 / 2 = 28`, wins `100 − 36 = 64`, `p = 64 / 92 = 0.696`. The weaker player's round wins drop from about 40% to about 30%, so upsets become rarer and the stronger player's advantage is visible much sooner.
3. From the table at `p = 0.65`: best of 3 gives 0.718, best of 5 gives 0.765. Best of 5 is the shortest that clears 75%.
4. (a) Input, the random hand comes before any decision. (b) Output, the roll comes after the decision to attack. (c) Input, the random track comes before the car choice.

</details>

## Lab hook

**Lab 10: Measuring luck in your prototype.** You first check this lecture's model against 100 rolled rounds and a spreadsheet simulation. Then you audit every random element in your own paper prototype, classify it as input or output randomness, run a small experienced-versus-new-player test, and change one dial to move the upset rate toward a target you choose. The deliverable is a luck audit table, a before-and-after result and a 250-word design note. See [labs/lab10.md](../labs/lab10.md).

## Sources

- Milton Bradley, Candy Land (1949). Wikipedia, "Candy Land": players never make choices, the game is described as complete chance.
- Wikipedia, "Elo rating system": expected score `1 / (1 + 10^((R_B − R_A)/400))`; a 200-point advantage gives an expected score of about 76%; FIDE uses Elo's rating-difference table.
- Wizards of the Coast, Magic Tournament Rules, section 2.1 "Match Structure", as annotated by the Magic Judges rules blog (accessed September 2026): a match is played until one player wins a set number of games, usually two.
- Wikipedia, "Tennis scoring system": game to four points with a two-point margin, set to six games with a two-game margin and tiebreak, matches best of three or five sets.
- Firaxis Games, XCOM: Enemy Unknown (2012). Wikipedia, "XCOM: Enemy Unknown": the interface shows the chance of a successful shot before the player commits.
- Mega Crit, Slay the Spire (full release 2019). Wikipedia, "Slay the Spire": after a won encounter the player usually receives a choice of one of three randomly selected cards; the map is a branching structure.
- Elias, G. S., Garfield, R. & Gutschera, K. R. (2012). *Characteristics of Games*. MIT Press. The chapter on luck and skill (assigned reading).
- Schreiber, I. (2010). *Game Balance Concepts*, Level 1 "Intro to Game Balance" (gamebalanceconcepts.wordpress.com): vocabulary of determinism and solvability.
- Costikyan, G. (2013). *Uncertainty in Games*. MIT Press. Background on the many sources of uncertainty beyond dice.
- The d6, d12 and d20 win counts and best-of-n values in section 2 are computed from the model in this lecture, not taken from any game.

## Interactive spec: examples/w10-luck-dial.html

**Purpose.** Let students see how the die size shrinks a fixed skill edge, and how match length wins it back.

**The one insight the visual must make obvious.** The same one-point skill edge is decisive on a small die and nearly invisible on a big one, and a longer match restores it at a cost in rounds.

**Layout.** Two linked views side by side on desktop, stacked at 390px. A results strip under them.

- Left, "One round": a `d × d` grid of squares. Row = A's roll (1 at top), column = B's roll (1 at left). Each square colored by outcome for A: win, tie, loss. Use the palette's positive, neutral and negative tokens plus a text or pattern difference (tie squares get a diagonal hatch) so color is not the only cue. For `d = 100` draw the grid as a canvas image without borders. Under the grid print `W`, `T`, `L` and `p = W/(W+L)` to three decimals.
- Right, "Whole match": line chart. x axis match length `n` = 1, 3, 5, ..., 31 (odd only). y axis P(A wins match) from 0.5 to 1.0. Plot the curve for the current `p` as a solid line with dots. A dashed horizontal line at the target (control below). Mark the first `n` where the curve reaches the target with a labeled dot ("best of 7 reaches 80%"). If it is not reached by 31, show text "needs more than 31 rounds (about N)", with N computed by continuing the loop up to 999.
- Results strip: "Round edge p", "Best of n chosen", "Match win chance", "Equivalent Elo gap" `= −400 × log10(1/p − 1)` rounded to a whole number.

**Controls** (all keyboard accessible, current values printed):

- Die size `d`: segmented buttons 4, 6, 8, 10, 12, 20, 100. Default 6.
- Skill gap `g`: slider 0 to `d − 1`, step 1, default 1. Clamp when `d` changes.
- Match length `n`: slider over odd values 1 to 31, default 3. Highlights the matching dot on the right chart.
- Target match win rate: slider 0.55 to 0.95, step 0.05, default 0.80.
- "Compare" toggle: when on, draw a second, fainter curve on the right chart for a frozen previous setting, labeled with its `d` and `g`, so students can compare d6 and d20 on one chart.
- Reset button.

**Formulas.**

- Ties `T = d − g`. Losses `L = (d − g − 1)(d − g) / 2`. Wins `W = d² − T − L`. Round edge `p = W / (W + L)`. When `g = 0`, `p = 0.5`.
- Grid square (a, b) is a win if `a + g > b`, tie if `a + g = b`, loss otherwise.
- `P(A wins best of n) = Σ from k = (n+1)/2 to n of C(n, k) p^k (1 − p)^(n − k)`.

**Test values.**

| d | g | W | T | L | p | Best of 3 | Best of 5 | Best of 7 |
|---|---|---|---|---|---|---|---|---|
| 6 | 1 | 21 | 5 | 10 | 0.677 | 0.755 | 0.806 | 0.843 |
| 6 | 2 | 26 | 4 | 6 | 0.813 | 0.908 | 0.951 | 0.973 |
| 12 | 1 | 78 | 11 | 55 | 0.586 | 0.628 | 0.659 | 0.684 |
| 20 | 1 | 210 | 19 | 171 | 0.551 | 0.577 | 0.595 | 0.611 |
| 20 | 2 | 229 | 18 | 153 | 0.599 | 0.647 | 0.682 | 0.709 |
| 20 | 3 | 247 | 17 | 136 | 0.645 | 0.711 | 0.757 | 0.792 |

At d20, g 1, target 0.80: first odd n reaching it is 67 (computed with the exact `p = 210/381`; with `p` rounded to 0.55 it would be 71). Equivalent Elo gaps: d6 g1 about 129, d20 g1 about 36.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`, light and dark themes, reduced motion respected (no animated grid fill when reduced motion is set). No game art; players are labeled "A (stronger)" and "B".
