# GD101 · Week 11 — Balance Intuition: Dominant Strategies and How to Spot Them

**Why this matters:** A dominant strategy is a move that is always best, no matter what anyone else does. Once players find one, every decision in your game collapses into a single obvious answer, and they will find it faster than you think. Spotting dominance before your players do is the first balance skill a designer needs, and it needs no math beyond a table and the word "always".

**You will be able to:**
- Build a payoff table for a small simultaneous-choice game and identify strictly and weakly dominated options by comparing rows.
- Compute the average payoff of each option against a mix of opponent choices, and use it to confirm or rule out a dominant strategy.
- Design a single rule change that removes a dominant strategy, and verify with the table that no new one appears.
- Critique a playtest report for the warning signs of a dominant strategy.

**Before class:** Ian Schreiber, *Game Balance Concepts* (blog course, 2010), Level 1 "Intro to Game Balance", the sections on solvability and on solving intransitive games. Fullerton, *Game Design Workshop* (4th ed.), chapter 10, "Functionality, Completeness, and Balance", the part on dominant strategies. Print or copy the Skirmish rules from section 2 onto six index cards (two sets of Strike, Guard, Bash).

**Prerequisites from earlier courses:** None outside GD101. From this course, [week 9, choice and meaningful decisions](w09-choice-and-meaningful-decisions.md), [week 7, playtesting](w07-playtesting-observe-dont-explain.md), and [week 10, chance vs skill](w10-chance-vs-skill-and-randomness.md). The payoff tables here are the first step of the game theory you'll meet in MMO303 ([payoff matrices and Nash equilibria](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w10-game-theory-payoff-matrices-and-nash-equilibria.md)).

**Interactive:** [Dominant strategy hunt](../examples/w11-dominant-strategy-hunt.html). Keep it open during section 2.

---

## 1. When one answer is always right

Week 9 gave three tests for an interesting decision: the outcome is discernable, it is integrated into the larger game, and the player is uncertain which option is best. A **dominant strategy** breaks the third test. It is an option that is at least as good as every other option in every situation, and strictly better in at least one. If one exists, the player's decision is already made before the game starts.

A few terms, used the same way for the rest of the course:

- **Strategy** here just means a choice or a plan for making choices: "play this card", "always rush", "hold the ball".
- **Strictly dominant:** better than every alternative in every situation.
- **Weakly dominant:** never worse than any alternative, and better in at least one situation.
- **Dominated option:** an option that some other option beats or ties everywhere. Nobody sensible picks it. Designers call it a **dead option**, a dead card or a trap.
- **Degenerate strategy:** a strategy that wins but makes the game boring or pointless to play, even if it isn't technically dominant. Stalling is the classic example.

Dominant strategies and dead options are two views of the same problem. If option X dominates option Y, then Y is dead. If X dominates everything, every other option is dead and the game has one move.

Why does this hurt so much? Because a game's fun lives in its decisions. When one answer is always right:

- Decisions vanish. Players stop thinking and start executing.
- Every game looks the same, because every player does the same thing.
- Your other content is wasted. You designed ten cards; players use one.
- Players who haven't found the answer yet lose to players who have, and they feel cheated when they learn it was never a contest.

The good news is that dominance is often visible on paper before a single playtest. That's what the worked example shows.

## 2. Worked example: a broken card game fixed with one rule change

### The hook

On 22 November 1950, the Fort Wayne Pistons beat the Minneapolis Lakers 19–18 in an NBA game, a score so low it is still cited whenever the shot clock comes up. Nothing was wrong with the players. The Pistons had found a strategy the rules allowed and nothing punished: once you are level or ahead, hold the ball and don't shoot. The Lakers had George Mikan, the league's dominant center, so every Lakers possession was dangerous, and the only safe defense was to keep the ball away from them. Holding the ball was the best choice whatever the Lakers did. For the 1954–55 season the NBA added a single rule, a 24-second shot clock, and the stall disappeared.

That is the whole lesson in one story: a legal strategy that is best in every situation, a game that stops being worth watching, and one rule that fixes it. Let's reproduce it in a game small enough to analyze on one page.

