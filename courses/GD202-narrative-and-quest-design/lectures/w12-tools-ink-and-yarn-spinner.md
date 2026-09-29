# GD202 · Week 12 — Tools: Ink and Yarn Spinner

**Why this matters:** Since week 3 you have drawn branching dialogue as boxes and arrows. Shipped games store it as text files written in a narrative scripting language, compiled, checked and run by a small engine inside the game. Ink and Yarn Spinner are the two open-source languages you are most likely to meet. This week you learn to read and write both, and you work out the math behind one feature they share, choosing which variant of a line to play so players don't notice the repetition.

**You will be able to:**
- Write a short branching scene with state in both ink and Yarn Spinner, and explain what each construct compiles to (a node, an edge, a variable, a counter).
- Compute the chance that a player hears a repeated line under random, shuffle-bag and cycle selection, and the number of lines each rule needs to meet a repetition target.
- Compare ink and Yarn Spinner on structure, variation, localization support and engine integration, and choose one for a given project.
- Describe how a game's code drives either runtime: ask for the next line, show choices, send back the player's pick, save state.

**Before class:** inkle, *Writing with Ink* (github.com/inkle/ink, `Documentation/WritingWithInk.md`), Part One sections 1-4 and section 8 "Variable Text", including the "Multiline blocks" part of Part Two. Yarn Spinner documentation, version 3.1, "Nodes and Lines", "Options", "Once" and "Line Groups" (docs.yarnspinner.dev). Install Inky (inkle's free editor) or open Try Yarn Spinner in a browser before class.

**Prerequisites from earlier courses:** [GD202 week 3, branching structures](w03-branching-structures-and-the-combinatorial-explosion.md) (ink's weave and gathers as fold-back points). [GD202 week 4, dialogue systems and state flags](w04-dialogue-systems-and-state-flags.md) (flags, counters, and ink knots as read counts). [GD202 week 11, writing for localization](w11-writing-for-localization.md) (line IDs, plurals). [CS102 week 8, graphs, maps and dialogue](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w08-graphs-maps-and-dialogue.md) (a dialogue file as a directed graph; ink's loose-end warning as a dead-end check). [CS102 week 11, state machines](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w11-state-and-state-machines.md). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md).

**Interactive:** [`examples/w12-bark-repetition.html`](../examples/w12-bark-repetition.html). Keep it open during section 2.

---

## 1. Why writers use a scripting language

You could store dialogue in a spreadsheet, or as nested data in JSON, or in a node editor with boxes and arrows. Many games do. A **narrative scripting language** makes a different trade: the writer types the scene as a plain text file that reads almost like a screenplay, and a compiler turns it into the graph and state the game runs.

What that buys a team:

- **Writers own the files.** Text files can be edited in any editor, compared line by line in version control, reviewed, and merged when two writers touch the same scene. Node editors and binary assets are much harder to merge.
- **The compiler checks structure.** CS102 week 8 built a linter that finds dead ends and unreachable lines. Ink's compiler warns about a "loose end", content where the flow runs out with no divert, choice or end. That is CS102 week 8's dead-end check, run every time you save.
- **State lives with the text.** Flags and counters from week 4 are declared and tested in the same file as the lines they control.
- **The game asks, the script answers.** Game code doesn't need to know the story's shape. It runs a loop: ask the runtime for the next line, show it; if there are choices, show them and send back the player's pick. That separation lets writers change a scene without a programmer.

The cost is that writers learn a small programming language, with its own syntax errors. Both tools keep it small on purpose.

Two tools dominate the open-source end of this space.

- **Ink**, by inkle, the studio behind 80 Days and the Sorcery! adaptations. Ink, its editor Inky and its Unity integration are free under the MIT license. An Unreal Engine integration called Inkpot was made by The Chinese Room. The current release is ink v1.2.1 (May 2026).
- **Yarn Spinner**, used in Night in the Woods, A Short Hike, DREDGE and Lost in Random, among others. It is MIT-licensed and supports Unity, Godot and Unreal. The current release of the core compiler and runtime is v3.2.1 (May 2026); the Unity package has its own, faster release numbers. This lecture follows the version 3.1 documentation.

Both do the same job. Section 2 works through a problem they both solve, then sections 3 and 4 teach each language through one scene.

## 2. Worked example: shuffle, cycle or dice?

### The hook

