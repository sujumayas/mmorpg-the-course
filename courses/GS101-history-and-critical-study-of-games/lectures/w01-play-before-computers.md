# GS101 · Week 01 — Play before computers: board games, sport, ritual

**Why this matters:** Most of the problems you will solve as a designer were first solved with sticks, stones and a painted board. Ancient randomizers, race tracks and wargames already show the trade-offs you will meet in loot tables, movement systems and simulations. This week gives you a method for reading any game as evidence about the people who made and played it.

**You will be able to:**
- Compute the outcome distribution of a set of two-sided lots (throwing sticks, tetrahedral dice, split sticks) and the average move it produces under a given scoring rule.
- Compare how Senet, the Royal Game of Ur and Yut Nori map the same random outcomes to different moves, and explain what each mapping does to play.
- Classify a game using Caillois's four categories and the paidia-ludus scale, and defend the classification with specific rules.
- Distinguish in writing between what the evidence shows about a historical game and what a modern reconstruction assumes.

**Before class:** Caillois, *Man, Play and Games* (1961 English translation), chapters 1 and 2, on the definition of play and the four categories (about 30 pages). Skim the British Museum's collection entry for the Royal Game of Ur board and its object description. Reread GD101 week 1 if you have already taken it.

**Prerequisites from earlier courses:** None. This is a first-semester course with no prerequisites. If you are taking them alongside, two lectures connect directly. [GD101 week 1, what is a game?](../../GD101-introduction-to-game-design/lectures/w01-what-is-a-game.md) covers the Suits, Salen & Zimmerman and Juul definitions and Huizinga's magic circle, so this lecture does not re-teach them. [MA102 week 6, the binomial distribution](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w06-binomial-crits-over-a-fight.md) gives the full theory behind the counting in section 2. You need only fractions here.

**Interactive:** [Throwing sticks](../examples/w01-throwing-sticks.html). Keep it open during section 2.

---

## 1. How we know anything about ancient games

A history of games has a strange problem. The oldest games survive as objects, and objects rarely come with rules. A board of thirty squares from an Egyptian tomb tells you the layout. It does not tell you how pieces moved, what counted as a win, or whether anyone cared who won.

Historians work with three kinds of evidence, and you should learn to name which one a claim rests on.

- **Artifacts.** Boards, pieces, dice, balls, courts. They show what existed and where. Senet boards survive from Egyptian tombs, including several from Tutankhamun's burial. Five gameboards came out of Leonard Woolley's excavation of the Royal Cemetery at Ur between 1922 and 1934.
- **Images and texts.** Tomb paintings, inscriptions, rule tablets. They show how people talked about a game. The earliest clear painting of Senet is in the mastaba (a flat-roofed tomb) of Hesy-Re, dated to about 2620 BCE.
- **Reconstructions.** Modern rules written by scholars who combine the other two kinds with guesswork. Most "ancient rules" you can buy today are reconstructions.

The third kind matters most for you, because it is the one people forget. When someone says "Senet was played like this," they are usually describing the rules proposed by the Egyptologist Timothy Kendall in the 1970s, or rules by R. C. Bell. Those reconstructions are careful and playable. They are also design work done by twentieth-century people. The Royal Game of Ur is a lucky exception. The British Museum curator Irving Finkel read a Babylonian clay tablet, written about 177 BCE by a scribe named Itti-Marduk-balāṭu, that describes a form of the game. Even so, the tablet is roughly 2,400 years younger than the oldest boards, so it tells us how the game was played late in its life, not at the start.

Keep one rule in mind for the whole course. **Every historical claim about a game should say what evidence it stands on.** "The board has 20 squares" is an artifact claim. "A throw of four lets you move four squares" is a text claim for Ur and a reconstruction claim for Senet. "Players found the game tense" is almost always an invention.

### Three roots of play

Before computers, organized play grew from at least three roots. They overlap, and most games draw on more than one.