### The broken game: Skirmish, version 1

Two players, 10 health each. Each round, both players secretly choose one of three cards and reveal at the same time. Cards return to your hand after each round, so you can play the same card again.

- **Strike:** deal 2 damage.
- **Guard:** if the opponent Strikes, block it completely and deal 1 damage back. Otherwise, nothing happens.
- **Bash:** deal 4 damage. Guard does not stop Bash; it's too heavy.

The designer's intent reads fine on paper. Strike is the basic attack. Guard punishes a predictable Striker. Bash is the big hit that goes through a Guard. First player to 0 health loses; if both reach 0 in the same round, it's a draw.

### The model: the payoff table

A **payoff table** lists every pair of choices and what one player gets from each. Put your choice on the rows and the opponent's choice on the columns. For the payoff, use **net damage**: damage you deal minus damage you take in that round. Positive is good for you.

Work out each cell from the card rules. Example: you Strike, they Bash. You deal 2 and take 4, so your net is 2 − 4 = −2.

**Skirmish v1, your net damage per round**

| You \ Opponent | Strike | Guard | Bash |
|---|---|---|---|
| **Strike** | 0 | −1 | −2 |
| **Guard** | +1 | 0 | −4 |
| **Bash** | +2 | +4 | 0 |

Every cell comes from the rules in one line:

- Strike vs Strike: both deal 2, net 0. Strike vs Guard: the Strike is blocked and you take 1 back, net −1.
- Guard vs Strike: you block and deal 1, net +1. Guard vs Guard: nothing happens. Guard vs Bash: you take 4, net −4.
- Bash vs Strike: you deal 4 and take 2, net +2. Bash vs Guard: 4 goes through, net +4. Bash vs Bash: both take 4, net 0.

The table is symmetric in a specific way: your payoff in (row X, column Y) is the negative of your payoff in (row Y, column X). That's a quick check that you haven't made an arithmetic slip.

### The test: compare rows

Here is the only rule you need. **Row X dominates row Y if every number in X is at least as big as the number in the same column of Y.** If every number is strictly bigger, the dominance is strict.

Compare Bash with Strike, column by column: +2 > 0, +4 > −1, 0 > −2. Bash is bigger in every column. Compare Bash with Guard: +2 > +1, +4 > 0, 0 > −4. Bigger everywhere again. **Bash strictly dominates both other cards.**

Say it in words, because this is what your players will feel. Whatever your opponent does, you are better off having played Bash. You don't need to guess or read your opponent. Bash every round.

### Numbers you can check: average against a mix

The row test is the proof. A second view is often more persuasive to a team that loves the design. Suppose your opponent mixes their choices, playing Strike, Guard and Bash in some proportions. Your average net damage for each card is the payoff row weighted by those proportions.

For example, against an opponent who plays each card a third of the time, Strike averages (0 − 1 − 2) / 3 = −1.

| Opponent's mix (Strike : Guard : Bash) | Your average with Strike | with Guard | with Bash |
|---|---|---|---|
| 1 : 1 : 1 | −1.00 | −1.00 | +2.00 |
| 1 : 1 : 0 | −0.50 | +0.50 | +3.00 |
| 0 : 1 : 1 | −1.50 | −2.00 | +2.00 |
| 1 : 0 : 1 | −1.00 | −1.50 | +1.00 |
| 4 : 2 : 1 | −0.57 | 0.00 | +2.29 |

Bash wins every row of this table. It has to: a card that is best in every column is best in every weighted average of columns. Now play it out. Both players Bash every round, both take 4 per round, and after three rounds both are at −2 health. **Every game of optimally played Skirmish v1 is a three-round draw.** Guard and Strike are dead cards, and the game has no decisions left.

### A visual you can move

Open [`examples/w11-dominant-strategy-hunt.html`](../examples/w11-dominant-strategy-hunt.html). The main view is a triangle. Every point inside it is one opponent mix: the corners are "always Strike", "always Guard" and "always Bash", and the middle is a third each. Each point is colored by the card that gives you the best average against that mix. For version 1 the whole triangle is one color, Bash, and no drag of the mix point changes it. That single-colored triangle is what a dominant strategy looks like. The side panel shows the payoff table and three bars for the three averages at the current point, so you can read the numbers in the table above straight off the screen.

