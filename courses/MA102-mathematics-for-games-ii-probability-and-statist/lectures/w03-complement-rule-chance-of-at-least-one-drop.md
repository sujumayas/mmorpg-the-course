# MA102 · Week 03 — Complement rule: chance of at least one drop

**Why this matters:** "It's a 1% drop, so I'll have it in 100 kills" is the most common probability mistake in games, and it shapes how players plan, how long they grind, and how angry they get. The complement rule turns that sentence into the right number in one line. It also gives you, the designer, a way to set drop rates from the experience of your unluckiest players instead of your average one.

**You will be able to:**
- Compute the probability of at least one success in `n` independent attempts using the complement rule.
- Derive the number of attempts needed to reach a target chance, such as 50%, 95% or 99%, and estimate it with the 0.7/3/4.6 rules of thumb.
- Explain why one "expected" run of `1/p` attempts gives about 63% for any small drop rate.
- Design a drop rate from a tail target ("no more than 1 in 20 players still dry after N kills") and critique a drop rate by the size of that tail.

**Before class:** Ian Schreiber, *Game Balance Concepts* (blog course, 2010), Level 4, "Probability and Randomness", the section on computing "at least one". Schreiber & Romero, *Game Balance* (2021), the chapter on probability, the section on complementary events.

**Prerequisites from earlier courses:** [MA102 week 1](w01-sample-spaces-and-events.md) (complement of an event), [MA102 week 2](w02-independent-events-and-the-gamblers-fallacy.md) (independence, multiplication rule). Exponentials and logarithms from MA101 [week 4](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) and [week 5](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md).

**Interactive:** [Drop curve](../examples/w03-drop-curve.html) (built from the spec at the end of this lecture). Keep it open during section 2.

---

## 1. The question that is hard to ask directly

Every player who has farmed a rare item has asked some version of "what are my chances of getting it in the next `n` tries?" The event they care about is "at least one drop in `n` attempts".

Try to count that event directly and it falls apart. "At least one drop in 3 kills" means exactly one drop, or exactly two, or all three. Each of those splits further by which kills dropped. For 3 kills that is 7 cases. For 100 kills it is `2^100 − 1` cases, a number with 31 digits. You could use the addition rule from week 1, but the overlaps between "kill 1 drops" and "kill 2 drops" and so on have to be subtracted and added back in layers. Nobody does it that way.

The other side of the event is simple. The opposite of "at least one drop" is "no drops at all". That happens in exactly one way, every kill fails.

This is the **complement rule**, which you met in week 1:

```
P(not E) = 1 − P(E)        so        P(E) = 1 − P(not E)
```

When an event is messy and its complement is clean, compute the complement and subtract from 1. You already did this with advantage, where counting the failing corner of the grid was easier than counting the lit L-shape. This week the complement is "every attempt fails", and week 2's multiplication rule makes it a single power.

## 2. Worked example: the 1% drop

### The hook

In *Old School RuneScape*, the abyssal whip drops from a standard abyssal demon at a rate of 1 in 512. The game's community wiki publishes the rate, and players quote it constantly. A common expectation is that after 512 kills you "should" have a whip.

Here is the surprising part. After 512 kills, only about 63% of players have one. More than a third are still hunting. After 1,533 kills, three times the "expected" number, about 1 player in 20 is still dry.

Now strip the game away and use a round number. A boss drops an item 1% of the time. After 100 kills, only about 63% of players have it, and 1 in 20 still lacks it after roughly 300 kills. The same 63% appears in both games, and the same "about three times as long" for the unlucky 5%. That is not a coincidence, and by the end of this section you will be able to say why.

### The model

Let each kill drop the item with probability `p`, rolled independently. After `n` kills:

```
P(no drop in n kills)          = (1 − p)^n
P(at least one drop in n kills) = 1 − (1 − p)^n
```

- `p` is the drop rate per attempt (0.01 for 1%, 1/512 for the whip).
- `n` is the number of attempts.
- `(1 − p)^n` is the chance that all `n` independent attempts fail, from the multiplication rule.

To go the other way, from a target chance `q` to the number of kills needed, solve `1 − (1 − p)^n ≥ q` for `n`. Take logarithms (MA101 week 5):

```
(1 − p)^n ≤ 1 − q
n ≥ ln(1 − q) / ln(1 − p)
```

Both logarithms are negative, so the fraction is positive. Round up, because you cannot kill a fraction of a boss.

### Numbers you can check

For `p = 1%`, so `1 − p = 0.99`:

