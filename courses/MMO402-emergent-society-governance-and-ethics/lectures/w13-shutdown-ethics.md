# MMO402 · Week 13 — Shutdown Ethics

**Why this matters:** Every online world you ship will close one day, and the players inside it will judge you by how it ends. The decisions that decide that judgment are small and concrete: how many weeks of notice, whether sales stop on the day of the announcement, who gets money back, and what happens to the data. This week gives you a way to price those decisions and a vocabulary to defend them.

**You will be able to:**
- Compute the stranded value of a shutdown from purchase history, useful life and notice period.
- Derive the notice period that minimises the combined cost of running the world longer and leaving value stranded, and explain why the first months of notice are the cheapest relief.
- Critique a real shutdown (Concord, Anthem, The Crew, Knockout City, City of Heroes) by naming which terms of the model the operator chose.
- Design a sunset charter that a studio could publish at launch, and argue for each commitment against its cost.

**Before class:** Reread Koster, "Declaring the Rights of Players" (2000), and write down the one clause you think says most about shutdowns. Read the Wikipedia articles "Concord (video game)" and "The Crew (video game)", the sections on the end of service only (about 15 minutes in total). Skim California Assembly Bill 2426 (2024), the short section that defines what a seller must tell a buyer of a digital game (leginfo.legislature.ca.gov).

