# MA101 exam bank

This bank holds 71 questions for the MA101 midterm and final. Students may study from it. The exams draw questions from it and change the numbers, as set out in [midterm-and-final-brief.md](midterm-and-final-brief.md).

Every question has three tags.

- **Weeks.** The lecture weeks the question uses. Cross-week questions list several.
- **Type.** `compute` asks you to run a model from the lectures on numbers you have not seen. `explain` asks you to say why a model behaves as it does, with numbers. `design` asks you to choose parameters that meet a brief. `critique` asks you to judge someone else's design and propose a fix.
- **Exam.** `midterm, final` questions use weeks 1 to 7 only and may appear on either exam. `final` questions use at least one week from 8 to 14 and appear only on the final.

Every answer below was recomputed in Python for this bank. Where a question uses a fact about a shipped game, the fact comes from the lecture named in the question, which cites its source and version.

## Coverage

| Week | Topic | Questions | Midterm-eligible |
|---|---|---|---|
| 1 | Functions as machines | 1 to 4, 71 | yes |
| 2 | Linear functions and rates | 5 to 9, 67 | yes |
| 3 | Polynomials and quadratics | 10 to 13 | yes |
| 4 | Exponentials | 14 to 18, 70 | yes |
| 5 | Logarithms | 18 to 24, 70 | yes |
| 6 | Rational functions | 25 to 30, 66, 67 | yes |
| 7 | Piecewise, caps and floors | 31 to 35, 66, 71 | yes |
| 8 | Lerp, inverse lerp, remap | 36 to 39, 68 | no |
| 9 | Easing | 40 to 43, 68 | no |
| 10 | Angles, sin and cos | 44 to 47, 69 | no |
| 11 | atan2 and turning | 48 to 51 | no |
| 12 | 2D vectors | 52 to 55, 69 | no |
| 13 | Dot product and cones | 56 to 60, 68 | no |
| 14 | Distances and ranges | 61 to 65, 69 | no |

Type counts are 51 compute, 4 explain, 6 design and 10 critique. Every compute question runs a lecture model on numbers that do not appear in the lectures, so 51 of 71 questions (72%) test use of a model rather than recall. Most critique and design questions also require new computation.

---

## Week 1. Functions as machines

1. **Week 1 · compute · midterm, final.** A species has base Speed 95. Your copy has IV 31, 252 Speed EVs and a Speed-boosting nature. Using the Generation III+ stat formula from [week 1](../lectures/w01-functions-as-machines.md), compute its Speed at level 50 and at level 100. Then, for the same Pokémon with a neutral nature, find the lowest level at which Speed reaches at least 200. Show a rough solve and a table check.

   <details>
   <summary>Answer and worked solution</summary>

   **Answer.** 161 at level 50, 317 at level 100. With a neutral nature, level 69.

   Combine first. `raw = 2 × 95 + 31 + floor(252 / 4) = 190 + 31 + 63 = 284`.

   Level 50. `floor(284 × 0.5) = 142`, plus 5 is 147, times 1.1 is 161.7, floor 161.

   Level 100. `284 + 5 = 289`, times 1.1 is 317.9, floor 317.

   Neutral nature, target 200. Drop the floors and solve `284 × L / 100 + 5 = 200`, so `L = 195 × 100 / 284 ≈ 68.7`. Check whole levels. Level 68 gives `floor(193.12) + 5 = 198`. Level 69 gives `floor(195.96) + 5 = 200`. The answer is level 69.

   </details>

2. **Week 1 · compute · midterm, final.** A survival game uses fall damage `max(0, 2·(d − 5))`, where `d` is whole blocks fallen. Players have 30 health and die at 0. (a) What is the highest fall a full-health player survives? (b) If falls are capped at 60 blocks, state the domain and range. (c) Does the function have an inverse on its whole domain?

   <details>
   <summary>Answer and worked solution</summary>

   **Answer.** (a) 19 blocks, taking 28 damage. (b) Domain 0 to 60 blocks. Range 0 to 110 damage, even values only. (c) No. It has an inverse only on the ramp, `d = damage / 2 + 5` for `d ≥ 5`.

   A player dies when damage reaches 30. Solve `2(d − 5) ≥ 30`, so `d ≥ 20`. A 20-block fall is fatal and a 19-block fall deals `2 × 14 = 28`.

   The top of the range is `2 × (60 − 5) = 110`. Every fall from 0 to 5 blocks gives 0 damage, so "which fall gave 0 damage?" has no single answer. That flat part has no inverse. On the ramp each damage value comes from exactly one fall.

   </details>

3. **Week 1 · compute · midterm, final.** In an action RPG each point of Agility gives 3 crit rating, and every 40 crit rating gives 1 percentage point of crit chance. (a) Write crit chance as a composed function of Agility and state its rate. (b) How much Agility buys +10 percentage points? (c) Separately, a character with 800 attack power receives a +50 flat buff and a +20% buff. Compute the final attack power for both orders.

   <details>
   <summary>Answer and worked solution</summary>

   **Answer.** (a) `crit% = Agi × 3 / 40 = 0.075 × Agi`. (b) 133.3, so 134 whole points. (c) 1,020 if the flat buff applies first, 1,010 if the percentage applies first.

   The rate of a chain is the product of the rates. `3 rating per Agi × 1/40 percentage point per rating = 0.075` percentage points per Agi. Invert for the target: `10 / 0.075 = 133.3`. A player cannot buy a third of a point, so 134.

   Order of buffs: `1.2 × (800 + 50) = 1,020`. `1.2 × 800 + 50 = 1,010`. A pipeline with an addition in it does not commute, so the spec must name the order.

   </details>

4. **Week 1 · explain · midterm, final.** A forum post says "a perfect IV is worth 31 points, so it always adds 31 to the stat." Using the week 1 stat machine, explain when the claim is true, what a perfect IV is worth at level 50, and which part of the formula makes the difference. Then say what would change if the game added the IV after the level step, as `... + 5 + I`.

   <details>
   <summary>Answer and worked solution</summary>

   **Answer.** The claim holds only at level 100. At level 50 a perfect IV adds 15 points (for base 100, no EVs, neutral nature, 120 against 105). The IV sits inside `raw`, which is multiplied by `L / 100`, so its worth is about `31 × L / 100`.

   At level 100 the multiplier is 1 and every IV point is one stat point. At level 50 it is 0.5, and flooring can make the gain 15 or 16 depending on whether `raw` is odd. The level is a multiplier on every input inside `raw`.

   If the IV were added after the level step, it would be worth exactly 31 at every level. That would make it large next to a level-5 stat and small next to a level-100 stat, so IVs would matter most early and least late. The current design keeps investments proportional across levels.

   </details>

## Week 2. Linear functions and rates

5. **Week 2 · compute · midterm, final.** A designer wants level 5 enemies to have 300 HP and level 45 enemies to have 2,700 HP. Find the line in point-slope form, compute HP at level 30 and level 1, and say whether the line is safe across a domain of levels 1 to 50.

   <details>
   <summary>Answer and worked solution</summary>

   **Answer.** `HP(L) = 300 + 60·(L − 5)`. `HP(30) = 1,800`. `HP(1) = 60`. The line stays positive over levels 1 to 50 (60 to 3,000), so it is safe.

   Slope `(2,700 − 300) / (45 − 5) = 2,400 / 40 = 60` HP per level. `HP(30) = 300 + 60 × 25 = 1,800`. Check the far end, `HP(45) = 300 + 60 × 40 = 2,700`. Check both ends of the real domain: `HP(1) = 300 − 240 = 60` and `HP(50) = 3,000`. A level-1 enemy with 60 HP is low but legal.

   </details>

