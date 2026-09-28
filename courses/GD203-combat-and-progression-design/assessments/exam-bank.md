# GD203 · Exam bank: practice, quiz and viva questions

GD203 has no written exam. The grade comes from the spreadsheet labs (40%), the simulation (20%) and the final combat system spec (40%). This bank exists for three other jobs.

- **Practice.** Work the questions for a week before its lab is due. If you can do them without the lecture open, the lab will go quickly.
- **Weekly quizzes.** Each week opens with a 10-minute ungraded quiz of two or three questions from this bank, usually one compute question with new numbers and one explain or critique question.
- **Viva.** The final spec ends with a short oral defense ([final-spec-brief.md](final-spec-brief.md)). Examiners draw viva questions in the style of this bank, rewritten with the numbers from your own spec. The spreadsheet-lab spot checks ([spreadsheet-labs-brief.md](spreadsheet-labs-brief.md)) use the same style.

Every question is tagged with the week or weeks it draws on and a type.

- **compute**: apply a lecture model to numbers you have not seen before.
- **explain**: say why a model behaves the way it does, with a number as evidence.
- **design**: choose values that meet a stated goal and show they meet it.
- **critique**: find what is wrong with a proposal and say how to fix it.

All numbers are fictional unless a question names a game, and every game fact used here comes from the lecture of the tagged week, which cites its source and version. Answers were recomputed in Python. Where rounding matters, the solution says how it was rounded. Open the answer only after you have written your own.

---

## Week 1: Stats as design language

1. *Week 1 · compute.* A character's additive damage pool already sits at +200% (a multiplier of 3.0). They can take one of two rewards, a +30% additive bonus that joins the same pool, or a +30% multiplicative bonus. By what fraction does each raise their damage?

<details>
<summary>Answer and worked solution</summary>

**Answer:** the additive bonus adds 10.0%, the multiplicative bonus adds 30%.

Additive: the pool goes from 3.0 to 3.3. The relative gain is `p / (1 + P) = 0.3 / 3.0 = 10%`.

Multiplicative: `3.0 × 1.3 = 3.9`, a gain of 30% whatever the pool held before.

The tooltips read the same. The additive bonus is diluted by everything already in the pool.
</details>

2. *Week 1 · compute.* Use the Diablo III main-stat model from the lecture, damage multiplier `1 + S/100`. A character has 3,000 main stat. (a) What real damage gain does an item with +150 main stat give? (b) How much more main stat does the character need to raise damage by 20%?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) about 4.8%. (b) 620 more main stat.

(a) The gain from `ΔS` is `ΔS / (100 + S) = 150 / 3,100 = 0.0484`, so 4.8%.

(b) The multiplier is `1 + 3,000/100 = 31`. A 20% gain means `31 × 1.2 = 37.2`. Solve `1 + S/100 = 37.2`, so `S = 3,620`. That is 620 more than the character has.
</details>

3. *Week 1 · compute.* In a Path of Exile style system, "increased" bonuses add into one pool and "more" bonuses multiply on their own. A skill has 500 base damage and 150% increased damage already. Option X is another 50% increased. Option Y is 30% more. Which gives more damage, and how large would an "increased" bonus have to be to match option Y?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Y. It gives 1,625 damage (+30%) against X's 1,500 (+20%). An increased bonus would need to be 75% to match it.

Current damage: the pool is `1 + 1.5 = 2.5`, so `500 × 2.5 = 1,250`.

X: `500 × (1 + 1.5 + 0.5) = 500 × 3.0 = 1,500`, a gain of `0.5 / 2.5 = 20%`.

Y: `1,250 × 1.3 = 1,625`, a gain of 30%.

To match a 30% gain from the pool, the increased bonus `p` must satisfy `p / 2.5 = 0.30`, so `p = 75%`. The one word "more" is worth half again as much as a bigger-looking number.
</details>

4. *Week 1 · critique.* A stat sheet for a three-class game has these four primary stats. **Power** raises attack damage, healing done, maximum health and movement speed. **Attack Power** adds 1 damage per 10 points. **Weapon Bonus** adds 1 damage per 10 points into the same pool as Attack Power. **Spirit** raises mana regeneration, and only one of the three classes uses mana. Name the problem with each stat and propose a fix for each.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Power is not orthogonal, Attack Power and Weapon Bonus overlap, and Spirit is dead for two classes.

Power secretly has four exchange rates (damage, healing, health, speed). It is hard to price and will become the stat every class stacks, because one point buys value everywhere. Split it into single-job stats, or keep it and price it at the sum of its four rates.

Attack Power and Weapon Bonus follow the same rule into the same pool. Players need a guide to tell them apart and the designer needs two prices for one effect. Merge them, or give Weapon Bonus a different rule (multiplicative, or scaling with weapon speed).

Spirit has an exchange rate of zero for two classes. That can be acceptable if loot is shared across classes, but it should be a written decision. Otherwise give Spirit a second job the other classes value, or remove it from their level-up screens.
</details>

## Week 2: Damage formulas

5. *Week 2 · compute.* A defender has 35 armor. Hits of 25, 70 and 350 arrive. What fraction of each gets through under subtractive armor with no floor? What fraction gets through under divisive armor with `K = 100`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** subtractive lets through 0%, 50% and 90%. Divisive lets through 74.1% of every hit.

Subtractive, `f = max(0, 1 − A/D)`. For 25: `35 ≥ 25`, so 0. For 70: `35/70 = 0.5`, so 50%. For 350: `1 − 35/350 = 0.9`.

Divisive, `f = K / (A + K) = 100 / 135 = 0.741`, the same for every hit size.
</details>

6. *Week 2 · compute.* A game uses divisive armor with `K = 150`. (a) What armor lets exactly 40% of a hit through? (b) In a second game with `K = 80`, a defender has 40 armor. At what hit size do subtractive and divisive armor let the same damage through? Which formula lets more of a 60-damage hit through, and which lets more of a 300-damage hit through?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 225 armor. (b) 120 damage. Divisive lets more of the 60-damage hit through (40 against 20). Subtractive lets more of the 300-damage hit through (260 against 200).

(a) `150 / (A + 150) = 0.4`, so `A + 150 = 375` and `A = 225`.

(b) The crossover is `D = A + K = 120`. Check: subtractive `120 − 40 = 80`, divisive `120 × 80 / 120 = 80`.

For 60: subtractive `60 − 40 = 20`, divisive `60 × 80/120 = 40`. For 300: subtractive 260, divisive `300 × 80/120 = 200`. Below `A + K` subtractive is harsher, above it subtractive is softer.
</details>

7. *Week 2 · compute.* A defender has a flat reduction of 15 and a 40% percent reduction, and damage cannot go below 0. For hits of 20, 60 and 400, compute the damage taken with the flat step first and with the percent step first. Separately, three percent layers of 25%, 15% and 10% are stacked. What is the total reduction?

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Hit | Flat first `(D − 15) × 0.6` | Percent first `D × 0.6 − 15` |
|---|---|---|
| 20 | 3 | 0 (12 − 15 is below 0) |
| 60 | 27 | 21 |
| 400 | 231 | 225 |

Percent first (flat last) protects the defender more, and the advantage is large for small hits. It cuts the 60-damage hit by a further 22% but the 400-damage hit by only 2.6%.

The three layers multiply: `0.75 × 0.85 × 0.90 = 0.574` gets through, so the total reduction is 42.6%, not 50%.
</details>

