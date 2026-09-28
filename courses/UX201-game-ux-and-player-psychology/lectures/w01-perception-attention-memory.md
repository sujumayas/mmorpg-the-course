# UX201 · Week 01 — Perception, Attention and Memory

**Why this matters:** Every screen you design is read by a brain that sees less than it thinks it does, notices only what it is looking for, and forgets most of what it was told. If your loot, your quest marker or your tutorial text doesn't fit those limits, the player never receives it, however good it looks in the editor. This week gives you a model that turns "players can't find anything" into milliseconds you can measure and design down.

**You will be able to:**
- Compute search time for a target among distractors with the linear search model, for pop-out and for item-by-item search, with the target present and absent.
- Estimate how much of a play session a loot screen or marker design spends on searching, and compare two designs by that cost.
- Predict when a game signal will be missed because of inattention, and redesign it so it does not depend on the player looking in the right place.
- Critique an interface for the load it puts on working memory, and move information from the player's head into the world.

**Before class:** Celia Hodent, *The Gamer's Brain* (CRC Press, 2017), the chapters "Perception" (pp. 19-34), "Memory" (pp. 35-50) and "Attention" (pp. 51-58). Jeremy Wolfe and Todd Horowitz, "Visual search", *Scholarpedia* 3(7):3325 (2008, free online), sections 1 to 6.

**Prerequisites from earlier courses:** [GD101 week 12, feedback, juice, clarity and readability](../../GD101-introduction-to-game-design/lectures/w12-feedback-juice-clarity-readability.md). You met the Hick-Hyman law and colour-only signals there, and this week continues from them. [GD101 week 7, playtesting](../../GD101-introduction-to-game-design/lectures/w07-playtesting-observe-dont-explain.md), for the observation method you will use in the lab. [MA101 week 2, linear functions and rates](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w02-linear-functions-and-rates.md), because this week's model is a straight line with an intercept and a slope.

**Interactive:** [Loot search: pop-out vs item-by-item search](../examples/w01-loot-search.html). Use it during section 2.

---

## 1. The player's brain is part of your platform

You test your game on target hardware: a console, a phone, a mid-range PC. You should test it on the other piece of hardware too, the one between the player's ears. It has hard limits, and they are better documented than most GPUs.

Three of those limits shape nearly every screen in a game.

- **Perception** is how the brain turns light and sound into objects. It is constructed, not recorded. Your visual system fills in gaps, groups things that are close together or look alike, and uses expectation to decide what it is seeing. Hodent's chapter on perception makes the point that two players can look at the same screen and perceive different things, because each brings different knowledge and goals.
- **Attention** is the filter that decides which of those perceived things get processed further. It is narrow. You can attend to very little at once, and what you attend to is driven partly by the screen (a flash, a moving object) and partly by what you are trying to do.
- **Memory** is where anything you want the player to use later must survive. Working memory holds a few things for a few seconds. Long-term memory holds a lot, but only what was encoded well, and it fades without use.

Psychologists call the screen-driven part of attention **bottom-up** (a bright flash grabs you whether you want it or not) and the goal-driven part **top-down** (you are hunting for a health potion, so red bottles stand out). Good game UI works with both. It makes the important thing physically distinct, and it puts it where a player with that goal will look.

The rest of this lecture turns one of these limits into numbers, then covers the other two more briefly. [Week 2](w02-cognitive-load-and-ui.md) and [week 10](w10-hud-and-information-design.md) build on all three.

## 2. Worked example: why loot games let you hide the loot

### The hook

In Path of Exile, monsters drop a lot of items, and most of them are worth nothing to you. Version 2.0.0 of the game added **item filters**, text files that change how dropped items look on the ground and can hide some of them completely. Version 3.4.0 went further. Filters could now add minimap icons and light beams to chosen item types, and the developers' patch note said this made them "much harder to miss."

Think about what that means. A game whose central reward is loot added a tool whose main job is to show you *less* loot. And it then added light beams, because players were missing items that were right there on screen.

