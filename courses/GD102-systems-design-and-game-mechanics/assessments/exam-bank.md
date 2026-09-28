# GD102 · Exam bank: quiz, practice and viva questions

GD102 has no written exam. The grade comes from the Machinations models and exercises (30%, [machinations-models-brief.md](machinations-models-brief.md)), the economy design (30%, [economy-design-brief.md](economy-design-brief.md)) and the final system design document with its simulation (40%, [final-sdd-brief.md](final-sdd-brief.md)). This bank has three other jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab will go quickly.
- **Weekly quizzes.** Most weeks open with a 10-minute ungraded quiz of two or three questions from this bank, usually one compute question and one explain or critique question.
- **Viva and spot checks.** The model review in week 12 and the viva at the end of the final SDD presentation draw questions in the style of this bank. Examiners rewrite them with the numbers from your own diagram, sheet or document.

Every question is tagged with the week or weeks it draws on and a type.

- **compute**: apply a lecture model to numbers you have not seen before.
- **explain**: say why a model behaves the way it does, with a number as evidence.
- **design**: choose values that meet a stated goal and show that they meet it.
- **critique**: find what is wrong with a proposal and say how to fix it.

All numbers are fictional unless a question names a game. Every game fact used here comes from the lecture of the tagged week, which cites its source and version, and no question relies on a game fact the lectures do not state. Answers were recomputed in Python. Where rounding matters, the solution says how it was rounded. Write your own answer before you open the solution.

---

## Week 1: Systems thinking

1. *Week 1 · compute.* A game has seven elements with degrees 4, 3, 3, 2, 2, 1 and 1 in its interaction graph. (a) How many rules does it have? (b) How many two-step chains? (c) The designer adds a rule between the degree-4 element and one of the degree-1 elements. How many new chains does it create? Confirm by recounting.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 8 rules. (b) 14 chains. (c) 5 new chains, for a total of 19.

(a) Degrees add to `4 + 3 + 3 + 2 + 2 + 1 + 1 = 16`, which is twice the number of rules, so `E = 8`.

(b) `C2 = Σ d(d − 1)/2 = 6 + 3 + 3 + 1 + 1 + 0 + 0 = 14`.

(c) New chains `= d(u) + d(v) = 4 + 1 = 5`, using degrees before the addition. Recount: the degrees become 5, 3, 3, 2, 2, 2, 1, so `C2 = 10 + 3 + 3 + 1 + 1 + 1 + 0 = 19 = 14 + 5`.
</details>

2. *Week 1 · compute.* You have nine elements and a budget of eight rules. Compare two layouts. In the star, one hub element has a rule with each of the other eight. In the path, the elements form a chain a–b–c–...–i. Then give the rule count and chain count if every pair of the nine elements were linked, and the chains per rule in that complete graph.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Star, 8 rules and 28 chains. Path, 8 rules and 7 chains. Complete graph, 36 rules, 252 chains, 7 chains per rule.

Star: the hub has degree 8 and the leaves degree 1, so `C2 = 8 × 7 / 2 = 28`.

Path: the seven middle elements have degree 2 and the two ends degree 1, so `C2 = 7 × 1 = 7`.

Complete graph with `n = 9`: `E = 9 × 8 / 2 = 36` and `C2 = 9 × 8 × 7 / 2 = 252`. Each rule is worth `n − 2 = 7` chains.

The same eight rules give four times as many chains when they meet at a hub. That is the week 1 argument for choosing hubs on purpose.
</details>

3. *Week 1 · explain.* A causal loop in a dungeon game has four links. More player gold (+) better gear. Better gear (−) fewer deaths per hour. More deaths (+) higher repair bills. Higher repair bills (−) less player gold. Is the loop reinforcing or balancing? Describe what it predicts for a player who starts slightly rich, and name one link you could add to stop it running away.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Reinforcing. Two minus signs is an even count.

Trace it. More gold buys better gear, which means fewer deaths, which means lower repair bills, which leaves more gold. A player who starts slightly rich gets richer, and a player who starts slightly poor gets poorer, because the same loop runs backward for them.

Two minus signs cancel. Beginners often call this loop balancing because it "has negatives in it". Count them.

To stop it running away, add a link with an odd number of minus signs around a new loop, for example a repair cost that scales with gear quality (better gear (+) repair bill per death). Now more gold also raises the cost of each remaining death, which pushes back.
</details>

4. *Week 1 · critique.* A designer says: "Our crafting system has 60 recipes, so it is deep." In the prototype, 50 recipes each take one ingredient used nowhere else, and 10 recipes all use iron. Using the chain model, where is the depth, and what would you ask the designer to change?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Almost all the depth is in iron. Iron has degree 10 and sits in the middle of `10 × 9 / 2 = 45` chains. The 50 single-use ingredients have degree 1 and add no chains through themselves.

Recipes are rules. The recipe count is `E`, and `E` does not measure play. The chains measure how many ways rules meet, and those come from shared elements.

Ask for the degree of every ingredient and output. To add depth, make some outputs inputs to other recipes and let a few more ingredients be shared. Each new rule on iron adds `10 + d` chains. Each new single-use recipe adds `1 + 1 = 2` at most. Also warn the designer that 45 chains through one element are 45 test cases and one likely dominant material.
</details>

## Week 2: Stocks and flows

5. *Week 2 · compute.* A stamina system restores 1 point every 8 minutes up to a cap of 90. (a) What is `T_fill`? (b) What share of inflow does a player waste who returns every 16 hours and spends everything? (c) Every 20 hours?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 12 hours. (b) 25%. (c) 40%.

(a) The inflow is `60 / 8 = 7.5` points per hour, so `T_fill = Cap / i = 90 / 7.5 = 12` hours.

(b) `W(N) = max(0, 1 − Cap / (i × N)) = 1 − 90 / (7.5 × 16) = 1 − 90/120 = 25%`.

(c) `1 − 90 / (7.5 × 20) = 1 − 90/150 = 40%`.

The cap asks for a 12-hour return. Past that, every extra hour away costs 7.5 points of inflow that never arrive.
</details>

6. *Week 2 · compute.* A frontier camp gains 250 settlers per day and loses 4% of its population per day. It starts empty. (a) What is the equilibrium population? (b) Step the population through days 1, 2 and 3. (c) Roughly how many days until it is halfway to equilibrium?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 6,250. (b) 250, 490, 720.4. (c) About 17 days.

(a) `S* = I / r = 250 / 0.04 = 6,250`.

(b) Use `S[t+1] = S[t] + I − r × S[t]`. Day 1: `0 + 250 − 0 = 250`. Day 2: `250 + 250 − 10 = 490`. Day 3: `490 + 250 − 19.6 = 720.4`.

(c) The gap to equilibrium shrinks by 4% a day, so it halves when `0.96^t = 0.5`, `t = ln 0.5 / ln 0.96 ≈ 17.0` days.
</details>

7. *Weeks 2 and 13 · compute.* Use the World of Warcraft rested figures from the week 2 lecture (retail, Dragonflight-era wiki page). A character logs out outside a rest area with an empty pool. (a) What is `T_fill`? (b) The player returns after 50 days. How much inflow was lost to the cap, and what is `W(50)`? (c) A designer wants the outside rate to fill the pool in 20 days instead. How many hours per bubble is that?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 40 days. (b) 37.5% of a level lost, `W = 20%`. (c) One bubble per 32 hours.

(a) Outside a rest area one bubble (10% of a level) arrives every 64 hours, which is `10% × 24/64 = 3.75%` per day. The cap is 150%, so `T_fill = 150 / 3.75 = 40` days.