| Kills n | Chance of at least one drop | Chance still dry | Players still dry, of 1,000 |
|---|---|---|---|
| 1 | 1.0% | 99.0% | 990 |
| 10 | 9.6% | 90.4% | 904 |
| 50 | 39.5% | 60.5% | 605 |
| 69 | 50.0% | 50.0% | 500 |
| 100 | 63.4% | 36.6% | 366 |
| 200 | 86.6% | 13.4% | 134 |
| 299 | 95.05% | 4.95% | 50 |
| 459 | 99.0% | 1.0% | 10 |

Check the 100-kill row with a calculator: `0.99^100 ≈ 0.366`, so `1 − 0.366 = 0.634`. Check the 299 row: `ln(0.05) / ln(0.99) = −2.996 / −0.01005 ≈ 298.1`, so 299 kills is the first count where fewer than 5% of players are still dry. The signature claim holds. After 100 kills, 63% have the item. After about 300, only 1 in 20 is still without it.

Three numbers from this table deserve names, because designers use them constantly:

- The **median** wait is 69 kills. Half of all players have the item by then.
- The **mean** wait is 100 kills, which is `1/p`. That is what "1% means 100 kills" is really about. Week 7 derives it properly from the geometric distribution.
- The **95th percentile** wait is 299 kills. One player in 20 waits longer than this.

The mean is higher than the median because a small number of very unlucky players wait a very long time, and they pull the average up. When a player says "it took me 400 kills", they are not lying and the game is not broken. They are in the tail.

### Why 63% again and again

Now compare drop rates. In each row, `n` is set to `1/p`, the "expected" number of attempts.

| Drop rate p | Kills n = 1/p | Chance of at least one after n | Kills for 50% | Kills for 95% | Kills for 99% |
|---|---|---|---|---|---|
| 1/10 | 10 | 65.1% | 7 | 29 | 44 |
| 1/20 | 20 | 64.2% | 14 | 59 | 90 |
| 1/100 | 100 | 63.4% | 69 | 299 | 459 |
| 1/128 | 128 | 63.4% | 89 | 382 | 588 |
| 1/512 | 512 | 63.2% | 355 | 1,533 | 2,356 |
| 1/4096 | 4,096 | 63.2% | 2,839 | 12,270 | 18,861 |

The third column settles near 63.2% for every small drop rate. The reason is a limit you may have seen in MA101's exponential week. As `p` gets small, `(1 − p)^(1/p)` gets closer and closer to `1/e ≈ 0.368`, where `e ≈ 2.718` is the base of natural logarithms. So:

```
P(at least one drop in 1/p attempts) → 1 − 1/e ≈ 63.2%
```

Whatever the drop rate, playing for the "expected" number of attempts gives you about a 63% chance. Not 100%, not 50%. The 63% is a fixed fact about independent rare events.

### Rules of thumb

The same limit gives you mental arithmetic. For small `p`, `ln(1 − p) ≈ −p`, so the kills needed for a target `q` are close to `−ln(1 − q) / p`:

| Target | Exact multiplier `−ln(1 − q)` | Rule of thumb |
|---|---|---|
| 50% of players have it | 0.693 | about 0.7 / p |
| 63% | 1.0 | 1 / p |
| 90% | 2.303 | about 2.3 / p |
| 95% | 2.996 | about 3 / p |
| 99% | 4.605 | about 4.6 / p |

For a 1% drop, 3/p gives 300 kills for 95%, one more than the exact 299. For the whip at 1/512, 3/p gives 1,536 against the exact 1,533. For any rate below about 5%, these multipliers are within a few percent, and you can use them in a meeting without a calculator.

### The visual

Open `examples/w03-drop-curve.html`. The left panel plots the chance of at least one drop against the number of kills. It is a smooth curve that rises steeply and then crawls toward 100% without reaching it. Dashed lines mark 50%, 63.2%, 95% and 99%, with the kill counts printed where the curve crosses them.

The right panel shows 1,000 players as a grid of dots. Drag the kills slider and dots light up as players get their drop. At 100 kills on a 1% drop, the grid is about two-thirds lit. Keep dragging. The last few dark dots hang on long after the curve on the left looks flat, and a counter shows exactly how many players are still dry.

The two views tell different stories on purpose. The curve says "by 300 kills this is basically done". The dot grid says "50 real people are still farming". Both are true. A designer needs to look at both.

Now press "Scale x-axis by p". The x-axis switches to "attempts in units of 1/p". Change the drop rate from 10% to 1% to 1/512. The curve barely moves. That is the 63% result made visible: every small drop rate is the same curve stretched along the x-axis.

