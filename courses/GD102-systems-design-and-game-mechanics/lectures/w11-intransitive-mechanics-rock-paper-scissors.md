# GD102 · Week 11 — Intransitive Mechanics: Rock-Paper-Scissors

**Why this matters:** Counters are how games keep many options alive at once. Spearmen beat cavalry, cavalry beat archers, and archers beat spearmen. The first time you make one counter hit harder than the others, players will not do what you expect, and you need to predict what they will do instead before you ship the change.

**You will be able to:**
- Tell a transitive relationship from an intransitive one, and explain why an intransitive loop works as a balancing feedback loop on popularity.
- Write a three-option counter game as a payoff matrix and compute each option's expected payoff against a given opponent mix.
- Compute the stable mix of a rock-paper-scissors game with unequal payoffs, and predict how it moves when one payoff changes.
- Critique a proposed counter change in terms of what players will do in the first week and in the long run.

**Before class:** Adams & Dormans, *Game Mechanics: Advanced Game Design* (2012), the sections on feedback in chapter 3. Meadows, *Thinking in Systems* (2008), chapter 2, the part on balancing loops with delays. Schreiber, *Game Balance Concepts* (2010, free online), "Level 9: Intransitive Mechanics", up to the end of the weighted rock-paper-scissors section.

**Prerequisites from earlier courses:** Expected value from [MA102 week 4](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md). Dominant strategies from GD101 [week 11](../../GD101-introduction-to-game-design/lectures/w11-dominant-strategies-and-how-to-spot-them.md). From this course, [week 3, positive feedback](w03-positive-feedback-loops-snowballing.md), [week 4, negative feedback](w04-negative-feedback-loops-rubber-banding.md), [week 5, Machinations diagrams](w05-machinations-diagrams-i.md), and [week 10, emergence vs progression](w10-emergence-vs-progression.md). This lecture is the first-year version of material you will meet again in MMO303 [week 9, intransitivity and counters](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w09-intransitivity-and-counters.md) and [week 10, payoff matrices and Nash equilibria](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w10-game-theory-payoff-matrices-and-nash-equilibria.md).

**Interactive:** [Weighted rock-paper-scissors](../examples/w11-weighted-rps.html). Keep it open during section 2.

---

## 1. Transitive and intransitive

A relationship is **transitive** if it passes along a chain. If a longsword beats a dagger, and a greatsword beats a longsword, then a greatsword beats a dagger. Height, damage per second and item level are usually transitive. Transitive relationships make a ladder. The top rung is always the best choice, so a game made only of them has a dominant strategy (GD101 week 11). Players find the top rung, and every other option becomes a trap for beginners.

A relationship is **intransitive** if it does not pass along the chain. Rock beats scissors, scissors beats paper, and paper beats rock. Follow the chain and you come back to where you started. There is no top rung. Each option is the best answer to one thing and the worst answer to another.

Designers use intransitive relationships, often called **counters**, to keep several options alive at once. Unit types in strategy games, attack types in fighting games, and type charts in monster-collecting games are all counter systems. The simplest one has three options in a loop, and that is the one this lecture analyzes completely.

### The loop as a feedback system

This is a systems course, so look at a counter triangle as a system. The stocks are the shares of players choosing each option. Now trace one arrow around the loop.

1. More players choose rock.
2. Paper, which beats rock, now wins more often.
3. Players notice and switch to paper.
4. Scissors, which beats paper, now wins more often.
5. Players switch to scissors.
6. Rock, which beats scissors, now wins more often.

Each option's popularity raises the payoff of its counter, which pulls players away from it. That is a **balancing loop**, the negative feedback of week 4. It pushes the system back toward a middle state whenever it drifts.

There is a catch. Players react with a delay. They notice what is winning after some games, not instantly. Meadows's chapter 2 shows what happens to a balancing loop with a delay. It overshoots, then corrects, then overshoots the other way. The system oscillates around its goal instead of settling on it. Counter metas do exactly this. Rock surges, then paper, then scissors, and the average over a long season sits near the middle state while no single week does.

So the questions a designer must answer are these. Where is the middle state? And how does it move when you change the numbers?

