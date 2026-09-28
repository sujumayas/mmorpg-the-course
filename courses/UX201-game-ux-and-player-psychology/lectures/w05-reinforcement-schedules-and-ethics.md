# UX201 · Week 05 — Reinforcement Schedules and Their Ethics

**Why this matters:** Two reward systems can pay out at exactly the same average rate and produce completely different players. One gives them a natural place to stop. The other never does. This week you learn why the random one keeps people going, how to compute the difference, and where that power stops being good design and starts being something regulators treat as gambling.

**You will be able to:**
- Name the four basic reinforcement schedules, give a game example of each, and predict the response pattern each produces.
- Compute the discounted value of the next action under fixed and random ratio schedules, and find where a player's natural stopping points fall.
- Compute how long a player on a random schedule takes to notice that rewards have stopped, and explain why that makes random schedules resistant to extinction.
- Evaluate a reward system against an ethics checklist that covers stopping points, money, disclosure and worst cases.

**Before class:** Celia Hodent, *The Gamer's Brain* (CRC Press, 2017), the chapter "Motivation" (pp. 59-72), the section on extrinsic rewards and conditioning. The Wikipedia article "Reinforcement," section on schedules (short, and enough for the vocabulary). David Zendle and Paul Cairns, "Video game loot boxes are linked to problem gambling: Results of a large-scale survey," *PLOS ONE* 13(11), e0206767 (2018), open access. Read the abstract, introduction and discussion.

**Prerequisites from earlier courses:** [UX201 week 4, Self-Determination Theory](w04-self-determination-theory.md). This week is the behaviourist view of the rewards that week 4 looked at from the motivation side. [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md), because a random ratio schedule is a geometric wait. [MA102 week 10, pseudo-random distribution and pity timers](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w10-pseudo-random-distribution-and-pity-timers.md), for the tools that cap the worst case. [MA101 week 6, rational functions and asymptotes](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w06-rational-functions-and-asymptotes.md), because the discount curve `1 / (1 + kD)` is one. [GS101 week 11, free-to-play, mobile and live service](../../GS101-history-and-critical-study-of-games/lectures/w11-free-to-play-mobile-and-live-service.md), for the business history behind loot boxes.

**Interactive:** [Fixed vs random reward schedules](../examples/w05-schedule-response.html). Use it during section 2.

---

## 1. Schedules of reinforcement

In **operant conditioning**, a behaviour followed by a reward, called a **reinforcer**, becomes more frequent. B. F. Skinner and Charles Ferster spent years studying what happens when the reinforcer doesn't follow every response, and published the results in *Schedules of Reinforcement* (1957). Their subjects were mostly pigeons pecking keys for grain. The patterns they found show up in people, and in games, with surprising faithfulness.

A **schedule** is the rule that decides which responses get reinforced. The four basic ones cross two questions. Does the reward depend on the *number* of responses (ratio) or on *time* passing (interval)? And is the requirement *fixed* or *variable*?

| Schedule | Rule | Game example | Typical pattern |
|---|---|---|---|
| Fixed ratio (FR) | Every `n`th response | "Kill 10 wolves" quest; 100 reputation tokens buy the mount | Pause after each reward, then a steady run to the next |
| Variable ratio (VR) | On average every `n`th, unpredictably | Random loot drops; opening a loot box | High, steady rate; no pause after rewards; most resistant to extinction |
| Fixed interval (FI) | First response after a fixed time | Daily quest reset; a crop that ripens in 4 hours | Little activity early, rising towards the end of the interval |
| Variable interval (VI) | First response after an unpredictable time | A rare creature that spawns at a random time; random world events | Steady, moderate checking |

Three terms from the laboratory matter for games.

