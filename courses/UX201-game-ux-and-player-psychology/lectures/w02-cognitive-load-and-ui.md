# UX201 · Week 02 — Cognitive Load and UI

**Why this matters:** Players judge an interface by how much thinking it costs them, not by how many buttons it takes. Teams that count clicks keep shipping menus that are short on paper and slow in the hand. This week gives you a way to count the thinking, so you can cut the effort the interface adds and keep the effort the game is supposed to demand.

**You will be able to:**
- Classify a player's mental effort as intrinsic, extraneous or germane load, and say which kind a design change removes.
- Compute the time of an interface task with the keystroke-level model, including mental operators and a scan cost from week 1.
- Compare interface designs for novices and experts and explain why the fastest design for one can be the slowest for the other.
- Redesign a screen to reduce split attention and working-memory load, and justify each change with the model.

**Before class:** Celia Hodent, *The Gamer's Brain* (CRC Press, 2017), the chapter "Usability" (pp. 109-134), and reread "Memory" (pp. 35-50). The Wikipedia article "Keystroke-level model" (short, and enough to follow the operator table). Optional: Card, Moran and Newell, *The Psychology of Human-Computer Interaction* (1983), the chapter introducing the keystroke-level model.

**Prerequisites from earlier courses:** [UX201 week 1, perception, attention and memory](w01-perception-attention-memory.md), especially the search model `T = a + k × N` and the four-chunk working memory limit. [GD101 week 12, feedback, juice, clarity and readability](../../GD101-introduction-to-game-design/lectures/w12-feedback-juice-clarity-readability.md), where the Hick-Hyman law priced choices among warnings. [GD101 week 9, choice and meaningful decisions](../../GD101-introduction-to-game-design/lectures/w09-choice-and-meaningful-decisions.md), which gives you the difference between a decision that is the game and one that is just an obstacle.

**Interactive:** [Inputs vs time: a KLM comparison of four designs](../examples/w02-klm-load.html). Use it during section 2.

---

## 1. Three kinds of load

**Cognitive load** is the amount of working memory a task uses. John Sweller developed cognitive load theory in the late 1980s while studying how students solve problems. His starting point was the limit you met last week. Working memory holds only a few chunks, so anything that fills it with the wrong material leaves less room for the right material.

The theory splits load into three kinds. Each has a direct game translation.

- **Intrinsic load** comes from the task itself. In a game, it is the challenge you designed on purpose: reading the boss, choosing a target, planning a build. Chandler and Sweller introduced the term in 1991.
- **Extraneous load** comes from the way information is presented, and the designer controls it. In a game, it is interface friction: hunting through a menu, cross-referencing two screens, remembering what an unlabelled icon means.
- **Germane load** is effort spent building understanding, the work of turning experience into skill. In a game, it is the player learning your systems.

The design rule follows directly. **Cut extraneous load. Tune intrinsic load. Protect germane load.** Every unit of working memory the menu uses is a unit the player can't spend on your boss or on learning your game.

This rule has a trap in it. Intrinsic load is the game. If you "simplify" a hard decision out of existence, you have made the game easier, not the interface better. So the first skill this week is telling the two apart, and the second is measuring them. For that you need a model that counts thinking, and a model already exists.

## 2. Worked example: count the thinking, not the clicks

### The hook

In The Elder Scrolls V: Skyrim, the inventory already lets you drink any potion and equip any weapon you carry. Yet the game adds a second, much smaller menu. Mark an item as a favourite and it appears in a quick list that opens on the Q key on PC, or the D-pad on a controller. From that list, PC players can bind items to the number keys 1 to 8. Controller players can bind only two.

Why would a team build a menu that contains less than the one they already have? It is last week's hook again, in a new place. And why does the answer differ between keyboard and controller? Counting clicks won't explain either. Counting thinking will.

### The model

The **keystroke-level model** (KLM) was proposed by Stuart Card, Thomas Moran and Allen Newell in 1980 to predict how long a skilled user takes to do a routine task with a given interface. You write the task as a sequence of operators and add up their standard times.

