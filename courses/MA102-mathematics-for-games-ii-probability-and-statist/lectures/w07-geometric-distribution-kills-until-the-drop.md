# MA102 · Week 07 — Geometric Distribution: Kills Until the Drop

**Why this matters:** Every "1% drop rate" is a promise about a crowd, and a very different promise to each player in it. The geometric distribution tells you how long players will actually wait, how many will still be waiting long after the average, and when your drop rate needs a safety net.

**You will be able to:**
- Compute the probability that a drop has appeared within n attempts, and the probability that it appears on exactly attempt k.
- Derive the mean (1/p) and compute the median and 95th-percentile wait for any drop rate.
- Explain memorylessness and use it to answer "am I due?" questions correctly.
- Critique a drop rate by the size of its dry tail, and propose a design fix.

**Before class:** Schreiber, *Game Balance Concepts*, Level 4 ("Probability and Randomness"). Schreiber & Romero, *Game Balance* (2021), the probability chapter, the sections on independent trials and expected value. Rewatch your notes from MA102 weeks 3 and 5.

**Prerequisites from earlier courses:** Logarithms for "how many tries until" questions, MA101 week 5 ([MA101 syllabus](../../MA101-mathematics-for-games-i-algebra-functions-trigon/syllabus.md)). The complement rule, MA102 week 3, expected value, MA102 week 4, variance, MA102 week 5, and independence, MA102 week 2 (all in the [MA102 syllabus](../syllabus.md)).

**Interactive:** [Kills until the drop](../examples/w07-kills-until-drop.html) (spec at the end of this lecture). Keep it open during section 2.

---

## 1. Counting until success

Last week you counted successes in a fixed number of tries. A fight lasts 20 swings, how many crit? That was the binomial distribution. This week flips the question. The number of tries is no longer fixed. You keep going until something happens, and the thing you count is how many tries it took.

This is the shape of most grinding in games. Kill the boss until the mount drops. Open chests until the rare appears. Fish until the legendary fish bites. Reroll until you get the stat you want. In each case the player's real question is "how long will this take me?"

We need three assumptions. Call a single try a **trial**.

1. Each trial either succeeds or fails. Nothing in between.
2. Every trial has the same success probability, `p`.
3. Trials are **independent**: the result of one does not change the odds of any other (MA102 week 2).

When all three hold, the number of the trial on which the first success happens is a random variable we call `X`. It follows the **geometric distribution**. `X` can be 1 (lucky on the first try), 2, 3, and so on, with no upper limit.

### The chance of succeeding on exactly trial k

For the first success to land on trial `k`, the first `k − 1` trials must all fail, and then trial `k` must succeed. Independence lets us multiply:

```
P(X = k) = (1 − p)^(k − 1) × p
```

- `p` is the success chance per trial.
- `1 − p` is the fail chance per trial.
- `k` is the trial number on which the first success happens.

This is the **probability mass function** (PMF). It answers "what is the chance the drop comes on exactly this kill?"

### The chance of having it by trial n

Players rarely ask about one exact kill. They ask "what are the odds I have it by now?" That is the **cumulative distribution function** (CDF). You already know how to compute it. It is the complement rule from week 3. The only way to *not* have the drop after `n` trials is to fail all `n` of them:

```
P(X > n) = (1 − p)^n            the chance you are still "dry" after n trials
P(X ≤ n) = 1 − (1 − p)^n         the chance you have it by trial n
```

Players call a long run without a drop being **dry**. `P(X > n)` is the dry chance, and it is the number this lecture cares about most.

## 2. Worked example: the 1% drop that one in twenty players still lacks after 300 kills

### The hook

Imagine a raid boss with a mount that drops 1% of the time. Most players hear "1%" and think "about 100 kills." Ask a room of them what happens at kill 100 and many will say "by then you should have it."

Here is what actually happens. After 100 kills, only about 63% of players have the mount. More than a third are still dry. Push on to 300 kills, three times the "expected" number, and about 1 in 20 players still do not have it. In a game with 100,000 people farming that boss, that is roughly 5,000 players who have done the content three times longer than the average and have nothing to show for it. Those players write the forum threads.

Old School RuneScape players have a word for this. They talk about going "dry" on a drop, and the community keeps tools and calculators that tell you how unlucky your current streak is. The feeling is real. The math tells you how many players will feel it.

