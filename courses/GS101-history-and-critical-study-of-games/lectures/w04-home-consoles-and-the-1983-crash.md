# GS101 · Week 04 — Home Consoles and the 1983 Crash

**Why this matters:** Between 1982 and 1985, sales of home video games in the United States fell from about $3 billion to about $100 million. Players had not stopped liking games. The industry drowned in its own unsold stock. Every platform you will ever ship on, from a console store to Steam to an MMO auction house, is a shelf with a supply and a demand, and this week shows what happens when nobody controls what goes onto it.

**You will be able to:**
- Explain the chain of causes of the North American crash (market saturation, third-party flooding, home computer competition, retail markdowns) and rank them with evidence.
- Compute a retailer's unsold stock and revenue year by year with a simple shelf model, and show how revenue can fall while demand in units holds steady.
- Compare Nintendo's licensing controls with Steam's open storefront as two answers to the same supply problem, and state what each gives up.
- Critique a popular history claim (the "millions of E.T. cartridges in a landfill" story) by checking it against primary and secondary sources.

**Before class:** Donovan, *Replay: The History of Video Games* (2010), the pages covering the Atari VCS, Activision and the crash. The course reader lists the pages. Skim the Wikipedia article "Video game crash of 1983" and follow at least two of its citations to their original source.

**Prerequisites from earlier courses:** None. GS101 has no prerequisites. This week follows [GS101 week 3, the arcade era and the coin-op business model](w03-arcade-era-and-the-coin-op-business-model.md), because the 2600's best-selling cartridges were arcade conversions. If you are also taking GD101, the causal chain here uses the same "rule, then behavior, then feeling" reading as [GD101 week 4, MDA](../../GD101-introduction-to-game-design/lectures/w04-mda-mechanics-dynamics-aesthetics.md). The shelf model in section 2 is a stock-and-flow model; you will study those properly in [GD102 week 2, stocks and flows](../../GD102-systems-design-and-game-mechanics/lectures/w02-stocks-and-flows.md).

**Interactive:** [The crash shelf model](../examples/w04-crash-shelf-model.html). Use it during section 2.

---

## 1. From one console to a crowded shelf

### The cartridge changes the business

The first home consoles played games built into the hardware. When you bought a Pong clone, you bought one game, forever. The cartridge changed that. A cartridge is a plastic case holding a ROM chip with one game's code. Plug in a different cartridge and the same machine plays a different game.

That one piece of hardware turned the console into a platform. A platform is a product whose value comes mostly from things other people make for it. The console maker now earned money twice, once on the machine and again on every game a household bought for years afterward. The machine could be sold cheaply because the games paid for it later. You will meet this "razor and blades" pattern again in [week 11](w11-free-to-play-mobile-and-live-service.md) when we study free-to-play.

The Atari VCS, launched in 1977 and renamed the Atari 2600 in late 1982, was not the first cartridge console. The Fairchild Channel F came first. But by 1980 the VCS was the most popular console of its generation by a wide margin. Its killer application arrived that year. Atari licensed Taito's arcade hit Space Invaders, sales of the console quadrupled, and the cartridge became the first title to sell more than a million copies.

Notice the dependency. The home console grew by selling the arcade experience you studied in week 3 at home, for a one-time price. That link is why arcade licenses, like Pac-Man in March 1982, were the biggest bets of the era.

### The first third-party publisher

Until 1979, only console makers published games for their consoles. Atari made the VCS and Atari made the games. Programmers were not credited on the box.

In 1979, four Atari programmers left and founded Activision. Their stated reason was recognition. They wanted royalties and public credit, the way musicians and film directors had them. Activision was the first third-party publisher, a company that makes games for someone else's hardware without the hardware maker's permission or cut. Atari sued and lost. The legal door was now open, and anyone who could build a cartridge could sell one.

Activision's games were good and sold well. That success is exactly what brought the flood. David Crane, one of Activision's founders, recalled that the number of third-party developers at the Consumer Electronics Show jumped from 3 to 30 between two consecutive shows. At the Summer 1982 show, 17 companies announced a combined 90 new Atari games. Companies with no game experience at all, including a film studio and food brands, entered the market.

### The shelf fills up

Here is the single most useful number in this lecture. In June 1982 there were about 100 Atari games on the market. By December 1982 there were over 400.