Now flip the toggle to version 2.

### The fix: one rule change

We want Bash to stay exciting, a big hit that beats Guard, but it must lose to something. The natural candidate is Strike: a quick jab should be able to catch someone winding up a heavy swing. So we add one rule and change nothing else.

- **New rule for Bash:** Bash is slow. If your opponent Strikes in the same round, their Strike lands first and interrupts your Bash, which deals no damage.

Only two cells change: Bash vs Strike and its mirror, Strike vs Bash.

**Skirmish v2, your net damage per round**

| You \ Opponent | Strike | Guard | Bash |
|---|---|---|---|
| **Strike** | 0 | −1 | **+2** |
| **Guard** | +1 | 0 | −4 |
| **Bash** | **−2** | +4 | 0 |

Run the row test again. Bash vs Strike: −2 < 0 in the first column, but +4 > −1 in the second. Neither dominates. Bash vs Guard: −2 < +1, +4 > 0. Neither. Strike vs Guard: 0 < +1, −1 < 0, +2 > −4. Neither. **No row dominates any other.** Every card beats one card and loses to another:

- Strike beats Bash (interrupt).
- Bash beats Guard (goes through).
- Guard beats Strike (block and counter).

That's a rock-paper-scissors loop, and it's the shape of the Pistons fix too. The shot clock gave the defense something that beats "hold the ball": wait, and the ball goes to them.

Now redo the averages with version 2.

| Opponent's mix (Strike : Guard : Bash) | Your average with Strike | with Guard | with Bash |
|---|---|---|---|
| 1 : 1 : 1 | +0.33 | −1.00 | +0.67 |
| 1 : 1 : 0 | −0.50 | +0.50 | +1.00 |
| 0 : 1 : 1 | +0.50 | −2.00 | +2.00 |
| 1 : 0 : 1 | +1.00 | −1.50 | −1.00 |
| 1 : 0 : 0 | 0.00 | +1.00 | −2.00 |
| 4 : 2 : 1 | 0.00 | 0.00 | 0.00 |

The best card now changes with the opponent's mix. Against a Strike-heavy player, Guard. Against a Guard-heavy player, Bash. Against someone who Bashes a lot, Strike. Back in the interactive, the version 2 triangle splits into three colored regions, and dragging the mix point across a border changes the best card. The three regions meet at one point, the 4 : 2 : 1 mix in the last row, where all three cards average exactly zero.

That meeting point is worth one sentence now and a full lecture later. If your opponent plays Strike 4/7 of the time, Guard 2/7 and Bash 1/7, nothing you do can gain on them on average, and the same holds the other way. Game theorists call it a mixed-strategy equilibrium. You can check it without any theory: plug 4 : 2 : 1 into each row and you get 0 every time (Strike: 0×4 − 1×2 + 2×1 = 0; Guard: 1×4 + 0 − 4×1 = 0; Bash: −2×4 + 4×2 + 0 = 0). [MMO303 week 10](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w10-game-theory-payoff-matrices-and-nash-equilibria.md) shows how to find it. For a designer, the useful reading is that the fixed game wants players to Strike most, Guard sometimes and Bash rarely, and you can tune those shares by changing the numbers.

### Cross-game recognition

**Basketball, 1954.** The table for a leading team without a shot clock has one dominant row: hold the ball. The shot clock rewrote one cell. Holding too long now hands the ball to the other team, so the stall has a counter. Same fix as Skirmish: don't delete the strong option, give it a loss.

**Football (soccer), 1992.** The 1990 World Cup was widely criticized for dull play, with teams passing back to their own goalkeeper, who could pick up the ball and hold it to waste time. For a team protecting a lead, the back-pass was the safe choice in every situation. FIFA adopted the back-pass rule in 1992, first used at that year's Olympic tournament: a goalkeeper can no longer handle a deliberate pass from a teammate's foot. One rule, and the stall option lost its safety. It is now widely considered one of the most successful rule changes in the modern game.

