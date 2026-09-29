# MMO406 · Week 04 — History and Timelines

**Why this matters:** A persistent world gets new story every few months for a decade. Every one of those updates lands on a date in your fictional calendar, and the rule you choose for how that calendar moves decides whether characters can age, whether wars can end, and whether a new player walking into your oldest zone is visiting the present or the past. Most teams never choose this rule. They inherit it from the first expansion that needed a date.

**You will be able to:**
- Compute a world's in-fiction span, event density and character ages after any number of real years, from its lore clock (drift rate and expansion jumps).
- Show that the span a world gains is exactly the "time gap" a new player feels in launch content, and use that to argue for a clock policy.
- Convert dates between two in-world calendars and explain what a calendar's epoch says about the culture that uses it.
- Design a three-era history with a precision gradient, content hooks per era, and reserved gaps for future expansions.

**Before class:** Wolf, *Building Imaginary Worlds* (2012), chapter 3, the section on the structures of time and timelines (roughly 12 pages; use the contents page). Guild Wars 2 Wiki, "Timeline" (skim the table from 1320 AE to the present, 10 minutes). UESP, "Lore:Second Era" (scroll to the entries dated 2E 582 and read the notes, 10 minutes).

**Prerequisites from earlier courses:** [MMO301 week 12, persistence and time](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w12-persistence-and-time-what-should-last.md) covered the day-scale clock (Eorzea time, accelerated days, why nobody ages) and the rule that only real-world dates carry feelings. This week works at the scale of years and expansions and does not repeat that material. [GD202 week 1, story vs narrative vs plot](../../GD202-narrative-and-quest-design/lectures/w01-story-vs-narrative-vs-plot.md) separated the order events happened in from the order the player learns them. [GD202 week 13, shared vs personal story](../../GD202-narrative-and-quest-design/lectures/w13-shared-vs-personal-story.md) priced phasing, which is one way to show two dates in one place. From this course, [week 1, setting as system](w01-setting-as-system.md), [week 2, geography](w02-geography-and-ecology.md) and [week 3, factions](w03-factions-and-conflict.md) give you the places and groups this week's history has to explain.

**Interactive:** [Lore clock](../examples/w04-lore-clock.html). Keep it open during section 2.

---

## 1. History is the part of the setting players stand on

Your setting's history does three jobs, and only one of them is telling players what happened.

First, history explains the present. Why is the river border fortified? Why do the hill clans refuse to trade with the coast? A present with no history reads as arbitrary, and players notice. Week 3's factions need grudges. Grudges need events.

Second, history makes content. A war five hundred years ago leaves ruins, and ruins become dungeons. A plague leaves a quarantined district. An empire that fell leaves roads that go nowhere, which gives level designers a reason for a path through the hills. When you write history for an MMO, you are also writing the list of places your content team will build for the next ten years.

Third, history is a promise about the future. A timeline that stops at "now" tells your players nothing is coming. A timeline with a dark century nobody talks about, or a sealed city whose fall is described in two contradictory sentences, tells them there is more. Players read gaps as hooks.

A **timeline** is the ordered list of events that make up this history, each with a date. An **epoch** is the event a calendar counts from, the year zero. A **chronology** is the whole system of calendars, their epochs, and the rules for converting between them.

This week has one model, the lore clock, which governs the part of the timeline that is still being written, the years after launch. Then it turns to the part you write before launch, the deep past.

## 2. Worked example: the lore clock

### The hook

The Elder Scrolls Online launched in April 2014, set in the year 2E 582 of Tamriel's calendar. Over the next five years the game shipped a long run of zones and chapters: Orsinium, the Gold Coast, Vvardenfell, Clockwork City, Murkmire, Elsweyr and more. Dragons returned. Daedric princes were thwarted. Kings died. UESP's timeline still dates nearly all of it to 2E 582.

In 2019 the game's loremaster, Leamon Tuttle, explained why. His argument was that time in the game is personal to each player, because different players play the content in different orders. So the team resisted moving the calendar to 2E 583 and treats all of it as happening in one year. By 2019, one of the busiest years in the history of any fictional world contained five real years of releases.

