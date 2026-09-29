# MMO306 · Exam bank: practice, lab quizzes and viva questions

MMO306 has no written exam. The grade comes from the encounter designs portfolio (40%, see [encounter-designs-brief.md](encounter-designs-brief.md)) and the final dungeon (60%, see [final-dungeon-brief.md](final-dungeon-brief.md)). This bank has three other jobs.

- **Practice.** Work a week's questions before its lab is due. If you can answer them with the lecture closed, the lab goes quickly.
- **Lab quizzes.** Each lab session from week 2 opens with a 10-minute ungraded quiz of two questions from this bank. Usually one applies a lecture model to new numbers, and one asks you to explain or critique.
- **Viva.** The portfolio spot checks and the week 15 dungeon review ask questions in this style, rewritten with the numbers from your own bosses, zone and roadmap.

Every question is tagged with the week or weeks it draws on and one type.

- **compute**: apply a lecture model to values you have not seen before.
- **code**: say what a short piece of Python prints, using the lecture's own functions.
- **explain**: say why a result comes out as it does, with a number as evidence.
- **design**: choose a value or a rule for a stated goal and justify it.
- **critique**: find what is wrong with a claim or a proposal and say how to fix it.

All numbers are invented unless a question names a game. Game facts come from the lecture of the tagged week, which cites its source and version. Every code snippet runs as shown with Python 3.13 (`.venv/bin/python`), and every number in the answers was recomputed in Python from the lecture's models. Write your own answer before you open the solution.

---

## Week 1: The content treadmill

1. *Week 1 · compute.* A drop holds `C = 16` content hours with replay `r = 5`, and the cadence is `P = 140` days. Three players play 5, 12 and 30 hours a week.
   (a) Give `T`, `L` and the drought in days for each player.
   (b) The team adds a gate of `g = 10` useful hours a week. Recompute all three rows.
   (c) By what factor does the gap between the 30-hour and the 5-hour player's `L` shrink?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 5 h: 112.0 days, `L = 1.25`, 28.0 days of drought. 12 h: 46.7 days, `L = 3.00`, 93.3 days. 30 h: 18.7 days, `L = 7.50`, 121.3 days. (b) 5 h unchanged. 12 h and 30 h both become 56.0 days, `L = 2.50`, 84.0 days of drought. (c) From 6× to 2×, a factor of 3.

`T = 7 × C × r / min(h, g)`, so `7 × 16 × 5 = 560` hour-days of content. The 5-hour player gets `560 / 5 = 112` days and `L = 140 / 112 = 1.25`. The 12-hour player gets `560 / 12 = 46.7` days. The 30-hour player gets `560 / 30 = 18.7` days.

With the gate, `min(5, 10) = 5`, so the first row does not move. Both heavier players now progress at 10 hours a week, `560 / 10 = 56` days. The gap in `L` was `7.5 / 1.25 = 6` and is now `2.5 / 1.25 = 2`. The gate touched only the players above it, which is the week 1 lesson.
</details>

2. *Week 1 · design.* Same drop as question 1. The team wants the p99 player, who plays 40 hours a week, at `L ≤ 2`. What gate does that need? Which of question 1's three players does that gate also bind, and what is the hidden cost?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `g = 8` hours a week. It binds the 12-hour and the 30-hour player as well. The cost is that everyone above 8 hours a week runs out on the same day, day 70.

`L = 2` means `T = 140 / 2 = 70` days. So `560 / g = 70`, and `g = 8`. Any player above 8 hours is capped at 8, so the 12-hour player's `T` rises from 46.7 to 70 days and the 30-hour player's from 18.7 to 70. The 5-hour player is still below the gate.

The lecture called this compression. Every player above the gate hits the drought together on day 70, which shows up as a cliff in the share of players who still have something to do. A gate this low also binds a large part of the population, which players feel as "the game won't let me play."
</details>

3. *Week 1 · critique.* A producer writes: "If we double `C`, we halve the drought for everyone." Test the claim on design B from the lecture (`C = 20`, `r = 6`, `P = 175`) for the p50 player (6 hours a week) and the p99.9 player (60 hours a week).

<details>
<summary>Answer and worked solution</summary>

**Answer:** Doubling `C` halves every `L`, but not every drought. The p50 player's drought falls from 35 days to 0. The p99.9 player's falls from 161 to 147 days, only 9%.

p50: `T = 7 × 20 × 6 / 6 = 140` days, drought `175 − 140 = 35`. With `C = 40`, `T = 280`, which outlasts the cycle, so the drought is 0. `L` goes from 1.25 to 0.625.

p99.9: `T = 840 / 60 = 14` days, drought 161. With `C = 40`, `T = 28`, drought 147. `L` goes from 12.5 to 6.25.

The claim confuses the ratio with the days. More content moves every `T` by the same factor, so a player whose `T` was short gains few days. The heavy player needs a gate or a high-replay repeatable, not volume. And doubling `C` doubles the production cost, the most expensive lever there is.
</details>

4. *Week 1 · code.* What does this print? Explain the second and third lines.

```python
def exhaust_days(C, r, h, gate=None):
    rate = h if gate is None else min(h, gate)
    return 7 * C * r / rate

P = 120
for h in (4, 8, 20):
    T = exhaust_days(12, 5, h, gate=8)
    print(h, round(T, 1), round(P / T, 2))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
4 105.0 1.14
8 52.5 2.29
20 52.5 2.29
```

`7 × 12 × 5 = 420`. The 4-hour player is under the gate, so `T = 420 / 4 = 105` days and `L = 120 / 105 = 1.14`. The 8-hour player sits exactly on the gate, `420 / 8 = 52.5`. The 20-hour player is capped at `min(20, 8) = 8`, so they get the same 52.5 days and the same `L`. Everyone at or above the gate lands on one row, which is why the lecture's design C table ends in three identical values.
</details>

5. *Week 1 · compute.* A team of 45 builds a drop in 20 weeks at 40 hours a week. The drop holds 15 content hours, and 400,000 players each play it with `r = 4`. Compute developer hours per content hour and developer hours per player hour. Then say in one sentence why hiring 45 more people would not halve `P`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 36,000 developer hours. That is 2,400 per content hour and 0.0015 per player hour.

`45 × 20 × 40 = 36,000`. Per content hour, `36,000 / 15 = 2,400`. Player hours are `400,000 × 15 × 4 = 24,000,000`, so `36,000 / 24,000,000 = 0.0015`.

By cost per hour of play the content is cheap. The problem is calendar time. Production runs in series while consumption runs in parallel, and a team twice the size does not build the same raid in half the time. That is why the lecture sends you to `r` and `g` first.
</details>

## Week 2: Quest hubs and zone pacing

6. *Week 2 · compute.* A zone takes players from level 20 to 23. XP to next level is 3,000, 3,300 and 3,600. Quests pay `q = 450` with `k = 0.1`. The zone has three hubs of 8 quests.
   (a) Give `X`, `n`, `c` and the share of each hub a solo quester sees.
   (b) Repeat for a player with `o = 0.25`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `X = 9,900`, `n = 20.0`, `c = 1.20`, hubs 100%, 100%, 50%. (b) `n = 15.0`, `c = 1.60`, hubs 100%, 87.5%, 0%.

Each quest is worth `450 × 1.1 = 495` XP. Solo, `n = 9,900 / 495 = 20`. Hubs 1 and 2 take 16 of those, and the last 4 fall in hub 3, half of it. `c = 24 / 20 = 1.2`.

With `o = 0.25`, `n = 9,900 × 0.75 / 495 = 15`. Hub 1 takes 8, hub 2 gets 7 of its 8, and hub 3 gets nothing. `c = 24 / 15 = 1.6`. Outside XP is paid for entirely out of the end of the zone.
</details>

7. *Week 2 · explain.* The solo quester from question 6 arrives fully rested, which doubles kill XP but not quest XP. How much of hub 3 do they see now? Why is the effect smaller than in the lecture's table, where rest cut `n` from 24 to 20?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 29% of hub 3 (2.3 of 8 quests), down from 50%. The effect is smaller because this zone's kill share `k` is only 0.1.