6. **Week 2 · compute · midterm, final.** A class has life `Life(L) = 80 + 15·(L − 1)`. Which is the first level-up that adds less than 3% to the character's life? Show the inequality and check the neighbouring level-ups.

   <details>
   <summary>Answer and worked solution</summary>

   **Answer.** The level-up from 30 to 31.

   A level-up to level `L` adds 15 to `Life(L − 1)`. We need `15 / Life(L − 1) < 0.03`, so `Life(L − 1) > 500`. `80 + 15·(L − 2) > 500` gives `L − 2 > 28`, so `L ≥ 31`.

   Check. Level 29 to 30 adds `15 / 500 = 3.00%`, which is not less than 3%. Level 30 to 31 adds `15 / 515 = 2.91%`.

   </details>

7. **Week 2 · compute · midterm, final.** Using the classic-era World of Warcraft rules from [week 2](../lectures/w02-linear-functions-and-rates.md) (14 AP per 1 DPS, 2 AP per Strength for warriors, damage per swing is bonus DPS times weapon speed), a warrior has 2,100 attack power. (a) How much bonus DPS is that? (b) How much bonus damage per swing on a 3.6-speed weapon and on a 1.8-speed weapon? (c) How much damage per swing do 90 more Strength add on the 3.6-speed weapon?

   <details>
   <summary>Answer and worked solution</summary>

   **Answer.** (a) 150 DPS. (b) 540 per swing on the 3.6 weapon, 270 on the 1.8 weapon. (c) About 46.3 per swing.

   `2,100 / 14 = 150` DPS. Per swing, multiply by seconds per swing: `150 × 3.6 = 540` and `150 × 1.8 = 270`. Per second both weapons gain the same 150.

   Chain the rates for (c): `2 AP/Str × 1/14 DPS/AP × 3.6 s/swing = 0.514` damage per swing per Strength. `90 × 0.514 = 46.3`.

   </details>

8. **Week 2 · design · midterm, final.** Ring A gives a flat +40 damage. Ring B gives `4 + 1.5·L` damage at character level `L`. (a) At what level should a player switch rings? (b) The designer wants the switch at level 30. Give two different fixes that each change one number, and name one fix that looks valid but breaks at low levels.

   <details>
   <summary>Answer and worked solution</summary>

   **Answer.** (a) Level 24. (b) Raise Ring A to +49, or lower Ring B's slope to 1.2. Lowering B's intercept to −5 also moves the crossing to 30 but gives negative damage below level 4.

   (a) `40 = 4 + 1.5·L` gives `L = 24`. Below 24 Ring A wins.

   (b) Keep B and set A to `4 + 1.5 × 30 = 49`. Or keep A and solve `40 = 4 + m × 30`, so `m = 1.2`. The intercept fix solves `40 = b + 45`, so `b = −5`, and B at level 1 is `−3.5`. Any of the first two is acceptable. A strong answer says which one fits the item's role (raising A makes the early ring stronger; lowering B's slope makes the late ring weaker everywhere).

   </details>

9. **Week 2 · critique · midterm, final.** A character has life `100 + 20·(L − 1)` and a same-level enemy hits for `10 + 5·(L − 1)`. (a) Compute hits to die at levels 1, 10, 50 and 99, and the value it settles toward. (b) The designer wants late-game fights where the player survives about 6 hits and proposes raising starting life to 300. Critique the proposal with numbers and propose a fix.

   <details>
   <summary>Answer and worked solution</summary>

   **Answer.** (a) 10.0, 5.09, 4.24, 4.12, settling toward `20 / 5 = 4`. (b) The proposal fails. At level 99 it gives only 4.52 hits. Raise the life slope to 30 instead, which settles toward 6 (6.08 at level 99).

   (a) Level 1: `100 / 10 = 10`. Level 10: `280 / 55 = 5.09`. Level 50: `1,080 / 255 = 4.24`. Level 99: `2,060 / 500 = 4.12`. The ratio of two lines approaches the ratio of their slopes.

   (b) With starting life 300, level 99 life is `300 + 20 × 98 = 2,260` and hits to die `2,260 / 500 = 4.52`. The intercept only matters early. Intercepts control the early game and slopes control the late game. With a life slope of 30, level 99 gives `(100 + 30 × 98) / 500 = 6.08` and level 50 gives `1,570 / 255 = 6.16`. The fix changes a slope, not an intercept.

   </details>

## Week 3. Polynomials and quadratic curves

10. **Week 3 · compute · midterm, final.** You want a jump that rises 2.5 tiles in 0.35 s. (a) Compute gravity `g` and launch speed `v₀`. (b) You add a fall multiplier of 4 after the apex. How long is the descent, and what is the total air time? (c) At 60 frames per second, what is the second difference in height between consecutive frames while gravity is unmodified?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) `g ≈ 40.8` tiles/s², `v₀ ≈ 14.3` tiles/s. (b) Descent 0.175 s, total 0.525 s. (c) About −0.0113 tiles per frame per frame.

    (a) `g = 2h / t_h² = 5 / 0.1225 = 40.82`. `v₀ = 2h / t_h = 5 / 0.35 = 14.29`.

    (b) With multiplier `m` the descent takes `t_h / √m = 0.35 / 2 = 0.175` s. Total `0.35 + 0.175 = 0.525` s.

    (c) The second difference is `−g·Δt² = −40.82 / 3,600 = −0.0113`.

    </details>

11. **Week 3 · compute · midterm, final.** A jump has `y(t) = 16t − 16t²` (tiles, seconds) and the character moves sideways at 6 tiles/s. (a) Over what range of horizontal distance is the character at or above a ledge 3 tiles high? (b) Can the jump reach a ledge 4.5 tiles high? Decide with the discriminant before solving for any time.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) From 1.5 to 4.5 tiles from take-off. (b) No. The discriminant is −32.

    (a) Solve `16t² − 16t + 3 = 0`. `D = 256 − 4 × 16 × 3 = 64`, `√D = 8`. `t = (16 ± 8) / 32`, so 0.25 s and 0.75 s. Multiply by 6 tiles/s: 1.5 and 4.5 tiles.

    (b) `D = 256 − 4 × 16 × 4.5 = 256 − 288 = −32`. A negative discriminant means no real time, so the arc never reaches 4.5. Check: the apex is `v₀² / (2g) = 256 / 64 = 4` tiles.

    </details>

12. **Week 3 · compute · midterm, final.** A data-mined table gives the XP needed for levels 1 to 6 as 2, 9, 28, 65, 126, 217. Find its degree using differences, give its formula, and use the ratio test to show it is not exponential.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** Cubic. `XP(n) = n³ + 1`.

    First differences 7, 19, 37, 61, 91. Second differences 12, 18, 24, 30. Third differences 6, 6, 6. Constant third differences mean cubic, and `6a = 6` gives `a = 1`. Try `n³ + c`. At `n = 1`, `1 + c = 2`, so `c = 1`. Check `n = 5`: `125 + 1 = 126`. Correct.

    Ratios of neighbours are 4.5, 3.11, 2.32, 1.94, 1.72. They fall toward 1, which is the signature of a polynomial. An exponential would keep a constant ratio.

    </details>

13. **Week 3 · critique · midterm, final.** A designer writes: "The jump felt floaty, so I raised gravity from 37.5 to 50 tiles/s² and left launch speed at 15 tiles/s. Now players can't reach the 3-tile ledges." Explain what happened with numbers, and propose a way to make the jump snappier while keeping the 3-tile height.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** With fixed launch speed, the apex dropped from 3 to 2.25 tiles. Design from height and time instead. Keep `h = 3` and shorten `t_h`, for example to 0.3 s, which gives `g ≈ 66.7` and `v₀ = 20`.

    Apex height is `v₀² / (2g)`. Before: `225 / 75 = 3`. After: `225 / 100 = 2.25`. Time to apex went from `15 / 37.5 = 0.4` s to `15 / 50 = 0.3` s, so the jump did get snappier, but it also got lower.

    With `h = 3`, `t_h = 0.3`: `g = 6 / 0.09 = 66.7` and `v₀ = 6 / 0.3 = 20`. Another valid fix is to keep the rise as it was and add a fall multiplier, which shortens only the descent. A strong answer notes that "snappy" comes from short air time and that high gravity is the consequence, not the dial.

    </details>