In The Elder Scrolls V: Skyrim (Bethesda, 2011), town guards share a pool of idle lines. One of them, a guard remembering that he "took an arrow in the knee", became one of the biggest memes of the game's year. A large part of the joke was repetition. Players heard it from guard after guard, often within minutes.

The Yarn Spinner documentation uses that same line to demonstrate its `once` feature. Tool makers know the problem well. Any line that fires on an event, such as a greeting, a bark, a reaction or a shopkeeper's hello, gets heard many times. Writing more variants helps, but the rule that picks the variant matters far more. The question for this week: *with `n` variants of a line, how soon does a player hear a repeat, and how many variants does each selection rule need?*

### The model

A line fires `k` times. There are `n` written variants. Four selection rules:

1. **Random (dice).** Each time, pick one of the `n` variants uniformly at random, independently of past picks. This is sampling with replacement.
2. **Shuffle bag.** Put all `n` variants in a bag in random order and play them one by one. When the bag is empty, reshuffle and start again.
3. **Cycle.** Play the variants in a fixed order, 1, 2, ..., `n`, then start over.
4. **Stopping.** Play them in order and stick on the last one forever. (A **once** rule is stopping with a blank last entry: after the variants run out, play nothing.)

Under random selection, the chance that the first `k` plays are all different is the birthday-problem product:

```
P(no repeat in k plays) = (n/n) × ((n − 1)/n) × ((n − 2)/n) × ... × ((n − k + 1)/n)
P(at least one repeat)   = 1 − P(no repeat in k plays)          (the complement rule, MA102 week 3)
P(this play repeats the last one)            = 1/n
expected back-to-back repeats in K plays     = (K − 1)/n
```

Under a shuffle bag, the first `n` plays never repeat. A back-to-back repeat can only happen where one bag ends and the next begins, when the new bag's first line happens to be the old bag's last. That has chance `1/n` at each boundary:

```
expected back-to-back repeats in K plays = floor((K − 1)/n) × (1/n)
longest wait between two hearings of the same line = 2n − 2 other lines
```

The longest wait comes when a line is first in one bag and last in the next.

A cycle never repeats back to back (for `n ≥ 2`), but its order is fixed, so a player who hears it twice learns the pattern.

### Numbers you can check

Chance of at least one repeat within the first `k` plays under random selection:

| Variants n | k = 2 | k = 3 | k = 4 | k = 5 | k = 6 |
|---|---|---|---|---|---|
| 5 | 0.20 | 0.52 | 0.81 | 0.96 | 1.00 |
| 10 | 0.10 | 0.28 | 0.50 | 0.70 | 0.85 |

Check the `n = 5`, `k = 3` cell. No repeat is `1 × 0.8 × 0.6 = 0.48`, so a repeat is `0.52`. With five variants picked by dice, more than half of players hear a repeat by the third bark. With ten variants, it's a coin flip by the fourth.

Under a shuffle bag, every cell with `k ≤ n` is exactly 0.

Back-to-back repeats over 100 plays of the same event:

| Variants n | Random | Shuffle bag | Cycle |
|---|---|---|---|
| 3 | 33.0 | 11.0 | 0 |
| 5 | 19.8 | 3.8 | 0 |
| 10 | 9.9 | 0.9 | 0 |

Check the `n = 5` shuffle cell. 100 plays make 20 bags with 19 boundaries between them, and each boundary repeats with chance 1/5, so `19 × 0.2 = 3.8`.

Now the number that should change how you budget writing time. Say you want at least a 90% chance that a player's first five hearings are all different:

```python
def p_no_repeat(n, k):
    """Chance that k random picks (with replacement) from n lines are all different."""
    p = 1.0
    for i in range(k):
        p *= (n - i) / n
    return p

def lines_needed(k, target):
    """Fewest lines so that k random picks are all different with chance >= target."""
    n = k
    while p_no_repeat(n, k) < target:
        n += 1
    return n

for n in [5, 10]:
    print(n, [round(1 - p_no_repeat(n, k), 3) for k in range(1, 7)])
print("random needs", lines_needed(5, 0.9), "lines; a shuffle bag needs", 5)
```

```
5 [0.0, 0.2, 0.52, 0.808, 0.962, 1.0]
10 [0.0, 0.1, 0.28, 0.496, 0.698, 0.849]
random needs 97 lines; a shuffle bag needs 5
```

