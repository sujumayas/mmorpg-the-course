# MA102 · Week 02 — Independent events: the gambler's fallacy in loot

**Why this matters:** Players are sure they are "due" for a drop after a long dry run, and they are sure the game cheats them after three misses at 80%. Sometimes they are wrong, and sometimes the designer has quietly made them right. You need to know which kind of randomness your system has, because it decides how long droughts last and what players will say about your game.

**You will be able to:**
- Compute the probability that several independent events all happen, using the multiplication rule.
- Compute a conditional probability and use it to test whether two events are independent.
- Compare an independent roll with a "bag" (drawing without replacement) and derive the chance of success on the next try after a dry streak for each.
- Critique a randomness design by predicting the longest droughts it allows and how players will read them.

**Before class:** Ian Schreiber, *Game Balance Concepts* (blog course, 2010), Level 5, "Probability and Randomness Gone Horribly Wrong", the sections on the gambler's fallacy and on how people perceive random sequences. Schreiber & Romero, *Game Balance* (2021), the chapter on probability, the part on cards and drawing without replacement.

**Prerequisites from earlier courses:** [MA102 week 1](w01-sample-spaces-and-events.md) (sample spaces, events, the addition rule). Powers and exponential decay from [MA101](../../MA101-mathematics-for-games-i-algebra-functions-trigon/syllabus.md) week 4.

**Interactive:** [examples/w02-dry-streaks.html](../examples/w02-dry-streaks.html) (built from the spec at the end of this lecture). Keep it open during section 2.

---

## 1. What "independent" means

Last week you combined events that lived on the same grid. This week the question is whether one random result tells you anything about another.

Two events are **independent** if knowing that one happened does not change the probability of the other. Rolling a 20 on one die tells you nothing about a second die. A boss dropping a mount this week tells you nothing about next week's kill, as long as the game rolls each kill fresh.

To make "does not change the probability" precise, you need **conditional probability**. The probability of `A` given `B`, written `P(A | B)`, is the chance that `A` happens when you already know `B` happened. On a sample space, knowing `B` shrinks the space to just the outcomes in `B`. You then ask what fraction of those are also in `A`:

```
P(A | B) = P(A and B) / P(B)
```

- `P(A | B)` is read "probability of A given B".
- `P(A and B)` is the chance both happen.
- `P(B)` must be above zero. You cannot condition on something impossible.

Try it on the 20 by 20 grid from week 1. Let `A` be "the second die is 11 or higher" and `B` be "the first die is 11 or higher". `P(A and B) = 100/400 = 0.25` and `P(B) = 0.5`, so `P(A | B) = 0.25 / 0.5 = 0.5`. That is the same as `P(A)` on its own. Learning the first die told you nothing about the second. That is what independence looks like in numbers.

The formal definition follows. `A` and `B` are independent when

```
P(A | B) = P(A)
```

which, after multiplying both sides by `P(B)`, is the same as the **multiplication rule for independent events**:

```
P(A and B) = P(A) × P(B)
```

The rule extends to any number of independent events. The chance that `n` independent events all happen is the product of their chances.

### Three quick uses

**Combos.** A fighter needs three hits in a row, each 80% and rolled independently, to finish a combo. The chance is `0.8 × 0.8 × 0.8 = 0.512`. A combo built from three "reliable" steps fails almost half the time. Designers who tune each step in isolation are regularly surprised by this.

**Dry runs.** A boss drops a trinket 10% of the time. The chance of 10 kills in a row with no trinket is `0.9^10 ≈ 0.349`. About one player in three who does ten kills walks away with nothing.

**Streaks of bad luck.** With an 80% hit chance, three misses in a row has a chance of `0.2^3 = 0.008`, less than 1%. That sounds rare. But over 100 shots in a campaign, the chance that a run of three misses happens **somewhere** is about 47%. Rare per attempt is not rare per player. Section 3 comes back to this.

### When events are not independent

Independence is a property of how the system works, not of randomness in general. Draw a card from a 30-card deck, and you change the deck. The next draw is still random, but its probabilities now depend on what came before. That is **dependence**, and the gambler's fallacy only makes sense once you can tell the two situations apart.

## 2. Worked example: am I due for the drop?

### The hook

In *XCOM 2* (Firaxis, 2016) and its *War of the Chosen* expansion (2017), players famously miss shots the game displayed at 80% or 90% and conclude the dice are rigged. What many players do not know is that on the easier difficulties the game really is rigged, in their favour. The *War of the Chosen* aim-calculation script tracks each soldier's **miss streak**. Once a shot's base chance clears a threshold (the code comment gives 50), each consecutive miss that turn adds a bonus to the next shot, up to a cap. The same code also tracks alien hit streaks and lowers the aliens' chances after consecutive hits.