## Week 4. Exponentials

14. **Week 4 · compute · midterm, final.** A game's total XP to reach level `L` is `200 · 2^(L/5)` with a cap of 50. (a) What is the halfway level? (b) At what level does a player hold one sixteenth of the level-50 total? (c) What is the level-50 total?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) 45. (b) 30. (c) 204,800 XP.

    The total doubles every 5 levels. This curve is a pure exponential with no constant term, so the halfway rule is exact here. Half the cap total sits one doubling interval below the cap, `50 − 5 = 45`. (For a table with constant terms, such as RuneScape's, the rule can be off by a level.) One sixteenth is four doublings down, `50 − 20 = 30`. `200 × 2^10 = 204,800`.

    </details>

15. **Week 4 · compute · midterm, final.** An upgrade's price is `50 · 1.12^M`, where `M` is the number already bought. (a) What does the 21st upgrade cost? (b) What do all 21 cost together? (c) What share of that total was the 21st? Compare it with the long-run share `(b − 1) / b` and explain the gap.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) About 482. (b) About 4,085. (c) 11.8%, against a long-run share of 10.7%.

    (a) The 21st upgrade has `M = 20`: `50 × 1.12^20 = 482.3`.

    (b) Geometric series: `50 × (1.12^21 − 1) / 0.12 = 4,084.9`.

    (c) `482.3 / 4,084.9 = 11.8%`. The long-run share is `0.12 / 1.12 = 10.7%`. The formula drops the `−1` in `b^N − 1`, which is only negligible when `b^N` is large. Here `1.12^21 ≈ 10.8`, so the `−1` still shifts the share by about a point.

    </details>

16. **Week 4 · explain · midterm, final.** Two XP tables give totals at levels 10, 20, 30 and 40. Table A: 1,000; 8,000; 27,000; 64,000. Table B: 1,000; 4,000; 16,000; 64,000. Classify each table, give the doubling interval of any exponential one, and say which one makes the late game relatively easier.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** A is polynomial (it is `L³`). B is exponential with a doubling interval of 5 levels. A makes the late game relatively easier.

    Ratios for A over each 10 levels: 8, 3.375, 2.37. They fall toward 1, so A is polynomial. Indeed `1,000 × (L/10)³ = L³`. Ratios for B: 4, 4, 4. A constant ratio means exponential. A factor of 4 per 10 levels is two doublings, so it doubles every 5 levels.

    For A the growth over a fixed stretch shrinks as you climb, so each late stretch costs relatively less than the last. For B every 5 levels doubles the total, everywhere.

    </details>

17. **Week 4 · compute · midterm, final.** XP per level grows like `2^(L/6)` and the XP a player earns per hour grows like `2^(L/10)`. (a) How does time per level grow? Give its doubling interval. (b) If level 20 takes 1.5 hours, how long does level 50 take? (c) What doubling interval for the earning rate would make every level take the same time?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) Time per level grows like `2^(L/15)`, doubling every 15 levels. (b) 6 hours. (c) 6 levels.

    Hours per level is cost over rate: `2^(L/6) / 2^(L/10) = 2^(L/6 − L/10) = 2^(L/15)`. From level 20 to 50 is 30 levels, two doublings: `1.5 × 4 = 6` hours. If the rate also doubled every 6 levels, the exponents would cancel.

    </details>

18. **Weeks 4 and 5 · critique · midterm, final.** For a 40-hour single-player RPG with a level cap of 60, a designer proposes total XP `100 · 1.25^L`. Critique the proposal with four numbers. Give the halfway level, the share of the total spent on the last level alone, the share already earned at level 30 and the size of the level-60 number. Propose one change.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** The curve doubles every 3.1 levels, so the halfway level is about 57. The last level alone is 20% of the total. Level 30 holds 0.12% of the total. The level-60 total is about 65 million. Almost half the game's XP (48.8%) sits in the last three levels, which is wrong for a 40-hour game. Lengthen the doubling interval (for example 10, which puts the halfway level at 50) or switch to a polynomial curve.

    Doubling interval: `ln 2 / ln 1.25 = 3.11`, so halfway at `60 − 3.1 ≈ 56.9`. The rule of 70 gives 2.8, which is rough at 25%. Last-step share: `(b − 1) / b = 0.25 / 1.25 = 20%`. Level 30 share: `1.25^−30 = 0.0012`. Total: `100 × 1.25^60 ≈ 65.3` million.

    A strong answer ties the numbers to time. If XP per hour grows slower than 25% per level, the last few levels take most of the play time, and the first 30 levels are almost free.

    </details>

## Week 5. Logarithms

19. **Week 5 · compute · midterm, final.** A building has base cost 250 and each copy raises the next price by 10%. How many can a player buy from zero with 1,000,000? With 2,000,000? With 4,000,000? Explain the pattern with a logarithm.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** 62, 70 and 77. Each doubling of the budget adds `log_1.1(2) ≈ 7.27` buildings.

    `N(C) = floor( ln(1 + 0.1·C / 250) / ln 1.1 )`. For 1,000,000: `ln(401) / 0.09531 = 62.89`, so 62. For 2,000,000: `ln(801) / 0.09531 = 70.2`, so 70. For 4,000,000: `ln(1,601) / 0.09531 = 77.4`, so 77.

    For large budgets `N ≈ log_1.1(C) + constant`, and doubling `C` adds `log_1.1(2) = 7.27`. The floors make the observed steps 8 and 7.

    </details>

20. **Week 5 · compute · midterm, final.** A ranked mode removes 5% of a player's points for each day they do not play. A player at 3,000 points stops logging in. On which day do they first fall below 1,000? Check the neighbouring days.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** Day 22.

    Solve `3,000 × 0.95^n < 1,000`, so `0.95^n < 1/3` and `n > ln(1/3) / ln(0.95) = 21.42`. Both logs are negative, so the inequality direction is preserved when you divide. Check: after 21 days, `3,000 × 0.95^21 = 1,021.7`. After 22 days, `970.6`.

    </details>

21. **Week 5 · compute · midterm, final.** Using the logistic Elo formula `E = 1 / (1 + 10^(−D/400))` from [week 5](../lectures/w05-logarithms-how-many-levels-until.md): (a) Player A is rated 1,850 and player B 1,550. What is A's expected score? (b) What rating gap gives the stronger player an expected score of 0.95?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) About 0.85. (b) About 512 points.

    (a) `D = 300`. `E = 1 / (1 + 10^−0.75) = 1 / (1 + 0.178) = 0.849`.

    (b) Expected score 0.95 means odds of `0.95 / 0.05 = 19`. `D = 400 × log₁₀(19) = 400 × 1.279 = 511.5`.

    </details>

22. **Week 5 · design · midterm, final.** An idle-game designer wants each doubling of a player's wealth to buy exactly 8 upgrades. (a) What growth factor and growth rate per upgrade does that require? (b) With a base cost of 40, how many upgrades can a player afford from zero with 100,000 and with 1,000,000? (c) Check that the difference fits the rule.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) `b = 2^(1/8) ≈ 1.0905`, a growth rate of about 9.05%. (b) 62 and 89. (c) Ten times the wealth is `log₂(10) ≈ 3.32` doublings, worth about `8 × 3.32 = 26.6` upgrades. The table gives 27.

    (a) If `k` purchases per doubling is the target, `b^k = 2`, so `b = 2^(1/k)`.

    (b) `N(C) = floor( ln(1 + 0.0905·C / 40) / ln 1.0905 )`. For 100,000 this is `floor(62.6) = 62`. For 1,000,000 it is `floor(89.2) = 89`.

    </details>