8. *Week 2 · design.* Your level-20 player has 120 armor under a subtractive formula. Rats hit for 15 and the zone boss hits for 300. The design promise is "ten rat hits still deal at least 15 damage in total to a level-20 player, and the floor never changes a boss hit." Choose a floor type and value, and show both parts of the promise hold.

<details>
<summary>Answer and worked solution</summary>

**Answer:** a percentage floor of 10% (`max(0.1 × D, D − A)`) meets the promise. Any value from 10% up to just below 60% works.

Rats: `max(1.5, 15 − 120) = 1.5` per hit, so ten hits deal 15. A lower percentage fails the 15 target.

Boss: `max(30, 300 − 120) = 180`. The floor (30) is below the subtractive result, so the boss hit is unchanged. The floor would start to bite only when `p × 300 > 180`, that is `p > 0.6`.

A flat floor of 1 does not work. Ten rats would deal only 10.
</details>

9. *Week 2 · critique.* A design document says: "We use subtractive armor so tanks feel strong. By the late game player armor reaches 400. Trash mobs in the final zone hit for 80 to 150." Critique this and propose two fixes with numbers.

<details>
<summary>Answer and worked solution</summary>

**Answer:** every final-zone trash hit deals 0, so the trash is harmless and the zone's content is retired on arrival.

With `A = 400` and `D ≤ 150`, `max(0, D − A) = 0` for every trash hit. Only enemies hitting above 400 matter, so either trash damage must inflate past player armor (and keep inflating as armor grows) or trash stops being a threat.

Fix 1: keep subtractive and add a percentage floor. With a 20% floor the 150-damage hit deals 30 and the 80-damage hit deals 16.

Fix 2: switch to divisive armor. With `K = 400`, 400 armor lets half of every hit through, so the trash deals 40 to 75 per hit and the tank still halves boss damage. The cost is the threshold fantasy: a divisive tank is never immune.
</details>

## Week 3: Mitigation curves and effective HP

10. *Week 3 · compute.* A game uses divisive armor with `K = 60`. A character has 1,500 HP and 90 armor. Compute mitigation, effective HP, the EHP added by one more armor point, and the number of 300-damage hits the character survives before dying.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 60% mitigation, 3,750 EHP, 25 EHP per armor point, dies on the 13th hit.

`f = 60 / (90 + 60) = 0.4`, so mitigation is 60%. `EHP = 1,500 / 0.4 = 3,750`. The slope of `EHP = HP × (1 + A/K)` is `HP / K = 1,500 / 60 = 25` per point, the same at every armor value.

Hits to die: `3,750 / 300 = 12.5`, so the 13th hit kills.
</details>

11. *Week 3 · compute.* A game uses linear percent resistance with a 75% cap. By what factor does effective HP against that element grow when resistance goes from 30% to 50%? From 55% to 75%? What does the comparison tell you about the returns of linear percent?

<details>
<summary>Answer and worked solution</summary>

**Answer:** ×1.40 for 30% to 50%, and ×1.80 for 55% to 75%. Linear percent has increasing returns in EHP.

The EHP multiplier is `1 / (1 − resistance)`. At 30% it is 1.43, at 50% it is 2.00, so the factor is 1.40 (2.00 / 1.43). At 55% it is 2.22 and at 75% it is 4.00, a factor of 1.80.

The same 20 points are worth more the higher you already are. That is why a cap is required and why players rush to it.
</details>

12. *Week 3 · compute.* A character has 2,000 HP, 150 armor and 30 magic resistance, both divisive with `K = 100`. The fight is 50% physical and 50% magical. They can add 100 armor or 100 magic resistance. Compute current EHP and EHP under each option.

<details>
<summary>Answer and worked solution</summary>

**Answer:** current EHP about 3,421. With 100 more armor, about 3,792. With 100 more magic resistance, about 4,792. Take the magic resistance.

`f_phys = 100/250 = 0.400`, `f_mag = 100/130 = 0.769`. `f_total = 0.5 × 0.400 + 0.5 × 0.769 = 0.585`, EHP `= 2,000 / 0.585 ≈ 3,421`.

+100 armor: `f_phys = 100/350 = 0.286`, `f_total = 0.527`, EHP ≈ 3,792.

+100 magic resistance: `f_mag = 100/230 = 0.435`, `f_total = 0.417`, EHP ≈ 4,792.

The weaker defense dominates the weighted average, so raising it pays more.
</details>

13. *Week 3 · compute.* A character starts with 800 HP and 0 armor, `K = 100`, and has 60 budget points. One point buys 40 HP or 4 armor. Find the split that maximizes EHP, the EHP at that split, and check it with the equal-margin rule `HP / h = (A + K) / a`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 32 or 33 points into health (a tie), EHP 4,409.6.

With `x` points into health, `HP = 800 + 40x` and `A = 4(60 − x)`. `EHP = (800 + 40x)(1 + A/100)`.

| x | HP | Armor | EHP |
|---|---|---|---|
| 0 | 800 | 240 | 2,720 |
| 20 | 1,600 | 160 | 4,160 |
| 32 | 2,080 | 112 | 4,409.6 |
| 33 | 2,120 | 108 | 4,409.6 |
| 60 | 3,200 | 0 | 3,200 |

Rule check at `x = 32`: `HP / h = 2,080 / 40 = 52` and `(A + K) / a = 212 / 4 = 53`. At `x = 33` the two sides are 53 and 52. The optimum sits between them, which is why the two whole-number splits tie.
</details>

14. *Week 3 · explain.* Character P has 25% dodge and 50 armor. Character Q has 0% dodge and 100 armor. Both use `K = 100` and have the same HP. Show that their EHP is equal, then explain why a designer would still treat them differently in a three-hit PvP exchange.

<details>
<summary>Answer and worked solution</summary>

**Answer:** both let 50% of raw damage through on average, so both have EHP = 2 × HP. P's damage taken is far more variable.

P: `f = 0.75 × 100/150 = 0.5`. Q: `f = 100/200 = 0.5`.

In three hits, Q takes exactly half of each. P takes nothing from a dodged hit and two thirds of a hit that lands. All three land with probability `0.75³ ≈ 42%`, and then P takes `3 × 2/3 = 2` hits' worth against Q's 1.5, a third more. EHP describes the long-run average, and a three-hit exchange is decided by variance, which week 6 measures.
</details>

## Week 4: Time-to-kill and time-to-die

15. *Week 4 · compute.* A weapon deals 17 damage every 0.7 seconds against a 120-health target with no mitigation. Compute hits-to-kill, TTK and the smooth estimate. What is the smallest whole-number damage that removes one hit, and what is the TTK then?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 8 hits, TTK 4.9 s, smooth estimate 4.94 s. 18 damage removes a hit, giving 7 hits and 4.2 s.

`120 / 17 = 7.06`, rounded up to 8. `TTK = (8 − 1) × 0.7 = 4.9` s. Smooth: `120 × 0.7 / 17 = 4.94` s.

For 7 hits, `d ≥ 120 / 7 = 17.14`, so 18. `TTK = 6 × 0.7 = 4.2` s. A 5.9% damage increase cuts TTK by 14%.
</details>

16. *Week 4 · design.* The player's weapon deals 15 damage every 0.6 seconds. You want a trash mob to die in exactly 3.0 seconds. Give the range of health values that does this, pick the value that gives the most balanced damage margin, and state the margin in both directions. What would the naive formula `H = DPS × TTK` have given, and what TTK would it produce?

<details>
<summary>Answer and worked solution</summary>