Players who have played any loot game know the feeling. A pack dies, the ground fills with labels, and you spend a second or two reading them only to find nothing worth picking up. That second is not a matter of taste. It is a measurable property of human vision, and it grows with every item you put on the ground.

### The model

Visual search is the task of finding a target among distractors. Researchers have studied it for decades with a simple setup. Show a display of `N` items, ask "is the target here?", and time the answer. The reaction time grows roughly in a straight line with `N`:

```
T(N) = a + k × N
```

- `T` is the time to answer, in milliseconds.
- `N` is the **set size**, the number of items on screen.
- `a` is the **intercept**. It covers everything that isn't search: seeing the display at all, deciding, and pressing a button. Wolfe and Horowitz note it is several hundred milliseconds even for simple searches.
- `k` is the **slope**, the extra time each added item costs. It is the standard measure of how efficient a search is.

The slope depends on how the target differs from the distractors.

- **Pop-out (efficient) search.** If the target differs in one basic feature that the visual system processes in parallel, such as colour, motion, orientation or size, it seems to jump out. The slope is near zero. Finding one orange label among grey ones takes about as long with 5 greys as with 50. Wolfe and Horowitz list colour, motion, orientation and size as the attributes with the strongest evidence for guiding attention this way.
- **Inefficient search.** If the target is defined by a combination of features (an orange *ring* among orange amulets and grey rings), or by something that must be read (the name of an item), the eye has to check items more or less one at a time. Treisman and Gelade's feature integration theory (1980) was the first influential account of this difference. In the laboratory, target-present slopes for simple inefficient searches are around 20 to 40 ms per item. Slopes are much steeper when each item has to be looked at directly to be identified, which is the usual case for text labels in a game.
- **Target absent costs about twice as much.** When the target isn't there, you can't stop early. You have to rule out every item. Target-absent slopes tend to be a little more than twice the target-present slopes. If items are checked one by one and never twice, a present target is found after checking on average `(N + 1)/2` items, while an absent target needs all `N`. That is where the factor of two comes from.

For this lecture we fix teaching values. They sit inside the published ranges, and you will replace them with your own measurements in the lab.

| Search type | `a` (ms) | `k`, target present (ms per item) | `k`, target absent (ms per item) |
|---|---|---|---|
| Pop-out | 500 | 0 | 0 |
| Item by item | 500 | 30 | 60 |

We use exactly twice the present slope for the absent case to keep the arithmetic clean.

### Numbers you can check

Search times from the model:

| Items on screen `N` | Pop-out | Item by item, target present | Item by item, target absent |
|---|---|---|---|
| 4 | 500 | 620 | 740 |
| 8 | 500 | 740 | 980 |
| 16 | 500 | 980 | 1,460 |
| 32 | 500 | 1,460 | 2,420 |
| 64 | 500 | 2,420 | 4,340 |

Check one row by hand. With 16 items and nothing worth taking, `500 + 60 × 16 = 1,460 ms`.

Now look at what players actually do. In most loot games, most packs drop nothing you want. So the common case is the expensive one, target absent. Put a session on it.

Suppose a player clears 300 packs an hour, each drops 16 items, and one pack in twenty (5%) drops something worth taking. Expected search time per pack is a weighted average of the two cases:

```
E[T] = 0.05 × T_present + 0.95 × T_absent
```

| Design | `N` searched | `E[T]` per pack | Per hour (300 packs) |
|---|---|---|---|
| Plain text labels, all shown | 16 | 0.05 × 980 + 0.95 × 1,460 = 1,436 ms | 431 s, about 7.2 min |
| Filter hides the 12 known-junk types | 4 | 0.05 × 620 + 0.95 × 740 = 734 ms | 220 s, about 3.7 min |
| Valuable items get a unique colour and beam | 16 | 500 ms | 150 s, 2.5 min |

Seven minutes an hour spent reading labels is a real share of play, and it is time the player experiences as chores. Hiding junk halves it by cutting `N`. Pop-out cuts it further by making `k` nearly zero, and it does that without removing anything from the screen.