**Dice need 97 lines to do what a shuffle bag does with 5.** That's the writing budget of a whole character spent on one bark, just to hide the repetition.

### A visual you can move

Open the interactive. The top view is a timeline of plays, one colored tick per play with its variant number printed, run under the rule you pick. Back-to-back repeats are ringed. Switch from Random to Shuffle bag and the rings mostly vanish. The ones left sit only at bag boundaries, which are drawn as faint dividers. The bottom view plots the chance of at least one repeat against the number of plays for random selection, with a flat zero line for the bag up to `k = n`. Drag `n` and watch how slowly the random curve moves right.

### Cross-game recognition

**Ink (v1.2.1).** Ink writes the four rules as inline alternatives. `{a|b|c}` is a stopping sequence, `{&a|b|c}` a cycle, `{!a|b|c}` once-only and `{~a|b|c}` a shuffle. The documentation calls the multiline `shuffle` block a "shuffled cycle", meaning it shuffles, plays through, then reshuffles. The runtime source confirms it's a bag. For each pass through the sequence, `NextSequenceShuffleIndex` in `Story.cs` seeds a random generator from the sequence's path and the loop count, builds the list of unpicked indices, and removes each one as it's chosen. No repeats within a loop, a fresh shuffle for the next. Ink's `RANDOM(min, max)` function, used to pick a line, gives you dice instead.

**Yarn Spinner (3.x).** A **line group** is a set of lines starting with `=>`. Yarn Spinner picks one for you, and the docs suggest them for barks. The choice is made by a **saliency strategy**. The default, "Random Best Least Recently Viewed", sorts the lines that pass their conditions by how often they've been shown, then by condition complexity, and picks randomly among the best. For a group of equal lines, that's a shuffle bag. Once every line has been seen once, they tie again, and the next pick is random among all of them, including the one just played. Same `1/n` boundary repeat as ink. The "First" and "Best Least Recently Viewed" strategies are deterministic, closer to a cycle.

**Tetris (Guideline-era games).** You met this one in [MA102 week 10](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w10-pseudo-random-distribution-and-pity-timers.md) as a pity counter for every piece at once. Here it is a variant selector. Most official Tetris games that follow the Tetris Guideline deal pieces with what the community calls the 7-bag. All seven tetrominoes are shuffled, dealt, then reshuffled. TetrisWiki notes that it can't produce a run of more than 12 pieces between one I piece and the next. That's `2n − 2` with `n = 7`, the same longest-wait formula as a bark bag. A game with no dialogue solves the same problem, "random, but never too streaky", with the same bag.

### Eyes-open design judgment

- **Default to a bag for barks.** It hides repetition for `n` plays for free. Both tools do it by default or with one character.
- **Remove the boundary repeat when it matters.** If a back-to-back repeat is jarring (a companion's line in a quiet scene), reshuffle until the new bag doesn't start with the old bag's last line. That is a few lines of game code, or a custom saliency strategy in Yarn Spinner.
- **Use a cycle when order carries meaning.** A shopkeeper who says "Welcome", then "Back again?", then "You practically live here" should use stopping, not shuffle. The escalation is the joke. Ink's `{a|b|c}` and Yarn Spinner's `once` with `else` are built for this.
- **Know the cost of predictability.** A cycle never repeats back to back, but a player who hears it twice learns the order. For ambient barks the bag's surprise is worth the rare repeat.
- **Spend lines where they are heard.** A line that fires 200 times in a play-through (a combat bark) needs more variants and a bag. A line heard twice needs one good version. Count plays per line before you assign writing time. Week 14's narrative testing starts from this count.
- **Repetition is also a state problem.** Week 4's rule matcher chooses *which* line fits the situation. This week's rule chooses *which variant* of it plays. Most shipped systems do both, and a rule that matches too often defeats any bag.

### Check yourself (worked example)

1. A guard bark has 8 variants picked at random. What is the chance the first three barks a player hears are all different?
2. Over 50 plays of a 4-variant bark in a shuffle bag, how many back-to-back repeats do you expect? And with dice?
3. A designer wants a 50% chance that a player's first 5 hearings of a line are all different, using random selection. What is the smallest `n` that achieves it? (Try values; the lecture's code gives 17.) Why is this a poor use of writing time?

<details>
<summary>Answers</summary>

