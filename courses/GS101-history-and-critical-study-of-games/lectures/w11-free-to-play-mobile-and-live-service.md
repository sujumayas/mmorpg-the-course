# GS101 · Week 11 — Free-to-play, mobile, and live service

**Why this matters:** Most of the money in games today comes from games that cost nothing to start. That business model did not appear from nowhere, and it is not neutral. It changes who a game is designed for, what a designer is asked to measure, and what kind of criticism a game deserves. This week you learn the history of free-to-play, the one equation behind it, and how to read a live game's design through its revenue model.

**You will be able to:**
- Place the key steps of free-to-play and live service on a dated timeline, from Nexon's QuizQuiz (1999) to the battle pass.
- Compute monthly revenue from players, payer share and average spend per payer, and check the result against King's published 2013 figures.
- Compare a subscription game and a free-to-play game by computing how many players each needs to earn the same revenue.
- Critique a monetization design by computing how concentrated its spending is and saying whose experience the design then serves.

**Before class:** Tristan Donovan, *Replay: The History of Video Games* (Yellow Ant, 2010), the late pages on online, casual and social games (skim). The course reader lists the pages. Read the Wikipedia article "Free-to-play" in full (about 20 minutes), paying attention to the history section and the whale/dolphin/minnow terms. Bring one free-to-play game you have played and a rough count of what you have spent on it.

**Prerequisites from earlier courses:** None formally. [GS101 week 10](w10-world-of-warcraft-and-the-mass-market-mmo.md) covers the subscription MMO this week contrasts with. If you are taking them alongside, [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) gives the expected-lifetime result used in section 3, and [MA102 week 12, descriptive statistics](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md) explains why the mean and median of skewed data differ. Looking ahead, [MMO304 week 1, artificial scarcity](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w01-why-virtual-economies-exist-artificial-scarcity.md) (year 3) explains why a copyable virtual item can have a price. The full business treatment comes later, in MMO403 weeks 1, 2 and 9 ([syllabus](../../MMO403-business-monetization-and-ethics-of-live-games/syllabus.md)).

**Interactive:** [F2P revenue funnel](../examples/w11-f2p-revenue-funnel.html). Keep it open during section 2.

---

## 1. Three ways to sell a game

Every game has to pay for itself somehow. For most of this course's history, the answer was one of two.

**The box (one-time purchase).** You pay once and own a copy. The publisher's revenue is copies sold times price. The design problem is getting you to buy. After that, the publisher earns nothing more from your play, so it has no direct reason to keep you playing for years.

**The subscription.** You pay every month to keep playing. Ultima Online, EverQuest and World of Warcraft (week 10) all used this model. Revenue is subscribers times the monthly fee. The design problem is keeping you subscribed, which is why subscription MMOs reward time spent: long levelling curves, raids that take weeks to clear, and reputation grinds.

**Free-to-play (F2P).** You pay nothing to start and can play indefinitely without paying. The publisher earns from a minority of players who choose to buy things inside the game: cosmetics, conveniences, extra content, random packs, or a season pass. The design problem is twofold. The game must attract a very large number of players, and it must persuade some of them to spend.

