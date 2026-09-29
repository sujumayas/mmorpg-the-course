# MMO406 · Week 12 — Transmedia

**Why this matters:** Sooner or later your world will appear outside the game: a novel, an animated short, a comic, a web story, maybe a show. Each one can bring new players in or leave current players confused. Which of those happens depends on one decision you make for every piece: does the game need it, or does it only add to it? This week gives you the arithmetic behind that decision, and a way to brief the people who write in your world without breaking it.

**You will be able to:**
- Compute the share of players who have the full context for a story that depends on outside media, and the share who get something extra from optional media, from each medium's reach.
- Derive the best and worst cases for both shares when reach is correlated, and explain why "required" media shrink your audience however the fans overlap.
- Critique the transmedia choices of Destiny, Guild Wars 2, World of Warcraft and EVE Online in terms of required and optional reach.
- Design a transmedia plan and a licensee brief for your world bible, with a retell line for every beat the game needs.

**Before class:** Henry Jenkins, "Transmedia Storytelling 101" (henryjenkins.org, 22 March 2007, 15 minutes). Jenkins, *Convergence Culture* (2006), chapter 3, on *The Matrix* (skim, about 30 pages). Wikipedia, "Destiny (video game)", the paragraph on the Grimoire cards in the Plot section (5 minutes).

**Prerequisites from earlier courses:** [MA102 week 2, independent events](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w02-independent-events-and-the-gamblers-fallacy.md) (multiplying chances of events that don't affect each other) and [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) (the chance of at least one). [GD202 week 10, lore delivery without walls of text](../../GD202-narrative-and-quest-design/lectures/w10-lore-delivery-without-walls-of-text.md) (in-game delivery channels). [MMO406 week 7](w07-lore-delivery-in-mmos.md) (who in the population still knows a beat), [week 8](w08-player-agency-vs-canon.md) (canon fit, the same product rule applied to player choices) and [week 11](w11-retcons-and-continuity.md) (canon tiers and frozen media).

**Interactive:** [w12-required-vs-optional.html](../examples/w12-required-vs-optional.html). Keep it open during section 2.

---

## 1. What transmedia means for a live world

Henry Jenkins introduced the term **transmedia storytelling** for a fiction whose parts are spread across several media on purpose, so that together they make one coordinated experience. His ideal is that each medium contributes something only it can do: the film gives spectacle, the game lets you act, the comic gives a side character a story, and so on. He also points out that each medium can be a different entry point for a different audience.

A persistent world meets transmedia in three ways.

1. **Outward.** The studio commissions stories set in the game world: novels, comics, animated shorts, web fiction. The game is the center, and the outside pieces orbit it.
2. **Inward.** The game is one part of a larger franchise that started elsewhere, as Star Wars: The Old Republic is part of Star Wars. The game has to respect a canon it doesn't own (week 11's tiers).
3. **From the players.** Stories about what players did, retold in other media. EVE Online's comic *EVE: True Stories* (Dark Horse, 2014, free online) was based on actual player-driven events. Week 13 covers community lore itself.

All three raise the same planning question. For each beat in your game's story, where does the player get it? If the answer is "in the game", the rest of this lecture is about enrichment. If the answer is "in the novel", you have made the novel **required**, and the arithmetic turns against you.

Two terms, defined once:

- The **reach** `s` of a medium is the share of your active players who have consumed it: read the novel, watched the short, finished the comic.
- A medium is **required** for a beat if a player cannot follow the game's story without it. It is **optional** (or enriching) if the game's story stands on its own and the medium adds to it.

## 2. Worked example: what if the story needs the novel?

### The hook

Destiny launched in 2014 with a large, carefully written setting, and most of it was not in the game. The backstory of characters, weapons, alien races and planets sat on Grimoire cards. Players collected the cards by playing, but could only read them on Bungie's website or in the companion app. The game itself was widely criticized for its thin in-game storytelling. For the sequel in 2017, Bungie dropped the Grimoire and moved lore into the game: objects on the maps that the player's companion can scan, and lore tabs on weapons and armor.

Destiny's writing was not the problem. Players who read the cards found a rich setting. The problem was arithmetic. Most players never opened the website, so for most players the story the game assumed they knew did not exist.

### The model

Take `k` outside media with reaches `s_1, s_2, ..., s_k`. Assume for now that reading one does not make a player more or less likely to consume another (independence, MA102 week 2).

