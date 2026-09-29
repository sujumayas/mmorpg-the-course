# MMO403 · Week 07 — Regulation: Belgium, Netherlands, China and Others

**Why this matters:** A loot box that is a normal feature in one country can be unlicensed gambling in the next, and a rating problem in a third. A live game ships one world to many markets, so the strictest market you serve often decides your design. This week you learn to read each country's rule as a test on a few facts about your box, and to predict what happens before your legal team has to tell you.

**You will be able to:**
- Encode a paid random reward as five facts (paid, chance, transfer, skill-embedded, minors) and apply eight jurisdictions' rules to it.
- Explain why the same card pack was gambling in Belgium in 2018 and not gambling in the Netherlands in 2022, naming the element of each legal test that differs.
- Compute which design changes clear which markets, and the revenue cost of a regional switch-off against a global redesign.
- Critique a monetization plan against the status of loot box rules as of September 2026, including rules that act through age ratings and consumer law rather than gambling law.

**Before class:** Belgian Gaming Commission, *Research Report on Loot Boxes* (April 2018, English translation, 25 pages); read section 5 on the four elements of a game of chance (pp. 8-12). PEGI press release "PEGI expands age rating criteria with interactive risk categories" (12 March 2026, about 5 minutes). Fields & Cotton, *Social Game Design: Monetization Methods and Mechanics* (Morgan Kaufmann, 2011), skim the material on random rewards again with this week's question in mind: which facts about the reward would a regulator ask for?

**Prerequisites from earlier courses:** [UX201 week 5, reinforcement schedules and their ethics](../../UX201-game-ux-and-player-psychology/lectures/w05-reinforcement-schedules-and-ethics.md) (why random rewards hold attention, and its 2017-2024 timeline of regulator actions, which this lecture updates rather than repeats). [MMO402 week 9, virtual property and law](../../MMO402-emergent-society-governance-and-ethics/lectures/w09-virtual-property-and-law.md) (when a virtual item has value in law). [MMO402 week 11, minors in online worlds](../../MMO402-emergent-society-governance-and-ethics/lectures/w11-minors-in-online-worlds.md) (age gates and defaults). From this course, [week 6, loot boxes and probability disclosure](w06-loot-boxes-and-probability-disclosure.md) (the disclosure rules in China, South Korea and on the app stores, which we do not repeat) and [week 3, premium currencies](w03-premium-currencies.md) (the 2025 EU key principles on in-game currencies).

**Interactive:** [Loot box law map](../examples/w07-loot-box-law-map.html). Keep it open during section 2.

---

## 1. Three kinds of rule

People say "loot boxes are banned in Belgium" or "loot boxes are legal in the UK" as if each country had one switch. They don't. Governments reach paid random rewards through three different bodies of law, and each one asks a different question.

**Gambling law** asks: is this a game of chance played for a stake? If yes, you need a gambling licence, which game publishers do not hold, so in practice the product must go. Gambling laws were written for casinos and lotteries. Each defines gambling with a short list of elements, and a loot box is gambling only where it has all of them. The elements differ from country to country, and that difference is this week's worked example.

**Consumer and child-protection law** asks: is the sale fair, and is it aimed at people who need extra protection? It doesn't care whether the product is gambling. Rules here include odds disclosure (week 6), bans on misleading prices, limits on selling to children, and outright bans for games children are likely to play.

**Age classification** asks: what age rating does the game carry? Ratings are not bans. In most places they are advice to parents, and in some they restrict sale. When a rating body raises the minimum age for games with paid random items, the publisher of a game aimed at 12-year-olds faces a choice between its audience and its store.

Keep the three apart. "The UK decided loot boxes are not gambling" answers only the first question.

### Three terms

- A **paid random reward** is any purchase where money, or a currency bought with money, buys a draw whose result is unknown in advance. Card packs, gacha pulls, crates and cases all count.
- The **stake** (or wager) is what the player puts in. The **prize** is what comes out. Gambling laws differ on whether each must have money's value.
- **Transfer** is whether players can pass items to each other. In-game trading, a platform market paying wallet credit, and outside sites paying cash are three levels of it.

