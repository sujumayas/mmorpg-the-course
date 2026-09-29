# GD101 · Week 05 — Player Experience Goals and the 8 Kinds of Fun

**Why this matters:** "Make it fun" is not a goal anyone can design toward or test against. This week gives you a sharper vocabulary for the feelings a game produces, and a way to turn one of those feelings into numbers you can tune. Every design document you write in this program starts with an experience goal, and every playtest checks one.

**You will be able to:**
- Describe a game's aesthetic profile with the eight MDA aesthetics, ranked by how much the game relies on each.
- Write a player experience goal that names a player, a feeling and an observable moment, and critique one that doesn't.
- Compute the challenge-to-skill ratio for a difficulty ramp and a learning curve, and classify each round as boredom, flow or anxiety.
- Compare fixed ramps, player-chosen difficulty and adaptive difficulty, and decide which fits a stated experience goal.

**Before class:** Hunicke, LeBlanc & Zubek (2004), "MDA: A Formal Approach to Game Design and Game Research," re-read the "Aesthetics" section. Fullerton, *Game Design Workshop* (4th ed.), chapter 1, the section on setting player experience goals. Optional: Jenova Chen, *Flow in Games* (MFA thesis, 2006), the sections "Flow as Fun" and "Expand the Flow Zone."

**Prerequisites from earlier courses:** [GD101 week 4, MDA](w04-mda-mechanics-dynamics-aesthetics.md). This week zooms into the A in MDA. The learning curve in section 3 uses repeated multiplication by a number below 1; [MA101 week 4](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) covers it properly, including decay.

**Interactive:** [The flow channel](../examples/w05-flow-channel.html). Use it during section 3.

---

## 1. Eight words instead of "fun"

Last week you saw that MDA calls the player's emotional response the game's **aesthetics**. The MDA paper argues that "fun" and "gameplay" are too vague to design with. It proposes a starter vocabulary of eight kinds of fun. Each is glossed as "game as" something. The glosses below are paraphrased.

| Aesthetic | Game as... | What the player is enjoying | A game that leans on it |
|---|---|---|---|
| Sensation | sense-pleasure | Sound, image, touch, rhythm | A rhythm game with a heavy beat and screen flash on every hit |
| Fantasy | make-believe | Being someone or somewhere else | A role-playing game where you play a knight |
| Narrative | drama | A story unfolding, tension and release | A mystery game where you uncover what happened |
| Challenge | obstacle course | Overcoming something hard | A platformer with a very demanding final level |
| Fellowship | social framework | Being with other people | Charades at a party, a cooperative raid |
| Discovery | uncharted territory | Finding out: places, secrets, how things work | An open-world game with hidden areas |
| Expression | self-discovery | Leaving your mark, making choices that say something about you | A character creator, a building game |
| Submission | pastime | Relaxing into something undemanding | Solitaire on a train, an idle game |

Three points about this list.

**It's a profile, not a label.** The paper describes four games this way. Charades is fellowship, expression and challenge. Quake is challenge, sensation, competition and fantasy. The Sims is discovery, fantasy, expression and narrative. Final Fantasy is fantasy, narrative, expression, discovery, challenge and submission. Every game pursues several aesthetics in different amounts. The paper notes that Charades puts fellowship ahead of challenge, and Quake puts challenge first. Order matters. Two games with the same set of aesthetics, ranked differently, are different games.

**It's open.** Look again at Quake's profile. "Competition" is not one of the eight. The authors reached outside their own list the moment it didn't fit, and the paper says the taxonomy is "not limited to" these words. Treat the eight as a checklist that stops you forgetting whole kinds of experience, not as a law. If you need "tension," "humor" or "competition," use them. Just define them.

**Submission is not an insult.** Students often skip it because it sounds passive. But a large share of real play is exactly this: a game you can do while half-listening to a podcast, one that asks little and gives a steady, pleasant rhythm back. Designing for submission means removing challenge on purpose. It is as deliberate as designing a hard boss.

