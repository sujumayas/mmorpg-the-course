# MA102 · Exam bank

This bank holds 66 questions covering all 14 weeks of MA102. Students may use it for practice. The final exam (see [final-exam-brief.md](final-exam-brief.md)) draws questions from the ones tagged **final**, with the numbers changed, so memorizing answers does not help. Knowing the model does.

Every question carries a tag in this form: **[Weeks · type · use]**.

- **Weeks** name the lectures the question depends on.
- **Type** is one of *compute* (apply a lecture model to new numbers), *explain* (say why, using the model), *design* (choose parameters to meet a target) or *critique* (find what is wrong in a claim or design, with numbers).
- **Use** is *final* when the question fits a timed, calculator-only exam, or *practice* when it needs software, long arithmetic or open-ended work better suited to a problem set or review session.

All numbers in the answers were recomputed with `.venv/bin/python` from the models stated in the lectures. Percentages are rounded at the last step. Where a question uses a real game, the fact comes from that week's lecture, which cites its source and version.

## Coverage

| Week | Topic | Questions |
|---|---|---|
| 1 | Sample spaces and events | 1, 2, 3, 4, 15 |
| 2 | Independence and the gambler's fallacy | 5, 6, 7, 8 |
| 3 | Complement rule | 9, 10, 11, 12, 62, 65, 66 |
| 4 | Expected value | 13, 14, 15, 16, 17 |
| 5 | Variance and swingy designs | 18, 19, 20, 21 |
| 6 | Binomial distribution | 22, 23, 24, 25, 26 |
| 7 | Geometric distribution | 17, 27, 28, 29, 30, 31, 65, 66 |
| 8 | Dice sums and the normal curve | 32, 33, 34, 35, 36 |
| 9 | Weighted loot tables | 29, 37, 38, 39, 40, 41, 42, 65 |
| 10 | PRD and pity timers | 43, 44, 45, 46, 47, 49, 65 |
| 11 | Monte Carlo simulation | 48, 49, 50, 51 |
| 12 | Descriptive statistics | 52, 53, 54, 55 |
| 13 | Sampling and confidence | 56, 57, 58, 59, 66 |
| 14 | Hypothesis testing (A/B) | 60, 61, 62, 63, 64 |

Type counts: 41 compute, 8 explain, 8 design, 9 critique. 62 questions are tagged final and 4 practice.

---

## Week 1 · Sample spaces and events

1. **[Week 1 · compute · final]** A check on a d20 succeeds on 13 or higher. Compute the success chance for a plain roll, with advantage (roll two d20, keep the higher), with disadvantage (keep the lower), and with a flat +5 bonus. At this target, is advantage worth more or less than +5?

   <details>
   <summary>Answer and worked solution</summary>

   **Answer:** plain 40%, advantage 64%, disadvantage 16%, +5 65%. Advantage is worth slightly less than +5 here.

   Plain: faces 13 to 20 are 8 of 20, so 40%.

   Advantage fails only when both dice are 12 or lower. That is the corner of `12 × 12 = 144` pairs out of 400. `P = 1 − 144/400 = 1 − 0.36 = 0.64`.

   Disadvantage succeeds only when both dice are 13 or higher, `8 × 8 = 64` pairs. `64/400 = 0.16`.

   +5 needs a die of 8 or higher, 13 faces, so `13/20 = 0.65`.

   Advantage adds 24 points and +5 adds 25. The two agree exactly only at T = 11, and T = 13 is close to that point, so the gap is small.
   </details>

2. **[Week 1 · compute · final]** Roll two fair six-sided dice. Let A be "at least one die shows a 6" and B be "the sum is 10 or more". Count outcomes in the 36-pair sample space to find P(A), P(B), P(A and B) and P(A or B). Check the last with the addition rule.

   <details>
   <summary>Answer and worked solution</summary>

   **Answer:** P(A) = 11/36, P(B) = 6/36, P(A and B) = 5/36, P(A or B) = 12/36 = 1/3.

   A: the pairs with no 6 are `5 × 5 = 25`, so A has `36 − 25 = 11` pairs.

   B: sums 10, 11 and 12 come from (4,6), (5,5), (6,4), (5,6), (6,5), (6,6). That is 6 pairs.

   A and B: every pair in B except (5,5) contains a 6, so 5 pairs.

   Addition rule: `11/36 + 6/36 − 5/36 = 12/36`. Adding without subtracting the overlap would give 17/36 and count five pairs twice.
   </details>

3. **[Week 1 · compute · final]** A chest table has weights Common 45, Uncommon 30, Rare 15, Epic 8, Legendary 2. (a) What is the chance of an Epic or better? (b) A designer adds an "Event token" row with weight 25 and changes nothing else. What is the Legendary chance now? (c) What single edit would have kept the Legendary at its old chance?

   <details>
   <summary>Answer and worked solution</summary>

   **Answer:** (a) 10%. (b) 1.6%, down from 2%. (c) Take the 25 weight out of another row, for example Common 45 to 20, so the total stays 100.

   (a) The total is 100. Epic and Legendary are mutually exclusive rows, so add them. `(8 + 2)/100 = 10%`.

   (b) The new total is 125. `2/125 = 1.6%`. Every existing row shrank by the factor `100/125 = 0.8`, including rows nobody touched.

   (c) Probabilities are shares of the total. Keep the total at 100 and every untouched row keeps its chance. Taking the weight from Common changes only Common, which is the row the designer chooses to pay for the new item.
   </details>

4. **[Week 1 · critique · final]** A spell tooltip reads "15% chance to stun and 15% chance to slow: 30% chance to apply a status effect." The two effects are rolled separately and independently. (a) What is the true chance of at least one effect? (b) A programmer implements both with one random number `r`, as `stun = r < 0.15` and `slow = r < 0.15`. What is the chance of at least one effect now, and what will players notice?

   <details>
   <summary>Answer and worked solution</summary>

   **Answer:** (a) 27.75%. (b) 15%, and every stun comes with a slow.

   (a) Both effects happen with chance `0.15 × 0.15 = 0.0225`. The addition rule gives `0.15 + 0.15 − 0.0225 = 0.2775`. The tooltip counted the both-effects case twice.

   (b) With one shared `r`, the two events are the same event. At least one happens exactly when `r < 0.15`, so 15%. The chance of both is also 15%, not 2.25%. Players will see that the two effects always arrive together and never alone, and they will report it within a day. Roll each effect with its own random number.
   </details>

## Week 2 · Independence and the gambler's fallacy

5. **[Week 2 · compute · final]** A crafting attempt succeeds 20% of the time. (a) Rolled independently, a player has failed 8 times in a row. What is the chance the 9th attempt succeeds, and what was the chance of 8 failures in a row? (b) The system is changed to a bag of 5 tickets with one success, refilled when empty. After 3 failures since the last refill, what is the chance the next draw succeeds? What is the longest possible run of failures between two successes?

   <details>
   <summary>Answer and worked solution</summary>

   **Answer:** (a) 20%; 16.8%. (b) 50%; 8 failures.

   (a) Independent attempts have no memory, so the 9th attempt is 20% whatever came before. The chance of the streak itself is `0.8^8 ≈ 0.168`, about one player in six.

   (b) After 3 losing draws, 2 tickets remain and one wins, so `1/(5 − 3) = 1/2`. The worst case is a success drawn first in one bag and last in the next, leaving `4 + 4 = 8` failures between them, which is `2N − 2` with N = 5.
   </details>

