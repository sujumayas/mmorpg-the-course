# MMO307 · Week 01 — The Endgame Problem

**Why this matters:** Most of a veteran player's hours in an MMO happen after the last level, in a part of the game the level curve no longer paces. What they do there, and how long it keeps meaning something, is the endgame problem. Get it wrong and your most committed players are either "done" in three weeks or stuck chasing one item for three months.

**You will be able to:**
- Compute the expected number of runs to finish a gear set under random drops, and the chance that the next run gives an upgrade.
- Derive how offering a choice of `m` rewards, a token currency or a pity rule changes both the finish time and the shape of the chase.
- Compare the gear chases of World of Warcraft and Final Fantasy XIV by rewriting each in the same model.
- Design a reward system whose upgrade rate stays above a target until the next content drop.

**Before class:** Schreiber & Romero, *Game Balance* (2021), the chapter "Progression in PvE Games" (the sections on endgame and on reward schedules). Warcraft Wiki, "Great Vault" (10 minutes, the Rewards section). Final Fantasy XIV Online Wiki, "Allagan Tomestones" (5 minutes, the two caps).

**Prerequisites from earlier courses:** [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) (expected waits of `1/p`). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (the chance of at least one success). [MA102 week 10, pity timers](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w10-pseudo-random-distribution-and-pity-timers.md). [GD203 week 14, horizontal vs vertical progression](../../GD203-combat-and-progression-design/lectures/w14-horizontal-vs-vertical-progression.md) (the power gap and shelf life). Running alongside this course, [MMO306 week 1, the content treadmill](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w01-the-content-treadmill-production-vs-consumption.md) (exhaustion time and gates).

**Interactive:** [`examples/w01-upgrade-decay.html`](../examples/w01-upgrade-decay.html). Keep it open during section 2.

---

## 1. What happens after the last level

For the first part of an RPG, the level curve does the pacing for you. Each level is a goal, each goal is a little further away than the last, and GD203 week 7 showed you how to shape that clock. Then the player hits the level cap. The Warcraft Wiki describes what comes next as the **endgame**, the part of the game where the focus moves from gaining experience to tackling challenges and earning top rewards.

The endgame is where MMOs keep their players. A player might level a character in a few weeks and then play the same character at the cap for years. So from here on, **endgame** means every activity a player does after the main progression has ended, and the **endgame problem** is the design question of what those activities are for.

A good endgame answers three demands at once.

1. **Felt progress.** Each session should have a fair chance of moving the player forward. A player who logs in and gets nothing ten times in a row stops logging in.
2. **Duration.** The goals must last until the next content drop. MMO306 week 1 calls the time a player takes to run out of content the exhaustion time `T`, and the time between drops the cadence `P`. If `T` is much shorter than `P`, players leave in the gap.
3. **Cohesion.** The goals should not split the player base. GD203 week 14 showed that every multiplicative power step shortens the time two players can share content.

These demands pull against each other. Rewards that keep coming feel good and run out fast. Rewards that last forever feel stingy. Rewards that grant power split veterans from newcomers. Every endgame is a compromise among them, and this course is largely about the tools for making it.

### Four families of answer

Look at any shipped MMO and its endgame activities fall into a few families.

- **Repeat.** Run the same dungeon or raid many times for a chance at better gear. This is the gear chase, and it is this week's worked example.
- **Reset.** Replace the gear everyone has with a new tier, so the chase starts again. Weeks 2, 4 and 11 cover the treadmill, item level and seasons.
- **Rank.** Give players a competitive number to push, such as a PvP rating or a timed-dungeon score. Weeks 8 to 10 build the rating systems.
- **Breadth.** Give players new options instead of more power, such as masteries, jobs or collections. Week 3 covers horizontal progression, and week 12 covers account-wide systems.

Most games use all four. The mix is what differs, and the mix is set by numbers you can compute.

## 2. Worked example: when is a player "done"?

### The hook

Two big MMOs pay out their endgame gear in very different ways.