| Operator | Meaning | Standard time |
|---|---|---|
| `K` | Press a key or button. Varies with skill: 0.08 s for an expert typist, 0.28 s for an average non-typist | 0.28 s |
| `P` | Point with a mouse at a target on screen | 1.1 s |
| `B` | Press or release a mouse button (a click is `BB`) | 0.1 s |
| `H` | Move a hand between keyboard and mouse | 0.4 s |
| `M` | Mental preparation: decide what to do next, or retrieve it from memory | 1.35 s |

We add one operator from week 1, because many game menus make you look through a list before you can act:

```
S(N) = e × (N + 1) / 2
```

`S(N)` is the time to find a known item in an unordered list of `N` text entries. The player checks items one at a time and on average finds the target after `(N + 1) / 2` of them. `e` is the time to check one entry. Text must be looked at directly to be read, so `e` is much larger than the lab slopes from week 1. **For this lecture we assume `e = 0.15 s` per entry checked.** That is a teaching value. You will measure a real one in the lab.

Task time is the sum:

```
T = Σ operator times
```

The operator that matters most here is `M`. It is the model's unit of thinking. One `M` costs as much as almost five key presses. KLM's authors gave rules for where to put `M`s, and the core idea is simple. You pay an `M` whenever you must stop and decide or remember, and you skip it when the next step is fully anticipated as part of a chunk you already know. That is where **novices and experts differ**. An expert has chunked "open, tab, tab, down, use" into one unit and pays one `M`. A novice pays an `M` at every decision.

### Numbers you can check

The task: during a fight, drink a fire resistance potion. The player carries 40 items, 12 of them potions. Four interface designs, all invented for this example:

- **A, unsorted list with mouse.** Press a key to open the inventory, find the potion in a list of 40 items whose order changes as you pick things up, click it, press a key to close. Because the order keeps changing, even experts must scan.
- **B, sorted tabs with keyboard.** Open the inventory, press right twice to reach the Potions tab, press down twice to reach the fire potion, press use, press close.
- **C, favourites list.** Press a key to open a short list of 6 favourites, press down twice, press use.
- **D, hotkey.** Press the key bound to the potion.

"Inputs" counts key presses and mouse clicks, the number a click-counting review would use.

| Design | Inputs | Expert operators | Expert time | Novice operators | Novice time |
|---|---|---|---|---|---|
| A, unsorted list | 3 | `M K S(40) P BB K` | 6.29 s | same | 6.29 s |
| B, sorted tabs | 7 | `M` + 7`K` | 3.31 s | 3`M` + 7`K` + `S(12)` | 6.99 s |
| C, favourites | 4 | `M` + 4`K` | 2.47 s | 2`M` + 4`K` + `S(6)` | 4.35 s |
| D, hotkey | 1 | `M K` | 1.63 s | `M` + `S(8)` + `K` | 2.31 s |

Check two rows by hand.

- **A:** `1.35 + 0.28 + 0.15 × 41/2 + 1.1 + 0.2 + 0.28 = 1.35 + 0.28 + 3.075 + 1.1 + 0.2 + 0.28 = 6.285 s`.
- **B, novice:** three decisions (open the inventory, find the right tab, find the potion), seven presses and a scan of the 12 potions. `3 × 1.35 + 7 × 0.28 + 0.15 × 13/2 = 4.05 + 1.96 + 0.975 = 6.985 s`.

The novice using D doesn't yet remember which key holds the potion. They glance at an on-screen bar of 8 slots to find it, `S(8) = 0.675 s`.

Three things stand out.

1. **Fewest clicks is not fastest.** A takes 3 inputs and B takes 7, yet the expert does B in about half the time of A. Nearly half of A's time is the scan, and scanning never shows up in a click count.
2. **The best design depends on who is playing.** For a novice, B's tabs cost more than A's list, 6.99 s against 6.29 s, because each tab is another decision. Tabs pay off only once the path is chunked into one move. That is germane load in action. The player is learning the interface, and the design repays them for it later.
3. **One `M` never goes away.** Every design keeps at least one `M`, the moment of deciding "I need fire resistance now." That `M` is intrinsic. It is the game. Everything else in the table is interface, and it is extraneous.