**Answer:** health from 76 to 90 gives 6 hits and 3.0 s. Health 82 is the most balanced: player damage can fall 8.9% or rise 9.3% before the hit count changes. The naive value is 75, which dies in 5 hits and 2.4 s.

Hits: `3.0 / 0.6 + 1 = 6`. Six hits means `5 × 15 < H ≤ 6 × 15`, so `75 < H ≤ 90`.

At `H = 82` the mob stays at 6 hits while `82/6 ≤ d < 82/5`, that is `13.67 ≤ d < 16.4`. Relative to 15: −8.9% and +9.3%. (At 83 the margins are −7.8% and +10.7%.)

Naive: DPS is 25, so `H = 75`. That is exactly 5 hits, `TTK = 4 × 0.6 = 2.4` s, and it sits on the edge of a step.
</details>

17. *Week 4 · compute.* A player has 300 health and 20% mitigation. An enemy hits for 40 every 1.5 seconds. The player's weapon deals 25 every 1.0 second, and the enemy has 110 health and no mitigation. Compute the player's TTD, TTK and safety ratio `R`, then the same ratio from smooth estimates.

<details>
<summary>Answer and worked solution</summary>

**Answer:** TTD 13.5 s, TTK 4.0 s, `R = 3.375`. The smooth estimate gives about 3.2.

Enemy damage after mitigation: `40 × 0.8 = 32`. Hits to kill the player: `ceil(300 / 32) = 10`, so `TTD = 9 × 1.5 = 13.5` s.

Player: `ceil(110 / 25) = 5` hits, `TTK = 4 × 1.0 = 4.0` s. `R = 13.5 / 4.0 = 3.375`.

Smooth: `TTD ≈ 300 × 1.5 / 32 = 14.06`, `TTK ≈ 110 / 25 = 4.4`, ratio 3.2. The staircase favors the player slightly here.
</details>

18. *Week 4 · compute.* A weapon deals 20 per hit. A patch gives +8% damage. Three enemies have 60, 85 and 105 health. For each, give hits-to-kill before and after, and explain in one sentence why the answers differ.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 60 health stays at 3 hits. 85 health drops from 5 to 4. 105 health drops from 6 to 5.

After the patch `d = 21.6`. `60/20 = 3` and `60/21.6 = 2.78`, both 3 hits. `85/20 = 4.25` (5 hits) and `85/21.6 = 3.94` (4 hits). `105/20 = 5.25` (6 hits) and `105/21.6 = 4.86` (5 hits).

The 60-health enemy sat exactly on a breakpoint with no overkill to trim, so the buff only adds waste. The other two were just past a breakpoint, so a small buff crosses it.
</details>

19. *Week 4 · explain.* (a) Two duelists each need 3 hits to kill the other and both swing every 1.0 second. Who wins, and what does a smooth DPS comparison predict? (b) A raid boss has 6,000,000 health and an 8-minute enrage. What raid DPS does that require, and why can you ignore breakpoints here but not in (a)?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) whoever swings first wins every time. Smooth DPS predicts a tie. (b) 12,500 DPS. The boss takes so many hits that rounding up adds at most one hit in many thousands.

(a) The first swinger lands hits at 0, 1 and 2 s, the second at 1 and 2 s only before losing. The first strike is worth a full interval.

(b) `6,000,000 / 480 = 12,500` DPS, or 13,750 with a 10% safety margin. The relative error of ignoring the staircase is at most `1 / hits`, which is negligible for a fight measured in tens of thousands of hits and up to a third for a 3-hit duel.
</details>

## Week 5: DPS, burst and sustain

20. *Week 5 · compute.* A launcher deals 50 per shot, holds 6 shots, fires every 0.5 s and reloads in 3.0 s. A beam deals 12 every 0.2 s and never pauses. First hits land at `t = 0`. Compute alpha, burst DPS, clip damage and sustained DPS for both, then the TTK of each against targets with 250, 300, 350 and 1,000 health.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Weapon | Alpha | Burst DPS | Clip | Sustained DPS |
|---|---|---|---|---|
| Launcher | 50 | 100 | 300 | 50 |
| Beam | 12 | 60 | — | 60 |

| Target health | Launcher TTK (s) | Beam TTK (s) | Faster |
|---|---|---|---|
| 250 | 2.0 | 4.0 | Launcher |
| 300 | 2.5 | 4.8 | Launcher |
| 350 | 6.0 | 5.8 | Beam |
| 1,000 | 18.5 | 16.6 | Beam |

Launcher cycle: `6 × 0.5 + 3.0 = 6.0` s for 300 damage, so 50 sustained. Its sixth shot lands at 2.5 s. A 350-health target survives the clip, so the seventh shot waits for the reload and lands at 6.0 s. That is the clip breakpoint: 17% more target health more than doubles the TTK.

Beam against 350: `ceil(350/12) = 30` hits, the 30th at `29 × 0.2 = 5.8` s. Against 1,000: 84 hits, `83 × 0.2 = 16.6` s. Launcher against 1,000: 20 shots, three full clips by 14.5 s (900 damage), then shots at 18.0 and 18.5 s.
</details>

21. *Week 5 · compute.* A boss has 80,000 health and heals 500 per second. The raid deals 1,300 DPS. Compute the TTK. You can either add 200 raid DPS or apply a debuff that halves the boss's healing. Which saves more time?

<details>
<summary>Answer and worked solution</summary>

**Answer:** base TTK 100 s. +200 DPS gives 80 s. Halving healing gives about 76.2 s, so the debuff wins.

Base: net rate `1,300 − 500 = 800`, `TTK = 80,000 / 800 = 100` s.

+200 DPS: net 1,000, TTK 80 s.

Healing halved to 250: net 1,050, TTK ≈ 76.2 s.

Removing 250 healing beats adding 200 damage because it removes more from the net rate. The closer healing is to damage, the more each point of healing reduction is worth, because TTK is a hyperbola in the net rate.
</details>

22. *Week 5 · compute.* A melee class has 200 paper DPS. In a boss fight it attacks 80% of the time, 90% of its attacks connect, the boss has 30% mitigation, and 5% of damage is overkill. What is its effective DPS? Which one term would you change first to close a gap with a ranged class that has 95% uptime and everything else equal?

<details>
<summary>Answer and worked solution</summary>

**Answer:** about 95.8 effective DPS. Uptime is the term to look at first.

`200 × 0.8 × 0.9 × 0.7 × 0.95 = 95.76`.

The ranged class at 95% uptime gets `200 × 0.95 × 0.9 × 0.7 × 0.95 = 113.7`, 19% more. The difference comes entirely from uptime, which encounter design controls (movement demands), so an encounter change or a gap-closer for the melee class addresses the cause directly.
</details>

23. *Week 5 · critique.* A game's item tooltip shows a single "DPS" number, computed as burst DPS. A heavy crossbow shows 120 DPS and a repeating bow shows 70. Players in long raid fights say the crossbow is a trap. Explain what the tooltip hides and propose a tooltip change.

<details>
<summary>Answer and worked solution</summary>

**Answer:** the tooltip hides clip damage and reload, so it shows burst, not sustained, DPS. In long fights sustained DPS decides.

If the crossbow fires, say, 2 bolts before a long reload, its sustained rate can fall well below 70 even though its burst is 120. The repeating bow never pauses, so its 70 is also its sustained rate. The tooltip answers "how fast while firing" when raid players need "how much over a minute."

Show two numbers, burst and sustained, or show damage over a stated fight length ("over 30 s: 1,650"). Name the fight length the number assumes.
</details>