6. **[Week 2 · critique · final]** A telemetry log has 50,000 attacks. 12,500 were crits. A rare "shatter" proc fired 1,000 times, and 600 of those were on crits. The design says crit and shatter are independent. (a) Compute P(shatter), P(shatter | crit) and P(shatter | no crit). (b) Are the events independent? (c) The lecture's shared-random-number bug would give a specific value for P(shatter | no crit). Is this log that bug, or something else?

   <details>
   <summary>Answer and worked solution</summary>

   **Answer:** (a) 2%, 4.8%, 1.07%. (b) No. A crit makes a shatter about 4.5 times as likely. (c) It is not the pure shared-roll bug, which would give P(shatter | no crit) = 0.

   (a) `P(shatter) = 1000/50000 = 2%`. `P(shatter | crit) = 600/12500 = 4.8%`. Non-crit attacks number 37,500 and carry 400 shatters, so `P(shatter | no crit) = 400/37500 ≈ 1.07%`.

   (b) Independence would put both conditional values near 2%. They differ by a factor of `4.8/1.07 ≈ 4.5` on thousands of attacks, far more than noise.

   (c) If one number `r` decided both, with shatter at `r < 0.02` and crit at `r < 0.25`, every shatter would be a crit, so no shatters would appear on non-crits. Here 400 do. The likely cause is code that raises the shatter chance when the attack crits, a conditional rule written as a separate roll. Look for a chance that reads the crit flag.
   </details>

7. **[Week 2 · explain · final]** Two players claim they are "due". Player 1 has killed abyssal demons 600 times without an abyssal whip (Old School RuneScape, 1/512 per kill, rolled independently). Player 2 has drawn 10 cards from a 30-card Hearthstone deck without seeing either copy of a two-copy card. For each, compute the chance the next attempt succeeds and compare it with the chance at the start. Explain in two sentences why one player is right and one is wrong.

   <details>
   <summary>Answer and worked solution</summary>

   **Answer:** Player 1's next kill is still 1/512 ≈ 0.20%, the same as at kill 1. Player 2's next draw is 2/20 = 10%, up from 2/30 ≈ 6.7% at the first draw.

   The whip roll is independent, so `P(success on the next kill | 600 failures) = p`. The deck is drawn without replacement, so each miss removes a non-copy card and leaves the two copies among fewer cards.

   Player 1 is committing the gambler's fallacy, because an independent roll has no memory. Player 2 is right, because a deck is a bag and a bag remembers what has already left it.
   </details>

8. **[Week 2 · design · final]** A rare crafting reagent should drop about 8% of the time, and design says no player should ever fail more than 30 times in a row. (a) Can independent rolls meet the drought rule? (b) Propose a bag with one winner and give its rate and maximum drought. (c) A teammate proposes a bag of 25 tickets with 2 winners (exactly 8%). What is its maximum drought, and does it meet the rule?

   <details>
   <summary>Answer and worked solution</summary>

   **Answer:** (a) No. (b) A bag of 12 gives 8.33% with a maximum drought of 22, or a bag of 13 gives 7.69% with a maximum of 24. Both meet the rule. (c) The 2-in-25 bag allows 46 failures in a row and fails the rule.

   (a) Independent rolls have no ceiling. The chance of 31 failures in a row at 8% is `0.92^31 ≈ 7.5%`, so many players would break the rule.

   (b) One winner in N tickets gives rate `1/N` and maximum drought `2N − 2`. N = 12 gives 22 and N = 13 gives 24. Neither hits 8% exactly. Pick based on whether a slightly generous or slightly stingy rate matters more.

   (c) With two winners, the worst case puts both winners at the start of one bag (positions 1 and 2) and both at the end of the next (positions 24 and 25). The gap is `23 + 23 = 46` failures, which is `2N − 4`. Exact rate is not worth doubling the worst drought.
   </details>

## Week 3 · Complement rule

9. **[Week 3 · compute · final]** A rare mount drops at 1 in 250 per kill, rolled independently. (a) What fraction of players have it after 250 kills? (b) Give the exact kill counts by which 50%, 95% and 99% of players have it. (c) Compare each with the rule of thumb (0.7/p, 3/p, 4.6/p).

   <details>
   <summary>Answer and worked solution</summary>

   **Answer:** (a) 63.3%. (b) 173, 748 and 1,149 kills. (c) Rules of thumb give 175, 750 and 1,150.

   (a) `1 − (249/250)^250 = 1 − 0.3671 ≈ 0.633`. This is the 63% that appears for any small drop rate after `1/p` attempts.

   (b) Solve `n ≥ ln(1 − q)/ln(1 − p)` with `ln(0.996) = −0.004008`.
   - 50%: `ln 0.5 / ln 0.996 = 172.9`, so 173.
   - 95%: `ln 0.05 / ln 0.996 = 747.4`, so 748.
   - 99%: `ln 0.01 / ln 0.996 = 1149.0`, so 1,149.

   (c) `0.7 × 250 = 175`, `3 × 250 = 750`, `4.6 × 250 = 1,150`. All within 2 kills, because p = 0.4% is small.
   </details>

10. **[Week 3 · compute · final]** A dungeon has three bosses that can each drop the same recipe, at 8%, 4% and 3%, independently. What is the chance of at least one recipe per full clear? Why is the quick answer of 15% wrong, and in which direction?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** 14.3%. Adding gives 15%, which is too high.

    All three fail with chance `0.92 × 0.96 × 0.97 = 0.8567`. At least one succeeds with chance `1 − 0.8567 = 0.1433`.

    Adding the three chances counts clears where two or three bosses drop the recipe more than once. The overcount is small at these rates and grows fast as rates rise.
    </details>

11. **[Week 3 · design · final]** A producer wants 95% of players who farm a boss to have its weapon within 40 kills. (a) What per-kill drop rate does that need? (b) With that rate, what fraction of players are still dry after 100 kills? In a population of 200,000 farmers, about how many is that?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) p ≈ 7.2%. (b) About 0.056%, roughly 112 players.

    (a) Solve `(1 − p)^40 = 0.05`. Then `1 − p = 0.05^(1/40) = 0.9278`, so `p = 0.0722`. The rule of thumb gives `3/40 = 7.5%`, slightly high because p is not tiny.

    (b) `0.9278^100 ≈ 0.00056`. Multiply by the population: `200,000 × 0.00056 ≈ 112`. The rate meets the 95% target, and there is still a tail of about a hundred players who will post their kill counts.
    </details>

12. **[Week 3 · explain · final]** Explain why a player who kills a boss exactly `1/p` times has about a 63% chance of having the drop, whether p is 1/20, 1/100 or 1/4096. Name the limit involved and say what the result means for a designer who tells players "it takes about 1/p kills".

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** The dry chance after `1/p` attempts is `(1 − p)^(1/p)`, which approaches `1/e ≈ 0.368` as p gets small. So the have-it chance approaches `1 − 1/e ≈ 63.2%`.

    For p = 1/20 the value is `1 − 0.95^20 = 64.2%`, for 1/100 it is 63.4%, and for 1/4096 it is 63.2%. The number barely depends on p because every small drop rate is the same curve stretched along the kill axis.

    For the designer, "about 1/p kills" is the mean, and at the mean over a third of players are still dry. Players at the mean feel behind, and players at `3/p` feel cheated. Quote a percentile, such as "95% of players by about 3/p kills", if you want a number that holds for nearly everyone.
    </details>

## Week 4 · Expected value

13. **[Week 4 · compute · final]** Two weapons: a Greatblade (100 to 160 damage, 3.2 s) and a Swift Dagger (22 to 34 damage, 0.9 s, +20% crit chance while equipped). The character misses 8% of swings, has 10% base crit, and crits deal ×2. (a) Compute tooltip DPS and expected DPS for both. (b) At what total crit chance does the Dagger tie the Greatblade?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) Greatblade tooltip 40.63, expected 41.11. Dagger tooltip 31.11, expected 37.21. (b) The Dagger ties at a total crit chance of 43.6%, a bonus of about +33.6 points.

    (a) Use `expected DPS = (1 − q) × D × (1 + c(m − 1)) / s`.
    - Greatblade: `D = 130`, tooltip `130/3.2 = 40.63`. Expected `0.92 × 130 × 1.10 / 3.2 = 41.11`.
    - Dagger: `D = 28`, tooltip `28/0.9 = 31.11`. Total crit `c = 0.30`. Expected `0.92 × 28 × 1.30 / 0.9 = 37.21`.

    (b) Set `0.92 × 28 × (1 + c) / 0.9 = 41.11`. Then `1 + c = 41.11 × 0.9 / 25.76 = 1.436`, so `c = 0.436`. The ranking matches the tooltip here, but the gap shrank from 9.5 DPS to 3.9 DPS, because the crit multiplier favours the Dagger.
    </details>