**Board and table games** put a contest onto a surface with tokens. Senet (Egypt, boards from about 3100 BCE onward), the Royal Game of Ur (Mesopotamia, earliest boards about 2600 to 2400 BCE) and later families such as mancala, Go and chess belong here. They are portable, they can be played by two people in a small space, and many of them use a randomizer.

**Sport** puts the contest in the body. The Mesoamerican ballgame is the longest-documented example. Solid rubber balls from the site of El Manatí in Mexico date to about 1700 to 1600 BCE, and the oldest known ballcourt, at Paso de la Amada, to about 1400 BCE. A form of it, ulama, is still played in parts of Mexico.

**Ritual** places play inside religion or ceremony. Here the evidence needs the most care. By Egypt's New Kingdom, Senet was tied to the passage of the soul through the underworld, and chapter 17 of the Book of the Dead refers to the deceased playing the game. The Mesoamerican ballgame is famously linked to human sacrifice, but the archaeological association appears only from the Classic era onward, is strongest among the Classic Veracruz and Maya cultures, and was not universal. "Losers were sacrificed" is a popular story that goes well beyond what the evidence supports for most times and places.

Notice the pattern in both cases. A game did not start as ritual and then become entertainment, or the reverse. The same activity carried different meanings at different times, and a history that picks one meaning is flattening the record.

## 2. Worked example: four sticks, one curve

### The hook

Three games from three continents and three millennia share a surprising piece of equipment. Egyptian Senet players threw four flat sticks, each painted on one side. Players of the Royal Game of Ur threw four pyramid-shaped dice with two of their four tips marked. Korean families still play Yut Nori at the new year by throwing four sticks, flat on one side and rounded on the other.

In every case the randomizer is four objects that each land one of two ways. And yet the games feel different. A throw of "nothing" is the worst result in Ur, you do not move at all. In Senet, as Kendall reconstructed it, and in Yut, the same "nothing" throw is the best result in the game. Why would designers who never met each other build the same machine and then disagree about what its rarest output means?

### The model

Call each stick or die a **lot**: an object that lands one of two ways. Let:

- `n` be the number of lots thrown (4 in all three games).
- `p` be the chance that one lot lands marked side up. For a fair lot, `p = 1/2`.
- `k` be the number of lots that land marked side up, from 0 to `n`.

The chance of seeing exactly `k` marked lots is:

```
P(k) = C(n, k) × p^k × (1 − p)^(n − k)
```

`C(n, k)` is the number of ways to choose which `k` of the `n` lots are marked. For four lots it is 1, 4, 6, 4, 1 for `k = 0` to 4. This is the binomial distribution, which MA102 week 6 derives in full. For fair lots every one of the 16 possible landings is equally likely, so you can count by hand.

The game then applies a **scoring rule** `m(k)`, a table that turns the count into a move. The randomizer is the same everywhere. The scoring rule is where the designer speaks.