(b) Inflow over 50 days is `3.75 × 50 = 187.5%`. The pool holds 150%, so 37.5% is lost. `W = 1 − 150 / 187.5 = 20%`.

(c) Filling 150% in 20 days needs 7.5% per day. One 10% bubble then takes `10 / 7.5 = 1.33` days, which is 32 hours. The knee in week 13's language moves from 40 days to 20.
</details>

8. *Week 2 · design.* A mobile puzzle game uses a lives stock with a cap of 6. The team wants `T_fill` to be exactly 4 hours. (a) How often must one life return? (b) What share of inflow does a player waste who returns every 5 hours and spends every life? (c) Say in one sentence what appointment this system asks for.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) One life every 40 minutes. (b) 20%. (c) It asks the player to come back at least every 4 hours.

(a) `i = Cap / T_fill = 6 / 4 = 1.5` lives per hour, one life per 40 minutes.

(b) `W(5) = 1 − 6 / (1.5 × 5) = 1 − 6/7.5 = 20%`.

(c) A player who returns every 4 hours or sooner loses nothing, so the design rewards three or four short sessions across a waking day.
</details>

## Week 3: Positive feedback loops

9. *Week 3 · compute.* Workers each earn 6 minerals per turn, and a new worker costs 40 minerals. Players reinvest everything. (a) What are `r` and the doubling time? (b) Player A starts with 12 workers and B with 9. What is B's time lead, in turns? (c) What are the gap and the ratio after 10 turns?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `r = 0.15`, `t_2 ≈ 4.96` turns. (b) About 2.06 turns. (c) Gap about 12.1 workers, ratio still 1.33.

(a) `r = 6 / 40 = 0.15`. `t_2 = ln 2 / ln 1.15 = 0.693 / 0.140 = 4.96` turns.

(b) `Δt = ln(A0 / B0) / ln(1 + r) = ln(12/9) / ln 1.15 = 0.288 / 0.140 = 2.06` turns.

(c) `G[10] = (12 − 9) × 1.15^10 = 3 × 4.046 = 12.1` workers. The ratio is `12/9 = 1.33` at every turn of an independent loop. The scoreboard gap quadruples. B is still two turns behind.
</details>

10. *Week 3 · compute.* Two players are coupled by the zero-sum model with raid rate `c = 0.08`. A starts with 15 and B with 10. (a) What is the total, and how fast does the gap grow? (b) Give A, B and the ratio at turn 5. (c) When is B eliminated?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Total 25, gap grows 16% per turn. (b) A 17.75, B 7.25, ratio 2.45. (c) At `t ≈ 10.8`, so during turn 11.

(a) Each turn A gains `c × A − c × B` and B loses the same, so `A + B = 25` forever. The gap grows by `1 + 2c = 1.16` per turn: `G[t] = 5 × 1.16^t`.

(b) `G[5] = 5 × 1.16^5 = 10.50`. With the total fixed, `A = (25 + 10.50)/2 = 17.75` and `B = (25 − 10.50)/2 = 7.25`. Ratio `17.75 / 7.25 = 2.45`, up from 1.5.

(c) B reaches zero when the gap equals the total: `5 × 1.16^t = 25`, so `t = ln 5 / ln 1.16 = 1.609 / 0.148 = 10.8`. Stepping the recurrence confirms it: after turn 10, B has 1.47 and after turn 11 it would be negative.
</details>

11. *Week 3 · compute.* Two independent economies grow with `r = 0.2` per turn and share a cap of 100. A starts at 20 and B at 15. (a) On which turn does each reach the cap? (b) When is A's lead largest, and how large is it? (c) What is the gap two turns after that?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) A on turn 9, B on turn 11. (b) Turn 9, 22.6. (c) 0 by turn 11.

(a) A reaches 100 when `20 × 1.2^t ≥ 100`, `t = ln 5 / ln 1.2 = 8.83`, so on turn 9. B needs `t = ln(100/15) / ln 1.2 = 10.4`, so turn 11.

(b) Stepping: turn 8, A 86.0 and B 64.5 (gap 21.5). Turn 9, A is capped at 100 and B is 77.4 (gap 22.6). Turn 10, B is 92.9 (gap 7.1).

(c) Turn 11, both at 100. A's biggest lead lasts one turn. If A has not converted it into another stock (army, tech, map control) by turn 10, it is gone.
</details>

12. *Week 3 · critique.* A strategy game has loop gain `r = 0.10` per turn and matches of about 30 turns. A designer proposes doubling every player's starting workers "so the early game runs twice as fast". What does the model predict this change does, in turns, and what does it leave unchanged?

<details>
<summary>Answer and worked solution</summary>

**Answer:** It skips exactly one doubling time, about 7.3 turns. Everything after that runs as before.

With `S[t] = S[0] × 1.1^t`, doubling `S[0]` gives the same curve shifted left by `t_2 = ln 2 / ln 1.1 = 7.27` turns. The early turns where little happens are removed. The ratio between players and their time lead do not change, and the rate of play after the skip is unchanged.

So the game does not run twice as fast. It starts about a quarter of a 30-turn match later on the same curve. If the goal was to cut dead time at the start, that is a fair change. If the goal was faster pacing throughout, the knob is `r`, and raising it also shortens the time before any coupling decides the match. The week 3 lecture's note on StarCraft II (Legacy of the Void raised starting workers) makes the same reading.
</details>

## Week 4: Negative feedback loops

13. *Week 4 · compute.* A leader gains `d = 1.5` m/s on a chaser, and the catch-up rule recovers `k = 0.3` of the gap each second. (a) What gap does the race settle at? (b) Starting from zero, give the gap after seconds 1, 2 and 3, and check second 3 with the closed form.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 5 m. (b) 1.5, 2.55, 3.285 m.

(a) `g* = d / k = 1.5 / 0.3 = 5` m.

(b) `g(t+1) = g(t) + d − k × g(t)`. Second 1: `0 + 1.5 − 0 = 1.5`. Second 2: `1.5 + 1.5 − 0.45 = 2.55`. Second 3: `2.55 + 1.5 − 0.765 = 3.285`.

Closed form: `g(3) = 5 × (1 − 0.7^3) = 5 × 0.657 = 3.285`. They agree.
</details>

14. *Week 4 · compute.* Set `d = 0` and a starting gap of 12 m. Give the first four values of the gap for `k = 1.25` and for `k = 2.2`. Say which of the two settles, and describe what each looks like in a race.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `k = 1.25`: 12, −3, 0.75, −0.19. `k = 2.2`: 12, −14.4, 17.28, −20.74. The first settles and the second blows up.

The update is `g(t+1) = (1 − k) × g(t)`. For `k = 1.25` the factor is −0.25, negative and smaller than 1 in size. The chaser overtakes, the lead flips sign every second, and the swings shrink toward zero. In a race, first place changes every second but the pack converges.

For `k = 2.2` the factor is −1.2. The flips grow by 20% each second. The correction is so strong that it throws each new leader further ahead than the last one was. Any `k` above 2 does this, and any `k` between 1 and 2 overshoots but settles.
</details>

15. *Week 4 · design.* A leader's natural edge is `d = 2.5` m/s. The team wants a steady gap of 10 m. (a) What `k` do they need? (b) Starting from zero, after how many whole seconds is the gap at least 90% of its steady value?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `k = 0.25`. (b) 9 seconds.

(a) `k = d / g* = 2.5 / 10 = 0.25`.

