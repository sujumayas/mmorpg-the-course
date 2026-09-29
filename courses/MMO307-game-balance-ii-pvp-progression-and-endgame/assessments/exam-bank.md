# MMO307 · Exam bank: quiz, practice and viva questions

MMO307 has no written exam. The grade comes from three components, set in `curriculum.yaml`.

| Component | Weight | Brief |
|---|---|---|
| Rating lab | 30% | [rating-lab-brief.md](rating-lab-brief.md) |
| Progression analysis | 30% | [progression-analysis-brief.md](progression-analysis-brief.md) |
| Final season design | 40% | [final-season-design-brief.md](final-season-design-brief.md) |

This bank has three other jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab will go quickly.
- **Lab quizzes.** Each lab session from week 2 on opens with a 10-minute ungraded quiz of two or three questions from this bank. Usually one applies a lecture model to new numbers and one asks you to explain or critique.
- **Viva.** The progression analysis interview and the week 15 season design viva ask questions in this style, rewritten with the numbers from your own design.

Every question is tagged with the week it draws on and one type.

- **compute**: apply a lecture model (the coupon-collector wait, the ratchet, `W / c`, `m_e`, `w*`, the clone constraint, `K(S − E)`, `RD'`, `W × w`, `τ ln(e₀/ε)`, `log_r k`, `D̄(T)`, `E((1 − f)δ)`) to numbers you have not seen before.
- **code**: say what a piece of Python prints, and why.
- **explain**: say why something behaves as it does, with a number as evidence.
- **design**: choose a value or a rule for a stated situation and justify it with the model.
- **critique**: find what is wrong with a piece of code or a proposal and say how to fix it.

All numbers are invented unless a question names a game. Every game fact used here comes from the lecture of the tagged week, which cites its source and version. Every code snippet runs as shown with Python 3.13 (`.venv/bin/python`) and prints exactly what the answer says. Every number in the answers was recomputed in Python from the lectures' own models. Write your own answer before you open the solution.

---

## Week 1: The endgame problem

1. *Week 1 · compute.* A tier's gear set has `S = 8` slots and pays out random single drops, one item per run for a slot chosen uniformly at random. `H_8 = 2.718`.
   (a) What is the expected number of runs to fill the set?
   (b) After how many runs does the average player's upgrade chance on the next run first fall below 25%? How many slots do they have filled at that point, on average?
   (c) The exact finish distribution puts the median at 20 runs and the 90th percentile at 33. Your median player runs the content 4 times a week. In which week do the median and the 90th-percentile players finish, and how many of the median player's runs are spent below the 25% floor?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 21.74 runs. (b) After 11 runs (`n* = 10.38`), so from run 12 on, with about 6 of 8 slots filled. (c) Week 5 and week 9. Nine of the median player's 20 runs (runs 12 to 20) sit below the floor.

(a) `E[runs] = S × H_S = 8 × 2.718 = 21.74`.

(b) The average upgrade chance after `n` runs is `u(n) = (1 − 1/8)^n = 0.875^n`. It crosses 25% at `n* = ln 0.25 / ln 0.875 = −1.386 / −0.1335 = 10.38`. Expected slots filled at that point are `S × (1 − u) = 8 × 0.75 = 6`.

(c) `20 / 4 = 5`, so the median player finishes in week 5. `33 / 4 = 8.25`, so the 90th-percentile player finishes in week 9. `u(n)` is the chance on run `n + 1`. `u(10) = 0.263` is still above the floor and `u(11) = 0.230` is below it, so runs 12 to 20, nine runs, are below it. Half of that player's chase happens in the part the lecture calls "where the frustration lives".
</details>

2. *Week 1 · compute.* `S = 12` and a player has 10 slots filled.
   (a) What is their chance of an upgrade from one random drop, and from a weekly vault that shows 4 random items and lets them keep one?
   (b) How many vault options are needed for at least a 75% chance of an upgrade?
   (c) A teammate says a choice of 4 "quadruples the upgrade chance". What number does that claim give, and why is it wrong?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 16.7% and 51.8%. (b) 8 options. (c) It claims 66.7%. The true value is 51.8%, because the four draws can repeat the same filled slots.

(a) One drop: `(12 − 10) / 12 = 16.7%`. Choice of 4, by the complement rule: `1 − (10/12)^4 = 1 − 0.4823 = 51.8%`.

(b) Need `(5/6)^m ≤ 0.25`, so `m ≥ ln 0.25 / ln(5/6) = 7.60`. Round up to 8.

(c) `4 × 16.7% = 66.7%`. Multiplying adds up the chance of each draw as if they could not overlap. The complement rule counts "no draw is an upgrade", `(10/12)^4`, and subtracts it from 1.
</details>

3. *Week 1 · compute.* A token track prices each of 9 items at 6 tokens. One run pays 2 tokens, and the track has a weekly cap of 12 tokens.
   (a) How many runs does the full set take? What is the upgrade rate per run?
   (b) In which week does a player who runs 10 times a week finish? A player who runs 4 times a week?
   (c) When would the 10-run player finish without the cap? What did the cap do to the spread between the two players?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 27 runs, one item per 3 runs (33%). (b) Week 5 and week 7. (c) Week 3. The cap pulled the heavy player back from week 3 to week 5, so the gap between them shrank from 4 weeks to 2.

(a) The set costs `9 × 6 = 54` tokens. At 2 per run that is `54 / 2 = 27` runs. An item every `6 / 2 = 3` runs.

(b) The heavy player would earn 20 tokens a week but the cap stops them at 12. `54 / 12 = 4.5`, so they finish during week 5. The light player earns `4 × 2 = 8` a week, below the cap. `54 / 8 = 6.75`, so they finish during week 7.

(c) Without the cap the heavy player needs `27 / 10 = 2.7` weeks, finishing in week 3. Uncapped, the gap is week 3 against week 7. Capped, it is week 5 against week 7. This is week 1's point that a cap turns hours into weeks and lets the designer set the finish date.
</details>

4. *Week 1 · code.* This is the lecture's code with a different `S`. What does it print? Why is the expected number of runs for `m = 6` still above 6?

```python
def upgrade_chance(k, S, m=1):
    return 1 - (k / S) ** m

def expected_runs(S, m=1):
    return sum(1 / upgrade_chance(k, S, m) for k in range(S))

for m in (1, 2, 6):
    print(m, round(expected_runs(6, m), 2), round(upgrade_chance(5, 6, m), 3))
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
1 14.7 0.167
2 9.56 0.306
6 6.62 0.665
```

For `m = 1`, the expected runs are `6 × H_6 = 6 × 2.45 = 14.7`. The third column is the chance of an upgrade for a player with 5 of 6 slots filled, `1 − (5/6)^m`. Even six options can all land on filled slots, with probability `(5/6)^6 = 0.335`. So the last slot still takes `1 / 0.665 = 1.5` runs on average, and every earlier slot takes a little over 1, which adds up to 6.62. Choice flattens the tail but cannot remove it.
</details>

---

## Week 2: Vertical progression and power creep

5. *Week 2 · compute.* A raid ladder has `D = 5` rungs, spacing `s = 8`, upgrade margin `u = 4` and overlap rule `o = 3`. There are 3 tiers per expansion. Power grows by `g = 1.2%` per item level and content serves a band `F = 2`.
   (a) Compute the creep per tier `c`, the creep per expansion `C`, the power growth per tier `r` and the shelf life `t*`.
   (b) The team moves to `o = 1`. Recompute `c` and `t*`.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `c = 28`, `C = 84`, `r = 1.397`, `t* = 2.08` tiers. (b) `c = 12`, `t* = 4.84` tiers.

(a) `c = o × s + u = 3 × 8 + 4 = 28`. `C = 3 × 28 = 84`. `r = 1.012^28 = 1.397`. `t* = ln F / (c × ln(1 + g)) = 0.693 / (28 × 0.01193) = 0.693 / 0.334 = 2.08`.

(b) `c = 1 × 8 + 4 = 12`. `t* = 0.693 / (12 × 0.01193) = 0.693 / 0.1432 = 4.84`. Lowering the overlap more than doubled the shelf life. The spacing and margin did not change at all.
</details>