- **Royal Game of Ur (Finkel's reading of the Babylonian tablet):** move `k` squares. A throw of 0 means no move.
- **Senet (Kendall's reconstruction):** move `k` squares for `k = 1` to 4. A throw of 0 marked sides (all four sticks black side up) moves 5.
- **Yut Nori (traditional rules):** count flat sides up. One flat is *do*, move 1. Two is *gae*, move 2. Three is *geol*, move 3. Four flat is *yut*, move 4. Zero flat, all four rounded sides up, is *mo*, move 5. Throwing *yut* or *mo* earns another throw.

The average move per throw is the **expected move**:

```
E[m] = Σ P(k) × m(k)     for k = 0 … n
```

### Numbers you can check

With fair lots, `P(k)` for `k = 0, 1, 2, 3, 4` is `1/16, 4/16, 6/16, 4/16, 1/16`, or 6.25%, 25%, 37.5%, 25% and 6.25%.

| Marked lots `k` | Ways | Chance | Ur move | Senet (Kendall) move | Yut move |
|---|---|---|---|---|---|
| 0 | 1 | 6.25% | 0 | 5 | 5 (*mo*) |
| 1 | 4 | 25% | 1 | 1 | 1 (*do*) |
| 2 | 6 | 37.5% | 2 | 2 | 2 (*gae*) |
| 3 | 4 | 25% | 3 | 3 | 3 (*geol*) |
| 4 | 1 | 6.25% | 4 | 4 | 4 (*yut*) |
| **Expected move** | | | **2.00** | **2.3125** | **2.3125** per throw |

Check the Ur figure yourself: `(0×1 + 1×4 + 2×6 + 3×4 + 4×1) / 16 = 32 / 16 = 2`. For Senet and Yut, the only change is that the `k = 0` row pays 5 instead of 0, which adds `5 × 1/16 = 0.3125`.

Yut's extra throw changes the picture again. A throw of *yut* or *mo* happens with chance `2/16 = 1/8`, and then you throw again, and possibly again. The expected total move per turn is the expected move per throw divided by the chance that the chain stops:

```
E[turn] = E[m] / (1 − 1/8) = 2.3125 × 8/7 ≈ 2.64
```

Three rules built on identical equipment produce three different paces: 2.00, 2.31 and 2.64 squares per turn.

Real lots are rarely fair. A curved stick or an uneven die may favour one side. Suppose the marked side comes up with `p = 0.6`. Then `P(k)` becomes 2.56%, 15.36%, 34.56%, 34.56% and 12.96%. The Ur expected move rises to `4 × 0.6 = 2.4` (the binomial mean is `n × p`). The Senet and Yut expected move rises to about 2.53, and the chance of the rare, lucrative 5 falls from 6.25% to 2.56%. Bias does not only speed the game up. It changes which results are rare.

### A visual you can move

Open `examples/w01-throwing-sticks.html`. The left panel shows the five raw outcomes as bars. The right panel shows the same throws after a scoring rule is applied. Switch between Ur, Senet and Yut and watch the left panel stay fixed while the right panel changes shape. Then drag the bias slider. Near `p = 0.5` the rare zero throw pays 5 in Senet about once in 16 throws. Push `p` toward 0.7 and the zero throw almost vanishes, so the big move disappears with it. The "throw 200 times" button lets you compare a simulated tally with the exact bars, which is what you will do by hand in the lab.

### Cross-game recognition

Once you see "count of successes, then a lookup table," you will find it far from ancient Egypt.

- **Pachisi**, from South Asia, uses cowrie shells, which land mouth up or mouth down. In one common six-shell table, 2 to 6 mouths up move 2 to 6 squares, but 1 mouth up moves 10 and 0 mouths up moves 25. The two rarest low counts get the biggest moves and an extra turn, called a grace. With fair shells, 0 up has chance `1/64 ≈ 1.6%`. It is Senet's jackpot idea, pushed further. Rules vary by region and family, so name your source when you quote a table.
- **Kriegsspiel**, the Prussian officers' wargame formalised by Georg von Reisswitz the younger in 1824, used specially made dice to decide casualties. The designer did not want the raw spread of a die. He wanted a table of combat results, so he built the table into the dice faces. The idea is the same: a random count, remapped to consequences the designer chose.
- **Modern loot tables** work the same way. A drop system rolls a number and looks up an item. MA102 later covers weighted tables in detail. The question you ask is the one this example asks: what does the raw roll look like, and what does the lookup do to it?

Rewrite each into the same form. Some randomizer produces a count or number with a known distribution. A table `m(·)` turns it into a game effect. Most of the design lives in `m`.

### Eyes-open design judgment

What do the three scoring rules buy, and what do they cost?

- **Ur's "0 means stand still"** keeps the game strictly proportional. More marked tips always means more movement. It also adds a small chance of a wasted turn, a moment of bad luck that punishes nobody in particular.
- **Senet's and Yut's "0 pays 5"** turns the rarest result into a jackpot. The distribution stops being a smooth hill and gets a spike at the far end. A player who is behind has a real hope of a big move, and every throw has a small chance of drama. The cost is that the scoring rule is harder to explain and seems arbitrary until you work out why it is there.
- **Yut's extra throw** makes the rare results rarer still in effect, because they chain. It raises the average pace and the spread together. A designer who adds it should expect longer comebacks and more swings.

The judgment a designer should make deliberately is this. The randomizer sets the shape of chance. The scoring rule sets which results feel good. Pick the rule for the feeling you want at the rarest outcome, then check the average so the game's length stays where you want it.

A caution for historians. It is tempting to say ancient designers "chose" the 5 for drama. We do not know their reasons. For Senet the 5 comes from a modern reconstruction. What you can say with confidence is what the rule does, because that follows from counting.

### Check the model

1. In Yut, how many of the 16 equally likely landings give *gae*? What is its chance?
2. You design a variant of Ur where a throw of 0 moves 6. What is the new expected move per throw?
3. If `p = 0.4` for a set of four lots, what is the chance of `k = 0`? Is the Senet jackpot now more or less common than with fair sticks?

<details>
<summary>Answers</summary>

1. `C(4, 2) = 6` landings, so `6/16 = 37.5%`.
2. `(6×1 + 1×4 + 2×6 + 3×4 + 4×1) / 16 = 38/16 = 2.375`.
3. `P(0) = 0.6^4 = 0.1296`, about 13%. Twice as common as with fair sticks.

</details>

## 3. Reading play: Caillois's four categories

The math tells you how a randomizer behaves. It does not tell you what kind of experience a game offers. For that you need a vocabulary, and the oldest widely used one comes from the French sociologist Roger Caillois. His book *Les jeux et les hommes* appeared in 1958 and in English as *Man, Play and Games* in 1961.

Caillois sorted play into four categories.

- **Agon**, competition. Players test one quality, such as speed, strength or skill, under equal conditions, and the better one wins. Chess, running races and the Mesoamerican ballgame are agon.
- **Alea**, chance. The player gives up control and waits for fortune. A pure lottery is alea. Caillois describes it as a surrender to destiny.
- **Mimicry**, make-believe. The player becomes someone else, as in theatre, children's pretend play or a masquerade.
- **Ilinx**, vertigo. The player seeks a pleasurable loss of stability, such as spinning until dizzy or riding a swing.

He crossed these with a second axis, from **paidia**, free improvised play, to **ludus**, play bound by explicit rules and increasing difficulty. Children spinning in a field is ilinx near the paidia end. A formal gymnastics routine with judges is closer to agon at the ludus end.

The categories are most useful in combination. Senet is a mixture of agon and alea. The sticks decide how far you may go, but you choose which piece to move. How much of each you get depends on the scoring rule. In section 2 you saw that a jackpot result increases the role of alea. By New Kingdom times Senet also had a strong mimicry layer, since the board could stand for the soul's journey.

Caillois also listed properties he thought all play shared. In his account, play is free, separate from ordinary life, uncertain, unproductive, governed by rules, and make-believe. You will meet close relatives of this list in GD101 week 1, where Juul builds his classic game model partly from Caillois and Huizinga. This course uses the list differently. For a historian, each property is a question to ask of a specific game at a specific time. Was Senet play "unproductive" when it was placed in a tomb to help its owner in the afterlife? Was the ballgame "separate from ordinary life" when rulers used it in public ceremony? The honest answer is often "partly," and saying why is the work of criticism.

### Where Caillois struggles

Two weaknesses are worth knowing. First, he wrote before video games, so he never faced games where one system mixes all four categories at once. A modern MMO raid is agon between the group and the boss, alea in its loot, mimicry in the character you play, and occasionally ilinx in its spectacle. Second, the "unproductive" property fits poorly with gambling, professional sport and, later in this course, games with real-money economies. Caillois handled gambling by saying it moves money around without creating anything. Whether that is still convincing when a game's currency trades for real money is a question MMO304 takes up.

## 4. Games as arguments and tools

Some pre-digital games were built to change how their players thought. Two examples set up threads this course follows for the rest of the semester.

### Kriegsspiel: the game as simulation

In 1812 the Prussian officer Georg Leopold von Reisswitz presented King Frederick William III with a wargame on a table of terrain tiles. His son, Georg Heinrich von Reisswitz, turned it into a practical training tool by 1824. Two changes made it work. Combat results came from dice and tables rather than argument. An umpire stood between the players, took written orders and revealed only what each side could see. The Prussian king ordered sets for the army's regiments, and Kriegsspiel became the first wargame widely adopted by a military for training.

Three ideas enter game history here. A game can model a real system (war) with numbers. Hidden information can be managed by a referee. And a game can be judged by whether it teaches something true. The first two lead through hobby wargames to Dungeons & Dragons, which this course reaches in week 6. The third is the root of every "serious game" argument you will hear.

### The Landlord's Game: the game as argument

In 1904 Elizabeth Magie received US patent 748,626 for The Landlord's Game. She designed it to show how private ownership of land concentrates wealth, following the economist Henry George. It came with two sets of rules. Under the monopolist rules, players tried to own property and ruin each other. Under the anti-monopolist rules, later called "Prosperity" rules, wealth created was shared and the game rewarded everyone when the poorest player had doubled their starting money. Home-made variants spread for years. In 1935 Parker Brothers, which had just bought Charles Darrow's Monopoly, also bought Magie's later patent for $500, then promoted Darrow's version.

Read that history critically. The version that became famous kept the monopolist rules, the ones Magie wrote to demonstrate a problem, and dropped the alternative she offered as a solution. A game built to criticise a system became a best-selling celebration of it. This is the first case in the course of a question you will ask again and again. Does a game's argument live in its rules, in its fiction, or in how players choose to play it?

## 5. A first method for close reading

One outcome of this course is a critical close reading of a game. You will write two. Here is the method in its first form. It grows over the semester.

1. **Describe before you judge.** List the components, the rules and the win condition. Say which you know from artifacts, texts or reconstructions.
2. **Find the machine.** Pick one rule or system and work out what it does, as you did for the throwing sticks. Numbers beat adjectives.
3. **Name the experience.** Use a vocabulary, such as Caillois's categories, to say what kind of play the machine produces.
4. **Place it in context.** Who made it, for whom, with what materials and what purpose. What did the context allow or forbid?
5. **Make one claim.** A close reading argues something a reader could disagree with. "Kendall's jackpot rule shifts Senet from agon toward alea" is a claim. "Senet is an interesting old game" is not.

Step 2 is what makes this program's version of criticism different. You are designers. When you read a game, you should be able to point at the rule that causes the effect you describe.

## In-class activity (25 min)

In groups of three, play two short games of the Royal Game of Ur using Finkel's rules and the printed board provided (or the board drawn on paper, 20 squares in the standard layout with five rosettes). The board and its rosettes are artifact evidence. The route pieces follow and the rule that a rosette grants another throw are modern conventions, and Finkel's and Bell's versions differ, so write down which one your group uses. Use four coins as lots. Heads counts as a marked tip.

1. Play one game with Ur scoring (0 means no move). Tally every throw on a sheet.
2. Play a second game with Senet-style scoring (0 moves 5). Tally again.
3. Compare your two tallies with the table in section 2. How many throws of 0 did you see? What did the rule change do to the game's length and to comebacks?
4. Write one sentence classifying each version using Caillois's categories, and one sentence of evidence for it from your play.

Expected output: two tally sheets, the game lengths in turns, and a four-sentence comparison.

## Common misconceptions

- **"We know the rules of Senet."** We know the board and the throwing sticks. The popular rules are modern reconstructions, mainly Kendall's. The Royal Game of Ur has a surviving rule text, but a late one.
- **"The losers of the Mesoamerican ballgame were always sacrificed."** The link to sacrifice appears late in the archaeological record and was strongest in particular cultures. The game was played for about three thousand years in many forms.
- **"Four fair sticks give each result the same chance."** They do not. Two marked out of four is six times as likely as four out of four, because there are six ways to get it and only one way to get four.
- **"Monopoly was designed to celebrate capitalism."** Its ancestor was designed to criticise land monopoly, and it shipped with an alternative rule set to show the other side.

## Check yourself

1. A game uses five fair two-sided lots and moves the number of marked lots, except that 0 moves 6. What is the chance of the 6? What is the expected move?
2. In Yut, a family decides that only *mo* earns an extra throw, not *yut*. What is the new expected move per turn?
3. A museum label says "Players of this game moved according to the throw of four sticks." Is that an artifact, text or reconstruction claim for Senet? What would you need to see to call it a text claim?
4. Classify Kriegsspiel using Caillois's categories. Which rule gives it the most alea?

<details>
<summary>Answers</summary>

1. `P(0) = (1/2)^5 = 1/32 ≈ 3.1%`. For `k = 1` to 5 the move is `k`, and the mean of `k` for five fair lots is `5 × 0.5 = 2.5`. The 0 row adds `6 × 1/32 = 0.1875`. Expected move `≈ 2.69`.
2. The per-throw expectation stays 2.3125. The chance of a chained throw is now `1/16`, so `E[turn] = 2.3125 / (15/16) ≈ 2.47`.
3. It rests on artifacts (sticks found with boards) plus reconstruction. A text claim needs an Egyptian text or image that shows the sticks being used for moves.
4. Mainly agon (officers compete in command decisions) with mimicry (they play commanders in a war that is not happening). The combat dice supply alea. The umpire's hidden-information role adds uncertainty without chance.

</details>

## Lab / assignment hook

[Lab 01, reconstructing an ancient game](../labs/lab01.md). You will throw lots 200 times, compare your tally with the model, play two reconstructed rule sets, and write a 500-word close reading that makes one claim about how a scoring rule shapes play. This is also practice for the first graded close reading.

## Sources

- Wikipedia, "Royal Game of Ur" (accessed September 2026). Boards dated about 2600 to 2400 BCE; Woolley's excavation 1922 to 1934; four tetrahedral dice with two marked tips; seven pieces each; the route and the extra throw on a rosette as modern reconstructions (Bell's and Finkel's routes differ); Finkel's reading of the tablet by Itti-Marduk-balāṭu, about 177 BCE, published in the early 1980s.
- Wikipedia, "Senet" (accessed September 2026). Hesy-Re painting about 2620 BCE; possible First Dynasty boards about 3100 BCE; 30 squares in three rows of ten; four throwing sticks; Kendall's scoring with all-black counting 5; link to chapter 17 of the Book of the Dead in the New Kingdom; boards in Tutankhamun's tomb.
- Kendall, T. (1978). *Passing Through the Netherworld: The Meaning and Play of Senet, an Ancient Egyptian Funerary Game*. Kirk Game Company. The reconstruction cited above.
- Bell, R. C. (1979). *Board and Table Games from Many Civilizations*, rev. ed. Dover. An alternative Senet reconstruction.
- Wikipedia, "Pachisi" (accessed September 2026). Six- and seven-cowrie scoring tables with grace throws; the six-shell table is used above.
- Wikipedia, "Yut" (accessed September 2026). Played by families especially at Seollal and Jeongwol Daeboreum; four split sticks; *do*, *gae*, *geol*, *yut*, *mo* moving 1 to 5; extra throw on *yut* or *mo*; 29-station board.
- Wikipedia, "Mesoamerican ballgame" (accessed September 2026). El Manatí balls about 1700 to 1600 BCE; Paso de la Amada court about 1400 BCE; sacrifice association from the Classic era, strongest in Classic Veracruz and Maya cultures; modern ulama.
- Caillois, R. (1958). *Les jeux et les hommes*. Gallimard. English translation *Man, Play and Games* (1961). Agon, alea, mimicry, ilinx; paidia and ludus; six properties of play.
- Wikipedia, "Kriegsspiel" (accessed September 2026). Reisswitz father 1812 and son 1824; combat dice; umpire; adoption by the Prussian army.
- Wikipedia, "The Landlord's Game" (accessed September 2026). Magie's 1904 US patent 748,626; Georgist purpose; monopolist and anti-monopolist rules; sale of the later patent to Parker Brothers in 1935 for $500.
- Juul, J. (2003). "The Game, the Player, the World: Looking for a Heart of Gameness." Referenced for the link between Caillois and the classic game model; see GD101 week 1.

## Interactive spec: examples/w01-throwing-sticks.html

**Purpose.** Show that the same randomizer (n two-sided lots) produces one fixed distribution, and that the scoring rule, not the equipment, decides which results are rare and valuable.

**The one insight the visual must make obvious.** Switching the scoring rule changes the right-hand chart and the expected move while the left-hand chart does not move. The rare zero throw becomes a spike at 5 under Senet or Yut rules.

**Layout.** Two linked bar charts side by side on desktop, stacked on mobile.
- Left, "Raw throw": bars for `k = 0 … n`, height `P(k)`, labelled with the percentage to one decimal and the count of ways `C(n,k)`.
- Right, "Move after scoring": bars for each distinct move value, height = sum of `P(k)` for all `k` that map to that move. Label each bar with the move and the percentage.
- Below the charts, a numbers panel: expected move per throw `E[m]`, chance of an extra throw `q`, expected move per turn `E[m] / (1 − q)` (show "n/a" if `q = 0`), and the variance of the move per throw.

**Controls.**
- Scoring rule radio group: "Ur (Finkel)", "Senet (Kendall)", "Yut Nori", "Custom".
  - Ur: `m(k) = k`, `m(0) = 0`, no extra throw.
  - Senet: `m(k) = k` for `k ≥ 1`, `m(0) = 5`, no extra throw.
  - Yut: `m(k) = k` for `k ≥ 1` (k counts flat sides), `m(0) = 5`, extra throw when `k = 4` or `k = 0`.
  - Custom: a small editable table of `m(k)` values (integers −2 to 10) and a checkbox per row for "extra throw".
- Lots `n`: slider 2 to 7, default 4. For Ur, Senet and Yut presets with `n ≠ 4`, keep `m(k) = k` for `k ≥ 1` and the preset rule for `k = 0`; extra throws for Yut occur at `k = n` and `k = 0`.
- Bias `p`: slider 0.30 to 0.70, step 0.01, default 0.50. Label "chance one lot lands marked (or flat) side up".
- "Throw 200 times" button: simulates 200 throws, overlays tally bars (outlined) on the left chart and the move tally on the right, and shows the observed mean move next to `E[m]`. A "Clear" button removes the overlay.

**Formulas.**
- `P(k) = C(n,k) p^k (1−p)^(n−k)`
- `E[m] = Σ P(k) m(k)`; `Var = Σ P(k) m(k)² − E[m]²`
- `q = Σ P(k)` over extra-throw rows; `E[turn] = E[m] / (1 − q)`

**Test values (n = 4).**
- `p = 0.5`: `P = 6.25%, 25%, 37.5%, 25%, 6.25%`. Ur `E[m] = 2.000`. Senet `E[m] = 2.3125`. Yut `E[m] = 2.3125`, `q = 12.5%`, `E[turn] = 2.643`.
- `p = 0.6`: `P = 2.56%, 15.36%, 34.56%, 34.56%, 12.96%`. Ur `E[m] = 2.400`. Senet `E[m] = 2.528`. Yut `q = 15.52%`, `E[turn] = 2.992`.
- Ur variance at `p = 0.5` is `1.000` (binomial `n p (1−p)`).

**Accessibility and style.** Bars keyboard-focusable with the numbers readable by screen readers. Use the shared tokens. Draw lots as plain rectangles or tetrahedra outlines, no museum images. First screen shows the Senet rule at `p = 0.5` so the spike at 5 is visible immediately.
