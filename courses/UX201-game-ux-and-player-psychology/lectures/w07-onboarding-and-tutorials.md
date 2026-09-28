# UX201 · Week 07 — Onboarding and Tutorials

**Why this matters:** A tutorial that "covers everything" can still send players into their first real fight unable to use half of what it covered. Teams check boxes ("dash taught, ward taught") and never ask whether the player can still pull the skill out of memory at the moment the game demands it. This week gives you a model for that moment, so you can schedule teaching the way you schedule difficulty.

**You will be able to:**
- Compute a player's chance of recalling a mechanic at the moment of need from when it was taught, how often it was practised and how long ago it was last used.
- Compare a front-loaded tutorial with an interleaved one by recall at the moment of need, and explain why a checklist of "taught" mechanics ranks them the wrong way round.
- Design a teaching schedule for a game's first 40 minutes that keeps every required mechanic above a target recall, and name what the schedule costs.
- Choose between a tutorial level, a contextual prompt, a gated practice area and a skill check for a given mechanic and a given player, and justify the choice.

**Before class:** Celia Hodent, *The Gamer's Brain* (CRC Press, 2017), reread the chapter "Memory" (pp. 35-50) and read the chapter "Learning Principles" (pp. 83-90). Christian Nutt, "The Structure of Fun: Learning from *Super Mario 3D Land*'s Director" (Game Developer, April 2012), the part where Koichi Hayashida describes how a level introduces and develops one idea. Optional: Roediger and Karpicke, "Test-enhanced learning," *Psychological Science* 17(3), 249-255 (2006).

**Prerequisites from earlier courses:** [UX201 week 1, perception, attention and memory](w01-perception-attention-memory.md), section 4, for the forgetting curve, the spacing effect and knowledge in the world. [UX201 week 2, cognitive load and UI](w02-cognitive-load-and-ui.md), because a tutorial that teaches four things at once is an extraneous-load problem before it is a memory problem. [UX201 week 3, flow and difficulty](w03-flow-and-difficulty.md), for Ana, the bored expert who needs a way past your tutorial. [MA101 week 4, exponentials](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w04-exponentials-and-the-xp-curve.md), for `e^(−x)` and how a decay constant sets its speed. [GD101 week 12, feedback, juice, clarity and readability](../../GD101-introduction-to-game-design/lectures/w12-feedback-juice-clarity-readability.md), for feedback the player can read in time.

**Interactive:** [The forgetting gap](../examples/w07-forgetting-gap.html). Use it during section 2.

---

## 1. What onboarding has to do

**Onboarding** is everything a game does to turn a new player into one who can play it on their own. Industry teams often call the first session the **first-time user experience (FTUE)**. A **tutorial** is one tool for onboarding: a stretch of play, or a set of messages, whose main job is teaching. Onboarding is bigger than the tutorial. It includes how the first quest is phrased, where the camera starts, which button prompt appears when, and what the game does when the player comes back after three months away.

A new player has to learn four kinds of thing.

- **Controls.** Which input does what. "Space jumps."
- **Rules.** What the game does in response. "Falling into water resets you to the last ledge."
- **Goals.** What they are trying to do, now and later. "Reach the tower. Then find the four shrines."
- **Systems.** How pieces combine. "Freezing a boulder stores the force of every hit until it thaws."

Each kind fails in its own way, and each failure matches a week of this course.

- **Overload.** The tutorial pushes six new controls in two minutes. Working memory holds about four chunks (week 1), and extraneous load crowds out the learning itself (week 2). The player "completes" the tutorial and retains little.
- **Boredom.** The tutorial forces a genre veteran through lessons they don't need. That is Ana from week 3, whose strain climbs on levels she could play asleep.
- **Forgetting.** The tutorial taught a mechanic well, then the game didn't ask for it for half an hour. By the time it matters, the memory has faded.

Weeks 2 and 3 gave you tools for the first two. This week is about the third, because it is the one teams almost never measure. A tutorial checklist records that a mechanic was *taught*. It says nothing about whether the player can *retrieve* it later.

### Learning by doing

Hodent's summary of the learning research for game designers comes down to a few principles you will see in every good tutorial.

