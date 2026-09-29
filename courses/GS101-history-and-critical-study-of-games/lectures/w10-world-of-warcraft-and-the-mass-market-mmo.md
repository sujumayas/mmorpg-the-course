# GS101 · Week 10 — World of Warcraft and the mass-market MMO

**Why this matters:** Before 2004, an online world with half a million paying players was a huge success. Within six years World of Warcraft passed 12 million. That jump reset what publishers expected from online games, and most MMO design since has been a reaction to it. This week you learn what changed, how to measure "bigger" without being fooled by the numbers companies publish, and how to read a design as a response to its market.

**You will be able to:**
- Place Ultima Online, EverQuest and World of Warcraft on a timeline with dated, sourced peak figures, and compute the size ratios and growth factors between them.
- Read MMO population figures on a logarithmic scale and explain why a linear chart hides most of the history.
- Distinguish subscribers, concurrent users and registered accounts, and convert between the first two with stated assumptions about play time.
- Critique a claim such as "WoW was the biggest MMO ever" by naming the metric, its definition and what it leaves out.

**Before class:** Richard Bartle, *Designing Virtual Worlds* (New Riders, 2003), chapter 1, "The Fifth Age: 1997-Present" (pp. 23-43 in the author's free PDF edition at mud.co.uk/richard/DesigningVirtualWorlds.pdf), which you started in week 9. Tristan Donovan, *Replay: The History of Video Games* (Yellow Ant, 2010), the pages on online worlds (skim). The course reader lists the pages. Reread your notes on MUD1 from week 5.

**Prerequisites from earlier courses:** None formally. This lecture follows [GS101 week 5, text adventures and MUD1](w05-text-adventures-and-mud1.md) and [GS101 week 9, graphical MMOs](w09-graphical-mmos-meridian-59-ultima-online-everquest.md), whose subscriber, concurrency and world-size model (`S`, `C`, `r`, `W`) this lecture uses without re-teaching. If you are taking them alongside, [MA101 week 5, logarithms](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w05-logarithms-how-many-levels-until.md) covers the log scales used in section 3, and [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md) covers growth factors. The design side of this story returns in MMO301 week 5, "World of Warcraft: accessibility and the themepark" ([lecture](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w05-world-of-warcraft-accessibility-and-the-themepark.md)).

**Interactive:** [WoW growth curve, linear vs log](../examples/w10-wow-growth-curve.html). Keep it open during section 3, next to week 9's `examples/w09-mmo-peaks-timeline.html`.

---

## 1. The world before World of Warcraft

By 2003 the graphical MMO had a settled shape. You met its founders last week. Recall one fact from Ultima Online (1997): its May 2000 Trammel split, covered in week 9, was one of the first large-scale admissions that most paying players did not want to be prey. That lesson matters for what Blizzard did next.

EverQuest (Sony Online Entertainment, 16 March 1999) came out of a different lineage. Its creators have said their shared experience of MUDs such as Sojourn and TorilMUD inspired it. Players roamed the world of Norrath fighting monsters for treasure and experience, with quests as a further source of both. It passed Ultima Online in subscriptions by the end of 1999 and reached an active subscriber peak of 550,000 by the end of 2004. Individual EverQuest servers showed peaks of more than 3,000 players each.

Those are the figures to hold in your head. In the early 2000s, **a successful Western MMO had a few hundred thousand subscribers**, and they were a particular kind of player: comfortable with a PC, a fast connection, and a game that asked for hours at a time.

## 2. What World of Warcraft changed

Blizzard Entertainment released World of Warcraft in North America on 23 November 2004, ten years after the first Warcraft game, and in Europe on 11 February 2005. Blizzard already had a large audience from its strategy games. Warcraft III, released in July 2002, had filled the world with characters and places that players already knew.

Several of WoW's design decisions made the game easier to start and easier to keep playing in short sessions. Each one is a response to a barrier in the earlier games. Read them as history. Every one of these features has since been copied so widely that it is easy to forget it was ever a choice.

**Quests as the main path.** WoW's levelling was organized around quests given by non-player characters: kill a number of creatures, gather items, find an object, deliver something. A new player always had a next task with a stated goal. EverQuest offered quests too, but there they were one source of experience beside fighting monsters. In WoW they were the spine of the levelling path.

**Rest instead of penalty.** WoW's "rested" system gives a bonus to experience from kills after a player has been away from the game, and it builds up while a character is logged off in an inn or a city. According to Warcraft Wiki, Blizzard's first design during testing *cut* experience by 50% after a few hours of play, and testers rejected it. The rested bonus delivers the same pacing, but framed as a reward for stepping away instead of a punishment for staying. The underlying numbers barely differ. The feeling differs completely.

**A lighter death.** When a WoW character dies, it becomes a ghost at a nearby graveyard and must run back to its body to revive. Equipped items lose 10% of their maximum durability. A player who cannot reach the body can use a "spirit healer" at the graveyard instead, at the cost of further item damage and "resurrection sickness," a temporary weakness lasting up to ten minutes depending on level. Death costs time and some gold for repairs, never the character's progress.

**Modest hardware requirements.** The original minimum memory requirement was 256 MB of RAM, raised to 512 MB in a later patch of the original game. Blizzard's stylized art style asked less of a machine than a push for realism would have.

**Several regions, several business models.** WoW launched in several regions, each with its own operator or billing. In China, players in internet cafés could buy hourly and daily time cards, a different model from the Western monthly subscription. That decision matters when you read the subscriber numbers below.

The subscription price stayed at US$15 for a month, where it has remained since the 2004 launch.

None of this means WoW was "easy." Its end-game raids asked large groups to coordinate for hours. What changed was the *slope* of the first hours. A new player could log in for 45 minutes, finish two quests and log out with visible progress. That is what "mass market" means in design terms. The game was built for people who had not played an MMO before.

## 3. Worked example: how big was World of Warcraft?

Week 9's timeline explorer put Ultima Online, EverQuest and EVE Online on one chart and separated subscribers from players sharing one world. This example zooms in on the one line that dwarfs the rest of that chart, and asks what its shape and its definition tell you.

### The hook

On 7 October 2010 Blizzard announced that World of Warcraft's subscriber base now exceeded 12 million players worldwide. EverQuest, the biggest Western MMO before it, peaked at 550,000. Plot both on an ordinary chart and EverQuest is a line along the bottom. Was WoW simply a bigger version of the same thing, or was it a different kind of thing? And is "12 million" even the same kind of number as "550,000"?

### The model, stated once

Two small models do all the work. The second one you already have from week 9.

**Growth factors and log distance.** The size gap between two figures `a` and `b` is the ratio `b / a`. On a logarithmic axis, position is `log10(value)`, so the distance between two points is `log10(b / a)`. Equal ratios look like equal distances, and one step of 1.0 is a factor of 10. When two figures are `n` months apart, the average monthly growth factor is `(b / a)^(1/n)`. A straight line on a log chart means a constant growth factor. A line that bends flatter means growth is slowing, even while the absolute numbers still climb.

**What the number counts.** Week 9 defined `S` (subscribers), `C` (concurrent users) and the concurrency ratio `r = C / S`. Add a third kind of figure, **registered accounts**: every account ever created, including those that played once and left. Registered accounts can only grow. Neither `S` nor `C` can be recovered from them without knowing what share of accounts are still active, which companies rarely publish.

One more way to read `r` helps with games that publish only a concurrent figure. If an average subscriber plays `h` hours a day and the busiest hour has `f` times the average number of players online, then:

```
peak r  ≈  (h / 24) × f
```

With `h = 2` and `f = 1.5`, `r = 0.125`, the same ratio week 9 computed from Ultima Online's 1998 figures. Using `r`, you can turn a concurrent figure into an implied subscriber range, as long as you state your `h` and `f`.

### Numbers you can check

Start with subscriber peaks, the one metric the three landmark games share.

| Game | Peak subscribers | When | Ratio to UO | `log10(peak)` |
|---|---|---|---|---|
| Ultima Online | about 250,000 | 2003 | 1× | 5.40 |
| EverQuest | 550,000 | end of 2004 | 2.2× | 5.74 |
| World of Warcraft | over 12,000,000 | October 2010 | 48× | 7.08 |

EverQuest was 2.2 times Ultima Online's peak. WoW was `12,000,000 / 550,000 ≈ 21.8` times EverQuest's. On the log axis, the step from UO to EQ is `5.74 − 5.40 = 0.34`, and the step from EQ to WoW is `7.08 − 5.74 = 1.34`, almost four times as long. WoW was not the next step of a steady climb. It was a jump of more than a factor of ten after a step of about a factor of two.

Now the growth itself, from Blizzard's own milestones. The last three columns are computed from the first two.

| Date | Subscribers | Months since previous | Growth factor | Monthly factor | Subscribers added per month |
|---|---|---|---|---|---|
| December 2004 | 400,000 | — | — | — | — |
| March 2005 | 1,500,000 | 3 | 3.75 | 1.554 | 366,667 |
| June 2005 | 3,250,000 | 3 | 2.17 | 1.294 | 583,333 |
| December 2005 | 5,600,000 | 6 | 1.72 | 1.095 | 391,667 |
| January 2007 | 8,000,000 | 13 | 1.43 | 1.028 | 184,615 |
| January 2008 | over 10,000,000 | 12 | 1.25 | 1.019 | 166,667 |
| December 2008 | 11,500,000 | 11 | 1.15 | 1.013 | 136,364 |
| October 2010 | over 12,000,000 | 22 | 1.04 | 1.002 | 22,727 |

Check one row by hand. From June to December 2005, `5,600,000 / 3,250,000 ≈ 1.723`, and `1.723^(1/6) ≈ 1.095`, so subscribers grew about 9.5% a month. The absolute gain was `2,350,000 / 6 ≈ 391,667` a month.

The two right-hand columns tell different stories. The monthly growth factor fell in every period, from 55% a month in the first quarter to 0.2% a month by 2010. The number of subscribers added per month peaked in the spring of 2005 and stayed above 130,000 a month into 2008. A linear chart shows the second story, with the line still climbing steeply in 2007. A log chart shows the first, with the curve bending flat from its first months. Both are true. Which one you draw decides what your reader thinks happened.

In its first year WoW grew from 400,000 to 5.6 million, a factor of `5.6 / 0.4 = 14`. Within four months of its North American launch, it had passed EverQuest's all-time peak.

The reported series continues downward after the peak: over 10 million in November 2014 (after the Warlords of Draenor expansion, up from 7.4 million), 5.6 million at the end of June 2015 and 5.5 million at the end of September 2015. In November 2015 Blizzard announced it would stop publishing regular subscriber updates. The reported line ends there.

### What "subscriber" meant

Before you plot 12 million next to 550,000, read Blizzard's definition. Blizzard's press releases in this period counted as a subscriber anyone who had paid a subscription fee, held an active prepaid card, or was inside the free month that came with buying the game. They also counted "Internet Game Room" players who had accessed the game in the last thirty days, and applied the same rules in licensees' territories. Free promotional accounts and expired subscriptions were excluded.

Now look at the January 2008 breakdown. Of the more than 10 million subscribers, Blizzard reported about 2 million in Europe, 2.5 million in North America and 5.5 million in Asia. More than half (`5.5 / 10 = 55%`) were in Asia, where many players bought time by the hour in internet cafés. Under Blizzard's definition, a café player who logged in once in thirty days counted the same as a player paying monthly at home. That does not make the figure false. It makes it a different quantity from EverQuest's mostly Western monthly subscribers. A careful sentence says "over 12 million subscribers, as Blizzard defined them, more than half of them in Asia in 2008."

### A visual you can move

Open `examples/w10-wow-growth-curve.html`. The left panel plots WoW's milestones with Ultima Online's and EverQuest's peaks as reference lines. Toggle the y-axis between linear and log. On the linear axis the pre-2004 games lie flat along the bottom and WoW's line still climbs steeply in 2007. Switch to log, and the earlier games become visible steps while WoW's curve visibly bends flat within its first year. The right panel shows the same data as two bar series per period, monthly growth factor and subscribers added per month, so you can see one fall while the other stays high. Both panels sit on the first tab, "Curve and rates." The second tab, "What 10 million was made of," stacks the January 2008 figure by region.

### Cross-game recognition

Other landmark games publish different metrics. Rewrite each into week 9's quantities and see what it can and cannot say.

**EVE Online (CCP Games).** On 5 May 2013, EVE recorded 65,303 accounts logged in at once, breaking its previous record of 63,170 from 23 January 2011. Week 9 paired this peak `C` with EVE's roughly 500,000 subscribers to get `r ≈ 0.131`. Read through `r ≈ (h / 24) × f`, that is `h × f ≈ 3.1` hours, for example two hours a day with a peak hour about 1.6 times the average. The record also makes a point WoW's numbers cannot. Every one of those accounts was on the same server, while WoW realms each held several thousand players. "How many play the game?" and "how many share one world?" are different questions, as week 9 showed.

**Old School RuneScape (Jagex).** GameSpot reported a peak of 241,016 concurrent players on 3 August 2025, a record Jagex confirmed without publishing its own figure. There is no published subscriber count to pair it with. With an assumed `r = 0.125` (`h = 2`, `f = 1.5`), `S ≈ 241,016 / 0.125 ≈ 1.93 million` active accounts. With `h = 3`, `r = 0.1875` and `S ≈ 1.29 million`. The answer depends entirely on your assumptions, so state them. Notice the sourcing too: a press outlet's count that the company confirmed.

**Final Fantasy XIV (Square Enix).** Square Enix reported 30 million lifetime registered players by January 2024. This is a **registered-account** figure. It can only grow, even when the game is shrinking, and neither `S` nor `C` can be recovered from it. On the log axis it would sit above WoW's subscriber peak (`log10(30,000,000) = 7.48` vs 7.08). Drawing it on the same line would claim Final Fantasy XIV was 2.5 times bigger than WoW at its peak. Nothing in the data supports that claim.

Three games, three metrics, one lesson. Before comparing any two MMO numbers, write down what each counts, and convert only with stated assumptions.

### Design judgment

What should a historian or a designer take from this?

- **Use subscriber peaks for the era they describe.** From 1997 to about 2012, the subscription model gives a comparable metric for Western MMOs. It breaks down once games go free-to-play (week 11), because "subscriber" stops meaning "player."
- **Choose the scale for the question.** A log chart shows growth rates and makes earlier games visible. A linear chart shows absolute gains. For a population history, draw the log chart and quote the absolute numbers in the text. Always say which scale you used.
- **Treat company figures as announcements, not measurements.** Blizzard published milestones when they were good news and stopped when the trend turned down. That is normal corporate behavior, and it means the record has a shape shaped by marketing. Note gaps in your timeline rather than filling them.
- **For designers, the bigger number is not the only goal.** WoW's accessibility decisions (quests, rest, light death) brought in millions of new players. The same decisions made the world less dangerous and less dependent on other players than Ultima Online or EverQuest. Blizzard's own WoW Classic, released on 26 August 2019 as a recreation of the game at patch 1.12, shows that a large audience still wanted the older, slower version. Decide which players your world is for before you decide how to measure it.

### Check yourself (worked example)

1. On a log10 axis, how far apart are 400,000 (WoW, December 2004) and 5,600,000 (December 2005)? What growth factor does that distance represent, and what was the average monthly growth factor over those 12 months?
2. A new MMO reports a peak of 90,000 concurrent players. Its players average 1.5 hours a day, and the peak hour is 1.8 times the daily average. Compute `r` and estimate its subscribers. What happens to the estimate if average play time is 3 hours?
3. A classmate's chart shows Final Fantasy XIV's 30 million next to WoW's 12 million under the heading "Biggest MMOs." Write the two-sentence correction.

<details>
<summary>Answers</summary>

1. `log10(5,600,000) − log10(400,000) = log10(14) ≈ 1.15`. The distance is a growth factor of 14 in one year, or `14^(1/12) ≈ 1.246`, about 25% a month on average.
2. `r ≈ (1.5 / 24) × 1.8 = 0.1125`, so `S ≈ 90,000 / 0.1125 = 800,000`. At 3 hours a day, `r = 0.225` and `S ≈ 400,000`. Doubling play time halves the implied population, which shows how much the estimate depends on the assumption.
3. The 30 million is a lifetime count of registered accounts (Square Enix, January 2024), while the 12 million is Blizzard's count of current subscribers in October 2010, so the two numbers measure different things. To compare the games, you would need the same metric for both, such as active subscribers in the same year.

</details>

## 4. After the peak

WoW's subscriber history after 2010 is a story of expansions and declines. Each expansion (The Burning Crusade in 2007, Wrath of the Lich King in 2008, Cataclysm in 2010, then Mists of Pandaria, Warlords of Draenor and later ones) brought players back for a while. Warlords of Draenor lifted subscriptions from 7.4 million to over 10 million in November 2014. By the end of June 2015 the figure was 5.6 million, the lowest since 2005. Then Blizzard stopped reporting.

For the rest of the industry, WoW's success had two effects you will meet again. First, WoW set the bar every subscription MMO was measured against. Several that could not hold a subscriber base, including Dungeons & Dragons Online and The Lord of the Rings Online, later added free-to-play options, which is where week 11 begins. Second, WoW became the reference point for MMO design. Its conventions (quests as the levelling path, instanced dungeons for small groups, raids at the level cap) became what players expected, and later designers had to justify every departure from them. In MMO301 you will study this as the "themepark" model and its alternative, the "sandbox."

## 5. Reading WoW critically

Put WoW through week 1's close-reading method, briefly.

- **Describe before you judge.** Name the version. "WoW" in 2005, in 2010 and today are three different games. WoW Classic exists because the difference matters.
- **Find the machine.** Pick the rested system. Compute what it does: kills give double experience while rested, and rest builds up while logged off. The machine turns time away from the game into faster progress on return.
- **Name the experience.** The rested bonus reframes a limit on play as a gift. Compare it with Papers, Please in week 12, where rules make you feel the cost of a system. Here the rules hide a cost.
- **Place it in context.** A subscription business earns the same fee whether you play two hours a week or twenty. It profits from players who stay subscribed, not from players who play the most, so it has a reason to make short sessions satisfying.
- **Make one claim.** For example: "WoW's rested system turned a pacing limit into a reward, and that change in framing, more than any new mechanic, is what let casual players stay subscribed." A reader can dispute that, and you can support it with the beta history and the subscriber curve.

## In-class activity (25 min)

In groups of three. Materials: the tables in section 3, squared paper, and a laptop per group.

1. (8 min) Each person picks one MMO not covered in this lecture (for example Lineage, RuneScape, Star Wars: The Old Republic, Guild Wars 2 or The Elder Scrolls Online). Find one published population figure for it. Record the number, the metric type, the date and the source.
2. (7 min) Put your three figures and WoW's October 2010 peak on one hand-drawn log axis (one decade per 3 cm). Convert any concurrent figure to an implied subscriber range with `r = (h / 24) × f`, using `h` from 1 to 3 hours and `f = 1.5`.
3. (5 min) Write one sentence per figure that states what it counts, in the style "over 12 million subscribers, as Blizzard defined them."
4. (5 min) Decide as a group which of your three figures you would refuse to put on a single comparative chart, and why.

Expected output: three sourced rows (value, metric, date, source), the conversions, the three sentences, and the rejected comparison with a reason.

## Common misconceptions

- **"WoW grew the same way earlier MMOs did, only more."** On a log scale the earlier steps were about a factor of two each. WoW's was more than a factor of 20 over EverQuest's peak, and it passed that peak within months.
- **"A subscriber is a player who pays every month."** Under Blizzard's definition, it included players in the free month after buying the game and internet-café players who logged in once in thirty days.
- **"Registered accounts show a game's size."** They show everyone who ever signed up. They can only grow, even while the active population falls.
- **"WoW was successful because it was easy."** Its end game was demanding. Its success came from making the first hours and short sessions rewarding, which widened who could start.

## Check yourself

1. EverQuest's peak was 550,000 and Ultima Online's about 250,000. How many times larger was WoW's October 2010 figure than the two combined?
2. Using the milestone table, compute the growth factor from December 2004 to March 2005 and from March 2005 to June 2005. Both periods are three months long. What does the difference tell you?
3. An MMO with 400,000 subscribers has players averaging 2.5 hours a day and a peak factor of 1.6. Compute `r` and estimate its peak concurrent users. If all of them share one server, how does that compare with EVE's 2013 record?
4. Explain in two sentences why Blizzard's decision to stop publishing subscriber numbers in November 2015 matters for anyone drawing a timeline of MMO populations.

<details>
<summary>Answers</summary>

1. Combined: 800,000. `12,000,000 / 800,000 = 15` times.
2. December 2004 to March 2005: `1,500,000 / 400,000 = 3.75`. March to June 2005: `3,250,000 / 1,500,000 ≈ 2.17`. Subscribers were still growing fast, but the growth factor was already falling. That is normal as a product reaches more of its possible audience, and it is easier to see on a log scale, where the line's slope drops.
3. `r ≈ (2.5 / 24) × 1.6 ≈ 0.1667`, so `C ≈ 0.1667 × 400,000 ≈ 66,667`. That is slightly above EVE's record of 65,303, so it would be a new record for players in one shared world.
4. Any line after 2015 must stop or switch to estimates from other sources, and estimates are not the same kind of evidence as the company's own counts. A chart that continues the line without marking the change hides a change of source.

</details>

## Lab / assignment hook

This week extends [Lab 09, auditing MMO numbers for the timeline](../labs/lab09.md), which is due at the start of week 12. Add World of Warcraft to your dataset: at least six subscriber milestones from this lecture's table, each with its source, plus Blizzard's subscriber definition quoted as a short phrase and paraphrased in full. Add one chart pair (linear and log) of WoW's growth and two sentences on what each view shows. This becomes the WoW entry of your timeline project (25%).

## Sources

- Blizzard Entertainment press release, "World of Warcraft Subscriber Base Reaches 12 Million Worldwide," Irvine, 7 October 2010 (archived by the Wayback Machine from us.blizzard.com). The 12 million figure.
- Blizzard Entertainment press release, "World of Warcraft Subscriber Base Reaches 11.5 Million Worldwide," dated 23 December 2008 in its text (archived by the Wayback Machine). The 11.5 million figure and Blizzard's definition of a subscriber, paraphrased here.
- Warcraft Wiki, "World of Warcraft" (subscriber timeline, including 400,000 in December 2004, 1.5 million March 2005, 3.25 million June 2005, 5.6 million December 2005, 8 million January 2007; the November 2015 end of regular updates), "Rested" (double experience from kills; accrual while logged off in inns and cities; the rejected 50% penalty tested in beta) and "Durability" (10% of maximum durability lost on death).
- Warcraft Wiki, "Game time" (page "Subscription"), and Colp, T. (22 March 2024), *PC Gamer*. US$15 monthly price unchanged since launch.
- Wikipedia, "World of Warcraft". Release dates (23 November 2004; Europe 11 February 2005); quest types; rested bonus; ghost, spirit healer and resurrection sickness; 256 MB minimum RAM at launch; hourly and daily cards in China; the January 2008 regional breakdown (Gamasutra, 22 January 2008); 7.4 million to over 10 million in November 2014 (Forbes, 19 November 2014); 5.6 million at end of June 2015; expansion years.
- Wikipedia, "World of Warcraft Classic". Released 26 August 2019, recreating patch 1.12.
- Wikipedia, "Warcraft III: Reign of Chaos". July 2002 release.
- Wikipedia, "EverQuest". Release 16 March 1999; creators' MUD influences; passed Ultima Online in subscriptions by end of 1999; active subscriber peak of 550,000 by end of 2004; server peaks above 3,000 players.
- Wikipedia, "Ultima Online". Release 24 September 1997; peak of about 250,000 subscribers in 2003 (the article gives both February and July 2003); unrestricted player combat; Renaissance expansion's Trammel and Felucca split in May 2000.
- Wikipedia, "Eve Online". 65,303 concurrent accounts on 5 May 2013; previous record 63,170 on 23 January 2011; over 500,000 subscribers in February 2013.
- Wikipedia, "Old School RuneScape". 241,016 concurrent players on 3 August 2025, as reported by GameSpot and confirmed by Jagex.
- Wikipedia, "Final Fantasy XIV". 30 million registered players by January 2024.
- Wikipedia, "Massively multiplayer online role-playing game". WoW realms housing several thousand players each.
- Bartle, R. (2003). *Designing Virtual Worlds*. New Riders. Free PDF edition from the author, mud.co.uk/richard/DesigningVirtualWorlds.pdf (chapter 1 is pp. 1-107).
- Donovan, T. (2010). *Replay: The History of Video Games*. Yellow Ant, East Sussex (xiv + 501 pp.).

## Interactive spec: examples/w10-wow-growth-curve.html

**Purpose.** Show that the same WoW subscriber data tells two true stories: on a linear axis the line keeps climbing steeply for years, while on a log axis the growth rate falls from the first months. Also show WoW's peak against Ultima Online's and EverQuest's, and what the January 2008 figure was made of. This example complements week 9's `w09-mmo-peaks-timeline.html` (which separates subscribers from world size); do not duplicate its world-size panel. Insight on first load: *linear axis, WoW's line rising steeply through 2007, with a prominent "log scale" toggle; beside it, the monthly-growth-factor bars already falling from the first bar.*

**Layout.** Left (top on mobile): the curve. Right (below on mobile): the rates panel. A tab bar with "Curve and rates" (default) and "What 10 million was made of". A data table toggle under everything. No game logos, box art or screenshots; generic markers and text labels only.

**Data (exact; every point carries its source label for the tooltip).**

| id | series | date | value | source label |
|---|---|---|---|---|
| w1 | WoW | 2004-12 | 400000 | Warcraft Wiki |
| w2 | WoW | 2005-03 | 1500000 | Warcraft Wiki |
| w3 | WoW | 2005-06 | 3250000 | Warcraft Wiki |
| w4 | WoW | 2005-12 | 5600000 | Warcraft Wiki |
| w5 | WoW | 2007-01 | 8000000 | Warcraft Wiki |
| w6 | WoW | 2008-01 | 10000000 | Blizzard via Gamasutra ("more than") |
| w7 | WoW | 2008-12 | 11500000 | Blizzard press release |
| w8 | WoW | 2010-10 | 12000000 | Blizzard press release ("exceeds") |
| w9 | WoW | 2014-11 | 10000000 | Forbes via Wikipedia ("over") |
| w10 | WoW | 2015-06 | 5600000 | Wikipedia |
| w11 | WoW | 2015-09 | 5500000 | Warcraft Wiki |
| uo | reference | 2003-07 | 250000 | Wikipedia, Ultima Online (peak, "about") |
| eq | reference | 2004-12 | 550000 | Wikipedia, EverQuest (peak) |

Draw UO and EQ as horizontal dashed reference lines labelled with name and value. Draw a vertical marker at 2015-11 labelled "Blizzard stops reporting". Draw the post-peak points (w9 to w11) in the same series but with a gap between w8 and w9 (no published points 2011 to 2014 in this dataset), rendered as a dotted segment labelled "no data in this set".

**Curve panel controls.** Scale toggle linear / log10 (default linear). Log ticks at 10^5, 10^6, 10^7 with labels 100k, 1M, 10M. "Compare two points" mode: select two points to show ratio `b/a`, log distance `log10(b/a)`, months between, and monthly factor `(b/a)^(1/n)`.

**Rates panel.** For each consecutive pair among w1 to w8, two bars side by side: monthly growth factor minus 1, as a percentage (left axis), and subscribers added per month (right axis). Label each bar pair with its period. Hovering or focusing a bar highlights the matching segment on the curve.

**Composition tab.** A single stacked bar for January 2008: Asia 5.5M, North America 2.5M, Europe 2.0M, with percentages (55%, 25%, 20%). Beside it, Blizzard's subscriber definition paraphrased in three bullet points (paid or prepaid; free month after purchase; Internet Game Room players active in the last 30 days), and "excluded: free promotions, expired or cancelled accounts".

**Test values.**
- Monthly factors and adds per month, w1 to w8: 1.554 / 366,667; 1.294 / 583,333; 1.095 / 391,667; 1.028 / 184,615; 1.019 / 166,667; 1.013 / 136,364; 1.002 / 22,727.
- Ratios: EQ/UO = 2.2; w8/EQ = 21.82; w8/UO = 48.0; w4/w1 = 14.0, log distance 1.146, monthly factor over 12 months 1.246.
- Log positions: UO 5.398, EQ 5.740, w8 7.079.
- Composition: 5.5 / 10 = 55%.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. The two bar series differ by fill pattern as well as color; reference lines are dashed and labelled in text. Tooltips also appear on keyboard focus. Respect reduced motion (no animated axis transitions when it is set).