A store has a fixed amount of shelf space. Four times as many games, over six months, competing for the same shelf and the same holiday money. Meanwhile Atari's own share of the cartridge market fell from 75% in 1981 to under 40% in 1982. Competing consoles arrived too, including Mattel's Intellivision and Coleco's ColecoVision, each with its own library.

In 1983 a Goldman Sachs analyst put the imbalance in two numbers. Demand for video games was up 100% on the previous year. Manufacturing output was up 175%. Both grew. Supply grew faster. Keep those two numbers in mind, because section 2 turns them into a model.

### Then the stock came back

In December 1982, Atari announced it had missed its holiday sales target, and video game stocks dropped. Stores tried to send their unsold games back to publishers for refunds. But many new publishers had no cash and no new products. Several, including Games by Apollo and U.S. Games, simply folded. Unable to return the games, stores marked them down and dumped them into discount bins. Games that had launched at $35 sat in bins at $5.

That markdown did more damage than the unsold games themselves. A $5 game in a bin competes with a $35 game on the shelf for the same player's money. The bargain bins drew sales away even from the good third-party publishers. By mid-1983 Atari had lost $356 million and laid off 30% of its 10,000 employees. By the end of the year its losses were over $536 million.

At the same time, a price war between Commodore and Texas Instruments pushed home computers down to console prices. Commodore cut the Commodore 64 to $300 in June 1983, and some stores sold it for $199. A computer played games and did homework and accounts. A magazine founder later summed up the shopper's question. Why buy a machine that only plays games? Mattel cancelled the Intellivision III that year, and a Boston paper asked the same question about a $200 games-only machine.

The full effect landed in 1985. Home video game sales in the United States had fallen from about $3 billion at the 1982 peak to about $100 million in 1985, a drop of roughly 97%. (Some summaries give the peak as $3.2 billion and date it to 1983. The cited book sources put the peak in 1982, before the crash began, which is the reading this lecture uses.) Many retailers stopped carrying video games entirely.

## 2. Worked example: the 1983 crash in numbers

### The hook

Two facts from the same winter do not seem to fit together. Demand for video games was growing fast, up 100% in a year by one analyst's count. Yet new games that had cost $35 a few months earlier were selling for $5, and the market leader was losing hundreds of millions of dollars.

How does an industry whose customers want more of its product lose most of its revenue? The answer is not that players got bored. It is what the unsold stock did to the price.

### The model

Treat the whole North American retail shelf as one pile of cartridges. Each year, four things happen:

```
D  = demand: cartridges players want to buy this year (units)
S  = shipments: new cartridges publishers send to stores this year (units)
U  = unsold stock left over from earlier years, now in the bargain bin (units)
c  = bargain share: the most of this year's demand the bin can capture (0 to 1)

bin_sold  = min(U, c × D)                  players buy cheap old stock first, up to c × D
new_sold  = min(S, D − bin_sold)           the rest of demand buys new games at full price
U_next    = U − bin_sold + (S − new_sold)  unsold new games join the bin next year
revenue   = P × new_sold + b × bin_sold    P = full price, b = bin price
```

- `D` and `S` are counts of cartridges, in any unit you like. We will use "thousand cartridges" and start both at 100. Because the units are thousands, every revenue figure in this section is in thousands of dollars: $7,000 means $7,000 thousand, or $7 million.
- `U` is a stock, a quantity that piles up. `S` and the two "sold" terms are flows, quantities per year that fill or drain it.
- `c` says how much bargains cannibalize full-price sales. Cannibalize means one product's sales eat another's. At `c = 0`, players ignore the bin. At `c = 1`, every player checks the bin first and only pays full price if the bin is empty.
- `P = $35` and `b = $5`, the launch and bin prices reported for the period.

This model is deliberately crude. It has one shelf, one price for new games and one for old ones, and players who treat games as interchangeable. Its job is to isolate one mechanism, not to reproduce 1983 to the dollar. The two growth rates come from the analyst's statement. The prices come from reports of the period. Everything else is invented, so do not quote this table as historical data.

### Numbers you can check

Start in balance. In year 1, demand and shipments are both 100. In year 2, demand grows 100% to 200 and shipments grow 175% to 275, the analyst's two numbers. From year 3 on, demand stays flat at 200, which means the market has saturated. Publishers keep shipping 275 because their production plans were made in the boom. Use `c = 0.5`.

