# GD101 · Week 06 — Paper Prototyping I: Cards, Dice, Boards

**Why this matters:** Weeks 4 and 5 showed that you can't see a dynamic by reading your rules. You have to play them. A paper prototype lets you play a rule an hour after you think of it, change it with a pencil, and play again. Every component you pick for it (a die, a deck, a board) is itself a design decision that shapes what players feel.

**You will be able to:**
- Choose the cheapest prototype that answers a stated design question, and name what it can't test.
- Map each common component (dice, cards, boards, tokens, tracks) to the formal element it models and the dynamics it tends to produce.
- Compute the chance of a dry spell under dice and under a deck with the same odds, by multiplying fractions.
- Decide between dice and a deck for a given experience goal, and justify it with numbers from the week's simulation.

**Before class:** Fullerton, *Game Design Workshop* (4th ed.), chapter 7 on prototyping (the sections on physical prototypes). Bring blank index cards, two six-sided dice, a pencil and scissors.

**Prerequisites from earlier courses:** GD101 [week 2](w02-players-objectives-procedures-rules.md) and [week 3](w03-resources-conflict-boundaries-outcome.md) (formal elements), [week 4 (MDA)](w04-mda-mechanics-dynamics-aesthetics.md) and [week 5 (experience goals)](w05-player-experience-goals-and-the-8-kinds-of-fun.md). No probability course is assumed. The one idea you need, multiplying chances for events in a row, is explained here. MA102 later covers it in full: see [MA102 week 2](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w02-independent-events-and-the-gamblers-fallacy.md) on independent draws and bags, and [MA102 week 8](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w08-dice-sums-and-the-normal-curve.md) on why two dice favor 7.

**Interactive:** [Dice vs deck](../examples/w06-dice-vs-deck.html). Use it during section 3.

---

## 1. Why paper first

A **prototype** is a playable model of a game built to answer a question. It is not a first draft of the finished game. The question comes first. "Is trading fun?" "Do players understand the turn order?" "Does the leader run away with it?" The prototype is the cheapest thing that can answer that question.

Paper is cheap in the way that matters most, **cost of change**. If a card is too strong, you cross out the 5 and write a 3. If the board is too big, you fold it. A rule change takes seconds and the next game can start at once. Iterating on the same idea in code means a build, a bug or two, and a test cycle. Designers use paper because it lets them run many more design loops in an afternoon, and week 8 is about how much more you learn from ten fast loops than from one slow one.

### What paper can test

Paper is good at anything that lives in the rules and the numbers.

- **Loops and economies.** Week 4's Mini-opoly is a paper game. You can see the runaway leader at the table.
- **Decisions.** Whether players have real choices each turn, and whether one choice always wins.
- **Pacing in turns.** How many turns a game lasts, when it gets decided, when players get bored.
- **Information.** What players know, what's hidden, what they can work out.
- **Social dynamics.** Trading, alliances, bluffing, ganging up on the leader.

### What paper can't test

Be honest about the limits, or you'll trust a prototype for the wrong question.

- **Timing and dexterity.** A jump that must be pressed within a tenth of a second. You can model the *decision* of when to jump, but not how the input feels.
- **Real-time pressure.** You can add a sand timer, which is a start. But a turn-based paper version of a real-time game changes the aesthetic from sensation and challenge toward strategy.
- **Presentation.** Sound, animation, screen shake. Week 12 covers that kind of feedback, and it needs a screen.
- **Scale.** A thousand players in a shared world. You can model the rules of one market stall, not the crowd.

### Digital games on paper

Most games you'll work on in this program are digital, and you can still prototype their systems on paper. The trick is to make one person the **computer**. They hold the hidden information (enemy stats, loot tables, the map), apply the rules exactly as written and say nothing else. The players make decisions; the computer resolves them. This works for turn-based combat, crafting systems, loot drops, quest structures and the core loop of many MMO systems you will meet later. An hour with a paper version of a crafting economy will tell you whether players hoard, trade or ignore it, long before anyone writes a line of code.

## 2. The component kit

Every physical component is a way of representing a formal element from weeks 2 and 3. Each also comes with habits, meaning dynamics it tends to create unless you design against them.