## 2. Worked example: the weakest win is the one you should use most

### The hook

David Sirlin's card game *Yomi* (2011) turns a fighting game's guessing into cards. Its core triangle is the fighting-game one. **Attacks** beat throws. **Throws** beat blocks. **Blocks** beat attacks. The three wins are not worth the same. An attack that wins deals damage. A throw that wins deals damage and often knocks the opponent down. A block that wins deals no damage at all. It stops the attack and lets you draw a card.

So blocking gives the smallest reward of the three. Should you block less than you attack?

The model below says no. In a stripped-down version of this triangle, with the block paying the least, the stable mix has players blocking more than anything else. Most students get this backwards the first time. By the end of the section you will be able to predict it in your head.

(We are modeling the triangle, not *Yomi* itself. The real game has card speeds, combos, many damage values and more card types. The point is the shape of the loop.)

### The model

Name the three options by what they beat, so the loop is always the same shape. Use rock, paper and scissors as generic names.

- Rock beats scissors. A rock win is worth `w_R`.
- Paper beats rock. A paper win is worth `w_P`.
- Scissors beats paper. A scissors win is worth `w_S`.

The game is **zero-sum**: whatever the winner gains, the loser loses. A tie is worth 0 to both. That gives the **payoff matrix**, a table of what the row player gets for each pair of choices.

| You \ Opponent | Rock | Paper | Scissors |
|---|---|---|---|
| **Rock** | 0 | −w_P | +w_R |
| **Paper** | +w_P | 0 | −w_S |
| **Scissors** | −w_R | +w_S | 0 |

Now suppose the opponent (or the whole player population you are matched against) plays rock with probability `r`, paper with `p` and scissors with `s`, where `r + p + s = 1`. The expected payoff of each of your options is one row of the table, weighted by those probabilities (MA102 week 4):

```
E(Rock)     = w_R × s − w_P × p
E(Paper)    = w_P × r − w_S × s
E(Scissors) = w_S × p − w_R × r
```

The **stable mix** is the one where no option is better than any other against it. If one option had a higher expected payoff, players would move toward it and the mix would change. So at the stable mix all three expected payoffs are equal. By symmetry of the zero-sum game, they all equal 0. Set each line to zero and solve:

```
w_R × s = w_P × p
w_P × r = w_S × s
```

Solving these together gives shares proportional to three numbers:

```
r : p : s  =  w_S : w_R : w_P
```

Divide each by `w_R + w_P + w_S` to turn them into percentages.

Read that result slowly, because it is the whole lecture. **Each option's share equals the prize of the option it beats.** Rock's share is set by `w_S`, the prize scissors earns. Rock beats scissors. Paper's share is set by `w_R`, the prize rock earns, and paper beats rock. Scissors's share is set by `w_P`.

Your own prize does not set your own share. It sets the share of your counter.

(Game theorists call this stable mix a **mixed-strategy Nash equilibrium**. MMO303 week 10 defines the term properly and solves bigger matrices. For now, "stable mix" is enough.)

### Numbers you can check

Keep `w_P = w_S = 1` and raise the prize for a rock win. Use `r : p : s = w_S : w_R : w_P = 1 : w_R : 1`.

| Rock's prize `w_R` | Rock | Paper | Scissors | E(Rock) vs a 1/3 mix | E(Scissors) vs a 1/3 mix |
|---|---|---|---|---|---|
| 1 | 33.3% | 33.3% | 33.3% | 0 | 0 |
| 1.5 | 28.6% | 42.9% | 28.6% | +0.167 | −0.167 |
| 2 | 25.0% | 50.0% | 25.0% | +0.333 | −0.333 |
| 3 | 20.0% | 60.0% | 20.0% | +0.667 | −0.667 |
| 4 | 16.7% | 66.7% | 16.7% | +1.000 | −1.000 |

Check the `w_R = 2` row by hand. Shares `1 : 2 : 1`, total 4, so 25%, 50%, 25%. Now confirm the stable mix really is stable. Against `r = 0.25, p = 0.5, s = 0.25`:

```
E(Rock)     = 2 × 0.25 − 1 × 0.5  = 0
E(Paper)    = 1 × 0.25 − 1 × 0.25 = 0
E(Scissors) = 1 × 0.5  − 2 × 0.25 = 0
```

All three are zero. No option beats any other, so nobody has a reason to switch.

Look at the last two columns. They show the **first-week** picture. Before players adapt, they are still playing an even third each. Against that mix, rock's expected payoff is `(w_R − 1)/3`, which is positive. Rock looks like the best option in the game. Players rush to it. And the long-run answer to "rock got stronger" is that rock gets rarer and paper, rock's counter, becomes the most common choice. The two columns point one way. The stable mix points the other. That is the balancing loop from section 1, with numbers.

Now the *Yomi*-shaped triangle. Say an attack win is worth 3, a throw win 2, and a block win 1. Attacks beat throws, throws beat blocks, blocks beat attacks. Apply the rule "your share equals the prize of what you beat":

- Attack beats throw, so attack's share is set by the throw prize, 2.
- Throw beats block, so throw's share is set by the block prize, 1.
- Block beats attack, so block's share is set by the attack prize, 3.

Shares `2 : 1 : 3`, total 6. Attack 33.3%, throw 16.7%, block 50.0%. The weakest win (block) is the most used option. The reason is visible in the rule. Block's small prize makes throwing, the counter to block, a poor investment. Throws become rare. With throws rare, blocking is safe, and it is the answer to the attack, which carries the biggest prize in the game. Check indifference: with `a = 1/3, t = 1/6, b = 1/2`, E(attack) `= 3 × 1/6 − 1 × 1/2 = 0`, E(throw) `= 2 × 1/2 − 3 × 1/3 = 0`, E(block) `= 1 × 1/3 − 2 × 1/6 = 0`.

### A visual you can move

Open the interactive. The left panel is the payoff matrix, with three sliders for `w_R`, `w_P` and `w_S`. The cells update as you drag, colored by sign.

The right panel has two linked views of the same numbers. The top view shows three bars, the expected payoff of each option against a naive even mix. The bottom view shows the stable mix as one stacked bar.

Start at `w_R = w_P = w_S = 1`. All top bars are at zero. The stable mix is thirds. Now drag `w_R` from 1 to 3. In the top view, the rock bar climbs and the scissors bar drops. Rock looks like the winner. In the bottom view, the rock segment *shrinks* from 33.3% to 20% and the paper segment grows to 60%. Same slider, two views that disagree, and the disagreement is the lesson.

Then press **Run a season**. A population of players starts at an even mix and adjusts a little each round toward whatever is winning. You will see it overshoot, swing through rock, paper and scissors in turn, and circle the stable mix without settling. A dashed marker shows the running average, which drifts toward the stable mix. That is Meadows's balancing loop with a delay, drawn as a spiral.

### Cross-game recognition

**Schreiber's weighted rock-paper-scissors.** Ian Schreiber's free *Game Balance Concepts* course (Level 9) works through a version where every rock win counts double. He finds that the optimal mix plays paper half the time and rock and scissors a quarter each. That is our `w_R = 2` row. He connects it to fighting games, where moves in a counter cycle do different damage. MMO303 week 10 revisits the same example for class balance.

**Pokémon's starter trio.** A main-series Pokémon game usually opens with the player choosing a first partner from three types, Grass, Fire and Water. Fire hits Grass for double damage, Water hits Fire for double, Grass hits Water for double, and each resists the type it beats (half damage). In our model the three links are equal, so the stable mix is a third each. That is a sensible property for a first choice. No starter is the right answer to the others, so the choice is about taste. The full chart of eighteen types is a much bigger counter graph with uneven links, which is where MMO303 week 9 picks the idea up.

**Side-blotched lizards.** Outside games entirely, males of the lizard *Uta stansburiana* come in three throat colors with three mating strategies. Orange males hold large territories and beat blue males. Blue males guard one or two females closely and beat yellow males. Yellow "sneaker" males slip into orange territories and beat orange males. Sinervo and Lively reported this in *Nature* in 1996 under a title that names the game. Write it in our form. Rock is orange, scissors is blue, paper is yellow. The morph shares in the population cycle rather than settling, the same delayed balancing loop as a player meta. The payoffs there are offspring rather than points, which is a reminder that the model is about the loop, not about games.