23. **Week 5 · compute · midterm, final.** Using the RuneScape inversion `L ≈ 7 · log₂((xp + 796) / 720.5)` from week 5, estimate the level for 250,000 XP. The exact table lists 247,886 XP for level 59 and 273,742 XP for level 60. Does your estimate agree? About how much XP does level 66 need?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** About 59.1, so level 59, which agrees with the table. Level 66 needs roughly double, about 500,000 XP (the exact table value is 496,254).

    `(250,000 + 796) / 720.5 = 348.1`. `log₂(348.1) = 8.44`. `7 × 8.44 = 59.1`. The unrounded constants from week 4, 720.53 and 795.53, give the same 59.1. 250,000 lies between the level-59 and level-60 thresholds, so the player is level 59.

    Seven more levels is one more doubling of total XP, so about `2 × 250,000 = 500,000`.

    </details>

24. **Week 5 · explain · midterm, final.** An options menu has a volume slider `v` from 0 to 1. Version 1 treats `v` as amplitude, so the mixer receives `20 · log₁₀(v)` dB. Version 2 maps the slider linearly onto −40 to 0 dB. (a) What gain does each version send at `v = 0.25` and `v = 0.5`? (b) Explain which version gives more even control across the slider, and why.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) Version 1: −12.0 dB at 0.25 and −6.0 dB at 0.5. Version 2: −30 dB at 0.25 and −20 dB at 0.5. (b) Version 2. Hearing responds roughly to ratios, which decibels already measure, so equal slider travel should mean equal dB steps.

    Version 1: `20 log₁₀(0.25) = −12.04` and `20 log₁₀(0.5) = −6.02`. The top half of that slider spans only 6 dB, so it barely changes loudness. Most of the audible range is squeezed into the bottom tenth. Version 2 changes the level by 4 dB for every tenth of travel. A full answer notes that version 2 needs its lowest position snapped to silence.

    </details>

## Week 6. Rational functions and A/(A + K)

25. **Week 6 · compute · midterm, final.** A game uses mitigation `A / (A + K)` with `K = 300`. A tank has 1,500 health. (a) How much armor gives 70% mitigation? (b) What is the tank's effective HP there? (c) How much EHP does each point of armor add?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) 700. (b) 5,000. (c) 5 EHP per point, at every armor value.

    (a) `A = K · m / (1 − m) = 300 × 0.7 / 0.3 = 700`.

    (b) `EHP = H · (1 + A / K) = 1,500 × (1 + 700/300) = 5,000`. Check: `1,500 / 0.3 = 5,000`.

    (c) The EHP line has slope `H / K = 1,500 / 300 = 5`.

    </details>

26. **Week 6 · compute · midterm, final.** A patch note gives armor reduction as `0.06·A / (1 + 0.05·A)`. (a) Rewrite it as a scale factor times `A / (A + K)`. (b) Give its horizontal and vertical asymptotes. (c) How much armor halves damage? (d) Where does the formula reach 100% reduction?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) `1.2 · A / (A + 20)`. (b) Horizontal asymptote 1.2 (120%). Vertical asymptote at `A = −20`. (c) About 14.3 armor. (d) At `A = 100`.

    (a) Divide top and bottom by 0.05: `1.2A / (20 + A)`.

    (b) Horizontal asymptote `a / c = 0.06 / 0.05 = 1.2`. Vertical asymptote where `0.05A + 1 = 0`, `A = −20`.

    (c) Solve `f(A) = 0.5`: `A = (0.5 × 1 − 0) / (0.06 − 0.5 × 0.05) = 0.5 / 0.035 = 14.29`. The scale factor moves the half point below `K = 20`.

    (d) `0.06A = 1 + 0.05A` gives `A = 100`. Past 100 armor the formula promises more than 100% reduction, so it needs a clamp.

    </details>

27. **Week 6 · compute · midterm, final.** In classic-era World of Warcraft (attacker levels 1 to 59), armor mitigation is `armor / (armor + 400 + 85 × attacker level)`, capped at 75% (week 6). Against a level-45 attacker: (a) what is `K`? (b) What does 3,000 armor mitigate? (c) How much armor reaches the cap?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) 4,225. (b) About 41.5%. (c) 12,675.

    `K = 400 + 85 × 45 = 4,225`. `3,000 / 7,225 = 0.415`. The cap is reached when `A / (A + K) = 0.75`, so `A = 3K = 12,675`.

    </details>

28. **Week 6 · compute · midterm, final.** Using League of Legends' ability haste rule `cooldown = base × 100 / (100 + haste)` from week 6, an ability has a 12 s base cooldown. (a) What is its cooldown at 80 haste? (b) How many casts per minute is that? (c) How many casts per minute does each 10 haste add?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) 6.67 s. (b) 9 casts per minute. (c) 0.5, at every haste value up to League's hard cap of 500 haste (week 7).

    (a) `12 × 100 / 180 = 6.67`. (b) `60 / 6.67 = 9`. (c) Casts per minute is `(60 / 12) × (1 + haste / 100) = 5 + 0.05 × haste`, a line with slope 0.05 per haste. The line stops at the 500-haste cap, far above the 80 here.

    </details>

29. **Week 6 · critique · midterm, final.** A designer must choose a soft-capped "toughness" stat that players can stack without limit. Option R is `A / (A + K)`. Option E is `1 − 0.5^(A/K)`. Compare the two at `A = 4K` in mitigation and in EHP multiplier, and recommend one for a game with long gear progression.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** At `A = 4K`, R gives 80% mitigation and an EHP multiplier of 5. E gives 93.75% and a multiplier of 16. Recommend R.

    R's EHP multiplier is `1 + A/K`, a line. E's is `2^(A/K)`, an exponential. The two agree at `A = K` (50%, ×2) and then split. Under long progression E makes stacked characters nearly unkillable, and each point of toughness is worth more than the last, which invites stacking. R gives every point the same survival. A good answer also says when E could be right, for example a short game where the designer wants stacking to feel explosive and caps the input.

    </details>

30. **Week 6 · critique · midterm, final.** A game computes damage taken as `D × K / (A + K)` with `K = 100`, and an armor-shred debuff can push armor below zero. (a) What damage multiplier does a target at −90 armor take? At −99? What happens at −100? (b) Propose a fix and compute its value at −90 armor.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) 10× at −90, 100× at −99, and a division by zero at −100. (b) Use a separate rule for negative armor, such as League's `2 − 100 / (100 − A)`, which gives 1.47× at −90 and never exceeds 2×. Clamping armor at 0 is also acceptable.

    (a) `100 / 10 = 10` and `100 / 1 = 100`. The vertical asymptote at `A = −K` is reachable in play.

    (b) `2 − 100 / 190 = 1.474`. As `A` falls, the multiplier approaches 2. A clamp `max(A, 0)` is simpler but makes shred useless below zero. The answer should name that trade-off.

    </details>

## Week 7. Piecewise functions, caps and floors

31. **Week 7 · compute · midterm, final.** A stat uses `f(x) = 4x` for `x < 15`, `60 + 1.5·(x − 15)` for `15 ≤ x < 35`, and `90 + 0.5·(x − 35)` for `x ≥ 35`. (a) Is it continuous at each breakpoint? (b) What is the per-point gain on each piece? (c) Compute `f(10)` and `f(50)`. (d) Is each breakpoint a kink or a jump?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) Yes at both. (b) 4, 1.5 and 0.5. (c) 40 and 97.5. (d) Both are kinks (soft caps).

    At 15 the first piece gives 60 and the second gives 60. At 35 the second gives `60 + 30 = 90` and the third gives 90. Values agree and slopes differ, so the graph has corners, not gaps. `f(10) = 40`. `f(50) = 90 + 7.5 = 97.5`.

    </details>