Notice the two different levers. A filter changes `N`. A unique signal changes `k`. They are separate design decisions with separate costs, and you will see those costs in the judgment section.

### A visual you can move

Open `examples/w01-loot-search.html`. The left panel is a field of generic loot labels, and you are the test subject. Press start, find the target (or answer "not here") and the page records your time. The right panel plots `T` against `N`, with the model's three lines (pop-out, present, absent) and your own trials as dots.

Run five trials in pop-out mode at `N = 8` and five at `N = 32`. Your dots sit at about the same height. Switch to item-by-item mode and repeat. The dots climb, and the "not here" trials climb about twice as fast. Your own slope, printed under the chart, is the number the lab asks you to measure properly. The picture on the right is the lesson. One line stays flat as `N` grows, and the other two tilt.

### Cross-game recognition

The same model explains a lot of UI you have used without thinking about it.

**World of Warcraft quest givers.** A non-player character with a quest for you shows a gold exclamation mark above its head. One whose quest you can't take yet shows a silver one, and repeatable quests use blue marks. The markers also appear on the minimap. In a crowded capital city with dozens of characters on screen, the gold mark is a pop-out target. It differs in colour and in shape from everything around it, and it sits above the crowd where nothing else competes. Using silver for "not yet" keeps gold rare, which is what keeps `k` near zero. If every character had a gold mark, the player would be back to reading names.

**World of Warcraft item quality colours.** Item names are coloured by quality: grey for poor, white for common, green for uncommon, blue for rare, purple for epic and orange for legendary. The wiki notes that grey items are almost synonymous with vendor trash. The colour scale turns "is anything here good?" into a colour search. You glance for purple or orange instead of reading names. It works best when the target colour is far from every distractor colour. Picking out green among a sea of whites works well. Picking out one particular blue among many blues does not, and the player is back to reading.

**Path of Exile item filters.** Filters attack both terms. Hiding items cuts `N`. Custom colours, sounds, minimap icons and beams give the items a player cares about a feature nothing else on the screen has, which pushes `k` toward zero. The game hands the choice to the player because only the player knows what their target is this week.

**The laboratory task.** Strip the game away and you have Treisman and Gelade's experiment: find the red letter among green letters (flat line), or find the red T among red Ls and green Ts (tilted line). Every loot screen, minimap and crowded menu is a version of it. When you meet a new interface, ask two questions. How many things must the player look through, and does the thing they want differ from all of them in one basic feature?

### Eyes-open design judgment

- **Pop-out is a budget, not a style.** Uniqueness is what makes it work. Each extra item type you give a glow or a beam becomes another distractor for the others. Decide which one or two things per screen deserve pop-out, and let the rest be quiet.
- **Colour alone excludes players.** Red-green colour vision deficiency is common, especially among men, as GD101 week 12 showed. A rarity that differs only in hue may not pop out for them at all. Pair colour with a second feature such as shape, size, a beam or a sound.
- **Hiding has a failure mode.** A filter that hides the wrong item makes a problem that is invisible by design. The player never learns what they missed. Path of Exile makes filters opt-in and editable. If you hide things by default, keep the rule simple and visible.
- **The absent case is where the time goes.** Designers test "can the player find the legendary?" They rarely test "how fast can the player confirm there's nothing?" In most sessions the second question is asked hundreds of times more often.
- **Consistent places cut search too.** Wolfe and Horowitz note that learning the few locations where a target can appear makes search more efficient. A HUD that always shows ammo in the same corner, or a vendor that always stands by the door, removes most of the search before it starts.
- **The numbers are placeholders.** The 500, 30 and 60 are teaching values. Text labels in a moving 3D scene are harder than letters on a lab screen. Measure your own game before you quote a number to your team.

### Check yourself (worked example)

1. A dungeon drops 24 items per pack and 10% of packs have something worth taking. With the lecture's values and no pop-out, what is the expected search time per pack?
2. A designer proposes cutting drops from 24 items to 12 but keeping plain labels. Another proposes keeping 24 items and giving the valuable ones a unique beam. Which saves more time per pack, and by how much?
3. Your team gives every item of blue quality or better a beam. In a typical pack, 6 of 16 items qualify. Does the beam still pop out the one item you want? Rewrite the situation in the model.