| Year | Demand D | Shipped S | New sold | Bin sold | Unsold stock U after | Revenue ($ thousands) |
|---|---|---|---|---|---|---|
| 1 | 100 | 100 | 100 | 0 | 0 | $3,500 |
| 2 | 200 | 275 | 200 | 0 | 75 | $7,000 |
| 3 | 200 | 275 | 125 | 75 | 150 | $4,750 |
| 4 | 200 | 275 | 100 | 100 | 225 | $4,000 |
| 5 | 200 | 275 | 100 | 100 | 300 | $4,000 |

Check year 3 by hand. The bin holds 75. Players would buy up to `0.5 × 200 = 100` from it, so all 75 thousand go, at $5 each, for $375 thousand. That leaves `200 − 75 = 125` thousand units of demand for new games, at $35 each, for $4,375 thousand. Revenue is $4,750 thousand. Of the 275 new games shipped, 150 did not sell, and they are next year's bin.

Three things stand out.

1. **Revenue fell 43% from year 2 to year 4 while demand in units never fell.** Players bought 200 cartridges every year. They just paid less for many of them.
2. **The bin keeps growing.** By year 5, 300 thousand unsold cartridges sit in stock, more than a full year of demand. In real life that pile goes back to warehouses, and in September 1983 part of Atari's went into a landfill near Alamogordo, New Mexico.
3. **The damage comes from the gap between the growth rates, not from either one.** Set supply growth equal to demand growth (both +100%) and the table shows 200 shipped, 200 sold at full price, zero bin and $7,000 every year from year 2.

Now raise the bargain share to `c = 1`, meaning every player looks in the bin first:

| Year | New sold | Bin sold | Unsold stock U after | Revenue ($ thousands) |
|---|---|---|---|---|
| 3 | 125 | 75 | 150 | $4,750 |
| 4 | 50 | 150 | 225 | $2,500 |
| 5 | 0 | 200 | 300 | $1,000 |

Revenue falls 86% from its peak with demand still flat at 200 units. Add the demand shock of a cheap home computer (demand halves in year 4) and the default model drops to $2,000 a year, with 500 thousand unsold cartridges by year 5.

The real crash was about 97%. Our model gets most of the way there with two ingredients, oversupply and cannibalizing markdowns, and the rest comes from demand actually falling. That is a claim you can argue in an essay. The crash started on the supply side and was finished by the demand side.

### The visual

Open the interactive. The left chart, "What the sales report shows," plots revenue per year as bars. The right chart, "What is on the shelf," plots demand as a line and the unsold stock as a filling area. At the defaults the left chart shows a peak and a slump, and the right shows demand holding flat while the pile grows under it.

Drag the supply-growth slider down from 175% to 100%. The pile disappears and the revenue slump with it. Now switch on "Licensing gate," which caps shipments at this year's demand. Watch what happens to the pile even at 175% planned growth. That toggle is the Nintendo answer in section 3.

### Cross-game recognition

The shelf model is not about cartridges. It describes any place where many sellers put copies of things in front of a limited number of buyers, and old stock can be sold cheaply. Rewrite each case in the same form. What is `S`, what is `D`, what is the bin, and who controls `S`?

**Nintendo Entertainment System (North America, from October 1985).** Nintendo's response was to control `S` directly. Because Nintendo manufactured every cartridge, it could set the terms. Third-party developers had to develop exclusively for the system, order at least 10,000 cartridges at a time, and make at most five games per year. A lockout chip, the 10NES, stopped unlicensed cartridges from running, and a "Seal of Quality" marked approved games. In 1986 Nintendo's president Hiroshi Yamauchi said, in paraphrase, that Atari had given third parties too much freedom and let the market fill with poor games. In the model, this is the licensing gate: `S` cannot run far ahead of `D` because one company approves every unit.

**Steam (from Greenlight in 2012 to Steam Direct in June 2017).** Valve went the other way. Steam Greenlight let players vote games onto the store. When Valve closed it, it mass-approved most of the roughly 3,400 games still waiting and replaced the vote with Steam Direct, a $100 fee per game that is refunded once the game earns $1,000. Valve itself acknowledged that an uncontrolled store leads to discovery problems and low-quality games. In the model, `S` is almost ungated. There is no physical bin, because digital copies cost nothing to store. The "bin" on Steam is attention. A game that nobody sees is unsold stock, and deep discount sales play the role of the $5 bin.