### Other lists you will meet

MDA's eight are not the only taxonomy. In MMO301 week 8 you will study Richard Bartle's 1996 paper "Hearts, Clubs, Diamonds, Spades: Players Who Suit MUDs," which sorts players rather than feelings. Bartle's four types are achievers, explorers, socialisers and killers, placed on two axes: acting versus interacting, and players versus world. See [MMO301 week 8](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w08-player-types-bartle-1996-and-the-heros-journey.md). The two lists overlap. Bartle's explorers want discovery, and his socialisers want fellowship. The difference is that MDA describes what a game offers, while player-type models describe what a person seeks. You need both. A game rich in discovery will find the players who want it.

## 2. Player experience goals

A **player experience goal** is a short statement of what you want a player to feel or do during play. Fullerton introduces the idea early in *Game Design Workshop* and makes it the anchor of the whole iterative process. You set the goal before you design any features, and you check every prototype against it.

The contrast is with a **feature list**. "The game has crafting, a day-night cycle and four character classes" is a feature list. It says what you'll build. It says nothing about why, or how you'd know if it worked.

### A template

Use this form until you have a reason not to:

> **[Which players]** should feel **[aesthetic, in plain words]** when **[observable moment in play]**.

- "First-time players should feel clever when they discover that two tools combine, within the first ten minutes."
- "In a four-player game, every player should believe they can still win until the last three turns."
- "A player on a commute should be able to play one satisfying round in under five minutes and stop without losing progress."

Each has a who, a feeling and a moment you can watch for in a playtest. The second one should look familiar. It is the experience goal that Monopoly's feedback loop breaks, from week 4.

### Weak goals and how to fix them

| Weak goal | Problem | Stronger version |
|---|---|---|
| "The game should be fun." | No aesthetic, no player, no moment | "Players should laugh out loud at least once per round when a bluff is revealed." |
| "Combat should be deep." | "Deep" names no feeling; it hints at challenge and discovery | "After ten hours, a player should still be finding combinations they hadn't tried." |
| "The game should be balanced." | A property of dynamics, not a feeling (see week 4) | "Whichever character a new player picks, they should win about as often as they lose in their first five games." |
| "Players will love the crafting system." | Assumes a feature causes a feeling | "Players should feel ownership of an item they made, shown by naming it or refusing to sell it." |

### Goals conflict

Aesthetics compete for the same design space. Challenge and submission pull opposite ways. Fellowship and competition coexist uneasily in a four-player game where one player's win is everyone else's loss. Discovery fights with narrative when the story needs you to go somewhere and the map invites you to wander.

You can't maximize all of them. Pick the one or two your game will rank first, and let the others serve those. When two goals conflict in a playtest, the ranking decides which one gives way. That is the most useful thing an experience-goal statement does for a team: it settles arguments before they happen.

## 3. Worked example: one difficulty ramp, three players

Challenge is the aesthetic that designers most often try to tune with numbers, so it is the one we model. The model works for any game where difficulty rises over time.

### The hook

In NES Tetris (Nintendo, 1989), pieces fall faster as you level up. The game stores the speed as the number of video frames a piece waits before dropping one row. The NES runs at about 60.1 frames per second.

| Level | Frames per row | Rows per second | Time to fall the 20-row well |
|---|---|---|---|
| 0 | 48 | 1.25 | 16.0 s |
| 5 | 23 | 2.61 | 7.7 s |
| 9 | 6 | 10.0 | 2.0 s |
| 18 | 3 | 20.0 | 1.0 s |
| 19 to 28 | 2 | 30.0 | 0.67 s |
| 29 and up | 1 | 60.1 | 0.33 s |

From level 0 the game goes up one level every 10 lines. The start screen lets you pick level 0 to 9 directly, or 10 to 19 by holding a button. At the Classic Tetris World Championship, both players in a match start at level 18.