| Component | Formal element it represents | What it does well | Dynamics it tends to create |
|---|---|---|---|
| Dice | Procedures with chance; outcome uncertainty | Fast, public, any odds you can build from faces | Streaks and droughts; players blame luck; everyone watches the roll |
| Cards (a deck) | Resources, procedures, hidden information | Chance with memory; variable content per card; hidden hands; a built-in clock (the deck runs out) | Counting what's left; holding cards back; bluffing |
| Board | Boundaries and space | Position, adjacency, distance, public state everyone can see | Blocking, racing, territorial conflict |
| Tokens and counters | Resources (stocks) | Visible quantities; easy to add and remove | Hoarding; comparing piles; spotting the leader at a glance |
| Tracks | Progress and resources | A number everyone can see, with thresholds marked | Racing; targeting the leader on the track |
| Tables and charts | Rules as lookup | Complex outcomes without memory load | Slow play; people skip checking the table |

Two points about this table.

**Components are rules.** Choosing "draw a card" instead of "roll a die" changes what can happen, not just how it looks. The next section shows how much.

**Visibility is a rule too.** Money in a face-up pile tells everyone who's winning. Money held in a hand hides it. Week 4's Monopoly loop depends partly on everyone seeing the gap. If you want to soften a runaway leader without changing any numbers, try hiding the scores. The underlying numbers stay the same, but players can no longer see the gap and react to it.

## 3. Worked example: dice or a deck?

### The hook

In Catan, every turn begins with a roll of two dice. Each land hex has a number token from 2 to 12, and every hex showing the rolled number produces resources for the settlements around it. The tokens carry dots, or pips, under the number, and the 2020 rulebook explains them: 6 and 8 are printed in red and carry 5 dots each, because there are 5 ways to roll each of them on two dice.

So a careful player puts their first settlements on 6 and 8. Then, sometimes, the dice don't cooperate. Eight or ten turns go by without a single 6 or 8, while someone who settled on 4 and 10 collects cards every other turn. Every Catan table has seen it. The strategy was right; the dice punished it anyway.

Catan's makers offer an alternative. The Traders & Barbarians expansion (rulebook as of 2025) includes a Catan Event Cards variant. It replaces the dice with a deck of 36 production cards, the same number as the equally likely outcomes of two dice. The rules have you shuffle the 36, deal 5 face down, put a New Year card on top of those 5, and stack the remaining 31 above it. When the New Year card comes up, you rebuild the deck. The rulebook describes the purpose plainly: a more consistent spread of production for players who want to avoid extreme dice results.

Here is the question for a paper prototyper. The deck has the same odds as the dice. What does it change, and how much?

### The model

Both randomizers pick from the same 36 equally likely outcomes. For two dice, those are the 36 ordered pairs, and each sum appears as many times as there are ways to roll it: one way to roll 2, five ways to roll 8, six ways to roll 7. For our model deck we give each sum exactly that many cards, so the deck holds five 8s, five 6s, six 7s and so on. (The rulebook gives the card count, 36, but we set the per-sum counts ourselves, to match two dice.)

The only difference is what happens after a draw.

- **Dice** put the outcome back. Every roll is fresh, and the chance of an 8 is 5/36 on every turn, no matter what came before. This is drawing **with replacement**.
- **A deck** keeps the drawn card out until the reshuffle. If no 8 has come up for a while, the remaining cards are richer in 8s, so the next draw is more likely to be one. This is drawing **without replacement**.

To find the chance of a dry spell, multiply the chance of missing on each turn in a row.

```
Dice, no 8 in n turns:   (31/36) × (31/36) × ... n times = (31/36)^n
Deck, no 8 in n draws:   (31/36) × (30/35) × (29/34) × ... n fractions
```

For the deck, each miss removes one non-8 card from the top and bottom of the fraction. There are still five 8s in a shrinking deck, so each next miss is a little less likely.

### Numbers you can check

Work the first two rows by hand.

For 10 turns with dice, `(31/36)^10 = 0.861^10 = 0.224`. For the deck, `(31/36)(30/35)(29/34)(28/33)(27/32)(26/31)(25/30)(24/29)(23/28)(22/27) = 0.174`.