Rest doubles `k` to 0.2, so a quest is worth `450 × 1.2 = 540` XP and `n = 9,900 / 540 = 18.3`. That leaves `18.3 − 16 = 2.3` quests in hub 3.

Rest multiplies only the kill part of each quest's XP. In the lecture, `k = 0.25`, so doubling it added 100 XP to a 500 XP quest, a 20% jump. Here it adds 45 XP to 495, a 9% jump. A zone that pays mostly through quests is less exposed to rested XP. It is still exposed to dungeon XP, which question 6(b) showed.
</details>

8. *Week 2 · design.* Using question 6's zone, a designer wants the `o = 0.25` player to finish hub 3 exactly, so they lower `q` and keep `k = 0.1`. What `q` does that need? What happens to the solo quester, and what would you do instead?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `q = 281.25` XP. The solo quester then needs 32 quests from a zone of 24, so `c = 0.75` and they cannot out-level the zone on quests alone.

Finishing hub 3 means `n = 24`. `24 = 9,900 × 0.75 / (q × 1.1)` gives `q = 7,425 / 26.4 = 281.25`. For the solo quester, `n = 9,900 / (281.25 × 1.1) = 32`. The zone runs out 8 quests early, about 2,475 XP they must grind or find elsewhere.

One fixed `q` cannot give both players `c` near 1. Better options from the lecture are scaling within the zone's range, so quests keep paying until the level where the next zone begins, or moving the climax into hub 2, where both players still are.
</details>

9. *Week 2 · code.* What does this print? Then a player who needs 13.5 quests does only 80% of the quests they meet (`s = 0.8`) in the first layout. Do they finish the zone's quests before they finish levelling?

```python
def hub_seen(n_done, hubs):
    seen, left = [], n_done
    for size in hubs:
        seen.append(min(size, max(0, left)) / size)
        left -= size
    return seen

print(hub_seen(13.5, [6, 5, 5]))
print(hub_seen(13.5, [5, 5, 6]))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
[1.0, 1.0, 0.5]
[1.0, 1.0, 0.5833333333333334]
```

The skipping player runs out of quests about 0.7 of a quest short of the level.

First layout: hub 1 takes 6, hub 2 takes 5, and 2.5 of hub 3's 5 remain, half. Second layout: 5 and 5, then 3.5 of 6 is 58.3%. Putting the big hub last raises its share seen, but it also puts more authored quests where fewest players reach.

With skipping, the player walks past `13.5 / 0.8 = 16.9` quests to complete 13.5. The zone has 16. After walking all 16 they have done `16 × 0.8 = 12.8`, short of 13.5. The test is `c × s ≥ 1`. Here `c = 16 / 13.5 = 1.185` and `c × s = 0.95`, so the zone is 5% too thin for this player.
</details>

10. *Week 2 · compute.* In question 6's zone, a quest takes 5 minutes including travel. Compute XP per minute and minutes for each of the three level-ups. A designer puts the zone's climax at quest 22 in hub 3. At what minute does a solo quester leave the zone, and do they see the climax?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 99 XP a minute. Level 20 takes 30.3 minutes, level 21 takes 33.3, level 22 takes 36.4. The solo quester leaves at about minute 100, after quest 20, and misses the climax.

`495 / 5 = 99` XP a minute. `3,000 / 99 = 30.3`, `3,300 / 99 = 33.3`, `3,600 / 99 = 36.4`. The sum is 100 minutes, which is `n × 5 = 20 × 5`.

The climax at quest 22 would land at minute 110, two quests past the point where the player out-levels the zone. Move it to quest 18 or earlier, or give players a reason other than XP to finish hub 3.
</details>

## Week 3: Dungeon design, trash, bosses and loot

11. *Week 3 · compute.* One trash type has `H = 1,200` health. The group's AoE deals `A = 60` to each target, with target cap 20. Each enemy deals `d = 25` to the tank, the healer heals `Q = 180`, the tank's buffer is `B = 4,000`, the walk between pulls is `w = 12` s, and the dungeon holds `M = 90` enemies. Find the largest safe pull and the clear time at that pull. Show why one more enemy wipes.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 15 enemies, 3.2 minutes. At 16 the tank lasts 18.2 s against a 20 s kill.

Under the cap `t_kill = 1,200 / 60 = 20` s for any `N`. The pull works while `4,000 / (25N − 180) ≥ 20`, so `25N − 180 ≤ 200` and `N ≤ 15.2`. At `N = 15` the tank lasts `4,000 / 195 = 20.5` s. At 16 it lasts `4,000 / 220 = 18.2` s and dies first.

Clear time at 15 is `90 / 15 × (20 + 12) / 60 = 6 × 32 / 60 = 3.2` minutes. The healer and the tank set the pull size, as the lecture said.
</details>

12. *Week 3 · compute.* Same numbers as question 11, but the target cap is 5. Find the largest safe pull and its clear time. Is the largest safe pull also the fastest?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 10 enemies, 7.8 minutes. Yes, 10 is the fastest safe pull here.

Past the cap, `t_kill = H × N / (A × m) = 1,200 N / 300 = 4N` seconds. At `N = 10`, `t_kill = 40` s and the tank lasts `4,000 / (250 − 180) = 57.1` s, so it works. At 11, `t_kill = 44` s and the tank lasts `4,000 / 95 = 42.1` s, a wipe.

Clear times: `N = 8` gives `11.25 × 44 / 60 = 8.25` min, `N = 9` gives `10 × 48 / 60 = 8.0`, `N = 10` gives `9 × 52 / 60 = 7.8`. The walk makes bigger pulls pay even past the cap. The low cap still makes the run 2.4 times longer than question 11's 3.2 minutes.
</details>

13. *Week 3 · compute.* Take question 11 with cap 20 and scale enemy health and damage by `1.08⁶` (six keystone levels). Find the largest safe pull and the clear time, and compare the run length with question 11.

<details>
<summary>Answer and worked solution</summary>

**Answer:** The scale is 1.587. The largest safe pull is 7 and the clear time 9.4 minutes, 2.9 times question 11's 3.2 minutes.

Scaled `H = 1,904`, so `t_kill = 1,904 / 60 = 31.7` s. Scaled `d = 39.7`. At `N = 7` the tank lasts `4,000 / (277.7 − 180) = 40.9` s, enough. At 8 it lasts `4,000 / (317.4 − 180) = 29.1` s, less than 31.7, a wipe.

Clear time `90 / 7 × (31.7 + 12) / 60 = 9.4` minutes. A 59% increase in both health and damage nearly tripled the run, because the kill got longer while the tank's time got shorter, and the pull had to halve.
</details>

14. *Week 3 · compute.* A dungeon's table has 10 items a player can use, and the chest holds one item for the party, two if timed. (a) Expected runs for one specific item if the group always times the run? (b) Chance the player still lacks it after 40 timed runs, and after 40 untimed runs? (c) The designer adds a currency: 15 per run, 300 buys the item. What does that do to the worst case and to the player's week 1 `T`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 25 runs. (b) 19.5% timed, 44.6% untimed. (c) No player needs more than 20 runs, and `T` shrinks for the unlucky players.

(a) The chance per run is `i / (5m) = 2 / 50 = 0.04`, so `1 / 0.04 = 25` runs.

(b) `0.96^40 = 0.195`. Untimed, the chance per run is `1 / 50`, and `0.98^40 = 0.446`.

(c) `300 / 15 = 20` runs guarantees the item. The currency cuts the long tail of the geometric wait, so the players who would have needed 60 or 80 runs finish sooner. In week 1 terms it lowers `r` for them, and they reach the end of the drop earlier.
</details>

## Week 4: Encounter mechanics

15. *Week 4 · compute.* A boss has `H = 9,000,000` and `T = 420` s. Mechanics: every 25 s, 2.5 s of lost attacking; every 60 s, 6 s; every 90 s, 4.5 s.
    (a) What is the tax?
    (b) Group E has paper DPS 30,000 and `x = 1.2`. Give its uptime, effective DPS, kill time and hidden health.
    (c) What paper DPS does a crisp group (`x = 1.0`) need?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 0.25. (b) `u = 0.70`, 21,000 effective DPS, 428.6 s (enrage, 8.6 s late), hidden health 12,857,143. (c) 28,571.

