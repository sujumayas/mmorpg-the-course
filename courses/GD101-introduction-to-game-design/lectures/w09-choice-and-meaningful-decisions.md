# GD101 · Week 09 — Choice and meaningful decisions

**Why this matters:** Players do not remember the rules of a game. They remember the moments when they had to choose and weren't sure. If your game hands them choices with an obvious right answer, or choices that change nothing, it will feel dead however good it looks, and you need a way to find those choices before your players do.

**You will be able to:**
- Build a small game tree and compute each position's value by working backwards from the end (minimax).
- Classify a decision as forced, no-stakes or stakes, and explain why a stakes decision stops being interesting once the player can compute its answer.
- Audit the decisions in a paper prototype with the discernable, integrated and uncertain tests, and name the weakest one.
- Propose a rule change that turns a dead decision into a trade-off, and predict its cost.

**Before class:** Salen & Zimmerman, *Rules of Play* (2003), the chapter "Meaningful Play" (short, and the source of two of this lecture's tests), then skim "Defining Games" and "The Magic Circle" from the course reading list. Watch or read a summary of Sid Meier's GDC 2012 talk "Interesting Decisions" (GDC Vault, listed in Sources).

**Prerequisites from earlier courses:** GD101 [week 2](w02-players-objectives-procedures-rules.md) (formal elements: procedures, rules and outcomes) and [week 4](w04-mda-mechanics-dynamics-aesthetics.md) (MDA). [GD101 week 7](w07-playtesting-observe-dont-explain.md), because section 3 turns this week's audit into playtest questions. No math beyond counting and comparing is needed.

**Interactive:** [Tic-tac-toe tree](../examples/w09-tictactoe-tree.html). Keep it open during section 2.

---

## 1. What makes a decision a decision

Sid Meier, the designer of Civilization, gave a talk at GDC 2012 titled "Interesting Decisions," built around his long-standing description of gameplay as "a series of interesting decisions." That phrase is quoted everywhere, and it is useful only once you can say what makes a decision interesting and what makes one dull. This lecture gives you three working tests, one model and a way to check your own prototype.

Start with vocabulary.

- A **choice point** is a moment where the rules let the player pick among two or more **options** (moves, cards, paths, purchases).
- An **outcome** is what happens as a result, now or later.
- A **decision** is the player's act of picking, based on what they believe about the outcomes.

Salen and Zimmerman define **meaningful play** in *Rules of Play* with two conditions. The relationship between an action and its outcome must be **discernable**, meaning the player can perceive what their action did. It must also be **integrated**, meaning the outcome matters to the larger game beyond the moment. A button that plays a sound but changes nothing is discernable and not integrated. A hidden modifier that silently decides the ending is integrated and not discernable. Neither is meaningful play.

These two tests are necessary but not enough. A decision can be discernable and integrated and still boring, because the player already knows the answer. That is the third test, and the one this week's worked example is about.

- **Uncertain:** before choosing, the player cannot simply know which option is best. They have to judge, guess, read the other player or weigh things that don't compare easily.

A decision that passes all three tests is what this course means by an **interesting decision**.

## 2. Worked example: tic-tac-toe is solved

### The hook

Almost every child who learns tic-tac-toe plays it obsessively for a while. Almost every adult finds it pointless. Nothing about the rules changed. There are 255,168 different ways a game of tic-tac-toe can unfold, which sounds like plenty of variety. Yet two adults who know what they are doing draw every single time.

What happened between age six and age twenty? The game tree didn't get smaller. The player's ability to see it got bigger.

### The model: game trees and minimax

A **game tree** is a diagram of every way a game can go. Each **node** is a **position**: the board plus whose turn it is. Each branch from a node is one legal move. The top node, the **root**, is the empty board. The nodes at the bottom, the **leaves**, are finished games: a win for X, a win for O, or a full-board draw.

Give each leaf a **value** from X's point of view: +1 if X won, 0 for a draw, −1 if O won. Then work backwards up the tree with one rule:

```
value(position) = the MAXIMUM of its children's values   if X is to move
value(position) = the MINIMUM of its children's values   if O is to move
value(leaf)     = +1 (X wins), 0 (draw), −1 (O wins)
```

X picks the move that is best for X. O picks the move that is worst for X. This backwards reasoning is called **minimax**, and the value it assigns to a position is what that position is worth if both players play perfectly from there on. When a game's root has a known minimax value and we know the moves that achieve it, the game is **solved**.

Try it by hand. Here is a position with X to move and three empty squares, numbered 0 to 8 left to right, top to bottom.

```
 .  .  O        squares:  0 1 2
 X  O  .                  3 4 5
 X  O  X                  6 7 8
```

- X plays 0. That completes the left column. X wins, value +1.
- X plays 5. O then plays 1 and completes the middle column. Value −1.
- X plays 1. O must now block at 0, because otherwise X plays 0 and wins down the left column. X takes the last square, 5, and nobody has a line. Value 0.

X is to move, so the position's value is the maximum, +1, and the right move is square 0. That is minimax on a tiny tree. A computer does the same thing for the whole game in a fraction of a second.

### Numbers you can check

Running minimax over the full tree gives these counts. You can reproduce them with the short program in lab 09, and the interactive shows the same totals.

| Quantity | Count |
|---|---|
| Distinct complete games (move sequences to a win or full board) | 255,168 |
| ... won by X (first player) | 131,184 |
| ... won by O | 77,904 |
| ... drawn | 46,080 |
| Distinct legal positions, including the empty board | 5,478 |
| Distinct positions if rotations and reflections count as the same | 765 |
| Minimax value of the empty board | 0 (a draw) |

Counting games makes X look strong: X wins more than half of all possible games. Minimax says the true value is a draw. Both are correct, and the gap between them is the lesson. Most of those 255,168 games contain a mistake.

Here is what happens when different kinds of players meet. "Random" means picking uniformly among legal moves. "Perfect" means picking uniformly among the moves that keep the minimax value.

| X plays | O plays | X wins | O wins | Draw |
|---|---|---|---|---|
| Random | Random | 58.5% | 28.8% | 12.7% |
| Perfect | Random | 96.8% | 0% | 3.2% |
| Random | Perfect | 0% | 77.7% | 22.3% |
| Perfect | Perfect | 0% | 0% | 100% |

When at least one player can't see the tree, results vary and skill shows. When both can see it, the outcome is fixed before the first move.

Now look at the decisions themselves. For every position where the game is not over, compare the minimax values of the available moves.

- **Forced:** only one legal move. No decision at all.
- **No-stakes:** several moves, all with the same value. Whatever you pick, perfect play from there gives the same result.
- **Stakes:** at least one move is worse than another. A mistake is possible.

| Kind of position | Count | Share of 4,520 unfinished positions |
|---|---|---|
| Forced | 222 | 4.9% |
| No-stakes | 1,107 | 24.5% |
| Stakes | 3,191 | 70.6% |

At first glance tic-tac-toe is full of stakes: in seven positions out of ten, you can blunder. The opening shows how those stakes feel in practice.

| X's first move | Value | O's replies that lose | O's replies that draw |
|---|---|---|---|
| Corner (4 squares) | 0 | 7 | 1 (the center) |
| Edge (4 squares) | 0 | 4 | 4 |
| Center (1 square) | 0 | 4 (the edges) | 4 (the corners) |

X's very first decision is a no-stakes decision: all nine openings draw with perfect play. O's reply to a corner opening is a high-stakes decision: seven of eight squares lose. But it has exactly one right answer, "take the center," and once you know it, the decision is not a decision. It is a lookup.

That is the whole story of why tic-tac-toe dies. A stakes decision is interesting only while the player is uncertain which option is best. Tic-tac-toe has 3,191 stakes positions, and a patient ten-year-old can learn a handful of rules (win if you can, block if you must, take the center, answer a corner with the center, and so on) that answer every one of them. After that, every stakes decision fails the uncertain test, every no-stakes decision was never interesting, and the game becomes a ritual that ends in a draw.

### The visual

Open [`examples/w09-tictactoe-tree.html`](../examples/w09-tictactoe-tree.html). It has two linked views of the same board. The left board is the game as a child sees it: empty squares, your move. The right board is the same position with the solution shown, every empty square coloured by its minimax value (win, draw or loss for the player to move). Play a few moves on the left. Then look right. The "decision" you just agonized over was already decided, and usually most squares on the right are the same colour. Under the boards, a meter labels the current position forced, no-stakes or stakes. Switch the opponent between Random and Perfect and play five games of each; the results table fills in and should drift toward the percentages above.

### Cross-game recognition

Tic-tac-toe is not a strange exception. Every finite game with perfect information and no chance has a minimax value, and many have been solved.

**Connect Four.** Solved in 1988, independently by James D. Allen and Victor Allis, about two weeks apart. With perfect play the first player wins. The tree is vastly bigger than tic-tac-toe's, far beyond what a person can hold in their head, so human games still feel like decisions. Solved for computers is not the same as solved for people.

**Checkers (English draughts).** Weakly solved in April 2007 by Jonathan Schaeffer's team after many years of computation, and published in *Science* that year. From the standard start, perfect play by both sides is a draw. It took one of the longest computations in game research to show that, and no human can reproduce it. People keep playing checkers because the solution is out of human reach.

**Nim.** Several heaps of counters; on your turn you take any number from one heap; whoever takes the last counter wins. Charles Bouton published the complete solution in 1901: write each heap size in binary and combine them with exclusive-or (XOR, add the binary digits without carrying). If the result is zero, the player to move loses against perfect play; otherwise they can win by moving to a position whose XOR is zero. For heaps of 3, 4 and 5: `011 XOR 100 XOR 101 = 010`, which is 2, not zero, so the first player wins, by taking 2 from the heap of 3 to leave heaps of 1, 4 and 5 (`001 XOR 100 XOR 101 = 000`). Nim is a stronger version of the tic-tac-toe problem: once you know the XOR rule, every decision in every Nim game is a two-second calculation.

**Tic-tac-toe in disguise.** Players take turns picking numbers from 1 to 9, each number once; the first to hold three numbers that sum to 15 wins. It feels like an arithmetic game. It is tic-tac-toe, played on this magic square, where every row, column and diagonal sums to 15:

```
 2  7  6
 9  5  1
 4  3  8
```

The eight triples from 1 to 9 that sum to 15 are exactly the eight lines of the square. Someone who knows tic-tac-toe's solution beats this game at once, and someone who doesn't finds it full of interesting decisions. The decisions are interesting only while the player can't see the structure.

Four games, one model. When you meet a deterministic game with no hidden information, ask: how big is its tree compared with what a player can hold in mind, and what happens to it when players learn the answer?

### Eyes-open design judgment

If tic-tac-toe dies because its answer is small and learnable, designers have several ways to keep decisions uncertain. Each one has a cost.

- **Make the tree too big.** Chess and Go keep their decisions interesting by having trees far too large to solve by hand, and neither game has been solved. Cost: a large tree also means a steep learning curve and long games. Complexity has to be learned before it can be enjoyed.
- **Hide information.** In poker you can't see your opponent's cards, so the same move can be right or wrong depending on what they hold. Cost: players can feel that outcomes are arbitrary if they never learn what was hidden. Reveal information at the end so players can learn.
- **Add randomness.** Dice and shuffled decks change the position each game, so memorized answers stop working. Cost: randomness weakens the link between decision and outcome, and too much of it breaks the discernable test. Week 10 measures this trade-off.
- **Make players move at the same time.** Rock-paper-scissors has no best move, because the right choice depends on what the other player picks at the same moment. Cost: pure guessing games have no depth unless players can read each other's habits over many rounds.
- **Give options that don't compare directly.** "Take 3 gold now, or gain 1 gold at the start of each of your remaining turns" has no fixed answer. With more than 3 turns left, the income is better; with fewer, the gold is better; at exactly 3, they tie. The best answer depends on the situation, so the player has to think each time. Cost: the designer has to keep the trade-off balanced across situations, or one option becomes the answer and the decision dies again. Week 11 calls that option a dominant strategy.

Two warnings. First, "solved" is a property of the rules, and "interesting" is a property of the player facing them. Connect Four is solved and still worth playing for most people. Design for the player you expect. Second, decisions are not the only source of enjoyment. Snakes and ladders has no decisions and small children still enjoy it for the suspense and the company. [Week 5's kinds of fun](w05-player-experience-goals-and-the-8-kinds-of-fun.md) reminds you that challenge is one aesthetic among several. But if your goal is challenge, dead decisions will sink it.

## 3. Auditing the decisions in your prototype

A **decision audit** is a systematic pass over every choice point in a design. You can do one on paper before any playtest, then confirm it with players using the week 7 method.

For each choice point, fill in one row.

| Question | Fails if |
|---|---|
| How many options are really available? | Only one (forced), or one option is always illegal in practice. |
| Do the options lead to different outcomes? | All options give the same result (no-stakes). |
| Can the player see the outcome of their choice? (discernable) | The effect is hidden, delayed without feedback, or too small to notice. |
| Does the outcome matter later? (integrated) | The choice changes nothing beyond this moment. |
| Can the player know the best option without judging? (uncertain) | A simple rule always gives the right answer. |
| Does the best option change with the situation? | The same option is best in every situation you can construct. |

The last question is the fastest test for a dead decision. Try to write down two situations where different options are best. If you can't, the decision is probably a lookup.

### Turning the audit into playtest evidence

Paper audits give you hypotheses. Players give you evidence. Using the week 7 method, watch for these signs at each choice point.

- **Hesitation.** The tester pauses, compares, reaches for one card then another. Evidence of uncertainty.
- **Instant, identical choices.** Every tester picks the same option without pausing, every time. Evidence of a lookup or a no-stakes choice.
- **"Does it matter?"** A tester asking this, aloud, is telling you the decision failed the discernable test.
- **Different choices from different testers in the same situation**, each with a reason in the debrief. Strong evidence of an interesting decision.

Record these as observations with counts, exactly as in week 7. "5 of 5 testers bought the sword on turn 1 without hesitating" is a finding. It points to a dead decision.

## 4. Fixing a dead decision

You have three moves, and each maps to one of the failed tests.

1. **Make it discernable.** Show the result. Add a number, a sound, a visible change on the board. If players can't tell that their choice did anything, they will stop treating it as a choice.
2. **Make it integrated.** Connect the outcome to something later. A choice of starting card that is forgotten after round one can become a choice that decides which cards you can buy later.
3. **Make it uncertain.** Break the lookup. The usual tool is a trade-off: give the obvious best option a cost that matters in some situations and not in others. The gold-now-or-income-later example in section 2 is the template: the break-even point moves with the number of turns left.

Here is a small case. In a student card game, players choose each turn between *Attack* (deal 3 damage) and *Defend* (block 2 damage this turn). Testers always attacked. The audit shows why: the opponent always has something to hit, and blocking 2 is always worth less than dealing 3. The decision fails the "best option changes with the situation" test.

A one-rule fix: *Defend also lets you draw a card.* Now the decision depends on the situation. If you are about to take lethal damage, defend. If your hand is weak, defend to draw. If the opponent is nearly dead, attack. Testers should start hesitating, and different testers should choose differently in the same position. That is what you check in the next loop (week 8). The fix may overshoot, so that everyone now defends every turn, which is why you test rather than assume.

## In-class activity (25 minutes)

Pairs. Materials: paper, pencil, a printout of the magic square from section 2, and one paper prototype from week 6.

1. (8 min) **Number game.** Play the pick-to-15 game from section 2 three times *without* the magic square. Then play three times with it on the table. Note how each game felt and how long each move took.
2. (5 min) **Hand minimax.** Draw the position from section 2 and the whole tree below it (every move to the end). Label every leaf and work the values up. Confirm the root is +1.
3. (12 min) **Audit.** Pick three choice points in the prototype and fill in the audit table from section 3 for each. Mark the weakest one and write a one-rule fix aimed at the test it fails.

**Expected output:** a note comparing the two sets of number games (most pairs report faster, flatter games with the square), a completed tree with values, and three audit rows with one proposed fix.

## Common misconceptions

- **"More options means more interesting decisions."** Twenty options where one is always best is a lookup with extra reading. Two options that trade off against each other can be more interesting than twenty.
- **"If a mistake is possible, the decision is interesting."** Tic-tac-toe has thousands of positions where a mistake is possible and still dies, because every one of them has a learnable answer. Stakes are necessary, and uncertainty is what makes them interesting.
- **"A solved game can't be fun."** Solved is about the rules; fun is about the player. Connect Four is solved and still makes decisions interesting for people who can't compute its tree.
- **"Randomness always makes decisions interesting."** Randomness breaks lookups, but too much of it cuts the link between choice and outcome, so decisions stop being discernable. It is a dial, not a fix (week 10).

## Check yourself

1. In the position below, it is O's turn. Squares are numbered as in section 2. List O's legal moves, give the minimax value of each (from X's point of view), and classify the position as forced, no-stakes or stakes.
   ```
    X  O  X
    .  O  .
    .  X  .
   ```
2. You design "Take 5 gold now, or 2 gold at the start of each of your remaining turns." For how many remaining turns is each option better? Is this decision interesting at the start of a 10-turn game? At turn 9? What would you change?
3. Nim with heaps of 1, 2 and 3. Is the player to move winning or losing? Show the XOR.
4. A classmate says their deck-building game has "tons of decisions" because there are 12 cards in the market each turn. Playtest logs show that 5 of 5 testers bought the most expensive card they could afford every turn. Which audit test does the market decision fail, and what one-rule change might fix it?

<details>
<summary>Answers</summary>

1. Empty squares are 3, 5, 6 and 8, so O has four moves. O at 3 threatens the middle row (3-4-5), so X must block at 5; after that no line can be completed, value 0. O at 5 is the mirror image: X blocks at 3, value 0. O at 6 or O at 8 creates no threat, and X cannot make two threats at once from there, so perfect play again ends in a draw, value 0. The children are {0, 0, 0, 0}, so this is a **no-stakes** position. It looks tense, with O holding the center and the top middle, but nothing O chooses here changes the result. (X, on the other hand, faces a stakes decision after O plays 3 or 5: blocking draws, anything else loses. Confirm both in the interactive.)
2. Income gives 2 per turn, so after `t` turns it gives `2t`. Income beats the lump sum when `2t > 5`, so with 3 or more turns left; the lump sum is better with 2 or fewer; there is no exact tie (2.5 turns). At the start of a 10-turn game, income wins by a mile (20 against 5), so the decision is a lookup. At turn 9 with 2 turns left, take the gold, again a lookup. The decision is only interesting in the narrow band around 2 to 3 turns left. A fix: make the lump sum grow over time, or offer it only at a moment when the break-even falls in a contested range, so the answer depends on the situation more often.
3. `01 XOR 10 XOR 11 = 00`. The XOR is zero, so the player to move loses against perfect play.
4. It fails the uncertain test (and the "best option changes with the situation" test): a simple rule, buy the most expensive card, always gives the answer, so 12 options collapse to one. A one-rule change: make expensive cards clog the deck (for example, each costly card adds a dead card to your discard pile), so cheaper cards are sometimes better. Then retest to see whether testers start hesitating.

</details>

## Lab hook

**Lab 09, solve it, then fix it** ([labs/lab09.md](../labs/lab09.md)). You run a provided minimax script on tic-tac-toe and one variant, reproduce this lecture's counts, then audit the decisions in your own prototype and test one rule change aimed at a dead decision with three silent testers.

## Sources

- Meier, S. (2012). "Interesting Decisions." Game Developers Conference 2012, Firaxis Games. GDC Vault session page describes gameplay as a series of interesting decisions. https://www.gdcvault.com/play/1015756/Interesting
- Salen, K. & Zimmerman, E. (2003). *Rules of Play: Game Design Fundamentals*. MIT Press. The chapter "Meaningful Play" (cited by title; chapter number not checked): the discernable and integrated conditions (paraphrased).
- Wikipedia, "Solved game" (accessed September 2026). Tic-tac-toe is a draw with perfect play; Connect Four solved October 1988 by James D. Allen and independently by Victor Allis, first-player win; checkers weakly solved April 29, 2007 by Jonathan Schaeffer's team, draw; Nim solved by C. L. Bouton (1901 to 1902). https://en.wikipedia.org/wiki/Solved_game
- Schaeffer, J. et al. (2007). "Checkers Is Solved." *Science*, 317(5844), 1518-1522.
- Bouton, C. L. (1901). "Nim, a game with a complete mathematical theory." *Annals of Mathematics*, 3(1/4), 35-39.
- Tic-tac-toe counts (255,168 games and their split, 5,478 positions, 765 up to symmetry, the decision classification, the random and perfect player outcomes, the opening table): computed for this lecture by exhaustive search with the lab 09 script. The 255,168 and 5,478 totals agree with the values widely reported for the game.

## Interactive spec: examples/w09-tictactoe-tree.html

**The one insight.** In tic-tac-toe, the decision you agonize over already has a known answer. Showing the solved values beside the "player's view" board makes the lookup visible: most squares share a colour, and the few that don't have one obvious best move.

**Layout.** Two linked boards side by side on desktop (≥ 800px), stacked on mobile, with a decision meter and a results panel below.

**Left board, "What the player sees".** A playable 3 × 3 board. The human plays X or O (toggle, default X, X moves first). Clicking or pressing Enter/Space on a focused square places a mark. The computer opponent then moves after a short delay (no delay if `prefers-reduced-motion`).

**Right board, "What the tree knows".** The same position, read-only. Each empty square is filled with its minimax result *for the player to move*: "Win" (success colour), "Draw" (neutral), "Loss" (danger colour), with text labels as well as colour. Occupied squares show the marks. A toggle "Hide the solution" (default: shown) blanks the right board so the class can play first and reveal after.

**Decision meter (below boards).** For the current position: number of legal moves; the class "Forced", "No-stakes" or "Stakes"; if stakes, "k of m moves keep the best result." For the empty board it must read "9 legal moves, No-stakes." After X in a corner it must read, for O, "8 legal moves, Stakes, 1 of 8 moves keeps the best result."

**Opponent control.** Radio: "Random" (uniform over legal moves) or "Perfect" (uniform over moves with the best minimax value). Seeded PRNG (mulberry32, seed 9) for reproducibility, reseeded per new game with seed + game number.

**Results panel.** Running tally of the human's games (wins, losses, draws) per opponent type. A "Simulate 1,000 games" button that plays the two computer policies against each other for the selected pairing (Random vs Random, Perfect vs Random, Random vs Perfect, Perfect vs Perfect) and shows the percentages beside the exact values from the lecture.

**Whole-tree panel (collapsible, "The whole game in numbers").** Static computed totals: 255,168 games (X 131,184, O 77,904, draws 46,080); 5,478 positions; 765 up to symmetry; unfinished positions 4,520 split into forced 222, no-stakes 1,107, stakes 3,191. A small bar chart of stakes positions by number of marks on the board: 0: 0 of 1; 1: 9 of 9; 2: 60 of 72; 3: 186 of 252; 4: 640 of 756; 5: 768 of 1,140; 6: 1,032 of 1,372; 7: 496 of 696; 8: 0 of 222.

**Formulas and algorithm.** Minimax with memoization over board strings. Leaf value +1 (X line), −1 (O line), 0 (full board, no line). X maximizes, O minimizes. "Result for the player to move" on the right board: for X, +1 → Win, 0 → Draw, −1 → Loss; for O, reversed. Class: forced if 1 legal move; no-stakes if all children share a value; otherwise stakes. Compute the whole-tree panel at load (it is fast) and assert it matches the static numbers; log a console warning if not.

**Test values (must match).**
- Empty board: value 0; every square shows Draw; meter "No-stakes".
- X at square 0 (corner): O's squares show Draw only at square 4, Loss elsewhere (7 squares).
- X at square 4 (center): O shows Draw at 0, 2, 6, 8 and Loss at 1, 3, 5, 7.
- Position `. . O / X O . / X O X`, X to move: square 0 Win, square 1 Draw, square 5 Loss.
- Position `X O X / . O . / . X .`, O to move: squares 3, 5, 6, 8 all Draw; meter "No-stakes". After O plays 3, X sees 5 Draw, 6 Loss, 8 Loss.
- Exact outcome probabilities: Random vs Random X 58.49%, O 28.81%, draw 12.70%; Perfect X vs Random O: 96.78% / 0% / 3.22%; Random X vs Perfect O: 0% / 77.75% / 22.25%; Perfect vs Perfect: 0 / 0 / 100%. The 1,000-game simulation should land within a few points of these.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css`. Squares are buttons with `aria-label` such as "Row 1, column 3, empty, result for X: Draw." Results never rely on colour alone. Live region announces each move and the new meter reading. Respect `prefers-reduced-motion` and `prefers-color-scheme`. Draw X and O as plain strokes; no themed art.