1. `1 × 7/8 × 6/8 = 42/64 ≈ 0.656`.
2. Bag: 50 plays make 12 full bags plus 2, so 12 boundaries, and `12 × 1/4 = 3`. Dice: `49 / 4 = 12.25`.
3. `n = 16` gives `P ≈ 0.4999`, just short, and `n = 17` gives `≈ 0.52`, so 17. A shuffle bag reaches 100% with 5 lines, so the other 12 lines buy nothing a free rule change wouldn't.

</details>

## 3. Ink through one scene

Ink stories are made of **knots** (named sections, `=== name ===`) joined by **diverts** (`-> name`). Choices start with `*` (once-only: used up after being picked) or `+` (sticky: always offered). A **gather**, a line starting with `-`, brings the branches of a choice back together, which week 3 called a fold-back point. Here is an invented scene at a town gate:

```
VAR has_pass = false

-> gate

=== gate ===
The guard looks up. {~"Move along."|"State your business."|"Road's closed."}
+ {has_pass} [Show the pass]
    "Fine. In you go."
    -> town
* [Ask about the road]
    "Raiders. Nobody gets through without a pass."
    -> gate
+ [Leave]
    -> END

=== town ===
You pass under the arch.
-> END
```

Read it as a graph and a state.

| Ink construct | In the scene | What it is |
|---|---|---|
| `=== gate ===` | the knot | a node |
| `-> town`, `-> gate` | diverts | edges |
| `VAR has_pass = false` | a global variable | a flag (week 4) |
| `+ {has_pass} [Show the pass]` | sticky choice with a condition | an edge that exists only when the flag is true |
| `* [Ask about the road]` | once-only choice | an edge removed after one use |
| `{~ ... }` | shuffle | variant selection (section 2) |
| `-> END` | end of story | a terminal node |

The text in square brackets is shown on the choice button but not printed after it's picked. That's how ink lets the button say "Ask about the road" while the story continues with the guard's reply.

Two more ink features you'll use constantly:

- **Read counts.** Every knot's name is also a number, how many times the player has seen it. `{gate > 2: "You again."}` works with no extra variable. Week 4 covered this.
- **Tags.** A line can end with `# tag`, and the game receives the tags alongside the line. Teams use tags for the speaker, portrait, camera, or a voice file.

**Running it.** The game compiles the `.ink` file to JSON (Inky and the Unity plugin do it for you) and drives the runtime with a short loop, described in inkle's *Running your ink* guide. While `canContinue` is true, call `Continue()` to get the next line and `currentTags` for its tags. When it stops, read `currentChoices`, show them, and call `ChooseChoiceIndex(i)` with the player's pick. Save with `state.ToJson()`. Variables are readable and writable from game code through `variablesState["has_pass"]`, which is how the game gives the player the pass.

## 4. Yarn Spinner through the same scene

Yarn Spinner organizes a story into **nodes**. Each node has a header (at least a `title:`), a `---` line, a body, and a closing `===`. Lines look like a screenplay, `Name: text`. Options start with `->`. Commands go in double angle brackets.

```
title: Setup
---
<<declare $has_pass = false>>
===

title: Gate
---
=> Guard: Move along.
=> Guard: State your business.
=> Guard: Road's closed.
-> Show the pass <<if $has_pass>>
    Guard: Fine. In you go.
    <<jump Town>>
-> Ask about the road <<once>>
    Guard: Raiders. Nobody gets through without a pass.
    <<jump Gate>>
-> Leave
===

title: Town
---
You pass under the arch.
===
```

The same scene, construct by construct:

| Yarn Spinner | Ink equivalent | Notes |
|---|---|---|
| node (`title: Gate`) | knot | Yarn nodes always have a header; ink knots are just a label line |
| `<<jump Town>>` | `-> town` | an edge |
| `<<declare $has_pass = false>>` | `VAR has_pass = false` | Yarn declarations take effect without the Setup node running |
| `-> ... <<if $has_pass>>` | `+ {has_pass} [...]` | conditional option |
| `-> ... <<once>>` | `*` | an option that can be picked only once |
| `=>` line group | `{~ ... }` | Yarn picks with a saliency strategy; the default behaves as a shuffle bag |
| `visited("Gate")`, `visited_count("Gate")` | `{gate}` read count | Yarn uses functions; ink makes the knot name a number |
| `#line:4c49c5` tags | none built in | Yarn adds unique line IDs for localization |

