# GD202 · Week 09 — Emergent Narrative

**Why this matters:** The stories players retell about online worlds are mostly stories nobody wrote: the orc who kept coming back, the colony that fell in one bad winter, the battle that started over a missed bill. You can't script those stories, but you can build the conditions that make them likely. This week you learn which conditions matter and how to put a number on one of them, so that "emergent narrative" becomes a design target instead of a hope.

**You will be able to:**
- Distinguish authored, embedded and emergent narrative, and name the four ingredients (cast, memory, stakes, retelling) a systemic story needs.
- Compute the chance that a player meets the same character again within `k` encounters, from the cast size `R` and the memory weight `w`.
- Choose a cast size and memory weight that make rivalries likely, and predict what the choice costs.
- Critique a shipped system (the Nemesis System, RimWorld's storytellers, EVE Online's sovereignty) by naming its cast, memory, stakes and pacing.

**Before class:** Aylett, R. (1999), "Narrative in Virtual Environments: Towards Emergent Narrative", AAAI Fall Symposium on Narrative Intelligence, technical report FS-99-01 (four pages, free on the AAAI site). RimWorld Wiki, "AI Storytellers" (10 minutes). Wikipedia, "Boatmurdered" (10 minutes). Bateman (ed.), *Game Writing: Narrative Skills for Videogames*, 2nd ed. (2021), the material on systemic and player-driven story (the course reader lists the pages).

**Prerequisites from earlier courses:** [GD102 week 12, emergent behavior from simple rules](../../GD102-systems-design-and-game-mechanics/lectures/w12-emergent-behavior-from-simple-rules.md) showed how global patterns come from local rules. This week asks when those patterns read as a story. [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) is the only probability you need for the worked example. [GD201 week 3, intensity graphs](../../GD201-level-and-world-design/lectures/w03-flow-pacing-and-intensity-graphs.md) (same semester) built the stock-and-decay model of pacing and Left 4 Dead's AI Director. Section 3 uses it without re-deriving it. [MMO301 week 7, themepark vs sandbox](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w07-themepark-vs-sandbox.md) asked where a player's next new experience comes from. Within this course, [week 1](w01-story-vs-narrative-vs-plot.md) introduced the play story, and [week 2](w02-the-player-as-co-author.md) met the Nemesis System as a source of callbacks.

**Interactive:** [`examples/w09-rival-recurrence.html`](../examples/w09-rival-recurrence.html). Keep it open during section 2.

---

## 1. Stories nobody wrote

### Three kinds of game story

You have now met three ways a game can hold a story. [GS101 week 13](../../GS101-history-and-critical-study-of-games/lectures/w13-ludology-vs-narratology.md) gave them names from Henry Jenkins's essay on narrative architecture, and it helps to line them up.

- **Authored (enacted) narrative** is written in advance and performed through play. A quest chain from week 8 is authored. The designer fixes the beats and most of their order.
- **Embedded narrative** is placed in the world for the player to find: a burned farmhouse, a diary, a skeleton by a trap. The story happened before the player arrived. GD201 week 8 computed the chance players notice it.
- **Emergent narrative** arises during play from the game's systems and the player's actions. Nobody wrote it. The designer wrote the rules that made it possible.

Ruth Aylett introduced the term "emergent narrative" in a 1999 symposium paper. Her team had put television characters into a 3D world where the user could walk around freely, and they found that a pre-scripted story broke as soon as the user was free to go anywhere. She proposed letting narrative emerge from the characters' behavior and their interactions with the user instead. Game designers adopted the term for the same tension: the more freedom the player has, the less a script can hold.

### Two stories nobody wrote

**Boatmurdered (Dwarf Fortress, November 2006 to March 2007).** Fourteen members of the Something Awful forums played one Dwarf Fortress fortress as a succession game. Each player ran the fortress for one in-game year, wrote up what happened, and passed the save file on. The fortress collapsed over the years into violence and ruin, and the players' write-ups, taken together, read as one continuous story. The game produced the events. The players chose which events mattered and told them.