**An MMO auction house.** Swap cartridges for a crafted item. `S` is how many copies players craft or loot each day. `D` is how many players want one. `U` is the pile of listings. If the drop rate or the crafting output grows faster than the player base, listings pile up and sellers undercut each other until the price reaches the floor, the amount a vendor NPC pays. That floor is the $5 bin. MMO304 builds this model in detail in [week 3, faucets, sinks and transformations](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w03-faucets-sinks-and-transformations.md).

Three settings, one shape. When supply outruns demand and the surplus can be sold cheaply, the surplus sets the price for everything.

### Design judgment, eyes open

Gatekeeping `S` worked for Nintendo. It also had costs you should name before copying it.

- **What the gate buys.** Stable prices, retailer trust and a quality floor. Retailers who had been burned by 1983 needed a reason to stock games again. Nintendo even sold the NES as an "entertainment system" with a toy robot accessory to get past buyers who refused to carry video games.
- **What the gate costs.** Every rule that controls `S` also controls who may create. The five-games-a-year limit protected shelves and also protected Nintendo's power over publishers. An open store like Steam lets a two-person studio ship without permission, which is where much of the indie movement you will study in [week 12](w12-indie-games-and-the-auteur-designer.md) came from. The price is a discovery problem that every indie developer feels.
- **What a designer controls.** In an MMO you own `S` completely, because you set every drop rate. The 1983 lesson for world designers is to watch the ratio of supply growth to demand growth, not either number alone, and to decide deliberately what the "bin" is. A vendor floor, a sink that destroys surplus items, or no floor at all are three different economies.

Do not take away the lesson that gates are good and open markets are bad. Take away that someone always decides how fast `S` can grow, and that the decision has winners and losers.

## 3. Reading the crash critically

A history course is also a course in how to doubt a good story. The crash comes wrapped in some of the best stories in game history, and several are wrong or misleading.

### The E.T. story, checked

The popular version goes like this. Atari rushed an E.T. game, it was so bad that nobody bought it, and Atari buried millions of copies in the desert. Each part of that sentence needs checking.

- **The rush is real.** Atari's rights negotiations ended in late July 1982. That left the programmer, Howard Scott Warshaw, just over five weeks to make the game for a December 1982 release. Atari paid a reported $20 to 25 million for the license.
- **"Nobody bought it" is wrong.** The game sold over 2.6 million copies by the end of 1982 and was in the top four of Billboard's video game chart in December 1982 and January 1983. At least 669,000 copies were then returned in 1983, according to Atari's internal cartridge sales records. That leaves about 1.9 million copies kept by buyers. Atari's chief executive Ray Kassar, quoted in Connie Bruck's 1994 biography of Steve Ross, gave a far bleaker figure: about 3.5 million of 4 million produced came back as unsold stock or returns, which leaves about 0.5 million kept. The two sources disagree by about 1.4 million copies. The first is a company sales record, the second an executive's recollection a decade later. Neither settles the question, so when you use either number, name its source and mention the other.
- **"Millions buried" is wrong.** In September 1983, a local newspaper reported ten to twenty semi-trailer loads of Atari boxes, cartridges and systems crushed and buried at the Alamogordo landfill. When the site was excavated on April 26, 2014, a former Atari manager told the Associated Press that about 728,000 cartridges of many different games had been buried. The dig recovered only about 1,300 cartridges, from 59 different games, E.T. among them.

The honest version is less dramatic and more useful. E.T. was a costly license with an impossible schedule. It sold well at first, then came back in huge numbers. Atari dumped excess stock of many games, not only E.T. The game is a symbol of the crash, not its cause.

### Whose crash?

The phrase "the video game crash" hides a geography. The collapse hit hardest in the United States. Sales stayed strong in Japan, Europe and Canada. On July 15, 1983, in the middle of the American collapse, Nintendo released the Family Computer (Famicom) and Sega released the SG-1000 in Japan. By 1986, 6.5 million Japanese homes owned a Famicom. In Europe, home computers were surging.

