# GD202 · Week 02 — The Player as Co-author

**Why this matters:** Players judge a story game by one question more than any other. Did my choices matter? Writing a separate story for every choice is unaffordable, and faking it gets you caught. This week you learn where players actually feel authorship, and how to buy that feeling at a price your team can pay.

**You will be able to:**
- Place any player action on a co-authorship scale (select, perform, express, retell) and name what the designer still controls at each level.
- Compute the words written, the share of written content one player sees, and the cost per acknowledgement for four ways of honoring a single choice.
- Design a scene in which one binary choice is acknowledged several times at under 5% extra writing cost.
- Critique a "choices matter" claim by separating what changed in the game state from what the player was told changed.

**Before class:** Janet Murray, *Hamlet on the Holodeck* (1997), the chapter on agency (the course reader lists the pages). Bateman (ed.), *Game Writing*, 2nd ed. (2021), the chapter on the player's role in nonlinear writing. Play the first 30 minutes of any choice-driven narrative game and write down every choice you made and whether the game ever mentioned it again.

**Prerequisites from earlier courses:** [GD202 week 1](w01-story-vs-narrative-vs-plot.md) (story, plot, narration and the play story). [GD101 week 9, choice and meaningful decisions](../../GD101-introduction-to-game-design/lectures/w09-choice-and-meaningful-decisions.md) gave you the discernable, integrated and uncertain tests; this lecture applies the first two to story choices. [GD102 week 10, emergence vs progression](../../GD102-systems-design-and-game-mechanics/lectures/w10-emergence-vs-progression.md) explains why systemic games hand players more of the pen. [GS101 week 13](../../GS101-history-and-critical-study-of-games/lectures/w13-ludology-vs-narratology.md) covered emergent narrative as a critical idea.

**Interactive:** [`examples/w02-choice-cost.html`](../examples/w02-choice-cost.html). Keep it open during section 2.

---

## 1. Who holds the pen

Last week you split a game's storytelling into four layers: story, plot, narration and the play story. This week asks how much of each layer the player writes.

A novelist writes everything. A game writer shares the pen, but not equally, and not in the same way in every game. It helps to name four levels of player authorship. Each one gives the player more of the pen and gives the designer less control.

**Select.** The player picks from options the writer prepared. A dialogue menu with three replies, a fork in a quest, a yes-or-no prompt. The writer wrote every outcome. The player chooses which one becomes their story.

**Perform.** The player acts inside the rules and the actions become story. You sneak past the guards or you fight them. Nobody wrote "the player crawled through the kitchen," yet in your play story that is what happened. The designer wrote the rules and the space, not the events.

**Express.** The player adds content of their own: a character's name and face, a house they furnish, a message written on a sign. The designer wrote the canvas and the limits.

**Retell.** The player tells the story to other people, outside the game. A forum post about a raid, a video of a heist, a guild's history page. The designer wrote nothing here. They can only make retelling easy (replays, screenshots, logs) and make the events worth retelling.

Most games mix all four. A quest in an online RPG may give you a dialogue choice (select), a fight you can win several ways (perform), your own character's name in the quest text (express), and a boss kill your guild will talk about for a year (retell).

### Agency, and the feeling of agency

Janet Murray's 1997 book *Hamlet on the Holodeck* gave the field its standard word for what players want here. She called it **agency**, and defined it as the satisfying power to take meaningful action and see the results of our decisions and choices.

Read that definition closely. It has two halves. Taking meaningful action is about what the player does. **Seeing the results** is about what the game shows back. A choice that changes a variable nobody ever reads gives the player nothing. A choice that changes almost nothing, but is visibly noticed by the game, can feel strong.

That gap between state and feeling is the core of this week. Designers talk about it in two ways, and both are useful:

- **Consequence**: what actually changed in the game's state because of the choice (a flag set, a character alive or dead, a relationship score).
- **Acknowledgement**: a moment where the game shows the player that it noticed the choice (a line of dialogue, a notification, a changed scene, a character's reaction).

The player never sees consequence directly. They only see acknowledgements. That fact is what makes interactive storytelling affordable, and it is also what makes it easy to abuse.

## 2. Worked example: the rescue that always fails

### The hook

In Telltale's The Walking Dead (2012, five episodes released between April and November 2012), the first episode puts the player's character on a farm under attack, where a young man named Shawn is caught by the undead. The player can try to save him. It does not matter. The writers were working in the universe of Robert Kirkman's comic, where Shawn has already become one of the undead, so the game makes sure Shawn is always bitten.

Yet players remember this scene as a choice that mattered. The reason is that the attempt is noticed. It changes how Shawn's friend Kenny sees the player's character, and the game has a choice notification feature that tells you when a decision has changed a character's attitude toward you. (Players can turn these notifications off in the game's Minimal mode.)

The outcome was fixed. The acknowledgement was real. Telltale built a hit series on that difference. How much did it cost, and how much would the alternative have cost?

### The model

Take a chapter of `N` scenes, each about `w` words long. At the end of scene `s`, the player makes a choice with `b` options. There are four ways to honor it.

1. **Branch.** Every scene after the choice is written once per option. The paths never rejoin.
2. **Acknowledge.** The scenes stay shared. At `k` moments later in the chapter, a line of about `a` words is written in `b` versions, one per option. A **flag** (a stored true/false or small value) records the choice so the game can pick the right version.
3. **Payoff.** The scenes stay shared except one later scene, which is written in `b` versions.
4. **Acknowledge + payoff.** Both of the previous two.

For each strategy, compute the words written `W`, the words one player sees `V`, and the number of acknowledgements `R` a player meets:

```
Branch:                W = s·w + b·(N − s)·w          R = N − s
Acknowledge:           W = N·w + (b − 1)·k·a          R = k
Payoff:                W = N·w + (b − 1)·w            R = 1
Acknowledge + payoff:  W = N·w + (b − 1)·(k·a + w)    R = k + 1

Seen by one player:    V = N·w        (every strategy)
Share of writing seen: V / W
Extra words:           W − V
Cost per acknowledgement: (W − V) / R
```

- `N` is the number of scenes, `s` the scene where the choice happens, `w` the words per scene.
- `b` is the number of options. `k` is the number of callback lines and `a` their length in words.
- `R` counts moments where the player can see the choice reflected. For branching, every later scene counts, since each is different.

One player always sees exactly `N·w` words, whichever strategy you choose. That is the key fact of the model. Extra writing never reaches any single player. It reaches the other players, the ones who chose differently.

### Numbers you can check

Use a chapter of `N = 10` scenes of `w = 1,000` words, a binary choice (`b = 2`) at the end of scene `s = 2`, and `k = 6` callback lines of `a = 40` words.

| Strategy | Words written `W` | Share seen `V/W` | Extra words | Acknowledgements `R` | Extra words per acknowledgement |
|---|---|---|---|---|---|
| Branch | 18,000 | 55.6% | 8,000 | 8 | 1,000 |
| Acknowledge | 10,240 | 97.7% | 240 | 6 | 40 |
| Payoff | 11,000 | 90.9% | 1,000 | 1 | 1,000 |
| Acknowledge + payoff | 11,240 | 89.0% | 1,240 | 7 | 177 |

Check the first row by hand. Scenes 1 and 2 are shared, 2,000 words. Scenes 3 to 10 are written twice, `2 × 8 × 1,000 = 16,000`. Total 18,000. A player reads 10,000 of them, which is 55.6%.

Check the second row. Every scene is written once, 10,000 words. Six callbacks each get one extra 40-word version, 240 words. Total 10,240, and a player reads 97.7% of it.

The code below reproduces the table. It runs as shown with `.venv/bin/python`.

```python
def plan(strategy, N=10, s=2, w=1000, b=2, k=6, a=40):
    """Words written, words one player sees, and reflections of one choice."""
    seen = N * w
    if strategy == "branch":
        written = s * w + b * (N - s) * w
        reflections = N - s
    elif strategy == "acknowledge":
        written = seen + (b - 1) * k * a
        reflections = k
    elif strategy == "payoff":
        written = seen + (b - 1) * w
        reflections = 1
    elif strategy == "acknowledge + payoff":
        written = seen + (b - 1) * (k * a + w)
        reflections = k + 1
    extra = written - seen
    return written, seen, extra, reflections

for name in ["branch", "acknowledge", "payoff", "acknowledge + payoff"]:
    written, seen, extra, r = plan(name)
    print(f"{name:21} written={written:6,} seen={seen/written:6.1%} "
          f"extra={extra:5,} reflections={r} extra/reflection={extra / r:,.0f}")
```