```
Full context (every medium required):   C = s_1 × s_2 × ... × s_k
Something extra (every medium optional): X = 1 − (1 − s_1) × (1 − s_2) × ... × (1 − s_k)
Pieces per player:                        n = s_1 + s_2 + ... + s_k
```

- `C` is the **context share**: the share of players who consumed **all** the required media. Only they can follow a story that assumes all of them. It is an AND, so the chances multiply.
- `X` is the **extra share**: the share of players who consumed **at least one** optional medium. It is an OR, so you use the complement rule from MA102 week 3. The chance of missing all of them is the product of the chances of missing each.
- `n` is the average number of outside pieces a player consumed. It is the same whether you call the media required or optional.

You have met the AND half before. Week 8's canon fit multiplied the take rates of players' choices in the same way. What is new here is that one label, required or optional, decides whether a medium enters the AND or the OR.

The last line of the model is the lecture. **The same media, reaching the same players, give opposite curves depending on one label.** Adding a required medium multiplies `C` by a number below 1, so `C` can only fall. Adding an optional medium multiplies the "missed everything" share by a number below 1, so `X` can only rise.

### Numbers you can check

Take an invented plan for *Thornmere*'s next expansion, with four outside pieces and their reach among active players: an animated short on the game's video channel (60%), a web comic (30%), a printed prequel novel (15%) and a free short story on the game's website (35%). Add them one at a time.

| Media so far | `n` | `C` if all required | `X` if all optional |
|---|---|---|---|
| Short (0.60) | 0.60 | 60.0% | 60.0% |
| + web comic (0.30) | 0.90 | 18.0% | 72.0% |
| + novel (0.15) | 1.05 | 2.7% | 76.2% |
| + web story (0.35) | 1.40 | 0.95% | 84.5% |

Check the third row by hand. Required: `0.60 × 0.30 × 0.15 = 0.027`. Optional: the chance of missing all three is `0.40 × 0.70 × 0.85 = 0.238`, so `X = 1 − 0.238 = 0.762`.

With all four pieces required, fewer than one player in a hundred can follow the story. With the same four pieces optional, more than four in five get something extra. Nothing about the media changed.

You can reproduce the table in a few lines:

```python
from math import prod

media = [("short", 0.60), ("web comic", 0.30), ("novel", 0.15), ("web story", 0.35)]

for k in range(1, len(media) + 1):
    s = [reach for _, reach in media[:k]]
    C = prod(s)
    X = 1 - prod(1 - x for x in s)
    print(f"{media[k-1][0]:<10} n={sum(s):.2f}  C={C:.2%}  X={X:.1%}")
```

It prints:

```
short      n=0.60  C=60.00%  X=60.0%
web comic  n=0.90  C=18.00%  X=72.0%
novel      n=1.05  C=2.70%  X=76.2%
web story  n=1.40  C=0.95%  X=84.5%
```

### When fans overlap

Independence is a convenient lie. The players who read the novel are probably the same players who watch the shorts. How much does that rescue a required plan?

Without assuming anything about overlap, the shares have hard limits (they are called the Fréchet bounds):

```
max(0, s_1 + ... + s_k − (k − 1))  ≤  C  ≤  min(s_1, ..., s_k)
max(s_1, ..., s_k)                  ≤  X  ≤  min(1, s_1 + ... + s_k)
```

For the first three media (0.60, 0.30, 0.15):