## 2. Worked example: one card pack, two answers

### The hook

In April 2018 the gambling regulators of Belgium and the Netherlands both published studies of loot boxes. They looked at overlapping games, including EA's football series. Belgium's Gaming Commission concluded that the paid packs in FIFA 18 were a game of chance under Belgian law. EA stopped selling FIFA Points for Ultimate Team packs to Belgian players in early 2019.

The Dutch regulator (the Kansspelautoriteit, KSA) also went after EA's packs. On 15 October 2019 it ordered EA to stop selling them in FIFA 19 and later editions, under a penalty of €250,000 per week up to €5 million. A district court agreed with the KSA in October 2020. Then, on 9 March 2022, the Netherlands' highest administrative court, the Council of State, overturned the order. It held that the packs were part of a larger game of skill, not a separate game of chance. EA went on selling them to Dutch players.

Same product, neighbouring countries, opposite outcomes. Nobody got the facts wrong. They applied different tests.

### The model

Describe any paid random reward with five facts. Each is a yes or no, except transfer, which has three levels.

| Symbol | Fact | Values |
|---|---|---|
| `P` | Paid. Real money, or a currency sold for real money, can buy a draw. | yes / no |
| `C` | Chance. The contents are random at the moment of purchase. | yes / no |
| `T` | Transfer. What players can do with what they win. | none / trade / cashout |
| `S` | Skill-embedded. The draw feeds a mode that is mainly a game of skill, and buyers open draws to play that mode. | yes / no |
| `M` | Minors. The game is aimed at, or likely to be played by, under-18s. | yes / no |

Here `trade` means items move between players (inside the game or on a platform market), and `cashout` means items can be turned into money or money's worth, through an official market or one the publisher tolerates.

Each jurisdiction's rule is a test on these facts. As of 28 September 2026:

| Jurisdiction | Legal source | Test | Outcome if the test is met |
|---|---|---|---|
| Belgium | Gaming and Betting Act of 7 May 1999, art. 2(1), as read by the Gaming Commission (April 2018) | `P and C` | Game of chance: needs a licence, so remove it |
| Netherlands | Betting and Gaming Act (Wok), as read by the Council of State (9 March 2022) | `P and C and T ≠ none and not S` | Game of chance: needs a licence |
| United Kingdom | Gambling Act 2005, as read by the Gambling Commission (November 2017) | `P and C and T = cashout` | Licensable gambling |
| United Kingdom | Industry guidance published 18 July 2023 at the government's request | `P and C` | Voluntary: no purchases by under-18s unless a parent enables them; spending controls; odds |
| China | Ministry of Culture notice (in force May 2017) | `P and C` | Publish odds (week 6) |
| South Korea | Amended Game Industry Promotion Act (in force March 2024) | `P and C` | Publish odds, by law (week 6) |
| Brazil | Law 15.211/2025, art. 20 (in force 17 March 2026) | `P and C and M` | Prohibited |
| Australia | Guidelines for the Classification of Computer Games 2023 (from 22 September 2024) | `P and C` | Minimum rating M (not recommended under 15) |
| PEGI countries | PEGI criteria for games submitted from June 2026 | `P and C` | Default rating PEGI 16, in some cases 18 |

Read the Belgian row closely, because it is the strictest. The Gaming Commission's report lists four cumulative elements: a game, a stake, a win or loss, and chance, where chance "may even be a secondary element". On the stake, it says any payment above the basic price of the game counts, including in-game currency that can be bought with money. Currency that can only be earned by playing does not count. On the prize, it says the win can be "of any type", and it gives the example that a skin of purely aesthetic value still counts if players value it. Put together, that leaves `P and C`. Transfer, skill and the audience don't enter.

The Dutch row adds two conditions. The KSA's 2018 study found that 4 of the 10 games it examined broke the law, and the factor it used to separate them was whether prizes could be transferred, because transferable prizes have economic value. The Council of State then added `not S`. Its reasoning, in summary: the FUT mode is a game of skill; most packs are earned by playing matches; players open packs to build a team for those matches; so the packs are a part of a skill game, not a free-standing game of chance.