(a) `2.5/25 + 6/60 + 4.5/90 = 0.10 + 0.10 + 0.05 = 0.25`.

(b) `u = 1 − 1.2 × 0.25 = 0.70`. `30,000 × 0.7 = 21,000`. `9,000,000 / 21,000 = 428.6` s. Hidden health `9,000,000 / 0.7 = 12,857,143`, so the mechanics are worth 3.86 million health to this group.

(c) `u = 0.75`, and `P_req = 9,000,000 / (0.75 × 420) = 28,571`. The crisp group can clear with 5% less paper DPS than group E brings, and group E still fails.
</details>

16. *Week 4 · compute.* Group C has paper DPS 26,000 and `x = 1.0`. Group D has 30,000 and `x = 1.5`. At what mechanic tax do they have the same effective DPS? Which group does a boss with tax 0.3 favour, and by how much?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Tax 0.211. At tax 0.3, group C out-damages group D by 18,200 against 16,500, about 10%.

Set `26,000 (1 − t) = 30,000 (1 − 1.5t)`. Then `26,000 − 26,000t = 30,000 − 45,000t`, so `19,000t = 4,000` and `t = 0.211`.

At 0.3, C has `26,000 × 0.7 = 18,200` and D has `30,000 × 0.55 = 16,500`. Below 0.211 the boss is a gear check that D wins. Above it, it is an execution check that C wins. The designer picks the winner by picking the tax, not the health.
</details>

17. *Week 4 · compute.* A boss has `H = 13,000,000`, `T = 420` s and tax 0.15. The group has 16 damage dealers, paper DPS 40,000 and `x = 1.0`. Using the average model with the death rule of section 3, find the kill time with no deaths, with one death at 90 s and with two deaths at 90 s. What deaths budget does this boss allow at that time?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 382.4 s, 401.8 s and 424.1 s. The budget is one death at 90 s.

`u = 0.85`, effective DPS `40,000 × 0.85 = 34,000`, and `13,000,000 / 34,000 = 382.4` s.

By 90 s the raid has dealt `34,000 × 90 = 3,060,000`, leaving 9,940,000. With one dead dealer the rate is `34,000 × 15/16 = 31,875`, so the rest takes 311.8 s and the kill lands at 401.8 s, 18 s inside the enrage. With two dead the rate is `34,000 × 14/16 = 29,750`, the rest takes 334.1 s, and the kill would land at 424.1 s, past 420.

The resolved mechanics cost seconds. Each failure costs about 20 s. The lecture's rule is to write the deaths budget into the design document and tune `H` to it.
</details>

18. *Week 4 · code.* This is the lecture's tick simulation. What do the two lines print? The average model gives 187.5 s and 214.3 s. Explain each gap.

```python
def kill_time(H, P, mechanics, x=1.0, deaths=(), limit_s=600):
    """Step through the fight in tenths of a second. Return the kill time in seconds."""
    done = 0.0
    for tick in range(limit_s * 10):          # tick 0 covers 0.0-0.1 s
        busy = any(tick >= first * 10 and (tick - first * 10) % (every * 10) < x * cost * 10
                   for first, every, cost in mechanics)
        alive = 1 - sum(share for when, share in deaths if tick >= when * 10)
        if not busy:
            done += P * alive / 10
        if done >= H:
            return (tick + 1) / 10
    return None                               # enrage reached first

boss = [(5, 15, 3)]                           # first cast at 5 s, every 15 s, costs 3 s
print(kill_time(3_000_000, 20_000, boss))
print(kill_time(3_000_000, 20_000, boss, x=1.5))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
189.0
213.0
```

The kill needs `3,000,000 / 20,000 = 150` s of attacking. The tax is `3 / 15 = 0.2`, so the average model gives `150 / 0.8 = 187.5` s at `x = 1` and `150 / 0.7 = 214.3` s at `x = 1.5`.

At `x = 1`, the windows are 5-8, 20-23, and so on. By 185 s, twelve windows (36 s) are over and the raid has attacked 149 s. The thirteenth window runs 185-188, so the last second of damage lands at 189. The kill fell just behind a window, so the fight paid a full last cycle, 1.5 s worse than the average.

At `x = 1.5`, each window is 4.5 s. By 200 s, thirteen windows (58.5 s) are over and the raid has attacked 141.5 s. The window at 200-204.5 follows, and the last 8.5 s of attacking end at 213.0, before the next window at 215. The kill landed early in an attack stretch, so it paid less than a full last cycle, and the free first 5 s helped too. That is the "partial last cycle" effect from section 3.
</details>

19. *Week 4 · critique.* A boss moves every 20 s, costing melee 3 s of attacking and ranged 0. A spread mechanic every 30 s costs everyone 1.5 s. A melee spec deals 8% more than a ranged spec on a target dummy. Compute each role's tax and effective output. The class team says melee is "8% ahead." Who is right on this boss, and what would you change in the encounter?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Melee tax 0.20, ranged tax 0.05. Melee brings `1.08 × 0.80 = 0.864` of the ranged spec's dummy damage, ranged brings 0.95. Ranged is ahead by 10% on this boss.

Melee: `3/20 + 1.5/30 = 0.15 + 0.05 = 0.20`. Ranged: `1.5/30 = 0.05`. `0.95 / 0.864 = 1.10`.

Both statements are true in their context. The class team measured a stationary dummy. The content moved the target. The lecture's point is that content and class balance must share numbers. Fixes include moving the boss less often or to a spot the melee already stand near, or adding a mechanic that ranged players pay for, such as a soak that must be taken at range. Also vary the per-role tax across the raid so no role pays on every boss.
</details>

## Week 5: Telegraphing and readability

20. *Week 5 · compute.* A 15-player raid faces a raid-wide wipe mechanic 4 times per pull. The telegraph is 1,050 ms, `μ = 700` ms, `σ = 150` ms. Give the per-player success `p`, the clean-pull chance and the expected misses per pull.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `p = 0.99018`, clean pull 55.3%, expected misses 0.59 per pull.

`z = (1,050 − 700) / 150 = 2.33`, and `Φ(2.33) = 0.99018`. There are `15 × 4 = 60` trials, and `0.99018^60 = 0.553`. Expected misses are `60 × (1 − 0.99018) = 0.59`.

As a wipe mechanic this fails almost half the pulls. As a damage debuff it would be about one cheap miss every other pull. Same telegraph, different design.
</details>

21. *Week 5 · compute.* For the raid and mechanic in question 20, what telegraph gives a 95% clean pull? How many milliseconds does that add, and what does the answer say about where 1,050 ms sat?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About 1,170 ms, 120 ms more than 1,050.

`p* = 0.95^(1/60) = 0.999145`. `z(p*) = 3.14`, so `T_tel = 700 + 150 × 3.14 = 1,170` ms.

120 ms moves the clean-pull chance from 55% to 95%. The mechanic was on the cliff the lecture described, where a small change in the telegraph sweeps the raid's success across most of its range. Far above the cliff, another 120 ms would change almost nothing.
</details>

22. *Week 5 · compute.* Use `μ_local = 620` ms and `σ = 150` ms. In the raid from question 20, 14 players have a 60 ms round trip and one has 200 ms. The telegraph is 1,150 ms, 4 casts per pull, targeting everyone. Compute the clean-pull chance, and compare it with all 15 players on 60 ms.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 90.1% with the distant player, 94.9% without. The one player costs about 5 points of clean pulls.

Fast players: `μ = 680`, `z = 470 / 150 = 3.13`, `p = 0.99914`. The slow player: `μ = 820`, `z = 330 / 150 = 2.2`, `p = 0.98610`. Clean pull `0.99914^56 × 0.98610^4 = 0.901`. All fast: `0.99914^60 = 0.949`.

The slow player makes up 4 of 60 trials but more than half of the expected failures (0.056 of 0.104 per pull). Tune for your worst-served region, and prefer mechanics judged by position over a window rather than at the snapshot.
</details>

23. *Week 5 · critique.* A designer tests a new wipe mechanic alone, 20 times, at a 1,000 ms telegraph and never fails. They write: "20 of 20, safe for our 20-player raid with 5 casts per pull." Use `μ = 700`, `σ = 150` to say what the test shows and what it hides.