### The model

One formula does all the work:

```
dry chance after n trials:   P(X > n) = (1 − p)^n
have-it chance:              P(X ≤ n) = 1 − (1 − p)^n
```

To turn it around and ask "how many trials until a fraction `q` of players have the drop?", solve `1 − (1 − p)^n = q` for `n` using logarithms (MA101 week 5):

```
n_q = ln(1 − q) / ln(1 − p)       round up to the next whole trial
```

- `q` is the share of players you want to have the drop, for example 0.5 for the median or 0.95 for "all but 1 in 20."
- `n_q` is the number of trials by which that share of players has succeeded.

### Numbers you can check

With `p = 0.01`, `1 − p = 0.99`. Every entry below is `0.99^n` or `1 − 0.99^n`. Check two or three with a calculator.

| Kills (n) | Have the mount | Still dry | Dry players out of 100,000 |
|---|---|---|---|
| 1 | 1.0% | 99.0% | 99,000 |
| 10 | 9.6% | 90.4% | 90,438 |
| 50 | 39.5% | 60.5% | 60,501 |
| 69 | 50.0% | 50.0% | 49,984 |
| 100 | 63.4% | 36.6% | 36,603 |
| 200 | 86.6% | 13.4% | 13,398 |
| 299 | 95.0% | 5.0% | 4,954 |
| 459 | 99.0% | 1.0% | 992 |
| 500 | 99.3% | 0.7% | 657 |

Read three rows closely.

- **Row 69.** Half of all players have the mount by kill 69, well before kill 100. The typical player is luckier than the average suggests.
- **Row 100.** The "expected" kill count leaves 36.6% of players dry. The mean is not a promise.
- **Row 299.** This is the signature number. At 299 kills, the dry share drops to 4.95%, just under 1 in 20. At 300 it is 4.90%.

The two numbers in the headline, "about 63% by kill 100" and "1 in 20 still dry near kill 300", come straight from `1 − 0.99^100 = 0.634` and `0.99^299 = 0.0495`.

A useful shortcut. For small `p`, `ln(1 − p)` is very close to `−p`, so:

```
n_q ≈ −ln(1 − q) / p
median (q = 0.5):   n ≈ 0.69 / p
95%    (q = 0.95):  n ≈ 3.0 / p
99%    (q = 0.99):  n ≈ 4.6 / p
```

Memorize the middle one. **To get 95% of players the drop, plan for about three times the average number of trials.** At `p = 0.01` the shortcut gives 300, and the exact answer is 299.

A second shortcut hides in row 100. When `n = 1/p`, the have-it chance is `1 − (1 − p)^(1/p)`, which is close to `1 − 1/e ≈ 63.2%` for any small `p`. So at the average number of trials, about 63% of players have succeeded, whatever the drop rate is. That is why "63%" keeps showing up in discussions of loot.

### The visual: two views of the same wait

Open the interactive. It shows the same distribution twice.

The left view is the PMF, `P(X = k)`, drawn as bars for kills 1 to 500. The tallest bar is at **kill 1**. Every later bar is 1% shorter than the one before it. The single most likely kill on which to get a 1% drop is the very first one. That surprises almost everyone. It is true because the drop on kill 1 needs only one success, while the drop on kill 100 needs 99 failures *and then* a success.

The right view is the dry curve, `P(X > n)`, falling from 100% toward 0. Vertical markers show the median (69), the mean (100) and the 95th percentile (299). The shaded area under the curve past the mean is the part of your player base that is "unlucky." Drag the drop-rate slider from 1% down to 0.2% and watch every marker slide right in proportion. Switch the population field to 100,000 and the y-axis relabels in players instead of percent. The dry tail becomes a crowd.

The left view makes it feel like everyone should get the drop early. The right view shows how long the tail really is. Both are true. The difference between them is the lesson.

### Cross-game recognition

The same model covers a lot of games once you rewrite each rule as "a fixed chance `p` per independent trial."

**Old School RuneScape, abyssal whip.** Abyssal demons drop the abyssal whip at a rate of 1/512 per kill, as listed on the Old School RuneScape Wiki's drop table. So `p = 1/512`. The mean is 512 kills. The median is 355 kills. By kill 1,533 you reach 95%, meaning 1 in 20 slayers is still without a whip after three times the average. The game's own wiki exists partly to answer exactly this, and players compare their kill counts to it constantly.

