# GD101 · Week 02 — Formal elements I: players, objectives, procedures, rules

**Why this matters:** When you design, you never change "the game". You change one part of it: how many people play, what they are trying to do, what they do on a turn, or what they are allowed to do. This week gives you names for those parts and shows that two games can look nothing alike and still be the same game underneath.

**You will be able to:**
- Describe any game with four formal elements: its player structure, objective, procedures and rules.
- Separate a game's rules into operational, constitutive and implicit rules, and find an implicit rule in a game you play.
- Prove that two differently presented games are the same game by building a one-to-one map between their states.
- Predict how changing one formal element (for example the player structure) changes what players do.

**Before class:** Fullerton, *Game Design Workshop* (4th ed., 2018), chapter 3, the sections on players, objectives, procedures and rules. Salen & Zimmerman, *Rules of Play* (2003), the chapter "Rules on Three Levels". Ian Schreiber, *Game Design Concepts* (online course, 2009), "Level 3: Formal Elements of Games".

**Prerequisites from earlier courses:** None. From this course, [week 1](w01-what-is-a-game.md) (the feature checklist and Suits's constitutive rules).

**Interactive:** [Three-to-Fifteen and tic-tac-toe](../examples/w02-fifteen-game.html). Keep it open during section 2.

---

## 1. The parts list

Tracy Fullerton's *Game Design Workshop* breaks every game into eight **formal elements**. "Formal" here means the parts that make up the structure of a game, the ones you could write down in a rulebook, as opposed to the art or the story. The eight are players, objectives, procedures, rules, resources, conflict, boundaries and outcome. This week covers the first four. Week 3 covers the rest.

Why a parts list? Because it turns a vague feeling ("this game is too chaotic") into a question about one part ("is it the player structure, with six people all attacking each other?"). It also lets you compare games that look nothing alike.

### Players

The first question about any game is who plays, and against whom. How many players? Is the number fixed or a range? Can people join or leave mid-game? Then the relationships between them. Ian Schreiber's online course lists these common **player structures** (the list is not complete, and Fullerton gives a similar one):

| Structure | Shape | Example |
|---|---|---|
| Solitaire | 1 vs the game | Klondike, Minesweeper |
| Head-to-head | 1 vs 1 | Chess, Go |
| Cooperative (PvE) | many vs the game | A World of Warcraft dungeon group; the board game Pandemic |
| One against many | 1 vs a team | Scotland Yard, where one player is Mr. X |
| Free-for-all | each vs each | Monopoly; deathmatch in a shooter |
| Separate individuals vs the system | each vs the house, not each other | Blackjack at a casino |
| Team competition | team vs team | Bridge; capture the flag |

The structure alone predicts a lot of behaviour. In a free-for-all with three or more players, the leader tends to get attacked by everyone else, so players hide their strength. In a cooperative game, the most experienced player tends to tell everyone else what to do. Designers of co-op board games call this the "quarterback" problem. Neither behaviour is in the rules. Both come from the player structure.

MMOs are unusual because they run many structures at once. The same character may be in a cooperative dungeon group, a team battleground, and a free-for-all auction house in one evening.

### Objectives

The **objective** is what the players are trying to achieve. It is usually the first thing a new player asks ("how do I win?") and one of the best places for a stuck designer to start. Schreiber lists common objectives:

- **Capture or destroy.** Remove the opponent's pieces. Chess, Stratego.
- **Territorial control.** Hold areas of the board. Risk, Diplomacy.
- **Collection.** Gather sets. Rummy.
- **Solve.** Work out hidden information. Clue.
- **Chase, race or escape.** Get somewhere first, or get away. Tag, Super Mario Bros.
- **Spatial alignment.** Put things in a pattern. Tic-tac-toe, Tetris.
- **Build.** Grow something to a target. The Settlers of Catan.
- **Avoid the forbidden act.** Lose if you do the wrong thing. Jenga, Twister.

Many games stack objectives. A raid in an MMO has a destroy objective (kill the boss) inside an escape-and-positioning objective (do not stand in the fire). The objectives also do not have to match the game's name or theme. "Chess" sounds like a war, and its objective is a very specific capture: trap one piece.

### Procedures

**Procedures** are the actions players take and the order they take them in. It helps to split them into three phases:

- **Setup.** What happens once, at the start. Deal seven cards. Place the pieces.
- **Progression.** What happens during play. On your turn, draw a card, then play one.
- **Resolution.** What ends the game and decides the result. When the deck runs out, highest score wins.

A procedure has an actor (who does it), an action (what they do) and a trigger (when). "At the start of your turn, draw a card" is a procedure triggered by the turn. "When a player reaches 10 points, the game ends" is triggered by the game state.

The order of actions is its own design lever, called **sequencing**:

- **Turn-based.** One player acts at a time. Most board games.
- **Simultaneous turns.** Everyone commits in secret, then reveals. Diplomacy; rock-paper-scissors.
- **Real-time.** Everyone acts as fast as they can. Most action video games.

Change the sequencing and the same actions become a different game. Chess is turn-based. If both players wrote their moves in secret and revealed them together, bluffing would appear where there was none.

### Rules

**Rules** are the limits on what players can do and what happens when they do it. Salen & Zimmerman split rules into three levels, and the split is the most useful idea in this lecture:

- **Operational rules** are the rules as written for players. "Take turns marking an empty square with your symbol. Three in a row wins."
- **Constitutive rules** are the abstract logic underneath: the states the game can be in, the moves that change them, and which states count as wins. They do not mention squares or symbols at all.
- **Implicit rules** are the unwritten expectations everyone assumes. "Don't take an hour over one move." "Don't read your opponent's hand when they drop it."

Implicit rules are where most real-life arguments about games happen. Schreiber's example is spawn camping in shooters: waiting at the spot where defeated players reappear and defeating them again before they can act. Nothing in the operational rules forbids it. Whether it is fair play depends on which implicit rules the players share. When two players hold different implicit rules, one calls the other a cheater and the other says "it's in the rules". The designer's job is to turn as many of those disputes as possible into operational rules, or to change the game so the behaviour does not pay.

The constitutive level is harder to see because nobody reads it. The worked example makes it visible.

## 2. Worked example: Three-to-Fifteen, the game you already know

### The hook

Here is a game for two players. Lay out nine cards numbered 1 to 9. Take turns picking one card. The first player to hold **exactly three cards that add up to 15** wins. You may hold more than three cards; only three of them need to add up. If the cards run out with no winner, it is a draw.

Play three rounds with a neighbour before you read on. Most people find it surprisingly hard. You have to keep track of all the ways to make 15, both yours and your opponent's, and the arithmetic crowds out the strategy.

The game goes by several names: Three-to-Fifteen, Pick 15, Number Scrabble. The psychologist John Michon described a version he called JAM in 1967. The economist and cognitive scientist Herbert Simon used it in *The Sciences of the Artificial* (1969) to make a point about problem solving, which you will see in a moment.

The surprise: you have played this game hundreds of times. It is tic-tac-toe.

### The model

Write the constitutive rules of a "claim game" with no board and no symbols:

- There is a set of **items**.
- There is a list of **winning sets**, each a group of items.
- Two players alternately claim one unclaimed item.
- A player who owns every item of some winning set wins. If all items are claimed with no winner, it is a draw.

That is the whole game. Two claim games are **the same game** (the mathematical word is **isomorphic**, "same shape") if you can relabel the items of one so that its winning sets become exactly the winning sets of the other. Then every move, every threat and every strategy in one has a twin in the other.

For tic-tac-toe, the items are the 9 squares and the winning sets are the 8 lines (3 rows, 3 columns, 2 diagonals).

For Three-to-Fifteen, the items are the numbers 1 to 9 and the winning sets are the groups of three different numbers that add to 15.

The relabelling that proves they are the same game is a **magic square**, a 3 × 3 grid where every row, column and diagonal adds to the same number:

```
2  7  6
9  5  1
4  3  8
```

Write each number in its square. Picking a number in Three-to-Fifteen is marking that square in tic-tac-toe.

### Numbers you can check

**Step 1. Every line of the square adds to 15.**

| Line | Numbers | Sum |
|---|---|---|
| Top row | 2, 7, 6 | 15 |
| Middle row | 9, 5, 1 | 15 |
| Bottom row | 4, 3, 8 | 15 |
| Left column | 2, 9, 4 | 15 |
| Middle column | 7, 5, 3 | 15 |
| Right column | 6, 1, 8 | 15 |
| Diagonal | 2, 5, 8 | 15 |
| Other diagonal | 6, 5, 4 | 15 |

That gives 8 lines, each a triple summing to 15.

**Step 2. There are no other triples.** List every set of three different numbers from 1 to 9 that adds to 15. Go in order of the smallest number:

- Starting with 1: {1, 5, 9}, {1, 6, 8}.
- Starting with 2: {2, 4, 9}, {2, 5, 8}, {2, 6, 7}.
- Starting with 3: {3, 4, 8}, {3, 5, 7}.
- Starting with 4: {4, 5, 6}.
- Starting with 5 or more: impossible, since 5 + 6 + 7 = 18 is already too big.

That is exactly 8 triples, and each one is a line in step 1. So the winning sets match one for one, and the two games are the same game. Nothing was approximated.

**Step 3. Strategy transfers.** In tic-tac-toe, the centre square is on 4 lines, each corner on 3 lines, and each edge on 2. Count how many of the 8 triples contain each number:

| Number | Triples containing it | Square in tic-tac-toe |
|---|---|---|
| 5 | 4 | centre |
| 2, 4, 6, 8 | 3 each | corners |
| 1, 3, 7, 9 | 2 each | edges |

Check the total: 4 + 4 × 3 + 4 × 2 = 24, and 8 triples × 3 numbers = 24. The advice "take the centre" becomes "take the 5". "Corners beat edges" becomes "even numbers beat odd ones".

**Step 4. A full game, both ways.** Player A plays 5 (centre). B plays 1 (right edge). A plays 2 (top-left corner), which threatens {2, 5, 8}. B must take 8. Now B holds 1 and 8 and threatens {1, 6, 8}, so A must take 6. But A now holds 2, 5 and 6, which threatens both {2, 6, 7} and {4, 5, 6}. B can block only one. A wins on the next pick. In tic-tac-toe this is a textbook **fork**: two threats at once. It looks like arithmetic in one game and geometry in the other, and it is the same move.

### A visual you can move

Open [`examples/w02-fifteen-game.html`](../examples/w02-fifteen-game.html). The first screen shows nine number cards and a hidden board. Play Three-to-Fifteen against the computer. Then press "Show the board": each card you and the computer took appears in its magic-square position, marked X or O. Play again with both views visible and watch each pick land on the grid. A panel lists your "live" triples, the ones you could still complete, and the same triples glow as lines on the board.

The insight: **the operational rules changed and the constitutive rules did not.** Everything that makes the game hard in card form is bookkeeping that the board does for you with your eyes.

### Cross-game recognition

The same constitutive rules turn up under very different operational rules and themes. Learning to see through the surface is the skill.

**The type triangle.** Rock-paper-scissors has three options, each beating one and losing to one. Write it as constitutive rules: three items A, B, C with A beats B, B beats C, C beats A. Pokémon's starter types have the same shape (Fire moves are super effective against Grass, Grass against Water, Water against Fire). The Fire Emblem series uses a weapon triangle: swords beat axes, axes beat lances, lances beat swords. Three games, three themes, one loop. The operational rules differ a lot (a simultaneous hand sign, a damage multiplier, a hit-rate bonus), and that difference matters for feel. The loop is identical. You will analyse these loops in depth in MMO303 week 9, [Intransitivity and counters](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w09-intransitivity-and-counters.md).

**The camera.** Schreiber points out that the arcade game Gauntlet and the shooter DOOM have highly similar gameplay: move through a maze of rooms, shoot waves of monsters, find keys to open doors. The biggest difference is where the camera sits, top-down versus first-person. The camera belongs to the presentation, not the constitutive rules. It still changes what players can see, which changes what they can plan.

**JAM.** Michon's JAM, described in 1967, is another tic-tac-toe in disguise, built from a different presentation again. Any game whose constitutive rules are "claim items, win by completing a set from a list of 8 sets matching the lines of a 3 × 3 grid" is tic-tac-toe, however it looks.

In every case, the method is the same: strip the theme and the operational wording, write the states, moves and win conditions, and compare.

### Eyes-open design judgment

If two games are the same game, why do players experience them so differently? That was Herbert Simon's point. The **representation** of a problem changes how hard it is for a human to solve, even when the problem itself is identical. Tic-tac-toe puts the winning sets on the table as straight lines your eye can find. Three-to-Fifteen hides them inside arithmetic you must redo every turn.

This gives you design decisions to make on purpose:

- **Choose the representation for the difficulty you want.** If a system is hard in the wrong way, you may not need new rules. You may need to show the existing rules better. A game that asks players to track eight sums in their head is testing memory, not strategy. If you want strategy, draw the board.
- **Sometimes hide the structure on purpose.** A puzzle game may want players to discover that two things are the same. Hiding the representation creates the "aha" moment. The cost is players who never get it and quit.
- **Theme helps memory.** Chess moves have nothing to do with their pieces' names, so new players must memorize them. Schreiber notes that in the board game Puerto Rico the roles roughly do what their names say (the builder lets you build), so the rules are easier to learn. A good theme is a free rules summary.
- **Don't confuse a reskin with a new game.** Changing the theme, the art or the wording leaves the constitutive rules untouched. If playtesters report the same problem after a reskin, it was never the skin.
- **Write your implicit rules down.** Every multiplayer game ships with implicit rules its designers assumed. The moment players disagree about one (spawn camping, stalling, stealing a kill in an MMO), you get a community argument. Decide which ones become operational rules, and enforce those in code.

### Check the model

1. Take the magic square and add 1 to every number (so it uses 2 to 10). What must the winning triples now sum to? Is the game still tic-tac-toe?
2. In Three-to-Fifteen, your opponent opens with 2. Which number should you take, according to the tic-tac-toe translation, and why?
3. Someone proposes "Four-to-Thirty-Four": numbers 1 to 16, win with four that sum to 34. Is it automatically 4 × 4 tic-tac-toe? What would you need to check?

Answers are in the Check yourself section.

## 3. Formal elements interact

The four elements in this lecture are not independent. Change one and the others shift.

**Player structure changes objectives.** Monopoly's objective is "be the last player not bankrupt". With two players that is a duel. With six it becomes a long elimination where knocked-out players can sit with nothing to do for an hour. The objective and the player count pull against each other.

**Sequencing changes the value of information.** In turn-based chess you see every move before you answer it. In simultaneous rock-paper-scissors you never do. The same "beats" relation produces a pure guessing game in one sequencing and would be trivial in the other. If rock-paper-scissors were played in turns, the second player would always win.

**Procedures create implicit rules.** Any procedure that has no time limit invites stalling. Any procedure that says "players may trade" invites the question "can I trade with someone who has been eliminated?" Each new procedure is a promise that you will answer the edge cases.

**Digital games enforce operational rules for you.** In a board game, players read, remember and apply the operational rules, and they sometimes forget or cheat. In a video game, the code applies them every time. That removes a whole class of arguments. It also means the code *is* the operational rules, including its bugs. A glitch that lets you walk through a wall is, from the machine's point of view, a legal move. Whether exploiting it is fair play goes back to implicit rules, and MMO companies publish their implicit rules as terms of service for this reason.

## In-class activity (25 min)

**Rules lawyers.** Pairs. Materials: one sheet of paper, a pen, and a coin or die.

1. (8 min) Pick a playground game you all know: tag, hide-and-seek, or musical chairs. Write its formal elements: player structure, objective, setup, progression, resolution, and its operational rules. Keep it under 150 words.
2. (5 min) Swap sheets with another pair. That pair now plays (or walks through) the game following your sheet *literally*, looking for any move the rules allow that obviously breaks the game. Example: hide-and-seek with no rule against hiding outside the building.
3. (7 min) Each loophole they found is an implicit rule you forgot to write. Add a line for each one. Count how many lines you added.
4. (5 min) Class tally: which element hid the most loopholes? (Expect resolution and boundaries, meaning "when does it end?" and "where can I go?")

**Expected output:** a rules sheet with the original rules, the added lines in a different colour, and one sentence on which loophole surprised you most.

## Common misconceptions

- **"The rules are what's in the rulebook."** The rulebook holds the operational rules. The constitutive rules are the logic under them, and the implicit rules are never written at all. All three shape play.
- **"Different theme, different game."** A theme changes presentation. Three-to-Fifteen and tic-tac-toe share every state, move and win, so they are the same game. The theme can still change how hard the game is for humans to play.
- **"If the computer allows it, it's allowed."** The computer enforces operational rules, bugs included. Players still bring implicit rules, and communities enforce them socially.
- **"Objectives are obvious."** Players often pursue objectives the designer did not intend (collecting everything, finishing fast, helping others). Watch what they actually try to do.

## Check yourself

1. Write the constitutive rules of Connect Four as a claim game. What makes it *not* a pure claim game like tic-tac-toe? (Hint: can you claim any empty cell?)
2. A two-player card game has a rule "Each turn, play one card face down; both players reveal at once." Name its sequencing type. Suggest what happens to bluffing if you change it to alternating turns with cards face up.
3. List three implicit rules of a World of Warcraft five-player dungeon run that are not enforced by the game's code.
4. Answer the three "Check the model" questions in section 2.

<details>
<summary>Answers</summary>

1. Items: the 42 cells of a 7-column, 6-row grid. Winning sets: every group of 4 cells in a straight line (horizontal, vertical, diagonal). Players alternately claim a cell. The difference is a move restriction: you may only claim the lowest empty cell in a column. That gravity rule is a constitutive rule that tic-tac-toe does not have, so Connect Four is a claim game with restricted moves.
2. Simultaneous turns. With alternating face-up play, the second player sees the first card before choosing, so bluffing disappears and the second player gets a large advantage. You would likely need a rule to rotate who goes first.
3. Any three of: don't pull extra monsters without warning; don't take loot you can't use when others need it; don't leave mid-run without a reason; let the tank set the pace; wait for the healer to regain mana. Each is a social expectation, not code.
4. (a) Each number goes up by 1, so each triple sum goes up by 3, to 18. The winning sets are still exactly the 8 lines, so it is still tic-tac-toe. You only relabelled the items. (b) 2 is a corner. Against a corner opening, the only reply that does not lose with perfect play is the centre, so take 5. (5 is in 4 triples, more than any other number.) (c) Not automatically. A 4 × 4 magic square has rows, columns and both diagonals summing to 34, which gives 10 winning lines. But there are many more sets of four numbers from 1 to 16 that sum to 34, which are not lines. You would have to list all 4-number sets summing to 34 and compare them with the 10 lines. They do not match, so the games differ.

</details>

## Lab hook

**Lab 02, Formal elements teardown.** Write the formal-elements sheet for a public-domain card game, change exactly one element, and playtest both versions. Deliverable: two sheets, playtest notes and a comparison memo. See [labs/lab02.md](../labs/lab02.md).

## Sources

- Fullerton, T. (2018). *Game Design Workshop*, 4th ed. CRC Press, chapter 3. The eight formal elements.
- Salen, K. & Zimmerman, E. (2003). *Rules of Play*. MIT Press, "Rules on Three Levels". Operational, constitutive and implicit rules. Paraphrased.
- Schreiber, I. (2009). *Game Design Concepts*, "Level 3: Formal Elements of Games" (gamedesignconcepts.wordpress.com). Player structures, objective types, setup/progression/resolution, the tic-tac-toe and Three-to-Fifteen example, spawn camping as an implicit-rule dispute, Gauntlet vs DOOM, and the Puerto Rico theme example. Paraphrased.
- Wikipedia, "Number Scrabble" (accessed September 2026). Rules; isomorphism with tic-tac-toe via the magic square; Michon (1967) "JAM"; Simon, *The Sciences of the Artificial* (1969).
- Pokémon type triangle and Fire Emblem weapon triangle: as verified and cited in MMO303 week 9 (Pokémon Database "Pokémon type chart"; Fire Emblem Wiki "Weapon triangle", accessed September 2026).
- The counts in section 2 (8 triples summing to 15; 4, 3 and 2 triples per number; centre as the only safe reply to a corner opening) were computed by exhaustive enumeration for this lecture.

## Interactive spec: examples/w02-fifteen-game.html

**The one insight.** Three-to-Fifteen and tic-tac-toe are one game. The card view makes you do arithmetic; the board view shows the same threats as lines you can see at a glance.

**Layout.** Two linked panels. Panel A (cards) on the left or top; Panel B (board) on the right or below. On first load Panel B is collapsed behind a "Show the board" button so the student feels the difficulty first. Once shown, it stays visible (remember with a try/catch-wrapped `localStorage` flag).

**Panel A, the cards.** Nine cards labelled 1 to 9 in a row (3 × 3 wrap on mobile, but in numeric order, *not* magic-square order). Claimed cards move to a "You" tray or a "Computer" tray. Under the trays, a "Your live triples" list: every triple summing to 15 that contains none of the computer's numbers, showing how many of its numbers you already hold (for example "{2, 6, 7}: 2 of 3"). Same list for the computer, toggled by a checkbox "Show computer's threats" (off by default).

**Panel B, the board.** A 3 × 3 grid with the magic square:
```
2 7 6
9 5 1
4 3 8
```
Each cell shows its number small in a corner, and X (player) or O (computer) when claimed. When a live triple is highlighted in Panel A (hover or focus), its line is drawn on the board. A win draws the winning line thickly.

**Game logic.**
- Items 1 to 9. Winning sets are the 8 triples {1,5,9}, {1,6,8}, {2,4,9}, {2,5,8}, {2,6,7}, {3,4,8}, {3,5,7}, {4,5,6}.
- A player wins when they hold all three numbers of any winning set (they may hold more numbers).
- Player moves first by default; a toggle lets the computer move first.
- Computer difficulty selector: "Random" (uniform over free numbers), "Greedy" (win if possible, else block, else random), "Perfect" (minimax; among equally good moves, pick the number in the most triples, then the lowest number). Default "Greedy".

**Readouts.** "Triples containing each number" as a small bar strip under the cards: 5 → 4; 2, 4, 6, 8 → 3; 1, 3, 7, 9 → 2. Game record in both notations, for example "5 (centre), 1 (right edge), 2 (top-left corner)". Use position names: centre; top-left, top-right, bottom-left, bottom-right corners; top, bottom, left, right edges.

**Controls.** Card buttons (keyboard: Tab to a card, Enter to pick). Board cells are also clickable and pick the matching number. "New game", "Computer moves first" toggle, difficulty select, "Show the board", "Replay the lecture game" (steps through the lecture's step-4 game one move per click).

**Test values (must match exactly).**
- The 8 winning triples above; no other triple of distinct numbers from 1 to 9 sums to 15.
- Lecture game: A 5, B 1, A 2, B 8, A 6, then A holds {2, 5, 6} with two live triples {2, 6, 7} and {4, 5, 6}; whichever B blocks, A's next pick wins. Replay must show the fork with both lines highlighted after A's third pick.
- Perfect vs Perfect always ends in a draw. Perfect computer answering an opening of 2, 4, 6 or 8 takes 5.
- Perfect (with the tie-break above) moving first against Random wins exactly 97.40% of games in exact expectation (374/384). A hidden self-test run only when the URL has `?selftest` plays 1,000 simulated games and logs the win rate to the console; it should land between 95% and 99%.

**Accessibility and style.** X and O differ in shape, not only colour. Live-triple highlights also use a dashed outline. Keyboard reachable throughout; announce each move in an `aria-live` region ("You took 5, the centre"). Use `templates/interactive-tokens.css`. Respect `prefers-reduced-motion` (no card-flight animation).