14. **[Week 4 · compute · final]** A mob drops 5 gold with probability 0.6, 20 gold with probability 0.3, a 100-gold gem with probability 0.08 and a 1,000-gold relic with probability 0.02. (a) What is the expected gold per kill? (b) What share of it comes from the relic? (c) What is the expected gold from 500 kills?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 37 gold. (b) 54%. (c) 18,500 gold.

    (a) `0.6 × 5 + 0.3 × 20 + 0.08 × 100 + 0.02 × 1000 = 3 + 6 + 8 + 20 = 37`.

    (b) `20/37 ≈ 0.54`. The row seen on one kill in fifty supplies more than half the income, so a small change to the relic moves the economy more than any change to common drops.

    (c) Linearity of expectation gives `500 × 37 = 18,500`.
    </details>

15. **[Weeks 1, 4 · compute · final]** In D&D 5th edition, an attack hits on a d20 roll of 12 or higher (a natural 20 always hits and crits). It deals 2d6 + 4, and on a crit the dice are rolled twice but the +4 is added once. (a) Compute the expected damage per attack. (b) Recompute with advantage. By what percentage does advantage raise expected damage?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 5.30. (b) 8.36, a rise of about 58%.

    (a) Faces 12 to 20 hit, so `P(hit) = 9/20 = 0.45`, of which the natural 20 (0.05) is a crit. Average 2d6 is 7. Every hit deals `7 + 4 = 11` on average, and a crit adds another 7. So `0.45 × 11 + 0.05 × 7 = 4.95 + 0.35 = 5.30`.

    (b) With advantage, `P(hit) = 1 − (11/20)^2 = 0.6975` and `P(crit) = 1 − (19/20)^2 = 0.0975`. Expected damage is `0.6975 × 11 + 0.0975 × 7 = 7.67 + 0.68 = 8.36`. The ratio is `8.36 / 5.30 = 1.58`. Advantage is strong here because T = 12 sits near the middle, where week 1 showed advantage helps most.
    </details>

16. **[Week 4 · critique · final]** In classic World of Warcraft, the Arcanite Reaper tooltip shows "153 - 256 Damage", "Speed 3.80" and "(53.8 damage per second)". A player says, "My character does 53.8 DPS with this axe." List which random factors the 53.8 averages over and which it leaves out, and say whether the player's real number is likely higher or lower, and why.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** The 53.8 is `(153 + 256)/2 / 3.8`. It averages over the damage roll only. It leaves out misses, dodges and other avoidance, crits, and any stat bonuses the character adds.

    The tooltip describes the item, not the wielder. Misses multiply by `(1 − q)` and pull the number down. Crits multiply by `1 + c(m − 1)` and push it up. Character bonuses to damage add further. The real number could land on either side, and the player cannot know without the character's miss and crit chances. A character with high crit is usually above the tooltip, and one fighting a target that avoids many attacks is usually below it. The claim is wrong as stated because it treats an item average as a character result.
    </details>

17. **[Weeks 4, 7 · compute · final]** An enhancement attempt costs 200 gold and succeeds with probability 0.4. Failure leaves the item unchanged. (a) What is the expected gold spent to get one success? (b) What fraction of players need more than 5 attempts? (c) Of 10,000 players, how many spend at least 1,200 gold?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 500 gold. (b) 7.8%. (c) About 778 players.

    (a) The number of attempts is geometric with mean `1/0.4 = 2.5`, so the expected cost is `2.5 × 200 = 500`.

    (b) More than 5 attempts means the first 5 fail: `0.6^5 = 0.0778`.

    (c) At least 1,200 gold means at least 6 attempts, which is the same event as (b). `10,000 × 0.0778 ≈ 778`. The average is 500 gold, and nearly 8% of players pay more than twice that. Those players shape the forum's opinion of the system.
    </details>

## Week 5 · Variance and swingy designs

18. **[Week 5 · compute · final]** A hit deals 25 damage, or 2.5 times that on a crit, with crit chance 20%. Compute the mean, variance, standard deviation and coefficient of variation of one hit.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** mean 32.5, variance 225, SD 15, CV 0.46.

    Mean: `25 × (1 + 0.2 × 1.5) = 32.5`.

    Variance: `b² (m − 1)² c(1 − c) = 625 × 2.25 × 0.16 = 225`.

    Check with the table method. Outcomes 25 (probability 0.8) and 62.5 (probability 0.2). `E[X²] = 0.8 × 625 + 0.2 × 3906.25 = 500 + 781.25 = 1281.25`. Then `1281.25 − 32.5² = 1281.25 − 1056.25 = 225`.

    SD `= √225 = 15`. CV `= 15/32.5 = 0.46`.
    </details>

19. **[Week 5 · compute · final]** A Steady weapon deals 30 per hit. A Swingy weapon deals 24 per hit with a 25% chance to crit for ×2, so its mean is also 30. The enemy has 90 HP. (a) How many hits does Steady need? (b) Compute the distribution of hits-to-kill for Swingy and its mean. (c) Which kills faster on average, and by how much?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 3 hits. (b) P(T = 2) = 0.0625, P(T = 3) = 0.5156, P(T = 4) = 0.4219, mean 3.36 hits. (c) Steady, by about 12%.

    (a) `3 × 30 = 90`, exactly enough.

    (b) After n hits with k crits, Swingy has dealt `24(n + k)`. The kill needs `n + k ≥ 4`, since `24 × 3 = 72` falls short and `24 × 4 = 96` is enough.
    - Dead by hit 1: impossible (max 48).
    - Dead by hit 2: needs 2 crits, `0.25² = 0.0625`.
    - Dead by hit 3: needs at least 1 crit, `1 − 0.75³ = 0.5781`.
    - Dead by hit 4: certain.

    So `P(T = 2) = 0.0625`, `P(T = 3) = 0.5781 − 0.0625 = 0.5156`, `P(T = 4) = 0.4219`. Mean `= 2(0.0625) + 3(0.5156) + 4(0.4219) = 3.36`.

    (c) `3.36/3 = 1.12`. Equal mean damage, 12% slower kills, because Swingy usually overkills.
    </details>

20. **[Week 5 · compute · final]** Use the hit from question 18 (CV 0.4615 per hit, hits independent). (a) What is the CV of total damage over a 25-hit fight? (b) How many hits must a fight last before the CV of total damage falls below 5%?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 9.2%. (b) 86 hits.

    (a) Variances of independent hits add, so the CV of the total is `CV / √n = 0.4615 / 5 = 0.092`.

    (b) Solve `0.4615 / √n < 0.05`. Then `√n > 9.23`, so `n > 85.2`, and the smallest whole fight is 86 hits. A raid boss that takes hundreds of hits hides this crit spread almost completely. A 5-hit duel shows it at `0.4615/√5 ≈ 21%`.
    </details>

21. **[Week 5 · design · final]** You want crit builds that all have a mean damage multiplier of 1.2. Design one configuration (crit chance c and multiplier m) with per-hit CV at most 0.20 and one with CV at least 0.50. Give the CV of each and say which one you would give a PvP class and why.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** Many answers work. Any pair with `c(m − 1) = 0.2` has mean multiplier 1.2. Examples: c = 50%, m = 1.4 has CV 0.167. c = 10%, m = 3 has CV 0.50. c = 5%, m = 5 has CV 0.73.

    Use `CV = (m − 1)√(c(1 − c)) / (1 + c(m − 1))`.
    - c = 0.5, m = 1.4: `0.4 × 0.5 / 1.2 = 0.167`.
    - c = 0.4, m = 1.5: `0.5 × 0.490 / 1.2 = 0.204`, just over the limit, a common near miss.
    - c = 0.1, m = 3: `2 × 0.3 / 1.2 = 0.50`.

    For PvP, where fights are short and a spike can decide them, the low-CV build is the safer choice. Frequent, small crits keep the average and remove most one-shot moments. The high-CV build suits long PvE fights, where week 5's `1/√n` rule averages the spread away and players still get the rare big number.
    </details>

## Week 6 · Binomial distribution