**Hex and the pie rule.** In the board game Hex, moving first is a real advantage, so "be the first player" dominates "be the second". Hex fixes it with the **pie rule**, named after "one cuts, the other chooses": after the first move, the second player may swap sides and take that move as their own. Now the first player's best move is a deliberately balanced one, because a strong opening will simply be stolen. One rule turned a dominant advantage into a decision.

**Magic: The Gathering cards.** Dominance happens at the level of single options too. Lightning Bolt costs one red mana and deals 3 damage to any target. Shock costs one red mana and deals 2 damage to any target. Same cost, same targets, one more damage: in a deck that could play either, Bolt dominates Shock, and Magic players have a name for this relation, "strictly better". Designers of any game with many cards, items or units face this constantly. Every new option has to be compared against every existing option at the same cost, or it will be dead on arrival or kill something already there.

Four contexts, one test. Write the options as rows, write the situations as columns, and look for a row that is never lower.

### Eyes-open design judgment

- **Prefer changing an interaction to changing a number.** You could "fix" Skirmish v1 by lowering Bash to 1 damage. Check the table: Bash becomes weak against everything, and you have traded a dominant card for a dead one. The rule change kept Bash strong and gave it a specific weakness. Number changes move a card up or down a single ladder; interaction changes create new ladders.
- **Recheck the whole table after every fix.** A fix can create a new dominant option. If the v2 rule had made Strike beat Bash *and* Guard, Strike would dominate instead. The table is cheap, so rebuild it every time.
- **Every rule costs attention.** "Bash is interrupted by Strike" is one more thing a new player must learn and remember. A fix that needs a paragraph of exceptions may cost more fun than the dominance it removes.
- **Some dominance is acceptable.** A tutorial may have one correct answer on purpose. A single-player game can have a best weapon if finding it is part of the fun. Dominance is a problem when it removes decisions players came for, especially against other players.
- **Loops need maintenance.** A counter loop only works while the payoffs stay in proportion. Make Bash deal 8 and the 4 : 2 : 1 balance point moves; make Strike's interrupt unreliable and Bash may dominate again.

### Check yourself (worked example)

1. In Skirmish v2, change Guard's counter from 1 damage to 3 damage. Rebuild the Guard row and the Strike row. Is any card now dominated?
2. A teammate suggests fixing v1 by letting Guard stop Bash instead. Write the new table and run the row test. What happens?
3. In v2, your opponent plays only Strike and Guard, half each. Which card should you play, and what is your average net damage?

<details>
<summary>Answers</summary>

1. Guard row becomes Strike +3, Guard 0, Bash −4. Strike row becomes Strike 0, Guard −3, Bash +2. Compare every pair: Strike vs Guard (0 < 3, −3 < 0, 2 > −4), Strike vs Bash (0 > −2, −3 < 4), Guard vs Bash (3 > −2, 0 < 4). No row dominates another, so the loop survives. Redo the balance-point check and the equal-average mix becomes 4 : 2 : 3. Guard's share falls from 2/7 to 2/9 and Bash's rises from 1/7 to 3/9, because a harder-hitting Guard invites more Bashes to punish it. Buffing a card in a loop can make its counter more common.
2. If Guard blocks Bash completely (and deals no counter to it), the cells become Guard vs Bash 0, Bash vs Guard 0. Rows: Strike (0, −1, −2), Guard (+1, 0, 0), Bash (+2, 0, 0). Bash vs Guard: +2 > +1, 0 = 0, 0 = 0, so Bash weakly dominates Guard. Bash vs Strike: +2 > 0, 0 > −1, 0 > −2, so Bash strictly dominates Strike. Bash still dominates, weakly. The fix failed.
3. From the table's "1 : 1 : 0" row: Strike −0.50, Guard +0.50, Bash +1.00. Play Bash, averaging +1 per round.

</details>

## 3. Spotting dominance without a table

Skirmish is small enough to tabulate. Your prototype probably isn't. You'll need other signals, and the best ones come from playtests (week 7).

**Convergence.** After a few games, do all players do the same thing? If three of four testers settle on the same opening, the same card or the same route, suspect dominance. Variety that disappears as players learn is the strongest warning sign you will get.