In Final Fantasy XIV's Dawntrail expansion, patch 7.05 introduced a currency called the Allagan Tomestone of Heliometry. It bought item level 720 gear. The official wiki lists the prices. Head, hands and feet cost 495 each, body and legs 825 each, and each of five accessories 375, for 5,010 tomestones in all, before the weapon. Players can usually earn at most 450 of the current tomestone per week. Divide and you get 11.1, so every player who hits the cap each week finishes that set in its twelfth week. The fastest player and the median player finish on the same day.

World of Warcraft's main gear arrives as random drops from bosses and dungeon chests. On top of that, the Great Vault gives each character a weekly choice. Depending on what they did the week before, up to nine items are revealed, and the player keeps one. There is no fixed finish date. Some players complete their set early. Others spend weeks on one missing trinket.

Both games have the same goal, a gear chase that lasts until the next tier. Here is a model that shows what each choice buys.

### The model

A character has `S` gear slots to fill with the current tier's gear. A slot is either filled (the player has the item they want there) or empty.

Each run of the content gives the player one item for a slot chosen uniformly at random. If that slot is empty, the item is an **upgrade**. If it is already filled, the item is a duplicate and worth nothing.

With `k` slots filled, the chance that the next run is an upgrade is:

```
p(k) = (S − k) / S
```

The wait for the next upgrade is geometric, so by MA102 week 7 its expected length is `1 / p(k) = S / (S − k)` runs. Add up the waits for every slot and you get the expected number of runs to fill the set:

```
E[runs] = S/S + S/(S−1) + ... + S/1 = S × H_S
```

where `H_S = 1 + 1/2 + ... + 1/S` is the `S`-th harmonic number. Probability texts call this the **coupon collector's problem**, after people collecting a full set of cards from cereal boxes.

One more quantity matters for how the chase feels. Average over all players who have done `n` runs, and the expected chance that their next run is an upgrade is:

```
u(n) = (1 − 1/S)^n
```

(Each slot is still empty after `n` runs with probability `(1 − 1/S)^n`, and the upgrade chance is the empty fraction.) This is the **upgrade rate**, and it falls exponentially with runs.

Symbols, once more:

- `S`, the number of slots in the set.
- `k`, slots already filled.
- `p(k)`, the chance that the next run is an upgrade for a player with `k` filled.
- `n`, runs done so far.
- `u(n)`, the average upgrade chance on run `n + 1`.

### Numbers you can check

Take `S = 10`.

| Filled `k` | Upgrade chance `p(k)` | Expected runs for the next upgrade | Expected runs so far |
|---|---|---|---|
| 0 | 100% | 1.00 | 1.00 |
| 1 | 90% | 1.11 | 2.11 |
| 2 | 80% | 1.25 | 3.36 |
| 3 | 70% | 1.43 | 4.79 |
| 4 | 60% | 1.67 | 6.46 |
| 5 | 50% | 2.00 | 8.46 |
| 6 | 40% | 2.50 | 10.96 |
| 7 | 30% | 3.33 | 14.29 |
| 8 | 20% | 5.00 | 19.29 |
| 9 | 10% | 10.00 | 29.29 |

The total is `10 × H_10 = 10 × 2.929 = 29.29` runs. Look at where those runs go. The first half of the set takes 8.46 runs. The last three items take `10/3 + 10/2 + 10/1 = 18.33` runs, or 63% of the whole chase. The last single item takes 10 runs, a third of the total.

Now the view by runs.

| Runs done `n` | Expected slots filled `S(1 − u(n))` | Upgrade chance on the next run `u(n)` |
|---|---|---|
| 0 | 0.00 | 100% |
| 5 | 4.10 | 59.0% |
| 10 | 6.51 | 34.9% |
| 15 | 7.94 | 20.6% |
| 20 | 8.78 | 12.2% |
| 25 | 9.28 | 7.2% |
| 30 | 9.58 | 4.2% |