Now back to the hook. Skyrim's favourites list is design C: it cuts `N` from the whole inventory to a handful, the same move as a loot filter. The number keys are design D. A controller has no spare row of number keys, which is why controller players get two hotkeys and PC players get eight.

### A visual you can move

Open `examples/w02-klm-load.html`. It shows the four designs twice. On the left, a bar chart of **inputs**: A looks efficient and B looks clumsy. On the right, the same designs as **stacked time bars**, one segment per operator, with `M` and `S` segments in one colour family ("thinking") and `K`, `P`, `B` in another ("doing").

Toggle between expert and novice and watch the right-hand chart. The thinking segments grow and reorder the designs, while the left-hand chart doesn't move at all. Then drag the inventory size from 40 to 80. A's bar grows by 3 seconds while the others barely change. The left chart can't show either effect. That is the lesson: the click count ignores exactly the part of the task that costs the most.

### Cross-game recognition

**Minecraft's recipe book (Java Edition 1.12, 2017).** Before 1.12, crafting in Minecraft meant remembering where each ingredient goes in the grid, which is knowledge in the head. The recipe book, added in Java Edition 1.12, lists the recipes you've unlocked. Clicking one puts the materials you have into the grid, and a toggle shows only recipes you can craft right now. In KLM terms it replaces a recall `M` per ingredient with a single recognition step, and the "craftable" toggle cuts `N` the way a filter does. Players who know their recipes by heart can still craft by hand, so experts lose nothing.

**Boss timer addons in World of Warcraft.** Deadly Boss Mods, a long-running third-party addon, shows alert messages and timer bars for each raid boss's abilities. Without it, a raider has to keep a running count in their head ("the fire wave is due in about ten seconds"), a chunk of working memory held for the whole fight. The addon moves that count into the world. In our terms it deletes a stream of recall `M`s and frees a working-memory slot for intrinsic load, the fight itself.

**The original office setting.** Card, Moran and Newell built KLM for office software such as text editors, not games. The operator table you just used was measured on people at keyboards doing routine work. The same arithmetic transfers to a potion menu because the limits it models belong to the person, not the software.

In all three, the move is to find the `M`s and `S`es that are not the game, then delete them by putting knowledge in the world, by shrinking `N`, or by letting practice chunk the path.

### Eyes-open design judgment

- **KLM models skilled, error-free work.** It predicts how long a task takes when nothing goes wrong. Novices also make errors, and errors cost far more than `M`s. Use KLM to compare designs, then use playtests ([week 8](w08-usability-testing-methods.md)) to find the errors.
- **Don't delete the intrinsic `M`.** A design that drinks the right potion automatically removes the last `M`, and with it a decision the game was built around. Decide deliberately which thinking is your game.
- **Hotkeys move knowledge into the head.** Design D is fastest only for players who remember their bindings. A returning player who has forgotten them falls back to C or worse. Show hotkey labels on screen, at least until the player has used them often, so the knowledge stays in the world.
- **Speed isn't the only goal.** An inventory you browse in town, with the game paused, can afford slow and rich. A potion you drink mid-fight cannot. Match the KLM budget to the moment.
- **Input devices change the operator set.** Controllers have no pointing and few spare buttons, so D is expensive to offer and radial menus or favourites lists take its place. Price each platform separately, as Skyrim does.
- **The numbers are placeholders.** 1.35 s for `M` is an average from office tasks. Your players, your genre and your `e` will differ. The ranking of designs is usually more robust than the absolute seconds.

### Check yourself (worked example)

1. The player now carries 80 items. Recompute design A. How much slower is it than with 40 items?
2. A designer adds a search box to design A. The player presses a key to focus it, types three letters (`3K`), then clicks the single result. Write the operators, with one `M` before the search, and compute the time. Is it faster than A?
3. An expert typist (`K = 0.12 s`) uses design B. What is their time? Why does their advantage over A grow?

<details>
<summary>Answers</summary>