**Pokémon, shiny encounters.** Since Generation VI (Pokémon X and Y, 2013), a wild encounter is shiny with base odds of 1 in 4,096. From Generation II through V it was 1 in 8,192. Treat each encounter as a trial with `p = 1/4096`. The median hunter needs 2,839 encounters, and 1 in 20 needs more than 12,270. Doubling the odds in Generation VI halved every one of these numbers. That is exactly what the `n_q ≈ −ln(1 − q)/p` shortcut predicts: halve `1/p` and every percentile halves with it.

**Genshin Impact, 5-star wishes without pity.** HoYoverse publishes a base 5-star rate of 0.6% per wish on its character event banner, and a guarantee within 90 wishes. Ignore the guarantee for a moment and treat each wish as a geometric trial with `p = 0.006`. Then `0.994^90 = 0.582`. **Without the guarantee, 58% of players would still be dry after 90 wishes.** The 95th percentile would be 498 wishes. That tail is too long for a product where players spend real money per trial, so the designers cut it off with a pity system. Week 10 takes that system apart.

Three games, one idea. When you meet a new "until it happens" rule, ask: what is one trial, what is `p`, and are the trials independent? If yes, the dry curve is `(1 − p)^n` and every percentile follows.

### Design judgment, eyes open

The geometric distribution is not a bug. It is what pure, fair, independent randomness looks like. Whether it is the right choice depends on what the drop is for.

- **It works well for bragging rights.** A 1-in-4,096 shiny is a trophy because most people will never see one. Rarity is the point, and the dry tail is part of the story players tell.
- **It works badly for required progress.** If a quest item, a raid key or a best-in-slot weapon sits behind a geometric wait, the 1-in-20 dry tail becomes a group of players who cannot progress through no fault of their own. At scale, that group is large.
- **Raising `p` is a blunt fix.** Doubling the rate halves every wait, including the lucky ones. The item becomes common, and its value in the economy drops (MMO304 covers why).
- **Capping the tail is a sharper fix.** Pity timers, bad-luck protection and token systems leave the early game random but put a ceiling on the worst case. The Genshin guarantee at 90 wishes is one example. Week 10 shows how to design these without changing the average much.
- **Deterministic rewards remove the tail entirely.** "Collect 50 tokens, buy the item" has no dry players. It also has no surprise. Many games combine the two: a random drop with a token fallback.

The decision a designer should make on purpose, not by reflex, is this: **for this item, how long may the unluckiest 5% of players wait?** Compute `n_0.95` before you ship, multiply by the time per trial, and read the answer in hours. If it makes you wince, players will feel it too.

## 3. Mean, median and spread

### The mean: 1/p

The expected number of trials is `E[X] = 1/p` (expected value is from week 4). There is a short argument for it that needs no infinite sums.

Let `E` be the expected number of trials. Do one trial. With probability `p` you are done, having used 1 trial. With probability `1 − p` you failed, used 1 trial, and are back where you started, because independence means the future looks exactly as it did before. So:

```
E = 1 + (1 − p) × E
E − (1 − p) × E = 1
p × E = 1
E = 1 / p
```

A 1% drop takes 100 trials on average. A 1/512 whip takes 512 kills on average. This part of players' intuition is correct.

### The median sits well below the mean

The median wait is the `n` where half of players have succeeded. From the shortcut, that is about `0.69/p`, so about 69% of the mean. The mean is pulled up by the long tail of unlucky players, the same way a few billionaires raise a country's average income without changing what a typical person earns.

This matters when you talk to players. If you say "the mount takes about 100 kills," the typical player will get it around kill 69 and think you exaggerated. The unlucky 5% will still be farming at kill 300 and think you lied. Both reactions come from the same true statement.

### The spread is as big as the mean

The variance of the geometric distribution is:

```
Var(X) = (1 − p) / p²
SD(X)  = √(1 − p) / p
```

For `p = 0.01`, `SD = √0.99 / 0.01 ≈ 99.5` kills. The standard deviation is almost exactly the mean. For small `p` this is always true. A process whose typical spread is as large as its average is about as "swingy" as a common game system gets (recall the swingy designs from week 5). If you want a reward to feel reliable, a geometric wait is the wrong tool.

