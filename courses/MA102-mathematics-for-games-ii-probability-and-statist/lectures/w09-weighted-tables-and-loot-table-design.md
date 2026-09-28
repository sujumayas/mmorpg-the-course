# MA102 · Week 09 — Weighted Tables and Loot Table Design

**Why this matters:** Almost every loot drop, random encounter and gacha pull in a shipped game is a weighted table. Weights look like local numbers, but every probability in the table depends on all of them, so a one-line edit can quietly nerf items you never touched. Knowing the math lets you change exactly what you intend and nothing else.

**You will be able to:**
- Convert a weighted table into probabilities, and compute the weight needed to give an entry a target probability.
- Compute drop chances through nested tables and repeated rolls.
- Predict how adding, removing or re-weighting one entry changes every other entry.
- Design a loot table from player-facing targets (kills to drop, value per kill) and critique a table someone else wrote.

**Before class:** Schreiber, *Game Balance Concepts*, Level 4 ("Probability and Randomness") for review, and Level 5 ("Probability and Randomness Gone Horribly Wrong"), on how players perceive odds. Schreiber & Romero, *Game Balance* (2021), the probability chapter, sections on loot tables. Minecraft Wiki, "Loot table" (read the sections on pools, rolls and weight).

**Prerequisites from earlier courses:** The complement rule, [MA102 week 3](w03-complement-rule-chance-of-at-least-one-drop.md). Expected value, [MA102 week 4](w04-expected-value-comparing-weapons.md). The geometric distribution and dry-streak percentiles, [MA102 week 7](w07-geometric-distribution-kills-until-the-drop.md). Ratios and rational expressions, [MA101 week 6](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w06-rational-functions-and-asymptotes.md). Data-driven stat tables in JSON and CSV, CS102 week 13 ([CS102 syllabus](../../CS102-programming-for-games-ii-structures-and-patterns/syllabus.md)).

**Interactive:** [examples/w09-loot-weights.html](../examples/w09-loot-weights.html) (spec at the end of this lecture). Keep it open during sections 2 and 3.

---

## 1. Weights instead of percentages

A **weighted table** is a list of outcomes, each with a non-negative number called its **weight**. To pick one outcome, the game chooses at random with each entry's chance proportional to its weight.

```
P(entry i) = w_i / W        where W = w_1 + w_2 + ... + w_n
```

- `w_i` is the weight of entry `i`.
- `W` is the **total weight** of the table.
- `P(entry i)` is the chance that one pick lands on entry `i`.

Here is a small boss table:

| Entry | Weight | Probability |
|---|---|---|
| Nothing | 600 | 60.0% |
| Gold pouch | 250 | 25.0% |
| Healing potion | 100 | 10.0% |
| Rare sword | 40 | 4.0% |
| Legendary ring | 10 | 1.0% |
| **Total** | **1,000** | **100%** |

Notice two things. First, "Nothing" is an ordinary entry with a weight. Most real loot tables have one, because it is the simplest way to control how often anything drops at all. Second, the weights happen to sum to 1,000, which makes the percentages easy to read. That is a convenience, not a rule. The same table with every weight halved gives the same probabilities.

### Why designers use weights

If probabilities are what matter, why not type percentages directly? Three practical reasons.

1. **Weights never have to sum to anything.** With percentages, adding a new entry means editing others so the column still sums to 100%. With weights, you can add a row and the table still works. That convenience is also the main danger, as section 2 shows.
2. **Weights are easy to think about relatively.** "The sword is four times as common as the ring" is one ratio, 40 to 10, and it stays true whatever else is in the table.
3. **Integer weights make exact code.** A computer picks a whole number from 0 to `W − 1` and walks the list. No rounding errors, and a designer can verify a drop by hand.

### How the game picks an entry

The standard algorithm is short. Here it is in pseudocode:

```
roll = random integer in [0, W − 1]
for each entry in table:
    if roll < entry.weight:
        return entry
    roll = roll − entry.weight
```

With the boss table, a roll of 0 to 599 returns Nothing, 600 to 849 returns Gold, 850 to 949 Potion, 950 to 989 Sword, and 990 to 999 Ring. Each entry owns a slice of the number line exactly as wide as its weight. That is the whole reason the probability is `w_i / W`.