Three contexts, one rule. When you meet a counter loop, list what each option beats and what each win is worth. Then the stable share of each option is the prize of the thing it beats.

### Eyes-open design judgment

- **Unequal prizes are a tool, not an error.** If you want an option to be common, give a big prize to the thing it beats. If you want an option to be rare but dramatic, give it a big prize of its own. Players will then rarely need it, but it will matter when they do. That is how you get "big move" options that appear sparingly without being useless.
- **Buffs move the counter, not the target.** The rule tells you that raising an option's reward raises the share of its counter. If your goal is to see more of an option, raise the prize of the thing it beats, or weaken the option that counters it.
- **Expect a first-week spike in the wrong direction.** Against the old mix, the buffed option wins more and gets more popular. Your telemetry will say the buff "worked" or "overshot" before the loop turns. Judge a counter change by where the running average settles over weeks, not by the first days.
- **Delays make the swing bigger.** The slower players adapt (few matches, little information), the wider the oscillation. Good in-game information about what is winning shortens the delay and calms the meta. Hiding it lengthens the swing.
- **Three options and no ties is a toy.** Real counter systems have partial counters, more options and skill in execution. The model's value is the direction of the effect, which survives in bigger systems. Its exact percentages do not.
- **Transitive layers break the loop.** If one option is also simply stronger (a higher damage number that applies against everything), the loop tilts and may collapse into a dominant strategy. Keep the counter relationships separate from any overall power stat, or balance the two together deliberately.

### Check this example

1. A three-way loop pays `w_R = 1`, `w_P = 3`, `w_S = 2`. What is the stable mix?
2. In the same game, the players are still at an even mix. Which option has the highest expected payoff this week?
3. You want scissors to be exactly 50% of play, with `w_P = 1` and `w_S = 1`. What must `w_R` be? If no value works, explain why using the rule.

<details>
<summary>Answers</summary>

1. `r : p : s = w_S : w_R : w_P = 2 : 1 : 3`, total 6. Rock 33.3%, paper 16.7%, scissors 50.0%.
2. Against thirds: E(Rock) `= (1 − 3)/3 = −0.667`, E(Paper) `= (3 − 2)/3 = +0.333`, E(Scissors) `= (2 − 1)/3 = +0.333`. Paper and scissors tie at +0.333. Rock is the worst.
3. Scissors's share is `w_P / (w_R + w_P + w_S) = 1 / (w_R + 2)`. For 50%, `w_R + 2 = 2`, so `w_R = 0`. A rock win worth nothing means rock never wins anything, and the loop breaks. So 50% is out of reach with these two prizes fixed. To make scissors common, raise `w_P`, the prize of what scissors beats.

</details>

## 3. Reading a counter chart as a system

The worked example had one loop of three. Real counter systems are bigger, and the systems view from section 1 still helps.

**Draw the graph.** Put each option in a box. Draw an arrow from each option to every option it beats. Label the arrow with the size of the win. This is a Machinations-style diagram of influence (weeks 5 and 6), except the resource flowing along the arrows is player share.

**Look for sinks and dominance.** An option with arrows going out and none coming in beats something and is beaten by nothing. That is a dominant option, and the loop will drain everything toward it. An option with arrows coming in and none going out is dominated and will vanish from play. Before any math, a quick look at the graph shows whether your counter system is a real loop.

**Count loops, not options.** A five-option system in which each option beats two others and loses to two others has many three-option loops inside it. Each loop has its own balancing feedback, and they overlap. The rule "your share is the prize of what you beat" does not carry over exactly to five options, but its direction does. A bigger prize on an arrow raises demand for whatever beats the arrow's source.

**Hard and soft counters.** In a **hard counter**, the winner almost always wins. In a **soft counter**, the winner has an edge, such as 60% instead of 50%. In payoff terms, a hard counter has large `w` on its arrow and a soft counter has small `w`. Soft counters leave room for skill to overturn the matchup, which players usually prefer. Hard counters make choosing the option the whole contest, which is the right call only when the choice itself is the game (as in rock-paper-scissors).

