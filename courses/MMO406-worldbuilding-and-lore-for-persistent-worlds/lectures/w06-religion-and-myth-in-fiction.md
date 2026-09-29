# MMO406 · Week 06 — Religion and Myth in Fiction

**Why this matters:** Every culture in your world tells a story about where the world came from, and most of those stories should disagree. Disagreement is what makes a mythology feel like it belongs to people rather than to a design document. But an MMO has players who will compare every account on a wiki within a week. This week you learn to plan how much truth survives in your myths, so the dedicated readers can dig it out and the casual ones still get a clear story.

**You will be able to:**
- Compute the share of a myth's core facts that end up settled, contested but answerable, or unrecoverable, from the number of in-world accounts and how often each one tells the truth or distorts it.
- Explain why adding more accounts can reduce the number of settled facts, and why copied accounts can manufacture a false consensus.
- Place a game's religion on a ladder of mechanical presence (flavour, system hooks, belief that acts, absent gods) and predict the design problems of each rung.
- Write a pantheon and a myth as a set of in-world accounts backed by a hidden fact matrix.

**Before class:** Wolf, *Building Imaginary Worlds* (2012), chapter 3, the part on mythology and philosophy (about 8 pages; use the contents page). UESP, "Lore:The Monomyth" (the introduction and the first two sections, 15 minutes; note how the book frames the split between human and elven views). Wikipedia, "Criterion of multiple attestation" (the description section, 5 minutes).

**Prerequisites from earlier courses:** [MA102 week 6, the binomial distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w06-binomial-crits-over-a-fight.md) gives the "k tries, chance p each" counting that this week uses without re-deriving. [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md). [GD202 week 10, lore delivery without walls of text](../../GD202-narrative-and-quest-design/lectures/w10-lore-delivery-without-walls-of-text.md) sorted lore into need to know, nice to know and for the fans; this week's model is about the for-the-fans tier. [GS101 week 14, games and representation](../../GS101-history-and-critical-study-of-games/lectures/w14-games-and-representation.md) is the background for section 4's advice on real religions. From this course, [week 4](w04-history-and-timelines.md) put myth at the deep end of the precision gradient, and [week 5](w05-cultures-languages-names.md) asked what each culture holds sacred.

**Interactive:** [examples/w06-myth-triangulation.html](../examples/w06-myth-triangulation.html). Keep it open during section 2.

---

## 1. What myth does in a setting

A **religion** in a setting is a culture's organized relationship with what it treats as sacred: gods, spirits, ancestors, a river. A **myth** is a sacred story a culture tells, usually about origins: how the world began, why people die, why the moons move. Myths are told inside the world by particular people for particular reasons.

Religion and myth do real work for an MMO.

- **They explain the world's rules.** Why magic exists, why the dead rise in one valley, why a mountain is forbidden. A myth turns a design constraint into a belief the characters hold.
- **They make factions.** Two churches with rival readings of one god are a faction conflict with built-in dialogue. Week 3's factions often need a religious fault line.
- **They make content.** Temples, pilgrim roads, relics, heresies, festivals, clergy with quests. A religion is a production list, as a history is (week 4).
- **They hold mystery.** Myths are the one place in your setting where contradiction is not a continuity error. That makes them the natural home for questions you want players to argue about for years.

The last job needs a distinction. Behind every set of myths, you as the designer should know what actually happened. Call that the **canon ledger**, a private list of the true facts about the event the myths describe. The myths are **accounts** of those facts, each told by a culture that keeps some, bends some and forgets some. Players never see the ledger. They see the accounts, and the most dedicated of them try to reconstruct the ledger by comparing accounts.

Whether they can succeed is something you can plan.

## 2. Worked example: the truth under the myths

### The hook

The Elder Scrolls series has a god who appears in every Tamrielic mythic tradition under a different name and with a different verdict. UESP lists him as Lorkhan to the elves, Shor in Skyrim, Shezarr in Cyrodiil and Sep in Hammerfell. In most traditions he persuaded or tricked the other divine spirits into making the mortal world. Whether that was a gift or a crime depends on who is telling it. The in-game book *The Monomyth*, which appears in Morrowind, Skyrim and The Elder Scrolls Online, lays out these accounts side by side. It frames the difference as a split in how humans and elves see their relationship to the divine, and it does not declare a winner.