So when a source says "the industry crashed in 1983," ask which industry. The US console market crashed. Worldwide, the estimated market for arcade, console and computer games fell from about $42 billion in 1982 to about $14 billion by 1985, which is serious but a very different number from 97%. Part of the "crash" was a shift of players and money from consoles to computers, not a disappearance.

### Why the causes matter for how you write

When you write your timeline project, each event needs a cause. The crash tempts you to pick one, such as bad games, greed or E.T. Resist. The evidence supports a chain:

1. A platform opened to anyone (Activision wins in court).
2. Supply grew faster than demand (100 games to 400 in six months; output +175% against demand +100%).
3. Returns failed because new publishers had no money, so stores marked down.
4. Markdowns cannibalized full-price sales, including good games.
5. Cheap home computers took demand at the same moment.
6. Retailers dropped the category, and demand could not recover until someone rebuilt their trust.

Each step is necessary for the next to matter. That is the shape of a good historical explanation. It names a mechanism and shows the evidence for each link.

## In-class activity (25 minutes)

Work in groups of three. You are a retail buyer for a department store chain in January 1983.

1. (10 min) Use the interactive with `c = 0.5`, planned supply growth of 175% and demand growth of 100%. Record years 3 to 5. Then switch on the licensing gate and find the loosest headroom (shipments capped at `headroom × D`) that still keeps unsold stock under half a year of demand (`U < 0.5 × D`) through year 5. Write down the value and the year-5 revenue. You should find it lands near 1.12, and that even this small overshoot costs revenue every year.
2. (10 min) Each group receives one of three claims: "E.T. caused the crash," "Home computers caused the crash," or "Activision caused the crash." Using only the facts in section 1 and section 3, write the strongest one-paragraph case for your claim, then the strongest one-sentence objection.
3. (5 min) Share. The class votes on which link in the six-step chain in section 3 was the one Nintendo's rules most directly fixed.

Expected output: the gate value from step 1, your paragraph and objection, and the class's answer with one reason.

## Common misconceptions

- **"Players stopped wanting games."** Demand was still growing when the trouble started. The first failure was supply outrunning demand, and falling prices, not falling interest. Demand fell later, pulled by home computers and by retailers dropping the category.
- **"E.T. was a flop that nobody bought."** It sold over 2.6 million copies in 1982. Its problem was the cost of the license and the returns that followed. Use the numbers, not the legend.
- **"The crash was worldwide."** It was centered on North America. Japan's console market launched two new machines in the middle of it.
- **"Nintendo saved the industry with better games."** Nintendo's games mattered, but the structural fix was control of supply: licensing terms, a five-games-a-year cap and a lockout chip. Those rules are why retailers trusted the NES.

## Check yourself

1. In the shelf model with default settings (`c = 0.5`), suppose publishers react in year 4 by cutting shipments back to 200. Compute year 4's new sold, bin sold, unsold stock and revenue.
2. Supply and demand both double in year 2, and demand stays flat afterward. What does the model predict for the bin and for revenue? What does that tell you about which number to watch?
3. A new MMO patch doubles the drop rate of a crafting material while the number of crafters grows 30%. Rewrite the situation in the shelf model's terms. What plays the role of the $5 bin, and what would a "licensing gate" look like in an MMO?
4. A classmate writes "Atari buried millions of E.T. cartridges because nobody bought the game." Rewrite the sentence so every claim in it is supported by a cited source.

<details>
<summary>Answers</summary>

1. Year 4 starts with `U = 150`. Bin sold `= min(150, 0.5 × 200) = 100`, at $5, for $500. New sold `= min(200, 200 − 100) = 100`, at $35, for $3,500. Revenue $4,000. Unsold stock `= 150 − 100 + (200 − 100) = 150`. Cutting shipments stops the pile from growing (it stays at 150) but revenue does not recover, because the bin still holds a year's worth of cheap stock that keeps eating full-price sales.
2. Shipments equal demand every year, so nothing is left over, the bin stays at zero and revenue is `35 × 200 = $7,000` every year from year 2. Growth itself is harmless. The ratio of supply growth to demand growth is the number that matters.
3. `S` is the materials entering the game per day, now doubled. `D` is the materials crafters use, up 30%. `U` is the pile of auction house listings. The bin is the vendor sell price, the floor below which nobody sells. A gate would limit how many materials can enter per day (lower drop rates, daily gathering caps) or add a sink that removes surplus.
4. For example: "In September 1983 Atari buried excess stock of many games at a landfill near Alamogordo. A former Atari manager later put the number of cartridges at about 728,000. E.T. had sold over 2.6 million copies in 1982, but at least 669,000 were returned in 1983." Each sentence maps to a cited source.