| Question | Dice | Deck (31 draws per shuffle) |
|---|---|---|
| Chance of no 8 in the first 10 turns | 22.4% | 17.4% |
| Chance of no 6 or 8 in the first 5 turns | 19.6% | 17.4% |
| Average number of 8s in 31 turns | 4.31 | 4.31 |
| Typical spread (standard deviation) of that count | 1.93 | 0.73 |
| Chance of at most two 8s in 31 turns | 17.6% | 1.3% |

The "typical spread" is the **standard deviation**, a number for how far results usually land from the average. You don't need its formula this week. Read it as "most results fall within about this distance of the average." MA102 week 5 defines it properly.

Look at the first rows, then the last. On any short stretch the deck is only a little kinder: 17% instead of 22% for a ten-turn drought of 8s. Over a whole shuffle it's a different game. With dice, about one 31-turn stretch in six gives a player on 8 two 8s or fewer. With the deck it happens about once in eighty.

The spread matters most over a whole game. We simulated 2,000 games of 60 turns each, tracking a player whose settlements sit on 6 and 8 (10 winning outcomes out of 36).

| 60-turn game, player on 6 and 8 | Dice | Deck |
|---|---|---|
| Average turns that produce | 16.6 | 16.7 |
| Standard deviation | 3.43 | 1.46 |
| Middle 90% of games | 11 to 22 | 14 to 19 |
| Worst and best game out of 2,000 | 5 and 31 | 11 and 20 |
| Longest dry spell, average game | 10.0 turns | 9.3 turns |
| Longest dry spell, 1 game in 20 | 17 turns | 14 turns |

Same average, less than half the spread. With dice, the unluckiest 5% of games give a 6-and-8 player 11 or fewer production turns, and the worst gives 5. A player on 4 and 10 (6 outcomes out of 36) collects 10 in an average 60-turn game. So with dice, the best spot does little better than a poor one in about one game in twenty. With the deck, the 6-and-8 player never dropped below 11 in 2,000 games.

### A visual you can move

Open [`examples/w06-dice-vs-deck.html`](../examples/w06-dice-vs-deck.html). It has two linked views.

- **Top, one draw.** Bar charts of how often each number from 2 to 12 comes up, for dice and for the deck. They are identical. Nothing here tells you the two randomizers differ.
- **Bottom, a whole game.** For each of many simulated games, the number of turns your chosen numbers produced, drawn as two histograms. The dice histogram is wide and flat-topped. The deck histogram is a narrow spike.

Pick different target numbers. Change the game length. Slide "cards left under the New Year card" from 0 to 10: at 0 the deck runs to the last card and becomes more predictable; at 10 more randomness creeps back. Press "play one game" to watch a single sequence of draws, with droughts marked.

The top chart is what the rules sheet says. The bottom chart is what players live through.

### Cross-game recognition

Rewrite each case as "same odds per draw; what happens to the draws already made?"

**Tetris Guideline games: the 7-bag.** Modern Tetris games that follow the Tetris Guideline deal pieces from a shuffled bag of all seven shapes, then refill the bag. Each shape is a card in a seven-card deck. That caps how long you can wait for the long straight piece. MA102 week 2 works through the numbers; see [MA102 week 2](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w02-independent-events-and-the-gamblers-fallacy.md).

**Deck-building card games.** In Dominion (2008) and its descendants, you shuffle your own deck and draw through it, and you only reshuffle when it runs out. Each card you own comes up once per pass through the deck. A strong card you bought is guaranteed to appear, just not when. The genre's strategy depends on this memory. Week 13 looks at deck-building as a cluster of mechanics; see [GD101 week 13](w13-genres-as-clusters-of-mechanics.md).

**Dota 2 and pseudo-random chance.** Digital games can't use a physical deck, but they can copy its effect. Dota 2's pseudo-random distribution raises the chance of a proc after every miss and resets it after a hit. That shrinks droughts the way the deck does, at the same long-run rate. See [MA102 week 10](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w10-pseudo-random-distribution-and-pity-timers.md).

Three contexts, one principle: **keeping memory of past draws reduces spread without changing the average.** When you choose between a die and a deck in a paper prototype, you are choosing how much memory your randomness has.

### Eyes-open design judgment

The deck is not simply better. Each choice buys something and costs something.