<details>
<summary>Answer and worked solution</summary>

**Answer:** With `p = 0.977`, a tester goes 20 for 20 about 63% of the time, so the test cannot tell this telegraph from a safe one. The raid's clean pull is 10%.

`z = 2`, `p = 0.97725`. The chance of 20 clean solo tries is `0.97725^20 = 0.631`. The raid runs `20 × 5 = 100` trials a pull, and `0.97725^100 = 0.100`.

A solo test samples the middle of the response-time curve, and a raid lives in its tail. To estimate a 2% failure rate you need hundreds of trials or measured percentiles from many players, which is what Lab 05 uses. Then set the telegraph for the clean-pull target, not for the per-player rate.
</details>

## Week 6: Raid design and difficulty tiers

24. *Week 6 · compute.* A flexible boss has `H(20) = 6,300,000`, `T = 360` s and `u = 0.75`. The roster is 2 tanks and `floor(N / 5)` healers, and only damage dealers hit the boss.
    (a) Under the linear rule `H(N) = H(20) × N / 20`, give the per-dealer requirement at 10, 20 and 30 players.
    (b) Write the neutral rule and give `H(10)` and `H(30)`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 1,944.4, 1,666.7 and 1,590.9. The 10-player group pays 16.7% more per dealer than the 20-player group. (b) `H(N) = 450,000 × d(N)`, so `H(10) = 2,700,000` and `H(30) = 9,900,000`.

`T × u = 270`. Damage dealers are `d = 6, 14, 22`. Linear health is 3,150,000, 6,300,000 and 9,450,000. So `r(10) = 3,150,000 / (270 × 6) = 1,944.4`, `r(20) = 6,300,000 / (270 × 14) = 1,666.7`, and `r(30) = 9,450,000 / (270 × 22) = 1,590.9`.

Neutral means holding `r = 1,666.7` everywhere, so `H(N) = 1,666.7 × 270 × d(N) = 450,000 × d(N)`. At 10 players that is 2,700,000, and the linear rule's 3,150,000 is 16.7% higher. The two fixed tanks cause it.
</details>

25. *Week 6 · compute.* A wipe mechanic has per-player success `p = 0.996` and is cast 6 times per pull. Give the clean-pull chance at 10 and 30 players if it is (a) raid-wide, (b) targeted at `floor(N / 5)` players, (c) fixed at 4 targets. Which choice is neutral to group size?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 78.6% and 48.6%. (b) 95.3% and 86.6%. (c) 90.8% at both. The fixed-target version is neutral.

(a) `0.996^60 = 0.786`, `0.996^180 = 0.486`. (b) `0.996^12 = 0.953`, `0.996^36 = 0.866`. (c) `0.996^24 = 0.908` whatever `N` is.

A raid-wide wipe mechanic makes the 30-player group's clean pulls 38% lower than the 10-player group's, even with health scaling that is neutral on damage. Fixed targets fix exposure, but a small group then sees each player chosen more often, which feels like "it's always me."
</details>

26. *Week 6 · compute.* Treat Determination as a 5% additive damage bonus per wipe, up to 10 stacks. (a) How many wipes does a group at 75% of the required effective DPS need? (b) A group at 64%? (c) Compare a flat 10% buff, like the Echo. Which groups does it let through on the first pull?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 7 wipes. (b) Never. (c) Only groups at 90.9% or more. The 75% group never clears with a flat 10% alone.

(a) The group needs a factor of `1 / 0.75 = 1.333`. `1 + 0.05w ≥ 1.333` gives `w ≥ 6.7`, so 7 wipes.

(b) `1 / 0.64 = 1.5625`, above the cap of 1.5. No number of wipes is enough.

(c) A flat 10% helps everyone from the first pull, but only groups at `1 / 1.1 = 90.9%` or better clear. The stacking buff reaches down to 66.7% and asks for wipes in return. The flat buff reaches less far and asks for nothing. Each is a choice about who an old tier is for.
</details>

27. *Week 6 · critique.* A proposed ladder: Heroic is Normal with 1.3× health and nothing else changed. Mythic adds three new wipe mechanics not present on Heroic, each raid-wide, 5 casts per pull, with a 950 ms telegraph for 20 players (`μ = 700`, `σ = 150`). Name two ladder rules this breaks, and put a number on the Mythic problem.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Heroic adds no new test, only gear. Mythic introduces mechanics no lower tier teaches. And at 950 ms each new mechanic alone has a 0.75% clean pull.

`z = 250 / 150 = 1.67`, `p = 0.9522`. With 100 trials, `0.9522^100 = 0.0075`. Three of them together give about `4 × 10⁻⁷`. No group clears that on reading alone.

Fixes from section 3: give Heroic a new test, such as a higher tax through faster cycles or one wipe mechanic with a shorter telegraph. Introduce Mythic's mechanics in Heroic in a gentler form so players can practise them. Then size Mythic's telegraph with week 5's model. At 1,250 ms, `p = 0.99988` and one mechanic's clean pull is 98.8%.
</details>

## Week 7: Tuning encounters with logs

28. *Week 7 · compute.* Twelve groups' best raid DPS on a boss, in thousands: 1,450, 1,320, 1,250, 1,210, 1,180, 1,150, 1,100, 1,080, 1,040, 990, 950, 880. The enrage is 360 s. Give the kill rate at `H = 414M`, after a 5% cut and after a 10% cut. Why do the two cuts add different numbers of groups?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 50%, 58.3% and 75%.

At 414M, `R = 414,000,000 / 360 = 1,150,000`. Six groups are at or above it, 6 of 12. After 5%, `R = 1,092,500`, and the group at 1,100 joins, 7 of 12. After 10%, `R = 1,035,000`, and the groups at 1,080 and 1,040 join, 9 of 12.

The first cut's band from 1,150 down to 1,092 held one group, and the second band held two. A small sample is lumpy. The smooth model shows the shape underneath, which the next question uses.
</details>

29. *Week 7 · compute.* In the smooth model, `m = 1,100,000`, `σ = 0.12`, `T = 360` s and `H = 430M`. Give `R`, `z` and `K`. Use the slope rule to predict the gain from a 4% health cut, then compute it exactly. Why is the exact gain larger?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `R = 1,194,444`, `z = 0.686`, `K = 24.6%`. Slope rule about 2.6 points per 1%, so about 10.5 points. Exact 36.5%, a gain of 11.8.

`z = ln(1,194,444 / 1,100,000) / 0.12 = 0.0824 / 0.12 = 0.686`. `K = 1 − Φ(0.686) = 0.246`. `φ(0.686) = 0.315`, and the slope is `0.315 × 0.01 / 0.12 = 2.6` points per 1%.

After the cut, `H = 412.8M`, `z = 0.346` and `K = 36.5%`. The cut moved `R` toward the median, where the curve is steeper, so the tangent at the start underestimates. Near the median the slope rule is good. Over large moves, compute the exact value.
</details>

30. *Week 7 · compute.* For question 29's boss, what health gives a 40% kill rate, and what cut is that? If median group DPS grows 2% a week from gear, about how many weeks until 40% arrives with no hotfix?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `H* = 408.2M`, a 5.1% cut. About 3 weeks of growth reaches the same point.

`z* = Φ⁻¹(0.6) = 0.253`. `H* = 360 × 1,100,000 × e^(0.12 × 0.253) = 408,200,000`. `1 − 408.2 / 430 = 5.1%`.

For growth, 40% needs `m = R / e^0.0304 = 1,158,700`, which is 5.3% above today's median. `ln 1.0533 / ln 1.02 = 2.6` weeks. The lecture's step 4 asks you to project this before you patch. If the target date is a month away, waiting may be the right call.
</details>

31. *Week 7 · compute.* 1,000 guilds attempt a boss. The top half by DPS uploads logs at 70%, the bottom half at 30%. At what population percentile is the median logged guild? What weights restore the real mix?

<details>
<summary>Answer and worked solution</summary>

**Answer:** About the 64th percentile. Weight top-half logs by `1 / 0.7 = 1.43` and bottom-half logs by `1 / 0.3 = 3.33`.