## Week 6: Critical hits and variance

24. *Week 6 · compute.* A weapon has 50 base damage, 15% crit chance and a 3× multiplier. Compute expected damage per hit, the standard deviation, the per-hit CV, and the CV of total damage over a 16-hit fight.

<details>
<summary>Answer and worked solution</summary>

**Answer:** expected damage 65, standard deviation about 35.7, per-hit CV about 0.55, 16-hit CV about 0.14.

`E = 50 × (1 + 0.15 × 2) = 65`. `σ = 50 × 2 × sqrt(0.15 × 0.85) = 100 × 0.357 = 35.7`. `CV = 35.7 / 65 = 0.549`.

Over 16 hits: `0.549 / sqrt(16) = 0.137`.
</details>

25. *Week 6 · compute.* Build A deals 40 per hit with no crits. Build B has 20% crit chance at 2× and the same average damage. Give B's hits-to-kill distribution and mean against a 100-health target and a 120-health target, and say whether B is faster or slower than A in each case.

<details>
<summary>Answer and worked solution</summary>

**Answer:** against 100 health, B kills in 2 hits 36% of the time and 3 hits 64%, mean 2.64, faster than A's 3. Against 120 health, B needs 2 hits 4%, 3 hits 44.8%, 4 hits 51.2%, mean 3.47, slower than A's 3.

B's base damage is `40 / 1.2 = 33.33`, and each crit adds another 33.33. B kills within `n` hits when `n + k ≥ H / 33.33`.

100 health: need `n + k ≥ 3`. Two hits need at least one crit: `1 − 0.8² = 0.36`. Three hits always kill. Mean `2 × 0.36 + 3 × 0.64 = 2.64`.

120 health: need `n + k ≥ 3.6`, so 4. Two hits need two crits: `0.04`. Three hits need at least one crit in three: `1 − 0.8³ = 0.488`, so exactly 3 is 0.448. Four hits always kill: 0.512. Mean `0.08 + 1.344 + 2.048 = 3.47`.

A wastes 20 damage against 100 health (just past a breakpoint), so B's variance helps. A sits exactly on its breakpoint at 120, so variance can only hurt.
</details>

26. *Week 6 · compute.* A build has 40% crit chance and a 1.6× crit multiplier. Which adds more expected damage, +4 points of crit chance or +8 points of crit multiplier? For this multiplier, at what crit chance are the two items worth the same?

<details>
<summary>Answer and worked solution</summary>

**Answer:** +8 points of crit multiplier (+0.032 against +0.024). They are equal at 30% crit chance.

Gain from chance: `Δc × (m − 1) = 0.04 × 0.6 = 0.024`. Gain from multiplier: `Δm × c = 0.08 × 0.40 = 0.032`. On the expected multiplier of 1.24 those are +1.9% and +2.6%.

Equal when `0.04 × 0.6 = 0.08 × c`, so `c = 0.30`.
</details>

27. *Week 6 · design.* Your PvP exchanges last about 3 hits, and your raid fights about 100 hits. The design goal is "crits add 10% to average damage, and the CV of a 3-hit exchange is between 0.10 and 0.20." A colleague proposes either (c = 5%, m = 3) or (c = 30%, m = 1.33). Test both, and if neither works, propose a (c, m) that does. What does your choice do in the raid?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (5%, 3) gives a 3-hit CV of 0.23, too swingy. (30%, 1.33) gives 0.08, too flat. Read 1.33 as 4/3, so that its expected multiplier is exactly 1.10. (10%, 2) gives 0.16 and meets the goal. In a 100-hit raid its CV is 0.027, almost no variance.

All three have expected multiplier `1 + c(m − 1) = 1.10`.

Per-hit CV is `(m − 1) × sqrt(c(1 − c)) / 1.10`, and the 3-hit CV divides it by `sqrt(3)`.

| (c, m) | Per-hit CV | 3-hit CV | 100-hit CV |
|---|---|---|---|
| 0.05, 3 | 0.396 | 0.229 | 0.040 |
| 0.30, 1.33 | 0.139 | 0.080 | 0.014 |
| 0.10, 2 | 0.273 | 0.157 | 0.027 |

The goal needs per-hit CV between `0.10 × sqrt(3) = 0.173` and `0.20 × sqrt(3) = 0.346`. (20%, 1.5) also qualifies, with a per-hit CV of 0.182 and a 3-hit CV of 0.105, near the low edge. The raid result shows crits cannot add tension to long fights.
</details>

## Week 7: XP curves

28. *Week 7 · compute.* A game uses exponential per-level XP costs with `r = 1.10` and a cap of 60. Estimate the halfway level, and say how many level-ups hold the second half of all XP. What happens to the halfway level if the cap is raised to 80?

<details>
<summary>Answer and worked solution</summary>

**Answer:** level 53. The last 8 level-ups (to levels 53 through 60) hold half the XP. With a cap of 80 the halfway level is 73, still about 7.3 levels from the end.

`log 2 / log 1.10 = 7.27`, so `n½ ≈ 60 − 7.27 = 52.7`, which rounds up to 53. Summing the table exactly also gives 53.

For a cap of 80, `80 − 7.27 = 72.7`, so level 73. Raising the cap lengthens the early game and leaves the prestige stretch the same size.
</details>

29. *Week 7 · compute.* An XP table reads `T(2) = 300`, `T(3) = 900`, `T(4) = 1,800`, `T(5) = 3,000`. Identify the family and its parameter, write `T(n)`, and find `T(30)` and the halfway level for a cap of 30. Which shipped table from the lecture has the same shape?

<details>
<summary>Answer and worked solution</summary>

**Answer:** linear cost (quadratic total) with `a = 300`. `T(n) = 150 × n × (n − 1)`, `T(30) = 130,500`, halfway level 22. D&D 3.5 has the same shape with `a = 1,000`.

Per-level costs are 300, 600, 900, 1,200. The difference is a constant 300, so costs are linear and `T(n) = 300 × n(n − 1)/2`.

`T(30) = 150 × 30 × 29 = 130,500`. Half is 65,250. `T(21) = 63,000` falls short and `T(22) = 69,300` passes it.
</details>

30. *Week 7 · compute.* Design a 20-hour, 25-level campaign backwards. Time per level grows by `g = 1.10`, XP income starts at `I₂ = 800` per hour and grows by `q = 1.15` per level. Compute `t₂`, `c(10)`, `T(25)`, the time halfway level and the XP halfway level.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `t₂ ≈ 13.6` min, `c(10) ≈ 1,186` XP, `T(25) ≈ 191,679` XP, time halfway at level 19, XP halfway at level 23.

`(1.10^24 − 1) / 0.10 = 88.50`, so `t₂ = 1,200 / 88.50 = 13.56` minutes.

Level 10: `t = 13.56 × 1.10^8 = 29.07` min, `I = 800 × 1.15^8 = 2,447` XP/h, `c = 29.07 / 60 × 2,447 = 1,186`.

Summing `c(n)` for `n = 2 … 25` gives about 191,679 (the sum is 191,678.5 before rounding). Cumulative time first reaches 600 minutes at level 19. Cumulative XP first reaches half of `T(25)` at level 23.

The two halfway levels differ because XP per level grows by `1.10 × 1.15 = 1.265` while time grows by only 1.10.
</details>