Why would a studio write code to make the displayed number less true? Because under honest, independent rolls, a soldier who just missed is exactly as likely to miss again, and players experience that as unfair. The designers chose to make the gambler's intuition partly correct.

That raises the question for this worked example. If a player has gone dry for many attempts, is the next attempt more likely to succeed? The answer depends entirely on how the system stores randomness, and you can compute it.

### The model

Compare two systems with the same long-run success rate `p`.

**Independent roll.** Each attempt succeeds with probability `p`, rolled fresh.

```
P(k failures in a row)                 = (1 − p)^k
P(success on attempt k+1 | k failures) = p
```

The second line is the gambler's fallacy in one equation. Condition on any history you like. The next attempt is still `p`. The first line tells you how often long dry runs happen, and they happen often.

**Bag of N tickets.** Put `N` tickets in a bag, exactly one of them a winner, so `p = 1/N`. Draw without putting tickets back. When the bag is empty, refill it.

```
P(success on draw k+1 | k failures since the bag was filled) = 1 / (N − k)
```

After `k` losing draws, `N − k` tickets remain and one is the winner. Each failure makes the next draw more likely to win, and after `N − 1` failures the next draw is certain. In a bag, the player **is** due.

- `p` is the success chance per attempt, the same long-run rate in both systems.
- `k` is the number of failures since the last reset.
- `N` is the bag size.

### Numbers you can check

Take `p = 10%`, so the bag has 10 tickets.

| Failures so far (k) | Chance of k failures in a row (independent) | Next attempt succeeds (independent) | Next draw succeeds (bag of 10) |
|---|---|---|---|
| 0 | 100% | 10% | 10.0% (1 of 10) |
| 1 | 90% | 10% | 11.1% (1 of 9) |
| 3 | 72.9% | 10% | 14.3% (1 of 7) |
| 5 | 59.0% | 10% | 20.0% (1 of 5) |
| 7 | 47.8% | 10% | 33.3% (1 of 3) |
| 9 | 38.7% | 10% | 100% (1 of 1) |
| 20 | 12.2% | 10% | impossible within one bag |
| 30 | 4.2% | 10% | impossible |

Read the columns in pairs.

The second and third columns belong to the independent roll. A run of 20 failures happens to one player in eight (`0.9^20 ≈ 0.122`). A run of 30 still happens to about one in 24 (`0.9^30 ≈ 0.042`). And after all that bad luck, the next attempt is exactly 10%, no more.

The last column belongs to the bag. Its chances climb, and it never allows 10 failures in a row within one bag. Across a refill, the worst case is a winner drawn first in one bag and last in the next, which leaves 18 failures between two wins. That is the **maximum drought**. The independent roll has no maximum at all.

Both systems pay out 10% of the time in the long run. What differs is the **shape** of the experience, and that shape is what players remember.

### The visual

Open `examples/w02-dry-streaks.html`. It simulates 1,000 players making 60 attempts each and draws every player's history as a thin row of cells, with successes lit.

The left panel shows the rows. Under "Independent", you see clumps of successes and long dark gaps, some longer than 30 cells. Switch to "Bag" and the rows become regular, with no gap longer than 18.

The right panel answers the gambler's question with data. Pick a streak length `k` with the slider. The simulation finds every moment, across all players, where someone had just failed `k` times in a row, and reports what fraction of the **next** attempts succeeded. Under "Independent" the bar sits at 10% for every `k`, within simulation noise. Under "Bag" it climbs along the curve `1/(10 − k)` when `k` counts failures since the bag was refilled. A streak that crosses a refill resets the count, so the observed bars sit a little off that curve.

The two views make one point together. The left panel shows why players feel due. Long droughts are common, and they look like they must be building toward something. The right panel shows that, under independent rolls, nothing is building. The feeling is real. The debt is not.

### Cross-game recognition

Once you ask "is the next attempt conditioned on the past?", you find both systems all over the place.

**Tetris (Guideline games).** Modern Tetris games that follow the Tetris Guideline use the "Random Generator", often called the 7-bag. The seven pieces are shuffled into a bag and dealt out in that order, then a new bag is shuffled. It is our bag model with `N = 7`. Each piece still appears one time in seven over the long run, but the longest possible gap between two I pieces is 12 other pieces. Under independent rolls, a player could wait 30 pieces for an I, and the Guideline chose to rule that out. The randomizer has a known origin in *The New Tetris*, which used a larger bag.