**The Bloodbath of B-R5RB (EVE Online, 27 to 28 January 2014).** A corporation on the N3 and Pandemic Legion side failed to make a scheduled sovereignty payment for a star system. The system lost its protection, and the rival coalition attacked. Over about 21 hours, more than 7,500 player characters took part, with up to 2,670 in the system at once. The losses were estimated at 11 trillion ISK, estimated at roughly 300,000 US dollars in real-world value. The battle ended when the servers went down for scheduled maintenance. A billing mistake became one of the largest battles the game has seen.

### What turns events into a story

Most emergent events are not stories. A wolf attacks, you kill it, nothing follows. Compare that with the two cases above and four ingredients stand out.

1. **Cast.** The events happen to a small set of characters the audience can keep track of. The fortress had named dwarves. B-R5RB was fought between named coalitions.
2. **Memory.** The world keeps what happened. The fortress stays ruined. The lost ships stay lost. A character who was hurt remembers who hurt them.
3. **Stakes.** Something is lost that took effort to build: a fortress, a fleet, a character's rank.
4. **Retelling.** Someone turns the events into a telling. The succession game's write-ups and the press coverage of B-R5RB did this work.

A designer can build for all four. This week's worked example puts a number on the first two together, because they interact in a way that is easy to get wrong.

## 2. Worked example: when does a stranger become a rival?

### The hook

In Middle-earth: Shadow of Mordor (Monolith Productions, 2014), the orc captains you fight are generated characters with names, ranks and traits. When a captain kills the player, the Nemesis System promotes him and makes him stronger for the next fight. Captains who survive an encounter remember it: one you threw into a fire may return scarred and angry about it. Warner Bros. was granted a US patent on the system in 2021.

Players tell stories about their personal nemesis in a way they don't about the hundreds of wolves they kill in a typical online RPG zone. Both games have combat, both have enemies with names on screen. Why does one produce rivals and the other produce a kill count?

One answer is memory: the orc remembers. But memory alone does nothing if you never meet the orc again. A rival needs a **rematch**, and whether a rematch happens is a matter of numbers you choose.

### The model

A **cast** of `R` characters can meet the player. Each encounter draws one of them at random. Most characters have weight 1. A **remembered** character, the one who beat the player, has weight `w ≥ 1`, so the game is `w` times as likely to pick him as any other single character.

```
P      = w / (R − 1 + w)          chance one encounter is the rematch
P_k    = 1 − (1 − P)^k            chance of at least one rematch in k encounters
wait   = 1 / P = (R − 1 + w) / w  mean encounters until the rematch
```

- `R` is the cast size: the number of distinct characters who could turn up.
- `w` is the memory weight. `w = 1` means the game gives the remembered character no preference.
- `k` is the number of encounters you look ahead.
- `P_k` uses the complement rule from MA102 week 3: the chance of at least one rematch is one minus the chance of none in `k` tries.

To reach a target chance `P*` of a rematch within `k` encounters, solve for the weight:

```
P needed  = 1 − (1 − P*)^(1/k)
w needed  = P needed × (R − 1) / (1 − P needed)
```

The weight you need grows in direct proportion to the cast.

### Numbers you can check

| Cast `R` | Weight `w` | `P` per encounter | Rematch within 5 | Rematch within 10 | Mean wait |
|---|---|---|---|---|---|
| 20 | 1 | 0.050 | 22.6% | 40.1% | 20.0 |
| 20 | 5 | 0.208 | 68.9% | 90.3% | 4.8 |
| 20 | 10 | 0.345 | 87.9% | 98.5% | 2.9 |
| 3 | 1 | 0.333 | 86.8% | 98.3% | 3.0 |
| 200 | 1 | 0.005 | 2.5% | 4.9% | 200.0 |
| 200 | 50 | 0.201 | 67.4% | 89.4% | 5.0 |

Check two cells by hand. For `R = 20, w = 10`, `P = 10 / (19 + 10) = 10/29 = 0.345`. Then `P_5 = 1 − (19/29)^5 = 1 − 0.121 = 0.879`. For `R = 3, w = 1`, `P = 1/3` and `P_5 = 1 − (2/3)^5 = 1 − 0.132 = 0.868`.

Now read the table as a designer. With a cast of 20 and no memory weight, fewer than one player in four sees their killer again within five fights. Set `w = 10` and nearly nine in ten do. The two rows `(20, 10)` and `(3, 1)` are almost the same: **a memory weight of 10 on a cast of 20 makes a rival as reliable as a cast of three**. And a cast of 200, the size of a busy zone's enemy population, needs `w = 50` just to reach two chances in three.