22. **[Week 6 · compute · final]** A rogue attacks 12 times per fight with a 15% crit chance, independently. Compute P(0 crits), P(exactly 2 crits), P(3 or more crits), and the mean and SD of the crit count. What is the most likely number of crits?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** P(0) = 14.2%, P(2) = 29.2%, P(≥ 3) = 26.4%, mean 1.8, SD 1.24. The most likely count is 1.

    `P(K = k) = C(12, k) 0.15^k 0.85^(12 − k)`.
    - `P(0) = 0.85^12 = 0.1422`.
    - `P(1) = 12 × 0.15 × 0.85^11 = 0.3012`.
    - `P(2) = 66 × 0.0225 × 0.85^10 = 0.2924`.
    - `P(≥ 3) = 1 − 0.1422 − 0.3012 − 0.2924 = 0.2642`.

    Mean `12 × 0.15 = 1.8`. SD `√(12 × 0.15 × 0.85) = √1.53 = 1.24`. The mode is the whole number just below `(n + 1)p = 1.95`, which is 1, matching P(1) as the largest value.
    </details>

23. **[Week 6 · compute · final]** A raid of 30 players each has an independent 3% chance to receive a mount from a boss. Compute the expected number of mounts, P(nobody gets one), P(exactly one) and P(two or more). What does this say about the design "about one mount per kill"?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** expected 0.9. P(0) = 40.1%, P(1) = 37.2%, P(≥ 2) = 22.7%.

    `P(0) = 0.97^30 = 0.4010`. `P(1) = 30 × 0.03 × 0.97^29 = 0.3721`. `P(≥ 2) = 1 − 0.4010 − 0.3721 = 0.2269`.

    The average is close to one, but 40% of kills drop nothing, and over a fifth drop two or more. If the design intent is one mount per kill, build that rule in (one guaranteed mount, then pick a winner) rather than relying on independent personal rolls.
    </details>

24. **[Week 6 · critique · final]** A player with 20% crit posts "0 crits in 40 attacks, the RNG is bugged". (a) How likely is that streak if the system works? (b) The game logs 2 million 40-attack sequences per day. How many players should see it daily? (c) Write the two-sentence reply a community manager should post.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) `0.8^40 ≈ 0.000133`, about 1 in 7,500. (b) About 266 per day. (c) See below.

    (b) `2,000,000 × 0.000133 ≈ 266`.

    (c) "With a 20% crit chance, going 40 attacks without a crit happens about once in 7,500 tries, which across our player base is a couple of hundred players every day. We checked our logs and your streak fits the expected rate, but if you see it again on the same setup, send us the combat log so we can check it."

    One report proves nothing. A cluster of reports from one class or one patch, well above 266 a day, is a real bug signal.
    </details>

25. **[Week 6 · explain · final]** For each count, say whether it is binomial. If not, name the condition that fails. (a) The number of 10 raiders who win an independent 5% pet roll. (b) The number of crits you land before a boss dies. (c) The number of crits in 8 attacks under Dota 2's pseudo-random distribution. (d) Crits in 8 attacks where a buff doubles crit chance for the last 3. (e) Legendary cards in a 5-card draw from a 30-card deck.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:**
    - (a) Binomial, n = 10, p = 0.05.
    - (b) Not binomial. The number of trials is not fixed, because the fight ends when the boss dies.
    - (c) Not binomial. Trials are not independent, because each non-proc raises the next chance.
    - (d) Not binomial. The probability is not the same on every trial.
    - (e) Not binomial. Drawing without replacement makes trials dependent, and the chance changes after each card.

    The binomial needs a fixed n, two outcomes, the same p, and independence. Most interesting game systems break one of them on purpose.
    </details>

26. **[Week 6 · compute · final]** A fighter makes 10 attacks. Each deals 50 damage, or 100 on a crit, with crit chance 30%, independently. The enemy has 650 HP. (a) What is the expected total damage? (b) What is the chance the enemy dies within the 10 attacks? (c) What lesson does this give about "expected damage equals enemy HP"?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 650. (b) 61.7%. (c) Matching the mean to the HP fails often.

    (a) `50 × (10 + 10 × 0.3 × 1) = 50 × 13 = 650`.

    (b) Total damage is `50(10 + K)` with K crits. The kill needs `10 + K ≥ 13`, so `K ≥ 3`. With `K ~ Binomial(10, 0.3)`, `P(K ≤ 2) = 0.0282 + 0.1211 + 0.2335 = 0.3828`, so `P(K ≥ 3) = 0.6172`.

    (c) When expected damage equals the HP exactly, the kill still fails 38% of the time. The SD of total damage is `50 × √(10 × 0.3 × 0.7) = 72.5`, a spread large enough that the threshold sits in the middle of the distribution. Tune content to a percentile of damage, not the mean.
    </details>

## Week 7 · Geometric distribution

27. **[Week 7 · compute · final]** A pet drops at 1 in 300 per kill. Compute the mean wait, the median, the 95th percentile and the SD. Then compare P(the drop comes on kill 1) with P(it comes on exactly kill 300).

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** mean 300, median 208, 95th percentile 898, SD 299.5. P(X = 1) = 0.333%, P(X = 300) = 0.123%.

    Median `= ceil(ln 0.5 / ln(299/300)) = ceil(207.6) = 208`. 95th `= ceil(ln 0.05 / ln(299/300)) = ceil(897.2) = 898`. SD `= √(1 − p)/p = √(0.99667) × 300 = 299.5`.

    `P(X = 1) = p = 0.00333`. `P(X = 300) = (299/300)^299 × p = 0.3685 × 0.00333 = 0.00123`. Kill 1 is the single most likely kill for the drop. Kill 300 needs 299 failures first.
    </details>

28. **[Week 7 · compute · final]** A player has opened 80 chests without a 3% rare item. (a) What is the chance they open 50 more without it? (b) How many more chests do they expect to need? (c) A fresh player asks the same two questions. What are their answers?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 21.8%. (b) 33.3 chests. (c) The same, 21.8% and 33.3.

    (a) Memorylessness gives `P(X > 130 | X > 80) = P(X > 50) = 0.97^50 = 0.218`.

    (b) The expected remaining wait is `1/p = 1/0.03 = 33.3` at any point.

    (c) The geometric distribution forgets the past, so the dry player and the fresh player face identical futures. Only a system with memory (pity, PRD, bags) would change this.
    </details>

29. **[Weeks 7, 9 · compute · final]** A boss rolls its loot table 3 times per kill, independently. Design wants 95% of players to see a gem within 25 kills. (a) What per-kill chance of at least one gem is needed? (b) What per-roll chance should the gem have? (c) Why is the answer to (b) not simply (a) divided by 3?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 11.29%. (b) 3.92%. (c) Rolls can both succeed on one kill, so dividing slightly undercounts.

    (a) `1 − 0.05^(1/25) = 1 − 0.8871 = 0.1129`.

    (b) The per-kill dry chance is `(1 − r)^3`, which must equal `0.8871`. So `r = 1 − 0.8871^(1/3) = 0.0392`. Equivalently, 25 kills of 3 rolls is 75 rolls, and `1 − 0.05^(1/75) = 0.0392`.

    (c) `0.1129/3 = 0.0376` would be too low. Three rolls at 3.76% give `1 − 0.9624^3 = 10.9%` per kill, not 11.29%. The gap is the kills that drop two or three gems.
    </details>

30. **[Week 7 · compute · final]** 60,000 players each attempt a daily 0.5% drop once per day. (a) After one year (365 days), how many are still dry? (b) After how many days have 95% of players got it?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) About 9,630 players. (b) 598 days.

    (a) `0.995^365 = 0.1605`, and `60,000 × 0.1605 ≈ 9,629`.

    (b) `ceil(ln 0.05 / ln 0.995) = ceil(597.6) = 598` days, over a year and a half. The rule of thumb `3/p = 600` agrees.
    </details>