32. **Week 7 · compute · midterm, final.** A game computes effective resistance as `clamp(listed − penalty, −100, 75)`. A programmer writes `clamp(listed, −100, 75) − penalty` by mistake. With a penalty of 60, compute both versions for listed resistance 95 and 160, and say what the bug does to players who stack resistance.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** Listed 95: correct 35, buggy 15. Listed 160: correct 75, buggy 15. The bug makes every point of resistance above 75 worthless, so stacking for the penalty stops working.

    Correct: `clamp(35) = 35` and `clamp(100) = 75`. Buggy: `clamp(95) = 75`, minus 60 is 15, and `clamp(160) = 75`, minus 60 is 15. The cap applied before the penalty erases the buffer players built.

    </details>

33. **Week 7 · compute · midterm, final.** A game defines `crit = min(0.015 × agility, 0.40)`. (a) At what agility does crit reach the cap? (b) A player has 35 agility. How many points are above the cap? (c) What is the per-point gain just below and just above the cap?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) 26.7, so 27 whole points reach it. (b) About 8 points (8.3 in exact terms). (c) 1.5 percentage points below, 0 above.

    `0.015 × A = 0.40` gives `A = 26.67`. At 26 agility crit is 39%. At 27 it would be 40.5%, clamped to 40%. `35 − 26.67 = 8.33` points buy nothing.

    </details>

34. **Week 7 · design · midterm, final.** Design a Stamina stat that runs from 10 to 60 and gives stamina points (SP) from 100 to 300. Use soft caps at 30 and 45, and make the per-point gain halve at each soft cap. Give the gain on each piece, write the function, and give SP at 30, 45 and 60.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** Gains 6.4, 3.2 and 1.6 SP per point. `SP = 100 + 6.4(S − 10)` for `10 ≤ S ≤ 30`, `228 + 3.2(S − 30)` for `30 < S ≤ 45`, `276 + 1.6(S − 45)` for `45 < S ≤ 60`. SP is 228 at 30, 276 at 45 and 300 at 60.

    The pieces are 20, 15 and 15 points long. With first gain `g`, the total is `20g + 15(g/2) + 15(g/4) = 31.25g = 200`, so `g = 6.4`. Check continuity at 30 (`100 + 128 = 228` from both sides) and at 45 (`228 + 48 = 276`).

    Grade other designs that meet the brief on the same basis: continuous, gain halves at each cap, never zero, endpoints 100 and 300.

    </details>

35. **Week 7 · critique · midterm, final.** A crafting skill gives success chance `0.40 + 0.01·s` for `s < 50` and `0.95` for `s ≥ 50`. (a) Compute the chance at 49 and at 50, and the size of the jump compared with the per-point gain. (b) What will players do? (c) Propose a continuous alternative that still reaches 95%.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) 0.89 at 49 and 0.95 at 50, a jump of 6 points against a gain of 1 point per level. After 50 the gain is 0. (b) Players will grind to exactly 50 and stop. (c) For example `0.40 + 0.01·s` up to 50 (reaching 0.90), then `0.90 + 0.0025·(s − 50)` up to 70 (reaching 0.95), capped there.

    The jump creates a breakpoint hunt. Skill 49 feels wasted and 51 is worthless. The alternative is continuous at 50 (0.90 from both sides) and has a smaller, non-zero gain until the cap. Any answer that removes the jump, keeps the gain above zero below the cap and reaches 95% earns full marks.

    </details>

## Week 8. Lerp, inverse lerp and remap

36. **Week 8 · compute · final.** Compute `lerp(−8, 24, 0.375)`, `inverseLerp(90, 30, 45)` and `remap(7, 2, 12, 100, 40)`.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** 4, 0.75 and 70.

    `−8 + 32 × 0.375 = 4`. `(45 − 90) / (30 − 90) = −45 / −60 = 0.75`. `inverseLerp(2, 12, 7) = 0.5`, then `lerp(100, 40, 0.5) = 70`.

    </details>

37. **Week 8 · compute · final.** A shotgun deals 60 damage at 10 m or closer and 20 damage at 40 m or farther, linear in between. Write it as a clamped remap and compute damage at 4, 18, 25 and 50 m.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** `damage = clampedRemap(d, 10, 40, 60, 20)`. Values: 60, 49.3, 40 and 20.

    At 4 m, `t = −0.2`, clamped to 0, so 60. At 18 m, `t = 8/30 = 0.267`, so `60 − 40 × 0.267 = 49.3`. At 25 m, `t = 0.5`, so 40. At 50 m, `t` clamps to 1, so 20.

    </details>

38. **Week 8 · compute · final.** A camera uses `x = lerp(x, target, 0.15)` every frame. It was tuned at 60 fps. (a) What fraction of the gap is left after 0.5 s at 30, 60 and 144 fps? (b) What `k` per frame at 144 fps matches the 60 fps behaviour? (c) Give the decay rate `λ` for the frame-rate-safe form `k = 1 − e^(−λ·dt)`.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) 0.087 at 30 fps, 0.0076 at 60 fps, about 0.0000083 at 144 fps. (b) About 0.0655. (c) About 9.75 per second.

    (a) The gap after `n` frames is `0.85^n`. Half a second is 15, 30 or 72 frames. `0.85^15 = 0.087`, `0.85^30 = 0.0076`, `0.85^72 ≈ 8.3 × 10⁻⁶`.

    (b) At 144 fps, 144/60 frames must shrink the gap as much as one 60 fps frame: `(1 − k)^(144/60) = 0.85`, so `k = 1 − 0.85^(60/144) = 0.0655`.

    (c) One 60 fps frame leaves `e^(−λ/60) = 0.85`, so `λ = −60 ln 0.85 = 9.75`.

    </details>

39. **Week 8 · compute · final.** Using Celeste's landing squash from [week 8](../lectures/w08-interpolation-lerp-inverse-lerp-remap.md) (`squish = min(v/240, 1)`, `scaleX = lerp(1, 1.6, squish)`, `scaleY = lerp(1, 0.4, squish)`, recovery at 1.75 scale units per second), Madeline lands at 180 px/s. Compute `squish`, both scales, the recovery time and the sprite's area as a fraction of normal.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** `squish = 0.75`, `scaleX = 1.45`, `scaleY = 0.55`, recovery about 0.26 s, area about 0.80 of normal.

    `180 / 240 = 0.75`. `1 + 0.6 × 0.75 = 1.45`. `1 − 0.6 × 0.75 = 0.55`. Each scale is 0.45 from 1, so recovery takes `0.45 / 1.75 = 0.257` s. Area `1.45 × 0.55 = 0.7975`.

    </details>

## Week 9. Easing curves

40. **Week 9 · compute · final.** (a) Compute `CubeInOut(0.3)` and `CubeInOut(0.7)`. (b) A dash covers 120 px in 0.3 s using `QuadOut`. Where is the character after 0.075 s, and what is its speed at the start in px/s?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) 0.108 and 0.892. (b) 52.5 px, and 800 px/s at the start.

    (a) `0.3 ≤ 0.5`, so `4 × 0.027 = 0.108`. `0.7 > 0.5`, so `1 − 4 × 0.3³ = 1 − 0.108 = 0.892`.

    (b) `t = 0.075 / 0.3 = 0.25`. `QuadOut(0.25) = 1 − 0.75² = 0.4375`, times 120 is 52.5 px. Average speed is `120 / 0.3 = 400` px/s. QuadOut starts at twice the average, 800 px/s.

    </details>

