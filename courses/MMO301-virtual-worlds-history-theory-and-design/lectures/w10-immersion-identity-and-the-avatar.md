# MMO301 · Week 10 — Immersion, Identity and the Avatar

**Why this matters:** Players stay in a virtual world for years because of who they are there, not because of the loot. The avatar is the object that carries that identity, and small decisions about it (how many faces the creator offers, which one is the default, whether names must be unique) decide whether players feel like someone or like one of a crowd of clones. This week gives you a way to measure that, and a vocabulary for talking about immersion without hand-waving.

**You will be able to:**
- Place a player's relationship to their avatar on Bartle's four levels of immersion and name the design features that push players up or down the ladder.
- Compute the chance that two avatars in a crowd look identical, using the birthday model and the effective number of looks `1 / Σp²`.
- Critique a character creator or naming policy by showing how defaults and popular choices shrink the space of identities it seems to offer.
- Explain the Proteus effect and design an avatar feature that uses it deliberately, stating its ethical limits.

**Before class:** Bartle, *Designing Virtual Worlds* (2003, free CC edition), chapter 3, "Levels of Immersion" and "Identity and Identification" (pp. 205-220). Yee & Bailenson, "The Proteus Effect" (2007), *Human Communication Research* 33(3), pp. 271-290, introduction and general discussion (about 8 pages).

