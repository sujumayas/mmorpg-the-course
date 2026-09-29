# GD202 · Week 04 — Dialogue Systems and State Flags

**Why this matters:** Last week you watched a dialogue tree explode. This week you learn how shipped games remember what the player did without writing a new branch for every combination. The answer is state: flags, counters and quest stages that the dialogue reads. Get state right and a small number of lines feels like a world that remembers you. Get it wrong and the barkeep thanks you for killing wolves you never met.

**You will be able to:**
- Model a dialogue line as a rule with conditions on world state, and compute which line a rule-based system picks for any state.
- Enumerate every combination of a set of flags and find uncovered states, ties and dead rules by hand and in code.
- Rewrite skill checks, quest-stage checks and read counts from shipped games and tools into the same rule form.
- Choose between booleans, counters and stages for a piece of story state, and justify the choice in terms of bugs it prevents.

**Before class:** inkle, *Writing with Ink* (github.com/inkle/ink, `Documentation/WritingWithInk.md`), Part One section 7 "Varying Choices" (conditional choices and read counts) and section 8 "Variable Text", then Part 3 section 1 "Global Variables". Bateman (ed.), *Game Writing: Narrative Skills for Videogames* (2nd ed., 2021), the chapter on interactive dialogue.

**Prerequisites from earlier courses:** [CS102 week 8, graphs, maps and dialogue](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w08-graphs-maps-and-dialogue.md) (dialogue as a graph, and why static reachability ignores flags). [CS102 week 11, state and state machines](../../CS102-programming-for-games-ii-structures-and-patterns/lectures/w11-state-and-state-machines.md) (four booleans make sixteen worlds). [CS101 week 6, dictionaries](../../CS101-programming-for-games-i/lectures/w06-dictionaries-item-databases.md) (the data structure behind a fact table). [GD101 week 9, choice and meaningful decisions](../../GD101-introduction-to-game-design/lectures/w09-choice-and-meaningful-decisions.md). [GD202 week 3, branching structures and the combinatorial explosion](w03-branching-structures-and-the-combinatorial-explosion.md) (paths, leaves and bottlenecks).

**Interactive:** [`examples/w04-rule-matcher.html`](../examples/w04-rule-matcher.html). Keep it open during section 2.

---

## 1. Two ways to remember a choice

A game can remember what the player did in two ways.

The first is **by position**. In a pure dialogue tree, the player's history is where they are. If you are standing on node 17, you must have picked options A, then C, then B, because that is the only path to node 17. [Week 3](w03-branching-structures-and-the-combinatorial-explosion.md) showed the cost. Every remembered choice multiplies the number of nodes, and three choices per node over five levels already gives 243 leaves.

The second is **by state**. The game writes a small fact into memory when something happens (`wolves_dead = true`) and any later scene can read it. The paths fold back together at a bottleneck (ink calls it a gather, as week 3 noted), but the fact survives the fold. The player's history lives in the variables, not in the shape of the graph.

Almost every shipped narrative game uses both. The shape of the conversation handles the next minute. State handles the next ten hours.

### Words we will use

- A **fact** is one named piece of world state with a value: `met = true`, `speech = 45`, `quest_stage = 30`. The whole collection is the **state**.
- A **flag** is a fact with only two values, true or false. Designers often say "flag" for any story fact. In this lecture a flag is strictly boolean.
- A **counter** is an integer fact that goes up (and sometimes down): times you visited, gold owed, approval.
- A **stage** is an integer fact that records how far a quest has progressed, with gaps left for later insertions (10, 20, 30).
- A **condition** (or **criterion**) is a test on one fact: `met == true`, `speech >= 50`.
- A **rule** pairs a set of conditions with a piece of content, usually a line of dialogue.
- A rule **matches** a state when every one of its conditions is true in that state.

### Where state lives in shipped games

You have met all of these as a player, even if you never saw the variable.