At the average finish time of about 30 runs, the average player still has a 4% chance per run of getting anything useful. That is where the frustration lives.

The spread is large too. Running the exact distribution (the lab does it), half of all players finish within 27 runs, one in ten needs 44 or more, and one in a hundred needs 66 or more. The token player in Final Fantasy XIV has no spread at all.

You can check the totals in a few lines of Python. The function takes an `m` for later. For now, `m = 1`.

```python
def upgrade_chance(k, S, m=1):
    """Chance that a run offering m random items holds at least one upgrade,
    when k of S slots are already filled."""
    return 1 - (k / S) ** m

def expected_runs(S, m=1):
    return sum(1 / upgrade_chance(k, S, m) for k in range(S))

for m in (1, 3, 9):
    print(m, round(expected_runs(10, m), 2))
```

```
1 29.29
3 14.78
9 10.84
```

### A visual you can move

Open the interactive. The left panel plots expected slots filled against runs. It is a smooth, reassuring curve that climbs quickly and levels off near `S`. From this view the chase looks healthy.

The right panel plots the upgrade chance on the next run, `u(n)`, with a dashed line at a threshold you choose, the lowest upgrade chance per run that still feels worth doing. Call it `p_min`. The curve crosses it at:

```
n* = ln(p_min) / ln(1 − 1/S)
```

With `S = 10` and `p_min = 20%`, `n* = ln 0.2 / ln 0.9 = 15.3` runs. After 16 runs, the average player is below your threshold, even though the left panel says they have only about 80% of the set. Switch the reward mode to "tokens" and the right panel becomes a flat line. Switch to "choice of 3" and the curve drops much more slowly. Same finish line, very different chase.

### Cross-game recognition

**World of Warcraft (The War Within and Midnight eras): choice as a multiplier.** The Great Vault reveals up to nine items per week, and the player claims one. In model terms, a vault with `m` options is a run that offers `m` random items and keeps the best. By the complement rule from MA102 week 3, the chance at least one of them is an upgrade is:

```
p_m(k) = 1 − (k/S)^m
```

With `S = 10` and 9 slots filled, a single drop is an upgrade 10% of the time. A choice of 3 is an upgrade `1 − 0.9^3 = 27.1%` of the time, and a choice of 9 is an upgrade `1 − 0.9^9 = 61.3%` of the time. The code above shows what this does to the whole chase. It falls from 29.3 runs to 14.8 with three options and to 10.8 with nine. The real vault draws its options from different activities rather than one shared table, so treat these as model numbers. The shape of the effect is what carries over. Choice helps most exactly where random drops hurt most, at the end.

**Final Fantasy XIV (Dawntrail, patch 7.05): tokens.** Each run pays currency, and the player buys the slot they want. If each item costs `q` tokens and a run pays `c`, every item takes `q/c` runs no matter how many slots are filled. The upgrade rate is flat, and the whole set takes exactly `S × q / c` runs. The weekly cap of 450 then turns runs into calendar time. The Heliometry set needs 5,010 tomestones, which is 12 capped weeks for every player. The wiki also notes that older tomestones lose their cap once a newer one arrives, which works as a catch-up rule (week 6).

**Pity rules (many games): random with a floor.** MA102 week 10 showed how a counter that raises the drop chance after each miss caps the worst-case wait. In this model, a "bad luck" rule that makes the drop an upgrade after `j` duplicates in a row puts a ceiling of `j + 1` runs on each wait. The early chase stays random and exciting. The last items can no longer take 30 runs.

Three games, three rewrites of one model. For any gear chase, ask what `S` is, whether a run gives one random item, a choice or currency, and what caps the wait.

### Eyes-open design judgment

Each option trades one of the three demands from section 1 against another.