Output:

```
branch                written=18,000 seen= 55.6% extra=8,000 reflections=8 extra/reflection=1,000
acknowledge           written=10,240 seen= 97.7% extra=  240 reflections=6 extra/reflection=40
payoff                written=11,000 seen= 90.9% extra=1,000 reflections=1 extra/reflection=1,000
acknowledge + payoff  written=11,240 seen= 89.0% extra=1,240 reflections=7 extra/reflection=177
```

Read the last column. Branching buys each acknowledgement at 1,000 words. Callback lines buy them at 40. That is a factor of 25, and it grows with scene length. The combined strategy gets seven acknowledgements, including one big one, for 12% more writing than a linear chapter. Branching gets eight for 80% more.

### A visual you can move

Open [the interactive](../examples/w02-choice-cost.html). The left view, "What the player feels," is a strip of `N` scenes for one playthrough, with a marker on every scene where the choice is acknowledged. The right view, "What the writer pays," stacks the words written for every option, with the part one player sees in solid color and the part they never see hatched.

Switch strategies and watch the two views disagree. Branching fills the left strip with markers and doubles the right stack. Acknowledge puts six markers on the left and barely moves the right. Then drag the choice point `s` earlier. The branching stack grows, since more scenes follow the choice. The acknowledge stack does not move at all. Its cost depends on how often you remember the choice, not on how early you ask it.

### Cross-game recognition

The same trade, acknowledgement bought cheaply instead of divergence bought expensively, shows up in very different kinds of games.

**Middle-earth: Shadow of Mordor (Monolith Productions, 2014).** The Nemesis System lets enemy captains remember earlier encounters with the player and react to them later. An orc you threw into a fire and who survived may come back scarred and angry about it. In the model's terms, the fight is the choice, the orc's memory is the flag, and his later taunt is the callback line. The difference is that a system generates the callbacks. The writers wrote reusable lines for categories of event ("you burned me") rather than for one specific scene. That drives the cost per acknowledgement down further and lets the player's performance, not only their selections, get acknowledged.

**Mass Effect 2 (BioWare, 2010).** Players could import a character from a completed save of the first Mass Effect, and several decisions made in that game then affected the story of the sequel. Most of those decisions come back as acknowledgements (a message, a cameo, a changed line) rather than as a different main story. That is our acknowledge strategy stretched across two whole games, with the save file as the flag.

**The Walking Dead itself, across episodes.** Choices carried over from one episode to the next, so the flag set in episode 1 could be read in episode 3. Across a season, the cost of branching would have multiplied with every episode. Acknowledgement kept it linear.

Three games, one structure. A choice writes a flag. The flag is read at later moments. Each read costs a few lines and gives the player a visible result.

### Eyes-open design judgment

The table makes acknowledgement look like a free lunch. It is not.

- **Acknowledgements have weight, and 40-word lines are light.** Six small callbacks do not feel like a changed story. Use at least one heavy acknowledgement (a payoff scene, a character who leaves) for choices you advertise as important. The combined strategy exists for this reason.
- **The notification is a promise.** Telling the player "they will remember" creates an expectation that the game will read that flag again. If it never does, players notice, and they tend to call it lying. Every flag you announce should have at least one later read. Keep a table of flags and their reads, which week 4 turns into a tool.
- **Some choices should branch.** If a choice changes who is in the party, which city you are in, or what the whole second act is about, callbacks will feel cheap. Week 3 shows how to afford branching by rejoining it (fold-back structures).
- **Acknowledge what the player cares about, not what the writer cares about.** A callback to a choice the player barely noticed is wasted. Playtests tell you which choices players remember. Ask them.
- **Be honest about fixed outcomes.** Shawn's fate is fixed. The scene still works because the game is honest about what changed (Kenny's view of you) and does not pretend to have changed what it did not. Players forgive fixed outcomes more easily than fake ones.