For very large tables picked millions of times a second, engines sometimes use faster methods such as binary search over running totals, or the **alias method**, which picks in constant time after some setup. The probabilities are identical. Only the speed changes. You will meet these again in data structures courses; for design, the slice picture is enough.

## 2. Worked example: Diablo II's NoDrop, one weight that moves every drop

### The hook

In Diablo II, playing in a game with more players makes monsters drop more items. Players knew this from experience long before anyone published the math, and single-player fans use the `/players` command to raise the effective player count for the same reason. More players, more loot on the ground.

The surprising part is how the game does it. Diablo II does not add extra drops or raise each item's chance separately. It edits one number in each monster's loot table, the weight of the "NoDrop" entry. Shrink that one weight and every item in the table becomes more likely, all at once, in proportion.

### The model

A Diablo II **treasure class** is a weighted table. Each entry has a weight the game files call `Prob`, and one special entry, NoDrop, means "nothing drops for this pick." Call the NoDrop weight `w₀` and the sum of all other weights `R`. Then:

```
P(nothing) = w₀ / (w₀ + R)
P(item i)  = w_i / (w₀ + R)
```

As players are added, the game wants the chance of NoDrop to fall from `P₀` to `P₀^N`, where `N` is an effective player count that the game computes from how many players are in the game and how many party members are nearby. `P₀^N` is the chance that *N independent picks would all be NoDrop*, so this is the complement rule from week 3 used as a design tool.

To hit that target, the game solves for the new NoDrop weight. That leads to a general formula worth knowing on its own:

```
To give one entry probability q, when the other entries sum to R:
    w = R × q / (1 − q)
```

Check it: `w / (w + R) = [Rq/(1 − q)] / [Rq/(1 − q) + R] = q / (q + 1 − q) = q`. It works.

Diablo II's rule is exactly this formula with `q = P₀^N`. Community documentation of the version 1.11 drop system writes it as `NewNoDrop = P^N / (1 − P^N) × SumProb`, rounded down to a whole number, where `SumProb` is our `R`.

### Numbers you can check

The PureDiablo copy of Hrus's Magic Find Guide for v1.11 uses a Devilkin-style example: NoDrop weight 100, all other weights summing to 60. So `P₀ = 100/160 = 0.625`. To see what happens to a single item, add one illustrative entry of weight 6 inside the 60 (this item is ours, not the game's).

| N | Target P(NoDrop) = 0.625^N | New NoDrop weight | P(NoDrop) after rounding | P(some item) | P(our weight-6 item) |
|---|---|---|---|---|---|
| 1 | 62.5% | 100 | 62.5% | 37.5% | 3.75% |
| 2 | 39.1% | 38 | 38.8% | 61.2% | 6.12% |
| 3 | 24.4% | 19 | 24.1% | 75.9% | 7.59% |
| 4 | 15.3% | 10 | 14.3% | 85.7% | 8.57% |
| 6 | 6.0% | 3 | 4.8% | 95.2% | 9.52% |
| 8 | 2.3% | 1 | 1.6% | 98.4% | 9.84% |

Compute any row yourself. For N = 3: `0.625³ = 0.2441`. New weight `= 60 × 0.2441 / 0.7559 = 19.38`, rounded down to 19. Then `P(NoDrop) = 19/79 = 24.1%` and the weight-6 item is `6/79 = 7.59%`.

Three things to see.

- **Our item's weight never changed.** It is 6 in every row. Its chance still rose from 3.75% to 9.84%, because the total shrank from 160 to 61.
- **Every non-NoDrop entry rose by the same factor.** At N = 8, the total is 61 instead of 160, so every item is `160/61 ≈ 2.6` times as likely. The ratios among items are untouched. A sword that was twice as common as a ring still is.
- **There is a ceiling.** Once NoDrop hits its floor, the item can never beat `6/60 = 10%`. Removing "nothing" from a table can only rescale the other entries up to their share among themselves.

### The visual: edit one weight, watch every bar

Open the interactive. The top panel is a weight editor, one row per entry with a number field and a slider. The bottom panel shows each entry's probability as a bar. When you change any weight, the old bars stay on screen as faded ghosts for comparison, and each bar is labelled with its change in percentage points and as a ratio (for example, "×1.63").