Guild Wars 2 made a different choice without quite meaning to. It launched in August 2012 in 1325 AE. Its wiki's timeline now runs to 1339 AE, with each expansion and Living World season landing a year or so later than the one before. The same wiki notes that ArenaNet's narrative team once tried to keep the in-game calendar synced with real time and gave that up, because releases were not continuous and some events could not plausibly last weeks.

EVE Online went the whole way. Its calendar counts years from the Yoiul Conference, and the conversion is a fixed offset. Add 1898 to the YC year to get the real year. EVE launched in YC105, which is 2003. In 2026 it is YC128 in New Eden and in the real world alike.

Three shipped games, three rules for how fictional time moves. Each rule has consequences you can compute.

### The model

Let `t` be real years since launch. The **lore clock** gives the in-world year:

```
w(t) = w0 + r × t + J × floor(t / T)
```

- `w0` is the in-world year at launch.
- `r` is the **drift rate**: in-world years that pass per real year of steady updates. `r = 0` freezes the calendar. `r = 1` ties it to real time.
- `J` is the **jump**: in-world years skipped when an expansion ships. Many story games open an expansion with "three years later".
- `T` is the expansion period in real years, so `floor(t / T)` counts the expansions shipped so far.

From the clock, three quantities follow.

```
span        S(t) = w(t) − w0
density     D(t) = E × t / max(S(t), 1)
NPC age     a(t) = a0 + S(t)
```

- `S` is how much in-world time the live game has covered.
- `E` is the number of **story beats** you ship per real year. A beat is any update that changes the world's story: a patch chapter, a seasonal arc, an expansion's main quest. `D` is then beats per in-world year. The `max(S, 1)` is a floor, since even a frozen world has one year to hold its events.
- `a0` is a character's age at launch and `a` is their age now.

The model assumes beats arrive at a steady rate and that in-world time between beats is spread evenly. Real release calendars are lumpier, but the totals come out the same.

### Numbers you can check

Take an invented game, *Thornmere*, launching in the year 1200 of its calendar. It ships six story beats per real year. Its young heir, Princess Ysolde, is 16 at launch. Here is where four clock policies leave it after ten real years (`t = 10`, 60 beats in total):

| Policy | r | J every T | Span S | Beats per in-world year D | Ysolde's age |
|---|---|---|---|---|---|
| Frozen | 0 | none | 0 | 60 | 16 |
| Slow drift | 0.25 | none | 2.5 | 24 | 18.5 |
| Real time | 1 | none | 10 | 6 | 26 |
| Stepped | 0 | 3 every 2.5 | 12 | 5 | 28 |

Check the stepped row. Four expansions ship in ten years (`floor(10 / 2.5) = 4`), each jumping three years, so `S = 12`. Sixty beats over twelve years is five per year. Ysolde is `16 + 12 = 28`.

This short script reproduces the table. It runs as shown with `.venv/bin/python`.

```python
from math import floor

def world_year(t, w0, r, J=0, T=None):
    """In-world year after t real years: steady drift r plus a jump J per expansion."""
    jumps = floor(t / T) if T else 0
    return w0 + r * t + J * jumps

policies = [
    ("Frozen",      0.0,  0, None),
    ("Slow drift",  0.25, 0, None),
    ("Real time",   1.0,  0, None),
    ("Stepped",     0.0,  3, 2.5),
]
t, beats_per_year, age0, w0 = 10, 6, 16, 1200
for name, r, J, T in policies:
    span = world_year(t, w0, r, J, T) - w0
    density = beats_per_year * t / max(span, 1)
    print(f"{name:11} span {span:5.1f}  beats/world-year {density:5.1f}  age {age0 + span:5.1f}")
```

```
Frozen      span   0.0  beats/world-year  60.0  age  16.0
Slow drift  span   2.5  beats/world-year  24.0  age  18.5
Real time   span  10.0  beats/world-year   6.0  age  26.0
Stepped     span  12.0  beats/world-year   5.0  age  28.0
```

### The same number, seen from the starting zone

Now look at the table from the point of view of a player who creates a character in real year 10.

They start at the beginning, in the launch zones, which were written for the year 1200. The world's present is `1200 + S`. So the new player's first hours take place `S` years before the world they will reach at the level cap. Call that the **time gap**. It is not a second quantity. It is the span again, seen from the other end.

```
time gap for a player starting at real year t = S(t)
```