- The **cumulative record** is Skinner's plot. The x axis is time, the y axis is total responses so far. A steep line means fast responding. A flat stretch is a pause.
- The **post-reinforcement pause** is the flat stretch after each reward on a fixed schedule. On fixed ratio schedules, the pause grows with the size of the upcoming requirement. The subject is pausing before the next job, not resting after the last one.
- **Extinction** is what happens when reinforcement stops completely. The behaviour eventually dies out. Behaviour learned on a variable schedule takes much longer to die out than behaviour learned on a fixed one. This is the **partial reinforcement extinction effect**.

A pure random draw with the same chance every time, like a drop roll, is strictly a *random ratio* schedule, a special case of variable ratio. Game designers and most writing on loot boxes call it variable ratio, and so will we.

## 2. Worked example: why the loot box is variable

### The hook

In April 2018, Belgium's Gaming Commission finished a study of loot boxes in four games and concluded that the paid loot boxes in FIFA 18, Overwatch and Counter-Strike: Global Offensive were games of chance under Belgian gambling law. The Dutch Gaming Authority had reached a similar verdict on four games that same month. No regulator has ever investigated a "kill ten wolves" quest. Both systems reward play. Both can be tuned to pay out at the same average rate. So what does the random one do that the fixed one doesn't?

Players can tell you part of the answer without any theory. Turn in a ten-wolf quest and you often stop, check the map, maybe log off. Open a box and you open the next one. The model below explains why, and puts numbers on it.

### The model

Behavioural researchers describe how much a delayed reward is worth now with a **hyperbolic discount**, the rule James Mazur and others have used to predict how pigeons choose between delayed rewards. A reward of size `A` that arrives after a delay `D` is worth

```
V = A / (1 + k × D)
```

- `A` is the reward's value when it arrives. We use 100 as an arbitrary unit.
- `D` is the delay, measured here in **actions still needed**, counting the next one. A reward the next action will surely deliver has `D = 1`.
- `k` is how steeply the player discounts. At `k = 0`, a reward is worth the same however far away it is. Larger `k` means a distant reward is worth much less.

You met this shape in MA101 week 6. It is a rational function, highest at `D = 0` and falling towards zero without reaching it.

When the delay is uncertain, the value of the next action is the **average of the discounted values**, taking every delay that could happen weighted by its probability. That is the rule Mazur tested on pigeons choosing between fixed and variable schedules.

```
V = Σ  P(D = d) × A / (1 + k × d)
```

Apply it to two schedules with the same mean ratio `N = 10`, one reward per ten actions on average.

- **FR 10.** After `j` actions since the last reward, the delay is certain, `D = 10 − j`. So `V_j = 100 / (1 + k × (10 − j))`.
- **VR 10 (random).** Every action has a 1-in-10 chance. From MA102 week 7, the wait is geometric, `P(D = d) = 0.1 × 0.9^(d−1)`, and it is **memoryless**. The value is the same after every action, whether you just got a drop or not.

Add one behavioural rule. The player pauses before each action for a time proportional to `1 / V`. We use `pause = 100 / V` seconds, plus one second to do the action. A player also decides whether to **stop**, meaning take a break or end the session, at a **decision point** right after each reward. They stop there if `V` is below `θ`, the value of the best other thing they could be doing. Both players have already chosen to start the session, so the first decision point is the first reward.

The model is a teaching simplification. Real delays are in time rather than actions, and real fixed-ratio pauses look more like a flat break followed by a fast run than the smooth slope this model gives. It gets the direction right, though. The longest pause comes right after the reward, and the pause grows with the size of the ratio.

### Numbers you can check

With `k = 1`, the FR 10 player's value of the next action climbs through the cycle:

| Actions since reward `j` | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| Delay `D` | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 |
| FR value `V_j` | 9.09 | 10.0 | 11.1 | 12.5 | 14.3 | 16.7 | 20.0 | 25.0 | 33.3 | 50.0 |
| FR pause (s) | 11 | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 |

Check one cell. At `j = 3`, `D = 7`, so `V = 100 / 8 = 12.5`, and the pause is `100 / 12.5 = 8` seconds.