### Cross-game recognition

The formula `1 − (1 − p)^n` appears wherever a game repeats an independent chance.

**Old School RuneScape, abyssal whip (1/512 from standard abyssal demons).** After 512 kills, 63.2% of players have the whip. It takes 355 kills for half of them and 1,533 kills to get 95% of players there. The OSRS community has a name for the players past the expected count, "going dry", and the math says a large minority always will.

**Pokémon shiny encounters.** From Generation VI onward, the base chance that a wild encounter is shiny is 1 in 4,096 (it was 1 in 8,192 in Generations II to V). After 4,096 encounters, 63.2% of hunters have seen one. It takes 2,839 encounters for 50% and 12,270 for 95%. The game series also shows the complement rule running the other way. Several newer boosts work by rolling the shiny check more than once per encounter, and the chance per encounter becomes `1 − (4095/4096)^r` for `r` rolls. That is "at least one success in r tries" inside a single encounter.

**Genshin Impact, 5-star characters on the character event wish.** HoYoverse publishes a base 5-star rate of 0.600% per wish, a consolidated rate of 1.600% once guarantees are included, and a guaranteed 5-star within 90 wishes. Suppose the 0.6% base rate simply held on every wish with no guarantee. Then the chance of at least one 5-star in 90 wishes would be `1 − 0.994^90 ≈ 41.8%`. Most players would reach wish 90 empty-handed. The real system avoids that with a hard guarantee, and community-collected wish data show the rate rising in the last stretch before it. HoYoverse does not publish that ramp, so treat it as a community estimate. Week 10 models that pity system and computes the expected number of wishes it produces.

**Group loot.** A party of five each has a personal 1% chance at an item from one boss kill. The chance that at least one of them gets it is `1 − 0.99^5 ≈ 4.9%`. The complement rule works over players as well as over time.

Four contexts, one formula. Whenever you see "at least one" over repeated independent tries, reach for `1 − (1 − p)^n`.

### Eyes-open design judgment

The complement rule changes how you should choose drop rates.

- **Design to the tail, not the mean.** The mean wait is `1/p`, but the players who shape your forums are the ones at `3/p` and `4.6/p`. With a million players farming a 1% drop, about 49,000 are still dry after 300 kills. Decide what wait you can accept for the unlucky 5% or 1%, then set `p` from that. If no player should need more than about 300 kills 95% of the time, `p` has to be at least 1%.
- **Independent rare drops have no ceiling.** After 1,000 kills on a 1% drop, the chance of still being dry is about 0.004%. That sounds like nothing. Among a million players it is about 43 people, and some of them will stream it. If a ceiling matters to you, you need memory (bags, streak bonuses or pity), which weeks 2 and 10 cover.
- **Pity systems are the complement rule's fix.** Genshin's guarantee exists because 41.8% is an unacceptable success rate over a 90-wish budget. Bad-luck protection in many MMOs does the same job for boss loot. Each one trades honesty of the displayed rate for a tail you control.
- **Rarity is also a feature.** A mount that 5% of the server owns after months of farming is valuable because the tail exists. Removing the tail removes the story. Decide whether an item is a reward for effort (control the tail) or a lottery trophy (let the tail run), and tell players which one it is.
- **Show the right number.** A tooltip saying "1% drop rate" invites the 100-kill misreading. Some games show "chance to have it by now" or keep a visible pity counter. Pick the number that matches the decision you want players to make.

The deliberate decision is the tail target. State it as a sentence, for example "95% of players who farm this boss for two hours a week should have the item within a month", convert it to a number of kills, then solve for `p` with `p = 1 − (1 − q)^(1/n)`.

### Check yourself (worked example)

1. A cosmetic drops at 2% per kill. What is the chance of having it after 50 kills? After 150 kills?
2. Using the rule of thumb and then the exact formula, how many kills does a 1-in-200 drop need for 95% of players to have it?
3. A designer wants 90% of players to have an item within 60 kills. What drop rate `p` does that require?

<details>
<summary>Answers</summary>

1. `1 − 0.98^50 ≈ 1 − 0.364 = 63.6%`. `1 − 0.98^150 ≈ 1 − 0.048 = 95.2%`.
2. Rule of thumb: `3 / (1/200) = 600`. Exact: `ln(0.05) / ln(0.995) = −2.996 / −0.005013 ≈ 597.6`, so 598 kills.
3. `(1 − p)^60 = 0.10`, so `1 − p = 0.10^(1/60) ≈ 0.9624`, and `p ≈ 3.8%`. The rule of thumb gives `2.3 / 60 ≈ 3.8%` too.

