# GD101 · Week 04 — MDA: Mechanics, Dynamics, Aesthetics

**Why this matters:** You only ever get to write rules. Players never experience your rules directly. They experience what the rules do once real people push on them, and they judge your game by how that feels. MDA is a way to trace a feeling ("this game drags") back to the rule that causes it, so you change the right thing.

**You will be able to:**
- Classify any element of a game as a mechanic, a dynamic or an aesthetic, and justify the choice with a one-line test.
- Compute how fast a lead grows under a simple reinvestment loop, using the growth factor `1 + 2r`.
- Predict the dynamic a proposed rule change will produce, then check the prediction with the week's simulation.
- Critique a fix for a runaway leader by naming which aesthetic it protects and which one it costs.

**Before class:** Hunicke, LeBlanc & Zubek, "MDA: A Formal Approach to Game Design and Game Research" (2004), all of it. It is five pages. Fullerton, *Game Design Workshop* (4th ed.), chapter 5, "Working with System Dynamics" (skim the sections on feedback loops).

**Prerequisites from earlier courses:** GD101 [week 2](w02-players-objectives-procedures-rules.md) and [week 3](w03-resources-conflict-boundaries-outcome.md), the formal elements (players, objectives, procedures, rules, resources, conflict, boundaries, outcome). This week turns that list into a causal chain. Growth by a constant factor is covered properly in [MA101 week 4](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md); you only need to multiply here.

**Interactive:** [Runaway leader simulator](../examples/w04-monopoly-feedback.html). Use it during section 2.

---

## 1. Three views of one game

In weeks 2 and 3 you learned to describe a game by listing its parts: its players, objectives, rules, resources and so on. A list of parts tells you what a game is made of. It does not tell you why one game with a plausible parts list is a joy and another with an equally plausible list is a chore. For that you need to follow cause and effect from the parts to the player.

The MDA framework does that. It was developed by Robin Hunicke, Marc LeBlanc and Robert Zubek, taught in the Game Design and Tuning Workshop at the Game Developers Conference from 2001 to 2004, and written up as a short paper in 2004. It splits a game into three layers.

- **Mechanics** are the rules and components, at the level of data and procedures. "Roll two dice and move that many squares." "A pistol holds 12 rounds." "You draw five cards at the start of your turn." A mechanic is something you could write down in a rulebook or in code before anyone plays.
- **Dynamics** are what the mechanics do at run time, when they act on player input and on each other over time. "Players hoard cards." "One player camps next to the respawn point." "The player in the lead pulls further ahead." A dynamic only exists while the game is being played.
- **Aesthetics** are the emotional responses the game evokes in the player. The paper deliberately avoids the word "fun" and offers a starter vocabulary of eight: sensation, fantasy, narrative, challenge, fellowship, discovery, expression and submission. Week 5 is about that list. For now, read "aesthetic" as "what it feels like to play."

The paper gives quick examples of the first link. The mechanics of card games include shuffling, trick-taking and betting, and from these a dynamic like bluffing emerges. Shooters have weapons, ammunition and spawn points, which sometimes produce camping and sniping. Nobody writes "bluff" into poker's rules. It appears because hidden cards and betting let it.

### Two directions

The layers are causally linked, and the direction you read them depends on who you are.

```
Designer:  Mechanics  →  Dynamics  →  Aesthetics
Player:    Aesthetics →  Dynamics  →  Mechanics
```

The designer can only touch mechanics. Every change you make enters at the left and has to travel through the dynamics before it reaches anyone's feelings. The player starts from the right. They feel tense, bored or clever first. They may notice the dynamic ("I always seem to be behind") and only rarely think about the mechanic that causes it.

This asymmetry is the practical point of MDA. Players report aesthetics. Playtesters say "the middle of the game drags," not "the rent schedule has a positive feedback loop." Your job is to translate their right-hand report into a left-hand change. And because the middle layer only exists in play, you usually cannot see a dynamic by reading your own rules. You have to run the game.

### A one-line test for each layer