41. **Week 9 · compute · final.** A notification slides 200 px over 0.5 s using smoothstep `S(t) = 3t² − 2t³`. (a) Where is it after 0.15 s? (b) What is its speed at that moment in px/s? (Its slope is `6t − 6t²`.) (c) What is its peak speed?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) 43.2 px. (b) 504 px/s. (c) 600 px/s, at the midpoint.

    `t = 0.15 / 0.5 = 0.3`. `S(0.3) = 0.27 − 0.054 = 0.216`, times 200 is 43.2. Slope `1.8 − 0.54 = 1.26` times the average speed of 400 px/s is 504 px/s. Smoothstep peaks at slope 1.5, so 600 px/s.

    </details>

42. **Week 9 · design · final.** Choose an ease and a duration for (a) an inventory panel that slides in when the player presses I, and (b) a damage number that floats up and leaves the screen. Justify each choice with start and end speeds from the week 9 slope table.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** A model answer. (a) `CubeOut` or `QuadOut`, about 0.15 to 0.25 s. (b) `QuadIn` or a linear rise with a fade, about 0.6 to 1.0 s.

    (a) The panel responds to input, so it needs speed on frame 1. CubeOut starts at 3× average speed and ends at 0. At 0.2 s and 60 fps, frame 2 (`t ≈ 0.17`) shows about 42% of the motion. An ease-in would start at speed 0 and read as input lag. The panel also arrives and stays, which fits a decelerating ease.

    (b) The number is not player-controlled and it leaves without stopping, so an accelerating ease fits. QuadIn ends at 2× average speed, which reads as "gone".

    Accept other choices argued from the two questions (does it respond to input? is it arriving or leaving?) with correct start and end speeds.

    </details>

43. **Week 9 · critique · final.** A designer animates a health bar's fill from 0 to its full 200 px width with `BackOut` after a full heal. What is the largest width the bar reaches? Explain the problem and propose a fix.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** About 220 px, 10% past the frame. Clamp the output to 200 px, or use `CubeOut` or `QuadOut`, which never exceed 1.

    `BackOut` peaks at about 1.100 near `t ≈ 0.58`. `1.1 × 200 = 220`. For a health bar the width is a readout of a real number, so a bar showing 110% health is a lie. The fill can also draw outside its frame. Overshoot suits buttons and icons, not values with a legal range.

    </details>

## Week 10. Angles, radians, sin and cos

44. **Week 10 · compute · final.** Five orbs circle a player at the origin with `r = 120` px, `ω = 2π/3` rad/s and `θ0 = 0` (math convention, y up). Where is orb 3 (counting from 0) at `t = 0.75` s?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** At 306°, position about (70.5, −97.1).

    `θ₃ = 0 + (2π/3)(0.75) + 2π × 3/5 = π/2 + 6π/5 = 17π/10`, which is 306°. `120 cos 306° = 120 × 0.588 = 70.5`. `120 sin 306° = 120 × (−0.809) = −97.1`.

    </details>

45. **Week 10 · compute · final.** A ring of orbs has radius 150 px and the chord gap between neighbours must be at most 80 px. (a) What is the smallest number of orbs? (b) With `ω = π/2` rad/s, how many hits per second land on a fixed spot of the ring? (c) How fast does each orb move?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) 12 orbs. (b) 3 hits per second. (c) About 236 px/s.

    (a) `2 × 150 × sin(π/N) ≤ 80`, so `sin(π/N) ≤ 0.267`, `π/N ≤ 0.270`, `N ≥ 11.6`. With 12 orbs the chord is 77.6 px. With 11 it is 84.5 px, too wide.

    (b) `N·ω / 2π = 12 × (π/2) / (2π) = 3`.

    (c) `ω·r = (π/2) × 150 = 235.6` px/s.

    </details>

46. **Week 10 · compute · final.** A script places a shield with `(r·cos(30), r·sin(30))`, meaning 30°. (a) What values do `sin(30)` and `cos(30)` return in a standard library? (b) At what angle in degrees does the shield actually sit? (c) Write the fix.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) `sin(30) ≈ −0.988`, `cos(30) ≈ 0.154`. (b) About 278.9°. (c) Convert at the boundary, `θ = 30 × π / 180 = 0.524`, giving 0.5 and 0.866.

    The library reads 30 as radians. `30 × 180/π = 1,718.9°`, which is 4 full turns plus 278.9°. That is down and slightly right, far from the intended up-right position.

    </details>

47. **Week 10 · compute · final.** A coin bobs up and down 8 px from its rest position, one full cycle every 1.25 s. (a) Give its frequency and angular speed. (b) What is its offset at `t = 0.5` s if its phase is 0? (c) Ten coins in a row should ripple so the wave travels once along the row. What phase does coin `k` get?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) `f = 0.8` Hz, `ω = 1.6π ≈ 5.03` rad/s. (b) About +4.70 px. (c) `φ_k = 2πk / 10`.

    `f = 1 / 1.25 = 0.8`. `ω = 2πf`. Offset `8 sin(2π × 0.8 × 0.5) = 8 sin(0.8π) = 8 × 0.588 = 4.70`. The ripple uses the same `2πk/N` spacing as orbs on a ring, applied in time.

    </details>

## Week 11. atan2 and turning toward a target

48. **Week 11 · compute · final.** A turret at (−20, 50) aims at a player at (−140, −40) in a y-up world. What angle does `atan2` return? What does `atan(dy/dx)` return, and how far off is it?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** `atan2` gives −143.1°. `atan(dy/dx)` gives 36.9°, exactly 180° off.

    `dx = −120`, `dy = −90`. `atan2(−90, −120) = −143.13°`, down and to the left. `atan(−90 / −120) = atan(0.75) = 36.87°`, up and to the right. Both components are negative, so the ratio is positive and `atan` reflects the direction through the origin.

    </details>

49. **Week 11 · compute · final.** A Dota 2 hero faces 160° and is ordered toward a target at −95°. (a) What is the shortest signed turn? (b) Using the week 11 model (turn rate in radians per 0.03 s, acting once within 11.5° = 0.2007 rad), how long before it can act at turn rate 0.6? At 0.5?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) +105° (counterclockwise). (b) About 0.082 s at 0.6 and 0.098 s at 0.5.

    (a) Raw `−95 − 160 = −255`. Wrapped: `−255 − 360 × round(−0.708) = −255 + 360 = 105`.

    (b) `105° = 1.8326` rad. Time `= 0.03 × (1.8326 − 0.2007) / turn_rate`. At 0.6: `0.03 × 1.6319 / 0.6 = 0.0816`. At 0.5: `0.0979`.

    </details>

50. **Week 11 · compute · final.** A homing missile flies at 520 px/s and turns at most 200° per second. (a) What is its turning radius? (b) A target sits 90 px to the side of the missile's path. What minimum turn rate, in degrees per second, lets the missile turn inside a 90 px circle?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) About 149 px. (b) About 331° per second.

    (a) `ω = 200 × π/180 = 3.491` rad/s. `R = v / ω = 520 / 3.491 = 149.0`.

    (b) `ω = v / R = 520 / 90 = 5.78` rad/s, which is `5.78 × 180/π = 331°/s`.

    </details>

51. **Week 11 · explain · final.** A C# turret computes `delta = (target − current) % 360` with `current = 170` and `target = −130`. (a) What value does the code get, and what is the shortest turn? (b) Why does `%` fail here, and what formula works in every language? (c) Why is lerping the raw angles from 170° to −130° also wrong?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) The code gets −300, so the turret swings 300° clockwise. The shortest turn is +60°. (b) C#'s `%` keeps the sign of the left operand. Use `delta = raw − 360 × round(raw / 360)`. (c) A raw lerp passes through 20°, 0° and so on, turning the long way.

    Raw `−130 − 170 = −300`. `−300 % 360 = −300` in C#. `round(−300/360) = round(−0.833) = −1`, so `delta = −300 + 360 = 60`. For a smooth turn, lerp the wrapped delta: `facing + delta × k`.

    </details>