Players have compared these accounts for more than twenty years. Some facts are treated as settled because account after account agrees on them. Others are argued about endlessly. That split did not happen by accident, and you can predict its shape.

### The model

Your canon ledger holds `F` core facts about one mythic event. You will write `k` in-world accounts of it, one per culture, book or shrine. For each fact, each account does one of three things:

- tells the **true** version, with chance `p`;
- tells a **distorted** version, with chance `q`;
- stays **silent** about it, with chance `1 − p − q`.

Assume the accounts are independent and that each distortion is unique to its account, so two cultures never distort a fact the same way. A player who compares accounts treats a version as confirmed when at least two accounts tell it. Only the true version can be told twice, so every fact falls into one of three outcomes:

```
unrecoverable   fewer than 2 accounts tell the truth
                U = (1 − p)^k + k × p × (1 − p)^(k−1)
settled         2+ tell the truth and none distorts
                S = (1 − q)^k − s^k − k × p × s^(k−1),   where s = 1 − p − q
answerable      2+ tell the truth and 1+ distorts (a mystery with an answer)
                A = 1 − U − S
```

- `U` is the binomial chance of zero or one true tellings in `k` tries (MA102 week 6).
- `S` counts the ways to have no distortion at all, `(1 − q)^k`, and removes those with fewer than two true tellings.
- `A` is the rest. These are the facts the fans can argue about and still solve.

A reader of a single account is in a different position. They see a share `p + q` of the facts stated, and a share `p / (p + q)` of those are true, with no way to tell which. With `p = 0.4` and `q = 0.2`, one account states 60% of the facts, and a third of what it states is wrong.

### Numbers you can check

Take `p = 0.4` and `q = 0.2`. For `k = 3`, check `A` by hand. The only way to have two or more true tellings and at least one distortion in three accounts is exactly two true and one distorted, `3 × 0.4² × 0.2 = 0.096`.

This script prints the whole table. It runs as shown with `.venv/bin/python`.

```python
def myth_outcomes(k, p, q):
    """Shares of core facts that end up settled, answerable-but-contested, or lost."""
    s = 1 - p - q                                          # an account stays silent
    lost = (1 - p) ** k + k * p * (1 - p) ** (k - 1)       # fewer than 2 true tellings
    settled = (1 - q) ** k - s ** k - k * p * s ** (k - 1)  # 2+ true, no distortion
    mystery = max(0.0, 1 - lost - settled)                 # 2+ true and 1+ distortion
    return settled, mystery, lost

print(" k  settled  mystery  lost")
for k in range(1, 7):
    settled, mystery, lost = myth_outcomes(k, p=0.4, q=0.2)
    print(f"{k:2}  {settled:7.1%}  {mystery:7.1%}  {lost:5.1%}")
```

```
 k  settled  mystery  lost
 1     0.0%     0.0%  100.0%
 2    16.0%     0.0%  84.0%
 3    25.6%     9.6%  64.8%
 4    28.2%    24.3%  47.5%
 5    26.6%    39.7%  33.7%
 6    23.3%    53.3%  23.3%
```

(The `max(0.0, ...)` only stops floating-point round-off from printing −0.0 in the first two rows.)

With twenty core facts and four accounts, you can expect about 5.6 settled facts, 4.9 answerable mysteries and 9.5 facts that nobody can recover.

### What the table says

Three things stand out.

First, **writing accounts independently loses most of the truth**. With four accounts nearly half the ledger is unrecoverable. If you wanted the fans to be able to reconstruct the creation myth, four independently written accounts are not enough.

Second, **settled facts peak and then fall**. Going from four to six accounts lowers the settled share from 28.2% to 23.3%. Every new account is another chance to distort a fact that was settled. More sources create more argument, not only more certainty.