| Share | Independent | Best case | Worst case |
|---|---|---|---|
| `C`, all required | 2.7% | 15% (every novel reader also saw the rest) | 0% (no one saw all three) |
| `X`, all optional | 76.2% | 100% (no overlap at all) | 60% (everyone else is a subset of the short's viewers) |

Even in the best case, a required plan can never reach more players than its **least-read** medium. The novel's 15% is a ceiling on `C` however loyal your fans are. For optional media, the worst case is the reach of the **most-watched** piece. Overlap moves you between the bounds. It cannot move `C` above the smallest reach.

### A visual you can move

Open the interactive. The left panel is what a franchise meeting sees: a bar per medium with its reach, and a big total "pieces per player" that grows as you add media. The right panel shows the players. A grid of 100 player tiles, each filled by the media that player consumed. Two counters above it read "can follow the story" (`C`) and "got something extra" (`X`). Start with every medium set to optional. Add media and watch `X` climb. Now flip the novel to required. The left panel does not change at all. On the right, 85 tiles go grey at once. Then try the overlap slider: from "independent" to "fans overlap fully", `C` rises to 15% and stops.

### Cross-game recognition

**Destiny (2014) and Destiny 2 (2017).** The Grimoire was not marked "required", but the game told its story as if players knew it. In the model, much of the setting sat in one medium with a low reach, and the game's plot was an AND over it. Destiny 2's fix was to move the lore into the game (scannable objects, lore tabs), which raises that medium's reach to "everyone who plays", `s ≈ 1`.

**Guild Wars 2 (2010 to 2012).** ArenaNet published three novels to bridge the time between Guild Wars and Guild Wars 2, starting with *Ghosts of Ascalon* (July 2010) and *Edge of Destiny* (December 2010). *Edge of Destiny* tells how the adventuring guild Destiny's Edge formed, lost a member to the dragon Kralkatorrik, and broke apart. The game's core story then asks the player to reunite that disbanded guild. That is a required-shaped dependency: a novel reader knows why the heroes don't speak to each other, and a player who skipped it meets the aftermath of a break-up they never saw. For the reunion to land for everyone, the game has to carry the essential facts itself, which is the retell line in section 3.

**World of Warcraft (2016 and 2018).** Before Legion (2016), Blizzard released *Harbingers*, a series of animated shorts starting at San Diego Comic-Con in July 2016, each following one character into the coming invasion. Before Battle for Azeroth (2018), it published a lead-in novel, *Before the Storm*, and two novellas, *Elegy* and *A Good War*, which were also published free on the World of Warcraft website. Free web publication raises `s`, and placing the pieces before the expansion makes them lead-ins, week 10's hooks with a short `d`. As long as the expansion retells what it needs, they are optional, and they push `X` up.

**EVE Online (2014).** *EVE: True Stories* ran the other way: a comic built from things players had done. No part of the game depends on it, so it is pure enrichment, and it gives players who were in those wars something the game cannot: their own history, retold.

Four studios, one rule. Destiny's story sat behind a low-reach medium and paid for it. Guild Wars 2 put a key backstory in a novel and had to carry it in the game. World of Warcraft placed free, optional lead-ins before its expansions. EVE's comic depends on the game, and nothing in the game depends on the comic.

### Eyes-open design judgment

- **Make outside media optional for the main story, always.** The ceiling on `C` is the smallest reach, and a printed novel's reach among players is small. If the game needs a fact, the game states it.
- **Required is sometimes right for small audiences.** A side mystery that only dedicated fans are meant to solve can live across media. Keep it off the main story's path, and expect `C` to be small by design.
- **Raise reach before you raise count.** One free, in-client story with 60% reach does more for `X` than three paid books at 10% each: `1 − 0.4 = 0.6` against `1 − 0.9³ = 0.27`.
- **Watch the direction of dependency.** A novel that depends on the game is safe. A game that depends on a novel inherits the novel's reach. Draw the arrows the way week 11 did.
- **Outside media are frozen.** Anything in print is frozen the moment it ships. Give tie-in writers leaves, not roots.

### Check yourself (worked example)

1. A story requires a comic (reach 40%) and a short (reach 70%). Under independence, what share can follow it? What are the best and worst cases?
2. A producer offers either one extra optional medium with reach 50%, or two with reach 25% each. Starting from the four-media plan's `X = 84.5%`, which raises `X` more?

<details>
<summary>Answers</summary>

1. Independent: `0.4 × 0.7 = 28%`. Best case `min(0.4, 0.7) = 40%`. Worst case `max(0, 0.4 + 0.7 − 1) = 10%`.
2. The missed-everything share is `0.155`. One at 50%: `0.155 × 0.5 = 0.0775`, so `X = 92.3%`. Two at 25%: `0.155 × 0.75 × 0.75 = 0.0872`, so `X = 91.3%`. The single wider piece wins by one point.

</details>

## 3. The retell line

For every beat the game's story needs, write a **retell line**: the in-game sentence, scene or item that delivers the essential fact to a player who never saw the outside medium. A retell line turns a required medium into an optional one, because the game now carries the beat itself and the outside piece only deepens it.

A good retell line has three properties.

1. **It states the one fact the game needs, not the whole story.** For the Guild Wars 2 case, an invented line such as "Logan left us to save the queen, and Snaff died because of it" would be enough to make a reunion scene work. The novel supplies the rest.
2. **It lives where everyone passes.** Week 7's catch-up reach `r` applies. A retell line in the main story has an `r` near 1. One in an optional side quest does not.
3. **It rewards the reader without punishing the non-reader.** A reader should recognize the scene and feel that they knew more. A non-reader should not feel they missed something they were supposed to know.

GD202 week 10 covers how to write the line itself so players actually read it. The planning step is making sure it exists at all. Audit every outside piece with one question: which game beat would a non-reader miss, and where is its retell line?

## 4. Briefing people who write in your world

Most outside media are written by people outside your writing team: novelists, comic writers, animation studios. They need a **licensee brief**, a short document that lets them write freely without breaking canon. The Holocron shows the stakes. Stories that made radical changes to Star Wars continuity, such as introducing a secret apprentice for Darth Vader in *The Force Unleashed*, needed George Lucas's own approval. A brief is how you decide in advance what needs that level of approval.

A licensee brief holds:

| Section | Content | Why |
|---|---|---|
| Tier | The tier the work will have (week 11), usually tie-in | The writer knows what outranks them |
| Allowed facts | Fact ids they may use, and ids they may add below | Leaves, not roots |
| Forbidden facts | Roots and open hooks they must not resolve or change | Keeps week 10's hooks available |
| Required beats | Anything the game will later reference, with the game's retell line | The game stays self-contained |
| Continuity contact | One named person who answers questions within two working days | Keeps `ε` low (week 11 section 3) |
| Timing | Release date relative to the game patch or expansion, and embargoes | Lead-ins must not spoil, follow-ups must not contradict |
| After release | Who adds the work's new facts to the canon graph, with dependencies | The graph stays complete |

Two rules make briefs work in practice. First, every new fact a tie-in adds is logged in the canon graph as a descendant of the facts it uses, and frozen. Second, the game team treats tie-in facts as read-only. If the game later needs to use one, it restates it in-game (a retell line) rather than depending on the book.

## 5. Timing and direction

Outside media can sit before, alongside or after the content they relate to.

- **Before (lead-ins).** Harbingers, *Before the Storm*. They build anticipation and act as hooks with a short lead time. Risk: a lead-in that reveals too much spoils the expansion, and one written before the expansion's story is final may be contradicted by it. Lead-ins should touch the expansion's setup, not its ending.
- **Alongside.** A web comic running in parallel with a patch cycle. Its reach grows with the patch's audience. Risk: two teams writing the same period at once, which is where same-tier contradictions come from.
- **After (follow-ups).** A novel about the aftermath of a raid, or a comic of player history like *EVE: True Stories*. Safest for continuity, since the game content it depends on is finished. Lowest marketing value.

Direction matters as much as timing. Draw the arrows. If the game depends on the outside piece, `C` applies and reach is a ceiling. If the outside piece depends on the game, `X` applies and every piece helps.

## In-class activity (25 minutes)

In groups of three, you run transmedia for *Thornmere*'s second expansion, "The Heir's Road". The expansion's climax is Ysolde's coronation. The marketing team has commissioned four pieces: a prequel novel about Queen Adelmar's last year (reach estimate 12%), an animated short of Adelmar's funeral (55%), a web comic about the Tidewarden schism (25%) and an in-client short story about Ysolde's childhood (70%).

1. (5 min) The current script assumes players know how Adelmar died (novel), that the Tidewardens split (comic) and what Ysolde promised her mother (short story). Compute `C` under independence and its best case.
2. (10 min) Write a retell line for each of the three beats, and say where in the game it goes.
3. (5 min) With all three now optional, compute `X` for all four pieces.
4. (5 min) Draft the "forbidden facts" row of the novelist's brief.

Expected output: `C = 0.12 × 0.25 × 0.70 = 2.1%` (best case 12%); three retell lines with locations; `X = 1 − 0.88 × 0.45 × 0.75 × 0.30 = 1 − 0.0891 = 91.1%`; at least two forbidden facts (for example, the cause of the Drowning and the identity of the spy from week 11).

## Common misconceptions

- **"More media means more players understand the story."** Only if the media are optional. Every required medium multiplies the share who can follow the story by its reach.
- **"Our fans overlap, so requiring the novel is fine."** Overlap lifts `C` toward the smallest reach and no further. If the novel reaches 15% of players, at most 15% have the full context.
- **"Transmedia means putting important story outside the game."** Jenkins's ideal is that each medium contributes something distinctive. For a game with a live population, the important part is the game's to carry. Outside media add depth, other viewpoints and history.
- **"A tie-in is marketing, so continuity doesn't apply."** A tie-in is canon at its tier, and it is frozen once printed. It needs a brief like any other writer's work.

## Check yourself

1. A raid's final cutscene assumes players read two web stories, with reaches 45% and 35%. What share can follow it under independence? What is the most it could be?
2. You can afford one more optional medium. Option A: a novel reaching 10% of players. Option B: an in-client story reaching 65%. Your existing optional media give `X = 70%`. Compute `X` for each option.
3. A comic depends on a quest chain, and a later dungeon depends on the comic. Draw the arrows. Which of `C` and `X` applies to the dungeon's story, and what should the dungeon team do?
4. Destiny 2 moved lore from a website into scannable objects in the game. In the model, what changed: the number of media, their reach, or whether they were required?

<details>
<summary>Answers</summary>

1. `0.45 × 0.35 = 15.75%`. At most `min(0.45, 0.35) = 35%`.
2. Missed-everything is 0.30. A: `0.30 × 0.90 = 0.27`, `X = 73%`. B: `0.30 × 0.35 = 0.105`, `X = 89.5%`.
3. Quest chain → comic → dungeon. The dungeon depends on the comic, so its story is an AND over the comic's reach, and `C` applies. The dungeon team should add a retell line for whatever the comic established, which removes the dependency.
4. The reach. The lore became part of the game, so `s` for that material rose toward the share of players who play. The story's dependency on the lore was unchanged, but with `s ≈ 1`, depending on it no longer shrinks `C`.

</details>

## Lab / assignment hook

[Lab 12, the transmedia plan](../labs/lab12.md). A design lab. You use a provided calculator to audit a *Thornmere* transmedia plan, then write a transmedia plan for your own world with a retell line for every required beat and a licensee brief for one tie-in. It feeds the "beyond the game" chapter of the final world bible (60%).

## Sources

- Jenkins, H. (2007). "Transmedia Storytelling 101". *Confessions of an Aca-Fan*, 22 March 2007. Definition of transmedia storytelling; each medium's own contribution; different entry points for different audiences; *The Matrix* spreading key information across films, shorts, comics and games. http://henryjenkins.org/blog/2007/03/transmedia_storytelling_101.html
- Jenkins, H. (2006). *Convergence Culture: Where Old and New Media Collide*. New York University Press.
- Wikipedia, "Destiny (video game)" (accessed September 2026). Most of the lore on Grimoire cards readable only on Bungie's website and the Destiny app.
- Wikipedia, "Destiny 2" (accessed September 2026). Grimoire cards did not return; Bungie shifted to in-game storytelling, which the original was criticized for lacking; scannable artifacts and lore tabs on gear.
- Guild Wars 2 Wiki, "Ghosts of Ascalon" and "Edge of Destiny" (current). The three bridge novels; release dates (27 July 2010, 28 December 2010); the formation and break-up of Destiny's Edge. https://wiki.guildwars2.com/wiki/Edge_of_Destiny
- Wikipedia, "Guild Wars 2" (accessed September 2026). The core game follows the re-emergence of Destiny's Edge, a disbanded guild.
- Warcraft Wiki, "Harbingers" (current). Animated shorts as a prelude to Legion; first episode (Gul'dan) released at the "Road to Legion" panel at San Diego Comic-Con. The wiki gives 21 June 2016, but its own source, a Wowhead preview of 11 July 2016, announces the panel as upcoming and San Diego Comic-Con 2016 ran in late July, so this lecture says July 2016. https://warcraft.wiki.gg/wiki/Harbingers
- Warcraft Wiki, "Before the Storm" (current). Christie Golden's lead-in novel to Battle for Azeroth. https://warcraft.wiki.gg/wiki/Before_the_Storm
- Wikipedia, "World of Warcraft: Battle for Azeroth" (accessed September 2026). The tie-in novellas *Elegy* and *A Good War*, published in hardcover and on the World of Warcraft website.
- Wikipedia, "Eve Online", section "Other media" (accessed September 2026). *EVE: True Stories*, Dark Horse Comics, free online in 2014, based on actual player-driven events.
- Wikipedia, "Star Wars Legends" (accessed September 2026). The Holocron's C-canon level; changes such as *The Force Unleashed*'s secret apprentice required George Lucas's approval.

## Interactive spec: examples/w12-required-vs-optional.html

**The one insight the visual must make obvious:** the same media with the same reach give opposite results depending on one label. Marked optional, each medium adds players who got something extra. Marked required, each medium removes players who can follow the story, and no amount of fan overlap lifts that share above the least-read medium.

**Layout.** Two linked panels, side by side on desktop, stacked on mobile (left on top).

- **Left, "The franchise view".** One horizontal bar per medium (up to 5), showing its reach as a percentage, each with a required/optional toggle beside it. Below the bars, a large total "pieces per player `n`" (2 decimals). This panel never shows `C` or `X`, and it does not change when a toggle flips (only the toggle's own state changes).
- **Right, "The player view".** A 10 × 10 grid of 100 player tiles. Each tile is drawn with small stripes for the media that player consumed. Two large counters above: "can follow the story" = `C` over required media (100% if none are required) and "got something extra" = `X` over optional media (0% if none are optional). Tiles that fail the required set are drawn grey; tiles that passed and consumed at least one optional medium get the accent outline.

**Tile assignment (deterministic).** For display, assign media to tiles so counts match the model to within rounding. Independent mode: for medium `i`, rank the tiles `t` (0 to 99) by `frac(t × φ_i + 0.5 × i / 5)`, ties broken by `t`, and give the medium the `round(100 × s_i)` lowest-ranked tiles. `φ_i` is a fixed irrational-like step per medium (use 0.6180339887, 0.4142135624, 0.7320508076, 0.2360679775, 0.1622776602). Ranking rather than thresholding makes each medium reach exactly its rounded share of tiles, so a 15% novel marks 15 tiles and a required novel greys 85. The counters always show the exact formula values, not tile counts; show the tile count in small text beside each counter so students can see the rounding.

**Overlap slider.** Three positions: "Independent" (default), "Fans overlap fully" (nested: the tiles with the lowest index consume every medium up to that medium's reach, so `C` = minimum reach and `X` = maximum reach), "No overlap" (media fill disjoint tile ranges while possible, so `X = min(1, Σ s)` and `C = max(0, Σ s − (k − 1))`). The counters show, respectively, the independent formulas, the upper bound on `C` with the lower bound on `X`, and the lower bound on `C` with the upper bound on `X`.

**Controls.**

1. Up to five media rows, each with: name (fixed labels "Short", "Web comic", "Novel", "Web story", "Extra"), reach slider 0 to 100% step 1, required/optional toggle, and include checkbox. Defaults: Short 60, Web comic 30, Novel 15 (included, all optional); Web story 35 and Extra 50, not included.
2. Overlap slider (above).
3. Presets: "All optional" (default), "Novel required", "Everything required", "Thornmere activity" (Novel 12 required, Short 55 optional, Web comic 25 required, Web story 70 required; recomputes the in-class numbers).

All controls are labelled native inputs, keyboard operable. An `aria-live` region states: "Can follow the story: 2.7%. Got something extra: 76.2%. Pieces per player: 1.05."

**Formulas.**

```
C = product of s_i over included required media        (1 if none)
X = 1 − product of (1 − s_i) over included optional media (0 if none)
n = sum of s_i over included media
Bounds over included required media R:   max(0, Σ_R s − (|R| − 1)) ≤ C ≤ min_R s
Bounds over included optional media O:   max_O s ≤ X ≤ min(1, Σ_O s)
```

**Test values (must match).**

| Setting | `n` | `C` | `X` |
|---|---|---|---|
| Short, comic, novel, all optional | 1.05 | 100% | 76.2% |
| Short, comic, novel, all required | 1.05 | 2.7% | 0% |
| Same, required, fans overlap fully | 1.05 | 15% | 0% |
| Short, comic, novel, all optional, no overlap | 1.05 | 100% | 100% |
| Short, comic, novel, web story, all optional | 1.40 | 100% | 84.5% |
| Short, comic, novel, web story, all required | 1.40 | 0.95% | 0% |
| Thornmere activity preset (independent) | 1.62 | 2.1% | 55.0% |

**First screen.** "All optional" preset with the first three media, then a one-line caption: "Same three stories. Flip one switch." The first toggle a student flips (novel to required) greys 85 tiles on the right while the left panel stays still.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css` inline, light and dark themes, `prefers-reduced-motion` respected. Stripes are distinguishable without colour (different stripe angles per medium). No game art or logos.