31. **[Week 7 · design · final]** A raid weapon that most players need for the next tier drops at 2% per weekly clear. (a) Compute the median, 95th and 99th percentile waits in weeks. (b) Propose one fix using hard pity and compute the new expected wait and the share of players who reach the pity. (c) Comment on what your fix does to the drop's role.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 35, 149 and 228 weeks. (b) Example: hard pity at 26 clears gives an expected wait of 20.4 weeks, and 60% of players reach the pity. (c) The pity becomes the main source of the item.

    (a) `ceil(ln 0.5/ln 0.98) = 35`, `ceil(ln 0.05/ln 0.98) = 149`, `ceil(ln 0.01/ln 0.98) = 228`. One player in 20 waits almost three years for a required item.

    (b) With hard pity H, `E = (1 − 0.98^H)/0.02`. For H = 26, `0.98^26 = 0.591`, so `E = 20.4` weeks. The share reaching clear 26 is `0.98^25 = 0.604`.

    (c) With a 2% base rate, a six-month cap turns the item into a mostly guaranteed reward on a timer. That may be right for required gear, but then say so. A cleaner design raises the base rate so most players get it by luck and keeps the pity as a rare safety net. For example, p = 10% with H = 26 gives `E = (1 − 0.9^26)/0.1 = 9.4` weeks, and only `0.9^25 = 7.2%` reach the pity.
    </details>

## Week 8 · Dice sums and the normal curve

32. **[Week 8 · compute · final]** Compare 2d10 and 1d20. (a) Give each rule's mean and SD. (b) Compute P(result ≥ 15) for each. (c) How many percentage points does a +1 bonus add at target 15 for each, and at target 20?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 2d10 mean 11, SD 4.06. 1d20 mean 10.5, SD 5.77. (b) 21% and 30%. (c) At 15, +7 points on 2d10 and +5 on 1d20. At 20, +2 points on 2d10 and +5 on 1d20.

    (a) `N(F + 1)/2` and `√(N(F² − 1)/12)`. 2d10: `2 × 5.5 = 11`, `√(2 × 99/12) = 4.06`. 1d20: `10.5`, `√(399/12) = 5.77`.

    (b) On 2d10, a sum s of 11 or more has `21 − s` ways out of 100. Sums 15 to 20 give `6 + 5 + 4 + 3 + 2 + 1 = 21`, so 21%. On 1d20, faces 15 to 20 are 6 of 20, so 30%.

    (c) A +1 turns the result just below the target into a success. On 2d10, `P(sum = 14) = 7/100` and `P(sum = 19) = 2/100`. On 1d20, every face is 5%. The bell rewards bonuses most near its middle.
    </details>

33. **[Week 8 · compute · final]** A spell deals 10d6 damage. (a) Compute its mean and SD. (b) Use the normal approximation with a continuity correction to estimate P(damage ≥ 42). You may use Φ(1.20) = 0.8849. (c) The exact value is 11.60%. How close is your estimate, and what would you get without the continuity correction?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) mean 35, SD 5.40. (b) About 11.5%. (c) Within 0.2 points. Without the correction, about 9.7%.

    (a) `10 × 3.5 = 35`. `√(10 × 35/12) = √29.17 = 5.40`.

    (b) Damage is a whole number, so use 41.5 as the boundary. `z = (41.5 − 35)/5.40 = 1.20`. `P ≈ 1 − 0.8849 = 0.115`.

    (c) The estimate, 11.5%, is off by about 0.1 points. Without the correction, `z = 7/5.40 = 1.30`, and `1 − Φ(1.30) = 1 − 0.9032 = 0.097`, which is off by about 2 points.
    </details>

34. **[Week 8 · compute · final]** A game uses 3d6 roll-under: you succeed if the total is at most your skill. The cumulative values are P(3d6 ≤ 9) = 81/216, P(≤ 10) = 108/216, P(≤ 14) = 196/216, P(≤ 15) = 206/216. (a) How much does +1 skill help a player going from 9 to 10? (b) From 14 to 15? (c) Explain the difference in one sentence.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) +12.5 points (37.5% to 50%). (b) +4.6 points (90.7% to 95.4%). (c) The bell is steep in the middle and flat in the tails.

    (a) `81/216 = 37.5%` and `108/216 = 50%`.

    (b) `196/216 = 90.7%` and `206/216 = 95.4%`.

    (c) A +1 turns exactly one total from failure into success, and totals near the middle (10 and 11 have 27 ways each) are far more common than totals near the edge (15 has 10 ways), so the same bonus buys almost three times as much for the average character.
    </details>

35. **[Week 8 · design · practice]** A basic attack must average 14 damage. Give one dice expression with SD under 2 and one with SD over 5. For each, give its range and the chance of dealing 20 or more.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** Examples: 2d4 + 9 (range 11 to 17, SD 1.58, P(≥ 20) = 0) and 1d20 + 1d6 (range 2 to 26, SD 6.01, P(≥ 20) = 22.5%).

    2d4 + 9: mean `5 + 9 = 14`. SD `√(2 × 15/12) = 1.58`. The maximum is 17, so 20 is impossible.

    1d20 + 1d6: mean `10.5 + 3.5 = 14`. Variances add, `399/12 + 35/12 = 36.17`, so SD 6.01. Count pairs with sum at least 20 among 120. For die-6 values 1 to 6, the d20 needs at least 19, 18, 17, 16, 15, 14, which gives `2 + 3 + 4 + 5 + 6 + 7 = 27` pairs. `27/120 = 22.5%`.

    The first never surprises anyone. The second hits 20+ on more than one attack in five, which matters if 20 damage triggers a stagger or a kill threshold.
    </details>

36. **[Week 8 · explain · final]** A designer says "every +1 is worth the same, so our item prices can be linear in bonus size." Explain when this is true and when it is false, naming the dice shape in each case and giving one number from the lectures for each.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** True for a single flat die. False for summed dice.

    On a flat roll such as 1d20, every face has the same chance, so a +1 always converts exactly one 5% face and is worth 5 points at any target. Linear prices are fair there.

    On a bell such as 2d6, a +1 converts the one total just below the target, and totals differ in likelihood. From week 8, +1 is worth 16.7 points at target 8 and 5.6 points at target 12. The value of a bonus depends on where the target sits, so prices should depend on the targets players actually face, and stacking bonuses in the middle of the bell is where balance breaks first.
    </details>

## Week 9 · Weighted loot tables

37. **[Week 9 · compute · final]** A boss table has weights Nothing 500, Gold 300, Potion 120, Rare 60, Legendary 20. (a) What is the Legendary chance, and how many kills do 95% of players need (one roll per kill)? (b) A seasonal item of weight 40 is added and nothing else changes. Recompute both. (c) What edit keeps the Legendary unchanged?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 2.0%, 149 kills. (b) 1.92%, 155 kills. (c) Cut Nothing from 500 to 460.

    (a) `20/1000 = 2%`. `ceil(ln 0.05 / ln 0.98) = ceil(148.3) = 149`.

    (b) The total becomes 1,040, so `20/1040 = 1.923%`. `ceil(ln 0.05 / ln(1 − 0.01923)) = ceil(154.3) = 155`. Six more kills for the unlucky 5%, from an edit that never touched the Legendary.

    (c) Take the 40 from Nothing so the total stays 1,000. Every item keeps its chance and the seasonal item gets 4%.
    </details>

38. **[Week 9 · compute · final]** The entries of a table (other than a new one) sum to 760. (a) What weight gives the new entry exactly a 5% chance? (b) An existing entry has weight 38. What was its chance before, and what is it after the new entry is added?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 40. (b) 5.00% before, 4.75% after.

    (a) `w = R × q/(1 − q) = 760 × 0.05/0.95 = 40`. Check: `40/800 = 5%`.

    (b) `38/760 = 5%` and `38/800 = 4.75%`. Every old entry is multiplied by `760/800 = 0.95`.
    </details>