Load the "Diablo II NoDrop" preset. Drag the N slider from 1 to 8. The NoDrop bar collapses, and every other bar grows together, each by the same ratio. The weight fields for the items do not move.

Then load the "Boss table" preset from section 1 and add a new row, "Event mount", with weight 50. Every existing bar shrinks. The ring falls from 1.00% to 0.95%. Nobody touched the ring. Switch on the "kills to 95%" column (it uses the week 7 formula `ceil(ln 0.05 / ln(1 − p))`) and the ring's 95th-percentile wait rises from 299 kills to 314.

The first view makes a weight look like a private property of one row. The ghost bars show that it is shared by the whole table.

### Cross-game recognition

**Minecraft (Java Edition) loot tables.** Minecraft stores chest, mob and fishing loot as data files. Each file has one or more **pools**. Each pool is rolled some number of times (`rolls`), and on each roll it picks one entry. The official format documentation states that an entry's chance is its weight divided by the total weight of all entries in the pool, our `w_i / W`. Minecraft also has a `quality` field: the effective weight becomes `max(floor(weight + quality × luck), 0)`. That is the Diablo II idea from the other direction. Luck raises or lowers some weights, and because the total changes, every entry's chance in the pool moves.

**Old School RuneScape, the rare drop table.** Many mid- and high-level monsters in Old School RuneScape can roll into a shared "rare drop table" as one entry of their own table. The rare drop table is itself a 128-slot weighted table. It contains ordinary items, a link into a "gem drop table" in 20 of its 128 slots, and a link into a "mega-rare" table in 15 of its 128 slots. The gem drop table has its own link to the mega-rare table in 1 of its 128 slots. That is nesting, covered in section 3. The design win is that Jagex can tune the shared table once for every monster that links to it.

**Your own spreadsheet.** Every time you write `=B2/SUM(B$2:B$20)` next to a list of weights, you are doing the same thing. The formula makes the dependency visible: every cell refers to the same `SUM`. Change any row and every probability changes.

Three systems, one principle: **in a weighted table, probabilities are shares of a total, so any change to the total is a change to every entry.**

### Design judgment, eyes open

- **Use a Nothing entry as your master volume knob.** Diablo II's approach is good design. One weight controls how generous the table is, and the relative rarity of items stays fixed. If you want "more loot" for groups, events or difficulty levels, shrink Nothing, as Diablo II does, instead of editing every item.
- **Know the ceiling.** Shrinking Nothing can never make an item more likely than its share among the other entries. If the ring must reach 5%, you have to change the ring or its neighbours, not Nothing.
- **Every insertion is a global nerf.** Adding an entry of weight `w` multiplies every other entry's chance by `W / (W + w)`. If you add seasonal items, a new tier, or a collectible to an existing table, decide whose chance pays for it. The honest way is to take the new weight out of Nothing, which keeps every other item exactly where it was. In the boss table, adding the mount at 50 and cutting Nothing from 600 to 550 leaves the ring at 1.00%.
- **Rounding bites at small weights.** Diablo II rounds the new NoDrop down. At N = 6 the target was 6.0% and the result was 4.8%. With small integer weights, rounding can change a probability by a large relative amount. Keep totals large enough (a few hundred at least) that one unit of weight is a small step.
- **Tell players the probability, not the weight.** A weight of 10 means nothing to a player. If you publish odds, publish `w_i / W`, and recompute it after every change to the table.

## 3. Nested tables: multiply along the path

Large games rarely use one flat table. They nest them: an entry in one table points to another table, which is rolled in turn. You saw this in Old School RuneScape's rare drop table and in Diablo II, where treasure classes can point to other treasure classes.

To find the chance of reaching an item, **multiply the probabilities along the path**. If there are several paths to the same item, compute each path and **add** them, because the paths are mutually exclusive (a single roll takes only one path).

### A two-tier boss table

Rebuild the boss table in two levels.

Top table (total 100): Nothing 60, Common 36 (points to the common table), Rare 4 (points to the rare table).
Rare table (total 4): Sword 3, Ring 1.

```
P(ring) = P(Rare) × P(Ring | Rare) = 4/100 × 1/4 = 1%
P(sword) = 4/100 × 3/4 = 3%
```