(b) The gap is `g* × (1 − 0.75^t)`. You need `0.75^t ≤ 0.1`, so `t ≥ ln 0.1 / ln 0.75 = 8.004`. After 8 seconds the gap is `1 − 0.75^8 = 89.99%` of 10 m, just short. After 9 seconds it is 92.5%. Rounding the log to 8 is the trap here.
</details>

16. *Week 4 · compute.* In a racer, the clean-track effect adds 4% of the gap per second (reinforcing) and the item box removes 3% of the gap per second (balancing). (a) Which loop dominates, and by how much does a gap change over 60 seconds? (b) A patch raises the item effect to 6%. Repeat. (c) What is the smallest item effect that makes the balancing loop dominate?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Reinforcing, net +1% per second. The gap grows to about 1.82 times in a minute. (b) Balancing, net −2% per second. The gap shrinks to about 0.30 of its size. (c) Anything above 4%.

(a) `1.01^60 = 1.82`.

(b) `0.98^60 = 0.30`.

(c) Dominance flips when the balancing rate passes the reinforcing rate. Nothing about the structure changed between (a) and (b). Only the relative strength did, which is Meadows's shifting dominance and the reason a small patch can change a game's character.
</details>

17. *Week 4 · critique.* A lead designer's brief for a party racer reads: "The halfway leader should win 30% to 40% of races, the best driver should win at least 45%, and there should be fewer than 25 lead changes per race." A teammate picks position mode at 50% because it "gives the closest races". Use the week 4 simulation table to judge the choice.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Position mode at 50% fails the brief. Distance mode at 50% meets it.

From the table: distance 50% gives a halfway-leader win rate of 33%, best driver 47% and 23 lead changes. All three conditions pass. Position 50% gives 34%, 47% and 28 lead changes, which fails the third condition. Its spread (21 m) is also slightly wider than distance mode's (19 m), so it is not even closer.

The teammate optimized the view players see (closeness) and ignored lead churn. Position mode pulls on the leader of a tight pack as hard as on a runaway leader, which is why it churns more at the same strength. Recommend distance mode at 50%, and ask whether the rule will be visible to players, since a hidden correction reads as the game cheating.
</details>

## Week 5: Machinations diagrams I

18. *Week 5 · compute.* A pool with capacity 12 starts at 3. An automatic source adds 0.75 per second and nothing is spent for 20 seconds. (a) When does the pool reach capacity? (b) How much is wasted by second 20? (c) Show the conservation check.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) At 12 seconds. (b) 6. (c) `3 + 15 = 12 + 6`.

(a) It needs 9 more at 0.75 per second, so `9 / 0.75 = 12` seconds.

(b) It sits at the cap for 8 seconds. `waste = rate × time at cap = 0.75 × 8 = 6`.

(c) `start + arrived = end + left + lost`: `3 + 0.75 × 20 = 18`, and `12 + 0 + 6 = 18`.
</details>

19. *Week 5 · compute.* In the course game *Lanes* (`r = 0.5` per second, `C = 10`, `p0 = 5`, 180-second match), a player only plays 5-cost cards and holds at the cap for 3 seconds before each play. (a) How long is one cycle, and how much is wasted per cycle? (b) How many cards are played, and how much is wasted over the match? (c) Show the conservation check.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 13 seconds, 1.5 elixir. (b) 13 plays, 20 wasted. (c) `5 + 90 = 65 + 20 + 10`.

(a) After a play the pool is at 5. Refilling 5 takes `5 / 0.5 = 10` seconds, then the hold adds 3. Waste per cycle is `0.5 × 3 = 1.5`.

(b) The pool first reaches 10 at 10 seconds, so plays happen at 13, 26, 39, ... The last that fits is `13 × 13 = 169`, so 13 plays. Waste: 13 holds of 1.5 is 19.5, plus the pool refills at 179 and sits at the cap for the final second, 0.5 more. Total 20.

(c) Generated `= 0.5 × 180 = 90`. Spent `= 13 × 5 = 65`. `5 + 90 = 95 = 65 + 20 + 10`. The waste is 22% of all generated elixir, from a habit of three seconds.
</details>

20. *Week 5 · compute.* Use the Hearthstone mana rules from the week 5 lecture. On turns 1 to 6 a player has 1 to 6 crystals and spends 1, 0, 3, 2, 5 and 6 mana. (a) How much mana was wasted over the six turns? (b) As a thought experiment (this is not a Hearthstone rule), suppose unspent mana carried over to the next turn with no cap, as the Slay the Spire Ice Cream relic does for energy. How much mana would the player have had on turn 3? Which node of the diagram did you delete?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 4 of 21. (b) 5 mana. You deleted the automatic end-of-turn drain.

(a) Waste per turn is crystals minus spent: `0, 2, 0, 2, 0, 0`. Total 4 out of `1 + 2 + ... + 6 = 21` available.

(b) Turn 2 left 2 unspent. With carry-over, turn 3 starts with `2 + 3 = 5`. The refill source is unchanged. The end-of-turn drain is what makes unspent mana certain waste, and removing it changes the resource from "use it this turn" to "save for a big turn".
</details>

21. *Week 5 · explain.* An interactive drain for a 4-cost card is connected to a pool holding 3. Say what happens when the player fires it with and without the all-or-nothing mark, and name two other rules in a game that must be all-or-nothing.

<details>
<summary>Answer and worked solution</summary>

**Answer:** With the mark, nothing moves and the pool keeps 3. Without it, the drain takes 3, the card is played without being paid for, and the model is wrong.

A pulling node without `&` takes whatever it can get. That is right for decay or theft ("lose up to 3") and wrong for any price. Rules that must be all-or-nothing include every purchase (a shop item, a building), every crafting recipe (a converter with several inputs), and firing a weapon that needs a full round.
</details>

## Week 6: Converters, traders, gates

22. *Week 6 · compute.* In the week 6 Catan model, a player has no ore hex. Their spare production is wool on 8 (5 pips), lumber on 6 (5 pips) and brick on 9 (4 pips), and grain comes from a 5 (4 pips). (a) Give the flow estimate for 3 ore at the 4:1 bank and at a 3:1 harbor. (b) How many rolls does 2 grain take? Which resource binds the city? (c) Will the simulated mean be higher or lower than your estimate, and why?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Bank about 30.9 rolls, harbor about 23.1 rolls. (b) 18 rolls, so ore binds either way. (c) Higher.

(a) Spare cards arrive at `5 + 5 + 4 = 14` pips per 36 rolls. At 4:1, ore arrives at `14/36 ÷ 4 = 3.5/36` per roll, so 3 ore takes `3 × 36 / 3.5 = 30.9` rolls. At 3:1, `14/36 ÷ 3 = 4.67/36`, so `3 × 36 / 4.67 = 23.1` rolls.

(b) `2 × 36 / 4 = 18` rolls.

(c) The flow estimate is a lower bound. Batching means spare cards sit idle below the ratio until four of one type pile up. And the hand needed to form batches passes 7 cards, so the discard on a 7 takes half of it. The bank path pays both costs more than the harbor path.
</details>

23. *Week 6 · critique.* The week 6 lecture cites Minecraft's recipe of 1 log into 4 planks. A modder proposes a reverse recipe, 3 planks into 1 log, "so players can undo mistakes". What does the loop of the two converters do? What is the smallest safe input for the reverse recipe?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Each loop creates one plank from nothing, an infinite source. The reverse recipe needs at least 4 planks.

Start with 1 log. Craft 4 planks. Convert 3 of them back into 1 log. You now hold 1 log and 1 plank. Repeat and the plank count grows by one per loop.