**Hearthstone (constructed decks).** A deck has exactly 30 cards, at most two copies of a normal card and one of a legendary. Drawing is drawing without replacement. If you have one legendary in the deck and have drawn `k` cards without seeing it, the chance your next draw is that legendary is `1/(30 − k)`. A player who says "it has to come soon" is reasoning correctly. The deck is a bag.

**XCOM 2, again.** The miss-streak bonus is a third design, somewhere between the two. The roll is still random on every shot, but the chance rises with each failure and resets on success. In this course that family goes by the name **streak-dependent chance**. Week 10 studies its best-known relative, the pseudo-random distribution used for critical strikes in *Dota 2*, and computes exactly how much it shortens droughts.

Three games, one question. Does this system remember? A deck remembers. A bag remembers. A streak bonus remembers. A fresh independent roll never does.

### Eyes-open design judgment

Which system should your drop, crit or hit roll use? Each choice buys something and costs something.

- **Independent rolls are honest and simple.** The displayed number is the true number on every attempt. They are easy to explain, easy to compute in a spreadsheet, and need no stored state. The cost is droughts with no ceiling. In a game with millions of players, some players will go ten times the expected number of attempts without the item, and they will post about it.
- **Bags cap droughts, but they are predictable.** Once players learn the bag size, they count. A Tetris player who has seen six different pieces knows the seventh. In a competitive game that is a skill. In a loot system it can be an exploit, for example if a player can see or reset the bag state.
- **Where the memory lives is a design decision.** A bag or streak counter must be stored somewhere. Per player, per character, per boss, or per server all give different behaviour. A server-wide bag for a rare mount means the first players to kill the boss drain the winners, and players who arrive later face worse odds. A per-player counter needs to survive logouts and patches.
- **Streak bonuses break the displayed number.** XCOM 2's help on easier difficulties means the shown 70% is not the chance on the second or third shot. That can be a kindness. It also means players who learn the rule will make different decisions, and players on the hardest mode will feel the change. Decide whether the tooltip should tell the truth.
- **Players will believe in memory either way.** If you use independent rolls, expect the gambler's fallacy and plan communication around it. If you add memory, you are designing for the fallacy, which is legitimate. Do it on purpose.

The deliberate decision is how long the worst-case drought should be, and for whom. Independence says "unbounded". A bag says "N − 1 within one bag, 2N − 2 across a refill". A streak bonus says "short, and adjustable". Pick the number, then pick the system.

### Check yourself (worked example)

1. A crafting attempt succeeds 25% of the time, rolled independently. A player has failed 6 times. What is the chance the 7th attempt succeeds? What was the chance of failing 6 in a row in the first place?
2. The same crafting system is changed to a bag of 4 tickets with one success. What is the chance of success on the next draw after 2 failures since the last refill? What is the longest possible run of failures between two successes?
3. A designer wants the longest drought on a 5% drop to be 38 kills. What bag size does that imply, and is the long-run rate still 5%?

<details>
<summary>Answers</summary>

1. 25%, because the attempts are independent. The chance of 6 failures in a row was `0.75^6 ≈ 0.178`, about 17.8%.
2. `1/(4 − 2) = 50%`. The longest run is `2 × 4 − 2 = 6`, a success first in one bag and last in the next.
3. A 5% rate means one winner in 20 tickets. The longest run across a refill is `2 × 20 − 2 = 38`, so a bag of 20 matches the target, and the long-run rate is exactly 1 in 20 = 5%.

</details>

## 3. Why random sequences look rigged

The gambler's fallacy is the belief that past independent results change the chances of the next one, so that after many failures a success is "due". It has a twin, the **hot hand** belief, that a success makes another success more likely. Both come from the same place. People expect short random sequences to look like the long-run average, and real random sequences are much streakier than that.

Schreiber's Level 5 reading describes the classic demonstration. Ask people to write down a made-up sequence of coin flips and they switch between heads and tails far more often than a real coin does. They avoid long runs because long runs "don't look random". Real coins produce long runs all the time.

Here are numbers you can check with the interactive's coin mode or a short script. In 100 fair coin flips:

| Run of the same face, at least | Chance it appears somewhere in 100 flips |
|---|---|
| 5 | 97.2% |
| 6 | 80.7% |
| 7 | 54.2% |
| 8 | 31.5% |

A run of five identical flips is almost guaranteed in 100 flips. A run of seven is more likely than not. If your crit chance is 50%, a player who attacks 100 times will very likely see seven crits or seven non-crits in a row, and that player will be sure something is wrong.