Now add the event mount. You have two choices.

- **Put it inside the rare table with weight 1.** The rare table total becomes 5. `P(ring) = 0.04 × 1/5 = 0.8%`, `P(sword) = 2.4%`, `P(mount) = 0.8%`. The rare items lost 20% of their chance. The common items did not move at all. Nesting **contained** the change.
- **Put it in the top table, taking 1 from Nothing.** Top table: Nothing 59, Common 36, Rare 4, Mount 1. Every other probability is unchanged, and the mount is 1%.

Nesting gives you **isolation**. Edits inside a sub-table only affect items in that sub-table. This is why well-organized loot systems group items into tiers or categories, pick the tier first, and then pick the item. Designers can tune "how often does a rare drop" separately from "which rare drops."

### Two paths to one table

Old School RuneScape's rare drop table shows the add-the-paths rule. Suppose a monster has rolled into the rare drop table. The chance of then reaching the mega-rare table is:

```
direct path:          15/128                    = 0.11719
through the gem table: 20/128 × 1/128           = 0.00122
total:                                            0.11841
```

The indirect path adds only about 1% to the total, but it shows why you must follow every link. Missing a path in a big nested system is a common source of "why does this item drop more than the spreadsheet says?"

## 4. Rolls, guarantees and what a player sees per kill

One pick from a table is not the same as one kill. Games vary in how many times they roll per kill.

- **Multiple rolls.** A Minecraft pool with `rolls: 3` picks three times, and a Diablo II treasure class can make several picks. If an entry has chance `p` per roll and the table is rolled `r` times independently:

  ```
  expected copies per kill = r × p
  P(at least one per kill) = 1 − (1 − p)^r
  ```

  Three rolls at 1% give 2.97% per kill, not 3%. The expected count is exactly 0.03, but some kills drop two.

- **Guaranteed drops.** Many games separate "always" drops (a boss always drops its currency or bones) from the weighted roll. Put these outside the table so they cannot be diluted.

- **Per-kill probability feeds the week 7 math.** Once you have `P(at least one per kill)`, the dry-streak formulas apply directly. A designer who wants 95% of players to see an item within 50 kills needs a per-kill chance of `1 − 0.05^(1/50) ≈ 5.8%`. Work backward from there to weights.

### Expected value per kill

Weighted tables also set the economy's income. If each entry `i` has a value `v_i` in gold (or any currency), the expected value of one roll is:

```
EV per roll = Σ P(i) × v_i = Σ (w_i / W) × v_i
```

For the flat boss table with Nothing = 0, gold pouch = 50, potion = 20, sword = 400 and ring = 2,000:

```
EV = 0.25 × 50 + 0.10 × 20 + 0.04 × 400 + 0.01 × 2000
   = 12.5 + 2 + 16 + 20
   = 50.5 gold per roll
```

Notice that the two rarest items produce 36 of the 50.5 gold. Rare, valuable drops dominate average income even though most kills never see them. This is why a single change to a rare item's weight can shift an MMO's gold supply more than any change to common items (MMO304 builds on this).

## 5. A design process for loot tables

Put the pieces together. When you design a table, work from player experience back to weights.

1. **List the rewards and their jobs.** Which are income, which are progression, which are trophies?
2. **Set a player-facing target for each.** For progression items, choose the 95th-percentile wait (week 7). For trophies, choose a median. For income, choose expected value per kill.
3. **Convert targets to per-kill chances.** For a 95th-percentile target of `n` kills, `p = 1 − 0.05^(1/n)`. Adjust for multiple rolls.
4. **Group into tiers.** Decide the chance of each tier, then the share of each item inside its tier. Put items you expect to add or change often into their own sub-table.
5. **Convert to weights.** Pick totals large enough that one unit is a small step. Use `w = R × q / (1 − q)` when you need an exact share.
6. **Check the result.** Recompute every probability, EV and percentile from the final weights. Simulate (week 11) to catch paths you missed.
7. **Document the ownership of weight.** Write down which entry absorbs changes (usually Nothing). The next designer to add an item will thank you.

## In-class activity (25 minutes)

Pairs, with a spreadsheet and the interactive.

A dungeon boss currently uses the flat boss table from section 1. The live team wants to add two things for a seasonal event:

- A cosmetic event mount that 50% of players should have within 40 kills.
- Double gold pouch drops during the event.

Constraints: the legendary ring's 95th-percentile wait must stay at 299 kills or fewer, and the sword's chance must not change.

1. Compute the per-kill chance the mount needs, using the median formula from week 7.
2. Design the event table. Show weights, probabilities and the ring's 95th percentile.
3. Compute the EV per kill before and during the event (use the values from section 4, and value the mount at 0 for gold).
4. Swap with another pair. Find any entry whose probability changed that the brief did not ask to change.

**Expected output:** a before-and-after table of weights and probabilities, the ring's 95th-percentile wait, and EV per kill before and during the event. A good answer takes the mount's weight and the extra gold weight out of Nothing.

## Common misconceptions

- **"A weight is the item's own setting."** A weight only has meaning relative to the total. Changing any weight in the table changes every entry's probability.
- **"Adding an item only affects that item."** Adding weight `w` multiplies every other entry's chance by `W / (W + w)`. Take the weight from Nothing, or from a chosen entry, to keep other items where they were.
- **"Removing Nothing makes every item as common as I want."** It rescales the other entries only up to their share among themselves. Past that, you have to change the items' own weights.
- **"Three rolls at 1% means 3% per kill."** The expected count is 0.03 per kill, but the chance of at least one is `1 − 0.99³ ≈ 2.97%`. The gap grows with more rolls or higher chances.

## Check yourself

1. A table has weights Nothing 70, Common 25, Rare 5. A designer adds a new Rare-tier item directly to this table with weight 5. What happens to the chance of the original Rare entry? What weight should be taken from Nothing to keep it unchanged?
2. Using `w = R × q / (1 − q)`, find the weight a new entry needs to have a 2% chance in a table whose other entries sum to 490. After you add it, what is the new chance of an existing entry with weight 49?
3. A Minecraft-style pool is rolled 2 times, and a diamond entry has weight 3 out of a pool total of 60. What is the chance of at least one diamond per chest? How many chests until 95% of players have found at least one?
4. In a Diablo II-style treasure class, NoDrop weight is 60 and the other entries sum to 40. For `N = 3`, compute the new NoDrop weight (rounded down) and the new chance that the pick drops some item.

<details>
<summary>Answers</summary>

1. The total rises from 100 to 105, so the original Rare falls from 5% to `5/105 ≈ 4.76%`. Take 5 from Nothing (70 to 65) and the total stays 100, so the original Rare stays at 5%.
2. `w = 490 × 0.02 / 0.98 = 10`. The new total is 500, so the weight-49 entry goes from `49/490 = 10%` to `49/500 = 9.8%`.
3. Per roll `p = 3/60 = 0.05`. Per chest `1 − 0.95² = 0.0975`. For 95% of players, `n = ceil(ln 0.05 / ln 0.9025) = ceil(29.20) = 30` chests.
4. `P₀ = 60/100 = 0.6`. Target `0.6³ = 0.216`. New weight `= 40 × 0.216 / 0.784 = 11.02`, rounded down to 11. New chance of some item `= 40 / 51 ≈ 78.4%` (it was 40%).

</details>

## Lab hook

**Lab 09, Loot table from targets** ([labs/lab09.md](../labs/lab09.md)). Design a two-tier loot table for a raid boss from a brief of player-facing targets, verify every probability, percentile and EV in a spreadsheet, then apply a seasonal change without moving any protected item. The table you build here is the starting point for the loot design assessment and for the pity-timer work in week 10.

## Sources