**World of Warcraft (current retail API).** Every quest has an ID, and the client can ask whether a quest is complete with `C_QuestLog.IsQuestFlaggedCompleted(questID)`, which returns true or false. The name says it all. A completed quest is stored as a flag. The Warcraft Wiki's example checks quest 176, the Elwynn Forest bounty on Hogger. Much of what an MMO shows you (which NPCs offer what, which follow-up quests appear) is decided by rules that read these flags.

**The Elder Scrolls V: Skyrim (Creation Kit, 2011).** Bethesda's quests carry numbered stages. The condition function `GetStage` returns the highest stage completed so far. If stages 10, 30 and 75 are done, `GetStage` returns 75, even if 30 was finished last. A separate function, `GetStageDone`, asks whether one specific stage has ever been completed. So one integer stands in for a whole set of flags, as long as the quest moves forward in order. The moment a quest can do stages out of order, the designer must switch to the second function, or the dialogue will read the wrong answer.

**ink (inkle's open-source narrative language).** In ink, the name of a section of script (a "knot") is also a variable. Writing `{seen_clue}` in a condition tests whether the player has read that section. The documentation points out that this is really an integer, the number of times the content has been seen, so `{seen_clue > 3}` also works. Every piece of content is its own counter, for free.

Three systems, one idea. Content is gated by tests on facts, and the facts are written by earlier content.

## 2. Worked example: who speaks when you walk into the inn?

### The hook

In Left 4 Dead (Valve, 2008) the four survivors chatter constantly. They call out items, tease each other and react to where they are and what just happened, and the lines rarely feel canned. At GDC 2012, Valve programmer Elan Ruskin explained the system behind it. Characters match hundreds of facts about the world against a database of thousands of candidate lines. The talk's description stresses that the system cascades from special cases to general ones.

That phrase, special to general, is the whole model. You do not write a branch for every situation. You write a general line that is always true, then more specific lines for situations worth marking. The system picks the most specific line that fits.

### The model

State `S` is a set of facts. Each rule `r` has a set of conditions `C_r` and a line of dialogue.

```
matches(r, S)  =  every condition in C_r is true in S
score(r)       =  |C_r|, the number of conditions
chosen line    =  the matching rule with the highest score
```

- A rule with zero conditions always matches. It is the **fallback**, the line of last resort.
- A rule with more conditions is more specific, so it wins when it matches.
- If two matching rules share the top score, the result is a **tie**. A real system must break it somehow, and the choice is a design decision (more below).

This is the simplest form of the rule-based approach. The cross-game part of this section shows how Valve's own code extends it with weights.

### Numbers you can check

A barkeep in a small town reads three flags.

- `met`: the player has spoken to her before.
- `wolves_dead`: the player finished the wolf quest.
- `thief`: a guard caught the player stealing in town.

The writer gives her six rules.

| Rule | Conditions | Line (paraphrased) | Score |
|---|---|---|---|
| R0 | none | "Welcome, traveller. Sit anywhere." | 0 |
| R1 | `met` | "Back again? Same table as before." | 1 |
| R2 | `wolves_dead` | "You're the one who cleared the wolves!" | 1 |
| R3 | `thief` | "Keep your hands where I can see them." | 1 |
| R4 | `met`, `wolves_dead` | "Back again, wolf-slayer. First drink's on me." | 2 |
| R5 | `wolves_dead`, `thief` | "Hero or not, I'm watching my till." | 2 |

Three flags make `2^3 = 8` possible states. Run every one through the model. Here it is in Python.

```python
from itertools import product

FLAGS = ["met", "wolves_dead", "thief"]

RULES = [
    ("R0", {}, "Welcome, traveller. Sit anywhere."),
    ("R1", {"met": True}, "Back again? Same table as before."),
    ("R2", {"wolves_dead": True}, "You're the one who cleared the wolves!"),
    ("R3", {"thief": True}, "Keep your hands where I can see them."),
    ("R4", {"met": True, "wolves_dead": True}, "Back again, wolf-slayer. First drink's on me."),
    ("R5", {"wolves_dead": True, "thief": True}, "Hero or not, I'm watching my till."),
]

def matches(criteria, state):
    return all(state[k] == v for k, v in criteria.items())

def best(state):
    scored = [(len(c), name) for name, c, _ in RULES if matches(c, state)]
    top = max(s for s, _ in scored)
    return [name for s, name in scored if s == top]

print("met  wolves thief  -> winner(s)")
for values in product([False, True], repeat=len(FLAGS)):
    state = dict(zip(FLAGS, values))
    winners = best(state)
    mark = "  TIE" if len(winners) > 1 else ""
    print(" ".join(f"{str(v):6}" for v in values), "->", ", ".join(winners) + mark)
```

It prints:

```
met  wolves thief  -> winner(s)
False  False  False  -> R0
False  False  True   -> R3
False  True   False  -> R2
False  True   True   -> R5
True   False  False  -> R1
True   False  True   -> R1, R3  TIE
True   True   False  -> R4
True   True   True   -> R4, R5  TIE
```

Check two rows by hand. In the state (met, not wolves, not thief), R0 and R1 match. R1 scores 1, R0 scores 0, so R1 wins. In the state (met, wolves, thief), all three flags are true, so all six rules match. R4 and R5 both score 2 and nothing scores higher. That is a tie.

### What the table tells you

Three things jump out.

**Six lines cover eight states.** No state is silent, because the fallback R0 matches everything. That is the economic argument for rules. A tree needs one leaf per state it distinguishes. Rules need one line per situation *worth distinguishing*, and the fallback absorbs the rest. Add a fourth flag and the state count doubles to 16. The rule count only grows if you decide the new flag deserves its own lines.

**Two states are ties.** A returning customer who is also a known thief gets either "Back again?" or "Keep your hands where I can see them." Which one is right? Almost certainly the thief line. Being caught stealing matters more to a barkeep than being a regular. The model cannot know that. Only the writer can, and the tie is the model telling the writer where it needs a decision. There are three standard fixes. You can add a more specific rule (R6 on `met` and `thief`, score 2, which beats both). You can give rules explicit priorities. Or you can accept a random pick, which is what Valve's code does, and which suits barks (short incidental lines) far better than plot.

**The all-true state is a tie between two 2-condition rules.** Adding R6 does not fix it, because R6 also scores 2 in that state. You would need a 3-condition rule, or a priority. Specific-to-general cascades have this property in general. The most crowded states are the ones where many flags are true at once, which is late-game, which is where your players have invested the most. Test there first.

Open the interactive now. The left panel has the three flags as toggles and shows every rule's score for the current state, with the winner highlighted. The right panel shows all eight states as a grid, each cell coloured by its winning rule and hatched where there is a tie. Toggle rules on and off and watch the grid recolour. Try deleting R0. One cell goes blank, the all-false state. That is a first-time visitor with no quest done and no crime, and that player hears nothing at all. The other seven states still match a more specific rule, and the counter drops to Covered 7.

### Cross-game recognition

Rule matching rarely looks like a table of six rows. The skill is rewriting what you see into "conditions, then content, then pick the most specific match".

**Valve's response system (Source SDK 2013 code).** The public Source SDK 2013 contains `AI_ResponseSystem.cpp`, an ancestor of the system Ruskin described. Each rule has criteria. Each criterion that matches adds its weight to the rule's score (the default weight is 1, so an unweighted rule scores its number of matched criteria). A criterion marked `required` that fails drops the rule's score to zero. The system keeps every rule tied for the best score and picks one of them at random. So our model is this code with every criterion marked required and every weight left at 1. Weights are a way to say "this condition counts double", which is how a writer makes the thief rule beat the regular-customer rule without writing a combined line.

**Fallout: New Vegas (Obsidian, 2010).** Dialogue options can be tagged with a skill check, such as needing a certain Speech or Explosives value. The Fallout Wiki notes that New Vegas uses a fixed threshold rather than a dice roll. Your skill meets the minimum or it does not. The option still appears when you fail, but it is a weak, unconvincing line that fails the check. In rule form there are two rules on the same option. One has the condition `speech >= 50` and the convincing line. The other has no skill condition and the unconvincing line. The more specific rule wins whenever it matches. That is a fallback, written for comic effect.

**Disco Elysium (ZA/UM, 2019).** Passive checks inject extra lines into a conversation only if the relevant skill total (skill level plus modifiers plus 6, per the fan wiki) meets the check's difficulty. There are also "anti-passives", which appear only when the requirement is *not* met. In rule form, a passive is a rule with a numeric condition that adds a line rather than replacing one, and an anti-passive is the same rule with the comparison flipped. Disco Elysium's white and red checks add one more idea. A white check can be retried later after you improve the skill, so failure writes no permanent fact. A red check cannot be retried, so its result is written into state and read by later scenes. The designers chose, check by check, whether an event deserved a flag.

**Skyrim quest stages, again.** A line conditioned on `GetStage MS01 >= 30` is a rule with one numeric condition. Stages let a single integer replace a family of booleans (`reached_10`, `reached_20`, `reached_30`), which is exactly the collapse that CS102 week 11 recommended for the platformer heroine's four booleans.

Four systems, one model. When you meet a new dialogue tool, find where its facts live, what its conditions can test, and what it does when two lines both fit.

### Design judgment

Rule matching is not automatically better than a hand-built tree. Choose it on purpose.

- **Rules suit reactive, repeated, low-stakes lines.** Greetings, barks, shopkeeper banter, companion comments. There are many states, the player hears each line in passing, and a sensible fallback is always acceptable.
- **Trees suit authored, one-time, high-stakes scenes.** A confession or a betrayal has a shape, and the order of lines matters. You still read flags inside such a scene, but you gate the whole conversation, not each line.
- **Ties are information.** Keep ties visible in your tools. A random tie-break hides design questions. A priority system answers them once and forever, which is also its danger, because nobody revisits the answer.
- **Specificity is not importance.** "Most conditions wins" assumes the most specific line is the most relevant. The thief example shows it often is not. Weights or priorities let importance override specificity.
- **Testing grows with the state space, not the line count.** Six lines were easy to check against 8 states. Twenty lines against 12 flags means 4,096 states. Nobody playtests that by hand. You enumerate it in code, which is Lab 04.

## 3. Choosing the shape of a fact

The rule model works on any facts. Which facts you create decides how many bugs you ship.

### Booleans are cheap to add and expensive to combine

Every boolean doubles the state space. CS102 week 11 put a number on it: four booleans hold 16 combinations, and a heroine with 4 real states then has 12 impossible ones waiting to happen. Story flags do the same. Suppose the wolf quest has three booleans, `wolves_accepted`, `wolves_dead` and `wolves_rewarded`. That is 8 combinations, but only 4 are legal (none, accepted, accepted and dead, all three). The other 4, such as rewarded but not dead, should never occur. If a bug or an unusual path ever sets one, some rule will match it, and the player will hear a line that makes no sense.

### Stages collapse ordered flags

If the facts happen in a fixed order, replace them with one stage. `wolves = 0` (not started), `10` (accepted), `20` (wolves dead), `30` (rewarded). Now the state space has exactly the four legal values, and a condition like `wolves >= 20` reads naturally as "at least done with the fight". The gaps of 10 let you insert a step later (15 for "found the den") without renumbering every condition in the game. This is the Creation Kit convention for a reason.

The cost is the case Skyrim's two functions exist for. If the player can do steps in either order (find the den or talk to the hunter first), a single "highest stage" number loses information. Then you need separate facts, and you should list which combinations are legal.

### Counters remember how much

A counter answers questions booleans cannot. How often has the player visited? How many times did they lie to this character? ink gives every knot a read count for this reason. Counters let a line escalate ("You again. Third time today.") without three separate flags.

Counters bring their own traps. Decide whether they can go down. Decide their range. Decide whether a condition should test `== 3` (exactly the third visit, which fires once) or `>= 3` (every visit from the third on, which fires forever). Most "the NPC keeps saying it" bugs are an `==` that should have been `>=`, or the reverse.

### One writer per fact

A fact written from many places is a fact nobody can reason about. Keep a **fact table**, a list of every story fact in the game, and give each one:

| Field | Example |
|---|---|
| Name | `wolves` |
| Type and legal values | stage: 0, 10, 20, 30 |
| Who writes it | quest script `q_wolves` only |
| Who reads it | barkeep rules R2, R4, R5; mayor greeting; notice board |
| Can it go backwards? | no |

This table is also how you debug. When the barkeep says the wrong thing, you look up her rules, read the state, and run the model by hand, exactly as you did in section 2.

## 4. Where flags go wrong

Three failure patterns cover most state bugs in narrative games. Each has a cheap check.

### Uncovered states

A state where no rule matches produces silence, or in some engines a crash or a placeholder string. The fix is a fallback for every speaker and every context in which that speaker can be addressed. The check is mechanical. Enumerate the states and look for empty winner lists.

### Dead rules

A **dead rule** can never win. Either its conditions can never all be true together (`wolves == 10` and `wolves >= 20`), or it always ties with or loses to a more specific rule. Writers spend hours on lines no player will ever hear. The check is to run every state and count wins per rule. A rule with zero wins is dead.

This is the flag-aware version of the reachability search from CS102 week 8. There you searched the dialogue graph and ignored conditions, which gave an optimistic answer. Here you search the states and ignore the graph. Real tools combine the two by searching over (node, state) pairs, and the number of pairs is the number of nodes times the number of legal states. That product is why teams keep the number of facts small.

### Stale reads

A condition is evaluated at a moment. If the barkeep's greeting is chosen when you enter the inn, and you finish the wolf quest while standing in the inn (because the last wolf followed you in), she will greet you as a non-hero until you leave and re-enter. Decide when each rule is evaluated, and re-evaluate on the events that matter. Valve's system chooses at the moment a character is about to speak, which is one reason its lines feel current.

## In-class activity (25 minutes)

In pairs, write the rule set for a town guard who stands at the gate.

1. Choose exactly four facts. At least one must be a stage or a counter, not a boolean. Write the fact table (name, legal values, who writes it).
2. Write at most seven rules, one of which must be a fallback. Each line is at most one sentence.
3. Enumerate the states by hand or with the section 2 code (edit the lists). With a stage of four values and three booleans you have `4 × 2 × 2 × 2 = 32` states.
4. Mark every tie and every dead rule. Fix them with at most two changes (a new rule, a changed condition, or a priority).
5. Swap with another pair. Find one state where their guard says something the fiction does not support.

Expected output: the fact table, the rule table, the number of states, the number of ties and dead rules before and after your fixes, and the one bad state your partners found.

## Common misconceptions

- **"More flags means more reactive dialogue."** More flags means more states. Reactivity comes from lines, and you only notice lines that are chosen. A flag nobody reads is pure testing cost.
- **"A fallback line is a failure of writing."** The fallback is what keeps the system safe. Good writers make fallbacks warm and neutral, so they fit any state.
- **"The most specific line is always the best line."** Specificity counts conditions. Importance is a judgment. The thief tie in section 2 shows the two can disagree, which is why real systems add weights or priorities.
- **"If the graph search says a line is reachable, players will hear it."** Graph search ignores conditions. A line can be reachable in the graph and never win any state, or win only in states no player can reach.

## Check yourself

1. Add rule R6 with conditions `met` and `thief` and the line "You've got a nerve, coming back here." Recompute the eight-state table. How many ties remain, and in which state?
2. A barkeep has one fallback plus one rule per flag for `k` flags, and no other rules. How many states are there, and in how many of them is there a tie? Give the formula and the value for `k = 4`.
3. In Fallout: New Vegas's threshold model, a player has Speech 45 and the check needs 50. They read a skill magazine that adds 10. Rewrite the two rules on that option and say which one wins before and after reading.
4. A quest uses stages 0, 10, 20, 30, but a designer adds a branch where the player can reach stage 30 without passing 20. A rule tests `GetStage >= 20` to mean "the wolves are dead". What goes wrong, and what should the rule test instead?

<details>
<summary>Answers</summary>

1. The state (met, not wolves, thief) now has R6 at score 2 against R1 and R3 at score 1, so R6 wins and that tie is gone. The state (met, wolves, thief) now has R4, R5 and R6 all at score 2, a three-way tie. One tie remains, in the all-true state.
2. There are `2^k` states. A state with `j` true flags matches `j` single-flag rules plus the fallback. It ties whenever `j ≥ 2`. The number of states with at least two flags true is `2^k − 1 − k`. For `k = 4`, that is `16 − 1 − 4 = 11` tied states out of 16.
3. Rule A has condition `speech >= 50` and the convincing line. Rule B has no skill condition and the weak line. Before reading, only B matches, so the player sees the failing line. After reading, Speech is 55, both match, A scores higher and wins.
4. `GetStage` returns the highest stage completed, so a player on the new branch returns 30 even though stage 20 never happened. The rule fires and the NPC praises a wolf hunt that did not occur. The rule should test whether stage 20 itself was done (Skyrim's `GetStageDone` is exactly this), or the design should add a separate fact for the wolves.

</details>

## Lab / assignment hook

[Lab 04, rule-based dialogue checker](../labs/lab04.md). You implement the matcher from section 2, extend it to numeric conditions and multi-valued facts, and write a checker that enumerates every state and reports uncovered states, ties and dead rules. Then you write a rule set for an NPC of your own that passes the checker cleanly. The rule set feeds the dialogue-exercise portion of the course assessment.

## Sources

- Ruskin, E. (2012). "AI-driven Dynamic Dialog through Fuzzy Pattern Matching. Empower Your Writers!" GDC 2012, Valve. GDC Vault session page (gdcvault.com/play/1015528). Description of matching world facts against a large line database and cascading from special to general cases; Left 4 Dead named as a user.
- Valve, Source SDK 2013, `src/game/server/AI_ResponseSystem.cpp` (github.com/ValveSoftware/source-sdk-2013, master branch, read September 2026). `ScoreCriteriaAgainstRule` sums weights of matched criteria (default 1), a failed `required` criterion zeroes the rule, and `FindBestMatchingRule` picks randomly among tied best rules.
- Warcraft Wiki, "API C_QuestLog.IsQuestFlaggedCompleted" (retail API, moved to `C_QuestLog` in patch 8.2.5, boolean return since patch 6.0.2). Example uses quest 176.
- UESP Creation Kit Wiki, "GetStage" (Skyrim Creation Kit, 2011). Returns the highest completed stage; `GetStageDone` for a specific stage.
- inkle, *Writing with Ink*, Part One section 7 (conditional choices; knot and stitch labels are read counts). github.com/inkle/ink, `Documentation/WritingWithInk.md`.
- Fallout Wiki, "Fallout: New Vegas skills" (2010 release). Score-based rather than probability-based dialogue skill checks; failing options shown with an unconvincing response; skill magazines give +10 (+20 with Comprehension).
- Disco Elysium Wiki, "Skills" (2019 release and The Final Cut). Passive checks use skill level plus modifiers plus 6; anti-passives; white checks retryable, red checks not.
- Bateman, C. (ed.) (2021). *Game Writing: Narrative Skills for Videogames*, 2nd ed. Bloomsbury Academic.

## Interactive spec: examples/w04-rule-matcher.html

**Purpose.** Make visible that a handful of rules plus a fallback covers every state, and that the states where many flags are true are where ties collect.

**Layout.** Two linked panels, stacked on mobile, side by side from 900px.

- **Left panel, "Right now".** Three toggle switches for `met`, `wolves_dead`, `thief` (keyboard: Tab to focus, Space to toggle). Below them, the rule table from section 2: one row per rule with an enable checkbox, its conditions as chips, its score, and a status (matches / does not match). The winning row is highlighted in the accent colour. If there is a tie, all tied rows get a hatched highlight and a label "TIE: n rules". Above the table, the chosen line in a speech bubble (for a tie, show "Tie between R4 and R5" and both lines, greyed). Show the numeric state, e.g. `state = (met: T, wolves: T, thief: F)`.
- **Right panel, "Every state".** A grid of all `2^k` states. With 3 flags, a 2 × 4 grid; each cell shows the state as three letters (e.g. `M W -`) and the winning rule ID. Fill colour per rule from the shared palette (6 categorical colours, R0 in neutral grey). Tied cells are hatched with both colours. Cells with no match are white with a red border and the text "silent". The cell matching the left panel's current state has a thick outline. Clicking a cell (or Enter on a focused cell) sets the left panel's toggles to that state.
- **Counters under the grid.** "States: 8 · Covered: 8 · Ties: 2 · Dead rules: none". A rule is dead if it wins no state (ties count as a shared win, so a rule that only ever ties is listed as "only ties").

**Controls.**
1. The three flag toggles.
2. Per-rule enable checkboxes.
3. A button "Add R6 (met + thief)" that appends rule R6 with conditions `met`, `thief` and line "You've got a nerve, coming back here." Pressing again removes it.
4. A tie-break selector with three options: "Show ties" (default), "Random (Valve style)", "Priority: later rule wins". In random mode the grid shows a tied cell's colour flickering between the tied rules once per second (disabled under `prefers-reduced-motion`; show both colours statically instead). In priority mode ties resolve to the highest-numbered rule, and the counter says "Ties: 0 (resolved by priority)".
5. A toggle "Add fourth flag: `paid_debt`". This doubles the grid to 16 cells (4 × 4) with no new rules, so the student sees the state count double while every cell stays covered by existing rules.

**The one insight.** Deleting R0 immediately creates a silent cell (the all-false state), and the hatched tie cells sit in the rows where two or more flags are true.

**Exact test values** (3 flags, R0 to R5 enabled, "Show ties"):

| met | wolves_dead | thief | Winner |
|---|---|---|---|
| F | F | F | R0 |
| F | F | T | R3 |
| F | T | F | R2 |
| F | T | T | R5 |
| T | F | F | R1 |
| T | F | T | tie R1, R3 |
| T | T | F | R4 |
| T | T | T | tie R4, R5 |

- Counters: States 8, Covered 8, Ties 2, Dead rules none.
- With R6 added: (T, F, T) → R6; (T, T, T) → tie R4, R5, R6; Ties 1.
- With R0 disabled: (F, F, F) is silent; every other state unchanged; Covered 7.
- With the fourth flag on (and R6 off): States 16, Covered 16, Ties 4. No rule reads `paid_debt`, so each of the 8 original states appears twice with the same winner, and the 2 tied states become 4. Compute all counters from the model; do not hard-code them.
- Scoring: `score = number of conditions`; a rule matches only if every condition holds.

**Accessibility.** All toggles are native checkboxes or buttons with labels. The grid is a table of buttons with `aria-label` like "met true, wolves false, thief true: tie between R1 and R3". Colour is never the only signal (rule IDs are printed in each cell; hatching plus the word "tie").