<details>
<summary>Answers</summary>

1. Present: `500 + 30 × 24 = 1,220 ms`. Absent: `500 + 60 × 24 = 1,940 ms`. Expected: `0.1 × 1,220 + 0.9 × 1,940 = 122 + 1,746 = 1,868 ms`.
2. Twelve items: present `860`, absent `1,220`, expected `0.1 × 860 + 0.9 × 1,220 = 1,184 ms`, a saving of 684 ms. The beam makes the search pop-out: 500 ms, a saving of 1,368 ms. The beam saves twice as much.
3. No. The beam now marks 6 items, so the player must search item by item among those 6 for the one they want. `N` drops from 16 to 6, but `k` goes back up. Target present: `500 + 30 × 6 = 680 ms`, not 500. The beam has turned into a filter.

</details>

## 3. Attention: you see what you are looking for

The search model assumes the player is searching. Much of the time they aren't. They are dodging, aiming or reading a quest, and your new signal has to break into a mind that is busy with something else.

### Selective attention and inattentional blindness

In 1999 Daniel Simons and Christopher Chabris asked people to watch a video of two teams passing basketballs and to count the passes made by one team. Partway through, a person in a gorilla suit walks through the scene. In most conditions about half the viewers did not report seeing the gorilla. Psychologists call this **inattentional blindness**. It is a failure to notice something fully visible because attention is engaged elsewhere. It isn't a problem with the eyes.

Now think of your game. A tutorial tip appears in the corner of the screen while the player is fighting their first enemy. The tip is large, legible and fully visible. A good share of players will not see it, for exactly the reason the gorilla went unseen. Their attention is on the fight, and the fight is the task.

Three design consequences follow.

- **Put new information where attention already is.** Show a dodge prompt on or next to the enemy that is attacking, not in a corner.
- **Teach in calm moments.** Introduce a rule when the player has nothing else to do, then test it when they do. Onboarding ([week 7](w07-onboarding-and-tutorials.md)) is largely the craft of timing this.
- **Use bottom-up signals sparingly.** Motion, flicker and sudden onsets grab attention even from a busy player. That is why they work for urgent warnings, and why using them for anything less urgent wears them out.

### Attention is a budget

Attention behaves like a limited resource shared among tasks. When a task gets harder, less is left for everything else. A player at low health in a boss fight has almost nothing to spare for a chat message or a quest update. You met the time version of this in GD101 week 12, where visual noise spent the reaction budget of a telegraph. The same thinking applies here. Every element that competes for attention during play is paid for out of one pool.

A useful habit is to list, for any moment of your game, the one thing the player must notice. If you can't name it, the screen has no priority. If you name three, the player will catch one of them, and you don't get to choose which.

## 4. Memory: what survives from one moment to the next

### Working memory

**Working memory** is the small space where you hold and manipulate information right now: the enemy's last attack, the key you need, the three numbers you are comparing. Its capacity is small. George Miller's 1956 paper put it at "seven plus or minus two" items. Later work by Nelson Cowan (2001) argued for a more conservative limit of about four **chunks** for young adults, where a chunk is a unit of meaning such as a word or a familiar pattern, not a single letter or digit. Baddeley and Hitch's model (1974) splits working memory into parts for sound-based information, visual and spatial information, and a controller that directs attention between them.

For design, take the smaller number. Assume a player can juggle about four new things at once, fewer when they're under stress, and plan the screen so it never asks for more.

**Chunking** is how experts cheat the limit. A new player sees a combo as six separate button presses. A practised one sees it as one move. Hodent points out that this is why the same interface can overload a newcomer and feel spare to a veteran. When you playtest, remember which of the two you are watching.

### Long-term memory and forgetting