Third, **mysteries grow fastest**. From three to six accounts, the answerable share goes from 9.6% to 53.3%. If you want a mythology that sustains community debate with real answers underneath, many accounts with modest distortion is the recipe.

### A visual you can move

Open [`examples/w06-myth-triangulation.html`](../examples/w06-myth-triangulation.html). The left view, "One reader", shows a single account as a column of twenty facts, each cell marked stated or silent, with no indication of which statements are true. It looks confident. The right view, "The community", shows all `k` accounts side by side as a grid, with the truth revealed. Rows with two or more true cells are outlined, green if no cell distorts and amber if one does. Rows that stay grey are unrecoverable. A stacked bar underneath gives the exact `S`, `A` and `U` from the formulas. Drag `k` from 2 to 6 and watch green rows turn amber. Then switch on "one account copies another" and see what happens to rows where the copied account lied.

### Cross-game recognition

**The Elder Scrolls (Morrowind 2002 to ESO, 2014 onward).** Lorkhan's story is told by many cultures, and *The Monomyth* collects several of them. In our terms `k` is large, since almost every culture has a version, and `q` is high on the question of whether the creation was a gift or a trap. The facts that recur across accounts (that a missing god drove the making of the mortal world, and that he is now absent from the pantheon) behave like settled facts. The verdict behaves like an answerable mystery at best, and the series seems content to leave it unrecoverable.

**Final Fantasy XIV (A Realm Reborn to Endwalker).** Eorzea's pantheon, the Twelve, is worshipped across the realm, with city-states choosing patron deities and many Seekers of the Sun following Azeyma. The Myths of the Realm alliance raid series, released during the Endwalker patches, explores what the Twelve actually are. That is the ledger being opened in play. The in-world accounts built the expectation, and the raid series is the team choosing, years later, which answerable mysteries to answer. Designers of long-running games need to plan for that moment. A mystery with no ledger behind it cannot be answered without a retcon (week 11).

**Historians and the criterion of multiple attestation.** Biblical scholars judge whether a saying or event is historical partly by how many independent sources report it. The criterion comes from F. C. Burkitt in 1906. Its key word is *independent*. The Wikipedia article's example is that Matthew and Luke probably depend on Mark, so agreement among the three does not count as three witnesses. That is our model's independence assumption, from a field that has used it for over a century.

Three contexts, one idea. A truth becomes recoverable when enough independent tellers keep it, and a mystery is a fact that enough tellers keep and at least one bends.

### Eyes-open design judgment

- **Don't leave it to chance.** The model shows what happens when writers produce accounts separately. In your bible, use it as a budget, then author deliberately. Keep a fact matrix (facts as rows, accounts as columns) and place each core fact in at least two accounts on purpose. The lab has you do exactly this.
- **Decide which facts are allowed to be lost.** Some facts should be unrecoverable forever, because a myth with every answer available is a textbook. Mark them in the ledger as such, and do not let a later writer "reveal" them casually.
- **Watch for copying.** If one culture's scripture is a translation of another's, the two are one witness, not two. Worse, a distortion in the original appears twice and passes the two-account test. A copied pair creates false consensus on every fact the original distorted. That can be a great plot device if you plan it, and an embarrassment if you don't.
- **Protect the casual player.** The single-reader view is what most players see. Make sure each account is a good story on its own, with its own voice, even though a third of what it states is false. GD202 week 10's need-to-know tier should never depend on triangulation.

## 3. Gods with mechanical teeth

The worked example treats religion as text. In an MMO, religion can also be a system. It helps to place a game's religion on a ladder of **mechanical presence**, from gods who are only believed in to gods who act.

| Rung | What religion does in play | Example |
|---|---|---|
| 0. Flavour | A choice or label with no mechanical effect | FFXIV's patron deity at character creation, since patch 4.2 |
| 1. System hooks | Belief changes faction, access or items | EverQuest's deity choice (classic era) |
| 2. Belief that acts | Worship makes things happen in the world | FFXIV's primals |
| Side rung: absent gods | Gods existed and left, so belief refers to the past | Guild Wars 2's Exodus |

