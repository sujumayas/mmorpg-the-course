# MMO308 · Exam bank: quiz, practice and viva questions

MMO308 has no written exam. The grade comes from the analytics labs (40%, see [analytics-labs-brief.md](analytics-labs-brief.md)), the A/B report (20%, see [ab-report-brief.md](ab-report-brief.md)) and the live-ops plan with its analysis report (40%, see [live-ops-plan-brief.md](live-ops-plan-brief.md)). This bank has three other jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab will go quickly.
- **Lab quizzes.** Each lab session opens with a 10-minute ungraded quiz of two or three questions from this bank. Usually one applies a lecture model to new numbers or traces a piece of code, and one asks you to explain or critique.
- **Viva.** The lab spot checks, the A/B report viva and the week 15 live-ops plan viva ask questions in this style, rewritten with your own data, your own parameters and your own code.

Every question is tagged with the week it draws on and one type.

- **compute**: apply a lecture model (layer cake, KPI tree, cohort table, funnel race, design effect, SRM, mix and rate, event lift, staged rollout, survey weights, poll threshold, CUSUM, revert-first, sunset forecast) to values you have not seen.
- **code**: predict what a piece of Python prints, or find the bug in it.
- **explain**: say why something behaves as it does, with a number as evidence.
- **design**: choose a unit, a rule or a setting for a stated situation and justify it.
- **critique**: find what is wrong with a report, a plan or a piece of code, and fix it.

All numbers are invented unless a question names a game. Every real-game fact used here comes from the lecture of the tagged week, which cites its source and era. Every code snippet runs as shown with Python 3.13 (`.venv/bin/python`), and every number was recomputed in Python from the lectures' own models. Simulated numbers are marked as such and carry the seed and run count, so yours may differ by the stated margin. Write your answer before you open the solution.

Week 15 has no lecture. Its viva draws on all fourteen weeks below.

---

## Week 1: What live ops is

Lecture: [w01](../lectures/w01-what-live-ops-is.md).

1. *Week 1 · compute.* A game launches with 120,000 installs, then gets 8,000 installs every week. Its weekly retention follows the two-type curve with `w = 0.20`, `qs = 0.94` and `qt = 0.25`. Compute the expected lifetime `L`, the plateau WAU, and the plateau as a share of launch-week WAU.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `L = 4.40` weeks, plateau 35,200 WAU, which is 29% of launch week.

`L = w / (1 − qs) + (1 − w) / (1 − qt) = 0.20 / 0.06 + 0.80 / 0.75 = 3.333 + 1.067 = 4.40`. The plateau is `I × L = 8,000 × 4.40 = 35,200`. Launch-week WAU is the launch cohort alone, 120,000, so the shelf sits at `35,200 / 120,000 = 29%` of it. Launch size does not appear in `I × L`. It only sets the starting height and the length of the cliff.
</details>

2. *Week 1 · code.* This is the lecture's layer-cake code with a launch of 300,000 instead of 200,000. Predict the three lines it prints, roughly, before you run it. Then explain why a bigger launch makes the week-12 figure look worse as a share of launch week.

```python
def R(a, w=0.30, qs=0.90, qt=0.30):
    return w * qs**a + (1 - w) * qt**a

installs = [300_000] + [10_000] * 52
for t in (4, 12, 26):
    launch = installs[0] * R(t)
    total = sum(installs[s] * R(t - s) for s in range(t + 1))
    print(f"week {t:2d}: WAU {total:7,.0f}  launch share {launch / total:4.0%}  vs launch week {total / installs[0]:4.0%}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** It prints

```
week  4: WAU  80,986  launch share  75%  vs launch week  27%
week 12: WAU  56,946  launch share  45%  vs launch week  19%
week 26: WAU  43,877  launch share  13%  vs launch week  15%
```

The launch layer is 1.5 times the lecture's (week 12: `300,000 × R(12) = 300,000 × 0.0847 ≈ 25,420`, against 16,946), and the later layers are unchanged (31,527). A producer reading the last column sees an 81% drop by week 12, worse than the lecture's 76%, for a game with identical retention and identical ongoing installs. The denominator grew and the shelf did not. Both launches settle on the same 40,000 plateau. Judge the drop against the model's prediction for your own launch size, not against a fixed percentage.
</details>

3. *Week 1 · compute.* For the lecture's reference game (`I = 10,000`, `w = 0.30`, `qs = 0.90`, `qt = 0.30`), a studio can afford one of three things: (a) marketing that raises weekly installs by 25%, (b) onboarding that raises `w` to 0.38, (c) an endgame update that raises `qs` to 0.93. Rank them by plateau WAU, and say which one keeps working after its budget stops.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (c) 52,857, then (a) 50,000, then (b) 46,857. The endgame update (c) and the onboarding change (b) keep working once built. Marketing (a) stops when the money stops.

(a) `L` stays 4.00, so plateau `12,500 × 4 = 50,000`. (b) `L = 0.38 / 0.10 + 0.62 / 0.70 = 3.800 + 0.886 = 4.686`, plateau 46,857. (c) `L = 0.30 / 0.07 + 0.70 / 0.70 = 4.286 + 1 = 5.286`, plateau 52,857. The `qs` lever is strong because `w / (1 − qs)` grows fast as `qs` approaches 1. Going from 0.90 to 0.93 cuts stayer churn from 10% to 7% a week, almost a third of it.
</details>

4. *Week 1 · compute.* A one-off free weekend in week 20 brings an extra 40,000 installs to the reference game, with the same retention curve as everyone else. How much does it add to WAU in week 21 and in week 40? What does it do to the plateau?

<details>
<summary>Answer and worked solution</summary>

**Answer:** +19,200 in week 21, about +1,459 in week 40, and nothing to the plateau.

Week 21 is age 1: `40,000 × R(1) = 40,000 × 0.48 = 19,200`. Week 40 is age 20: `R(20) = 0.3 × 0.9^20 + 0.7 × 0.3^20 = 0.3 × 0.1216 + (almost 0) = 0.0365`, so `40,000 × 0.0365 ≈ 1,459`. The plateau is `I × L` with the steady inflow `I`, so a one-off layer only adds a bump that wears away at the stayers' rate. If the weekend also brought friends who installed later, that would show as a higher `I`, which is a different claim you would have to measure.
</details>

## Week 2: KPIs: DAU, MAU, stickiness, ARPDAU

Lecture: [w02](../lectures/w02-kpis-dau-mau-stickiness-arpdau.md).

5. *Week 2 · compute.* In a 30-day month, 800,000 regulars each play on 35% of days and 400,000 tourists each play 2 days. Compute MAU, mean DAU, stickiness, player-days, and the tourist share of MAU and of player-days. How many tourists in total would push stickiness below 0.25?

<details>
<summary>Answer and worked solution</summary>

**Answer:** MAU 1,200,000; mean DAU 306,667; stickiness 0.256; player-days 9,200,000; tourists are 33.3% of MAU and 8.7% of player-days. Stickiness falls below 0.25 above about 436,000 tourists.

Player-days `= 800,000 × 0.35 × 30 + 400,000 × 2 = 8,400,000 + 800,000 = 9,200,000`. Mean DAU `= 9,200,000 / 30 = 306,667`. Stickiness `= 306,667 / 1,200,000 = 0.256`. Tourist share of play `= 800,000 / 9,200,000 = 8.7%`.

For the threshold, solve `(280,000 + T × 2 / 30) / (800,000 + T) = 0.25`. That gives `280,000 + 0.0667 T = 200,000 + 0.25 T`, so `T = 80,000 / 0.1833 ≈ 436,364`. Another 36,000 tourists, 3% more MAU, would move stickiness across a line many dashboards colour red, while regular play did not change at all.
</details>

6. *Week 2 · compute.* An MMO's month A had mean DAU 200,000, 5,000 payers per day and revenue of $60,000 per day. Month B had mean DAU 230,000, 5,290 payers per day and $60,720 per day. Fill in the KPI tree (ARPDAU, payer rate, ARPPU) for both months and write the revenue change and the ARPDAU change each as a product of factor ratios.

<details>
<summary>Answer and worked solution</summary>

**Answer:** ARPDAU $0.300 then $0.264; payer rate 2.50% then 2.30%; ARPPU $12.00 then $11.48. Revenue ratio `1.012 = 1.15 × 0.88`. ARPDAU ratio `0.88 = 0.92 × 0.957`.

ARPDAU is revenue over DAU: `60,000 / 200,000 = 0.300` and `60,720 / 230,000 = 0.264`. Payer rate is payers over DAU: `5,000 / 200,000 = 2.5%` and `5,290 / 230,000 = 2.3%`. ARPPU is revenue over payers: `60,000 / 5,000 = 12.00` and `60,720 / 5,290 = 11.48`.

DAU grew 15% and ARPDAU fell 12%, so revenue grew 1.2%, not 3%. Inside ARPDAU, the payer rate fell 8% and spend per payer fell 4.3%. The new players converted less often than the old ones, which is typical of a month with many newcomers. That points at the mix (week 7), not at a pricing problem.
</details>

7. *Week 2 · code.* This snippet computes DAU, a 7-day rolling active count and daily stickiness from a tiny log. What does it print? On which day does the rolling count drop a player, and why does stickiness jump that day?

```python
active = {  # player: the days they played (day 0 is a Monday)
    "ana": {0, 1, 2, 3, 4, 5, 6, 7, 8, 9},
    "bo": {0, 3, 6, 9},
    "cy": {2},
    "di": {5, 6},
}