A difference that shows in the listing is who owns the structure. In ink, the flow is the text, and diverts are sparse because choices and gathers do most of the work inside a knot. In Yarn Spinner, each node is a small scene and `<<jump>>` connects them. Yarn Spinner's VS Code extension has a graph view that draws the nodes and the jumps between them. Writers who think in boxes and arrows often find Yarn Spinner easier to start with. Writers who think in prose often prefer ink's weave.

**Commands.** Anything in `<<...>>` that isn't a built-in is sent to the game as a command, for example `<<camera_shake 0.5>>`. The game registers a handler for each command name. This is Yarn Spinner's main way for scripts to make things happen in the scene, where ink teams usually use tags or external functions.

**Running it.** A **Dialogue Runner** component loads the compiled project and sends your game lines, options and commands. **Dialogue presenters** show them. You rarely write the loop yourself in Unity or Godot, but it is the same loop as ink's: line, line, options, pick, line.

## 5. Choosing and integrating

The comparison below lists only features documented by each project as of their current releases.

| Question | Ink (v1.2.1) | Yarn Spinner (v3.2.1, docs 3.1) |
|---|---|---|
| License | MIT | MIT |
| Engines | Unity plugin from inkle; Unreal via Inkpot (The Chinese Room) | Unity, Godot (C# and GDScript), Unreal |
| Structure | Knots, stitches, weave (choices and gathers), diverts | Nodes, options, jumps; node groups with `when:` conditions |
| Variation | Stopping, cycle, once, shuffle, shuffle once, shuffle stopping | Line groups and node groups picked by saliency strategies; `once` blocks |
| State | Global and temporary variables, lists, read counts, `TURNS_SINCE` | Declared variables, `visited`, `visited_count`, smart variables |
| Localization | No workflow described in *Writing with Ink*; teams build their own | `#line:` IDs, strings files, `plural` and `ordinal` markup using CLDR categories |
| Editor | Inky (desktop), plus plugin preview | VS Code extension with preview, Try Yarn Spinner in the browser |

Some honest rules of thumb:

- **Heavy localization or voice-over?** Yarn Spinner's line IDs and plural markup (week 11) solve problems an ink team will solve by hand. Ink can be localized. You just build the pipeline.
- **Prose-heavy, deeply branching text game?** Ink's weave was designed for writing long choice-rich passages without drawing boxes, which is how inkle's own games are made.
- **Many short, reactive conversations in a 3D world?** Either works. Yarn Spinner's node groups and saliency give you a storylet system (content chosen by conditions, like week 4's rule matcher) built in.
- **Who writes?** Hand a writer both tools for an afternoon and ask which one they want. The tool the writer is fastest in beats small feature differences.

Whatever you pick, set up three things on day one:

1. **Compile in the build.** Script errors should fail the build, not appear at playtest.
2. **Lint for your own rules.** The compiler checks syntax and structure. Your team's rules (every line has a speaker tag, every bark group has at least `n` variants, no line over 120 characters) need a small linter, like lab 11's.
3. **Keep IDs stable.** Line IDs tie a line to its translations and voice files. Never regenerate them for existing lines.

## In-class activity (30 minutes)

Pairs. One laptop runs Inky, the other Try Yarn Spinner.

1. Take the gate scene from section 3 in ink and section 4 in Yarn Spinner. Run both. Pick "Ask about the road" and confirm it disappears afterwards.
2. Add, in both tools, a line the guard says only the third time the player arrives at the gate (ink: a read count; Yarn Spinner: `visited_count`). Run it three times to check.
3. Add a second bark group for when the player *has* the pass, with four variants, and set it up so that it never repeats within four visits. Say which rule each tool used.
4. Swap laptops and review your partner's script. Write down one thing that was easier in each tool.

Expected output: both scripts, and a four-line comparison (two lines per tool) of what was easier.

## Common misconceptions

- **"Random is the natural way to vary a line."** Random is the worst of the four rules for hiding repetition. With 10 variants, half of players hear a repeat within four plays.
- **"A shuffle bag never repeats back to back."** It can, at the boundary between bags, with chance `1/n`. Fix it in code if it matters.
- **"Ink is for text games and Yarn Spinner is for 3D games."** Both are engine-agnostic runtimes that hand lines to your game. The difference is writing style and built-in features, not genre.
- **"The compiler catches narrative bugs."** It catches syntax, loose ends and missing targets. It can't tell you that a flag is never set or that a line fires too often. That's week 14.