In the frozen world the gap is zero. Ysolde is 16 in the tutorial and 16 at the cap, and the launch story and the newest patch happen in the same year. That is Tuttle's argument in one line. If the calendar never moves, content can be played in any order without anyone travelling in time.

In the stepped world the gap is twelve years. The new player meets a 16-year-old princess in the tutorial and a 28-year-old queen at the cap. The launch zone shows a war that ended a decade ago in world time. The town it burned has been rebuilt in the newest zone. The game is showing that player the past and calling it the present.

This is the insight the interactive is built to make obvious. **The span a world gains is the gap its old content opens.** Any clock that lets characters age, wars end and cities rebuild also turns the launch zones into a history lesson. You can shrink the gap only by shrinking the span, and then you are back to a crowded single year.

### A visual you can move

Open [`examples/w04-lore-clock.html`](../examples/w04-lore-clock.html). The top strip is the real release calendar: sixty evenly spaced beats over ten years, with expansion markers. The bottom strip is the in-world timeline. The same sixty beats are drawn at their in-world dates, with a line tracing Ysolde's age. Start with the "Frozen" preset. The top strip is evenly spread. The bottom strip is a single tower of sixty dots stacked in one year. Drag the drift slider up. The tower spreads into a line, Ysolde's age climbs, and the "time gap" readout grows in step with the span, always the same number. Switch to "Stepped" and watch the in-world strip break into flat plateaus separated by jumps.

### Cross-game recognition

**The Elder Scrolls Online (2014 to 2025).** Here `r = 0` and `J = 0` for most of the game's life, and the span is zero. The density is extreme. UESP dates the game's releases through the 2024 Gold Road chapter to 2E 582. What bought the zero is order-free content. The game's One Tamriel update (Update 12, October 2016) let players go to almost any zone at any level, which only makes sense if no zone is "later" than another. In 2025 the Season of the Worm Cult storyline moved the calendar forward by an unstated amount, according to a September 2025 developer answer cited on UESP. Rewritten in our form, that is the game's first `J > 0`, eleven years after launch.

**Guild Wars 2 (2012 to 2025).** Launch in 1325 AE, the present day at 1339 AE after the Visions of Eternity expansion of October 2025. That is 14 in-world years over about 13 real years, so the effective drift is about `r = 1.06`. Note that the team stopped syncing to real time on purpose. They got close to `r = 1` anyway, because story seasons kept landing about a year apart in fiction. The time gap is correspondingly large. A character created today plays the 1325 AE personal story, against an Elder Dragon who died years earlier in the world's present.

**EVE Online (2003 to present).** Exactly `r = 1`, `J = 0`, with `YC = real year − 1898`. EVE can afford it because its story is mostly about player events and it has no levelling path of old story zones to fall behind. There is no launch zone set in YC105 for a new player to walk into. The time gap exists only in old news articles, where it belongs.

Rewrite any MMO's history this way. Find `w0`, find the in-world year of the latest content, divide by real years for an effective `r`, and check whether the increases arrived in steps (`J`) or smoothly (`r`). Then ask what the game does about its time gap.

### Eyes-open design judgment

No policy is free.

- **Frozen (`r = 0`).** Order-free content, a clean fit for scaled zones, no ageing characters. Cost: the world cannot show consequence over time. Wars cannot end, children cannot grow, and your one year fills with an implausible number of world-changing crises. ESO kept this policy for eleven years before its 2025 storyline moved the calendar on.
- **Real time (`r = 1`).** Consequences are dated and characters can age with the audience. Cost: a large time gap in old content, and cast members who age out of their roles. It suits worlds where the story lives in the present and old content is thin, like EVE.
- **Stepped (`J > 0` per expansion).** Expansions become eras, and the jump hides a lot. Characters change off screen and wars end between chapters. Cost: the biggest time gaps of all, and a strong expectation that each expansion will jump again.
- **Slow drift (`0 < r < 1`).** A compromise that keeps the gap modest and still lets a war end. Cost: characters age strangely slowly, and players who do the arithmetic will point it out.

Whatever you choose, decide three things on purpose. Decide what old content claims about its date. You can have old zones say "this is the past" out loud, use phasing (GD202 week 13) so each player sees the date that matches their progress, or refuse to date the story at all. Decide which characters are allowed to age. Decide who owns the calendar, so the date of every new beat is set in one document rather than by whoever writes the patch.