- Hrus, "Magic Find Guide v1.11", hosted by PureDiablo ("Magic Find Guide v1.11 – Diablo 2 Resurrected" page) and Diablo Wiki. The NoDrop formula `P^N / (1 − P^N) × SumProb` and the example with NoDrop 100 and other weights summing to 60 (Diablo II: Lord of Destruction, patch 1.11 era). The exact rule for computing the effective player count N is simplified in this lecture.
- The Phrozen Keep forums, "How does NoDrop in treasureclassex.txt work?", community reverse-engineering of the same formula (Diablo II 1.10 to 1.11 era), used as a cross-check.
- Minecraft Wiki, "Loot table" (Java Edition, current format, accessed September 2026). Pools, rolls, entry weight, "weight ÷ total weight" selection, and the `quality × luck` weight adjustment.
- Old School RuneScape Wiki, "Rare drop table" (current game, accessed September 2026). 128-slot table, gem drop table in 20/128, mega-rare table in 15/128, and the gem table's 1/128 link to the mega-rare table.
- Schreiber, I. (2010). *Game Balance Concepts*, Level 4, "Probability and Randomness", and Level 5, "Probability and Randomness Gone Horribly Wrong" (4 August 2010, online course).
- Schreiber, I. & Romero, B. (2021). *Game Balance*. CRC Press. Probability chapter.

## Interactive spec: examples/w09-loot-weights.html

**Purpose.** Show that in a weighted table every probability is a share of the total, so changing, adding or removing one weight moves every other entry. The insight that must be obvious on first load: *faded ghost bars next to the current bars, with ratio labels, after a single weight changed.* On load, show the Diablo II preset at N = 3 with ghosts from N = 1, so the change is already visible.

**Layout.** Left (top on mobile): weight editor. Right (below on mobile): horizontal bar chart of probabilities. Below both: numbers table.

**Weight editor.** One row per entry: name (editable text), weight (integer field 0 to 100,000, plus a slider 0 to 2 × current total), value in gold (optional), a "protected" checkbox, and a delete button. An "Add entry" button (new entry defaults to name "New item", weight 10). A "Snapshot" button stores the current table as the ghost baseline; ghosts also update automatically to the previous state whenever a single edit is committed, unless "Pin baseline" is on.

**Bar chart.** For each entry, a bar of `w_i / W` in percent, and a faded ghost bar for the baseline value. Label each bar with the current percent (2 decimals), the change in percentage points, and the ratio current/baseline (2 decimals). If a protected entry's probability differs from baseline by more than 0.005 points, outline it in the warning colour and show a note "protected entry moved".

**Numbers table.** Columns: entry, weight, probability, rolls-adjusted per-kill chance `1 − (1 − p)^r`, kills to 50% `ceil(ln 0.5 / ln(1 − p_kill))`, kills to 95% `ceil(ln 0.05 / ln(1 − p_kill))`, and EV contribution `p × value × r`. Footer: total weight, EV per kill. Show "n/a" for the kills columns when `p_kill` is 0 or 1.

**Controls.**
- Rolls per kill stepper, 1 to 10, default 1.
- "Take new weight from" select: None (default) or any entry name. When set, adding weight to one entry subtracts the same amount from the chosen entry (not below 0), so other probabilities stay fixed.
- Diablo II mode toggle: marks one entry as NoDrop and shows an N slider from 1 to 8. The NoDrop weight is recomputed as `floor(R × P0^N / (1 − P0^N))` where `P0 = w0_base / (w0_base + R)` and R is the sum of other weights. The item weights must not change as N moves.
- Presets: "Boss table" (Nothing 600, Gold pouch 250 value 50, Healing potion 100 value 20, Rare sword 40 value 400, Legendary ring 10 value 2,000), "Diablo II NoDrop" (NoDrop 100, Item A 6, Item B 54), "Two-tier boss" (a nested mode is optional; if implemented, show the rare sub-table as an indented group whose top-level weight is 4 and whose inner weights are Sword 3, Ring 1, and compute path probabilities as products).

**Test values.**
- Boss table: probabilities 60 / 25 / 10 / 4 / 1 percent. EV per kill 50.5. Ring kills to 95%: 299. Add "Event mount" weight 50: ring 0.952%, ring kills to 95%: 314, nothing 57.14%. With "Take new weight from: Nothing", ring stays 1.00%.
- Diablo II preset (NoDrop 100, others 60): N = 1, 2, 3, 4, 6, 8 give NoDrop weights 100, 38, 19, 10, 3, 1 and Item A (weight 6) at 3.75%, 6.12%, 7.59%, 8.57%, 9.52%, 9.84%.
- Rolls = 3 with an entry at 1%: per-kill 2.97%.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`. Ghost bars differ by opacity and a dashed outline, not colour alone. All fields and sliders keyboard operable, with labels. No game item icons or names beyond generic text.