**Rung 0.** Final Fantasy XIV asks you to choose a nameday and a patron deity when you create a character. Older guides describe elemental resistances attached to each deity. The game's community wiki notes that this effect was removed, and that the choice has had no stat effect since patch 4.2 (2018). The design moved religion down the ladder on purpose. It is now pure identity, which spares players from feeling pushed to pick the "right" god.

**Rung 1.** EverQuest in its classic era (1999 to 2001, as preserved by the Project 1999 community) offered sixteen deities plus agnostic at character creation. Which ones you could choose depended on your race and class. Your deity helped set your starting faction standings, and some items could only be used by followers of particular deities. Belief here is a permanent build choice with social consequences. A follower of a hated god finds certain guards hostile. That is powerful for identity and roleplay, and it also means a new player makes a permanent decision before understanding it.

**Rung 2.** In Final Fantasy XIV the beast tribes summon primals, beings they worship as gods, by combining crystals with the aether of their faith and prayer. A primal, once summoned, can bend the minds of those nearby into devoted servants. Here belief literally creates a boss. The design is elegant, because the religion explains why the same enemy can be fought again (the tribe keeps praying) and why primals keep coming back as trials. It also raises a question every rung-2 design must answer. If faith has power, why don't the player's own gods act?

**Absent gods.** Guild Wars 2's main calendar counts from the Exodus, the moment the gods left Tyria (week 4). Absent gods are a common answer to the **active god problem**. If the gods are real, powerful and on your side, why do they need a hero? Designers handle it by making gods absent, limited, dependent on belief, bound by rules, or divided among themselves. Pick one on purpose, write it in the ledger, and apply it to every expansion. The problem gets worse over time. Every expansion villain is a new occasion for players to ask where the gods are.

## 4. Writing a pantheon and its myths

A workable process, which the lab follows:

1. **Write the ledger first.** Ten to twenty true facts about the origin event, in plain sentences, including which ones must stay unrecoverable.
2. **Write the pantheon.** For each god: domain, what they want, whom they favour, and their rung on the mechanical ladder. Gods who want things make better stories than gods who represent things.
3. **Write the tellers.** For each account: which culture, which institution (priests, poets, heretics), for which audience, and what it gains from its version. A distortion should always serve the teller. The elves in *The Monomyth* have a reason to describe the mortal world as a loss.
4. **Fill the fact matrix.** Mark each cell true, distorted or silent. Check that settled, answerable and unrecoverable facts land where you want them.
5. **Write the accounts.** Each in its own voice, as a book, a hymn, a shrine inscription or a quest-giver's story.

**On real religions.** Fictional religions often borrow from real ones: a sun-god church with cathedral architecture, a monastic order with borrowed ritual. Players will recognize the source. Borrowing structure (hierarchies, calendars, pilgrimage) is usually safe. Borrowing the specific sacred figures, texts or symbols of a living faith and making them villains or jokes is not, and it will be read as a statement about that faith. GS101 week 14 covers representation in general. For religion, the practical rule is that anything recognizably sacred to real players needs the same review you would give a real-world ethnic reference.

## In-class activity (25 minutes)

In groups of three, you inherit a creation myth with a ledger of 12 core facts and are told to write accounts for three cultures.

1. Decide a target: how many of the 12 facts should be settled, answerable and unrecoverable after release? Justify the split in two sentences.
2. Using the interactive, find values of `k`, `p` and `q` that give roughly that split in expectation. Note how far the result is from your target.
3. Now abandon chance. On paper, fill a 12 × 3 fact matrix (T, D or blank) that hits your target exactly. Check each row against the definitions.
4. For one distorted cell, write one sentence saying why that culture tells it that way.

Expected output: the target split, the parameter values and their expected split, the filled matrix, and one motive sentence. Swap matrices with another group and count their settled, answerable and unrecoverable rows without looking at their target.

## Common misconceptions