6. *Week 2 · design.* You plan four expansions of three tiers each. The budget formula gives `g = 0.5%` per item level, the band is `F = 1.8`, and the director wants a shelf life of at least 3 tiers. Your ladder has `D = 4`, `s = 12` and `u = 6`.
   (a) What is the largest creep per tier you can allow?
   (b) What is the largest whole overlap rule `o` that fits? What creep and shelf life does it give?
   (c) What is the plan's total creep and power multiplier?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 39.3 item levels. (b) `o = 2`, `c = 30`, `t* = 3.93` tiers. (c) 360 item levels, a power multiplier of 6.02.

(a) `c ≤ ln 1.8 / (3 × ln 1.005) = 0.5878 / 0.01496 = 39.3`.

(b) `12 × o + 6 ≤ 39.3` gives `o ≤ 2.77`, so `o = 2` and `c = 30`. Then `t* = 0.5878 / (30 × 0.004988) = 3.93`.

(c) Twelve tiers at 30 levels is 360 levels. `1.005^360 = 6.02`. Hand that number to the engineers, as the lecture's section 5 does, to find out whether damage and health values still fit.
</details>

7. *Week 2 · code.* An invented game's top item level per expansion is below. What does the code print? Is this creep additive or multiplicative on the label, and what top do you predict for the next expansion?

```python
tops = [100, 160, 230, 290, 360]
steps = [b - a for a, b in zip(tops, tops[1:])]
ratios = [round(b / a, 3) for a, b in zip(tops, tops[1:])]
print(steps)
print(ratios)
print(round(sum(steps) / len(steps), 1))
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
[60, 70, 60, 70]
[1.6, 1.438, 1.261, 1.241]
65.0
```

Additive. The steps stay near 65 while the ratios fall from 1.60 to 1.24, which is the Final Fantasy XIV pattern from section 3. The same step is a smaller share of a bigger number. An additive model predicts about `360 + 65 = 425`. A multiplicative model using the last ratio would predict `360 × 1.241 ≈ 447`, and the falling ratios say that overshoots.
</details>

8. *Week 2 · explain.* Use the lecture's World of Warcraft tops. Compute the ratio of each of these steps: Legion (735 to 1,000), Battle for Azeroth after the 8.0.1 squish (265 to 485) and Shadowlands after the 9.0.1 squish (140 to 311). Then explain, in terms of the ratchet, why a squish did not slow creep.

<details>
<summary>Answer and worked solution</summary>

**Answer.** 1.361, 1.830 and 2.221.

`1,000 / 735 = 1.361`, `485 / 265 = 1.830`, `311 / 140 = 2.221`. The increments were 265, 220 and 171 levels. The ratchet adds `c = o × s + u` levels per tier, and none of those terms depends on how large the label is. A squish rescales the label, so the next expansion adds about the same number of levels on a smaller base. That is a larger ratio. The squish reset the chart and made the ratios worse. To slow creep you change `o`, `s`, `u` or the number of tiers, not the size of the numbers.
</details>

---

## Week 3: Horizontal progression

9. *Week 3 · compute.* A game has five situations with frequencies 0.35, 0.25, 0.20, 0.10 and 0.10. Every horizontal tool gives `b = 0.4` in its own situation. The upgrade margin is `u = 5%`.
   (a) What is each tool worth? Which ones clear the margin?
   (b) Compute `N_eff` and the gap ceiling `G_max`.
   (c) What would `G_max` be if the five situations were equally common?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 14%, 10%, 8%, 4%, 4%. Three tools clear 5%. (b) `N_eff = 4.08`, `G_max = 1.228`. (c) 1.296.

(a) Values are `b × f_i = 0.4 × f_i`.

(b) `Σ f² = 0.1225 + 0.0625 + 0.04 + 0.01 + 0.01 = 0.245`, so `N_eff = 1 / 0.245 = 4.08`. `G_max = (1 + b) / (1 + b × f_1) = 1.4 / 1.14 = 1.228`.

(c) `1.4 / (1 + 0.4/5) = 1.4 / 1.08 = 1.296`. The even mix widens the ceiling because the newcomer's single tool covers less of play.
</details>

10. *Week 3 · code.* This extends question 9 with a rotation. What does it print? What did the rotation buy, and what did it cost?

```python
b = 0.4
f = [0.35, 0.25, 0.20, 0.10, 0.10]

def summary(f):
    n_eff = 1 / sum(x * x for x in f)
    ceiling = (1 + b) / (1 + b * max(f))
    return round(n_eff, 2), round(ceiling, 3)

def rotate(f, lam):
    n = len(f)
    return [lam / n + (1 - lam) * x for x in f]

print(summary(f))
g = rotate(f, 0.4)
print([round(x, 2) for x in g], summary(g))
print(sum(1 for x in g if b * x >= 0.05))
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
(4.08, 1.228)
[0.29, 0.23, 0.2, 0.14, 0.14] (4.63, 1.254)
5
```

`rotate` applies `f' = λ/n + (1 − λ) f` with `λ = 0.4`, so each frequency moves 40% of the way to 0.2. The two rare tools rise from 4% to `0.4 × 0.14 = 5.6%`, so all five tools now clear the margin, up from three. `N_eff` rises from 4.08 to 4.63. The cost is a gap ceiling up from 1.228 to 1.254. Both are small, which is why the lecture says the trade usually favours rotating.
</details>

11. *Week 3 · compute.* A hard-content system uses gate tools. There are 4 counter types, and every activity requires exactly 2 of them. All 6 pairs are equally common.
   (a) What share of activities can a player open with 0, 1, 2, 3 and 4 counters? What is the marginal value of each counter?
   (b) Repeat for 5 counter types where every activity needs 3 (10 triples, equally common).
   (c) Propose one change that gives the first counter some value, and say what it does to the marginal shape.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 0%, 0%, 16.7%, 50%, 100%. Marginals 0, 16.7, 33.3 and 50 points. (b) 0%, 0%, 0%, 10%, 40%, 100%. Marginals 0, 0, 10, 30, 60 points. (c) Add activities that need only one counter.

(a) With `j` counters a player opens `C(j, 2)` of the 6 pairs: 0, 0, 1, 3, 6. As shares, 0, 0, 1/6, 1/2 and 1.

(b) `C(j, 3) / 10`: 0, 0, 0, 1, 4, 10 triples.

(c) Section 4's first response. If some activities need a single counter, the first counter opens those at once, so its marginal value is no longer zero. The shape still rises, because the last counter completes every pair, but players who own none now have a reason to start.
</details>

---

## Week 4: Gear treadmills and item level

12. *Week 4 · compute.* A season's ladder runs from item level 500 to 572. The next season's entry is 548. Use an exponential budget with `g = 0.9%` per level.
   (a) Give `W`, `c` and the carry-over ratio.
   (b) Where does the old top land on the new ladder, and how many seasons does it survive? Same questions for an old item at 530.
   (c) Compute the patch-day gap, the season growth and the in-season spread.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `W = 72`, `c = 48`, `W / c = 1.5`. (b) The top lands at `x₁ = 0.33` and survives 1 season. The 530 item lands at `−0.25`, below the ladder, and survives 0. (c) 1.240, 1.537 and 1.906.

(b) `x₁ = (572 − 548) / 72 = 0.333` and `n_max = floor(72 / 48) = 1`. For 530, `x₁ = (530 − 548) / 72 = −0.25` and `n_max = floor((530 − 500) / 48) = 0`.

(c) Patch day `1.009^(72 − 48) = 1.009^24 = 1.240`. Growth `1.009^48 = 1.537`. Spread `1.009^72 = 1.906`. Same carry-over ratio as Midnight's seam, so the old top lands at the same third of the way up.
</details>

13. *Week 4 · design.* Work backwards with `g = 0.8%`. The band is `F = 1.8`, and the producer wants the old top to land at `x = 0.4`.
   (a) What is the widest ladder that keeps the in-season spread inside `F`? Use the largest whole width.
   (b) What creep lands the old top at 0.4? What are the patch-day gap and the season growth?
   (c) The producer adds a patch-day target of `P = 1.15`. Show that it conflicts with (b), and give the `x` that `W = 73` and the smallest allowed `c` would produce.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `W = 73`. (b) `c = 44`, patch-day gap 1.26, growth 1.42. (c) The target needs `W − c ≤ 17.5`, so `c ≥ 56`, which lands the old top at `x = 0.23`, not 0.4.

