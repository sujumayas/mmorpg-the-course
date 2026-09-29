# GD202 · Week 10 — Lore Delivery Without Walls of Text

**Why this matters:** Your world will have more history than any player will read. Every sentence you add to a text panel is read by fewer people than the one before it, so a long lore dump spends your writing budget on the sentences almost nobody reaches. This week you learn to predict how much of a text players actually read, and to split lore into pieces the world hands out.

**You will be able to:**
- Compute the expected number of sentences read from a text of any length, and its completion rate, with the reading-decay model.
- Estimate a game's per-sentence keep-reading chance from a completion rate measured in a playtest.
- Compare a single lore dump with a plan that splits the same lore into found pieces, and find the find-chance at which splitting stops paying.
- Critique a shipped game's lore delivery by naming its channels, its piece length and what the player must do to reach each piece.

**Before class:** Harvey Smith and Matthias Worch, "What Happened Here? Environmental Storytelling" (GDC 2010 talk, free on GDC Vault). From the course text, Bateman (ed.), *Game Writing: Narrative Skills for Videogames* (2nd ed., Bloomsbury, 2021), use the contents page to find the material on exposition and backstory, and read it. Reread your notes on quest text from [GD202 week 6](w06-quest-anatomy-hook-objective-complication-reward.md) (quest anatomy).

**Prerequisites from earlier courses:** [MA102 week 7, the geometric distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w07-geometric-distribution-kills-until-the-drop.md) (a constant chance of stopping at every step). [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md). [GD101 week 7, playtesting](../../GD101-introduction-to-game-design/lectures/w07-playtesting-observe-dont-explain.md) (how to watch without coaching). Running alongside this course, [GD201 week 8, environmental storytelling](../../GD201-level-and-world-design/lectures/w08-environmental-storytelling.md) computes the chance a player notices a clue in a space. This week uses that notice chance as an input and does not re-derive it.

**Interactive:** [`examples/w10-lore-chunking.html`](../examples/w10-lore-chunking.html). Keep it open during section 2.

---

## 1. Lore, story and the wall

**Lore** is the background of your world: history, factions, places, the reasons things are the way they are. It is different from the **story** the player is living through right now (week 1 separated story, narrative and plot). Lore explains why the bridge is broken. The story is that the player needs to cross it.

Writers always know far more lore than the player needs. That is healthy. A writer who knows why the bridge broke writes a better bridge scene. The trouble starts when the writer tries to hand all of it to the player at once, usually through a quest giver who talks for three screens, a codex entry the length of an essay, or a scrolling intro text. Players call these **walls of text**, and they skip them.

It helps to sort lore into three tiers before you write any of it:

| Tier | Question it answers | Who needs it | Example for the broken bridge |
|---|---|---|---|
| Need to know | What must the player understand to act? | Every player | The bridge is out. The ford is to the south. |
| Nice to know | What makes the current scene make sense? | Most players | Raiders burned it to stop the militia. |
| For the fans | What rewards digging? | A minority | The bridge was built by a guild that no longer exists, and its mark is on every stone. |

The tiers are about who needs the information, not about how important the writer feels it is. This week's model tells you where each tier has to go.

## 2. Worked example: the reading-decay model

### The hook

Destiny (Bungie, 2014) launched with a large body of written lore: backstory for characters, weapons, alien races and planets. Players unlocked it as Grimoire cards while they played. But the cards could only be read on Bungie's website or the Destiny companion app, not inside the game. At launch, the game was criticized for its lack of story content. The lore existed. Almost nobody read it. For Destiny 2 (2017), Bungie dropped the Grimoire cards and moved its storytelling into the game.

Destiny is the extreme case, but the same thing happens on a smaller scale in every game with long text. So ask a precise question. *If I write N sentences, how many does the average player read?*

### The model

Picture a player reading a text panel one sentence at a time. Before each sentence they either keep going or stop, close the panel and get back to playing. Assume the chance they keep going is the same at every sentence. Call it `s`, the **keep-reading chance**.