The design lesson is subtle. Random systems do not feel random to players, because players' sense of randomness is wrong. If you want a system to **feel** fair, pure independence may not be the best tool, even though it is the most honest one. This is the reason bags, streak bonuses and pity timers exist, and the rest of this course gives you the tools to build them with exact control.

## 4. Accidental dependence in code

Independence is also an implementation property. Two events are only independent if the code rolls them separately.

Here is a real class of bug. A programmer writes the hit handler with one random number:

```
r = random()            # uniform between 0 and 1
crit = (r < 0.20)       # 20% crit chance
drop = (r < 0.05)       # 5% chance to drop a trophy on hit
```

It looks fine. Each line gives the right chance on its own. But both events are decided by the same `r`. Every roll below 0.05 is also below 0.20, so **every trophy drop comes with a crit**. The chance of both is 5%, not `0.2 × 0.05 = 1%`. Players will notice within a day that trophies only drop on crits, and they will build theories about it.

The fix is to roll each event separately, `crit = random() < 0.20` and `drop = random() < 0.05`, with separate calls. In networked games there is a related trap. If client and server share a seeded random stream and consume numbers in different orders, events that should be independent can become linked or predictable. CS202 and MMO309 return to this.

You can test for independence with data. Log many attacks. Compute `P(drop | crit)` and `P(drop | no crit)` from the log. If the system is independent, both should be close to `P(drop)`. In the buggy version, `P(drop | crit) = 0.05 / 0.20 = 25%` and `P(drop | no crit) = 0`. That gap is impossible to miss once you look.

## In-class activity (25 minutes)

Work in groups of three. You need a deck of ordinary playing cards, a d10 (or an app), and a laptop.

1. **Two systems (8 min).** One person runs an independent 10% drop by rolling a d10, where a 10 is the drop. Another runs a bag of 10 using ten cards, one of them an ace, shuffled and drawn without replacement, then reshuffled when empty. Each makes 40 attempts and writes the sequence of successes and failures.
2. **Measure droughts (5 min).** For each sequence, write the length of every run of failures. Record the longest drought in each.
3. **Condition (7 min).** Pool the class data on the board. For all moments where a system had just failed at least 5 times in a row, count how often the next attempt succeeded. Compare the two systems with the table in section 2.
4. **Judge (5 min).** Your team is designing a rare crafting reagent that drops at 2%. Write two sentences recommending independent rolls or a bag, naming the longest drought each would allow and the player behaviour you expect.

**Expected output:** a sheet with both sequences, the longest drought in each, the pooled conditional frequencies, and the two-sentence recommendation.

## Common misconceptions

- **"I've failed so many times that I'm due."** Only if the system remembers. For independent rolls, the next attempt has the same chance whatever the history. For decks, bags and streak systems, the claim can be true, and you can compute by how much.
- **"Low probability per attempt means it won't happen to anyone."** Multiply by attempts and players. A 1-in-125 streak happens to thousands of players a day in a large game.
- **"Two correct chances in code make correct combined behaviour."** Only if they use separate random numbers. Reusing one roll links the events.
- **"Independent means evenly spread."** Independent sequences are clumpy. Evenly spread sequences come from systems with memory.

## Check yourself

1. A quest needs you to win three independent coin-flip mini-games in a row. What is the chance you succeed on a given try? What is the chance you fail 4 tries in a row?
2. A game logs 10,000 kills. 2,000 were crits. 400 kills dropped a gem, and 80 of those were crits. Compute `P(gem | crit)` and `P(gem)`. Are gem drops independent of crits?
3. You have a 30-card deck with two copies of a card and have drawn 10 cards without either copy. What is the chance the next card is one of them?
4. An MMO uses a shared server-wide bag of 100 tickets for a rare mount, one of them the mount. Explain who benefits and who loses compared with independent 1% rolls.

<details>
<summary>Answers</summary>

1. `0.5^3 = 0.125`. Failing a try has chance `0.875`, so four failures in a row is `0.875^4 ≈ 0.586`.
2. `P(gem | crit) = 80 / 2000 = 4%`. `P(gem) = 400 / 10000 = 4%`. They are equal, so the data is consistent with independence.
3. 20 cards remain and 2 are copies, so `2 / 20 = 10%`.
4. Players who kill the boss while the bag is fresh face roughly 1% at first, and the chance rises as others drain losing tickets. After someone wins the mount, everyone faces up to 99 guaranteed losses until the refill. Players who kill often and early gain. Players who arrive just after a win lose. Independent rolls give every kill the same 1%, which is fairer across players but has no drought cap.