(a) `W ≤ ln 1.8 / ln 1.008 = 0.5878 / 0.00797 = 73.8`, so 73.

(b) `c = (1 − x) W = 0.6 × 73 = 43.8`, round to 44. Patch day `1.008^(73 − 44) = 1.008^29 = 1.26`. Growth `1.008^44 = 1.42`.

(c) `W − c ≤ ln 1.15 / ln 1.008 = 0.1398 / 0.00797 = 17.5`. With `W = 73`, `c ≥ 55.5`, so 56. Then `x = 1 − 56/73 = 0.23`. Section 4's table predicts the clash. Carry-over wants `c` small next to `W`, and a small patch-day gap wants `c` close to `W`. Relax one of them in writing.
</details>

14. *Week 4 · compute.* Use the Burning Crusade epic weapon formula from the lecture, `DPS = 0.6 × ilvl + 15.5`.
   (a) What is the effective `g` per item level at item level 200?
   (b) What percentage does a +13 step add from 200?
   (c) At what item level has the effective `g` fallen to half its value at 200?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 0.44% per level. (b) 5.8%. (c) About item level 426.

(a) `DPS(200) = 135.5`, and `g_eff = a / (a i + b) = 0.6 / 135.5 = 0.443%`.

(b) `DPS(213) = 143.3`, and `143.3 / 135.5 − 1 = 5.76%`.

(c) Halving `a / (a i + b)` needs `a i + b` to double, to 271. So `0.6 i = 271 − 15.5 = 255.5` and `i = 425.8`. Under a linear budget each fixed step is worth half as much here, so a designer who wants the same felt upgrade must double `c`.
</details>

---

## Week 5: Stat squish

15. *Week 5 · compute.* A game's smallest meaningful creature health is 500 and its largest is 4,000,000. The display wants values between 200 and 40,000.
   (a) Does a uniform divisor exist? Show both bounds on `d`.
   (b) How wide would the readable band `b / a` have to be for a uniform squish to work?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) No. `d` would need to be at least 100 and at most 2.5. (b) `b / a ≥ 8,000`.

(a) The dynamic range is `4,000,000 / 500 = 8,000`. The band allows `40,000 / 200 = 200`. The largest value needs `d ≥ 4,000,000 / 40,000 = 100`. The smallest needs `d ≤ 500 / 200 = 2.5`. No `d` satisfies both.

(b) A uniform squish needs `v_max / v_min ≤ b / a`, so the band ratio must reach 8,000. With `a = 200` that means `b = 1,600,000`, which defeats the point of squishing.
</details>

16. *Week 5 · compute.* Three eras of creature health are 5,000, 60,000 and 900,000. A current player hits for 300,000. The team squishes with divisors 5, 20 and 150.
   (a) Give each era's new health and the player's new hit.
   (b) Give hits to kill before and after the squish, era by era.
   (c) Build the compensation table `m_e`. How does it restore era 2?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 1,000, 3,000, 6,000. The hit becomes 2,000. (b) Before 1, 1, 3. After 1, 2, 3. (c) `m = 30, 7.5, 1`.

(a) `5,000 / 5`, `60,000 / 20`, `900,000 / 150`. The hit shrinks by the current era's divisor, `300,000 / 150 = 2,000`.

(b) Before, `ceil(v / 300,000)` gives 1, 1, 3. After, `ceil(new / 2,000)` gives 1, 2, 3. The current era is untouched. Era 2 went from one hit to two.

(c) `m_e = d_E / d_e = 150/5, 150/20, 150/150`. Against era 2 the player's hit becomes `2,000 × 7.5 = 15,000`, which is more than the 3,000 health, so one hit kills again. The ratio against era 2 fell by `d_2 / d_E = 20 / 150`, and `m_2` is exactly its inverse.
</details>

17. *Week 5 · compute.* Numbers in a game grow by `R = 1.5` per year.
   (a) The team squishes by `d = 30`. How many years of headroom does that buy?
   (b) What divisor would last 10 years?
   (c) Why does the answer to (b) worry the team, using section 2's dynamic range?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 8.4 years. (b) `d ≥ 57.7`. (c) Almost doubling the divisor buys only 1.6 extra years, and it pushes old-era values toward the bottom of the readable band.

(a) `T = ln 30 / ln 1.5 = 3.401 / 0.4055 = 8.39`.

(b) `d = 1.5^10 = 57.7`.

(c) Headroom grows with `ln d`. Going from 30 to 57.7 adds `ln(57.7/30) / ln 1.5 = 1.6` years. The larger divisor also shrinks every era by more, so the oldest eras hit the resolution bound `a` sooner and need a stronger bend and a bigger compensation table. Lowering `R` is the lever that moves the calendar.
</details>

18. *Week 5 · code.* A damage-over-time tick is squished by 25 with rounding and a floor of 1. What does this print? Which ticks does the squish break, and what is one fix?

```python
def tick_after(old, d):
    return max(1, round(old / d))

for old in (4, 9, 30, 55, 2_000):
    new = tick_after(old, 25)
    exact = old / 25
    print(old, new, f"{(new - exact) / exact:+.0%}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
4 1 +525%
9 1 +178%
30 1 -17%
55 2 -9%
2000 80 +0%
```

`4 / 25 = 0.16` rounds to 0 and the floor lifts it to 1, which is 6.25 times the exact value. `9 / 25 = 0.36` becomes 1 as well, so two ticks that differed by more than a factor of two are now equal. The small ticks are broken, by both the floor and rounding. Fixes from section 4: tick less often with bigger ticks, keep one or two decimals of precision in storage, or give the oldest era a smaller divisor.
</details>

19. *Week 5 · compute.* A squish divides all damage and healing by 20 and player health by 10. Before the squish, a player survived 8 seconds under a boss's damage, and a healer's big heal restored a quarter of a player's health. What are both numbers after the squish? Is this part of the squish or a balance change?

<details>
<summary>Answer and worked solution</summary>

**Answer.** 16 seconds, and an eighth of a player's health. It is a balance change.

Time to die is health over incoming damage per second. Health falls by 10 and damage by 20, so time to die doubles, `8 × 2 = 16` seconds. A heal of `H/4` becomes `(H/4)/20` against a health of `H/10`, which is `(1/4) × (10/20) = 1/8` of the new health. Healing per cast halved relative to health, while each player has twice as long to be healed. Both effects are real balance changes. Section 4 says to write them on the intended-changes list, as WoW did in 2014, not to let them ride in as side effects.
</details>

---

## Week 6: Catch-up mechanics

20. *Week 6 · compute.* A currency has a weekly allowance `L = 500` and a finish line `N = 8,000`. A late player misses the first 5 weeks and then plays at `v = 1,250` a week.
   (a) Under a rolling cap, when does the late player catch the allowance, and when do they finish?
   (b) Under a weekly cap, when do they finish, and how far behind a veteran are they until the veteran stops earning?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) They catch the allowance during week 9 (`w* = 8.33`) and finish in week 16, the same week as the veteran. (b) Week 21, and 2,500 behind until week 16.

(a) `w* = v j / (v − L) = 1,250 × 5 / 750 = 8.33`. The finish week is `max(j + N/v, N/L) = max(5 + 6.4, 16) = 16`. From week 9 the allowance, not speed, holds them back.

(b) They earn `min(v, L) = 500` a week, so they need `8,000 / 500 = 16` playing weeks and finish in week 21. The gap is `L × j = 2,500` until the veteran reaches `N` in week 16. In a 20-week season they never finish.
</details>

21. *Week 6 · compute.* Same season (`L = 500`, `N = 8,000`, rolling cap).
   (a) Compute the free lateness window for `v = 500`, `1,250` and `2,000`.
   (b) The team adds a head start, so the allowance becomes `1,000 + 500 w`. Recompute the window for `v = 1,250`.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 0, 9.6 and 12 weeks. (b) 7.6 weeks.