**Prerequisites from earlier courses:** [GS101 week 5, text adventures and MUD1](../../GS101-history-and-critical-study-of-games/lectures/w05-text-adventures-and-mud1.md) introduces Bartle's defining properties of a virtual world, including the one-character-per-player rule that this week builds on. [MA102 week 1, sample spaces and events](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w01-sample-spaces-and-events.md) and [MA102 week 3, the complement rule](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w03-complement-rule-chance-of-at-least-one-drop.md) give you the probability tools. [GS101 week 14, games and representation](../../GS101-history-and-critical-study-of-games/lectures/w14-games-and-representation.md) covers who appears on screen; this week covers how players appear to each other. Within this course, [week 1, Bartle's definition](w01-what-is-a-virtual-world-bartles-definition.md), comes first, and so does [week 9 on Yee's motivation facets](w09-motivation-research-beyond-bartle-yee.md), which include immersion.

**Interactive:** [examples/w10-avatar-twins.html](../examples/w10-avatar-twins.html). Keep it open during section 2.

---

## 1. Immersion is a ladder

"Immersive" is the most overused word in game marketing. It usually means "has good graphics" or "has a lot of lore." In virtual-world design it means something narrower. Bartle defines immersion as the player's sense of being in the world, and he measures it by one thing: how the player regards the object they control.

He describes four levels, each separated from the next by a barrier the player has to cross.

| Level | How the player sees the in-world object | How they talk about it |
|---|---|---|
| Player | A computer construct, like a document in a word processor | "The program did X" |
| Avatar | A puppet that represents them, a tool for acting in the world | "My guy picked up the sword" |
| Character | A representation of them, a rounded personality they put on | "Thorina lost her sword last night" |
| Persona | Themselves, in the world. No separate character remains | "I lost my sword" and meaning it |

Bartle's claim is that most players sit at the character level, and that the persona level is what virtual worlds offer that no other medium does. At persona level, a player who dies in a fight feels that they died, not that their character did. Note how precise this is. It says nothing about screen resolution or story. A text MUD can take a player to persona level. A photorealistic single-player game with a fixed protagonist rarely does, because you cannot be a character someone else wrote.

Two terms need care because designers use them loosely:

- **Avatar**, in Bartle's technical sense, is the second rung: the object treated as a puppet. In everyday studio talk "avatar" just means the player's in-world body, and that is how this lecture uses it outside this table.
- **Presence** is the related idea from computer-mediated communication research: the illusion of being somewhere else. Presence is about the senses. Immersion in Bartle's sense is about identity.

### What moves players up the ladder

You cannot force a player up the ladder, but you can remove the things that knock them off it. From the definition, the levers are the ones that make the object feel like the player's own:

- **Choice at creation.** A body, face and name the player chose. A preset hero sits at the avatar level for most people.
- **Continuity.** The same character, with the same name and history, every time the player logs in. This is why Bartle's definition requires persistence. Week 12 returns to it.
- **Being seen.** Other players recognizing you, remembering what you did, reacting to you. A persona needs witnesses.
- **Challenges that ask who you are.** Bartle argues that identity grows through the player's responses to situations the world throws at them: responsibility, betrayal, success, strangers. Each response is a small decision about who they are.

And the things that knock players down: reminders that it is software (loading screens, visible resets, which Bartle calls anti-immersion), fiction that contradicts itself, and meeting your own face on a stranger. That last one is this week's worked example.

## 2. Worked example: twins in the capital

### The hook

You spend forty minutes in a character creator. You pick a face, a hairstyle, a hair colour and a skin tone. The creator has thousands of combinations, so your character should be one of a kind. Then you walk into the capital city and within a few minutes you pass someone who looks exactly like you.

Many MMO players report this. It feels like bad luck, or like everyone copied you. It is neither. It is the birthday problem, made worse by defaults, and you can predict it before launch.

### The model

Think of every look the creator allows as a box. A player's appearance lands in one box. Two players are **twins** if they land in the same box.

Let `M` be the number of boxes, the product of the option counts in each category. For a creator with `m₁` faces, `m₂` hairstyles and so on:

```
M = m₁ × m₂ × … × m_k
```

If every player chose every option with equal chance, the probability that two random players are twins is `c = 1/M`. Real players do not choose evenly. Let `p_i` be the share of players in box `i`. Then the chance that two random players match is:

```
c = Σ p_i²                 (collision probability)
M_eff = 1 / c              (effective number of looks)
```

`M_eff` is how many equally popular looks would give the same twin rate. When choices are even, `M_eff = M`. When choices bunch up, `M_eff` falls, sometimes by a factor of ten or more.

In a crowd of `n` players there are `n(n − 1)/2` pairs, and each pair is a twin pair with chance `c`. So:

```
expected twin pairs   E = n(n − 1)/2 × c
P(at least one twin)  ≈ 1 − e^(−E)
```

- `n` is the number of players you can see at once, for example a city square.
- `e^(−E)` is the chance of no twin pairs. The approximation is accurate when `c` is small, which it always is here. It comes from the complement rule you used in MA102 week 3.

If categories are chosen independently, `c` multiplies across categories: `c = c₁ × c₂ × … × c_k`, where each `c_j = Σ p²` within category `j`. That makes it easy to compute by hand.

### Numbers you can check

Take an invented creator with four categories: 8 faces, 10 hairstyles, 12 hair colours and 6 skin tones. That gives `M = 8 × 10 × 12 × 6 = 5,760` looks.

**Case A, even choices.** Every option equally likely, so `c = 1/5,760 = 0.000174`.

**Case B, sticky defaults.** Each category has a default option that 40% of players keep. The other 60% spread evenly over the remaining options. For a category with `m` options:

```
c_j = 0.4² + 0.6² / (m − 1) = 0.16 + 0.36 / (m − 1)
```

| Category | Options `m` | `c_j` even (`1/m`) | `c_j` with 40% default |
|---|---|---|---|
| Face | 8 | 0.125 | 0.16 + 0.36/7 = 0.2114 |
| Hairstyle | 10 | 0.100 | 0.16 + 0.36/9 = 0.2000 |
| Hair colour | 12 | 0.0833 | 0.16 + 0.36/11 = 0.1927 |
| Skin tone | 6 | 0.1667 | 0.16 + 0.36/5 = 0.2320 |
| Product `c` | | 0.000174 | 0.001891 |
| `M_eff = 1/c` | | 5,760 | 529 |

The defaults cut the creator's real variety by a factor of about 11. The box says 5,760 looks. The crowd behaves as if there were 529.

Now fill a city square:

| Players in view `n` | Pairs | Even: `E` | Even: P(twin) | Defaults: `E` | Defaults: P(twin) |
|---|---|---|---|---|---|
| 10 | 45 | 0.008 | 0.8% | 0.085 | 8.2% |
| 20 | 190 | 0.033 | 3.2% | 0.359 | 30.2% |
| 50 | 1,225 | 0.213 | 19.2% | 2.316 | 90.1% |
| 100 | 4,950 | 0.859 | 57.7% | 9.359 | 99.99% |
| 200 | 19,900 | 3.455 | 96.8% | 37.6 | ~100% |

Check one row by hand. With defaults and 50 players, `E = 1,225 × 0.001891 = 2.316`, and `1 − e^(−2.316) = 1 − 0.0987 = 0.901`.

The crowd size at which a twin becomes more likely than not solves `E = ln 2`, which gives `n ≈ ½ + √(2 ln 2 / c)`. With even choices that is about 90 players. With 40% defaults it is about 28. A busy bank or auction house holds more than 28 people at peak hours in most MMOs.

One more number is worth a gasp. The share of players who keep the default in all four categories is `0.4⁴ = 2.56%`. In a city of 1,000 players, about 26 of them are the identical default character. The default is the most common look in the world by a wide margin.

### Why the nominal count lies

Two effects stack. The first is the birthday effect. The number of pairs grows with the square of the crowd, so twins appear long before `n` gets close to `M`. With `M = 5,760`, you need only about 90 people, 1.6% of `M`, for even odds. This is the same arithmetic behind the classic result that 23 people are enough for a 50.7% chance of a shared birthday among 365 days.

The second is the popularity effect. Squaring the shares makes large shares dominate `c`. A default with 40% of players contributes `0.16` to `c_j`. All the other options in a 12-option category together contribute `0.033`. One popular choice outweighs eleven unpopular ones.

### A visual you can move

Open `examples/w10-avatar-twins.html`. The left view, "What the creator promises," shows `M` as a large number and one bar per category, split into a segment per option sized by its share, with the default segment highlighted. The right view, "What the crowd sees," shows `M_eff`, a curve of P(twin) against crowd size, and a dot for the current crowd. Drag the "default stickiness" slider from 0% to 60%. The left number never changes. The right curve slides left, and at 60% stickiness `M_eff` falls to 47 and a crowd of 10 already has a 61.5% chance of twins. Then add a fifth category with the "add a category" button and watch how much less it helps when that category also has a sticky default.

### Cross-game recognition

The same model governs any system where players need to tell each other apart. Rewrite each one as "boxes, shares, crowd" and you have the same arithmetic.

**Discord usernames (May 2023 change).** Until 2023 Discord gave every account a name plus a four-digit discriminator, such as `Name#1234`. That makes each base name a category with 9,999 boxes. Discord's own announcement explained that popular base names like "Mike" ran out of discriminators entirely, while rare names never came close. That is the popularity effect: the shares were skewed, so the popular boxes filled while the space as a whole looked huge. The company also reported that nearly half of all friend requests failed because people typed the name wrong. A namespace that is technically unique but hard to remember fails at the thing identity is for. Discord moved to unique usernames with a separate free-form display name.

**Final Fantasy XIV character names (current game).** Each character needs a forename and a surname, and no two characters on the same World (server) may share the full pair. Two name parts multiply the space, exactly like our categories. If a World had 200 common forenames and 200 common surnames, it would offer 40,000 pairs. But the same skew applies: if many players reach for the same few fantasy names, the effective space is far smaller than 40,000, and the uniqueness rule turns collisions into "name taken" messages at creation instead of twins in the street. The per-World scope is the crowd size `n` in our model. Uniqueness is only enforced within the crowd that can see you.

**The classic birthday problem.** 365 days, one box per day, and a room of `n` people. With even shares, `c = 1/365`, and the model gives 50% at about 23 people. Real birth dates are not perfectly even across the year, which makes shared birthdays slightly more likely than the even-share answer. Same model, same lesson: uneven shares always raise `c`.

Three systems, one idea. When someone tells you a system offers "millions of combinations," ask what `M_eff` is and how big the crowd is.

### Eyes-open design judgment

What should you do with this? Not "maximize options." Each response has costs.

- **Weaken the default.** The cheapest fix is to stop having one. Randomize the starting look, or make the player pick each category before continuing. Cost: some players want to get into the game fast, and a random start can produce a face they dislike and never change. Randomizing within a curated set of good-looking presets is a reasonable middle ground.
- **Add categories that people actually vary.** A new category only helps if choices within it spread out. A 30-option category where 70% keep the default barely moves `c`. Before adding a slider, look at telemetry from the ones you have. DB201 teaches the telemetry side.
- **Let gear and history carry identity.** In many MMOs, players are recognized more by armour, titles, mounts and guild tags than by faces. Those are also boxes with shares, and a single dominant "best in slot" set creates twins as reliably as a default face. Appearance systems that let players show one item while wearing another exist to fix exactly that.
- **Decide how unique names must be.** Unique names per server make names reliable identifiers but force late joiners into odd spellings. Non-unique display names plus a hidden unique ID are friendlier but make impersonation easier. Choose based on how much your world depends on reputation. A world with player trading and scams needs names people can trust.
- **Accept some twins.** A world of perfectly unique faces is not the goal. Players at the avatar level do not care. Players at the character and persona level do, and they are the ones who stay for years. Measure the twin rate in your busiest hub and set a target.

### Check yourself (worked example)

1. A creator has 6 faces, 6 hairstyles and 6 colours, chosen evenly. What is `M`, and roughly how many players in view give even odds of a twin?
2. The same creator, but 50% of players keep the default in each category and the rest spread evenly. What is `M_eff`?
3. A designer adds 20 new hairstyles to the creator in question 2 without touching the default. Estimate `M_eff` again. Was it worth it?

<details>
<summary>Answers</summary>

1. `M = 216`, `c = 1/216`. Even odds at `n ≈ ½ + √(2 × 0.693 × 216) = ½ + √299.4 ≈ 17.8`, so about 18 players.
2. Each category: `c_j = 0.25 + 0.25/5 = 0.30`. Product `0.30³ = 0.027`, so `M_eff ≈ 37`.
3. Hairstyles become 26 options: `c_j = 0.25 + 0.25/25 = 0.26`. Product `0.30 × 0.26 × 0.30 = 0.0234`, so `M_eff ≈ 43`. Twenty new hairstyles added 6 effective looks. The default is doing almost all the damage. Changing the default policy would have done far more.

</details>

## 3. The avatar changes the player

So far the avatar has been something other players look at. It also changes the person controlling it.

In 2007 Nick Yee and Jeremy Bailenson at Stanford published two laboratory experiments in immersive virtual reality. In the first, participants were randomly given a more or less attractive avatar and then talked with a stranger in the virtual room. Those with more attractive avatars behaved more intimately, standing closer and telling the stranger more about themselves. In the second, participants were given taller or shorter avatars and then split a sum of money with another person. Those with taller avatars negotiated more confidently. Yee and Bailenson named this the **Proteus effect**: people's behaviour shifts to match the self-representation they have been given, whether or not anyone else sees it that way.

Read the scope carefully before you use it:

- These were short lab sessions with assigned avatars. MMO players choose their avatars, which means you cannot tell from outside whether the avatar changed the player or the player chose an avatar that matched them.
- The effect is about behaviour in the session. It does not claim that a tall elf turns a shy player into a confident one for life.

Bartle makes a related but slower claim. He argues that players try out sides of themselves in the world, and over months the ones that work migrate back into who they are. The world, in his words, cannot make you something you are not. It lets you find out what you already were.

### Designing with the Proteus effect

The design question is: what do you want players to feel able to do, and does the avatar you give them support it?

- A new player whose default avatar is small, drab and identical to hundreds of others starts at the bottom of the ladder and has a reason to feel like a nobody. The twins example and the Proteus effect point the same way.
- Visible progress on the body (armour that looks earned, scars, a title) gives the player a representation that matches their history.
- Height, size and beauty options interact with social behaviour. That is a reason to think about them, and a reason to be careful. Using appearance to push spending, for example by making default avatars deliberately unattractive so that cosmetic purchases feel necessary, turns a psychological effect into a lever on players' self-image. MMO403 treats the ethics of monetization in depth.

## 4. Identity: what makes you "you" in a shared world

Immersion is private. Identity in a virtual world is also social. You are who other people can recognize, remember and hold to account. Four features carry that.

**The name.** The most stable identifier. Name policy decides how unique names are, whether they can change, and what happens to a name when an account goes idle. Each choice is a trade between reliability (people can find you and trust that you are you) and freedom (you can start over). A world with a single unique name per account makes every scam follow the scammer. A world with free renames lets players outgrow a bad name, and lets bad actors outgrow a bad reputation.

**The look.** As section 2 shows, a look is only an identifier if it is rare enough. Most MMO players identify each other by name plates, not faces, which is itself a sign that appearance alone does not do the job.

**The history.** Titles, achievements, guild membership, known deeds. These are the parts of identity other players can verify. They are also persistence decisions: they only work if they last. Week 12 asks what should last.

**The body of the character across time.** Bartle's definition requires that one player acts through one character in the world. Alts (second characters), shared accounts and character sales all break the link between the character and the player behind it. When a famous character is sold, players who trusted the name are now trusting a stranger. Real-money trade ([MMO304 week 11](../../MMO304-virtual-economies-i-faucets-sinks-and-markets/lectures/w11-real-money-trade-and-gold-farming.md)) is an identity problem as much as an economic one.

### Anonymity cuts both ways

The same distance that lets a shy player try being outgoing lets an unpleasant player be cruel without consequence. Koster's Laws, which you study next week, include an observation that anonymity makes people behave worse, and another that every population contains an irreducible share of troublemakers. Identity design is how you manage that. A name that persists, a history other people can see, and a reputation that follows you are the tools. Each also makes it harder for players to start fresh after a mistake. There is no free choice here. Pick the trade-off deliberately.

### Gender swapping and representation

Many players play characters of a different gender from their own, for many reasons: preference for how a model looks from behind, role-play, curiosity, avoiding unwanted attention. For design, the lesson is modest and practical. Do not assume the character's gender, age or body tells you anything about the player's. Tools that infer players' demographics from their avatars will be wrong. Moderation systems that treat a character's appearance as a fact about the person are wrong too. GS101 week 14 covers how to count who appears on screen. Here the point is that the person on screen and the person at the keyboard are two different data points.

## In-class activity (25 minutes)

Work in groups of three with one laptop.

1. **(5 min)** Pick one MMO or online game character creator you know. List its categories and estimate the number of options in each. Compute `M`.
2. **(5 min)** For each category, guess the share of players who keep the default or pick the single most popular option. Justify each guess in a few words ("default hair colour is the only non-garish one").
3. **(10 min)** Compute `c_j` for each category using the sticky-default formula, then `c` and `M_eff`. Using the interactive or by hand, find the crowd size at which P(twin) passes 50%. Compare it to the busiest place in that game.
4. **(5 min)** Propose one change to the creator that would at least double `M_eff`, and name its cost.

Expected output: one table (categories, `m`, guessed default share, `c_j`), the numbers `M`, `M_eff` and the 50% crowd size, and a one-sentence change with its cost. Groups share their `M / M_eff` ratio. The class usually finds that the ratio is between 5 and 50 and that the default policy explains most of it.

## Common misconceptions

- **"More options means more unique characters."** Only if players use them. `M_eff` depends on the shares, and one sticky default can wipe out the benefit of dozens of new options.
- **"Twins only appear when the population gets close to the number of combinations."** Pairs grow with the square of the crowd, so twins appear when the crowd is roughly the square root of `M_eff`, far below `M`.
- **"Immersion means realistic graphics."** In Bartle's sense it is about how the player regards their character. A text world can reach persona level. Realistic graphics with a fixed protagonist usually do not.
- **"The Proteus effect proves avatars change who players are."** The original evidence is short lab sessions with assigned avatars. It shows behaviour in the moment shifts. Long-term claims need more evidence, and in real games self-selection gets in the way.

## Check yourself

1. A game has 4 faces, 5 hairstyles, 8 hair colours and 3 skin tones, all chosen evenly. What is the chance of at least one twin pair among 30 players?
2. In the invented creator from section 2 (8, 10, 12, 6 options), the design team removes the default from the face category, so faces are chosen evenly, but keeps 40% defaults elsewhere. What is the new `M_eff`?
3. A player says, "I don't care what my guy looks like, I just want the best gear." Which level of immersion is this player at, most likely, and what feature would matter more to them than the character creator?
4. A server allows 3,000 players in its main city. Names must be unique per server and there are 12,000 characters on it. A designer proposes making names unique across all 40 servers instead, "for better identity." Name one benefit and one cost, using the idea of the crowd that can see you.
5. Explain in two sentences why the Proteus effect is hard to measure in a commercial MMO.

<details>
<summary>Answers</summary>

1. `M = 4 × 5 × 8 × 3 = 480`, `c = 1/480`. Pairs `= 30 × 29 / 2 = 435`. `E = 435/480 = 0.906`. P(twin) `= 1 − e^(−0.906) ≈ 0.596`, about 60%.
2. Face `c_j` becomes `1/8 = 0.125` instead of 0.2114. New `c = 0.125 × 0.2 × 0.1927 × 0.232 = 0.001118`. `M_eff = 1/0.001118 ≈ 895`, up from 529.
3. Most likely the avatar level: the character is a tool for acting in the world. Gear, stats and the progression system matter more to them than appearance. Your creator design is not for this player, but your gear appearance is, because gear becomes their look.
4. Benefit: a name identifies one person across the whole game, so reputation follows them when they move servers or meet players from other servers in shared content. Cost: the crowd for name collisions grows from 12,000 to about 480,000 characters, so many more names are taken, and late joiners are pushed to odd spellings. The per-server rule was already enough for the crowd that could see you, unless servers mix.
5. Players choose their avatars, so a tall confident avatar may reflect a confident player rather than cause confidence. Without randomly assigning avatars, which commercial games rarely do, you cannot separate the avatar's effect from the player's choice.

</details>

## Lab / assignment hook

[Lab 10, the crowd audit](../labs/lab10.md). You will build a spreadsheet that computes `M`, `c`, `M_eff` and P(twin) for a character creator, run it on a supplied sample of 120 characters from an invented MMO, and write a 400-word redesign memo. The same method feeds the identity section of your world design bible in week 15.

## Sources

- Bartle, R. A. (2003). *Designing Virtual Worlds*. New Riders. Free Creative Commons edition from the author (mud.co.uk). Chapter 1: definition of a virtual world, including one character per player and persistence. Chapter 3, "Levels of Immersion" (pp. 205-208): player, avatar, character and persona; persona level as what virtual worlds uniquely offer; presence as a related idea. Chapter 3, identity development through challenges and the claim that a world lets you find out who you are (pp. 214-216). Chapter 4, resets described as anti-immersion.
- Yee, N. & Bailenson, J. (2007). "The Proteus Effect: The Effect of Transformed Self-Representation on Behavior." *Human Communication Research* 33(3), 271-290. Two experiments: attractive avatars and intimacy with a stranger; taller avatars and confidence in negotiation.
- Discord company blog, usernames announcement (discord.com/blog/usernames, 2023). Change announced for May 2023; 9,999 discriminators per base name so popular names ran out; nearly half of friend requests failed because of mistyped names; move to unique lowercase usernames plus display names.
- Final Fantasy XIV Online wiki (consolegameswiki), "Character Creation" (current game, accessed September 2026). Forename and surname up to 15 characters each and 20 combined; no two players on the same World may share the full name.
- Koster, R., "The Laws of Online World Design" (raphkoster.com, collected from the MUD-Dev list from the late 1990s). Observations on anonymity and on a fixed share of troublemakers, used here as a forward reference to week 11.
- The 23-person, 50.7% birthday result is standard probability, computed exactly as `1 − Π(365 − i)/365` for `i = 0…22`.

## Interactive spec: examples/w10-avatar-twins.html

**The one insight:** the number of looks a character creator promises (`M`) is not the number the crowd sees (`M_eff = 1/Σp²`). Sticky defaults shrink `M_eff` by an order of magnitude, and the birthday effect means twins appear at crowd sizes near `√M_eff`, not near `M`.

**Layout.** Two linked views, side by side on desktop, stacked on mobile (left view on top).

- **Left view, "What the creator promises":** a large readout of `M` (thousands separator), and below it one horizontal bar per category. Each bar is split into `m_j` segments with widths proportional to the option shares. The default segment is drawn in the palette's accent colour, the rest in a neutral colour. When stickiness is 0, all segments are equal.
- **Right view, "What the crowd sees":** a large readout of `M_eff` (rounded to a whole number), then a line chart of P(at least one twin) on the vertical axis (0 to 100%) against crowd size `n` on the horizontal axis (2 to 300, linear). Draw two curves: even choices (thin, neutral, dashed) and current settings (thick, accent). Mark the current `n` with a dot and its P value, and draw a horizontal dashed line at 50% with a label showing the crowd size where the current curve crosses it.
- **Below both views, "Default clones":** one line of text: "Players who kept every default: X.XX% (about Y in a city of 1,000)".
- **Readouts (copyable):** `M`, `c` (6 decimals), `M_eff` (whole number), `E` (3 decimals), P(twin) at current `n` (1 decimal percent), even-odds crowd size (1 decimal), all-default share (2 decimals percent).

**Controls (keyboard accessible, labelled):**

1. Crowd size `n`: slider 2 to 300, step 1, default 50.
2. Default stickiness `d`: slider 0% to 80%, step 5%, default 40%. Applies to every category. When `d = 0` the category is even.
3. Option counts: four number inputs, one per category, labelled Face, Hairstyle, Hair colour, Skin tone. Range 2 to 50, defaults 8, 10, 12, 6.
4. "Add a category" button: adds a fifth category "Extra" with 10 options (editable, range 2 to 50). Pressing again removes it (the button label switches to "Remove extra category").
5. Per-category override: a checkbox next to each category, "no default (even)". When checked, that category uses `c_j = 1/m_j` regardless of `d`.
6. Reset button.

**Formulas.**

```
M        = Π m_j
c_j      = d² + (1 − d)² / (m_j − 1)     sticky category (d > 0)
c_j      = 1 / m_j                        even category, or d = 0
c        = Π c_j
M_eff    = 1 / c
pairs    = n (n − 1) / 2
E        = pairs × c
P(twin)  = 1 − exp(−E)
n_50     = 0.5 + sqrt(0.25 + 2 ln 2 / c)
clones   = Π d  over sticky categories (0 if any category is even or d = 0)
```

Note: with `d = 1/m_j` the sticky formula equals `1/m_j`, so the curve is continuous.

**Test values** (four categories 8, 10, 12, 6):

| Setting | `c` | `M_eff` | `n` | `E` | P(twin) | `n_50` |
|---|---|---|---|---|---|---|
| `d = 0` | 0.000174 | 5,760 | 50 | 0.213 | 19.2% | 89.9 |
| `d = 0` | 0.000174 | 5,760 | 100 | 0.859 | 57.7% | 89.9 |
| `d = 25%` | 0.000355 | 2,816 | 50 | 0.435 | 35.3% | 63.0 |
| `d = 40%` | 0.001891 | 529 | 20 | 0.359 | 30.2% | 27.6 |
| `d = 40%` | 0.001891 | 529 | 50 | 2.316 | 90.1% | 27.6 |
| `d = 60%` | 0.021236 | 47 | 10 | 0.956 | 61.5% | 8.6 |

Default clones at `d = 40%`: 2.56%, about 26 in 1,000. At `d = 60%`: 12.96%, about 130.

Face set to "no default (even)", `d = 40%`: `c = 0.001118`, `M_eff = 895`.

**First screen:** defaults above (`n = 50`, `d = 40%`). Caption above both views: "5,760 looks promised. The crowd sees 529. In a square of 50 players, 90% chance someone is your twin."

**Content rules.** No game art or characters. Draw categories as plain bars and the crowd as dots. Small text under the views: "Invented creator. Categories are assumed independent; real players' choices are correlated, which usually lowers M_eff further."