</details>

## Lab hook

**Lab 02, Streak detective** ([`labs/lab02.md`](../labs/lab02.md)). You will simulate independent, bag and streak-bonus systems with the same long-run rate, measure the distribution of droughts, and test a supplied kill log for accidental dependence between two events. The deliverable is a short report with your plots and a recommendation.

## Sources

- Firaxis Games, *XCOM 2: War of the Chosen*, script `X2AbilityToHitCalc_StandardAim.uc` as distributed with the official modding SDK and mirrored in the X2WOTCCommunityHighlander repository on GitHub (2017 release and later). The code tracks unit miss and hit streaks, applies a miss-streak adjustment to XCOM shots above a minimum base chance (commented as 50), caps the assisted value, and its comments state the adjustments apply on easy and normal difficulty. Per-difficulty values live in configuration files and are not quoted here.
- Tetris Wiki, "Random Generator". Seven-piece bag dealt in shuffled order, maximum of 12 pieces between two I pieces, origin in *The New Tetris*, used in Tetris Guideline games.
- Hearthstone Wiki (hearthstone.wiki.gg), "Deck". 30-card constructed decks, at most two copies of a card and one of a legendary (current rules as of 2026, with noted card-specific exceptions).
- Schreiber, I. (2010). *Game Balance Concepts*, Level 5, "Probability and Randomness Gone Horribly Wrong". gamebalanceconcepts.wordpress.com. Source of the made-up-coin-flip demonstration, paraphrased.
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Chapter on probability, cards and drawing without replacement.
- Run-length and drought probabilities in this lecture are computed by exact dynamic programming over the stated models and can be reproduced with the lab's starter script.

## Interactive spec: examples/w02-dry-streaks.html

**The one insight.** Long dry streaks are common under independent rolls, yet after any streak the next attempt is still exactly `p`. A bag with the same long-run rate makes the player truly "due" and caps the drought.

**Layout.** Two linked panels, stacked on mobile. Left panel "What players see". Right panel "What happens next".

**Simulation.** 1,000 simulated players, 60 attempts each, seeded RNG (seed shown, button "New seed"). Success probability `p` from the slider. Three systems:
- Independent: success if `rand() < p`.
- Bag: `N = round(1/p)` tickets, one winner, shuffled per player; refill when empty.
- Streak bonus: chance on attempt = `min(1, p + b × k)` where `k` is failures since the last success and `b` is a bonus slider (0 to 10 percentage points, default 5). Label this "hypothetical streak bonus, see week 10".

**Left panel.** Draw the first 60 players as rows of 60 small cells (successes filled, failures empty). Below, a histogram of the longest drought per player across all 1,000 players, with the mean and maximum printed. Theoretical overlays: bag maximum `2N − 2`.

**Right panel.** Slider `k` from 0 to 30. For the selected system, scan all histories for positions where exactly `k` consecutive failures have just occurred (since the last success or since start), and plot the observed success rate on the next attempt as a bar, with the count of such moments. Overlay the theoretical value as a line across all k:
- Independent: `p`.
- Bag: `1/(N − j)` where `j` is failures since the last refill. Because j and k differ across refills, plot the theoretical curve for "failures since the bag was filled" and note in small text that the observed bar can differ slightly when streaks cross a refill.
- Streak bonus: `min(1, p + b × k)`.
Show "n/a" when fewer than 30 moments exist for that k.

**Controls.** System toggle (Independent / Bag / Streak bonus), slider `p` with preset stops 5%, 10%, 20%, 25% (default 10%), slider `k`, slider `b` (visible only in streak mode), "New seed" button. All keyboard operable.

**Secondary mode "Coin runs".** Button that shows 100 fair flips as a row and highlights the longest run, with the exact table: at least 5 → 97.2%, 6 → 80.7%, 7 → 54.2%, 8 → 31.5% (exact, from dynamic programming), next to the observed frequency over 1,000 simulated sequences.

**Test values (theory lines must match).** With `p = 10%`: independent `P(k failures in a row)` at k = 5, 10, 20, 30 is 59.05%, 34.87%, 12.16%, 4.24%. Bag of 10 next-draw chance at j = 0, 1, 3, 5, 7, 9 is 10.0%, 11.1%, 14.3%, 20.0%, 33.3%, 100%. Bag maximum drought 18. With `p = 25%`, bag of 4, maximum drought 6.

**Accessibility.** Colour plus fill pattern for success cells; reduced motion disables any row-by-row animation; all numbers available as text.