- **Pure random drops** give the best early sessions and the most exciting moments. They also give a long, frustrating tail, a wide spread between lucky and unlucky players, and a finish time you cannot promise. Use them when the chase is short or when the tail is protected by something else.
- **Choice of `m`** keeps the excitement of random drops and flattens the tail. It also shortens the whole chase, so the content runs out sooner. The Great Vault is weekly for a reason. Giving a choice on every run would end the chase in days.
- **Tokens** make the chase predictable and fair. Everyone finishes on the same day, and you can set that day to match your content calendar. The cost is that nothing surprising ever happens, so games that use tokens usually pair them with random drops for excitement.
- **Pity rules** protect the unlucky without changing the median much. They add a counter players will learn to track, and they can make the early chase feel like waiting for the counter.

A designer who picks one of these by reflex is picking a finish date by accident. Decide the finish date and the upgrade-rate floor you want, then choose the mix.

### Check yourself (worked example)

1. With `S = 12` and random single drops, what is the expected number of runs to complete the set? (`H_12 = 3.103`.)
2. With `S = 10`, a player has 8 slots filled. What is their chance of an upgrade from a single drop, and from a choice of 3?

<details>
<summary>Answers</summary>

1. `12 × 3.103 = 37.2` runs.
2. Single drop `2/10 = 20%`. Choice of 3, `1 − 0.8^3 = 1 − 0.512 = 48.8%`.

</details>

## 3. Tokens against drops: same finish line, different chase

Set the random-drop chase next to a token chase with the same length. With `S = 10` and one token per run, pricing each item at 3 tokens makes the token set take exactly 30 runs, close to the random average of 29.3.

| Items owned | Random drops, expected runs so far | Tokens at 3 per item, runs so far |
|---|---|---|
| 3 | 4.79 | 9 |
| 5 | 8.46 | 15 |
| 7 | 14.29 | 21 |
| 9 | 19.29 | 27 |
| 10 | 29.29 | 30 |

Random drops are ahead for most of the chase and then stall. Tokens are slower early and never stall. The crossover comes where the random upgrade chance falls below the token rate of one item per 3 runs, that is where `(10 − k)/10 < 1/3`, so after the seventh item.

This is why so many games run both. Drops make the first weeks exciting, and tokens guarantee the last slots. In a **hybrid** each run gives a chance `d` at a random drop and `c` tokens, and the player buys whatever slot the drops have not filled. The tokens set a ceiling on the finish time, and the drops usually beat that ceiling. You will simulate a hybrid in the lab and find its finish time and spread.

There is a second design lever inside tokens, the **cap**. A weekly cap stops players from converting extra hours into gear. It does not change the number of runs a set needs. It changes how the runs map onto weeks. A player who can run the content 20 times a week and a player who can run it 5 times finish on the same week if the cap binds for both. MMO306 week 1 explains why a gate like this compresses the spread between light and heavy players, so we will not repeat it here. For this course the key point is that the cap lets you set the finish date directly.

## 4. Sizing the chase to the calendar

Now put the three demands together and design one chase.

Suppose your next tier arrives in 16 weeks (`P = 16`). Your median player runs the content 3 times per week, so they have 48 runs before the next tier. You want two things.

- **Duration.** The median player should not finish much before week 16, or they will have nothing to do for the last weeks. Aim to finish around week 14.
- **Felt progress.** The upgrade chance per run should stay at or above 20% until the player is done.

Pure random drops with `S = 10` fail both tests. The median player finishes in 27 runs, which is week 9. And the upgrade rate falls below 20% after about 15 runs, in week 5.

You can try to stretch the chase by making drops rarer. Suppose a run gives an item only half the time. Every wait doubles, so the median finish moves to about 54 runs (week 18). The upgrade chance is also halved at every stage of the set, `0.5 × (10 − k)/10`, so it falls below 20% after the seventh item instead of the ninth. Stretching random drops always makes the felt progress worse.

Tokens pass both tests by construction. At one token per run, price each item at `q` tokens so that `10 × q ≈ 14 weeks × 3 runs = 42`. With `q = 4` the set takes 40 runs, finishing in week 14. The upgrade rate is a steady one item per 4 runs, or 25% per run. Add a weekly cap of 3 tokens and heavy players finish in week 14 too.