## Check yourself

1. In ink, what is the difference between `* [Ask]` and `+ [Ask]`? What is the Yarn Spinner equivalent of the first?
2. Rewrite this ink line in Yarn Spinner as a line group: `The merchant {~waves|nods|ignores you}.`
3. A companion comment has 6 variants in a shuffle bag. What is the longest run of other comments a player can hear between two hearings of the same one?
4. A team must localize into eight languages with voice-over. Give two reasons from this lecture to choose Yarn Spinner, and one thing an ink team would need to build to match it.
5. Your bark fires 300 times per play-through and has 12 variants picked with dice. How many back-to-back repeats will a player hear, on average? With a bag?

<details>
<summary>Answers</summary>

1. `*` is once-only: the choice disappears after it's picked. `+` is sticky and stays. Yarn Spinner: `-> Ask <<once>>`.
2. Three `=>` lines, for example `=> The merchant waves.`, `=> The merchant nods.`, `=> The merchant ignores you.` With the default saliency strategy it behaves as a shuffle bag, as ink's `~` does.
3. `2 × 6 − 2 = 10` other comments.
4. Built-in `#line:` IDs that tie each line to its translations and audio files, and `plural` markup using CLDR categories. The ink team would need its own line-ID scheme and string export, and its own plural handling.
5. Dice: `299 / 12 ≈ 24.9`. Bag: `floor(299 / 12) = 24` boundaries, `× 1/12 = 2`.

</details>

## Lab hook

[Lab 12, variation engine](../labs/lab12.md). You implement the five selection rules (random, shuffle bag, no-repeat bag, cycle, stopping) in Python, measure them against this lecture's formulas, and then write a gate-guard scene of your own in ink or Yarn Spinner that uses stopping for escalation and a bag for ambient barks. Deliverable: the passing code, the script, and a short report with your measured repeat counts.

## Sources

- inkle, *Writing with Ink*, `Documentation/WritingWithInk.md`, github.com/inkle/ink (master branch, read September 2026). Loose-end warning; once-only `*` and sticky `+` choices; read counts; sequences, cycles, once-only and shuffles; the multiline `shuffle` as a "shuffled cycle"; `shuffle once` and `shuffle stopping`; `RANDOM`; `TURNS_SINCE`. The document has no localization section.
- inkle, *Running your ink*, `Documentation/RunningYourInk.md` (same repository). `Continue`, `canContinue`, `currentChoices`, `ChooseChoiceIndex`, `currentTags`, `state.ToJson`, `variablesState`.
- inkle, ink runtime source, `ink-engine-runtime/Story.cs`, method `NextSequenceShuffleIndex` (master branch, read September 2026). Shuffle picks without replacement within each loop, seeded from the sequence path and loop index.
- inkle, "ink" product page, inklestudios.com/ink (retrieved September 2026). Used in 80 Days and Sorcery!; ink, Inky and the Unity plugin under the MIT license; Inkpot Unreal integration by The Chinese Room.
- GitHub releases: inkle/ink v1.2.1 and YarnSpinnerTool/YarnSpinner v3.2.1, both May 2026.
- Yarn Spinner documentation, version 3.1 (docs.yarnspinner.dev): "Line Groups" (`=>`, conditions, `once`, barks), "Once", "Saliency" (strategies; default Random Best Least Recently Viewed), "Functions" (`visited`, `visited_count`), "Logic and Variables" (`<<declare>>`), "Tags and Metadata" (`#line`). The docs' own `once` example uses the "arrow in the knee" guard line.
- Yarn Spinner website, yarnspinner.dev (retrieved September 2026). Shipped games including Night in the Woods, A Short Hike, DREDGE and Lost in Random; Unity, Godot and Unreal support. MIT license stated in the documentation's introduction.
- Wikipedia, "The Elder Scrolls V: Skyrim" (retrieved September 2026). The "arrow in the knee" line became a widely circulated meme.
- TetrisWiki, "Random Generator" (retrieved September 2026). The 7-bag used in Tetris Guideline games; at most 12 pieces between one I piece and the next.

## Interactive spec: examples/w12-bark-repetition.html