Think about what that means. The best players in the world skip the first 18 levels of the difficulty ramp. For a new player, level 5 is tense and level 9 is frightening. For a champion, levels 0 to 17 would be minutes of waiting. Same game, same ramp, and one player's challenge is another's chore. The ramp was never going to fit both, so the game lets players choose where to join it.

### The model

We need two curves and one ratio.

- **Skill** `S(n)` is what the player can handle after `n` rounds of play, on a 0 to 10 scale. People learn fast at first and then plateau. A simple curve with that shape is

```
S(n) = 10 − (10 − S0) × g^n
```

  `S0` is the starting skill (2 for a newcomer) and `g` is the learning factor, a number just below 1. Smaller `g` means faster learning. We use three learners: fast (`g = 0.8`), average (`g = 0.9`) and slow (`g = 0.95`). Each round, the gap to the ceiling of 10 shrinks by the factor `g`.

- **Challenge** `C(n)` is how hard round `n` is, on the same scale. This is the designer's ramp. Start with a straight line:

```
C(n) = 2 + 0.5n
```

- The **challenge ratio** is `R = C / S`. It compares demand with ability.

Psychologist Mihaly Csikszentmihalyi described **flow** as the state of full absorption that happens when a challenge matches a person's skill. Push the challenge well above skill and people become anxious; drop it well below and they become bored. Game designers call the region in between the **flow channel**. For this course we draw the channel with fixed edges:

| Ratio `R` | Zone |
|---|---|
| below 0.8 | Boredom |
| 0.8 to 1.25 | Flow |
| above 1.25 | Anxiety |

The edges 0.8 and 1.25 are our teaching choice, not measured constants. Real players differ, and the same player's channel moves with mood and fatigue. What matters is the shape of the argument, which holds for any band you pick.

### Numbers you can check

Newcomers (`S0 = 2`) playing the linear ramp. Compute `S` with a calculator. For the average learner at round 10, `0.9^10 = 0.349`, so `S = 10 − 8 × 0.349 = 7.21`.

| Round `n` | `C(n)` | Fast `S` | Fast `R` | Average `S` | Average `R` | Slow `S` | Slow `R` |
|---|---|---|---|---|---|---|---|
| 0 | 2.0 | 2.00 | 1.00 flow | 2.00 | 1.00 flow | 2.00 | 1.00 flow |
| 2 | 3.0 | 4.88 | 0.61 bored | 3.52 | 0.85 flow | 2.78 | 1.08 flow |
| 5 | 4.5 | 7.38 | 0.61 bored | 5.28 | 0.85 flow | 3.81 | 1.18 flow |
| 10 | 7.0 | 9.14 | 0.77 bored | 7.21 | 0.97 flow | 5.21 | 1.34 anxious |
| 15 | 9.5 | 9.72 | 0.98 flow | 8.35 | 1.14 flow | 6.29 | 1.51 anxious |
| 20 | 12.0 | 9.91 | 1.21 flow | 9.03 | 1.33 anxious | 7.13 | 1.68 anxious |
| 29 | 16.5 | 9.99 | 1.65 anxious | 9.62 | 1.71 anxious | 8.19 | 2.01 anxious |

The session is 30 rounds, numbered 0 to 29, so the last row is round 29. Count the rounds in each zone:

| Learner | Bored | Flow | Anxious |
|---|---|---|---|
| Fast (`g = 0.8`) | 10 | 11 | 9 |
| Average (`g = 0.9`) | 0 | 18 | 12 |
| Slow (`g = 0.95`) | 0 | 8 | 22 |

One ramp, three players, three different games. The fast learner is bored for the first third, then briefly happy, then overwhelmed once their skill plateaus below the still-rising ramp. The average learner, the one the ramp was implicitly tuned for, gets 18 good rounds and then hits the same wall. The slow learner is anxious for most of the session and is the player most likely to quit.