Two converters in a cycle conserve or destroy resources only if the product of their ratios is at most 1. Here `4 × (1/3) = 1.33`. With 4 planks per log the product is exactly 1, so the loop is neutral. With 5 it loses a plank per loop, which is the usual choice because it also makes "undo" cost something. Check every converter cycle in a diagram this way before it ships.
</details>

24. *Week 6 · compute.* A factory game uses the gear recipe from the week 6 lecture: 2 plates and 0.5 seconds make 1 gear. Treat each converter as working at exactly that speed. A belt delivers 30 plates per second. (a) How many plates does one converter use per second? (b) How many converters do you need so no plates pile up? (c) With one converter fewer, how fast does the backlog grow?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 4 plates per second. (b) 8 converters. (c) 2 plates per second, 120 per minute.

(a) One gear per 0.5 seconds is 2 gears per second, and each takes 2 plates.

(b) `30 / 4 = 7.5`, so 8 converters, one of them idle half the time.

(c) Seven converters use 28 plates per second, leaving 2 per second on the belt. A converter's throughput is its ratio and its speed together. The ratio alone does not tell you whether the line keeps up.
</details>

25. *Week 6 · compute.* A party of three splits loot with a deterministic gate weighted 2, 1, 1 (the first output gets two items, then the second one, then the third one, and it repeats). (a) After 18 items, how many has each player received? (b) What would a random gate with the same weights give on average? (c) Which gate would you use for a guild bank tax, and why?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 10, 4, 4. (b) 9, 4.5, 4.5. (c) Deterministic.

(a) One cycle is 4 items (2, 1, 1). Eighteen items are 4 full cycles (8, 4, 4) plus 2 more, and both of those go to the first output. So 10, 4, 4.

(b) Random: `18 × 2/4 = 9` and `18 × 1/4 = 4.5` each on average, with individual runs straying from that.

(c) A tax is a fixed share. Players can check a deterministic split exactly, and a random tax would sometimes take nothing and sometimes take everything, which reads as unfair.
</details>

26. *Week 6 · explain.* Your MMO has an NPC blacksmith who "trades" 200 gold for a sword, and an auction house where players buy swords from each other for gold. Which is a converter and which is a trader? Why does the answer matter for an inflation model?

<details>
<summary>Answer and worked solution</summary>

**Answer:** The blacksmith is a converter. The auction house (without any fee) is a trader.

The blacksmith's gold and swords are not tracked, so 200 gold leaves the game and a sword appears. That is a sink for gold. A player-to-player sale moves gold from buyer to seller and conserves the total. If you draw the blacksmith as a trader, your model misses a sink and overstates the money stock. If you draw the auction house as a converter, you invent a sink that does not exist. A quick test from the lecture: if you can only draw one owner's pools, it is a converter.
</details>

## Week 7: Internal economies

27. *Week 7 · compute.* Town D has `N = 300` players, a faucet of 90 gold per player per day, flat drains of 60, velocity `v = 0.2`, a market cut of 5% and `q = 8` potions per player per day. (a) Compute `s`, `M*`, equilibrium money per player and `P*`. (b) What is the half-life of a gap from equilibrium? (c) What does (b) mean for a designer watching a patch?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `s = 0.01`, `M* = 900,000`, 3,000 per player, `P* = 75`. (b) About 69 days. (c) The town takes months to show the full effect of any faucet change.

(a) `s = τ × v = 0.05 × 0.2 = 0.01`. `M* = N × (F − D) / s = 300 × 30 / 0.01 = 900,000`. Per player, 3,000. `P* = v × M* / (N × q) = 0.2 × 900,000 / 2,400 = 75`.

(b) `ln 0.5 / ln 0.99 = 69.0` days.

(c) A proportional drain this weak corrects slowly. A faucet mistake will look like inflation for the first month even though the town is heading to a new level. Either raise `τ` for faster correction, or judge patches on the computed `M*` rather than on the first weeks of price data.
</details>

28. *Week 7 · compute.* Town B from the lecture sits at equilibrium with `F = 100` (`M = 200,000`, price 60, `s = 0.03`, `D = 40`, `N = 100`, `q = 10`, `v = 0.3`). A patch raises the faucet to 120. (a) What are the new `M*` and `P*`? (b) What are the money stock and price on day 30? (c) Is this inflation?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 266,667 and 80. (b) About 239,933 and 71.98. (c) No. It is a one-time price-level rise of 33.3%.

(a) `M* = 100 × (120 − 40) / 0.03 = 266,667`. `P* = 0.3 × 266,667 / 1,000 = 80`.

(b) `M(30) = M* + (M(0) − M*) × 0.97^30 = 266,667 − 66,667 × 0.401 = 239,933`. Price `0.3 × 239,933 / 1,000 = 71.98`. Stepping the recurrence gives the same number.

(c) The price settles at 80 and stops. Inflation means prices that keep rising, which only happens here if the drain cannot respond to the stock.
</details>

29. *Week 7 · compute.* A flat-drain town (like town A) has `N = 100`, `F = 105`, `D = 100`, `M(0) = 200,000`, `v = 0.3`, `q = 10`. (a) How fast do money and price change? (b) What are they on day 180? (c) The designer sets `D = 106` to "fix it". What happens next?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) +500 gold and +0.15 price per day. (b) 290,000 and 87. (c) Deflation that never stops.

(a) Net `N × (F − D) = 500` per day. Price change `0.3 × 500 / 1,000 = 0.15` per day.

(b) `200,000 + 180 × 500 = 290,000`. Price `0.3 × 290,000 / 1,000 = 87`, up 45% from 60.

(c) At `D = 106` the town loses 100 gold per day forever. The price stops at 87 on the day of the change and then falls 0.03 per day with no floor. A flat-only economy has no resting point unless `F = D` exactly, and every later faucet change reopens the gap. A proportional drain would settle it.
</details>

30. *Week 7 · compute.* Use the EVE Online market fees from the week 7 lecture (current era). A trader with Accounting at level 5 places a sell order in an NPC station at the base broker's fee and sells an item for 100 million ISK. (a) How much ISK leaves circulation? (b) How much for a new character at base rates? (c) What does the skill do to the sink's effect on the economy?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 6.37 million. (b) 10.5 million. (c) It lowers `τ` for heavy traders, so the sink removes less per sale from them.

(a) Sales tax 3.37% plus broker's fee 3% is 6.37% of 100 million.

(b) Sales tax 7.5% plus broker's fee 3% is 10.5%.

(c) In the town model a lower `τ` means a higher `M*`. The skill trades some sink strength for goodwill with dedicated traders, which the lecture names as a way to avoid pushing trade off the market.
</details>

31. *Weeks 6 and 7 · critique.* Town B has settled at a potion price of 70 (`F = 110`). The team wants the price back near 35. One designer proposes doubling crafting yield (`q` from 10 to 20). Another proposes doubling the market cut from 10% to 20%. Compare the two with numbers and say who pays in each case.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Both reach 35. Doubling `q` gets there immediately and leaves the money stock alone. Doubling `τ` gets there over weeks (half-life about 11 days) by removing gold.

Doubling `q`: `P = 0.3 × 233,333 / (100 × 20) = 35` on the next day. The converter changed, not the money stock. Crafters pay, because each potion they make is now worth half as much gold.

Doubling `τ`: `s = 0.06`, `M* = 100 × 70 / 0.06 = 116,667`, `P* = 35`. The gap halves every `ln 0.5 / ln 0.94 = 11.2` days. Traders pay, in proportion to how much they trade, and hoarders who never trade pay nothing.

Neither is wrong. Pick by who you want to carry the cost and how fast you need the change.
</details>

## Week 8: Core loops and meta loops