def dau(day):
    return sum(day in days for days in active.values())

def rolling(day, window):
    return sum(any(day - window < d <= day for d in days) for days in active.values())

for day in (6, 8, 9):
    print(day, dau(day), rolling(day, 7), round(dau(day) / rolling(day, 7), 2))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
6 3 4 0.75
8 1 4 0.25
9 2 3 0.67
```

The window on day `t` covers days `t − 6` to `t`. On day 8 it covers days 2 to 8, which still includes cy's only day. On day 9 it covers days 3 to 9, so cy falls out and the rolling count drops from 4 to 3. Part of the jump from 0.25 to 0.67 is real (bo played on day 9), and part is the echo of cy's single visit on day 2 leaving the window exactly 7 days later. Nobody did anything new to make the denominator shrink. Annotate the day an event enters the window and the day it leaves.
</details>

8. *Week 2 · compute.* A game has 500,000 regulars who each play on half of all days, and no tourists. On day 0 a one-day event brings 200,000 tourists who never return. The dashboard shows daily stickiness as DAU divided by a 7-day rolling active count. Give the stickiness on day −1, day 0, days 1 to 6, and day 7.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 0.504 on day −1, 0.646 on day 0, 0.359 on days 1 to 6, and 0.504 again on day 7.

A regular misses all 7 days of a window with chance `0.5^7 = 0.0078`, so the rolling count of regulars is `500,000 × (1 − 0.0078) = 496,094`. DAU is 250,000 on normal days. Day −1: `250,000 / 496,094 = 0.504`. Day 0: `450,000 / 696,094 = 0.646`. Days 1 to 6: `250,000 / 696,094 = 0.359`. On day 7 the event leaves the window and the ratio returns to 0.504, a 40% "jump" with no change in behaviour. A 30-day rolling MAU would show the same step on day 30.
</details>

## Week 3: Cohorts and retention curves

Lecture: [w03](../lectures/w03-cohorts-and-retention-curves.md).

9. *Week 3 · compute.* A game's daily retention follows `R(a) = w × 0.98^a + (1 − w) × 0.25^a` for `a ≥ 1`. Normally `w = 0.30`. A patch on day 40 breaks a tutorial quest, so cohorts installed on day 40 or later have `w = 0.22`. Compute D1, D7 and D30 for a normal and a broken cohort, and the change in points and percent for each.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Checkpoint | Normal | Broken | Change |
|---|---|---|---|
| D1 | 46.9% | 41.1% | −5.8 points (−12%) |
| D7 | 26.0% | 19.1% | −6.9 points (−27%) |
| D30 | 16.4% | 12.0% | −4.4 points (−27%) |

D1 normal: `0.30 × 0.98 + 0.70 × 0.25 = 0.294 + 0.175 = 0.469`. Broken: `0.22 × 0.98 + 0.78 × 0.25 = 0.2156 + 0.195 = 0.411`. D7 uses `0.98^7 = 0.8681` and `0.25^7 = 0.00006`: `0.30 × 0.8681 = 0.2604` against `0.22 × 0.8681 = 0.1910`. D30 uses `0.98^30 = 0.5455`: 0.1636 against 0.1200. The tourist term is gone by day 7, so D7 and D30 change by the same relative amount, the ratio of the `w` values, `0.22 / 0.30 = 0.733`. D1 moves less in relative terms because it is still dominated by tourists.
</details>

10. *Week 3 · compute.* Using question 9's model with 1,500 installs a day, compute the standard error of the D7 difference between one normal cohort and one broken cohort, and how many standard errors the break is. How many standard errors is it if you pool four cohorts on each side of the patch date?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Standard error 1.52 points, a 4.6 standard-error break. Pooled over four cohorts per side, 0.76 points and 9.1 standard errors.

Variances: `0.2605 × 0.7395 / 1,500 = 0.0001284` and `0.1910 × 0.8090 / 1,500 = 0.0001030`. Their sum is `0.0002314`, whose square root is 0.0152. The difference is 6.94 points, so `6.94 / 1.52 = 4.6`. Pooling four cohorts makes each `n = 6,000`, four times as large, which halves the standard error and doubles the ratio to 9.1. The price is four more days before you can read the result.
</details>

11. *Week 3 · compute.* A login outage hits calendar day 72 only. On which install days does it appear in the D1, D7 and D30 series? Now a different change lowers D7 for every cohort installed from day 58 onward. How would the two look different on the checkpoint-by-install-day chart?

<details>
<summary>Answer and worked solution</summary>

**Answer:** The outage appears at install day 71 in D1, 65 in D7 and 42 in D30. The second change is a step at install day 58 in all three series together.

A one-day period effect on day `t` hits the cell with `c + a = t`, so in the Dn series it lands at install day `t − n`: `72 − 1 = 71`, `72 − 7 = 65`, `72 − 30 = 42`. Each series shows a single dip, at a different install day. A cohort effect from install day 58 changes every age of those cohorts, so D1, D7 and D30 all step at the same install day and stay changed. Staggered single dips mean a date. An aligned step means a cohort.
</details>

12. *Week 3 · code.* An endgame patch on calendar day 50 lowers stayers' daily survival from 0.985 to 0.96 for everyone. What does this print? From which install day does each of D1, D7 and D30 first differ from an unpatched cohort?

```python
QS, QT, W = 0.985, 0.30, 0.25
P, QS_AFTER = 50, 0.96          # endgame patch on calendar day 50

def R(c, a):
    if a == 0:
        return 1.0
    after = max(0, min(a, c + a - P))   # days of this cohort's life after the patch
    return W * QS**(a - after) * QS_AFTER**after + (1 - W) * QT**a