- **Spread is a design dial.** Week 10 covers how luck lets weaker players win sometimes. Lower spread means the better settlement spot wins more reliably. That rewards skill and punishes the new player who placed badly. In week 4's terms, dice luck is a crude catch-up tool, because it hands trailing players occasional windfalls. A deck takes some of that away. If your experience goal says "every player believes they can win," the deck may work against it.
- **Memory invites counting.** With a deck, a player who tracks what's been drawn knows what's left. Late in a shuffle that's real information. Catan's variant blunts this with the 5 cards under the New Year card: you never know which 5 outcomes will be skipped this cycle. Counting then becomes a skill some players enjoy and others resent. Decide whether you want it.
- **The roll is a moment.** Dice are loud, physical and public. Everyone leans in. A card flip is quieter. In MDA terms, the dice carry some sensation and some shared drama that the deck gives up.
- **Handling cost is real on paper.** 36 cards need shuffling and a table space; two dice fit in a pocket. In code the cost is zero. But the paper prototype is where you find out whether players like the feel of each, so test both.
- **You can mix them.** A deck for the big recurring event and a die for small combat rolls is a normal solution. So is a die whose result is modified by a card. Pick per decision, not per game.

### Check yourself (worked example)

1. A player's only settlement is on a 5 (4 outcomes of 36). What is the chance of no 5 in the first 6 turns with dice? With a fresh 36-card deck?
2. Using the table, a player on 6 and 8 has a 1-in-20 chance of a dry spell of 17 or more turns in a 60-turn game with dice. In a 4-player game, roughly what is the chance that some player on 6 and 8 has a spell like that? Why is the real answer lower if all four are on 6 and 8?
3. Your experience goal is "in a 30-minute family game, a child who placed badly still has a real chance to win." Dice or deck? Name the number from this section that supports your choice.

<details>
<summary>Answers</summary>

1. Dice: `(32/36)^6 = 0.889^6 = 0.494`, about 49%. Deck: `(32/36)(31/35)(30/34)(29/33)(28/32)(27/31) = 0.465`, about 47%. For a short stretch the difference is small.
2. Treating the players as independent: `1 − 0.95^4 = 0.185`, about 19%. If all four are on 6 and 8, their droughts happen at the same time, because the same roll serves everyone. The four chances are then not independent, and the chance that at least one has a drought is closer to a single player's 5%.
3. Dice. The wider spread (middle 90% of games from 11 to 22 production turns, against 14 to 19 for the deck) means a badly placed player sometimes out-produces a well placed one. That's the luck that keeps the child in the game.

</details>

## 4. Building your first paper prototype

Here is a process that works for first prototypes. You'll repeat it in lab 06.

1. **Write the question.** One sentence at the top of the page. "Does the leader run away with it?" or "Is the choice between saving and spending interesting?" If you can't write the question, you're not ready to build.
2. **Write the experience goal** from week 5 that the question serves.
3. **List the minimum components.** For each, name the formal element it represents (section 2 table). Cut anything that doesn't serve the question. Art, flavor text and nice boards come much later, if ever.
4. **Write rules v0.1.** One page, numbered steps for a turn, and a clear end condition. Give the sheet and every card a version number.
5. **Play it alone first.** Play every seat yourself. Look for holes: situations the rules don't cover, a turn where nobody can do anything, a game that can't end. Fix these before anyone else sees it. They are bugs, not design findings.
6. **Play with others.** Now watch. Week 7 teaches you how to watch without explaining. For now, keep a tally of the moments that relate to your question.
7. **Change one thing and play again.** Keep a changelog: version, change, why, what happened.

### Practical tips

- **Blank index cards and a pencil.** Pencil means numbers can change mid-game. Card sleeves with a normal playing card behind make blank cards shuffle well.
- **Put numbers where players can see them.** A card that says "Deal damage" with the amount in your head is not a prototype.
- **Use existing components.** A standard deck of playing cards is a ready-made 52-card randomizer with suits and ranks. Poker chips are resources. A chessboard is an 8 × 8 grid.
- **Make a hidden-information screen** from a folder when someone plays the computer.
- **Time your turns.** If a turn takes more than two minutes on paper, it will not get faster just because a computer runs it. Players still have to decide.
- **Don't fall in love with the prototype.** It exists to be changed. Week 8 is about letting go of the parts that don't work.

## In-class activity (30 minutes)