1. `S(80) = 0.15 × 81/2 = 6.075 s`. `T = 1.35 + 0.28 + 6.075 + 1.1 + 0.2 + 0.28 = 9.285 s`, which is 3 s slower.
2. `M K` (open) `K` (focus search) `3K` (type) `P BB` (click result) `K` (close) = `1.35 + 6 × 0.28 + 1.1 + 0.2 = 4.33 s`. Faster than A's 6.29 s, because typing replaces the scan. It would be slower if the player had to stop and recall the name, which adds another `M`.
3. `1.35 + 7 × 0.12 = 2.19 s`. Design A with `K = 0.12` is `1.35 + 0.12 + 3.075 + 1.1 + 0.2 + 0.12 = 5.965 s`. A faster hand shrinks B's seven `K`s but does nothing about A's scan and pointing, so skill widens the gap.

</details>

## 3. Split attention: when the player has to hold one thing to read another

Chandler and Sweller's 1991 experiments found that the format of material changed how much students learned, even when the content was the same. One of the clearest effects was **split attention**. When two pieces of information must be combined to be understood but are shown apart, a diagram here and its labels over there, the learner must hold one in working memory while looking for the other. That holding is pure extraneous load.

Games are full of split attention.

- **Item comparison.** A player looks at a new sword on the ground, then opens the character screen to see their current sword's numbers, then back. They are holding four or five numbers across two screens. A comparison tooltip that shows both items side by side, with the differences marked, removes the holding.
- **Legends and keys.** A map whose icons are explained in a separate legend window forces the player to remember what each symbol meant. Labels on the map, or a tooltip on hover, remove the round trip.
- **HUD placement.** A health bar in the top-left corner and a boss in the centre of the screen split attention during the moment the player can least afford it. Many action games put key status on or near the player character for this reason.

The fix is always the same in principle. **Put information where it is used, at the time it is used.** Integrate it into the thing it describes instead of placing it beside that thing.

There is a limit. Integrating everything into the scene can clutter it, which raises `N` for every search from week 1. The split-attention fix and the pop-out budget pull against each other. The designer's job is to decide which few things earn a place next to the action.

## 4. A working-memory budget for your UI

Week 1 set the working-memory limit at about four chunks. You can turn that into a check for any moment of play. List what the player must *hold in mind*, not what they can see, at that moment.

Take a raid encounter with one boss and three mechanics.

| Item the player must hold | Held in the head? | Could it be in the world? |
|---|---|---|
| Time until the fire wave | Yes, counting | Timer bar |
| Which side is safe this time | Yes, from an earlier cue | Ground marking |
| Whether their cooldown is ready | No, the icon shows it | Already in the world |
| Their assigned position | Yes, from a pre-fight chat message | Marker on the floor or on the character |
| The healer they should stand near | Yes | Highlight on that player |

Four items are held in the head. That is the whole budget before the player does anything with the intrinsic challenge of reading the boss. It is also why some groups find this fight impossible and others find it easy. The easy groups have moved items into the world, with addons, floor markers or rehearsal until the pattern is chunked.

A design team has three honest options for each held item.

1. **Put it in the world.** Show the timer, draw the marker. This cuts extraneous load, but it may also remove intrinsic challenge if remembering the pattern was meant to be the test.
2. **Make it chunkable.** Use a consistent rhythm so experienced players can store the whole fight as one pattern. This turns extraneous load into germane load.
3. **Keep it in the head on purpose.** If memorising the sequence is the challenge, say so, test it, and don't add anything else to hold.

Whichever you pick, count the items. If the count is above four, some players will drop one, and you don't get to choose which.

## In-class activity (25 minutes)

Groups of three. One laptop or phone with a game that has an inventory (or use the Minecraft or Skyrim screens described in this lecture, from memory or video).

1. **Pick a task (5 min).** Choose one routine interface task in a game you know: equip a weapon, sell junk to a vendor, find a quest in the log. Write the steps down.
2. **Model it (10 min).** Write the KLM operator sequence for an expert and for a novice. Include `S(N)` wherever the player scans a list, with an honest estimate of `N`. Compute both times.
3. **Redesign (10 min).** Propose one change that removes at least one `M` or cuts one `S`. Recompute. Say whether the change removes extraneous load or intrinsic load, and defend your answer to the group next to you.