Or use a hybrid. Here the model has a trap. Drops and tokens both fill slots, so a hybrid always finishes sooner than either part alone. With full-rate drops and tokens at 3 per item, the median hybrid player is done in about 12 runs, not 30. To fill a long tier, a hybrid needs rarer drops or pricier tokens than either system would on its own. In a simulation of 20,000 players, a drop on one run in four (`d = 0.25`) plus tokens at 8 per item puts the median finish at run 40 (week 14) and the 90th percentile at run 48 (week 16). The early runs still surprise, and the tokens still rescue the unlucky. The lab asks you to reproduce this and to find the upgrade rate such a design gives.

The broader lesson is about direction. A design that fixes the finish time too early leaves players with empty weeks, and the usual reflex is to add more random, slower rewards. That buys duration with felt progress, the worst trade of the three. The better levers change the shape of the chase (tokens, choice, pity) or add a second family of goals that does not end (rank, breadth).

## 5. When the chase ends: what the other families add

Every gear chase ends. The question is what the player does in the weeks between finishing and the next tier.

- **Reset** gives them a new chase, and a new `S`. Week 2 shows that a steady diet of resets forces power creep.
- **Rank** gives them a goal with no finish line. A rating can always go up. It also has no power attached, so it does not split the player base. It does create a new kind of gap, which weeks 8 to 10 handle.
- **Breadth** gives them new options, like a second job or a traversal mastery. Guild Wars 2's masteries are an account-wide track that level-80 characters train through play, unlocking things like gliding and mounts. Week 3 models when options like these are worth chasing.

A healthy endgame staggers these. The gear chase fills the first weeks of a tier, rank and breadth fill the tail, and the reset comes before players run out of both.

## In-class activity (25 minutes)

Groups of three. You are designing the gear chase for one tier of a small MMO. The tier lasts 12 weeks, the set has `S = 8` slots, and your median player runs the content 4 times a week.

1. **(5 min)** Compute the expected runs to finish with random single drops (`H_8 = 2.718`). In which week does the median player finish? Use the interactive to find the run where the upgrade chance falls below 25%.
2. **(8 min)** Choose one of choice-of-`m`, tokens or a hybrid. Set its numbers so the median player finishes in week 10 or 11 and the upgrade chance stays at or above 25% until they finish. Show the arithmetic.
3. **(7 min)** A heavy player runs the content 15 times a week. When do they finish under your design? If it is before week 6, add a cap and say what it is.
4. **(5 min)** Swap designs with another group. Find the player your partners' design treats worst (the unlucky one, the heavy one or the light one) and say how far behind the median they finish.

Expected output: one paragraph describing your system, a table of finish weeks for light, median and heavy players, and the weakness your partners found.

## Common misconceptions

- **"If the average finish time is right, the chase is right."** The average hides both the tail and the shape. Two systems with a 30-run average can have upgrade rates of 4% or 33% at run 25.
- **"Choice of 3 triples the upgrade chance."** It raises it by the complement rule, `1 − (k/S)^3`. At `k = 5` of 10 that is 87.5%, not 150%.
- **"Making drops rarer makes the endgame last longer, so it's better for retention."** It lengthens the chase and lowers the upgrade rate at every point. Players feel the rate, and a low rate is the most common reason they quit a chase.
- **"Tokens are boring, so they're bad design."** Tokens are predictable. That is a design property, and it lets you set the finish date. Pair them with something surprising rather than dropping them.

## Check yourself

1. A chase has `S = 16` slots and random single drops. Players in your target group quit a chase when the upgrade chance per run falls below 10%. After how many runs does the average player cross that line? About how many slots do they have filled at that point?
2. With `S = 10` and 7 filled, how many options `m` must the vault offer so that the chance of at least one upgrade is at least 90%?
3. A token system prices every item at 5 tokens and pays 2 tokens per run, with a weekly cap of 10 tokens. The set has 12 slots. How many runs does the set take? How many weeks for a player who runs 8 times a week?
4. Your team proposes halving drop rates to make a tier last twice as long. Using the model, describe what happens to the upgrade chance on the next run after 10 runs, for `S = 10`, and name a lever that stretches the tier without that cost.

