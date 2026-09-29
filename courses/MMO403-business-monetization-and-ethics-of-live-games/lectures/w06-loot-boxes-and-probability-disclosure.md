# MMO403 · Week 06 — Loot Boxes and Probability Disclosure

**Why this matters:** In most large markets, a game that sells random items must now print the odds of each item. Those odds are true, and they still do not answer the question a buyer actually has, which is "how much will it cost me to get what I want?" This week you learn to compute that answer, how duplicate protection and pity change it, and what a disclosure has to show before a player can make an informed choice.

**You will be able to:**
- Compute the expected, median and 90th-percentile number of boxes needed to complete a set with unequal item odds.
- Compare no protection, duplicate protection and pity rules by their effect on the typical buyer and on the unlucky tail.
- Design a probability disclosure that meets the per-item odds rule and also shows cost in real money.
- Summarize the research on loot boxes and harm accurately, including what it does not show.

**Before class:** Fields & Cotton, *Social Game Design: Monetization Methods and Mechanics* (Morgan Kaufmann, 2011), the chapter on random rewards and gacha-style sales. Xiao, Henderson, Yang & Newall, "Gaming the system: sub-optimal compliance with loot box probability disclosure regulations in China", *Behavioural Public Policy* (2021/2022), abstract, introduction and results (about 10 pages). Zendle & Cairns, "Video game loot boxes are linked to problem gambling", *PLOS ONE* (2018), abstract and discussion.