## 3. The deep past: writing history before launch

The lore clock governs the years after launch. Before launch you write the centuries behind it. Different rules apply, because nobody will ever play those years directly. They exist to explain the present and to supply content.

### Eras, not years

Organize the deep past into **eras**, stretches of time with one defining condition, bounded by events that changed it. "The Age of the Twin Crowns", "the Drowning", "the Long Truce". Eras are easier to remember than dates and easier to build around. Eras are also the level at which players talk about your past.

A workable rule is three to five eras before the present, each shorter and better known than the one before it. Deep eras are myth (week 6 handles how myth works as evidence). Middle eras are legend and ruins. The most recent era is living memory, and it is where your factions' grudges come from.

### Each era leaves three things

For each era, write down what it left in three places:

1. **In the ground.** Physical remains your level designers can build: ruins, roads, mines, graves, a dam. This is the list your dungeon and zone designers pull from. GD201 week 8 covers how to make those remains tell their story in the space itself ([environmental storytelling](../../GD201-level-and-world-design/lectures/w08-environmental-storytelling.md)).
2. **In the living.** Things people still believe, owe, fear or fight over: a treaty, a debt, a banned family name, a holiday. These become faction motives, quest hooks and NPC dialogue.
3. **In the dark.** One question about the era you deliberately leave open. Who opened the gate? Where did the fleet go? This is a reserved gap, a place where a future expansion can put a new truth without contradicting anything.

An era with nothing in the ground gives your content team nothing to build. An era with nothing in the living has no effect on play. An era with nothing in the dark closes a door you may want later.

### The precision gradient

How exact should dates be? A useful rule is that precision should fall with distance. The last fifty years have exact years and named people. The last five centuries have approximate dates, "early in the reign of", "some ninety years after". The deep past has only order, this before that.

The gradient is realistic, since real societies know their recent past better than their distant past. It is also practical. Every exact date is a constraint that future writers must respect. A vague date is a small reservoir of freedom. When week 11 discusses retcons, you will see that the most expensive facts to change are precise ones that many pieces of content refer to.

### Calendars and epochs

A calendar's epoch says what its makers thought mattered. Guild Wars 2's Mouvelian calendar counts from the Exodus, the moment the gods left Tyria, so the dominant human calendar is built around a religious loss. EVE's counts from the Yoiul Conference. When you pick an epoch, you are writing a line of culture.

Worlds with several cultures should usually have several calendars. Guild Wars 2's wiki lists three side by side. Its timeline table gives 1325 AE as 1835 in the Canthan calendar and 1525 in another reckoning, so each converts by a fixed offset: Canthan year = AE year + 510. Conversions are cheap to compute and they create texture, like two nations disagreeing about how old a treaty is. The cost is confusion. Pick one calendar as the reference in your bible and in any player-facing tooltip.

## 4. The timeline document

The timeline is a working tool, so it needs columns that a novel would never need. A timeline row in a live MMO bible should hold at least:

| Column | What it holds | Why |
|---|---|---|
| Date | In the reference calendar, at the precision the gradient allows | One source of truth for when |
| Event | One sentence | Short enough to scan |
| Public or secret | Whether in-world people know it | Stops NPCs knowing too much |
| Who knows | Groups or characters | Dialogue checks against it |
| Left behind | Ground, living, dark | Links to content |
| Referenced by | Every quest, item, zone or book that mentions it | The cost of changing it later |

The last column is the one teams skip, and it is the one that saves them. A fact referenced by one book is cheap to revise. A fact referenced by forty quests, three zones and a raid is effectively permanent. When a writer proposes a new beat, check its date against the lore clock policy, check its participants against the "who knows" column, and add its references as they ship.

## In-class activity (25 minutes)

In groups of three, you are the narrative leads for *Thornmere*, eighteen months before launch.

1. Pick a clock policy (values for `r`, `J`, `T`) for the first eight real years. Write two sentences justifying it with the game's structure. Is there a levelling path of story zones? Can players do zones in any order?
2. With the interactive's custom mode, record the span, the density and Ysolde's age at year 8 under your policy, assuming six beats per real year.
3. Write the one-sentence answer your game gives a new player at year 8 who asks "is the war in the starting zone still going?"
4. Sketch three eras before the present, with one item in the ground, one in the living and one in the dark for each.