31. *Week 7 · critique.* A game's per-level XP cost grows 14% per level and its XP income grows 10% per level. (a) By how much does time per level grow, and how much longer is a level 15 levels later? (b) A designer then doubles the XP from bosses in levels 15 to 17, where bosses are half of all XP income. Critique the change.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) about 3.6% per level, and 1.71 times longer after 15 levels. (b) income in those levels rises by 50%, so those levels take a third less time and players out-level the next zone.

(a) `1.14 / 1.10 = 1.036`. `1.036^15 ≈ 1.71`.

(b) If bosses are half of income, doubling them multiplies income by `0.5 + 0.5 × 2 = 1.5`, so `t(n)` falls to two thirds. The XP table did not change, yet pacing broke. Players arrive at the next zone above its level and skip content. Reward the boss with something other than XP, or rebalance the table for those levels.
</details>

## Week 8: Power curves and level scaling

32. *Week 8 · compute.* Attack and health each grow 6% per level. How much does power grow per level? How much more powerful is a character 8 levels higher? How many levels double power?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 12.36% per level, 2.54 times for 8 levels, about 5.95 levels to double.

Power grows by `1.06² = 1.1236` per level. Eight levels: `1.1236^8 = 2.54`. Doubling: `log 2 / log 1.1236 = 5.95`.
</details>

33. *Week 8 · compute.* A game uses `a(L) = 15 + 3L` and `h(L) = 150 + 30L`. What is the power ratio of level 10 over level 5, and of level 45 over level 40? What kind of power curve is this?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 2.25 early and about 1.23 late. It is a linear power curve, so a fixed gap shrinks in importance as the game goes on.

Both stats are proportional to `5 + L`, so power is proportional to `(5 + L)²`. Level 10 over 5: `(15/10)² = 2.25`. Level 45 over 40: `(50/45)² = 1.235`.
</details>

34. *Week 8 · compute.* Power grows 21% per level. (a) A zone is band-scaled with `L_e = clamp(L_p, 12, 20)`. What is `R` for players at levels 8, 16 and 26? (b) A downscaling system sets the player to the zone's maximum level plus one and keeps gear worth 1.25 times power. A level 50 player enters a level 1 to 30 zone and fights a level 27 enemy. What is `R`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 0.47, 1.00 and 3.14. (b) about 2.68.

(a) Level 8: enemies clamp to 12, `R = 1.21^(−4) = 0.47`. Level 16: inside the band, `R = 1`. Level 26: enemies clamp to 20, `R = 1.21^6 = 3.14`.

(b) Effective level 31, four above the enemy. `R = 1.21^4 × 1.25 = 2.14 × 1.25 = 2.68`.
</details>

35. *Week 8 · explain.* A game uses full level scaling. Each level-up multiplies the player's power by 1.15, and each enemy's power by 1.20 because enemies also scale their gear. What happens to `R` over 10 levels, and why do players say "leveling makes the game harder"? Name one fix.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `R` falls to about 0.65 of its starting value after 10 levels. The player's growth is real, but the enemy's is faster, so each level-up lowers the safety ratio.

`R` changes by `1.15 / 1.20 = 0.958` per level, and `0.958^10 = 0.65`.