| Drop rate p | Mean 1/p | Median | 95th percentile | SD |
|---|---|---|---|---|
| 1/10 (10%) | 10 | 7 | 29 | 9.5 |
| 1/100 (1%) | 100 | 69 | 299 | 99.5 |
| 1/512 | 512 | 355 | 1,533 | 511.5 |
| 1/4,096 | 4,096 | 2,839 | 12,270 | 4,095.5 |

The median and 95th-percentile columns are `ceil(ln(0.5)/ln(1 − p))` and `ceil(ln(0.05)/ln(1 − p))`. Notice the ratios stay almost the same down every row. That is why the shortcuts work.

## 4. Memorylessness: nobody is ever "due"

Suppose a player has killed the 1% boss 100 times and is still dry. What is the chance they get the mount in the next 50 kills?

Many players reason that they have "used up" their bad luck. The model says otherwise. The chance of being dry for 50 *more* kills, given that you were dry for the first 100, is:

```
P(X > 150 | X > 100) = P(X > 150) / P(X > 100)
                     = 0.99^150 / 0.99^100
                     = 0.99^50
                     ≈ 0.605
```

That is exactly the chance a brand-new player has of being dry after 50 kills. The first 100 kills changed nothing. This is the **memoryless property**: the geometric distribution forgets the past. In general:

```
P(X > m + n | X > m) = P(X > n)
```

This is the gambler's fallacy from week 2 seen from the other side. In week 2 you learned that independent trials do not care about history. Here you see the consequence for waiting times: at every kill, the expected number of kills remaining is still `1/p`. A player on kill 250 has, on average, 100 kills to go. So does a player on kill 1.

Memorylessness is also a design lever. The whole point of a pity timer is to *break* it, so that the past does change the future. A player who has been unlucky gets better odds. You cannot do that with a fixed `p`, and that is the reason week 10 exists.

## 5. From one player to a whole server

A drop rate is a statement about one player. Your community sees a population. Multiply the dry chance by the number of players and the abstract tail becomes a concrete group of people.

Take a raid mount at 1% and a server population of 20,000 players who farm it once a week.

- After 69 weeks, about half the server has it.
- After 100 weeks, about 7,300 players still do not.
- After 299 weeks, almost six years, about 990 players still do not.

Those 990 players are statistically ordinary. Nothing is wrong with the game's random number generator. But from their side it looks broken, and every one of them can post a screenshot of a kill count to prove it. Once a large population plays, rare events happen every day to someone. A 1-in-1,000 streak in a population of 100,000 players happens to about 100 of them.

This is why designers of games with large audiences often talk about the worst case rather than the average. The average is what your spreadsheet shows. The worst case is what your forums show.

### Two players on the same boss

Here is one more trap. Two friends farm the 1% mount together, and each gets an independent 1% roll per kill. What is the chance *at least one* of them has it after 100 kills? Each is dry with chance 0.366, so both are dry with chance `0.366² ≈ 0.134`. So 86.6% of pairs have at least one mount. That is the same as a solo player after 200 kills. Two independent players farming `n` kills behave like one player farming `2n` for the question "has anyone got it yet?" For the question "have *both* got it?" the answer is much worse: `0.634² ≈ 0.40`. Group loot rules (who gets the drop when only one falls) change these numbers again, and you will model them in the lab.

## 6. When the model does not apply

The geometric model depends on its three assumptions. Check them every time.

- **Same `p` every trial.** If the drop rate rises with each failure (pity systems, bad-luck protection), the distribution is not geometric. The tail is shorter and the curve bends downward faster near the cap.
- **Independence.** If the game uses a shuffled "deck" of outcomes, or a pseudo-random distribution that raises the chance after each miss, trials are linked and the geometric formulas give wrong answers. Week 10 covers these.
- **One success ends it.** If players keep farming after the first drop for duplicates, you want the count of successes in `n` trials, which is the binomial model from week 6.
- **The trial is well defined.** "Per kill" and "per loot roll" differ when a boss rolls its table several times per kill. If a boss rolls 3 times at 1% each, the per-kill success chance is `1 − 0.99³ ≈ 2.97%`, not 3%. Week 9 builds on this.

## In-class activity (25 minutes)