The weight formula gives exact targets. For a 50% chance of a rematch within 5 encounters, `P needed = 1 − 0.5^(1/5) = 0.129`. With `R = 20`, `w needed = 0.129 × 19 / 0.871 = 2.8`, so a weight of 3. With `R = 200`, it is `0.129 × 199 / 0.871 = 29.6`, so 30.

The table's first four rows come from this code:

```python
def p_meet(R, w):
    return w / (R - 1 + w)

def within(k, R, w):
    return 1 - (1 - p_meet(R, w)) ** k

for R, w in [(20, 1), (20, 5), (20, 10), (3, 1)]:
    print(R, w, round(p_meet(R, w), 3), round(within(5, R, w), 3),
          round(within(10, R, w), 3), round(1 / p_meet(R, w), 1))
```

```
20 1 0.05 0.226 0.401 20.0
20 5 0.208 0.689 0.903 4.8
20 10 0.345 0.879 0.985 2.9
3 1 0.333 0.868 0.983 3.0
```

### A visual you can move

Open the interactive. The left view shows a single encounter as a row of `R` tokens, with the remembered character's token drawn `w` times wider. At `R = 20, w = 1` his token is a sliver, and the per-encounter chance of 5% looks like nothing. The right view shows the chance of at least one rematch as a curve over the next 1 to 30 encounters, with the curve for `w = 1` kept as a faint reference.

Drag `w` from 1 to 10 and watch the token grow to a third of the row while the curve on the right jumps from a slow climb to a near-certain rematch within five fights. Then drag `R` up to 200 and watch how much weight it takes to get the curve back. The per-encounter view makes memory look like a small tweak. The cumulative view shows it is the difference between a rival and a stranger.

### Cross-game recognition

Many systems that produce emergent stories either shrink `R` or raise `w`. Rewrite them in those terms and they line up.

**Middle-earth: Shadow of Mordor (2014).** The game splits its orcs in two. Generic Uruks fight in crowds and are forgotten, with `R` effectively huge. The Nemesis System tracks only the Uruks who do something notable, such as killing the player or surviving a fight, and promotes them to captain. That shrinks the cast that can recur from every orc on the map to a short list of named captains. Killing the player also makes the captain stronger and raises his standing, which acts like a large `w` applied at the moment a story starts. Week 2 looked at the same system as a way to generate callback lines. Callbacks only pay off if the rematch happens, which is what `w` buys.

**RimWorld (Ludeon Studios, current 1.x versions).** The default Crashlanded scenario starts with three colonists, chosen from eight offered. The Lost Tribe scenario starts with five. Every event in the game happens to this cast, so `R` is tiny and every character recurs in almost every story. RimWorld's stories are about the same three people because there are only three people. Growth of the colony is growth of `R`, and long-running colonies make stories about fewer characters feel sharper by losing some of them.

**EVE Online (2003 onward).** The server holds tens of thousands of players, so `R` for random strangers is enormous and chance meetings rarely recur. Players shrink `R` themselves by joining corporations, alliances and coalitions, which fight the same enemies again and again. B-R5RB was a battle between two coalitions with a long shared history. The players built the cast.

**Your typical online RPG zone.** Hundreds of respawning enemies with `w = 1`. The model predicts what players feel: no individual enemy is ever met twice on purpose, so the story lives in the quests (week 8) rather than in the fights. That is a valid choice, but it is a choice.

### Eyes-open design judgment

- **Small `R` is cheap and strong.** A small cast needs no special memory system. The cost is variety: players see the same faces, and each face must carry more writing and more animation.
- **High `w` is powerful and has a failure mode.** A player who keeps losing to the same enemy meets him more and more. A rival is fun at 1 or 2 losses and punishing at 5. Cap `w`, decay it over time, or make the rival easier to beat on each rematch to leave the player a way out.
- **Memory must be shown to count.** A weight that the player never notices does nothing for the story. Pair every weighted rematch with a visible sign of memory: a scar, a taunt, a changed rank. Week 4's flags and week 2's callbacks are the writing side of `w`.
- **Emergent does not mean unplanned.** You chose `R`, `w`, what counts as a memorable event, and what the game shows. Those choices are authored. What you give up is control over which story any one player gets.
- **In online games, players are the cast.** You cannot weight which strangers meet. You can make small groups persistent and visible: guilds, rivalries tracked by the game, server-wide event histories. MMO305 covers the social side.