**Long-term memory** is large, but storage is not guaranteed and retrieval is not automatic. Hermann Ebbinghaus, testing himself on lists of nonsense syllables in the 1880s, published a curve in 1885 showing that memory for new material drops steeply at first and then levels off. Reviewing material at spaced intervals slows the loss. That finding, the spacing effect, is behind every game that reintroduces a mechanic a few levels after teaching it.

Games meet forgetting in two places you can plan for.

- **Within a session.** A player told about a mechanic at the start of a level and asked to use it twenty minutes later has probably lost it, unless they used it in between.
- **Between sessions.** A player returning to an MMO after three months has forgotten their rotation, their keybinds and what they were doing. Quest logs, "previously" summaries and a clear current objective are memory aids for that player.

### Knowledge in the world

Donald Norman's *The Design of Everyday Things* (1988) distinguishes **knowledge in the head** from **knowledge in the world**. Knowledge in the head is fast once learned, but it must be learned and can be forgotten. Knowledge in the world is always there to be read. It costs screen space and a moment of looking, but it asks nothing of memory. Jakob Nielsen's usability heuristics (1994) put the same idea as "recognition rather than recall." Make the options visible so the user doesn't have to remember them.

Every game UI is a split between these two. A quest marker on the map is knowledge in the world. A quest description you read once and must remember is knowledge in the head. The gold exclamation mark from section 2 does both jobs. It pops out, and it means nobody needs to remember which character had the quest.

The design question is not "which is better." It is "what should this player have to remember, at this point in their learning?" New players need more in the world. Experts often want it removed, because it clutters the screen and they already carry it in their heads. Next week puts numbers on that trade.

## In-class activity (25 minutes)

Work in pairs with one phone stopwatch each.

1. **Build two displays (8 min).** On paper, draw two grids of 20 small symbols. In grid A, 19 symbols are grey circles and one is an orange circle. In grid B, the distractors are a mix of orange squares and grey circles, and the target is an orange circle. Draw a second copy of B with no target.
2. **Run it (10 min).** Your partner looks away. Put a grid face down, flip it, start the stopwatch, and stop when they point to the target or say "not here." Do three trials per grid, reshuffling the target's position between trials. Swap roles.
3. **Compare (7 min).** Compute the mean time per grid. Which grid is pop-out, and which is item-by-item? Is the no-target copy of B slower than B with a target? By roughly how much?

Expected output: a six-cell table of mean times, one sentence naming which grid is which search type, and one sentence on how close your target-absent to target-present ratio came to 2. Stopwatch timing adds a few hundred milliseconds of noise, so look for large differences only.

## Common misconceptions

- **"If it's on screen, the player saw it."** Visible is not the same as noticed. Inattentional blindness affects fully visible objects when attention is elsewhere. Place information where the player's task already takes their eyes.
- **"More colours make things easier to find."** A colour pops out only when it is unique among the things around it. Colour-code everything and nothing stands out, and players are back to reading.
- **"Players remember seven things."** Seven plus or minus two was Miller's 1956 estimate. More recent work suggests about four chunks, and fewer under stress. Design for four.
- **"Search time is about how many items there are."** Only for inefficient search. For pop-out targets the number of distractors barely matters. The slope, not the count, is the design variable.

## Check yourself

1. A crafting screen shows 40 materials as text labels, sorted randomly. A player checks whether they have "iron ore." Using the lecture's values, how long does the check take if they have it, and if they don't?
2. A minimap shows 12 icons, all white. The designer makes the one objective icon white and pulsing. Which search type is this now, and what time does the model predict?
3. A tutorial tells the player about three new mechanics on one screen during the first boss fight. Name two separate reasons, one from attention and one from memory, why most players will not use the third mechanic.
4. An MMO shows buff icons in a row of up to 16. Players complain they can't tell if their shield buff is up. Propose one change that lowers `k` and one that lowers `N`.

<details>
<summary>Answers</summary>

