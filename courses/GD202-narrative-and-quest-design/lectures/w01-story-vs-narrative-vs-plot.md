# GD202 · Week 01 — Story vs Narrative vs Plot in Games

**Why this matters:** When a team says "the story isn't working," they usually mean one of three different things, and each has a different fix. Sometimes the events are weak. Sometimes the events are fine but the player meets them in a confusing order. Sometimes the player is never shown them at all. Designers who can name the layer that failed fix the right thing on the first try.

**You will be able to:**
- Separate any game's storytelling into story (what happened), plot (the order the player meets it) and narration (how each piece is delivered), and name who controls each layer.
- Compute how far a telling departs from chronological order, as an inversion count and a scramble index between 0 and 1.
- Compare fixed-order, player-ordered and systemic plots in shipped games, and predict what each costs in writing and testing.
- Design a plot order for a short backstory that produces a chosen effect (surprise, suspense or dramatic irony).

**Before class:** Bateman (ed.), *Game Writing: Narrative Skills for Videogames*, 2nd ed. (2021), the opening chapter on what game writers do and the chapter on nonlinear structure (the course reader lists the pages). Play Her Story for 30 minutes if you can, or watch a spoiler-free video of its first ten minutes. Read the Wikipedia article "Fabula and syuzhet" (10 minutes).

**Prerequisites from earlier courses:** [GD101 week 4, MDA](../../GD101-introduction-to-game-design/lectures/w04-mda-mechanics-dynamics-aesthetics.md) gave you the habit of tracing a feeling back to a rule. This week does the same for feelings about story. [GS101 week 13, ludology vs narratology](../../GS101-history-and-critical-study-of-games/lectures/w13-ludology-vs-narratology.md) covered the academic debate and Jenkins's four kinds of game narrative (evocative, enacted, embedded, emergent). This lecture uses those terms without re-teaching them.

**Interactive:** [`examples/w01-plot-order.html`](../examples/w01-plot-order.html). Keep it open during section 2.

---

## 1. Three words that people use as one

Ask five developers what "the story" of a game is and you will get five answers. One will summarize the backstory. One will describe the cutscenes. One will tell you about the time their character got lost in a swamp and was rescued by a stranger. All three are talking about something real, and they are not talking about the same thing.

This course uses three terms, and it uses them the same way every week.

**Story** is the set of events in the fictional world, in the order they happened in that world. A murder at midnight, a confession at dawn, a trial a month later. The story does not care when or whether anyone finds out. Literary theorists in the Russian Formalist tradition of the early twentieth century called this layer the **fabula**.