### Check the model

1. Same chapter as the table, but the choice has 3 options (`b = 3`). Compute `W` and the share seen for Branch and for Acknowledge.
2. A producer says "we can afford 5% extra writing on this chapter." With `N = 10`, `w = 1,000`, `b = 2`, `a = 40`, what is the largest `k` you can use for one choice? For how many separate binary choices with `k = 6` each?

<details>
<summary>Answers</summary>

1. Branch: `W = 2 × 1,000 + 3 × 8 × 1,000 = 26,000`, share seen `10,000 / 26,000 = 38.5%`. Acknowledge: `W = 10,000 + 2 × 6 × 40 = 10,480`, share seen 95.4%.
2. 5% of 10,000 is 500 words. One choice: `k × 40 ≤ 500`, so `k = 12`. At `k = 6` each choice costs 240 words, so you can afford 2 choices (480 words).

</details>

## 3. Beyond selection: performance, expression and retelling

The worked example dealt with selection, the level of authorship where the writer still wrote every outcome. The other three levels change what a narrative designer's job is.

### Performance: acknowledge what the player did

When a player sneaks through a castle without raising an alarm, that is a play story. The designer did not write it, but can acknowledge it. Later, a guard captain complains that the intruder left no trace. That line reads a flag set by the stealth system, not by a dialogue menu. Shadow of Mordor generalizes the idea into a whole system.

The design move is the same as in section 2. Pick the actions players are proud of. Record them as flags or counters. Write a few lines that read them. Performance acknowledgements are often the most valued kind, because the player did something, rather than clicked something.

### Expression: leave room on the canvas

Character creation, housing, naming a pet, writing on a sign. Here the player writes content directly, and the designer's job is to leave space for it without breaking the fiction. Two classic problems follow.

- **The name problem.** Voiced dialogue cannot say a name the player typed, so voiced games tend to refer to the player's character by title or pronoun. Text games can insert the name, but then every line with a name needs checking for grammar in every language (week 11, localization).
- **The tone problem.** If players can make their character silly, a grave scene may land badly. Decide how much of the canvas you hand over and where you take it back.

### Retelling: design for the story told afterwards

In an online game, players tell each other stories constantly. The designer's levers are indirect. Give memorable events a clear shape (a beginning, a turn, an end), make them visible to others (a server-wide announcement when a rare boss falls), and give players tools to record them (logs, replays, screenshots). Week 9 on emergent narrative and week 13 on shared versus personal story develop this. For now, note that retelling is where MMO players do most of their authoring, and a quest designer who only thinks about the selection level misses most of it.

## 4. Writing choices for a co-author

Some practical rules follow from the model and from the four levels.

**Separate tone choices from content choices.** A tone choice changes how the player's character says something (kind, blunt, joking) and usually only needs a different next line. A content choice changes what happens (help or refuse). Tone choices are cheap and give the player a voice. Content choices are expensive and give them control. A dialogue that offers only tone choices feels like dressing up. One that offers only content choices is unaffordable. Most good scenes mix them.

**Make every option discernable.** In GD101 week 9 you met the test that a decision must be discernable: the player must be able to see what their options are and, later, what came of them. For story choices, that means option text must tell the player what they are choosing. An option labelled "Maybe" that turns out to mean "betray the village" fails the test and feels like a trick, however good the consequence scene is.

**Place acknowledgements where they will be seen.** An acknowledgement in optional dialogue reaches only players who take that dialogue. Put at least one acknowledgement of every important choice on the critical path, the sequence of content every player must go through.

**Use time pressure deliberately.** The Walking Dead gives players a limited time to answer in many conversations. That forces a gut answer and makes the choice feel like the character's, not a calculation. It also punishes slow readers and players using assistive tools, so offer a setting that removes the timer.

**Keep a flag ledger from day one.** Every choice that writes a flag gets a row. Every place that reads a flag gets an entry in that row. A flag with no reads is a broken promise. A read with no matching write is a bug. You will build this ledger for your lab this week, and week 4 turns it into the backbone of a dialogue system.

## In-class activity (25 minutes)

Work in groups of three. Materials: the interactive, a shared document, a timer.