The logs hold `500 × 0.7 = 350` top-half and `500 × 0.3 = 150` bottom-half guilds. The median logged guild is the 250th from the top, which is inside the top-half uploaders. Those are spread through the top 500, so it sits at population rank `250 / 0.7 = 357`, the 64th percentile.

With the weights, 350 top-half logs count as 500 and 150 bottom-half logs count as 500, which restores the half-and-half split. The bias here is smaller than the lecture's 80/20 example, but tuning to the raw logs still aims at a guild better than about two thirds of the field.
</details>

32. *Week 7 · code.* What does this print? Which ability would you change first, and why does the share column mislead?

```python
exposures = {"Cinder Wave": 400, "Falling Glass": 60, "Shard Rain": 150}
first_deaths = {"Cinder Wave": 52, "Falling Glass": 21, "Shard Rain": 3}

total = sum(first_deaths.values())
for ability in exposures:
    share = first_deaths[ability] / total
    per_100 = 100 * first_deaths[ability] / exposures[ability]
    print(f"{ability:13s} share {share:5.1%}  per 100 exposures {per_100:5.1f}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
Cinder Wave   share 68.4%  per 100 exposures  13.0
Falling Glass share 27.6%  per 100 exposures  35.0
Shard Rain    share  3.9%  per 100 exposures   2.0
```

There are 76 first deaths. Cinder Wave leads the share because players face it 400 times, more than the other two together. Per exposure, Falling Glass kills 35 players per 100 faced against Cinder Wave's 13, so it is almost three times as deadly.

Change Falling Glass first. Its telegraph, damage or target count is the likely problem. Cinder Wave may still deserve a look because of its volume, but the share column mostly reflects how often and how early it is cast, the trap section 3 warns about.
</details>

## Week 8: Repeatable content

33. *Week 8 · compute.* A daily board offers `a = 8` quests from a pool of `S = 30`, drawn at random each day. Give `p`, the expected repeats from yesterday, the exposure after 5 days and the days to 90%. What does a fixed cycle give for exposure on day 3, and on what day has the whole pool been seen?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `p = 0.267`, 2.1 repeats, 78.8% after 5 days, 7.4 days to 90%. Fixed cycle: 80.0% on day 3, whole pool on day 4.

`p = 8 / 30 = 0.267`. Repeats `8 × 0.267 = 2.13`. `X(5) = 1 − (22/30)^5 = 1 − 0.212 = 0.788`. Days to 90% `ln 0.1 / ln(0.733) = 7.4`.

A fixed cycle shows `3 × 8 = 24` of 30 by day 3, and all 30 on day 4 (32 slots). It never repeats within a cycle and shows the pool fastest, which is exactly why it also wears out fastest.
</details>

34. *Week 8 · design.* A daily hub offers 5 quests a day at random. The design target is that a player who does every daily has seen at most 70% of the pool after 10 days. How many quests must the pool hold? Check the answer and the value one below it.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 45 quests.

`S = a / (1 − (1 − x)^(1/d)) = 5 / (1 − 0.3^(0.1)) = 5 / 0.1134 = 44.1`, so round up to 45.

Check: `S = 45` gives `1 − (40/45)^10 = 69.2%`, inside the target. `S = 44` gives `1 − (39/44)^10 = 70.07%`, just over. Now the authoring cost is known before anyone writes a quest. Halving the offer to 3 a day would cut the pool needed to 27, at the cost of less to do each day.
</details>

35. *Week 8 · compute.* Repeatables pay `r_c = 40` currency an hour, the weekly cap is `C = 400`, and the goal is `G = 4,000`. Player A plays 15 hours a week, player B 9 hours a week. Both miss weeks 1 to 3. In which week does each finish under a hard cap and under an accumulating cap? Where does the cap start to bind?

<details>
<summary>Answer and worked solution</summary>

**Answer:** A: week 13 hard, week 10 accumulating. B: week 15 under both. The cap binds above `h* = 400 / 40 = 10` hours a week.

A earns 600 uncapped. Under the hard cap A earns 400 a week from week 4 and needs 10 weeks, finishing in week 13. Under the accumulating cap the allowance is `400w`. A earns 600 in each of weeks 4 to 8 (3,000 total, under the allowance), then 600 in week 9 to reach 3,600, the allowance, then 400 in week 10 to reach 4,000. That is the same week 10 as a player who never missed.

B earns 360 a week, below the cap either way. `4,000 / 360 = 11.1`, so 12 weeks of play, from week 4 to week 15. B's hours sit close to `h*`, so the accumulating cap cannot help. It forgives missed weeks only for players with spare hours, as the lecture said.
</details>

36. *Week 8 · compute.* A dungeon run takes `t = 0.4` hours, pays `b = 30`, and the first run of the day pays a bonus `B = 90`. (a) Give the reward per hour of the first run, of each later run, and the average after 4 runs. (b) What `B` makes the average after two runs exactly twice the later-run rate?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) 300, 75 and 131.25 per hour. (b) `B = 60`.

(a) First run `(90 + 30) / 0.4 = 300`. Later runs `30 / 0.4 = 75`. After 4 runs `(90 + 4 × 30) / 1.6 = 131.25`.

(b) Twice the later rate is 150. `(B + 60) / 0.8 = 150` gives `B + 60 = 120`, so `B = 60`.

With `B = 90` the first run pays four times a later run, which teaches players to do one run and log off. That fills queues across the day and turns the bonus into a daily chore. A smaller bonus weakens both effects.
</details>

## Week 9: Procedural and systemic content

37. *Week 9 · code.* A generator has 7 layouts picked evenly, 3 bosses weighted 2 : 1 : 1 and 6 modifiers weighted 3 : 1 : 1 : 1 : 1 : 1. What does this print? What is the perceived variety `M`, and what do the skewed weights cost?

```python
import math

def effective_variety(weights):
    total = sum(weights)
    return 1 / sum((w / total) ** 2 for w in weights)

axes = {"layout": [1] * 7, "boss": [2, 1, 1], "modifier": [3, 1, 1, 1, 1, 1]}
m_eff = math.prod(effective_variety(w) for w in axes.values())
print(round(m_eff, 1), round(0.5 + math.sqrt(0.25 + 2 * math.log(2) * m_eff), 1))
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
85.3 11.4
```

`M = 7 × 3 × 6 = 126`. The boss axis has probabilities 0.5, 0.25, 0.25, so `1 / (0.25 + 0.0625 + 0.0625) = 2.67`. The modifier axis has 0.375 and five of 0.125, so `1 / (0.1406 + 5 × 0.0156) = 4.57`. `M_eff = 7 × 2.67 × 4.57 = 85.3`, and `n_50 = 0.5 + √(0.25 + 1.386 × 85.3) = 11.4`.

With even weights, `M_eff = 126` and `n_50 = 13.7`. The skewed weights cost about two runs before half of players see a repeat, for nothing but a data-file choice.
</details>

38. *Week 9 · design.* For question 37's generator, the target is a median first repeat of at least 18 runs. What `M_eff` does that need? Compare these options: flatten both weighted axes; add 2 layouts; add a salient axis with 2 even values after flattening the modifier weights. Which meets the target most cheaply?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `M_eff ≥ 220.7`. Flattening both gives 126 (`n_50 = 13.7`, fails). Two more layouts give 109.7 (12.8, fails). Flat modifiers plus a 2-value axis gives 224 (18.1, meets). That is the cheapest, since flattening costs nothing and a 2-value axis is the smallest new axis.

From `n_50 = 18`, `(18 − 0.5)² − 0.25 = 2 ln 2 × M_eff`, so `M_eff = 306 / 1.386 = 220.7`.

Flat modifiers with skewed bosses: `7 × 2.67 × 6 = 112`. Doubled by a new even 2-value axis: 224. Flattening everything and adding the 2-value axis gives 252 (19.2) for the same authoring cost. Layouts are the most expensive art and buy the least, because they add to one factor instead of multiplying by a new one.
</details>

39. *Week 9 · compute.* A radiant-style quest picks one of 10 locations evenly. Give the exact chance of a repeat within 4 quests and the birthday approximation. Why do they differ?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Exact 49.6%, approximation 45.1%.

Exact: `1 − (10 × 9 × 8 × 7) / 10⁴ = 1 − 5,040 / 10,000 = 0.496`. Approximation: `1 − exp(−4 × 3 / 20) = 1 − e^(−0.6) = 0.451`.