</details>

## 3. At least one, when the chances differ

The attempts do not have to share one probability. If attempt `i` succeeds with chance `p_i`, independently, then the chance they all fail is the product of the individual failure chances:

```
P(at least one success) = 1 − (1 − p_1)(1 − p_2) ... (1 − p_n)
```

A dungeon has three bosses that can each drop the same rare pattern, at 10%, 5% and 2%. The chance of at least one pattern in one full clear is

```
1 − (0.90 × 0.95 × 0.98) = 1 − 0.8379 = 16.2%
```

Compare with the tempting shortcut of adding, `10% + 5% + 2% = 17%`. Adding overcounts clears where two or three bosses drop it. For small chances the gap is small, which is why the shortcut survives. It grows fast. Adding 100 attempts at 1% gives "100%", which the table in section 2 shows is really 63.4%.

The same rule answers combat questions. A character with a 15% crit chance attacks 8 times in a fight. The chance of at least one crit is `1 − 0.85^8 ≈ 72.8%`. So about 27% of fights have no crit at all. If your class fantasy depends on "you will see crits", that is worth knowing before a playtest tells you.

## 4. What the complement rule does not answer

"At least one" is a special case. The complement rule gives it cheaply because "none" is a single outcome pattern. Other questions are not so tidy.

- **"Exactly two drops in 100 kills"** or **"at least three crits in a fight"** need you to count the ways to place the successes among the attempts. That is the binomial distribution, week 6.
- **"On which kill does the first drop happen?"** is a question about waiting time, and its full distribution, including the mean of `1/p`, is the geometric distribution, week 7.
- **Systems with memory.** The formula assumes every attempt has the same fixed chance, independently. For bags, streak bonuses, and pity timers, `(1 − p)^n` is wrong, and you will need to multiply the changing failure chances step by step, or simulate (week 11).

Use the complement rule when the question is "at least one" and the attempts are independent. For anything else, check which of those two conditions has broken.

## In-class activity (25 minutes)

Work in pairs with a laptop and a spreadsheet.

1. **Build the curve (8 min).** In column A, put kills 1 to 500. In column B, compute `1 − (1 − p)^n` with `p` in a single cell. Plot B against A. Set `p` to 1% and find where the curve crosses 50%, 95% and 99%. Check your results against the table in section 2.
2. **Design from the tail (10 min).** You are designing a rare mount for a boss that players can kill once per day per character. Your producer's target is "90% of players who kill it every day have the mount within 120 days". Compute the drop rate. Then compute how many players out of 200,000 are still dry after 240 days.
3. **Critique (7 min).** Another pair proposes a 0.5% rate "because it is special". Using the same daily cadence, compute when 95% of players will have it. Write two sentences on whether that is acceptable for a mount players can see on each other.

**Expected output:** the spreadsheet with the curve, the computed drop rate and dry-player count, and the two-sentence critique with its numbers.

## Common misconceptions

- **"A 1% drop means I'll have it in 100 kills."** About 63% of players will. The mean is 100 kills, the median is 69, and 5% of players wait longer than 299.
- **"Chances over repeated tries add up."** They do not. Adding gives `n × p`, which passes 100% for large `n`. Use `1 − (1 − p)^n`.
- **"If I'm past the expected count, the game owes me."** For independent rolls, no. Week 2 applies: every attempt is still `p`, and the chance of a drop in the next 100 kills is 63.4% whether you are on kill 1 or kill 400.
- **"Rare means rarely a problem."** A 1-in-25,000 bad-luck streak happens to 40 people in a million.

## Check yourself

1. A rare fish bites with probability 1/300 per cast. How many casts give a 50% chance of catching one? A 99% chance? Use the rules of thumb, then check one exactly.
2. Four players in a raid each have a 3% personal chance at a trinket. What is the chance at least one of them gets it on a given kill?
3. A player has done 150 kills on a 1% drop without success. What is the chance they get it within the next 150 kills? Compare with the chance a fresh player gets it within 150 kills.
4. A gacha shows a 2% rate per pull with no pity. What fraction of players who do 50 pulls get nothing?

<details>
<summary>Answers</summary>

1. 50%: `0.7 × 300 ≈ 210` casts (exact `ln 0.5 / ln(299/300) ≈ 207.6`, so 208). 99%: `4.6 × 300 ≈ 1,380` casts (exact about 1,380).
2. `1 − 0.97^4 ≈ 1 − 0.885 = 11.5%`.
3. Both are `1 − 0.99^150 ≈ 77.9%`. The past 150 kills do not change the next 150, because the attempts are independent.
4. `0.98^50 ≈ 0.364`, so about 36.4% of players get nothing.