1. Present: `500 + 30 × 40 = 1,700 ms`. Absent: `500 + 60 × 40 = 2,900 ms`. Sorting the list alphabetically would let the player skip straight to the right region, which cuts the effective `N` sharply.
2. Pop-out, because motion is a basic feature the visual system processes in parallel. About 500 ms regardless of the number of icons.
3. Attention: during a boss fight the player's attention is on the boss, so the tip may not be read at all. Memory: three new items at once, under stress, sit at or beyond the four-chunk limit, and the third is the most likely to be lost before it's needed.
4. Lower `k`: give the shield buff a distinct shape or border colour no other buff uses, or show it as a ring around the health bar. Lower `N`: let players pin a short list of buffs they care about, or hide buffs from other players by default.

</details>

## Lab hook

[Lab 01, measuring search cost](../labs/lab01.md). You run a visual search study with five participants on displays generated by the starter script, fit `a` and `k` for pop-out and item-by-item search with the target present and absent, and then apply your own numbers to a loot or minimap screen from a shipped game. Deliverable: the data sheet, your fitted lines and a one-page redesign memo.

## Sources

- Path of Exile Wiki, "Item filter", version history (poewiki.net, accessed September 2026). Item filters added in version 2.0.0; version 3.4.0 added minimap icons and light beams for chosen item types, with the patch note phrase "much harder to miss."
- Wolfe, J. M. & Horowitz, T. S. (2008). "Visual search." *Scholarpedia*, 3(7):3325. Linear RT by set size; near-zero slopes for efficient search; 20-40 ms/item target-present slopes for simple inefficient search; target-absent slopes a bit more than twice as steep; intercepts of several hundred milliseconds; the `(N + 1)/2` average for serial self-terminating search; colour, motion, orientation and size as the attributes with the strongest evidence for guiding attention; learning a few likely locations improves search.
- Treisman, A. M. & Gelade, G. (1980). "A feature-integration theory of attention." *Cognitive Psychology*, 12, 97-136.
- Warcraft Wiki, "Quest giver" (warcraft.wiki.gg, current retail era, accessed September 2026). Gold exclamation mark for available quests, silver for quests not yet available, blue marks for repeatable quests; minimap markers.
- Warcraft Wiki, "Quality" (warcraft.wiki.gg, current retail era, accessed September 2026). Poor (grey), common (white), uncommon (green), rare (blue), epic (purple), legendary (orange); poor items are mostly vendor trash.
- Simons, D. J. & Chabris, C. F. (1999). "Gorillas in our midst: sustained inattentional blindness for dynamic events." *Perception*, 28, 1059-1074. Summary via Wikipedia, "Inattentional blindness": in most groups about 50% did not report the gorilla.
- Miller, G. A. (1956). "The magical number seven, plus or minus two." *Psychological Review*. Cowan, N. (2001). "The magical number 4 in short-term memory." *Behavioral and Brain Sciences*, 24, 87-114. Baddeley, A. D. & Hitch, G. (1974). "Working memory." Summaries via Wikipedia, "Working memory."
- Ebbinghaus, H. (1885). *Über das Gedächtnis*. Summary via Wikipedia, "Forgetting curve."
- Norman, D. A. (1988). *The Design of Everyday Things* (originally *The Psychology of Everyday Things*). Chapter "Knowledge in the Head and in the World."
- Nielsen, J. (1994). "10 Usability Heuristics for User Interface Design." Nielsen Norman Group. Heuristic 6, recognition rather than recall.
- Hodent, C. (2017). *The Gamer's Brain: How Neuroscience and UX Can Impact Video Game Design*. CRC Press. Chapters "Perception", "Memory", "Attention."
- The values `a = 500 ms`, `k = 30` and `60 ms per item`, the 300 packs per hour and the 5% chance of a worthwhile drop are teaching assumptions, not measurements from any game.

## Interactive spec: examples/w01-loot-search.html

**Purpose.** Let students feel and measure the difference between pop-out and item-by-item search, and see that the cost of item-by-item search grows with the number of items, twice as fast when the target is absent.

**The one insight the visual must make obvious.** On the right-hand chart, the pop-out line stays flat as `N` grows while the item-by-item lines tilt, and the student's own timed dots follow the same pattern.