(a) `J_free = N/L − N/v`. For `v = 500` it is `16 − 16 = 0`. For 1,250 it is `16 − 6.4 = 9.6`. For 2,000 it is `16 − 4 = 12`. A player at four times the allowance can skip three quarters of the season at no cost.

(b) The veteran now reaches 8,000 when `1,000 + 500 w = 8,000`, in week 14. The late player still needs 6.4 playing weeks, so `J_free = 14 − 6.4 = 7.6`. A head start moves `N/L` earlier for everyone, which is one of section 3's two fixes.
</details>

22. *Week 6 · code.* This models a rolling cap with an optional raise. What does it print? Who did the raise after week 8 help?

```python
def allowance(w, L=500, rolling=True, raise_after=None, L2=None):
    """Most a player may have earned in total by the end of week w."""
    if not rolling:
        raise ValueError("weekly caps are per week; see earned()")
    if raise_after is None or w <= raise_after:
        return L * w
    return L * raise_after + L2 * (w - raise_after)

def earned(w, j, v, N=8_000, **rule):
    """A player who misses the first j weeks, then plays at speed v."""
    return min(N, max(0, min(v * (w - j), allowance(w, **rule))))

for w in (6, 8, 10, 12):
    print(w, earned(w, 5, 1_250), earned(w, 5, 1_250, raise_after=8, L2=1_000))
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
6 1250 1250
8 3750 3750
10 5000 6000
12 6000 8000
```

By week 8 the late player (`j = 5`, `v = 1,250`) has earned `3 × 1,250 = 3,750`, below the allowance of 4,000. At week 10 their speed would give 6,250 but the old allowance stops them at 5,000. The raise lifts the allowance to `4,000 + 2 × 1,000 = 6,000`. At week 12 they hit `N` under the raise and are at 6,000 without it. The raise helped because this player was cap-limited from week 9 on. A late player slower than the old `L` would gain nothing, as section 4 says.
</details>

23. *Week 6 · compute.* In the rolling-cap season of question 20 (`L = 500`, `N = 8,000`), the designers remove the cap after week 6.
   (a) A heavy veteran plays at `v = 2,000` and was capped all season. When do they finish?
   (b) A light veteran plays at exactly 500. When do they finish?
   (c) The late player of question 20 (`j = 5`, `v = 1,250`) has 1,250 at the end of week 6. When do they finish now?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) Week 9. (b) Week 16, unchanged. (c) Week 12, four weeks earlier than with the cap.

(a) They have `6 × 500 = 3,000` at the end of week 6. At 2,000 a week they reach 5,000, 7,000 and then 9,000, so they finish during week 9.

(b) Their speed equals the old allowance, so removing the cap changes nothing. `8,000 / 500 = 16`.

(c) They need 6,750 more at 1,250 a week, which is 5.4 weeks, so they finish during week 12. Before the removal the allowance held them to week 16. The removal helped the heavy veteran most (7 weeks earlier), which is section 2's warning that removing a cap rewards speed.
</details>

---

## Week 7: PvP vs PvE split tuning

24. *Week 7 · compute.* Use the lecture's model (`C = 60` s, `H = 30,000`, PvE target 1,100 ± 3%, PvP band 15 to 22 s). A class has `s = 800` and `B = 20,000`.
   (a) Compute its PvE DPS and PvP TTK. Which band does it fail?
   (b) What fraction of the standard target's health does its opener remove?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) PvE 1,133.3 and TTK 12.5 s. It sits just outside the PvE band (1,067 to 1,133) and well below the PvP band. (b) Two thirds.

(a) `s + B/60 = 800 + 333.3 = 1,133.3`. `(30,000 − 20,000) / 800 = 12.5` seconds.

(b) `20,000 / 30,000 = 67%`. The defender loses two thirds of their health before they can act.
</details>

25. *Week 7 · compute.* Change the PvE target to `D = 1,200`, keeping `C = 60` and `H = 30,000`.
   (a) Find the clone shape for `T = 18` s.
   (b) Find the clone shapes at `T = 15` and `T = 22`. What range of burst can a class carry and still meet both targets?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `s = 1,000`, `B = 12,000`. (b) At 15 s, `s = 933.3` and `B = 16,000`. At 22 s, `s = 1,105.3` and `B = 5,684`. Burst must sit between about 5,700 and 16,000.

(a) `s = (C D − H) / (C − T) = (72,000 − 30,000) / 42 = 1,000`. `B = H − T s = 30,000 − 18,000 = 12,000`. Check: `1,000 + 12,000/60 = 1,200`.

(b) `s = 42,000 / 45 = 933.3`, `B = 30,000 − 15 × 933.3 = 16,000`. `s = 42,000 / 38 = 1,105.3`, `B = 30,000 − 22 × 1,105.3 = 5,684`. A "one big hit" class with 25,000 burst and a "steady pressure" class with 3,000 both fall outside, which is the clone constraint.
</details>

26. *Week 7 · compute.* Put the class from question 24 (`s = 800`, `B = 20,000`) at a PvP target of 16 s without touching PvE.
   (a) Compute the burst multiplier `p` and round it to 0.05. What TTK results?
   (b) Compute the sustain multiplier `q` and round it to 0.05. What TTK results?
   (c) Which split would you ship, and why?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `p = 0.86`, rounded 0.85, TTK 16.25 s. (b) `q = 0.78`, rounded 0.80, TTK 15.6 s. (c) The burst split.

(a) `p = (H − T s) / B = (30,000 − 12,800) / 20,000 = 0.86`. With 0.85, `(30,000 − 17,000) / 800 = 16.25`.

(b) `q = (H − B) / (T s) = 10,000 / 12,800 = 0.78`. With 0.80, `10,000 / 640 = 15.6`.

(c) Both land in the band. Section 2's rule says to split the field the two metrics weigh differently. PvE counts burst once a minute and PvP counts it once a fight, so burst is the field. Cutting sustain in PvP would also weaken the class in long PvP fights, which nobody asked for.
</details>

27. *Week 7 · code.* What does this print? Explain the last line in one sentence.

```python
H = 30_000
roster = {"Duelist": (900, 12_000), "Ravager": (700, 24_000), "Channeler": (1_050, 3_000)}

def pvp_ttk(s, B, h=1.0):
    return max(0.0, h * H - B) / s

for h in (1.0, 1.5, 3.0):
    ttks = {name: round(pvp_ttk(s, B, h), 1) for name, (s, B) in roster.items()}
    fastest = min(ttks, key=ttks.get)
    print(h, ttks, fastest)
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
1.0 {'Duelist': 20.0, 'Ravager': 8.6, 'Channeler': 25.7} Ravager
1.5 {'Duelist': 36.7, 'Ravager': 30.0, 'Channeler': 40.0} Ravager
3.0 {'Duelist': 86.7, 'Ravager': 94.3, 'Channeler': 82.9} Channeler
```

At `h = 3` the target has 90,000 effective health, so the Ravager's 24,000 opener is only 27% of it and the fight becomes a sustain contest that the Channeler's 1,050 per second wins. A global health multiplier is a balance change that moves power from burst classes to sustain classes, as section 3 warns.
</details>

28. *Week 7 · compute.* Under the Dampening rule in section 2 (3v3 starts after five minutes, one 1% stack every 10 seconds), a healer produces 4,800 healing per second against 4,300 incoming damage per second. At what minute of the match does healing first fail to keep up?

<details>
<summary>Answer and worked solution</summary>

**Answer.** About 6 minutes 50 seconds into the match.

Healing holds while `4,800 × (1 − stacks/100) ≥ 4,300`, so while `stacks ≤ 100 × (1 − 4,300/4,800) = 10.4`. The 11th stack arrives 110 seconds after dampening starts at 300 seconds, at 410 seconds, which is 6 minutes 50 seconds. From then on the healer loses ground and the stalemate from MMO303 week 11 ends.
</details>

---

## Week 8: Elo and expected score

29. *Week 8 · compute.* A 1,850 player meets a 1,600 player with `K = 24`.
   (a) What is the favourite's expected score?
   (b) How many points does the favourite gain for a win and lose for a loss?
   (c) At what true win probability would this favourite's average change be zero?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 0.808. (b) +4.6 and −19.4. (c) 0.808.