## 3. Shaping emergence: storytellers and pacing

Cast and memory decide who the story is about. Pacing decides how it feels. GD201 week 3 built the model for pacing: an intensity stock that rises with threat and decays over time, and Left 4 Dead's AI Director, which cycles through build up, sustained peak, fade and a relax period of 30 to 45 seconds. Emergent-story games use the same idea at a larger scale.

**RimWorld's storytellers** are the clearest case. The player picks one of three, and the choice sets how events are paced.

- **Cassandra Classic**, the default, alternates fixed phases. From day 11, she runs a 4.6-day "on" phase in which she sends one or two major threats (50-50), at least 1.9 days apart, then a 6-day "off" phase. The cycle repeats every 10.6 days, which works out to about 8.5 major threats per 60-day RimWorld year.
- **Randy Random** fires an event on average every 1.35 days, drawn from weighted categories, with no on and off phases and no spacing rule. He also multiplies raid strength by a random factor from 0.5 to 1.5. If 13 days pass without a major threat, his next event is forced to be one. The wiki's calculation puts his average gap between major threats at about 7.1 days.

Notice the numbers. Cassandra averages about 1.5 major threats per 10.6-day cycle, about one per 7.1 days. Randy averages about one per 7.1 days too. **The two storytellers send major threats at almost the same average rate.** Players still describe them as different games, because Randy can send two strong raids back to back and then nothing for nearly two weeks. That is week 7's lesson again, in a different place: same mean, different tail, and the tail is what players tell stories about.

So the storyteller is a designer's lever on emergent narrative. Cassandra's fixed rhythm produces stories with a recognizable shape (rise, crisis, recovery), because the rules force breathing room between crises. Randy produces rarer, stranger stories: the colony that survived three raids in four days, or the one that never saw it coming. RimWorld lets the player choose which kind of story they want, which is itself a design decision about emergent narrative.

## 4. Retelling: the fourth ingredient

An emergent story that nobody retells is lost. Boatmurdered exists because the players wrote it down, one year at a time. B-R5RB exists as a story because players and the press told it.

Designers can help without writing the story themselves.

- **Record what happened.** A log of notable events, with names, dates and causes, gives players the raw material for a telling. The events to log are the ones that touch the four ingredients: a cast member dies, a memory is formed, something built is lost.
- **Name things.** Named characters, places and objects are easier to retell than "a raider" or "the base".
- **Make the moment shareable.** Screenshot modes, replays and exportable logs let players carry the story out of the game.
- **Leave gaps.** Players fill gaps with their own interpretation. A chronicle that explains everything leaves nothing to tell. Week 10 returns to this when it discusses lore delivery.

In an online world, retelling also spreads across players. One player's rival can become a server's legend, and a guild's war can become the game's history. That shared memory is the MMO version of the fourth ingredient, and week 13 takes up the problem of whose story it is.

## In-class activity (25 minutes)

Work in groups of three. You are designing a rival system for a small online RPG zone that has 40 named bandit lieutenants and 200 generic bandits.

1. **(5 min)** Decide the cast. Which characters can become rivals: the 40 lieutenants, the 200 bandits, or a subset? State `R`.
2. **(5 min)** Choose `w` so that a player who loses to a rival has at least a 60% chance of meeting him again within 8 encounters. Use the formula or the interactive. (For `R = 40`, `P needed = 1 − 0.4^(1/8) = 0.108` and `w needed = 0.108 × 39 / 0.892 = 4.7`, so 5.)
3. **(10 min)** Write the rival's memory in four lines: one for the first rematch, one for a second rematch, one if the player wins, and one if the player loses again. Each line must refer to what happened last time without naming specific numbers or items (so it works for any encounter).
4. **(5 min)** Name one way the system could frustrate a player and the rule you would add to prevent it.

Expected output: `R`, `w` with the calculation, four lines of rival dialogue, and one safeguard rule.

