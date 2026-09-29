# MMO406 · Week 09 — Living World Events

**Why this matters:** A living world event lets players push the story forward: they gather the supplies, hold the line, and the gates open. That promise has a clock inside it. If the goal is the same on every server, big servers finish before your aftermath content is ready and small ones may never finish at all. Players on each server then live in a different chapter of your history. This week you learn to set the goal so the story arrives on time everywhere, and to decide what the world keeps afterwards.

**You will be able to:**
- Compute each realm's finish day for a collective goal from its population, participation and contribution rate, with and without participation fatigue.
- Show that a fixed goal spreads finish dates in proportion to realm population, and find the largest goal a realm can ever reach under fatigue.
- Design a goal rule and a narrative window (earliest and latest acceptable finish) that land every realm's finish inside the window, with a fallback for realms that miss it.
- Critique shipped world events (the Gates of Ahn'Qiraj, the Ishgardian Restoration, the Triglavian Invasion) by their goal rule, their window and what the world kept afterwards.

**Before class:** Warcraft Wiki, "Ahn'Qiraj War Effort" and "Gates of Ahn'Qiraj" (the supply list and the realm opening dates, 15 minutes). EVE University Wiki, "Triglavian Invasion" (chapter 3 and its outcome, 10 minutes). Wolf, *Building Imaginary Worlds* (2012), chapter 6, "Transmedial Growth and Adaptation" (use the contents page to pick about 15 pages).

**Prerequisites from earlier courses:** [MMO306 week 11, events and world bosses](../../MMO306-content-design-at-scale-quests-dungeons-and-raid/lectures/w11-events-and-world-bosses.md) (reach and crowd for repeating events, and scaling a boss to the crowd; this week is about one-time events and their place in the story). [GD202 week 13, shared vs personal story](../../GD202-narrative-and-quest-design/lectures/w13-shared-vs-personal-story.md) (the consequence budget; living world events sit in the shared and permanent cell). [MMO308 week 8, event design and calendars](../../MMO308-live-operations-analytics-and-experimentation/lectures/w08-event-design-and-calendars.md) (borrowed play and event fatigue in live-ops terms). This course: [week 7, lore delivery in MMOs](w07-lore-delivery-in-mmos.md) (permanence and knowledge share) and [week 8, player agency vs canon](w08-player-agency-vs-canon.md) (delegating canon to players).

**Interactive:** [w09-realm-clock.html](../examples/w09-realm-clock.html). Keep it open during section 2.

---

## 1. When the world's story moves

Most MMO story is **authored and replayable**. Every player walks through the same chapters at their own pace. A **living world event** is different. It changes the shared world once, at a time, often with the players' help, and the change stays. GD202 week 13 placed this in the "shared and permanent" cell of the consequence budget and warned that it leaves latecomers behind. Week 7 of this course measured how fast that happens. This week looks at the moment itself.

Three kinds of living world event cover most shipped cases.

- **Scheduled change.** The story moves on a date the studio sets. The city falls on patch day for everyone. Players take part, but they don't decide when or whether.
- **Collective goal.** Players contribute toward a target (supplies delivered, enemies defeated, structures built), and the story moves when they reach it. The goal is a clock that players drive.
- **Contested outcome.** Players split between sides, and the result depends on which side does more. The outcome itself is up to the players, which week 8 called delegating canon.

Scheduled changes are easy to plan and give players little agency. Contested outcomes give the most agency and are hard to write for, because you don't know the result. Collective goals sit in between. The story's direction is fixed, but its timing depends on players. That timing is what goes wrong most often, so it gets this week's worked example.

### Realms make timing a story problem

Many MMOs run the same world as several copies, called **realms**, **worlds** or **servers**, each with its own population. A collective goal usually runs separately on each realm, because the whole point is that *these* players, the ones you see every day, did it. That means each realm has its own clock. When the clocks disagree, your world has several histories at once. On one realm the gates have been open for a month. On another the war effort is still collecting supplies. Every piece of story content that refers to the event has to work on both.

## 2. Worked example: the realm clock

### The hook

World of Warcraft patch 1.9 (3 January 2006) started the Ahn'Qiraj War Effort. On every realm, both factions had to deliver the same list of war supplies, among them 90,000 copper bars, 26,000 purple lotus, 80,000 thick leather, 17,000 spotted yellowtail and 400,000 runecloth bandages, before the ancient gates could open. When the supplies were in and a player had finished a long quest chain for the Scepter of the Shifting Sands, that player could ring a gong. A ten-hour war across the continent followed, and the raids behind the gates opened.

The list was the same on every realm. The opening dates were not. Warcraft Wiki records the first US realm, Medivh, opening on 22 January 2006, and Icecrown on 7 February. In Europe the recorded dates run from 30 January to 11 February. For weeks, the question "are the gates of Ahn'Qiraj open?" had a different answer depending on where you played. From February 2009, shortly after patch 3.0.8a, new realms simply started with the gates open.

[GD202 week 13](../../GD202-narrative-and-quest-design/lectures/w13-shared-vs-personal-story.md) used the same event to show a change that reached every player on a realm at once. This week asks a different question, about timing across realms.

Here is the puzzle. The goal was identical everywhere. Why should the story arrive on different days, and what should the designer have wanted?

### The model

Take a realm with `N` active players. Each day, a share `q` of them contribute, and each contributor delivers `u` units of the goal on average. The realm's goal is `G` units.

```
daily rate          R = N × q × u
finish day          T = ⌈G / R⌉                          (no fatigue)

with fatigue d:     contributions on day t = R × d^(t − 1)
cumulative          C(T) = R × (1 − d^T) / (1 − d)
ceiling             C(∞) = R / (1 − d)
finish day          T = ⌈ ln(1 − G(1 − d)/R) / ln d ⌉    if G < C(∞), otherwise never
```

- `N` is the realm's active players, `q` the daily **participation** share, and `u` the units a participant delivers per day.
- `G` is the goal. A **fixed goal** is the same on every realm. A **scaled goal** is `G = g × N`, where `g` is the goal per active player.
- `d` is the daily **fatigue** factor. Each day, participation is `d` times the day before. `d = 1` means no fatigue. `d = 0.97` means participation falls 3% a day, which is a reasonable shape for a grind that pays little after the first days (MMO308 week 8 measures real event fatigue).
- `⌈x⌉` means round up to a whole day.

The ceiling `C(∞)` is the most a realm can ever deliver once fatigue sets in. Divide by `N` and it becomes `q × u / (1 − d)` per active player. **A goal above the ceiling is never reached, however long you wait.**

Add the story's constraint. The event's **narrative window** runs from `D_min`, the earliest day the aftermath content is ready, to `D_max`, the latest day the story can wait before the next patch needs the event finished. A good goal rule lands every realm's finish day inside the window.

### Numbers you can check

Four realms, invented but typical in their spread: 1,500, 3,000, 6,000 and 12,000 active players. Participation `q = 0.2`, contribution `u = 10` units a day, so each realm's daily rate is `2 × N`. The narrative window is day 14 to day 42.

**Fixed goal, `G = 300,000`, no fatigue.**

| Realm | `N` | Daily rate `R` | Goal per active player | Finish day | In window 14-42? |
|---|---|---|---|---|---|
| Small | 1,500 | 3,000 | 200 | 100 | Late |
| Medium | 3,000 | 6,000 | 100 | 50 | Late |
| Large | 6,000 | 12,000 | 50 | 25 | Yes |
| Huge | 12,000 | 24,000 | 25 | 13 | Early |

Check the small realm by hand. `300,000 / 3,000 = 100` days. The finish days are in inverse proportion to population. An eight-fold spread in players becomes an eight-fold spread in dates. The huge realm finishes a day before the aftermath content exists. The small realm's players each have to deliver eight times as much as the huge realm's, for the same story.

**Scaled goal, `g = 50` per active player, no fatigue.** Every realm has `G = 50 × N`, so `T = g / (q × u) = 50 / 2 = 25` days everywhere. One date for the whole world, inside the window, with the same effort per player.

**Now add fatigue, `d = 0.97`.** The ceiling per active player is `q × u / (1 − d) = 2 / 0.03 = 66.7` units.

| Realm | Fixed goal: per player | Fixed goal: finish day | Scaled `g = 50`: finish day | Scaled `g = 45`: finish day |
|---|---|---|---|---|
| Small | 200 | Never | 46 | 37 |
| Medium | 100 | Never | 46 | 37 |
| Large | 50 | 46 | 46 | 37 |
| Huge | 25 | 16 | 46 | 37 |

With fatigue, the fixed goal no longer produces late realms. It produces realms that never finish. The small and medium realms need 200 and 100 units per player against a ceiling of 66.7. The scaled goal of 50 still finishes everywhere, but on day 46, past the window. To land inside it, the goal per player must satisfy `g ≤ 66.7 × (1 − 0.97^42) = 48.1`. At `g = 45` every realm finishes on day 37.

Check the scaled `g = 45` case by hand. `G / R = 45 / 2 = 22.5` days of full-strength effort. `1 − 22.5 × 0.03 = 0.325`. `ln 0.325 / ln 0.97 = −1.124 / −0.0305 = 36.9`, so day 37.

The whole table in a few lines:

```python
import math

def finish_day(goal, rate, d=1.0):
    """First whole day on which cumulative contributions reach the goal (None if never)."""
    if d == 1.0:
        return math.ceil(goal / rate)
    x = 1 - goal * (1 - d) / rate
    return None if x <= 0 else math.ceil(math.log(x) / math.log(d))

realms = {"Small": 1500, "Medium": 3000, "Large": 6000, "Huge": 12000}
for d in (1.0, 0.97):
    fixed = {r: finish_day(300_000, 2 * n, d) for r, n in realms.items()}
    scaled = {r: finish_day(45 * n, 2 * n, d) for r, n in realms.items()}
    print(d, "fixed", fixed, "scaled45", scaled)
```

```
1.0 fixed {'Small': 100, 'Medium': 50, 'Large': 25, 'Huge': 13} scaled45 {'Small': 23, 'Medium': 23, 'Large': 23, 'Huge': 23}
0.97 fixed {'Small': None, 'Medium': None, 'Large': 46, 'Huge': 16} scaled45 {'Small': 37, 'Medium': 37, 'Large': 37, 'Huge': 37}
```

Without fatigue the scaled goal of 45 finishes on day 23 (`45 / 2 = 22.5`, rounded up). With fatigue it takes until day 37, as computed by hand above. `None` marks a realm that never finishes.

### Reading the answer to the hook

The Ahn'Qiraj list was a fixed goal. The model predicts that the realms' opening dates would spread according to how much each realm could deliver per day, which depends on population and on how organized each realm's players were. That fits what players saw. The first recorded realm opened 19 days after the patch, and the five recorded US dates spread over 16 days, with a similar spread in Europe. Warcraft Wiki records the dates. It doesn't record realm populations, so we can't test the model's exact prediction against it. Treat this as a hypothesis the data is consistent with, not a result.

What should the designer have wanted? That depends on the story. If the event's point is "each realm's players open the gates themselves, whenever they manage it," a spread of dates *is* the story, and different histories per realm are the cost of that agency. If the point is "the world moves into a new chapter," the spread is a bug, and a scaled goal is the fix.

### A visual you can move

Open [`w09-realm-clock.html`](../examples/w09-realm-clock.html). The left chart shows each realm's progress toward its goal over 60 days, with the narrative window shaded. The right panel is a timeline of finish days, one dot per realm, with realms that never finish drawn at the right edge as hollow markers. Start with the fixed goal and no fatigue. The progress lines fan out and the dots spread across the timeline. Switch to a scaled goal and the lines lie on top of each other. Then turn on fatigue and watch the small realms' lines flatten below 100% for good.

### Cross-game recognition

**Final Fantasy XIV, the Ishgardian Restoration (patch 5.1 through 5.5, Shadowbringers era, from late 2019).** Crafters and gatherers delivered materials to rebuild a district of the city of Ishgard. Each world ran its own stockpile, managed separately, and group construction work was scheduled when a world's stockpile was large enough. The construction phases themselves advanced with patches. In model terms, each patch set a `D_min` that no world could outrun, however fast its players delivered, while the world's own stockpile set its pace within the phase. When the restoration ended, a monument on each world showed which crafting class had contributed most there in the last phase. That is a permanent, per-realm record of a collective goal.

**EVE Online, the Triglavian Invasion, chapter 3 (26 May to 13 October 2020).** Players fought for either the invading Triglavian Collective or the defending EDENCOM, and each star system moved along one of two paths depending on which side players supported there. This is a contested outcome with many small "realms", one per system. By the end, 27 systems had fallen to the Triglavians and became a new region, Pochven. One of them, Niarja, fell on 18 August 2020 and cut the high-security route between major trade hubs. The EVE University Wiki reports that the trip grew from 10 jumps to 45. The players wrote canon into the map, and the map kept it.

**Guild Wars 2, the Cutthroat Politics election (July and August 2013).** Week 8 used it as an example of delegated canon. In this week's terms it was a contested outcome with a fixed window. The election closed on a set date whatever the totals, so `D_min = D_max`, and only the winner, not the timing, was up to the players.

**Guild Wars 2, the Battle for Lion's Arch (March 2014).** The end of Living World Season 1 destroyed the hub city on a date the studio set, for everyone at once. A scheduled change, the opposite end from the war effort. It had no timing risk and gave players no say in the outcome, and week 7 showed its knowledge cost.

Four events, one question each. Who sets the clock, players or the studio? Is there one clock or many? And what does the world keep afterwards?

### Eyes-open design judgment

- **Fixed goals produce per-realm histories.** That can be the point. Players on a small realm who finally open the gates after weeks have a story that players on a huge realm don't. Choose it deliberately and write aftermath content that works whenever it unlocks.
- **Scaled goals produce one history.** They also remove the sense that *our* realm did something special, because every realm needs the same effort per player. You can scale the goal and still give each realm a distinct record with per-realm rankings or monuments. The Ishgard monument is that kind of record. Square Enix did not publish whether its per-world stockpile targets scaled with population, so don't cite it as a scaled goal.
- **Fatigue sets a hard ceiling.** Check `g` against `q × u / (1 − d)` before launch, and add a fallback. Common fallbacks are a studio-driven finish on `D_max` ("the reinforcements arrive"), a goal that shrinks after a set day, or a contribution bonus that grows over time.
- **Participation is not a constant.** `q` depends on the reward, the rest of the calendar (MMO308 week 8) and whether players believe the goal can be reached. A realm that falls behind early can see `q` collapse, which is a loop the model does not include. Lab 09 adds it.
- **Decide deliberately:** is the timing part of the story, or a risk to it? Write the answer in the event brief before anyone chooses a number.

### Check yourself (worked example)

1. A realm has 4,000 active players, 25% of whom contribute 8 units a day. The goal is 200,000 units. On what day does it finish without fatigue? With `d = 0.95`?
2. With `q = 0.25`, `u = 8` and `d = 0.95`, what is the largest goal per active player that is ever reached, and what `g` finishes by day 30?

<details>
<summary>Answers</summary>

1. `R = 4,000 × 0.25 × 8 = 8,000` a day. Without fatigue, `200,000 / 8,000 = 25` days. With fatigue, `x = 1 − 200,000 × 0.05 / 8,000 = 1 − 1.25 < 0`, so never. The ceiling is `8,000 / 0.05 = 160,000`, below the goal.
2. Ceiling per player `0.25 × 8 / 0.05 = 40` units. By day 30, `g ≤ 40 × (1 − 0.95^30) = 40 × (1 − 0.215) = 31.4` units per player.

</details>

## 3. Writing for several histories at once

A collective goal on separate realms means that for some weeks your world has as many histories as it has realms. Four writing rules keep that manageable.

**Write the before, the during and the after as separate states.** Each realm is in exactly one of them. Every NPC line, quest and zone that refers to the event needs a version for each state it can be seen in. Keep the number of states small. Three is plenty.

**Make "during" talk about the effort, not the outcome.** During the war effort, NPCs should talk about the supplies, the stakes and the rumors, not about what happens when the gates open. That keeps "during" content correct however long it lasts.

**Make "after" content independent of the finish date.** Aftermath content should not say "last week the gates opened," because on some realms it was a month ago. Write it as the world's present state. Week 7's rule for recaps applies unchanged.

**Plan the reconvergence.** At some point, usually the next major patch, every realm must be in the same state again, because the next chapter is written once. Set `D_max` so that the slowest realm reaches "after" before then, or use the fallback. Realms created later start in the final state, as World of Warcraft's did for Ahn'Qiraj from 2009.

## 4. What the world keeps

Every living world event ends in one of the permanence classes from week 7. The event itself is almost always temporary. What it leaves behind is a design choice, and it is the part that becomes lore.

| What remains | Example | Who it serves |
|---|---|---|
| Changed geometry | A destroyed city, an open gate, a region renamed | Everyone. The highest-reach channel you have. |
| A record of who did it | A monument listing a realm's top contributors, a title for the gong-ringer | The live audience, and newcomers who ask about it |
| Replayable version | A story instance that retells the event | Newcomers, at the cost of the "you had to be there" value |
| Nothing | The event ends and the world resets | Nobody. Use only for recurring events, which MMO306 week 11 covers |

The first row deserves most of your effort. Players who missed the Triglavian Invasion still fly through Pochven. Players who missed the Battle for Lion's Arch walked through its ruins. **The world's geometry is the only record of a living event that every future player is guaranteed to see.** Plan the aftermath zone state as carefully as the event.

A record of who did it turns a collective goal into personal canon for the participants. That makes it valuable to them and invisible to everyone else. The Ishgard monument's per-world class ranking shows a middle path. The record belongs to the realm, not to any single player.

### The event brief

Before an event is built, write a one-page brief with these parts.

1. **Kind.** Scheduled change, collective goal or contested outcome.
2. **Story.** The world state before and after, in two sentences each.
3. **Clock.** Goal rule (fixed, scaled or scheduled), window `D_min` to `D_max`, and the predicted finish day per realm size from the model, with fatigue.
4. **Fallback.** What happens on `D_max` on a realm that hasn't finished.
5. **States.** The list of world states NPCs and quests must support, and the content that changes in each.
6. **Legacy.** What stays in the world, from the table above, and its permanence class.
7. **Canon.** If the outcome is contested, how later content refers to it, using the five answers from week 8.

## In-class activity (25 minutes)

In groups of three, design a collective goal for your setting bible.

1. Pick an event from your world's tension ledger (week 1) that players could push forward: a siege, a rebuilding, a migration (5 minutes).
2. Your game has realms of 2,000, 5,000 and 15,000 active players. Choose `q`, `u` and `d` with a one-line justification each (5 minutes).
3. Choose a goal rule and a window. Compute each realm's finish day with the interactive, and adjust until all land in the window (8 minutes).
4. Write the fallback and the legacy lines of the event brief (7 minutes).

Expected output: parameters, a three-row finish-day table, and two brief sections. Be ready to defend whether your event's timing is part of the story or a risk to it.

## Common misconceptions

- **"The same goal everywhere is the fair choice."** The same total goal asks each player on a small realm to do more. Equal effort per player means a scaled goal.
- **"If a realm is slow, it will get there eventually."** Not under fatigue. A goal above `q × u / (1 − d)` per player is never reached.
- **"Player-driven events give players agency over the story."** Collective goals give agency over timing. Only contested outcomes give agency over what happens. Know which one you are offering.
- **"The event is the content."** The event lasts weeks. The world state it leaves lasts years and is what most future players meet.

## Check yourself

1. Two realms of 2,500 and 10,000 active players face a fixed goal of 400,000 units, with `q = 0.2`, `u = 10`, no fatigue. On which days do they finish? What goal per player does each face?
2. You want every realm to finish on day 30 with no fatigue, with `q = 0.25` and `u = 6`. What `g` do you set?
3. With `d = 0.96`, `q = 0.2`, `u = 10`, what is the ceiling per active player? A scaled goal of `g = 40` finishes on which day?
4. A contested event lets players decide whether a fortress falls. Using week 8's model, what share of players are contradicted by the outcome if 58% supported the winning side? Name one way to reduce the cost for the losing side.

<details>
<summary>Answers</summary>

1. Rates are 5,000 and 20,000 a day. Finish days `400,000 / 5,000 = 80` and `400,000 / 20,000 = 20`. Goals per player are 160 and 40 units.
2. `T = g / (q × u)`, so `g = 30 × 0.25 × 6 = 45` units per active player.
3. Ceiling `0.2 × 10 / 0.04 = 50` units. `x = 1 − 40 × 0.04 / 2 = 0.2`. `ln 0.2 / ln 0.96 = −1.609 / −0.0408 = 39.4`, so day 40.
4. 42% of participants are contradicted, since the canon choice has take rate `p = 0.58`. Ways to reduce it: give the losing side a record of its own (a memorial, a title), write aftermath content in which the losing side's goal survives in another form, or let each side's participants keep a personal-canon flag that later dialogue honors.

</details>

## Lab / assignment hook

[Lab 09, the realm clock](../labs/lab09.md). You implement the realm clock with fatigue, add a feedback loop in which falling behind lowers participation, and design a collective-goal event for your setting with a full event brief. It counts toward the exercises grade, and the brief goes into the events section of your world bible.

## Sources

- Warcraft Wiki, "Ahn'Qiraj War Effort" (now a redirect to "Gates of Ahn'Qiraj"; read September 2026). Patch 1.9.0 on 3 January 2006; per-realm war supplies for both factions, including 90,000 copper bars, 26,000 purple lotus, 80,000 thick leather, 17,000 spotted yellowtail and 400,000 runecloth bandages; the gong and the ten-hour war. https://warcraft.wiki.gg/wiki/Ahn%27Qiraj_War_Effort
- Warcraft Wiki, "Gates of Ahn'Qiraj" (read September 2026). Realm opening dates (US: Medivh 22 January 2006 to Icecrown 7 February 2006; EU: Kael'thas and Magtheridon 30 January to Destromath 11 February 2006); gates open automatically on new realms from February 2009, after patch 3.0.8a. The page's introduction gives Medivh's date as 23 January and its realm list gives 22 January; the difference does not affect the argument. https://warcraft.wiki.gg/wiki/Gates_of_Ahn%27Qiraj
- Final Fantasy XIV Online Wiki (consolegameswiki), "Ishgardian Restoration" (read September 2026). Construction from patch 5.1 to 5.5; the effort and stockpile run separately on each world; concerted works scheduled when enough supplies were stockpiled; the Skybuilders' monument showing each world's leading class in phase IV. https://ffxiv.consolegameswiki.com/wiki/Ishgardian_Restoration
- EVE University Wiki, "Triglavian Invasion (Chapter 3)" (the "Triglavian Invasion" page redirects there; read September 2026). Chapter 3 from 26 May to 13 October 2020; EDENCOM and Triglavian system paths; 27 systems reached Final Liminality and formed Pochven; Niarja fell on 18 August 2020, and the trade-hub route grew from 10 to 45 jumps. https://wiki.eveuniversity.org/Triglavian_Invasion_(Chapter_3)
- Guild Wars 2 Wiki, "Cutthroat Politics" (read September 2026). Election from 23 July to 5 August 2013. https://wiki.guildwars2.com/wiki/Cutthroat_Politics
- Guild Wars 2 Wiki, "Living World Season 1" (read September 2026). Season ended with the Battle for Lion's Arch and its aftermath on 18 March 2014. https://wiki.guildwars2.com/wiki/Living_World_Season_1
- Wolf, M. J. P. (2012). *Building Imaginary Worlds: The Theory and History of Subcreation*. Routledge. Course text. Chapter titles checked against the publisher's table of contents (Routledge, September 2026): 1 "Worlds within the World", 3 "World Structures and Systems of Relationships", 4 "More Than a Story: Narrative Threads and Narrative Fabric", 6 "Transmedial Growth and Adaptation", 7 "Circles of Authorship".
- The realm sizes, participation, contribution rates, fatigue factors and windows in the worked example and exercises are invented for teaching.

## Interactive spec: examples/w09-realm-clock.html

**Purpose.** Let students see that a fixed collective goal spreads realms' finish days in inverse proportion to population, that participation fatigue turns late realms into realms that never finish, and that a scaled goal below the fatigue ceiling lands every realm in the narrative window.

**The one insight the visual must make obvious.** With a fixed goal the progress lines fan out and some never reach 100%; switching to a scaled goal makes the lines coincide, and the finish dots gather in one spot inside the shaded window.

**Layout.** Two linked views side by side at 1280 px, stacked at 390 px (progress chart on top), with a results table underneath.

- Left, "Progress": a line chart. x axis is days 0 to 60. y axis is the share of each realm's goal delivered, 0 to 100% (clip at 100%). One line per realm (four realms), distinguished by both color token and dash pattern, labeled at the line end. The narrative window `D_min` to `D_max` is a shaded band. A horizontal line at 100%. When fatigue is on, a dotted line per realm at its ceiling share `C(∞) / G` if that is below 100%, labeled "ceiling".
- Right, "Finish day": a horizontal timeline from day 0 to 60 plus a "never" zone at the right edge. One dot per realm at its finish day, labeled with the realm name. Dots inside the window use the positive token; dots outside use the negative token and a hollow ring as a second cue. Realms that never finish sit in the "never" zone as hollow markers.
- Results table: one row per realm with `N`, daily rate `R`, goal `G`, goal per active player, ceiling per active player (if fatigue on), finish day (or "never"), and "early / in window / late / never".

**Controls** (keyboard accessible, values printed next to each):

- Realm populations: four number inputs, defaults 1,500, 3,000, 6,000, 12,000 (range 100 to 50,000).
- Participation `q`: slider 0.05 to 0.50, step 0.01, default 0.20.
- Contribution `u`: slider 1 to 30, step 1, default 10.
- Goal rule: segmented buttons "Fixed" and "Scaled", default "Fixed".
- Fixed goal `G`: slider 50,000 to 1,000,000, step 10,000, default 300,000 (enabled in Fixed mode).
- Goal per player `g`: slider 5 to 150, step 1, default 50 (enabled in Scaled mode).
- Fatigue toggle, default off, with `d` slider 0.90 to 1.00, step 0.005, default 0.97.
- Window: two sliders `D_min` (0 to 60, default 14) and `D_max` (0 to 60, default 42), with `D_min ≤ D_max` enforced.
- Button "Largest g that fits the window" (Scaled mode with fatigue on): sets `g` to `floor(q × u / (1 − d) × (1 − d^D_max))`, or without fatigue to `floor(q × u × D_max)`.
- Reset button.

**Formulas.**

- `R = N × q × u`. Goal `G` (fixed) or `G = g × N` (scaled).
- Progress on day `t` (whole days, contributions arrive at the end of each day): without fatigue `min(1, t × R / G)`; with fatigue `min(1, R × (1 − d^t) / (1 − d) / G)`.
- Finish day: without fatigue `ceil(G / R)`; with fatigue `x = 1 − G (1 − d) / R`, finish `ceil(ln x / ln d)` if `x > 0`, else "never". Guard floating error so exact integers are not bumped up (for example compute with a tolerance of 1e-9 before `ceil`).
- Ceiling per active player `q × u / (1 − d)`.

**Test values.**

| Rule | Fatigue | Small | Medium | Large | Huge |
|---|---|---|---|---|---|
| Fixed 300,000 | off | 100 | 50 | 25 | 13 |
| Scaled g = 50 | off | 25 | 25 | 25 | 25 |
| Fixed 300,000 | d = 0.97 | never | never | 46 | 16 |
| Scaled g = 50 | d = 0.97 | 46 | 46 | 46 | 46 |
| Scaled g = 45 | d = 0.97 | 37 | 37 | 37 | 37 |

Ceiling per active player at the defaults with fatigue: 66.7. "Largest g that fits the window" at the defaults with fatigue on: 48.

**First screen.** Fixed goal, no fatigue. Caption above the views: "Same goal on every realm. When does each one's story move on?" The four progress lines fan out; the finish dots sit at 13 (early), 25 (in window), 50 and 100 (late, the last one drawn at the chart edge with its label "day 100").

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css` inline, light and dark themes, `prefers-reduced-motion` respected (no animated line drawing when set). Realm lines are distinguished by dash pattern as well as color. An `aria-live` region summarizes each realm's finish day and status after each change. No game art, logos or screenshots.