The approximation replaces each factor `(1 − j/M)` with `e^(−j/M)`, which is accurate when `j/M` is small. With only 10 values and 3 draws already made, `j/M` reaches 0.3 and the approximation underestimates. For small pools, compute the exact product. For the MMO-scale generators in the lecture, the approximation is fine.
</details>

40. *Week 9 · compute.* A generator passes validation 30% of the time. Give the expected attempts and the chance of needing more than 10. The server generates 20,000 dungeons a day and falls back to a hand-built layout after 10 failures. How many fallbacks a day? What must you measure on the accepted outputs, and why?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 3.3 attempts on average, 2.8% need more than 10, about 565 fallbacks a day. Measure `M_eff` on the accepted outputs.

`1 / 0.3 = 3.33`. `0.7^10 = 0.0282`. `20,000 × 0.0282 = 565`.

565 groups a day get the same fallback layout, which is itself a repeat players will notice. The validator also filters the distribution. If some signatures fail more often, the accepted outputs under-represent them, so the input weights no longer describe what players see. Lab 09 shows `M_eff` falling from 59.5 to about 53 for exactly this reason.
</details>

41. *Week 9 · critique.* A faction system has 4 forts that each side can hold and 3 mines that can be overrun or not. The pitch says "128 different world states." Logs show one state, "side A holds everything, no mines overrun," 90% of the time, and the other 127 share the rest evenly. What is the effective variety, and what would you change?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `M_eff = 1.23`. The region is almost always the same.

`2⁴ × 2³ = 128` possible states. The sum of squares is `0.9² + 127 × (0.1/127)² = 0.81 + 0.00008 = 0.8101`, so `M_eff = 1 / 0.8101 = 1.23`.

A system that settles into one state is a rotation of one. Add a negative feedback loop (GD102 week 4) so the winning side's advantages shrink as it wins, bound every stock, log the state so you can see how often each state occurs, and give players a lever that moves it. Then report the measured `M_eff` in the pitch instead of 128.
</details>

## Week 10: Player-generated content

42. *Week 10 · compute.* Player missions overpay by an exponential amount with mean `m = 0.06`, and 2,000 missions pay rewards. Give the median rate and the expected best rate. If 25% of play time moves to the best mission, what is the inflow multiplier?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Median 1.042×, expected best 1.491×, inflow multiplier 1.123.

The median of an exponential with mean 0.06 is `0.06 × ln 2 = 0.042`. `H_2000 = 8.178` (the estimate `ln 2000 + 0.577 = 8.178` agrees), so the best is `1 + 0.06 × 8.178 = 1.491`.

Inflow `1 + 0.25 × 0.491 = 1.123`, 12% more reward entering the game than planned. The typical author overpays 4%. Selection by farmers finds the one who overpays 49%.
</details>

43. *Week 10 · design.* For question 42's system, you want the expected best at or below 1.2× with 2,000 paying missions. (a) What `m` must a server-computed reward reach? (b) With `m = 0.06` unchanged, how large can a curated paying pool be? Check the boundary. (c) Name one cost of each lever.

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) `m ≤ 0.0245`. (b) 15 missions. (c) See below.

(a) `m × 8.178 ≤ 0.2` gives `m ≤ 0.0245`, less than half today's value.

(b) `0.06 × H_N ≤ 0.2` needs `H_N ≤ 3.333`. `H_15 = 3.318` gives 1.199. `H_16 = 3.381` gives 1.203. So 15.

(c) The server-computed rule takes pacing and payoff away from authors, and the server has to measure difficulty honestly. The curated pool means almost every creator's players earn nothing, so fewer players try their work. A 1.2× cap, the third option, sets the rate farmers will earn, so you must tune the economy as if they earn it all the time.
</details>

44. *Week 10 · compute.* A funnel receives 12,000 submissions a month. 55% pass a completion check, 20% of those get enough reviewer plays to be rated, and 45% of the rated ones clear the rating bar. How many reach the public list, and what share of authors do not? Moderators review the 8% of submissions that are flagged, at 4 minutes each. How many hours a month is that?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 594 reach the list, 95% of authors do not, and moderation takes 64 hours a month.

`12,000 × 0.55 × 0.20 × 0.45 = 594`. `11,406 / 12,000 = 95%`. `12,000 × 0.08 × 4 = 3,840` minutes, 64 hours.

The funnel's weakest gate is the 20% reviewer stage, which is also the one that decides whether a creation gets an audience at all. A guaranteed small audience for every new creation (the lecture's "new and rising" slot) attacks that gate directly and keeps authors motivated.
</details>

## Week 11: Events and world bosses

45. *Week 11 · compute.* A map has `N = 2,400` interested daily players, 80-minute sessions and a 20-minute join window. Find the knee and the crowd there. Give reach, crowd and players shut out at `T = 60` and `T = 240`. What is `N_crit` for `n_min = 50`?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Knee at 100 minutes, crowd 166.7. At 60 minutes: 100% reach, 100.0 per occurrence, none shut out. At 240 minutes: 41.7% reach, 166.7 per occurrence, 1,400 shut out. `N_crit = 720`.

`S + W = 100`. Crowd at the knee `2,400 × 100 / 1,440 = 166.7`. At 60 minutes, `2,400 × 60 / 1,440 = 100`. At 240, reach `100 / 240 = 0.417`, crowd stays at 166.7, and `2,400 × 0.583 = 1,400` players cannot attend.

`N_crit = 1,440 × 50 / 100 = 720`. The population can fall by 70% before no schedule can fill this event.
</details>

46. *Week 11 · compute.* On question 45's map, 15% of interested players plan around a published time. Compare the crowd at a once-a-day boss with the crowd at one occurrence of an hourly boss. What does the daily boss cost?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Daily: about 527 (166.7 random plus 360 planners). Hourly: 115 (100 random plus 15 planners). The daily boss shuts out about 2,233 players a day.

Planners are `0.15 × 2,400 = 360`. A daily boss gets all of them plus the random arrivals at the knee value, 166.7. An hourly boss spreads the 360 over 24 occurrences, 15 each, plus `2,400 × 60 / 1,440 = 100` random arrivals.

Daily reach for random arrivals is `100 / 1,440 = 6.9%`, so `2,400 × 0.931 = 2,233` players whose sessions miss it, except for those who rearrange their evening. That is the honest trade the lecture described. Rarity gathers the planners and shuts out everyone else.
</details>

47. *Week 11 · design.* Each participant deals `d = 400` damage per second. Design a health rule `H(n) = H_0 + h × n` so that 15 players kill the boss in 240 s and 150 players in 150 s. What is the kill time at 50 players?

<details>
<summary>Answer and worked solution</summary>

**Answer:** `H_0 = 600,000` and `h = 56,000`. Kill time at 50 players is 170 s.

`t(n) = H_0 / (400 n) + h / 400`. So `H_0 / 6,000 + h/400 = 240` and `H_0 / 60,000 + h/400 = 150`. Subtracting, `H_0 × (1/6,000 − 1/60,000) = 90`, which gives `H_0 = 600,000`. Then `h / 400 = 150 − 10 = 140`, so `h = 56,000`.

Check: `600,000 / 6,000 + 140 = 240`. At 50 players, `600,000 / 20,000 + 140 = 170` s. Kill time stays between two and a half and four minutes over a tenfold range of crowd. The floor, `h / d = 140` s, is what very large crowds approach.
</details>

48. *Week 11 · critique.* A zone's knee crowd is 120. Two world bosses, each needing 70 players, start at the same time. The server holds at most 100 players per zone copy. Find both problems and one fix for each.

<details>
<summary>Answer and worked solution</summary>

**Answer:** Together, the bosses split the crowd to about 60 each, below 70. Apart, one boss draws 120, which the copy cap splits into two copies of 60, also below 70.

With equal pull, each boss gets `120 / 2 = 60`. Staggering the start times lets players attend both and restores 120 each, for free.