The VR 10 value is the sum `Σ 0.1 × 0.9^(d−1) × 100 / (1 + d)`. The first three terms are `0.1 × 50 = 5.00`, `0.09 × 33.3 = 3.00` and `0.081 × 25 = 2.03`, and the whole sum comes to **17.32**. The VR pause is `100 / 17.32 = 5.78` seconds, the same after every action.

Now compare the two schedules on the questions that matter.

| Question | FR 10 | VR 10 |
|---|---|---|
| Value right after a reward | 9.09 | 17.32 |
| Longest pause | 11 s, right after each reward | 5.78 s, never longer |
| Time for 10 actions | 65 s of pauses + 10 s = 75 s | 10 × 6.775 = 67.8 s on average |
| Actions per minute | 8.0 | 8.86 |
| Stops if `θ = 12`? | Yes, right after the first reward (`V = 9.09 < 12`) | Never (`V = 17.32 > 12`) |

The VR player is about 11% faster, which matches the laboratory finding that variable ratio schedules produce the highest steady rates. That is not the big difference, though. Look at the last row, which explains the hook. The rates are close, but the fixed schedule contains a **natural stopping point**, the moment after each reward when the next one is as far away as it will ever be. On the random schedule, that moment never comes. Right after a drop, the next drop is exactly as close as it was before. Any player whose alternatives are worth between 9.09 and 17.32 stops on the fixed schedule and keeps going on the variable one. Over a whole session, the fixed player meets a decision point with a low value every ten actions. The random player meets decision points too, after every drop, but the value there is the same 17.32 as everywhere else, so none of them is a natural place to stop.

The gap grows as rewards get rarer. The value right after a reward, `k = 1`:

| Mean ratio `N` | FR value after reward `100/(1+N)` | VR value | VR ÷ FR |
|---|---|---|---|
| 5 | 16.7 | 25.3 | 1.52 |
| 10 | 9.09 | 17.3 | 1.90 |
| 20 | 4.76 | 11.3 | 2.38 |
| 50 | 1.96 | 6.11 | 3.11 |
| 100 | 0.99 | 3.69 | 3.73 |

A rare, valuable prize is exactly where a variable schedule outperforms a fixed one most. Under a fixed schedule, a 1-in-100 prize would mean a certain grind of 100 steps and a deep valley after each reward. Under a random one, the next action always carries a real chance of the prize. The reason is in the curve's shape. Short delays are worth much more than long ones lose, so averaging over a spread of delays beats the fixed delay at the mean. Pigeons show the same preference. Offered a fixed or a variable delay with the same average, they usually choose the variable one.

### Extinction: how long until the player notices?

Suppose the rewards stop entirely, whether by a bug, a nerf or the end of an event. How many empty actions before a player can be sure?

- On FR 10, the eleventh unrewarded action is impossible under the old rule. The player knows at once.
- On VR 10, a player might reasonably conclude something has changed when a dry streak becomes less than 5% likely. `0.9^m < 0.05` first holds at `m = 29`. It takes about three times the mean ratio before the evidence is clear.
- On a 1% drop, `0.99^m < 0.05` needs `m = 299`.

That is the partial reinforcement extinction effect, rewritten in MA102 week 7's terms. Long dry streaks are normal on a random schedule, so their absence of reward carries little information. The player keeps going through exactly the stretches that would end a fixed-schedule player's session.

### A visual you can move

Open `examples/w05-schedule-response.html`. The top chart is the cumulative record, total actions over ten minutes for an FR player and a VR player with the same mean ratio. The two lines end at almost the same height. The FR line has a visible slow patch after every reward tick, and the VR line is straight. The bottom chart shows the thing the top one hides, the value of the next action. The FR value is a sawtooth that drops to 9.09 after every reward. The VR value is a flat line at 17.32. Drag the stop threshold `θ` up from 5. At 9.1 the FR player starts stopping after every reward, and the VR player doesn't stop until `θ` passes 17.32. Then raise `N` and watch the sawtooth's valleys sink while the flat line falls much more slowly.

### Cross-game recognition