**Purpose.** Let students see how often players hear repeated lines under each selection rule, and that the rule matters far more than the number of variants.

**The one insight the visual must make obvious.** With the same `n`, switching from random to a shuffle bag removes almost every back-to-back repeat, and the random rule needs roughly 20 times as many lines to match the bag's "first `k` plays all different" guarantee.

**Layout.** Two linked views, stacked at all widths (the timeline needs the width). A results strip between them.

- Top, "What the player hears": a horizontal timeline of `K` plays (default 40), one tick per play, drawn as a small rounded block with the variant number (1 to `n`) printed in it and a color per variant. Back-to-back repeats get a thick ring in the negative token plus a "!" glyph. For the bag rules, faint vertical dividers mark bag boundaries. For `K > 60`, blocks shrink and numbers are hidden, but rings stay.
- Results strip: "Back-to-back repeats: measured R, expected E", "First repeat at play j", "Distinct lines heard: d of n".
- Bottom, "How soon the first repeat comes": line chart, x axis plays `k` from 1 to 2n (at most 40), y axis 0 to 1. Solid line: `P(at least one repeat in first k)` for random selection. Dashed line: the same for the bag (0 up to `k = n`; after that, show the exact value from simulation, see below). Vertical marker at the current `k` target with the value printed. A text line: "Random needs N lines for a T chance of no repeat in the first k plays; a bag needs k."

**Controls** (keyboard accessible, values printed):

- Rule: radio group Random, Shuffle bag, No-repeat bag, Cycle, Stopping. Default Random on first load, with a "compare" button that splits the timeline into two rows (Random above, Shuffle bag below) using the same `n` and `K`.
- Variants `n`: slider 2 to 20, default 5.
- Plays `K`: slider 10 to 200, default 40.
- Target `k` and target chance `T`: sliders 2 to 10 (default 5) and 0.5 to 0.99 (default 0.90), used by the "lines needed" text.
- Seed: number input plus "Reroll" button. Same seed gives the same timeline.
- Reset button.

**Rules.**

- Random: each play is uniform on 1..n.
- Shuffle bag: Fisher-Yates shuffle of 1..n, play in order, reshuffle when empty (the new bag may start with the previous bag's last line).
- No-repeat bag: as shuffle bag, but if the new bag's first line equals the previous line, swap it with a random other position in the new bag.
- Cycle: 1, 2, ..., n, 1, 2, ...
- Stopping: 1, 2, ..., n, n, n, ...
- Use a small seeded generator (for example mulberry32) so seeds are reproducible.

**Formulas.**

- `P(no repeat in k) = Π_{i=0}^{k−1} (n − i)/n` for random; `P(at least one) = 1 − that`.
- Expected back-to-back: random `(K − 1)/n`; shuffle bag `floor((K − 1)/n)/n`; no-repeat bag, cycle 0; stopping `max(0, K − n)`.
- Lines needed: smallest `N ≥ k` with `P(no repeat in k) ≥ T` for random.
- Bag curve beyond `k = n`: estimate by 20,000 seeded simulations, cached per `n`.

**Test values.**

| n | k | P(at least one repeat), random |
|---|---|---|
| 5 | 2 | 0.200 |
| 5 | 3 | 0.520 |
| 5 | 4 | 0.808 |
| 10 | 4 | 0.496 |
| 10 | 5 | 0.698 |
| 20 | 5 | 0.419 |

Expected back-to-back repeats in `K = 100`: n = 3 random 33.0, bag 11.0; n = 5 random 19.8, bag 3.8; n = 10 random 9.9, bag 0.9. Lines needed for `k = 5`, `T = 0.90`: 97. For `k = 4`, `T = 0.90`: 59. For `k = 5`, `T = 0.50`: 17. Longest gap between two hearings of the same line in a shuffle bag: `2n − 2` (12 for n = 7).

**First screen.** Compare mode on, `n = 5`, `K = 40`, seed 1. The random row shows several rings; the bag row shows at most one or two, at dividers. Caption: "Same five lines. Different rule."

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css` inline, light and dark themes, reduced motion respected (no animated tick-by-tick playback when set; otherwise an optional "play" button animates the timeline at 4 plays per second). Variant colors are paired with printed numbers so color is never the only cue. Results strip is an `aria-live` region. No game art; lines are shown as numbers, not quoted text.