for c in (10, 20, 45):
    print(c, [f"{100 * R(c, a):.1f}" for a in (1, 7, 30)])
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
10 ['47.1', '22.5', '15.9']
20 ['47.1', '22.5', '15.9']
45 ['47.1', '21.4', '8.4']
```

Dn for cohort `c` is measured on calendar day `c + n`, and the patch affects days after 50. Cohort 20 reaches age 30 on day 50 itself, so `after = 0` and its D30 is unchanged. D30 first differs for cohort 21, D7 for cohort 44 and D1 for cohort 50. Cohort 45 shows it in D7 (day 52, two patched days) and much more in D30 (day 75, 25 patched days). That staggered bend, D30 first and D1 last, is the signature of a lasting period effect. An onboarding break would move all three at the same install day.
</details>

## Week 4: Funnels and churn

Lecture: [w04](../lectures/w04-funnels-and-churn.md).

13. *Week 4 · compute.* Players on a story chapter progress with daily chance `q = 0.12` and quit for good with daily chance `h = 0.03`. What is the eventual step conversion, how many days does a step take to resolve on average, and what share of starters eventually finish six chapters? A designer shortens each chapter so that `q = 0.16` with the same `h`. Recompute the six-chapter share.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `c = 0.80`, 6.7 days per step, 26.2% finish six chapters. With `q = 0.16`, `c = 0.842` and 35.7% finish.

`c = q / (q + h) = 0.12 / 0.15 = 0.80`. A step resolves after `1 / (q + h) = 1 / 0.15 = 6.7` days on average. Six chapters keep `0.8^6 = 0.262`. With `q = 0.16`, `c = 0.16 / 0.19 = 0.842` and `0.842^6 = 0.357`. The daily hazard did not change. Only the pace did, and a third more players reach chapter 6. The cost is less content per chapter.
</details>

14. *Week 4 · compute.* An onboarding funnel has step conversions 85%, 55%, 90%, 80% and 95%. Your team can afford one of: +5 points at step 2, +8 points at step 4, or +6 points at step 1. Which gives the highest end-to-end conversion?

<details>
<summary>Answer and worked solution</summary>

**Answer:** +8 points at step 4 (35.2%) beats +5 at step 2 (34.9%) and +6 at step 1 (34.2%). The base is 32.0%.

End-to-end is the product: `0.85 × 0.55 × 0.9 × 0.8 × 0.95 = 0.3198`. A change moves the end by its relative size at that step. Step 2: `0.60 / 0.55 = +9.1%`, giving 34.9%. Step 4: `0.88 / 0.80 = +10.0%`, giving 35.2%. Step 1: `0.91 / 0.85 = +7.1%`, giving 34.2%. The weakest step is not the winner here because the offers are different sizes. Compare relative gains, then divide by cost.
</details>

15. *Week 4 · compute.* Each day a still-playing player returns with chance `a`, and after each session quits for good with chance `h = 0.05`. For players with `a = 0.25`, what share of those labelled churned by a 10-day inactivity window are still playing? By a 21-day window? For occasional players with `a = 0.15` and a 21-day window?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 51.7% at 10 days and 4.3% at 21 days for `a = 0.25`. 38.5% at 21 days for `a = 0.15`.

Still playing after `W` quiet days is `(1 − h)(1 − a)^W`. For `a = 0.25`, `W = 10`: `0.95 × 0.75^10 = 0.95 × 0.0563 = 0.0535`, so the false-churn share is `0.0535 / (0.0535 + 0.05) = 0.517`. For `W = 21`: `0.95 × 0.75^21 = 0.00226`, share `0.00226 / 0.05226 = 0.043`. For `a = 0.15`, `W = 21`: `0.95 × 0.85^21 = 0.0313`, share `0.0313 / 0.0813 = 0.385`. One window cannot suit both cadences. Pick the window per segment.
</details>

16. *Week 4 · compute.* A studio had 3.0 million monthly players in March and 2.6 million in April. In April, 250,000 played for the first time and 150,000 returned after a long break. How many players churned in April, and what was the churn rate? What would a chart of the stock alone have told the team?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 800,000 churned, a churn rate of 26.7% of March's players.

`end = start + new + returning − churned`, so `2.6 = 3.0 + 0.25 + 0.15 − churned`, and churned is 0.8 million. The rate is `0.8 / 3.0 = 26.7%`. The stock chart shows a net drop of 400,000, half the gross churn. It hides that the game still attracts 400,000 new and returning players a month and cannot keep them. That calls for work on retention (`qs` in week 1's terms), not on acquisition.
</details>

17. *Week 4 · code.* This steps one install cohort through a three-step funnel day by day, as the lecture's interactive does. What do the two lines print? Explain the gap between them.

```python
def funnel(q, h, days, steps=3):
    act = [0.0] * (steps + 1)    # still playing, with k steps done
    gone = [0.0] * (steps + 1)   # quit, with k steps done
    act[0] = 1.0
    for _ in range(days):
        new = [0.0] * (steps + 1)
        for k in range(steps + 1):
            if k < steps:
                new[k + 1] += q * act[k]
                new[k] += (1 - q - h) * act[k]
            else:
                new[k] += (1 - h) * act[k]
            gone[k] += h * act[k]
        act = new
    return [round(sum(act[j] + gone[j] for j in range(k, steps + 1)), 3) for k in range(steps + 1)]

print(funnel(0.2, 0.05, 3))
print(funnel(0.2, 0.05, 200))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
[1.0, 0.463, 0.1, 0.008]
[1.0, 0.8, 0.64, 0.512]
```

The second line is the eventual funnel, `c^k` with `c = 0.2 / 0.25 = 0.8`. The first is the same cohort at age 3 days. Step 3 needs three progress days in a row, `0.2^3 = 0.008`. Step 1 is one minus the share still sitting at step 0 or quit there: `0.75^3 = 0.422` still at step 0 and `0.05 × (1 + 0.75 + 0.5625) = 0.116` quit there, so `1 − 0.538 = 0.463`. At age 3 the snapshot shows step 3 ÷ step 2 as 8%, against a true 80%. Nothing is wrong with step 3. The cohort is three days old.
</details>

## Week 5: A/B testing: design

Lecture: [w05](../lectures/w05-ab-testing-design.md).

18. *Week 5 · compute.* A test randomizes 15 servers per arm of 4,000 players each. The primary metric is D7 retention with a 25% baseline, and its intraclass correlation across servers is `ρ = 0.004`. Compute the design effect, the effective sample per arm, the ceiling on `n_eff` for 15 servers, and the MDE at 80% power.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `deff = 17.0`, `n_eff ≈ 3,530` per arm, ceiling 3,750, MDE about 2.9 points.

`deff = 1 + (m − 1)ρ = 1 + 3,999 × 0.004 = 16.996`. `n = 15 × 4,000 = 60,000`, so `n_eff = 60,000 / 16.996 = 3,530`. The ceiling is `k / ρ = 15 / 0.004 = 3,750`, and the test is already at 94% of it, so bigger servers would add almost nothing. `MDE = 2.80 × sqrt(2 × 0.25 × 0.75 / 3,530) = 2.80 × 0.01031 = 0.0289`, about 2.9 points. With 60,000 independent players it would be 0.7 points.
</details>

19. *Week 5 · compute.* For the design in question 18, how many servers per arm (at 4,000 players each) do you need to detect a 2-point change in D7? Your game has 40 servers. What do you tell the producer?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 32 servers per arm, 64 in all. The game has 40, so a server-level test cannot detect 2 points.

The effective sample needed is `2 × 0.25 × 0.75 × (2.80 / 0.02)² = 0.375 × 19,600 = 7,350`. Each server contributes `4,000 / 16.996 = 235.3` effective players, so `k = 7,350 / 235.3 = 31.2`, rounded up to 32. With 20 per arm, the MDE is about 2.5 points. Tell the producer to accept a 2.5-point MDE, or find a smaller unit that contains the interference (a guild or a party), or use a whole-game switchback if the change must apply to shared systems.
</details>

20. *Week 5 · compute.* A crafting change raises the share of triggered players who craft from 5% to 6%. Only 25% of assigned players ever open the crafting station. Using MA102's sample-size formula, how many triggered players per arm do you need, and how many assigned? If you analyse all assigned players instead (effect diluted to 0.25 points), how many per arm? With 4,000 new players a day, how long is the triggered test from launch to readout, if the metric is "crafted within 3 days"?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 8,156 triggered per arm (32,621 assigned). Untriggered analysis needs about 122,122 per arm, 3.7 times as many. The triggered test takes 24 days to readout.

`n = (1.96 + 0.8416)² × (0.05 × 0.95 + 0.06 × 0.94) / 0.01² = 7.849 × 0.1039 / 0.0001 ≈ 8,156`. At a 25% trigger rate that is `8,156 / 0.25 = 32,621` assigned. Diluted to 5% against 5.25%: `7.849 × (0.0475 + 0.04974) / 0.00000625 ≈ 122,122`. The rule of thumb predicts about `1/f = 4`. Here it is 3.7, because the diluted rates sit slightly lower.

Duration: 4,000 new players a day, 25% trigger, 1,000 triggered a day, 500 per arm. `8,156 / 500 = 16.3` days of assignment, rounded up to 21 (three whole weeks), plus 3 days for the last cohort's window.
</details>

21. *Week 5 · compute.* Last month, per-server D7 retention across 40 servers had an overall rate of 30%. After removing binomial noise, the between-server variance of the server rates was `σ_b² = 0.0006`. Estimate `ρ`. With 5,000 players per server, what is the design effect?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `ρ ≈ 0.0028` and `deff ≈ 15.2`.

`ρ = σ_b² / (σ_b² + p(1 − p)) = 0.0006 / (0.0006 + 0.21) = 0.00285`. `deff = 1 + 4,999 × 0.00285 = 15.2`. A server-level test on 100,000 players per arm has the precision of about 6,600 independent players. A standard deviation of `sqrt(0.0006) = 2.4` points between server means looks small on a dashboard, and it still costs 93% of the sample.
</details>

22. *Week 5 · code.* A team's assignment code hashes the player id with no experiment name. Two experiments run at once, and later one is ramped from 10% to 30%. What do the two lines print (approximately)? What is wrong with the first result and what is right about the second?

```python
import hashlib
from collections import Counter