Fixes: make the enemy's per-level gain no larger than the player's, give the player power sources the enemy does not copy (abilities, gear the scaling ignores), or use partial scaling (week 13's `α` below 1).
</details>

## Week 9: Item budgets and stat weights

36. *Week 9 · compute.* Use the lecture's price list (Str 1.0, Sta 0.5, Crit 0.8, Haste 0.8) and weights (build X: 1.0, 0, 1.1, 0.5; build Y: 1.0, 0, 0.5, 1.1; build T: 0.5, 1.0, 0.3, 0.3, in the order Str, Sta, Crit, Haste). An item level 55 belt has 45 Str, 40 Sta, 30 Crit and 35 Haste, and the budget is 110 with a ±5% tolerance. Is it on budget? Which build values it most? Propose the smallest edit that brings it on budget without changing which build wants it.

<details>
<summary>Answer and worked solution</summary>

**Answer:** it costs 117, which is 106.4% of budget and outside tolerance. Build Y values it most (98.5). Cutting 14 Stamina brings it to exactly 110.

Cost: `45 + 40 × 0.5 + 30 × 0.8 + 35 × 0.8 = 45 + 20 + 24 + 28 = 117`. `117 / 110 = 1.064`.

Values: X `45 + 33 + 17.5 = 95.5`. Y `45 + 15 + 38.5 = 98.5`. T `22.5 + 40 + 9 + 10.5 = 82`.

Stamina matters only to build T, so removing 14 Stamina (7 points) lowers the cost to 110 and leaves Y's value unchanged at 98.5. Removing just 3 Stamina reaches 115.5, the edge of tolerance.
</details>

37. *Week 9 · compute.* You add a new stat, Versatility. Its weights are 0.9 for build X, 0.7 for build Y and 0.6 for build T. Strength weights are 1.0, 1.0 and 0.5. Players are 50% X, 30% Y and 20% T. What should Versatility cost per point, normalized so Strength costs 1?

<details>
<summary>Answer and worked solution</summary>

**Answer:** about 0.87 points per Versatility.

Average Versatility weight: `0.5 × 0.9 + 0.3 × 0.7 + 0.2 × 0.6 = 0.78`. Average Strength weight: `0.5 + 0.3 + 0.1 = 0.9`. Price `0.78 / 0.9 = 0.867`.
</details>

38. *Week 9 · compute.* A ring has "8% chance on hit to deal 300 damage." The reference build hits 1.6 times per second, and one point of Strength gives it 0.6 DPS. How many budget points is the proc worth?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 64 points.

Expected proc DPS: `0.08 × 300 × 1.6 = 38.4`. In Strength terms: `38.4 / 0.6 = 64` Strength, so 64 points at a Strength price of 1.
</details>

39. *Week 9 · compute.* A build's DPS is `50 × (1 + Str/100) × (1 + Crit/300)`. Compute stat weights by adding 10 of each stat at two gear sets, (Str 150, Crit 90) and (Str 150, Crit 240). Normalize Crit to Strength at each. Explain the change.

<details>
<summary>Answer and worked solution</summary>

**Answer:** at (150, 90), Str 0.65 and Crit 0.417, so Crit is worth 0.64 Str. At (150, 240), Str 0.90 and Crit 0.417, so Crit is worth 0.46 Str.

First set: baseline `50 × 2.5 × 1.3 = 162.5`. +10 Str gives `50 × 2.6 × 1.3 = 169.0`, weight 0.65. +10 Crit gives `50 × 2.5 × 1.3333 = 166.67`, weight 0.417.

Second set: baseline `50 × 2.5 × 1.8 = 225`. +10 Str gives 234, weight 0.90. +10 Crit gives 229.17, weight 0.417.

The two factors multiply. Strength's weight is proportional to the crit factor, so stacking Crit raises Strength's weight while Crit's own weight stays put. Relative to Strength, the stat you already have most of becomes the cheapest. A weight is a slope at one gear set.
</details>

40. *Week 9 · critique.* Using the lecture's Hearthstone budget line `cost = (Attack + Health − 1) / 2`, a designer proposes an 8/1 minion at 4 mana and argues it is "exactly on curve." Critique the argument.

<details>
<summary>Answer and worked solution</summary>

**Answer:** the formula does give `(8 + 1 − 1) / 2 = 4`, but a linear price list cannot see that attack is worth little on a body that dies to anything. Like Magma Rager, the card is likely weaker than its cost.

The value of attack depends on health (a synergy between stats), which a sum of prices ignores. Fixes are a nonlinear price that charges less for extreme splits, or a rule that prices attack by the turns the minion is expected to survive.
</details>

## Week 10: Enemy design by the numbers

41. *Week 10 · compute.* A player deals 30 DPS. An enemy has 180 health and 5 DPS. What does one enemy cost the player in health? What does a pack of five cost under focus fire? Under AoE at `a = 0.5`? What AoE fraction breaks even with focus fire for this pack?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 30 for one, 450 for the pack under focus fire, 300 under half-strength AoE. AoE breaks even at `a = 1/3`.

`c = d × h / P = 5 × 180 / 30 = 30`. Pack: `c × n(n + 1)/2 = 30 × 15 = 450`. AoE: `n × c / a = 5 × 30 / 0.5 = 300`. Break-even: `a = 2 / (n + 1) = 2/6`.
</details>

42. *Week 10 · compute.* A player with 25 DPS and 250 health faces a Mage (50 health, 10 DPS), a Hound (40 health, 6 DPS) and a Knight (150 health, 9 DPS). Find the best and worst kill orders and their costs as a share of the player's health.

<details>
<summary>Answer and worked solution</summary>

**Answer:** best is Mage, Hound, Knight at 128 (51%). Worst is Knight, Hound, Mage at 195.6 (78%).

Priority ratios `d/h`: Mage 0.20, Hound 0.15, Knight 0.06.

Best: deaths at 2.0, 3.6 and 9.6 s. Cost `10 × 2.0 + 6 × 3.6 + 9 × 9.6 = 20 + 21.6 + 86.4 = 128`.

Worst: deaths at 6.0, 7.6 and 9.6 s. Cost `9 × 6.0 + 6 × 7.6 + 10 × 9.6 = 54 + 45.6 + 96 = 195.6`.

The fight lasts 9.6 s in every order. Kill order only changes who is alive during it.
</details>

43. *Week 10 · compute.* The player has `P = 60` and `H = 900` at a level. Build an elite with a 20-second TTK, a 30% cost share and a 3-second attack interval. Then an affix gives the elite ×1.4 health and ×1.3 damage. What is its new cost share, and what happens if two such affixes stack?

<details>
<summary>Answer and worked solution</summary>

**Answer:** health 1,200, 13.5 DPS, 40.5 per hit (4.5% of player health). One affix multiplies cost by 1.82, to about 55%. Two stacked multiply it by 3.31, to about 99%.

`h = 60 × 20 = 1,200`. `d = 0.3 × 900 / 20 = 13.5`. Per hit `13.5 × 3 = 40.5`.

Cost is proportional to `h × d`, so the affix multiplies it by `1.4 × 1.3 = 1.82`, giving `0.30 × 1.82 = 0.546`. Two affixes: `1.82² = 3.31`, giving 0.99. Two "moderate" affixes turn a 30% elite into one that nearly kills the player.
</details>

44. *Week 10 · design.* A dungeon room has three enemy types, all with a priority ratio of 0.15. Explain why that is a design problem, then redesign the three so that the best kill order saves at least 20% of player health compared with the worst, against a player with `P = 20` and `H = 200`, one of each enemy. Show the costs.

<details>
<summary>Answer and worked solution</summary>

**Answer:** with equal ratios every kill order costs the same, so target selection is not a decision. One redesign that meets the goal is Archer (20 health, 6 DPS), Shaman (40, 8), Brute (120, 12), as in the lecture, with best cost 138 and worst 190, a gap of 52 health (26% of 200).

With equal `d/h`, swapping any two neighbours in the order leaves the cost unchanged, so all orders tie.

Redesign check: ratios 0.30, 0.20 and 0.10. Best order Archer, Shaman, Brute dies at 1, 3 and 9 s, cost `6 + 24 + 108 = 138`. Worst order Brute, Shaman, Archer dies at 6, 8 and 9 s, cost `72 + 64 + 54 = 190`. Other designs pass if their computed gap is at least 40 health. Make the high-ratio enemy readable at a glance.
</details>

## Week 11: Spreadsheet balancing workshop

45. *Week 11 · compute.* In a game, player damage grows like `L^1.2` and enemy health like `L^1.8`. Hits-to-kill is 4 at level 5. Estimate hits-to-kill at level 40, and say which way the game drifts.

<details>
<summary>Answer and worked solution</summary>

**Answer:** about 14 hits. Fights get longer as the player levels.

`hits ∝ L^(1.8 − 1.2) = L^0.6`. Level 40 is 8 times level 5, so hits scale by `8^0.6 = 3.48`. `4 × 3.48 = 13.9`.
</details>

46. *Week 11 · compute.* A student's sheet uses `W(L) = 8 + 3L` for weapon damage and `S(L) = 8 + 3L` for Strength, `damage = W × S / 20`, and enemy health `40 + 12L`. (a) Compute damage per hit and hits-to-kill (unrounded) at levels 1, 10 and 25. (b) Fix it by dividing by `Def(L) = 8 + 3L` instead of 20. Why is the result nearly flat but not exactly flat, and what one change makes it exactly flat?

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Level | Damage (multiplied) | Enemy health | Hits (multiplied) | Hits (ratio fix) |
|---|---|---|---|---|
| 1 | 6.05 | 52 | 8.60 | 4.73 |
| 10 | 72.2 | 160 | 2.22 | 4.21 |
| 25 | 344.45 | 340 | 0.99 | 4.10 |

(a) Damage grows like `L²` and health like `L`, so hits fall until every enemy dies in one hit by level 25.

(b) With the ratio, damage equals `W`, and hits are `(40 + 12L) / (8 + 3L)`. The level terms have ratio `12/3 = 4` and the constants have ratio `40/8 = 5`, so hits drift from 5 toward 4 as the constants stop mattering. Setting enemy health to `32 + 12L` makes both ratios 4 and hits exactly 4 at every level.
</details>

47. *Week 11 · explain.* A sensitivity table shows that a 10% change in soldier TTK moves room D's cost by 7 percentage points, and a 10% change in player health growth moves it by 1 point. The budget is 70% and room D currently costs 66%. What does this tell you about the next patch, and what would a single scenario test have missed?

<details>
<summary>Answer and worked solution</summary>

**Answer:** room D is fragile with respect to soldier TTK. A 10% increase in soldier TTK would push it to about 73%, over budget. Player health growth can be tuned freely.

A scenario test reports one outcome at the current inputs (66%, inside budget) and looks safe. The sensitivity table shows which input the result depends on and how steeply. Any patch touching soldier TTK needs the full room table rechecked. Record that dependency in the sheet's notes.
</details>

48. *Week 11 · critique.* A teammate's level table is correct at level 1, off by a little at level 2 and more at each level after. A second teammate typed 145 over a formula in the level 18 row to "fix" a spike. Diagnose both problems and give the fix for each.

<details>
<summary>Answer and worked solution</summary>

**Answer:** the first is a missing absolute reference (the dollar sign), and the second is a hardcoded patch.

A formula that should point at a fixed input cell uses a relative reference, so filling it down shifts the reference one row per row. Make it absolute (`$B$4`) or, better, use a named input.

The typed 145 does not follow any input change, so the next time growth rates change, level 18 silently disagrees with the rest. If level 18 needs a special case, make it an input with a label and a reason, and let the formula read it.
</details>

## Week 12: Simulation-driven balance

49. *Week 12 · compute.* A sword deals 12 damage with a 30% chance to crit for double. The enemy has 60 health. Give the exact hits-to-kill distribution and mean, and say what a spreadsheet using average damage would report.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 3 hits 21.6%, 4 hits 54.4%, 5 hits 24.0%, mean 4.02. The spreadsheet reports `60 / 15.6 = 3.85`, rounded up to 4, every time.

Damage after `n` hits with `k` crits is `12(n + k)`, so a kill needs `n + k ≥ 5`.

Three hits need at least 2 crits: `3 × 0.3² × 0.7 + 0.3³ = 0.216`. Four hits need at least 1 crit: `1 − 0.7⁴ = 0.760`, so exactly 4 is 0.544. Five hits always kill: 0.240. Mean `3 × 0.216 + 4 × 0.544 + 5 × 0.240 = 4.02`.
</details>

50. *Week 12 · compute.* (a) A simulator reports a 56% win rate from 1,600 fights. Give the 95% interval and say whether the matchup is favored. (b) How many fights do you need for a ±1 point interval on a win rate near 70%?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 56% ± 2.4, from 53.6% to 58.4%. The whole interval is above 50%, so the matchup is favored. (b) about 8,070 fights.

(a) `SE = sqrt(0.56 × 0.44 / 1,600) = 0.0124`. `1.96 × 0.0124 = 0.0243`.

(b) `1.96 × sqrt(0.7 × 0.3 / N) = 0.01` gives `N = 1.96² × 0.21 / 0.0001 = 8,067.4`, so at least 8,068.
</details>

51. *Week 12 · compute.* Two fighters have 60 health each and alternate swings. A hits a steady 12. B deals 30 with probability 1/3 and 0 otherwise, an average of 10. Compute B's win rate when A swings first and when B swings first. What would B's win rate be with a steady 10?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 40.7% with A first, 53.9% with B first. With a steady 10, B needs 6 swings to A's 5 and wins 0% in both orders.

A needs 5 swings. B needs 2 heavy hits.

A first: B gets 4 swings before A's fifth. `P(at least 2 of 4) = 1 − (2/3)⁴ − 4 × (1/3) × (2/3)³ = 1 − 16/81 − 32/81 = 33/81 = 40.7%`.

B first: B gets 5 swings. `P(at least 2 of 5) = 1 − 32/243 − 80/243 = 131/243 = 53.9%`.

A 200,000-fight simulation with a fixed seed gives 40.7% and 54.0%, inside the expected error. Variance turned a certain loss into a coin flip for the underdog.
</details>

52. *Week 12 · compute.* A shotgun fires 4 pellets, each dealing 5 × (1d6), so 5 to 30 each and 70 on average. An enemy has 60 health. What is the chance one blast kills? Compare it with a single slug dealing a whole number from 20 to 120 with equal odds, also averaging 70.

<details>
<summary>Answer and worked solution</summary>

**Answer:** the shotgun kills 76.1% of the time. The slug kills 60.4% of the time.

The shotgun kills when the four dice sum to at least 12. Counting all `6⁴ = 1,296` outcomes, 986 qualify: `986 / 1,296 = 0.761`.

The slug kills on 61 of its 101 values (60 through 120): 0.604.

Many small random pieces make a tighter distribution than one large one, so the same average is more reliable.
</details>

53. *Week 12 · explain.* You have written a duel simulator. Describe two checks you run before trusting any result from it, and explain what "a random-number generator with opinions" means.

<details>
<summary>Answer and worked solution</summary>

**Answer:** turn randomness off and confirm the simulator matches the spreadsheet exactly, then compare one random case with an exact result (for example the lecture's 68.4% hero-first duel) and check the exact value falls inside the reported interval.

A simulator that has never been validated still prints precise-looking numbers, but nothing ties them to the rules you meant to model. Precision (many fights) is not correctness. Record the seed so any strange fight can be replayed.
</details>

## Week 13: Difficulty modes and scaling

54. *Week 13 · compute.* A base fight has `R₀ = 3` and a 10-second TTK. Hard mode sets `p = 0.8`, `e = 1.5`, `h = 1.25`. Compute the new safety ratio, health cost per fight and fight length.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `R = 1.28`, health cost about 78%, fight length 15.6 s. Danger rises by a factor of 2.34 and duration by 1.56.

`R = 3 × 0.8 / (1.25 × 1.5) = 2.4 / 1.875 = 1.28`. Health cost `1 / 1.28 = 0.78`. Length `10 × 1.25 / 0.8 = 15.625` s.
</details>

55. *Week 13 · design.* A default fight has `TTK₀ = 6` s and `TTD₀ = 24` s. Design a Nightmare rung with safety ratio 1 and a fight-length cap of 1.25 times the default, with `p ≥ 0.75`. Give two different `(p, e, h)` solutions and explain why they need the same `e`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `(p, e, h) = (1, 3.2, 1.25)` or `(0.8, 3.2, 1)`. Both have `h / p = 1.25` and `e = 3.2`.

`R₀ = 24 / 6 = 4`. Target factor `1/4`. `R = R₀ × p / (h × e)`, and `p / h = 1 / 1.25 = 0.8` once the length is fixed at the cap. So `e = 0.8 / 0.25 = 3.2` for any `p` and `h` with that ratio.

Check the first: TTK `6 × 1.25 = 7.5` s, TTD `24 / 3.2 = 7.5` s, `R = 1`, health cost 100%. Once duration is fixed, `e` carries all the remaining danger.
</details>

56. *Week 13 · compute.* A player's power grows by a factor of 12 over the campaign. You want the safety ratio at the end to be 3 times the safety ratio at the start. What scaling exponent `α` should enemies use?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `α ≈ 0.56`.

`12^(1 − α) = 3`, so `1 − α = ln 3 / ln 12 = 1.099 / 2.485 = 0.442`, and `α = 0.558`.
</details>

57. *Week 13 · design.* A base fight has `R₀ = 3`. You want a hard rung with safety ratio 0.75 using enemy count instead of damage multipliers, with `p = h = 1` and focus fire, where `R = 2R₀ / (N(N + 1) × e)` and fight length is `N × TTK₀`. The fight-length cap is 1.5 times the default. Find the smallest `N` and matching `e`, or show that none fits.

<details>
<summary>Answer and worked solution</summary>

**Answer:** no whole `N` of 2 or more fits, because two enemies already double the fight length. Only `N = 1` with `e = 4` meets both targets.

`N = 2` gives `R = 6 / (6e) = 1/e`, so `e = 4/3` hits 0.75, but length is `2 × TTK₀`, over the 1.5 cap. Any larger `N` is longer still.

`N = 1` gives `R = 3 / e`, so `e = 4`, with no change in length. Enemy count behaves like raising `h` and `e` together, so it always costs duration.
</details>

58. *Week 13 · critique.* A game's menu describes its hardest mode as "enemies deal 3× damage." Under the hood it uses Skyrim's Legendary multipliers from the lecture, `p = 0.25`, `e = 3`, `h = 1`. Critique the description with numbers and propose an honest one.

<details>
<summary>Answer and worked solution</summary>

**Answer:** the mode is 12 times as dangerous as the default and makes fights 4 times longer. The description mentions neither the 12 nor the 4.

Safety ratio factor `p / (h × e) = 0.25 / 3 = 1/12`. Length factor `h / p = 4`. Half the difficulty comes from the player damage cut, which also produces the damage-sponge feel.

An honest description: "Enemies deal 3× damage and you deal ¼ damage. Fights last about 4× as long and are about 12× as dangerous as Normal." Or change the mode to raise `e` alone if longer fights are not the goal.
</details>

## Week 14: Horizontal vs vertical progression

59. *Week 14 · compute.* Power grows 12% per tier. How many tiers apart can two players be and still share a dungeon (`F = 2`)? A raid (`F = 1.5`)?

<details>
<summary>Answer and worked solution</summary>

**Answer:** up to 6 tiers apart for a dungeon, 3 for a raid.

Dungeon: `t* = ln 2 / ln 1.12 = 6.12`. Check: `1.12^6 = 1.97 ≤ 2` and `1.12^7 = 2.21 > 2`.

Raid: `ln 1.5 / ln 1.12 = 3.58`, so 3 tiers.
</details>

60. *Week 14 · compute.* A horizontal system has 5 equally common situations and tools with `b = 0.4`. What is the largest power gap between a newcomer with one tool and a veteran with all five? If a shared fight costs the newcomer 70% of their health, what does it cost the veteran? Separately, what largest `r` lets players 6 tiers apart share a dungeon at `F = 2`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** gap about 1.30, veteran pays 54%. The largest vertical growth is `r ≈ 1.122` per tier.

`P_h(5) = 1.4`, `P_h(1) = 1 + 0.4/5 = 1.08`. Gap `1.4 / 1.08 = 1.296`. Veteran's cost `70% / 1.296 = 54%`.

`r^6 ≤ 2`, so `r ≤ 2^(1/6) = 1.122`, about 12% per tier.
</details>

61. *Week 14 · compute.* Three existing weapons have DPS in (single target, swarm, armored): Axe (90, 70, 60), Spear (70, 95, 55), Mace (75, 60, 95). Two new ones are proposed: Glaive (92, 72, 58) and Warblade (95, 75, 60). The content mix is 40% single, 35% swarm, 25% armored, and the tolerance is 3% above the median expected DPS of the existing weapons. Apply the dominance test and the expected-value test to both. Then repeat the expected-value test for a mix of 60/20/20.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Warblade dominates Axe and fails both tests. Glaive dominates nothing and passes under the first mix (2.0% above median) but fails under the second (6.8% above).

Dominance: Warblade is at least as good as Axe everywhere (95 ≥ 90, 75 ≥ 70, 60 ≥ 60) and better in two, so it dominates Axe. It also dominates Glaive. Glaive loses to Axe on armored (58 < 60), so it dominates nothing.

| Weapon | EV at 40/35/25 | EV at 60/20/20 |
|---|---|---|
| Axe | 75.50 | 80.0 |
| Spear | 75.00 | 72.0 |
| Mace | 74.75 | 76.0 |
| Glaive | 76.50 | 81.2 |
| Warblade | 79.25 | 84.0 |

Medians of the existing three: 75.0 and 76.0. Glaive is 2.0% and 6.8% above. Warblade is 5.7% and 10.5% above. A sidegrade that passes under one content mix can fail under another.
</details>

62. *Week 14 · critique.* A veteran is 12 tiers ahead of a newcomer at `r = 1.1`. The studio announces a stat squish that divides every number by 10 "to let old friends play together again." Critique the claim, and compute what a catch-up rule that raises the newcomer to tier 8 would do instead.

<details>
<summary>Answer and worked solution</summary>

**Answer:** the squish leaves the power gap at 3.14, so it does not help the friends play together. A catch-up to tier 8 cuts the gap to 1.46, inside `F = 2`.

Before: `1.1^12 = 3.14`. After dividing both players by 10, the ratio is unchanged. A squish fixes readability and overflow, not distance.

Catch-up: the newcomer jumps to tier 8, four tiers behind. `1.1^4 = 1.46 ≤ 2`, so they can share a dungeon.
</details>

## Across weeks

63. *Weeks 3 and 9 · design.* A tank starts with 1,000 HP and 0 armor, `K = 100`, and has 50 budget points. One point buys 40 HP. You want the EHP-maximizing build to put exactly 25 points into health and 25 into armor. How much armor should one point buy? Verify by computing EHP at 20, 25 and 30 points into health.

<details>
<summary>Answer and worked solution</summary>

**Answer:** one point should buy 4 armor. EHP is 4,000 at the 25/25 split, against 3,960 at 20 and at 30.

At the target split, `HP = 1,000 + 40 × 25 = 2,000` and `A = 25a`. The equal-margin rule `HP / h = (A + K) / a` gives `2,000 / 40 = (25a + 100) / a`, so `50a = 25a + 100` and `a = 4`.

EHP at `x` points into health is `(1,000 + 40x)(1 + 4(50 − x)/100)`. At `x = 20`: `1,800 × 2.2 = 3,960`. At 25: `2,000 × 2.0 = 4,000`. At 30: `2,200 × 1.8 = 3,960`. Prices decide what the correct tank looks like.
</details>

64. *Weeks 7 and 8 · compute.* A level-up at level 10 takes 40 minutes and one at level 30 takes 200 minutes. Compute power gained per hour at both levels for an exponential curve (21% per level) and a linear curve (`P ∝ L²`, counting the level-up into 10 and into 30). What does the comparison predict about late-game feel?

<details>
<summary>Answer and worked solution</summary>

**Answer:** exponential: 31.5% per hour at level 10 and 6.3% at level 30. Linear: 35.2% per hour at level 10 and 2.1% at level 30.

Exponential: `21% / (40/60 h) = 31.5%`, and `21% / (200/60 h) = 6.3%`.

Linear: into level 10, `(10/9)² − 1 = 23.5%`, over 0.667 h is 35.2%. Into level 30, `(30/29)² − 1 = 7.0%`, over 3.33 h is 2.1%.

On the linear curve progress per hour falls twice over (longer levels, smaller gains), so the late game will feel like a grind unless other rewards fill the gap.
</details>

65. *Weeks 4, 6 and 12 · explain.* Your sheet says a crit build and a no-crit build with the same average damage both kill a key enemy in 4 hits. Playtesters say the crit build "feels slower" against that enemy. Explain how that can be true, what number you would compute to check it, and when you would move from the sheet to a simulation.

<details>
<summary>Answer and worked solution</summary>

**Answer:** if the enemy's health sits exactly on the no-crit build's breakpoint (4 hits with no overkill), the crit build's variance can only push it to 5 hits more often than it pulls it to 3, so its mean hits-to-kill is above 4.

Compute the crit build's hits-to-kill distribution with the binomial method from week 6 (or the lecture example, which gives 4.16 hits against 100 health for a 25% crit build averaging 25). Simulate when the average hits-to-kill is within about one standard deviation of a whole number, or when turn order or state-dependent behaviour matters, because the sheet can only report the mean.
</details>

66. *Weeks 10 and 13 · design.* You need a Hard rung that cuts the safety ratio of a base fight (`R₀ = 3`, 10-second TTK) to 1. Compare two ways: doubling the enemy count with focus fire, or keeping one enemy and raising `e`. Give the fight length and safety ratio of each, and say which one you would ship for an action game where you want kill-order decisions.

<details>
<summary>Answer and worked solution</summary>

**Answer:** two enemies give `R = 1` and a 20-second fight. One enemy at `e = 3` gives `R = 1` and a 10-second fight. For an action game that wants kill-order decisions, ship the two-enemy version, and make the two enemies differ in `d/h` so the order matters.

Two identical enemies focused one at a time cost `1 + 2 = 3` single fights of damage over twice the time, so `R = 3 / 3 = 1` and length is 20 s.

One enemy with `e = 3`: `R = 3 / 3 = 1`, length unchanged.

With identical enemies the order does not matter, so the design goal needs different priority ratios. If fight length matters more than decisions, raise `e` instead.
</details>