39. **[Week 9 · compute · final]** A Diablo II-style treasure class has NoDrop weight 80 and all other entries summing to 40. With an effective player count N, the game wants P(NoDrop) to become P₀^N and sets `new NoDrop = floor(R × P₀^N / (1 − P₀^N))`. For N = 4, compute the target, the new NoDrop weight, and the chance the pick drops some item. What did rounding do?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** target 19.75%, new weight 9, P(some item) = 81.6%. Rounding cut NoDrop to 18.4%, below the target.

    `P₀ = 80/120 = 0.6667`. `P₀^4 = 0.1975`. `w = 40 × 0.1975/0.8025 = 9.85`, floored to 9. The new total is 49, so `P(item) = 40/49 = 81.6%` and `P(NoDrop) = 9/49 = 18.4%`.

    With small weights, rounding moves probabilities by a large relative amount. The item side got slightly more generous than intended. Larger weight totals shrink this error.
    </details>

40. **[Week 9 · compute · final]** A top table has Nothing 70, Common 25 and Rare 5, where Common and Rare point to sub-tables. The Rare sub-table has A 3, B 1, C 1. The Common sub-table has total weight 50, and one of its entries is also item C with weight 1. What is the chance one pick yields item C? What is the chance it yields item A?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** P(C) = 1.5%. P(A) = 3%.

    Multiply along each path and add the paths, since one pick takes only one path.
    - Through Rare: `5/100 × 1/5 = 1.0%`.
    - Through Common: `25/100 × 1/50 = 0.5%`.

    `P(C) = 1.0% + 0.5% = 1.5%`. A has one path, `0.05 × 3/5 = 3%`. A spreadsheet that follows only the Rare path reports 1% for C and misses a third of its drops.
    </details>

41. **[Week 9 · compute · final]** Use the table from question 37 (before the seasonal change), with values Nothing 0, Gold 40, Potion 15, Rare 300, Legendary 2,500. The table is rolled twice per kill. (a) What is the expected gold value per roll and per kill? (b) What share of it comes from the Legendary?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 81.8 per roll, 163.6 per kill. (b) 61%.

    (a) `0.30 × 40 + 0.12 × 15 + 0.06 × 300 + 0.02 × 2500 = 12 + 1.8 + 18 + 50 = 81.8`. Two independent rolls give `2 × 81.8 = 163.6` by linearity.

    (b) `50/81.8 = 0.61`. A 2% row supplies 61% of the income, so the Legendary's weight is the economy's main dial.
    </details>

42. **[Week 9 · critique · final]** For the question 37 table, a producer asks for the Legendary to reach 5% "by shrinking Nothing". (a) What is the highest chance the Legendary can reach by shrinking Nothing alone? (b) What Legendary weight gives 5% if Nothing stays at 500?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 4%. (b) 52 (5.04%), from the exact value 51.6.

    (a) With Nothing at 0, the Legendary is `20/500 = 4%`. Shrinking Nothing rescales every item by the same factor and can never lift an item past its share among the non-Nothing entries.

    (b) The other weights sum to `500 + 300 + 120 + 60 = 980`. `w = 980 × 0.05/0.95 = 51.6`, so use 52, giving `52/1032 = 5.04%`. The request as phrased cannot be met. The producer has to change the Legendary's own weight.
    </details>

## Week 10 · PRD and pity timers

43. **[Week 10 · compute · practice]** A 20% effect uses PRD with C = 0.0557 (the chance on the Nth attack since the last proc is min(1, C × N)). (a) What is the chance on the first attack after a proc, and what is the longest possible gap? (b) Compute the chance of no proc in the first 3 attacks under PRD and under independent 20% rolls. (c) Do the same for no proc in the first 9 attacks. (d) What pattern do (b) and (c) show together?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 5.57%, 18 attacks. (b) PRD 69.9%, independent 51.2%. (c) PRD 4.4%, independent 13.4%. (d) PRD makes short gaps rarer and long gaps rarer, and piles gaps into the middle.

    (b) PRD: `(1 − 0.0557)(1 − 0.1114)(1 − 0.1671) = 0.9443 × 0.8886 × 0.8329 = 0.699`. Independent: `0.8³ = 0.512`.

    (c) PRD: `Π_{i=1..9} (1 − 0.0557 i) = 0.044`. Independent: `0.8^9 = 0.134`.

    (d) Both systems have mean gap 5.00. PRD suppresses back-to-back procs (early chances are small) and cuts off long droughts (late chances are large). Its gap SD is 2.43 against 4.47 for independent rolls.
    </details>

44. **[Week 10 · compute · final]** A card pack has a 3% chance of a top-rarity card, with hard pity at pack 50. (a) What is the expected number of packs per top card? (b) What long-run rate does that imply? (c) What share of players reach the pity pack?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 26.1 packs. (b) 3.84%. (c) 22.5%.

    (a) `E = (1 − 0.97^50)/0.03 = (1 − 0.2181)/0.03 = 26.06`.

    (b) `1/26.06 = 0.0384`.

    (c) Reaching pack 50 needs 49 misses, `0.97^49 = 0.225`. Nearly a quarter of players get their card from the guarantee, so the pity is a regular part of the experience, not a rare safety net.
    </details>

45. **[Week 10 · compute · practice]** A small gacha has a 10% base rate on pulls 1 to 5. Soft pity then sets the chance to 30%, 50%, 70% and 90% on pulls 6 to 9, and pull 10 is guaranteed. (a) Compute the expected number of pulls by summing survival probabilities. (b) What is the consolidated rate? (c) What is the median pull? (d) Compare with hard pity at 10 alone.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 5.37 pulls. (b) 18.6%. (c) Pull 6. (d) Hard pity alone gives 6.51 pulls, a 15.4% rate.

    (a) Survival before each pull, `P(no success in the first k pulls)` for k = 0 to 9, is 1, 0.9, 0.81, 0.729, 0.6561, 0.5905, 0.4133, 0.2067, 0.0620, 0.0062. Their sum is 5.374.

    (b) `1/5.374 = 0.186`.

    (c) The cumulative chance is 40.95% after pull 5 and 58.67% after pull 6, so the median is pull 6.

    (d) `(1 − 0.9^10)/0.1 = 6.51`. Soft pity takes more than a pull off the average and moves most successes into pulls 6 to 8.
    </details>

46. **[Week 10 · critique · final]** A game publishes a 1% base rate, a guarantee within 80 pulls and a "consolidated rate of 1.8%". A forum post claims the numbers prove a hidden soft pity, "just like Genshin". Check the claim with hard pity alone, and compare with the Genshin Impact numbers from the lecture (0.6% base, 90 hard pity, 1.6% consolidated).

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** The claim is not supported. Hard pity alone gives 55.2 expected pulls, a rate of 1.81%, which already matches 1.8%.

    `E = (1 − 0.99^80)/0.01 = (1 − 0.4475)/0.01 = 55.25`, and `1/55.25 = 1.81%`.

    For Genshin, hard pity alone gives `(1 − 0.994^90)/0.006 = 69.7` pulls, a rate of 1.43%, which cannot reach the published 1.6%. That gap is what showed a rise before pull 90. Here there is no gap, so the published numbers are consistent with no soft pity. They do not rule soft pity out either, only a small one. Note also that 45% of players (`0.99^79`) would reach the guarantee.
    </details>

47. **[Week 10 · design · final]** Choose a variance-control tool (independent rolls, PRD, hard pity, soft pity, or a shuffle bag) for each case and justify it in one or two sentences with a number where possible. (a) A 30% evasion chance on every incoming hit in a PvP game. (b) A 0.5% raid mount, one kill per week. (c) The order of 5 rune types in a match-3 game.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** A strong answer looks like this.

    (a) PRD. The event is frequent and visible, and under independent rolls three evasions in a row happen `0.3³ = 2.7%` of the time, which decides PvP fights. PRD keeps the 30% average and makes streaks rare, at the cost of a counter per unit.

    (b) Hard or soft pity with a cap. PRD's ramp is too slow for a 0.5% rate, and independent rolls leave `0.995^260 = 27%` of players dry after five years of weekly kills. A cap sets the worst case directly.

    (c) A shuffle bag of the 5 types (or a multiple). It tracks all types at once and caps the gap between two of the same type at 8 draws for a bag of 5, which keeps boards solvable.

    Any choice is acceptable if the justification names the event frequency, the worst case, and the state the tool needs.
    </details>

## Week 11 · Monte Carlo simulation