(a) `E = 1 / (1 + 10^(−250/400)) = 1 / (1 + 0.237) = 0.808`.

(b) Win `24 × (1 − 0.808) = 4.6`. Loss `24 × 0.808 = 19.4`. The two add to K.

(c) The average change is `K (p − E)`, which is zero when `p = E = 0.808`. If the favourite really wins 80.8% of these games, farming them neither helps nor hurts.
</details>

30. *Week 8 · compute.* A new player at 2,000 uses `K = 40`. An established player at 2,100 uses `K = 10`.
   (a) The new player wins. How many points does each move, and what happens to the pool?
   (b) The new player loses. Same questions.
   (c) New players on this ladder usually start underrated. Which way does the pool drift?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) +25.6 and −6.4, so the pool gains 19.2. (b) −14.4 and +3.6, so the pool loses 10.8. (c) It inflates.

The new player's `E = 1 / (1 + 10^(100/400)) = 0.360`.

(a) `40 × 0.640 = 25.6` and `10 × 0.640 = 6.4`.

(b) `40 × 0.360 = 14.4` and `10 × 0.360 = 3.6`.

(c) An underrated player wins more than `E` predicts, so wins outnumber the model's expectation and each one injects points. Section 5's unequal-K argument.
</details>

31. *Week 8 · design.* A public ladder must keep an established player's settled wobble under 40 points.
   (a) What is the largest whole K that meets this? Use `g = ln 10 / 1600`.
   (b) With that K, what are the time constant and the number of games needed to close a 400-point gap to 40?
   (c) Why does this result push you toward a two-stage K?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `K = 18`, with a wobble of 39.5. (b) `τ = 38.6` games and about 89 games. (c) New players would take nearly 90 games to place.

(a) `σ = sqrt(K / (8g)) ≤ 40` gives `K ≤ 40² × 8 × 0.001439 = 18.4`. At `K = 18`, `σ = 39.5`.

(b) `τ = 1 / (18 × 0.001439) = 38.6`. Closing 400 to 40 takes `τ × ln 10 = 88.9` games.

(c) One K cannot serve both a new player and a settled one. A provisional K of 40 for the first 30 games covers almost two time constants at `τ = 17.4`, then K drops to 18 for a steady public number. That is FIDE's structure.
</details>

32. *Week 8 · code.* What does this print? What does the last line show, and would it still hold if each player used their own K?

```python
def expected(r_a, r_b):
    return 1 / (1 + 10 ** ((r_b - r_a) / 400))

def update(r_a, r_b, score_a, k=20):
    delta = k * (score_a - expected(r_a, r_b))
    return r_a + delta, r_b - delta

a, b = 1_700, 1_500
for result in (1, 1, 0):
    a, b = update(a, b, result)
    print(round(a, 1), round(b, 1))
print(round(a + b, 6))
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
1704.8 1495.2
1709.4 1490.6
1693.8 1506.2
3200.0
```

The first win at a 200-point gap pays `20 × (1 − 0.760) = 4.8`. The second win pays a little less because the gap has grown. The loss costs 15.6 because the gap is now 219 points and the favourite was expected to win about 78% of the time. The sum stays at 3,200 because `update` moves the same `delta` from one player to the other. With separate K values for the two players, the changes would differ and the sum would drift, as question 30 shows.
</details>

33. *Week 8 · compute.* A ladder counts any gap above 400 as 400 in the formula, as FIDE does below 2,650. A player's true edge over a weaker regular opponent is 500 points. `K = 16`. What is their average rating change per game against this opponent, and over 80 games?

<details>
<summary>Answer and worked solution</summary>

**Answer.** About +0.60 per game, and about +48 over 80 games.

True `p = E(500) = 1 / (1 + 10^(−1.25)) = 0.947`. The capped `E` is `E(400) = 0.909`. The average change is `K (p − E) = 16 × 0.0377 = 0.60`. Over 80 games that is about 48 points gained without any change in true strength. Without the cap `E = p` and the average change is zero. Section 5 asks you to run exactly this check on every rule patch.
</details>

34. *Week 8 · explain.* A calibration bucket holds 900 games in which the favourite's predicted `E` averaged 0.65. Favourites won 58% of them. Is the system calibrated in this bucket? If not, what does the result say about the scale constant 400?

<details>
<summary>Answer and worked solution</summary>

**Answer.** No. 58% is outside the 95% interval of about 61.9% to 68.1%. The game has more randomness per match than 400 assumes, so the scale constant should be larger.

The margin is `1.96 × sqrt(0.65 × 0.35 / 900) = 0.031`, so about ±3.1 points around 65%. Favourites winning less often than predicted means a given rating gap is worth less than the curve says. A larger constant stretches the curve so the same gap predicts a smaller edge. In GD101's language, the die is bigger than the ratings assume.
</details>

---

## Week 9: Glicko and TrueSkill

35. *Week 9 · compute.* A player rated 1,500 meets an opponent rated 1,600. Use `q = ln 10 / 400`.
   (a) Compute `g(RD)` for an opponent RD of 200, and the Glicko expected score. Compare it with plain Elo.
   (b) Repeat for an opponent RD of 30.
   (c) Explain the difference in one sentence.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `g(200) = 0.844`, Glicko `E = 0.381`, Elo `E = 0.360`. (b) `g(30) = 0.995`, `E = 0.361`. (c) An uncertain opponent pulls the prediction toward 50%.

(a) `g = 1 / sqrt(1 + 3 q² 200² / π²) = 1 / sqrt(1 + 0.4029) = 0.844`. Then `E = 1 / (1 + 10^(0.844 × 100 / 400)) = 0.381`. Elo gives `1 / (1 + 10^0.25) = 0.360`.

(b) `g(30) = 0.995`, so the gap barely shrinks and `E = 0.361`.

(c) When you know little about the opponent you know less about the result, so Glicko predicts less boldly.
</details>

36. *Week 9 · compute.* A settled player has RD 70. The game uses a drift constant `c = 50` per period and caps RD at 350.
   (a) What is their RD after 8 idle periods?
   (b) In which idle period does RD first reach the cap?
   (c) Another game wants RD 45 to grow back to 350 in 36 periods. What `c` does Glickman's rule of thumb give?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 157.8. (b) The 48th. (c) `c = 57.8`.

(a) `sqrt(70² + 50² × 8) = sqrt(4,900 + 20,000) = 157.8`.

(b) Need `4,900 + 2,500 t ≥ 122,500`, so `t ≥ 47.04`. After 47 periods RD is 349.9, so the 48th period hits the cap.

(c) `350² = 45² + 36 c²`, so `c² = (122,500 − 2,025) / 36 = 3,346.5` and `c = 57.8`.
</details>

37. *Week 9 · code.* This is the lecture's Glicko-1 update. What does it print? What does the comparison of the two lines show?

```python
import math

Q = math.log(10) / 400

def g(rd):
    return 1 / math.sqrt(1 + 3 * Q**2 * rd**2 / math.pi**2)

def expected(r, rj, rdj):
    return 1 / (1 + 10 ** (-g(rdj) * (r - rj) / 400))

def glicko_update(r, rd, games):
    inv_d2 = Q**2 * sum(g(rdj)**2 * expected(r, rj, rdj) * (1 - expected(r, rj, rdj))
                        for rj, rdj, _ in games)
    denom = 1 / rd**2 + inv_d2
    r_new = r + Q / denom * sum(g(rdj) * (s - expected(r, rj, rdj)) for rj, rdj, s in games)
    return r_new, math.sqrt(1 / denom)

for rd in (120, 40):
    r, new_rd = glicko_update(1600, rd, [(1700, 60, 1)])
    print(rd, round(r - 1600, 1), round(new_rd, 1))
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
120 46.9 114.1
40 5.7 39.8
```

The same upset win against a 1,700 opponent with RD 60 moves a player with RD 120 by 46.9 points and a player with RD 40 by 5.7. The step size is `q · RD'²`, so it scales with the square of the player's own uncertainty. The uncertain player's RD also drops more, from 120 to 114.1, while the settled player's barely moves. This is the "effective K" of section 2. Against this opponent Elo would pay a winner `0.640 K`, so the RD-120 player moves like an Elo player with `K ≈ 73` and the RD-40 player like one with `K ≈ 9`.
</details>