def bucket(unit_id):
    digest = hashlib.sha256(str(unit_id).encode()).digest()
    return int.from_bytes(digest[:8], "big") / 2**64

def variant(unit_id, share_b=0.5):
    return "B" if bucket(unit_id) < share_b else "A"

both = Counter((variant(pid), variant(pid)) for pid in range(10_000))
print(sorted(both.items()))
ramp = Counter((variant(pid, 0.1), variant(pid, 0.3)) for pid in range(10_000))
print(sorted(ramp.items()))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** It prints

```
[(('A', 'A'), 4942), (('B', 'B'), 5058)]
[(('A', 'A'), 6939), (('A', 'B'), 2043), (('B', 'B'), 1018)]
```

The first line has only two cells. Without a salt, both experiments compute the same bucket, so every player in B of one is in B of the other and the two effects can never be separated. Add the experiment name to the hashed string, and each of the four cells should hold about 2,500.

The second line is correct behaviour. At 10% about 1,000 players are in B. At 30% those same 1,018 are still in B, plus 2,043 new ones, and no player moved from B to A. Ramping by raising the share, not by changing the salt, keeps players in the arm they already saw.
</details>

## Week 6: A/B testing: statistics and pitfalls

Lecture: [w06](../lectures/w06-ab-testing-statistics-and-pitfalls.md). Questions on sequential boundaries here are conceptual or simulation-based. Do not memorize published boundary constants for this course.

23. *Week 6 · compute.* A test planned 50/50 reports 40,300 players in A and 39,700 in B. Run the SRM check. Do the same for 40,120 against 39,880, and for a ramped 80/20 test with 79,450 in A and 20,550 in B.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `chi² = 4.5`, `p = 0.034` for the first. `chi² = 0.72`, `p = 0.40` for the second. `chi² = 18.9`, `p ≈ 0.00001` for the third.

First: `E = 40,000` each, `chi² = 300² / 40,000 × 2 = 4.5`, `p = erfc(sqrt(2.25)) = 0.034`. Second: `120² / 40,000 × 2 = 0.72`, `p = 0.40`, ordinary noise. Third: `E = 80,000` and `20,000`, `chi² = 550² / 80,000 + 550² / 20,000 = 3.78 + 15.13 = 18.9`. The third is a clear mismatch. A is 550 players short of its planned 80,000, and B has 550 too many. The first sits in a grey zone. An automated check that alerts at `p < 0.001`, as many platforms use, would pass it, so look at the daily split before trusting the result.
</details>

24. *Week 6 · code.* A teammate wrote this peeking simulation and reports that 10 looks give "only 5.5%, so peeking is fine". Find the bug, say why it gives roughly 5%, and say what a correct version should give.

```python
import math
import random

def false_positive_rate(looks, sims=20_000, bound=1.96, seed=6):
    rng = random.Random(seed)
    hits = 0
    for _ in range(sims):
        total = 0.0
        for k in range(1, looks + 1):
            total += rng.gauss(0, 1)
            if abs(total / k) > bound:
                hits += 1
                break
    return hits / sims

print(f"{false_positive_rate(10):.1%}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** It prints `5.5%`. The z-statistic must be `total / math.sqrt(k)`, not `total / k`. The correct simulation gives about 19% for 10 looks.

`S_k` is a sum of `k` standard normals, so its standard deviation is `sqrt(k)`. Dividing by `k` makes `z_k` shrink like `1 / sqrt(k)`, so after the first look it almost never reaches 1.96. The simulation then measures little more than the first look's 5%. With the fix, the lecture's table gives 19.3% for 10 looks. Test a simulation on a case you know first: with `looks = 1` both versions give 5%, and only a case with more looks exposes the bug.
</details>

25. *Week 6 · code.* Adapt the lecture's `false_positive_rate` to 3 looks with 100,000 simulations. What rate should you get, and how far from it may your run land? Explain in one sentence why 3 looks already costs more than half of the rate that 5 looks cost.

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 10.7% (seed 6, 200,000 runs gave 10.68%). A run of 100,000 should land within about ±0.2 points of the long-run value.

The margin is `1.96 × sqrt(0.107 × 0.893 / 100,000) = 0.0019`. The looks are equally spaced, so the first extra look (at one third of the data) is the least correlated with the final one and adds the most new chance to cross. Later looks share more data with their neighbours and add less each, which is why the rate climbs fast at first (5% to 8.3% to 10.7%) and then slowly (14.2% at 5 looks, 22% at 14).
</details>

26. *Week 6 · code.* Change the code so every look uses the same stricter boundary `b` instead of 1.96, with 10 looks. A 200,000-run simulation (seed 6) gives 5.8% at `b = 2.5` and 2.6% at `b = 2.8`. What does that tell you about the constant boundary that gives exactly 5%, and how would you find it? What does a constant boundary cost compared with one final look?

<details>
<summary>Answer and worked solution</summary>

**Answer:** The 5% boundary for 10 equal looks lies between 2.5 and 2.8, a little above 2.5. Find it by bisection on `b`, with enough runs that the rate's margin (about ±0.1 points at 200,000 runs) is smaller than the gap you are closing.

Every look with a boundary above 1.96 is less sensitive than a single final test at 1.96. With a real effect sized for 80% power at the end, a constant raised boundary loses power unless you raise the maximum sample. The lecture's power table shows the trade for five looks. What you buy is the right to stop early when the effect is large, with the false-positive rate still at 5%.
</details>

27. *Week 6 · compute.* Each arm of a store test has 12,000 players. A earns $30,000 and B earns $33,600. The top spender in B spent $5,000. Compute revenue per player for both arms, then for B with that player removed, and for B with each player's spend capped at $600.

<details>
<summary>Answer and worked solution</summary>

**Answer:** A $2.50, B $2.80 (+12%). Without the top spender B is $2.38. With a $600 cap B is $2.43.

`30,000 / 12,000 = 2.50` and `33,600 / 12,000 = 2.80`. Removing one player: `28,600 / 11,999 = 2.38`, below A. Capping: `(33,600 − 5,000 + 600) / 12,000 = 29,200 / 12,000 = 2.43`, still below A. One person, assigned by the hash, created the whole lift. Report conversion and spend per payer separately, cap at a percentile fixed in the plan, and size the test from the metric's past variance.
</details>

28. *Week 6 · explain.* A 14-day A/A test is watched daily and crosses 1.96 on day 4. By day 14 its z is 0.6. The producer says "it was significant once, so there must be something there". Using the lecture's simulation results, explain what happened, and name two things wrong with shipping B on day 4 even if B were truly better.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Under no effect, 22% of 14-look tests cross 1.96 at some look, and only 23% of those crossings are still past it at the last look. A crossing that drifts back is the common case.

Even with a real effect, stopping at the first crossing has two costs. The false-positive rate of the procedure is about 22%, not 5%, so the team ships many changes that do nothing. And a test stopped when noise happened to push in the winning direction overstates the effect size, so the lift will shrink after launch. The planned single analysis on day 14 (`z = 0.6`) is the only result that carries its stated error rate.
</details>

## Week 7: Segmentation

Lecture: [w07](../lectures/w07-segmentation.md).

29. *Week 7 · compute.* D7 retention of new accounts by acquisition source:

| Segment | Week 0 accounts | Week 0 D7 | Week 1 accounts | Week 1 D7 |
|---|---|---|---|---|
| Organic | 12,000 | 35% | 12,000 | 34% |
| Paid ads | 3,000 | 20% | 18,000 | 21% |

Compute the overall rate in both weeks, and decompose the change into mix and rate effects with both orderings and the midpoint. What should the note to the producer say?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Overall 32.0% then 26.2%, a change of −5.8 points. Old-rate ordering: mix −6.0, rate +0.2. New-rate ordering: mix −5.2, rate −0.6. Midpoint: mix −5.6, rate −0.2 points.

Shares move from 0.8 / 0.2 to 0.4 / 0.6. Old rates: mix `= (0.4 − 0.8) × 0.35 + (0.6 − 0.2) × 0.20 = −0.14 + 0.08 = −0.060`; rate `= 0.4 × (−0.01) + 0.6 × 0.01 = +0.002`. New rates: mix `= −0.4 × 0.34 + 0.4 × 0.21 = −0.052`; rate `= 0.8 × (−0.01) + 0.2 × 0.01 = −0.006`.

Here the two orderings disagree on the sign of the rate effect, which is exactly when the lecture says to report the midpoint and name it. The note: almost all of the drop is the shift toward paid-ad players, organic retention slipped by a point (which is inside the noise of a week-to-week difference for 12,000 players, about ±1.2 points), and paid-ad players did not get worse.
</details>

30. *Week 7 · compute.* A region-and-platform cell has 400 new players and D7 of 30%. What is its 95% margin of error? How many players does the cell need before a 3-point week-to-week change is larger than the margin of the difference between two such weeks?

<details>
<summary>Answer and worked solution</summary>

**Answer:** ±4.5 points at 400. About 1,800 players per week.

`1.96 × sqrt(0.3 × 0.7 / 400) = 1.96 × 0.0229 = 0.045`. For the difference of two independent weeks, the margin is `1.96 × sqrt(2 × 0.21 / n)`. Setting it equal to 0.03 gives `n = 2 × 0.21 × (1.96 / 0.03)² = 1,793`. With 400 players per week the cell cannot support a 3-point claim, so merge it with a neighbour or report it monthly.
</details>

31. *Week 7 · code.* A teammate's decomposition does not add up. What does it print, and what is the bug?

```python
before = {"organic": (12_000, 0.35), "paid": (3_000, 0.20)}
after = {"organic": (12_000, 0.34), "paid": (18_000, 0.21)}