32. *Week 8 · compute.* A crop's seeds cost 30 gold, it sells for 50 and takes 5 days. (a) What is its growth factor per day when gold binds, and its profit per tile per day when tiles bind? (b) Against parsnip (15.0% a day and 3.75 gold per tile per day), which crop wins in each case?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) About +10.8% a day and 4.0 gold per tile per day. (b) Parsnip wins when gold binds. The new crop wins when tiles bind.

(a) `(50/30)^(1/5) = 1.1076`. `(50 − 30) / 5 = 4.0`.

(b) With little gold, parsnip compounds faster (15.0% against 10.8%). With a full watering limit, each tile of the new crop earns more (4.0 against 3.75). Asking which crop is better without asking what binds has no answer.
</details>

33. *Week 8 · compute.* Use the week 8 farm model (energy 270, watering cost `2 − 0.1 × L`, parsnips at 20 and 35). You are at Farming level 3 with 2,500 gold, and your level does not change. (a) What is the watering limit? (b) How many tiles do you plant in this cycle and the next, and what is your gold after each? (c) What kind of growth follows?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 158 tiles. (b) 125 tiles then 158 tiles, gold 4,375 then 6,745. (c) Linear, +2,370 per cycle.

(a) `w = 2 − 0.3 = 1.7`, `W = floor(270 / 1.7) = 158`.

(b) Cycle 1: gold allows `floor(2,500/20) = 125`, below 158, so gold binds. Gold becomes `2,500 + 15 × 125 = 4,375`. Cycle 2: gold allows 218, above 158, so water binds. Gold becomes `4,375 + 15 × 158 = 6,745`.

(c) From now on each cycle adds `15 × 158 = 2,370`. Only a meta move (levels, sprinklers) that raises `W` changes that.
</details>

34. *Week 8 · compute.* A roguelite's first upgrade costs 500 gold and a run pays 100. Each upgrade costs 1.25 times the last and raises gold per run by 15%. Runs last 20 minutes. (a) How many runs does the first upgrade take, and how long is that? (b) The fifth? (c) Which upgrade is the first to need more than 10 runs, and what is its cadence?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 5 runs, 100 minutes. (b) About 7.0 runs. (c) The 10th upgrade, about 10.6 runs or 212 minutes.

Runs for the k-th upgrade, counting the first as `k = 0`, is `(500/100) × (1.25/1.15)^k = 5 × 1.087^k`.

(b) `k = 4`: `5 × 1.087^4 = 6.98`.

(c) Solve `1.087^k > 2`: `k > ln 2 / ln 1.087 = 8.3`, so `k = 9`, the 10th upgrade, at `5 × 1.087^9 = 10.6` runs, about 212 minutes. Because `g > h`, the meta loop winds down slowly.
</details>

35. *Week 8 · critique.* Players quit a farming game around day 20. A designer proposes a meta upgrade that gives "+5% sell price per season". Using the model, explain why this may not reach the problem, and propose a change that targets the constraint. Say whether it changes numbers or verbs.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Around day 20 the watering limit binds and growth turns linear. A 5% price rise nudges the slope and does nothing to the limit.

After the bend, gold grows by `(p − c) × W` per cycle. A 5% price rise on parsnip moves `p − c` from 15 to 16.75, so the linear slope grows 11.7%. It also speeds the early compounding and moves the bend earlier. The player still spends every morning watering the same tiles.

Target `W` instead. Earlier sprinkler recipes or cheaper sprinkler ingredients raise the limit and also remove the watering verb for the covered tiles, which frees the morning for mining or fishing. That is a meta move that changes verbs, the kind the lecture says keeps a core loop fresh.
</details>

## Week 9: Skill vs power

36. *Week 9 · compute.* A boss has 2,400 health and hits for 200. Your character has 900 health and deals 120 per hit. (a) Compute `H`, `A`, the mistake budget and the power ratio. (b) What is your win chance at `m = 0.15` and at `m = 0.25`? (c) Raise your health and damage by 10% and recompute the budget and the win chance at `m = 0.15`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `H = 20`, `A = 4`, budget 20%, power ratio 22.5%. (b) 83.0% and 41.5%. (c) Budget 21.1%, win chance 85.6%.

(a) `H = ceil(2,400/120) = 20`. `A = ceil(900/200) − 1 = 5 − 1 = 4`. Budget `4/20 = 20%`. Power ratio `(900 × 120) / (2,400 × 200) = 22.5%`.

(b) `P(X ≤ 4)` for `X ~ Binomial(20, m)`: 0.830 at `m = 0.15`, 0.415 at `m = 0.25`.

(c) Health 990, damage 132. `H = ceil(2,400/132) = ceil(18.2) = 19`. `A = ceil(990/200) − 1 = 5 − 1 = 4`. Budget `4/19 = 21.1%`. Win chance `P(X ≤ 4)` for `Binomial(19, 0.15)` is 0.856. The power ratio rose 21%, but the budget rose only 5% because the health gain missed a breakpoint in `A`.
</details>

37. *Week 9 · compute.* Use the lecture's boss (2,000 health, hits for 250) and player (100 health and 10 damage per level). A player at level 11 has `m = 0.25`. They can grind to level 13, or practice at level 11 until `m = 0.2`. Which gives the higher win chance?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Grinding to level 13 (81.0%) beats practicing to `m = 0.2` at level 11 (67.3%). Today's chance is 46.5%.

Level 11: `H = ceil(2,000/110) = 19`, `A = ceil(1,100/250) − 1 = 4`. `P(X ≤ 4)` with `Binomial(19, 0.25)` is 0.465, and with `m = 0.2` it is 0.673.

Level 13: `H = ceil(2,000/130) = 16`, `A = ceil(1,300/250) − 1 = 5`. `Binomial(16, 0.25)` gives 0.810.

Level 13 crosses breakpoints in both `H` and `A`. The practiced player keeps their skill for every later fight, which the table does not count.
</details>

38. *Week 9 · compute.* The lecture's "assist after each loss" valve gives 2% damage reduction per failed attempt. A level 12 player with `m = 0.25` keeps losing. (a) What is their win chance with 0, 1 and 2 losses? (b) After how many losses does the valve first help, and by how much? (c) Explain the flat stretch.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 57.4% each time. (b) After 3 losses, rising to 76.5%. (c) The boss hit must fall below 240 to add a survivable hit.

At level 12, `HP_p = 1,200`, `d_p = 120`, `H = ceil(2,000/120) = 17`. With no assist `A = ceil(1,200/250) − 1 = 4`, and `P(X ≤ 4)` for `Binomial(17, 0.25)` is 0.574.

One loss makes the hit 245 and two make it 240. `1,200/240 = 5` exactly, so `ceil` gives 5 and `A` stays 4. Three losses make it 235, `ceil(5.11) = 6`, `A = 5`, and the win chance becomes 0.765.

Because `A` is a whole number, help arrives in steps. The first two losses feel like the game ignored the player. A designer could start the valve at 5% so the first loss already crosses the breakpoint.
</details>

39. *Week 9 · critique.* A designer says: "We will scale every boss to the player's level so the game stays balanced." Using the skill-power map, say what this does to `A / H`, when it fails, and what a stuck player can still do.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Scaling holds `A / H` constant only while the player's power grows as fast as the boss's. Then levels buy nothing, and only moving down the skill axis helps.

In the lecture's interactive, turning scaling on makes every column of the map the same: 41.1% at `m = 0.2` at every level. If the player can level without getting stronger, as the lecture's Oblivion example with involuntary skills shows, the boss's power grows and the player's does not, so the budget falls as the player levels. The game gets harder the more you play.