38. *Week 9 · compute.* A three-player TrueSkill team has `σ = 2, 4` and `6`. After a win the update factor is `v / c = 0.08`.
   (a) How much does each player's `μ` rise?
   (b) What share of the team's total `μ` gain goes to the most uncertain player?
   (c) A 2v2 match puts `μ = 27, 23` against `μ = 25, 24`, with every `σ = 3` and `β = 25/6`. Ignoring `τ`, what is `P(first team wins)`?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 0.32, 1.28 and 2.88. (b) 64%. (c) 0.539.

(a) Each rise is `σ² × v / c`: `4 × 0.08`, `16 × 0.08`, `36 × 0.08`.

(b) `36 / (4 + 16 + 36) = 0.643`. TrueSkill rewards the most uncertain player, not the best one.

(c) `c² = 4β² + 4 × 9 = 69.44 + 36 = 105.44`, so `c = 10.27`. The skill gap is `50 − 49 = 1`. `Φ(1 / 10.27) = Φ(0.097) = 0.539`. Adding `τ` to every σ changes this only in the sixth decimal place.
</details>

---

## Week 10: Matchmaking quality vs queue time

39. *Week 10 · compute.* A population has `σ = 180`, and `λ = 20` players enter the queue per minute.
   (a) Use the shortcut to find the median player's `W × w` constant, and the window that gives a 20-second mean wait.
   (b) A player sits at `z = 2.5`. By roughly what factor are their waits longer than the median player's at the same window?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `W × w ≈ 677` and `w ≈ 34`. (b) About 23 times longer.

(a) `σ √(2π) = 451.2`, so `p ≈ 2w / 451.2 = w / 225.6`. Then `W = 60 / (20 × w / 225.6) = 676.8 / w`. A 20-second wait needs `w ≈ 676.8 / 20 = 33.8`.

(b) The density falls by `exp(−z²/2) = exp(−3.125) = 0.044`, so waits grow by `1 / 0.044 = 22.8`. A 20-second median queue is about 7.6 minutes for this player.
</details>

40. *Week 10 · code.* This uses the lecture's model. What does it print? How long does the 1,700 player wait off-peak compared with the median player at peak?

```python
from math import erf, sqrt

MU, SIGMA, LAM = 1500, 200, 12

def Phi(z):
    return 0.5 * (1 + erf(z / sqrt(2)))

def share_in_window(r, w):
    return Phi((r + w - MU) / SIGMA) - Phi((r - w - MU) / SIGMA)

def mean_wait_seconds(r, w, lam=LAM):
    return 60 / (lam * share_in_window(r, w))

for r in (1500, 1700):
    print(r, round(share_in_window(r, 75), 4), round(mean_wait_seconds(r, 75), 1),
          round(mean_wait_seconds(r, 75, lam=3), 1))
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
1500 0.2923 17.1 68.4
1700 0.1814 27.6 110.2
```

The 1,700 player off-peak waits 110.2 seconds, about 6.4 times the median player's 17.1 seconds at peak. One standard deviation up multiplies the wait by `0.2923 / 0.1814 = 1.61`, and dropping `λ` from 12 to 3 multiplies it by 4. The two effects stack.
</details>

41. *Week 10 · compute.* A game with one ranked queue at `λ = 12` splits into four equal queues, each at `λ = 3`. Use the lecture's table and shortcuts (`σ = 200`).
   (a) What does the median player's wait become at `w = 50`?
   (b) Using `W × w ≈ 1,253` scaled for the smaller pool, what window keeps the median wait near 25 seconds? What fairness does the shortcut predict?
   (c) The exact model says the window must be about 251, with fairness 0.648. Why are both of the shortcut's numbers off?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) About 101 seconds. (b) About `w = 200`, with a shortcut fairness of 0.644. (c) Both shortcuts assume a narrow window.

(a) `W ∝ 1/λ`, so `4 × 25.3 = 101.2` seconds.

(b) `W × w ≈ 4 × 1,253 = 5,012`, so `w ≈ 5,012 / 25 = 200`. `E_fav ≈ 0.5 + 0.00072 × 200 = 0.644`.

(c) At `w = 200` the density is not flat across the window, so the share is smaller than `2w f(r)` and the exact wait at `w = 200` and `λ = 3` is `4 × 7.3 = 29.2` seconds. It takes `w ≈ 251` to reach 25.3. The fairness shortcut is good only to about 150. The lecture's table gives 0.626 at `w = 200`, and at 251 the exact value is 0.648. The split cost every median match about 0.11 of favourite expected score.
</details>

42. *Week 10 · compute.* Waits for the first acceptable opponent follow the continuous version of MA102's geometric wait.
   (a) With a mean wait of 30 seconds, what is the 90th-percentile wait, and what share of queues last longer than a minute?
   (b) What mean wait meets "95% of queues under 90 seconds"?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 69 seconds, and 13.5% of queues. (b) At most 30.0 seconds.

(a) The 90th percentile is `ln 10 × 30 = 69.1` seconds. The share longer than `t` is `exp(−t / mean) = exp(−2) = 0.135`.

(b) Need `exp(−90 / mean) ≤ 0.05`, so `mean ≤ 90 / ln 20 = 90 / 2.996 = 30.0` seconds.
</details>

---

## Week 11: Seasonal structures and resets

43. *Week 11 · compute.* A ladder has mean 1,500 and uses `K = 40`. A player's true rating is 1,950. The season ends with a soft reset at `α = 0.7`.
   (a) What rating do they restart at, and what is their error?
   (b) Using the linear model with `ε = 25`, how many games until they are within 25 points? How many games do they spend more than 100 points off?
   (c) They play 40 ranked games a season. What is their misplaced share?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 1,815, and 135 points too low. (b) About 29 games, and about 5 games more than 100 off. (c) About 73%.

(a) `r_new = 1,500 + 0.7 × 450 = 1,815`. `e₀ = 0.3 × 450 = 135`.

(b) `τ = 1 / (40 × 0.001439) = 17.4`. Games to 25: `17.4 × ln(135/25) = 17.4 × 1.686 = 29.3`. Games more than 100 off: `17.4 × ln(1.35) = 5.2`.

(c) `29.3 / 40 = 0.73`. Even a light reset costs a casual player most of their season. Section 4 says to move the reset to a visible track in that case.
</details>

44. *Week 11 · compute.* A visible ladder of 200 stars resets to the bottom each season. Matching is by hidden rating, so an accurate player wins 50% of games. A loss costs 1 star.
   (a) With `b = 5` stars per win, how many games does an accurate player need to climb?
   (b) What `b` lets them climb in 40 games?
   (c) A player who is underrated wins 55% of games with `b = 3`. How many games do they need?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 100 games. (b) `b = 11`. (c) About 167 games.

(a) `(b − 1) / 2 = 2` stars per game, so `200 / 2 = 100`.

(b) Need 5 stars per game, so `(b − 1)/2 = 5` and `b = 11`, Hearthstone's top Star Bonus.

(c) `0.55 × 3 − 0.45 × 1 = 1.2` stars per game, so `200 / 1.2 = 167`. The bonus is the visible track's K-factor and does far more than a 5-point edge in win rate.
</details>

45. *Week 11 · code.* What does this print? Read the table to test the claim "a reset half as strong settles twice as fast."

```python
from math import log

g = log(10) / 1600

def games_to_settle(error, k, eps=25):
    return (1 / (k * g)) * log(error / eps)

true, mu = 1_900, 1_500
for alpha in (0.0, 0.6, 0.9):
    error = (1 - alpha) * (true - mu)
    print(alpha, round(error), round(games_to_settle(error, 24), 1), round(games_to_settle(error, 48), 1))
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
0.0 400 80.3 40.1
0.6 160 53.7 26.9
0.9 40 13.6 6.8
```