```
P(player reads sentence k)       = s^k
completion rate (reads all N)    = s^N
expected sentences read, E(N)    = s + s^2 + ... + s^N = s × (1 − s^N) / (1 − s)
ceiling as N grows without limit = s / (1 − s)
```

- `N` is the number of sentences in the text.
- `k` is a sentence's position, counting from 1.
- `s` is the keep-reading chance, a number between 0 and 1. The first sentence is a chance to stop too, since opening a panel is not reading it.

This is the geometric distribution from MA102 week 7 in a new costume. There, every kill was another roll for the drop. Here, every sentence is another roll for "the player stops reading." A constant stopping chance is an assumption, and section 3 says when it breaks. It is a good first model because it is simple enough to check by hand and it has one parameter you can measure.

Notice the ceiling. With `s = 0.8`, no text of any length gets more than `0.8 / 0.2 = 4` sentences read on average. **Past a certain length, extra sentences are written for almost nobody.**

### Numbers you can check

Take `s = 0.8`, a plausible value for quest text in the middle of a play session. (It is an assumption for this lecture. You measure your own game's `s` in section 3.)

| Sentences written (N) | Expected read, E(N) | Share of text read | Completion rate s^N |
|---|---|---|---|
| 1 | 0.80 | 80% | 80.0% |
| 2 | 1.44 | 72% | 64.0% |
| 3 | 1.95 | 65% | 51.2% |
| 5 | 2.69 | 54% | 32.8% |
| 10 | 3.57 | 36% | 10.7% |
| 20 | 3.95 | 20% | 1.2% |

Check one row by hand. For `N = 3`, `E = 0.8 + 0.64 + 0.512 = 1.952`. Going from 10 sentences to 20 doubles the writing, the voice-over cost and the translation cost (week 11). It adds 0.38 sentences read per player.

The same model tells you *which* sentences get read. Sentence 1 reaches 80% of players, sentence 3 reaches 51%, sentence 5 reaches 33%, sentence 10 reaches 11%. Whatever is in the need-to-know tier goes first. Journalists call this the **inverted pyramid**. The most important fact goes in the first sentence and detail comes after. Your quest text should be written the same way.

Here is the model in Python, so you can run your own numbers:

```python
def expected_read(n, s):
    """Expected sentences read from an n-sentence text, keep-reading chance s."""
    return s * (1 - s**n) / (1 - s)

s = 0.8
for n in [1, 2, 3, 5, 10, 20]:
    print(f"N={n:>2}  read={expected_read(n, s):.2f}  finish={s**n:.1%}")
```

```
N= 1  read=0.80  finish=80.0%
N= 2  read=1.44  finish=64.0%
N= 3  read=1.95  finish=51.2%
N= 5  read=2.69  finish=32.8%
N=10  read=3.57  finish=10.7%
N=20  read=3.95  finish=1.2%
```

### Splitting the wall

Now take 20 sentences of lore and stop delivering them as one wall. Split them into `k` pieces of `L / k` sentences each, where `L = 20` is the total. Put the pieces in the world: an item description, a note on a desk, a line a guard says, an inscription. Each piece is found with chance `f`, the **find chance**. GD201 week 8 shows how to estimate a find chance from where a thing is placed. Here we take it as given.

```
expected sentences read = k × f × E(L / k)
```

Each piece is a short text, so it lives on the steep, efficient part of the curve. The price is that the player may never find it.

| Plan | Pieces k | Sentences per piece | Find chance f | Expected sentences read |
|---|---|---|---|---|
| One forced wall (quest giver) | 1 | 20 | 1.0 | 3.95 |
| Two long notes | 2 | 10 | 0.6 | 4.29 |
| Four notes | 4 | 5 | 0.6 | 6.45 |
| Ten short pieces | 10 | 2 | 0.6 | 8.64 |
| Twenty one-liners | 20 | 1 | 0.6 | 9.60 |

Check the four-note row. Each note has 5 sentences, so `E(5) = 2.69`. Four notes found 60% of the time give `4 × 0.6 × 2.69 = 6.45`.

Splitting more than doubles the lore that reaches players, even though 40% of the pieces go unfound. The limit, when every piece is one sentence, is `f × s × L = 0.6 × 0.8 × 20 = 9.6`.

Splitting is not free, and it does not always win. Drop the find chance to `f = 0.3`, pieces hidden off the main path, and four notes give `4 × 0.3 × 2.69 = 3.23`, *worse* than the wall. The break-even find chance for a plan is

```
f* = E(L) / (k × E(L / k))
```

For four notes, `f* = 3.95 / (4 × 2.69) = 0.37`. For twenty one-liners, `f* = 3.95 / (20 × 0.8) = 0.25`. If you cannot get pieces found at least that often, a single short text you force on everyone does better.

### The best plan mixes tiers

You don't have to choose one channel. Put the need-to-know tier in a short forced text, and scatter the rest. A 2-sentence forced summary (`E(2) = 1.44`, and every player gets its first sentence 80% of the time) plus the other 18 sentences as one-liners found 60% of the time gives

```
1.44 + 18 × 0.6 × 0.8 = 1.44 + 8.64 = 10.08 sentences read
```

That beats every row in the table and guarantees the critical information reaches the most players.

### A visual you can move

Open the interactive. The left view is the wall, one bar per sentence, and each bar's height is the share of players who reach it. Drag `N` up and watch the bars on the right fade toward zero. The right view plots expected sentences read against the number of pieces, with the wall as a flat dashed line. Drag the find chance down and watch the curve sink below the dashed line. The point where they cross is `f*`.

### Cross-game recognition

Rewrite each game's lore delivery as `N`, `k` and `f`, and they turn out to be choices on the same curve.

**Dark Souls (FromSoftware, 2011).** The plot is told mostly through environmental details, the flavor text on items, and conversations with non-player characters, and players piece the story together themselves instead of watching cutscenes. In model terms, `N` per piece is small (a short description on an item you already hold), `k` is very large (every item carries some), and `f` varies from 1 for items on the main path to small values for hidden ones. The design takes the one-liner row to its limit and accepts that few players see everything.

**BioShock (2K, 2007).** The main narrative device is the audio diary, a recording left by a citizen of the city. Picking one up stores it in a menu and offers to play it with one button press. A handful of plot-critical diaries play automatically when picked up. That is the mixed-tier plan exactly. Designers set `f = 1` for the need-to-know pieces and let the others be found. Audio adds something the text model lacks. The player can keep moving while listening, so stopping to read is not the cost. In model terms, an audio channel raises `s`.

**Destiny (2014) and Destiny 2 (2017).** The Grimoire put a large `k` of pieces behind a step outside the game. In model terms, every piece's find chance was multiplied by the small chance that a player would open a website to read it. Destiny 2's shift to in-game storytelling raised `f` by removing that step.

**Environmental storytelling in general.** Smith and Worch's GDC 2010 talk describes spaces built so the player infers what happened from props, lighting and arrangement. These pieces have `N = 0` words. The reading-decay idea still applies with time in place of sentences. A scene that takes 30 seconds to parse loses players the way a long text does, which is why the talk stresses scenes that read at a glance.

### Eyes-open design judgment

The model argues for short pieces. That is not the same as "short is always right."

- **Strength:** it turns "players don't read" from a complaint into a number you can budget, and it tells you where the need-to-know sentence goes (first).
- **Strength:** it gives you a test for splitting. If you cannot get pieces found above `f*`, don't split.
- **Cost:** fragmentation. Twenty one-liners found in random order are harder to assemble into a story than one coherent page. Dark Souls turns that into the fun of the game. A game whose players want to follow a plot may just leave them confused. The model counts sentences read, not understanding, and it assumes sentences are worth the same wherever they are read.
- **Cost:** production. Each piece needs a place in the world, an object or a speaker, and a hook in the quest or level. Twenty pieces cost far more to build than one panel.
- **Decide deliberately:** which players you are writing for. A fan who reads everything has `s` near 1 and loves the codex. A player in a hurry has `s` near 0.5 and reads one sentence. Your need-to-know tier has to survive the second player.

### Check yourself (worked example)

1. With `s = 0.7`, what is the most sentences any text can get read on average? How many sentences does a 5-sentence text get read?
2. A designer splits 12 sentences into 6 pieces of 2 sentences, each found with chance 0.5. With `s = 0.8`, does this beat a single 12-sentence forced text?
3. What find chance would the plan in question 2 need to break even?

<details>
<summary>Answers</summary>

1. The ceiling is `0.7 / 0.3 ≈ 2.33` sentences. `E(5) = 0.7 × (1 − 0.7^5) / 0.3 = 0.7 × 0.832 / 0.3 ≈ 1.94`.
2. The wall gives `E(12) = 4 × (1 − 0.8^12) = 4 × 0.931 ≈ 3.73`. The split gives `6 × 0.5 × 1.44 = 4.32`. The split wins, narrowly.
3. `f* = 3.73 / (6 × 1.44) ≈ 0.43`.

</details>

## 3. Measuring s in your own game

The model has one parameter, so one measurement fits it. If a playtest shows that a fraction `c` of players finish an `N`-sentence text, then `c = s^N` and

```
s = c^(1/N)
```

Suppose 30% of testers reach the end of a 6-sentence quest description, judged by the moment they press Accept after the text finishes scrolling, or by asking them afterwards what the last sentence said. Then `s = 0.3^(1/6) ≈ 0.82`.

Some ways to get `c`:

- **Paged text.** If your dialogue box shows one sentence or line per page and the player presses a button to advance, log each page view. The share who reach the last page is `c`, and the drop from page to page shows you whether `s` really is constant.
- **Recall questions.** After a playtest, ask what the NPC said. Only ask about facts that appear in one sentence, so an answer tells you that sentence was read.
- **Skip button telemetry.** If you have a "skip" control, log the line on which it was pressed.

Three warnings.

1. `s` is not a property of the player alone. It depends on the moment. A player who has just died to a boss and wants to retry has a tiny `s`. The same player in a quiet town at night may read everything. Measure in context.
2. `s` often rises for a text that has earned it. A first sentence with a mystery in it keeps readers. A first sentence that lists four proper nouns loses them. The constant-`s` model is the baseline you are trying to beat with good writing.
3. The model says nothing about players who never open the text at all. That is the find chance, and it is a level design problem as much as a writing problem.

## 4. Delivery channels

Each channel has a typical piece length, a find chance and a cost to the player. Choosing channels is choosing positions on the curve.

| Channel | Typical length | Interrupts play? | Who chooses to see it | Good for |
|---|---|---|---|---|
| Quest-giver dialogue | 1-6 lines | Yes | Forced | Need to know |
| Barks (lines NPCs say as you pass) | 1 line | No | Forced, often missed | Nice to know, mood |
| Item descriptions | 1-3 sentences | Only if opened | Player | For the fans |
| Found notes, books | 1 paragraph to pages | Yes | Player | Nice to know, for the fans |
| Audio logs | 20-90 seconds | No | Player | Nice to know |
| Environment (props, bodies, damage) | 0 words | No | Player's eye | Nice to know |
| Codex or journal entry | Paragraphs | Yes, in a menu | Player | For the fans, reference |
| Names on the map, item and enemy names | 1-4 words | No | Forced | Every tier, one noun at a time |

Two channels deserve more attention than they get.

**Names are lore.** A zone called "the Drowned Market" tells the player something before they arrive. A sword called "Warden's Last Oath" hints at a story in four words that nobody will skip. Names are the one lore channel with `s` close to 1, because reading them costs nothing. Spend them carefully.

**Barks cost almost nothing to hear.** A guard who mutters that the raiders burned the bridge delivers the nice-to-know tier without stopping play. Barks repeat, and repetition has its own math, which week 12 works out.

## 5. Writing the pieces

The model tells you how long a piece may be. It doesn't tell you how to write it. Some rules that follow from it:

- **Lead with the payoff.** The first sentence of a piece must be worth reading on its own, since it's the only one most players see. Put the need-to-know fact there, or a question the player wants answered.
- **One idea per piece.** A note that explains the bridge, the guild and the militia is three pieces. Split it.
- **Budget proper nouns.** Every new name is something the player must hold in memory until it pays off. A reasonable house rule is at most one new proper noun per piece, and never a name in the need-to-know tier that the player hasn't seen before. Treat it as a starting rule for your team, not as research.
- **Tie pieces to objects the player cares about.** An item description is read when the player is deciding whether to equip the item. That moment has a higher `s` than any other.
- **Let the world confirm the text.** If a note says the raiders burned the bridge, put scorch marks on the pilings. A player who sees the marks without reading the note still gets part of the story. A player who reads the note and then sees the marks gets a small moment of recognition. That is the environmental storytelling link from GD201 week 8.
- **Cut, then cut again.** Take a finished piece and delete its second sentence. If nothing is lost, leave it deleted.

A before-and-after, all invented:

> **Before (5 sentences, one panel).** Long ago, in the Age of Tides, the river-folk of Hallow Reach built the great bridge under the direction of the Mason's Circle. For three centuries it carried trade between the Reach and the eastern baronies. Last spring, raiders from the Ashen Company set it alight to stop the Reach militia from pursuing them. The militia captain, Orsa Venn, has not forgiven herself. You will need to cross at the ford, a mile to the south.

With `s = 0.8`, the need-to-know sentence (the ford) is fifth, so 33% of players read it. The panel introduces five proper nouns before it.

> **After (four pieces).** Quest giver, forced: "The bridge is gone. Cross at the ford, a mile south." Guard bark near the ruins: "Ashen Company burned it. Captain Venn saw the whole thing." Scorch marks on the pilings, no text. Item description on a stone the player can pick up: "A mason's block, stamped with a compass inside a circle. The guild that cut it was gone before your grandmother was born."

The ford now sits in the first forced sentence, read by 80% of players. The rest reaches whoever finds it.

## In-class activity (25 minutes)

Pairs. Use the interactive and the invented lore text your instructor hands out (about 300 words, 18 sentences, one quest's worth of backstory for a flooded mine).

1. Mark each sentence need to know, nice to know or for the fans. Every pair must agree with at least one other pair on the need-to-know set, so argue it out.
2. Measure: assume `s = 0.8` and compute `E(18)` for the text as written, and the share of players who reach the first need-to-know sentence in its current position.
3. Redesign: split the text into a forced summary of at most 2 sentences and any number of placed pieces. For each piece, name its channel (from section 4) and estimate a find chance of 0.3, 0.6 or 0.9 based on where it sits (on the main path, one room off it, hidden).
4. Compute the expected sentences read for your plan and compare it with step 2. Find `f*` for your pieces.

Expected output: the tiered text, your plan as a table (piece, channel, sentences, find chance), the two totals, and one sentence on what your plan loses compared with the wall.

## Common misconceptions

- **"Players don't read, so write nothing."** Players read short things placed at the right moment. The model shows the first sentence of a text reaches most players. The problem is the twentieth sentence.
- **"Splitting lore into collectibles always helps."** Only above the break-even find chance. Hidden pieces with `f = 0.3` can deliver less than one forced paragraph.
- **"If the text is in the game, the player has the lore."** Destiny's Grimoire was technically in the product. Delivery is what reaches the player, not what exists in the files.
- **"A codex is where lore goes."** A codex is a reference for players who already care, with `s` near 1. It is the worst place for the need-to-know tier.

## Check yourself

1. A playtest shows 40% of players finish a 4-sentence text. Estimate `s`. What share would you expect to finish an 8-sentence text?
2. Your quest text has the need-to-know fact in sentence 4. With `s = 0.85`, what share of players read it? What share would read it if you moved it to sentence 1?
3. You have 15 sentences of lore and `s = 0.8`. Plan A is one forced panel. Plan B is a 3-sentence forced summary plus 12 one-sentence pieces, each found with chance 0.5. Which delivers more sentences read?
4. A colleague says an audio log is "the same as a text note, just voiced." Using the model, give one reason the audio log can deliver more lore and one reason it can deliver less.
5. Rewrite the Destiny Grimoire problem in the model's terms. Which parameter did moving lore into the game change?

<details>
<summary>Answers</summary>

1. `s = 0.4^(1/4) ≈ 0.795`. An 8-sentence text finishes at `s^8 = 0.4^2 = 0.16`, so 16%.
2. `0.85^4 ≈ 52%`. In sentence 1, `0.85`, so 85%. Moving one sentence gains a third of your players.
3. Plan A gives `E(15) = 4 × (1 − 0.8^15) = 4 × 0.965 ≈ 3.86`. Plan B gives `E(3) + 12 × 0.5 × 0.8 = 1.95 + 4.8 = 6.75`. Plan B wins.
4. More: the player keeps playing while listening, so the cost of continuing is lower and `s` is higher. Less: an audio log that plays over combat or another voice may be missed entirely, and a player cannot skim audio to find the one sentence they want. Either answer that uses `s` or `f` is right.
5. Every piece's find chance was multiplied by the chance a player left the game to read it, which was small. Moving lore into the game raised `f`.

</details>

## Lab hook

[Lab 10, lore budget](../labs/lab10.md). You implement the model in a small Python planner, fit `s` from a playtest table, and then rewrite a supplied 400-word lore dump into a delivery plan that beats the wall by at least 50% while keeping the need-to-know tier in forced text. Deliverable: the passing planner, your delivery plan and a 250-word justification.

## Sources

- Wikipedia, "Destiny (video game)" (retrieved September 2026). The majority of the lore was on Grimoire cards readable only through Bungie's website and the Destiny app; the game was criticized at launch for its lack of story content.
- Wikipedia, "Destiny 2" (retrieved September 2026). Grimoire cards did not return; Bungie shifted focus to in-game storytelling.
- Wikipedia, "Dark Souls" (retrieved September 2026). The plot of Dark Souls (2011) is told primarily through environmental details, item flavor text and dialogue with non-player characters.
- BioShock Wiki, "Audio Diary" (retrieved September 2026). Audio diaries are the main narrative device in BioShock (2007); picked-up diaries are stored and played on a button press; a handful of plot-critical diaries play automatically.
- Smith, H. and Worch, M. (2010). "What Happened Here? Environmental Storytelling." Game Developers Conference 2010, GDC Vault.
- The reading-decay model and all values of `s` and `f` in this lecture are teaching assumptions, not measurements from any game.

## Interactive spec: examples/w10-lore-chunking.html

**Purpose.** Let students see that sentences at the end of a long text are read by almost nobody, and that splitting lore into found pieces beats a wall only when the find chance is above a threshold.

**The one insight the visual must make obvious.** Doubling a text's length barely moves "sentences read", while splitting the same text into pieces moves it a lot, until the find chance drops below `f*` and the split line sinks under the wall line.

**Layout.** Two linked views, side by side at 1280 px, stacked at 390 px (wall on top). A results strip underneath.

- Left, "One wall": a vertical bar chart with one bar per sentence, `k = 1..N`. Bar height is `s^k` on a 0 to 100% axis. Bars for sentences tagged need-to-know (see controls) are drawn in the accent color with a solid outline; other bars use the neutral token. Above the chart print "Expected read: E(N) of N sentences (x%)" and "Finish rate: s^N". A thin horizontal line marks 50%, labeled "half your players".
- Right, "Split into pieces": a line chart. x axis is the number of pieces `k` over the divisors of `L` (for `L = 20`: 1, 2, 4, 5, 10, 20). y axis is expected sentences read, 0 to `L`. Solid line with dots is `k × f × E(L/k)`. Dashed horizontal line is the wall value `E(L)`. A dotted horizontal line is the limit `f × s × L`. Dots above the dashed line are filled with the positive token; dots below are filled with the negative token and get a hollow ring as a second cue. Selected `k` is highlighted and its value printed.
- Results strip: "Wall: E(L)", "Your plan: k × f × E(L/k)", "Gain: ×ratio", "Break-even f* for this k", and, if the mixed-tier toggle is on, "Mixed plan".

**Controls** (keyboard accessible, values printed next to each):

- Keep-reading chance `s`: slider 0.50 to 0.95, step 0.01, default 0.80.
- Total sentences `L` (also the wall length `N`): segmented buttons 6, 12, 20, 30, default 20. The x axis of the right chart uses the divisors of `L`.
- Find chance `f`: slider 0.10 to 1.00, step 0.05, default 0.60.
- Pieces `k`: stepper over the divisors of `L`, default 4.
- Need-to-know position: slider 1 to `L`, default 5. Highlights that bar on the left and prints "reaches x% of players".
- Mixed-tier toggle, default off. When on, a forced summary of `m` sentences (stepper 1 to 3, default 2) is read with `E(m)` and the remaining `L − m` sentences are one-liners with find chance `f`. Adds a second dot series on the right chart at `k = L − m` labeled "mixed".
- Reset button.

**Formulas.**

- `E(n) = s × (1 − s^n) / (1 − s)`.
- Split value `V(k) = k × f × E(L / k)` for `k ≥ 2`. At `k = 1` the plan is the wall itself, forced on every player as in the lecture's first table row, so `V(1) = E(L)` whatever the `f` slider says (show the label "the wall, forced").
- Break-even `f* = E(L) / (k × E(L / k))`, clamped to at most 1 and printed as "never" if above 1.
- Mixed value `E(m) + (L − m) × f × s`.
- Estimating `s` helper (small panel under the controls): inputs finish rate `c` (0.01 to 0.99) and length `N` (1 to 30); output `s = c^(1/N)` to three decimals, with a button "use this s".

**Test values** (must match to two decimals).

| s | L | f | k | E(L) | V(k) | f* |
|---|---|---|---|---|---|---|
| 0.80 | 20 | 0.60 | 1 | 3.95 | 3.95 | 1.00 |
| 0.80 | 20 | 0.60 | 4 | 3.95 | 6.45 | 0.37 |
| 0.80 | 20 | 0.60 | 10 | 3.95 | 8.64 | 0.27 |
| 0.80 | 20 | 0.60 | 20 | 3.95 | 9.60 | 0.25 |
| 0.80 | 20 | 0.30 | 4 | 3.95 | 3.23 | 0.37 |
| 0.70 | 20 | 0.60 | 20 | 2.33 | 8.40 | 0.17 |

Mixed plan at `s = 0.8`, `L = 20`, `f = 0.6`, `m = 2`: 10.08. Estimating helper: `c = 0.30`, `N = 6` gives `s = 0.818`.

**First screen.** Defaults, with `k = 4` highlighted, so the right chart shows the split line well above the dashed wall and the left chart shows the fifth bar (need-to-know) at 33%. Caption above the views: "Twenty sentences written. How many get read?"

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css` inline, light and dark themes, `prefers-reduced-motion` respected (no animated bar growth when set). Every chart has a text summary in an `aria-live` region that updates with the numbers. No game art, logos or screenshots; the only labels are generic ("sentence 1", "piece").