Groups of three. Each group gets a prompt card with a question and an experience goal, a stack of blank index cards, two dice and a pencil. Example prompt: *Question: does a shared market make players compete or cooperate? Goal: players should feel tempted to help a rival at least once per game.*

1. **Design (10 min).** List at most five components and what each represents. Write rules v0.1 on one side of one card: turn steps and end condition.
2. **Solo test (5 min).** One person plays all seats for three turns and marks every rules hole.
3. **Dice or deck (5 min).** Your prototype has at least one random element. Decide dice or deck for it, and write one sentence tying the choice to your experience goal.
4. **Play (8 min).** Play as far as you get. Tally moments that answer your question.
5. **Log (2 min).** Write v0.2's one change.

Expected output: the component list, the rules card with a version number, the hole list, the dice-or-deck sentence, the tally and the next change.

## Common misconceptions

- **"A prototype is an early version of the game."** A prototype is built to answer a question. Many are thrown away once they have answered it.
- **"A deck with the same cards as the dice is the same randomness."** Same odds per draw, very different spread over a game. Section 3 has the numbers.
- **"Paper prototypes only work for board games."** Turn-based systems from digital games (combat, crafting, loot, quests) prototype well on paper, with one person acting as the computer.
- **"Polish helps testers take it seriously."** Polish makes you reluctant to change things and makes testers comment on art. Keep it ugly until the rules are settled.

## Check yourself

1. You want to test whether a stealth game's guard patrols give players interesting choices. What can a paper prototype tell you, and what can't it?
2. A game draws monster encounters from a deck of 20 cards, 4 of which are "Boss." What is the chance of drawing no Boss in the first 5 draws? Compare with a d20 where 1 to 4 means Boss.
3. Your card game's players always know who is winning because victory points are kept in face-up piles, and the leader gets ganged up on. Name two component changes, one about visibility and one about randomness, and predict the dynamic each creates.

<details>
<summary>Answers</summary>

1. Paper can test the decisions: which route to take, when to wait, whether patrol patterns are readable and whether several routes are viable. Play it as turns on a grid with the guards moved by the computer player. It can't test the timing and tension of moving in real time, or how visibility feels on screen.
2. Deck: `(16/20)(15/19)(14/18)(13/17)(12/16) = 0.282`. d20: `(16/20)^5 = 0.8^5 = 0.328`. The deck makes a five-draw Boss drought less likely.
3. Hide points: keep victory points face down, or score them only at the end. That makes it harder to target the leader, and players may misjudge who's ahead, which keeps tension up. Randomness: add a random element that trailing players benefit from more, such as a die rolled only by the player in last place, or a deck of bonus cards drawn by whoever has fewest points. That is conditional catch-up (week 4) and shrinks leads.

</details>

## Lab hook

**Lab 06, prototype v0.1 and the dice-or-deck test** ([labs/lab06.md](../labs/lab06.md)). You build version 0.1 of the paper prototype for your course project, using your week 5 experience goals. You then run a controlled comparison of a dice version and a deck version of its main random element, measuring droughts and spread. The prototype carries into week 7's silent playtests.

## Sources

- CATAN GmbH, *Catan* base game rules (2020 edition, catan.com). Number tokens with pips; 6 and 8 in red with 5 pips, because 5 of the 36 two-dice outcomes give each.
- CATAN GmbH, *Catan: Traders & Barbarians* rulebook (2025 printing, catan.com, "Game Rules"), "Catan Event Cards" variant. 36 cards replace the dice; 5 dealt face down under the New Year card; the deck is rebuilt when the New Year card is revealed; stated purpose, a more consistent distribution of production values. The rulebook text does not list cards per number; the per-sum counts in section 3 are this course's model.
- Wikipedia, "Catan." First published 1995 by Kosmos; the Event Cards deck first appeared in a boxed expansion set and was later re-released in Traders & Barbarians.
- Fullerton, T. *Game Design Workshop* (4th ed., CRC Press, 2018), chapter 7, physical prototyping. Paraphrased.
- Tetris Guideline 7-bag and Dota 2 pseudo-random distribution: facts and sources in the linked MA102 lectures (weeks 2 and 10).
- Dominion (Donald X. Vaccarino, Rio Grande Games, 2008): publication details as cited in GD101 week 13. The reshuffle-when-empty rule is the genre's defining procedure.
- All probabilities and simulation figures are this course's own, reproducible from the spec below.