</details>

## Lab / assignment hook

[Lab 04, the crash spreadsheet](../labs/lab04.md). Build the shelf model in a spreadsheet, reproduce the table in section 2, run three causal scenarios and write a 400-word argument about which cause mattered most. The argument feeds the 1982 to 1985 stretch of your timeline project.

## Sources

- Wikipedia, "Video game crash of 1983" (accessed September 2026), and the sources it cites, notably Ernkvist, M. (2006), "Down Many Times, but Still Playing the Game: Creative Destruction and Industry Crashes in the Early Video Game Industry 1971-1986," XIV International Economic History Congress. Used for: VCS history and Space Invaders; Activision's 1979 founding and reasons; Crane's 3-to-30 developers; 17 companies and 90 games at Summer 1982 CES; 100 to over 400 Atari games from June to December 1982; Atari's cartridge share 75% (1981) to under 40% (1982); the Goldman Sachs demand +100% and output +175% statement; December 1982 missed target; failed returns and $35 to $5 markdowns; Atari losses of $356 million by mid-1983 and over $536 million by end of 1983; C64 price cut to $300 in June 1983 and $199 in some stores; US sales about $3 billion at the 1982 peak to about $100 million (1985), the 1982 peak as given in Kinder, M. (1993), *Playing with Power in Movies, Television, and Video Games*, University of California Press, p. 90 (the article's lead gives $3.2 billion in 1983, uncited); worldwide $42 billion to $14 billion; Famicom and SG-1000 launch on July 15, 1983; 6.5 million Famicom homes by 1986; Yamauchi's 1986 comment; the Seal of Quality.
- Wikipedia, "Nintendo Entertainment System" (accessed September 2026). Third-party contract terms: exclusivity, minimum order of 10,000 cartridges, five games per year; October 1985 North American release; 10NES lockout chip.
- Wikipedia, "E.T. the Extra-Terrestrial (video game)" (accessed September 2026). Five-week schedule, $20 to 25 million license, December 1982 release, over 2.6 million sold by end of 1982, at least 669,000 returned in 1983, Billboard top-15 chart, January 8, 1983; at least 669,000 returned in 1983, from Atari Corp., *Cartridge Sales Since 1980* (internal report, as shown in *Once Upon Atari*, episode 4, 2003); Kassar's 3.5 of 4 million figure, from Bruck, C. (1994), *Master of the Game: Steve Ross and the Creation of Time Warner*, Penguin edition 1995, pp. 179-180.
- Wikipedia, "Atari video game burial" (accessed September 2026), citing the Alamogordo Daily News (September 1983) and the Associated Press, "Diggers find Atari's E.T. games in landfill" (April 26, 2014). Ten to twenty truckloads in September 1983; James Heller's 728,000 cartridges; about 1,300 cartridges recovered from 59 different games.
- Wikipedia, "Steam Greenlight" (accessed September 2026). Greenlight 2012 to 2017, Steam Direct launched June 13, 2017, $100 fee refunded after $1,000 in sales, about 3,400 games mass-approved, Valve's acknowledgment of discovery and quality problems.
- Donovan, T. (2010). *Replay: The History of Video Games*. Yellow Ant, East Sussex (xiv + 501 pp.).
- The shelf model, its starting values and every revenue figure in section 2 are invented for teaching. Only the two growth rates and the two prices come from the sources above.

## Interactive spec: examples/w04-crash-shelf-model.html

**The one insight:** revenue can collapse while demand in units stays flat, because unsold stock sold at a markdown eats full-price sales. The gap between supply growth and demand growth, not either rate alone, fills the shelf.

**Layout.** Two linked charts side by side on desktop, stacked on mobile (revenue on top). Shared horizontal axis "Year" 1 to 5 (integer steps).