</details>

## Lab hook

**Lab 03, The drop-rate calculator** ([`labs/lab03.md`](../labs/lab03.md)). You will build a drop-rate calculator that reports the median, mean, 95th and 99th percentile waits for any `p`, verify it with a 100,000-player simulation, and use it to set drop rates for a small boss table from tail targets supplied by a "producer" brief.

## Sources

- Old School RuneScape Wiki, "Abyssal whip". Drop rate 1/512 from standard abyssal demons (current game, 2026). Kill counts in this lecture are computed from that rate.
- Bulbapedia, "Shiny Pokémon" and "Shiny Charm". Base shiny encounter rate 1/8,192 in Generations II to V and 1/4,096 from Generation VI onward; modern boosts reroll the shiny check.
- HoYoverse, *Genshin Impact* Character Event Wish details (in-game "Details" page, current through version 7.x in 2026; the official event wish notices point players to this page rather than printing the rates). Base 5-star probability 0.600%, consolidated probability 1.600%, guaranteed 5-star within 90 wishes. The late-counter "soft pity" ramp is not published by HoYoverse; it is a community estimate from logged wishes (week 10). The 41.8% figure is a hypothetical computed in this lecture, not a published rate.
- Schreiber, I. (2010). *Game Balance Concepts*, Level 4, "Probability and Randomness". gamebalanceconcepts.wordpress.com.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Chapter on probability.
- The limit `(1 − p)^(1/p) → 1/e` is standard calculus; all table values are computed from the stated formulas.

## Interactive spec: examples/w03-drop-curve.html

**The one insight.** After the "expected" `1/p` attempts, only about 63% of players have the drop, for any small `p`, and a visible tail of players stays dry for three to five times as long.

**Layout.** Two linked panels, stacked on mobile. Left "The curve". Right "The players".

**Left panel.** X-axis kills `n` from 0 to `ceil(5/p)` (or 0 to 5 in units of `1/p` when scaled). Y-axis `P(at least one) = 1 − (1 − p)^n`, 0% to 100%. Horizontal dashed guides at 50%, 63.2%, 95%, 99%, each labelled with the exact kill count `ceil(ln(1 − q)/ln(1 − p))` where the curve crosses it. A vertical cursor at the current `n` with a readout "At n kills: X% have it, Y% still dry". Draw a lighter second line for the naive "n × p" (clamped at 100%) with a label "adding chances (wrong)".

**Right panel.** 1,000 dots in a 40 × 25 grid, one per simulated player. Each player's first-drop kill is pre-sampled from the geometric distribution with a seeded RNG (`floor(ln(U)/ln(1 − p)) + 1`, U uniform in (0,1]). A dot is lit if that kill number is at most `n`. Print "Still dry: K of 1,000 (theory: 1000 × (1 − p)^n)". Optional reduced-motion-safe animation "Play" that advances `n`.

**Controls.**
- Drop-rate selector with presets 1/10, 1/20, 1/100 (default), 1/128, 1/512, 1/4096, plus a free numeric input (0.0001 to 0.5).
- Kills slider `n`, default 100 so the first screen shows 63.4% and roughly 366 dark dots.
- Toggle "Scale x-axis by p" that relabels the x-axis in units of `1/p`, so all presets draw the same curve.
- Button "New players" (reseed).
All controls keyboard operable; slider supports arrow and page keys.

**Summary strip under both panels.** For the current `p`: median wait `ceil(ln 0.5 / ln(1 − p))`, mean wait `1/p`, 95th percentile `ceil(ln 0.05 / ln(1 − p))`, 99th percentile `ceil(ln 0.01 / ln(1 − p))`.

**Test values (must match).**

| p | n | P(at least one) | Median | 95th pct | 99th pct |
|---|---|---|---|---|---|
| 1/100 | 100 | 63.40% | 69 | 299 | 459 |
| 1/100 | 299 | 95.05% | 69 | 299 | 459 |
| 1/10 | 10 | 65.13% | 7 | 29 | 44 |
| 1/512 | 512 | 63.25% | 355 | 1,533 | 2,356 |
| 1/4096 | 4096 | 63.22% | 2,839 | 12,270 | 18,861 |

**Accessibility.** Lit and dark dots differ in lightness and shape (filled vs ring); readouts are live text; respects `prefers-color-scheme` and `prefers-reduced-motion`.