Work in pairs. You have a spreadsheet or Python, and the interactive.

You are designing three rewards for a dungeon that takes 15 minutes per run.

1. A cosmetic pet meant as a long-term trophy.
2. A weapon that most players need to clear the next tier.
3. A crafting reagent that players need 5 of.

For each reward:

1. Pick a per-run drop rate `p`.
2. Compute the median runs, the 95th-percentile runs and the 99th-percentile runs. Convert each to hours.
3. For the weapon, decide the longest wait you will accept for the unluckiest 5%. Work backward to the `p` that achieves it using `p ≈ 3 / n_0.95`.
4. For the reagent, you need 5 successes, not 1. Use the interactive's "successes needed" field (it sums geometric waits) or simulate it. Compare the 95th percentile to five times the single-drop 95th percentile. Is it bigger or smaller? Why?

**Expected output:** a one-page table with your three rates, the percentile waits in runs and hours, and two sentences per reward justifying the choice. Swap tables with another pair and find the reward whose tail you would complain about as a player.

## Common misconceptions

- **"A 1% drop means I'll have it after 100 kills."** After 100 kills, 36.6% of players are still dry. The mean is 100, but it is not a deadline. Use the 95th percentile, about `3/p`, when you want a number that holds for nearly everyone.
- **"I've been unlucky, so I'm due."** The geometric distribution is memoryless. After any number of failures, the expected remaining wait is still `1/p`. Past failures only matter if the game deliberately changes `p`, as pity systems do.
- **"The most likely kill for the drop is around kill 100."** The most likely single kill is kill 1. Each later kill is slightly less likely to be *the* kill, because it requires more failures first. The mean is large only because the tail is long.
- **"Three rolls at 1% means 3%."** It means `1 − 0.99³ ≈ 2.97%`. The difference is small here but grows fast. Ten rolls at 20% is not 200%, it is `1 − 0.8^10 ≈ 89.3%`.

## Check yourself

1. A crafting material drops at 4% per gather. How many gathers until half of players have it? Until 95% have it? Give exact whole-trial answers and the shortcut estimates.
2. A player has opened 60 chests without the 2% rare item. What is the chance they open 60 more without it? What is the expected number of chests they still need to open?
3. A designer wants 95% of players to get a raid weapon within 20 clears. What is the smallest drop rate per clear that achieves it? If the boss instead rolls its loot table 2 times per clear, what per-roll rate is needed?
4. Players complain that a 1-in-500 drop is "bugged" because a streamer went 2,000 kills without it. How rare is that streak? In a population of 50,000 players each doing 2,000 kills, about how many would share the streamer's experience?

<details>
<summary>Answers</summary>

1. `n_0.5 = ln(0.5)/ln(0.96) = 16.98`, so 17 gathers. Shortcut `0.69/0.04 ≈ 17.3`. `n_0.95 = ln(0.05)/ln(0.96) = 73.4`, so 74 gathers. Shortcut `3/0.04 = 75`. The shortcut overestimates slightly because `p = 0.04` is not tiny.
2. Memoryless, so the past 60 do not matter. `P(dry for 60 more) = 0.98^60 ≈ 0.298`. The expected remaining chests are `1/0.02 = 50`.
3. Solve `1 − (1 − p)^20 = 0.95`, so `(1 − p)^20 = 0.05` and `1 − p = 0.05^(1/20) = 0.8609`. The smallest rate is `p ≈ 13.9%` per clear. With 2 independent rolls per clear, the per-clear dry chance is `(1 − r)^2`, which must equal `0.8609`. So `1 − r = √0.8609 = 0.9278` and `r ≈ 7.2%` per roll. That is slightly more than half of 13.9%, because two rolls at 7.2% can both succeed.
4. `P(X > 2000) = (499/500)^2000 = 0.998^2000 ≈ e^(−4.0) ≈ 0.0182`, about 1 in 55. Of 50,000 players, about `50,000 × 0.0182 ≈ 910` would go 2,000 kills dry. The streamer is unlucky but in a crowd of hundreds.

</details>

## Lab hook

**Lab 07, Dry streaks at scale** ([labs/lab07.md](../labs/lab07.md)). Simulate 10,000 players farming a drop, compare the simulated dry curve to `(1 − p)^n`, and write a one-page recommendation on where a pity cap should go for a required raid item. The simulation code from this lab is reused in the Monte Carlo lab in week 11.