## Interactive spec: examples/w06-dice-vs-deck.html

**Purpose.** Show that two dice and a 36-card deck with identical odds look the same draw by draw but produce very different outcomes over a game. The insight on first load: *two identical bar charts on top, and below them a wide dice histogram next to a narrow deck spike.*

**Layout.** Top panel: per-draw frequency (two bar charts or one grouped chart). Bottom panel: histogram of production turns per game for dice and deck, overlaid or side by side. A "one game" strip under the panels. Controls on the right on desktop, below on mobile.

**PRNG.** mulberry32, identical to GD101 week 4's spec:

```
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;}}
```

Game `s` (for `s = 1..G`) uses its own `mulberry32(s)`, separately for dice and for deck.

**Randomizers.**
- Dice: each turn `d1 = 1 + floor(rnd()*6)`, then `d2 = 1 + floor(rnd()*6)`; result `d1 + d2`.
- Deck: build the array in order, sum 2 once, 3 twice, 4 three times, 5 four times, 6 five times, 7 six times, 8 five times, 9 four times, 10 three times, 11 twice, 12 once (36 cards). Fisher-Yates from the end: for `i` from 35 down to 1, `j = floor(rnd()*(i+1))`, swap `i` and `j`. Draw from index 0 upward. Stop after `36 − h` cards, where `h` is "cards left under the New Year card" (default 5). Then rebuild and reshuffle a fresh 36 with the same `rnd`.

**Controls.**
- Target numbers: toggle buttons 2 to 12 (default 6 and 8).
- Game length `T`: 10 to 120 turns, default 60.
- Cards left under New Year `h`: 0 to 10, default 5.
- Number of games `G`: 500, 2,000 (default), 5,000.
- "Play one game" with a seed stepper (default seed 1): shows the sequence of `T` results as a strip of cells, targets highlighted, and the longest dry spell bracketed.

**Top panel.** Frequency of each sum 2 to 12 over all `G × T` draws, for dice and deck, as proportions, with the exact values `ways/36` as tick marks.

**Bottom panel.** For each game, the number of turns on which the result is in the target set. Histograms for dice and deck on a shared x-axis. Also a second tab, "longest dry spell," with histograms of the longest run of non-target turns per game.

**Numbers panel.** For dice and deck: mean, standard deviation (population), 5th and 95th percentile, min and max of production turns; mean and 95th percentile of the longest dry spell. Exact values: `P(no target in first 10 turns)` for dice `(1 − k/36)^10` and for a fresh deck the product `∏_{i=0..9} (36 − k − i)/(36 − i)`, where `k` is the number of cards in the target set.

**Test values.**
- Seed 1, first 10 dice results: 5, 10, 8, 9, 9, 6, 4, 3, 4, 8. Seed 1, first 10 deck results (`h = 5`): 8, 5, 6, 7, 7, 7, 9, 8, 9, 6.
- Targets {6, 8}, `T = 60`, seed 1: dice 16 production turns, longest dry spell 5; deck 16 production turns, longest dry spell 9.
- Targets {6, 8}, `T = 60`, `h = 5`, `G = 2,000` (seeds 1 to 2,000): dice mean 16.60, SD 3.43, 5th to 95th percentile 11 to 22, min 5, max 31, dry spell mean 10.01, 95th percentile 17. Deck mean 16.68, SD 1.46, 14 to 19, min 11, max 20, dry spell mean 9.27, 95th percentile 14. (Percentiles taken as the 101st and 1,901st values of the 2,000 sorted results.)
- Target {8}, `T = 60`, `G = 2,000`: dice mean 8.40, SD 2.66; deck mean 8.37, SD 1.09.
- Exact: `P(no 8 in first 10)` dice 0.2242, deck 0.1745. `P(no 6 or 8 in first 5)` dice 0.1965, deck 0.1745.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Dice and deck differ by colour and by fill pattern (solid versus hatched). All controls keyboard operable. No Catan artwork, hex tiles, number tokens or logos; plain bars and cells only. Respect reduced motion: the "play one game" strip appears at once rather than animating.