- **Learn by doing.** A player who presses the button remembers it better than one who reads about it. Text boxes are the weakest form of teaching you have.
- **Teach in context.** Introduce a mechanic when the player has a reason to use it. A prompt about climbing means little on a flat field. In front of a cliff, it is an invitation.
- **Space and repeat.** One use is not enough. A mechanic needs several uses spread over time before it sticks.
- **Retrieval makes memory.** Having to pull a skill out of memory, without a prompt, strengthens it more than seeing it again. Roediger and Karpicke (2006) showed this with students learning prose passages. Students who were tested on the material remembered more a week later than students who spent the same time restudying it. Psychologists call it the **testing effect**. In a game, the "test" is a situation that needs the mechanic and doesn't say so.

The last two principles are what the worked example turns into numbers.

## 2. Worked example: the forgetting gap

### The hook

The Legend of Zelda: Breath of the Wild (2017) is famous for letting you go anywhere. Yet it starts by trapping you. Link wakes on the Great Plateau, a high area surrounded by cliffs. An old man tells him there is no safe way down without a paraglider like his own. He offers to trade it for the treasure in a nearby shrine. When Link returns with it, the old man changes the deal. He wants the treasures of all four shrines on the plateau.

Each of those four shrines gives Link one new ability, called a rune: Magnesis (moving metal objects), Remote Bomb, Stasis (freezing an object in time) and Cryonis (making ice pillars in water). Between the shrines lies open ground, full of metal boxes, boulders, enemy camps and water.

So an open-world game holds the player in a fenced area and makes them earn four abilities one at a time before letting them out. Why would a game about freedom open with a fence?

The designers' intentions aren't something we can read off the game. The model below gives one account of what the plateau's structure *does*, and it works for any tutorial you will design.

### The model

We track one number per mechanic: the chance the player can recall it at a given moment.

```
recall(t) = e^(−Δ / s)
```