## Common misconceptions

- **"Emergent narrative means the designer does nothing."** The designer chooses the cast, the memory, the stakes and the pacing. What emerges is which story each player gets, not whether stories are possible.
- **"Memory is enough."** A remembered character the player never meets again produces no story. Memory needs recurrence, and recurrence needs a small `R` or a high `w`.
- **"More characters means more stories."** More characters means more events, spread over more faces. Past a point, a larger cast lowers the chance that any one story continues.
- **"Random storytellers are harder."** Randy and Cassandra send major threats at about the same average rate. Randy's difference is spread, not volume.

## Check yourself

1. A game has a cast of 30 captains and gives the player's killer a weight of 6. What is the chance of a rematch in the next encounter? Within the next 5?
2. You want a 75% chance of a rematch within 4 encounters on a cast of 12. What is the smallest whole `w`?
3. A designer doubles the cast from 20 to 40 to "add variety" and keeps `w = 5`. By how much does the chance of a rematch within 5 encounters fall? What `w` would restore it?
4. Explain, using the storyteller numbers in section 3, why a player could lose a colony to Randy that would have survived Cassandra, even though both send major threats at about the same average rate.

<details>
<summary>Answers</summary>

1. `P = 6 / (29 + 6) = 6/35 = 0.171`. `P_5 = 1 − (29/35)^5 = 1 − 0.391 = 0.609`, so about 61%.
2. `P needed = 1 − 0.25^(1/4) = 1 − 0.707 = 0.293`. `w needed = 0.293 × 11 / 0.707 = 4.56`, so `w = 5`. Check: `P = 5/16 = 0.3125`, `P_4 = 1 − 0.6875^4 = 0.777`.
3. At `R = 20, w = 5`, `P_5 = 0.689`. At `R = 40, w = 5`, `P = 5/44 = 0.114` and `P_5 = 1 − 0.886^5 = 0.453`. The chance falls by about 24 points. To restore `P = 5/24` with `R = 40` you need `w / (39 + w) = 5/24`, so `w = 195/19 ≈ 10.3`, a weight of about 10. Doubling the cast roughly doubles the weight needed.
4. Cassandra's rules force at least 1.9 days between major threats and a 6-day off phase after each on phase, so a colony always gets time to recover. Randy has no spacing rule and can multiply raid strength by up to 1.5, so two strong raids can arrive with no recovery between them. The average rate is the same. The worst case is not, and colonies die in the worst case.

</details>

## Lab / assignment hook

[Lab 09, stranger to rival](../labs/lab09.md). You implement the recurrence model, check it against a Monte Carlo simulation, and build a tiny nemesis system that promotes and remembers characters and logs every rematch. You then tune `R` and `w` for a zone of your own and write the rival's memory lines. The rival design feeds your final quest chain.

## Sources

- Aylett, R. (1999). "Narrative in Virtual Environments: Towards Emergent Narrative." *Narrative Intelligence: Papers from the AAAI Fall Symposium*, technical report FS-99-01, AAAI Press. The clash between pre-scripted narrative and user freedom in a virtual environment; emergent narrative proposed as a way around it. https://cdn.aaai.org/Symposia/Fall/1999/FS-99-01/FS99-01-014.pdf
- Jenkins, H. (2004). "Game Design as Narrative Architecture." In Wardrip-Fruin, N. and Harrigan, P. (eds.), *First Person*, MIT Press. The enacted, embedded and emergent categories, as taught in GS101 week 13.
- Wikipedia, "Boatmurdered". Dwarf Fortress succession game, November 2006 to March 2007; 14 Something Awful forum members; one in-game year each.
- Wikipedia, "Bloodbath of B-R5RB". 27 to 28 January 2014; missed sovereignty payment; over 7,548 characters, peak 2,670 in system; about 21 hours, ended by server maintenance; about 11 trillion ISK, estimated at 300,000 to 330,000 US dollars.
- Wikipedia, "Middle-earth: Shadow of Mordor". Monolith Productions; released 30 September 2014; generic Uruks versus tracked Uruks; the Nemesis System promotes Uruks who kill the player or survive an encounter to captain and lets survivors remember encounters; US patent 10,926,179 granted to Warner Bros. in February 2021.
- RimWorld Wiki, "AI Storytellers", "Cassandra Classic" and "Randy Random" (game versions 1.5 and 1.6, as of 2026). Cassandra: first on phase day 11, on 4.6 days, off 6.0 days, minimum spacing 1.9 days, 1 to 2 threats per on phase, about 8.5 major threats per year. Randy: event mean time 1.35 days, 13-day maximum without a major threat, raid points factor 0.5 to 1.5, about 7.14 days between major threats. https://rimworldwiki.com/wiki/AI_Storytellers
- RimWorld Wiki, "Scenario system". Crashlanded starts with three people chosen from eight; Lost Tribe with five. https://rimworldwiki.com/wiki/Scenario_system
- Booth, M. (2009). "The AI Systems of Left 4 Dead." Valve, keynote at AIIDE 2009. Director cycle of build up, sustain peak, peak fade and a 30 to 45 second relax period. Used here only through GD201 week 3.
- The cast sizes, weights and bandit zone in the worked example and activity are invented for teaching.