**The option nobody picks.** Record every choice in your playtest notes, not only the outcomes. An option chosen 0 times in 20 games is either dominated, unclear, or badly explained. Ask the players which. (Week 12 is about the "unclear" case.)

**Fast solving.** If a new player asks "why would anyone ever do X?" in the first game, they may be right. Write the question down word for word.

**The extreme test.** Deliberately play the most one-sided strategy you can: all attack, all defense, only the cheapest card, never move. Designers tend to test the game they meant to make. Players test the game the rules allow. If an extreme strategy wins, you've found either a dominant strategy or a degenerate one.

**The stall test.** Ask what happens if a winning player simply stops engaging. The Pistons and the back-pass both answer the same question: can a leader freeze the game? If yes, you need a clock, a pressure rule or a reason to act.

**Cost outliers.** For games with many items or cards, put every option in a spreadsheet with its cost and its effect. An option that gives more of everything than another at the same or lower cost is dominant over it, the Bolt-and-Shock case. MMO303 turns this into a full method for classes and gear ([what "balanced" means](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w01-what-balanced-means.md)).

## 4. Dead options cascade

Dominance has a sneaky second-order effect. Once one option is dead, the others need to be rechecked, because some options were only good *against* the dead one.

Suppose a game has a card that is only good at punishing Sell, and Sell turns out to be dominated by another card. Nobody plays Sell anymore, so the punisher has no targets, and now it may be dominated too. Remove it, recheck, and something else may fall. Game theorists call this **iterated elimination of dominated strategies**. You just need the habit: after crossing out a dead row, cross out its column too (nobody will play it against you), and compare the remaining rows again.

This is why a small balance mistake can empty a whole game. Lab 11 gives you a four-card game where exactly this happens: one card looks only slightly too good, and following the cascade leaves a single card standing.

## 5. Dominant or just strong?

Not every strong option is dominant, and nerfing strong options by reflex makes games bland. Two questions separate them.

1. **Does anything beat it?** If some situation or counter-choice makes it the wrong pick, it's strong, not dominant. In Skirmish v2, Bash is the best card against a Guard-heavy opponent, but it is terrible against a Striker. That's a strong card with a job.
2. **Does its strength depend on what others do?** A dominant option is best no matter what. A strong option is best in some range of opponent behavior. On the interactive's triangle, a strong card owns a big region; a dominant card owns the whole triangle.

When a strong option is popular, the first fix to try is often to make its counter more attractive, not to weaken it. MMO303's lecture on [intransitivity and counters](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w09-intransitivity-and-counters.md) shows a surprising version of this: in a counter loop, buffing one option can make its counter more common.

## In-class activity (25 minutes)

In groups of three: two players and one recorder. You need the six Skirmish cards from the pre-class prep and scrap paper for health.

1. **Play v1 (6 minutes).** Play three games of Skirmish v1 as written. The recorder notes every card choice. Don't tell the players the analysis from this lecture if they haven't read it; see how many rounds it takes before both Bash every round.
2. **Play v2 (6 minutes).** Play three games of v2. Record choices again.
3. **Compare (5 minutes).** Count card shares for each version. Did v1 converge on Bash? Did v2 stay mixed? How close did the v2 shares get to 4 : 2 : 1 (57% Strike, 29% Guard, 14% Bash)?
4. **Break it again (8 minutes).** Invent a fourth card for v2. Write its row and column into the table, and run the row test. Your goal is a card that is neither dominant nor dead. Swap with another group and let them try to find a flaw in yours.

Expected output: a choice tally for each version, the extended payoff table, and one sentence on whether your fourth card survived the other group's attack.

## Common misconceptions

- **"A dominant strategy means the game is too hard."** It usually means the opposite: the game becomes trivial once you know the answer. Difficulty comes from decisions, and dominance removes them.
- **"If it's dominant, nerf its numbers."** Lowering numbers often turns a dominant option into a dead one. Changing how it interacts with other options, as the Bash interrupt did, keeps it interesting.
- **"The most popular option must be dominant."** Popularity can come from being strong, easy or fun. Dominance is a claim about every situation, so check it with the table or the extreme test, not the pick rate alone.
- **"Randomness fixes dominance."** Week 10 showed that luck pulls results toward 50%. A dominant strategy under heavy randomness still wins more, just more slowly, and players still find it.