## Sources

- Old School RuneScape Wiki, "Abyssal whip", drop sources table (current game, accessed September 2026). Abyssal demons drop the whip at 1/512.
- Bulbapedia, "Shiny Pokémon", and Wikipedia, "Shiny Pokémon". Base shiny odds 1/8,192 in Generations II to V, 1/4,096 from Generation VI (X and Y, 2013) onward, without modifiers such as the Shiny Charm.
- HoYoverse, "Chronicled Wish Rules & FAQ", Genshin Impact official news, and the in-game wish details for the character event banner (Genshin Impact 1.0 to 5.x era). Base 5-star rate 0.600%, consolidated rate 1.600%, 5-star guaranteed within 90 wishes. Game8, "Gacha Pull Rates", used as a cross-check.
- Old School RuneScape Wiki, general use of "dry" streak terminology and kill-count calculators (community practice, 2013 to present).
- Schreiber, I. (2010). *Game Balance Concepts*, Level 4, "Probability and Randomness" (online course).
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Probability chapter.

## Interactive spec: examples/w07-kills-until-drop.html

**Purpose.** Show that a geometric wait has its most likely value at trial 1 but a long tail, and that the mean leaves about 37% of players dry. The one insight that must be obvious on first load: *at the "expected" 100 kills, a third of players still have nothing, and the tail runs to 300 and beyond.*

**Layout.** Two linked charts side by side on desktop (stacked on mobile, PMF first). Below them, a numbers panel and the controls.

**Left chart, PMF.** Bars for `P(X = k) = (1 − p)^(k − 1) × p`, k = 1 to `kmax`. `kmax = ceil(ln(0.001)/ln(1 − p))` (the 99.9th percentile), capped at 20,000. If `kmax > 400`, bin bars so there are at most 400 bins, and plot the bin's summed probability; label the y-axis "chance the drop lands in this bin". Highlight the bar for k = 1 and label it "most likely single kill".

**Right chart, dry curve.** Line of `P(X > n) = (1 − p)^n` for n = 0 to `kmax`. Y-axis in percent, or in players when population mode is on (`population × (1 − p)^n`). Three vertical markers with labels: median `ceil(ln 0.5 / ln(1 − p))`, mean `1/p`, 95th percentile `ceil(ln 0.05 / ln(1 − p))`. Shade the area where `n > 1/p` in a warning tint. A draggable cursor on the x-axis (keyboard: arrow keys move it by 1, Page Up and Page Down by 10) shows `n`, have-it %, dry % and dry players at that n. The same `n` is highlighted as a vertical line on the PMF chart.

**Controls.**
- Drop rate slider, logarithmic, from 1/5,000 to 1/2 (0.0002 to 0.5). Default 0.01. Also a numeric text field accepting either a percent ("1%") or a fraction ("1/512").
- Presets as buttons: "1% mount" (0.01), "Whip 1/512", "Shiny 1/4096", "Wish 0.6% (no pity)" (0.006).
- Population field, default off; when on, default 100,000.
- "Successes needed" stepper, 1 to 10, default 1. When above 1, replace the formulas by the negative binomial: `P(X = k) = C(k − 1, r − 1) p^r (1 − p)^(k − r)`, and the dry curve by `P(X > n) = 1 − Σ_{k=r..n} P(X = k)`. Mean `r/p`. Compute percentiles by accumulation, not a closed form.

**Numbers panel.** Mean, median, 95th and 99th percentile, SD `√(1 − p)/p` (for r = 1), dry % at the mean, and dry players if population is on. All values update live.

**Test values (r = 1).**
- p = 0.01: median 69, mean 100, 95th 299, 99th 459, SD 99.5, dry at 100 = 36.6%, dry at 300 = 4.9%, P(X = 1) = 1.000%, P(X = 100) = 0.370%.
- p = 1/512: median 355, 95th 1,533, 99th 2,356.
- p = 1/4096: median 2,839, 95th 12,270.
- p = 0.006: dry at 90 = 58.2%, median 116, 95th 498.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. The cursor and slider are keyboard operable with visible focus. Respect reduced motion (no animated transitions). No game art or logos; preset buttons use text only.