A stuck player can only improve `m`. That suits competitive play (Guild Wars 2 structured PvP normalizes power on purpose) and is harsh in single-player. Offer a valve that does not route through levels, such as Celeste-style slower game speed or a summon.
</details>

## Week 10: Emergence vs progression

40. *Week 10 · compute.* A prototype has 24 systemic objects and QA can check 100 pairs. (a) How many pairs are there, and what share is untested? (b) The team wants at most 25% untested. What is the largest `k` they can ship?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 276 pairs, 63.8% untested. (b) `k = 16`.

(a) `C(24, 2) = 24 × 23 / 2 = 276`. Untested `1 − 100/276 = 63.8%`.

(b) You need `1 − 100 / C(k,2) ≤ 0.25`, so `C(k,2) ≤ 133.3`. `C(16,2) = 120` gives 16.7% untested. `C(17,2) = 136` gives 26.5%. So 16.
</details>

41. *Week 10 · compute.* A systemic game has 6 properties and 30 objects. (a) What is the maximum number of property rules? (b) How many object pairs does each rule cover on average? (c) How many object triples are there?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 21. (b) About 20.7. (c) 4,060.

(a) `R = m(m + 1)/2 = 6 × 7 / 2 = 21`.

(b) `C(30,2) = 435`, and `435 / 21 = 20.7`.

(c) `C(30,3) = 30 × 29 × 28 / 6 = 4,060`. You can test 21 rules on paper. You cannot test 4,060 triples. Test the rules and sample the pairs.
</details>

42. *Week 10 · design.* A team can build 4 puzzles a week for 25 weeks, and a puzzle takes 12 minutes to solve. (a) How many hours of plan P content is that? (b) Late in production, the team can add either 3 new puzzles or 3 new systemic objects to an existing set of 12. How many situations does each add? (c) Where in the game would you put each, and why?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 20 hours. (b) Puzzles add 3. Objects add 39 pairs. (c) Puzzles in the parts that must be guaranteed, objects in the parts players repeat.

(a) 100 puzzles × 12 minutes = 1,200 minutes = 20 hours, consumed once each.

(b) `C(15,2) − C(12,2) = 105 − 66 = 39`.

(c) The 39 pairs are also 39 untested cells, added late in production. Put the new objects in replayed spaces (combat arenas, an open hub) with property rules already tested, and put new puzzles where the story or tutorial needs a fixed beat. If any object can reach areas a story gate protects, test those pairs first.
</details>

43. *Week 10 · critique.* In a hybrid game, players discover that stacking two systemic crates lets them climb onto a roof and skip a quest gate meant to open in chapter 3. The producer wants the crates made unstackable. Critique that fix and propose a policy.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Removing stacking deletes a property rule used by every crate pair, to fix one cell of the grid. Fix the gate, not the rule.

Stacking is one property rule. It covers every pair of stackable objects, and players may use it for dozens of intended solutions. Removing it trades a sequence break for a smaller game. The problem is a physical wall guarding a progression gate, which the lecture warns is exactly where untested cells become sequence breaks.

Better options: make the gate a story gate (the roof event only triggers after chapter 3), or let the skip happen and make the roof content work early. Write the keep/patch policy before launch: keep discoveries that create skill, patch ones that break a gate you care about or create a dominant strategy.
</details>

## Week 11: Intransitive mechanics

44. *Week 11 · compute.* A three-way loop pays `w_R = 2`, `w_P = 1`, `w_S = 3`. (a) What is the stable mix? (b) Players are still at an even mix. What is each option's expected payoff this week? (c) Which option will look strongest in the first week, and which will be most common in the long run?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Rock 50.0%, paper 33.3%, scissors 16.7%. (b) Rock +0.333, paper −0.667, scissors +0.333. (c) Rock and scissors tie for strongest this week. Rock is most common in the long run.

(a) `r : p : s = w_S : w_R : w_P = 3 : 2 : 1`, total 6.

(b) Against thirds, `E(Rock) = (w_R − w_P)/3 = 1/3`, `E(Paper) = (w_P − w_S)/3 = −2/3`, `E(Scissors) = (w_S − w_R)/3 = 1/3`.

(c) Rock is common because scissors, the option rock beats, pays the biggest prize. Each share is the prize of the thing it beats.
</details>

45. *Week 11 · design.* With `w_P = w_S = 1`, what rock prize makes paper 40% of the stable mix? Give the full mix and check that it is stable.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `w_R = 4/3 ≈ 1.33`. Mix rock 30%, paper 40%, scissors 30%.

Paper's share is `w_R / (w_R + 2) = 0.4`, so `w_R = 0.8 + 0.4 w_R`, `w_R = 4/3`. Total prize `10/3`, so shares `1 : 4/3 : 1` are 30%, 40%, 30%.

Check against `(0.3, 0.4, 0.3)`: `E(Rock) = 4/3 × 0.3 − 1 × 0.4 = 0`. `E(Paper) = 1 × 0.3 − 1 × 0.3 = 0`. `E(Scissors) = 1 × 0.4 − 4/3 × 0.3 = 0`. All equal, so nobody has a reason to switch.
</details>

46. *Week 11 · compute.* In a *Yomi*-shaped triangle (attacks beat throws, throws beat blocks, blocks beat attacks), an attack win is worth 4, a throw win 2 and a block win 1. What is the stable mix?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Attack 28.6%, throw 14.3%, block 57.1%.

Each share is the prize of what the option beats. Attack beats throw, so attack's share is set by 2. Throw beats block, so throw's share is set by 1. Block beats attack, so block's share is set by 4. Shares `2 : 1 : 4`, total 7.