The claim is false. Going from a hard reset to `α = 0.6` cuts the error by 60%, from 400 to 160, but saves only `80.3 − 53.7 = 26.6` games at `K = 24`, a third of the recovery. Recovery depends on the logarithm of the error. Doubling K, the last column, halves every recovery exactly, because `τ = 1/(Kg)`.
</details>

46. *Week 11 · critique.* A programmer implements the soft reset like this. With `α = 0.5`, what rating does a 2,100 player get, and what should they get? Does the matchmaker notice the bug? Who does it hurt?

```python
def soft_reset(ratings, alpha):
    return [alpha * r for r in ratings]
```

<details>
<summary>Answer and worked solution</summary>

**Answer.** They get 1,050 instead of 1,800. The matchmaker does not notice. New players entering at 1,500 are hurt.

The lecture's rule is `r_new = μ + α (r_old − μ)`. The code compresses toward 0 instead of toward μ. Every gap is still multiplied by `α`, exactly as in the correct rule, so every expected score between existing players is the same. Only gaps matter (week 8). But the whole ladder now sits `(1 − α) μ = 750` points lower, with a mean of 750. A new account created at the default 1,500 starts far above everyone else and loses its first dozens of games against players the system thinks are weaker. Fix it with `mu + alpha * (r - mu)`, or reset new accounts to the ladder's current mean.
</details>

---

## Week 12: Alternative advancement and account progression

47. *Week 12 · compute.* An AA track uses flat costs of 6 hours per point and 0.5% power per point. A light player plays 4 post-cap hours a week, a heavy player 16.
   (a) After 52 weeks, how many points does each hold, and what is the gap `G`?
   (b) What value does `G` approach in the long run?
   (c) Treating points as continuous, in which week does `G` first exceed 1.3?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 34 and 138 points, `G = 1.444`. (b) 4. (c) About week 33.

(a) `floor(208 / 6) = 34` and `floor(832 / 6) = 138`. `P = 1.17` and `1.69`, so `G = 1.69 / 1.17 = 1.444`.

(b) Points are proportional to hours, so the ratio tends to `16/4 = 4`, and `G` tends to 4 once `v × n` swamps the 1.

(c) Light earns `0.005 × 4/6 = 0.00333` per week in `P`, heavy `0.01333`. `(1 + 0.01333 w) / (1 + 0.00333 w) = 1.3` gives `0.009 w = 0.3`, so `w = 33.3`.
</details>

48. *Week 12 · compute.* A geometric cost schedule has ratio `r = 1.08`.
   (a) In the long run, how many points ahead does a player with 5 times the hours of another end up?
   (b) How many points ahead with 4 times the hours?
   (c) Explain why both players wait about the same number of weeks for their next point.

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 20.9 points. (b) 18.0 points. (c) The next point costs about `r − 1 = 8%` of each player's own history.

(a) `log_1.08 5 = ln 5 / ln 1.08 = 1.609 / 0.0770 = 20.9`.

(b) `ln 4 / ln 1.08 = 18.0`. Adding hours adds a fixed number of points, not a multiple.

(c) With `n` points held, the next costs `a r^n`, and the hours played are about `a r^n / (r − 1)`. So the next point costs `(r − 1)` times everything played so far, and a player's wait in weeks is `(r − 1) × weeks played`, whatever their hours per week.
</details>

49. *Week 12 · compute.* A decaying-value track has flat costs, `v₀ = 1.5%` and `d = 0.99`.
   (a) What is the power ceiling?
   (b) How many points earn 75% of the total bonus?
   (c) What is point 200 worth?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 2.5. (b) 138 points. (c) 0.20% power.

(a) `1 + v₀ / (1 − d) = 1 + 0.015 / 0.01 = 2.5`.

(b) `1 − 0.99^n = 0.75`, so `n = ln 0.25 / ln 0.99 = 137.9`, round up to 138.

(c) `1.5% × 0.99^199 = 1.5% × 0.135 = 0.20%`. Points still arrive every few hours, but by point 200 each one is worth a seventh of the first.
</details>

50. *Week 12 · code.* This is the lecture's geometric schedule. What does it print? A player at 1,600 hours plays 20 hours a week. How many weeks until their next point, and what share of their history does that cost?

```python
from math import log, floor

def points_geometric(hours, first=2, ratio=1.05):
    return floor(log(1 + hours * (ratio - 1) / first) / log(ratio) + 1e-9)

for hours in (100, 400, 1_600):
    n = points_geometric(hours)
    print(hours, n, round(2 * 1.05 ** n, 1))
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
100 25 6.8
400 49 21.8
1600 76 81.5
```

The third column is the cost of the next point, `first × r^n`. At 1,600 hours the next point costs 81.5 hours, about 4.1 weeks at 20 hours a week. That is `81.5 / 1,600 = 5.1%` of the player's history, close to `r − 1 = 5%`. Quadrupling hours from 400 to 1,600 added only 27 points.
</details>

51. *Week 12 · compute.* Bringing a character from the cap to endgame-ready takes `T_c = 50` hours.
   (a) With an account-wide share `s = 40%`, what do five characters cost?
   (b) What `s` keeps five characters at or under 100 hours?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 170 hours. (b) `s ≥ 75%`.

(a) `50 × (1 + 4 × 0.6) = 170`.

(b) `50 × (1 + 4(1 − s)) ≤ 100` gives `1 − s ≤ 0.25`. Section 4's default applies. Share access and convenience, and keep power earned in play per character so a veteran's fresh alt stays inside the band.
</details>

---

## Week 13: Meta-game and patch cycles

52. *Week 13 · compute.* A meta settles from `D₀ = 9` to `D_s = 3` with `τ = 4` days. The team patches every 12 days.
   (a) What is the average diversity over a cycle?
   (b) What share of each cycle is spent settled?
   (c) On which day after each patch should the team first judge it from pick data?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 4.90. (b) 23%. (c) Day 8.

(a) `T/τ = 3`, so `D̄ = 3 + 6 × (1/3) × (1 − e^(−3)) = 3 + 2 × 0.950 = 4.90`.

(b) Settled from `τ ln 10 = 9.2` days, so `(12 − 9.2)/12 = 23%`.

(c) `2τ = 8` days. The team can judge each patch four days before the next one ships.
</details>

53. *Week 13 · compute.* A dashboard shows `N_eff = 7.2` on day 1 after a patch and 4.1 on day 8. The settled value is `D_s = 3`.
   (a) Estimate `τ`.
   (b) On which day has 90% of the gap closed?
   (c) With `D₀ = 9`, what average diversity does a 14-day cadence give?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 5.2 days. (b) Day 12. (c) 5.09.

(a) `τ = (8 − 1) / ln((7.2 − 3)/(4.1 − 3)) = 7 / ln(3.82) = 7 / 1.340 = 5.22`.

(b) `τ ln 10 = 12.0` days.

(c) `T/τ = 2.68`. `D̄ = 3 + 6 × (5.22/14) × (1 − e^(−2.68)) = 3 + 6 × 0.373 × 0.931 = 5.09`.
</details>

54. *Week 13 · code.* This fits `τ` by least squares, as in section 3, to the in-class data. What does it print? Which value would you report, and why do the other two differ?

```python
import math

def fit_tau(days, diversity, ds):
    pts = [(t, math.log(d - ds)) for t, d in zip(days, diversity) if d > ds]
    mx = sum(t for t, _ in pts) / len(pts)
    my = sum(y for _, y in pts) / len(pts)
    slope = (sum((t - mx) * (y - my) for t, y in pts)
             / sum((t - mx) ** 2 for t, _ in pts))
    return -1 / slope

days = [0, 2, 5, 9, 14, 21, 28]
n_eff = [10.0, 8.4, 6.7, 5.4, 4.6, 4.2, 4.1]
print(round(fit_tau(days[:5], n_eff[:5], 4.0), 2))
print(round(fit_tau(days, n_eff, 4.0), 2))
print(round(fit_tau(days[:5], n_eff[:5], 4.3), 2))
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
6.07
6.63
4.79
```

Report about 6 days, from days 0 to 14 with `D_s = 4`. Adding days 21 and 28 gives 6.63 because the tail points sit only 0.1 to 0.2 above `D_s`, where a small error in `D_s` bends `ln(D − D_s)` a lot. Raising `D_s` to 4.3 shortens the fit to 4.79, because every remaining gap shrinks most at the late days and the line steepens. Section 3's first caution: fix `D_s` before you trust `τ`.
</details>