- `Δ` is the time in minutes since the player **last used** the mechanic (or since it was taught, if they haven't used it since).
- `s` is the **stability** of the memory, also in minutes. Larger `s` means slower forgetting. When `Δ = s`, recall has fallen to `e^(−1) = 0.37`.
- When a mechanic is taught with one guided use, stability starts at `s₀`. We use `s₀ = 20` minutes.
- Each later **practice use**, where the player uses the mechanic again on their own, multiplies stability by a gain `g` and resets `Δ` to zero. We use `g = 2.5`.

So after `k` practice uses, `s = s₀ × g^k`. This is a simplified version of the forgetting curve from week 1, with the spacing effect built in as the growth in `s`. The exponential shape is the one you met in MA101 week 4.

The numbers `s₀ = 20` and `g = 2.5` are teaching choices, not measurements. Real values depend on the mechanic, the player and how the use happened. What we want from the model is the *comparison* between two schedules, and that turns out to hold across a wide range of parameters. You will test that claim in the interactive.

Three definitions complete the model.

- The **moment of need** `T` is the first time the game requires the mechanic without prompting, for example a fight that can't be won without it.
- The **forgetting gap** for a mechanic is `Δ` at `T`, the time between its last use and the moment of need.
- **All-ready recall** is the product of the recall values of every mechanic the moment of need requires, assuming they are forgotten independently. It is the chance the player walks in with everything available.

### Numbers you can check

An invented action RPG teaches four abilities before its first elite fight, the Warden, at minute 40. The Warden needs all four: **Dash**, **Ward**, **Hook** and **Burst**. Two teams propose two schedules.

**Schedule A, front-loaded.** A tight ten-minute tutorial. Dash is taught at minute 2, Ward at 4, Hook at 6, Burst at 8. At minute 10 a "training arena" makes the player use all four once more. Then the story takes over. Thirty minutes of exploration, dialogue and easy enemies follow, none of which needs the four abilities.

**Schedule B, interleaved.** Each ability arrives in its own small area and is then used by the content that follows.

| Ability | Taught (min) | Practice uses (min) |
|---|---|---|
| Dash | 2 | 6, 14, 24 |
| Ward | 10 | 16, 26 |
| Hook | 20 | 28, 34 |
| Burst | 30 | 36 |

Compute recall at `T = 40` for each ability.

| Ability | A: practice uses | A: `s` | A: gap `Δ` | A: recall | B: practice uses | B: `s` | B: gap `Δ` | B: recall |
|---|---|---|---|---|---|---|---|---|
| Dash | 1 | 50 | 30 | 0.549 | 3 | 312.5 | 16 | 0.950 |
| Ward | 1 | 50 | 30 | 0.549 | 2 | 125 | 14 | 0.894 |
| Hook | 1 | 50 | 30 | 0.549 | 2 | 125 | 6 | 0.953 |
| Burst | 1 | 50 | 30 | 0.549 | 1 | 50 | 4 | 0.923 |
| **All-ready** | | | | **0.091** | | | | **0.747** |

Check two cells by hand. Schedule A, any ability: one practice use gives `s = 20 × 2.5 = 50`, the last use was at minute 10, so `Δ = 30` and recall is `e^(−30/50) = e^(−0.6) = 0.549`. Schedule B, Ward: two practice uses give `s = 20 × 2.5² = 125`, the last use was at 26, so `Δ = 14` and recall is `e^(−14/125) = e^(−0.112) = 0.894`.

Under schedule A, the average player walks into the Warden fight with about 55% recall of each ability and a 9% chance of having all four. Put differently, they expect to be missing `4 × (1 − 0.549) = 1.8` abilities. Under schedule B, the same player expects to be missing `0.05 + 0.11 + 0.05 + 0.08 = 0.28` abilities, and three players in four have all of them.

Now look at the number a busy team tracks. "Minute at which every required ability has been taught": schedule A scores 8, schedule B scores 30. By that measure, A is almost four times better. It is the checklist view, and it ranks the schedules the wrong way round.

Remove the training arena from schedule A and the gap gets worse. Each ability is then used once, at teaching, and recall at minute 40 is `e^(−38/20) = 0.150` for Dash up to `e^(−32/20) = 0.202` for Burst. All-ready recall drops to under 0.1%. The arena is doing a lot of work for A. It just happens too early.

### A visual you can move

Open `examples/w07-forgetting-gap.html`. The top panel is a timeline from minute 0 to 60. Each ability has a row with a dot where it is taught, ticks where it is practised, and a vertical line at the moment of need. The top panel also carries a "taught" counter that fills to 4/4, and on schedule A it fills early. The bottom panel draws each ability's recall curve over the same minutes. It jumps up at each use and decays between them. At the moment of need the curves are read off and multiplied into the all-ready number.

On first load, schedule A is shown. The top panel looks finished by minute 8. The bottom panel shows four curves sagging together through the long story stretch and meeting the Warden line at 0.55. Switch to schedule B. The counter now fills late, but the curves arrive at the Warden line above 0.89. Then drag the practice ticks. Move one of Dash's uses in schedule B from minute 24 to minute 38 and watch its recall at the Warden rise. Or add a practice use at minute 30 to schedule A and see how much one late use buys compared with the whole arena.

Change `s₀` and `g` in the advanced panel. With `s₀ = 10` and `g = 2`, both schedules drop, and B still beats A. With `s₀ = 40` and `g = 3`, both rise, and B still beats A. Find a setting where A wins. You will need to make forgetting so slow that the gap barely matters. Then ask whether that describes new players learning a new game.

### Cross-game recognition

Rewrite any onboarding sequence as a timeline of *taught*, *practised* and *needed*, and the same question appears. How long is the gap between the last use and the moment of need, and how many uses built up stability before it?

**The Legend of Zelda: Breath of the Wild (2017).** On the Great Plateau, each shrine is a teaching event for one rune, followed by practice uses inside the shrine. The open ground between shrines gives spaced practice. Metal boxes invite Magnesis, boulders invite Stasis, and water invites Cryonis. The moment of need is the rest of Hyrule, where the game stops pointing at the right tool. The paraglider trade makes sure no player reaches that moment with a rune they have used only once. Read through the model, the fence enforces a minimum number of practice uses per rune before the long gaps begin.

**Super Mario 3D Land (2011).** In his 2012 interview with Game Developer, director Koichi Hayashida described building levels around the four-part structure of Japanese four-panel comics, *kishōtenketsu*. The level introduces a concept in a safe setting, develops it, throws in a twist that makes the player use it in an unexpected way, and ends with a conclusion. In our terms, a single gimmick is taught, practised at least twice, and then *retrieved under changed conditions* within a few minutes, with gaps short enough that recall stays high. The twist is the testing effect built into level design.

**World of Warcraft, Exile's Reach (Shadowlands pre-expansion, patch 9.0.1, October 2020).** New players now start on an island built as a level 1-10 starting zone. The story on the island ends in a two-boss mini-dungeon for one to five players, with scaling difficulty and no role requirements. Existing players making a new character can choose it or their race's usual starting zone. The mini-dungeon is a designed moment of need, placed at the end of the teaching zone rather than an hour later in the open world. It also introduces grouping in a setting where a mistake costs little.

Three games, three structures, one timeline. When you review a tutorial, don't ask "was it taught?" Ask "when was it last used before it was needed?"

### Eyes-open design judgment

- **Interleaving costs pace.** Schedule B delays the fourth ability to minute 30. If Burst is the most exciting thing in your game, you have hidden your best toy for half an hour. Some teams accept a lower recall for a faster "wow." Make that trade on purpose, and add a late practice use before the moment of need.
- **The model rewards gating, and gating costs autonomy.** The Great Plateau works because the player can't leave. Players feel a fence, and some resent it. [Week 4](w04-self-determination-theory.md) covers why autonomy matters. Gate only the mechanics the next stretch of the game truly requires.
- **Practice has to be real use.** A practice tick counts only if the player actually retrieves the mechanic. A prompt that says "Press Q to Hook!" at every hook point makes each use a reading exercise rather than retrieval. Remove prompts as soon as the player has used the mechanic unprompted once or twice.
- **Knowledge in the world is the alternative to memory.** For a mechanic used once an hour, stop fighting the forgetting curve. Put the reminder on the screen when it is needed, as week 1's "knowledge in the world" suggests. A contextual prompt at the moment of need sets recall to 1. It costs screen space and attention (week 2), and it removes the retrieval that would have strengthened the memory.
- **The numbers are illustrative.** Nobody measured `s₀ = 20` for Dash. Use the model to compare schedules and to find long gaps, and use a playtest (week 8) to find out whether players actually forget.

### Check yourself (worked example)

1. A mechanic is taught at minute 0, practised at minutes 5 and 15, and needed at minute 45. With `s₀ = 20` and `g = 2.5`, what is recall at the moment of need?
2. Schedule A's team refuses to change their tutorial but agrees to one extra use of each ability, all at the same minute. Which minute between 11 and 39 maximises all-ready recall at minute 40, and what is it?
3. How many practice uses does a mechanic need so that recall is still at least 0.9 after a 60-minute gap?

<details>
<summary>Answers</summary>

1. `s = 20 × 2.5² = 125`, `Δ = 45 − 15 = 30`, recall `= e^(−30/125) = e^(−0.24) = 0.787`.
2. Each ability then has two practice uses, so `s = 125`, and recall at minute 40 is `e^(−(40 − m)/125)` for a use at minute `m`. That rises as `m` approaches 40, so the latest minute wins. At minute 39, recall is `e^(−1/125) = 0.992` per ability and all-ready recall is `0.992⁴ = 0.969`. The catch is that one late use of everything is massed revision right before an exam. It works for this fight and builds less stability for the next one than spaced uses would.
3. Need `e^(−60/s) ≥ 0.9`, so `s ≥ 60 / 0.1054 = 569.5`. Then `20 × 2.5^k ≥ 569.5` gives `2.5^k ≥ 28.5`, so `k ≥ ln 28.5 / ln 2.5 = 3.65`. Four practice uses.

</details>

## 3. A toolkit of teaching patterns

The worked example compared two schedules. In practice, each mechanic gets its own teaching pattern, chosen by how often it is needed, how dangerous it is to get wrong, and who is learning.

| Pattern | What it is | Good for | Costs |
|---|---|---|---|
| Tutorial level | A dedicated space with guided steps | Core controls every player needs in the first minutes | Pace; bores experts unless skippable |
| Safe practice then test | Introduce in a low-risk room, then require it under pressure | Core mechanics that the game will test hard later | Level design time; can feel slow |
| Gated area | Player can't progress until the mechanic has been used | Mechanics the next stretch of content depends on | Autonomy; players feel the fence |
| Contextual prompt | A hint shown at the moment the mechanic becomes useful | Rarely used actions; first use of a new system | Screen space, attention, and it replaces retrieval |
| Delayed hint | A hint shown only after the player has been stuck for a while | Puzzles and exploration where discovery is the fun | Some players wait out the timer instead of trying |
| Skill check or skip | A short test that lets a skilled player bypass teaching | Genre veterans, returning players, alts | Players who skip may miss a genuinely new mechanic |
| Codex or help screen | Reference material the player can open | Detailed rules, numbers, lore | Players rarely open it; it teaches nothing by itself |

A few rules of thumb follow from the model and from earlier weeks.

**One new thing at a time.** Four chunks of working memory (week 1) is the ceiling for a player who is otherwise idle. A tutorial that introduces a mechanic while the player is also learning the camera is spending that budget twice. Hayashida's structure puts one gimmick in each level for a reason.

**Teach where it's used.** A mechanic taught in context gets its first practice use for free. A mechanic taught in a menu gets none.

**Fade the prompts.** The best prompt is one that disappears. Show the button prompt the first two times, then show it only if the player hesitates for a few seconds, then never. Each stage turns a reading task into a retrieval task.

**Give experts a door.** Week 3's Ana quit after three bored levels. A skill check at the start, or a "skip tutorial" option that confirms the player already knows the controls, costs little and keeps her. Make sure the skip doesn't also skip a mechanic that is unique to your game. A veteran of other action RPGs still doesn't know how your Ward works.

**Plan for the returning player.** MMOs have a second onboarding problem. A player who comes back after three months has a forgetting gap of 130,000 minutes. Their keybinds are there. Their rotation is gone. Expansions that open with a short, low-risk "refresher" quest and a clear current objective are running a second tutorial for exactly this player.

## 4. Measuring onboarding

You can't see recall directly, but you can see its effects. Four measures are worth building into every playtest and every build's telemetry.

**Step completion funnel.** List the onboarding steps in order and record the share of players who complete each one. The week 3 lecture turned achievement percentages into retention per step. Do the same here with your own tutorial steps. A step that loses 20% of players is a place to look.

**Time to first unprompted use.** For each core mechanic, log the time between teaching and the first use the player makes without a prompt. Long times, or players who never do it, signal a mechanic that was taught but not learned.

**Performance at the moment of need.** At the first elite fight, the first puzzle that combines two runes, or the first group dungeon, record which mechanics players use. If a third of players never use Ward in the Warden fight, that is your forgetting gap made visible, whatever the tutorial checklist says.

**Help and hint usage.** Count how often players open the help screen, trigger a delayed hint or search the settings for a keybind. Those are players reaching for knowledge in the world because their memory failed.

Next week you will run a usability test on an onboarding sequence. The Age of Empires II team you'll meet there wrote down, before testing, a list of things every player had to be able to do after the tutorial. That list is a list of moments of need. Write yours before you build your tutorial, not after.

## In-class activity (25 minutes)

Pairs. Pick a game you both know, and write down its first 30 minutes from memory as best you can. If neither of you remembers it well, use Breath of the Wild's Great Plateau from section 2.

1. **Timeline (10 min).** On a sheet with minutes across the top, mark every mechanic the game teaches (dot), every time you remember using it again (tick), and the first moment the game required it without a prompt (vertical line).
2. **Compute (8 min).** For the two mechanics with the longest forgetting gap, compute recall at the moment of need with `s₀ = 20` and `g = 2.5`.
3. **Redesign (7 min).** Move or add at most two practice uses so that both mechanics reach recall of at least 0.8. Say where in the game each new use would happen and what content it would need.

Expected output: an annotated timeline, two recall values before and after, and one sentence naming what your change costs (pace, autonomy, level design time).

## Common misconceptions

- **"We taught it, so the player knows it."** Taught and retrievable are different things. The checklist measures the first. The moment of need tests the second.
- **"More tutorial text makes a better tutorial."** Text is the weakest teaching form, and every box competes for working memory. Replace text with a situation that makes the player use the mechanic.
- **"A prompt every time is the safe choice."** It guarantees this use and weakens the next, because it removes retrieval. Fade prompts after the player has used a mechanic unprompted.
- **"The tutorial is the first ten minutes."** Onboarding runs until the player can play without help, often hours in an RPG. It also restarts for every returning player.

## Check yourself

1. A mechanic has stability `s = 50` minutes. How long after its last use does recall fall below 0.5?
2. A tutorial teaches a mechanic at minute 5 and the game first needs it at minute 65, with no uses in between. The team proposes one practice use. Using the model, compare placing it at minute 15 with placing it at minute 55.
3. Your game's crafting system is used about once per hour of play. Would you teach it with a tutorial level, a contextual prompt or a codex entry? Justify with the model and with week 2.
4. Telemetry shows that 35% of players never use the Ward ability in the first elite fight, although 98% completed the tutorial step that taught it. Give two explanations and say what data would tell them apart.

<details>
<summary>Answers</summary>

1. Solve `e^(−Δ/50) = 0.5`, so `Δ = 50 × ln 2 = 34.7` minutes.
2. After one practice use, `s = 50`. At minute 15, `Δ = 50` at the need and recall is `e^(−1) = 0.368`. At minute 55, `Δ = 10` and recall is `e^(−0.2) = 0.819`. The late use wins by a wide margin. Two uses, one early and one late, would be better still for the long run.
3. A contextual prompt at the crafting station. With an hour between uses, a mechanic needs many spaced uses before recall survives the gap (question 3 of the worked example needed four for a 60-minute gap at 0.9). A tutorial level would be forgotten before the second use. The prompt puts the knowledge in the world, and its cost in attention is paid only when the player is already at the station and not under pressure. A codex entry alone teaches nothing, because few players open it.
4. Forgetting: players learned Ward but lost it by the fight. Check the time since their last use of Ward, and whether players with a shorter gap used it more. Never learned: players clicked through the tutorial step without understanding. Check time on that step, whether they ever used Ward unprompted after it, and think-aloud remarks from a playtest. A third possibility is that the fight doesn't need Ward as much as the designers think, which you can check by comparing clear rates for players who used it and those who didn't.

</details>

## Lab hook

[Lab 07, onboarding timeline audit](../labs/lab07.md). You record the first 30 to 45 minutes of a shipped game, log every teaching event, practice use and moment of need for its core mechanics, run the starter script to compute recall at each moment of need, and propose a revised schedule. Deliverable: the event log, the script output, a timeline figure and a two-page audit.

## Sources

- The Legend of Zelda: Breath of the Wild (Nintendo, 2017). Zelda Wiki (zeldawiki.wiki), "Great Plateau," "Paraglider," "Oman Au Shrine," "Ja Baij Shrine," "Owa Daim Shrine" and "Keh Namut Shrine," accessed September 2026. The plateau is isolated by cliffs; the Old Man offers the paraglider for the treasure of the Oman Au Shrine and then asks for the remaining three shrines; the four shrines grant Magnesis, Remote Bomb, Stasis and Cryonis.
- Nutt, C. (2012, April 13). "The Structure of Fun: Learning from *Super Mario 3D Land*'s Director." Game Developer (then Gamasutra). Koichi Hayashida on introducing a concept safely, developing it, a twist, and a conclusion, and the comparison with *kishōtenketsu* in four-panel comics.
- Warcraft Wiki (warcraft.wiki.gg), "Exile's Reach," accessed September 2026. Introduced in patch 9.0.1 (13 October 2020); level 1-10 starting zone; new players start there automatically; ends in a two-boss mini-dungeon for 1 to 5 players with scaling difficulty and no role requirements.
- Roediger, H. L. & Karpicke, J. D. (2006). "Test-enhanced learning: Taking memory tests improves long-term retention." *Psychological Science*, 17(3), 249-255. The testing effect.
- Ebbinghaus, H. (1885). *Über das Gedächtnis*. The forgetting curve and the spacing effect, as summarised in UX201 week 1.
- Hodent, C. (2017). *The Gamer's Brain*. CRC Press. Chapters "Memory" (pp. 35-50) and "Learning Principles" (pp. 83-90).
- The recall model, `s₀ = 20`, `g = 2.5`, the four abilities and both schedules are teaching models built for this lecture, not measurements of any game.

## Interactive spec: examples/w07-forgetting-gap.html

**Purpose.** Show that a tutorial that finishes teaching early can leave players worse prepared at the moment of need than one that finishes late, because recall depends on the gap since last use and the number of spaced uses.

**The one insight the visual must make obvious.** With schedule A loaded, the "taught" counter reads 4/4 at minute 8 while the recall curves meet the moment-of-need line at 0.55 each (all-ready 9%). Switching to schedule B makes the counter fill later (minute 30) and the curves meet the line near 0.9 or above (all-ready 75%).

**Layout.** Two stacked panels sharing one x axis (minutes 0 to 60), controls below, numbers panel at the side on desktop (1280px) and below the charts on mobile (390px).

- Top panel, "Taught and practised": one row per ability. A filled circle at the teaching minute, a tick at each practice use, a vertical dashed line across all rows at the moment of need `T`. A counter at the top right reads "Taught: n/4" and updates as a playhead moves; also show a small step line of "abilities taught so far" across the panel.
- Bottom panel, "Recall": y axis 0 to 1. One line per ability showing `recall(t)` from its teaching minute onward, jumping to 1 at each use and decaying between uses. At `T`, a marker on each line with its value labelled. A shaded band from 0.8 to 1 labelled "reliable."

**Data (defaults).**

- `T = 40`, `s₀ = 20`, `g = 2.5`.
- Schedule A: Dash taught 2, uses [10]; Ward taught 4, uses [10]; Hook taught 6, uses [10]; Burst taught 8, uses [10].
- Schedule B: Dash taught 2, uses [6, 14, 24]; Ward taught 10, uses [16, 26]; Hook taught 20, uses [28, 34]; Burst taught 30, uses [36].
- Schedule A without arena (preset): all four with uses [].

**Controls.**

- Schedule toggle A / B / Custom. Choosing Custom copies the current schedule for editing.
- In Custom, drag teaching dots and practice ticks along their row (snap to whole minutes), click on a row to add a tick, and select a tick and press Delete (or a remove button) to remove it. Keyboard alternative: a table of numeric inputs per ability.
- `T` slider 10 to 60 (default 40).
- Advanced: `s₀` slider 5 to 60 (step 1, default 20), `g` slider 1.0 to 4.0 (step 0.1, default 2.5).
- Toggle "Prompt at the moment of need": when on, recall at `T` is shown as 1.0 for every ability, with a note "knowledge in the world: recall not tested."
- Presets: "A: front-loaded", "B: interleaved", "A without arena", "A plus one late use at 39", "Slow forgetting (s₀ = 40, g = 3)", "Fast forgetting (s₀ = 10, g = 2)".
- Reset.

**Formulas.**

- For each ability with teaching minute `t₀` and sorted uses `u₁ < u₂ < ...` (only uses after `t₀` count; uses at or after `T` are ignored for the value at `T`): stability after `k` uses is `s₀ × g^k`. For a time `t ≥ t₀`, let `k` be the number of uses at or before `t` and `last` be the latest of `t₀` and those uses. Then `recall(t) = exp(−(t − last) / (s₀ × g^k))`. Before `t₀`, draw nothing.
- All-ready recall = product of the four `recall(T)` values.
- Expected abilities missing = `Σ (1 − recall(T))`.
- "Fully taught at" = the latest teaching minute.

**Numbers panel.** Per ability: practice uses before `T`, stability `s`, gap `Δ`, recall at `T` (3 decimals). Totals: all-ready recall (percent, 1 decimal), expected abilities missing (2 decimals), "fully taught at minute n". A sentence built from the data, for example "Schedule A finished teaching at minute 8. At the Warden (minute 40), a typical player has a 9.1% chance of having all four abilities ready."

**Test values.**

- Schedule A defaults: each ability `s = 50`, `Δ = 30`, recall 0.549; all-ready 0.091 (9.1%); expected missing 1.80; fully taught at 8.
- Schedule B defaults: Dash `s = 312.5`, `Δ = 16`, 0.950; Ward `s = 125`, `Δ = 14`, 0.894; Hook `s = 125`, `Δ = 6`, 0.953; Burst `s = 50`, `Δ = 4`, 0.923; all-ready 0.747; expected missing 0.28; fully taught at 30.
- A without arena: Dash 0.150, Ward 0.165, Hook 0.183, Burst 0.202; all-ready 0.0009.
- A plus one late use at 39 for every ability: each `s = 125`, `Δ = 1`, 0.992; all-ready 0.969.
- Single-mechanic check: taught 0, uses [5, 15], `T = 45`: `s = 125`, recall 0.787.
- With `s₀ = 10, g = 2` and `s₀ = 40, g = 3`, schedule B's all-ready recall stays above schedule A's.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark. Abilities differ by colour and by marker shape (circle, square, triangle, diamond) and each line is labelled at its right end. The "reliable" band uses a pattern as well as a tint. All drag interactions have the numeric-table alternative and are keyboard operable. Respect reduced motion (no animated playhead when set). No game art, logos or screenshots; abilities are drawn as plain shapes.