Two separate problems hide in this table.

1. **The ramp has the wrong shape.** Skill curves bend; a straight ramp doesn't. Any straight ramp eventually outruns a plateauing learner. Replace the ramp with the average learner's own curve, `C(n) = 10 − 8 × 0.9^n`, and the average learner spends all 30 rounds in flow. The fast learner gets 20 flow rounds and 10 bored; the slow one gets 10 flow and 20 anxious.
2. **Players differ.** Even a perfectly shaped ramp fits only the learner it was shaped for. Chen's thesis makes this point directly. Different people have different skills and different flow zones, so a single fixed curve can't keep everyone inside theirs.

### A visual you can move

Open [`examples/w05-flow-channel.html`](../examples/w05-flow-channel.html). It shows two linked views of the same session.

- **Left, over time.** `S(n)` and `C(n)` as two lines over 30 rounds. For most settings this looks reassuring: both lines go up, and they stay near each other.
- **Right, the flow channel.** Skill on the horizontal axis, challenge on the vertical, with the band between `R = 0.8` and `R = 1.25` shaded. Each round is a dot, and the dots are joined into a path. Here the same session can be seen leaving the band.

Switch the learner from average to fast and back. On the left, the lines barely change their look. On the right, the path swings from inside the band to below it. The time chart hides the ratio; the channel chart shows it. Then try the four ramp types: linear, shaped, adaptive, and adaptive with rhythm. Player-chosen difficulty is not a separate type. It is the start-level offset `k` on the linear ramp, which slides the player's entry point along the same line, as Tetris's level select does.

Set a returning expert (`S0 = 9`, `g = 0.9`) on the linear ramp. Twelve of their first 30 rounds are boring, with `R = 0.22` at round 0. Now set the start-level offset to 14, the Tetris answer. The first round sits at `R = 1.00`. The boredom disappears. But by round 5 the expert is at `R = 1.22` and climbing, because the ramp is still a straight line. Level select fixes where you join the ramp. It can't fix the ramp's shape.

### Cross-game recognition

Each of these is a different answer to "whose flow channel do we aim at?"

**NES Tetris (1989): pick your entry point.** One fixed ramp, with player-chosen start levels. It serves beginners and experts with the same code. At the top end it doesn't try to keep anyone comfortable. From level 29 pieces fall a row every frame and the original game never gets faster. Once top players learned to survive there, the championship changed the game code in 2023 so that pieces fall two rows per frame from level 39. Tetris's answer for very high skill is a wall that ends the game.

**flOw (Jenova Chen, Flash version, 2006): choose by playing.** Chen built flOw to test his thesis. The Flash version has 20 levels. Instead of finishing a level to unlock the next, you move deeper by eating one kind of food and back up by eating another, at any time. Dying pushes you back to the easier level above. Difficulty choice is built into the core action of swimming and eating, so players adjust without stopping to answer a menu. Chen had also built a simpler test, Traffic Light, that asked players between rounds whether they wanted it faster or slower. That extended play time, but he reports the frequent questions themselves broke the players' flow. Same goal, and the delivery made the difference.

**Left 4 Dead (Valve, 2008): the game measures you.** Valve's "AI Director," described by Michael Booth in a 2009 talk at the AIIDE conference, estimates an "emotional intensity" value for each survivor. It rises when a player takes damage, is incapacitated, is pulled off a ledge, or sees an infected die nearby. It decays over time, except while enemies are actively engaging. The Director then cycles through build-up (full threat population until intensity peaks), sustain peak (3 to 5 seconds more), peak fade and relax (minimal threats for 30 to 45 seconds), then builds up again. Note what this is not. It does not hold players at a comfortable ratio. It pushes them over the top on purpose, then lets them recover. That is flow plus narrative tension: rise, release, rise again.