The UK row is narrower still. Its gambling law requires a prize of "money or money's worth". The Gambling Commission said in 2017 that where loot box items are confined to the game and cannot be cashed out, the product is unlikely to be licensable gambling. That is `T = cashout`. The UK government decided in July 2022 not to change the Gambling Act and asked the industry for voluntary protections instead, which is the second UK row.

In code, the three gambling tests are three lines:

```python
def gambling(paid, chance, transfer, skill_embedded):
    be = paid and chance
    nl = paid and chance and transfer != "none" and not skill_embedded
    uk = paid and chance and transfer == "cashout"
    return be, nl, uk

designs = {
    "A cosmetic crate":      (True,  True,  "none",    False),
    "B sports pack":         (True,  True,  "trade",   True),
    "C case with market":    (True,  True,  "cashout", False),
    "D tradeable crate":     (True,  True,  "trade",   False),
    "E earned chest":        (False, True,  "none",    False),
}
for name, facts in designs.items():
    be, nl, uk = gambling(*facts)
    print(f"{name:20} BE {'yes' if be else 'no ':3}  NL {'yes' if nl else 'no ':3}  UK {'yes' if uk else 'no'}")
```

Running it prints:

```
A cosmetic crate     BE yes  NL no   UK no
B sports pack        BE yes  NL no   UK no
C case with market   BE yes  NL yes  UK yes
D tradeable crate    BE yes  NL yes  UK no
E earned chest       BE no   NL no   UK no
```

### Numbers you can check

Now apply all nine rows of the rule table to the five designs, plus a sixth, F, a direct-purchase shop with no randomness. Assume designs A, B and D are in games rated for teenagers, so `M = yes`, and C is in a game rated 18, so `M = no`.

| Design | P | C | T | S | M | BE | NL | UK law | UK guidance | CN, KR | BR | AU | PEGI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A cosmetic crate | yes | yes | none | no | yes | licence | — | — | applies | odds | banned | M | 16 |
| B sports pack | yes | yes | trade | yes | yes | licence | — | — | applies | odds | banned | M | 16 |
| C case with market | yes | yes | cashout | no | no | licence | licence | licence | applies | odds | — | M | 16 |
| D tradeable crate | yes | yes | trade | no | yes | licence | licence | — | applies | odds | banned | M | 16 |
| E earned chest | no | yes | none | no | yes | — | — | — | — | — | — | — | — |
| F direct shop | yes | no | none | no | yes | — | — | — | — | — | — | — | — |

Count the "must remove" outcomes (licence or banned) for each design across the eight markets: A has 2 (Belgium, Brazil), B has 2 (Belgium, Brazil), C has 3 (Belgium, Netherlands, UK), D has 3 (Belgium, Netherlands, Brazil), E and F have 0.

Three patterns fall out of the table.

1. **`P and C` is the switch that matters most.** It alone triggers six of the rows. Turn off either `P` (E) or `C` (F) and every cell goes blank.
2. **Transfer matters in two places only.** Moving from `none` to `trade` adds the Netherlands (unless the box is skill-embedded). Moving to `cashout` adds the UK. Nothing else in the table reacts to transfer.
3. **The audience matters in one legal place and in all the ratings.** Brazil's ban turns on `M`. The Australian and PEGI rows don't ban anything, but a game with a paid crate is now rated M or PEGI 16 by default, which pushes it away from a teen audience whether or not `M` was your intent.

### Back to the hook