**Old School RuneScape (current game).** Abyssal demons drop the abyssal whip at a rate of 1 in 512. The mean wait is 512 kills. Half of players need more than 355 kills, and a player needs 1,533 dry kills before the streak falls below 5% probability. Players farm demons for hours at a steady pace and talk about being "dry," not about being done. That is VR behaviour, with the extinction numbers above scaled up by 50.

**Reputation and token vendors (World of Warcraft and most MMOs).** "Collect 100 tokens and buy the mount" is FR 100. The model predicts a slow start to each batch of tokens, a steady run as the purchase gets close, and a natural break once it is made. The stopping point is designed in.

**Hearthstone card packs.** Each pack is a random draw, but a pity timer guarantees a Legendary within a fixed number of packs (see MA102 week 10 for the numbers). In this lecture's terms, it is a VR schedule with an FR ceiling. It keeps the flat value line for most players and cuts off the worst dry streak. It does not add a natural stopping point, because the counter resets when the guarantee fires and the next pack is as close to a Legendary as ever.

**Slot machines.** The "Reinforcement" article's standard example of a VR schedule producing persistent responding. The difference from a drop table is the direction the money flows, which is the subject of the next section.

Four systems, one model. For any reward system, ask two questions. Is the number of actions to the next reward known or random? And where are the moments when the next reward is furthest away?

### Eyes-open design judgment

- **Variable schedules are not evil.** Random drops make ordinary play exciting, and a game where every reward is on a fixed schedule feels like a spreadsheet. Most good reward design mixes the two. Fixed schedules give goals you can plan around. Variable ones add surprise.
- **Stopping points are a feature.** A fixed schedule gives the player a moment to ask, "Do I want to keep going?" Designs that remove every such moment are building for session length, not for the player's choice. Week 4 called that thwarting autonomy.
- **Pity timers cap the pain, not the pull.** They fix the worst case (MA102 week 10), which is good, but they don't create a stopping point. If you want players to stop, you have to design the stop. That might be a daily cap, a session summary, or a reward that ends a loop.
- **Discount rate matters.** At `k = 0` the two schedules have equal value in the model. The variable schedule's advantage exists because players discount distant rewards, and it grows with `k`. Any group that discounts more steeply feels the pull more. That is one reason the checklist below asks about the audience.
- **Money changes the question.** A random drop paid for with play time and a random drop paid for with money use the same schedule. What they cost the player when the schedule works too well is not the same.

### Check yourself (worked example)

1. For FR 5 with `k = 1` and `A = 100`, list the value of the next action at `j = 0` to 4. The VR 5 value is 25.3. For which values of `θ` does the FR player stop after rewards while the VR player never stops?
2. A rare mount has a 1% drop chance per weekly boss kill. How many weeks of dry kills does it take before the streak has less than a 5% chance of happening? What does this imply for a player trying to tell whether the drop was secretly removed?
3. With `k = 0`, compute the FR 10 and VR 10 values of the next action. What does the result say about where the variable schedule's advantage comes from?

<details>
<summary>Answers</summary>

1. `D` = 5, 4, 3, 2, 1, so `V` = 16.7, 20.0, 25.0, 33.3, 50.0. The FR player stops after rewards for any `θ` above 16.7, and the VR player never stops while `θ` is below 25.3. So `16.7 < θ < 25.3`.
2. `0.99^m < 0.05` gives `m = 299` weeks, almost six years. Players on a rare random drop cannot detect its removal from their own results, so the designer carries all the responsibility for telling them, which is one argument for published odds.
3. Both are 100. With no discounting, every delay is worth the same, so the spread of delays doesn't matter. The advantage comes entirely from discounting, from near rewards being worth much more than far ones.

</details>

## 3. When a schedule becomes a problem

Everything in section 2 applies equally to a random drop from a monster and to a random item from a paid box. The ethics depend on what the player puts in, what they can see, and who they are.

### What the research shows