**Where counters come from.** In a finished game, nobody writes "archers beat infantry, worth 1.4." The counter comes from other rules: range against speed, armor against damage type, area damage against swarms. That makes counters an emergent property in the sense of [week 10](w10-emergence-vs-progression.md). Change one number (movement speed, say) and several arrows in the graph change size at once. The practical habit is to compute the graph from the game, then check it against play data, before and after every patch.

## 4. Asymmetric and non-zero-sum variations

Two quick variations show what the basic model leaves out.

**Ties that are not neutral.** Suppose a tie costs both players something (both attack at once and trade damage). That adds a negative number on the diagonal of the matrix. The stable mix now avoids mirror matches a little, which pushes shares toward whichever options were already rare. The loop still balances, but around a slightly different point. The interactive has a tie-value slider so you can watch this.

**Different option sets.** In many games the two sides do not choose from the same list. A goalkeeper chooses left or right to dive. A kicker chooses left or right to shoot. MMO303 week 10 shows that real penalty takers mix close to the stable mix predicted by exactly this kind of model. The approach is the same. Each side mixes so the other side is indifferent between its options.

These variations are where the course hands off to MMO303. For a first-year designer, the core habit is enough. Write the loop down, attach prizes to the arrows, and find where the balancing feedback will pull the population.

## In-class activity (25 minutes)

**Weighted rock-paper-scissors tournament.** Pairs, then the whole room.

Materials: printed payoff cards with three prize settings (A: 1/1/1, B: `w_R = 3`, others 1, C: `w_R = 1, w_P = 2, w_S = 3`), a tally sheet per pair, and one shared spreadsheet on the projector.

1. Each pair plays 20 rounds of setting A, 20 of B and 20 of C, throwing on a count of three. Record each throw and the score. (12 min)
2. Before playing setting B, each student writes down the share of rock they expect to throw. (1 min)
3. Enter your throws in the shared sheet. The sheet shows the room's share of each option per setting next to the stable mix from the rule. (4 min)
4. Discuss. Did the room overplay rock in setting B at first? Did it drift toward the stable mix over the 20 rounds? In setting C, which option did the room underplay compared with the model? (8 min)

Expected output: per-setting room shares versus the stable mix, and one sentence per pair on what they did differently from the model and why.

## Common misconceptions

- **"If rock's win is worth more, rock should be played more."** Rock's prize sets the share of paper, rock's counter. Rock's own share is set by the prize of scissors.
- **"A balanced counter system settles down."** A balancing loop with a delay oscillates. The stable mix is where the long-run average lands, not where any given week sits.
- **"Equal shares mean a balanced system."** Equal shares follow from equal prizes. A system with unequal prizes can be perfectly healthy with shares of 20/60/20. Whether that is good depends on your design goal, not on the shares being equal.
- **"Counters fix dominance."** Counters remove a dominant option only if every option is beaten by something. One option with no incoming arrow turns the whole loop into a ladder.

## Check yourself

1. A strategy game has cavalry beating archers (win worth 2), archers beating spearmen (worth 1), and spearmen beating cavalry (worth 1). What share of each unit does the stable mix predict?
2. In question 1, the designer raises the archer win to 2. Which unit's share rises the most? Which falls?
3. Your telemetry shows the buffed option's play rate rising in the first three days after a patch. Using the model, give two explanations and say what data would tell them apart.
4. A three-option loop has prizes 2, 2 and 2. A colleague says doubling every prize will change the meta. Are they right?

<details>
<summary>Answers</summary>