- **"More sources always means more certainty."** Settled facts peak and then fall as accounts are added, because each new account is another chance to distort. More sources mean more answerable arguments.
- **"If two accounts agree, it's true."** Only if they are independent. A copied account repeats its source's distortions and manufactures false agreement.
- **"Contradictory myths are continuity errors."** Inside myths, contradiction is the point. The error is a contradiction with no ledger behind it, because it can never be resolved without a retcon.
- **"Mechanical religion is always richer."** Each rung adds a problem. System hooks make belief a build decision. Belief that acts raises the active god problem. FFXIV removed its deity stat effects for a reason.

## Check yourself

1. With `p = 0.5`, `q = 0.1` and `k = 2`, what shares of facts are settled, answerable and unrecoverable?
2. With `p = 0.4`, `q = 0.2`, how many of 20 core facts do you expect to be unrecoverable with three accounts? How many accounts do you need before fewer than a quarter are unrecoverable?
3. A reader has only one account, with `p = 0.3` and `q = 0.3`. What share of the facts does it state, and what share of its statements are true?
4. Two of your four accounts are a scripture and its translation. For a fact where the original distorts (chance `q = 0.2`), what does the community see? Roughly what share of all facts gets a false version that looks confirmed?
5. Your game's primary villain for the next expansion is a demon that threatens the world. Your gods are real and on rung 2. Write two sentences that answer the active god problem for this expansion, and name the rung-2 rule you are relying on.

<details>
<summary>Answers</summary>

1. With two accounts, a fact is settled only if both tell the truth, `0.5² = 25%`. Answerable needs two true tellings and a distortion, impossible with `k = 2`, so 0%. Unrecoverable is `1 − 0.25 = 75%`.
2. `U(3) = 0.648`, so about 13 of 20 facts. The table shows `U(5) = 33.7%` and `U(6) = 23.3%`, so six accounts.
3. It states `p + q = 60%` of the facts, and `0.3 / 0.6 = 50%` of its statements are true.
4. The translation repeats the distortion, so the false version appears in two accounts and passes the two-account test. The fact looks settled or contested in the wrong direction. Roughly `q = 20%` of all facts get such a false confirmation, unless a third account tells the truth often enough to contest it.
5. For example: "The gods draw power from prayer, and the demon's first act is to burn the three great temples, so the gods are weakened exactly when they are needed. Restoring the pilgrim roads is how the player restores the gods." The rule relied on is that divine power depends on worship. Any answer that names a limiting rule from the ledger works.

</details>

## Lab / assignment hook

[Lab 06, a pantheon, a ledger and four accounts](../labs/lab06.md). You implement the outcome model and a checker for fact matrices, then write a pantheon, a canon ledger and four in-world accounts for your own world, with a matrix that hits a target split. The pantheon and myths become the religion chapter of your world bible.

## Sources

- UESP, "Lore:Lorkhan" (accessed September 2026). Present in every Tamrielic mythic tradition; names Lorkhan, Shor (Skyrim), Shezarr (Cyrodiil), Sep (Hammerfell); he convinced or contrived the Original Spirits to create the mortal world.
- UESP, "Lore:The Monomyth" (accessed September 2026). In-game book in *Morrowind*, *Skyrim* and *The Elder Scrolls Online*; frames the human and Aldmeri (elven) schism as a difference in the mortal's relationship to the divine; presents several cultural accounts.
- Wikipedia, "Criterion of multiple attestation" (accessed September 2026). Independent sources; Burkitt 1906; Matthew and Luke likely dependent on Mark.
- Final Fantasy XIV Online Wiki (consolegameswiki), "Character creation" (accessed September 2026). Patron deity choice has had no stat effect since patch 4.2; elemental resistances removed.
- Final Fantasy XIV Online Wiki, "Primals" (accessed September 2026). Primals summoned by beast tribes from crystals and the aether of faith and prayer; tempering, which makes followers into devoted servants.
- Final Fantasy XIV Online Wiki, "The Twelve" (accessed September 2026). Twelve worship, city-state patron deities, Seekers of the Sun and Azeyma; Myths of the Realm alliance raids explore the Twelve's nature (Endwalker patches).
- Project 1999 Wiki, "Deities" and "Faction" (classic EverQuest, 1999-2001 content, accessed September 2026). Sixteen deities plus agnostic, availability by race and class, deity-specific items; starting faction standings depend on race, class and deity.
- Guild Wars 2 Wiki, "Mouvelian calendar" (accessed September 2026). The calendar counts from the Exodus, when the gods left Tyria.
- Wolf, M. J. P. (2012). *Building Imaginary Worlds: The Theory and History of Subcreation*. Routledge. Chapter 3.