Zendle and Cairns (2018) surveyed 7,422 gamers and found a link between the amount spent on loot boxes and the severity of problem gambling, with an effect size of `η² = 0.054`. That means loot box spending accounts for about 5.4% of the variance in problem gambling scores. The link between problem gambling and spending on other in-game items was far weaker, `η² = 0.004`. The authors argue that the gambling-like features of loot boxes, not spending in general, drive the relationship. They are explicit about what they can't say. A survey can't tell whether loot boxes lead people towards problem gambling, or whether people who already gamble heavily are drawn to loot boxes. A later meta-analysis of 15 studies (Garea and colleagues) found loot box spending and problem gambling symptoms moderately correlated.

Two cautions. Correlation at population scale says nothing about any single player. And "moderate" still means most of the variance is explained by other things. Neither caution makes the finding go away.

### What regulators did

| Date | Where | What |
|---|---|---|
| May 2017 | China | Online games must publish the draw probabilities of random items (announced December 2016). |
| December 2017 | Apple App Store | Games with paid random items must disclose the odds before purchase. |
| April 2018 | Netherlands | Gaming Authority finds four games' loot boxes with transferable items violate gambling law; eight weeks to comply. |
| April 2018 | Belgium | Gaming Commission rules paid loot boxes in FIFA 18, Overwatch and CS:GO are games of chance. Several publishers remove paid boxes for Belgian players. |
| April 2020 | PEGI (Europe) | Adds the notice "Includes Paid Random Items." |
| February 2023 (enforced March 2024) | South Korea | Law requires published odds, with fines for non-compliance. |

Rules keep changing, and enforcement is uneven. A 2023 study by Leon Xiao found that in July 2022, 82 of the 100 highest-grossing iPhone games in Belgium were still selling loot boxes despite the ban. MMO403 weeks 6 and 7 cover the current state of regulation in detail (see the [MMO403 syllabus](../../MMO403-business-monetization-and-ethics-of-live-games/syllabus.md)). For this course, the point is that regulators across very different legal systems looked at the same mechanism and found the same features worrying. The prize is random, the player pays real money for the draw, and the odds are hidden.

### An ethics checklist for any reward schedule

Use this in design reviews and in the lab. Each question maps to a part of the model.