Expected output: two operator sequences, two times, one redesign with its new time, and a one-line classification of what the redesign removed.

## Common misconceptions

- **"Fewer clicks means a better interface."** Click count ignores decisions and scanning, which usually cost more than the clicks. Count `M`s and `S`es.
- **"Cognitive load is bad."** Intrinsic load is the game, and germane load is the player learning it. Only extraneous load is waste.
- **"Experts and novices want the same UI, just faster."** They want different trade-offs. Novices need knowledge in the world. Experts want it out of the way, because they carry it as chunks.
- **"Put everything on the HUD so nothing is in the player's head."** Every added element raises `N` for every search. Integration reduces split attention only while the screen stays searchable.

## Check yourself

1. A menu takes `M K K K M K` for a novice and `M K K K K` for an expert. Compute both times with the standard values. Which KLM rule explains the missing `M` for the expert?
2. A strategy game shows unit stats only in a panel at the bottom of the screen, while units fight in the centre. Name the load effect and propose a fix.
3. A shop screen lists 30 unsorted items. Adding category tabs costs one extra `K` and one extra `M` for a novice, and reduces the scanned list to 6 items. Is the novice faster with or without tabs? Show the numbers.
4. A designer says, "Let's auto-select the best armour for the player so they never have to compare." When is this cutting extraneous load, and when is it deleting the game?

<details>
<summary>Answers</summary>

1. Novice: `2 × 1.35 + 4 × 0.28 = 2.7 + 1.12 = 3.82 s`. Expert: `1.35 + 4 × 0.28 = 2.47 s`. The second `M` is deleted because the expert has chunked the whole sequence, so the next step is fully anticipated.
2. Split attention. The player must hold stats from the panel while watching the fight. Fix it with health and key stats drawn on or above each unit, or a hover tooltip at the unit.
3. Without tabs: `S(30) = 0.15 × 31/2 = 2.325 s`. With tabs: `M + K + S(6) = 1.35 + 0.28 + 0.525 = 2.155 s`. The tabs save 0.17 s, a small gain. With a smaller list, or with tabs that need more thought, they would lose.
4. It cuts extraneous load when armour choice is a chore, with one obviously better option and the comparison only arithmetic. It deletes the game when choosing between trade-offs (weight against protection, set bonuses) is a meaningful decision the game is built on. Check it with the three tests from GD101 week 9 (discernable, integrated, uncertain). If the right answer is always obvious, the choice fails the uncertain test and automating it costs nothing.

</details>

## Lab hook

[Lab 02, keystroke-level audit of a shipped game](../labs/lab02.md). You pick one frequent task in a shipped game, time five players doing it, model it with KLM, compare your model's prediction with the measured times, and propose a redesign with a predicted saving. Deliverable: the timing sheet, both operator sequences and a two-page memo.

## Sources

- UESP, "Skyrim:Controls" (en.uesp.net, accessed September 2026; The Elder Scrolls V: Skyrim, original release and later editions). Favourites quick menu on Q (PC) or the D-pad; PC hotkeys 1 to 8; on Xbox, PlayStation and Switch controllers only two items or spells can be hotkeyed.
- Wikipedia, "Keystroke-level model" (accessed September 2026). Card, Moran and Newell (1980; book 1983); operator times K (0.08 to 1.2 s by skill, 0.28 s for an average non-secretary typist), P 1.1 s, B 0.1 s, H 0.4 s, M 1.35 s; rules for placing and deleting M operators.
- Card, S. K., Moran, T. P. & Newell, A. (1983). *The Psychology of Human-Computer Interaction*. Lawrence Erlbaum.
- Sweller, J. (1988). "Cognitive load during problem solving: effects on learning." *Cognitive Science*, 12(2), 257-285. Chandler, P. & Sweller, J. (1991). "Cognitive load theory and the format of instruction." *Cognition and Instruction*, 8(4), 293-332. Summaries of intrinsic, extraneous and germane load and the split-attention effect via Wikipedia, "Cognitive load."
- Minecraft Wiki, "Recipe book" (minecraft.wiki, accessed September 2026). Added in Java Edition 1.12 (snapshot 17w13a, 2017); clicking a recipe places available materials in the grid; toggle to show only craftable recipes.
- Warcraft Wiki, "Deadly Boss Mods" (warcraft.wiki.gg, accessed September 2026). A boss alert addon made of per-boss modules that trigger alert messages and timer bars.
- Wikipedia, "Hick's law" (accessed September 2026). Finding an item in a randomly ordered list requires scanning each item, in linear time, so Hick's law does not apply there.
- Hodent, C. (2017). *The Gamer's Brain*. CRC Press. Chapters "Memory" and "Usability."
- The scan time `e = 0.15 s` per entry and the four inventory designs are teaching assumptions, not measurements of any shipped game.

