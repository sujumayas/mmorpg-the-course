# MMO406 · Week 08 — Player Agency vs Canon

**Why this matters:** Your players make choices, and your next expansion has to be written for all of them at once. Each time you declare one outcome "what really happened," you tell some players that their story didn't happen. A single choice looks harmless. A few in a row can leave almost nobody whose story matches the world. This week gives you the number that shows it, and a short list of ways to spend a limited writing budget on the choices that hurt most.

**You will be able to:**
- Compute a canon's fit (the share of players whose own choices all match it) and the distribution of contradictions per player, from the take rates of the canonized options.
- Show that honoring the choices with the most even splits raises fit the most, and pick which choices to honor under a budget.
- Classify a shipped game's handling of past choices as honor, canonize, absorb, reconcile or delegate, and predict what each costs.
- Design a canon policy for a setting bible, stating which choices are world canon, which are personal canon, and how later content refers to each.

**Before class:** Wolf, *Building Imaginary Worlds* (2012), chapter 7, "Circles of Authorship," the parts on canon (use the contents page, about 15 pages). The Unofficial Elder Scrolls Pages, "Lore:Warp in the West" (10 minutes). Reread [GD202 week 2](../../GD202-narrative-and-quest-design/lectures/w02-the-player-as-co-author.md), section 2, on the price of acknowledging a choice.

**Prerequisites from earlier courses:** [GD202 week 2, the player as co-author](../../GD202-narrative-and-quest-design/lectures/w02-the-player-as-co-author.md) (what it costs to acknowledge a choice once). [GD202 week 3, branching structures](../../GD202-narrative-and-quest-design/lectures/w03-branching-structures-and-the-combinatorial-explosion.md) (why branches that never close are unaffordable). [GD202 week 13, shared vs personal story](../../GD202-narrative-and-quest-design/lectures/w13-shared-vs-personal-story.md) (the visible share `V` and the consequence budget; we assume you know both). [MMO308 week 11, community-voted design](../../MMO308-live-operations-analytics-and-experimentation/lectures/w11-community-voted-design-old-school-runescape-polls.md) (vote thresholds, which this week does not repeat). Last week's [lore delivery in MMOs](w07-lore-delivery-in-mmos.md) (knowledge share and permanence).

**Interactive:** [examples/w08-canon-fit.html](../examples/w08-canon-fit.html). Keep it open during section 2.

---

## 1. Two kinds of truth in a persistent world

A persistent world holds two kinds of truth at once.

**World canon** is what is true for everyone. The capital burned. The old king is dead. The rift opened in the northern sea. Every player's future content is built on it, and every new player inherits it.

**Personal canon** is what is true for one character. You spared the smuggler. You sided with the guild. You are a member of the old order. It lives in flags on your character, in your dialogue history and, if the team can afford it, in phased versions of the world (the costs of which GD202 week 13 measured with `V`).