Then the second problem shows. 120 is above the copy size, so the players land in two copies of 60. Each copy must still exceed `n_min`. Either lower `n_min` to 60 or less by scaling health to the crowd, or raise the copy size to hold 120, which the server team must price (MMO302 week 1). The lecture's calendar rule covers both. Every event's crowd, after splitting, must stay above its `n_min`.
</details>

## Week 12: Content tooling and pipelines

49. *Week 12 · compute.* A team introduces 40 data defects and 20 logic defects per 1,000 items. Stages: author (0.25 h per fix; catches 20% of data, 10% of logic), review (1 h; 30%, 30%), QA (4 h; 50%, 60%), then live at 40 h per defect. (a) Give defects found, hours per stage and the total. (b) Add a validator after the author (0.5 h; 95% of data, 20% of logic) and recompute. (c) What share of escapes is logic after the validator?

<details>
<summary>Answer and worked solution</summary>

**Answer:** (a) Author 10.0, review 15.0, QA 18.8, live 16.2 defects. Hours 2.5, 15.0, 75.0 and 649.6, total 742.1. (b) Author 10.0, validator 34.0, review 4.8, QA 6.6, live 4.6. Total 234.4 hours. (c) 88%.

(a) Data: author finds 8, leaving 32; review finds 9.6, leaving 22.4; QA finds 11.2, leaving 11.2. Logic: 2 then 18; 5.4 then 12.6; 7.56 then 5.04. Live gets `11.2 + 5.04 = 16.24` defects, `16.24 × 40 = 649.6` hours, 87.5% of the total.

(b) After the author, the validator finds `32 × 0.95 + 18 × 0.2 = 30.4 + 3.6 = 34` defects at 0.5 h. Downstream, escapes fall to 0.56 data and 4.03 logic, and the total falls to 234.4 hours, less than a third.

(c) `4.03 / 4.59 = 88%`. The next hour of tooling belongs on logic defects (state search, playtests), not on a better data validator.
</details>

50. *Week 12 · code.* This uses the lecture's validator on new data. What does it print? Name one defect in this data that it does not report, and the rule family that would catch it.

```python
quests = {
    "q_a": {"level": 20, "giver": "npc_ola", "requires": [],             "xp": 1800, "text": "s_1"},
    "q_b": {"level": 21, "giver": "npc_ola", "requires": ["q_a", "q_z"], "xp": 2100, "text": "s_2"},
    "q_c": {"level": 20, "giver": "npc_mai", "requires": ["q_b"],        "xp": 1900, "text": "s_3"},
}
npcs = {"npc_ola", "npc_mai"}
strings = {"s_1", "s_2"}
XP_BUDGET = {20: 2000, 21: 2000}

def validate(quests):
    errors = []
    for qid, q in quests.items():
        if q["giver"] not in npcs:
            errors.append(f"{qid}: unknown quest giver {q['giver']}")
        if q["text"] not in strings:
            errors.append(f"{qid}: missing text {q['text']}")
        if q["xp"] > XP_BUDGET[q["level"]]:
            errors.append(f"{qid}: {q['xp']} XP over the level {q['level']} budget")
        for r in q["requires"]:
            if r not in quests:
                errors.append(f"{qid}: requires unknown quest {r}")
            elif quests[r]["level"] > q["level"]:
                errors.append(f"{qid}: level {q['level']} but requires level {quests[r]['level']} quest {r}")
    return errors

for e in validate(quests):
    print(e)
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
q_b: 2100 XP over the level 21 budget
q_b: requires unknown quest q_z
q_c: missing text s_3
q_c: level 20 but requires level 21 quest q_b
```

For `q_b`, the giver and text exist, so the first error is the XP budget. Then `q_a` is fine (level 20 is not above 21) and `q_z` does not exist. For `q_c`, the text is missing, and it requires the level 21 quest `q_b`.

The validator never says that `q_c` is unreachable. `q_c` needs `q_b`, and `q_b` needs a quest that doesn't exist, so no player can ever start `q_c`. The error on `q_b` hides the knock-on effect. A graph rule (every quest reachable from a starting state, no cycles) catches it, which is the "graphs" family in section 3 and Lab 12's `CYCLE` check extended to reachability.
</details>

51. *Week 12 · compute.* A designer's edit takes 3 minutes. Give iterations per 6-hour design day with an 8-minute rebuild wait and with a 15-second hot reload. A lead then adds a full validator run of 90 s to every save. What happens to the hot-reload day, and what would you do instead?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 32.7 iterations a day with the rebuild, 110.8 with hot reload, and 75.8 once the full validator runs on every save.

`360 / (3 + 8) = 32.7`. `360 / (3 + 0.25) = 110.8`. With the validator, `360 / (3 + 0.25 + 1.5) = 75.8`, a loss of about a third of the day's tries.

Run the validator in the hot-reload path on the changed records only, so it adds about a second. A check on every save has a catch rate near its maximum. A slow check tempts designers to skip it, and a skipped check catches nothing.
</details>

52. *Week 12 · critique.* After the validator from question 49 goes in, a producer proposes halving QA's catch rates (to 25% of data and 30% of logic) "because the validator now catches the data bugs." Recompute live defects and total hours. Is the saving real?

<details>
<summary>Answer and worked solution</summary>

**Answer:** Live defects rise from 4.6 to 7.9 and the total from 234.4 to 353.4 hours. QA's fixing hours fall by only 13.2.

With the weaker QA, QA finds 3.3 defects (13.2 hours instead of 26.4), and live receives `0.84 + 7.06 = 7.9` defects, costing 315.8 hours instead of 183.7. Net, the pipeline costs 119 hours more per 1,000 items.

The validator mostly catches data defects. QA was the main catcher of logic defects, which the validator barely sees (20%). Cutting QA moves those to live at ten times the cost per fix. The lecture's misconception "a good validator means we can cut QA" is exactly this.
</details>

## Week 13: Content budgets and cadence planning

53. *Week 13 · compute.* A drop is estimated at `a = 150`, `m = 200`, `b = 340` days. Give `μ` and `σ`. Two staggered teams run a 110-day cadence. Give the window, `z`, the on-time chance and the average days late.

<details>
<summary>Answer and worked solution</summary>

**Answer:** `μ = 215`, `σ = 31.7`. Window 220 days, `z = 0.16`, on time 56.3%, 10.3 days late on average.

`μ = (150 + 800 + 340) / 6 = 215`. `σ = 190 / 6 = 31.7`. `W = 2 × 110 = 220`. `z = 5 / 31.7 = 0.16`. `Φ(0.16) = 0.563`. Average lateness `σ × (φ(z) − z (1 − Φ(z))) = 31.7 × (0.394 − 0.158 × 0.437) = 10.3` days.

The plan divides roughly the mean build time by the team count, so it is barely better than a coin flip. Note that `μ` is 15 days later than `m`, because the estimate is lopsided.
</details>

54. *Week 13 · compute.* For question 53's estimate, how many teams does a 90-day cadence need for 90% on time? What is the fastest cadence 2 teams and 3 teams can promise at 90%?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 3 teams. The fastest 90% cadence is 127.8 days for 2 teams and 85.2 days for 3.

For 90%, `z* = 1.2816`, and the window needed is `215 + 1.2816 × 31.7 = 255.6` days. `ceil(255.6 / 90) = ceil(2.84) = 3`. Two teams: `255.6 / 2 = 127.8`. Three: `255.6 / 3 = 85.2`.

The staircase shows here. Any cadence from 128 days down to 86 costs the same third team. A studio that pays for three teams and ships every 110 days holds 75 days of spare window per drop, which it can spend on scope or on reliability.
</details>

55. *Week 13 · compute.* A drop is 25 days late with `P = 120`. The alternative is to ship on time with 20% of the next drop cut. For players with `T = 200`, 110, 60 and 20 days, give the extra drought under a slip and under a cut. Which players prefer which?

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| `T` | Slip | Cut |
|---|---|---|
| 200 | 0 | 0 |
| 110 | 25 | 22 |
| 60 | 25 | 12 |
| 20 | 25 | 4 |

Slip `= min(X, max(0, P + X − T))`. For `T = 110`, `min(25, 35) = 25`. For `T = 200`, `P + X − T = −55`, so 0.