## Check yourself

1. Here is a payoff table for a new game (your net points per round). Which options, if any, are dominated? By what, strictly or weakly?

   | You \ Opponent | Charge | Hold | Retreat |
   |---|---|---|---|
   | Charge | 0 | +2 | +1 |
   | Hold | −2 | 0 | +1 |
   | Retreat | −1 | −1 | 0 |

2. In the table above, after removing any dominated rows and the matching columns, what does optimal play look like? Suggest one rule change that could give the weakest option a job.
3. A playtest report says: "Players liked the game. All four testers used the Fortress opening by game three. Nobody used the Scout card." List two warning signs in this report and one test you would run next.
4. In Skirmish v2, what is your average net damage with each card if your opponent plays Strike 2/7, Guard 4/7 and Bash 1/7? Which card should you play?

<details>
<summary>Answers</summary>

1. Charge vs Hold: 0 > −2, +2 > 0, +1 = +1, so Charge weakly dominates Hold. Charge vs Retreat: 0 > −1, +2 > −1, +1 > 0, so Charge strictly dominates Retreat. Hold vs Retreat: −2 < −1, so Hold does not dominate Retreat.
2. Charge dominates both other options, so both players Charge every round and every round nets 0. One fix: give Retreat a counter to Charge, for example "Retreat vs Charge: the charger overextends and you score 2", which changes Retreat vs Charge to +2 and Charge vs Retreat to −2. Recheck: Charge (0, +2, −2), Hold (−2, 0, +1), Retreat (+2, −1, 0). No row dominates another.
3. Warning signs: convergence on one opening (Fortress) within three games, and an option picked zero times (Scout). Next test: an extreme test with Fortress against every other opening, or a forced-Scout game to see whether Scout is dominated or just unclear.
4. Strike: (0×2 − 1×4 + 2×1) / 7 = −2/7 ≈ −0.29. Guard: (1×2 + 0 − 4×1) / 7 = −2/7 ≈ −0.29. Bash: (−2×2 + 4×4 + 0) / 7 = 12/7 ≈ +1.71. Play Bash, which is exactly what a Guard-heavy opponent invites.

</details>

## Lab hook

**Lab 11: Dominant strategy hunt.** You get the rules of Market Stall, a four-card trading game with a hidden dominance cascade. You build its payoff table, trace which cards die and in what order, confirm it with a short playtest, and fix the game with one rule change that you verify on paper and at the table. See [labs/lab11.md](../labs/lab11.md).

## Sources

- Wikipedia, "Shot clock": Fort Wayne Pistons 19, Minneapolis Lakers 18, 22 November 1950, the Pistons holding the ball to limit George Mikan; the NBA adopted the 24-second shot clock for the 1954–55 season.
- Wikipedia, "Back-pass rule": criticism of the 1990 World Cup for back-passing and time-wasting; FIFA adopted the rule in 1992 after testing, first applied at the 1992 Summer Olympics; described as one of the most successful changes in the modern game.
- Wikipedia, "Pie rule": the swap rule used in Hex to balance a first-move advantage; named after divide-and-choose.
- Scryfall card database (Oracle text, accessed September 2026): Lightning Bolt, {R}, deals 3 damage to any target; Shock, {R}, deals 2 damage to any target.
- Schreiber, I. (2010). *Game Balance Concepts*, Level 1 "Intro to Game Balance" (gamebalanceconcepts.wordpress.com): solvability and solving intransitive games.
- Fullerton, T. (2018). *Game Design Workshop* (4th ed.). CRC Press. Chapter 10, "Functionality, Completeness, and Balance": assigned reading on balance and dominant strategies.
- Skirmish and Market Stall are original games written for this course. All payoff values are computed from their rules.

## Interactive spec: examples/w11-dominant-strategy-hunt.html

**Purpose.** Show what a dominant strategy looks like across every possible opponent, and how one rule change breaks it into a loop.