<details>
<summary>Answers</summary>

1. `n* = ln 0.1 / ln(1 − 1/16) = −2.303 / −0.0645 = 35.7`, so after about 36 runs. Expected filled slots `16 × (1 − 0.1) = 14.4`. They quit with one or two slots still empty.
2. Need `1 − 0.7^m ≥ 0.9`, so `0.7^m ≤ 0.1`, `m ≥ ln 0.1 / ln 0.7 = 6.46`. The vault must offer 7 options.
3. `12 × 5 / 2 = 30` runs. At 8 runs a week the player would earn 16 tokens, but the cap stops them at 10. The set needs 60 tokens, so it takes 6 weeks, the same as for a player who runs exactly 5 times a week.
4. With half-rate drops, a run gives an item for a given slot with probability `0.5/10 = 0.05`, so the average upgrade chance on run 11 is `0.5 × 0.95^10 = 0.30`, against `0.9^10 = 0.35` at full rate. At any fixed fraction of the set, the half-rate chance is exactly half the full-rate chance. A token track, a weekly cap, or a second family of goals (rank, breadth) extends the tier without lowering the rate.

</details>

## Lab / assignment hook

[Lab 01, gear chase simulator](../labs/lab01.md). You will implement the exact finish-time distribution for random drops, choice-of-`m` and tokens, simulate a hybrid, and tune a tier's chase to a 14-week calendar. It feeds the progression analysis assignment (30%).

## Sources

- Warcraft Wiki, "Level" (current). Defines the endgame as the part of play at the level cap where the focus moves from experience to challenges and rewards. https://warcraft.wiki.gg/wiki/Level
- Warcraft Wiki, "Great Vault" (Shadowlands onward; requirements as listed for Midnight Season 2, 2026). Up to 9 items revealed from the previous week's raid, dungeon and world activities; only one may be claimed. https://warcraft.wiki.gg/wiki/Great_Vault
- Final Fantasy XIV Online Wiki, "Allagan Tomestones" (Dawntrail era, 2026). Newest tomestone usually capped at 450 per week, at most 2,000 held; older tomestones become uncapped when a new one arrives. https://ffxiv.consolegameswiki.com/wiki/Allagan_Tomestones
- Final Fantasy XIV Online Wiki, "Allagan Tomestone of Heliometry" (patch 7.05, Dawntrail). Item level 720 gear; head, hands and feet 495 each, body and legs 825 each, accessories 375 each, weapon 500 plus one Universal Tomestone. https://ffxiv.consolegameswiki.com/wiki/Allagan_Tomestone_of_Heliometry
- Guild Wars 2 Wiki, "Mastery" (current, through the Visions of Eternity expansion). Account-wide PvE progression for level-80 characters that unlocks gliding, mounts and other abilities. https://wiki.guildwars2.com/wiki/Mastery
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Chapter "Progression in PvE Games".
- Coupon collector's problem: any probability text, for example Ross, S. *A First Course in Probability* (10th ed., 2019), the worked example on collecting coupons.

## Interactive spec: examples/w01-upgrade-decay.html

**The one insight.** A gear chase that looks healthy on a "slots filled" chart is failing on an "upgrade chance per run" chart. Random drops fill most of a set fast and then leave players below any reasonable upgrade-rate floor for a third or more of the chase. Choice and tokens change the shape of the right panel far more than the left.

**Layout.** Two linked panels, side by side at 1280px and stacked at 390px, controls below, readout table under the controls.