## Week 12. 2D vectors

52. **Week 12 · compute · final.** Normalize `(−8, 15)` and give the velocity for a speed of 34 units/s in that direction. What should the code do if the input is `(0, 0)`?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** `(−0.471, 0.882)`. Velocity `(−16, 30)`. For `(0, 0)`, skip the division and use a zero velocity (or keep the last facing).

    `|(−8, 15)| = √(64 + 225) = 17`. `(−8/17, 15/17)`. Times 34 gives `(−16, 30)`. Check `√(256 + 900) = 34`. Dividing `(0, 0)` by its length 0 gives NaN, which spreads to position.

    </details>

53. **Week 12 · compute · final.** A game moves the player forward at 6 units/s and sideways at 4 units/s, and adds the two as perpendicular vectors when both keys are held. (a) How fast does the player move with both held? (b) By what percentage does that beat moving forward only? (c) If the game clamps the combined length to 6, what are the two components?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) About 7.21 units/s. (b) About 20% faster. (c) About (4.99, 3.33).

    `√(36 + 16) = √52 = 7.21`. `7.21 / 6 = 1.20`. The clamp scales the vector by `6 / 7.21`: `(6 × 0.832, 4 × 0.832) = (4.99, 3.33)`. The ratio between forward and sideways is kept. Only the length changes.

    </details>

54. **Week 12 · compute · final.** A gamepad stick reports `(0.36, 0.48)` and the character's top speed is 12 units/s. Give the velocity under raw input, normalize and clamp-length-to-1. Which rule is right for a stick, and why?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** Raw `(4.32, 5.76)`, speed 7.2. Normalize `(7.2, 9.6)`, speed 12. Clamp `(4.32, 5.76)`, speed 7.2. Clamp-length is right.

    The input length is `√(0.1296 + 0.2304) = 0.6`. The player pushed the stick 60% of the way, so 60% speed is correct. Normalize throws that away and turns a gentle push into a sprint. Clamp leaves short vectors alone and only shrinks inputs longer than 1, such as `(0.9, 0.9)` from a square gate.

    </details>

55. **Week 12 · critique · final.** A team making a competitive top-down arena shooter for keyboard wants to keep un-normalized diagonal movement "like Doom". Using numbers from week 12, give one argument for and two against, and make a recommendation.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** A model answer. Diagonals are `√2 ≈ 1.414` times faster, 41% more speed. The argument for it is that Doom shows a movement quirk can become valued skill, and the team may want a high skill ceiling. The first argument against is that in a 100 × 100 room, corner to corner takes 20 s with the bug, the same as walking one wall, so players will zigzag through every level. The second is that every chase and dodge window tuned with straight-line speed is off by up to 41%, and for an arena shooter the fastest direction is fixed to the screen's diagonals, which feels arbitrary. The recommendation is to normalize (or clamp length) and, if a skill-based speed option is wanted, add it as an explicit mechanic with a tuned value.

    Grade on use of the 41% figure and a concrete consequence for level or combat design. Either recommendation earns full marks if argued with numbers.

    </details>

## Week 13. Dot product and vision cones

56. **Week 13 · compute · final.** A guard at (4, −2) faces `f̂ = (0.8, −0.6)`. Its half-angle is 35° and its range 18 m. The player stands at (18, −4). Is the player seen? Then repeat the test with the squared form (no square root) and confirm.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** Seen, about 28.7° off centre.

    `d = (14, −2)`, `|d| = 14.14`, inside 18. `d̂ = (0.990, −0.141)`. `f̂ · d̂ = 0.792 + 0.085 = 0.877`. The threshold is `cos 35° = 0.819`, and `0.877 ≥ 0.819`, so seen.

    Squared form: `f̂ · d = 11.2 + 1.2 = 12.4`, which is non-negative. `12.4² = 153.8`. `c² × (d · d) = 0.671 × 200 = 134.2`. `153.8 ≥ 134.2`, so seen.

    </details>

57. **Week 13 · compute · final.** A guard at the origin faces `(0, 1)` with half-angle 40°. The player is at (−7, 9), inside range. Decide whether the player is seen using only the squared form from week 13 section 5.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** Seen.

    `f̂ · d = 9`, non-negative. `(f̂ · d)² = 81`. `d · d = 49 + 81 = 130`. `c² = cos² 40° = 0.587`, so `c² × 130 = 76.3`. `81 ≥ 76.3`, so the player is inside. The angle, for display only, is about 37.9°.

    </details>

58. **Week 13 · compute · final.** A turret faces `f̂ = (0.6, 0.8)`. Two targets sit at offsets `(−3, 5)` and `(5, 1)`. For each, is it in front or behind, and should the turret turn left or right?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** `(−3, 5)` is in front and to the left. `(5, 1)` is in front and to the right.

    The left vector is `l̂ = (−f.y, f.x) = (−0.8, 0.6)`. For `(−3, 5)`: `f̂ · d = −1.8 + 4 = 2.2 > 0` (front), `l̂ · d = 2.4 + 3 = 5.4 > 0` (left). For `(5, 1)`: `f̂ · d = 3 + 0.8 = 3.8 > 0` (front), `l̂ · d = −4 + 0.6 = −3.4 < 0` (right).

    </details>

59. **Week 13 · compute · final.** A detection meter uses `focus = clamp(invlerp(cos 45°, cos 15°, f̂ · d̂), 0, 1)`. Compute focus for players 10°, 20°, 30° and 40° off centre, and describe the shape of the falloff.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** 1.00, 0.90, 0.61 and 0.23. Focus stays high near 15° and drops faster toward the 45° edge.

    `cos 45° = 0.707`, `cos 15° = 0.966`. At 10°, `cos = 0.985`, above the top, so 1. At 20°: `(0.940 − 0.707) / 0.259 = 0.899`. At 30°: `(0.866 − 0.707) / 0.259 = 0.614`. At 40°: `(0.766 − 0.707) / 0.259 = 0.228`. Equal angle steps give unequal focus steps because cosine is flat near 0° and steeper further out.

    </details>

60. **Week 13 · critique · final.** A design document says "the guard sees 90°". A designer sets Unreal's `PeripheralVisionAngleDegrees` to 90 (which week 13 shows is a half-angle). (a) What cone does the guard get, and what is its threshold `c`? (b) What should the document have said? (c) The same designer sets a turret to fire when `f̂ · d̂ ≥ 0.998`. Within how many degrees of perfect aim is that?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) A 180° cone with `c = 0`. The guard sees the whole half-plane in front of it. (b) "Half-angle 45°, full cone 90°, `c = 0.707`" (if a 90° total was meant). (c) About 3.6°.

    A half-angle of 90° gives `cos 90° = 0`, the plain front-or-behind sign test. That is twice the angle the designer probably intended. `acos(0.998) = 3.62°`. The fix is to write the half-angle and the stored `c` in the spec so no one guesses.

    </details>

## Week 14. Distances and ranges

61. **Week 14 · compute · final.** A game uses Minecraft-style despawn rings with `r_near = 24` and `r_far = 96` blocks. A mob is at the origin and the nearest player at offset (50, 70, 10). Compute the squared distance, the stored thresholds and the zone, without a square root.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** `S = 7,500`. Thresholds 576 and 9,216. Random zone.

    `S = 2,500 + 4,900 + 100 = 7,500`. `24² = 576` and `96² = 9,216`. `576 < 7,500 ≤ 9,216`. The real distance, for humans only, is 86.6.

    </details>