**The one insight the visual must make obvious.** In version 1 the best card is the same everywhere in the triangle (one color). In version 2 the triangle splits into three regions that meet at the 4 : 2 : 1 point, so the best card depends on what the opponent does.

**Layout.** Main view left (desktop) or top (390px): an equilateral triangle (a ternary plot of opponent mixes). Side panel: the payoff table and a bar readout.

- Triangle corners labeled "Always Strike" (bottom left), "Always Guard" (bottom right), "Always Bash" (top). A point with barycentric weights (s, g, b), `s + g + b = 1`, is at `s × S_corner + g × G_corner + b × B_corner`.
- Fill every pixel (or a fine grid, at least 120 steps per side) with the color of the card with the highest average payoff at that mix. Use three palette colors plus a pattern or label per region so color is not the only cue. Where two or three cards tie within 1e-9, draw the border line.
- A draggable mix point (default at 1/3, 1/3, 1/3) with a label showing `s : g : b` as percentages.
- Side panel: the 3×3 payoff table for the current version, with changed cells highlighted when version 2 is on. Under it, three horizontal bars for the averages of Strike, Guard and Bash at the current mix, with values to two decimals and the best one marked "best".
- A line of text under the triangle: version 1 shows "Bash is best at every mix: dominant". Version 2 shows "Best card depends on the mix" and the current best card.

**Controls** (keyboard accessible):

- Version toggle: "v1 as written" / "v2 with interrupt rule". Default v1.
- Mix point: drag with pointer, or three linked number inputs (percent, step 1) that renormalize the other two when one changes; arrow keys move the point by 1% along the focused axis.
- Preset buttons: "1 : 1 : 1", "4 : 2 : 1", "Strike-heavy (6 : 3 : 1)", "Guard-heavy (2 : 4 : 1)".
- Advanced (collapsed by default): number inputs for Strike damage (default 2), Guard counter (default 1), Bash damage (default 4), and a checkbox "Strike interrupts Bash". Changing these rebuilds the table and triangle live, so students can answer Check yourself question 1 on screen. Print "Dominated: X by Y (strict/weak)" for every dominated pair found by the row test.
- Reset button.

**Formulas.**

Let `k` = Strike damage, `c` = Guard counter, `h` = Bash damage, `I` = 1 if the interrupt rule is on, else 0. Row player's net damage:

- Strike vs Strike 0; Strike vs Guard `−c`; Strike vs Bash `I ? +k : k − h`.
- Guard vs Strike `+c`; Guard vs Guard 0; Guard vs Bash `−h`.
- Bash vs Strike `I ? −k : h − k`; Bash vs Guard `+h`; Bash vs Bash 0.
- Average for a card = `row · (s, g, b)`.
- Row test: X dominates Y if `X[j] ≥ Y[j]` for all j (weak) and `X[j] > Y[j]` for all j (strict).

**Test values** (defaults k = 2, c = 1, h = 4).

| Version | Mix s : g : b | Strike | Guard | Bash | Best |
|---|---|---|---|---|---|
| v1 | 1/3 each | −1.00 | −1.00 | +2.00 | Bash |
| v1 | 4 : 2 : 1 | −0.57 | 0.00 | +2.29 | Bash |
| v2 | 1/3 each | +0.33 | −1.00 | +0.67 | Bash |
| v2 | 4 : 2 : 1 | 0.00 | 0.00 | 0.00 | tie (all three) |
| v2 | 1 : 0 : 0 | 0.00 | +1.00 | −2.00 | Guard |
| v2 | 1 : 0 : 1 | +1.00 | −1.50 | −1.00 | Strike |
| v2 | 2 : 4 : 1 | −0.29 | −0.29 | +1.71 | Bash |

v1 dominance readout: "Bash strictly dominates Strike", "Bash strictly dominates Guard". v2 readout: "No dominated cards". With the interrupt off and Guard counter 3, v1 readout still shows Bash strictly dominating Strike (Bash row 2, 4, 0 vs Strike 0, −3, −2) and Guard row (3, 0, −4) not dominated by Bash, since 2 < 3.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`, light and dark themes, reduced motion respected. Cards are drawn as plain labeled rectangles with text; no fantasy art.