## Interactive spec: examples/w02-klm-load.html

**Purpose.** Show that counting inputs and counting time rank interface designs differently, because decisions (`M`) and scanning (`S`) dominate task time and are invisible to a click count.

**The one insight the visual must make obvious.** Switching between expert and novice, or growing the inventory, reorders the time bars on the right while the input-count bars on the left stay the same.

**Layout.** Two charts side by side at 1280px, stacked at 390px. Controls below. A numbers table under the controls.

- Left, "Inputs": horizontal bars for designs A, B, C, D, length = number of `K` plus number of clicks (`BB` counts as one input). Values printed at bar ends.
- Right, "Time (KLM)": horizontal stacked bars for the same designs on a shared axis from 0 to 12 s. Segment order follows the operator sequence. `M` and `S` segments use the "thinking" colour family (two shades, and a hatch pattern for `S`); `K`, `P`, `B`, `H` use the "doing" family. Total printed at the end of each bar. The fastest design gets a small marker.

**Controls.**

- Player: segmented Expert / Novice, default Expert.
- Inventory size `N` for design A: slider 10 to 100, step 1, default 40.
- Potions in the Potions tab (B's scan): slider 2 to 30, default 12.
- Favourites (C's scan): slider 2 to 12, default 6.
- Hotbar slots (D's novice scan): slider 4 to 12, default 8.
- Scan time per entry `e`: slider 0.05 to 0.40 s, step 0.01, default 0.15.
- Keystroke time `K`: select 0.08 (expert typist), 0.12, 0.20, 0.28 (average, default), 0.50.
- `M`: slider 0.6 to 2.0 s, step 0.05, default 1.35. `P` 1.1 and `B` 0.1 fixed, shown in the legend.
- Toggle "Add search box to A": replaces A's sequence with `M K K 3K P BB K`.
- Reset button.

**Operator sequences.**

- A (both players): `M K S(N) P B B K`.
- B expert: `M K K K K K K K` (7 K). B novice: `M K M K K M S(n_potions) K K K K` (3 M, 7 K, one scan).
- C expert: `M K K K K`. C novice: `M K M S(n_fav) K K K`.
- D expert: `M K`. D novice: `M S(n_slots) K`.
- `S(n) = e × (n + 1) / 2`.

**Numbers table.** For each design: inputs, expert time, novice time, and the share of the current time that is "thinking" (`M` + `S`).

**Test values** (defaults: `K = 0.28`, `M = 1.35`, `P = 1.1`, `B = 0.1`, `e = 0.15`, N = 40, potions 12, favourites 6, slots 8).

| Design | Inputs | Expert (s) | Novice (s) |
|---|---|---|---|
| A | 3 | 6.285 | 6.285 |
| B | 7 | 3.310 | 6.985 |
| C | 4 | 2.470 | 4.345 |
| D | 1 | 1.630 | 2.305 |

- A with N = 80: 9.285 s. A with search box: 4.33 s.
- `K = 0.12`: A 5.965 s, B expert 2.19 s.
- Thinking share for A at defaults: `(1.35 + 3.075) / 6.285 = 70.4%`.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark. Thinking vs doing segments differ by pattern as well as colour. Every control keyboard operable with visible values. No game art or logos; designs are labelled A to D with the one-line descriptions from the lecture. First screen shows both charts at defaults with the novice/expert toggle visible above them.