48. **[Week 11 · compute · final]** A simulation of 20,000 trials estimates a probability of 13.7%. (a) What is the 95% margin of error? (b) How many trials give a margin of ±0.25 percentage points? (c) By what factor must trials grow to halve the margin?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) ±0.48 points. (b) About 72,700 trials. (c) Four times.

    (a) `1.96 × √(0.137 × 0.863 / 20000) = 1.96 × 0.00243 = 0.0048`.

    (b) `n = 1.96² × 0.137 × 0.863 / 0.0025² = 72,671`.

    (c) The margin scales with `1/√n`, so halving it needs `2² = 4` times the trials.
    </details>

49. **[Weeks 10, 11 · critique · final]** A teammate simulates a 25% PRD effect with C = 0.0847 and reports a mean gap of 3.28 ± 0.01 attacks over a million gaps. The exact mean is 4.00. (a) Is this sampling error or model error? (b) The teammate's code increments the counter before the roll, so the first attack after a proc uses 2C. Is that consistent with 3.28? (c) Name a validation check that would have caught it before the full run.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) Model error. (b) Yes. Starting the ramp at 2C gives an exact mean gap of 3.28. (c) Check the proc rate on the first attack after a proc, which should equal C = 8.47%.

    (a) The margin is ±0.01 and the miss is 0.72, about 70 margins away. More trials would only make the wrong answer more precise.

    (b) Computing the gap distribution with chances 2C, 3C, 4C and so on gives a mean of 3.28, which matches. The bug skips the first step of the ramp.

    (c) Validate small pieces against known values before the whole run. The first-attack chance should be C, the longest gap should be `ceil(1/C) = 12` (the bug gives 11), and the mean gap should be 4.00. Any one of these would flag the bug.
    </details>

50. **[Week 11 · compute · final]** A gacha simulation of 25,000 players gives a mean of 41.3 pulls with a sample SD of 18. (a) What is the standard error and the 95% margin of the mean? (b) An exact calculation gives 41.5. Is it consistent? (c) How many players would you need for a margin of ±0.05 pulls?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) SE 0.114, margin ±0.22. (b) Yes. (c) About 498,000 players.

    (a) `SE = 18/√25000 = 0.114`, margin `1.96 × 0.114 = 0.223`.

    (b) The interval is 41.08 to 41.52, which contains 41.5, though near the edge.

    (c) `n = (1.96 × 18 / 0.05)² = 497,871`.
    </details>

51. **[Week 11 · explain · practice]** Explain why a Monte Carlo study should (a) use a fixed seed with its own generator object, and (b) be validated on a case with a known exact answer before it answers the real question. Use the Hearthstone mulligan example from the lecture in your answer to (b).

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:**

    (a) A seed makes every run reproducible, so a colleague gets the same numbers and a bug can be replayed. A private generator keeps other code that draws random numbers from shifting your results. Changing the seed on purpose then checks that a result is not a fluke of one sequence.

    (b) The margin of error measures only sampling noise and says nothing about wrong rules. In the lecture, the no-mulligan case has an exact answer, `1 − 552/870 = 0.3655`, going first. Running the program without the mulligan and seeing its interval cover 0.3655 tests the deal and draw code. A program that dealt 4 cards to the first player would fail this check at once, while on the mulligan question it would print a confident 0.587 that is simply the going-second value.
    </details>

## Week 12 · Descriptive statistics

52. **[Week 12 · compute · final]** Eleven testers cleared a dungeon in these times (minutes), sorted: 12, 13, 15, 15, 16, 18, 19, 21, 24, 26, 55. Using the inclusive percentile rule (position `h = (n − 1)p + 1`), compute the mean, median, Q1, Q3, IQR and the 1.5 × IQR fences. Is 55 an outlier? Recompute the mean and median without it.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** mean 21.27, median 18, Q1 15, Q3 22.5, IQR 7.5, fences 3.75 and 33.75. 55 is an outlier. Without it, mean 17.9 and median 17.

    Sum 234, so mean `234/11 = 21.27`. The median is the 6th value, 18.

    Q1: `h = 10 × 0.25 + 1 = 3.5`, halfway between 15 and 15, so 15. Q3: `h = 8.5`, halfway between 21 and 24, so 22.5. IQR 7.5.

    Fences: `15 − 11.25 = 3.75` and `22.5 + 11.25 = 33.75`. 55 is far above.

    Without 55: sum 179 over 10, mean 17.9. The median is the average of the 5th and 6th values, `(16 + 18)/2 = 17`. The mean moved 3.4 minutes and the median moved 1. (The sample SD drops from 12.0 to 4.6.)
    </details>

53. **[Week 12 · explain · final]** Eighteen testers rated a boss from 1 (far too easy) to 5 (far too hard). Counts: 1 → 5, 2 → 3, 3 → 1, 4 → 2, 5 → 7. Compute the mean, median and mode. Which should go on the slide, and what is the design finding?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** mean 3.17, median 3.5, mode 5. Put the distribution itself on the slide with n = 18.

    Sum `5 + 6 + 3 + 8 + 35 = 57`, mean `57/18 = 3.17`. The 9th and 10th values are 3 and 4, so the median is 3.5.

    Both the mean and the median say "about right", yet only one tester chose 3. The data are bimodal. Eight testers found it too easy and nine found it too hard. The finding is a split audience, and the next step is to check what separates the two groups (class, experience, a missed mechanic).
    </details>

54. **[Week 12 · compute · final]** Three testers' deaths and play time: A died 8 times in 80 minutes, B 5 times in 25 minutes, C 3 times in 12 minutes. (a) Rank them by raw deaths and by deaths per hour. (b) Which denominator would you use to ask whether a boss is too punishing per attempt, and which to ask how often sessions get interrupted?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) Raw deaths rank A > B > C. Per hour, A 6, B 12, C 15, so C > B > A. (b) Deaths per attempt for punishment per try. Deaths per hour for interruptions.

    `8/(80/60) = 6`, `5/(25/60) = 12`, `3/(12/60) = 15`. The tester with the fewest deaths had the roughest time per hour. Compare counts only after dividing by exposure.
    </details>

55. **[Week 12 · explain · final]** Two summaries. Dungeon clear times have mean 31 minutes and median 24. Pulls to a 5-star in a soft-pity gacha have mean 62.3 and median 76. For each, name the skew direction, explain what creates it, and say which number better describes the typical player.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** Clear times are right-skewed, because a few slow or idle runs pull the mean up. The median (24) describes the typical tester. The gacha is left-skewed, because a long run of lucky early pulls pulls the mean down while soft pity piles most players up near 74 to 80. The median (76) describes the typical player.

    The rule to keep: the mean lies on the side of the long tail. Use the mean when you need a total (server hours, pulls sold), and the median when you need the typical experience.
    </details>

## Week 13 · Sampling and confidence

56. **[Week 13 · compute · final]** Seven of 8 playtesters cleared a boss. (a) Compute the simple (Wald) 95% interval. (b) Compute the plus-four interval. (c) The Wilson interval is 52.9% to 97.8%. Write the one-sentence version for a report.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 64.6% to 110.4%. (b) 50.5% to 99.5%. (c) "7 of 8 testers cleared the boss, and the true clear rate could be anywhere from about 53% to 98% (Wilson 95%, n = 8)."

    (a) `p̂ = 0.875`, `SE = √(0.875 × 0.125/8) = 0.117`, margin `1.96 × 0.117 = 0.229`. The upper end passes 100%, the first sign the simple formula is breaking.

    (b) Use 9 of 12: `p̂ = 0.75`, `SE = √(0.75 × 0.25/12) = 0.125`, margin 0.245, giving 50.5% to 99.5%.
    </details>

57. **[Week 13 · compute · final]** You killed a boss 150 times with no drop. (a) What is the rule-of-three 95% upper bound on the drop rate? (b) The wiki says 1.5%. How likely is your streak at that rate? Should you doubt the wiki?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 2%. (b) 10.4%. No, one streak like this is not strong evidence.

    (a) `3/150 = 0.02`.

    (b) `0.985^150 = 0.104`, about 1 in 10. The wiki's 1.5% sits inside your bound, and one player in ten sees a streak like yours.
    </details>