**Celeste (2018): the player sets the dial, openly.** Celeste's Assist Mode lets you lower game speed to as little as 50%, in steps of 10%, alongside options such as infinite stamina and invincibility. Here the player sees the dial and chooses. Nothing is hidden.

Rewritten in our model, all four are different rules for `C(n)`.

| Game | Rule for challenge | Who controls it |
|---|---|---|
| NES Tetris | `C(n) = ramp(n + start level)` | Player, once per game |
| flOw | `C` moves up or down one level whenever the player chooses by eating; down on death | Player, continuously, inside play |
| Left 4 Dead | `C` follows measured intensity in a build-up and relax cycle | System, continuously, hidden |
| Celeste Assist Mode | `C` multiplied by a speed setting the player picks | Player, openly, from a menu |

GD203 week 13 turns difficulty settings into multipliers on time-to-kill and time-to-die. Read it when you get there; it is this model with combat numbers. See [GD203 week 13](../../GD203-combat-and-progression-design/lectures/w13-difficulty-modes-and-scaling.md).

### Eyes-open design judgment

- **The flow channel is a lens, not a law.** The band edges are ours, and skill is not a single number. Use the model to find the shape of a problem ("the ramp is straight and learning curves bend"), not to promise a percentage of flow.
- **Constant flow is flat.** In the interactive, an adaptive ramp that tracks skill exactly (`C = 1.1 × S`) scores 30 of 30 rounds in flow and is dull to watch. The "adaptive with rhythm" option cycles `R` through 0.9, 1.0, 1.1, 1.2, 1.3 every five rounds. It puts 6 of 30 rounds in the anxiety zone on purpose, which is roughly Left 4 Dead's idea. Tension needs peaks, and peaks sit outside the comfortable band.
- **Hidden adaptation can feel like cheating.** When a game quietly eases off because you're struggling, some players feel patronized once they notice, and good players may feel punished for doing well. This is the negative feedback loop from week 4 aimed at a single player. Tell players about it, or make it the player's choice.
- **Measuring skill is hard.** A system can only adapt to what it can observe: deaths, damage, time taken. Chen's thesis notes that a game has no direct reading of what the player is thinking. Adaptive systems misread a player who is deliberately taking risks, or one who is just distracted.
- **Challenge is one of eight.** A game aimed at submission wants `R` well below 1 on purpose. A cozy farming game that "fixes" its boredom zone by adding challenge has misread its own experience goal. Check the goal before you tune the ramp.

### Check yourself (worked example)

1. An average learner (`S0 = 2`, `g = 0.9`) plays a ramp `C(n) = 3 + 0.3n`. Compute `R` at rounds 0 and 20 and name the zone of each.
2. A designer wants a newcomer with `g = 0.85` to stay in flow at round 10 under the linear ramp `C = 2 + 0.5n`. Is the player in flow? If not, what constant challenge value at round 10 would give `R = 1`?
3. Your experience goal is "players should feel relaxed and in control, with no failure screens." Which of the four cross-game approaches would you start from, and what `R` range would you aim at?

<details>
<summary>Answers</summary>

1. Round 0: `S = 2`, `C = 3`, `R = 1.5`, anxiety. Round 20: `S = 10 − 8 × 0.9^20 = 10 − 8 × 0.122 = 9.03`, `C = 3 + 6 = 9`, `R = 1.00`, flow. The ramp starts too steep and then becomes about right.
2. `S(10) = 10 − 8 × 0.85^10 = 10 − 8 × 0.197 = 8.43`. `C(10) = 7`, `R = 0.83`, just inside flow. `R = 1` needs `C = 8.43`.
3. A player-controlled, visible approach such as Celeste's Assist Mode, or flOw's move-back-up choice, fits "in control." Aim below 1, for example `R` between 0.5 and 0.8. That is the model's boredom zone, which is correct here, because the goal is submission rather than challenge. Name the zone for your goal, not for the model's default.

</details>