Students often mislabel layers. Use these tests.

| Layer | Test | Example that passes | Example that fails |
|---|---|---|---|
| Mechanic | Could you write it down before anyone plays? | "Passing Go pays $200." | "The rich get richer." (You can't write that as a rule.) |
| Dynamic | Does it describe a pattern of play over time that only appears when people play? | "Players stop buying property late in the game." | "Properties cost money." (That's a mechanic.) |
| Aesthetic | Is it a feeling a player would report? | "I felt like I was out of the game by the halfway point." | "Players go bankrupt." (That's an event, a dynamic.) |

A common trap is the word "balance." "The game is balanced" is not an aesthetic. It is a claim about dynamics (no strategy dominates, several players stay competitive) that you hope produces an aesthetic (challenge, tension). Push vague words down to a layer before you act on them.

## 2. Worked example: Monopoly's runaway leader

### The hook

If you have played Monopoly to the end, you know the shape of the last hour. One player owns most of the board. Everyone else circles it, paying rent, mortgaging property to pay more rent, waiting to be eliminated. The winner was obvious long before the game was over. That hour is so familiar that the MDA paper uses it as its main example. The authors describe how, as the leaders get richer, they can penalize the others more and more effectively, and poorer players get poorer. Once the gap is wide, only one or two players are still really invested, and the paper says dramatic tension and agency are lost.

Here is the surprising part. Monopoly's ancestor was designed to do exactly this on purpose. Lizzie Magie patented The Landlord's Game in 1904 (US patent 748,626) to show how collecting rent on land enriches owners and impoverishes tenants. Her game shipped with two rule sets: a monopolist set where you win by bankrupting everyone, and an anti-monopolist set, later called Prosperity, that rewarded all players as wealth was created. The runaway leader was the lesson. Monopoly kept the monopolist rules and lost the lesson.

So the same dynamic produces an aesthetic one designer wanted (a lesson you feel in your wallet) and one the MDA authors call a flaw (a dead last hour). MDA helps you see both, and see which mechanic to touch.

### The model

Strip Monopoly down to the loop. Two players, A and B. Ignore the board for a moment and work with expected values, the average amounts per turn.

- `S` is the salary each player collects per turn on average from passing Go. We use `S = $10`.
- `L_A` and `L_B` are each player's **rent power**: the rent they expect to collect from the other player per turn. It grows when they build houses.
- `r` is the return on building. Every dollar spent on houses adds `r` dollars of rent power. We use "$50 of houses adds $1 of rent per turn," so `r = 1/50 = 0.02`.
- Each turn, a player's income is salary plus rent collected minus rent paid:

```
income_A = S + L_A − L_B
income_B = S + L_B − L_A
```

- Each player spends all positive income on houses, so rent power grows by `r × income`. If income is negative, the player pays it from cash. A player who can't pay is bankrupt.

Now look at the gap in rent power, `d = L_A − L_B`. In one turn, A's rent power grows by `r(S + d)` and B's by `r(S − d)`. Subtract:

```
d_next = d + r(S + d) − r(S − d)
       = d + 2rd
       = (1 + 2r) × d
```

That last line is the whole loop. **The gap grows by a constant factor every turn.** With `r = 0.02` the factor is 1.04, so the gap grows 4% per turn, compounding, and doubles about every 18 turns. Notice what dropped out: the salary `S`. Paying everyone the same salary does nothing to the gap. It raises both players equally and the difference is untouched.

The 2 in `2r` is also worth a look. The leader's extra rent comes out of the trailer's pocket. Every dollar of advantage counts twice, once as money the leader gains and once as money the trailer loses. That is what makes this a zero-sum loop, and why it is so much harsher than two players simply growing at different speeds.

### Numbers you can check

Start A with `L_A = 6` and B with `L_B = 4`. A got one extra property early from a lucky roll, worth $2 of rent per turn. Both players start with $40 in cash. While both players have positive income, `d(t) = 2 × 1.04^t`.

| Turn | `L_A` | `L_B` | Gap `d` | A's income | B's income | B's cash |
|---|---|---|---|---|---|---|
| 0 | 6.00 | 4.00 | 2.00 | 12.00 | 8.00 | 40.00 |
| 10 | 8.48 | 5.52 | 2.96 | 12.96 | 7.04 | 40.00 |
| 20 | 11.19 | 6.81 | 4.38 | 14.38 | 5.62 | 40.00 |
| 30 | 14.24 | 7.76 | 6.49 | 16.49 | 3.51 | 40.00 |
| 40 | 17.80 | 8.20 | 9.60 | 19.60 | 0.40 | 40.00 |
| 45 | 19.84 | 8.21 | 11.63 | 21.63 | −1.63 | 37.61 |
| 50 | 22.09 | 8.21 | 13.88 | 23.88 | −3.88 | 25.03 |
| 55 | 24.58 | 8.21 | 16.37 | 26.37 | −6.37 | 0.73 |

Check two cells by hand. At turn 20, `2 × 1.04^20 = 2 × 2.191 = 4.38`. The sum `L_A + L_B` at turn 20 is 18.00, which is the starting 10 plus `2rS × 20 = 0.4 × 20 = 8`. The total grows in a straight line while the gap grows exponentially.

Read the table as a story in three acts.

1. **Turns 0 to 40, the quiet act.** Both players are building. Both incomes are positive. B's income is shrinking (8, then 7, then 5.6), but B still feels like they are progressing. A $2 lead from one lucky roll is invisible at the table.
2. **Turn 42, the tipping point.** B's income reaches zero when `d = S`, that is when `2 × 1.04^t = 10`, so `1.04^t = 5` and `t = ln 5 / ln 1.04 ≈ 41.04`. The model moves in whole turns. At turn 41 B still earns one cent and builds a sliver. Turn 42 is the first turn B's income is negative. From here B can't build. (To solve `1.04^t = 5` for `t`, divide the two natural logarithms on a calculator, `ln 5 / ln 1.04`. That is a recipe for now. [MA101 week 5](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) explains why it works.) `L_B` freezes at 8.21 while A keeps growing.
3. **Turns 42 to 56, the dead act.** B pays out of savings every turn, faster and faster. B has 73 cents left at turn 55, owes $6.37 that turn, and is bankrupt at turn 56.

The winner was decided at turn 0 by a $2 difference, and certain by turn 42. The game ends at turn 56. Those last 14 turns are the hour the MDA paper describes.

### A visual you can move

Open [`examples/w04-monopoly-feedback.html`](../examples/w04-monopoly-feedback.html). It runs a four-player version of the loop on a small board with real dice (the spec at the end gives the exact rules). It shows two linked views.

- **Left, one game.** Each player's net worth over 50 rounds. It looks noisy and personal. Someone gets lucky, someone gets unlucky, and it feels like a story about dice.
- **Right, 500 games.** The average share of all wealth held by whoever is leading, and the average number of players still "in contention" (net worth at least half the leader's). This curve is smooth and relentless. The leader's share climbs from 25% to about 39% by round 10, 55% by round 25 and 64% by round 50. Contenders fall from 4 to about 1.8.

Click "new game" a few times on the left and the story changes every time. The right curve barely moves. That is the difference between a dynamic and an event. The dice decide who runs away with the game. The mechanics decide that someone will.

Then try the toggles, which are the fixes the MDA paper itself proposes, plus one it doesn't.

| Rule set (500 games, round 50) | Leader's share of wealth | Players in contention |
|---|---|---|
| Base game | 64% | 1.8 |
| Go tax 10%, shared equally | 56% | 2.1 |
| Go tax 25%, shared equally | 51% | 2.4 |
| Houses don't raise rent (loop cut) | 38% | 3.2 |
| All rent doubled | 97% | 1.1 |

### Cross-game recognition

Once you know the shape `gap_next = (1 + k) × gap`, you see it everywhere a resource buys more of the thing that makes the resource. Rewrite each case as "what is the stock, and what does it buy?"

**Risk (1993 Parker Brothers rules).** At the start of each turn you get armies equal to your territories divided by three, rounded down, with a minimum of 3. Holding a whole continent adds a fixed bonus printed on the board. Territories buy armies, and armies take territories. That is our loop with territories as rent power. Risk adds a second loop on top. Traded card sets are worth 4, 6, 8, 10, 12 and 15 armies, then 5 more for each set after that, counted across all players. The escalation pushes the game toward an end, the same job the MDA paper's "double all payouts" proposal does.

**Catan (Kosmos, first published 1995; rules as of the 2020 edition).** Settlements and cities produce resources, and resources build more settlements and cities. That is the loop again. Catan also ships two brakes. When a 7 is rolled, every player holding more than 7 resource cards discards half, rounded down, and the player who rolled moves the robber to block one hex and steals a card. The discard rule is a mechanic that taxes big hands. The robber is subtler. The rules don't say "put it on the leader," but players almost always do. The brake is a dynamic that the robber mechanic makes possible, with the players doing the targeting. That is MDA at its clearest: a negative feedback loop that nobody wrote down as a rule.

**The Landlord's Game, Prosperity rules (1904 and later).** Magie's second rule set is a fix of the kind the MDA paper proposes, designed 100 years earlier. It rewarded all players when wealth was created and ended the game when the poorest player had doubled their starting money. The victory condition itself tracks the trailer, not the leader.

**Racing games with catch-up items.** GD102 week 4 takes apart Mario Kart's item distribution, which gives better items to players further back. It is the mirror image of this week's loop, a negative feedback loop by race position. You will build both loops as systems diagrams in GD102 [week 3, positive feedback](../../GD102-systems-design-and-game-mechanics/lectures/w03-positive-feedback-loops-snowballing.md) and [week 4, negative feedback](../../GD102-systems-design-and-game-mechanics/lectures/w04-negative-feedback-loops-rubber-banding.md).

Four games, one question. What does the leader's advantage buy, and does it buy more advantage?

### Eyes-open design judgment

A positive feedback loop is not a bug. It is one of the few tools that makes a game end. Without Monopoly's loop, nobody would ever go bankrupt and the game would never finish. The table shows this directly: with houses that don't raise rent, 3.2 of 4 players are still in contention at round 50. That is a game that goes nowhere. The question is never "loop or no loop." It is **how long is the gap between the moment the outcome is decided and the moment the game ends?** In our two-player model that gap is 14 turns out of 56. Every fix is a way to shorten it.

- **Help the trailer or tax the leader.** The MDA paper suggests subsidies for poor players and taxes on rich ones, collected when crossing Go, leaving jail or owning monopolies above some value. In the two-player model, if the leader hands back a fraction `τ` of the gap each turn, the growth factor becomes `1 + 2r(1 − τ)`. At `τ = 0.5` the gap after 50 turns is 5.38 instead of 13.88. At `τ = 1` it never grows at all. The cost is the one the paper warns about. Complex tax calculations make it harder for players to track their standing, so they feel less invested. A tax you can't compute at the table buys fairness with confusion.
- **Cut the loop.** Make building give something other than rent. The game becomes fair and endless. You have traded a dead last hour for no last hour.
- **Speed the loop up.** The paper also suggests doubling payouts on monopolies so players separate faster. In the simulation this pushes the leader to 97% of the wealth by round 50. This is a real option. A short, decisive game can be better than a long, fair one. It is the choice a lot of modern board games make: let the snowball roll, but make the whole game 45 minutes.
- **Hand the brake to the players.** Catan's robber lets the table gang up on the leader. It costs nothing in rules complexity. It can feel unfair to the leader and produces "kingmaking," where a player who can't win decides who does.
- **Decide what the loop is for.** Magie wanted the loop, because the aesthetic she was after was understanding. The MDA paper notes that fixing Monopoly might hurt its ability to model real monopoly practice, and adds that reality isn't always fun. Before you tune a loop away, write down the aesthetic you want. Only then do you know whether the loop is a flaw.

### Check yourself (worked example)

1. In the two-player model, change `r` to 0.05 and keep everything else. What is the growth factor of the gap? About how many turns until B's income reaches zero?
2. A designer doubles the salary to `S = $20` "to keep the poorer player in the game." Using the formula for `d_next`, what happens to the gap? What does happen to the tipping-point turn, and why?
3. In the simulation, cutting the loop gives 3.2 contenders at round 50 and doubling rent gives 1.1. Which would you ship for a 30-minute game night, and which aesthetic are you choosing?

<details>
<summary>Answers</summary>

1. Factor `1 + 2 × 0.05 = 1.10`. B's income hits zero when `2 × 1.1^t = 10`, so `1.1^t = 5`, `t = ln 5 / ln 1.1 ≈ 16.9`, about turn 17.
2. The gap is unchanged, because `S` cancels in `d_next = (1 + 2r)d`. The tipping point moves later, because B's income is `S − d` and now reaches zero at `d = 20`: `1.04^t = 10`, `t ≈ 58.7`. Salary delays the collapse; it does not slow the snowball.
3. There is no single right answer, but you must name the trade. Doubling rent gives a short game that is decided fast (challenge and a clear winner, at the cost of tension late on). Cutting the loop keeps everyone in (fellowship, less frustration) but the game may never end, so it needs a new end condition such as a fixed number of rounds.

</details>

## 3. Naming dynamics well

Most of the work in MDA happens in the middle layer, and the middle layer is where students are vaguest. "The game is unbalanced" and "it gets boring" are not dynamics. A good dynamic statement has three parts: **who** does **what**, **when** or under what condition.

- Weak: "Snowballing."
- Better: "The player who completes the first color group usually wins." (A playtest log would let you put a number on "usually.")
- Best: "Once one player's rent income exceeds everyone else's salary, the others stop building and only pay rent. This happens around the midpoint of the game."

The best version points straight at mechanics you could change (rent income, salary) and at a moment in play you could observe. When you playtest in week 7, you will write dynamics in this form in your observation log.

### Feedback: the most important dynamic family

The MDA paper uses a thermostat to explain feedback. A thermostat measures the room and turns the heater on when it's too cold and off when it's too hot. It pushes the system back toward a target. That is **negative feedback**: the further you get from the target, the harder the system pushes you back. A **positive feedback loop** is the reverse: the further you get ahead, the harder the system pushes you further ahead.

In games:

- **Positive feedback** ("snowballing") makes leads grow. It ends games and rewards early success. It is dangerous when it decides the winner long before the end.
- **Negative feedback** ("rubber-banding" or "catch-up") shrinks leads. It keeps games close and keeps everyone invested. It is dangerous when it makes early play meaningless or punishes skill.

Almost every competitive game has both, and the balance between them sets how long games last and how late they are decided. GD102 spends two whole weeks on this. For GD101, the skill is to spot a loop by asking "what does being ahead let you do?"

### Mechanics hide in content too

The paper counts content (levels, assets, the specific cards in a deck) as part of what supports dynamics, alongside mechanics. The dice rule "roll 2d6" is a mechanic. The placement of Monopoly's properties is content. They interact: the paper points out that a model of two six-sided dice lets you work out how long it takes to get around the board, and that the same model lets you predict how a change to board size would lengthen or shorten a game. When you look for the cause of a dynamic, check the numbers and layout as well as the rules.

## 4. Using MDA in both directions

### Designer direction: start from the feeling you want

The paper's advice is to start with aesthetics even though you can only build mechanics. Write the target feeling first ("every player should believe they can still win until the last few turns"). Then write the dynamic that would produce it ("leads change hands at least twice per game"). Only then pick mechanics that should produce that dynamic, and test whether they do. The paper calls this experience-driven design, as opposed to feature-driven design, which starts from "wouldn't it be cool if there were a stock market?"

### Player direction: work backward from a report

When a tester says "I was bored after the first 20 minutes," climb down the layers.

1. **Aesthetic reported:** boredom, loss of challenge.
2. **Dynamic that could cause it:** the outcome was decided, or the tester had no meaningful choices, or the same turn repeated.
3. **Mechanics that could cause that dynamic:** a positive feedback loop, a dominant strategy, a rule that removes choices once you're behind.

Only the third step gives you something to change. You usually need to observe play to know which dynamic is at work. That is the bridge to week 7.

### What MDA does not do

MDA is a lens, and the paper presents it as such. It does not tell you which aesthetics to want. Its list of eight is a vocabulary, explicitly "not limited to" those eight. It says little about story, art or sound as sources of feeling, although those plainly shape the experience. It treats the player as a single person, while in multiplayer games a large part of the experience comes from the other people at the table. And it gives you no numbers. The numbers come from models like the one in section 2, and from playtests. Use MDA to decide where to look and models to decide how much.

## In-class activity (25 minutes)

Work in groups of three. You need one board or card game the instructor provides (Uno, Monopoly Deal, Catan or similar) and a sheet of paper.

1. **Decompose (8 min).** Draw three columns: M, D, A. List at least five mechanics, three dynamics and two aesthetics. Every dynamic must be written in the "who does what, when" form from section 3. Draw an arrow from each dynamic back to at least one mechanic.
2. **Find the loop (5 min).** Ask "what does being ahead let you do?" Write the loop as "more X buys more Y, which buys more X." Is it positive or negative feedback?
3. **Propose one change (7 min).** Change exactly one mechanic to shorten the gap between "decided" and "ended." Predict, in one sentence each, the new dynamic and the aesthetic it produces. Also predict one aesthetic you might lose.
4. **Swap (5 min).** Give your change to another group. They name the likeliest unintended dynamic.

Expected output: one sheet with the three columns, the loop sentence, the change, two predictions and the other group's objection. Keep it; lab 04 asks you to test a change like this.

## Common misconceptions

- **"Dynamics are just complicated mechanics."** A mechanic is written before play; a dynamic appears only during play. "Rent doubles on a full color group" is a mechanic. "Players refuse to trade the last property of a group" is a dynamic that mechanic creates.
- **"Positive feedback is bad design."** It is the most common way games end. The design question is how early it decides the winner, not whether it exists.
- **"Giving everyone more money helps the player who's behind."** A flat bonus to everyone leaves the gap untouched, as `S` cancels in the model. It only delays the moment the trailer runs dry. Catch-up has to be conditional on being behind.
- **"Aesthetics means graphics."** In MDA, aesthetics means the player's emotional response. A text-only game has aesthetics.

## Check yourself

1. Classify each as M, D or A, and give the test you used: (a) "A turn lasts 30 seconds." (b) "Players rush to claim the corners." (c) "I felt clever when my trap worked." (d) "Players who fall behind stop trading."
2. A two-player game uses the section 2 model with `r = 0.01`. The trailer starts 3 behind in rent power. How big is the gap after 50 turns? After 100?
3. A designer adds "the player with the least money collects double salary." Write the new income equations for A (leader) and B (trailer) in the model, with salary `S`. Does the gap still grow by a constant factor?
4. A tester says "the end of the game felt pointless." Walk the report down the three layers and name two different mechanics that could be responsible.

<details>
<summary>Answers</summary>

1. (a) M, written before play. (b) D, a pattern that appears only when people play (it comes from mechanics that make corners valuable). (c) A, a feeling a player reports (challenge, maybe expression). (d) D, a pattern over time, likely caused by a feedback loop.
2. Factor `1 + 2 × 0.01 = 1.02`. After 50 turns `3 × 1.02^50 = 3 × 2.692 = 8.08`. After 100 turns `3 × 7.245 = 21.7`, as long as the trailer's income stays positive.
3. `income_A = S + L_A − L_B` and `income_B = 2S + L_B − L_A`. Then `d_next = d + r(S + d) − r(2S − d) = (1 + 2r)d − rS`. The gap still grows by `(1 + 2r)` but now loses `rS` every turn, so a small gap shrinks and a large gap still grows. The break-even gap is `d = S/2`. Conditional catch-up bends the loop at small gaps only.
4. Aesthetic: loss of tension or agency. Dynamic: the outcome was already decided, so the remaining turns had no meaningful choices. Candidate mechanics: a positive feedback loop such as rent that grows with investment, and an end condition such as "last player standing" that keeps a decided game running. You could also name a rule that removes a trailing player's options, such as forced mortgaging.

</details>

## Lab hook

**Lab 04, Mini-opoly: find and fix a runaway leader** ([labs/lab04.md](../labs/lab04.md)). You play a 20-minute paper version of the section 2 loop, record when each game was decided and when it ended, then rebuild the two-player model in a spreadsheet and test one fix of your own. Deliverable: the sheet, your play log and a one-page MDA memo.

## Sources

- Hunicke, R., LeBlanc, M. & Zubek, R. (2004). "MDA: A Formal Approach to Game Design and Game Research." Proceedings of the AAAI Workshop on Challenges in Game AI (AAAI 2004 workshop papers, WS-04-04; venue checked on aaai.org). Paper version read from the authors' PDF (users.cs.northwestern.edu/~hunicke/MDA.pdf). Source of the three definitions, the designer and player directions, the eight aesthetics, the card game and shooter examples, the thermostat figure, the 2d6 board-length point and the Monopoly analysis and proposed fixes (subsidies, taxes at Go or jail, a constant-rate tax, doubling monopoly payouts). Paraphrased; the phrase "reality isn't always fun" is shortened from the paper.
- Hasbro, *Monopoly* rules (rules sheet © 2004, 2007). $1,500 starting money, $200 salary for passing Go, double rent on unimproved properties of a complete color group, and that Free Parking pays nothing under the official rules.
- Wikipedia, "The Landlord's Game." Elizabeth Magie, US patent 748,626 (1904); a second patent granted 1924; monopolist and anti-monopolist ("Prosperity") rule sets, with Prosperity won when the poorest player doubles their starting money.
- Parker Brothers, *Risk* rules (rules © 1959 to 1993). Armies equal territories divided by three, minimum 3; continent bonuses; card sets worth 4, 6, 8, 10, 12, 15, then +5 each.
- CATAN GmbH, *Catan* base game rules (2020 edition, catan.com). A 7 makes players with more than 7 resource cards discard half, rounded down; the robber blocks a hex and steals one card. Wikipedia, "Catan," for the 1995 Kosmos first publication.
- The Mini-opoly model and all simulation figures in section 2 are this course's own and are reproducible from the spec below.

## Interactive spec: examples/w04-monopoly-feedback.html

**Purpose.** Make it obvious that a single game looks like a story about dice, while the average over many games shows a steady, rule-driven climb in the leader's share. The insight on first load: *the noisy single game on the left next to the smooth rising curve on the right, with the "decided vs ended" gap marked.*

**Layout.** Two linked panels side by side on desktop (single game left, 500-game aggregate right), stacked on mobile. Below them a rules panel with toggles and a numbers panel. A third tab, "Two-player model," shows the deterministic table from section 2.

**PRNG.** mulberry32, seeded per game. Implementation (must match exactly so test values reproduce):

```
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;}}
```

Die roll: `1 + Math.floor(rnd() * 6)`. A turn rolls two dice, first die first.

**Board game rules (defaults).**
- 4 players, 50 rounds. Each round, players 0, 1, 2, 3 take turns in order; bankrupt players are skipped.
- Board of 24 squares, indices 0 to 23. Squares 0, 6, 12, 18 are safe (no effect). The other 20 are lots.
- Start: $300 cash each, all at square 0, no lots owned.
- Move by the 2d6 sum. If the new position is ≥ 24, collect salary $20 (then apply Go tax if on), and wrap the position mod 24.
- Landing on an unowned lot: buy it for $60 if cash ≥ 60.
- Landing on another player's lot: rent = (base $6 + $10 × houses on that lot) × rent multiplier. If "houses raise rent" is off, rent = $6 × multiplier. If cash ≥ rent, pay the owner. Otherwise pay all remaining cash to the owner, become bankrupt (net worth 0), and all your lots, with their houses, transfer to that owner.
- After resolving the landing, if not bankrupt, build: while cash ≥ $100 reserve + $50 house cost and you own a lot with fewer than 4 houses, add one house to your lot with the fewest houses (ties to the lowest square index) and pay $50.
- Go tax (if on, rate τ): after collecting salary, pay `τ × cash` into a pot. At the end of each round, split the pot equally among surviving players.
- Net worth = cash + $60 per lot owned + $50 per house owned. Bankrupt players have net worth 0.

**Left panel (one game).** Line chart of each player's net worth, rounds 0 to 50 (51 points). Players differ by colour and by line dash. "New game" button increments the seed (default seed 1). Mark with a vertical line the round from which the eventual round-50 leader stays leader to the end ("decided"), and label round 50 "ended."

**Right panel (aggregate).** Games with seeds 1 to 500 (a control lets the viewer pick 100, 500 or 1,000). Two series over rounds 0 to 50: mean leader share (max net worth / total net worth; left axis, 0 to 100%), and mean players in contention (net worth ≥ 50% of the leader's; right axis, 0 to 4). When a toggle changes, draw the base-game curve as a faint ghost so the change is visible.

**Controls.** Go tax slider (0%, 5%, 10%, 15%, 20%, 25%); "houses raise rent" toggle (default on); rent multiplier (×1, ×2); salary stepper ($0 to $60, step 10, default 20); presets "Base," "MDA subsidy (Go tax 10%)," "Cut the loop," "MDA speed-up (double rent)." All keyboard operable. Recompute on change; 500 games of 50 rounds must finish in well under a second.

**Numbers panel.** At rounds 10, 25 and 50: mean leader share and mean contenders. Percentage of games with at least one bankruptcy. For the single game: each player's net worth at the selected round (a round slider scrubs both panels).

**Two-player model tab.** Inputs `S` (default 10), `r` (0.02), `L_A` (6), `L_B` (4), starting cash (40), leader hand-back `τ` (0 to 1, default 0). Each turn: `inA = S + L_A − L_B − τ(L_A − L_B)`, `inB = S + L_B − L_A + τ(L_A − L_B)`; a player with positive income adds `r × income` to L, otherwise adds income to cash; stop when a cash value goes below 0. Show a chart of `L_A`, `L_B` and gap `d`, plus the table at turns 0, 10, 20, 30, 40, 45, 50, 55. Mark the tipping point (first turn B's income ≤ 0) and the bankruptcy turn.

**Test values.**
- Two-player, defaults: `d(20) = 4.38`, `d(40) = 9.60`, B's income first negative at turn 42, B's cash at turn 50 = 25.03, B's cash first below zero at turn 56 (bankruptcy).
- Two-player, `τ = 0.5`: `d(50) = 5.38`, no bankruptcy by turn 60.
- Board game, seed 1, base rules, net worth by player at round 10: 406, 320, 0, 674; at round 50: 662, 392, 0, 1006.
- Board game, seeds 1 to 500, base rules: mean leader share 0.391 / 0.554 / 0.639 at rounds 10 / 25 / 50; contenders 3.09 / 2.14 / 1.78; 85.2% of games have a bankruptcy.
- Go tax 10%: leader share at round 50 = 0.564, contenders 2.09. Go tax 25%: 0.512, 2.36. Houses don't raise rent: 0.379, 3.24. Double rent: 0.967, 1.06.
- Allow ±0.01 on aggregate values if floating-point order differs; the seed-1 values must match exactly.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Player series differ by colour and dash pattern. No Monopoly board art, token shapes, logos or property names; plain squares and generic labels ("Player 1"). Respect reduced motion (no animated replays unless the viewer presses play).