1. **(5 min)** Each person names one story choice from a game they played recently. As a group, classify each choice as select, perform, express or retell, and say whether it was a tone or a content choice.
2. **(8 min)** Pick one choice. List every acknowledgement you remember. Classify each as light (one line) or heavy (a scene, a character's fate, a changed location). Estimate `R` and guess which strategy from section 2 the game used.
3. **(8 min)** Redesign it. Using the interactive, choose `N`, `s`, `k` and a strategy so that the chapter costs no more than 10% extra writing and includes at least one heavy acknowledgement. Record `W`, `V/W` and `R`.
4. **(4 min)** Each group reads out its redesign in one sentence: "The choice is X, the flag is Y, it is read at Z moments, and the heavy payoff is W."

Expected output: a classified list of choices, one redesign with its numbers, and the one-sentence summary.

## Common misconceptions

- **"Choices only matter if the story branches."** Players experience acknowledgements, not branches. A choice with no divergence and well-placed callbacks can feel more significant than a branch the player never notices.
- **"Players can't tell when a choice is fake."** They can, when the game promises a consequence and never delivers one. The problem is the broken promise, not the fixed outcome.
- **"Extra content improves each player's experience."** Extra branch content reaches none of the players who chose the other way. It improves replay value and the sense that the world is responsive. It does not add to any single playthrough.
- **"Emergent games have no author."** The designer authors the rules, the spaces and the acknowledgements. The player authors the events. Both are co-authors, with different parts of the pen.

## Check yourself

1. A chapter has `N = 12` scenes of 800 words and a binary choice at the end of scene 4. Compute `W` and `V/W` for full branching.
2. The same chapter uses acknowledgement with `k = 8` callbacks of 30 words, plus one payoff scene. Compute `W`, `R` and the extra words per acknowledgement.
3. A game shows "The captain will remember this" after a choice, but no later scene reads that flag. Using this lecture's terms, describe what went wrong and give the cheapest fix.
4. Classify each as select, perform, express or retell: (a) naming your starship; (b) escaping a fight by jumping off a cliff; (c) posting a video of your guild's first boss kill; (d) choosing to spare a prisoner from a menu.

<details>
<summary>Answers</summary>

1. `W = 4 × 800 + 2 × 8 × 800 = 3,200 + 12,800 = 16,000`. `V = 12 × 800 = 9,600`. `V/W = 60%`.
2. `W = 9,600 + 8 × 30 + 800 = 10,640`. `R = 9`. Extra words `1,040`, so about 116 words per acknowledgement.
3. The game created an acknowledgement promise (the notification) without a later read of the flag, so the player expects a result that never comes. The cheapest fix is a single callback line on the critical path that reads the flag, for example the captain referring to the choice at the next meeting. Cost: one extra line version.
4. (a) express, (b) perform, (c) retell, (d) select.

</details>

## Lab / assignment hook

[Lab 02, the remembered choice](../labs/lab02.md). You will write a short branching scene in which one binary choice is acknowledged at least four times, keep a flag ledger, and report the scene's `W`, `V/W` and `R`. It is the second dialogue exercise (40% of the course grade, shared across the exercise labs).

## Sources

- Wikipedia, "The Walking Dead (video game)" (accessed September 2026). Telltale Games, 2012; five episodes released April to November 2012; choice notification feature that signals changes in characters' attitudes, which Minimal mode disables; limited time to respond in conversations; Shawn Greene is always bitten to stay consistent with the comic, while the attempt to save him influences Kenny's perception of the protagonist; choices carry over across episodes; writers aimed for choices that seem significant but often had little effect on the larger narrative.
- Wikipedia, "Middle-earth: Shadow of Mordor" (accessed September 2026). Monolith Productions, 2014; the Nemesis System lets non-player characters remember prior interactions with the protagonist, for example an orc thrown into a fire seeking revenge.
- Wikipedia, "Mass Effect 2" (accessed September 2026). BioWare, 2010; importing a character from a completed save of the first game lets several earlier decisions affect the sequel's story.
- Murray, J. H. (1997). *Hamlet on the Holodeck: The Future of Narrative in Cyberspace*. MIT Press. Definition of agency, paraphrased in section 1.
- Salen, K. & Zimmerman, E. (2003). *Rules of Play*. MIT Press. The discernable and integrated tests, as taught in GD101 week 9.
- Bateman, C. (ed.) (2021). *Game Writing: Narrative Skills for Videogames*, 2nd ed. Bloomsbury.

## Interactive spec: examples/w02-choice-cost.html

**The one insight.** One player always sees the same number of words, whatever you do. Branching spends thousands of words the player never sees to create acknowledgements, while callback lines create nearly as many acknowledgements for a few percent extra.

**Layout.** Two linked views, stacked on mobile (below 700px), side by side above. A strategy switcher above both.

- **View A, "What the player feels."** A horizontal strip of `N` equal boxes, one per scene, for a single playthrough on option A. Scenes up to and including `s` are neutral. The choice point is a vertical marker after scene `s`. Every acknowledgement is drawn as a filled marker on its scene: for Branch, a full-height tint on every scene after `s`; for Acknowledge, `k` small pins spread evenly over scenes `s+1..N` (pin `i` at scene `s + ceil(i × (N − s) / (k + 1))`, several pins may share a scene); for Payoff, one large star on the last scene; for combined, both. Readout under the strip: `Acknowledgements R = ...` and a legend light (pin) vs heavy (tint or star).
- **View B, "What the writer pays."** A vertical stacked bar of words written, with a second bar showing a linear chapter (`N·w`) for comparison. In the strategy bar, the part one player sees (`N·w`) is solid, the rest hatched and labelled "written for players who chose differently". Readouts: `W`, `V`, `V/W` as a percent, `extra = W − V`, `extra per acknowledgement = (W − V)/R`.
- **Summary table** below both views with all four strategies for the current parameters, the current one highlighted, so students can copy numbers.

**Controls.**
- Strategy segmented control: Branch, Acknowledge, Payoff, Acknowledge + payoff. Default Acknowledge + payoff.
- Sliders: `N` scenes 3 to 20 (default 10); choice after scene `s` 1 to `N − 1` (default 2); words per scene `w` 200 to 3,000 step 100 (default 1,000); options `b` 2 to 4 (default 2); callbacks `k` 0 to 20 (default 6); callback length `a` 10 to 200 step 10 (default 40).
- Toggle "Show as percent of a linear chapter" for View B.
- All sliders keyboard operable, with visible numeric values; changes update both views immediately.

**Formulas.**
- Branch: `W = s·w + b·(N − s)·w`, `R = N − s`.
- Acknowledge: `W = N·w + (b − 1)·k·a`, `R = k`.
- Payoff: `W = N·w + (b − 1)·w`, `R = 1`.
- Combined: `W = N·w + (b − 1)·(k·a + w)`, `R = k + 1`.
- `V = N·w` for all. When `R = 0`, show "no acknowledgement" instead of dividing.

**Test values (must match).**

| Parameters | Strategy | W | V/W | Extra | R | Extra per ack |
|---|---|---|---|---|---|---|
| N=10, s=2, w=1000, b=2, k=6, a=40 | Branch | 18,000 | 55.6% | 8,000 | 8 | 1,000 |
| same | Acknowledge | 10,240 | 97.7% | 240 | 6 | 40 |
| same | Payoff | 11,000 | 90.9% | 1,000 | 1 | 1,000 |
| same | Ack + payoff | 11,240 | 89.0% | 1,240 | 7 | 177 |
| same but b=3 | Branch | 26,000 | 38.5% | 16,000 | 8 | 2,000 |
| same but b=3 | Acknowledge | 10,480 | 95.4% | 480 | 6 | 80 |
| N=12, s=4, w=800, b=2 | Branch | 16,000 | 60.0% | 6,400 | 8 | 800 |
| N=12, s=4, w=800, b=2, k=8, a=30 | Ack + payoff | 10,640 | 90.2% | 1,040 | 9 | 116 |

**Accessibility and style.** Solid versus hatched is also distinguished by a text label. Pins and stars have text equivalents in the readout. Respect `prefers-reduced-motion` (no animated transitions) and `prefers-color-scheme`. Use `templates/interactive-tokens.css`. No game characters or art.
