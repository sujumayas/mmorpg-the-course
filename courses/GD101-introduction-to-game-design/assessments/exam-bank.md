# GD101 · Exam bank

GD101 has no written exam. The grade comes from the paper prototype (40%), three playtest reports (30%), the analysis essay (20%) and participation (10%). This bank exists for three other uses.

- **Weekly quizzes.** Tutors draw two or three questions from the week just taught for a 10-minute check at the start of the lab. Quiz completion counts toward participation (see [participation-brief.md](participation-brief.md)). The score itself is feedback, not a grade.
- **Practice.** Students can work through any week before starting its lab. Every numeric answer has a full working so you can find where your method went wrong.
- **Viva at the showcase.** In week 15 each team gets a five-minute viva as part of the paper prototype mark (see [paper-prototype-brief.md](paper-prototype-brief.md)). The assessor picks two questions tagged "apply", swaps the question's example for the team's own prototype, and asks the team to answer about their game. The viva prompts at the end of this file show the pattern.

**How to read the tags.** Each question starts with `[Weeks · type · mode]`.

- Type is one of **compute** (produce a number with a lecture model), **explain** (state and use a concept), **design** (propose a rule or artifact that meets a stated goal) or **critique** (judge someone else's claim, design or report).
- Mode is **apply** when the question gives a case the lectures did not work through, so you must carry a model or framework to it. Mode is **recall** when the question checks a definition or result from the lecture itself. 57 of the 60 questions are apply.

The games in the questions are either invented for this bank or are games the lectures already discuss, used only with the facts the lectures cite. All numbers were recomputed for this bank.

**Coverage.**

| Week | Topic | Questions |
|---|---|---|
| 1 | What is a game? | 1 to 4 |
| 2 | Players, objectives, procedures, rules | 5 to 8 |
| 3 | Resources, conflict, boundaries, outcome | 9 to 13 |
| 4 | MDA | 14 to 17 |
| 5 | Experience goals and kinds of fun | 18 to 21 |
| 6 | Paper prototyping | 22 to 25 |
| 7 | Playtesting | 26 to 30 |
| 8 | Iteration and kill-your-darlings | 31 to 34 |
| 9 | Choice and meaningful decisions | 35 to 39 |
| 10 | Chance and skill | 40 to 43 |
| 11 | Dominant strategies | 44 to 47 |
| 12 | Feedback, juice, readability | 48 to 51 |
| 13 | Genres as clusters of mechanics | 52 to 54 |
| 14 | One-pagers and pitch | 55 to 57 |
| Several | Integrated cases | 58 to 60 |

---

## Week 1 · What is a game?

Lecture: [w01-what-is-a-game.md](../lectures/w01-what-is-a-game.md)

1. **[1 · explain · recall]** Using the lecture's feature columns (F1 rules, F2 variable measurable outcome, F3 valued outcomes, F4 effort matters, F5 attachment, F6 negotiable consequences, S rules forbid the efficient route), list the features each of the three definitions requires. Which definition is the only one that does not require F2, and which is the only one that does not require F4?

   <details>
   <summary>Answer</summary>

   Suits requires F1, F3, F4, F6 and S. Salen & Zimmerman require F1, F2, F3 and F6. Juul requires F1 to F6.

   Suits is the only one without F2, which is why a self-set challenge with no measured result (the Minecraft castle challenge) passes Suits and fails the other two. Salen & Zimmerman is the only one without F4, which is why Snakes and Ladders passes Salen & Zimmerman and fails the other two.

   </details>

2. **[1 · compute · apply]** A scratch card bought for real money shows six hidden boxes. You scratch them all, and if three show the same symbol you win that prize. (a) Score the scratch card in the seven columns and give the verdict under each definition, naming the missing features. (b) A teacher runs the same cards in class, paid for with matchsticks. Which column changes, and which verdicts change?

   <details>
   <summary>Answer</summary>

   (a) F1 = 1 (fixed rules for what wins). F2 = 1 (you win a prize or nothing, and prizes differ). F3 = 1 (winning beats losing). F4 = 0 (nothing you do changes the symbols). F5 = 1 (people care). F6 = 0 (real money is at stake and you cannot opt out of the loss once bought). S = 0 (there is no more efficient route that the rules forbid you; the card is simply revealed).

   - Suits: not a game, missing F4, F6 and S.
   - Salen & Zimmerman: not a game, missing F6.
   - Juul: not a game, missing F4 and F6.

   (b) Only F6 changes, to 1, because matchstick stakes are negotiable. Salen & Zimmerman now call it a game. Juul still does not (F4 is missing), and Suits still does not (F4 and S). The class version is a pure-chance game in the Salen & Zimmerman sense, like Snakes and Ladders, and a borderline case for Juul.

   </details>

3. **[1 · design · apply]** Waiting in a supermarket queue fails all three definitions. Design the smallest set of rules that turns it into an activity two friends can play that passes Suits, Salen & Zimmerman and Juul. Add the missing columns one at a time and name each column as you add it.

   <details>
   <summary>Answer</summary>

   Start row: F1 0, F2 0, F3 0, F4 0, F5 0, F6 1, S 0. One workable sequence:

   1. F3, a goal. "Guess which of the two queues next to ours will reach the till first."
   2. F2, a measurable outcome. "One point per correct guess; first to 3 points wins."
   3. F1 and S, a rule that forbids the easy route. "You must lock your guess before either queue moves, and you may not count items in the baskets." Without the second clause you could compute the answer, which removes the obstacle.
   4. F4, effort that matters. Reading the queues (number of people, a cashier who is fast) now changes your chance of a correct guess. This comes from step 3 leaving some information to judge.
   5. F5 tends to follow once there is a score and a rival.

   Check: F1 to F6 and S all equal 1, so it passes all three. Other answers are fine if each step names its column and the final row has every column at 1. A common error is to add a goal with no measurable result, which passes Suits only.

   </details>

4. **[1 · critique · apply]** A forum post says "Cozy farming games with no way to lose aren't real games." Rewrite the claim as a claim about one or two feature columns, say which definitions agree with it, and explain what the claim gets wrong as a design judgment.

   <details>
   <summary>Answer</summary>

   "No way to lose" is a claim about F2 (no variable measurable outcome) and possibly F3 (no outcome valued above another). Under Juul and Salen & Zimmerman, an activity with F2 = 0 is not a game, so the claim matches those definitions for free play. Under Suits, if the player sets a goal (a full harvest by the first winter) and a rule, it can still be a game.

   The design error is to treat "not a game under Juul" as a verdict on quality. Juul files well-loved activities as borderline on purpose. Removing F2 and F3 is a deliberate choice that costs something (players must bring their own goals) and buys something (submission, expression). The critique should ask whether the farming game gives players enough small goals, not whether it deserves the word "game".

   </details>

## Week 2 · Players, objectives, procedures, rules

Lecture: [w02-players-objectives-procedures-rules.md](../lectures/w02-players-objectives-procedures-rules.md)

5. **[2 · compute · apply]** Take the lecture's magic square (2 7 6 / 9 5 1 / 4 3 8) and double every number, so the items are 2, 4, 6, ..., 18. Players alternately pick numbers and win by holding three that sum to a target. What target makes this game tic-tac-toe? Prove that no triple outside the eight lines reaches it.

   <details>
   <summary>Answer</summary>

   Every line sums to 15 before doubling, so it sums to 30 after. The target is 30.

   Proof that the winning sets still match: any three distinct numbers from {2, 4, ..., 18} are 2a, 2b, 2c for distinct a, b, c in 1 to 9. Their sum is 30 exactly when a + b + c = 15. The lecture showed there are exactly 8 such triples and they are the 8 lines. So the doubled game has exactly 8 winning sets, one per line, and it is tic-tac-toe with the items relabelled. Only the operational rules changed.

   </details>

6. **[2 · explain · apply]** Write rock-paper-scissors at the three rule levels: operational, constitutive and implicit. Then name the implicit rule whose breaking turns it into a turn-based game, and say which player then always wins.

   <details>
   <summary>Answer</summary>

   - Operational: "On the count of three, both players show rock (fist), paper (flat hand) or scissors (two fingers). Rock beats scissors, scissors beats paper, paper beats rock. Same shape is a draw."
   - Constitutive: three items A, B, C. Each player picks one without seeing the other's pick. A beats B, B beats C, C beats A; equal picks draw.
   - Implicit: "Throw at the same moment. Do not delay to see the other hand." Others: do not change your hand after it is shown; best of three unless agreed.

   The "throw at the same moment" rule is what makes the sequencing simultaneous. A player who delays turns it into a turn-based game, and the second player always wins because they see the first pick and choose the item that beats it (lecture section 3).

   </details>

7. **[2 · design · apply]** An invented party game has five players. One is secretly a traitor. The other four must find the traitor within five rounds of discussion and voting. (a) Name the player structure using the lecture's table. (b) Predict one dynamic that comes from the structure alone, not from any rule. (c) The designer changes it to a free-for-all where each player has a secret personal target. Predict how the discussion changes.

   <details>
   <summary>Answer</summary>

   (a) One against many, with the "one" hidden. It resembles Scotland Yard's structure, with secrecy added.

   (b) Any dynamic that follows from the structure. For example, loyal players who speak most confidently steer the vote, the co-op "quarterback" problem the lecture names. Or the traitor copies the most trusted player's opinions to hide.

   (c) In a free-for-all, nobody shares a goal, so the group has no reason to pool information. Expect less open discussion, more private deals and more targeting of whoever looks ahead, the free-for-all behaviour the lecture predicts (the leader gets attacked, players hide strength). The same actions (talk, vote) produce a different game because one formal element changed.

   </details>

8. **[2 · critique · apply]** Two versions of an invented puzzle game share every state, move and win condition. In version A the winning sets are drawn as lines on a grid. In version B they are listed as a column of number sums on a card. Testers find B much harder, and the lead designer concludes "B needs simpler rules". Critique this conclusion using the week 2 ideas.

   <details>
   <summary>Answer</summary>

   The constitutive rules are identical, so there are no "simpler rules" to find. The difference is representation, Herbert Simon's point from the Three-to-Fifteen example. Version A lets the eye find threats; version B makes players redo arithmetic every turn, so it tests memory rather than strategy.

   The right move is to decide which difficulty the game wants. If it wants strategy, change the presentation (draw the board, or print the sums as visible groups). If it wants the "aha" of discovering the hidden structure, keep B and accept that some players will quit before they see it. Either way the rules stay.

   </details>

## Week 3 · Resources, conflict, boundaries, outcome

Lecture: [w03-resources-conflict-boundaries-outcome.md](../lectures/w03-resources-conflict-boundaries-outcome.md)

9. **[3 · compute · apply]** A run has 3 stages. Each attempt clears a stage with probability `p = 0.7`. Using `W(n, L) = p × W(n − 1, L) + (1 − p) × W(n, L − 1)`, build the table by hand for `n` from 0 to 3 and `L` from 0 to 2, and give `W(3, 2)`.

   <details>
   <summary>Answer</summary>

   Edges: `W(0, L) = 1`, `W(n, 0) = 0`.

   | n \ L | 0 | 1 | 2 |
   |---|---|---|---|
   | 0 | 1 | 1 | 1 |
   | 1 | 0 | 0.7 | 0.91 |
   | 2 | 0 | 0.49 | 0.784 |
   | 3 | 0 | 0.343 | 0.6517 |

   Working: `W(1, 2) = 0.7 × 1 + 0.3 × 0.7 = 0.91`. `W(2, 2) = 0.7 × 0.91 + 0.3 × 0.49 = 0.637 + 0.147 = 0.784`. `W(3, 2) = 0.7 × 0.784 + 0.3 × 0.343 = 0.5488 + 0.1029 = 0.6517`, about 65%. The `L = 1` column is `0.7^n`.

   </details>

10. **[3 · compute · apply]** A 6-stage game has players with `p = 0.75`. (a) Use the rule of thumb (about one more life than the average number of failures) to suggest starting lives for a 50% finish rate. (b) The exact values are `W(6, 2) = 0.445` and `W(6, 3) = 0.679`. Does the rule of thumb hold here?

    <details>
    <summary>Answer</summary>

    (a) Average failures in a finished run: `n × (1 − p) / p = 6 × 0.25 / 0.75 = 2`. The rule of thumb says 3 lives.

    (b) Yes. With 2 lives the player finishes 44.5% of the time, below half. With 3 lives it is 67.9%. So 3 is the first life count above 50%, as the rule predicted.

    </details>

11. **[3 · compute · apply]** A 4-stage run at `p = 0.8`. Compare three designs: (i) 1 starting life, (ii) 1 starting life plus a 1-up for clearing stage 2, (iii) 2 starting lives. The values are 0.4096, 0.5734 and 0.7373. Match each value to its design, explain the order, and say which design to choose for a tutorial level aimed at new players.

    <details>
    <summary>Answer</summary>

    (i) 1 life: `0.8^4 = 0.4096`. (ii) 1 life plus the stage-2 1-up: 0.5734. (iii) 2 lives: `W(4, 2) = 0.7373`.

    The earned life is worth less than a starting life because it only reaches players who clear stage 2 without dying. Players who fail at stage 1 or 2 never collect it. That is the week 3 point that a success-based faucet helps the players who needed it least.

    For a tutorial aimed at new players, give the life at the start (design iii), or give it after a failure rather than after a success. The 1-up rewards players who are already doing well.

    </details>

12. **[3 · explain · apply]** An invented survival game has a one-life "iron mode". A careful player survives each dangerous encounter with probability 0.95. What is the chance of surviving 10 encounters? Use the model to explain why iron mode stays tense even for skilled players, and name one design alternative for an online game where deleting a character is too harsh.

    <details>
    <summary>Answer</summary>

    With one life, `W = p^n = 0.95^10 = 0.599`, about 60%. After 50 encounters it is `0.95^50 ≈ 0.077`.

    The chance heads toward zero as encounters pile up, whatever the skill, so the run never becomes safe. It only becomes longer, and each new encounter puts everything at risk. That is the one-life pattern the lecture shows for Hardcore modes.

    An online game can keep death meaningful without a game over by charging a different resource, as the lecture's MMO point says. Examples: time (a walk back to where you died) or currency (repair costs). This turns lives into an economy question.

    </details>

13. **[3 · critique · apply]** An invented online trading game adds an official exchange: you can buy gold with real money, and sell gold for store credit. The designers say "this doesn't change the game, it's just a shop". Describe the boundary in the lecture's three questions (space, time, what crosses) and critique the claim, using the WoW Token as the lecture describes it.

    <details>
    <summary>Answer</summary>

    Space and time are unchanged: play still happens in the same world and sessions. What crosses the boundary has changed. Real money now enters as gold, and gold leaves as store credit, which has real value.

    The claim is wrong. Juul's negotiable consequences (F6) weaken once in-game losses have a price in money. The magic circle, already a porous membrane for online worlds (Castronova), now has a door with a set exchange rate. The WoW Token example in the lecture is exactly this kind of door. Blizzard chose what may cross (money in as gold, gold out as game time or Battle.net balance) and at what rate. The designers should treat the exchange as a boundary and economy decision, set what may cross and the rate on purpose, and expect effects on in-game prices.

    </details>

## Week 4 · MDA

Lecture: [w04-mda-mechanics-dynamics-aesthetics.md](../lectures/w04-mda-mechanics-dynamics-aesthetics.md)

14. **[4 · explain · apply]** Classify each item as mechanic, dynamic or aesthetic, and give the one-line test you used. (a) "Each player starts with 12 food tokens." (b) "By round four, players stop trading food with whoever is in the lead." (c) "I felt betrayed when my ally broke our deal." (d) "The game is balanced." (e) "Players who fall behind start hoarding food."

    <details>
    <summary>Answer</summary>

    (a) Mechanic. You can write it down before anyone plays. (b) Dynamic. It is a pattern of play over time, in "who does what, when" form. (c) Aesthetic. It is a feeling a player reports. (d) None as written. "Balanced" is a claim about dynamics (no dominant strategy, several players stay competitive) that you hope produces an aesthetic. Push it down to a layer before acting on it. (e) Dynamic. It is a pattern that only exists in play, probably caused by a feedback loop.

    </details>

15. **[4 · compute · apply]** In the lecture's two-player rent model, set `r = 0.03`, salary `S = 12` and a starting gap of `d = 1.5`. (a) What is the gap's growth factor per turn? (b) During which turn does the trailer's income first reach zero? (c) A teammate proposes raising `S` to 15 to "help the trailer". What does that change?

    <details>
    <summary>Answer</summary>

    (a) `1 + 2r = 1.06`, so the gap grows 6% per turn.

    (b) The trailer's income `S − d` reaches zero when `d = 12`. Solve `1.5 × 1.06^t = 12`, so `1.06^t = 8` and `t = ln 8 / ln 1.06 = 2.079 / 0.0583 ≈ 35.7`. The income first hits zero during turn 36.

    (c) `S` cancels out of `d_next = (1 + 2r) × d`, so the snowball is exactly as fast. The tipping point moves later because the trailer now runs dry at `d = 15`: `1.06^t = 10`, `t ≈ 39.5`. Raising salary delays the collapse by about 4 turns and does not slow it.

    </details>

16. **[4 · compute · apply]** Same model with `r = 0.02` and a starting gap of 2 (the lecture's values). The leader hands back a fraction `τ = 0.25` of the gap every turn. (a) Give the new growth factor. (b) Compute the gap after 50 turns. (c) Check that the trailer's income stays positive for all 50 turns, with `S = 10`.

    <details>
    <summary>Answer</summary>

    (a) The lecture gives the factor `1 + 2r(1 − τ) = 1 + 2 × 0.02 × 0.75 = 1.03`.

    (b) `2 × 1.03^50 = 2 × 4.384 = 8.77`. Compare the lecture's untaxed game, where the gap reaches 13.88 by turn 50 (and would be 14.21 had the trailer not stopped building from turn 42).

    (c) With the hand-back, the trailer's income is `S − d + τd = 10 − 0.75d`. It reaches zero at `d = 13.3`. The gap is at most 8.77 over the 50 turns, so the trailer keeps building throughout and the pure formula is valid.

    </details>

17. **[4 · critique · apply]** A designer says "The trailing player gets a flat $6 bonus each turn, so we've fixed the runaway leader." In the two-player model the leader's income is `S + d` and the trailer's is `S + 6 − d`. (a) Derive `d_next`. (b) For which gaps does the bonus shrink the gap? (c) Critique the claim.

    <details>
    <summary>Answer</summary>

    (a) The leader's rent power grows by `r(S + d)`, the trailer's by `r(S + 6 − d)`. So `d_next = d + r(S + d) − r(S + 6 − d) = (1 + 2r)d − 6r`.

    (b) The gap shrinks when `2rd < 6r`, that is when `d < 3`. Above a gap of 3, it still grows.

    (c) The claim is half right. The bonus is conditional on being behind, so unlike a flat bonus to everyone it does touch the gap, but only while the gap is small. Once a lucky early lead passes 3, the snowball runs as before, just 6r slower per turn. It softens small leads and leaves the runaway leader for large ones. To test it, the designer should state the aesthetic it protects (hope for the trailer), run the model or the week 4 interactive, and check how often games cross the break-even gap.

    </details>

## Week 5 · Player experience goals and the 8 kinds of fun

Lecture: [w05-player-experience-goals-and-the-8-kinds-of-fun.md](../lectures/w05-player-experience-goals-and-the-8-kinds-of-fun.md)

18. **[5 · compute · apply]** A learner starts at `S0 = 3` with learning factor `g = 0.85`, so `S(n) = 10 − 7 × 0.85^n`. The ramp is `C(n) = 2.5 + 0.4n`. Compute `R = C / S` at rounds 0, 5 and 15 and name each zone (boredom below 0.8, flow 0.8 to 1.25, anxiety above 1.25). What does the pattern tell the designer?

    <details>
    <summary>Answer</summary>

    | n | S(n) | C(n) | R | Zone |
    |---|---|---|---|---|
    | 0 | 3.00 | 2.5 | 0.83 | flow |
    | 5 | 6.89 | 4.5 | 0.65 | boredom |
    | 15 | 9.39 | 8.5 | 0.91 | flow |

    Working for round 5: `0.85^5 = 0.4437`, `S = 10 − 7 × 0.4437 = 6.89`, `R = 4.5 / 6.89 = 0.65`.

    The player starts in flow, learns faster than the straight ramp climbs, drops into boredom in the middle rounds, and then the ramp catches up as learning plateaus. The ramp is too gentle early and has the wrong shape. A curved ramp that rises fast early, or a player-chosen start level, would fix the middle.

    </details>

19. **[5 · design · apply]** Rewrite each weak goal in the template "[which players] should feel [aesthetic in plain words] when [observable moment]". Name the problem with each original. (a) "Crafting should be satisfying." (b) "The multiplayer should be social."

    <details>
    <summary>Answer</summary>

    (a) Problem: no player and no observable moment, and "satisfying" names no specific aesthetic. Example rewrite: "Players who craft their first item should feel ownership of it, shown by naming it or refusing to sell it within the first session."

    (b) Problem: "social" hints at fellowship but names no moment you could watch for. Example rewrite: "In a four-player session, strangers should feel they are a team, shown by at least one player offering a resource to another without being asked before the halfway point."

    Any rewrite passes if it names who, a feeling and something a silent observer could record.

    </details>

20. **[5 · explain · apply]** An invented game: "Players take turns placing garden tiles on a shared board. There is no score. Each finished garden is photographed and pinned to a wall at the end of the session." Rank the top three MDA aesthetics for this game and tie each one to a mechanic. Which aesthetic would a designer be wrong to "fix" by adding a score?

    <details>
    <summary>Answer</summary>

    A reasonable ranking: 1. Expression (players choose what their garden says about them; the photo wall makes the result public). 2. Fellowship (a shared board means players build next to and around each other). 3. Submission (no score and no failure make it relaxing).

    Adding a score would move challenge up the profile and push expression and submission down. If the experience goal is expression or relaxation, that "fix" misreads the goal. Other rankings pass if each aesthetic is tied to a mechanic.

    </details>

21. **[5 · design · apply]** Your experience goal is "Players on a commute should be able to adjust the difficulty without stopping play, and should not feel patronised." Choose among the four approaches from the lecture (fixed ramp with level select, choose by playing as in flOw, hidden adaptation as in Left 4 Dead's Director, open assist settings as in Celeste) and justify the choice against both halves of the goal.

    <details>
    <summary>Answer</summary>

    Choose by playing, the flOw approach. The player moves deeper or back up through an action inside play, so there is no menu and no stopping, which meets the first half. The player makes the choice, so the game is not deciding for them in secret, which meets the second half.

    Hidden adaptation fails the second half: the lecture notes players can feel patronised once they notice. Level select and assist menus meet the second half but need a menu, so they fail the first. Chen's Traffic Light result (asking between rounds broke flow) is the warning against asking the player too often.

    </details>

## Week 6 · Paper prototyping

Lecture: [w06-paper-prototyping-cards-dice-boards.md](../lectures/w06-paper-prototyping-cards-dice-boards.md)

22. **[6 · compute · apply]** A player's only settlement produces on a two-dice total of 9 (4 of 36 outcomes). What is the chance of no 9 in the first 8 turns with dice? With a fresh 36-card deck that has one card per outcome? Is the deck's effect large over this stretch?

    <details>
    <summary>Answer</summary>

    Dice: `(32/36)^8 = 0.8889^8 = 0.390`, about 39.0%.

    Deck: `(32/36)(31/35)(30/34)(29/33)(28/32)(27/31)(26/30)(25/29) = 0.348`, about 34.8%.

    The deck is kinder by about 4 percentage points over 8 turns. On short stretches the difference is small. The lecture's point is that the gap grows over a whole shuffle and a whole game, where the deck's spread is less than half of the dice's.

    </details>

23. **[6 · compute · apply]** A dungeon crawl draws encounters from a 30-card deck with 6 "Ambush" cards. The alternative is a d10 where 1 or 2 means Ambush, the same 20% per draw. Compute the chance of no Ambush in the first 4 encounters for each. Then say which to pick if the experience goal is "players should never feel completely safe".

    <details>
    <summary>Answer</summary>

    Deck: `(24/30)(23/29)(22/28)(21/27) = 0.388`. d10: `0.8^4 = 0.410`.

    Across a whole deck the difference is larger than these short-stretch numbers suggest. With the deck, every safe draw makes the next Ambush more likely, and all 6 are guaranteed before the reshuffle. So long safe spells are rarer than with the die, which fits "never completely safe". The die allows longer droughts, which some players read as permission to relax. There is a cost: players who count cards know when the Ambushes are used up. Leave a few cards unseen at the bottom, as Catan's Event Cards variant does, to blunt counting.

    </details>

24. **[6 · explain · apply]** Your team is designing an invented real-time co-op cooking game for screens. You have one afternoon and paper only. Name two design questions a paper prototype can answer and two it cannot. For the ones it can answer, say how you would run it.

    <details>
    <summary>Answer</summary>

    Paper can answer questions that live in rules and numbers. For example, (1) "Do players split tasks or all rush the same station?" and (2) "Is the recipe economy (ingredients in, dishes out) too tight or too loose?" Run it as turns on a grid of stations, with a sand timer per round and one person as the computer who deals orders from a hidden deck and applies the rules exactly.

    Paper cannot answer (1) how the controls feel under time pressure (timing and dexterity), or (2) whether screen feedback (sound, animation) tells players an order is about to expire. The lecture's warning applies: a turn-based paper version shifts the aesthetic from sensation and challenge toward strategy, so do not trust it for questions about feel.

    </details>

25. **[6 · design · apply]** In an invented card game, victory points are face-up piles and the leader gets ganged up on in every playtest. You want to reduce this without changing any card numbers. Propose one change to visibility and one to randomness, and predict the dynamic each creates.

    <details>
    <summary>Answer</summary>

    Visibility: score points face down in a personal pile, or add them up only at the end. Players can no longer see the gap and react to it, so ganging up drops and players misjudge who is ahead, which keeps tension higher. The numbers are unchanged.

    Randomness: add a random element that favours trailing players, for example a bonus deck drawn only by whoever has the fewest cards in hand, or a die rolled only by the last player. That is conditional catch-up from week 4, and it shrinks leads.

    Either fix needs a playtest, because hidden scores can also make the last turn feel arbitrary if players did not know they were losing.

    </details>

## Week 7 · Playtesting: observe, don't explain

Lecture: [w07-playtesting-observe-dont-explain.md](../lectures/w07-playtesting-observe-dont-explain.md)

26. **[7 · compute · apply]** (a) A problem affects 15% of players. What is the chance that 6 silent testers show it at least once? (b) How many silent testers do you need for a 95% chance of seeing a problem that affects 20% of players?

    <details>
    <summary>Answer</summary>

    (a) `1 − 0.85^6 = 1 − 0.377 = 0.623`, about 62%.

    (b) Solve `1 − 0.8^n ≥ 0.95`, so `n ≥ ln(0.05) / ln(0.8) = −2.996 / −0.2231 = 13.4`. You need 14 testers. Check: `1 − 0.8^14 = 1 − 0.044 = 0.956`.

    </details>

27. **[7 · compute · apply]** A prototype has four suspected problems with frequencies 0.40, 0.25, 0.10 and 0.05. The first two are onboarding problems. (a) With 4 silent testers, how many problems do you expect to see? (b) The facilitator explains the two onboarding rules before play. How many now? (c) How much did the explanation improve the game?

    <details>
    <summary>Answer</summary>

    (a) Add each problem's `1 − (1 − p)^4`: `0.870 + 0.684 + 0.344 + 0.185 = 2.08`.

    (b) The explained problems have `p = 0` in the room, so only the last two count: `0.344 + 0.185 = 0.53`.

    (c) Not at all. The two onboarding problems still hit 40% and 25% of players at home. The explanation removed them from the report, not from the game. The team now expects to see about half a problem where it would have seen about two.

    </details>

28. **[7 · critique · apply]** Here is part of a session transcript. Mark each facilitator line as neutral prompt, deflection, leading prompt or explanation, and rewrite the non-neutral ones.

    > Tester: "Can I play two cards this turn?"
    > Facilitator (F1): "No, just one, but you can hold the other for later."
    > Tester: (pauses 20 seconds over the market)
    > Facilitator (F2): "What are you looking for?"
    > Facilitator (F3): "Did you notice the trade icon in the corner?"
    > Tester: "Is this card good?"
    > Facilitator (F4): "What do you think the rules say?"

    <details>
    <summary>Answer</summary>

    - F1 is an explanation, and it also adds a hint. It sets `p` to zero for "players think they can play two cards" and for "players don't know they can hold cards". Rewrite: "What do you think the rules say?" and log the question.
    - F2 is a neutral prompt. Keep it.
    - F3 is a leading prompt. It tells the tester what to notice. Rewrite: "What are you thinking right now?" Then log whether the tester finds the trade icon unaided.
    - F4 is a correct deflection. Keep it, and log the question, because a tester's question is a finding.

    </details>

29. **[7 · explain · apply]** Rank these findings from three silent sessions using the lecture's method (severity first, then count). (A) 3 of 3 testers took over a minute to set up the board, severity 1. (B) 1 of 3 testers could not continue after the market deck ran out, and needed an ASSIST, severity 3. (C) 2 of 3 testers never used the trade action, severity 2. (D) 2 of 3 misread the scoring and played for the wrong goal, severity 2. Then say what the ranking does with B, and why.

    <details>
    <summary>Answer</summary>

    Rank: B (severity 3, 1 of 3), then C and D (severity 2, 2 of 3 each, tied), then A (severity 1, 3 of 3).

    B goes first even though only one tester showed it. A blocker seen once in a three-tester test is exactly the kind of problem small tests usually miss, and at home nobody will give the ASSIST. A, seen by everyone, is only friction. Keep each finding separate from its fix ("maybe add a reshuffle rule" goes in the optional column).

    </details>

30. **[7 · critique · recall]** A classmate's report says "Five testers find 85% of the problems, so our five-tester test found almost everything." Explain what the 85% figure is, where it comes from, and what it does not promise.

    <details>
    <summary>Answer</summary>

    It comes from Nielsen and Landauer's model, `1 − (1 − L)^n`, where L was about 0.31 when averaged over web usability projects. With `n = 5`, `1 − 0.69^5 ≈ 0.84`. It is an average over problems whose typical frequency was 31%. It does not promise 85% for your game. For a problem that affects 5% of players, five testers show it only 22.6% of the time. The correct question is "85% of problems of what frequency?" A GD101 report should also write counts ("3 of 5 testers"), not percentages of players.

    </details>

## Week 8 · Iteration loops and kill-your-darlings

Lecture: [w08-iteration-loops-and-kill-your-darlings.md](../lectures/w08-iteration-loops-and-kill-your-darlings.md)

31. **[8 · compute · apply]** A team has 40 days, a 4-day loop and a hit rate of 12%. How many loops fit, what is the chance of at least one keeper, and what is the expected number of days to the first keeper?

    <details>
    <summary>Answer</summary>

    `I = floor(40/4) = 10`. `P = 1 − 0.88^10 = 1 − 0.279 = 0.721`, about 72.1%. Expected days `c / q = 4 / 0.12 = 33.3`.

    </details>

32. **[8 · compute · apply]** You have 50 days and a hit rate of 10%. Plan A uses a 10-day digital loop for all 50 days. Plan B spends the first 20 days on 2-day paper loops and the last 30 days on 10-day digital loops. Compare the chance of at least one keeper, and name one question that must stay in the digital phase.

    <details>
    <summary>Answer</summary>

    Plan A: `floor(50/10) = 5` loops, `1 − 0.9^5 = 0.410`, 41.0%.

    Plan B: `floor(20/2) + floor(30/10) = 10 + 3 = 13` loops, `1 − 0.9^13 = 0.746`, 74.6%.

    Plan B nearly doubles the odds with the same people and days. Questions about real-time feel stay digital, for example "does the dodge feel responsive?" Paper cannot test timing or input feel (week 6).

    </details>

33. **[8 · compute · apply]** With a hit rate of 20% per loop, what is the median number of loops to the first keeper? What is the mean? Why do they differ?

    <details>
    <summary>Answer</summary>

    Median: the first count where the chance of a keeper passes one half. `1 − 0.8^3 = 0.488` (not yet), `1 − 0.8^4 = 0.590`. So the median is 4 loops. Equivalently `ceil(ln 0.5 / ln 0.8) = ceil(3.11) = 4`.

    Mean: `1 / q = 5` loops.

    The distribution is skewed. Many teams hit early, and a few wait a long time, which pulls the mean above the median. Plan for the tail, not the average: about one team in ten still has nothing after 10 loops (`0.8^10 = 0.107`).

    </details>

34. **[8 · critique · apply]** A teammate says "We spent five weekends on the bartering system. We can't cut it now. Let's give it two more weeks of polish." (a) Name the error. (b) Write a keep, change and kill table for the bartering system that a five-tester silent playtest could check, including a limit on change loops.

    <details>
    <summary>Answer</summary>

    (a) The sunk cost trap. The five weekends are gone whatever the team decides, so they should not appear in the decision. The only question is whether the next two weeks are better spent on bartering or on something else.

    (b) Example, written and dated before testing:

    | Decision | Criterion |
    |---|---|
    | Keep | At least 3 of 5 testers make a barter offer by round 3 without prompting, and at least 2 describe it in the debrief as a choice they weighed. |
    | Change | 1 or 2 of 5 barter, or testers barter but call it automatic. Make one change aimed at the finding and retest. |
    | Kill | 0 of 5 barter after two change loops, or bartering causes a stalled game (severity 3) twice. |

    </details>

## Week 9 · Choice and meaningful decisions

Lecture: [w09-choice-and-meaningful-decisions.md](../lectures/w09-choice-and-meaningful-decisions.md)

35. **[9 · compute · apply]** Tic-tac-toe, squares numbered 0 to 8 left to right, top to bottom. X holds squares 0 and 8 (opposite corners), O holds 4 (the centre), and O is to move. Give the minimax value (from X's view) of each of O's six moves, classify the position as forced, no-stakes or stakes, and explain the losing moves.

    ```
     X  .  .
     .  O  .
     .  .  X
    ```

    <details>
    <summary>Answer</summary>

    | O plays | Value |
    |---|---|
    | 1 (top edge) | 0 |
    | 2 (corner) | +1 |
    | 3 (left edge) | 0 |
    | 5 (right edge) | 0 |
    | 6 (corner) | +1 |
    | 7 (bottom edge) | 0 |

    The children have different values, so this is a **stakes** position. Four of six moves keep the draw.

    Why the corners lose: say O plays 2. That threatens the diagonal 2-4-6, so X must block at 6. Now X holds 0, 6 and 8 and threatens both 0-3-6 (needs 3) and 6-7-8 (needs 7). O can block only one, so X wins. That is a fork, the same move as in the week 2 Three-to-Fifteen game. Playing 6 is the mirror case. Once a player learns "answer opposite corners with an edge", the decision stops being uncertain, which is the week 9 story of why tic-tac-toe dies.

    </details>

36. **[9 · compute · apply]** Nim with heaps of 2, 5 and 6. Is the player to move winning or losing against perfect play? If winning, give the winning move and show the XOR after it.

    <details>
    <summary>Answer</summary>

    In binary, 2 = 010, 5 = 101, 6 = 110. `010 XOR 101 = 111`, then `111 XOR 110 = 001`. The XOR is 1, not zero, so the player to move wins.

    To win, move to a position with XOR zero. For each heap `h`, the target is `h XOR 1`: heap 2 would need to become 3 (you cannot add), heap 6 would need to become 7 (cannot), heap 5 becomes 4. So take 1 from the heap of 5. Check: `010 XOR 100 XOR 110 = 000`.

    </details>

37. **[9 · design · apply]** A card offers "Take 8 gold now, or 3 gold at the start of each of your remaining turns." (a) For how many remaining turns is each option better? (b) In a 12-turn game, at which turns is this an interesting decision? (c) Propose one change that makes it a real decision more often.

    <details>
    <summary>Answer</summary>

    (a) Income gives `3t` over `t` turns. It beats 8 when `3t > 8`, so with 3 or more turns left (9 against 8). With 2 or fewer turns left, take the 8. There is no exact tie.

    (b) Almost never. Early on, income wins by a wide margin (with 11 turns left, 33 against 8), and late, the lump sum wins. Only near 2 to 3 turns left is the answer close, so the decision is a lookup nearly all game and fails the uncertain test.

    (c) Make the options trade off in more situations. For example, make the lump sum grow each round ("take 2 gold per turn already played"), so the break-even point moves. Or tie the income to a risk ("income stops if you are raided"). Then write two situations where each option is best, and playtest for hesitation.

    </details>

38. **[9 · critique · apply]** In an invented duel game, each turn you choose between Shield (block 2 damage) and Potion (heal 3). Playtest logs show 5 of 5 testers always take Potion, instantly. Run the section 3 audit on this decision, name the test it fails, and propose a one-rule fix with two situations in which different options are best.

    <details>
    <summary>Answer</summary>

    Options: 2, both legal. Different outcomes: yes. Discernable: yes (health visibly changes). Integrated: yes (health decides the duel). Uncertain: no. Healing 3 is always worth more than blocking 2, so a simple rule always gives the answer. Best option changes with the situation: no. Instant identical choices are the playtest sign of a lookup.

    One-rule fix: "Potion cannot raise health above its starting value, and Shield also reflects 1 damage to the attacker." Situation 1: you are at full health, so Potion does nothing and Shield (block and reflect) is best. Situation 2: you are low and the opponent is not attacking hard, so Potion is best. Retest and watch for hesitation, and for the opposite failure where everyone now shields.

    </details>

39. **[9 · explain · recall]** Define discernable, integrated and uncertain, and give one example of a decision that passes the first two and fails the third.

    <details>
    <summary>Answer</summary>

    Discernable: the player can perceive what their action did. Integrated: the outcome matters to the larger game beyond the moment (both from Salen & Zimmerman's meaningful play). Uncertain: before choosing, the player cannot simply know which option is best.

    Example: O's reply to a corner opening in tic-tac-toe. The result is visible and decides the game, but once you know "take the centre" it is a lookup, so it fails the uncertain test.

    </details>

## Week 10 · Chance vs skill

Lecture: [w10-chance-vs-skill-and-randomness.md](../lectures/w10-chance-vs-skill-and-randomness.md)

40. **[10 · compute · apply]** Two players each roll a d8 and add their skill. The stronger player has a skill gap of 1. Ties are re-rolled. (a) Count W, T and L with the shortcut and compute the round edge `p`. (b) Compute the chance the stronger player wins a best-of-3 using `p² × (3 − 2p)`. (c) What Elo rating gap gives the same single-round edge, using `D = −400 × log10(1/p − 1)`?

    <details>
    <summary>Answer</summary>

    (a) Ties `T = d − g = 7`. Losses `L = (d − g − 1)(d − g) / 2 = 6 × 7 / 2 = 21`. Wins `W = 64 − 7 − 21 = 36`. `p = 36 / 57 = 0.632`.

    (b) `0.632² × (3 − 1.263) = 0.3989 × 1.737 = 0.693`.

    (c) `1/p − 1 = 0.583`, `log10(0.583) = −0.234`, so `D = 94` rating points.

    </details>

41. **[10 · design · apply]** Brief: "the stronger player should win at least 75% of best-of-3 matches". Which of these designs meets it? d6 with gap 1, d8 with gap 1, d10 with gap 2, d12 with gap 2, d20 with gap 4. Show `p` and the best-of-3 value for each, and pick one for a family game.

    <details>
    <summary>Answer</summary>

    | Design | p | Best of 3 | Meets 75%? |
    |---|---|---|---|
    | d6, g 1 | 21/31 = 0.677 | 0.755 | yes |
    | d8, g 1 | 36/57 = 0.632 | 0.693 | no |
    | d10, g 2 | 64/92 = 0.696 | 0.778 | yes |
    | d12, g 2 | 89/134 = 0.664 | 0.737 | no |
    | d20, g 4 | 264/384 = 0.688 | 0.768 | yes |

    A round edge of about 0.674 is the minimum for 75% in a best of 3.

    For a family game, pick the passing design with the most luck per round: d6 with gap 1 sits just above the target (0.755), so upsets stay common while the brief is met. Notice that d12 g2 and d20 g4 have the same gap-to-die ratio and still differ by 3 points. The ratio is a guide, not an exact rule, because ties and the triangle shape depend on the counts.

    </details>

42. **[10 · explain · apply]** Classify each random element in an invented trading game as input or output randomness, and predict what players will say after a loss caused by each. (a) At the start of each round a weather card is revealed, then players plan routes. (b) After you make a trade offer, you roll a die to see whether the buyer accepts. (c) Each player draws three contracts and keeps one. (d) After a raid is declared, a die decides whether it succeeds.

    <details>
    <summary>Answer</summary>

    (a) Input: the weather comes before the decision. Losers tend to say "I planned badly for the storm", which names a decision. (b) Output: the roll comes after the offer. Expect "I made a good offer and the dice said no". (c) Input: the random menu comes before the pick. Skill shows in the choice. (d) Output: the roll decides after you commit. It adds suspense at the moment of action and, if the swing is large, complaints of unfairness.

    Lecture test: after a loss, ask "what would you do differently?" Input randomness usually gets a named decision in answer; output randomness gets "roll better".

    </details>

43. **[10 · critique · apply]** A designer finds that strategy A beats strategy B in 68% of rounds on a d6. They switch the round die to a d20 and report "A now wins only 55%, so the game is balanced." Critique the claim with the lecture's model and numbers.

    <details>
    <summary>Answer</summary>

    In the "skill plus a die" model, a 1-point edge gives `p = 0.677` on a d6 and `p = 0.551` on a d20. The numbers fit a fixed 1-point advantage for A with only the die changed. A is still better in every round. The bigger die pulls results toward 50% and hides the gap. It does not remove it.

    Consequences: players who play enough rounds still find A (in a best of 15 at `p = 0.55`, A wins about 65% of matches), and the game now also shows less skill for everyone. The lecture misconception applies: randomness hides imbalance rather than fixing it. The real fix is to make B better in some situations (week 11), then choose the die for the audience.

    </details>

## Week 11 · Dominant strategies

Lecture: [w11-dominant-strategies-and-how-to-spot-them.md](../lectures/w11-dominant-strategies-and-how-to-spot-them.md)

44. **[11 · compute · apply]** An invented siege game. Each round both players secretly pick Rush, Scout or Fort. Your net points per round:

    | You \ Opponent | Rush | Scout | Fort |
    |---|---|---|---|
    | Rush | 0 | +2 | −1 |
    | Scout | −2 | 0 | −1 |
    | Fort | +1 | +1 | 0 |

    (a) Find every dominance (strict or weak). (b) Follow the cascade: cross out dominated rows and their columns, then retest. What is left? (c) A fix changes Scout vs Fort to +3 for Scout (and Fort vs Scout to −3). Show that no card is dominated, and find the mix at which all three cards average zero.

    <details>
    <summary>Answer</summary>

    (a) Fort vs Scout: +1 > −2, +1 > 0, 0 > −1, so Fort strictly dominates Scout. Rush vs Scout: 0 > −2, +2 > 0, −1 = −1, so Rush weakly dominates Scout. Fort vs Rush: +1 > 0 but +1 < +2, no dominance either way.

    (b) Remove Scout's row and column. On columns Rush and Fort: Rush (0, −1), Fort (+1, 0). Fort strictly dominates Rush. Remove it. Fort is the only card left, so both players Fort every round and every round nets 0.

    (c) New rows: Rush (0, +2, −1), Scout (−2, 0, +3), Fort (+1, −3, 0). Rush vs Scout: 0 > −2 but −1 < +3. Rush vs Fort: 0 < +1 but +2 > −3. Scout vs Fort: −2 < +1 but +3 > 0. No row is at least as big everywhere, so nothing is dominated. It is now a loop: Rush beats Scout, Scout beats Fort, Fort beats Rush.

    Balance point: let the opponent play Rush, Scout, Fort in proportions r : s : f. Rush row `2s − f = 0`, Scout row `−2r + 3f = 0`, Fort row `r − 3s = 0`. So `f = 2s` and `r = 3s`, a mix of 3 : 1 : 2. Check Fort: `3 − 3 + 0 = 0`.

    </details>

45. **[11 · compute · apply]** A four-card game with cards A, B, C, D has this table (your net per round):

    | You \ Opp | A | B | C | D |
    |---|---|---|---|---|
    | A | 0 | −3 | −3 | −2 |
    | B | +3 | 0 | −3 | −2 |
    | C | +3 | +3 | 0 | −3 |
    | D | +2 | +2 | +3 | 0 |

    Check the table's mirror property, then run iterated elimination. List each card as it dies, with the card that kills it and whether the dominance is strict or weak.

    <details>
    <summary>Answer</summary>

    Mirror check: every cell (X, Y) is the negative of (Y, X), and the diagonal is 0. It holds.

    Round 1, all columns: D vs A is +2 > 0, +2 > −3, +3 > −3, 0 > −2, so D strictly dominates A. B vs A: 3 > 0, 0 > −3, −3 = −3, −2 = −2, so B weakly dominates A. No other row is dominated. A dies.

    Round 2, columns B, C, D: B (0, −3, −2), C (+3, 0, −3), D (+2, +3, 0). D vs B: 2 > 0, 3 > −3, 0 > −2, strict. D vs C: 2 < 3, no. C vs B: 3 > 0, 0 > −3, −3 < −2, no. B dies.

    Round 3, columns C, D: C (0, −3), D (+3, 0). D strictly dominates C. C dies.

    D is left. The order is A, B, C. Every step looked like one card "slightly too good", which is how a small mistake empties a game.

    </details>

46. **[11 · compute · apply]** In Skirmish v2 (lecture section 2), your opponent plays Strike, Guard and Bash in the ratio 5 : 1 : 1. Compute your average net damage with each card, and say what to play.

    <details>
    <summary>Answer</summary>

    Rows (vs Strike, Guard, Bash): Strike (0, −1, +2), Guard (+1, 0, −4), Bash (−2, +4, 0).

    - Strike: `(0 × 5 − 1 × 1 + 2 × 1) / 7 = 1/7 ≈ +0.14`.
    - Guard: `(1 × 5 + 0 − 4 × 1) / 7 = 1/7 ≈ +0.14`.
    - Bash: `(−2 × 5 + 4 × 1 + 0) / 7 = −6/7 ≈ −0.86`.

    Strike and Guard tie. Avoid Bash, which a Strike-heavy opponent punishes. The mix sits on the border between the Strike and Guard regions of the lecture's triangle.

    </details>

47. **[11 · design · apply]** An invented shop sells a Bronze Sword (cost 3, +2 attack) and a Quick Dagger (cost 3, +2 attack, attacks first). (a) Which relation holds? (b) Propose two different fixes, one that changes a number and one that changes an interaction, and say which keeps both items alive.

    <details>
    <summary>Answer</summary>

    (a) At the same cost the dagger gives everything the sword gives plus "attacks first". The dagger weakly dominates the sword, the Lightning Bolt and Shock relation from the lecture ("strictly better" in player slang). The sword is a dead option.

    (b) Number fix: raise the sword to +3 attack. Now the sword hits harder and the dagger strikes first, a trade-off, but check the table against the enemies in the game so the sword does not dominate instead.

    Interaction fix: "The sword breaks shields; the dagger does not." Now each item has a job against a different enemy type. The interaction fix usually keeps both alive more robustly, because it creates a situation where each is best (week 11 judgment: interaction changes create new ladders, number changes move items along one ladder). Either way, rebuild the table afterwards.

    </details>

## Week 12 · Feedback, juice, clarity, readability

Lecture: [w12-feedback-juice-clarity-readability.md](../lectures/w12-feedback-juice-clarity-readability.md)

48. **[12 · compute · apply]** Using the lecture's assumptions (`a = 200 ms`, `b = 150 ms` per doubling, 4-frame start-up and 50 ms lag at 60 fps), a boss has 6 attacks with distinct responses and a 45-frame windup. A particle burst hides the boss for 100 ms at the start of each windup. (a) Is the telegraph fair? Give the margin. (b) Name two changes that make it fair, each with the new margin.

    <details>
    <summary>Answer</summary>

    (a) One frame is `1000/60 = 16.7` ms. `T_needed = 100 + 200 + 150 × log2(6) + 4 × 16.7 + 50 = 100 + 200 + 387.7 + 66.7 + 50 = 804.4 ms`, which is 49 frames. The windup is `45 × 16.7 = 750 ms`. Unfair by 54.4 ms, about 4 frames.

    (b) Remove the hiding (draw the warning on top of the particles): `T_needed = 704.4 ms`, margin +45.6 ms, fair. Or make the six attacks share responses so only four are distinct: `100 + 200 + 300 + 66.7 + 50 = 716.7 ms`, margin +33.3 ms, fair. A third option is a longer windup of at least 49 frames. Variety and visual noise are paid from the same budget.

    </details>

49. **[12 · compute · apply]** In the ruler-drop activity, a student's median catch is 15 cm on the simple drop and 24 cm on the red-or-blue drop. (a) Convert both to times with `t = √(2d / 980)` and estimate `b`. (b) Using `a = 175 ms` and `b = 46 ms`, with a 4-frame start-up and 50 ms lag, what is the largest number of distinct warnings this student can handle with a 30-frame telegraph at 60 fps?

    <details>
    <summary>Answer</summary>

    (a) `√(30/980) = 0.175 s` and `√(48/980) = 0.221 s`. The red-or-blue drop is `n = 2`, and `log2(2) = 1`, so `b ≈ 221 − 175 = 46 ms`.

    (b) The telegraph is 500 ms. Room for choice cost: `500 − 175 − 66.7 − 50 = 208.3 ms`. So `46 × log2(n) ≤ 208.3`, `log2(n) ≤ 4.53`, `n ≤ 2^4.53 = 23.1`. The student handles up to 23 distinct warnings. This student's `b` is far below the lecture's placeholder of 150 ms, which is why the lecture asks you to measure. A class-wide design must use the slow end of the pooled range, not one fast student.

    </details>

50. **[12 · explain · apply]** Classify each piece of feedback in an invented paper game by job (confirm, report, forecast). (a) You slide your ship token onto a new square. (b) A face-up "next storm" card shows which column floods next round. (c) The scorekeeper moves your marker up the score track after a delivery. (d) A sand timer is turned over when the last player passes.

    <details>
    <summary>Answer</summary>

    (a) Confirm (your move registered), and report where you now are. (b) Forecast, a board-game telegraph. (c) Report, the consequence of the delivery. (d) Forecast (the round is about to end), and confirm that everyone has passed.

    </details>

51. **[12 · critique · apply]** A team's resource card shows its value as small black text in the centre, and uses a red border for "can be traded" and a green border for "cannot be traded". Players fan cards in one hand. Critique the design against hierarchy, one meaning per signal and redundancy, and propose a redesign.

    <details>
    <summary>Answer</summary>

    Hierarchy: the value is the number players need every turn, but it sits small in the centre, hidden when cards are fanned. Move it large to a top corner.

    One meaning per signal: if red means anything else in the game (damage, danger), the border now has two meanings. Check the signal dictionary.

    Redundancy: tradeable versus not is carried by colour alone, and it is a red-green distinction, which fails for players with red-green colour deficiency (the lecture cites up to 8% of men of Northern European descent) and breaks WCAG 1.4.1. Add a second channel, for example a two-arrow icon printed on tradeable cards and a padlock on the others, in the same corner as the value.

    Test the redesign with the one-second glance test and the squint test from lab 12.

    </details>

## Week 13 · Genres as clusters of mechanics

Lecture: [w13-genres-as-clusters-of-mechanics.md](../lectures/w13-genres-as-clusters-of-mechanics.md)

52. **[13 · compute · apply]** Use the lecture's columns and its six coded games (Rogue {P, R, T, M}, Spelunky {P, R, A, M, J, U}, Hades {P, R, A, M, U}, Slay the Spire {P, R, T, D, U}, Dominion {R, T, D}, Super Metroid {A, M, J, G}). (a) Game Z = {P, R, A, M, J}. Compute J against all six and name its nearest neighbour. (b) Game Y = {R, T, D, G}. Same questions. (c) What single column would you add to Z to make it identical to its nearest neighbour?

    <details>
    <summary>Answer</summary>

    (a) Z against Rogue: shared {P, R, M} = 3, union 6, J = 0.50. Spelunky: shared 5, union 6, J = 0.83. Hades: shared {P, R, A, M} = 4, union 6, J = 0.67. Slay the Spire: shared {P, R} = 2, union 8, J = 0.25. Dominion: shared {R} = 1, union 7, J = 0.14. Super Metroid: shared {A, M, J} = 3, union 6, J = 0.50. Nearest neighbour: Spelunky at 0.83.

    (b) Y against Rogue: shared {R, T} = 2, union 6, J = 0.33. Spelunky: 1/9 = 0.11. Hades: 1/8 = 0.125. Slay the Spire: shared {R, T, D} = 3, union 6, J = 0.50. Dominion: shared 3, union 4, J = 0.75. Super Metroid: shared {G} = 1, union 7, J = 0.14. Nearest neighbour: Dominion at 0.75.

    (c) Add U (unlocks between runs). Z becomes {P, R, A, M, J, U}, exactly Spelunky's coded set.

    </details>

53. **[13 · compute · apply]** Five invented board games are coded on six columns: TR (trading), DR (dice resolution), HC (hidden information), AP (area placement), EL (player elimination), CO (cooperative). Harbor {TR, DR, AP}, Lanterns {HC, CO}, Siege {DR, AP, EL}, Bazaar {TR, HC, AP}, Vigil {HC, CO, DR}. (a) Compute all ten Jaccard values. (b) List the clusters at t = 0.5 and at t = 0.25, allowing chains. (c) Which pair shows the chaining effect at t = 0.5?

    <details>
    <summary>Answer</summary>

    (a)

    | Pair | Shared | Union | J |
    |---|---|---|---|
    | Harbor, Lanterns | 0 | 5 | 0 |
    | Harbor, Siege | 2 | 4 | 0.50 |
    | Harbor, Bazaar | 2 | 4 | 0.50 |
    | Harbor, Vigil | 1 | 5 | 0.20 |
    | Lanterns, Siege | 0 | 5 | 0 |
    | Lanterns, Bazaar | 1 | 4 | 0.25 |
    | Lanterns, Vigil | 2 | 3 | 0.67 |
    | Siege, Bazaar | 1 | 5 | 0.20 |
    | Siege, Vigil | 1 | 5 | 0.20 |
    | Bazaar, Vigil | 1 | 5 | 0.20 |

    (b) At t = 0.5: {Harbor, Siege, Bazaar} and {Lanterns, Vigil}. At t = 0.25: one cluster of all five, joined by the Lanterns and Bazaar link at exactly 0.25.

    (c) Siege and Bazaar share only one mechanic (J = 0.20), yet land in the same cluster at 0.5 through Harbor. Each link looks reasonable; the ends of the chain have little in common.

    </details>

54. **[13 · critique · apply]** A student pitch says "It's a roguelike, but you keep all your items when you die, and the dungeon is the same every time." Using the genre-as-contract table from the lecture, name the expectations the pitch breaks, predict what players who read "roguelike" will do or feel, and rewrite the pitch's first line so the breaks are deliberate and stated.

    <details>
    <summary>Answer</summary>

    Broken expectations: permadeath runs (a death no longer costs the run) and randomized content (the dungeon never changes). Predicted effects from the table: players hoard resources "for later", because risk has no cost, and they memorize the route, so the game turns into a timing test. Players who came for "every run is fresh" may feel cheated.

    With two of the cluster's core mechanics gone, "roguelike" is a poor label. Rewrite example: "A fixed dungeon you learn by heart, where every death keeps your gear but moves the monsters. Closest to a Metroidvania, with one deliberate break: death reshuffles enemy positions." The rewrite names the nearest neighbour and the break in the first line, as week 14's pitch structure asks.

    </details>

## Week 14 · Design documents: one-pagers and pitch

Lecture: [w14-design-documents-one-pagers-and-pitch.md](../lectures/w14-design-documents-one-pagers-and-pitch.md)

55. **[14 · compute · apply]** A one-pager has pillars A, B, C and D and mechanics m1 to m6. Links: m1 to A and B; m2 to A; m3 to C; m4 to nothing; m5 to B and C; m6 to C. (a) Compute every support and load, and check the totals agree. (b) Name unsupported pillars, fragile pillars and orphans. (c) Run the swap test on every mechanic and give each verdict.

    <details>
    <summary>Answer</summary>

    (a) Support: A = 2 (m1, m2), B = 2 (m1, m5), C = 3 (m3, m5, m6), D = 0. Load: m1 = 2, m2 = 1, m3 = 1, m4 = 0, m5 = 2, m6 = 1. Totals: 7 by pillar, 7 by mechanic. They agree.

    (b) Unsupported: D. Fragile: none. Orphan: m4.

    (c)

    | Remove | A | B | C | D | Verdict |
    |---|---|---|---|---|---|
    | m1 | 1 | 1 | 3 | 0 | structural |
    | m2 | 1 | 2 | 3 | 0 | structural |
    | m3 | 2 | 2 | 2 | 0 | safe |
    | m4 | 2 | 2 | 3 | 0 | safe |
    | m5 | 2 | 1 | 2 | 0 | structural |
    | m6 | 2 | 2 | 2 | 0 | safe |

    D is already at 0, so no removal can make it newly unsupported, and no mechanic is critical. The page's real problem is D: add a mechanic that serves it or cut the pillar from the page and the pitch. Then decide m4: cut it, or write the reason it stays.

    </details>

56. **[14 · compute · apply]** In the lecture's Diablo pitch grid, suppose the team had cut the magic items (m4) and the lighting and line of sight (m6), and kept everything else. Recompute every pillar's support and name any fragile pillar.

    <details>
    <summary>Answer</summary>

    Start from the lecture's supports: Rp 2, Ex 4, Xp 2, Cf 3, Cd 3. m4 serves Ex, Cf and Cd. m6 serves Xp.

    - Rp = 2 (m1, m9), unchanged.
    - Ex = 4 − 1 = 3 (m1, m8, m9).
    - Xp = 2 − 1 = 1 (m1 only).
    - Cf = 3 − 1 = 2 (m2, m8).
    - Cd = 3 − 1 = 2 (m3, m5).

    Exploration becomes fragile, resting on the random dungeon alone. No pillar is unsupported. Note that cutting m4 alone was safe (the lecture's swap test), and cutting m6 alone was structural. Swap tests must be rerun when you cut two things at once.

    </details>

57. **[14 · critique · apply]** Here is a student's pitch plan. Critique it against the lecture's three-minute structure and the common pitch failures, then give the order you would use instead.

    > 0:00 to 1:30: the history of the kingdom and its three factions.
    > 1:30 to 2:30: "It has crafting, trading, a day-night cycle and 40 unique cards."
    > 2:30 to 3:00: "It's deep, strategic and really emotional. Any questions?"

    <details>
    <summary>Answer</summary>

    Failures: the lore opening (90 seconds before the listener knows what they do), the feature list (features without pillars sound like costs), and the adjective pitch ("deep, strategic, emotional" are claims nobody can check). There is no hook, no nearest neighbour or deliberate break, no one-turn walk-through, no pillars with supporting mechanics, no playtest evidence and no ask.

    Use the lecture's order: hook (0:00 to 0:20), what it is like (to 0:40), one turn with a real decision (to 1:40, with setting shown through things the player touches), why it holds together (each pillar and two mechanics, to 2:20), one number from playtesting and what changed (to 2:45), the ask (to 3:00). Every claim should point to a line on the one-pager.

    </details>

## Integrated cases (several weeks)

58. **[4, 9, 11 · critique · apply]** A playtest report on an invented card game reads: "Players liked it. By game three, all four testers opened with Harvest every time. The Market card was played 0 times in 16 games. One tester said the last five turns were pointless because the leader couldn't be caught." Identify one issue for each of weeks 4, 9 and 11, name the evidence, and state the first test you would run for each.

    <details>
    <summary>Answer</summary>

    - Week 11, dominance: convergence on one opening (4 of 4 by game three) and a card picked 0 times in 16 games. First test: build a payoff table or run the extreme test (Harvest against every other opening), and a forced-Market game to see whether Market is dominated or just unclear.
    - Week 9, dead decision: an opening chosen identically every time is a lookup and fails the uncertain test. First test: write two situations where a different opening should be best. If you cannot, the decision is dead.
    - Week 4, runaway leader: "the leader couldn't be caught" in the last five turns is an aesthetic report (lost tension). Climb down to a dynamic (the outcome is decided before the end) and a mechanic (a positive feedback loop, perhaps Harvest feeding more Harvest). First test: log net worth each round and measure the decided-to-ended gap, as in lab 04.

    "Players liked it" is the weakest evidence in the report (week 7).

    </details>

59. **[3, 6, 10 · design · apply]** You are tuning an invented dice race for new players. Each stage is cleared by rolling 6 or more on two dice (p = 26/36). There are 6 stages. The lecture gives `W(6, 2) = 0.378` and `W(6, 4) = 0.779` at this p. Your goal: "a first-time player finishes about three times in four, and a failure never comes from one unlucky streak". Choose lives, and decide whether stage clears should come from dice or from a deck of 36 cards. Justify with numbers and name one cost of your choice.

    <details>
    <summary>Answer</summary>

    Lives: 4. `W(6, 4) = 0.779` is closest to three in four; 2 lives gives only 37.8%.

    Randomizer: a deck. The goal says a failure should not come from one unlucky streak, and the week 6 result is that a deck with the same odds per draw has much smaller spread and shorter dry spells over a game. Note that the `W` values assume independent rolls, so with a deck the finish rate shifts slightly. Recheck by simulation or a paper run.

    Cost: counting. Players who track the deck know when failures are used up, and the roll as a shared moment (sensation, suspense) is lost. Leaving a few cards unseen at the bottom blunts counting.

    </details>

60. **[7, 8, 14 · explain · apply]** Viva question. Pick one finding from your own playtest reports. Trace it through to your one-pager: the observation and count, the kill criteria you wrote, the decision, the change-log line, and which pillar's support changed. If no pillar's support changed, explain why the change still mattered.

    <details>
    <summary>Answer</summary>

    A strong answer names every link with real numbers. Example: "3 of 5 testers never traded (severity 2, lab 07). Kill criteria before loop 2: keep if at least 3 of 5 trade by round 3. We changed trading to happen at the shared market and retested: 4 of 5 traded (lab 08). Keep. Change log v4: 'Trading moved to market; 4 of 5 used it.' Trading links to pillar P1 ('I had to choose between helping myself and hurting you'), so P1's support rose from 1 to 2 and it is no longer fragile."

    Assessors look for the chain from observation to decision to document, counts rather than percentages, criteria set before the test, and a swap-test view of the change. A change that moved no support can still matter as a readability fix (week 12) or an orphan cut (week 14).

    </details>

---

## Viva prompts for the week 15 showcase

Assessors adapt tagged questions to the team's game. Pick one from each group.

- **Models on your game.** Question 10 or 11 (lives), 22 or 23 (dice or deck), 40 or 41 (luck dials), 44 or 45 (payoff table), 48 (telegraph budget, for any timed element), 52 (nearest neighbour), 55 (pillar grid). Replace the example with the team's own numbers or components.
- **Method.** Question 29 (ranking findings), 34 (kill criteria), 38 (decision audit), 58 or 60 (tracing evidence).

A good viva answer uses the model on the team's own prototype, gives counts from the team's logs, and says what the model does not capture.