## 4. From goal to test

An experience goal is only useful if a playtest can fail it. For each goal, write down in advance what you will watch for.

| Experience goal | Observable sign it's working | Observable sign it's failing |
|---|---|---|
| "Every player believes they can still win until the last three turns." | Trailing players still make risky plays near the end; nobody asks "can we just end it?" | Players concede, check phones, or ask how many turns are left |
| "First-time players feel clever when they discover a combination." | A player pauses, tries something, then reacts out loud | The player reads the rules sheet for the answer, or asks you |
| "One satisfying round in under five minutes." | Median round time under 5 minutes; players start another voluntarily | Rounds overrun; players stop after one |

The middle column is what you'll record in week 7's observation log. Notice that none of these signs is "the tester said it was fun." Players are unreliable reporters of their own feelings, and they are polite to designers. Behavior is harder to fake.

Numbers can join the list too. For a challenge goal, you can count failures per attempt, or the time a player takes on each round, and plot them against round number. That gives you a rough `R` curve from real play instead of from the model. MA102 week 12 covers how to summarize such playtest numbers without fooling yourself; see [MA102 week 12](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md).

## In-class activity (25 minutes)

Pairs. You need the aesthetics table from section 1, one game each of you knows well (any format) and the interactive, or a calculator.

1. **Profile (6 min).** Each of you ranks your game's top four aesthetics, most important first. Swap and rank your partner's game without looking at their list. Compare. Where you disagree, find the mechanic each of you was thinking of.
2. **Write the goal (6 min).** Write one experience goal for your game in the section 2 template. Your partner checks it has a who, a feeling and a moment.
3. **Tune a ramp (10 min).** Your game's challenge rises over time. Using the interactive or the formulas, find a linear ramp `C(n) = a + b·n` that keeps an average learner (`g = 0.9`, `S0 = 2`) in flow for at least 25 of 30 rounds. Then check the same ramp against a slow learner. Record both counts.
4. **Decide (3 min).** Say in one sentence which of the four approaches in the cross-game table your game should use, and why, citing your goal.

Expected output: two ranked profiles, one goal statement, your `a` and `b` with both flow counts, and the one-sentence decision.

## Common misconceptions

- **"A good game hits all eight aesthetics."** Profiles are rankings, and strong games commit. A game that tries to lead with all eight usually leads with none.
- **"Flow means easy enough to win."** Flow sits where challenge roughly matches skill. A player in flow is working hard and failing sometimes.
- **"Adaptive difficulty solves difficulty."** It fits the ratio for the player it measures, at the cost of flatness, measurement error and players' trust. It is one option with trade-offs, not an answer.
- **"The experience goal is whatever the players say they felt."** Goals are set by the designer before testing, then checked against behavior. What players say is one kind of evidence, and often the weakest.

## Check yourself

1. Rank the aesthetics for a cooperative board game in which players must pool cards to stop a spreading threat. Which two would you put first, and which mechanic supports each?
2. Rewrite this as a proper experience goal: "The boss fight should be epic."
3. A slow learner (`S0 = 2`, `g = 0.95`) plays the shaped ramp `C(n) = 10 − 8 × 0.9^n`. Compute `R` at round 10. Which zone, and what does that tell you about shaping a ramp to the average?
4. The "adaptive with rhythm" ramp sets `R` to 0.9, 1.0, 1.1, 1.2, 1.3, repeating. What fraction of rounds is in anxiety? Would you move the top value to 1.2 or 1.4 for a horror game, and why?

<details>
<summary>Answers</summary>