Cut `= max(0, P − 0.8T) − max(0, P − T)`. For `T = 110`, `(120 − 88) − 10 = 22`. For 60, `(120 − 48) − 60 = 12`. For 20, `(120 − 16) − 100 = 4`. For 200, both terms are 0.

The player who never runs out does not care. Every player who runs out prefers the cut, and the heavier they are, the more strongly. The 110-day player, who barely runs out, gains only 3 days from the cut, and would lose more if the cut content was a story chapter they would have played.
</details>

56. *Week 13 · compute.* Using question 53's estimate, one drop comes in 40 days late and its team does not cut. Give that team's on-time chance for its next drop under 3 teams at `P = 110` and under 2 teams at `P = 110`.

<details>
<summary>Answer and worked solution</summary>

**Answer:** 99.1% with 3 teams, 13.5% with 2.

Three teams: `W = 330 − 40 = 290`, `z = (290 − 215) / 31.7 = 2.37`, `Φ = 0.991`. Two teams: `W = 220 − 40 = 180`, `z = −1.11`, `Φ = 0.135`.

The generous plan absorbs a 40-day slip. The tight plan turns it into a probably-late next drop, which is the cascade of section 4, and drops ship in order, so the other team's finished drop may wait too. Lab 13 simulates the whole roadmap because this effect has no neat formula.
</details>

## Week 14: Accessibility in group content

57. *Week 14 · code.* This uses the lecture's four profiles. What does it print? Which single channel would you add next, and what does `E` become?

```python
PROFILES = {
    "typical":          (0.78, {"colour", "shape", "icon", "text", "sound"}),
    "colour-deficient": (0.05, {"shape", "icon", "text", "sound"}),
    "sound off":        (0.15, {"colour", "shape", "icon", "text"}),
    "low vision":       (0.02, {"colour", "shape", "sound"}),
}

def shut_out(fight):
    return sum(w for w, reads in PROFILES.values()
               if any(not (channels & reads) for channels in fight.values()))

fight = {"beam": {"colour", "icon"}, "roar": {"sound"},
         "pools": {"shape", "text"}, "mark": {"text"}}
E = shut_out(fight)
print(f"{E:.0%}", f"{1 - (1 - E) ** 10:.1%}")
fight["roar"] = fight["roar"] | {"text"}
E = shut_out(fight)
print(f"{E:.0%}", f"{1 - (1 - E) ** 10:.1%}")
```

<details>
<summary>Answer and worked solution</summary>

**Answer:**

```
17% 84.5%
2% 18.3%
```

Next, add sound or shape to "mark". `E` becomes 0.

"beam" is read by everyone, since the colour-deficient profile reads the icon and low vision reads the colour. "roar" is sound only, so sound off (15%) is shut out. "pools" has shape, which everyone reads. "mark" is text only, so low vision (2%) is shut out. `E = 17%`, and `1 − 0.83^10 = 84.5%` of 10-player groups contain someone who cannot read a mechanic.

Adding text to "roar" recovers the 15% profile, leaving `E = 2%` and 18.3% of groups. Adding a sound (or a shape) to "mark" recovers low vision. For essential mechanics, XAG 103's two-senses rule points to sound, so a visual and an audio channel both carry the message.
</details>

58. *Week 14 · compute.* You want at most 25% of randomly formed groups to contain a shut-out player. What is the largest `E` you can accept for 10-player groups, and for 25-player groups?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 2.84% for 10 players, 1.14% for 25.

`1 − (1 − E)^N ≤ 0.25` means `E ≤ 1 − 0.75^(1/N)`. For 10, `1 − 0.75^0.1 = 0.0284`. For 25, `1 − 0.75^0.04 = 0.0114`.

Even a lenient group target forces the player-level share close to zero as groups grow. For raids, aim for `E = 0` on essential mechanics.
</details>

59. *Week 14 · compute.* A game's player base is 70% men and 30% women. About 8% of men and 0.4% of women have a colour vision deficiency. What share of players is that? What share of 5-player and 8-player groups contain at least one of them?

<details>
<summary>Answer and worked solution</summary>

**Answer:** 5.72% of players. 25.5% of 5-player groups and 37.6% of 8-player groups.

`0.7 × 8% + 0.3 × 0.4% = 5.6% + 0.12% = 5.72%`. `1 − 0.9428^5 = 0.255`. `1 − 0.9428^8 = 0.376`.

A colour-only mechanic in a dungeon fails someone in about one group in four. In a fixed guild, the colour-deficient member meets it in every run, which `G` does not show.
</details>

60. *Week 14 · critique.* A designer says: "The Polarity mechanic uses colour, icon and text, three channels, so it passes accessibility." Test the claim with the lecture's profiles and with XAG 103. Then classify these fixes as a per-player setting, a shared encounter change or an alternative way to play: (a) a client option that reads alert text aloud, (b) a 200 ms longer telegraph on the Story tier only, (c) NPC party members for the dungeon.

<details>
<summary>Answer and worked solution</summary>

**Answer:** It passes the four-profile model, but all three channels are visual, so it fails XAG 103's two-senses rule and fails a player who is not looking at that part of the screen. (a) Per-player setting. (b) Shared encounter change, limited to one tier. (c) Alternative way to play.

Colour-deficient players read the icon and text. Sound-off players read everything visual. Low vision players read the colour. So `E = 0` for this mechanic with these profiles. But a player looking at raid frames, or a player with severe low vision, gets nothing, and the model has no profile for them. XAG 103 asks for a second sense, so add a distinct sound.

(a) changes one client and costs no one anything. (b) changes the fight for everyone in that tier. (c) removes the group, which is the only fix for barriers such as a fixed raid night or voice-chat anxiety.
</details>

## Across weeks

61. *Weeks 4 and 5 · compute.* Group B from the week 4 lecture (paper DPS 22,000, `x = 1.0`) clears Quakemaw with 15.9 s to spare, and the lecture's simulation shows a single death at 60 s pushes it past the enrage. The designer adds a raid-wide mechanic that kills on failure: 20 players, 5 casts per pull, 1,050 ms telegraph, `μ = 700`, `σ = 150`. Give the expected deaths per pull and the chance of a pull with no deaths. Repeat at 1,150 ms. What do you tell the designer?

<details>
<summary>Answer and worked solution</summary>

**Answer:** At 1,050 ms, 0.98 expected deaths and a 37.3% chance of none. At 1,150 ms, 0.13 and 87.4%.

At 1,050 ms, `p = Φ(2.33) = 0.99018`. Expected deaths `100 × 0.00982 = 0.98`. No deaths `0.99018^100 = 0.373`. At 1,150 ms, `p = Φ(3) = 0.99865`, expected deaths 0.13, and `0.99865^100 = 0.874`.

Group B's deaths budget is zero, so at 1,050 ms about 63% of its pulls end in an enrage caused by the telegraph, not by damage. Either lengthen the telegraph to about 1,150 ms, cut the targets, change the failure to a debuff (week 5, section 5), or lower `H` so group B can survive one death. Decide which, and write it in the design document.
</details>

62. *Weeks 1 and 13 · design.* A studio ships the week 1 design B drop (`C = 20`, `r = 6`) with 3 teams and the week 13 estimate `μ = 320`, `σ = 40`. It is choosing between `P = 150` and `P = 120`. For each, give the drought for the p50 (6 hours a week) and p90 (16 hours a week) player, the on-time chance and the average days late. Recommend one.

<details>
<summary>Answer and worked solution</summary>

**Answer:**

| `P` | p50 drought | p90 drought | On time | Days late |
|---|---|---|---|---|
| 150 | 10 | 97.5 | 99.94% | 0.0 |
| 120 | 0 | 67.5 | 84.1% | 3.3 |

p50 `T = 840 / 6 = 140` days, p90 `T = 840 / 16 = 52.5` days. At 150, the droughts are 10 and 97.5 days. At 120, 0 and 67.5. The windows are 450 and 360 days, `z = 3.25` and 1.0.

The shorter cadence saves the p90 player 30 days of drought per cycle, but one drop in six arrives late, and every slip lands on the players who run out. A good answer takes `P = 150` and puts a cheap, high-replay minor drop around day 50 for the top percentiles, as the lecture's roadmap did. An answer that takes 120 must say how the studio absorbs the 16% of late drops, for example with a planned cut.
</details>