def shares(groups):
    total = sum(n for n, _ in groups.values())
    return {s: (n / total, m) for s, (n, m) in groups.items()}

def decompose(before, after):
    b, a = shares(before), shares(after)
    mix = sum((a[s][0] - b[s][0]) * b[s][1] for s in b)
    rate = sum(b[s][0] * (a[s][1] - b[s][1]) for s in b)
    return mix, rate

total = sum(w * m for w, m in shares(after).values()) - sum(w * m for w, m in shares(before).values())
mix, rate = decompose(before, after)
print(f"total {total:+.3f}  mix {mix:+.3f}  rate {rate:+.3f}  mix + rate {mix + rate:+.3f}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** It prints `total -0.058  mix -0.060  rate -0.006  mix + rate -0.066`.

The mix term uses the old rates, so the rate term must use the new shares, `a[s][0]`, to make the cross terms cancel. This code weights the rate term by the old shares. That pairs the two halves of different orderings and double-counts the interaction, `Σ (w1 − w0)(m1 − m0) = −0.4 × (−0.01) + 0.4 × 0.01 = +0.008`, which is the gap between −0.066 and −0.058. The lab's test that "mix plus rate equals the total" catches this bug in one line.
</details>

32. *Week 7 · compute.* A flat A/B test is read across 12 pre-registered segments at a 5% false-positive rate each. What is the chance that at least one segment shows a "significant" win if the change does nothing? What if the team had pre-registered only 6 segments?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 46% with 12 segments, 26% with 6.

`1 − 0.95^12 = 1 − 0.540 = 0.460` and `1 − 0.95^6 = 1 − 0.735 = 0.265`. Treating the segments as independent is a simplification, since segments of one test share a control period, but the order of magnitude is right. A winning segment from a flat test is a hypothesis for the next test, with that segment as its pre-registered population.
</details>

33. *Week 7 · critique.* A report says "players who joined a guild in their first week had D7 of 58%, players who did not had 22%, so the new guild finder more than doubles retention". Name the flaw, and describe a comparison that would measure the guild finder's effect.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The segment is defined by behaviour after the change, so it mixes the feature's effect with who chose to use it.

Players who were already going to stay have the time and interest to join guilds in week one, so the 36-point gap is mostly selection. Segment on attributes fixed before the change (install date, platform, account type), or randomize the guild finder by player or by party with a hashed assignment, and compare D7 by assigned arm, including players who never opened it. If only some players can meet the finder, trigger on an event that happens the same way in both arms, such as reaching the level where it unlocks.
</details>

## Week 8: Event design and calendars

Lecture: [w08](../lectures/w08-event-design-and-calendars.md).

34. *Week 8 · compute.* A game averages 15,000 player-hours per day. It announces a 5-day event 10 days ahead. Players dip 12% while waiting, the event runs at +80%, and play dips 20% for 7 days afterwards. Compute gross lift, borrowed play, net lift and the incrementality ratio. An analyst uses the average of the 7 days before the event as the baseline. What gross lift does the report show, and by how much does it overstate the true gross?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Gross 60,000; borrowed 39,000; net 21,000; ratio 0.35. The lazy report shows 69,000, 15% too high.

Gross `= 15,000 × 0.80 × 5 = 60,000`. Borrowed `= 15,000 × (0.12 × 10 + 0.20 × 7) = 15,000 × 2.6 = 39,000`. Net `= 21,000`, ratio `21,000 / 60,000 = 0.35`. The week before the event is inside the pre-dip, so its average is `15,000 × 0.88 = 13,200`. Against it each event day shows `27,000 − 13,200 = 13,800`, and five days give 69,000. The report also ignores the hangover, so compared with the net lift it overstates by more than three times.
</details>

35. *Week 8 · compute.* Events of one kind recover their appeal as `L(g) = 0.50 × (1 − e^(−g/25))`, where `g` is the gap in days since the last one. Each event lasts 7 days. Compare spacings of 21, 35 and 70 days by lift per event, gross lift-days per year, and cost per lift-day relative to the 70-day spacing.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| Gap | Lift per event | Lift-days per year | Relative cost per lift-day |
|---|---|---|---|
| 21 days | 28.4% | 34.6 | 1.65 |
| 35 days | 37.7% | 27.5 | 1.25 |
| 70 days | 47.0% | 17.1 | 1.00 |

`L(21) = 0.5 × (1 − e^−0.84) = 0.5 × 0.568 = 0.284`. Lift-days per year `= 365 / 21 × 0.284 × 7 = 34.6`. Relative cost is `L(70) / L(g)`: `0.470 / 0.284 = 1.65`. Three-week events buy twice the yearly gross lift of ten-week events, at 65% more production cost per unit, and before any extra pre-dip from players learning the pattern.
</details>

36. *Week 8 · code.* What does this print? Explain what the peak and the final value each mean for an event report.

```python
B = 12_000
actual = [B * 0.92] * 7 + [B * 1.70] * 5 + [B * 0.85] * 10
lift = [a - B for a in actual]

running, path = 0.0, []
for x in lift:
    running += x
    path.append(running)
print(f"peak {max(path):,.0f} on day {path.index(max(path))}, final {path[-1]:,.0f}")
print(f"ratio {path[-1] / sum(x for x in lift if x > 0):.2f}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
peak 35,280 on day 11, final 17,280
ratio 0.41
```

The pre-dip costs `7 × 960 = 6,720`. The event adds `5 × 8,400 = 42,000`, so the cumulative lift peaks at 35,280 on the last event day (index 11, since the list starts at 0). The hangover costs `10 × 1,800 = 18,000`, and the line settles at 17,280. The peak is neither gross nor net. It already has the pre-dip subtracted and not the hangover. The final value is the net lift, and the ratio `17,280 / 42,000 = 0.41` is the incrementality ratio. The measurement window must run until the line stops moving.
</details>

## Week 9: Patch management and hotfixes

Lecture: [w09](../lectures/w09-patch-management-and-hotfixes.md).

37. *Week 9 · compute.* A patch goes to `N = 300,000` players. A bug hits one player in 3,000. Compute the expected number of players hit under a big bang and under a two-stage plan of 2% then 100%, with perfect detection. Then redo the staged plan with `d = 0.25`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Big bang 100. Staged 15.3 at `d = 1` and 61.4 at `d = 0.25`.

The canary exposes 6,000 players, of whom `6,000 / 3,000 = 2` are expected to be hit. It stays clean with probability `(1 − 1/3,000)^6,000 ≈ e^−2 = 0.135`. Stage 2 exposes 294,000, so it adds `0.135 × 98 = 13.3`. Total 15.3. With `d = 0.25`, the chance a canary player is hit and detected is `1 / 12,000`, and the canary stays clean with `e^−0.5 = 0.607`, so stage 2 adds `0.607 × 98 = 59.4`. Total 61.4. Poor detection gives back most of what staging saved. A middle stage (say 2% → 20% → 100%) or better crash reporting would help.
</details>

38. *Week 9 · compute.* How large a canary do you need to catch a one-in-8,000 bug with 95% probability at `d = 1`? At `d = 0.4`? On a 150,000-player game, which is realistic?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 23,965 players at `d = 1` and about 59,914 at `d = 0.4`. The second is 40% of the game, which is not a canary.

`n = ln(0.05) / ln(1 − q)`. At `q = 1/8,000`, `n = 2.996 / 0.000125 = 23,965`, close to the rule of three `3 × 8,000 = 24,000`. At `q = 0.4 / 8,000 = 1/20,000`, `n ≈ 59,914`. Raise detection (automatic crash and error reports per build) before you enlarge the canary.
</details>

39. *Week 9 · compute.* A bug costs 120 player-hours per hour. The next scheduled patch is 48 hours away. A hotfix needs a 20-minute restart with 24,000 players online and carries an 8% chance of a problem costing 15,000 player-hours. Hotfix or wait? What is the break-even harm rate, and what is it if hotfixes needed no restart?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Wait (5,760 against 9,200). Break-even 192 player-hours per hour with the restart, 25 without it.

Wait cost `= 120 × 48 = 5,760`. Hotfix cost `= D + r × H = 24,000 × 20 / 60 + 0.08 × 15,000 = 8,000 + 1,200 = 9,200`. Break-even `= 9,200 / 48 = 191.7`. Without a restart, `D = 0` and the hotfix costs 1,200, break-even `1,200 / 48 = 25`, so this bug would be worth fixing today. Investing in restart-free hotfixes changes the decision for every bug between 25 and 192 player-hours per hour.
</details>

40. *Week 9 · code.* What does this print? Which plan would you choose, and what does the model leave out that might change your mind?

```python
def expected_harm(N, p, d, stages):
    q = p * d
    total, prev, reach = 0.0, 0.0, 1.0
    for f in stages:
        newly_exposed = N * (f - prev)
        total += reach * newly_exposed * p
        reach *= (1 - q) ** newly_exposed
        prev = f
    return total

for plan in ([1.0], [0.005, 0.05, 1.0], [0.02, 0.2, 1.0]):
    print(plan, round(expected_harm(50_000, 1 / 500, 0.5, plan), 1))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
[1.0] 100.0
[0.005, 0.05, 1.0] 11.8
[0.02, 0.2, 1.0] 8.6
```

For a common bug (one in 500), a larger canary is better: the 2% canary (1,000 players) catches it often enough that the rollout rarely reaches the last stage. The 0.5% canary exposes only 250 players, and with `d = 0.5` it stays clean with chance `(1 − 0.001)^250 = 0.78`, so the bug usually escapes to stage 2. The model leaves out time. Both plans have the same number of stages, but a slow bug needs soak time longer than the bug takes to show, and it assumes a halt helps no one already hit. For a rarer bug the ranking can flip, so check the plan across a range of `p` before adopting it.
</details>

## Week 10: Player feedback loops: forums, surveys, polls

Lecture: [w10](../lectures/w10-player-feedback-loops-forums-surveys-polls.md).

41. *Week 10 · compute.* An MMO has 7,000 light players (3 hours a week, 40% approve of a change), 2,500 mid players (10 hours, 55%) and 500 heavy players (30 hours, 85%). An in-game survey asks players who are online at random moments. What approval does it report, and what is the truth? What average weekly hours does the survey think its players have?

<details>
<summary>Answer and worked solution</summary>

**Answer:** The survey reports 57.2%. The truth is 46.0%. Respondents average 12.5 hours against a real 6.1.

Online time is `21,000 + 25,000 + 15,000 = 61,000` hours, so respondent shares are 34.4%, 41.0% and 24.6%. Raw approval `= 0.344 × 0.40 + 0.410 × 0.55 + 0.246 × 0.85 = 0.572`. Truth `= 0.70 × 0.40 + 0.25 × 0.55 + 0.05 × 0.85 = 0.46`. The survey and the players disagree on the majority. Mean hours of respondents is `Σ n h² / Σ n h = 763,000 / 61,000 = 12.5`. Check with the identity: variance `= 76.3 − 6.1² = 39.09`, and `6.1 + 39.09 / 6.1 = 12.5`.
</details>

42. *Week 10 · compute.* In question 41, 1,200 players answer in proportion to online time. Weight each by `1 / h`. Compute the weighted approval and Kish's effective sample size. How wide is a 95% interval with `n_eff` compared with one that uses `n`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Weighted approval 46.0%. `n_eff ≈ 757`. The honest interval is about ±3.6 points, against ±2.8 with `n`.

Respondents are about 413, 492 and 295. Segment weight totals `413 / 3 = 137.7`, `492 / 10 = 49.2`, `295 / 30 = 9.8`, total 196.7, which is 70%, 25% and 5%, the real mix. Weighted approval equals the truth, 46.0%. `Σ w² = 413 / 9 + 492 / 100 + 295 / 900 = 45.9 + 4.9 + 0.3 = 51.1`, so `n_eff = 196.7² / 51.1 = 757`. Interval: `1.96 × sqrt(0.46 × 0.54 / 757) = 0.0355`, against `1.96 × sqrt(0.46 × 0.54 / 1,200) = 0.0282`.
</details>

43. *Week 10 · code.* What does this print? Explain the first number in terms of which respondents carry the information.

```python
def kish_neff(weights):
    return sum(weights) ** 2 / sum(w * w for w in weights)

hours = [2] * 300 + [10] * 500 + [40] * 400
print(round(kish_neff([1 / h for h in hours])))
print(round(kish_neff([1.0] * 1200)))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** It prints `550` and `1200`.

`Σ w = 300 / 2 + 500 / 10 + 400 / 40 = 150 + 50 + 10 = 210`. `Σ w² = 300 / 4 + 500 / 100 + 400 / 1,600 = 75 + 5 + 0.25 = 80.25`. `n_eff = 210² / 80.25 = 549.5`. The 300 two-hour players carry most of the weight, because they were the hardest to reach. Each forty-hour player counts one twentieth as much as a two-hour player, so all 400 of them together weigh the same as 20 light players. Equal weights leave `n_eff = n`. The lesson for trigger design is that a random-account survey of 600 can carry more information than this online-now survey of 1,200.
</details>

44. *Week 10 · compute.* 180 distinct accounts posted in a bug thread, 450 filed in-game reports, and 36 did both. Estimate the number of affected players with Lincoln-Petersen and with Chapman's correction. What share of affected players said nothing? Would you expect the truth to be higher or lower?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Lincoln-Petersen 2,250, Chapman about 2,205. Only 594 players spoke up, so about 74% said nothing. The truth is probably higher.

`180 × 450 / 36 = 2,250`. Chapman: `181 × 451 / 37 − 1 = 2,205`. Distinct reporters: `180 + 450 − 36 = 594`, so `1 − 594 / 2,250 = 74%` are silent. Engaged players tend to use both channels, which inflates the overlap and pulls the estimate down, so treat 2,250 as a floor. Count stuck accounts from quest-state telemetry if the bug leaves a trace.
</details>

## Week 11: Community-voted design: Old School RuneScape polls

Lecture: [w11](../lectures/w11-community-voted-design-old-school-runescape-polls.md).

45. *Week 11 · compute.* A poll question gets 45,000 "Yes", 17,500 "No" and 3,000 skips. What is the yes share? Does it pass at 70%, and how many "No" votes would block it? Does it pass at 75%, and if not, how many voters would have to switch from "No" to "Yes"? What happens if skips count as "No"?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 72.0%. Passes at 70%, and 19,286 "No" votes (1,786 more) would block it. Fails at 75%, and 1,875 switchers would pass it. Counting skips as "No" gives 68.7%, which fails at 70%.

`45,000 / 62,500 = 0.72`. At 70% the question passes while `N ≤ 45,000 × 0.3 / 0.7 = 19,285.7`, so the 19,286th "No" blocks it. At 75% it needs `Y ≥ 0.75 × 62,500 = 46,875`, so 1,875 must switch. With skips as "No", `45,000 / 65,500 = 0.687`. The same ballot passes or fails depending on a denominator rule most voters never read.
</details>

46. *Week 11 · compute.* A game with 250,000 eligible players expects 7% turnout. Compare the smallest group of eligible players that can block any question at thresholds of 60% and 80%, as a share and as a head count. What turnout would a 75% threshold need for the blocking group to reach 3% of eligible players?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 2.8% (7,000 players) at 60%, and 1.4% (3,500 players) at 80%. A 75% rule needs 12% turnout.

Blocking share `= τ × (1 − T)`: `0.07 × 0.40 = 0.028` and `0.07 × 0.20 = 0.014`, times 250,000. For 3% at `T = 0.75`, `τ = 0.03 / 0.25 = 0.12`. Raising the threshold halves the number of people who can veto content, which concentrates power rather than spreading it. Raising turnout is the other lever.
</details>

47. *Week 11 · code.* A teammate stores thresholds as whole percentages. What does this print, and why is the first line wrong? Rewrite the rule so it cannot fail this way.

```python
def passes(yes, no, threshold_percent):
    t = threshold_percent * 0.01
    return yes / (yes + no) >= t

print(passes(7_000, 3_000, 70))
print(passes(7_500, 2_500, 75))
print(passes(2_000, 1_000, 66.7))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:** It prints `False`, `True`, `False`. The first should be `True`, since 7,000 of 10,000 is exactly 70%.

`70 * 0.01` is `0.7000000000000001` in binary floating point, slightly above `7,000 / 10,000`, which rounds to the nearest double of 0.7. The 75% case works only because 0.75 is exact in binary. The third line is correct (66.7% is above two thirds), but it shows how a threshold written as a rounded decimal differs from the intended fraction. Use integers: `100 * yes >= threshold_percent * (yes + no)`, or `Fraction`, as the lecture's code does. A poll that sits exactly on the line must not be decided by rounding.
</details>

48. *Week 11 · design.* Your studio wants players to choose one of three new zones to build next, and separately to decide whether to change how the premium currency works. Which voting rule suits each question, and why? Use the Minecraft Mob Vote and the OSRS threshold from the lecture.

<details>
<summary>Answer and worked solution</summary>

**Answer:** A plurality vote for the zone choice, and a supermajority yes/no question (with skip allowed and results hidden) for the currency change, or no poll at all if prices are business-controlled.

Choosing among options where one will certainly be built is what plurality settles, as Mojang's Mob Vote did. There is no status-quo option and no blocking group. Changing an existing system that players have invested in is a "should we change anything?" question, which a threshold like OSRS's 70% protects against a bare majority. The OSRS Polling Charter keeps membership and bond prices off the ballot, a reason to exclude the currency question if it touches pricing. State the blocking group `τ × (1 − T)` next to the threshold so the team sees how few players can stop the change.
</details>

## Week 12: Economy monitoring

Lecture: [w12](../lectures/w12-economy-monitoring.md).

49. *Week 12 · compute.* A faucet's standardized residuals for nine days are 0.9, −0.3, 1.4, 1.1, 0.2, 1.6, 0.8, 1.3 and 1.2. Run an upward CUSUM with `k = 0.5` and `h = 4` from `S = 0`. On which day does it fire? Would the spike rule `z > 3` have fired?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `S` = 0.4, 0, 0.9, 1.5, 1.2, 2.3, 2.6, 3.4, 4.1. It fires on day 9. The spike rule never fires.

Each day `S = max(0, S + z − 0.5)`. Day 2: `0.4 − 0.3 − 0.5 = −0.4`, clipped to 0. Day 9: `3.4 + 1.2 − 0.5 = 4.1 > 4`. The largest single `z` is 1.6. This is a leak of about 1σ, which a one-day rule would take weeks to see.
</details>

50. *Week 12 · compute.* An economy team runs upward CUSUM with `k = 0.5` on 25 daily series. At `h = 5` the in-control average run length is about 930 days, and at `h = 6` about 2,500. How many false alarms per year does each give? The same team also runs spike rules at `z > 3` on 60 series. How many false alarms do those add?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 9.8 a year at `h = 5` and 3.7 at `h = 6`. The spike rules add about 30 a year.

`25 × 365 / 930 = 9.8` and `25 × 365 / 2,500 = 3.7`. A spike rule on a normal series fires with chance 0.00135 a day, once every 741 days, so `60 × 365 / 741 = 29.6`. The spike rules are the bigger problem. Move most of them to tickets rather than pages, and keep paging only for the reconciliation residual and item-count series. Raising `h` to 6 costs about two days of detection delay for a 1σ leak (about 12 days instead of 10).
</details>

51. *Week 12 · compute.* A double-gold event is planned for a weekend with the note "mob-loot faucet × 1.5". The Saturday baseline is 38 million gold and `σ = 1.2` million. During the event, Saturday reads 61.0 million. Compute `z` against the raw baseline and against the planned baseline. Should the alarm page someone?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Against the raw baseline `z = 19.2`, a meaningless alarm. Against the planned baseline of 57.0, `z = 3.3`, which is worth a page.

Raw: `(61.0 − 38) / 1.2 = 19.2`. Planned: `38 × 1.5 = 57.0`, and `(61.0 − 57.0) / 1.2 = 3.33`. The event pays more than planned, about 7% over plan. That could be a stacking bug between the event multiplier and another bonus. Multiplying the baseline by the plan turns the alarm into a check of the plan.
</details>

52. *Week 12 · compute.* Seven clean days of a faucet read 10.2, 9.8, 10.1, 10.4, 9.9, 10.0 and 17.5 million (the last day had an unlogged incident). Estimate `σ` from the sample standard deviation and from the median absolute deviation. Which should the alarm use, and what does the other one do to detection?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Standard deviation 2.82 million. MAD-based `σ ≈ 1.4826 × 0.2 = 0.30` million. Use the robust value.

Median 10.1. Absolute deviations 0.1, 0.3, 0.0, 0.3, 0.2, 0.1, 7.4, whose median is 0.2. The single bad day inflates the standard deviation about nine times. With `σ = 2.82`, a 1-million leak would be a 0.35σ shift, below the allowance `k = 0.5`, so CUSUM would never see it. With `σ = 0.30` it is a 3.3σ shift, caught in a day or two.
</details>

53. *Week 12 · code.* This runs the mirror CUSUM on a sink series. What does it print, and on which day does it alarm? Would a downward spike rule at `z < −3`, or "alarm if today is 10% below baseline", have fired?

```python
BASE, SIGMA, K, H = 20.0, 0.4, 0.5, 4.0
observed = [20.1, 19.7, 20.3, 19.5, 19.6, 19.4, 19.7, 19.3, 19.5]   # sink, millions of gold

s = 0.0
for day, x in enumerate(observed, start=1):
    z = (x - BASE) / SIGMA
    s = max(0.0, s - z - K)          # mirror CUSUM: evidence of a fall
    print(day, f"{z:+.2f}", f"{s:.2f}", "ALARM" if s > H else "")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
1 +0.25 0.00 
2 -0.75 0.25 
3 +0.75 0.00 
4 -1.25 0.75 
5 -1.00 1.25 
6 -1.50 2.25 
7 -0.75 2.50 
8 -1.75 3.75 
9 -1.25 4.50 ALARM
```

The sink started charging less around day 4 (about 1.2σ, or 0.5 million a day). Neither alternative fires. The lowest `z` is −1.75, far from −3, and the lowest day is 3.5% below baseline, not 10%. A sink that silently stops charging is a fall in the sink series, which is why the lecture runs the mirror score on sinks. Reading the path backwards to the last zero (day 3) dates the start of the problem.
</details>

## Week 13: Incident response

Lecture: [w13](../lectures/w13-incident-response.md).

54. *Week 13 · compute.* A team has diagnosis rounds of `r = 20` minutes that each find the cause with `p = 0.2`, a fix that takes `F = 30` minutes to ship, and a revert that takes `R = 10` minutes. The on-call engineer believes `q = 0.25` that the last deploy is to blame. Compute both expected outages and `q*`. What `R` would make the two strategies equal at `q = 0.3`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Fix forward 130 minutes, revert first 107.5 minutes, `q* = 0.077`. At `q = 0.3`, `R = 39` minutes makes them equal.

`E[fix] = r / p + F = 100 + 30 = 130`. `E[revert] = 10 + 0.75 × 130 = 107.5`. `q* = R / E[fix] = 10 / 130 = 0.077`, so any belief above about 8% favours reverting. Equal at `q = 0.3` when `R = q × 130 = 39`. A 10-minute revert gives a lot of room. If reverting needed a 45-minute restart, this team should fix forward at `q = 0.3`.
</details>

55. *Week 13 · code.* Using the lecture's parameters, what does this print? Why does the fix-forward column not change between minutes 75 and 95?

```python
import math

r, p, F, R, q = 30, 0.25, 45, 20, 0.6

def ff(t):
    if t < F + r:
        return 1.0
    return (1 - p) ** math.floor((t - F) / r)

def still_down(t, first):
    if first == "fix":
        return ff(t)
    return 1.0 if t < R else (1 - q) * ff(t - R)

for t in (74, 75, 95, 180):
    print(t, round(still_down(t, "fix"), 3), round(still_down(t, "revert"), 3))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
74 1.0 0.4
75 0.75 0.4
95 0.75 0.3
180 0.316 0.169
```

The earliest a fix-forward team can be back is minute `r + F = 75`: one round to find the cause and 45 minutes to ship. At minute 75 the chance of still being down drops to `1 − p = 0.75`, and it stays there until minute 105, when a success in round 2 could first ship. The step function only moves every `r` minutes. The revert column drops to `1 − q = 0.4` at minute 20 and then follows the fix-forward staircase shifted by 20 minutes, so at minute 95 it takes its first step to `0.4 × 0.75 = 0.3`. At minute 180, `floor(135 / 30) = 4` failed rounds give `0.75^4 = 0.316`, and the revert column is `0.4 × 0.75^3 = 0.169`.
</details>

56. *Week 13 · compute.* An incident's gap between the scaled baseline and today's concurrent players, sampled every 30 minutes from the incident start, is 5,000, 18,000, 22,000, 21,000, 9,000, then −3,000 and −1,500. Compute the gross loss, the rebound and the net loss in player-hours. What does a small rebound predict?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Gross 37,500 player-hours, rebound 2,250, net 35,250.

Gross `= (5,000 + 18,000 + 22,000 + 21,000 + 9,000) × 0.5 = 75,000 × 0.5 = 37,500`. Rebound `= (3,000 + 1,500) × 0.5 = 2,250`. Net `= 35,250`. The rebound recovered 6% of the loss, so most affected players did not come back that evening. A missing rebound is the number that predicts churn. Check next week's retention of players who tried to log in during the outage against those who did not, and target any compensation at the first group.
</details>

57. *Week 13 · critique.* A postmortem's action items are "be more careful with migrations", "add a runbook for login failures after a patch", "put the new auction feature behind a kill switch" and "canary patches to one realm for an hour". Map each to the model parameter it moves, or say it moves none. Rank the three useful ones by what you would measure to prove they worked.

<details>
<summary>Answer and worked solution</summary>

**Answer:** "Be more careful" moves nothing and is not an action item. The runbook moves `r` down and `p` up. The kill switch moves `R` down (and makes `q` specific to one feature). The realm canary lowers `N` for the next bad patch.

To prove each worked, measure the parameter it targets in the next incidents. For the kill switch, time from page to mitigation when the flag is flipped (minutes, against the old revert time). For the runbook, rounds to diagnosis on login incidents. For the canary, players affected per bad patch. Rank by expected player-hours saved per engineer-day, using the lecture's model with your team's `r`, `p`, `F` and `R`. A kill switch often ranks first because `q*` is `R / (r/p + F)` and a small `R` makes reverting pay at almost any belief.
</details>

## Week 14: Sunsetting content and servers

Lecture: [w14](../lectures/w14-sunsetting-content-and-servers.md).

58. *Week 14 · compute.* A game had 120,000 MAU at the start of its decline and 84,000 six months later. Fit a single rate through those two points. What is its half-life? With revenue of $3 per MAU per month and a maintenance cost of $45,000 a month, when does the game stop paying, and when must you announce with nine months' notice?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `λ = 0.0594` per month, half-life 11.7 months. Break-even 15,000 MAU at month 35.0. Announce by month 26.0.

`λ = −ln(84,000 / 120,000) / 6 = −ln(0.7) / 6 = 0.3567 / 6 = 0.0594`. Half-life `= ln 2 / 0.0594 = 11.7` months. Break-even MAU `= 45,000 / 3 = 15,000`. Crossing `= ln(120,000 / 15,000) / 0.0594 = ln 8 / 0.0594 = 35.0`. Announce at `35.0 − 9 = 26.0`. Watch the six-month ratio. If it rises above 0.70 in the next periods, a slower core exists and this date is too early.
</details>

59. *Week 14 · code.* What does this print? By how many months does a cost cut from $45,000 to $36,000 delay the crossing under a single rate, and why would the delay be longer if the game had a slow core?

```python
import math

M0, a, notice = 120_000, 3.0, 9
lam = -math.log(84_000 / M0) / 6          # one rate from month 0 and month 6

def single(t):
    return M0 * math.exp(-lam * t)

def crossing(model, cost):
    k = 0
    while a * model(k / 10) > cost:
        k += 1
    return k / 10

for cost in (45_000, 36_000):
    t = crossing(single, cost)
    print(f"cost {cost:,}: crossing month {t}, announce by month {t - notice:.1f}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
cost 45,000: crossing month 35.0, announce by month 26.0
cost 36,000: crossing month 38.8, announce by month 29.8
```

A 20% cost cut buys `ln(45 / 36) / 0.0594 = 0.223 / 0.0594 = 3.8` months under a single rate. Under a single exponential every cut of the same proportion buys the same number of months. A mixture's curve flattens as the fast leavers go, so near the crossing it falls more slowly than the single rate. Lowering the cost line then moves the crossing much further along the time axis. The lecture's example moved from month 46.8 to 57.6 for a smaller cut, against 28.3 to 31.3 for the single rate.
</details>

60. *Week 14 · compute.* A game's MAU follows `M(t) = 100,000 × (0.4 × 2^(−t/40) + 0.6 × 2^(−t/4))`. Compute MAU at months 0, 4, 8 and 12 by hand, and the three four-month ratios. What would the ratios be under a single rate fitted through months 0 and 4?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 100,000; 67,321; 49,822; 39,990. Ratios 0.673, 0.740, 0.803. A single rate would give 0.673 every time.

Month 4: core `40,000 × 2^(−0.1) = 40,000 × 0.933 = 37,321`, casual `60,000 × 0.5 = 30,000`, total 67,321. Month 8: `40,000 × 2^(−0.2) = 34,822` plus 15,000, total 49,822. Month 12: `32,490 + 7,500 = 39,990`. Ratios `67,321 / 100,000`, `49,822 / 67,321` and `39,990 / 49,822`. Under a single rate the ratio is `e^(−4λ)`, constant. Two rises in a row are the evidence the lecture asks for before trusting a mixture fit.
</details>

61. *Week 14 · compute.* An activity has 2% of play hours and 8% of maintenance cost. Compute its hours-to-cost ratio and compare it with an activity at 25% of hours and 12% of cost. Before retiring the first, name the three checks the lecture requires and the data each one needs.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 0.25 against 2.08. The first buys an eighth as much play per unit of cost.

`2 / 8 = 0.25` and `25 / 12 = 2.08`. The checks: who plays it (hours by segment, including new players and small communities, since 2% may be all of one group), what was bought (purchase records linking the activity to paid content, the problem Destiny 2's vault raised), and what leaves the economy (the ledger's faucets and sinks tagged by activity, to find items that become impossible to earn or spend).
</details>