1. A reasonable profile is fellowship first (pooling cards forces talk and joint plans), then challenge (the spreading threat is the obstacle course). Discovery and narrative can follow. Any ranking is acceptable if each top aesthetic is tied to a mechanic.
2. For example: "Players who reach the boss with average gear should feel close to losing at least twice, and win on their second or third attempt." It names who, the feeling (tension, challenge) and observable moments (near-losses, attempt count).
3. `S(10) = 10 − 8 × 0.95^10 = 10 − 8 × 0.599 = 5.21`. `C(10) = 7.21`. `R = 1.38`, anxiety. A ramp shaped to the average learner still overwhelms a slower one, so you need a second tool (start level, assist, adaptation) for players far from the average.
4. One round in five is 1.3, above 1.25, so 20%. For horror, raising the peak to 1.4 makes the peaks sharper, which suits dread and relief, as long as the relax rounds really do let players recover. Lowering it to 1.2 would keep every round inside the band and remove the peaks the genre depends on.

</details>

## Lab hook

**Lab 05, experience goals and a difficulty ramp** ([labs/lab05.md](../labs/lab05.md)). You write an aesthetic profile and three experience goals for a game concept, fit a ramp to three learner types in a spreadsheet, and run a short timed test of a simple paper speed game to see real challenge ratios. Your goals carry into the week 6 paper prototype.

## Sources

