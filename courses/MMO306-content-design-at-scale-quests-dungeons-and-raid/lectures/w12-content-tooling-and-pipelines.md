# MMO306 · Week 12 — Content Tooling and Pipelines

**Why this matters:** An MMO ships thousands of quests, encounters, items and props, and each one passes through the same chain of editors, exports, checks and test servers before players see it. That chain decides how fast your team can build and how many broken things reach players. A mistake that costs fifteen minutes in the editor costs days once it is live. Designers who understand the pipeline put their checks where they are cheap, and stop paying for the same bug over and over.

**You will be able to:**
- Compute how many defects of each kind escape a pipeline of stages with given catch rates, and what they cost to fix at each stage.
- Decide where an automated validator pays for itself, and which defects it cannot catch.
- Write validation rules for content data (references, budgets, prerequisites, text) and run them on a sample content set.
- Estimate how iteration time limits a designer's output, and argue for a tool change with numbers.

**Before class:** Philip Kollar, "Final Fantasy 14 killed by Square Enix's stubbornness, reborn by a new approach," Polygon, 20 March 2014 (a report of Naoki Yoshida's GDC 2014 talk, 10 minutes). Warcraft Wiki, "Public Test Realm" (5 minutes). Reread [GD202 week 14, narrative testing](../../GD202-narrative-and-quest-design/lectures/w14-narrative-testing.md) sections 3 and 5.

**Prerequisites from earlier courses:** [GD202 week 12, Ink and Yarn Spinner](../../GD202-narrative-and-quest-design/lectures/w12-tools-ink-and-yarn-spinner.md) (content written as text files and compiled). [GD202 week 14, narrative testing](../../GD202-narrative-and-quest-design/lectures/w14-narrative-testing.md) (state search and invariants for branching stories; this lecture uses them as one stage and does not re-teach them). [GD202 week 11, writing for localization](../../GD202-narrative-and-quest-design/lectures/w11-writing-for-localization.md) (string IDs). [MMO301 week 11, Koster's laws](../../MMO301-virtual-worlds-history-theory-and-design/lectures/w11-kosters-laws-of-online-world-design.md) (Corrupted Blood and the Falador Massacre, and why pairs of systems break). [DB201 week 9, schema migrations in a live game](../../DB201-data-persistence-and-telemetry/lectures/w09-schema-migrations-in-a-live-game.md). Looking ahead, CS201 weeks 7 and 14 cover hot reload and editors from the engine side ([week 7](../../CS201-game-engine-architecture/lectures/w07-resource-management-and-hot-reload.md), [week 14](../../CS201-game-engine-architecture/lectures/w14-tools-and-editors.md)).

**Interactive:** [`examples/w12-defect-funnel.html`](../examples/w12-defect-funnel.html). Keep it open during section 2.

---

## 1. Content is data, and data flows through a pipeline

A quest in a shipped MMO is rarely code. It is a record: an ID, a level, a quest giver's ID, a list of objectives that point at monster and item IDs, a reward, and string IDs for its text in every language. An encounter is a record that points at a boss, its abilities, its timers and its loot table. A prop is a mesh file with a polygon count, textures and a material.

Treating content as data has one large benefit. Designers can make and change content without a programmer, in tools built for them. It also has one large risk. A record can point at something that doesn't exist, break a budget, or depend on a quest the player can't reach, and nothing stops it until someone notices.

A **content pipeline** is the path a piece of content takes from a designer's head to players. A typical MMO pipeline has these stages:

1. **Authoring.** The designer builds the content in an editor: a quest tool, an encounter scripting language, a spreadsheet, a level editor. Good editors prevent some errors outright (a dropdown of valid NPCs can't hold a misspelled one).
2. **Export and validation.** The content is saved as data files, and automated checks run on them. A **validator** is a program that reads content data and reports anything that breaks a rule.
3. **Review.** Another designer reads and plays the content. Writers review text.
4. **QA.** Testers play the build on purpose to break it.
5. **Public test.** Players try the patch on a test server before it goes live. World of Warcraft's Public Test Realm is a special server where features for the next patch are tested, with a bug reporter for feedback. EVE Online's equivalent, Singularity, has since May 2023 opened only in scheduled test windows with a specific focus.
6. **Live.** The content reaches all players. Defects found here need a hotfix, a patch, sometimes a rollback, and player communication.

Each stage finds some defects and lets others through. The next section puts numbers on that.

## 2. Worked example: where the defects get caught

### The hook

Final Fantasy XIV first launched in September 2010 and was so badly received that Square Enix rebuilt it as A Realm Reborn. At GDC 2014, A Realm Reborn's director Naoki Yoshida described what had gone wrong with the original. One example became famous. A single flowerpot outside an inn had over 1,000 polygons and 150 lines of shader code, so it cost about as much to draw as a player character. The graphics budget went on scenery, and the original team limited the number of player characters on screen at once to 20, in a game whose appeal was crowds of players.

A flowerpot that costs as much as a character is the easiest defect in the world to catch. One line in an export script would do it: "props may not exceed N polygons." Yet it reached the shipped game and became part of a performance problem the team answered by capping players on screen. Yoshida blamed an obsession with graphical quality. In pipeline terms, no stage weighed each asset's detail against a budget before players saw it.

That is the question for this week. Given the defects your team will make, which stage catches each kind, and what does each catch cost?

### The model

Sort defects into **classes**, because stages see classes differently:

- **Data defects.** Broken references, missing text strings, budgets exceeded, wrong levels. A machine can check them against rules.
- **Logic defects.** A quest that can't be completed in some order, a boss script with a timer that never fires. Some can be found by searching states (GD202 week 14), most by playing.
- **Interaction defects.** Two parts that each work and break together, like Corrupted Blood's debuff and hunter pets (MMO301 week 11). Tuning problems that only show at scale belong here too.

Each stage `s` catches a share `c_s,k` of the class-`k` defects that reach it, and each defect found there costs `x_s` hours to fix. Defects that aren't caught move to the next stage. So for class `k`, starting with `n_k` defects:

```
reach stage s:     n_k × (1 − c_1,k) × (1 − c_2,k) × ... × (1 − c_(s−1),k)
found at stage s:  (defects reaching s) × c_s,k
escape to live:    n_k × Π over all stages (1 − c_s,k)
total cost:        Σ over stages (found at s) × x_s  +  (escaped) × x_live
```

- `n_k` is the number of class-`k` defects introduced per 1,000 content items.
- `c_s,k` is the catch rate of stage `s` for class `k`, between 0 and 1.
- `x_s` is the hours to fix one defect found at stage `s`. It grows along the pipeline, because a late fix means rebuilding, retesting, rescheduling and, once live, a hotfix and an apology.

### Numbers you can check

A team introduces 100 defects per 1,000 content items: 60 data, 30 logic, 10 interaction. The catch rates and costs below are teaching values, chosen to be plausible, not measured from a studio.

| Stage | Hours per fix `x_s` | Catch: data | Catch: logic | Catch: interaction |
|---|---|---|---|---|
| Author self-check | 0.25 | 0.30 | 0.20 | 0.00 |
| Validator (added later) | 0.5 | 0.90 | 0.30 | 0.00 |
| Review | 1 | 0.30 | 0.20 | 0.10 |
| QA | 4 | 0.50 | 0.60 | 0.30 |
| Public test | 8 | 0.50 | 0.40 | 0.50 |
| Live | 40 | everything left | | |

```python
# Defects per 1,000 content items, by class
defects = {"data": 60, "logic": 30, "interaction": 10}

# Stages in order: (name, hours to fix a defect found here, catch rate by class)
PIPELINE = [
    ("author",    0.25, {"data": 0.30, "logic": 0.20, "interaction": 0.00}),
    ("review",    1.0,  {"data": 0.30, "logic": 0.20, "interaction": 0.10}),
    ("QA",        4.0,  {"data": 0.50, "logic": 0.60, "interaction": 0.30}),
    ("PTR",       8.0,  {"data": 0.50, "logic": 0.40, "interaction": 0.50}),
]
LIVE_COST = 40.0
VALIDATOR = ("validator", 0.5, {"data": 0.90, "logic": 0.30, "interaction": 0.00})

def run(stages):
    left = dict(defects)
    hours = 0.0
    for name, cost, catch in stages:
        found = {c: left[c] * catch[c] for c in left}
        for c in left:
            left[c] -= found[c]
        n = sum(found.values())
        hours += n * cost
        print(f"  {name:9s} finds {n:5.1f}  costs {n * cost:6.1f} h")
    live = sum(left.values())
    hours += live * LIVE_COST
    print(f"  {'live':9s} finds {live:5.1f}  costs {live * LIVE_COST:6.1f} h")
    print(f"  escaped by class: " + ", ".join(f"{c} {v:.2f}" for c, v in left.items()))
    print(f"  total {hours:.1f} h")
    return live, hours

print("without validator")
run(PIPELINE)
print("with validator after the author")
run(PIPELINE[:1] + [VALIDATOR] + PIPELINE[1:])
```

It prints:

```
without validator
  author    finds  24.0  costs    6.0 h
  review    finds  18.4  costs   18.4 h
  QA        finds  28.9  costs  115.7 h
  PTR       finds  13.6  costs  108.6 h
  live      finds  15.1  costs  604.3 h
  escaped by class: data 7.35, logic 4.61, interaction 3.15
  total 853.0 h
with validator after the author
  author    finds  24.0  costs    6.0 h
  validator finds  45.0  costs   22.5 h
  review    finds   5.6  costs    5.6 h
  QA        finds  12.2  costs   48.9 h
  PTR       finds   6.0  costs   48.3 h
  live      finds   7.1  costs  284.4 h
  escaped by class: data 0.73, logic 3.23, interaction 3.15
  total 415.8 h
```

Check the escaped data defects without a validator by hand: `60 × 0.7 × 0.7 × 0.5 × 0.5 = 7.35`. With the validator, one more factor of `0.1` gives `0.735`.

Three things stand out.

**Count and cost point in opposite directions.** Without the validator, live finds 15 of the 100 defects, fewer than any stage except the public test. But it costs 604 of 853 hours, 71% of the total. A chart of defect counts tells you live is a small problem. A chart of hours tells you it is the problem.

**A cheap early check halves the bill.** The validator finds 45 defects at half an hour each. Everything downstream then has less to find, and total cost falls from 853 to 416 hours per 1,000 items. Most of the saving isn't at the validator. It is at QA, the public test and live, which now receive fewer defects.

**The validator can't see everything, and what's left changes shape.** Escaped data defects fall from 7.35 to 0.73. Interaction defects stay at 3.15, because no rule-checker catches them. Before the validator, interaction defects were 21% of what escaped (3.15 of 15.1). After, they are 44% (3.15 of 7.1). Your next improvement is no longer a better validator. It is a better public test, or live safeguards, because that is where the remaining cost is.

### A visual you can move

Open the interactive. The top view is a funnel: 100 defects enter at the left, and at each stage a coloured band drops out (steel for data, ochre for logic, blood for interaction). The bottom view shows the same stages as bars of hours. Toggle the validator and watch the top view barely change past the first stages while the bottom view's live bar shrinks by more than half. Then drag the public test's interaction catch rate. It is the one slider that moves the live bar after the validator is on.

### Cross-game recognition

**Final Fantasy XIV (2010 original).** The flowerpot is a data defect, in the model's terms: a number broke a budget. A validator with a polygon budget per asset type has a catch rate near 1 for it. With no such stage, its catch rate was effectively 0 until it met players, and by then the cost was a performance ceiling for the whole game.

**RuneScape, the Falador Massacre (June 2006).** MMO301 week 11 tells the story. The RuneScape Wiki's account adds the pipeline detail. Content developers had to code every way a player could leave a player-owned house by hand, each removing the house's player-versus-player option, and one way was missed. Jagex never found which. They fixed it with a safety net in the game's safe zones, which removes any stray player-versus-player state when a player leaves a dangerous area. In the model, that is a new live-stage check with a high catch rate and low cost per defect. When you can't enumerate every path, check the state that must be true at the end.

**World of Warcraft, the Public Test Realm and Corrupted Blood (patch 1.7, September 2005).** The PTR is a stage where thousands of players test a patch. It has a high catch rate for defects players stumble into, and a low one for defects that need an unusual combination, because testers don't play like a live realm. Corrupted Blood spread when players carried a raid debuff out on dismissed pets into crowded cities. The fix came in patch 1.8, which made pets unable to carry it and confined it to Zul'Gurub. A crowded city, a full raid and players looking for trouble are exactly the conditions a test server rarely reproduces. Interaction defects need scale to show up, which is why they escape.

**EVE Online, Singularity.** CCP's test server opens only in scheduled test windows with specific testing focuses. A focused window raises the catch rate for the class under test and does little for the rest, which is a deliberate trade of breadth for depth.

Four games, one model. A defect escapes when no stage has a catch rate for its class. You fix that with a check at the right stage, cheap and early for data (the flowerpot), a state check at the end for paths you can't list (the Falador fix), and scale testing for interactions (Corrupted Blood).

### Eyes-open design judgment

- **Automate every rule you can write down.** If a rule fits in one sentence ("every quest giver exists," "no prop over 5,000 triangles"), it belongs in the validator, not in a reviewer's memory. Validators are cheap to run on every save.
- **Make errors impossible where you can.** A dropdown of existing NPCs, a level field that only allows the zone's range, a reward field that shows the budget. Each has a catch rate of 1 at the cheapest stage of all.
- **Don't let the validator cry wolf.** A validator that reports 300 warnings a day gets ignored, and its real catch rate falls to zero. Separate errors (block the build) from warnings (someone reviews them weekly), and keep the error list empty.
- **Spend the next hour where the cost is.** After data defects are handled, the cost sits in interaction and tuning defects. They need playtests at realistic scale, telemetry, and live safeguards such as kill switches that disable one quest or boss without a patch.
- **Measure your own catch rates.** Every defect found live should be tagged with the stage that should have caught it. After a few months, you have real `c_s,k` values instead of the teaching values used here.

### Check yourself (worked example)

1. With no validator, how many logic defects reach QA? How many does QA find?
2. The team raises the public test's interaction catch rate from 0.5 to 0.8, with the validator on. How many interaction defects escape now, and how many live hours does that save?
3. A second validator rule costs 0.5 hours per defect and catches 30% of interaction defects. Is it worth adding? Compare it with question 2.

<details>
<summary>Answers</summary>

1. `30 × 0.8 × 0.8 = 19.2` reach QA; QA finds `19.2 × 0.6 = 11.52`.
2. Interaction defects reaching the public test: `10 × 1 × 1 × 0.9 × 0.7 = 6.3`. Escaping at 0.8: `6.3 × 0.2 = 1.26`, down from 3.15. Live saving `(3.15 − 1.26) × 40 = 75.6` hours (the public test spends `(5.04 − 3.15) × 8 = 15.1` more, so the net saving is about 60.5 hours).
3. It would catch 3 of the 10 early (1.5 hours), and every later stage sees 70% as many. Escapes fall from 3.15 to 2.205, saving about 37.8 live hours, plus smaller savings at QA and the public test. It is worth adding, but a rule that catches 30% of interaction defects is rare. Most interaction rules can only be written after you've seen the defect once.

</details>

## 3. What a validator checks

A validator reads the content data and checks it against rules. Here is a small one for quests. It runs on four records and three kinds of rule: references (every ID points at something that exists), budgets (rewards within the level's limit), and ordering (a quest never requires a harder one).

```python
quests = {
    "q_wolves":  {"level": 12, "giver": "npc_hana", "requires": [],           "xp": 900,  "text": "str_101"},
    "q_den":     {"level": 13, "giver": "npc_hana", "requires": ["q_wolves"], "xp": 1400, "text": "str_102"},
    "q_alpha":   {"level": 14, "giver": "npc_ravi", "requires": ["q_den"],    "xp": 5200, "text": "str_103"},
    "q_return":  {"level": 12, "giver": "npc_hana", "requires": ["q_alpha"],  "xp": 700,  "text": "str_104"},
}
npcs = {"npc_hana"}
strings = {"str_101", "str_102", "str_104"}
XP_BUDGET = {12: 1000, 13: 1500, 14: 2000}   # most XP one quest may give, by level

def validate(quests):
    errors = []
    for qid, q in quests.items():
        if q["giver"] not in npcs:
            errors.append(f"{qid}: unknown quest giver {q['giver']}")
        if q["text"] not in strings:
            errors.append(f"{qid}: missing text {q['text']}")
        if q["xp"] > XP_BUDGET[q["level"]]:
            errors.append(f"{qid}: {q['xp']} XP over the level {q['level']} budget")
        for r in q["requires"]:
            if r not in quests:
                errors.append(f"{qid}: requires unknown quest {r}")
            elif quests[r]["level"] > q["level"]:
                errors.append(f"{qid}: level {q['level']} but requires level {quests[r]['level']} quest {r}")
    return errors

for e in validate(quests):
    print(e)
```

It prints:

```
q_alpha: unknown quest giver npc_ravi
q_alpha: missing text str_103
q_alpha: 5200 XP over the level 14 budget
q_return: level 12 but requires level 14 quest q_alpha
```

Each line is a defect that would otherwise travel to review or QA. The first two would show up as an empty NPC spot and a blank quest window. The third is a faucet error (MMO304 week 3) that a reviewer might never notice, because 5,200 looks like a reasonable number. The fourth is the kind of ordering mistake that creeps in when two designers edit the same chain.

The rule families worth building, roughly in order of payoff:

- **References.** Every ID points at a record that exists: NPCs, items, monsters, strings, zones, loot tables.
- **Uniqueness.** No two records share an ID. Duplicate IDs in merged spreadsheets are a classic silent failure.
- **Budgets.** Rewards within the level's curve, loot tables within their drop-rate totals, assets within polygon and texture limits, encounter timers within the fight length.
- **Graphs.** Prerequisite chains have no cycles and every quest is reachable from a starting state. GD202 week 14 shows how to search states for this.
- **Text.** Every string ID exists in every shipped language, and strings fit their UI boxes at the longest translation (GD202 week 11).
- **Invariants.** Statements that must always hold, such as "no quest item is sellable" or "every boss has an enrage condition." The Falador fix was an invariant checked at runtime.

## 4. The iteration loop

The pipeline has a second cost that doesn't show up as defects: the time between a designer making a change and seeing it in the game. Call it the **iteration time**. It is the edit time plus the wait (export, build, server restart, walking back to the spot, re-triggering the encounter).

```
iterations per hour = 60 / (t_edit + t_wait)
```

With a 2-minute edit:

| Wait after each change | Minutes per iteration | Iterations per hour | Per 6-hour design day |
|---|---|---|---|
| 10 minutes (full rebuild and restart) | 12 | 5.0 | 30 |
| 1 minute (reload the zone) | 3 | 20.0 | 120 |
| 10 seconds (hot reload the data) | 2.17 | 27.7 | 166 |

A designer tuning a boss needs dozens of tries to get a phase to feel right. At 30 tries a day, that is one phase a day. At 166, it is several. Nothing about the designer changed. Only the wait did.

Two tool features cut the wait most for content work. **Hot reload** means the running game notices that a data file changed and loads the new version without a restart. **Debug commands** let designers jump straight to a state: teleport to the boss, set its health to 30%, complete the quest's first objective, spawn the loot. CS201 week 7 covers how engines implement hot reload.

The two halves of this lecture connect. A fast loop tempts designers to skip the validator because it is "slow." Run the validator in the hot-reload path, on the changed records only, so it adds a second, not a minute. A check that runs on every save has a catch rate near its maximum. A check that runs nightly has a catch rate of zero for everything a designer reverted before night.

## 5. Changing content in a live game

Content data outlives the build that shipped it. A few practices keep that safe.

- **Stable IDs.** Once shipped, an ID never changes meaning. Players have it in their quest logs and inventories. Retire records instead of reusing their IDs. DB201 week 9 covers the database side of changing shipped data.
- **Content lock.** Some days before a patch, content for it stops changing except for fixes, so QA and the public test are testing what will ship.
- **Kill switches.** A server-side flag can turn off one quest, boss, item or event without a patch. It turns a 40-hour live defect into a 1-hour one: switch it off, fix it in the next build.
- **Data versioning.** Content files live in version control like code, so every change has an author and a reason, and a bad change can be reverted.

## In-class activity (25 minutes)

In pairs. Your team ships a zone of 200 quests each patch, and last patch 12 defects reached live.

1. **(5 min)** Sort these 12 real-sounding defects into data, logic and interaction: missing German text on 3 quests; a quest that pays 4× the level budget; a chain unfinishable if step 2 is abandoned; an escort NPC that walks through a wall; two event timers that start the same boss twice; a reward item that duplicates when traded mid-quest; a quest giver placed underground; an item ID that points to a deleted item; a boss that resets if pulled across a zone border; a daily quest that can be done twice across midnight; a trash pack that respawns inside the dungeon entrance; a quest objective counting kills of the wrong monster.
2. **(10 min)** For each defect, name the cheapest stage that could catch it and write the rule or test that would.
3. **(10 min)** Estimate hours saved per patch if your proposals had been in place, using 40 hours per live defect and your own guesses for the earlier costs.

Expected output: the sorted list, one rule or test per defect, and a savings estimate.

## Common misconceptions

- **"Live bugs are rare, so they are a small problem."** They are few and expensive. In the teaching numbers, live defects are 15% of the count and 71% of the cost.
- **"A good validator means we can cut QA."** A validator catches rule breakers. Interaction and tuning defects pass straight through it, and after the validator they are the larger share of what escapes.
- **"Tools are a programmer's concern."** Designers decide which rules exist and which states need debug shortcuts. Only designers know that 5,200 XP is wrong for a level-14 quest.
- **"More warnings mean a safer pipeline."** Warnings that nobody reads have a catch rate of zero and bury the real errors. Keep the error list short and empty.

## Check yourself

1. A pipeline has three stages catching 40%, 50% and 50% of a class, with 50 defects of that class. How many escape?
2. Using the teaching table without a validator, how many interaction defects escape, and what share of live cost do they make up?
3. A tool change cuts the wait from 5 minutes to 30 seconds with a 3-minute edit. How many more iterations does a 6-hour day allow?
4. Write one validator rule each for a loot table, a boss encounter and a localized string.
5. Why did the Falador Massacre fix check the state in safe zones instead of the paths out of the house?

<details>
<summary>Answers</summary>

1. `50 × 0.6 × 0.5 × 0.5 = 7.5`.
2. `10 × 1 × 0.9 × 0.7 × 0.5 = 3.15` escape. They cost `3.15 × 40 = 126` of 604.3 live hours, about 21%.
3. Before, `360 / 8 = 45`. After, `360 / 3.5 = 102.9`, so about 58 more.
4. Examples: loot drop chances in a table sum to at most 100%; every boss has an enrage timer shorter than the instance's reset time; every string ID exists in every shipped language and is no longer than its UI box at the widest font.
5. The paths couldn't all be listed (one was missed and never found). The end state could: nobody in a safe zone should have a player-versus-player option. Checking the invariant catches every path, including ones nobody knows about.

</details>

## Lab / assignment hook

[Lab 12, a content validator](../labs/lab12.md). You write a validator for a sample zone's quests, NPCs, items and loot tables, run it on seeded bad data, and use a defect funnel calculator to show what your rules save. The rules you write are required for the final dungeon's content files.

## Sources

- Kollar, P. "Final Fantasy 14 killed by Square Enix's stubbornness, reborn by a new approach." Polygon, 20 March 2014 (read via the Internet Archive copy of 21 March 2015). Report of Naoki Yoshida's GDC 2014 talk; the original game launched in 2010; the flowerpot had over 1,000 polygons and 150 lines of shader code, about the resources of one player character; player characters on screen limited to 20.
- Wikipedia, "Final Fantasy XIV (2010 video game)" (accessed September 2026). Release date 30 September 2010.
- Warcraft Wiki, "Public Test Realm" (accessed September 2026). A special server where upcoming patch features are tested, with a bug reporter for feedback.
- Warcraft Wiki, "Corrupted Blood (debuff)" (accessed September 2026). Patch 1.7.0 (13 September 2005) opened Zul'Gurub; the debuff left the raid on dismissed hunter pets and warlock minions and spread in cities; patch 1.8.0 made pets ineligible and confined it to Zul'Gurub.
- RuneScape Wiki, "Falador Massacre" (accessed September 2026). 5 to 6 June 2006, World 111; developers coded each exit path from player-owned houses by hand and one was missed; the cause was never found; fixed with a safety net in safe zones that removes stray state when a player leaves a dangerous area (citing Calvin, *RuneScape: The First 20 Years*, Dark Horse, 2021, p. 59).
- EVE University Wiki, "Singularity" (accessed September 2026). CCP's public test server; since late May 2023 opened only during scheduled test windows with specific testing focuses.

## Interactive spec: examples/w12-defect-funnel.html

**Insight the visual must make obvious:** defect counts and defect costs point in opposite directions. Live catches few defects and costs most of the hours. A cheap validator early cuts the total bill by half, mostly at later stages, and leaves interaction defects as the new largest share of what escapes.

**Layout.** Two linked views stacked (funnel on top, cost bars below), full width on mobile.

- **Top view, "Where defects are found."** A horizontal funnel (a stacked band chart) over the stages Author, Validator (only when on), Review, QA, Public test, Live. The band's height at each stage is defects remaining, split into three stacked colours: data (steel), logic (ochre), interaction (blood). Below each stage, the number found there, to one decimal.
- **Bottom view, "What they cost."** Bars per stage of hours spent (`found × x_s`), same order, with the total above. The live bar is outlined in blood. Beside the bars, a small stacked bar of escaped defects by class, with each class's share in percent.

**Controls (labelled, keyboard reachable):**
- Toggle "Validator after author" (default off).
- For each stage, three catch-rate sliders (data, logic, interaction), 0 to 1, step 0.05, defaults from the lecture table. Collapse them under a "Stage settings" disclosure per stage so the first screen shows the picture.
- Cost per fix per stage (numeric inputs), defaults 0.25, 0.5, 1, 4, 8 and live 40.
- Defects entering: data, logic, interaction (numeric inputs), defaults 60, 30, 10.
- Toggle "Counts / hours" on small screens to swap which view is shown full size.

**Readouts:** total hours, live hours and live share of total, escaped defects by class with shares.

**Test values (defaults):**
- Validator off: found author 24.0, review 18.4, QA 28.9, public test 13.6, live 15.1; hours 6.0, 18.4, 115.7, 108.6, 604.3; total 853.0; escaped data 7.35, logic 4.61, interaction 3.15; live share of hours 70.8%; interaction share of escapes 20.8% (exact 3.15 / 15.108 = 0.20850, which rounds down).
- Validator on: found author 24.0, validator 45.0, review 5.6, QA 12.2, public test 6.0, live 7.1; hours 6.0, 22.5, 5.6, 48.9, 48.3, 284.4; total 415.8; escaped data 0.73, logic 3.23, interaction 3.15; interaction share of escapes 44.3%.
- Validator on and public test interaction catch 0.8: interaction escaped 1.26.

Use the program palette from `templates/interactive-tokens.css`. No game names or art; stage labels are generic.