**Plot** is the order in which the audience meets those events. A detective novel may open with the trial and reveal the murder last. The events are the same, the plot is different. The Formalists called this layer the **syuzhet**. Film and literature scholars later wrote it as the distinction between story and discourse (Seymour Chatman's 1978 book uses those two words as its title).

**Narration** is how each piece reaches the audience. A cutscene, a line of dialogue, a note on a corpse, a bloodstain on a wall, a quest log entry, an item description. Two games can share story and plot and still feel nothing alike, because one delivers everything through voiced cinematics and the other through objects lying around a room.

You will also hear **narrative**. In this course "narrative" is the umbrella for the whole system (story, plot and narration together) plus the player's part in it. When a job ad asks for a "narrative designer," it means someone who designs that whole system, not only someone who writes lines.

### The layer only games have

Books and films stop at those three layers. Games add a fourth.

The **play story** is the sequence of events that happened during your play session. It includes things nobody wrote: you died three times on the bridge, you sold your sword to afford a horse, your guild wiped on a boss at 1% health. Play stories are the stories players tell each other. Jenkins's "emergent narrative," which you met in GS101 week 13, is what we get when the play story becomes the main thing a game offers.

The four layers let you ask one sharp question about any game:

> Who controls each layer: the writer, the player, or the rules?

In a novel, the writer controls all of them. In a film, the writer and director do. In games, control splits. That split is the subject of this whole course, and this week you learn to measure one part of it.

### A quick diagnostic

When a playtester says "I don't get the story," run through the layers in order.

| Symptom from playtest | Layer that failed | Typical fix |
|---|---|---|
| "I understood what happened but I didn't care." | Story | Rewrite events, raise stakes, change who wants what. |
| "I only understood it at the end, and then it was too late." | Plot | Move a key event earlier, or add a reminder. |
| "I never found out why the village burned." | Narration | Deliver the event somewhere the player actually goes. |
| "I did something cool and the game ignored it." | Play story | Let the game acknowledge the player (week 2). |

This table is the most useful thing in the lecture for your future job. Most story arguments on a team are really plot or narration arguments, and they go nowhere until someone names the layer.

## 2. Worked example: who wrote the plot of Her Story?

### The hook

Her Story (Sam Barlow, June 2015, iOS, OS X and Windows) gives you an old police desktop and a database of 271 short video clips cut from seven police interviews recorded in 1994. You cannot watch an interview from start to finish. You type a word, the database returns the clips whose transcripts contain it, and you watch them. Then you type another word.

Every player sees the clips in a different order. Your friend may see the most shocking clip in her first ten minutes. You may see it two hours in. The story (what happened in 1994) is fixed, and every clip was written and filmed in advance. The plot is not fixed. The player builds it one search at a time.

So who wrote the plot of Her Story? And how would you even compare one player's plot to another's?

### The model

Number the story events in chronological order, 1 to `n`. A plot is then a list of those numbers in the order the player meets them. A perfectly chronological telling is `[1, 2, 3, ..., n]`.

To measure how far a plot departs from chronological order, count its **inversions**:

```
inversion = a pair of events shown in the opposite order to the order they happened
I = number of inversions in the plot
I_max = n × (n − 1) / 2       (every pair reversed)
scramble S = I / I_max          (0 = chronological, 1 = fully reversed)
```

- `n` is the number of story events you are tracking.
- `I` counts pairs. For each pair of events, ask: did the later event appear first? If yes, that pair is one inversion.
- `I_max` is the number of pairs. With 8 events there are 28 pairs.
- `S` puts different tellings on one scale.

Each inversion is a place where the player learns about something before they learn about its cause. That is exactly where mystery, surprise and dramatic irony come from. An inversion is a small debt the plot owes the player: "you'll find out how this happened later." The scramble index counts the debts.

### Numbers you can check

Here is an invented backstory with eight events. It is short enough to count by hand.

| # | Story event (chronological) |
|---|---|
| 1 | An apprentice arrives at a remote lighthouse. |
| 2 | The keeper and the apprentice argue about the failing lamp. |
| 3 | The apprentice secretly sells lamp oil to smugglers. |
| 4 | On a storm night, the lamp goes dark. |
| 5 | A supply ship wrecks on the rocks. |
| 6 | The keeper is found dead at the foot of the stairs. |
| 7 | A new keeper (the player) arrives. |
| 8 | The new keeper relights the lamp. |

Four ways to tell it:

| Telling | Plot order | Inversions `I` | Scramble `S` |
|---|---|---|---|
| Chronological | 1 2 3 4 5 6 7 8 | 0 | 0.00 |
| In medias res (open on the body) | 6 1 2 3 4 5 7 8 | 5 | 0.18 |
| Mystery (arrive after the wreck, dig back) | 5 6 7 2 3 4 1 8 | 15 | 0.54 |
| Fully reversed | 8 7 6 5 4 3 2 1 | 28 | 1.00 |

Check the second row by hand. Event 6 appears before events 1, 2, 3, 4 and 5, so it creates five inversions. Every other pair is in story order. `I = 5` and `S = 5/28 = 0.18`.

Check the third row. Events 5, 6 and 7 each appear before 2, 3, 4 and 1, which gives 4 + 4 + 4 = 12. Then 2, 3 and 4 each appear before 1, which adds 3. Total 15, and `15/28 = 0.54`.

Here is the same calculation in code. It runs as shown with `.venv/bin/python`.

```python
def inversions(plot):
    """Count pairs the telling shows in the opposite order to the story."""
    count = 0
    for i in range(len(plot)):
        for j in range(i + 1, len(plot)):
            if plot[i] > plot[j]:
                count += 1
    return count

def scramble(plot):
    n = len(plot)
    return inversions(plot) / (n * (n - 1) // 2)

tellings = {
    "chronological": [1, 2, 3, 4, 5, 6, 7, 8],
    "in medias res": [6, 1, 2, 3, 4, 5, 7, 8],
    "mystery":       [5, 6, 7, 2, 3, 4, 1, 8],
    "reverse":       [8, 7, 6, 5, 4, 3, 2, 1],
}
for name, plot in tellings.items():
    print(f"{name:14} {inversions(plot):2d} {scramble(plot):.2f}")
```

Output:

```
chronological   0 0.00
in medias res   5 0.18
mystery        15 0.54
reverse        28 1.00
```

Notice what the numbers say about design. The in medias res opening has only five inversions, and all of them hang on one event. It is a single, big promise ("you'll learn how he died"). The mystery telling has three times as many, spread across the whole backstory. It asks the player to hold more open questions at once. That is more engaging for a player who enjoys puzzles and more tiring for one who does not.

### A visual you can move

Open [the interactive](../examples/w01-plot-order.html). The top row shows the plot, the cards in the order the player meets them. The bottom row shows the story, the same cards in chronological order. A line joins each card to its twin. **Every crossing between two lines is one inversion.** Drag cards in the top row to reorder them and watch crossings appear and disappear, with `I` and `S` updating beside the picture.

Then press "Simulate a Her Story player." The tool reveals cards in a random order, as a player's searches might, and draws the crossings live. Press it five times. Five players, five plots, one story. Most random orders land near `S = 0.5`, because a random list reverses about half its pairs. Designers of player-ordered games do not control where a single player lands. They control which orders are possible.

### Cross-game recognition

The same split between a fixed story and a variable plot shows up across very different games. In each case, ask who decides the plot order.

**Outer Wilds (Mobius Digital, 2019).** The solar system resets every 22 minutes. Nothing you carry survives a reset except the ship's computer log, which records what you have learned and can display it as a web of connections. The story (what an ancient civilization did, long ago) is fixed. The plot is the order you discover it, and it is set by where you choose to fly. The ship's log is a plot-management tool. It lets the player hold many inversions at once without forgetting them, which is the tiring part of a high-scramble plot.

**The Walking Dead: 400 Days (Telltale Games, July 2013).** This add-on episode tells five short stories, and the player can approach them in any order. The designers made each story self-contained enough that any order works. That is a coarse version of the Her Story design. The player orders five blocks instead of 271 clips.

**The Odyssey (Homer, ancient epic).** The poem opens late in the story, with Odysseus stranded far from home, and much of his earlier voyage reaches the audience later, as a story he tells at a feast. That is in medias res, the same move as our second telling, three thousand years old. The difference from Her Story is who holds the plot. In the Odyssey the poet does. In Her Story the player does, clip by clip.

Rewrite each of these in the model's terms and you get one idea. There is a fixed list of story events. There is an order of presentation. Someone (writer, player or rules) chooses that order, and the inversions it creates are where curiosity lives.

### Eyes-open design judgment

Player-ordered plots are fashionable, and they have real costs. Decide deliberately.

- **Every piece must stand alone.** In a fixed plot, clip 40 can lean on clip 39. In a player-ordered plot, any clip may be the first one a player sees, so each must make sense with no setup. Writers lose the cheapest tool they have (the line that builds on the previous line).
- **Spoilers become possible inside your own game.** If the player can reach the revelation first, the revelation stops working. Her Story's answer is the search interface itself. You must guess words to find clips, so the most revealing clips are found only by players who already suspect something. The interface controls the plot without fixing it.
- **Testing explodes.** A fixed plot has one order to test. A player-ordered plot of 8 blocks has `8! = 40,320` orders. You cannot test them all, so you design pieces that are robust to order and test the extremes (the revelation first, the revelation last).
- **High scramble tires players.** Each inversion is an open question. Give players a tool that holds the questions for them (Outer Wilds' log, a journal, a case board) or keep `S` moderate.
- **Low scramble is not a failure.** A chronological plot with one strong in medias res opening is the right choice for most quest content, where players arrive, act and leave. Save high scramble for content that is about discovery.

### Check the model

1. A cutscene opens with event 8 of an 8-event story, then plays 1 to 7 in order. What are `I` and `S`?
2. You want a plot with exactly one inversion. Describe how to build it. Where would you put that inversion to get the most suspense?

<details>
<summary>Answers</summary>

1. Event 8 appears before seven later-shown events, so `I = 7` and `S = 7/28 = 0.25`.
2. Swap two adjacent events. The strongest single inversion usually shows an effect just before its cause near a key moment, for example showing the dark lamp (4) one beat before the oil sale (3), so the player sees the consequence and then learns who caused it.

</details>

## 3. Narration: the delivery layer

Story and plot say what the player learns and when. Narration says how. Games have more delivery channels than any other medium, and each channel has its own cost and its own reach.

| Channel | Example | Can the player miss it? | Relative cost |
|---|---|---|---|
| Cutscene | A scripted camera sequence | Rarely (often skippable) | High (animation, voice, camera) |
| Dialogue | A conversation with a character | Sometimes | Medium |
| Text in the world | Notes, logs, item descriptions | Often | Low |
| Environmental | A burned house, a trail of footprints | Often | Medium (art and level time) |
| Systemic | A faction that attacks you because you robbed them | Depends on play | Medium to high (design and code) |

Two principles follow.

**The channel changes the plot.** A cutscene arrives when the designer says. A note on a corpse arrives when the player walks past the corpse, if they do. So choosing a channel is also choosing who controls the plot position of that event. When you move an event from a cutscene into a note, you have handed its plot position to the player. Your scramble index is no longer yours to set.

**The channel changes the audience.** Only a fraction of players read optional text. That is fine for flavor and fatal for anything the player needs to understand the ending. A rule used by many teams, and one you will practice in week 10, is to put anything the player must know in a channel they cannot miss, and put the depth in channels they can.

## 4. The play story and the MMO problem

In a single-player game, the play story is private. In an online game it is shared. That changes how story, plot and narration work.

**Plot order is out of your hands at scale.** A zone in an online RPG usually offers several quests at once, and players take them in whatever order they like. Two friends in the same zone will meet its backstory in different orders, just like two Her Story players. Quest writers therefore write each quest so it works first, middle or last, and they reserve fixed order for the few beats that must come in sequence. You will build this in week 8, on quest chains and zone storytelling.

**The world cannot have one plot for everyone.** If the dragon dies in your story, it cannot also be alive for the player standing next to you who has not reached that quest yet. Online games solve this with techniques you will meet in week 13 (instancing, phasing, personal story versus world story).

**Play stories are the product.** Players remember the raid, the betrayal, the trade that made them rich. None of those were written by a writer. A narrative designer on an online game spends much of their time building the conditions for good play stories, which is week 9's topic, emergent narrative.

So the four-layer model does real work. It tells you which layer you control, which layer the player controls and which layer the rules control, before you write a single line.

## 5. Choosing a plot order on purpose

Once you can count inversions, you can design with them. Three effects come from three different arrangements. The terms come from film and theater, and they carry over directly.

**Surprise.** The player learns a cause after its effect, and the cause is unexpected. You need at least one inversion, placed so the late event reframes earlier ones. In the lighthouse story, holding back event 3 (the oil sale) until after the player has met the apprentice as a sympathetic character creates surprise.

**Suspense.** The player knows something bad is coming and waits for it. Suspense comes from showing an effect early (an inversion) and then playing the lead-up in order. The in medias res telling does exactly this. The player sees the body first, then watches the storm approach.

**Dramatic irony.** The player knows something a character does not. In games this is common and strong, because the player is also a character. If a note tells you the apprentice sold the oil, and the apprentice later asks you for help, your choice in that conversation carries the irony.

A useful practice for any quest or backstory you write is to plan the plot as a list of event numbers before you write prose. Compute `I`. Mark where each inversion resolves. If an inversion never resolves (the player never learns the cause), decide whether that is a deliberate open question or a hole.

### A note on time

Plot order is one of two ways a telling bends time. The other is duration. A story can cover years in one line of text or stretch one second across a slow-motion cutscene. The narratologist Gérard Genette catalogued these moves for novels in the 1970s. Games add a third clock, play time. Outer Wilds shows it neatly. Each loop covers 22 minutes of story time, while a full playthrough takes many hours of play time spread across dozens of loops. You will use this distinction in week 8, when you pace a zone so that story beats land at the right play-time intervals.

## In-class activity (25 minutes)

Work in pairs. Materials: eight index cards per pair, a pen, the interactive open on one laptop.

1. **(5 min)** Write an eight-event backstory for a small quest location of your choice (a farm, a mine, an abandoned camp). One event per card, numbered 1 to 8 in story order. Keep it original, no existing characters.
2. **(8 min)** Produce three plot orders: one for surprise, one for suspense, one for dramatic irony. For each, compute `I` and `S` by hand, then check them in the interactive.
3. **(7 min)** For your highest-scramble telling, assign a narration channel to each event (cutscene, dialogue, note, environment). Circle every event whose channel lets the player miss it. For each circled event, answer: if the player misses it, does any inversion stay unresolved?
4. **(5 min)** Swap with another pair. Read only their plot order (not the story order) and try to reconstruct the story. Report which event confused you.

Expected output: three plot orders with `I` and `S`, a channel map, and one confusion the other pair found.

## Common misconceptions

- **"Story and plot are the same thing."** Story is what happened. Plot is the order you learn it. You can change either without changing the other, and the fixes for each are different.
- **"A nonlinear game has no plot."** Every play session has a plot, the order that player met the events. A player-ordered game has many plots, and the designer controls which ones are possible.
- **"More scramble is more sophisticated."** High scramble adds open questions and cognitive load. It suits discovery games and hurts content the player must understand to act.
- **"If it's in the game, the player knows it."** Only events delivered through a channel the player cannot miss are guaranteed to reach them. The rest are optional plot.

## Check yourself

1. A plot of 6 events is `[3, 1, 2, 6, 4, 5]`. Compute `I` and `S`.
2. A designer moves event 2 of a story from a cutscene into an optional note. Which of the four layers changed, and what happens to the plot for players who skip the note?
3. A game offers 5 quests in a zone, playable in any order. How many different plot orders of those quests are possible? What does that imply for writing each quest?
4. Two tellings of the same 8-event story both have `I = 7`. Must they feel the same to a player? Give an example of two orders with `I = 7` that feel different.

<details>
<summary>Answers</summary>

1. Pairs out of order: (3,1), (3,2), (6,4), (6,5). `I = 4`, `I_max = 15`, `S = 4/15 = 0.27`.
2. Narration changed (the channel), and with it control of plot position moved to the player. Players who skip the note never learn event 2, so any inversion that depends on it never resolves for them. Their plot has a hole.
3. `5! = 120` orders. Each quest must make sense whether it comes first or last, so it cannot depend on setup from another quest in the set unless you gate it.
4. No. `[8, 1, 2, 3, 4, 5, 6, 7]` puts all seven inversions on one event, a single big promise that builds suspense. `[3, 2, 1, 6, 5, 4, 8, 7]` also has `I = 7` (3 + 3 + 1), but spreads them across three small local reversals. That reads as choppy editing rather than suspense. The count measures how much the telling departs from story order, not where.

</details>

## Lab / assignment hook

[Lab 01, plot order audit](../labs/lab01.md). You will log the order in which you discover the backstory in a game of your choice, compute its inversions with a small script, then write two alternative plot orders for your own backstory and justify each by the effect it produces. It is the first of the dialogue exercises (40% of the course grade).

## Sources

- Wikipedia, "Her Story (video game)" (accessed September 2026). Release on 24 June 2015 for iOS, OS X and Windows; seven fictional police interviews from 1994; a database of 271 clips searchable by transcript words; interviews cannot be watched in full; developed by Sam Barlow after leaving Climax Studios.
- Wikipedia, "Outer Wilds" (accessed September 2026). Mobius Digital, 2019; 22-minute time loop; only the ship's computer log persists across loops and can display discoveries as a web of connections.
- Wikipedia, "The Walking Dead (video game)" (accessed September 2026). Telltale Games; 400 Days released July 2013 as downloadable content.
- Walking Dead Wiki, "400 Days" (accessed September 2026). Five linked stories that can be played in any order, joined by an epilogue. https://walkingdead.fandom.com/wiki/400_Days
- Wikipedia, "Fabula and syuzhet" (accessed September 2026). Terms from the Russian Formalists (Propp, Shklovsky), early twentieth century; fabula as chronological events, syuzhet as the order of telling.
- Chatman, S. (1978). *Story and Discourse: Narrative Structure in Fiction and Film*. Cornell University Press.
- Genette, G. (1980). *Narrative Discourse: An Essay in Method* (English translation of the 1972 French text). Cornell University Press. Order and duration as separate dimensions of narrative time.
- Homer, *The Odyssey*. The opening in the middle of events and Odysseus's retelling of his voyage at the court where he is a guest.
- Jenkins, H. (2004). "Game Design as Narrative Architecture." In Wardrip-Fruin & Harrigan (eds.), *First Person*. MIT Press. Covered in GS101 week 13.
- Bateman, C. (ed.) (2021). *Game Writing: Narrative Skills for Videogames*, 2nd ed. Bloomsbury.

## Interactive spec: examples/w01-plot-order.html

**The one insight.** The story stays fixed while the plot changes, and every place where the telling runs against the story shows up as a visible crossing of lines. The number of crossings is the inversion count `I`.

**Layout.** Two linked views, stacked on mobile (below 700px), side by side above.

- **View A, "Two timelines."** Two horizontal rows of 8 cards. Top row labelled "Plot (the order the player meets it)". Bottom row labelled "Story (the order it happened)", always sorted 1 to 8. Each card shows its story number and a short label from the lighthouse table (for example "3 · Oil sold"). A straight or gently curved line joins each top card to its twin below. Lines that cross each other are drawn in the accent color; lines with no crossings are neutral. At each crossing point draw a small dot.
- **View B, "The numbers."** A readout panel: `I = <count>`, `I_max = 28`, `S = <I/28 to 2 decimals>`, and a horizontal bar from 0 to 1 with a marker at `S` and tick labels at the four presets. Under it, a list "Open questions at each step": for plot position `p` from 1 to 8, the number of events already shown whose cause (any smaller story number) has not yet been shown. Show it as a small bar chart of 8 bars.

**Controls.**
- Drag and drop cards in the top row (pointer and touch). Keyboard: focus a card with Tab, move it left or right with the arrow keys, announced through an `aria-live` region ("Oil sold moved to position 3. Inversions 6.").
- Preset buttons: "Chronological", "In medias res", "Mystery", "Reversed". These load the four orders from the lecture's table.
- Button "Simulate a Her Story player": resets the top row to empty and reveals the 8 cards one at a time in a uniformly random order (Fisher-Yates with a visible seed number), about 400 ms per card, instantly if `prefers-reduced-motion`. Lines and counts update as each card appears. `I` counts only pairs already revealed.
- Button "Show 200 random players": computes `S` for 200 random permutations (seeded) and draws a small histogram under View B, with the current order's `S` marked. Mean of the sample is printed.
- Optional text field to rename the 8 labels so students can load their own backstory in class.

**Formulas.**
- `I = count of pairs (i < j) with plot[i] > plot[j]`.
- `I_max = n(n − 1)/2`, `S = I / I_max`.
- Open questions at position `p`: number of shown events `e` such that some `c < e` is not yet shown. (This is a simple proxy for "effects whose causes are still unknown.")
- Expected `S` of a uniformly random permutation is 0.5; show "Random players average about 0.50" as a caption next to the histogram.

**Test values (must match).**

| Preset | Order | I | S |
|---|---|---|---|
| Chronological | 1 2 3 4 5 6 7 8 | 0 | 0.00 |
| In medias res | 6 1 2 3 4 5 7 8 | 5 | 0.18 |
| Mystery | 5 6 7 2 3 4 1 8 | 15 | 0.54 |
| Reversed | 8 7 6 5 4 3 2 1 | 28 | 1.00 |
| Check-yourself Q1 of section 2 | 8 1 2 3 4 5 6 7 | 7 | 0.25 |

Open-questions bars for "In medias res" must read `1, 1, 1, 1, 1, 0, 0, 0` (event 6 stays open until 5 is shown). For "Chronological" all bars are 0.

**Accessibility and style.** Crossing lines differ from non-crossing lines in both color and dash pattern. Every number is live text. Use the shared tokens from `templates/interactive-tokens.css`. No game art; cards are plain rectangles with text.
