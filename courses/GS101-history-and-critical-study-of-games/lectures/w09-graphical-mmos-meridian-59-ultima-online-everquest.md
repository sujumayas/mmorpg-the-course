# GS101 · Week 09 — Graphical MMOs: Meridian 59, Ultima Online, EverQuest

**Why this matters:** Between 1996 and 1999, three games turned the text MUDs of week 5 into graphical worlds that hundreds of thousands of people paid for every month. Almost every number you will read about these games, and about the MMOs that followed, is a subscriber count. Subscriber counts measure a business. They do not tell you how many people were in the world with you. This week you learn to tell those apart, and to read the history of online worlds with that difference in mind.

**You will be able to:**
- Distinguish subscribers, concurrent users and players per world (shard), and compute a concurrency ratio and a per-world population from published figures.
- Estimate a missing figure with the model and label it as an estimate, stating the assumption it rests on.
- Compare the design choices of Meridian 59, Ultima Online and EverQuest and connect each to a business or technical pressure of the late 1990s.
- Critique a claim about an MMO's size by asking which number it uses, who published it and when.

**Before class:** Bartle, *Designing Virtual Worlds* (2003), chapter 1, the history of virtual worlds from "The First Age: 1978-1985" to the end of "The Fifth Age: 1997-Present" (pp. 5-43 in the author's free PDF edition at mud.co.uk/richard/DesigningVirtualWorlds.pdf). Skim the Wikipedia articles "Meridian 59", "Ultima Online" and "EverQuest" for their Sales and subscriptions sections (about 20 minutes in total), and note every number and its date.

**Prerequisites from earlier courses:** None; this is a first-semester course. Within this course, [week 5, text adventures and MUD1](w05-text-adventures-and-mud1.md) covers the text worlds these games grew from, and [week 6, the RPG lineage from Dungeons & Dragons to Ultima and Wizardry](w06-the-rpg-lineage-dnd-to-ultima-and-wizardry.md), covers the single-player Ultima series behind Ultima Online. The difference between an average and a peak is treated properly in [MA102 week 12, descriptive statistics](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w12-descriptive-statistics-for-playtests.md). If you continue to the MMO specialization, [MMO301](../../MMO301-virtual-worlds-history-theory-and-design/syllabus.md) returns to Ultima Online (week 3), EverQuest (week 4) and EVE Online (week 6) as design case studies.

**Interactive:** [MMO peaks timeline](../examples/w09-mmo-peaks-timeline.html). Keep it open during section 2.

---

## 1. From text worlds to paid graphical worlds

### What came between MUD1 and Meridian 59

Week 5 ended with MUD1 (1978) and the MUD family. Two strands carried the idea toward pictures.

**Habitat** (Lucasfilm Games, beta test on the Quantum Link service in 1986) put avatars on a Commodore 64 screen. It is usually called the first graphical virtual world, though it was closer to a social space than a role-playing game.

**Neverwinter Nights** on AOL (March 1991) was a graphical role-playing game on a commercial online service. Its history shows the limit that every later game fought. Each server held 50 players in 1991 and 500 by 1995. Near the end of its run in 1997, it had about 115,000 players and typically hosted around 2,000 adventurers during prime evening hours. Services like AOL charged by the hour, so a long play session was expensive for the player and profitable for the service.

### Meridian 59 (Archetype Interactive and 3DO, 1996)

Meridian 59 went online in an early form on 15 December 1995 and launched commercially on 7 October 1996, about a year before Ultima Online. About 17,000 players joined its public beta. Three things make it a landmark.

- It is usually described as the first 3D graphical MMO role-playing game.
- It charged a **flat monthly subscription** instead of an hourly rate. At the September 1996 Online Game Developer's Conference, a panel of heads of online game services called flat-rate pricing unsustainable. Within a few years it was the standard.
- The phrase "massively multiplayer" came out of meetings inside 3DO during its development.

Its servers split players into parallel worlds of a few hundred people each, to keep any one world from getting too crowded. Remember that "few hundred." It is the most important number in this lecture.

### Why the pricing model mattered to design

Pricing is a design force. Under hourly pricing, the operator earns more when you play longer in each session, and a player has a reason to log off. Under a flat monthly fee, the operator earns the same whether you play one hour or a hundred, so what it needs is for you to renew next month. That rewards goals that take months to reach, social ties that make leaving costly, and a steady supply of new content. When you study EverQuest's long level curve and raids below, and World of Warcraft next week, ask how much of the design follows from the fee.

## 2. Worked example: three numbers for one world

### The hook

Before launch, an Origin Systems employee reported that the company expected Ultima Online to top out at about 15,000 subscribers. By December 1998, fifteen months after its 24 September 1997 launch, it had 100,000. That growth is the famous number.

IGN's report of the 100,000 milestone, published in December 1998, gives a quieter one. At 100,000 subscribers, Ultima Online averaged about 12,500 people playing at the same time. So at a typical moment, seven out of eight subscribers were not in the world at all. And the ones who were online were divided across many separate copies of the world, called **shards**.

So how big was Ultima Online? It depends which number you mean, and each number answers a different question.

### One model, stated once

```
S = subscribers (paying accounts at a date)
C = concurrent users (people logged in at the same moment; say whether peak or average)
N = number of worlds (shards or servers) those users are split across

r = C / S        concurrency ratio: the share of subscribers online at once
W = C / N        world size: players sharing one world at once
N = r × S / W    worlds needed to keep each world at size W
```

- `S` answers "how big is the business?"
- `C` answers "how much server capacity does the operator need?"
- `W` answers "how many people could I meet?" This is the number that shapes the player's experience of the world.

The third line is the same relation rearranged. It says that if each world has a fixed capacity, growing the business adds more worlds, not bigger ones.

### Numbers you can check

These are the figures that published sources support. Each one comes from the Sources section, with its date.

| World and date | `S` | `C` | `N` | `r = C/S` | `W = C/N` |
|---|---|---|---|---|---|
| Neverwinter Nights (AOL), about 1997 | about 115,000 players | about 2,000 (prime time, typical) | at least 4 (cap 500 each) | about 1.7% | at most 500 |
| Meridian 59, 1996 | — | — | several | — | a few hundred |
| Ultima Online, December 1998 | 100,000 | 12,500 (average) | not published | 12.5% | — |
| EverQuest, peaks in the early 2000s | 550,000 (peak, end of 2004) | not published | not published | — | more than 3,000 per server at peak |
| EVE Online, 2013 | over 500,000 (February) | 65,303 (record peak, 5 May) | 1 | about 13.1% | 65,303 |

Check two rows by hand. Ultima Online: `12,500 / 100,000 = 0.125`. EVE Online: `65,303 / 500,000 ≈ 0.131`. Two games fifteen years apart, both around one in eight. That similarity is interesting, but notice the fine print. Ultima Online's 12,500 is an average. EVE's 65,303 is a record peak. A peak ratio should be higher than an average one, so these two are not quite comparable. Keep that in mind whenever you put two numbers side by side.

Neverwinter Nights has a much lower ratio, about 1.7%. Its 115,000 are "players" over the life of the service, not paying subscribers at one date, and it charged by the hour. Different definitions, different pricing, different ratio. This row is here to show you that a ratio is only as good as the definitions behind it.

### Estimating what nobody published

EverQuest's publisher never gave a total concurrent figure in the sources we have, or a server count at its peak. The model lets you estimate them, as long as you label the result as an estimate.

Assume EverQuest's concurrency ratio was similar to Ultima Online's, `r = 0.125`. Then at its 550,000-subscriber peak:

```
C ≈ 0.125 × 550,000 = 68,750 concurrent users
N ≈ C / W = 68,750 / 3,000 ≈ 23 servers
```

Now test how much the estimate depends on the assumption:

| Assumed `r` | Estimated `C` | Estimated `N` at `W` = 3,000 |
|---|---|---|
| 0.10 | 55,000 | about 18 |
| 0.125 | 68,750 | about 23 |
| 0.15 | 82,500 | about 28 |

Every number in this table is a model output, not a fact about EverQuest. If you write "EverQuest had about 23 servers," you have made something up. If you write "under the assumption that one in eight subscribers was online at peak, and with more than 3,000 players per server, EverQuest would have needed roughly 18 to 28 servers," you have made a checkable estimate. Historians of games have to do this constantly, because companies publish the numbers that suit them.

### The comparison that changes the picture

Put EverQuest at its peak beside EVE Online in 2013.

- By subscribers, they were similar: 550,000 versus a little over 500,000. EverQuest was about 10% bigger.
- By world size, they were not remotely similar: more than 3,000 per EverQuest server versus 65,303 in EVE's single world. `65,303 / 3,000 ≈ 22`. A player in EVE shared a world with over twenty times as many people.

EVE Online (CCP Games, May 2003) chose to run every player in one world, a design often called single-shard. EverQuest, like Ultima Online and Meridian 59, split its players into many copies. The business numbers say these games were the same size. The world numbers say they were different kinds of place.

### A visual you can move

Open the timeline explorer. It has two linked panels sharing one time axis, 1990 to 2016.

- **Business view (top):** subscriber counts on a logarithmic scale. Ultima Online's climb to about 250,000, EverQuest's to 550,000, EVE's to 500,000, and, for context, World of Warcraft's 12 million in 2010, which dwarfs the rest and which you will study next week.
- **World view (bottom):** the largest number of people known to share one world at once. Neverwinter Nights rises from 50 to 500, Meridian 59 sits at a few hundred, EverQuest servers at over 3,000, and EVE jumps to 63,170 in 2011 and 65,303 in 2013.

In the top panel, World of Warcraft makes everything else look tiny. In the bottom panel, EVE towers and World of Warcraft has no marker, because the sources used here give no per-realm figure for it. Hover any point to see its source, its date and its type (dated report, undated claim, or model estimate). Turn on "show estimates" to add the EverQuest estimate from above, drawn hollow, with an `r` slider so you can watch it move. The gaps in the bottom panel are part of the lesson. The history of how many people shared a world is mostly unpublished.

### Cross-game recognition

The three-number model applies well beyond 1990s MMOs.

**Ultima Online's own growth.** Ultima Online reached about 250,000 subscribers by October 2000 and held around that level until a peak in mid-2003. Its players were split across shards, and the company opened new servers in Japan, Europe and South Korea in 1999 as demand grew. In the model, `S` went up and `N` went up with it. `W` did not have to change at all.

**Neverwinter Nights on AOL.** Here the world cap itself grew, from 50 to 500 per server between 1991 and 1995. That is `W` rising with better servers and connections. Growing `W` changes what kind of play is possible. A world of 50 is a party. A world of 500 has politics, and the sources describe exactly that: guilds, alliances and a social community that players valued more than the game itself.

**EVE Online's record peaks.** CCP reported a new record of 65,303 simultaneous accounts on the same server on 5 May 2013, beating 63,170 from 23 January 2011, and records have almost always been set on Sundays. That is `C` measured at its maximum, and it shows why operators care about peak rather than average. The server must survive the busiest hour of the busiest day. Then, in 2014, CCP stopped publishing subscriber counts altogether. The `S` line in the interactive simply stops. Which numbers a company publishes is itself historical evidence.

### Eyes-open judgment

- **Always ask which number.** "Biggest MMO" by subscribers, by concurrency and by world size give three different winners. Choose the one that answers your question, and say which you used.
- **Definitions drift.** "Subscriber," "player," "account" and "active user" mean different things at different companies and at different times. NCSoft said its 1998 game Lineage had more than three million subscribers at one point, most in Korea, without a date in the source we have. A number without a date and a definition is a claim, not a data point. The interactive draws it as a flagged band, not a dot.
- **Peak versus average.** Mixing them inflates or deflates ratios. Label every concurrency figure.
- **Estimates are allowed, invented facts are not.** The model is a tool for filling gaps honestly, with the assumption stated and a range shown.
- **For designers:** `W` is a design decision with costs. Small worlds are cheap to run and let you control crowding, but they split friends across servers and make the world feel empty at quiet hours. Large worlds make an economy and a society possible, as EVE shows, but need server technology and design (week 6 of MMO301) to handle thousands of players in one place.

### Check yourself (worked example)

1. A 2005 MMO reports 200,000 subscribers and a peak of 30,000 concurrent users across 12 servers. Compute `r` and `W`.
2. The same game wants each server to feel busier, with 4,000 players at peak, without losing subscribers. Using `N = r × S / W`, how many servers should it run? What will players whose friends are on different servers experience?

<details>
<summary>Answers</summary>

1. `r = 30,000 / 200,000 = 0.15` (a peak ratio). `W = 30,000 / 12 = 2,500`.
2. `N = 0.15 × 200,000 / 4,000 = 7.5`, so 7 or 8 servers. Merging from 12 to about 8 means some players must move, and friends split across servers may be reunited or separated depending on how the merge is done. Designers usually add character transfers for this reason.

</details>

## 3. Three worlds, three philosophies

The numbers tell you how the worlds were sized. The designs tell you what people did inside them.

### Meridian 59: factions and player justice

Meridian 59 focused on player-versus-player (PvP) combat. Players could join one of three political factions, fight for territory and tokens of power, and form guilds that went to war over guild halls. It also had a player-run justice system to mediate killing between players. With worlds of a few hundred, you could know most of the people on your server, and a reputation system made sense. Small `W` supports personal politics.

### Ultima Online: the simulation dream

Ultima Online grew from Richard Garriott's idea of a fantasy world shared by several thousand people, with Raph Koster as lead designer. Its ambition was a world that ran by its own rules, where players could do almost anything the simulation allowed, including attacking and killing each other.

Two stories from its early years show what that meant.

- On 9 August 1997, during a beta stress test, a player cast a fire spell that killed Lord British, Garriott's own in-game character. His invulnerability had not been reset after a server crash. Players will do whatever the system permits, including things the designers did not imagine.
- Unrestricted player killing drove many players away from the open world. With the Renaissance expansion in May 2000, Ultima Online split each shard's world into two copies of the map. In Trammel, one player could not attack another without consent. Felucca kept the original, harsher rules.

The Trammel split is a design decision you can read with this week's model. It did not change `S` or `N`. It split each world's population into two sub-worlds with different rules, letting players choose which society to live in. MMO301 week 3 studies this case in depth.

### EverQuest: groups, guilds and raids

EverQuest (Verant Interactive and Sony Online Entertainment, 16 March 1999) was a 3D world; Computer Games Magazine singled out its first-person perspective. Its designers, Brad McQuaid, Steve Clover and Bill Trost, pointed to their time playing text MUDs as the main influence. It moved the center of play from the open simulation to structured group combat. Characters progressed by killing monsters in groups, and the hardest content needed many players working together. The Game Developers Choice Online Awards gave EverQuest a Hall of Fame award in 2011, citing it as the first MMORPG with a guild system and raiding.

EverQuest outgrew Ultima Online in subscriptions by the end of 1999. It had 10,000 active subscribers one day after launch, 60,000 by April 1999 and 259,000 by September 2000, rising to its 550,000 peak at the end of 2004. Connect this to the pricing section. A flat monthly fee rewards goals that take months, and raids that need a stable group of dozens of players are a strong reason to keep paying. MMO301 week 4 studies this "treadmill."

### A comparison table

| | Meridian 59 | Ultima Online | EverQuest |
|---|---|---|---|
| Launch | Oct 1996 (online from Dec 1995) | Sep 1997 | Mar 1999 |
| Graphics | 3D | 2D (a 3D-style client came only in 2001) | 3D, first-person view praised at launch |
| Centre of play | Faction PvP and guild wars | Open simulation, player freedom | Group combat, raids |
| World size `W` | A few hundred | Not published | More than 3,000 at peak |
| Known subscriber peak | Not published | About 250,000 (2000 to 2003) | 550,000 (end of 2004) |

## 4. Reading MMO history critically

Two habits will help you in the timeline project and the close readings.

**Separate the number from the claim.** "EverQuest was bigger than Ultima Online" is true by subscribers from the end of 1999. It may or may not be true by world size, and the sources do not tell us Ultima Online's per-shard figure. Write the claim at the level the evidence supports.

**Notice who is speaking.** Subscriber milestones come mostly from company press releases, published when the number is good. Declines are often reported by the press, or not at all. The absence of EverQuest concurrency figures, or EVE subscriber figures after 2014, is information about what the companies wanted known. A timeline built only from press releases will show a history of growth.

## In-class activity (25 min)

In groups of three, audit one number.

1. Each group gets one claim card, for example "Ultima Online had 250,000 players," "EVE Online is the biggest MMO world," "Lineage had over three million subscribers," or "EverQuest had about 23 servers."
2. Find the original source of the number (follow the citation chain from a wiki to a press release, interview or contemporary article). Record the date, the publisher and the exact definition used.
3. Classify the number as `S`, `C` (peak or average) or `W`, and by who published it: the company, the press, or an estimate by someone else.
4. Rewrite the claim so it is accurate, dated and scoped. If it cannot be rescued, say why.
5. Add your audited point to the shared class timeline sheet.

Expected output: one rewritten claim with source, date, definition and classification. The class sheet feeds Lab 09.

## Common misconceptions

- **"More subscribers means a more crowded world."** Operators add shards as they grow. World size `W` can stay flat while subscribers rise tenfold.
- **"A concurrency ratio is a property of the genre."** It depends on pricing, time zones, the definition of a subscriber, and whether the figure is peak or average. Neverwinter Nights and Ultima Online differ by a factor of seven partly for these reasons.
- **"If a number is on a wiki, it's a fact."** It is a claim with a citation. Follow the citation and check the date and definition.
- **"Meridian 59 failed because it was small."** Its small worlds were a deliberate choice to prevent crowding, and its flat monthly fee became the industry standard. Being first and being biggest are different achievements.

## Check yourself

1. Ultima Online had 100,000 subscribers and 12,500 average concurrent users in December 1998. If its ratio stayed the same at 250,000 subscribers, what average concurrency would you expect? Why might the true figure differ?
2. EverQuest had 550,000 subscribers at its peak and more than 3,000 players per server. EVE had about 500,000 subscribers and 65,303 players in one world. Which game was "bigger"? Give an answer that uses two of the model's numbers.
3. Estimate EverQuest's peak server count assuming `r = 0.12` and `W = 3,500`. State your estimate as a sentence a careful historian could publish.
4. Explain how a flat monthly subscription changes the designer's incentives compared with hourly pricing. Name one EverQuest feature that fits the flat-fee incentive.
5. Ultima Online's Trammel split in 2000 did not change `S` or `N`. What did it change, and why might that have mattered more to players than adding shards?

<details>
<summary>Answers</summary>

1. `0.125 × 250,000 = 31,250`. The ratio can change with the player mix (more international players spread across time zones), pricing, the game's age and how "subscriber" was counted in 2000.
2. By subscribers, EverQuest (550,000 against about 500,000, 10% more). By world size, EVE (65,303 against more than 3,000, over twenty times as many in one world). "Bigger" must name its measure.
3. `C ≈ 0.12 × 550,000 = 66,000`; `N ≈ 66,000 / 3,500 ≈ 19`. For example: "Assuming about 12% of its 550,000 subscribers were online at peak and each server held about 3,500, EverQuest would have needed roughly 19 servers; the company did not publish the figure."
4. Hourly pricing rewards long sessions; a flat fee rewards renewal, so designers add goals that take months and ties that make leaving costly. Raids, which need a stable group of many players over weeks, fit this incentive.
5. It changed the rules each player lived under, and split each world's population into consenting and non-consenting PvP sub-worlds. Players who had quit because of player killing could return without leaving their friends' shard, which adding new shards would not have offered.

</details>

## Lab hook

[Lab 09, auditing MMO numbers for the timeline](../labs/lab09.md). You build a sourced dataset of at least 15 figures for three MMOs, classify each as `S`, `C` or `W` and by source type, produce two linked charts, and write a 500-word note on what the published record hides. The dataset becomes the MMO strand of your timeline project.

## Sources

- Wikipedia, "Habitat (video game)", accessed September 2026. Lucasfilm Games beta on Quantum Link in 1986.
- Wikipedia, "Neverwinter Nights (1991 video game)", accessed September 2026. March 1991 launch on AOL; server capacity from 50 players (1991) to 500 (1995); about 115,000 players and typically 2,000 in prime time near the end of its run in 1997; AOL's announced two-dollar hourly games channel.
- Wikipedia, "Meridian 59", accessed September 2026. Early online launch on 15 December 1995, commercial release on 7 October 1996, about 17,000 public beta players, parallel worlds of a few hundred people, the origin of "massively multiplayer" inside 3DO, the flat monthly subscription and the September 1996 Online Game Developer's Conference panel (via Next Generation), factions and player justice system.
- Ultima Online figures, each from the original report as cited in Wikipedia, "Ultima Online" (accessed September 2026), with archived copies at web.archive.org:
  - Geryk, B., "PC Gaming Graveyard: Jane's A-10 Warthog," GameSpot (archived August 2000). The Origin employee's pre-launch expectation of 15,000 subscribers at most.
  - IGN Staff, "Ultima's Population Reaches 100,000," IGN, 15 December 1998. 100,000 subscribers, average simultaneous count of 12,500.
  - GameDaily Staff, "Ultima Online Spring Promo," GameDaily, 11 March 1999. 120,000 subscribers (plotted at 1999-03).
  - Gentry, P., "UO Hits 150,000 Subscribers," CNET Gamecenter, 24 February 2000. 150,000 subscribers (plotted at 2000-02).
  - Ocampo, J., "EverQuest: 300,000 and Counting," CNET Gamecenter, 30 October 2000. Ultima Online at 250,000 subscribers (plotted at 2000-10).
  - Everingham, M., "Gaming Goes Global," PC Gamer US 8(7), July 2001, pp. 44-52. 240,000 subscribers, 64,000 of them in Japan (plotted at 2001-07).
  - Woodcock, B. S., MMOGChart subscription charts (mmogchart.com and mmodata.blogspot.com, archived July 2012). A compiled secondary series, not a company report: a peak of around 250,000 in July 2003 and around 100,000 in 2008 (the 2008 value is plotted at mid-year with a year-wide whisker).
  - Also from the Wikipedia article: launch on 24 September 1997; 1999 server openings in Japan, Europe and South Korea; Lord British's death in beta on 9 August 1997; Renaissance expansion in May 2000 and the Trammel and Felucca rulesets; Garriott and Koster roles.
- EverQuest figures, as cited in Wikipedia, "EverQuest" (accessed September 2026). Launch on 16 March 1999 and 10,000 subscribers after one day (Sony Online Entertainment milestone release); Asher, M., "Game Spin: On an EverQuest," CNET Gamecenter, 7 April 1999 (60,000 subscribers); "EverQuest or 'EverCrack'?", USA Today, 8 September 2000 (259,000 subscribers); Ocampo (2000) above for passing Ultima Online; Ivory, J. D. (2012), *Virtual Lives: A Reference Handbook*, ABC-CLIO, p. 154 (peak of 550,000 active subscribers by the end of 2004); server populations above 3,000 per server once visible at login (from the article, era of the original login screen); designers' MUD influences; 2011 Game Developers Choice Online Hall of Fame citation for guilds and raiding.
- EVE Online figures, each from CCP or the press at the time, as cited in Wikipedia, "Eve Online" (accessed September 2026):
  - CCP Manifest, "EVE's 6th birthday with 300,000 of your closest friends (and enemies)," eveonline.com news, 6 May 2009 (archived at web.archive.org/web/20090509080352/). More than 300,000 active subscriptions (plotted at 2009-05).
  - Guðmundsson, E., *Quarterly Economic Newsletter Q4 2010*, CCP (archived at web.archive.org/web/20110408190526/). 357,000 active subscriptions at the end of 2010 (plotted at 2010-12).
  - CCP press release on the 63,170 concurrent record of 23 January 2011 (eveonline.com press release 72, archived at web.archive.org/web/20110810190256/).
  - CCP developer post, "PCU Record Attempt and EVE Birthday" (EVE Online forums, May 2013, updated with the success), for 65,303 concurrent accounts on one server on 5 May 2013 and the Sunday pattern.
  - Macdonald, K., "EVE Online Passes Half a Million Subscribers," IGN, 28 February 2013. Over 500,000 subscribers.
  - Release on 6 May 2003, and CCP no longer publishing active subscription counts from 2014, from the Wikipedia article.
- Wikipedia, "Lineage (video game)", accessed September 2026. NCSoft's statement of more than three million subscribers at one point, mostly in Korea (undated in the article); a little under one million in April 2008.
- Wikipedia, "World of Warcraft", accessed September 2026. 10 million subscribers in January 2008, over 12 million on 7 October 2010, 5.6 million at the end of June 2015. Context only; week 10 covers it.
- Wikipedia, "MUD1", accessed September 2026. 1978 origin, Trubshaw and Bartle.
- Bartle, R. (2003). *Designing Virtual Worlds*. New Riders. Free PDF edition from the author, mud.co.uk/richard/DesigningVirtualWorlds.pdf (chapter 1 is pp. 1-107). Chapter 1.

## Interactive spec: examples/w09-mmo-peaks-timeline.html

**Insight the visual must make obvious:** the business view (subscribers) and the world view (players sharing one world at once) rank the same games differently. World of Warcraft dominates the first and is missing from the second; EVE Online is mid-sized in the first and towers over everything in the second. Most of the world view is blank because companies rarely published those numbers.

**Layout:** two stacked panels sharing one x axis (years 1990 to 2016), at every width. Top panel "Business view: subscribers (log scale)", bottom panel "World view: most players known in one world at once (log scale)". A details card beside the panels at 1280px, below them at 390px. A data table with every plotted point below everything.

**Top panel data (`S`, one series per game, points joined by lines within a game):**

| Game | Date | Value | Type |
|---|---|---|---|
| Ultima Online | 1998-12 | 100,000 | dated report |
| Ultima Online | 1999-03 | 120,000 | dated report |
| Ultima Online | 2000-02 | 150,000 | dated report |
| Ultima Online | 2000-10 | 250,000 | dated report |
| Ultima Online | 2001-07 | 240,000 | dated report |
| Ultima Online | 2003-07 | 250,000 (peak, "around") | dated report |
| Ultima Online | 2008-01 | 100,000 ("around", year only) | dated report |
| EverQuest | 1999-03 | 10,000 | dated report |
| EverQuest | 1999-04 | 60,000 | dated report |
| EverQuest | 2000-09 | 259,000 | dated report |
| EverQuest | 2003-06 | 500,000 ("over", year only) | dated report |
| EverQuest | 2004-12 | 550,000 (peak) | dated report |
| Eve Online | 2009-05 | 300,000 | dated report |
| Eve Online | 2010-12 | 357,000 | dated report |
| Eve Online | 2013-02 | 500,000 ("over") | dated report |
| World of Warcraft | 2008-01 | 10,000,000 | dated report |
| World of Warcraft | 2010-10 | 12,000,000 | dated report |
| World of Warcraft | 2015-06 | 5,600,000 | dated report |

Points whose date is known only to the year (UO 2008, EQ 2003) are drawn at mid-year with a horizontal whisker spanning the year. Lineage is drawn as a flagged horizontal band at 3,000,000 spanning 1998 to 2008 with a dashed outline and the label "undated company claim: more than 3 million at one point", plus one solid point at 2008-04, 1,000,000 ("a little under"). Add a vertical marker at 2014-01 on the EVE line labelled "CCP stops publishing subscriber counts".

**Bottom panel data (`W`):**

| World | Date | Value | Type |
|---|---|---|---|
| Neverwinter Nights (AOL) | 1991-03 | 50 (server cap) | dated report |
| Neverwinter Nights (AOL) | 1995-06 | 500 (server cap, year only) | dated report |
| Meridian 59 | 1996-10 | band 200 to 500, labelled "a few hundred" | dated report |
| EverQuest | 2002-06 | 3,000 ("more than", era of login-screen counts; whisker 1999 to 2004) | dated report |
| Eve Online | 2011-01-23 | 63,170 | dated report |
| Eve Online | 2013-05-05 | 65,303 | dated report |

For Ultima Online, Lineage and World of Warcraft, draw a small hollow marker on the panel's baseline at launch year with the label "not published".

**Estimate layer (toggle "Show model estimates", default off):** adds a hollow EverQuest point to the bottom panel's companion readout and a hollow point in a third mini-row "Estimated total concurrency `C`" under the top panel: `C = r × 550,000` at 2004-12, and the estimated server count `N = C / W` with `W` from a slider. Estimates are always hollow and labelled "model estimate".

**Controls:**
- "Show model estimates" toggle.
- `r` slider 0.05 to 0.20, step 0.005, default 0.125.
- `W` slider 1,000 to 5,000, step 100, default 3,000.
- Game filter checkboxes (all on by default).
- "Linear scale" toggle for the top panel (default off), so students can see World of Warcraft flatten everything else.
- Clicking or focusing any point opens the details card: game, date, value, series (`S` or `W`), type, and the one-line source text from the lecture's Sources section.

**Formulas:** `r = C / S`, `W = C / N`, `N = r × S / W`. Estimated `C = r × 550,000`; estimated `N = C / W`, shown to one decimal and rounded to the nearest whole number in the label.

**Readout (always visible):** the two computed ratios from the lecture, "Ultima Online, Dec 1998: r = 12,500 / 100,000 = 0.125 (average)" and "EVE Online, 2013: r = 65,303 / 500,000 = 0.131 (peak)", plus "EVE world ÷ EverQuest server = 65,303 / 3,000 = 21.8". With estimates on, show `C` and `N`.

**Test values:** `r = 0.10`, `W = 3,000`: `C = 55,000`, `N = 18.3`. `r = 0.125`, `W = 3,000`: `C = 68,750`, `N = 22.9`. `r = 0.15`, `W = 3,000`: `C = 82,500`, `N = 27.5`. `r = 0.12`, `W = 3,500`: `C = 66,000`, `N = 18.9`.

**Encoding rules:** marker shape encodes type (filled circle = dated report, hollow circle = model estimate, dashed band = undated claim, hollow baseline marker = not published), so type does not rely on colour. Series colours come from the palette tokens. Text labels only; no logos, box art or screenshots. Respect `prefers-reduced-motion` for any transitions.