- Hunicke, R., LeBlanc, M. & Zubek, R. (2004). "MDA: A Formal Approach to Game Design and Game Research." AAAI Workshop on Challenges in Game AI (AAAI 2004 workshop papers, WS-04-04; listed at aaai.org). The eight aesthetics and their "game as" glosses; the Charades, Quake, The Sims and Final Fantasy profiles (including "Competition" in Quake's); the statement that the taxonomy is "not limited to" the eight.
- Fullerton, T. *Game Design Workshop* (4th ed., CRC Press, 2018), chapter 1: player experience goals as the starting point of the playcentric process. Paraphrased.
- Bartle, R. (1996). "Hearts, Clubs, Diamonds, Spades: Players Who Suit MUDs." mud.co.uk/richard/hcds.htm. Four player types and the two axes.
- Csikszentmihalyi, M. (1990). *Flow: The Psychology of Optimal Experience.* Harper & Row. Flow as the match of challenge and skill, with anxiety and boredom on either side. Summary checked against Wikipedia, "Flow (psychology)."
- Chen, J. (2006). *Flow in Games.* MFA thesis, University of Southern California (jenovachen.com). A short version appeared as Chen, J. (2007), "Flow in games (and everything else)," *Communications of the ACM* 50(4), doi:10.1145/1232743.1232769. Different players have different flow zones; passive versus active difficulty adjustment; the Traffic Light test and its result; flOw's 20 levels in the Flash version, food choices that move you deeper or back, pushed back a level on death; presented at the GDC 2006 Experimental Gameplay Workshop.
- TetrisWiki, "Tetris (NES, Nintendo)." 1989 release; 60.0988 frames per second; frames per row by level (48, 43, 38, 33, 28, 23, 18, 13, 8, 6 for levels 0 to 9; 5 for 10 to 12; 4 for 13 to 15; 3 for 16 to 18; 2 for 19 to 28; 1 from 29); start-level selection 0 to 19; a level every 10 lines from level 0.
- Wikipedia, "Classic Tetris World Championship." Matches played on Type A starting at level 18; from 2023, modified game code doubles the fall speed at level 39.
- Booth, M. (2009). "The AI Systems of Left 4 Dead." Talk at the Artificial Intelligence and Interactive Digital Entertainment Conference (AIIDE 2009), Stanford University; venue per Valve's publications page (valvesoftware.com/en/publications). Valve slides (steamcdn-a.akamaihd.net). Survivor intensity rules, and the build-up, sustain peak (3 to 5 s), peak fade and relax (30 to 45 s) cycle.
- Celeste Wiki, "Assist Mode." Celeste (2018); game speed down to 50% in 10% steps; other assist options.
- The learning-curve and ramp model, band edges and all computed tables are this course's own.

## Interactive spec: examples/w05-flow-channel.html

**Purpose.** Show that a difficulty ramp that looks fine on a time chart can put one player in flow and another in boredom or anxiety, and that the fix depends on whether the problem is the ramp's shape or the spread between players. The insight on first load: *the two lines on the left staying close while the path on the right leaves the shaded band.*

**Layout.** Two panels side by side on desktop, stacked on mobile. Left: time chart. Right: flow-channel chart. Controls and a numbers panel below. A round slider scrubs both panels together and highlights round `n` in each.

**Model.**
- Skill: `S(n) = 10 − (10 − S0) × g^n`, `n = 0..29`. Controls: learner preset (fast `g = 0.8`, average `0.9`, slow `0.95`, custom `g` slider 0.70 to 0.99 step 0.01), `S0` slider 1 to 9 step 0.5, default 2.
- Challenge, by ramp type (select):
  - Linear: `C(n) = a + b × (n + k)`; `a` default 2 (0 to 6, step 0.5), `b` default 0.5 (0 to 1, step 0.05), start-level offset `k` default 0 (0 to 20, step 1).
  - Shaped: `C(n) = 10 − 8 × g_d^n`, with designer's `g_d` default 0.9 (0.70 to 0.99).
  - Adaptive: `C(n) = t × S(n)`, target `t` default 1.1 (0.5 to 1.5).
  - Adaptive with rhythm: `C(n) = S(n) × (0.9 + 0.4 × ((n mod 5) / 4))`.
- Ratio `R = C / S`. Zones: `R < 0.8` boredom, `0.8 ≤ R ≤ 1.25` flow, `R > 1.25` anxiety. Band edges adjustable in an "advanced" section (defaults 0.8 and 1.25).

**Left chart.** `S(n)` and `C(n)` against `n`, `y` from 0 to 20. Behind the lines, colour each round's column lightly by zone.

**Right chart.** `x` = skill 0 to 10, `y` = challenge 0 to 20. Shade the region between `y = 0.8x` and `y = 1.25x` as the flow band; label the areas above "anxiety" and below "boredom." Plot each round as a dot at `(S(n), C(n))`, joined in order, first dot hollow, last dot filled.

**Compare toggle.** "Show all three learners": draws the fast, average and slow paths together on the right chart (different colour and dot shape) and shows a zone-count row for each.

**Numbers panel.** For round `n`: `S`, `C`, `R`, zone. For the session: counts of bored, flow and anxious rounds (0 to 29), for the current learner and, with compare on, for all three.

**Test values** (rounds 0 to 29 counted).
- Linear defaults (`a = 2`, `b = 0.5`, `k = 0`), `S0 = 2`. Fast: 10 bored, 11 flow, 9 anxious. Average: 0, 18, 12. Slow: 0, 8, 22. Average at `n = 10`: `S = 7.21`, `C = 7.00`, `R = 0.97`.
- Shaped `g_d = 0.9`, `S0 = 2`: fast 10 bored / 20 flow; average 30 flow; slow 10 flow / 20 anxious.
- Adaptive `t = 1.1`: 30 flow for any learner.
- Adaptive with rhythm: 24 flow, 6 anxious for any learner; `R` sequence 0.9, 1.0, 1.1, 1.2, 1.3.
- Expert `S0 = 9`, `g = 0.9`, linear: `k = 0` gives 12 bored, 9 flow, 9 anxious and `R(0) = 0.22`; `k = 14` gives 0 bored, 6 flow, 24 anxious and `R(0) = 1.00`.

**Presets.** "One ramp, three players" (linear defaults, compare on), "Shape the ramp" (shaped), "Tetris level select" (expert, linear, `k = 14`), "Left 4 Dead rhythm" (adaptive with rhythm).

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Zones differ by colour and by pattern (hatching for anxiety, dots for boredom) so they read in greyscale. The three learners differ by colour and marker shape. All controls keyboard operable, with visible values. No Tetris pieces, logos or screenshots; draw only lines, dots and bands.