**Prerequisites from earlier courses:** [MMO301 week 13, worlds that died](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w13-worlds-that-died-shutdowns-and-their-lessons.md) (why worlds close, the density spiral, and the five questions of a sunset plan; this week assumes all of it). [MMO301 week 12, persistence and time](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w12-persistence-and-time-what-should-last.md) (what a world promises to keep). [MMO401 week 11, premium currencies](../../MMO401-virtual-economies-ii-markets-governance-and-macr/lectures/w11-premium-currencies-and-exchange-rates.md) (why a currency balance is a liability on the operator's books). [MA101 week 3, polynomials and quadratic curves](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w03-polynomials-and-quadratic-curves.md) (the total-cost curve is a parabola, and the quadratic formula locates its lowest point). In this course, [week 1, worlds as polities](w01-worlds-as-polities.md) (legitimacy), and [week 5](w05-rules-eulas-and-terms-of-service.md), [week 8](w08-rights-of-avatars-koster-2000.md) and [week 9](w09-virtual-property-and-law.md) on terms of service, the rights of avatars and virtual property.

**Interactive:** [Stranded value and notice](../examples/w13-stranded-value.html). Keep it open during section 2.

---

## 1. What a shutdown takes

MMO301 week 13 asked why worlds die and how to plan the last day. This week asks a narrower question. When you switch a world off, what have you taken from the people inside it, and what do you owe them for it?

Start by listing what is lost. There are four kinds of loss, and they need different remedies.

| Loss | Example | Can money repair it? | Remedy that fits |
|---|---|---|---|
| Purchases | A cosmetic bought last week, a season pass half used, unspent premium currency | Yes, in part | Refunds, notice, stopping sales early |
| Time and progress | A level-80 character, a rare mount, years of crafting reputation | Not really | Notice, exports, an offline or private-server mode |
| Place and community | A guild's hall, the square where a friend group met, a player-run market | No | Notice, a final event, a new home for the community |
| Records | Chat logs, screenshots, forum history, account data | No, and some of it should be deleted | Exports for players, deletion of personal data, curated archives |

Only the first row is easy to count, so it gets most of the public argument. That is fine as a start, because counting it well forces you to face the others. Section 2 builds a model for the first row. Sections 3 and 4 return to the rest.

### Three ways to argue about what is owed

When players say a shutdown was "unfair," they usually mean one of three things. Philosophers give them names, and you will use all three in the week 14 debates.

- **A broken promise.** The operator led players to expect something and did not deliver it. This is a contract-style argument. Its question is what a reasonable buyer was told, in the store, on the box and in the terms of service. Week 5 covered how little most EULAs promise. Law is catching up with the gap. California's AB 2426, signed in September 2024, bars sellers of digital games from using words such as "buy" or "purchase" unless they also tell the buyer, clearly and separately from other terms, that they are getting a licence that can be revoked. That law does not stop a shutdown. It changes what the buyer can be said to have expected.
- **Harm.** Whatever was promised, the shutdown left people worse off, and a decent operator should keep that loss small where it can do so cheaply. This is a consequence-style argument. Its question is how much loss, borne by whom, and at what cost to avoid.
- **Standing.** Players built part of the world. Their characters, their houses and their communities are partly their work, so they have a claim to be consulted and to keep something. This is the rights-style argument Koster raised in 2000, which you met in full in week 8. Its question is who gets a say.

The model in section 2 is a harm model. It prices one kind of loss. Keep in mind which question it answers and which it cannot.

## 2. Worked example: the stranded-value curve

### The hook

Three live-service games closed within two years of each other, and their operators made three different choices.

- **Concord** (Sony, released 23 August 2024). Sony announced on 3 September 2024 that it would take the game offline, and the servers went down on 6 September. Every copy sold was refunded. The game had run for 14 days.
- **Anthem** (EA and BioWare, released 22 February 2019). On 3 July 2025, EA stopped selling the game's premium currency and announced that servers would close on 12 January 2026. Because the game's content lived on the servers, closure made it unplayable. Wikipedia's account of the closure records no refunds.
- **The Crew** (Ubisoft, 2014). The game was removed from stores on 14 December 2023, and servers closed on 31 March 2024. In early April 2024, Ubisoft began removing the game from players' libraries. Players later found code for an unused offline mode.

Concord refunded everything and got little criticism for how it ended. Anthem gave more than six months of notice and, on the record, no refunds. The Crew became the case that started a European Citizens' Initiative. Which operator treated its players best? You cannot answer by feel. You need to count what each player lost and what each remedy cost.

### The model

Think about one purchase. A player pays a price `P` for something that lasts: a skin, an expansion, a season pass. They expect to enjoy it for some **useful life** `L`, measured in months. Treat that enjoyment as spread evenly across the life, the way an accountant writes down a machine. After `a` months the purchase has delivered a share `a / L` of its value and still holds `1 − a / L`.

Now switch the world off. The operator announces the shutdown at time 0, stops real-money sales that day, and closes the servers `N` months later. `N` is the **notice period**. A purchase bought `a` months before the announcement is `a + N` months old when the servers go dark, so the value it loses is

```
stranded value of one purchase = P × max(0, 1 − (a + N) / L)
```

Purchases older than `L − N` have been fully enjoyed by the last day and lose nothing.

Now let players spend steadily at `s` dollars a month before the announcement. Add up the stranded value over every month of purchases. The sum is an area under a straight line, a triangle, and its area is

```
V(N) = s × (L − N)² / (2L)      for 0 ≤ N ≤ L
V(N) = 0                         for N ≥ L
```

- `V` is the total **stranded value**: real money players paid for value they will never receive.
- `s` is the spend rate in the months before the announcement.
- `L` is the useful life a reasonable buyer expected.
- `N` is the notice period in months.

Two more terms finish the picture. Keeping a world running costs the operator `C` per month (servers, a skeleton team, customer support), and after the announcement there are no new sales to pay for it. So notice is not free. The combined cost of a shutdown plan is

```
total(N) = C × N + V(N)
```

The first term is paid by the operator in time. The second is paid by players in lost value, unless the operator refunds it in cash. Either way, somebody pays the sum, and a fair plan makes it small.

For `N` between 0 and `L`, `total(N)` is an upward parabola. Expand it: `total(N) = (s / 2L) × N² − (s − C) × N + sL/2`. From MA101 week 3, the lowest point of `aN² + bN + c` sits halfway between the roots of the quadratic formula, at `N = −b / (2a)`. You can read the same answer month by month. Near notice `N`, one more month relieves about `s × (L − N) / L` of stranded value, the most at `N = 0` and nothing at `N = L`, and it costs `C`. Extend notice while it relieves more than it costs. Either way, the best notice period is

```
N* = L × (1 − C / s)      if C < s,   else N* = 0
```

### Numbers you can check

Take an invented world. Players spent `s = $200,000` a month on durable items, the expected life is `L = 12` months, and running the world costs `C = $100,000` a month. All three figures are made up for teaching. No studio publishes them.

| Notice N (months) | Stranded value V(N) | Share of V(0) left | Running cost C × N | Total |
|---|---|---|---|---|
| 0 | $1,200,000 | 100% | $0 | $1,200,000 |
| 1 | $1,008,333 | 84.0% | $100,000 | $1,108,333 |
| 3 | $675,000 | 56.3% | $300,000 | $975,000 |
| 6 | $300,000 | 25.0% | $600,000 | $900,000 |
| 9 | $75,000 | 6.3% | $900,000 | $975,000 |
| 12 | $0 | 0% | $1,200,000 | $1,200,000 |

Check two rows by hand. At `N = 0`, `V = 200,000 × 144 / 24 = 1,200,000`. At `N = 3`, `V = 200,000 × 81 / 24 = 675,000`. The best notice is `N* = 12 × (1 − 100,000 / 200,000) = 6` months, with a total of $900,000.

Now look at the column of differences. The first month of notice removes $191,667 of stranded value for $100,000 of running cost. The twelfth month removes only $8,333 for the same $100,000. Each month of notice protects every recent purchase at once, and the most recent purchases have the most value left, so early months do the most work.

Compare a cash remedy. An operator that closes with no notice and refunds each purchase its exact unused value pays $1,200,000. An operator that gives six months' notice and then refunds the rest pays $600,000 in running costs plus $300,000 in refunds, $900,000 in all. Players end up equally whole in both plans. The operator saves $300,000 by paying partly in time. That is the insight of this model. **Notice is a refund paid in time, and the first months of it are cheaper than cash.**

### The visual

Open the interactive. The left panel shows every month of purchases as a column. Its height is the share of value that column still holds on the last day. At `N = 0` the columns form a triangle that runs from 100% for last month's purchases down to 0% for purchases a year old. Drag the notice slider and the triangle shrinks from both sides at once, so its area falls with the square of what is left. The right panel plots `V(N)`, `C × N` and their sum against `N`, with the minimum marked. Push `C` up toward `s` and watch the minimum slide to zero notice. Push `L` up and watch every curve stretch to the right.

### Cross-game recognition

Each real shutdown can be rewritten as a choice of `N`, a cash refund, or a change to `L`. Doing that rewriting is the skill this example teaches.

**Concord (2024): a young game, where full refunds equal fair refunds.** The model assumes purchases stretch back at least `L` months. Concord's purchases stretched back two weeks. If a game has been live only `T` months and `T` is shorter than `L`, then with no notice the stranded share of everything ever spent is `1 − T / (2L)`. With `T = 0.5` and `L = 12`, that is 97.9%. So refunding every copy at full price cost Sony only about 2% more than refunding exact unused value, and it was far simpler to explain. For a game live three years with steady spending, the full-refund bill would be `36s` against an unused value of `6s`, six times more. That is why operators of old games almost never refund everything. Generosity is part of it, but the bigger reason is that the two policies have come apart.

**Anthem (2025-2026): notice without cash.** EA gave `N` of about 6.3 months, from 3 July 2025 to 12 January 2026, and stopped premium-currency sales on the first day. With `L = 12`, the stranded share falls to `(1 − 6.3/12)² ≈ 22.6%` of what it would have been with no notice. Most of the recent value was relieved in time. Stopping currency sales at once also matters, because it keeps new money from flowing into balances that would be stranded in full. What the model does not see is the part of the loss that is not purchases. A game whose content lives on the server leaves nothing to play afterwards.

**The Crew (2023-2024): the model breaks because `L` was never agreed.** The Crew was sold as a boxed and downloadable game, not as a season pass. Many buyers expected to keep it indefinitely, which in the model means `L` is very large. As `L` grows, `V(N)` barely falls with notice at all. Three and a half months between delisting and closure could not relieve a purchase the buyer expected to keep for a decade. Removing the game from libraries afterwards turned a harm argument into a broken-promise argument. A class action filed in California in November 2024 claimed that Ubisoft had misrepresented licences as ownership. AB 2426 is the legislature's answer to the same problem. It forces the seller to state the licence at the point of sale, which in model terms forces a shared, honest `L`.

**Knockout City (2023): lowering the loss instead of the time.** Velan Studios announced the end of online service in early 2023 and closed the official servers on 6 June 2023. It also released a PC version that works with privately hosted servers. Add a preserved share `ρ` to the model, the fraction of value that survives the closure, and stranded value becomes `(1 − ρ) × V(N)`. A community server release pushes `ρ` above zero for every purchase at once, including the old ones that notice cannot reach.

**City of Heroes (2012, and 2024).** MMO301 week 13 covered the closure and the licence NCSoft granted to a community host in January 2024. In this model's terms, the world had `ρ = 0` for more than six years and then a large `ρ` arrived through an unlicensed route. A preservation clause written at launch would have given players the same outcome through a cleaner route.

Outside games, the same model runs every "end of life" notice for a product people paid for in advance. Gym memberships, software subscriptions and prepaid transit passes all face it. The operator can pay in time (honour the product until it runs out), in cash (a pro-rata refund), or in preservation (let the product keep working without the operator).

### Eyes-open design judgment

The model helps you see the price of each option. It does not decide for you. Use it with these limits in view.

- **Adding player loss to operator cost is a value judgment.** `total(N)` counts a dollar lost by a player the same as a dollar spent by the studio. You could weight player losses more, because players did not choose the shutdown. Weighting them by `k > 1` moves the best notice to `N* = L × (1 − C / (k × s))`, which is longer. Say which weight you use and why.
- **`L` carries most of the ethics.** Choose a short `L` and almost nothing is ever stranded. Choose a long one and every shutdown is a disaster. The fair `L` is the one players were led to expect, which is why the store copy, the tooltip and the terms of service belong in this discussion. A season pass that says "for 90 days" has an honest `L`. A skin sold "forever" does not.
- **Stranded currency is the easiest loss to prevent.** An unspent balance is stranded in full, whatever the notice. Stop selling currency on the day you announce. Then either refund balances or let players spend them on items during the notice period.
- **Notice has social value that the model does not count.** Six months lets a guild plan a last raid, lets players export screenshots and lets the community find a new home. Those benefits sit in the rows of section 1 that money cannot repair, and they also favour longer notice.
- **Notice can be abused.** A long notice period during which the store keeps selling is worse than a short one. The model assumes sales stop on day 0. If they do not, every new sale is stranded almost in full.

## 3. The losses money cannot repair

Go back to the last three rows of the table in section 1. They have no price, but you still have choices about them.

### Time and progress

A character is a record of hours. Nothing you return makes up for losing it, but you can make the loss less total. The cheapest option is a character export: a static page or a downloadable file with the character's name, appearance, level, gear and achievements. It costs a few days of engineering if you plan it early and weeks if the team that knows the database has already left. MMO301 week 13 showed with WildStar how fast that knowledge leaves.

The expensive option is an offline mode or a server release. The Crew shows that the code for one can exist and still go unused. Releasing server software needs licence clearance for every piece of middleware and every piece of licensed music or art in the build. That work takes months, which is another reason to decide at launch.

### Place and community

A guild that loses its world does not always lose its members. Many move together to another game, and a studio can help: a last in-game gathering, a public list of guilds and how to contact them, a forum that stays open for a while. Tabula Rasa and Star Wars Galaxies both ran final events. MMO301 week 13 argued that such events change how players remember the end. Here the ethical point is different. A final event is also a funeral. People need a shared moment to mark a loss, and a world that ends with a login error gives them none.

### Records and privacy

Shutdown creates a clash between two duties. Players and historians want the world preserved: chat logs, forum threads, player-built cities. Data protection law points the other way. Under the EU's General Data Protection Regulation (2016), personal data may be kept only as long as the purpose it was collected for requires. When the world closes, that purpose ends for most of it. Chat logs are personal data, and many of them contain things people said on the understanding that the conversation would not outlive the game.

The honest answer has three parts. Give each player their own data to keep (their characters, their mail, their screenshots). Delete personal data the operator no longer needs. Preserve the world itself (code, maps, item tables, public lore) in an archive, with player names removed unless players opt in. Week 12's research ethics apply to anyone who wants to study the archive later.

## 4. A sunset charter

MMO301 week 13 ended with a sunset plan, a private document that answers five questions. A **sunset charter** is the public half of that plan. It is a short list of commitments a studio publishes at launch, so players know before they spend what will happen at the end. It connects directly to the legitimacy checklist from week 1: predictable rules, fair process and a voice that sometimes works. A charter makes the rules predictable before anyone needs them.

Here is a draft, with what each line costs and what it buys.

| Commitment | What it costs the operator | Model term it moves |
|---|---|---|
| At least 90 days' notice before servers close | About three months of running cost at the end of life | `N ≥ 3` |
| Real-money sales stop on the day of the announcement | Lost revenue in the final months | Keeps `V` from growing after day 0 |
| Unspent premium currency refunded or converted | The currency liability, which is already on the books | Removes the balance term |
| Purchases in the last 30 days refunded in full | A small, predictable refund bill | Removes the cohorts with most value left |
| Character export page available for a year after closure | A few days of engineering, if built early | Keeps some of the value of time and progress |
| Server software or a community licence considered, with the decision published at announcement | Legal and middleware review | Raises `ρ` |
| Personal data deleted within a stated period; world data archived without names | Archive storage, legal review | Resolves the records row |

A studio does not have to promise all of this. It should decide which lines it will promise and publish them. The Stop Killing Games movement's European Citizens' Initiative, registered as "Stop Destroying Videogames," collected signatures from July 2024 to July 2025 and submitted 1,294,188 verified ones. On 16 June 2026 the European Commission replied that it would not create a legal duty to keep games playable. It would instead work with the industry toward voluntary standards and a code of conduct. A published charter is exactly what a voluntary code of conduct would contain. Studios that write one now will be ahead of any standard that follows.

### Who decides, and who is consulted

A shutdown is a governance act. In the terms of week 1, it is the moment the sovereign uses its most absolute power. The legitimacy of that act depends on process as much as on outcome. Three process questions matter.

- **Who is told first?** Staff, partners, players and press will all hear. Players hearing it from a news story before an official post is a failure of process, whatever the charter says.
- **Is there any room for voice?** Players sometimes offer to fund, host or buy a world. The operator is rarely obliged to agree, but publishing the reason for saying no costs little.
- **Who guards the commitments after the team is gone?** A charter that nobody is left to honour is worth nothing. Put the export page and data deletion in the budget of the publisher, not the studio that is closing.

## In-class activity (25 minutes)

Groups of four. Each group plays the shutdown council of an invented world, "Harrowmere," a five-year-old MMO whose publisher has decided to close it. Each member takes one role: producer (owns the budget), community lead (speaks for players), legal counsel (owns the terms of service and data duties), and lead engineer (knows what can be built in time).

Materials: the interactive, plus these invented numbers. Spend on durable items over the last year averaged $80,000 a month with an expected life of 12 months. Running the world costs $60,000 a month. Players hold $250,000 in unspent premium currency. The server build uses licensed physics middleware whose licence forbids redistribution.

1. (8 min) Use the model to find `N*` and the stranded value at `N*`. Then decide the currency policy.
2. (10 min) Draft a five-line shutdown announcement that names the date, the sales stop, the refund policy, what players can keep, and what happens to their data.
3. (7 min) Each role names one line of the plan it would fight against and why. Resolve at least one disagreement by changing a number.

Expected output: `N*` with your working, the announcement, and one recorded disagreement with how you resolved it. (Check: `N* = 12 × (1 − 60/80) = 3` months, with `V(3) = 80,000 × 81 / 24 = $270,000`.)

## Common misconceptions

- **"A full refund is always the most ethical option."** For a young game it is close to exact. For an old one it pays out six times the unused value or more, and the money has to come from somewhere, often from the budget that would have paid for notice, exports or a server release. Fairness means returning what was lost. A full refund can return more than that.
- **"Long notice fixes everything."** Notice relieves only purchases younger than `L`. It does nothing for unspent currency, very little for things buyers expected to keep forever, and harm grows if the store stays open during the notice period.
- **"The terms of service say we can shut down at any time, so there is nothing to discuss."** The terms settle the legal question in most places. They do not settle the harm question or the standing question, and courts and legislatures are narrowing the legal one too.
- **"Preservation and privacy are the same goal."** They pull apart at chat logs. Preserve the world. Return personal data to its owners, and delete what nobody needs.

## Check yourself

1. A world had spend `s = $300,000` a month, `L = 9` months and running cost `C = $150,000` a month. Compute `N*`, `V(N*)` and the total cost at `N*`. Compare with closing at `N = 0` and refunding exact unused value.
2. A game has been live for `T = 2` months with `L = 12`. What share of everything ever spent is stranded if it closes with no notice? How much more than exact unused value does a full refund of everything cost, in percent?
3. With the numbers of section 2 (`s = $200,000`, `L = 12`, `C = $100,000`), a studio decides to count each player dollar lost as worth 1.5 operator dollars. What is the new `N*`?
4. A studio gives 12 months' notice but keeps selling cosmetics until the last month. Explain with the model why this may leave players worse off than 3 months' notice with sales stopped on day 0.
5. Which of the three arguments from section 1 (promise, harm, standing) best describes the complaint against The Crew's licence removal? Name a change that would answer that argument without extending notice.

<details>
<summary>Answers</summary>

1. `N* = 9 × (1 − 150/300) = 4.5` months. `V(4.5) = 300,000 × 4.5² / 18 = 300,000 × 20.25 / 18 = $337,500`. Running cost `150,000 × 4.5 = $675,000`, total $1,012,500. At `N = 0`, `V = 300,000 × 81 / 18 = $1,350,000`, all paid as refunds. The notice plan is $337,500 cheaper for the same player outcome.
2. Stranded share `1 − T/(2L) = 1 − 2/24 = 0.917`, so 91.7%. A full refund pays 100% of spend, so it costs `1 / 0.917 − 1 ≈ 9.1%` more than exact unused value.
3. `N* = L × (1 − C / (k × s)) = 12 × (1 − 100,000 / 300,000) = 8` months.
4. Every sale during the notice period is bought with little time left to enjoy it. A purchase made one month before closure with `L = 12` loses 11/12 of its value. Eleven months of such sales can strand more new value than the extra notice relieves. With 3 months' notice and sales stopped on day 0, `V(3)` is 56.3% of `V(0)` and nothing new is added.
5. Mainly a broken promise. Buyers thought they owned a game, and removal from their libraries contradicted that belief. Answers without more notice: tell buyers at the point of sale that they are getting a revocable licence (as AB 2426 now requires in California), leave installed copies in libraries, or release an offline patch or server software so that `ρ > 0`.

</details>

## Lab / assignment hook

[Lab 13, shutdown policy memo](../labs/lab13.md). You run the stranded-value model on a purchase history with three item types, implement the best-notice search and a refund-window policy, and write a 700-word shutdown announcement and policy memo defending your numbers. The memo counts toward the case analyses (30%). The best memos become source material for the week 14 debate on shutdown obligations.

## Sources

- Wikipedia, "Concord (video game)" (accessed September 2026). Release 23 August 2024; announcement 3 September 2024 that the game would go offline with all copies refunded; servers offline 6 September 2024; Firewalk Studios closed 29 October 2024.
- Wikipedia, "Anthem (video game)" (accessed September 2026). Release 22 February 2019; premium-currency sales stopped and shutdown announced 3 July 2025; servers closed 12 January 2026; content on the servers, so unplayable after closure. The article records no refunds.
- Wikipedia, "The Crew (video game)" (accessed September 2026). Delisted 14 December 2023; servers closed 31 March 2024, citing server infrastructure and licensing constraints; removal from player libraries in early April 2024; unused offline-mode code; California class action filed 4 November 2024; fan server emulator released September 2025.
- Wikipedia, "Knockout City" (accessed September 2026). End of service announced early 2023; official servers closed 6 June 2023; PC version for privately hosted servers released.
- California Legislative Information, Assembly Bill 2426 (2023-2024 session), chaptered 24 September 2024. Disclosure required before "buy" or "purchase" can be used for digital goods; games included in the definition.
- European Citizens' Initiative register, ECI(2024)000007 "Stop Destroying Videogames" (register.eci.ec.europa.eu, accessed September 2026). Collection 31 July 2024 to 31 July 2025; 1,294,188 verified signatures; status "answered", 16 June 2026. Wikipedia, "Stop Killing Games" (accessed September 2026), for the content of the Commission's reply: no legal obligation to keep games playable; voluntary standards and a code of conduct instead. Also cited in MMO301 week 13.
- Regulation (EU) 2016/679 (General Data Protection Regulation), Article 5(1)(e), the storage-limitation principle.
- Koster, R. (2000). "Declaring the Rights of Players." raphkoster.com.
- The stranded-value model, all spend and cost figures, and the Harrowmere scenario are invented for teaching and describe no real game.

## Interactive spec: examples/w13-stranded-value.html

**The one insight.** Notice is a refund paid in time. Stranded value falls with the square of the remaining life, so the first months of notice relieve far more value than the last ones, and the cheapest fair plan mixes some notice with a smaller cash refund.

**Layout.** Two linked panels side by side at 1280px, stacked at 390px (left first). Controls above both. A readout strip below.

**Controls (sliders with numeric inputs, keyboard operable).**
- Spend rate `s`: $0 to $500,000 per month, step 10,000, default 200,000.
- Useful life `L`: 1 to 60 months, step 1, default 12.
- Running cost `C`: $0 to $500,000 per month, step 10,000, default 100,000.
- Notice `N`: 0 to 24 months, step 0.1, default 0.
- Months live `T`: 0.5 to 60, step 0.5, default 60 (purchases exist only for ages below `T`).
- Player-loss weight `k`: 1 to 3, step 0.1, default 1.
- Preserved share `ρ`: 0 to 1, step 0.05, default 0.
- Preset buttons: "Section 2 world" (defaults), "Concord-like" (`T = 0.5`, `N = 0`), "Anthem-like" (`N = 6.3`), "Community server" (`ρ = 0.5`). Presets set only the named values and keep the rest.

**Formulas.**
- Let `m = min(T, max(0, L − N))`.
- `V(N) = (1 − ρ) × s × (m × (1 − N / L) − m² / (2L))`. For `T ≥ L − N` this reduces to `(1 − ρ) × s × (L − N)² / (2L)`.
- Total spent in the last `min(T, L)` months: `s × min(T, L)`.
- `total(N) = C × N + k × V(N)`.
- `N*`: minimise `total` numerically over `N` in [0, 24] in steps of 0.01. With `T ≥ L` and `ρ = 0`, check against `N* = L × (1 − C / (k × s))` clamped to [0, L].

**Left panel, the cohort triangle.** Horizontal axis is age of purchase at announcement, 0 to `min(T, 24)` months, in 0.5-month columns. Each column's height is `max(0, 1 − (a + N) / L) × (1 − ρ)`, where `a` is the column midpoint. Columns with zero height are drawn as a thin outline. Label the shaded area "stranded value" with its dollar amount. As `N` grows the shaded region must visibly shrink from the left edge's height and from the right edge's reach at the same time.

**Right panel, the cost curves.** Horizontal axis `N` from 0 to 24. Plot `k × V(N)` (solid), `C × N` (dashed), `total(N)` (thick). Mark `N*` with a dot and label, and the current `N` with a vertical line. Shade the region where one more month of notice relieves more than it costs (`N < N*`).

**Readout.** `V(0)`, `V(N)`, share left `V(N)/V(0)`, `C × N`, `total(N)`, `N*`, `total(N*)`, and "first month of notice relieves $X, last month before `L` relieves $Y", where X is `V(0) − V(1)` and Y is `V(L−1) − V(L)` (both with current `ρ`, and using `T`).

**Test values (the builder must check these).**
- Defaults: `V(0) = 1,200,000`; `V(1) = 1,008,333`; `V(3) = 675,000`; `V(6) = 300,000`; `V(9) = 75,000`; `V(12) = 0`. `N* = 6`, `total(N*) = 900,000`. First month relieves 191,667; last month relieves 8,333.
- `C = 50,000`: `N* = 9`, `total = 525,000`.
- `C = 250,000` (greater than `s`): `N* = 0`, `total = 1,200,000`.
- `k = 1.5`: `N* = 8`.
- Concord-like, `T = 0.5`, `N = 0`: `V = 200,000 × 0.48958 = 97,917`; total spent in window 100,000; stranded share 97.9%.
- Anthem-like, `N = 6.3`: `V(N)/V(0) = 0.2256`.
- `ρ = 0.5`, `N = 0`: `V = 600,000`.
- Harrowmere (`s = 80,000`, `C = 60,000`): `N* = 3`, `V(3) = 270,000`.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. The three right-panel curves differ in dash pattern and have direct labels, so they read without colour. Respect reduced motion. State on screen that all numbers are invented. No game names in the drawing, no logos or art.