1. **Stopping points.** Where does the value of the next action dip? If nowhere, what gives the player a moment to choose to stop? (Section 2's `θ` test.)
2. **Money in.** Can real money buy a draw directly, or through a currency that money buys? If yes, every problem in this section applies.
3. **Disclosure.** Are the odds published where the player makes the choice, in a form they can use, such as "1 in 200" rather than "0.5%"?
4. **Worst case.** What is the 95th-percentile cost of getting the prize (MA102 week 7)? Is there a cap, and is the cap published?
5. **Audience.** Will minors play? Regulators single them out, and they have less control over spending than adults.
6. **Exit.** If the player stops, what do they lose? A streak, a pity counter that resets, a timed item? Losses on exit turn a reward schedule into a trap.
7. **Informational alternative.** Could the same moment reward skill or discovery instead (week 4)?

No single "yes" makes a design unethical. A clear set of them, such as money in, hidden odds, no cap, minors in the audience and a penalty for leaving, describes the systems that regulators have acted on.

## 4. Designing schedules on purpose

A few patterns follow from the model and hold up in shipped games.

- **Fixed goals with random texture.** A quest with a fixed requirement (FR) where each kill also rolls on a small random table. The FR structure gives planning and a stopping point. The VR layer keeps each action interesting.
- **Bad-luck protection that the player can see.** A visible counter turns a hidden worst case into a known one. It also gives back some of the information a pure random schedule removes.
- **Session-end rewards.** A reward for finishing a session, such as a summary, a rest bonus or a crafted item ready next time, puts a peak at a stopping point instead of inside the loop. World of Warcraft's rested experience (week 4) works this way.
- **Caps on randomness where money is involved.** If you sell randomness, publish odds, cap the worst case and prefer direct purchase of the item the player wants. Some of the publishers that faced Belgian rules removed paid random items there rather than change them. Plan for the stricter market from the start.

## In-class activity (25 minutes)

Groups of three. Each group takes one reward system from a game a group member has played recently.

1. **Classify (5 min).** Name its schedule (FR, VR, FI, VI, or a mix) and its mean requirement.
2. **Model (10 min).** Using `k = 1` and `A = 100`, compute the value of the next action right after a reward and just before the next one. If it is random, use the VR table in section 2 for the nearest `N`. Where are the stopping points?
3. **Audit (10 min).** Answer the seven checklist questions in section 3. Propose one change that adds a stopping point or removes a "yes" without cutting the system.

Expected output: the classification, two computed values, the seven answers and one proposed change with its cost.

## Common misconceptions

- **"The point of a variable schedule is a faster click rate."** Players do respond somewhat faster, about 11% in this model, and fastest of all schedules in the lab. But rate is the smaller effect. The differences that hold up are the missing post-reward pause, the absence of stopping points and the resistance to extinction.
- **"A pity timer fixes the ethics of loot boxes."** It caps the worst case, which helps. It does not add stopping points, disclose odds or remove money from the draw.
- **"Random drops and loot boxes are the same thing."** Same schedule, different stakes. The ethics depend on what the player pays for a draw and who the player is.
- **"If the average rate is fair, the player is treated fairly."** The average hides the spread. At a 1-in-512 rate, some players go past 1,500 kills. Publish the worst case, not only the mean.

## Check yourself

1. Classify each: (a) a harvest node that respawns 10 minutes after it is gathered; (b) a quest to gather 15 herbs; (c) a 2% chance that a chest contains a rare dye; (d) a world boss that appears at a random time between 2 and 6 hours after the last kill.
2. A designer changes a crafting upgrade from "100% success after 8 attempts' worth of materials" (FR 8) to "12.5% success per attempt" (VR 8). Using `k = 1`, compute the value of the next attempt right after a success before and after the change. The VR 8 value is 19.7. What will change in how players stop?
3. A mobile game sells a box with a 0.5% chance of a character. Rewrite the odds in the "1 in N" form, give the mean number of boxes to get the character, and compute how many boxes a player must open for the chance of still not having it to fall below 5%.
4. Answer the seven checklist questions for a game-wide 3% drop of a cosmetic pet from any monster, where the pet can't be bought or traded.

<details>
<summary>Answers</summary>

1. (a) Fixed interval. (b) Fixed ratio. (c) Variable ratio. (d) Variable interval.
2. FR 8 after a success: `100 / 9 = 11.1`. VR 8: 19.7 after every attempt. Players with alternatives worth between 11.1 and 19.7 used to stop after each success and now won't. Sessions get longer, and the upgrade no longer offers a natural pause.
3. 1 in 200. Mean 200 boxes. `0.995^m < 0.05` gives `m = 598` boxes.
4. Stopping points: none from the drop itself, but no loss on leaving. Money: no. Disclosure: depends. Recommend publishing "1 in 33". Worst case: 95th percentile about 99 kills (`0.97^m < 0.05`, `m = 99`). Audience: check. Exit: nothing lost. Informational alternative: possible, for example a pet for a feat. Few "yes" answers, so this is ordinary VR texture, not a concern.

</details>

## Lab hook

[Lab 05, reward schedule audit](../labs/lab05.md). You play a game of your choice for 60 minutes and log every reward event with its time and trigger. You classify each reward stream by schedule, feed the log into the starter script to plot the cumulative record and the value-of-next-action curve, and mark every natural stopping point. Then you run the seven-question ethics checklist and propose one change. Deliverable: the log, the plots and a two-page audit.

## Sources

- Ferster, C. B. & Skinner, B. F. (1957). *Schedules of Reinforcement*. Appleton-Century-Crofts. Summary of schedule effects (post-reinforcement pause on fixed schedules as a function of the upcoming requirement; high, steady VR responding; greatest resistance to extinction on VR; the partial reinforcement extinction effect; slot machines as the standard VR example) via Wikipedia, "Reinforcement" (accessed September 2026).
- Mazur, J. E. (1986). "Fixed and variable ratios and delays: further tests of an equivalence rule." *Journal of Experimental Psychology: Animal Behavior Processes*, 12(2), 116-124 (PubMed 3701262). Pigeons' choices between fixed and variable ratios and delays; the equivalence rule of Mazur (1984).
- McSweeney, F. K., Kowal, B. P. & Murphy, E. S. (2003). "The effect of rate of reinforcement and time in session on preference for variability." *Learning & Behavior*, 31(3), 225-241 (PubMed 14577547). Pigeons usually preferred the variable option over a fixed one with the same arithmetic mean. Orduña, V. & Bouzas, A. (2004), *Behavioural Processes* 67(2), 147-156 (PubMed 15240052): preference for variability explained by models based on temporal proximity to the reinforcer.
- Wikipedia, "Hyperbolic discounting" (accessed September 2026). The discount factor `1 / (1 + kD)`.
- Zendle, D. & Cairns, P. (2018). "Video game loot boxes are linked to problem gambling: Results of a large-scale survey." *PLOS ONE* 13(11): e0206767. n = 7,422; η² = 0.054 for loot box spending against 0.004 for other in-game spending; direction of causation unknown.
- Garea, S. et al. (2021). "Meta-analysis of the relationship between problem gambling, excessive gaming and loot box spending." *International Gambling Studies*, 21(3), 460-479. 15 studies, moderate positive correlation. Via Wikipedia, "Loot box."
- Wikipedia, "Loot box" (accessed September 2026). China's disclosure rule (announced December 2016, from May 2017); Apple's December 2017 App Store rule; the Dutch Gaming Authority's April 2018 findings; the Belgian Gaming Commission's April 2018 ruling on FIFA 18, Overwatch and CS:GO and publishers' responses; PEGI's April 2020 "Includes Paid Random Items" notice; South Korea's February 2023 law with enforcement from March 2024; Xiao (2023), 82 of the top 100 grossing iPhone games in Belgium still selling loot boxes in July 2022.
- Xiao, L. Y. (2023). "Breaking Ban: Belgium's Ineffective Gambling Law Regulation of Video Game Loot Boxes." *Collabra: Psychology*, 9(1), 57641. doi:10.1525/collabra.57641. Abstract checked via Crossref (September 2026): 82.0% of the 100 highest-grossing iPhone games in Belgium still used paid randomised monetisation.
- Old School RuneScape Wiki, "Abyssal demon," drop table (current game, accessed September 2026). Abyssal whip at 1/512.
- Hearthstone Wiki (hearthstone.wiki.gg), "Card pack" (accessed September 2026). Guaranteed rarities within a fixed number of packs. Figures as given in MA102 week 10.
- Hodent, C. (2017). *The Gamer's Brain*. CRC Press. Chapter "Motivation" (pp. 59-72).
- The value-of-next-action model with delay counted in actions, the pause rule `100 / V`, the stop threshold `θ` and the ethics checklist are this course's own teaching models.

## Interactive spec: examples/w05-schedule-response.html

**Purpose.** Show that fixed and variable ratio schedules with the same mean produce similar totals but different moment-to-moment value, and that only the fixed schedule has natural stopping points.

**The one insight the visual must make obvious.** In the bottom chart, the FR value is a sawtooth that dips to its minimum after every reward, while the VR value is a flat line above that minimum. When the threshold `θ` sits between them (default 12), the FR player's line in the top chart stops after the first reward while the VR player's line keeps climbing.

**Layout.** Two charts stacked (top and bottom) at all widths, sharing a legend. Controls and a numbers panel below at 390px, to the right at 1280px.

- Top, "Cumulative record": x axis time 0 to 600 s, y axis total actions. One line per schedule (FR, VR). Small tick marks on each line at reward events. If a player stops (value below `θ`), their line ends with a labelled "stops" marker. Toggle "ignore stopping" to draw both lines for the full 600 s.
- Bottom, "Value of the next action": x axis actions 0 to 60, y axis 0 to 100 (or auto). FR as a sawtooth (step at each action), VR as a horizontal line. A dashed horizontal line at `θ`, labelled. Shade FR segments below `θ` as "natural stopping points".

**Controls.**

- Mean ratio `N`: 2 to 100 (integer), default 10.
- Discount `k`: 0 to 2, step 0.05, default 1.
- Reward `A`: fixed at 100 (display only).
- Stop threshold `θ`: 0 to 60, step 0.1, default 12.
- Pause constant `c`: 20 to 300, default 100 (pause = `c / V` s); action time 1 s fixed.
- Random seed for VR reward positions (number input, default 7), plus a "reroll" button. Only the tick positions depend on the seed; the VR value and pace do not.
- Toggle "ignore stopping".
- Presets: "Default (N = 10, θ = 12)", "Rare prize (N = 100)", "No discounting (k = 0)", "FR 5 check (N = 5, θ = 20)".
- Reset.

**Formulas.**

- FR value at `j` actions since reward (`j = 0..N−1`): `V_j = A / (1 + k × (N − j))`.
- VR value: `V = Σ_{d=1}^{∞} p (1 − p)^(d−1) × A / (1 + k × d)` with `p = 1/N`. Sum until the term is below 1e-9 (cap at 100,000 terms).
- Pause before an action = `c / V` s; action time 1 s. FR: time per cycle = `Σ_j (c / V_j + 1)`. VR: time per action = `c / V + 1`.
- Stopping: both players start the session. Each reward is a decision point, and a player stops at the first decision point where the value of the next action is below `θ`. FR: stops right after the first reward if `V_0 < θ`. VR: stops right after its first reward if `V < θ`, else never. Unless "ignore stopping" is on, the numbers panel reports "after 1st reward" or "never" for each.
- Extinction line in the numbers panel: FR "notices after N + 1 unrewarded actions"; VR "5% dry streak after m actions", `m = ceil(ln 0.05 / ln(1 − p))`.

**Numbers panel.** FR value after a reward, FR value before a reward, FR mean pause, VR value, VR pause, actions per minute for each, VR ÷ FR value after reward, whether each player stops at `θ`, and the two extinction numbers.

**Test values** (`A = 100`, `c = 100`).

- `N = 10`, `k = 1`: FR values 9.09, 10.00, 11.11, 12.50, 14.29, 16.67, 20.00, 25.00, 33.33, 50.00. VR 17.32. FR pauses 11 down to 2 s, cycle 75 s (65 s of pauses plus 10 s of actions), 8.0 actions/min. VR pause 5.78 s, 8.86 actions/min (60 / 6.775 = 8.856). `θ = 12`: FR stops after the first reward, VR never. Extinction: FR 11, VR 29.
- `N = 5`, `k = 1`: FR after reward 16.67, VR 25.29.
- `N = 20`: FR 4.76, VR 11.33. `N = 50`: FR 1.96, VR 6.11. `N = 100`: FR 0.99, VR 3.69, ratio 3.73. Extinction for `N = 100`: VR 299.
- `k = 0`: every value 100 for both schedules.
- `k = 0.5`, `N = 10`: FR after reward 16.67, VR 27.37.
- `N = 8`, `k = 1`: FR after reward 11.11, VR 19.66 (end-of-lecture Check yourself, question 2).

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark. FR and VR differ by line style (solid and dashed) and marker shape as well as colour. The stopping-point shading uses a hatch pattern. All controls keyboard operable with visible values. Respect reduced motion (no animated drawing of the cumulative record when set; otherwise a short draw-in is allowed but the final frame must be readable at once). No game art, logos, slot machine imagery or loot box art; label the schedules "fixed (every Nth action)" and "random (1 in N chance each action)".