**Left panel, "Slots filled."** x-axis runs 0 to `n_max` (default 60, auto-extend to 1.2 times the 99th percentile finish of the current mode). y-axis slots filled 0 to `S`.
- Expected slots filled for the current mode (solid line).
- Optional "one player" path, a step line from a seeded simulation (button "New player" re-rolls with a new seed; show the seed).
- A shaded band between the 10th and 90th percentile finish runs, drawn as a horizontal bracket at `y = S`.

**Right panel, "Chance the next run is an upgrade."** Same x-axis. y-axis 0% to 100%.
- Expected upgrade chance on run `n + 1` for the current mode (solid line).
- Dashed horizontal line at `p_min`, and a dot where the curve first falls below it, labelled "n* = {value}".
- In token mode the line is flat at `c/q` (capped at 100%) until the set is complete, then 0.

**Modes (radio buttons).**
- Random drops. `p(k) = (S − k)/S`. Expected upgrade chance at run `n` is `u(n) = (1 − 1/S)^n`. Expected filled `S(1 − u(n))`.
- Choice of `m`. `p(k) = 1 − (k/S)^m`. Compute the expected curves from the exact Markov chain over `k` (state vector of length `S + 1`, update each run). Expected upgrade chance at run `n` is `Σ_k P(K_n = k) p(k)`.
- Tokens. `c` tokens per run, `q` tokens per item. Upgrade every `q/c` runs (deterministic). Show the step function on the left and the flat rate `c/q` on the right.
- Hybrid. Each run gives a random single drop with probability `d` and `c` tokens. Whenever the player holds `q` tokens and has an empty slot, they buy one immediately. Compute by Monte Carlo with 20,000 seeded players (fixed seed 7 by default); show "simulated" next to the numbers.

**Controls.**
- `S` stepper 4 to 20, default 10.
- `m` slider 1 to 9, default 3 (active in choice mode).
- `c` stepper 1 to 5, default 1; `q` stepper 1 to 12, default 3 (token and hybrid modes).
- `d` slider 0.10 to 1.00, step 0.05, default 1.00 (hybrid mode only).
- `p_min` slider 5% to 50%, step 1%, default 20%.
- Mode radio buttons as above.
- All controls keyboard operable with visible labels and live values. Respect `prefers-reduced-motion` (no animated transitions).

**Readout (exact numbers).** For the current mode: expected runs to finish (2 decimals), median, 10th, 90th and 99th percentile finish runs (exact from the Markov chain for random and choice, from the simulation for hybrid, exact for tokens), `n*` (2 decimals, or "never" if the curve never drops below `p_min` before finishing), and expected slots filled at `n*`. Plus a small table of `k`, `p(k)`, expected runs for the next upgrade, cumulative, for `k = 0` to `S − 1`.

**Formulas.**
```
p_random(k)   = (S - k) / S
p_choice(k,m) = 1 - (k / S)^m
E_runs        = sum_{k=0}^{S-1} 1 / p(k)
u_random(n)   = (1 - 1/S)^n
n_star        = ln(p_min) / ln(1 - 1/S)          // random mode, closed form
tokens_total  = S * q / c
```

**Test values.**
- Random, `S = 10`: expected runs 29.29; median 27; 90th percentile 44; 99th percentile 66; `u(10) = 0.349`, `u(20) = 0.122`, `u(30) = 0.042`; with `p_min = 20%`, `n* = 15.28`, expected filled at `n*` about 8.0.
- Choice, `S = 10`: `m = 3` expected runs 14.78; `m = 9` expected runs 10.84; `p(9) = 0.271` for `m = 3` and `0.613` for `m = 9`.
- Tokens, `S = 10, c = 1, q = 3`: 30 runs exactly, flat rate 33.3%.
- Hybrid (simulated, allow ±2 runs): `S = 10, c = 1, d = 1, q = 3` median 12, mean about 12.6; `d = 0.25, q = 8` median 40, 90th percentile 48.
- `S = 12` random: expected runs 37.24. `S = 16`, `p_min = 10%`: `n* = 35.68`.