62. **Week 14 · compute · final.** Compute Euclidean, Manhattan, Chebyshev and the D&D 3.5 alternating-diagonal distance for offsets (7, 3) and (8, 8). Which metric is closest to Euclidean on the pure diagonal?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (7, 3): 7.62, 10, 7, 8. (8, 8): 11.31, 16, 8, 12. The alternating rule is closest on the diagonal.

    Euclidean `√58 = 7.62` and `√128 = 11.31`. Manhattan `7 + 3` and `8 + 8`. Chebyshev `max`. Alternating `max + floor(min/2)`: `7 + 1 = 8` and `8 + 4 = 12`. On the diagonal the alternating rule counts about 1.5 per step against `√2 ≈ 1.414`.

    </details>

63. **Week 14 · compute · final.** A mob has aggro radius 12 m and leash radius 35 m and starts IDLE. The player is at these distances on successive checks: 30, 14, 11, 20, 34, 36. Give the mob's state after each check and the squared values the code compares. What would a single 12 m radius have done at the 20 m check?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** IDLE, IDLE, CHASE, CHASE, CHASE, RETURN. A single radius would have dropped the chase at 20 m.

    Stored thresholds `12² = 144` and `35² = 1,225`. IDLE checks `S ≤ 144`: 900 no, 196 no, 121 yes (CHASE). CHASE checks `S > 1,225`: 400 no, 1,156 no, 1,296 yes (RETURN).

    </details>

64. **Week 14 · compute · final.** Positions are stored as 32-bit signed integers in millimetres. (a) Beyond what single-axis difference does `dx²` overflow? (b) On an exact diagonal, beyond what per-axis difference does `dx² + dy²` overflow? Give both in metres.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) About 46.3 m (46,341 mm). (b) About 32.8 m per axis (32,768 mm).

    The maximum is `2³¹ − 1 = 2,147,483,647`. `√ of that = 46,340.95`, so 46,340 mm is safe and 46,341 overflows. On a diagonal `2·dx² ≤ 2³¹ − 1` gives `dx ≤ 32,767.99`, so 32,768 mm overflows. Use 64-bit integers or floating point for `S`.

    </details>

65. **Week 14 · compute · final.** Two circular hitboxes have radius 0.75 at (2, 3) and radius 1.1 at (3.2, 4.4). Do they overlap? What threshold should the code store, and what answer does the common wrong threshold give?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** Yes, they overlap. Store `(0.75 + 1.1)² = 3.4225`. The wrong threshold `0.75² + 1.1² = 1.7725` says no.

    `S = 1.2² + 1.4² = 1.44 + 1.96 = 3.40 ≤ 3.4225`. The centres are 1.844 apart and the radii sum to 1.85, so they overlap by 0.006. Squaring each radius separately shrinks every hitbox.

    </details>

## Cross-week questions (final only)

66. **Weeks 6 and 7 · design · final.** A designer wants crit chance from a rating `A` to reach 25% at 100 rating and never exceed 50%. Option 1 is `0.5 · A / (A + K)`. Option 2 is `min(0.0025·A, 0.5)`. (a) Find `K` for option 1. (b) Tabulate both at 50, 100, 200 and 400 rating. (c) Where does each stop paying, and which would you ship?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) `K = 100`. (b) Option 1: 16.7%, 25%, 33.3%, 40%. Option 2: 12.5%, 25%, 50%, 50%. (c) Option 2 stops paying at 200 rating (hard cap, dead zone after). Option 1 never stops but slows. Ship option 1 if players stack the stat over a long progression; option 2 if you want a clear build target and accept the dead zone.

    With scale 0.5, the value at `A = K` is `0.5 × 0.5 = 25%`, so `K = 100`. Option 1 reaches 40% only at `A = 0.4 × 100 / (0.5 − 0.4) = 400`. Option 2 hits 50% at `0.5 / 0.0025 = 200`.

    </details>

67. **Weeks 2 and 6 · compute · final.** A champion has 2,000 health and 100 armor, with `K = 100`. Item H gives +300 health. Item R gives +40 armor. (a) Compute EHP after each item. (b) At 100 armor, at what health do the two items tie? (c) Which item is better for a 1,200-health champion with 100 armor?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** (a) Item H gives 4,600 EHP, item R gives 4,800. (b) 1,500 health. (c) Item H (+600 EHP against +480).

    `EHP = H·(1 + A/K)`. Now: `2,000 × 2 = 4,000`. Item H: `2,300 × 2 = 4,600`. Item R: `2,000 × 2.4 = 4,800`. Health adds `300 × (1 + A/K)` and armor adds `40 × H/K`. Set equal at `A = 100`: `600 = 0.4·H`, so `H = 1,500`. At 1,200 health the armor adds `40 × 12 = 480`. Each stat is worth more when the other is high.

    </details>

68. **Weeks 8, 9 and 13 · compute · final.** Take the detection meter from question 59 (focus 0.614 at 30° and 0.228 at 40°) and pass focus through smoothstep before using it. What are the new values at 30° and 40°, and how does the change affect a player sneaking near the edge of the cone?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** 0.668 at 30° and 0.132 at 40°. Near the edge detection now fills even more slowly, widening the safe margin at the cone's edge while leaving the middle nearly unchanged.

    `S(0.614) = 3 × 0.377 − 2 × 0.2315 = 0.668`. `S(0.228) = 3 × 0.0519 − 2 × 0.0118 = 0.132`. Smoothstep has slope 0 at both ends, so it flattens the response near 0 and near 1. The designer should choose this on purpose. It rewards edge play more than the plain remap.

    </details>

69. **Weeks 10, 12 and 14 · compute · final.** A turret at the origin aims at `atan2(3, 4)` and fires a bullet of radius 4 at 500 px/s. After 0.4 s, where is the bullet? A target of radius 12 sits at (150, 130). Is it hit? What does a programmer who stores `12² + 4²` as the threshold conclude?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** The bullet is at (160, 120). It hits. The wrong threshold of 160 reports a miss.

    `atan2(3, 4) = 36.87°`, direction `(0.8, 0.6)`. Velocity `(400, 300)`. After 0.4 s: `(160, 120)`, which is 200 px out. Offset to target `(−10, 10)`, `S = 200`. Correct threshold `(12 + 4)² = 256`, so `200 ≤ 256`, hit. Wrong threshold `144 + 16 = 160`, so `200 > 160`, miss.

    </details>

70. **Weeks 4 and 5 · design · final.** Design an exponential XP curve `xp(L) = a · 2^(L/d)` for a 40-level skill so that the halfway level is 35 and level 40 needs 2,000,000 XP. Then find the level a player with 500,000 XP has reached, and the XP for level 35.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** `d = 5`, `a = 7,812.5`, so `xp(L) = 7,812.5 · 2^(L/5)`. 500,000 XP reaches level 30. Level 35 needs 1,000,000.

    For a pure exponential with no constant term, the halfway level is exactly the cap minus one doubling interval, so `d = 40 − 35 = 5`. `a = 2,000,000 / 2^8 = 7,812.5`. Invert: `L = 5 · log₂(xp / 7,812.5)`. For 500,000: `log₂(64) = 6`, so `L = 30`. `xp(35) = 7,812.5 × 2^7 = 1,000,000`, half of the level-40 total as designed.

    </details>

71. **Weeks 1 and 7 · critique · final.** Two programmers disagree on where a damage floor goes. Version P: `damage = max(1, atk − def) × crit`. Version Q: `damage = max(1, atk × crit − def)`. An attack of 40 hits a target with 55 defense for a 2× crit. Compute both, and say which version the spec should choose and why.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer.** P gives 2. Q gives 25. A model answer recommends Q if crits should let weak attackers break through armor, and P if defense should reliably shut out weak attacks.

    P: `max(1, −15) = 1`, times 2 is 2. Q: `max(1, 80 − 55) = 25`. The floor and the multiplier do not commute. Under P, a crit is worth only 1 extra damage against high defense. Under Q, crit doubles attack before defense, so it can turn a blocked hit into real damage. Full marks require the two numbers and a reason tied to the intended role of defense.

    </details>