1. Name them by the loop. Cavalry beats archers (cavalry prize 2), archers beat spearmen (archer prize 1), spearmen beat cavalry (spearman prize 1). Each share equals the prize of what it beats. Cavalry beats archers, so cavalry's share is set by the archer prize, 1. Archers beat spearmen, so the archer share is set by the spearman prize, 1. Spearmen beat cavalry, so the spearman share is set by the cavalry prize, 2. Shares 1 : 1 : 2, so cavalry 25%, archers 25%, spearmen 50%.
2. Now prizes are cavalry 2, archers 2, spearmen 1. Cavalry's share is set by the archer prize (2), archers by the spearman prize (1), spearmen by the cavalry prize (2). Shares 2 : 1 : 2, so cavalry 40%, archers 20%, spearmen 40%. Cavalry, the counter to archers, rises most (25% to 40%). Spearmen fall (50% to 40%), and archers fall (25% to 20%).
3. Explanation one: the first-week effect. Against the old mix, the buffed option really does win more, so players move to it before the counter rises. Explanation two: the buff also changed something transitive (a stat that helps against everything), so the option is simply stronger. Win rates by matchup tell them apart. In the first case the buffed option's win rate against its counter is unchanged, and its counter's play rate rises over the next weeks. In the second, its win rate rises in every matchup.
4. No. Shares depend on the ratios `w_S : w_R : w_P`. Doubling every prize leaves the ratios and the stable mix the same (a third each). It does raise the stakes of each round, which changes how swingy matches feel.

</details>

## Lab hook

**Lab 11, payoff matrix lab** ([`labs/lab11.md`](../labs/lab11.md)). You build a spreadsheet that computes expected payoffs and the stable mix for any three-option loop, run a 60-round tournament against three scripted bot mixes, and write a patch note that moves a target option to a chosen share. The sheet is reused in your final system design document's balance appendix.

## Sources

- Sirlin, D. (2011). *Yomi* (card game). Rules summary via Wikipedia, "Yomi (card game)" (first edition 2011, accessed September 2026): attacks beat throws, throws beat blocks and dodges and often cause a knockdown, blocks beat attacks and draw a card. Our 3/2/1 prizes are illustrative and are not *Yomi*'s damage values.
- Schreiber, I. (2010). "Level 9: Intransitive Mechanics." *Game Balance Concepts*, online course (gamebalanceconcepts.wordpress.com). The weighted rock-paper-scissors example with a rock win worth 2 and the solution paper 1/2, rock 1/4, scissors 1/4.
- Wikipedia, "Pokémon (video game series)", Gameplay section (accessed September 2026): each game begins with a choice of one of three starter types; double damage from types a Pokémon is weak to and half from types it resists; the Generation 6 trio (Chespin, Fennekin, Froakie) as a Grass, Fire and Water example.
- Pokémon Database, "Pokémon type chart" (pokemondb.net/type, Generation 6 onward chart, accessed September 2026): eighteen types; Fire is super effective against Grass, Water against Fire, Grass against Water, and each reverse matchup is not very effective. The Grass, Fire and Water triangle of the starter trio is also summarized in MMO303 week 9.
- Sinervo, B. & Lively, C. M. (1996). "The rock–paper–scissors game and the evolution of alternative male strategies." *Nature* 380, 240–243. Summary of the three morphs and who beats whom via Wikipedia, "Side-blotched lizard" (accessed September 2026): orange males hold large territories, blue males guard one or two females and fend off yellow "sneakers", yellow males mate on the fringes of orange territories.
- Meadows, D. H. (2008). *Thinking in Systems: A Primer*. Chelsea Green. Chapter 2, balancing loops and the oscillation caused by delays.
- Adams, E. & Dormans, J. (2012). *Game Mechanics: Advanced Game Design*. New Riders. Chapter 3, feedback structures.

## Interactive spec: examples/w11-weighted-rps.html

**The one insight:** raising the prize of one option's win makes that option look best against today's mix and makes its counter the most common choice in the stable mix. Each option's stable share equals the prize of the option it beats.

**Layout.** Two panels plus a season strip. At 900px and wider, the matrix panel sits left and the analysis panel right, with the season strip full width below. At 390px everything stacks in the order matrix, analysis, season.

**Panel 1, "Payoff matrix."** A 3 × 3 table, rows "You play", columns "Opponent plays", options Rock, Paper, Scissors (generic shapes: circle, square, triangle; no hand art). Cells show the row player's payoff with the formulas in the lecture's matrix, plus the tie value `t` on the diagonal. Positive cells tinted with the "good" token, negative with the "bad" token, zero neutral. Under the table, a small loop diagram (three shapes in a triangle, arrows from each to what it beats) with each arrow's thickness proportional to its prize and the prize printed on it.