Expected output: the parameter values, three numbers from step 2, the sentence from step 3, and a nine-cell era table. Swap tables with another group and find one era whose "in the dark" question could not support an expansion.

## Common misconceptions

- **"A frozen calendar means nothing changes."** The story still advances. Only the dates do not, so all change is packed into one year. The density column measures how crowded that year gets.
- **"Syncing to real time avoids timeline problems."** It trades them for a time gap in old content that grows by one year every year. Guild Wars 2's writers stopped syncing on purpose and ended up near `r = 1` anyway.
- **"The deep past should be as detailed as possible."** Precision is a cost as well as a gift. Every exact date is a constraint on future writers. Keep the deep past to order and eras.
- **"Players only care about history if they read the books."** Most players never read the timeline, but all of them walk through its ruins and fight its factions. History reaches players mostly through content.

## Check yourself

1. A game launches in the year 400 of its calendar with `r = 0.5` and a jump of 2 years with each expansion, shipped every 3 real years. What is the in-world year at real year 9? What is the time gap for a player starting then?
2. The same game ships 8 story beats per real year. What is the density at real year 9? A character is 30 at launch. How old are they?
3. In the Guild Wars 2 table, 1336 AE is which Canthan year? A Canthan text dates a treaty to 1790 CC. What AE year is that?
4. Your director wants characters to age "a bit" and wants all zones playable in any order. Explain with the model why these two goals conflict, and propose a policy that gives up as little of each as possible.
5. An era in your bible has two ruins and one open question but no entry "in the living". What will players notice, and what would you add?

<details>
<summary>Answers</summary>

1. Three expansions have shipped by `t = 9` (`floor(9/3) = 3`). `w = 400 + 0.5 × 9 + 2 × 3 = 410.5`, so late in the year 410. The time gap equals the span, 10.5 years.
2. `D = 8 × 9 / 10.5 ≈ 6.9` beats per in-world year. The character is `30 + 10.5 = 40.5`.
3. The offset is +510, so 1336 AE is 1846 CC. 1790 CC is `1790 − 510 = 1280` AE.
4. Ageing needs `S > 0`. Any `S > 0` creates a time gap of the same size in old content, so zones are no longer equivalent in date. A compromise is slow drift (`r` around 0.2 to 0.3) plus phasing or undated side content, so the gap stays small and only a few zones need to declare "this is the past". Or keep `r = 0` for the open world and let only an expansion's own zones jump, marked as a new era.
5. The era explains places but nobody in the present cares about it. It will feel like decoration. Add something the era left in the living: a feud, a debt, a festival, a law, a banned symbol that a faction still uses.

</details>

## Lab / assignment hook

[Lab 04, the lore clock and timeline checker](../labs/lab04.md). You implement the clock and a checker that flags impossible timeline rows (characters acting before birth or after death, events dated outside their era). Then you write your own world's three-era history and a ten-year clock policy and run them through the checker. The history becomes the history chapter of your world bible.

## Sources

- UESP, "Lore:Second Era" (timeline entries dated 2E 582 and their notes, accessed September 2026). ESO's events dated to 2E 582; Leamon Tuttle's explanation from the Elsweyr and Update 22 "Ask Us Anything" (2019) that the team resisted moving to 2E 583 because players play content in any order; the note that the Season of the Worm Cult (2025) moved the timeline forward an unknown amount, citing Bill Slavicsek in the official ESO leadership AUA of 9 September 2025.
- UESP, "Online:Online" (accessed September 2026). ESO is set in 2E 582.
- Guild Wars 2 Wiki, "Timeline" (accessed September 2026). Personal story begins 1325 AE; End of Dragons 1335 AE; Janthir Wilds 1337 AE; Visions of Eternity 1338 AE; present day 1339 AE; parallel Canthan (CC) and third-calendar columns (1325 AE = 1835 CC = 1525).
- Guild Wars 2 Wiki, "Mouvelian calendar" (accessed September 2026). Epoch at the Exodus of the gods; ArenaNet's narrative team once tried syncing the calendar to real time and abandoned it.
- EVE University Wiki, "Yoiul Conference" (accessed September 2026). YC dating; add 1898 to convert to the real year (YC105 = 2003).
- UESP, "Online:One Tamriel" (Update 12, 5 October 2016; any PvE zone at any level with scaling).
- Wikipedia, "The Elder Scrolls Online" and "Guild Wars 2" (release dates: April 2014; August 2012; Visions of Eternity, 28 October 2025).
- Wolf, M. J. P. (2012). *Building Imaginary Worlds: The Theory and History of Subcreation*. Routledge. Chapter 3 on world structures including timelines.