**Layout.** Two panels side by side at 1280px, stacked at 390px (search field first). Controls and a numbers panel below.

- Left, "Search field": a square area with `N` generic loot labels placed at random non-overlapping positions on a jittered grid. Each label is a short rounded rectangle with a small shape icon (circle, square, triangle, diamond) and a two-word invented item name in a neutral font ("Dusty Ring", "Cracked Amulet"). No game art or real item names.
- Right, "Search time vs items": x axis `N` from 0 to 64, y axis ms from 0 to 5,000. Draw the model lines for pop-out, item-by-item present and item-by-item absent using the current `a` and slopes. Plot the student's trials as dots, colour and marker by condition (hollow for absent). Show a least-squares line through the student's item-by-item present dots once there are trials at two or more set sizes, and print its fitted `a` and `k`.

**Modes.**

- Pop-out: the target is the only label with the accent colour and the diamond icon. Distractors use the neutral colour and a mix of the other icons.
- Item by item (conjunction): the target is "accent colour + diamond." Half the distractors are accent colour with other icons; half are neutral colour with diamonds. The target differs from every distractor only in the combination.
- Target present is chosen at random with probability 0.5 on each trial (toggle "always present" for demos).

**Trial flow.** Press "Start trial" (or Space). A fixation cross shows for 600 ms, then the field appears and a timer starts. The student clicks the target, or presses "Not here" (or the N key). Record RT, `N`, mode, present/absent and correctness. Wrong answers are recorded and shown with a cross but excluded from the fitted line. The field clears after each answer. Keyboard-only users can answer with Enter ("found it", then Tab through labels to confirm the item; record time at Enter) or N; document this in a help line.

**Controls.**

- Set size `N`: segmented 4 / 8 / 16 / 32 / 64, default 16.
- Mode: pop-out or item by item, default pop-out.
- Model parameters (advanced section): `a` 200 to 1,000 ms, step 10, default 500; present slope 0 to 100 ms, step 1, default 30; absent slope 0 to 200, default 60.
- "Session cost" calculator: packs per hour (default 300), items per pack (default 16), chance a pack has a worthwhile item (0 to 1, default 0.05), items hidden by filter (0 to items per pack, default 0), and a toggle "valuable items pop out."
- Buttons: Start trial, Not here, Clear my data, Export CSV (columns: trial, mode, N, present, rt_ms, correct).

**Formulas.**

- `T_popout(N) = a`.
- `T_present(N) = a + k_p × N`. `T_absent(N) = a + k_a × N`.
- Session: `N_eff = items − hidden`. If pop-out is on, `E[T] = a`. Otherwise `E[T] = p × T_present(N_eff) + (1 − p) × T_absent(N_eff)`. Per hour = `packs × E[T]`, shown in seconds and minutes.
- Fitted line: ordinary least squares of RT on `N` over correct trials of the selected condition.

**Test values** (defaults `a = 500`, `k_p = 30`, `k_a = 60`).

| N | Pop-out | Present | Absent |
|---|---|---|---|
| 4 | 500 | 620 | 740 |
| 16 | 500 | 980 | 1,460 |
| 32 | 500 | 1,460 | 2,420 |
| 64 | 500 | 2,420 | 4,340 |

Session cost: 300 packs, 16 items, `p = 0.05`, no filter, pop-out off gives `E[T] = 1,436 ms` and 430.8 s per hour. Hidden 12 gives 734 ms and 220.2 s. Pop-out on gives 500 ms and 150 s. With 24 items and `p = 0.1`: 1,868 ms.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark themes. The target in pop-out mode differs in both colour and icon shape so colour-blind students still see pop-out (a note explains this choice and links it to section 2's judgment). Honour `prefers-reduced-motion` (no fade-ins; the field appears instantly, which is also correct for timing). All controls keyboard operable with visible focus. The first screen shows the chart with model lines and a sample dataset of 12 pre-filled dots (clearly labelled "example data") so the insight is visible before any trial is run; the first real trial replaces the sample.