## Interactive spec: examples/w06-myth-triangulation.html

**The one insight.** A single myth looks complete and confident, but the truth is only recoverable where two independent accounts agree. As accounts are added, settled facts peak and then turn into contested-but-answerable mysteries, and a copied account quietly manufactures agreement on falsehoods.

**Model.**

```
s = 1 − p − q
U = (1 − p)^k + k p (1 − p)^(k−1)              unrecoverable
S = (1 − q)^k − s^k − k p s^(k−1)              settled
A = 1 − U − S                                  answerable (clamp tiny negatives to 0)
single reader: stated share p + q, true share of statements p / (p + q)
```

**Default state.** `F = 20` facts, `k = 4`, `p = 0.40`, `q = 0.20`, copying off, seed 1.

**Layout: two linked views plus a bar.**

1. *One reader* (left, or top on mobile). One column of 20 cells for account 1 (selectable with a small account picker). Stated cells are filled in a single neutral colour, silent cells empty. No truth shown. Caption with the single-reader numbers: "states 60% of facts; 67% of what it states is true, and you can't tell which."
2. *The community* (right, or below). A 20-row by `k`-column grid. Cells coloured true (accent), distorted (warning colour, each with a small distinct glyph so distortions visibly differ), silent (empty). Each row gets an outline. Green when 2+ true and no distortion. Amber when 2+ true and 1+ distortion. Grey otherwise. With copying on, one account (the last) is drawn as a copy of account 1. Its cells duplicate account 1's cells, and rows where the duplicated cell is a distortion get a red "false consensus" outline.
3. *Outcome bar* (full width). A stacked horizontal bar with the exact `S`, `A`, `U` from the formulas (labelled to one decimal percent), and beneath it the counts observed in the sampled grid ("this sample: 6 settled, 5 answerable, 9 unrecoverable").

**Sampling rule.** For each row and account, draw `u` uniform in [0, 1) from a seeded generator (for example mulberry32). If `u < p` the cell is true. If `u < p + q` it is distorted. Otherwise it is silent. A "reroll" button advances the seed.

**Controls.**
- Slider `k`, 1 to 8.
- Slider `p`, 0 to 1, step 0.05; slider `q`, 0 to 1, step 0.05, constrained so `p + q ≤ 1` (moving one past the limit pushes the other down).
- Slider `F`, 5 to 40 (grid rows).
- Toggle "one account copies another". When on, the formula bar also shows the approximate false-consensus share, `q`, for rows where the copy and its source both distort.
- Button "reroll"; all controls keyboard accessible with visible values.

**Test values (formula bar, `p = 0.4`, `q = 0.2`).**

| k | Settled | Answerable | Unrecoverable |
|---|---|---|---|
| 2 | 16.0% | 0.0% | 84.0% |
| 3 | 25.6% | 9.6% | 64.8% |
| 4 | 28.2% | 24.3% | 47.5% |
| 5 | 26.6% | 39.7% | 33.7% |
| 6 | 23.3% | 53.3% | 23.3% |

Also: `p = 0.5, q = 0.1, k = 2` gives 25.0%, 0.0%, 75.0%. `p = 0.3, q = 0.3` single reader gives 60% stated, 50% true.

**Visual notes.** First screen at the defaults so the confident single column and the half-grey community grid appear together. Use the shared palette tokens and never rely on colour alone (outlines also carry a letter: S, A, U, or F for false consensus). No game names, logos or art in the graphic.