**Prerequisites from earlier courses:** [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (the chance of at least one success in `n` tries). [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) (the wait for one item, and why its median is well below its mean's tail). [MA102 week 10, pity timers](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w10-pseudo-random-distribution-and-pity-timers.md) (hard and soft pity, and the Genshin Impact consolidated rate; we do not repeat that example). [GD202 week 14, narrative testing](../../GD202-narrative-and-quest-design/lectures/w14-narrative-testing.md) (the coupon collector mean `L × H_L` for equally likely endings). [MA102 week 9, weighted loot tables](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w09-weighted-tables-and-loot-table-design.md). [UX201 week 5, reinforcement schedules and their ethics](../../UX201-game-ux-and-player-psychology/lectures/w05-reinforcement-schedules-and-ethics.md) (why a random reward holds attention; this lecture covers cost and disclosure, not the psychology).

**Interactive:** [What the set costs](../examples/w06-set-completion-cost.html). Keep it open during section 2.

---

## 1. What a loot box is, and what the rules make you print

A **loot box** is a purchase whose contents are chosen at random after you pay. Card packs, gacha pulls, weapon cases and crates are all loot boxes in this sense. The player pays a fixed price and receives one draw, or a few draws, from a table of items with set probabilities. Your week 9 loot tables from MA102 are the engine. The only new ingredient is that the draw costs money.

Since 2017, the main requirement placed on loot boxes has been **probability disclosure**: publish the chance of receiving each item, or each type of item, before the player pays. The timeline is short.

| When | Who | Rule |
|---|---|---|
| Announced December 2016, in force May 2017 | China, Ministry of Culture | Online game publishers must publish the draw probability of virtual items and services. |
| December 2017 | Apple, App Store Review Guidelines 3.1.1 | Apps offering loot boxes or other randomized virtual items for purchase must disclose the odds of receiving each type of item before purchase. |
| By May 2019 | Google Play, Payments policy | Apps offering randomized virtual items from a purchase must disclose the odds in advance of, and close in time to, the purchase. |
| August 2019 | Entertainment Software Association (US industry body) | Microsoft, Nintendo and Sony announced odds-disclosure requirements for paid loot boxes on their consoles, with major publishers committing to the same on other platforms, targeted for 2020. |
| March 2024 | South Korea, amended Game Industry Promotion Act (passed February 2023) | Probability disclosure required by law, in the game, in advertising and on official websites, with fines or prison for failing to disclose or for false probabilities. |
| January 2025 | US Federal Trade Commission, order against Cognosphere (HoYoverse, *Genshin Impact*) | $20 million settlement. The order bans misrepresenting loot box odds and prices, requires disclosure of odds and of exchange rates for multi-tier virtual currency, and requires an option to buy loot boxes directly with real money. |

Week 7 covers the wider legal picture, including the countries that treat some loot boxes as gambling. For this week, notice what almost every rule above asks for: the probability of each item or type of item. Notice also the one exception. The FTC order goes further and asks for exchange rates, because the complaint said that layered currencies hid how much real money players spent. That is the gap this lecture is about.

## 2. Worked example: the set that costs six times its size

### The hook

In August 2017, Blizzard added duplicate protection for Legendary cards to *Hearthstone*. From then on, a pack could not give you a second copy of a Legendary from a set until you owned every Legendary in that set. In March 2020 it extended protection to every rarity: no third copy of a Common, Rare or Epic until you have two of each card of that rarity. In June 2017, Blizzard had already cut the frequency of duplicate items from *Overwatch* loot boxes. Both games were selling random items with published or well-known rarity odds. Neither changed those odds. Why did both studios spend engineering time on duplicates?

Because the odds of each item are not what a collector pays for. They pay for the set. And a set bought one random box at a time costs far more than the per-item odds suggest, with most of the cost in the last few items.

### The model

A **set** has `N` items. Each box contains one item, drawn independently, with item `i` appearing with probability `p_i`. The probabilities add up to 1. Let `T` be the number of boxes a player opens before they own every item at least once. This is the **coupon collector's problem**, with unequal odds.

If every item has the same chance `1/N`, GD202 week 14 gave you the mean:

```
E[T] = N × H_N,  where H_N = 1 + 1/2 + 1/3 + ... + 1/N
```

With unequal odds, use **inclusion-exclusion** over sets of missing items. For any group `S` of items, let `P(S)` be the chance that one box gives an item in `S`. Then:

```
P(T ≤ n) = Σ over all groups S  (−1)^|S| × (1 − P(S))^n
E[T]     = Σ over non-empty S   (−1)^(|S|+1) / P(S)
```

- `P(T ≤ n)` is the chance that `n` boxes complete the set. The term for the empty group is 1.
- `|S|` is the number of items in `S`.
- `(1 − P(S))^n` is the chance that `n` boxes all miss `S`, the complement rule from MA102 week 3 applied to a whole group.

This looks expensive, since a 20-item set has about a million groups. But items of the same rarity are interchangeable, so you only need to count how many items you take from each tier. With tiers of size `n_1, n_2, n_3` and per-item probabilities `p_1, p_2, p_3`, the group of `j_1, j_2, j_3` items from each tier has `P(S) = j_1 p_1 + j_2 p_2 + j_3 p_3` and appears `C(n_1, j_1) × C(n_2, j_2) × C(n_3, j_3)` times. A three-tier set of 20 items needs only 160 terms.

### Numbers you can check

Start with the equal case, 20 items at 5% each. `H_20 = 3.598`, so `E[T] = 20 × 3.598 = 71.95` boxes. Split that by progress. The first 10 items take `20 × (1/20 + 1/19 + ... + 1/11) = 13.4` boxes on average. The last 10 take 58.6. The final item alone takes 20 boxes on average, because by then 19 out of 20 draws are duplicates. Half the set costs about a fifth of the whole.

Now a realistic set with rarities. It has 15 Common items at 5.4% each, 4 Rare items at 4.5% each and 1 Legendary at 1%. The disclosure page for this box, done by the rules, would say:

| Rarity | Items | Chance per item | Chance per tier |
|---|---|---|---|
| Common | 15 | 5.4% | 81% |
| Rare | 4 | 4.5% | 18% |
| Legendary | 1 | 1.0% | 1% |

Every number on that page is true. Here is what it does not show. The code runs as shown with `.venv/bin/python`.

```python
from itertools import product
from math import comb

# (number of items in the tier, chance per box of each item in that tier)
SET = [(15, 0.054), (4, 0.045), (1, 0.01)]

def terms(tiers):
    """Yield (sign x count, probability) for every mix of items from each tier."""
    for picks in product(*(range(n + 1) for n, _ in tiers)):
        k = sum(picks)
        ways = 1
        for (n, _), j in zip(tiers, picks):
            ways *= comb(n, j)
        q = sum(j * p for (_, p), j in zip(tiers, picks))
        yield (-1) ** k * ways, q

def expected_boxes(tiers):
    return sum(-w / q for w, q in terms(tiers) if q > 0)

def p_complete(n, tiers):
    """Chance that n boxes contain every item at least once."""
    return sum(w * (1 - q) ** n for w, q in terms(tiers))

def boxes_for(share, tiers):
    n = 0
    while p_complete(n, tiers) < share:
        n += 1
    return n

for name, tiers in [("20 items at 5% each", [(20, 0.05)]), ("15/4/1 tiers", SET)]:
    print(f"{name}: mean {expected_boxes(tiers):.2f}, "
          f"median {boxes_for(0.5, tiers)}, 90th percentile {boxes_for(0.9, tiers)}")
```

Output:

```
20 items at 5% each: mean 71.95, median 67, 90th percentile 103
15/4/1 tiers: mean 120.55, median 90, 90th percentile 230
```

A 20-item set with one 1% item costs 120.55 boxes on average, six times its size. Half of all collectors need 90 boxes or more. One in ten needs 230 or more. At a price of one dollar per box, the disclosed "1%" means a $230 bill for the unluckiest tenth of collectors who want the whole set.

Where does the tail come from? Almost entirely from the Legendary. On its own, the wait for a 1% item has a mean of 100, a median of 69 and a 90th percentile of 230 boxes (MA102 week 7). The 90th percentile of the whole set equals the 90th percentile of the Legendary alone. The Commons and Rares are usually done long before.

Now apply rules like the ones Hearthstone and Overwatch adopted. **Duplicate protection** here means the rarity is drawn at the published odds, but within a rarity you always get an item you do not yet own, until you own them all. A **Legendary pity at 40** means that if 39 boxes in a row had no Legendary, the 40th is a Legendary. Once you own the Legendary the pity counter stops, since a forced duplicate would only waste a box. Computed exactly (lab 06 builds the code):

| Rule | Mean boxes | Median | 90th percentile |
|---|---|---|---|
| No protection, no pity | 120.55 | 90 | 230 |
| Duplicate protection only | 103.22 | 70 | 230 |
| Legendary pity at 40 only | 69.70 | 65 | 100 |
| Both | 36.61 | 40 | 40 |

Two lessons are in this table. Duplicate protection helps the typical collector a lot (the median falls from 90 to 70) and does nothing for the unlucky tail, because the tail is one missing item and protection only matters when there is a choice. Pity attacks the tail directly. With both, 94% of collectors finish within 40 boxes (the rest are still short of a Common or Rare, and 99% finish by box 53), and the cost of the set becomes almost a fixed price. The per-item odds on the disclosure page are the same in all four rows.

### Move it yourself

Open `examples/w06-set-completion-cost.html`. The left view is the disclosure page: a bar per rarity with the published per-item chance. The right view is the cost: a cumulative curve of the share of collectors who have completed the set after `n` boxes, with the mean, median and 90th percentile marked, and a box price that converts boxes into money. Drag the Legendary chance from 1% to 0.5%. The left view barely changes, one short bar gets shorter. The right view's 90th percentile jumps from 230 to 460 boxes. Then turn on duplicate protection and watch the middle of the curve move left while the top stays put. Turn on pity and watch the top snap to the pity line.

### Cross-game recognition

**Hearthstone (packs, 2017 and 2020 rule changes).** Beyond duplicate protection, Hearthstone turns unwanted cards into a crafting currency, Arcane Dust. A normal card disenchants for 5 (Common), 20 (Rare), 100 (Epic) or 400 (Legendary) dust, and crafting one costs 40, 100, 400 or 1,600. So a duplicate Legendary returns a quarter of the cost of crafting the one you want, and a duplicate Common returns an eighth. In our model this puts a ceiling on the cost of any single missing item. Once your duplicates have produced 1,600 dust, the Legendary you lack no longer depends on luck. Dust is a pity timer paid in a second currency. Players can compute their worst case, which the plain box cannot offer.

**Overwatch 2 (Season 15, February 2025).** Blizzard brought loot boxes back to Overwatch 2, earned through play, the battle pass and challenges, and not sold directly. Each box guarantees at least one Rare, an Epic within every 5 boxes and a Legendary within every 20. In our terms these are hard pity counters on each tier, with `H = 5` for Epic and `H = 20` for Legendary. Because the boxes are not sold, the cost is measured in play time rather than money, but the arithmetic is identical.

**Genshin Impact (pulls, current versions).** MA102 week 10 showed how a 0.6% base rate, soft pity from about pull 74 and a hard guarantee at 90 produce the published 1.6% consolidated rate. The same point applies here from a different angle. The consolidated rate describes the average. The pity rule describes the worst case. Only the second tells a player their maximum spend. The FTC's 2025 order against HoYoverse, which required the company to disclose odds and currency exchange rates, turned on exactly that gap between the rate on the page and the money spent.

Three games, three mechanisms (protection, crafting currency, pity counters), one question underneath: how far can a collector's cost exceed the average, and who tells them?

### Design judgment

- **Decide the worst case you are willing to sell.** Without pity or crafting, the 90th-percentile wait for a 1% item is 230 boxes, 2.3 times its mean, and the 99th percentile is 459. If you would be uncomfortable with a player spending that much, cap it with a pity rule or a crafting path.
- **Duplicate protection is for the middle, pity is for the tail.** Pick by which group you are trying to help. Protection makes the typical experience cheaper. Pity makes the unlucky experience bounded. Both change revenue, so model both before launch.
- **Tradeable duplicates change the analysis.** If players can sell duplicates to each other, a set's cost to one player is lower, but the boxes then produce assets with real market value. That is the trigger for the gambling rulings in the Netherlands in 2018 and a topic for week 7.
- **The disclosure you are required to print is not the one players need.** The next section proposes a fuller one.

### Check this example

1. A set has 10 items, all at 10%. Compute the expected number of boxes to complete it and the expected boxes for the last item alone.
2. In the 15/4/1 set, what is the chance that a collector who has opened 100 boxes still lacks the Legendary?

<details>
<summary>Answers</summary>

1. `H_10 = 2.929`, so `E[T] = 10 × 2.929 = 29.3` boxes. The last item has a 10% chance per box, so it takes 10 boxes on average, about a third of the total.
2. `0.99^100 = 0.366`, so 36.6%.

</details>

## 3. What a good disclosure shows

The rules in section 1 set a floor: per-item or per-type odds before purchase. Research on how companies meet that floor shows why a floor is not enough.

Xiao and colleagues studied the 100 highest-grossing iPhone games in mainland China, the first market to require disclosure. They found loot boxes in 91 of them, and disclosures for about 95.6% of those. But only 5.5% put the odds on the purchase page itself. The rest placed them in menus, help screens or websites, where a buyer must go looking. The authors called this "sludge", friction that makes information technically available and practically unseen. A follow-up study of South Korea after its law took effect found paid loot boxes in 90 of the top 100 iPhone games and disclosures in 84.4% of those, with regulators fining several companies for publishing false or misleading odds.

Even well-placed odds may not change much. In a survey of 879 players in mainland China, 84.6% of loot box buyers said they had seen probability disclosures, and only 19.3% of that group said they spent less as a result. A per-item percentage is hard to turn into a cost, which is what section 2 just showed.

A disclosure that serves the buyer answers four questions, in this order, on the purchase screen:

1. **What can I get, and how likely is each item?** The per-item odds, as the rules require. Show them per item, not only per rarity, when items within a rarity differ in desirability.
2. **What protects me from bad luck?** State the pity, protection or crafting rules exactly: "A Legendary is guaranteed within 40 boxes. You will not receive a duplicate Rare until you own all four."
3. **What does the thing I want cost?** For the most desirable item and for the full set, give the median and the 90th percentile in boxes and in real money. The code in section 2 computes these. If a pity rule exists, give the maximum as well.
4. **What is the real price of one box?** If the box is bought with premium currency, show the real-money price at the most common bundle rate. The FTC's 2025 order required exchange-rate disclosure for exactly this reason, and week 3 showed how currency bundles hide it.

None of these requires the studio to reveal anything it does not already know. Every number comes from the drop table and the price list. The cost of this disclosure is commercial: some players who see "$230 for the unluckiest tenth" will not buy. That is the point of it.

## 4. The evidence on harm, read carefully

Arguments about loot boxes often claim more than the research shows, on both sides. Here is what the most cited work supports.

**The correlation.** Zendle and Cairns surveyed 7,422 gamers in 2018 and found that the amount spent on loot boxes was related to the severity of problem gambling (effect size η² = 0.054). The link was much weaker for other in-game purchases (η² = 0.004), which suggests something about loot boxes specifically. Many later studies in Western samples found similar associations. The UK government's 2022 response to its call for evidence accepted that loot box purchasing is associated with gambling, financial and mental health harms.

**What the correlation does not show.** A survey at one point in time cannot say which way the link runs. Loot boxes might lead some players toward problem gambling. Or people who already gamble heavily might also spend heavily on loot boxes. Zendle and Cairns said this themselves. The link also varies by context. A preregistered survey in mainland China, where legal gambling products are scarce, did not replicate the correlation with problem gambling, and found only small correlations between loot box spending and past-year gambling and impulsiveness.

**What that means for you as a designer.** The evidence supports treating paid random rewards as a product with a known association with harm for a minority of buyers, and designing with that minority in mind. It does not support claims that every loot box buyer is being harmed, or that loot boxes are harmless because most buyers spend little. Week 9 shows that spending in live games is highly concentrated, which is why the minority matters so much for both revenue and harm.

Reasonable design responses include spending limits and cooling-off prompts, age gates, direct real-money pricing, bounded worst cases through pity, and disclosure of the kind in section 3. Some studios choose a different response and sell only direct-purchase items or battle passes, which week 5 covered. That trade-off between revenue and risk is a business decision you should make explicitly and write down.

## In-class activity (25 minutes)

Work in pairs. You are given a box design for a fantasy MMO's mount collection. The set has 12 mounts: 8 Common at 9% each, 3 Rare at 8% each, and 1 Mythic at 4%. A box costs 150 gems, and the most common bundle sells 1,000 gems for $9.99.

1. Check that the odds sum to 1. Use the section 2 code (change `SET`) to compute the mean, median and 90th percentile boxes for the full set, and convert each into dollars.
2. Compute the median and 90th-percentile boxes for the Mythic alone.
3. Propose one rule (duplicate protection, pity, or a crafting currency) that brings the 90th-percentile cost of the Mythic below $60. Show the arithmetic.
4. Draft the four-part disclosure from section 3 for your final design, in at most 80 words.

Expected output: a table of costs before and after your rule, and the disclosure text, which two pairs will swap and critique.

## Common misconceptions

- **"If the odds are published, players know what they're paying."** They know the chance per box. The cost of a set, or of one rare item for an unlucky buyer, has to be computed, and most players will not compute it.
- **"A 1% item takes 100 boxes."** That is the mean. Half of buyers need 69 or fewer, and one in ten needs 230 or more.
- **"Duplicate protection fixes the unlucky tail."** It helps the median. The tail comes from waiting for one rare item, and protection only matters when there is more than one item left to choose from.
- **"The research proves loot boxes cause problem gambling."** It shows a consistent association in many Western samples. The direction of cause is not established, and the association varies by country.

## Check yourself

1. A set has 5 Common items at 18% each and 1 Epic at 10%. Using inclusion-exclusion by hand, write out the terms for `E[T]` grouped by `(j_common, j_epic)` and compute the result. (Hint: there are 11 non-empty groups.)
2. Your game's box has a 2% Legendary and no pity. The design team proposes a hard pity at 60 boxes. Compute the chance that a buyer reaches the pity box, and the new expected number of boxes for the Legendary. (Use MA102 week 10's formula `E = (1 − (1 − p)^H) / p`.)
3. A studio publishes "Legendary: 1%" on its purchase screen and a full cost table in a help article two menus away. Which of the four disclosure questions in section 3 does the purchase screen answer? What would you change?
4. A colleague says loot box research is settled and all loot boxes are gambling. Another says the research shows nothing. Write two sentences that state what the evidence supports.

<details>
<summary>Answers</summary>

1. Groups with `j_epic = 0`: `j = 1..5` Commons, sign `(−1)^(j+1)`, count `C(5, j)`, probability `0.18 j`. With `j_epic = 1`: `j = 0..5` Commons, sign `(−1)^j`, count `C(5, j)`, probability `0.18 j + 0.10`. The first group sums to `H_5 / 0.18 = 2.2833 / 0.18 = 12.685`. The second sums to `1/0.1 − 5/0.28 + 10/0.46 − 10/0.64 + 5/0.82 − 1/1.0 = 10 − 17.857 + 21.739 − 15.625 + 6.098 − 1 = 3.355`. Total `E[T] ≈ 16.04` boxes.
2. Reaching box 60 needs 59 misses: `0.98^59 = 0.304`, so 30.4%. `E = (1 − 0.98^60) / 0.02 = (1 − 0.298) / 0.02 = 35.1` boxes, down from 50.
3. Only the first question, per-item odds. Move the median and 90th-percentile cost in real money, the pity or protection rules, and the real price of one box onto the purchase screen.
4. For example: "Many studies find that people who spend more on loot boxes tend to have more gambling problems, so paid random rewards carry a real risk for a minority of buyers. The studies cannot yet say whether loot boxes cause that, and the link is weaker in some countries, so the case for specific rules rests on precaution and consumer protection rather than proof of cause."

</details>

## Lab / assignment hook

[Lab 06, cost of a collection and a disclosure page](../labs/lab06.md). You implement the inclusion-exclusion cost functions, a duplicate-protection model and a pity simulation, reproduce the table in section 2, then design a box for your team's game and write its full four-part disclosure. The disclosure and its numbers go into the ethics analysis assignment (20%).

## Sources

- Hearthstone Wiki (hearthstone.wiki.gg), "Card pack" (accessed September 2026). Legendary duplicate protection from 10 August 2017; protection extended to all rarities on 26 March 2020.
- Hearthstone Wiki, "Arcane Dust" (accessed September 2026). Crafting 40 / 100 / 400 / 1,600 and disenchanting 5 / 20 / 100 / 400 dust for normal Common, Rare, Epic and Legendary cards; unchanged by the May 2022 golden-upgrade patch.
- Wikipedia, "Loot box" (accessed September 2026). Overwatch's June 2017 reduction in duplicate frequency; China's December 2016 announcement and May 2017 start of disclosure; Google Play's policy by May 2019; the ESA's August 2019 announcement at the FTC workshop; Apple's December 2017 change.
- Apple, App Store Review Guidelines, section 3.1.1 (current text, accessed September 2026). Odds of each type of item must be disclosed before purchase.
- Google Play Console Help, "Payments" policy (accessed September 2026). Odds must be disclosed in advance of, and in close and timely proximity to, the purchase.
- Game World Observer, "South Korea passes loot box probability disclosure law" (28 February 2023). Amendment to the Game Industry Promotion Act, passed 27 February 2023; disclosure in games, ads and websites; penalties.
- Xiao, L. Y. & Park, S. (2025). "Better than industry self-regulation: Compliance of mobile games with newly adopted and actively enforced loot box probability disclosure law in South Korea." *Acta Psychologica*. doi:10.1016/j.actpsy.2025.105490. Law in force from March 2024; 90 of the top 100 iPhone games with paid loot boxes; 84.4% disclosing; enforcement actions.
- US Federal Trade Commission, press release, "Genshin Impact game developer will be banned from selling lootboxes to teens under 16 without parental consent, pay a $20 million fine" (17 January 2025). Allegations on odds and virtual currency; order requirements on odds, exchange rates and direct real-money purchase.
- Xiao, L. Y., Henderson, L. L., Yang, Y. & Newall, P. W. S. (2021). "Gaming the system: sub-optimal compliance with loot box probability disclosure regulations in China." *Behavioural Public Policy*. doi:10.1017/bpp.2021.23. 91 of 100 top-grossing iPhone games with loot boxes; disclosures missing for 4.4%; 5.5% on the purchase page.
- Xiao, L. Y., Fraser, T. C. & Newall, P. W. S. (2022). "Opening Pandora's Loot Box: Weak links between gambling and loot box expenditure in China, and player opinions on probability disclosures and pity-timers." *Journal of Gambling Studies*. doi:10.1007/s10899-022-10148-0. N = 879; no replication of the problem-gambling link; 84.6% saw disclosures, 19.3% of those spent less.
- Zendle, D. & Cairns, P. (2018). "Video game loot boxes are linked to problem gambling: Results of a large-scale survey." *PLOS ONE* 13(11): e0206767. doi:10.1371/journal.pone.0206767. n = 7,422; η² = 0.054 for loot boxes vs 0.004 for other purchases; direction of cause unclear.
- UK Department for Culture, Media and Sport, government response to the call for evidence on loot boxes (July 2022), as summarized in Wikipedia, "Loot box". Association with harms accepted; industry-led measures preferred to legislation at that time.
- Wikipedia, "Overwatch 2" (accessed September 2026). Season 15 (February 2025) earned-only loot boxes with at least one Rare, an Epic within every 5 and a Legendary within every 20 boxes.
- The 15/4/1 set, box price and mount set are invented for teaching.

## Interactive spec: examples/w06-set-completion-cost.html

**The one insight.** The disclosure page (per-item odds) barely changes when the rarest item gets rarer, while the cost of completing the set, especially for unlucky buyers, changes enormously. Duplicate protection moves the middle of the cost curve; pity moves the tail.

**Layout.** Two linked views side by side at 1280px, stacked at 390px. Left: "What the disclosure shows", a horizontal bar chart of the per-item chance for each tier (Common, Rare, Legendary), with the tier count and tier total printed on each bar. Right: "What the set costs", a cumulative curve with boxes `n` on the x axis (0 to a max that auto-scales to the 99th percentile, at least 100) and share of collectors complete on the y axis (0 to 100%). Vertical markers for mean, median and 90th percentile, labeled with boxes and money. A thin second curve shows the Legendary alone (`1 − (1 − p_L)^n`, or the pity version) for comparison.

**Controls (all update instantly).**
- Common count `n_C` 1 to 20 (default 15), Rare count `n_R` 0 to 8 (default 4), Legendary count fixed at 1.
- Legendary chance `p_L`, 0.2% to 5% in 0.1-point steps, default 1.0%.
- Rare per-item chance `p_R`, 1% to 10% in 0.1-point steps, default 4.5%. Common per-item chance is derived: `p_C = (1 − p_L − n_R p_R) / n_C`; if it falls below 0, disable the change and show "odds exceed 100%".
- Duplicate protection toggle (off by default).
- Legendary pity toggle with a number input `H`, 10 to 200, default 40 (off by default).
- Box price in dollars, 0.25 to 5.00, default 1.00.
- Reset button.

**Formulas.**
- No protection, no pity: inclusion-exclusion by tier counts, `P(T ≤ n) = Σ (−1)^(j_C+j_R+j_L) C(n_C, j_C) C(n_R, j_R) C(1, j_L) (1 − j_C p_C − j_R p_R − j_L p_L)^n`, and `E[T] = Σ_{nonempty} (−1)^(k+1) × count / P(S)`.
- Duplicate protection: tiers drawn at `n_C p_C`, `n_R p_R`, `p_L`; completion needs `n_C` Common-tier hits, `n_R` Rare-tier hits and 1 Legendary hit. Compute `P(T ≤ n)` by a dynamic program over capped hit counts `(a, b, c)` with `a ≤ n_C`, `b ≤ n_R`, `c ≤ 1`.
- Pity (with or without protection): dynamic program over `(owned or hit counts, boxes since start without Legendary)`; the Legendary chance is 1 on box `H` if none yet. After the Legendary is owned the counter is dropped. Run in a Web Worker or cap `n` at `max(4 × H, 600)` to keep it responsive.
- `E[T] = Σ_{n≥0} (1 − P(T ≤ n))`, summed until `1 − P(T ≤ n) < 1e-9`. Percentiles are the smallest `n` with `P(T ≤ n) ≥ q`.
- Money = boxes × price.

**Readouts.** Mean (two decimals), median, 90th and 99th percentile in boxes and dollars; Legendary-alone median and 90th percentile. A sentence under the chart: "The disclosed chance of the Legendary is X%. One collector in ten needs Y boxes ($Z) or more."

**Test values.**
- 20 items at 5% (set `n_C = 19`, `n_R = 0`, `p_L = 5%`): mean 71.95, median 67, 90th 103.
- Defaults (15/4/1, 5.4% / 4.5% / 1%): mean 120.55, median 90, 90th 230, 99th 459; Legendary alone median 69, 90th 230.
- Defaults + protection: mean 103.22, median 70, 90th 230.
- Defaults + pity 40: mean 69.70, median 65, 90th 100.
- Defaults + protection + pity 40: mean 36.61, median 40, 90th 40.
- `p_L = 0.5%` (Common derived 5.433%): Legendary-alone 90th percentile 460.

**Accessibility and style.** Native range inputs and checkboxes with visible labels; percentile markers carry text labels, not color alone. Colors from `templates/interactive-tokens.css`. No card art, logos or game characters; tiers are drawn as plain shapes.