A business model is a design constraint. The same fantasy world designed for a box, a subscription and free-to-play will end up with different pacing, different progression and different social systems. When you read a game critically, the business model belongs in your context step (week 1's step 4) and often explains rules that otherwise look odd.

### A timeline of free-to-play

Place these on the timeline you are building for the course project.

| Year | Event | Why it matters |
|---|---|---|
| 1999 | Nexon releases QuizQuiz in South Korea | One of the first free-to-play online games funded by selling items. Most items were cosmetic, and a few gave small advantages. |
| 2003 | MapleStory launches in South Korea | Nexon's item-selling model in a side-scrolling MMO, later localized for many regions. |
| 2008 | Apple's App Store opens (10 July) | A worldwide store on a phone most people carry. Apps are free or paid at first. |
| 2009 | Apple adds in-app purchases | In-app purchase quickly becomes the dominant way to earn from apps, especially games. |
| 2009 | Dungeons & Dragons Online goes free-to-play (summer, "Eberron Unlimited") | A Western subscription MMO switches. The company later says subscriptions rose 40% by October. |
| 2009 | League of Legends launches (27 October in North America) | Free-to-play from day one, earning from purchasable character customization. Publishers of the time were confused by the model. |
| 2010 | The Lord of the Rings Online goes free-to-play (September in North America, November in Europe) | A second major subscription MMO adds a free option with an in-game store. |
| 2011 | Team Fortress 2 goes free-to-play (June) | A paid PC shooter becomes free, selling items through an in-game store tied to Steam. |
| 2012 | Candy Crush Saga released (12 April, first on Facebook) | King's top title. It produced 78% of King's gross bookings in the last quarter of 2013. |
| 2013 | Dota 2's Compendium for The International 2013 | An early form of the battle pass. |
| 2013 | Warframe open beta (March) | Free-to-play shooter designed around continual updates. |
| 2014 | Destiny released (9 September) | A boxed console game designed to keep changing after release. |
| 2017 | Fortnite Battle Royale released | Free-to-play with a seasonal battle pass. Fortnite as a whole grossed about US$9 billion by December 2019. |
| 2018 | Dutch regulator orders changes to four games' loot boxes; Valve blocks Counter-Strike: Global Offensive case opening for Dutch and Belgian players (July) | Governments begin treating some paid random rewards as gambling. |

Two patterns stand out. The model began in Asian PC games and reached Western players first through struggling subscription MMOs and then through phones. And every step made the store part of the game, not a separate shop you visit once.

## 2. Worked example: why "free" can earn twelve times more

### The hook

In June 2011 Valve made Team Fortress 2 free to play and started selling weapons, hats and other items in an in-game store. Within nine months, Valve reported that the game's revenue had risen by a factor of twelve. The game had become free and was making far more money than when it cost money. How can giving a game away increase revenue twelvefold?

### The model, stated once

Every free-to-play revenue report reduces to one product:

```
monthly revenue  R = N × p × A
average revenue per user  ARPU = p × A
```

- `N` is the number of players active in the month (monthly active users, MAU).
- `p` is the payer share: the fraction of those players who spend anything that month.
- `A` is the average revenue per paying user in the month (ARPPU).
- `ARPU` spreads the revenue over everyone, payers and non-payers. It is the revenue one extra player brings, on average.

A subscription game is the special case where every active player pays one fixed amount, so `p = 1` and `A` equals the fee. Its revenue is `R = S × fee`, where `S` is subscribers.

The equation shows the two levers free-to-play pulls. Removing the price at the door raises `N`, often by a large multiple. And spending has no ceiling, so `A` is an average over players who spend a little and a few who spend a great deal. A subscription caps every player at the fee.

### Numbers you can check: King in late 2013

When King, maker of Candy Crush Saga, applied to list its shares in the United States in 2014, it published exactly these three quantities. For the quarter ending 31 December 2013:

| Quantity | King's name for it | Value (Q4 2013, monthly averages) |
|---|---|---|
| `N` | average monthly unique users (MUUs) | 304 million |
| payers | average monthly unique payers (MUPs) | 12.165 million |
| `p` | payers / users | 12.165 / 304 = 4.0% |
| `A` | monthly gross average bookings per paying user (MGABPPU) | US$17.32 |

Compute the revenue the model predicts:

```
R per month = 304,000,000 × 0.040 × 17.32 ≈ $210.6 million
R per quarter = 3 × 210.6 ≈ $632 million
```

King reported gross bookings of US$632 million for that quarter. The model matches to the million, because King defines its per-payer average from those same bookings. That is the point of the check. The three numbers a company reports are one equation, and if you know any two of the terms and the total you can recover the third.

Now the comparison. King's ARPU was `0.040 × 17.32 = $0.69` per player per month. A subscription MMO charging US$15 a month (World of Warcraft's one-month US price, unchanged since its 2004 launch) earns $15 from every active player. So:

```
F2P players needed per subscriber = 15 / 0.69 ≈ 21.7
```

With the unrounded ARPU of $0.6928, the ratio is 21.65, which is the value the interactive shows.

At King's rates, a free-to-play game needs about 22 active players to earn what one subscriber pays. That sounds like a terrible deal until you remember that the subscription's price at the door turns most potential players away, and the free game's does not.

Here is the same idea for an invented game with 1,000,000 monthly players and King's US$17.32 average spend per payer:

| Payer share `p` | Payers | ARPU | Monthly revenue | Subscribers at $15 needed to match |
|---|---|---|---|---|
| 1% | 10,000 | $0.17 | $173,200 | 11,547 |
| 2% | 20,000 | $0.35 | $346,400 | 23,093 |
| 4% | 40,000 | $0.69 | $692,800 | 46,187 |
| 8% | 80,000 | $1.39 | $1,385,600 | 92,373 |

Every row is `1,000,000 × p × 17.32`, and the last column divides that by 15. Doubling the payer share doubles revenue, which is why free-to-play teams spend so much effort on the first purchase.

Back to the hook. We do not know Team Fortress 2's `N`, `p` or `A` before and after, so we cannot decompose Valve's twelvefold figure. But the model says what must have happened. A twelvefold rise in revenue means `N × p × A` grew twelvefold. Removing the price raised `N`. Selling items with no cap on how many a player can buy let `A` for the keenest players rise above a one-time box price. Any combination of the two that multiplies to 12 fits.

### The second view: who actually pays

`A` is an average, and averages of spending hide a lot. In January 2014 the analytics firm Swrve reported, across the free-to-play mobile games it tracked, that only 1.5% of players spent any money, and that half of all in-game purchase revenue came from 0.15% of players. Since 0.15 / 1.5 = 0.1, that means **the top 10% of payers produced 50% of the revenue.** Players nicknamed the biggest spenders "whales," a term borrowed from casino gambling.

A simple model for this kind of skew is a **Pareto distribution**, the "80/20" curve. It has one shape number, `α` (alpha). The smaller `α` is, the more the top spenders dominate. Its useful property:

```
share of revenue from the top fraction q of payers = q^(1 − 1/α)
```

Set the top 10% share to 50% and solve: `0.1^(1 − 1/α) = 0.5` gives `α ≈ 1.43`. Here is what different shapes imply, holding the average spend per payer at King's $17.32:

| Shape `α` | Top 1% of payers' share | Top 10% share | Top 20% share | Median payer spends |
|---|---|---|---|---|
| 1.16 (the "80/20" curve) | 53% | 73% | 80% | $4.34 |
| 1.43 (fits Swrve's figure) | 25% | 50% | 62% | $8.46 |
| 2 | 10% | 32% | 45% | $12.25 |
| 3 | 5% | 22% | 34% | $14.55 |

The median comes from the Pareto rule `median = x_m × 2^(1/α)`, where the minimum spend `x_m = A × (α − 1) / α`. Check one row. With `α = 2`, `x_m = 17.32 × 0.5 = 8.66` and the median is `8.66 × 2^0.5 = 12.25`.

Look at the first row. The average payer spends $17.32, but the typical (median) payer spends $4.34, and the top 1% of payers bring in more than half the money. This is the mean-versus-median lesson from MA102 week 12, with money attached. Treat the Pareto shape as a model we chose, not as King's actual data, which King did not publish at this level.

### A visual you can move

Open `examples/w11-f2p-revenue-funnel.html`. The left panel is a funnel for one game in two versions side by side: players at the door, payers, and monthly revenue, for a subscription and a free-to-play version. Drag the payer share and watch the revenue bars. The right panel is the spending curve for the free version's payers, sorted from biggest to smallest, with the cumulative share of revenue drawn above it. Drag `α` down from 3 to 1.2. The revenue on the left does not move, because the average is fixed. The right panel shows the same revenue coming from fewer and fewer people. Two games with identical earnings can have completely different player bases behind the numbers.

### Cross-game recognition

Rewrite each case as `N × p × A` and ask which term the design is built to move.

**Team Fortress 2 (from June 2011).** Going free raised `N`. The item store, tied to Steam, created `A` where there had been only a one-time price, and a player could now spend again and again.

**League of Legends (from October 2009).** Free from launch, so `N` was never gated. Riot earns from character customization. A design that sells mainly cosmetics keeps paying and non-paying players on equal terms in a match, which protects the competitive game at the cost of a lower `A` than a game selling power.

**Fortnite Battle Royale (from 2017) and the battle pass.** A battle pass is a fixed-price seasonal purchase that unlocks tiers of rewards as you play. It puts a soft ceiling on most payers' `A` (the pass price each season) and raises `p` by making a first purchase feel like good value. In the shape table, it pushes spending toward a larger `α`, which means flatter spending that depends less on whales. Epic still sells other items alongside it, so the ceiling is not absolute.

**Dungeons & Dragons Online (from 2009).** A hybrid. Players could play free, buy from a store, or subscribe. The company reported that subscriptions rose 40% after the switch. Here the free tier raised `N` for the subscription itself, which became one of the things free players could buy.

Four games, one equation. When you meet a new free-to-play game, your first critical question should be which term each rule is designed to move, and at whose expense.

### Design judgment

Free-to-play is neither a scam nor a gift. It is a set of trade-offs a designer should choose knowingly.

- **Strength: the door is open.** Removing the price lets in players who could never pay a box price or a monthly fee, including players in lower-income countries and children. In the funnel, `N` is the term that grows most.
- **Strength: spending can match enjoyment.** A player who loves the game can pay more than a subscription would take, and a player who does not can pay nothing.
- **Cost: the designer is asked to serve the whale.** When half the revenue comes from 10% of payers, pressure builds to design content, pacing and prices around the players who spend most. Their experience becomes the one that pays for everyone else's. Decide whether you accept that, and which features you refuse to build for it.
- **Cost: frustration becomes a product.** If the store sells relief from waiting, grinding or losing, the game has a reason to make waiting, grinding and losing worse. A subscription game's time sinks have a similar incentive, but they sell the same thing to everyone at one price.
- **Cost: random paid rewards look like gambling.** When the item sold is a random draw (a loot box), regulators in the Netherlands and Belgium have acted. A designer choosing random rewards is choosing a legal risk as well as a feeling.
- **Decide deliberately:** what you sell (cosmetic, convenience, content, power), whether the price is fixed or random, and what the game is like for the player who never pays. That last player is most of your audience.

### Check yourself (worked example)

1. A game has 2 million monthly players, 3% of whom pay, spending an average of $20 each. What is its monthly revenue and ARPU? How many $15 subscribers would earn the same?
2. A studio says its revenue per payer is $30 and its revenue per player is $0.60. What is its payer share?
3. Using the Pareto rule, if the top 10% of payers produce 32% of revenue, what is `α`? What share do the top 20% produce?

<details>
<summary>Answers</summary>

1. `R = 2,000,000 × 0.03 × 20 = $1,200,000` a month. ARPU is `0.03 × 20 = $0.60`. Matching subscribers: `1,200,000 / 15 = 80,000`.
2. `ARPU = p × A`, so `p = 0.60 / 30 = 0.02`, or 2%.
3. `0.1^(1 − 1/α) = 0.32`, so `1 − 1/α = ln 0.32 / ln 0.1 ≈ 0.495` and `α ≈ 1.98`, about 2. Then the top 20% produce `0.2^0.495 ≈ 0.45`, about 45%, matching the α = 2 row of the table.

</details>

## 3. Live service: the game that never ships

"Live service" (also "games as a service") means a game designed to keep receiving new content, and to keep earning, for an open-ended period after release. The idea began with subscription MMOs, whose fees paid for servers, staff and new content. Warframe (2013) and Destiny (2014) brought it to shooters, and free-to-play games adopted it because a free game that stops changing stops earning.

A live game is judged by a second number alongside ARPU: how long players stay. Suppose that each month, a fraction `r` of this month's players are still playing next month (the **retention rate**). The number of months a player stays is then a geometric random variable, the same shape as "kills until the drop" in MA102 week 7, and its expected value is:

```
expected lifetime in months  L = 1 / (1 − r)
lifetime value  LTV = ARPU × L
```

Take King's ARPU of about $0.69 and try four invented retention rates:

| Monthly retention `r` | Expected lifetime `L` | LTV at $0.69 ARPU |
|---|---|---|
| 50% | 2 months | $1.38 |
| 80% | 5 months | $3.45 |
| 90% | 10 months | $6.90 |
| 95% | 20 months | $13.80 |

Moving retention from 90% to 95% doubles the value of every player. That single fact explains most of the design of live games. Seasons, daily login rewards, limited-time events and roadmaps are all attempts to raise `r`. When a live game announces "Season 7," read it as a retention intervention first and a creative decision second, then look for evidence of both.

It also explains why live games are hard to study historically. A boxed game exists as a fixed object you can replay. A live game exists as a series of versions, most of which no longer run. When you write about one, always name the season or patch, just as MMO303 asks you to name the patch for a formula.

## 4. Reading a live game critically

You now have two numbers to bring to a close reading of any free-to-play or live game: what the store sells and to whom (`p`, `A` and the shape of spending), and what the game does to keep players (`r`). Use them in week 1's method.

- In **find the machine**, trace one rule to the term it moves. A daily reward moves `r`. A starter pack at a low price moves `p`. A random premium draw moves `A` for the few who chase it.
- In **place it in context**, name the business model and the market (platform, region, year). A 2003 Korean PC game and a 2017 console battle royale faced different players and different laws.
- In **make one claim**, argue about who the design serves. "This event is built for players who spend over $100 a month" is a claim you can support with the store's prices and the event's rewards.

A caution about evidence. Companies publish these numbers when it suits them (King published its figures because listing its shares required it). Most do not. Industry reports like Swrve's cover only the games using that firm's tools. When you cite a spending figure, say whose figure it is, what games it covers and what month it describes.

## In-class activity (25 min)

In pairs. Materials: one free-to-play game each pair has played, its store screen (on a phone or from memory), the model from section 2 and the interactive.

1. (8 min) List everything the store sells, with prices. Label each item cosmetic, convenience, content, power or random.
2. (7 min) For each label, write which term of `N × p × A` or `r` it is designed to move, and why.
3. (5 min) Estimate `p` and `A` for the game (be honest that these are guesses), then use the interactive's `α` slider to pick a shape you think fits. Write down the median payer's spend it implies.
4. (5 min) Write one sentence naming the player whose experience this store is built around.

Expected output: the labelled store list, the term each item moves, your `p`, `A`, `α` estimates, and the one-sentence claim.

## Common misconceptions

- **"Free-to-play games make money from everyone a little."** Usually a few percent pay at all (4% at King in late 2013, 1.5% across Swrve's network in January 2014), and a small share of those pay most of the money.
- **"ARPU and ARPPU are the same thing."** ARPU averages over all players. ARPPU averages over payers only. `ARPU = p × ARPPU`, so they differ by a factor of 1/p, which is 25 at King's 4% payer share.
- **"A higher average spend means most payers spend more."** Not when spending is skewed. With `α = 1.16` and a $17.32 average, the median payer spends $4.34.
- **"Live service is a free-to-play invention."** Subscription MMOs were live services first. Free-to-play games adopted the model because free games need continuing revenue.

## Check yourself

1. King's Q4 2013 figures were 304 million monthly users, 4.0% payers and $17.32 per payer per month. If the payer share had been 5% with everything else unchanged, what would quarterly bookings have been?
2. A subscription game at $15 has 300,000 subscribers. It goes free-to-play and reaches 3 million monthly players with a 5% payer share. What ARPPU does it need to match its old revenue?
3. A live game has an ARPU of $1.20 and monthly retention of 85%. What is the expected LTV? A designer proposes an event that raises retention to 88% but lowers ARPU to $1.10. Is the change worth it by LTV?
4. Place these in order and give a year for each: League of Legends launches, Apple adds in-app purchases, QuizQuiz launches, Team Fortress 2 goes free, the first battle pass-like Compendium.

<details>
<summary>Answers</summary>

1. `304,000,000 × 0.05 × 17.32 × 3 ≈ $789.8 million`, up from about $632 million.
2. Old revenue is `300,000 × 15 = $4,500,000` a month. The free game has `3,000,000 × 0.05 = 150,000` payers, so ARPPU must be `4,500,000 / 150,000 = $30`.
3. At 85%, `L = 1 / 0.15 ≈ 6.67` months and LTV ≈ `1.20 × 6.67 = $8.00`. At 88%, `L = 1 / 0.12 ≈ 8.33` months and LTV ≈ `1.10 × 8.33 = $9.17`. Yes, by LTV the event is worth it, about $1.17 more per player.
4. QuizQuiz (1999), Apple in-app purchases (2009), League of Legends (October 2009), Team Fortress 2 free (June 2011), Dota 2 Compendium (2013).

</details>

## Lab / assignment hook

[Lab 11, free-to-play teardown](../labs/lab11.md). You build a spreadsheet of one free-to-play game's store, estimate `N`, `p`, `A` and `r` from public sources, and write a 600-word critique naming who the store is built for. The timeline table in section 1 also feeds the course's timeline project.

## Sources

- Wikipedia, "Team Fortress 2". Free-to-play from June 2011 with items sold through Steam; Valve's report that revenue rose twelvefold within nine months.
- King Digital Entertainment plc, Form F-1/A, Amendment No. 3, filed with the US SEC on 25 March 2014 (file 333-193984). Average MUUs 304 million, average MUPs 12.165 million, MGABPPU US$17.32 and gross bookings US$632 million for the quarter ended 31 December 2013; about 4% of MUUs paying in December 2013; definition of MGABPPU.
- Johnson, E. (26 February 2014). "A Long Tail of Whales: Half of Mobile Games Money Comes From 0.15 Percent of Players." *Recode* (now hosted by Vox). Reports Swrve's January 2014 data: 1.5% of players paid; 0.15% of players produced half of in-app purchase revenue.
- Wikipedia, "Free-to-play". Nexon's role in Korea; whale, dolphin and minnow terms.
- Wikipedia, "QuizQuiz" and "MapleStory". QuizQuiz released 1999 as an early item-funded free-to-play game; MapleStory in South Korea by 2003.
- Wikipedia, "App Store (Apple)". Opened 10 July 2008; in-app purchases added in 2009.
- Wikipedia, "Dungeons & Dragons Online". Eberron Unlimited free-to-play model, summer 2009; subscriptions up 40% by 13 October 2009, per the company.
- Wikipedia, "The Lord of the Rings Online". Free-to-play launched 10 September 2010 in North America and 2 November 2010 in Europe.
- Wikipedia, "League of Legends". North American release 27 October 2009; free-to-play with purchasable customization; publishers' confusion over the model.
- Wikipedia, "Candy Crush Saga". Released 12 April 2012, first on Facebook.
- Wikipedia, "Battle pass". Origin in Dota 2's Compendium for The International 2013.
- Wikipedia, "Warframe" and "Destiny (video game)". Warframe open beta March 2013; Destiny released 9 September 2014.
- Wikipedia, "Fortnite" and "Fortnite Battle Royale". Battle Royale released 2017 with a seasonal battle pass; Fortnite grossed about US$9 billion up to December 2019.
- Wikipedia, "Loot box". The Dutch regulator's 2018 order to four games; Valve's July 2018 block on case opening in the Netherlands and Belgium.
- Wikipedia, "Games as a service". Origin of the model in subscription MMOs such as RuneScape and World of Warcraft.
- Warcraft Wiki, "Game time" ("Subscription"), and Colp, T. (22 March 2024), PC Gamer, on World of Warcraft's subscription price. US$15 for one month, unchanged since the 2004 launch.
- Donovan, T. (2010). *Replay: The History of Video Games*. Yellow Ant, East Sussex (xiv + 501 pp.).

## Interactive spec: examples/w11-f2p-revenue-funnel.html

**Purpose.** Show that free-to-play revenue is one product, `N × p × A`, and that the same revenue can come from very different spending patterns. Insight on first load: *the free version's revenue bar matches the subscription's, while the spending curve on the right shows the top 10% of payers producing half of it.*

**Layout.** Two linked panels side by side on desktop, stacked on mobile (funnel first). Controls under the panels, then a numbers table. Generic shapes only; no game logos, store art or characters. The words "King (Q4 2013)" and "Swrve (Jan 2014)" appear only as preset labels and in the caption with the source.

**Left panel, the funnel.** Two columns of three bars each, labelled "Subscription" and "Free-to-play". Bars: players at the door (`S` or `N`), payers (`S` or `N × p`), monthly revenue (`S × fee` or `N × p × A`). Use a log scale for the first two bar rows (players range over 10^3 to 10^9) and a linear scale for revenue; label every bar with its exact value. Under the revenue bars, print "F2P players needed per subscriber = fee / (p × A)".

**Right panel, the spending curve.** For the free version's payers, draw the Lorenz-style curve of cumulative share of revenue (y, 0 to 100%) against the top fraction of payers (x, 0 to 100%, sorted biggest spender first), using `share(q) = q^(1 − 1/α)`. Draw the diagonal (equal spending) for reference. Mark q = 1%, 10% and 20% with dots and labels. Beside the chart, show "average payer spends $A" and "median payer spends $M", with `x_m = A × (α − 1) / α` and `M = x_m × 2^(1/α)`.

**Controls.**
- Subscription: subscribers `S` (slider 10,000 to 5,000,000, log steps, default 46,187), fee (default 15, range 5 to 20, step 0.01).
- Free-to-play: players `N` (slider 10,000 to 500,000,000, log steps, default 1,000,000), payer share `p` (0.5% to 20%, step 0.1%, default 4%), ARPPU `A` (1 to 100, step 0.01, default 17.32), shape `α` (1.05 to 4, step 0.01, default 1.43).
- Presets: "King Q4 2013" (N = 304,000,000, p = 4.0%, A = 17.32, α unchanged), "Swrve Jan 2014" (p = 1.5%, α = 1.43), "Lecture table" (N = 1,000,000, A = 17.32, p = 4%). All controls keyboard operable; values update on input.

**Numbers panel.** R (monthly), R × 3 (quarterly), ARPU, payers, subscription revenue, the players-per-subscriber ratio, top 1%/10%/20% shares, mean and median payer spend.

**Test values.**
- N = 304,000,000, p = 0.04, A = 17.32: R = $210,611,200 per month; quarterly $631,833,600 (display "≈ $632 million"). ARPU $0.69 (0.6928).
- fee 15, p = 0.04, A = 17.32: players per subscriber = 21.65.
- N = 1,000,000, A = 17.32: p = 1% → $173,200; 2% → $346,400; 4% → $692,800; 8% → $1,385,600. Matching subscribers at 15: 11,547; 23,093; 46,187; 92,373 (round to nearest).
- α = 1.16: top 1% 53.0%, top 10% 72.8%, top 20% 80.1%, median $4.34 at A = 17.32.
- α = 1.43: top 10% 50.0% (50.04% unrounded), top 20% 61.6%, median $8.46.
- α = 2: top 1% 10.0%, top 10% 31.6%, top 20% 44.7%, median $12.25.
- α = 3: top 10% 21.5%, median $14.55.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Subscription and free-to-play series differ by color and by fill pattern. The curve's marked points have text labels, not color alone. Respect reduced motion.