EA's packs are design B: paid, random, tradeable on the in-game transfer market, and embedded in a skill mode. Belgium's test is `P and C`, so B is a game of chance there. The Dutch test in 2019 (the KSA's reading) was `P and C and T ≠ none`, which B also meets. The Council of State's reading added `not S`, and B has `S = yes`. That single fact, a legal judgment about what the packs are for, is the whole difference between the two outcomes.

### The visual

Open `examples/w07-loot-box-law-map.html`. The left panel has the five facts as switches. The right panel colours each of the eight markets by outcome. Start from design A and flip `T` to `trade`, and only the Netherlands changes. Flip it to `cashout`, and only the UK changes. Now flip `P` off. Every market clears at once. The second view, "one global build", lists the fewest switch changes that clear every "must remove" cell, and it almost always says the same thing: remove `P` or `C`, or switch the box off market by market.

### Cross-game recognition

Rewrite each case as the five facts and check the table's prediction against what the publisher did.

**Overwatch (2018 version).** Crates bought with money, random, no trading, not skill-embedded in the Dutch sense. That is design A. Belgium's report named it. Blizzard stopped selling crates to Belgian players, while players could still earn them in play, which turns off `P` for Belgium only.

**Counter-Strike: Global Offensive (2018).** Cases need a paid key, contents are random, and items trade on the Steam Community Market for wallet credit, with outside sites paying cash. That is design C, and the table predicts trouble in both Belgium and the Netherlands. In July 2018 Valve stopped players in both countries from opening cases.

**Guild Wars 2 (after the 2018 report).** The game had no loot boxes for sale, but players could use in-game currency on random item draws, and that currency could be bought with money. Under the Belgian reading of "stake", a currency bought with money is a stake. ArenaNet's fix was to stop Belgian players from buying the premium currency with real money. That breaks `P` at the currency link without touching the draw.

**Nintendo, Fire Emblem Heroes and Animal Crossing: Pocket Camp (after the 2018 report).** Both sold random draws for a purchasable currency. Nintendo withdrew both games from Belgium rather than redesign them. That is the regional switch-off at its extreme: `P and C` stays, and the market goes.

Four publishers, four responses, one table. Each response changes exactly one fact, or removes the market.

### Eyes-open design judgment

- **Design for the strict market or plan the regional build from day one.** A global build that satisfies Belgium has no paid random rewards. A regional build keeps them elsewhere but needs a separate store configuration, testing and support for each switched-off market. Both are legitimate. Deciding late is the expensive option.
- **Trading is a legal decision, not only an economy decision.** Every step up the transfer ladder adds a market that may treat your prizes as having value. A player market (MMO304) and a paid random box in the same game is the combination the Dutch regulator and the UK Gambling Commission both singled out.
- **"Skill-embedded" is a court's judgment, not a feature you can toggle.** The Council of State reached it on the facts of one mode in one game. Treat any argument of the form "our boxes are part of a skill game" as a risk your lawyers must own, not as a design pattern.
- **Non-enforcement is not permission.** Leon Xiao's study of the Belgian iPhone store found that in July 2022, 82 of the 100 highest-grossing games still sold loot boxes. The law had not changed. Enforcement had simply not reached them. A game that relies on that gap is one complaint away from a switch-off.

### Check this example

1. A mobile game sells random pet eggs for gems. Gems can be bought or earned. Pets cannot be traded. The game is rated for all ages and marketed to children. Which markets in the table require removal, and which require something else?
2. The same game adds a player-to-player pet market with no cash-out. Which cells change?
3. A publisher claims its paid packs are fine in Belgium "because the items are only cosmetic". Using the Commission's report, explain why that argument fails.

<details>
<summary>Answers</summary>

1. `P = yes` (gems bought with money are a stake in Belgium), `C = yes`, `T = none`, `S = no`, `M = yes`. Removal is required in Belgium (licence) and Brazil (games likely accessed by minors). China and South Korea require odds, the UK guidance applies, Australia gives at least M, PEGI gives 16 by default. The rating result conflicts directly with a children's audience.
2. Only the Netherlands changes, to "licence", because `T` moves to `trade` and the eggs are not skill-embedded. The UK is unaffected without cash-out.
3. The Commission reads "a win of any type" broadly and says it does not matter if a skin is only aesthetic, provided players attach value to it. The Belgian test has no value-of-prize condition beyond that, so cosmetic prizes still meet it.

</details>

## 3. Beyond gambling law: ratings, children and consumer law

Since 2022 almost no new rule has asked "is it gambling?". The new rules ask who the product is sold to and how.

**Age ratings.** Australia's classification changes, in force from 22 September 2024, set a minimum of M for games with paid loot boxes and R18+ for games with simulated gambling. PEGI, the rating system used across most of Europe, announced on 12 March 2026 that games submitted from June 2026 are rated with new criteria. Paid random items give a default of PEGI 16, and sometimes 18. The same release adds PEGI 12 for time-limited or quantity-limited offers, PEGI 7 for daily reward mechanics and PEGI 12 when a game punishes players for not returning. PEGI notes that Germany's USK made similar changes in 2023 after the German Youth Protection Act was updated. For a studio making a game for 10-to-14-year-olds, these rules act like a ban even though they ban nothing. Week 8 returns to the offer and daily-reward criteria.

**Children.** Brazil's Law 15.211, signed 17 September 2025 and in force from 17 March 2026, is the clearest statutory ban so far. Article 20 prohibits loot boxes in games aimed at children and adolescents or likely to be accessed by them, judged by the game's age rating. Its definition requires payment, so earned chests are outside it. China acts through spending and time rather than through loot box law. Its November 2019 rules capped minors' monthly spending at 200 to 400 yuan by age, and an August 2021 notice from the National Press and Publication Administration limited minors to one hour of online play, from 20:00 to 21:00, on Fridays, weekends and public holidays.

**Consumer law.** The United States has no federal loot box statute. It has acted under general consumer law instead. The Federal Trade Commission's January 2025 settlement with Cognosphere (HoYoverse, Genshin Impact) bans selling loot boxes to under-16s without a parent's consent, requires disclosure of odds and currency exchange rates, and requires an option to pay for loot boxes in real money (week 6 covers the disclosure side). In the European Union, the Consumer Protection Cooperation Network's key principles on in-game currencies (21 March 2025) set out how enforcers read existing consumer law (week 3). The European Commission's Digital Fairness Act, which targets dark patterns and addictive design, finished its public consultation on 24 October 2025. The Commission's planning page lists the proposal for the fourth quarter of 2026. As of 28 September 2026 it has not been published, so nothing in it binds yet.

**Courts.** In March 2023 a district court in Hermagor, Austria, reportedly found FIFA packs to be illegal gambling in a player's refund claim. The ruling is not in Austria's public case database, so treat the details as press reports. It was a first-instance ruling in one case, but it shows a player can win in court where no regulator has acted.

### Where each rule sits

| Question the rule asks | Where | Design fact it reads |
|---|---|---|
| Is it gambling? | Belgium, Netherlands, UK, Austrian courts | `P`, `C`, `T`, `S` |
| Is the sale fair and clear? | EU consumer law, US FTC, odds laws in China and South Korea | how price and odds are shown |
| Who can buy it? | Brazil, China, US FTC order, UK guidance | `M` and age checks |
| What age is the game? | Australia, PEGI, USK | `P and C`, offers, daily rewards |

A compliance review walks all four rows.

## 4. The cost of complying

Your options for a market that says "remove it" are a regional switch-off or a global redesign. The arithmetic is simple, and it is worth doing before an argument starts.

Let `R` be the game's total revenue, `s_m` the share of it from market `m`, and `b_m` the share of that market's revenue that comes from paid random rewards. Switching the box off in market `m` loses at most

```
regional cost = R × s_m × b_m × (1 − k)
```

where `k` is the share of that spending players move to other products (direct purchases, a battle pass) when the box goes away. A global redesign that removes paid randomness everywhere loses

```
global cost = R × b × (1 − k)
```

where `b` is the box share of all revenue.

Take an invented game with `R` = $50 million a year and `b = 30%` everywhere. Belgium is 0.4% of revenue and Brazil 2%, and assume `k = 0.5` in both cases.

| Option | Calculation | Revenue lost per year |
|---|---|---|
| Switch off in Belgium only | 50,000,000 × 0.004 × 0.30 × 0.5 | $30,000 |
| Switch off in Belgium and Brazil | 50,000,000 × 0.024 × 0.30 × 0.5 | $180,000 |
| Remove paid randomness everywhere | 50,000,000 × 0.30 × 0.5 | $7,500,000 |

The regional switch-off is about 40 times cheaper here, which is why most publishers in the cross-game list chose it. The formula leaves out its other costs: a store variant per market, geolocation and payment checks, and support tickets from players who travel or use VPNs. It also leaves you exposed to the next market that tightens, while the global option costs nothing extra when the next law arrives. Choosing between them depends on how many markets you expect to tighten over your game's life. That is a judgment. Put the number next to it.

## In-class activity (25 minutes)

Groups of three. Each group gets one card describing an invented game's monetization (the instructor has six; examples include a gacha RPG rated 12, a trading-card MMO with an auction house, and a shooter with key-and-case drops).

1. (5 min) Encode the paid random reward as `P, C, T, S, M`. Argue `S` both ways and record the disagreement.
2. (8 min) Fill one row of the section 2 table for your game, all eight markets. Check it in the interactive.
3. (7 min) Using the section 4 formulas with the revenue shares on your card, compute the cost of switching off every "must remove" market and of a global redesign.
4. (5 min) Write a three-sentence recommendation to your producer: which option, which markets, and what you would change in the design to reduce exposure next year.

Expected output: the encoded facts, one table row, the two costs, and the recommendation.

## Common misconceptions

- **"Loot boxes are banned in the EU."** There is no EU-wide loot box law as of September 2026. Belgium's ban comes from its own gambling law, and the Digital Fairness Act is still a planned proposal.
- **"If items can't be sold for money, it isn't gambling anywhere."** That is roughly the UK test. Belgium's test ignores the prize's money value entirely, and the Netherlands looks at transferability, not cash-out.
- **"The Dutch court ruled loot boxes are legal."** It ruled that FIFA's packs, as used in that mode, were part of a game of skill. A tradeable box that stands on its own is still a risk under the KSA's test.
- **"A rating is only a label."** A PEGI 16 default for paid random items can remove a game from its intended teen audience, and in Brazil the rating is what decides whether the ban applies.

## Check yourself

1. An MMO sells random mount boxes for premium currency. Mounts are account-bound (`T = none`), the game is rated 12 and has a large teen audience. List the outcome in each of the eight markets.
2. The same MMO lets players sell mounts on the auction house for gold, and gold can be bought from an official token (week 11). Which fact changes, and which markets change outcome? Argue whether the token makes `T = cashout`.
3. Using section 4, a game earns $20 million a year, 40% from boxes, 1.5% from the Netherlands. Its boxes trade freely. With `k = 0.4`, what does a Dutch switch-off cost? What does a global removal cost?
4. A colleague says "Brazil only bans loot boxes for kids, so we'll add an age gate." Using the text of article 20, explain what the law actually keys on and why an age gate may not be enough.

<details>
<summary>Answers</summary>

1. Belgium: licence needed, remove. Netherlands: no gambling (no transfer). UK: not gambling; the voluntary guidance applies. China and South Korea: publish odds. Brazil: banned, since a 12-rated game with a teen audience is likely accessed by minors. Australia: at least M. PEGI (new submissions): default 16.
2. `T` rises to `trade`, so the Netherlands becomes "licence" (the mounts are not skill-embedded). If gold can be bought with money and mounts can be sold for gold, a player can turn money into mounts and mounts back into something bought with money, but not into cash. Most readings keep this at `trade`, so the UK stays unaffected; a regulator could argue gold bought with money is "money's worth", which would make it `cashout`. Flag it as a risk.
3. Dutch switch-off: 20,000,000 × 0.015 × 0.40 × 0.6 = $72,000 a year. Global: 20,000,000 × 0.40 × 0.6 = $4,800,000.
4. Article 20 bans loot boxes in games directed at children and adolescents or likely to be accessed by them, judged by the game's age rating. It is about the game, not the individual buyer, so an age gate on the store does not change whether the game is likely to be accessed by minors. The safe routes are a rating that places the game outside that scope or removing paid randomness in Brazil.

</details>

## Lab / assignment hook

[Lab 07, a loot box rules engine](../labs/lab07.md). You implement the rule table as code, extend it with compliance checks (odds shown, parental gate) and a search for the fewest design changes that clear a chosen set of markets, then write a 400-word compliance memo for one real game. The memo is the second input to the ethics analysis (20%).

## Sources

- Belgian Gaming Commission (Kansspelcommissie), *Research Report on Loot Boxes* (April 2018, English translation of the Dutch original). Section 5: four cumulative elements, bought currency as a stake, "a win of any type". https://www.gamingcommission.be/sites/default/files/2021-08/onderzoeksrapport-loot-boxen-Engels-publicatie.pdf
- Raad van State (Dutch Council of State), ruling of 9 March 2022, case 202005769/1/A3, ECLI:NL:RVS:2022:690. KSA order of 15 October 2019 and its penalty; district court ruling of 15 October 2020; FUT packs part of a skill game. https://data.rechtspraak.nl/uitspraken/content?id=ECLI:NL:RVS:2022:690
- UK Gambling Commission, "Loot boxes within video games" (24 November 2017).
- UK Department for Digital, Culture, Media and Sport, "Government response to the call for evidence on loot boxes in video games" (updated 18 July 2022). DCMS, "Loot boxes in video games: update on improvements to industry-led protections" (18 July 2023), on the Ukie guidance of that date.
- Presidência da República (Brazil), Lei nº 15.211, de 17 de setembro de 2025. Art. 2 definition (payment required), art. 20, art. 41-A in force 17 March 2026 (Lei nº 15.352/2026). https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15211.htm
- PEGI, "PEGI expands age rating criteria with interactive risk categories" (Brussels, 12 March 2026; https://pegi.info/news/pegi-expands-age-rating-criteria-interactive-risk-categories).
- Australian Government, Classification website, "New classifications for gambling-like content in video games" (18 September 2024; Internet Archive copy, accessed 29 September 2026). https://www.classification.gov.au/about-us/media-and-news/news/new-classifications-for-gambling-content-video-games
- European Commission, Have Your Say, initiative 14622 "Digital Fairness Act" (planning API accessed 29 September 2026). Call for evidence and public consultation published 17 July 2025 and closed 24 October 2025; proposal planned for Q4 2026, not yet adopted. https://ec.europa.eu/info/law/better-regulation/have-your-say/initiatives/14622
- US Federal Trade Commission, "Genshin Impact Game Developer Will be Banned from Selling Lootboxes to Teens Under 16 without Parental Consent, Pay a $20 Million Fine to Settle FTC Charges" (17 January 2025; Internet Archive copy of that date). Stipulated order, subject to court approval.
- National Press and Publication Administration (China), notice 国新出发〔2021〕14号 (30 August 2021). https://www.gov.cn/zhengce/zhengceku/2021-09/01/content_5634661.htm The 2021 notice cites the 2019 notice 国新出发〔2019〕34号, whose minors' spending limits of 200-400 yuan per month (effective 1 November 2019) are taken from Xiao, L. Y. (2020), "People's Republic of China Legal Update: The Notice on the Prevention of Online Gaming Addiction in Juveniles", *Gaming Law Review* 24(1), 51-53, as cited by Wikipedia, "Loot box" (accessed 28 September 2026).
- Wikipedia, "Loot box" (accessed 28 September 2026). Publisher responses in Belgium (Blizzard, ArenaNet, Nintendo, EA in January 2019); Valve's July 2018 block on case opening in the Netherlands and Belgium; the KSA's April 2018 study (4 of 10 games); the Hermagor district court ruling of March 2023 (press reports only); South Korea's in-force date of March 2024 (Korea JoongAng Daily, 26 February 2024). These points are secondary.
- Korea Ministry of Government Legislation, National Law Information Center, Game Industry Promotion Act, art. 2(11) definition of probability-type items and art. 33(2) duty to display their types and supply probabilities, added by the amendment of 21 March 2023 (accessed 29 September 2026). https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=265811
- Xiao, L. Y. (2023). "Breaking Ban: Belgium's Ineffective Gambling Law Regulation of Video Game Loot Boxes." *Collabra: Psychology* 9(1), 57641. doi:10.1525/collabra.57641. 82 of the 100 highest-grossing iPhone games in Belgium sold loot boxes in July 2022.
- Fields, T. & Cotton, B. (2011). *Social Game Design: Monetization Methods and Mechanics*. Morgan Kaufmann.

## Interactive spec: examples/w07-loot-box-law-map.html

**Purpose.** Show that each market's loot box rule is a test on a few facts about the box, and that one fact (paid and random together) drives most outcomes. Insight on first load: *design A triggers a rule in seven of eight markets (six from paid and chance alone, plus Brazil because minors are likely; only the Netherlands has none); flipping "paid" off clears all of them at once, while flipping transfer changes only the Netherlands and the UK.*

**Layout.** Two panels side by side on desktop, stacked on mobile (switches first). Left: "Your box", five controls. Right: "Eight markets", a 2 × 4 grid of cards (4 × 2 on mobile). Below both: the "one global build" panel and a numbers table. Generic shapes and text only. No game logos, flags drawn from copyrighted art, or screenshots; country names as text, optional two-letter codes.

**Controls.**
- `P` paid: toggle (default on). `C` chance: toggle (default on). `T` transfer: three-way segmented control none / trade / cashout (default none). `S` skill-embedded: toggle (default off). `M` minors likely: toggle (default on).
- Presets (buttons): A cosmetic crate (on, on, none, off, on), B sports pack (on, on, trade, on, on), C case with market (on, on, cashout, off, off), D tradeable crate (on, on, trade, off, on), E earned chest (off, on, none, off, on), F direct shop (on, off, none, off, on).
- All controls keyboard operable; state changes redraw immediately.

**Market cards.** Each shows the market name, the outcome label, the legal source in one line and the date. Outcome categories and colours (colour plus an icon or text badge, never colour alone): "Must remove" (licence or ban), "Rating floor", "Disclose odds", "Voluntary guidance", "No rule".
- Belgium: must remove if `P and C`.
- Netherlands: must remove if `P and C and T ≠ none and not S`.
- United Kingdom: must remove if `P and C and T = cashout`; else "Voluntary guidance" if `P and C`; else no rule.
- China: disclose odds if `P and C`.
- South Korea: disclose odds if `P and C`.
- Brazil: must remove if `P and C and M`; else no rule.
- Australia: rating floor "M" if `P and C`.
- PEGI: rating floor "16" if `P and C`.
Show a count above the grid: "Must remove in N of 8 markets".

**One global build panel.** Search all single-fact changes and all pairs of changes (P off; C off; T to none, trade or cashout; S toggled; M off) and list the smallest sets that bring "must remove" to 0 across all markets. Also list "regional switch-off" as the alternative, naming the markets. For design A the panel must list "P off" and "C off" as one-change solutions, and "M off" is not sufficient (Belgium stays).

**Numbers table.** Under the panels, replicate the section 2 table row for the current state (P, C, T, S, M, then the eight outcomes) so students can copy it.

**Cost strip (optional second tab).** Inputs `R` (default 50,000,000), `b` (default 0.30), `k` (default 0.5), and a market share for each market (defaults: Belgium 0.004, Brazil 0.02, Netherlands 0.015, others 0). Output regional cost `R × Σ s_m × b × (1 − k)` over "must remove" markets and global cost `R × b × (1 − k)`.

**Test values.**
- Preset A: must remove in 2 of 8 (Belgium, Brazil); UK voluntary; CN and KR disclose; AU M; PEGI 16; NL no rule.
- Preset B: identical outcomes to A.
- Preset C: must remove in 3 of 8 (Belgium, Netherlands, UK); Brazil no rule.
- Preset D: must remove in 3 of 8 (Belgium, Netherlands, Brazil).
- Presets E and F: 0 of 8 and every card "No rule".
- From A, set T = trade: Netherlands becomes must remove (3 of 8). Set T = cashout: Netherlands and UK must remove (4 of 8).
- Cost tab with defaults and preset A: regional cost $180,000 (Belgium and Brazil); global $7,500,000.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Outcome badges carry text. Respect `prefers-reduced-motion` (no card flip animation) and `prefers-color-scheme`. Include a line under the grid: "Status as of 28 September 2026. Rules change; check the lecture's sources."