58. **[Week 13 · compute · final]** (a) How many players do you need to measure a tutorial completion rate near 25% to within ±3 points? (b) How many kills to measure a 0.4% drop rate to within ±15% of itself?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 801 players. (b) About 42,500 kills.

    (a) `n = 1.96² × 0.25 × 0.75 / 0.03² = 800.3`, so 801.

    (b) `n ≈ 3.84 × (1 − p)/(p × r²) = 3.84 × 0.996 / (0.004 × 0.0225) = 42,496`. A drop rate "measured" from a few hundred kills is a rumour.
    </details>

59. **[Week 13 · critique · final]** A fan site collects drop logs. The true rate is 2%. Each player kills the boss 20 times, but only players who got at least one drop bother to submit. (a) What share of players submit? (b) What drop rate does the pooled submitted data show, on average? (c) Why would collecting ten times as many logs not fix it?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 33.2%. (b) About 6.0%, three times the truth. (c) The bias is in who submits, and more of the same logs give a tighter interval around the same wrong number.

    (a) `1 − 0.98^20 = 0.332`.

    (b) Each player expects `20 × 0.02 = 0.4` drops, and all of those drops belong to submitters. So submitters average `0.4/0.332 = 1.20` drops in 20 kills, a rate of `1.20/20 = 6.0%`.

    (c) Sample size shrinks random error only. Self-selection is sampling bias, and it does not shrink with n. Fix the collection, for example by asking every player to log from the start, dry runs included.
    </details>

## Week 14 · Hypothesis testing (A/B)

60. **[Week 14 · compute · final]** An A/B test of a new onboarding flow: A retains 360 of 3,000 players on day 1 (12%), B retains 420 of 3,000 (14%). (a) Compute the pooled rate, SE, z and the two-sided p-value. You may use Φ(2.30) = 0.9893. (b) State the verdict at α = 0.05 and the relative lift. (c) Give the 95% interval for the difference using the unpooled SE.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) pooled 13%, SE 0.00868, z = 2.30, p ≈ 0.021. (b) Significant. Relative lift 16.7%. (c) 0.3 to 3.7 points.

    (a) `p̂ = 780/6000 = 0.13`. `SE = √(0.13 × 0.87 × (2/3000)) = 0.00868`. `z = 0.02/0.00868 = 2.30`. `p = 2(1 − 0.9893) = 0.021`.

    (b) `|z| > 1.96`. Lift `0.02/0.12 = 16.7%`.

    (c) Unpooled `SE = √(0.12 × 0.88/3000 + 0.14 × 0.86/3000) = 0.00868`. `0.02 ± 1.96 × 0.00868` gives 0.003 to 0.037. The effect is real at this level but could be as small as a third of a point, which matters for whether it pays for itself.
    </details>

61. **[Week 14 · compute · final]** Baseline day-1 retention is 20%. You want 80% power at α = 0.05 to detect a rise to 22%. (a) Estimate n per group with Lehr's rule, `n ≈ 16 p(1 − p)/d²`. (b) Compute it with the full formula, `7.85 × (p_A(1 − p_A) + p_B(1 − p_B))/d²`. (c) With 800 new players per day, how long does the test run?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 6,400. (b) About 6,508. (c) About 16 to 17 days. Plan for 21 to cover three full weeks.

    (a) `16 × 0.2 × 0.8 / 0.02² = 6,400`.

    (b) `7.85 × (0.16 + 0.1716)/0.0004 = 6,508`.

    (c) Two groups of about 6,500 need 13,000 players, so `13,000/800 ≈ 16.3` days. Round up to whole weeks so weekday and weekend players are both covered.
    </details>

62. **[Weeks 3, 14 · compute · final]** A producer tracks 12 metrics in one A/B test of a change that truly does nothing. (a) What is the chance at least one metric comes out significant at α = 0.05, assuming the metrics are independent? (b) What threshold would a Bonferroni correction require per metric? (c) What is the simpler fix?

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) 46%. (b) p < 0.0042. (c) Fix one primary metric before the test.

    (a) The complement rule: `1 − 0.95^12 = 0.46`.

    (b) `0.05/12 = 0.0042`.

    (c) Name the primary metric, α and n in the test plan before any data arrive. Report the others as exploratory.
    </details>

63. **[Week 14 · design · final]** Your MMO team wants to test whether a 20% cheaper repair cost increases hours played. A designer proposes randomizing half the players on each server. Name two problems specific to an online world and propose a better design, including what happens to the effective sample size.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** Problems: (1) interference, because players in both groups share guilds, groups and a market, so the cheaper group's gold and behaviour leak into the control group; (2) fairness and visibility, because players compare costs, see the difference within hours, and complain or change behaviour because they know they are in a test.

    Better design: randomize whole servers (or regions), or run on a public test realm with the test announced. The unit of randomization becomes the server, so the effective n is the number of servers, not players, and the test needs more servers or a larger effect to reach useful power. Run at least one full week to cover the weekly cycle and let novelty fade.
    </details>

64. **[Week 14 · explain · final]** A team reports "B beat A, p = 0.03, so there is a 97% chance B is better." Explain what p = 0.03 does mean, why the team's reading is wrong, and name one more number they should report.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** p = 0.03 means that if A and B were truly identical, a gap at least this large would appear 3% of the time. It is computed assuming no effect, so it cannot be the probability that an effect exists.

    The reading also ignores effect size. A tiny lift can have a small p-value with enough players. The team should report the effect size with its confidence interval, for example "+1.2 points (0.1 to 2.3)". Power and the pre-registered primary metric also help a reader judge whether the result can be trusted.
    </details>

## Integrative questions

65. **[Weeks 3, 7, 9, 10 · design · final]** A crafting reagent sits in a boss table with total weight 1,000, rolled twice per clear. Design wants 95% of players to have one within 20 weekly clears. (a) Find the per-roll chance and the integer weight. Check that your rounded weight still meets the target. (b) Add a hard pity at clear 15. Compute the expected clears and the share of players who reach the pity. (c) State in one sentence what the pity costs.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** (a) Per-roll 7.22%, so weight 73 (72 misses the target). (b) Expected 6.38 clears, 12.0% reach the pity. (c) A per-player counter per reagent, and a slightly more common reagent.

    (a) 20 clears of 2 rolls is 40 rolls, so `r = 1 − 0.05^(1/40) = 0.0722`, which is 72.2 on a total of 1,000.
    - Weight 72: per clear `1 − 0.928² = 0.1388`, and `ceil(ln 0.05 / ln 0.8612) = 21` clears. Misses by one.
    - Weight 73: per clear `1 − 0.927² = 0.1407`, and `ceil(19.76) = 20`. Meets the target.

    Round in the direction that keeps the promise.

    (b) `E = (1 − 0.8593^15)/0.1407 = 6.38` clears, down from `1/0.1407 = 7.11`. Reaching clear 15 needs 14 dry clears, `0.8593^14 = 0.120`.

    (c) The game must store and replicate a counter per player, and the reagent's effective rate rises from 14.1% to about 15.7% per clear, which the crafting economy has to absorb.
    </details>

66. **[Weeks 3, 7, 13 · critique · final]** A producer writes: "The mount drops at 2% per kill, so everyone will have it within 50 kills. Our playtest confirms it: 5 of 6 testers got it within 50 kills." Find every error. Use numbers.

    <details>
    <summary>Answer and worked solution</summary>

    **Answer:** Three errors.

    First, 50 kills is the mean wait, not a deadline. `P(have it by 50) = 1 − 0.98^50 = 63.6%`, so 36% of players are still dry at kill 50, and 95% need up to 149 kills.

    Second, 5 of 6 cannot confirm anything. The Wilson 95% interval for 5 of 6 is 43.6% to 97.0%, which contains the true 63.6% and nearly everything else.

    Third, the playtest result is not even unusual at the true rate. If each tester has a 63.6% chance, the chance that 5 or 6 of 6 succeed is `6(0.636^5)(0.364) + 0.636^6 = 29.3%`. The playtest is a lucky but ordinary draw. Use small playtests to find problems, and use the model or large logs to state rates.
    </details>