The conflict between **player agency** (the player's power to shape the story) and canon appears at one moment. A later piece of content needs a personal-canon fact to be a world-canon fact. The expansion's villain is the smuggler you spared, or you didn't. The guild you sided with is now in power, or it isn't. At that moment the writer has to pick. Either the content splits by the player's choice, or the world decides for everyone.

In a single-player series the moment comes once per sequel. In an MMO it comes every patch, for choices made by millions of characters, over years. A **canon policy** is your standing answer to it. This lecture builds the number that tells you when your policy is hurting players, and the five answers games use.

### Five answers

Every shipped game uses some mix of these.

- **Honor.** Later content checks the player's choice and plays a different version. Cost: variant content, paid every time the choice is referenced.
- **Canonize.** The world picks one option. Players who chose otherwise are contradicted. Cost: those players' sense that their choice mattered.
- **Absorb.** Later content is written so that it doesn't depend on the choice. The smuggler left the region either way. Cost: the choice stops having consequences, and players notice if you do it too often.
- **Reconcile.** The world declares that every option somehow happened. Cost: a strain on the world's logic, and usually an in-world device to explain it.
- **Delegate.** The players collectively pick, and the result becomes world canon. Cost: the losing side is contradicted by design, and the vote has to be run well (MMO308 week 11).

## 2. Worked example: the canon that fits almost nobody

### The hook

The Elder Scrolls II: Daggerfall (Bethesda, 1996) ended its main quest in one of several ways, depending on which faction the player gave control of an ancient war machine to. The Unofficial Elder Scrolls Pages list seven possible outcomes. The sequels still had to say what happened next in the region. The lore writers did not pick the most popular ending. Instead they wrote that every ending happened at the same time, in a reality-warping event known as the Warp in the West (dated 3E 417 in the setting's calendar). The same world is now the setting of The Elder Scrolls Online.

Star Wars: The Old Republic launched in 2011 with eight separate class stories, four per faction, each with its own three-act storyline and choices. Its 2015 expansion, Knights of the Fallen Empire (27 October 2015), merged all eight into one storyline in which every player character becomes the Outlander.

Why would a studio invent a reality-breaking event instead of picking the most popular ending? And why merge eight stories into one? Surely if you pick the majority option every time, most players agree with the canon.

### The model

A later piece of content depends on `n` past choices. For each choice `i`, the canon picks one option. Call the share of players who chose that option its **take rate** `p_i`. A **canonized** choice contradicts the `1 − p_i` players who chose otherwise. An honored, absorbed or reconciled choice contradicts nobody, so it contributes a factor of 1.

Assume players make the choices independently of each other. Then:

```
fit                      F = p_1 × p_2 × … × p_n           (canonized choices only)
expected contradictions  E = (1 − p_1) + (1 − p_2) + … + (1 − p_n)
per-choice agreement     p_i, one number per choice
```

- **Fit** `F` is the share of players whose own choices match the canon on every canonized choice. These are the players for whom the new content fully "remembers" their story.
- `E` is the average number of canonized choices on which a player is contradicted.
- The full distribution, the chance that a player is contradicted exactly `k` times, is the **Poisson binomial distribution**: the count of successes in independent trials with different probabilities. MA102 covered the binomial, where every trial has the same probability. Here each choice has its own `1 − p_i`, and you compute the distribution one choice at a time.

The independence assumption matters, and section 3 returns to it. For now, notice the two views the model gives you. The **per-choice view** is a list of `p_i`, each usually above 50% if you canonize majorities. The **per-player view** is `F`, a product, and products of numbers below 1 shrink fast.

### Numbers you can check

An expansion depends on five choices from the launch story. The team canonizes the most popular option each time. Telemetry gives the take rates.

| Choice | Canon option take rate `p_i` | Players contradicted `1 − p_i` |
|---|---|---|
| Spare or execute the smuggler | 0.90 | 10% |
| Join the guild or the watch | 0.75 | 25% |
| Burn or keep the letters | 0.60 | 40% |
| Trust the envoy or not | 0.55 | 45% |
| Free the prisoner or not | 0.50 | 50% |

In the per-choice view this looks fine. Every canon option is a majority or a tie. Average agreement is 66%.

Now the per-player view.

```
F = 0.90 × 0.75 × 0.60 × 0.55 × 0.50 = 0.111
E = 0.10 + 0.25 + 0.40 + 0.45 + 0.50 = 1.70
```

Only 11.1% of players have a history that the expansion fully matches. The average player is contradicted on 1.7 of the five choices. The full distribution:

| Contradictions `k` | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| Share of players | 11.1% | 32.6% | 35.3% | 17.1% | 3.5% | 0.2% |

The most common experience is being contradicted twice. Majority canon, applied choice by choice, produced a world that almost nobody's story fits.

That is the answer to the hook. Daggerfall had one choice with seven outcomes. Even if one ending had been chosen by 30% of players, picking it contradicts 70%. Reconciling made every ending's `p` equal to 1 in the model, and bought that with a strange event in the world's history. The Old Republic's eight class stories held thousands of personal choices. Merging them into one story going forward is closer to absorbing: the new story is written so that most old choices don't need to be true or false in it.

The code below reproduces both tables.

```python
from math import prod

def distribution(ps):
    """P(a player is contradicted on exactly k canonized choices), k = 0..n."""
    d = [1.0]
    for p in ps:
        d = [a * p + b * (1 - p) for a, b in zip(d + [0.0], [0.0] + d)]
    return d

ps = [0.90, 0.75, 0.60, 0.55, 0.50]
print(f"fit {prod(ps):.3f}  expected contradictions {sum(1 - p for p in ps):.2f}")
print(" ".join(f"{k}:{100 * x:.1f}%" for k, x in enumerate(distribution(ps))))
```

```
fit 0.111  expected contradictions 1.70
0:11.1% 1:32.6% 2:35.3% 3:17.1% 4:3.5% 5:0.2%
```

### Spending an honor budget

Suppose you can afford to honor two of the five choices. Each honored choice means variant scenes wherever the expansion refers to it (GD202 week 2 prices those). Which two?

Honoring choice `i` removes the factor `p_i` from the product, so it multiplies `F` by `1 / p_i`. The gain is largest where `p_i` is smallest. **Honor the most even splits. Canonize the lopsided ones.**

| Honored | Canonized take rates | Fit `F` | Contradictions `E` |
|---|---|---|---|
| None | 0.90, 0.75, 0.60, 0.55, 0.50 | 11.1% | 1.70 |
| The two most lopsided (0.90, 0.75) | 0.60, 0.55, 0.50 | 16.5% | 1.35 |
| The two most even (0.55, 0.50) | 0.90, 0.75, 0.60 | 40.5% | 0.75 |

The same writing budget gives 16.5% fit or 40.5% fit, depending only on which choices you spend it on. Teams tend to honor the choice that felt most dramatic in the writers' room. The model says to honor the one players split on.

A useful companion is the log view. Take `−log2(p_i)` for each canonized choice. The values for the five choices are 0.15, 0.42, 0.74, 0.86 and 1.00, which sum to 3.17. Then `F = 2^(−3.17) = 0.111`. Each choice contributes a number of **dissonance bits** you can add up and compare. A 50/50 choice costs a full bit. A 90/10 choice costs 0.15. Every bit you remove doubles the fit.

### A visual you can move

Open [`w08-canon-fit.html`](../examples/w08-canon-fit.html). The left panel is the per-choice view: five bars, one per choice, each showing its canon option's take rate against a 50% line. The right panel is the per-player view: a histogram of how many times a player is contradicted, with the zero bar (the fit) highlighted. Every bar on the left sits at or above 50%, and the zero bar on the right is small. Click a choice to change it from "canonize" to "honor" and watch the zero bar grow. Try honoring the 90% choice first, then the 50% choice, and compare.

### Cross-game recognition

Rewrite each case as a set of `p_i` values and an action per choice.

**The Elder Scrolls, Daggerfall to the Warp in the West.** One choice with seven options. Reconcile makes every option's contradiction zero. It is the extreme answer for a choice where even the best canon option would have a low `p`.

**Star Wars: The Old Republic, class stories (2011) to Knights of the Fallen Empire (2015).** Eight stories full of choices with unknown take rates, then one shared storyline. Absorbing is the only affordable answer when `n` is in the thousands, because `F` for any canonized set would round to zero.

**Mass Effect 2 (BioWare, 2010).** A single-player case that shows honoring at full scale. Players could import a save from the first game, and several of their earlier decisions shaped the sequel's story. The PlayStation 3 release, where the first game was not available, added an interactive comic that let players make the major earlier decisions. That comic is an honor mechanism for players who have no history. MMOs face the same question with every new player, who arrives with no personal canon at all.

**Guild Wars 2, the Cutthroat Politics election (23 July to 5 August 2013).** Players earned support tokens through new activities and gave them to one of two candidates for a seat on the Lion's Arch council, Ellen Kiel or Evon Gnashblade. The winner's platform decided future content. Kiel won, and her promised investigation of the Thaumanova Reactor arrived as a new fractal. This is delegation. There is one choice, and `p` is the winner's share of support, above 50% by construction in a two-way race. Support was counted in tokens earned through play, not one vote per player, so a very active minority could outweigh a casual majority. That blurs `p` as a measure of how many players are on the losing side.

**Guild Wars 2, biography questions (launch, 2012).** At character creation, race-specific questions decide the content of a character's early personal story missions. This is honoring at the cheapest point, the start of a story, where every variant is played by the players who chose it and no earlier content has to be kept consistent.

Five games, five answers, one product. When you read a studio's decision about past choices, ask what `p_i` they were facing and which answer they picked for it.

### Eyes-open design judgment

- **Strength of the model:** it turns "players will be upset" into a number, and it shows that the problem compounds. One canonized choice is survivable. Five in one expansion are not, unless the splits are lopsided.
- **Strength:** it gives a clear spending rule. Honor the even splits, canonize the lopsided ones, absorb the ones that matter little.
- **Cost of honoring:** variants multiply when choices are referenced together. Two honored binary choices referenced in the same scene need four versions (GD202 week 3). Keep honored choices in separate scenes where you can.
- **Cost of absorbing:** it is cheap and invisible once, and obvious by the tenth time. Players learn that choices never matter and stop reading them. Budget it like any other resource.
- **Cost of reconciling:** it spends the world's credibility. A setting can afford a Warp in the West once or twice. Used every expansion, it tells players that nothing is fixed.
- **Decide deliberately:** before you write a choice, decide which of the five answers it will get when a later patch depends on it. A choice written without that plan will be canonized by default, at the worst possible `p`.

## 3. When choices are not independent

The fit formula assumes players make each choice on its own. Real players don't. Some consistently pick the merciful option, others the ruthless one. Some follow one faction through every choice.

**Positive correlation raises fit.** Suppose 60% of players are loyalists, who pick the canon option on each of five choices with probability 0.9, and 40% are rebels, who pick it with probability 0.3. Each choice's take rate is `0.6 × 0.9 + 0.4 × 0.3 = 0.66`. The independent formula predicts `F = 0.66^5 = 0.125`. The real fit is the mixture:

```
F = 0.6 × 0.9^5 + 0.4 × 0.3^5 = 0.6 × 0.590 + 0.4 × 0.002 = 0.355
```

Nearly three times the independent prediction. The loyalists mostly fit, and the rebels almost never do.

That is both good news and a warning. Fit is higher than the naive product. But the contradictions now fall on one group of players, who are contradicted nearly every time. A rebel player's experience is that the game never listens. Two consequences follow.

- **Canon should not always follow the same "type" of option.** If every canonized choice is the merciful one, the ruthless players carry all the contradiction. Mix the canon across types, or honor the choices where a type's identity is at stake.
- **Measure by player, not by choice.** A telemetry report of take rates per choice cannot show this. Ask your analyst for the distribution of contradictions per player, split by player segment. Lab 08 builds that report.

The upper limit on fit is the smallest `p_i`, reached when every player who picked the rarest canon option also picked every other canon option. Real populations sit between the independent product and that limit.

## 4. Writing a canon policy

A canon policy belongs in the setting bible, next to the permanence tags from last week. It answers four questions.

**1. Which layers of canon exist?** Most MMOs need three.

| Layer | Holds | Who can change it | Example |
|---|---|---|---|
| World canon | Events every player's content depends on | Only the lore team, in patches | The capital burned |
| Faction or class canon | Events true for one side or one class | The lore team, per side | Your faction took the pass |
| Personal canon | The character's choices | The player | You spared the smuggler |

**2. How does later content refer to each layer?** World canon can be stated. Faction canon can be stated to that faction's players. Personal canon can only be referenced through the player's own flags, never stated as fact by the world.

**3. What happens to a personal choice when later content needs it?** Pick one of the five answers when the choice is written, and record it. Use the fit calculation to check the whole set before an expansion locks its script.

**4. What does a new character inherit?** Every new character starts with no personal canon. Decide the defaults. A new character in year three should not be told they spared a smuggler they never met. Either the default is neutral ("the smuggler is gone"), or the character's content is written to establish the choice fresh, as Mass Effect 2's comic did.

### The hero problem, briefly

GD202 week 13 covered the problem of millions of players each being "the hero" and three ways to write around it. A canon policy adds one rule. **The world may say what happened; only the character may say who did it.** World canon records "the dragon fell." Personal canon records "you were there." This keeps world canon compatible with every character's story, including characters who never fought the dragon.

### Sandbox canon

In a sandbox world, some world canon is written by players, not by the lore team. EVE Online's alliances write much of that world's history through wars and treaties, and Andrew Groen's *Empires of EVE* (2016) is a whole book of it. MMO402 [week 2](../../MMO402-emergent-society-governance-and-ethics/lectures/w02-emergent-player-government-alliances-and-councils.md) covers how those alliances govern themselves. Here the canon policy runs the other way. The lore team's job is to decide which player-made events it will acknowledge in official lore, and how. Next week's living world events look at the tools for turning player action into world canon on purpose.

## In-class activity (25 minutes)

Work in groups of three with your setting bible's launch story.

1. List six choices from your launch story that a first expansion would likely depend on (5 minutes).
2. Estimate a take rate for each option. Justify each estimate in one line, using what you know about how players pick (merciful options tend to be popular, and so on) (5 minutes).
3. Compute the fit and expected contradictions if you canonize every majority option, by hand or with the interactive (5 minutes).
4. You have a budget to honor two choices. Pick them with the model, then pick them "by story instinct." Compute fit for both (5 minutes).
5. Assign one of the five answers to every choice and write one sentence per choice on how the expansion will refer to it (5 minutes).

Expected output: a six-row table with take rates, the two fit numbers from step 4, and the answer per choice. Each group reports the choice where the model and their instinct disagreed.

## Common misconceptions

- **"If canon follows the majority each time, most players agree with it."** Most players agree with each choice. Few agree with all of them. Fit is a product.
- **"Honor the most dramatic choice."** Honoring gains the most where the split is most even. A dramatic 90/10 choice barely moves fit.
- **"Reconciling is free because nobody is contradicted."** It costs the world's credibility. A setting where everything happened stops feeling like a place with rules.
- **"The per-choice report tells us who is unhappy."** It can't. Correlated choices concentrate contradictions on a few players. You need the per-player distribution.

## Check yourself

1. An expansion canonizes four choices with take rates 0.8, 0.7, 0.7 and 0.6. What is the fit? What is the expected number of contradictions?
2. In question 1 you can honor one choice. Which one, and what is the new fit?
3. A choice has three options chosen by 45%, 35% and 20% of players. The team canonizes the first. How many dissonance bits does the choice cost, and what fraction of players is contradicted?
4. Two player types make up the population, 70% and 30%. On each of three choices, the first type picks the canon option with probability 0.8 and the second with 0.2. Compute the fit under the independence assumption and the real fit. Explain the difference in one sentence.

<details>
<summary>Answers</summary>

1. `F = 0.8 × 0.7 × 0.7 × 0.6 = 0.235`. `E = 0.2 + 0.3 + 0.3 + 0.4 = 1.2`.
2. Honor the 0.6 choice, the most even split. `F = 0.8 × 0.7 × 0.7 = 0.392`.
3. `−log2(0.45) = 1.15` bits. 55% of players are contradicted.
4. Take rate per choice `0.7 × 0.8 + 0.3 × 0.2 = 0.62`. Independent fit `0.62^3 = 0.238`. Real fit `0.7 × 0.512 + 0.3 × 0.008 = 0.358 + 0.002 = 0.361`. The first type mostly fits and the second almost never does, so the contradictions pile onto the second type instead of being spread across everyone.

</details>

## Lab / assignment hook

[Lab 08, canon fit](../labs/lab08.md). You implement fit, the contradiction distribution and the honor-budget rule, extend them to a population of player types, and write a canon policy for your setting bible with a fit check for your first expansion. It counts toward the exercises grade and becomes the canon section of your world bible.

## Sources

- Wolf, M. J. P. (2012). *Building Imaginary Worlds: The Theory and History of Subcreation*. Routledge. Course text; authorship and canon in imaginary worlds. Chapter titles checked against the publisher's table of contents (Routledge, September 2026): 1 "Worlds within the World", 3 "World Structures and Systems of Relationships", 4 "More Than a Story: Narrative Threads and Narrative Fabric", 6 "Transmedial Growth and Adaptation", 7 "Circles of Authorship".
- The Unofficial Elder Scrolls Pages, "Lore:Warp in the West" (read September 2026). Event dated 3E 417 in which all of Daggerfall's quest outcomes (seven, per the page) happened at once, so that no single ending is canon. https://en.uesp.net/wiki/Lore:Warp_in_the_West
- Wikipedia, "Star Wars: The Old Republic" (read September 2026). Eight classes, each with a three-act storyline; Knights of the Fallen Empire released 27 October 2015 with a single storyline for all classes as the Outlander. https://en.wikipedia.org/wiki/Star_Wars:_The_Old_Republic
- Wikipedia, "Mass Effect 2" (read September 2026). Save import carrying earlier decisions into the story; the Genesis interactive comic for PlayStation 3 players. https://en.wikipedia.org/wiki/Mass_Effect_2
- Guild Wars 2 Wiki, "Cutthroat Politics" (read September 2026). Election from 23 July to 5 August 2013; support tokens earned through activities and turned in to Ellen Kiel's or Evon Gnashblade's basket; the winner's platform decided future content. https://wiki.guildwars2.com/wiki/Cutthroat_Politics
- Guild Wars 2 Wiki, "Captain Ellen Kiel" (read September 2026). Kiel won the council seat; her promised investigation of the Thaumanova Reactor followed in the Fractured release. https://wiki.guildwars2.com/wiki/Captain_Ellen_Kiel
- Guild Wars 2 Wiki, "Biography" (read September 2026). Race-specific biography questions at character creation shape the personal story's missions. https://wiki.guildwars2.com/wiki/Biography
- The five choices, take rates and player types in the worked example and exercises are invented for teaching.

## Interactive spec: examples/w08-canon-fit.html

**Purpose.** Let students see that a canon built from majority options, one choice at a time, fits only a small share of players, and that honoring the most evenly split choices raises that share far more than honoring the lopsided ones.

**The one insight the visual must make obvious.** Every bar in the per-choice view is at or above 50%, while the zero-contradictions bar in the per-player view is small. Switching a choice from canonize to honor grows the zero bar most when that choice is the most even split.

**Layout.** Two linked views side by side at 1280 px, stacked at 390 px (per-choice on top), with a results strip underneath.

- Left, "Per choice": five horizontal bars, one per choice, labeled with generic names ("Choice 1" to "Choice 5", editable text is not needed). Bar length is the canon option's take rate `p_i` on a 0 to 100% axis. A vertical line marks 50%. Honored choices are drawn hollow with a dashed outline and the label "honored"; canonized choices are solid. Each bar prints its `p_i` and its dissonance bits `−log2(p_i)` (or "0 bits" if honored).
- Right, "Per player": a vertical bar histogram of `P(k)` for `k = 0..n_canon`, where `n_canon` is the number of canonized choices. The `k = 0` bar uses the accent token and carries the label "fit"; other bars use the neutral token. Each bar prints its percentage.
- Results strip: "Fit F", "Expected contradictions E", "Dissonance bits", "Average per-choice agreement" (mean of `p_i` over canonized choices), and, when the mixture toggle is on, "Fit with player types".

**Controls** (keyboard accessible, values printed next to each):

- Five sliders, one per choice, for `p_i`: 0.50 to 1.00, step 0.01. Defaults 0.90, 0.75, 0.60, 0.55, 0.50.
- Five toggles (buttons with `aria-pressed`), one per choice, "canonize" or "honor". Default all canonize.
- "Honor budget" helper: a stepper 0 to 5 (default 0) and a button "Apply best honor set", which honors the `h` choices with the smallest `p_i` and canonizes the rest.
- Mixture toggle, default off. When on, show two extra sliders: loyalist share `w` (0 to 1, step 0.05, default 0.6), loyalist canon probability `q_L` (0 to 1, step 0.05, default 0.9) and rebel canon probability `q_R` (0 to 1, step 0.05, default 0.3). In this mode the five `p_i` sliders are disabled and each choice's take rate is `w × q_L + (1 − w) × q_R`; the histogram shows the mixture distribution.
- Reset button.

**Formulas.**

- Canonized set `C`. `F = Π_{i∈C} p_i` (1 if `C` is empty). `E = Σ_{i∈C} (1 − p_i)`. Bits `= Σ_{i∈C} −log2(p_i)`.
- Distribution by the recurrence: start with `d = [1]`; for each `i ∈ C`, `d'[k] = d[k] × p_i + d[k − 1] × (1 − p_i)`.
- Mixture mode: each type has the same probability on every canonized choice, so its distribution is binomial. `P(k) = w × Binom(k; n_canon, 1 − q_L) + (1 − w) × Binom(k; n_canon, 1 − q_R)`. Fit is `P(0) = w × q_L^n_canon + (1 − w) × q_R^n_canon`. Also print the independent prediction `p^n_canon` with `p = w q_L + (1 − w) q_R` next to it.

**Test values** (percentages to one decimal).

| Setting | F | E | Distribution k = 0..n |
|---|---|---|---|
| Defaults, all canonized | 11.1% | 1.70 | 11.1, 32.6, 35.3, 17.1, 3.5, 0.2 |
| Honor choices 4 and 5 (0.55, 0.50) | 40.5% | 0.75 | 40.5, 45.0, 13.5, 1.0 |
| Honor choices 1 and 2 (0.90, 0.75) | 16.5% | 1.35 | 16.5, 41.0, 33.5, 9.0 |
| Mixture, defaults, five canonized | 35.5% | — | independent prediction 12.5% |

Dissonance bits at the defaults: 3.17. "Apply best honor set" with `h = 2` must reproduce the second row.

**First screen.** Defaults. Caption above the views: "Every choice follows the majority. Whose story still fits?" The left bars all clear the 50% line, and the right panel's fit bar reads 11.1%.

**Accessibility and style.** Shared palette from `templates/interactive-tokens.css` inline, light and dark themes, `prefers-reduced-motion` respected. Honored versus canonized is shown by fill and outline style as well as color. An `aria-live` region states the fit, `E` and the distribution after each change. No game art, logos or screenshots.