## Interactive spec: examples/w09-rival-recurrence.html

**The one insight.** A memory weight that looks tiny per encounter decides whether a stranger becomes a rival. On a cast of 20, raising `w` from 1 to 10 takes the chance of a rematch within five fights from 23% to 88%, the same as having a cast of only three.

**Layout.** Two linked views side by side on wide screens, stacked on phones.
- **Left view, "One encounter".** A horizontal strip divided into `R` segments. The remembered character's segment has width proportional to `w`; all others have width proportional to 1. Color the remembered segment with the accent color and label it "your rival"; draw the others in a neutral tone (for `R > 60`, draw the others as one hatched block labeled "R − 1 others"). Above the strip, the large number `P` per encounter as a percentage.
- **Right view, "The next k encounters".** Line chart of `P_k = 1 − (1 − P)^k` for `k = 1 … 30`. The current setting as a solid line, the `w = 1` curve for the same `R` as a faint dashed reference, and a horizontal target line at the target chance. Mark the current `k` on the curve with a dot and its value.
- **Number panel:** `R`, `w`, `P`, `P_k` at the current `k`, mean wait `(R − 1 + w)/w`, and "weight needed for target" computed from the formula (show both the exact value and the rounded-up whole number).

**Controls.**
- Slider `R` (2 to 500, step 1, default 20; use a log-feel mapping so 2 to 50 gets half the track).
- Slider `w` (1 to 100, step 1, default 1).
- Slider `k` (1 to 30, default 5).
- Slider "target chance" (10% to 99%, default 50%).
- Presets: "Stranger (20, 1)", "Nemesis (20, 10)", "Small colony (3, 1)", "Busy zone (200, 1)", "Busy zone, weighted (200, 50)".
- Button "Run 1,000 players": simulate 1,000 players for the current `R`, `w`, `k` with a seeded generator, and show the observed share with a rematch next to `P_k` (they should agree within about 3 points).

**Formulas.**
- `P = w / (R − 1 + w)`.
- `P_k = 1 − (1 − P)^k`.
- Weight needed: `P* = 1 − (1 − target)^(1/k)`, `w* = P* (R − 1) / (1 − P*)`, shown rounded up to a whole number (minimum 1).

**Test values.**
- (20, 1): `P = 0.050`, `P_5 = 0.2262`, `P_10 = 0.4013`, wait 20.0.
- (20, 5): `P = 0.2083`, `P_5 = 0.6890`, wait 4.8.
- (20, 10): `P = 0.3448`, `P_5 = 0.8793`, `P_10 = 0.9854`, wait 2.9.
- (3, 1): `P = 0.3333`, `P_5 = 0.8683`.
- (200, 1): `P_5 = 0.0248`. (200, 50): `P_5 = 0.6740`, wait 4.98.
- Weight needed for 50% within 5: `R = 20` gives 3 (exact 2.83); `R = 200` gives 30 (exact 29.59).
- Check yourself Q1: (30, 6) gives `P = 0.1714`, `P_5 = 0.6095`.

**First screen.** Preset "Stranger (20, 1)" with the dashed reference hidden behind the solid line, and a one-click hint chip "Now try w = 10". The number panel shows 22.6% within 5 encounters.