## Interactive spec: examples/w04-lore-clock.html

**The one insight.** The in-world span a live game gains is the same number as the time gap a new player feels in launch content. Moving any control that grows the span grows the gap by exactly the same amount, and the only way to a zero gap is a frozen calendar whose single year fills with every story beat.

**Model (all values in real years `t` since launch, 0 to 15).**

```
w(t)   = w0 + r × t + J × floor(t / T)      (J term omitted when T is "none")
S(t)   = w(t) − w0                           span, also the time gap
D(t)   = E × t / max(S(t), 1)                beats per in-world year
a(t)   = a0 + S(t)                           Ysolde's age
beat i (i = 1..E×t) ships at real time t_i = i / E, in-world date w(t_i)
```

Defaults: `w0 = 1200`, `E = 6`, `a0 = 16`, `t = 10`, `r = 0`, `J = 0`, `T = none`.

**Layout: two linked views, stacked on mobile, side by side above 900px.**

1. *Real calendar* (top or left). A horizontal axis from 0 to the chosen `t`, real years. One dot per beat at `t_i`, evenly spaced. Vertical tick marks for expansions at `T, 2T, ...` when `T` is set, labelled "Exp 1", "Exp 2".
2. *In-world timeline* (bottom or right). A horizontal axis from `w0` to `w0 + max(S, 1)`, in-world years. The same dots placed at `w(t_i)`. When several beats share an in-world year (frozen or plateau), stack them vertically into a tower so the crowding is visible. A second line in this panel plots Ysolde's age `a` against in-world date, right-hand axis from 16 to 40.
3. A thin connector: hovering or focusing a dot in either view highlights its twin in the other and shows "beat i: real year t_i, in-world year w(t_i)".

**Readouts (large, next to the views).** Span `S`, time gap (same value, labelled "time gap for a new player"), density `D` to one decimal, Ysolde's age to one decimal, current in-world year `w(t)` to one decimal. Place span and time gap side by side so the student sees them move together.

**Controls.**
- Slider `t`, real years, 1 to 15, step 0.5.
- Slider `r`, 0 to 1.5, step 0.05.
- Slider `J`, 0 to 5 years, step 1.
- Select `T`: none, 1, 2, 2.5, 3, 4.
- Slider `E`, beats per real year, 2 to 12, step 1.
- Presets (buttons): "Frozen (ESO 2014 to 2024)" `r=0, J=0`; "Real time (EVE)" `r=1, J=0`; "Guild Wars 2 effective" `r=1.06, J=0`; "Stepped" `r=0, J=3, T=2.5`; "Slow drift" `r=0.25`.
- All controls keyboard operable; sliders have visible numeric values.

**Test values (defaults except as listed, `t = 10`, `E = 6`).**

| Setting | S and time gap | D | Age |
|---|---|---|---|
| Frozen `r=0` | 0 | 60.0 | 16.0 |
| Slow drift `r=0.25` | 2.5 | 24.0 | 18.5 |
| Real time `r=1` | 10 | 6.0 | 26.0 |
| Stepped `r=0, J=3, T=2.5` | 12 | 5.0 | 28.0 |
| `t=9, r=0.5, J=2, T=3, E=8, w0=400, a0=30` | 10.5 | 6.9 | 40.5 |

The last row matches check-yourself questions 1 and 2 (allow editing `w0` and `a0` in an "advanced" disclosure).

**Visual notes.** First screen shows the Frozen preset so the tower of 60 dots is the first thing seen. Use the shared palette tokens; beats in the accent colour, expansions in a muted second colour, the age line in a third. No game logos or art. Respect reduced motion (no animated transitions when set).