**Panel 2, "Two views of the same change."**
- Top view, "This week (players still at 1/3 each)": three vertical bars for `E(Rock)`, `E(Paper)`, `E(Scissors)` against `r = p = s = 1/3`, on a shared zero line, values printed on each bar to 3 decimals. With a nonzero tie value, each also includes `t/3`.
- Bottom view, "Stable mix": one horizontal stacked bar with three segments, percentages to 1 decimal printed inside or beside each segment. A ghost outline shows the 1/3 split for comparison, and each segment has a signed change label versus 1/3 (for example "+16.7 pts").

**Panel 3, "Run a season."** A ternary triangle (corners Rock, Paper, Scissors) showing the population's path, and a line chart of the three shares over rounds. Buttons: Run, Pause, Reset. The running average of the path is a separate marker with a dashed trail, and the stable mix is a fixed star.

**Controls.**
- `w_R`, `w_P`, `w_S`: range 0.5 to 5, step 0.5, default 1 each.
- Tie value `t`: range −1 to 0, step 0.1, default 0.
- Presets: "Even (1,1,1)", "Schreiber (2,1,1)", "Block pays least (Yomi-shaped)" which relabels options Attack, Throw, Block with Attack beats Throw prize 3, Throw beats Block prize 2, Block beats Attack prize 1 (mapped to Rock = Attack, Scissors = Throw, Paper = Block, so `w_R = 3`, `w_S = 2`, `w_P = 1`).
- Adjustment speed `η`: range 0.01 to 0.2, step 0.01, default 0.05. Rounds per second: 20 (instant jump to the final state if reduced motion is on).
- All controls keyboard accessible with visible values.

**Formulas.**
- Expected payoffs vs mix `(r, p, s)`: `E_R = t·r − w_P·p + w_R·s`, `E_P = w_P·r + t·p − w_S·s`, `E_S = −w_R·r + w_S·p + t·s`.
- Stable mix with `t = 0`: `(r, p, s) = (w_S, w_R, w_P) / (w_R + w_P + w_S)`.
- Stable mix with `t ≠ 0`: solve `E_R = E_P = E_S` with `r + p + s = 1` as a 3 × 3 linear system (Cramer's rule is fine). If any share comes out negative, show "no fully mixed solution" and clamp the display.
- Season update each round: `Ē = r·E_R + p·E_P + s·E_S`; `x_i ← x_i × (1 + η(E_i − Ē))`; renormalize so the shares sum to 1; start at `(1/3, 1/3, 1/3)` nudged by `+0.001` to rock if all prizes are equal (so the even case shows a tiny orbit instead of a frozen point). Keep a running average of all visited states.

**Test values (builder must reproduce).**
- `(1,1,1)`: stable 33.3/33.3/33.3; this-week bars 0, 0, 0.
- `(1.5,1,1)`: stable 28.6/42.9/28.6; bars +0.167, 0, −0.167.
- `(2,1,1)`: stable 25.0/50.0/25.0; bars +0.333, 0, −0.333.
- `(3,1,1)`: stable 20.0/60.0/20.0; `(4,1,1)`: 16.7/66.7/16.7.
- Yomi-shaped preset (`w_R = 3, w_P = 1, w_S = 2`): stable Rock (Attack) 33.3, Paper (Block) 50.0, Scissors (Throw) 16.7.
- Season, `(2,1,1)`, `η = 0.05`, start at thirds: after round 1 the shares are 33.89/33.33/32.78; after round 10, about 38.3/34.2/27.5; the running average over 400 rounds is about 25.8/48.9/25.4 (within 1.5 points of the stable mix).

**First screen.** Load with the Schreiber preset `(2,1,1)`, so the top view shows rock ahead (+0.333) and the bottom view shows rock shrinking to 25% and paper at 50% with "+16.7 pts". Caption: "Rock's win is worth double. Rock looks best this week. Paper wins the season."

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`, light and dark themes. Options differ by shape as well as color. Signed labels on bars so sign is not shown by color alone. The ternary path has a text alternative (current shares and running average). `prefers-reduced-motion` disables animation and shows the finished path. No game art, card art or logos.