55. *Week 13 · design.* Two games have the same `D₀` and `D_s`. Game A settles with `τ = 9` days and patches every 18 days. Game B settles with `τ = 4.5` days. What cadence gives game B the same average diversity as game A, and how many more patches a year is that?

<details>
<summary>Answer and worked solution</summary>

**Answer.** Every 9 days, which is about 20 more patches a year (40.6 against 20.3).

`D̄` depends only on `T/τ`. Game A has `T/τ = 2`, so game B needs `T = 2 × 4.5 = 9` days. That is `365/9 = 40.6` patches a year against `365/18 = 20.3`. A faster-settling community demands twice the patches for the same average diversity, which section 2 predicts as information tools improve.
</details>

---

## Week 14: Measuring balance with win rates and pick rates

56. *Week 14 · compute.* In a game with a per-player rating, a player spends 40% of their ranked games on a champion with advantage `δ = +50`.
   (a) What win rate do they show on it against equal-rated opponents?
   (b) How far above their skill does their rating sit?
   (c) An analyst reads the win rate as if `f = 0` and converts it back to `δ`. What do they get?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 54.3%. (b) 20 points. (c) 30 points, an underestimate by the factor `1 − f`.

(a) `E((1 − f) δ) = E(30) = 1 / (1 + 10^(−0.075)) = 0.543`.

(b) `f × δ = 0.4 × 50 = 20`.

(c) `400 × log₁₀(0.543 / 0.457) = 30`. Step 3 of section 4 says to divide the win-rate excess by `(1 − f)`, which recovers `30 / 0.6 = 50`.
</details>

57. *Week 14 · compute.* A per-spec ladder (`f = 1`, `σ = 200`) has 30,000 players. A spec with `δ = +40` holds 8% of them.
   (a) What is its representation ratio in the top 5%?
   (b) How many of its players would you expect in the top 5% if it were balanced, and how many with `δ = +40`?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) 1.48. (b) 120 if balanced, about 178 with the advantage.

(a) `z_0.05 = 1.645`. The shift is `40 / 200 = 0.2` standard deviations, so the top share is `1 − Φ(1.445) = 7.42%`. `7.42 / 5 = 1.48`.

(b) `30,000 × 0.08 × 0.05 = 120`. With the shift, `30,000 × 0.08 × 0.0742 = 178`. The spread of the balanced count is about `√120 ≈ 11`, so 178 is far outside it.
</details>

58. *Week 14 · code.* What does this print? Which cutoff and which `f` give the strongest signal, and what does the deeper cutoff cost?

```python
from statistics import NormalDist

N = NormalDist()

def ratio(delta, f, q, sigma=200):
    z = N.inv_cdf(1 - q)
    return (1 - N.cdf(z - f * delta / sigma)) / q

for f in (0.25, 1.0):
    print(f, [round(ratio(40, f, q), 2) for q in (0.10, 0.01)])
```

<details>
<summary>Answer and worked solution</summary>

**Answer.**

```
0.25 [1.09, 1.14]
1.0 [1.4, 1.67]
```

The strongest signal is `f = 1` at the top 1%, 1.67. With `f = 0.25` the rating absorbs only a quarter of the advantage, so the shift is 10 points and the ratio barely moves. On that ladder, read the win rate instead. The top 1% magnifies more than the top 10% but holds a tenth as many players, so its count is noisier. Choose the deepest cutoff that still gives dozens of expected players.
</details>

59. *Week 14 · compute.* After a patch, a spec on a per-spec ladder wins 57% of its players' first ten games, over 2,500 games in total.
   (a) Estimate `δ`.
   (b) Put a 95% interval on the win rate, and convert both ends to `δ`.
   (c) Is the true `δ` more likely above or below your estimate?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) About 49 points. (b) 55% to 59%, so `δ` between about 35 and 63. (c) Above.

(a) `δ = 400 × log₁₀(0.57 / 0.43) = 49.0`.

(b) `±1.96 × sqrt(0.25 / 2,500) = ±0.0196`. `400 log₁₀(0.55/0.45) = 34.9` and `400 log₁₀(0.59/0.41) = 63.2`.

(c) Above. Ratings absorb about 3.5% of the gap per game at `K = 24`, so even the first ten games show a partly absorbed signal.
</details>

60. *Week 14 · compute.* A game with a ban phase has 10 champions. One champion is picked in 18% of games and banned in 40%. What is its available pick rate, and how does it compare with a fair share?

<details>
<summary>Answer and worked solution</summary>

**Answer.** 30%, three times the fair share of 10%.

Available pick rate is `pick / (1 − ban) = 0.18 / 0.60 = 0.30`. The raw 18% hides how popular it is when it can be picked. Its presence, pick plus ban, is 58%.
</details>

---

## Week 15: Synthesis for the season design

61. *Weeks 8, 11, 13 and 14 · critique.* A producer's plan for a 12-week arena season reads as follows. Hard-reset hidden MMR each season (`α = 0`), `K = 32`. Ship a balance patch every 7 days. Judge each patch from the season-long win rate of each spec on the per-spec ladder. The meta settles with `τ ≈ 7` days, and a typical player plays 60 ranked games a season. Name three problems, each with a number from the lectures, and propose a fix for each.

<details>
<summary>Answer and worked solution</summary>

**Answer.** The reset wastes the season, the cadence outruns the measurement, and the chosen signal cannot see a strong spec.

1. **Reset.** A 2,100 player needs about 69 games in the model and 78 in the lecture's simulation to settle after a hard reset at `K = 32`, and spends 39 games more than 100 points off. With 60 games a season they never settle. The fix is to keep the hidden rating (`α = 1`) and reset a visible star track with a bonus tied to hidden rating, or compress lightly and raise K for the first games.
2. **Cadence.** With `τ = 7` days, `2τ = 14` days, so every weekly patch ships before its predecessor is readable. Weekly patching gives `D̄ = 9.06` against 7.46 for a two-week cadence, at twice the patch count. The fix is to patch every 14 days and keep hotfixes for outliers visible in two days of data.
3. **Signal.** On a per-spec ladder `f = 1`, so a spec's season win rate converges to 50% whatever its `δ`. A +60 spec is 2.14 times over-represented in the top 1% with a 50% win rate. The fix is to judge from the early-window win rate and the change in top-slice representation.
</details>

62. *Weeks 2, 4 and 6 · design.* A progression plan uses a four-rung raid ladder with `s = 13`, `u = 7` and the rule "new entry beats old top" (`o = 3`). Each season's ladder is `W = 69` wide, `g = 1%` per item level and `F = 2`.
   (a) Compute the creep per tier and the shelf life. Compare `c` with Midnight's seam.
   (b) Move to `o = 1`. Recompute `c` and `t*`, and the old top's landing spot and patch-day gap.
   (c) What catch-up rule would you pair with the `o = 1` design, and why?

<details>
<summary>Answer and worked solution</summary>

**Answer.** (a) `c = 46`, `t* = 1.51` tiers, the same `c` as Midnight Season 1 to 2. (b) `c = 20`, `t* = 3.48`, landing at `x₁ = 0.71`, patch-day gap 1.63. (c) A rolling cap on the upgrade currency, or a cap removal late in the season.

(a) `c = 3 × 13 + 7 = 46`. `t* = ln 2 / (46 × ln 1.01) = 0.693 / 0.458 = 1.51`.

(b) `c = 13 + 7 = 20`, `t* = 0.693 / 0.199 = 3.48`. `x₁ = 1 − 20/69 = 0.71`, and the old top survives `floor(69/20) = 3` seasons. The patch-day gap is `1.01^(69 − 20) = 1.01^49 = 1.63`.

(c) Lower creep keeps gear alive but opens a large patch-day gap between veterans and anyone who missed a season. A rolling cap lets late or returning players close their currency gap at their own speed (`w* = v j / (v − L)`), and a late-season cap removal lets them finish before the next seam. Accept the free lateness window it creates, or keep one weekly-only source.
</details>