- **Left chart, "What the sales report shows":** revenue per year as bars. Each bar is stacked in two colors, full-price revenue (`P × new_sold`) at the bottom and bin revenue (`b × bin_sold`) on top. Label the peak bar with its value and the last bar with "−X% from peak".
- **Right chart, "What is on the shelf":** demand `D` as a solid line with dots, shipments `S` (after the gate) as a dashed line, and unsold stock `U` (end of year) as a filled area. A faint horizontal reference at `0.5 × D` labeled "half a year of demand".
- **Readout table (copyable)** under the charts, one row per year: Year, D, S, New sold, Bin sold, U after, Revenue. One decimal for units, whole dollars for revenue.
- **Caption line** above both charts: "Demand year 2 → 5: 200 → 200. Revenue peak → year 5: $7,000 → $4,000 (−43%)." Update live.

**Controls (keyboard accessible, labeled, each with numeric readout):**

1. Year-2 demand growth, slider 0% to 200%, step 5, default 100%.
2. Year-2 supply growth, slider 0% to 300%, step 5, default 175%.
3. Demand change per year from year 3, slider −50% to +50%, step 5, default 0%.
4. Bargain share `c`, slider 0 to 1, step 0.05, default 0.5.
5. Full price `P`, stepper $10 to $60, step 1, default $35. Bin price `b`, stepper $0 to $20, step 1, default $5.
6. Demand shock toggle (default off) with year selector (2 to 5, default 4) and size slider (0% to 90%, step 5, default 50%). The shock multiplies that year's `D` by `(1 − size)` and the lower level carries into later years.
7. Licensing gate toggle (default off) with headroom slider 0.50 to 2.00, step 0.01, default 1.00. When on, shipments that year are `min(S, headroom × D)`.
8. Reset button restoring all defaults.

**Formulas (evaluate years 1 to 5 in order).**

```
Year 1: D = 100, S = 100, U = 0
Year 2: D = D × (1 + demand growth), S = S × (1 + supply growth)
Year ≥ 3: D = D × (1 + later demand change); S unchanged
If shock on and year == shock year: D = D × (1 − shock size)
S_eff = gate on ? min(S, headroom × D) : S
bin_sold = min(U, c × D)
new_sold = min(S_eff, D − bin_sold)
U = U − bin_sold + (S_eff − new_sold)
revenue = P × new_sold + b × bin_sold
```

Note that the shock scales `D` at the moment it is applied, and later years build on the reduced value.

**Test values.**

Defaults (`c = 0.5`, +100% / +175%, no shock, no gate):

| Year | D | S | New sold | Bin sold | U after | Revenue ($ thousands) |
|---|---|---|---|---|---|---|
| 1 | 100 | 100 | 100 | 0 | 0 | 3,500 |
| 2 | 200 | 275 | 200 | 0 | 75 | 7,000 |
| 3 | 200 | 275 | 125 | 75 | 150 | 4,750 |
| 4 | 200 | 275 | 100 | 100 | 225 | 4,000 |
| 5 | 200 | 275 | 100 | 100 | 300 | 4,000 |

`c = 1`, other defaults: year 4 new 50, bin 150, U 225, revenue 2,500; year 5 new 0, bin 200, U 300, revenue 1,000 (−86% from peak).

Shock on (year 4, 50%), other defaults: year 4 D 100, new 50, bin 50, U 325, revenue 2,000; year 5 D 100, new 50, bin 50, U 500, revenue 2,000.

Gate on, headroom 1.10, other defaults: S 220 from year 2; year 3 new 180, bin 20, U 40, revenue 6,400; year 5 new 140, bin 60, U 80, revenue 5,200. Headroom 1.12 is the loosest value that keeps U below 0.5 × D through year 5 (year 5 U = 96).

Gate on, headroom 1.0, other defaults: every year from 2 has S 200, new 200, bin 0, U 0, revenue 7,000.

Supply growth 100%, other defaults: identical to the gate case.

**First screen:** defaults, so the left chart shows a peak at year 2 and a slump to $4,000, and the right chart shows a flat demand line at 200 with the unsold area climbing to 300 beneath the dashed shipments line. No instructions above the charts, only the caption.

**Content rules.** No console, cartridge or logo art. Draw generic bars, lines and areas using the shared palette. Add one line of small text under the charts: "Illustrative model. Growth rates from a 1983 analyst estimate; prices from reports of the period; all other numbers invented."