Raising the attack prize from 3 (the lecture's version) to 4 made blocking more common, from 50% to 57.1%, and attacking less common, from 33.3% to 28.6%.
</details>

47. *Week 11 · compute.* Run one round of the lecture's season update with prizes `(w_R, w_P, w_S) = (3, 1, 1)`, adjustment speed `η = 0.1`, starting from thirds. Give the three shares after the round, then say where the running average will drift over a long season.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Rock 35.6%, paper 33.3%, scissors 31.1%. The running average drifts toward the stable mix of 20%, 60%, 20%.

Against thirds: `E_R = 3 × 1/3 − 1 × 1/3 = 0.667`, `E_P = 1/3 − 1/3 = 0`, `E_S = 1/3 − 3 × 1/3 = −0.667`. The average payoff `Ē = 0`.

Update `x ← x × (1 + η(E − Ē))`: rock `1/3 × 1.0667 = 0.3556`, paper `0.3333`, scissors `1/3 × 0.9333 = 0.3111`. They already sum to 1.

In the first round rock grows, the "wrong" direction. The delayed balancing loop then swings the population around the stable mix, and the long-run average settles near `(1 : 3 : 1)/5`.
</details>

48. *Week 11 · critique.* A four-unit counter chart has these arrows (A beats B means A wins that matchup): A beats B, B beats C, C beats A, D beats A, D beats B. Nothing beats D. The designer says the system is balanced "because every unit has a counter". Critique the claim and propose a fix.

<details>
<summary>Answer and worked solution</summary>

**Answer:** D has no incoming arrow, so it is dominant. The loop A, B, C is real, but D beats two of its members and loses to nothing.

The lecture's check is to look for options with arrows out and none in. D is one. Players will drain toward D, and the three-way loop collapses into a ladder with D on top. The claim "every unit has a counter" is false for D.

Fix it by giving D an incoming arrow, for example C beats D, so D is the best answer to A and B and the worst answer to C. Then attach prizes to the arrows and check the direction of the shares with the rule "a bigger prize on an arrow raises demand for whatever beats that arrow's source".
</details>

## Week 12: Emergent behavior from simple rules

49. *Week 12 · compute.* Apply the cave rule (wall if the 3 × 3 count `n ≥ 5`) to the center of each block. Rows are written top to bottom, `#` is wall. (a) `. . #` / `. # #` / `# . .`. (b) `# # #` / `# . #` / `. . .`. (c) `# . .` / `. . .` / `. . #`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `n = 4`, floor. (b) `n = 5`, wall. (c) `n = 2`, floor.

(a) Walls at top right, center, middle right and bottom left, 4. The center wall erodes.

(b) Five walls around a floor center. The gap fills.

(c) Two walls, both corners. The center stays floor.
</details>

50. *Week 12 · compute.* Apply one step of the cave rule to this 5 × 5 grid, counting off-grid cells as walls. Give the count grid and the result, and the number of walls before and after.

```
# # . . .
# . # . .
. . . . .
. . # . #
. . . # #
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** 8 walls before, 10 after.

```
Counts n        After
8 7 5 4 5       # # # . #
6 4 2 1 3       # . . . .
4 3 2 3 4       . . . . .
3 1 2 4 6       . . . . #
5 4 5 7 8       # . # # #
```

Check two cells. Top-left: 5 off-grid walls, itself, and neighbors `#`, `#`, `.` give 8. Center: its block is `# . .`, `. . .`, `. # .`, which holds 2 walls, so it becomes floor.

The interior clears and the corners harden into wall. On a grid this small, the off-grid walls decide most of the result, as in the lecture's example.
</details>

51. *Week 12 · compute.* Apply Conway's Life rule. (a) Three live cells on a diagonal, at (0,0), (1,1) and (2,2). What happens over two steps? (b) Three live cells in an L, at (0,0), (1,0) and (0,1). What happens?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) One cell remains after step 1, and nothing after step 2. (b) It becomes the 2 × 2 block in one step and never changes again.

(a) The middle cell has 2 live neighbors and survives. Each end has 1 and dies. No dead cell touches all three, so none has exactly 3 and none is born. Step 1 leaves (1,1) alone. It has 0 neighbors and dies in step 2.

(b) Each live cell has 2 live neighbors and survives. The empty corner (1,1) touches all three and is born. The result is a block, where every live cell has 3 neighbors and no dead cell has more than 2, so it is a still life.
</details>

52. *Week 12 · explain.* Use the lecture's dial table (64 × 40 map, 5 steps, 20 seeds). A designer wants maps with about 40% wall and at least 95% of floor in one region. Another wants about 50% wall. Choose `p` for each and say what else each needs.

<details>
<summary>Answer and worked solution</summary>

**Answer:** First designer, `p = 0.44` (39.3% wall, 96.1% largest region). Second, `p` between 0.46 and 0.48, which needs a connectivity repair.

At 0.44 the connectivity target is met on average, but the table shows 1.85 separate regions on average, so some maps still have pockets. Add a flood-fill check that fills all but the largest region.

For about 50% wall, 0.46 gives 46.1% and 0.48 gives 53.3%. The largest region falls from 88.5% to 79.2% of floor and the mean number of regions rises from 3.05 to 4.55. That is the steep part of the curve. Every map at that setting needs tunnels or fill, and a small balance tweak to `p` will change many maps at once.
</details>

53. *Week 12 · critique.* A tester reports: fire arrows ignite grass, burning grass spreads to a wooden town gate, and the burnt gate lets players skip a quest. A designer proposes "fire arrows cannot ignite grass". Write the chain, then say where you would break it and why.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The chain is fire arrow (writes fire on a grass tile), fire spreads through grass (writes fire on neighbors), fire burns wood (reads fire, writes damage on the gate), a destroyed gate opens the path (reads gate state). Break it at the gate, not at the arrow.

Removing arrow ignition deletes a rule that many good chains use (burning out an ambush, clearing brush). The bug is a quest-critical object that shares a property ("burns") with the systemic world. Either give the quest gate a property it does not share (stone, or a gate the story opens), or damp the quantity at the fire-to-wood step for quest objects. That is a general limit at one link, which keeps every other chain through the same rules.
</details>

## Week 13: Systems documentation

54. *Week 13 · compute.* A game has a cap of 8 charges and regenerates one every 45 minutes. (a) What are the knee and the daily maximum? (b) A player checks in every 10 hours and spends everything. How many charges per day do they get, what share of the maximum is that, and how many are lost to the cap each day?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Knee 6 hours, daily maximum 32. (b) 19.2 per day, 60%, 12.8 lost.

(a) Knee `C × R = 8 × 45 min = 360 min = 6 h`. Daily maximum `24 h / 45 min = 32`.

(b) 10 hours is above the knee, so each visit finds the full 8. Visits per day `24 / 10 = 2.4`, so `2.4 × 8 = 19.2`. Share `19.2 / 32 = 60%`. Lost `32 − 19.2 = 12.8`.
</details>

55. *Week 13 · design.* A studio wants its stamina system to reward exactly two sessions a day with nothing lost, and to allow at most 24 stamina per day. Choose `C` and `R`, write the parameter table rows for them, and give one derived number that belongs next to the table.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `R = 1` hour per stamina and `C = 12`, for two sessions 12 hours apart.

Daily maximum `24 / R = 24` gives `R = 1 h`. For nothing to be lost at a 12-hour interval, the knee `C × R` must be at least 12 hours, so `C = 12`. (A 9-hour knee with `C = 9` would suit a player who plays at 9:00 and 18:00, but they would lose 6 stamina over the 15-hour night.)

| Name | Value | Unit | Safe range | Why this value | Owner |
|---|---|---|---|---|---|
| `stamina_cap` | 12 | stamina | 9 to 16 | Knee of 12 h with `regen_minutes = 60` | Systems designer |
| `regen_minutes` | 60 | minutes per stamina | 45 to 90 | Daily maximum of 24 | Systems designer |

Derived number: knee `= stamina_cap × regen_minutes = 12 h`.
</details>

56. *Week 13 · compute.* Lives regenerate every 30 minutes up to 5. A player checks in every 70 minutes and spends every life. How many lives per visit and per day do they get under "restart on spend"? Under "pause at full"? What share of income does the bug cost?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Restart on spend, 2 per visit and 41.1 per day. Pause at full, 48 per day. The bug costs 14.3%.

Restart on spend: the spend resets the timer to zero. Seventy minutes later two lives have arrived (at 30 and 60) and the timer holds 10 minutes of progress. The spend wipes that progress. Every visit yields exactly 2, and there are `1,440 / 70 = 20.57` visits a day, so 41.1 lives.

Pause at full: the 10 minutes carry over, and the player averages `70/30 = 2.33` lives per visit, 48 a day. A minute-by-minute simulation over days 8 to 21, as in the lecture's spec, gives 41.14 and 48.0.

Loss `1 − 41.1/48 = 14.3%`, and it falls only on frequent players.
</details>

57. *Week 13 · critique.* A design document contains the rule "Bought lives should usually add to your lives, up to a reasonable limit." Name the problems, rewrite it as numbered testable rules, and write one given/when/then case.

<details>
<summary>Answer and worked solution</summary>

**Answer:** "Should" and "usually" make the rule optional. "Reasonable limit" has no parameter. It does not say whether regeneration continues above the cap.

Rewrite:

- 4.5 A purchase adds `lives_bought` to `lives`, even if the result exceeds `lives_cap`, up to `lives_overfill_max`.
- 4.6 While `lives ≥ lives_cap`, the refill timer is stopped at zero.

Test case: given `lives = 5`, `lives_cap = 5`, `lives_bought = 3`, `lives_overfill_max = 10`, when the player buys lives, then `lives = 8` and the timer stays stopped. Add both new parameters to the table with units, safe ranges and reasons.
</details>

## Week 14: Tuning with spreadsheets

58. *Week 14 · compute.* A guild bank earns 120 gold a day and pays upkeep of 8% of its balance a day. It starts empty. (a) What is the equilibrium? (b) Give the balance after days 1, 2 and 3, and check day 3 with the closed form.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 1,500. (b) 120, 230.4, 332.0.

(a) `G* = I / s = 120 / 0.08 = 1,500`.

(b) Day 1: `0 + 120 − 0 = 120`. Day 2: `120 + 120 − 9.6 = 230.4`. Day 3: `230.4 + 120 − 18.43 = 331.97`.

Closed form: `1,500 × (1 − 0.92^3) = 1,500 × 0.2213 = 331.97`.
</details>

59. *Week 14 · compute.* In a game with price growth `g = 1.08` per purchase, building A pays back three times faster than building B at base prices. A greedy player owns 30 of A. About how many of B do they own?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 16.

Gap `= ln(payback ratio) / ln g = ln 3 / ln 1.08 = 1.099 / 0.077 = 14.3`. So B sits about 14 purchases behind: `30 − 14.3 ≈ 16`.

A small `g` makes the gap large, because `ln g` is in the denominator. At `g = 1.15` the same ratio gives a gap of 7.9.
</details>

60. *Week 14 · compute.* With Cookie Clicker's base numbers from the week 14 lecture (Grandma 100 price and 1 CpS, Mine 47 CpS) and `g = 1.15`, what range of Mine base prices makes the first Mine arrive when the player owns exactly 9 Grandmas? Check one value inside and one outside the range.

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 14,377 to 16,534.

The Mine's base payback must sit between the paybacks of the 9th and 10th Grandma: `100 × 1.15^8 = 305.9` s and `100 × 1.15^9 = 351.8` s. Times 47 CpS gives 14,377 to 16,534.

Checked with the greedy simulation: at 14,400 and at 16,500 the first Mine comes with 9 Grandmas owned (purchases 22 and 24). At 14,300 it comes with 8, and at 16,600 with 10. The boundary values themselves are ties, so pick a value with margin, such as 15,500.
</details>

61. *Week 14 · explain.* The guild bank has `I = 100` and `s = 0.10`. Its day-10 balance is 651.3. Build a one-at-a-time sensitivity table for ±20% changes in each input and say which input day-10 gold depends on more. Why does this differ from the lecture's day-14 table, where upkeep looked like the more sensitive knob?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Income is the more sensitive input here.

| Input changed | Day-10 gold, low | Default | Day-10 gold, high |
|---|---|---|---|
| `guild_income` 80 / 120 | 521.1 | 651.3 | 781.6 |
| `upkeep_rate` 0.08 / 0.12 | 707.0 | 651.3 | 601.2 |

Income moves the result ±20%, exactly in proportion. Upkeep moves it +8.6% and −7.7%.

Two things changed from the lecture's table. The lecture moved upkeep by ±50% and income by ±10%, so the swings are not like for like. And at day 10 the balance is still far below equilibrium, so upkeep (which acts on the balance) has had less to act on. A sensitivity table answers "sensitive to this change, at this horizon". Report both.
</details>

62. *Week 14 · compute.* With `s = 0.10`, the design target is 1,000 gold in the guild bank at the end of day 20. What income does goal seek find? Confirm with the closed form.

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 113.8 gold per day.

Solve `(I / s) × (1 − 0.9^20) = 1,000`. `0.9^20 = 0.1216`, so `I = 1,000 × 0.1 / 0.8784 = 113.84`. Stepping the recurrence with 113.84 gives 1,000.0 at day 20.
</details>

63. *Week 14 · compute.* The week 14 lecture uses a growth factor of about `2^(1/7)` per level for Old School RuneScape XP. A player raising total level greedily has one skill that trains three times as fast (in XP per hour) as another. How many levels ahead does the fast skill stay?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 11 levels.

Gap `= ln 3 / ln(2^(1/7)) = 7 × ln 3 / ln 2 = 7 × 1.585 = 11.1`. The lecture's example with a rate ratio of 2 gives exactly 7. Tripling the ratio does not triple the gap, because the gap grows with the log of the ratio.
</details>

## Mixed questions for the viva

64. *Weeks 2, 7 and 13 · design.* Your SDD's town has 500 players, a faucet of 80 gold per player per day, a flat drain of 50, velocity 0.25 and 12 potions per player per day. The team wants an equilibrium potion price of 50 and a half-life under 30 days. Choose the market cut `τ`, show both targets are met, and name the two derived numbers you would add to the document.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The cut alone cannot meet both targets. `τ = 5%` gives `P* = 50` but a half-life of about 55 days. Raise the cut and lower the flat drain together. One solution is `τ = 10%` with a flat drain of 20, which gives `P* = 50` and a half-life of 27.4 days.

Start from `P* = v × M* / (N × q)` and `M* = N × (F − D) / (τ v)`. Substituting, `P* = (F − D) / (τ × q)`. With `F − D = 30` and `q = 12`, `P* = 50` needs `τ = 30 / (50 × 12) = 5%`. Then `s = 0.05 × 0.25 = 0.0125` and the half-life is `ln 0.5 / ln 0.9875 = 55` days. Too slow.

The half-life depends only on `s = τ v`. Under 30 days needs `s > 1 − 0.5^(1/30) = 0.0228`, so `τ > 9.1%`. Keep `P* = 50` by raising `F − D` with it: at `τ = 10%`, `F − D = 50 × 0.10 × 12 = 60`, so drop the flat drain to 20. Now `s = 0.025`, half-life `ln 0.5 / ln 0.975 = 27.4` days, and `P* = 60 / (0.1 × 12) = 50`.

Derived numbers for the document: `P* = (F − D)/(τ q)` and half-life `= ln 0.5 / ln(1 − τ v)`.
</details>

65. *Weeks 4 and 11 · critique.* A three-unit game has a counter loop: Archer beats Lancer, Lancer beats Mage, Mage beats Archer, every win worth 1. The patch notes say: "Lancers were everywhere, so we doubled the Archer's win prize, since Archers counter Lancers, and added a catch-up bonus for players who lose to a Lancer." Predict the new stable mix and the first-week picture, then say whether either change is the right tool.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Stable mix Archer 25%, Lancer 25%, Mage 50%. Archers look best in the first week, then Mages take over. The Archer buff cuts Lancers only as a side effect, and the catch-up bonus answers a question nobody asked.

Map the loop to week 11's names. Archer is rock (a rock win now pays 2), Lancer is scissors, Mage is paper. Stable shares `r : p : s = w_S : w_R : w_P = 1 : 2 : 1`, so Archer 25%, Mage 50%, Lancer 25%. Against the old even mix, `E(Archer) = (2 − 1)/3 = +0.333`, so Archer play rises first. Then Mages, which beat Archers, become the most common unit.

The Lancer's share is set by the prize of the unit it beats, the Mage. To cut Lancers directly, lower the Mage's win prize. That sounds backward, which is why the rule is worth writing in the patch plan.

The catch-up bonus (week 4) is a balancing loop on a lead between players inside a match. A skewed pick rate is not a lead, so there is nothing for it to pull back, and it rewards losing to one unit in particular. Before either change, check whether the Lancer is also transitively stronger, a stat that helps in every matchup. If its win rate is high everywhere, fix that stat instead.
</details>
