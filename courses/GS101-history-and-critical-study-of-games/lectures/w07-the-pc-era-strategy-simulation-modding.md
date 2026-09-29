# GS101 · Week 07 — The PC era: strategy, simulation, the modding scene

**Why this matters:** Three of the biggest genres of the last twenty years, the team shooter, the MOBA and the battle royale, did not start in a studio's pitch meeting. They started as free modifications of somebody else's PC game. If you want to explain where genres come from, you have to explain why the PC let players build games, and who ended up owning what they built.

**You will be able to:**
- Explain three properties of the 1990s PC (open platform, mouse and keyboard, downloadable distribution) and link each to a genre or business model it made possible.
- Place a mod on a host-to-standalone timeline and compute its two lags: host to mod, and mod to standalone game.
- Compare lags across cases grouped by who owned the host game, and state what the comparison can and cannot prove.
- Critique a "this genre was invented by game X" claim using a lineage table instead of a single date.

**Before class:** Donovan, *Replay: The History of Video Games* (2010), the pages on the rise of PC gaming in the late 1980s and 1990s (strategy, simulation and id Software's shooters). The course reader lists the pages. Skim the Wikipedia article "Doom modding" (about 10 minutes) for the WAD file system and the first fan-made editors.

**Prerequisites from earlier courses:** None; this is a first-semester course. Two lectures you may be taking alongside connect directly. [GD102 week 1, systems thinking](../../GD102-systems-design-and-game-mechanics/lectures/w01-systems-thinking-parts-relationships-emergence.md) explains the stocks-and-relationships view of SimCity that section 3 relies on. [GD101 week 13, genres as clusters of mechanics](../../GD101-introduction-to-game-design/lectures/w13-genres-as-clusters-of-mechanics.md) gives you a way to say what a genre is before we ask where one came from. Within this course, [week 3, the arcade era and the coin-op business model](w03-arcade-era-and-the-coin-op-business-model.md) and [week 4, home consoles and the 1983 crash](w04-home-consoles-and-the-1983-crash.md) set up the contrast with a closed platform.

**Interactive:** [The mod pipeline](../examples/w07-mod-pipeline.html). Keep it open during section 2.

---

## 1. What was different about the PC

In week 4 you saw a closed platform. A console maker decides which cartridges or discs can run on its machine, takes a licence fee on each one and controls the shelf. The IBM-compatible PC of the late 1980s and 1990s worked the other way. Nobody owned the whole platform. Anyone with a compiler could write software for it, and anyone with a modem could pass that software to a friend. Three properties follow, and each one shaped design.

**An open platform.** No licence fee and no approval step meant small teams and odd ideas could ship. Will Wright's SimCity (1989) had no way to win and no way to lose in its core mode. Publishers turned it down because they did not believe a game with no goal could sell. Brøderbund eventually agreed to distribute it. It sold about 500,000 copies on home computers before the console port. A closed platform with a gatekeeper would very likely have kept saying no.

**Mouse and keyboard.** A mouse lets you point at any spot on the screen at once. A gamepad makes you walk a cursor there. Genres that need many precise selections per minute, like real-time strategy, grew up on the PC because the input device suited them.

**Distribution over wires.** Before broadband, bulletin board systems and early internet sites let players copy files freely. id Software used this deliberately. On 10 December 1993, the team uploaded the first episode of Doom as shareware to a University of Wisconsin FTP server, free to copy, and sold the other two episodes directly. Shareware turned players into the distribution network.

The same wires carried something else back the other way. Players did not only download games. They uploaded new levels, new rules and eventually whole new games built inside old ones. That is the modding scene, and it is the subject of the worked example.

### A vocabulary for this week

- A **host game** is the commercial game a mod runs inside.
- A **mod** (modification) is player-made content that changes a host game. A **map** or **level** changes only the space. A **total conversion** replaces rules, art and setting while keeping the host's engine.
- An **engine** is the reusable code that draws the screen, runs physics and handles input.
- **Tools** are what a developer releases so players can make mods. That can be a level editor (Warcraft III shipped with its World Editor), a software development kit or SDK (Valve released the Half-Life SDK in April 1999), or a scripting language (Quake's QuakeC).
- A **standalone** game is a commercial product that no longer needs the host to run.

## 2. Worked example: the mod pipeline

### The hook

Counter-Strike began as a free Half-Life mod made by two hobbyists, Minh Le and Jess Cliffe. Defense of the Ancients (DotA), the map that defined the MOBA genre, was built with the level editor bundled with Warcraft III. PUBG, the game that carried the battle royale format to a mass audience in 2017, grew from a mod for the military simulator Arma 2.

A player's natural question is "who invented this genre?" A historian's better question is "how long did each step take, and what made it faster or slower?" You can answer the second one with a table.

### One model, stated once

Treat every mod-born genre as a three-step pipeline:

```
host game released  ──►  mod first public  ──►  standalone game released
      t_H                      t_M                        t_S

tool lag            L_M = t_M − t_H
commercial lag      L_S = t_S − t_M
total lag           L   = t_S − t_H = L_M + L_S
```

- `t_H` is the year the host game shipped.
- `t_M` is the year the mod first reached the public (an alpha or beta counts).
- `t_S` is the year a company released a standalone game built from the mod. If the standalone was sold in early access first, use that year, because that is when it went on sale.
- `O` is a label, not a number: **host-owned** if the company that owns the host game (or one it bought) made the standalone, **third-party** if a different company did.

We work in whole years because several mods have no reliable month for their first public release. That is a real limit of the evidence, and it is why the model uses years at all.

### Numbers you can check

Every date below comes from the Sources section. Compute the two lags yourself before reading the last columns.

| Case | Host, `t_H` | Mod, `t_M` | Standalone, `t_S` | `L_M` | `L_S` | Owner `O` |
|---|---|---|---|---|---|---|
| Team Fortress | Quake, 1996 | Team Fortress (Quake mod), 1996 | Team Fortress Classic (Valve), 1999 | 0 | 3 | third-party |
| Counter-Strike | Half-Life, 1998 | beta 1, June 1999 | Counter-Strike retail (Valve), Nov 2000 | 1 | 1 | host-owned |
| DotA to League | Warcraft III, 2002 | DotA, 2003 | League of Legends (Riot), Oct 2009 | 1 | 6 | third-party |
| DotA to Dota 2 | Warcraft III, 2002 | DotA, 2003 | Dota 2 (Valve), July 2013 | 1 | 10 | third-party |
| DayZ | Arma 2, 2009 | DayZ mod alpha, 2012 | DayZ early access (Bohemia), Dec 2013 | 3 | 1 | host-owned |
| Battle royale | Arma 2, 2009 | DayZ: Battle Royale, about 2013 | PUBG early access (Bluehole, now Krafton), Mar 2017 | 4 | 4 | third-party |

A few notes on the coding, because coding is where historians disagree:

- Team Fortress Classic was released in April 1999 as a free Half-Life mod made by Valve after Valve bought the original team's company in 1998. It was a studio product, but it still needed Half-Life, so a strict reader would use Valve's standalone Team Fortress 1.5 (2000) and get `L_S = 4`. Either way the case stays third-party, because id Software owned Quake and Valve did not.
- Counter-Strike is host-owned because Valve, which made Half-Life, acquired the mod's rights and released the retail game on 9 November 2000.
- DayZ is host-owned because Bohemia Interactive, which made Arma 2, hired the mod's designer, Dean Hall, and announced the standalone on 7 August 2012.
- Brendan Greene's battle royale mod is dated "around 2013" in the sources. Using 2013 is a choice. Write it down when you make choices like this.

Now group the commercial lag `L_S` by owner:

| Owner | Cases | `L_S` values | Median `L_S` |
|---|---|---|---|
| host-owned | Counter-Strike, DayZ | 1, 1 | 1 year |
| third-party | Team Fortress, League, Dota 2, PUBG | 3, 6, 10, 4 | 5 years |

And look at the tool lag `L_M`. All six mods reached the public within four years of the host, and four of them within a year. Counter-Strike's first beta came out on 18 June 1999, a few months after Valve released the Half-Life SDK in April 1999. Tools arrive, mods follow fast.

### A visual you can move

Open the interactive. The left panel is a calendar timeline, 1993 to 2018, one row per case, with three dots (host, mod, standalone) joined by a line. It looks like a mess of overlapping bars from different decades. The right panel lines up every row so the host release sits at zero. Now the pattern jumps out. Every mod dot huddles near the left edge. The standalone dots split into two groups by colour: host-owned rows end close to their mod, third-party rows trail off to the right.

Use the "Colour by owner" button to recolour, the "Strict Team Fortress" button to switch Team Fortress to the 2000 standalone, and the readout table to test your own coding choices. Each row there has number boxes for the mod and standalone years and a menu for the owner. Watch the medians in the readout. The gap between the two groups survives every reasonable recoding you try, but it shrinks or grows by a year or two. That is the honest size of the claim.

### Why the pattern makes sense

A company that owns the host game has two advantages. It already has the engine, so turning a mod into a product is mostly polish. And it has the legal right to do so without negotiating. Valve could buy Counter-Strike and ship it in about eighteen months because the engine was Valve's own.

A third party has neither. Riot Games had to build a new game for League of Legends, and hired Steve Feak, one of DotA's designers, to help. Valve had to acquire the DotA rights in 2009, hire the map's maintainer IceFrog in October 2009, and build Dota 2 as a new game. Greene's battle royale idea passed through a consulting job on Sony Online's H1Z1 before Bluehole built PUBG as a new game. Each of those steps takes years.

### Cross-game recognition

The pipeline model is not only about famous genres. Rewrite these other cases in the same form and you will see the same two forces, tools and ownership.

**Doom (id Software, December 1993).** Doom stored its levels and graphics in WAD files, separate from the engine, because John Carmack wanted fans to be able to modify the game. id released no editing instructions, yet players built their own level editor. Wikipedia's history of Doom modding dates the first public Doom Editor Utility to 26 January 1994 and the first custom level to March; no primary record of those dates was reachable. On those dates, the tool lag is about three months, even without official tools, because the data format was deliberately open. It is the lower bound for `L_M` in this era.

**Aeon of Strife to DotA (StarCraft custom map to Warcraft III map).** DotA itself was not the first step. Its first author, Eul, took inspiration from Aeon of Strife, a StarCraft custom map, and rebuilt the idea with the more capable Warcraft III World Editor in 2003. So DotA is a mod of an idea that already lived in another host. Pipelines chain. When you see a genre "invented" by one game, look one step upstream.

**SimCity and its own editor (Maxis, 1989).** Will Wright started SimCity because, while building the helicopter game Raid on Bungeling Bay, he enjoyed making islands in the level editor more than playing the game. SimCity is, in a sense, a level editor turned into the product. Shortly after release Maxis sold the SimCity Terrain Editor as an add-on. Here the host owner and the tool maker are the same company, so `L_S` is effectively zero: the "mod" was sold by the studio from the start.

Three contexts, one shape: open data or bundled tools shrink the first lag, and ownership of the host shrinks the second.

### Eyes-open judgment

The table is useful. It is also easy to over-read. Before you use a model like this in an essay, decide these things on purpose.

- **Survivorship bias.** You only know about mods that became famous. Thousands of mods were never commercialized. Six successes cannot tell you the chance that a mod becomes a product. They can only compare timing among successes.
- **Sample size.** Two host-owned cases is a pattern, not a law. Present it as "in these cases" and say what new case would falsify it. A third-party standalone released one year after its mod would weaken the claim.
- **Coding choices move the numbers.** Early access versus full release, month versus year, which "standalone" counts. Report your rule and show at least one alternative coding, as the Team Fortress note does.
- **Why a designer should care.** If you ship tools, you are funding your players' research and development. Valve's history is a studio treating its mod scene as a talent pipeline. Blizzard's history with DotA shows the opposite outcome: the most valuable idea built with its editor became two competitors' products. Neither result was an accident of the tools alone; licence terms and hiring decisions decided them.

### Check yourself (worked example)

1. A studio ships a host game in 2015 with no official tools. A mod appears in 2019 and a third party releases a standalone in 2024. Compute `L_M`, `L_S` and `L`. Which of the two groups does it fall into, and does it support or weaken the pattern?
2. Recode DotA's standalone as "first playable version of League of Legends in 2009" and Dota 2 as its 2011 public showing instead of its 2013 release. Recompute the third-party median. Does the gap with host-owned cases survive?

<details>
<summary>Answers</summary>

1. `L_M = 4`, `L_S = 5`, `L = 9`. Third-party, with a five-year commercial lag, which sits at the third-party median and supports the pattern. The four-year tool lag fits a host with no official tools.
2. League stays at 6. Dota 2 becomes `2011 − 2003 = 8`. The third-party values are 3, 6, 8, 4, median 5. The host-owned median is still 1. The gap survives.

</details>

## 3. Strategy and simulation: the PC's home genres

Mods explain where some genres came from. But the PC's own signature genres, strategy and simulation, came from studios, and they show the platform's properties at work.

### Turn-based strategy and the 4X label

Sid Meier's Civilization (MicroProse, September 1991), designed by Sid Meier and Bruce Shelley, asked you to guide a people from the first city to the space age. It is usually named as the game that established the 4X genre (explore, expand, exploit, exterminate), and it sold 1.5 million copies over its life. A turn-based design suits a machine with a mouse, a large screen of information and a player who sits at a desk for hours. It does not suit a living-room couch and a gamepad, which is one reason 4X stayed a PC genre for decades.

### Real-time strategy

Westwood's Dune II (December 1992) was not the first real-time strategy game, but it set the template that others followed. You harvest a resource with a vehicle, convert it to credits at a refinery, build structures that unlock other structures (a technology tree) and spend credits on units. Warcraft: Orcs & Humans (Blizzard, November 1994), Command & Conquer (Westwood, September 1995) and StarCraft (Blizzard, March 1998) refined that loop. Read Dune II with GD102's stock-and-flow vocabulary and the core is a two-stock machine: spice in the field flows through harvesters into credits, credits flow into units, units protect the harvesters.

Notice a thread that connects this section to section 2. Blizzard shipped a map editor with Warcraft II, StarCraft and Warcraft III. The genre that grew out of those editors, the MOBA, is a real-time strategy game with the base-building removed and one hero per player. The PC's strategy genres were the soil the mod scene grew in.

### Simulation as a "toy"

SimCity is the clearest case of the open platform letting an unusual design ship. Its core mode has no victory condition. You zone land, the simulation grows or shrinks a city, and you judge the result. Broderbund, its eventual distributor, suggested adding time-limited scenarios you could win or lose, to make it look more like a conventional game. That detail is a good example of a business pressure leaving a visible mark on a design. When you close-read a game in this course, look for features like the scenarios: things that exist because someone had to sell the game.

## 4. Reading history critically: "first" claims

History writing about games is full of "firsts." Dune II was "the first RTS." DotA "invented" the MOBA. Treat every such claim as a question with three parts.

1. **First by what definition?** If a genre is a cluster of mechanics (GD101 week 13), then "first" depends on which mechanics you require. Dune II was not the first real-time strategy game; the sources say it set the template. Those are different claims.
2. **First to whom?** A game can be first in a country, on a platform or in sales. Aeon of Strife came before DotA, so "first MOBA" depends on whether you mean the first map with the idea or the first one that made it popular.
3. **What was upstream?** Look one step up the pipeline. Almost every "first" has a parent, a host or an inspiration.

A lineage table like the one in section 2 is a better answer than a single "first." It shows the chain, dates each link and states the coding rules. That is the format you will use in the timeline project.

## In-class activity (25 min)

In groups of three, extend the mod pipeline table.

1. Each group gets one card with a case not covered above: Doom total conversions, Team Fortress 2, a tower-defense map lineage, or a mod of the group's choosing that has a standalone game.
2. Find `t_H`, `t_M` and `t_S` from at least one reliable source each (developer site, contemporary press or a well-maintained wiki). Record the source next to each date.
3. Compute `L_M` and `L_S`, and code the owner `O`.
4. Enter your row in the shared class sheet and in the interactive's "add a row" form. Recompute the medians.
5. Write one sentence stating whether your case supports, weakens or does not bear on the pattern, and one sentence naming the coding choice you were least sure of.

Expected output: one table row with three sourced dates, two lags, an owner code and two sentences. The class sheet at the end is a larger sample, and you should see whether the gap between owner groups holds up.

## Common misconceptions

- **"The modder invented the genre, so they got rich."** Ownership decided who profited. DotA's original designers did not own Warcraft III or its engine. Some later joined studios (Feak at Riot, IceFrog at Valve in October 2009), but the genre's commercial value went mainly to companies.
- **"Mods only happen when the developer supports them."** Doom's first editors were built by players without official instructions. Open data formats lower the barrier. Official tools lower it further.
- **"The PC era was about better graphics than consoles."** The bigger differences were openness, input and distribution. SimCity and Civilization were not graphics showcases.
- **"Six cases prove the pattern."** Six cases show a pattern among successes. They cannot show how often mods succeed or rule out other causes.

## Check yourself

1. Warcraft III shipped in July 2002 and DotA appeared in 2003. League of Legends shipped in October 2009. Compute `L_M`, `L_S` and `L` for this chain and name the owner category.
2. Explain in two sentences why a host-owned standalone can ship faster than a third-party one. Name the two advantages.
3. A friend says "SimCity was the first city-builder, so every city-builder copies it." Rewrite this as a claim that survives the three questions in section 4.
4. Name one design feature of SimCity that exists because of a business pressure, and the pressure behind it.
5. A 2018 host game ships with full modding tools. A mod appears in 2019 and the host's studio releases it as a standalone in 2021. A historian says this proves host ownership causes short lags. What is wrong with that inference, and what evidence would make it stronger?

<details>
<summary>Answers</summary>

1. `L_M = 1`, `L_S = 6`, `L = 7`. Third-party, because Riot did not own Warcraft III.
2. The host owner already has the engine, so commercialization is mostly polish, and it has the legal right to sell the result without negotiating for it. A third party usually has to build a new engine or acquire rights, and each of those takes time.
3. For example: "SimCity (1989) is the earliest widely sold commercial city-building simulation on home computers, and its no-win core mode influenced many later city-builders." It names the definition, the audience and the date, and leaves room for predecessors.
4. The time-limited scenarios you can win or lose. Broderbund, its distributor, suggested them to make an open-ended simulation look like a conventional, sellable game.
5. One case cannot establish a cause, and the case may differ in other ways (tool quality, team size, market). Stronger evidence would be many cases, including failures, with host-owned and third-party groups compared on similar tools and eras, and a stated coding rule.

</details>

## Lab hook

[Lab 07, a mod lineage for the timeline project](../labs/lab07.md). You build a sourced lineage table for one mod-born genre, with at least five links and two alternative codings, and write a 400-word argument about what caused the timing you found. It becomes one strand of your timeline project (25% of the course grade).

## Sources

- Wikipedia, "SimCity (1989 video game)", accessed September 2026. February 1989 release, publishers' refusals, Broderbund's distribution and suggested scenarios, 500,000 home-computer sales, the Raid on Bungeling Bay level-editor origin, the SimCity Terrain Editor add-on.
- Doom Wiki, "Doom" (doomwiki.org, archived 14 January 2026, read September 2026). First release on 10 December 1993 as a shareware upload to an FTP server at the University of Wisconsin.
- Wikipedia, "Doom (1993 video game)" and "Doom modding", accessed September 2026. WAD files and Carmack's intent; Doom Editor Utility on 26 January 1994 and first custom level in March 1994 (Wikipedia only; the Doom Wiki page on DEU was unreachable).
- Wikipedia, "Civilization (video game)", accessed September 2026. September 1991 release by MicroProse, designers Meier and Shelley, 1.5 million copies, role in establishing 4X.
- Wikipedia, "Dune II", "Warcraft: Orcs & Humans", "Command & Conquer (1995 video game)" and "StarCraft (video game)", accessed September 2026. Release dates and Dune II's template (harvesting, technology tree).
- Wikipedia, "Quake (video game)", accessed September 2026. June 1996 release, QuakeC and its role in popularizing mods.
- Wikipedia, "Team Fortress Classic", accessed September 2026. Team Fortress as a 1996 Quake mod, Valve's 1998 acquisition of TF Software (Wikipedia gives June 1998), April 1999 release, Team Fortress 1.5 in 2000.
- Wikipedia, "Counter-Strike (video game)" and "Half-Life (video game)", accessed September 2026. Half-Life on 19 November 1998, Half-Life SDK on 7 April 1999 (Wikipedia only; the lecture gives the month), Valve's acquisition of the rights, retail release on 9 November 2000.
- Jensen, J., "Counter-Strike Year 1", CS-Nation (csnation.counter-strike.net, archived 15 August 2000, read September 2026), page 2. Beta 1 released "June 18th, 1999 8:06 PM Pacific Time", "a few short months after the Half-Life SDK was released".
- Wikipedia, "Defense of the Ancients", "Warcraft III: Reign of Chaos", "League of Legends" and "Dota 2", accessed September 2026. Warcraft III on 3 July 2002 with World Editor, Eul's 2003 map, Aeon of Strife inspiration, Feak joining Riot, Valve's 2009 acquisition of DotA rights, League of Legends on 27 October 2009 (Wikipedia only; the lecture relies on the year), Dota 2 on 9 July 2013.
- O'Connor, A., "DotA Dev Joins Valve, Hints at Future Game", Shacknews, 5 October 2009 (archived April 2012, read September 2026). IceFrog announces he is leading a team at Valve.
- Wikipedia, "Arma 2", "DayZ (video game mod)" and "DayZ (video game)", accessed September 2026. Arma 2 in May to July 2009 by region, DayZ mod reaching one million players by August 2012, standalone announced 7 August 2012, early access on 16 December 2013.
- Wikipedia, "PUBG: Battlegrounds", accessed September 2026. Greene's DayZ: Battle Royale mod around 2013, H1Z1 consultancy, early access in March 2017, full release December 2017.
- Primary release records on Steam (store.steampowered.com, and the Steam news feed for each app, accessed September 2026). Dota 2 (app 570) release date 9 July 2013. DayZ (app 221100) Steam announcement "DayZ is now live" and "Now Available on Steam Early Access," 16 December 2013. PUBG (app 578080) announcements "Early Access is now available!" and "Early Access Launch Day Patch Notes!", 23 March 2017. Half-Life (app 70) release date 19 November 1998. Steam lists Counter-Strike (app 10) as 1 November 2000; the retail boxed release by Sierra is dated 9 November 2000 in the Wikipedia article. Both fall in 2000, so the year coding does not change.
- Donovan, T. (2010). *Replay: The History of Video Games*. Yellow Ant, East Sussex (xiv + 501 pp.).

## Interactive spec: examples/w07-mod-pipeline.html

**Insight the visual must make obvious:** on a calendar the six cases look unrelated, but aligned at host release they show two regularities at once. Mods appear soon after the host (tool lag is short), and standalone games come fast only when the host's owner makes them (commercial lag depends on ownership).

**Layout:** two linked panels, side by side at 1280px (calendar left, aligned right), stacked at 390px (calendar on top). Below them, a readout table and an "add a row" form.

**Left panel, "Calendar":** x axis years 1993 to 2018, one row per case (six defaults). Each row has three markers joined by a line: host (hollow square), mod (filled circle), standalone (filled diamond). Row label is the case name as text. Row line colour by owner: host-owned uses the palette's accent colour, third-party uses the palette's secondary colour. Include a text legend. No logos or game art.

**Right panel, "Aligned at host release":** same rows, x axis `years since host` from 0 to 15. Host marker at 0, mod at `L_M`, standalone at `L`. Draw a vertical dashed line at the median `L` of each owner group, labelled "host-owned median" and "third-party median". Hovering or focusing a row in either panel highlights it in both.

**Default data (years):**

| Case | t_H | t_M | t_S | owner |
|---|---|---|---|---|
| Team Fortress | 1996 | 1996 | 1999 | third-party |
| Counter-Strike | 1998 | 1999 | 2000 | host-owned |
| DotA to League of Legends | 2002 | 2003 | 2009 | third-party |
| DotA to Dota 2 | 2002 | 2003 | 2013 | third-party |
| DayZ | 2009 | 2012 | 2013 | host-owned |
| Battle royale to PUBG | 2009 | 2013 | 2017 | third-party |

**Controls:**
- "Colour by owner" toggle (default on). Off draws all rows in one neutral colour and hides the median lines, so students can see the pattern disappear without the grouping.
- "Strict Team Fortress" toggle (default off). On sets Team Fortress `t_S = 2000`.
- For each row, a small number input for `t_M` and one for `t_S` (step 1, min `t_H`, max 2025), reachable by keyboard, so students can test alternative codings.
- An owner dropdown per row (host-owned, third-party).
- "Add a row" form: case name (text), `t_H`, `t_M`, `t_S`, owner. Validate `t_H ≤ t_M ≤ t_S`; show an inline error otherwise. Maximum 12 rows.
- Reset button restores the default data.

**Formulas:** `L_M = t_M − t_H`, `L_S = t_S − t_M`, `L = t_S − t_H`. Medians computed per owner group over `L_S` and over `L` (for an even count, the mean of the two middle values).

**Readout:** a table with every row's `t_H`, `t_M`, `t_S`, `L_M`, `L_S`, `L`, owner, plus two summary lines: median `L_S` per owner group and median `L_M` over all rows.

**Test values (defaults):** `L_S` host-owned {1, 1}, median 1; third-party {3, 6, 10, 4}, median 5. `L_M` all rows {0, 1, 1, 1, 3, 4}, median 1. `L` host-owned {2, 4}, median 3; third-party {3, 7, 11, 8}, median 7.5. With "Strict Team Fortress" on: Team Fortress `L_S = 4`, third-party `L_S` median 5 (values {4, 6, 10, 4}), `L` third-party {4, 7, 11, 8}, median 7.5.

**Accessibility and motion:** all markers have text equivalents in the readout table. Row highlight must not rely on colour alone (thicken the line and bold the label). Respect `prefers-reduced-motion` for any transitions.
