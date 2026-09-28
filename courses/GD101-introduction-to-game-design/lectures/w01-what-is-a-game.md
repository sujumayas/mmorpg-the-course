# GD101 · Week 01 — What is a game? Definitions from Suits, Salen & Zimmerman and Juul

**Why this matters:** Every design meeting eventually hits the question "but is it still a game?" A definition turns that argument into a list of parts you can check, add or remove on purpose. This week you learn three well-known definitions and use them as tools rather than as rulings.

**You will be able to:**
- State the definitions of Suits, Salen & Zimmerman and Juul, and name the parts each one requires.
- Classify an activity under each definition by filling in a feature checklist, and count where the definitions agree and disagree.
- Design a game out of a non-game activity by adding the specific features it is missing.
- Critique a claim such as "sandbox games aren't real games" by naming the exact feature it depends on.

**Before class:** Fullerton, *Game Design Workshop* (4th ed., 2018), chapters 1 and 2. Salen & Zimmerman, *Rules of Play* (2003), chapter 7, "Defining Games". Jesper Juul, "The Game, the Player, the World: Looking for a Heart of Gameness" (2003), sections 1 to 3 (about 10 pages, free on the author's site).

**Prerequisites from earlier courses:** None. This is a first-semester course. You only need to have played games.

**Interactive:** [Definition tester](../examples/w01-definition-tester.html). Keep it open during section 2.

---

## 1. Three definitions, and why designers bother

You already know what a game is, in the sense that you can point at chess and say "game" and point at a tax return and say "not a game". The trouble starts at the edges. Is a slot machine a game? Is building a castle in Minecraft's Creative mode a game? Is a round of tic-tac-toe between two people who both know the perfect strategy still a game?

These are not trivia questions. When you design, you remove and add parts all the time. If you take away the win condition, you need to know what else might break. A definition gives you a list of parts. The list is the useful bit.

Philosophers have warned that the list will never be perfect. Ludwig Wittgenstein, in *Philosophical Investigations* (published 1953), used "game" as his main example of a word with no single shared feature. Board games, ball games, card games and ring games overlap the way members of a family resemble each other: some share a nose, some share a chin, none share everything. He called this **family resemblance**. Keep that warning in mind. The three definitions below are useful because they are precise, and they will each fail somewhere because they are precise.

### Suits: the voluntary attempt to overcome unnecessary obstacles

Bernard Suits was a philosopher. In *The Grasshopper: Games, Life and Utopia* (1978) he summed up playing a game as a voluntary attempt to overcome unnecessary obstacles. The longer version has four parts:

- **Prelusory goal.** A state of affairs you try to reach, describable before the game exists. In golf, "the ball is in the hole".
- **Lusory means.** The ways of reaching the goal that the rules allow. In golf, hitting the ball with a club.
- **Constitutive rules.** The rules that forbid the more efficient ways. In golf, you may not walk over and drop the ball in the hole.
- **Lusory attitude.** You accept those rules because they make the activity possible, not because anything outside the game forces you to.

"Lusory" comes from the Latin *ludus*, game. The striking part of Suits's definition is the inefficiency. A game is defined by what it forbids. The rules deliberately make the goal harder to reach, and the players agree to that.

### Salen & Zimmerman: a system of artificial conflict with a quantifiable outcome

Katie Salen and Eric Zimmerman, both designers and teachers, compared eight earlier definitions in *Rules of Play* (2003, chapter 7) and wrote their own. Paraphrased, a game is a system in which players engage in an artificial conflict, defined by rules, that produces a quantifiable outcome. The parts:

- **System.** A set of parts that affect each other. Change one, and others move.
- **Players.** People who actively take part.
- **Artificial.** The game is separate from ordinary life in time and space. A lost game of Risk does not cost you a country.
- **Conflict.** A contest of powers, against other players or against the system.
- **Rules.** Limits on what players can do.
- **Quantifiable outcome.** At the end, someone won or lost, or got a score. The book's phrase is "quantifiable outcome", and it is the part that most often throws things out.

### Juul: the classic game model

Jesper Juul, a game researcher, took seven definitions (Huizinga, Caillois, Suits, Avedon & Sutton-Smith, Crawford, Kelley, and Salen & Zimmerman) and pulled out the features they shared. His 2003 paper lists six features of what he calls the **classic game model**:

1. **Rules.** Fixed and well defined enough that you do not argue them during play.
2. **Variable, quantifiable outcome.** Different plays can end differently, and the ending can be measured.
3. **Value assigned to possible outcomes.** Some outcomes are better than others. Winning beats losing.
4. **Player effort.** What the player does changes the outcome.
5. **Player attached to outcome.** The player feels good winning and bad losing.
6. **Negotiable consequences.** Whether the game has real-life consequences is up to the players. You can play poker for money or for matchsticks.

Juul then sorted activities into three groups. Games have all six. **Borderline cases** have most: open-ended simulations such as SimCity and The Sims (no outcome is marked as better), games of pure chance (effort does not matter), gambling, and pen-and-paper role-playing with a game master who can change the rules. **Not games** miss something basic: free-form play, hypertext fiction, a circle game like ring-a-ring o' roses (the ending is always the same), and traffic or war, which have rules and stakes but whose consequences you cannot opt out of.

Juul's model is the most useful of the three for design because each feature is a separate switch. You can ask of any activity "which of the six does it have?" and get six answers instead of one yes-or-no verdict.

## 2. Worked example: is it a game? Three definitions as checklists

### The hook

Minecraft is the best-selling video game of all time. In October 2023 it became the first game to pass 300 million copies sold. Its Creative mode gives you unlimited blocks, lets you fly, and has no win condition at all. Under Juul's model, Creative mode is not a game. It sits with SimCity in the borderline group, and arguably below it. Yet nobody at a store would shelve Minecraft next to the LEGO bricks.

Either the definition is wrong, or "game" means something narrower than "thing sold as a video game". The worked example settles which, with a table you can check line by line.

### The model

Turn each definition into a **feature vector**: a row of yes/no answers to the same questions. Use Juul's six features, F1 to F6, plus one extra column that only Suits needs:

- **F1** Rules.
- **F2** Variable, quantifiable outcome.
- **F3** Some outcomes valued above others (a goal).
- **F4** Player effort affects the outcome.
- **F5** Player attached to the outcome.
- **F6** Negotiable consequences (the activity is voluntary and separable from real life).
- **S** The rules forbid a more efficient way to the goal (Suits's inefficiency).

Each definition then becomes a set of required columns. This mapping is our reading, a simplification for class use, and you should argue with it:

| Definition | Required features |
|---|---|
| Suits (1978) | F1, F3, F4, F6, S |
| Salen & Zimmerman (2003) | F1, F2, F3, F6 |
| Juul (2003) | F1, F2, F3, F4, F5, F6 |

The reasoning: Suits needs a goal (F3), an attempt (F4), rules (F1), voluntary acceptance (F6) and inefficient means (S), but never says the outcome must be measurable. Salen & Zimmerman need rules, an artificial conflict (F6), and a quantifiable outcome (F2, which implies F3), but do not require that effort decides the result. Juul needs all six.

An activity counts as a game under a definition if it has **every** required feature. One missing feature is enough to fail.

### Numbers you can check

Here are ten activities scored against the seven columns. A 1 means the feature is present, a 0 means it is absent.

| # | Activity | F1 | F2 | F3 | F4 | F5 | F6 | S | Juul features (of 6) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Chess | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 6 |
| 2 | A World of Warcraft raid boss attempt | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 6 |
| 3 | Snakes and Ladders, no stakes | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 5 |
| 4 | Roulette for real money | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 4 |
| 5 | Driving to work in traffic | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 5 |
| 6 | Minecraft Creative, free building | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 3 |
| 7 | Minecraft Creative, "build a castle without flying" | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 5 |
| 8 | Minecraft Survival, aiming to defeat the Ender Dragon | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 6 |
| 9 | Ring-a-ring o' roses | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 2 |
| 10 | Tic-tac-toe between two experts | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 6 |

A few scoring notes, so you can check the judgment calls:

- Row 3. In Snakes and Ladders every move is set by the die. Your effort changes nothing (F4 = 0), but the rules still forbid moving your token straight to square 100 (S = 1).
- Row 4. Real money means you cannot opt out of the consequences once you bet (F6 = 0). Juul lists gambling as borderline for this reason.
- Row 5. Traffic has rules, outcomes you care about, and effort that matters. The rules do not make the trip harder on purpose (S = 0), and you cannot declare "it's only a game" after a crash (F6 = 0). Juul uses traffic as his example of a rule system that is not a game.
- Row 7. The player added a goal and a rule that forbids the efficient means (flying). Nothing in the game measures when the castle is "done", so F2 stays 0.
- Row 10. Formally, the outcome can vary: someone could blunder. In practice two experts always draw. Hold that thought.

Now apply the definitions. A row passes if it has a 1 in every required column.

| # | Activity | Suits | Salen & Zimmerman | Juul |
|---|---|---|---|---|
| 1 | Chess | game | game | game |
| 2 | WoW raid attempt | game | game | game |
| 3 | Snakes and Ladders | not (F4) | game | not (F4) |
| 4 | Roulette for money | not (F4, F6) | not (F6) | not (F4, F6) |
| 5 | Traffic | not (F6, S) | not (F6) | not (F6) |
| 6 | Minecraft Creative, free | not | not (F2, F3) | not |
| 7 | Creative castle challenge | game | not (F2) | not (F2) |
| 8 | Minecraft Survival | game | game | game |
| 9 | Ring-a-ring o' roses | not | not (F2, F3) | not |
| 10 | Expert tic-tac-toe | game | game | game |
| | **Total "game"** | **5** | **5** | **4** |

Count the agreement. All three definitions give the same verdict on 8 of the 10 rows. They disagree on exactly two:

- **Snakes and Ladders** is a game for Salen & Zimmerman and not for the other two, because they alone do not require player effort.
- **The castle challenge** is a game for Suits and not for the other two, because Suits alone does not require a measurable outcome. A self-imposed rule and a self-chosen goal are enough for him.

And the hook resolves cleanly. Free-building in Creative (row 6) fails all three. Survival mode with the dragon as a target (row 8) passes all three. Minecraft is two activities in one box: a toy and a game. Players move between them, and the castle challenge (row 7) shows the exact moment a player turns the toy into a game by adding a goal and a rule.

### A visual you can move

Open [`examples/w01-definition-tester.html`](../examples/w01-definition-tester.html). The left panel is the feature grid above. The right panel shows each definition as a column of chips, one chip per activity, lit when that activity passes.

Do two things. First, click the F2 header to stop requiring a quantifiable outcome in all three definitions. Watch the Minecraft castle challenge light up under Salen & Zimmerman. Second, flip row 10's F2 cell to 0, arguing that two experts always draw so the outcome no longer varies. Tic-tac-toe drops out of Juul and Salen & Zimmerman, and stays in for Suits.

The insight to take away: **almost every argument about whether something is a game is an argument about one column.** Usually it is F2 (is there a measurable outcome?), F4 (does effort matter?) or F6 (can I walk away?). Name the column and the argument gets short.

### Cross-game recognition

The same checklist works on any game. Two cases where the designers or players flipped a single column on purpose:

**Old School RuneScape, Ironman mode (released 13 October 2014).** An Ironman account is locked out of trading, the Grand Exchange market and most group activities. Everything you own, you gathered yourself. In our vector, nothing changes in F1 to F6. What changes is S. The developers built extra "unnecessary obstacles" into an official mode, forbidding the efficient route of buying what you need. Every Ironman player chose this at account creation. That is Suits's lusory attitude, shipped as a menu option. The Hardcore variant goes further: one unsafe death and the account becomes a regular Ironman and its HiScores entry is locked.

**Super Mario Bros. (NES, 1985).** The game has 8 worlds of 4 levels, 32 levels in total. Warp Zones in World 1-2 and World 4-2 let you skip ahead, and the one in 4-2 reached by a beanstalk goes straight to World 8. The shortest route plays 1-1, 1-2, 4-1, 4-2 and 8-1 to 8-4, which is 8 levels. A player who decides "no warps" has added a constitutive rule that makes the goal four times longer, 32 levels instead of 8. In vector form, S goes from "set by the designer" to "set by the player", and every other column stays the same.

**Traffic, again, as a design move.** Juul's traffic example fails only F6. Games that simulate driving put it back: in a racing game a crash costs you a position, not your car. Turning a rule system into a game can mean nothing more than making the consequences negotiable.

Three cases, one tool. When you meet a new activity, write the seven-column row first. Then ask which column is in dispute.

### Eyes-open design judgment

Definitions are strong design tools and weak gatekeepers.

- **Use them to find missing parts.** If playtesters drift away from your prototype, check the vector. No valued outcome (F3)? They have nothing to aim at. No effort that matters (F4)? They feel like spectators. This is a faster diagnosis than "it isn't fun".
- **Remove a feature on purpose, not by accident.** Sandbox games, cozy games and many MMO social spaces drop F2 and F3 deliberately. That is a design choice with costs. Without a goal, players need to bring their own, as in the castle challenge. Some will, many won't. MMOs usually solve this by offering many small goals (quests, raid bosses, achievements) inside a world that itself has no final outcome.
- **Do not use a definition to dismiss work.** "Walking simulators aren't games" is a claim about F4 or F2 dressed up as a claim about quality. Juul himself files well-loved things as borderline. Borderline is a description, not a grade.
- **Remember what the checklist cannot see.** Expert tic-tac-toe passes every definition in its formal version, yet adults stop playing it. The definitions describe structure. They say nothing about whether the choices inside the structure are still interesting. That gap is the subject of the tic-tac-toe game tree in [week 9, choice and meaningful decisions](w09-choice-and-meaningful-decisions.md).

### Check the model

1. Using the required-feature table, does a game of Monopoly played for no stakes pass Suits, Salen & Zimmerman and Juul? Fill in its seven-column row first.
2. Poker for money fails F6. Poker for matchsticks passes it. What changed, and which definitions change their verdict?
3. Find the one column you would change to move row 6 (free building) into Suits's definition, and say what rule a player might add. Is one column enough?

Answers are in the Check yourself section.

## 3. What each definition leaves out

Every definition makes choices about where to draw the line. Knowing the choices helps you pick the right tool for a question.

**Suits leaves out measurement.** A goal you set yourself, with rules you set yourself, is enough. That makes Suits the best definition for player-made games: speedrun rules, "no-hit" challenges, the castle challenge. It also means Suits says nothing about whether the designer built in a way to know who won.

**Salen & Zimmerman leave out effort.** Pure chance games pass, as long as there is a conflict and a result. That fits the everyday use of the word: people call Snakes and Ladders and bingo games. It also means their definition cannot, by itself, separate a game of skill from a lottery. For a designer that is a big difference, and you will return to it when the course reaches chance and skill.

**Juul leaves out nothing from the classic model, and pays for it.** Requiring all six features makes the definition strict. Many modern video games (open worlds, life simulations, narrative games) fall into his borderline group. Juul says this is intended. His paper argues that video games often break the classic model on purpose, and that the borderline cases are where much of the interesting design happens.

**All three leave out fun.** None of the definitions says a game must be enjoyable, fair or interesting. That is on purpose. A definition tells you what an activity is. Whether it is good is a design question, and the rest of this course is about answering it.

A fourth view is worth knowing even though it is not on the reading list. Johan Huizinga, a Dutch historian, argued in *Homo Ludens* (1938) that play happens inside a space marked off from ordinary life, with its own rules. Salen & Zimmerman later named this space the **magic circle**. You will use that idea in week 3, when the course reaches boundaries.

## 4. From definition to design: making a non-game into a game

The most practical use of the checklist is generative. Pick an activity that fails, find the missing columns, and add them one at a time. Each addition is a design decision.

Take bouncing a ball against a wall. Its row is F1 = 0, F2 = 0, F3 = 0, F4 = 1, F5 = 0, F6 = 1, S = 0.

1. **Add a goal (F3).** "Keep the ball going." Now some states are better than others.
2. **Add a measurable outcome (F2).** "Count consecutive bounces." Now each attempt ends with a number.
3. **Add a rule that forbids the easy way (F1 and S).** "The ball must hit the wall above the chalk line, and bounce once on the ground before you catch it." Now the obstacle is unnecessary and chosen.
4. **Attachment (F5)** tends to follow on its own once there is a number to beat. Add a second player with alternating turns, and the count becomes a contest between you.

Notice that each step changed how people behave. After step 2 they care about the count. After step 3 they aim, which is a skill. The definition did not tell you which rule to add. It told you which kind of rule was missing. That is the pattern for the whole course: frameworks point at the gap, and you fill it with judgment and playtesting.

## In-class activity (25 min)

**Definition court.** Groups of three. Materials: the ten-row table printed on A3, a pack of sticky notes, and the interactive on one laptop.

1. (5 min) Each group receives two activities from this list: a Sudoku puzzle, a Tamagotchi, fantasy football, a treasure hunt at a birthday party, Wordle, a flight simulator in free-flight mode, a crossword with the answers on the back page, an MMO player who logs in only to chat in the capital city.
2. (10 min) Score each one in the seven columns. Where the group disagrees on a cell, write both arguments on a sticky note.
3. (5 min) Apply the three definitions. Record the verdicts and the column that decided each "not".
4. (5 min) Each group presents one disputed cell to the class in under a minute. The class votes. The lecturer tallies which columns caused the most disputes across all groups.

**Expected output:** two scored rows per group, and a class tally. Expect F2 and F4 to cause most disputes. If they do, that is the lesson.

## Common misconceptions

- **"A definition of games tells you what makes games good."** It tells you what makes something a game. Expert tic-tac-toe passes every definition here and is still boring. Quality is a separate question.
- **"If a famous game fails a definition, the definition is wrong."** Sometimes. More often the game has deliberately dropped a feature, as Minecraft Creative drops the outcome. The failure tells you which feature.
- **"Chance games aren't games."** Under Juul, pure chance is borderline because effort does not matter. Under Salen & Zimmerman it is a game. State which definition you mean.
- **"Suits says games are about difficulty."** Suits says the obstacles are unnecessary and accepted voluntarily. A trivial game with a silly rule still fits. Difficulty is a tuning choice, not part of the definition.

## Check yourself

1. A friend proposes "Hot lava": you must cross the living room without touching the floor. Score it in the seven columns and state its verdict under each definition. Which single rule would you add to make it pass Salen & Zimmerman?
2. A mobile game gives you a reward every day you log in, whatever you do. Which of Juul's six features does the log-in reward lack? Is the reward loop a game under Juul's model?
3. In the table, two rows split the definitions. Invent a third activity that Suits and Juul call a game but Salen & Zimmerman do not, or explain why no such activity exists given the required-feature table.
4. Answer the three "Check the model" questions in section 2.

<details>
<summary>Answers</summary>

1. Row: F1 1, F2 0, F3 1, F4 1, F5 1, F6 1, S 1. Suits: game (all of F1, F3, F4, F6, S present). Salen & Zimmerman: not, F2 is missing. Juul: not, F2 is missing. Add a measurable outcome, for example "fastest time wins" or "touching the floor means you are out, last player standing wins". That sets F2 = 1 and it passes all three.
2. It lacks F4, player effort, since the reward arrives whatever you do. It also has only one outcome per day, so F2 is weak. Under Juul it is not a game. It is a reward schedule attached to a game.
3. No such activity exists under this mapping. Juul requires every feature Salen & Zimmerman require (F1, F2, F3, F6), so anything that passes Juul also passes Salen & Zimmerman. An activity that splits them the other way (S&Z yes, Juul no) is possible, and Snakes and Ladders is one.
4. (a) Monopoly for no stakes: F1 to F6 all 1 (dice decide a lot, but buying, trading and building are choices, so effort matters), and S = 1 (you may not simply take money from the bank). It passes all three. (b) Only F6 changed. Salen & Zimmerman and Juul flip from "not" to "game". Suits also needs F6, so he flips too, provided the other columns hold. (c) Row 6 lacks F3 and S for Suits. One column is not enough. The player must add a goal (F3) and a rule that forbids the easy means (S), for example "build a working castle gate using only blocks found in a 50-block radius, no flying". That is two additions, as in the castle challenge row.

</details>

## Lab hook

**Lab 01, Make it a game.** Start from a non-game activity, add Juul's missing features one at a time, and playtest each version. Deliverable: four scored versions, playtest notes and a 300-word reflection. See [labs/lab01.md](../labs/lab01.md).

## Sources

- Suits, B. (1978). *The Grasshopper: Games, Life and Utopia*. University of Toronto Press. Definition and the four elements (prelusory goal, lusory means, constitutive rules, lusory attitude), as summarized in Wikipedia, "Bernard Suits" (accessed September 2026). Paraphrased.
- Salen, K. & Zimmerman, E. (2003). *Rules of Play: Game Design Fundamentals*. MIT Press, chapter 7, "Defining Games". Definition wording checked against Wikipedia, "Game" (accessed September 2026); the lecture quotes only the phrase "quantifiable outcome".
- Juul, J. (2003). "The Game, the Player, the World: Looking for a Heart of Gameness." *Level Up: Digital Games Research Conference Proceedings*, Utrecht University. Six features, the seven definitions compared, and the borderline and non-game examples (SimCity, The Sims, pure chance, gambling, pen-and-paper RPGs, traffic, war, ring-a-ring o' roses). Online at jesperjuul.net.
- Wittgenstein, L. (1953). *Philosophical Investigations*. Family resemblance and "game", as summarized in Wikipedia, "Game" (accessed September 2026).
- Huizinga, J. (1938). *Homo Ludens*. Origin of the magic circle idea; Wikipedia, "Magic circle (games)" (accessed September 2026).
- Gerken, T. (16 October 2023). "Minecraft becomes first video game to hit 300m sales." BBC News. Sales figure and best-selling status as of that date. Wikipedia, "Minecraft" (accessed September 2026), gives a higher current total but cites the October 2023 reports for it, so the lecture uses the dated figure.
- Wikipedia, "Minecraft" (accessed September 2026). Creative mode has no win condition; Survival can be "finished" by defeating the Ender Dragon, after which play continues.
- Old School RuneScape Wiki, "Ironman Mode" (accessed September 2026). Released 13 October 2014; trading, Grand Exchange and most group activities restricted; Hardcore Ironman loses status on an unsafe death.
- Wikipedia, "Super Mario Bros." and Super Mario Wiki, "Warp Zone" (accessed September 2026). 8 worlds of 4 levels (NES, 1985); Warp Zones in World 1-2 (to 2, 3, 4) and World 4-2 (to 5, and via beanstalk to 6, 7, 8).
- Fullerton, T. (2018). *Game Design Workshop*, 4th ed. CRC Press, chapter 1 ("The Role of the Game Designer") and chapter 2 ("The Structure of Games"). Chapter numbers and titles checked against the publisher's chapter DOIs (10.1201/b22309-11 to -28).

## Interactive spec: examples/w01-definition-tester.html

**The one insight.** Almost every "is it a game?" argument is about one feature column. Flip one column and whole groups of activities move in or out of a definition.

**Layout.** Two linked panels, side by side on desktop (grid left, verdicts right), stacked on mobile (verdicts first, so the first screen shows the result).

**Panel A, the feature grid.** Ten rows (activities, exactly as in the lecture table, same order and short labels) by seven columns F1, F2, F3, F4, F5, F6, S. Each cell is a toggle button showing 1 or 0, with a filled or hollow square. Column headers are buttons with full names as tooltips and visible labels on desktop ("F2 · measurable outcome"). A last column shows "Juul features: n/6", recomputed live. A "Reset to lecture values" button restores the default table.

Default cell values (rows 1 to 10, columns F1 F2 F3 F4 F5 F6 S):
```
1 Chess                         1 1 1 1 1 1 1
2 WoW raid attempt              1 1 1 1 1 1 1
3 Snakes and Ladders            1 1 1 0 1 1 1
4 Roulette for money            1 1 1 0 1 0 1
5 Traffic                       1 1 1 1 1 0 0
6 Minecraft Creative, free      1 0 0 1 0 1 0
7 Creative castle challenge     1 0 1 1 1 1 1
8 Minecraft Survival (dragon)   1 1 1 1 1 1 1
9 Ring-a-ring o' roses          1 0 0 0 0 1 0
10 Expert tic-tac-toe           1 1 1 1 1 1 1
```

**Panel B, the verdicts.** Three columns: Suits, Salen & Zimmerman, Juul. Each column lists all ten activities as chips. A chip is lit ("game") if the row has 1 in every required feature of that definition, otherwise dim, with the missing feature codes printed on it ("not: F2"). Under each column, show "Games: n of 10". Above the panel, show "All three agree on n of 10 activities" and list the disputed rows.

Required features (defaults):
- Suits: F1, F3, F4, F6, S
- Salen & Zimmerman: F1, F2, F3, F6
- Juul: F1, F2, F3, F4, F5, F6

**Controls.**
- Cell toggles (Panel A), keyboard: arrow keys move focus in the grid, Space or Enter toggles.
- "Edit definitions" disclosure: a 3 × 7 checkbox matrix to change which features each definition requires. Changing it recolours Panel B immediately.
- Clicking a column header in Panel A toggles that feature's requirement in all three definitions at once (a shortcut for the lecture's F2 exercise). Show a small banner "F2 no longer required" while active.
- "Add activity" button: adds an eleventh editable row with a text label (max one extra row).

**Test values (must match exactly).**

| State | Suits games | S&Z games | Juul games | Agree on |
|---|---|---|---|---|
| Default | 5 (rows 1, 2, 7, 8, 10) | 5 (rows 1, 2, 3, 8, 10) | 4 (rows 1, 2, 8, 10) | 8 of 10 (disputed: 3, 7) |
| F2 requirement removed from all | 5 | 6 (adds row 7) | 5 (adds row 7) | 9 of 10 (disputed: 3) |
| Default, then row 10 F2 set to 0 | 5 | 4 | 3 | 7 of 10 (disputed: 3, 7, 10) |
| Default, then row 4 F6 set to 1 | 5 | 6 (adds row 4) | 4 | 7 of 10 (disputed: 3, 4, 7) |

Row 6 shows "Juul features: 3/6" by default; row 9 shows "2/6".

**Accessibility and style.** Lit and dim chips differ in lightness and have a text label ("game" / "not: F2"), never colour alone. Use the shared tokens from `templates/interactive-tokens.css`. No game logos or art; activities are text only. Respect `prefers-reduced-motion` (no chip transition animations when set).
