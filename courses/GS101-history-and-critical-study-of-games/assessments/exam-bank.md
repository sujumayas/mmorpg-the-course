# GS101 · Exam bank

GS101 has no written exam. The grade comes from the timeline project (25%), two close readings (40%) and the final essay (35%). This bank is quiz, practice and viva material, used in three ways.

- **Weekly quizzes.** Tutors draw two or three questions from the week just taught for a 10-minute check at the start of the lab. Quizzes are formative. The score is feedback and does not count toward the grade.
- **Practice.** Work through any week before its lab. Every numeric answer shows the full working, so you can find where your method went wrong.
- **Viva at the final presentation.** In week 15 each student presents the final essay and then answers a five-minute viva, marked as part of the essay grade (see [final-essay-brief.md](final-essay-brief.md)). The assessor picks two questions tagged "apply", swaps the question's case for the student's own essay game, and asks the student to answer about that game. The viva prompts at the end of this file show the pattern. Tutors may also use them in the short follow-up conversation that the [close readings brief](close-readings-brief.md) allows.

**How to read the tags.** Each question starts with `[Weeks · type · mode]`.

- Type is one of **compute** (produce a number with a lecture model), **explain** (state and use a concept), **design** (propose a rule, definition or artifact that meets a stated goal) or **critique** (judge a claim, source or reading).
- Mode is **apply** when the question gives a case the lectures did not work through, so you must carry a model or framework to it. Mode is **recall** when it checks a definition or result from the lecture itself. 59 of the 61 questions are apply.

The games in the questions are either invented for this bank (and say so) or are games the lectures already discuss, used only with the facts the lectures cite. Every number was recomputed for this bank.

**Coverage.**

| Week | Topic | Questions |
|---|---|---|
| 1 | Play before computers | 1 to 5 |
| 2 | Early computer games | 6 to 9 |
| 3 | Arcade era and the coin-op business model | 10 to 13 |
| 4 | Home consoles and the 1983 crash | 14 to 18 |
| 5 | Text adventures and MUD1 | 19 to 22 |
| 6 | The RPG lineage | 23 to 27 |
| 7 | The PC era and modding | 28 to 30 |
| 8 | 3D and the genre explosion | 31 to 33 |
| 9 | Graphical MMOs | 34 to 37 |
| 10 | World of Warcraft and the mass-market MMO | 38 to 41 |
| 11 | Free-to-play, mobile and live service | 42 to 45 |
| 12 | Indie games and the auteur designer | 46 to 49 |
| 13 | Ludology vs narratology | 50 to 53 |
| 14 | Games and representation | 54 to 57 |
| Several | Integrated cases | 58 to 61 |

---

## Week 1 · Play before computers

Lecture: [w01-play-before-computers.md](../lectures/w01-play-before-computers.md)

1. **[1 · compute · apply]** An invented race game uses three fair two-sided lots. A throw of `k` marked lots moves `k` squares for `k = 1` to 3. A throw of 0 moves 4 and earns another throw. (a) Give the chance of each `k`. (b) Compute the expected move per throw. (c) Compute the expected move per turn. (d) Compare with Ur-style scoring on the same three lots, where 0 means no move, and say what the zero rule does to the game.

   <details>
   <summary>Answer</summary>

   (a) With three fair lots there are 8 equally likely landings. `C(3, k)` is 1, 3, 3, 1, so `P(k)` is 1/8, 3/8, 3/8, 1/8 (12.5%, 37.5%, 37.5%, 12.5%).

   (b) `E[m] = (4 × 1 + 1 × 3 + 2 × 3 + 3 × 1) / 8 = 16 / 8 = 2.00`.

   (c) The extra throw happens with chance `q = 1/8`. `E[turn] = 2.00 / (1 − 1/8) = 2.00 × 8/7 ≈ 2.29`.

   (d) Ur-style scoring gives the binomial mean `n × p = 3 × 0.5 = 1.5`. The zero rule adds `4 × 1/8 = 0.5` per throw, a third more pace, and the chained throw adds more. It also turns the rarest-but-one result into the best one, so a player who is behind gets a real jackpot to hope for. That shifts the game toward alea in Caillois's terms.

   </details>

2. **[1 · compute · apply]** A reconstruction uses curved sticks. Tests show the marked side lands up only 40% of the time (`p = 0.4`). Use four sticks. (a) Compute `P(k)` for `k = 0` to 4. (b) Compute the expected move per throw under Ur scoring and under Kendall's Senet scoring. (c) Under Yut rules, where `k` counts flat sides and `p = 0.4` is the chance of a flat side, compute the expected move per turn. (d) Which result is now the rarest, and what does that do to the "jackpot" feel of the 0 throw?

   <details>
   <summary>Answer</summary>

   (a) `P(k) = C(4, k) × 0.4^k × 0.6^(4 − k)`. That gives 12.96%, 34.56%, 34.56%, 15.36% and 2.56% for `k = 0` to 4.

   (b) Ur: the binomial mean is `4 × 0.4 = 1.60`. Senet: add `5 × 0.1296 = 0.648` for the 0 row, so `E[m] = 2.248`.

   (c) Yut has the same per-throw moves as Senet, so `E[m] = 2.248`. The extra throw comes on `k = 0` or `k = 4`, so `q = 0.1296 + 0.0256 = 0.1552`. `E[turn] = 2.248 / (1 − 0.1552) ≈ 2.66`.

   (d) The rarest result is now `k = 4` (2.56%), which moves only 4. The 0 throw that pays 5 happens about one throw in eight, twice as often as with fair sticks. The big move stops being a rare miracle and becomes a routine event. Bias did not only speed the game up. It changed which result is special, which is the lecture's point that the scoring rule and the equipment together decide what feels rare.

   </details>

3. **[1 · explain · apply]** A museum label for an invented find, "the Tell Hamra board", makes five claims. (a) The board has three rows of 12 holes and was found in a grave. (b) A carved relief from the same site and period shows two seated people with the board between them and a heap of knucklebones. (c) Pieces raced around the holes, moving by the throw of four knucklebones. (d) The game was used to settle disputes between families. (e) Players found the last row tense. Classify each claim as an artifact claim, an image or text claim, a reconstruction, or an invention. Then say what evidence would turn (c) into a text claim.

   <details>
   <summary>Answer</summary>

   (a) Artifact claim. The board and its find-spot are physical evidence. (b) Image claim. The relief shows the board and knucklebones together, which is evidence that they were used together, not of how. (c) Reconstruction. It combines the artifact and the image with a guess about movement. (d) Unsupported as stated. It could become a text claim if an inscription or document said so. As written it is an invention or at best a reconstruction. (e) Invention. No kind of evidence here records how players felt.

   To make (c) a text claim you would need a written source from the culture (a rule tablet, an inscription, a letter) that describes pieces moving by the count of knucklebones. The lecture's parallel is the Babylonian tablet Finkel read for the Royal Game of Ur, which exists, against Senet, for which the movement rules are Kendall's reconstruction.

   </details>

4. **[1 · explain · apply]** Classify two activities with Caillois's four categories and place each on the paidia to ludus scale. (a) Children spin in circles until dizzy, then race to a tree. There are no written rules and the first to touch the tree shouts that they won. (b) A card game tournament where each player opens sealed random packs at the table, builds a deck from them and plays timed rounds under a printed rulebook. Many players attend in costume. Support each category with one rule or feature.

   <details>
   <summary>Answer</summary>

   (a) Ilinx (the spinning seeks a pleasurable loss of balance) and agon (the race to the tree). It sits near the paidia end, since the rules are improvised and unwritten.

   (b) Agon (players compete under equal conditions and the better player usually wins), alea (the random packs decide what each player can build, and every draw is random), and mimicry (costumes, and the fiction of the cards). It sits near the ludus end, with a printed rulebook, timed rounds and rising difficulty through the bracket.

   The judgment the lecture asks for is the mix, not a single label. The random packs are where alea enters, just as the jackpot rule adds alea to Senet.

   </details>

5. **[1 · critique · recall]** A student writes: "Monopoly proves that board games celebrate capitalism." Use the history of The Landlord's Game to critique the claim, and say where a game's argument can live.

   <details>
   <summary>Answer</summary>

   Monopoly descends from Elizabeth Magie's Landlord's Game (US patent 748,626, 1904), which she designed to show how private land ownership concentrates wealth, following Henry George. It shipped with two rule sets. The monopolist rules let players ruin each other. The anti-monopolist ("Prosperity") rules shared created wealth. The famous commercial version kept the monopolist rules, which Magie wrote to demonstrate a problem, and dropped her alternative.

   So the claim confuses one surviving rule set with the purpose of the design. An argument can live in the rules (the rent rule concentrates money), in the fiction (property, landlords), or in how players choose to play. The same rules can support a celebration or a critique depending on which rule set ships and how players read it.

   </details>

## Week 2 · Early computer games

Lecture: [w02-early-computer-games.md](../lectures/w02-early-computer-games.md)

6. **[2 · compute · apply]** Tennis for Two's 1959 version offered a low-gravity setting. Use `g = 1.63` as a stand-in (illustrative, as the lecture notes), launch `vy = 6`, `dt = 0.1`. (a) Compute the height after steps 1, 2 and 3 with semi-implicit Euler and with explicit Euler. (b) Compare each with the exact height at `t = 0.3`. (c) How does the error compare with the Earth case in the lecture, and why? (d) What is the exact highest point?

   <details>
   <summary>Answer</summary>

   (a) Semi-implicit: `vy = 6 − 0.163 = 5.837`, `y = 0.584`. Then `vy = 5.674`, `y = 1.151`. Then `vy = 5.511`, `y = 1.702`. Explicit, position first with the old velocity: `y = 0.600`, then `1.184`, then `1.751`.

   (b) Exact `y(0.3) = 6 × 0.3 − 0.5 × 1.63 × 0.09 = 1.727`. Semi-implicit is 0.025 low, explicit 0.024 high.

   (c) On Earth at `t = 0.3` the errors were about ±0.147 (1.212 and 1.506 against 1.359). The error per step is proportional to `g × dt`, so cutting `g` to one sixth cuts the error to about one sixth. The update order still decides which side of the true curve you land on.

   (d) `vy² / (2g) = 36 / 3.26 ≈ 11.04` units, six times the Earth apex of 1.84.

   </details>

7. **[2 · compute · apply]** A Spacewar!-style ship starts at `(2, 0)` with velocity `(0, 0.7071)` around a star with `G = 1`. (That speed, `√(G / r)`, gives an exact circular orbit of radius 2.) Use `dt = 0.1`. (a) How strong is the pull at `r = 2` compared with `r = 1`? (b) Compute the distance from the star after one explicit step and after one semi-implicit step. (c) Which one moves outward, and what does that predict over many laps?

   <details>
   <summary>Answer</summary>

   (a) The pull is `1 / d²`, so at `d = 2` it is one quarter of the pull at `d = 1`.

   (b) Explicit, position first: `(2 + 0 × 0.1, 0 + 0.7071 × 0.1) = (2, 0.0707)`, distance `√(4 + 0.005) ≈ 2.0012`. Semi-implicit, velocity first: acceleration is `(−2 / 8, 0) = (−0.25, 0)`, so `vx = −0.025` and `vy = 0.7071`. Position becomes `(1.9975, 0.0707)`, distance ≈ 1.9988.

   (c) The explicit ship steps along the tangent and ends up outside the circle. It will keep spiralling out, as in the lecture's radius-1 table. The semi-implicit ship dips slightly inside, then wobbles back, so its orbit holds. The effect is smaller than at radius 1 because the step is a smaller fraction of the orbit, but the direction is the same.

   </details>

8. **[2 · design · apply]** Using the candidates table in the lecture (1947 device, Bertie the Brain, Nimrod, OXO, Tennis for Two, Spacewar!), write a definition of "video game" under which Tennis for Two is the first. Then name which earlier candidate your definition excludes and which criterion does the excluding, and name one reasonable criterion that would make Spacewar! first instead.

   <details>
   <summary>Answer</summary>

   One definition: "a game that runs on a computer of any kind, shows a moving picture on a screen that updates in real time, and was made mainly for play." Tennis for Two (1958) meets all three. The 1947 cathode-ray tube amusement device fails "runs on a computer" (analog circuits, not a computer). Bertie the Brain and Nimrod fail "picture on a screen" (light bulbs) and "made mainly for play". OXO fails "moving picture updated in real time", since it redraws a static board.

   Add "runs on a digital computer" and Spacewar! (1962, PDP-1) becomes first, since Tennis for Two used an analog computer. The lecture's point is that the historian states the criteria and shows what each includes rather than crowning one game.

   </details>

9. **[2, 3 · compute · apply]** An invented university lab in the 1960s owns a $60,000 minicomputer. Ten research groups each allow two hours of play a week, 40 weeks a year, for four years. (a) Charging the whole machine to play, what is the hardware cost per hour? (b) If a coin-op version had to recover that cost from three-minute games at those hours, what would each game need to cost? (c) Compare with the prices Galaxy Game and Pong charged, and say what this tells you about why the 1971 teams chose different hardware.

   <details>
   <summary>Answer</summary>

   (a) `10 × 2 × 40 × 4 = 3,200` hours. `$60,000 / 3,200 = $18.75` per hour.

   (b) A three-minute game is 1/20 of an hour, so `$18.75 / 20 ≈ $0.94` per game.

   (c) Galaxy Game charged 10 cents a game (or 25 cents for three) and Pong 25 cents. Even this generous usage would need a price four to nine times higher. That is why Galaxy Game could not be copied cheaply, and why Computer Space and Pong threw the computer out and used dedicated circuits. The cost per machine had to fall by orders of magnitude before pay-per-play worked. The charge in (a) is unfair, since the machine did other work, but it shows the scale.

   </details>

## Week 3 · Arcade era and the coin-op business model

Lecture: [w03-arcade-era-and-the-coin-op-business-model.md](../lectures/w03-arcade-era-and-the-coin-op-business-model.md)

10. **[3 · compute · apply]** An invented cabinet costs $3,000, charges $0.25 and averages 2.5-minute sessions. It is busy 80% of the time in a location open 12 hours a day, and the operator keeps half the cash box. Compute plays per day, revenue per hour, cash box per day, operator share per day and payback in days.

    <details>
    <summary>Answer</summary>

    Plays per day `= 0.8 × 12 × 60 / 2.5 = 230.4`. Revenue per hour `= 0.25 × 0.8 × 60 / 2.5 = $4.80`. Cash box per day `= 230.4 × $0.25 = $57.60`. Operator share `= $28.80` a day. Payback `= $3,000 / $28.80 ≈ 104` days.

    </details>

11. **[3 · compute · apply]** A student-union arcade has a different crowd from the lecture's bar: 70% novices (`S = 2`), 20% regulars (`S = 6`) and 10% experts (`S = 15`). Keep `d₀ = 1`, `p = $0.25`, `u = 0.75`, the 0.5-minute floor and the 30-minute cap. (a) Compute each group's session, the average `L` and revenue per hour for ramps `r = 0.5`, 1 and 2. (b) What share of the machine's busy time do the experts hold? (c) What does the result say about who the ramp is for?

    <details>
    <summary>Answer</summary>

    (a) Session `= min(30, max(0.5, (S − 1) / r))`.

    | `r` | Novice | Regular | Expert | Average `L` | Revenue per hour |
    |---|---|---|---|---|---|
    | 0.5 | 2.0 | 10.0 | 28.0 | 6.20 | $1.81 |
    | 1 | 1.0 | 5.0 | 14.0 | 3.10 | $3.63 |
    | 2 | 0.5 | 2.5 | 7.0 | 1.55 | $7.26 |

    Check the `r = 1` row: `0.7 × 1 + 0.2 × 5 + 0.1 × 14 = 3.1`, and `0.25 × 0.75 × 60 / 3.1 ≈ $3.63`.

    (b) At `r = 1` the experts hold `0.1 × 14 / 3.1 ≈ 45%` of the busy time, though they are only 10% of the players. No floor or cap binds in these three rows, so every session scales by the same factor and the share stays 45% at every ramp.

    (c) One player in ten holds almost half the machine. The ramp's money comes from cutting those long sessions. Novices already end their games in a minute or two, so a steeper ramp costs them fun for little gain. The lecture's advice, "ramp the experts, protect the novices", follows directly.

    </details>

12. **[3 · critique · apply]** An invented press kit, published in 2002 for a company's anniversary, says: "In 1982 our cabinet Zenith Blaster earned more than the ten top films of that year combined." Apply the four source questions from the lecture and rewrite the claim so a historian could use it.

    <details>
    <summary>Answer</summary>

    Who counted: the manufacturer, twenty years later, in marketing material. It has a reason to round up. What was counted: probably quarters in cash boxes across all cabinets (gross takings), which is not money to the manufacturer and not profit. Over what period: "in 1982" may be one year or may be a running total. Compared with what: box-office takings or studio revenue? The comparison class is not given.

    Usable version: "The manufacturer's 2002 anniversary press kit claimed that Zenith Blaster cabinets took in more than the top ten films of 1982 combined. The kit does not say whether this counts gross coin takings or company revenue, or how the film figure was measured." Better still, find the period report the kit relied on.

    </details>

13. **[3 · design · apply]** You are converting an invented arcade game to a home cartridge sold once at a fixed price. (a) Which variable in the revenue model disappears, and why does that change the designer's incentive about `L`? (b) Name two of the arcade traits from the lecture (learnable in seconds, a ramp inside the session, loss built into the structure, a reason to put in another coin) that you would change, and what you would put in their place.

    <details>
    <summary>Answer</summary>

    (a) The price per session `p` disappears. Revenue is now copies sold times price, so the publisher earns nothing extra from short sessions and has no reason to cut `L`. The lecture notes that home games grew longer for this reason. The new pressure is making the box worth buying, which favours length and replay value.

    (b) Two reasonable changes. Replace "loss built into the structure" (lives that end the session) with saves, continues or checkpoints, since a lost session no longer earns a coin. Replace "a reason to put in another coin" with long-term goals, such as levels to unlock or a score to beat over weeks. You might keep "learnable in seconds" if the box is sold in shops to strangers, and keep a gentler ramp so the game still ends each sitting. Any answer that ties each change to the missing `p` is acceptable.

    </details>

## Week 4 · Home consoles and the 1983 crash

Lecture: [w04-home-consoles-and-the-1983-crash.md](../lectures/w04-home-consoles-and-the-1983-crash.md)

14. **[4 · compute · apply]** Run the shelf model with the lecture's defaults (demand 100 then 200 and flat, shipments 100 then 275, in thousand cartridges, `P = $35`, `b = $5`) but with a bargain share `c = 0.25`. As in the lecture, revenue comes out in $ thousands. Compute years 3 to 5: bin sold, new sold, unsold stock and revenue. Compare with the `c = 0.5` table and say what `c` controls and what it does not.

    <details>
    <summary>Answer</summary>

    Year 2 ends as before with `U = 75` and $7,000.

    Year 3: bin sold `= min(75, 0.25 × 200) = 50`. New sold `= min(275, 200 − 50) = 150`. `U = 75 − 50 + (275 − 150) = 150`. Revenue `= 35 × 150 + 5 × 50 = $5,500`.

    Year 4: bin sold `= min(150, 50) = 50`, new sold 150, `U = 225`, revenue $5,500. Year 5: same flows, `U = 300`, revenue $5,500.

    At `c = 0.5` revenue settles at $4,000 (−43% from the peak). At `c = 0.25` it settles at $5,500 (−21%). The pile grows to 300 in both cases. So `c` controls how much the unsold stock hurts full-price sales, not whether stock piles up. The pile comes from the gap between supply growth and demand growth.

    </details>

15. **[4 · compute · apply]** Rewrite the shelf model for an invented MMO's auction house. Crafters want 1,000 ore a day. Before a patch, 1,000 ore enters the game a day. From day 2 a drop-rate change puts 1,400 a day into the game while demand stays flat. Listings sell at 20 gold, and ore nobody buys can always be sold to a vendor for 2 gold. Treat `c = 0.5`. (a) Compute days 1 to 4: new sold, bin sold, unsold stock and sellers' total income. (b) Now add a daily gathering cap that limits entry to 1.1 times demand. Recompute day 4. (c) What does (b) tell you about gates with headroom above 1?

    <details>
    <summary>Answer</summary>

    (a)

    | Day | Enters `S` | New sold | Bin sold | Unsold `U` after | Income (gold) |
    |---|---|---|---|---|---|
    | 1 | 1,000 | 1,000 | 0 | 0 | 20,000 |
    | 2 | 1,400 | 1,000 | 0 | 400 | 20,000 |
    | 3 | 1,400 | 600 | 400 | 800 | 12,800 |
    | 4 | 1,400 | 500 | 500 | 1,200 | 11,000 |

    Day 3: bin sold `= min(400, 500) = 400`, new sold `= min(1,400, 600) = 600`, `U = 400 − 400 + 800 = 800`, income `= 20 × 600 + 2 × 400 = 12,800`.

    Income falls 45% with demand unchanged. The vendor price is the $5 bin.

    (b) With the cap, 1,100 enter a day. Day 2 leaves 100 unsold. Day 3: bin 100, new 900, `U = 200`, income 18,200. Day 4: bin 200, new 800, `U = 300`, income 16,400.

    (c) The gate slows the damage but does not stop it. With flat demand, any headroom above 1 adds a fixed surplus every day, so the pile keeps growing (by 100 a day here). An MMO designer also needs a sink that removes surplus, which is the week 4 cross-game point about auction houses.

    </details>

16. **[4 · critique · apply]** A documentary says: "The 1983 crash wiped out 97% of the games industry worldwide." Using only facts from the lecture, identify what is wrong, compute the worldwide drop the lecture's figures imply, and rewrite the sentence.

    <details>
    <summary>Answer</summary>

    The 97% figure is US home video game sales, from about $3 billion in 1982 to about $100 million in 1985 (`1 − 0.1 / 3 ≈ 97%`). It is not a worldwide figure and it excludes arcades and computers. The lecture gives a worldwide estimate for arcade, console and computer games of about $42 billion in 1982 and about $14 billion by 1985, a fall of `1 − 14 / 42 ≈ 67%`. Japan launched the Famicom and the SG-1000 on 15 July 1983, in the middle of the US collapse, and Europe's home computers were surging.

    Rewrite: "US home video game sales fell about 97% between 1982 and 1985. Estimates of the worldwide market for arcade, console and computer games show a fall of about two thirds over the same years, and console sales in Japan grew."

    </details>

17. **[4 · explain · apply]** The lecture gives a six-step causal chain for the crash. For each of these Nintendo rules, name the step it acts on and the shelf-model variable it controls: (a) at most five games per publisher per year, (b) a minimum order of 10,000 cartridges, (c) the 10NES lockout chip, (d) the Seal of Quality. Which step did none of them fix directly?

    <details>
    <summary>Answer</summary>

    (a) Step 2, supply outrunning demand. It caps `S` per publisher. (b) Steps 2 and 3. It limits `S` to publishers with cash, and a publisher that can pay for 10,000 cartridges is less likely to fold and leave stores unable to return stock. (c) Step 1, the open platform. It stops unlicensed cartridges from running, so `S` passes through Nintendo's gate. (d) Step 6, retailer trust. It signals to retailers and buyers which games passed the gate, which makes the bin less likely to fill with poor games.

    None of them fixes step 5, home computers taking demand. That was a demand-side change Nintendo could not control with licensing. Any answer that ties each rule to `S` or to the chain with a reason is acceptable.

    </details>

18. **[4, 12 · design · apply]** An invented console maker is opening a digital store for small studios. Propose one rule that controls `S`, state what it buys and what it costs, and say what the "bin" is in a digital store. Use Nintendo (1985) and Steam Direct (2017) as the two ends of the range.

    <details>
    <summary>Answer</summary>

    Example: a quarterly release slot per studio plus a short review for crashes and misleading store pages, but no review of the game's idea. It buys some control over `S` and a quality floor that makes the front page trustworthy. It costs speed and freedom for studios, and it gives the platform power over who can publish, the cost the lecture names for Nintendo's five-games-a-year rule. It sits between Nintendo's tight gate and Steam Direct's $100 fee refunded after $1,000 in sales.

    In a digital store there is no physical bin, because copies cost nothing to store. The bin is attention. A game nobody sees is unsold stock, and deep discounts play the part of the $5 bin. Any rule is acceptable if the answer names what it controls, who gains and who loses.

    </details>

## Week 5 · Text adventures and MUD1

Lecture: [w05-text-adventures-and-mud1.md](../lectures/w05-text-adventures-and-mud1.md)

19. **[5 · compute · apply]** An invented shared world holds `V = 8,000` points of treasure per reset. A player alone earns `f = 500` points an hour, and the reset period is `L = 3` hours. Keep MUD1's 102,400-point wizard threshold. (a) Compute the crossover population `N*`. (b) For 4, 10 and 16 players, compute income, hours to make wiz and the dry share of each period.

    <details>
    <summary>Answer</summary>

    (a) `N* = V / (f × L) = 8,000 / 1,500 ≈ 5.33` players.

    (b)

    | Players | Income (points/hour) | Hours to wiz | Dry share |
    |---|---|---|---|
    | 4 | 500 | 204.8 | 0% |
    | 10 | 266.7 | 384.0 | 46.7% |
    | 16 | 166.7 | 614.4 | 66.7% |

    For 10 players: `income = min(500, 8,000 / 30) = 266.7`, wiz `= 102,400 / 266.7 = 384` hours, dry share `= 1 − 8,000 / (10 × 500 × 3) = 46.7%`.

    </details>

20. **[5 · design · apply]** An invented MMO has one fishing spot. At peak hours about 40 players fish there. A player alone catches `f = 30` fish an hour, and the spot restocks every `L = 0.5` hours. (a) What stock `V` per restock makes `N* ≥ 40`? (b) Give a second way to reach the same `N*` with a smaller stock per restock. (c) Name one thing each design choice gives up, using McQuaid's or Koster's argument.

    <details>
    <summary>Answer</summary>

    (a) `N* = V / (f × L) ≥ 40` gives `V ≥ 40 × 30 × 0.5 = 600` fish per restock.

    (b) Halve the period to `L = 0.25` hours and 300 fish per restock gives the same `N* = 300 / (30 × 0.25) = 40`. The supply per hour (1,200 fish) is what matters. A third way is to make the spot per-player, which removes `N*` altogether.

    (c) A generous shared stock or a fast restock keeps the spot shared but removes the contest, so other anglers stop mattering and the spot's social life thins. Per-player fishing removes contention entirely, which is the change McQuaid argued harms a world's community and economy. Koster's answer would ask whether a private spot makes sense in the fiction. Any answer that states a cost to the shared world is acceptable.

    </details>

21. **[5 · explain · apply]** Apply Bartle's six properties (automated rules, one character per player, real time, shared, persistent, not the real world) to each case and say whether it is a virtual world. (a) A 100-player match that ends when one player is left and resets fully. (b) A text MUD hosted on a university server that has run without a reset of characters since 1995. (c) Four friends on a video call playing a tabletop role-playing game with a human referee. (d) A single-player open-world game that saves your progress.

    <details>
    <summary>Answer</summary>

    (a) Automated rules, one character each, real time, shared, not the real world. It fails persistence, since the world ends with the match. Not a virtual world.

    (b) All six. It is a virtual world.

    (c) Each player has a character, play is roughly real time, the world is shared and it is not the real world. It fails automated rules, because a human referee applies the rules, and persistence lives only in notes. Not a virtual world in Bartle's sense, which is why the lecture treats MUD1 as the step that put the D&D dungeon under automated rules.

    (d) Rules, character, real time, not real, and your save persists. It fails "shared". Not a virtual world.

    The definition is a tool for asking which design problems each case has. The match avoids long-term contention; the single-player game avoids all of it.

    </details>

22. **[5 · critique · apply]** A producer proposes doubling a server's population cap from 12 to 24 "to make the world feel alive". The server's main resource is the lecture's pool (`V = 5,000`, `f = 400`, `L = 2`). Compute income, hours to make wiz and the dry share at 12 and 24 players, and write a two-sentence reply to the producer.

    <details>
    <summary>Answer</summary>

    `N* = 6.25`. At 12 players: income `= 5,000 / 24 = 208.3`, wiz 491.5 hours, dry share 47.9%. At 24 players: income `= 5,000 / 48 = 104.2`, wiz `= 102,400 / 104.2 ≈ 983` hours, dry share `= 1 − 5,000 / (24 × 800) = 74.0%`.

    Reply: "Doubling the cap halves everyone's income from the pool and leaves the world empty of treasure three quarters of the time, so the extra players will spend most of their time competing with each other. If we want a busier world, we should raise `V` or shorten `L` with it, or decide which resources should be instanced."

    </details>

## Week 6 · The RPG lineage

Lecture: [w06-the-rpg-lineage-dnd-to-ultima-and-wizardry.md](../lectures/w06-the-rpg-lineage-dnd-to-ultima-and-wizardry.md)

23. **[6 · compute · apply]** Under the 3rd edition rule with the natural 1 and 20 clamps, a character with attack bonus +3 attacks a target with AC 17. A hit deals 8 damage. (a) What must they roll and what is the hit chance? (b) What are the hit chance and expected damage with advantage? (c) Compare advantage with a flat +5 bonus here.

    <details>
    <summary>Answer</summary>

    (a) `need = 17 − 3 = 14`. Faces 14 to 20 are seven faces, so `P = 7/20 = 35%`. Expected damage `= 0.35 × 8 = 2.8`.

    (b) `P_adv = 1 − 0.65² = 0.5775`, about 57.8%. Expected damage `= 0.5775 × 8 ≈ 4.62`.

    (c) A +5 bonus makes `need = 9`, twelve faces, 60%, expected damage 4.8. Here advantage adds 22.75 points and +5 adds 25, so +5 is slightly better. Advantage is worth the most near the middle of the range (55% becomes 79.75%) and less near the edges, as the lecture shows.

    </details>

24. **[6 · compute · apply]** An AD&D 2nd edition character has THAC0 12 and attacks a monster with descending AC −1. Convert both numbers to the 3rd edition form and compute the hit chance. Check with the 2e rule.

    <details>
    <summary>Answer</summary>

    `B = 20 − THAC0 = 8`. `AC = 20 − AC_2e = 20 − (−1) = 21`. `need = 21 − 8 = 13`. Faces 13 to 20 are eight faces, so `P = 40%`.

    Check with 2e: `THAC0 − AC_2e = 12 − (−1) = 13`. Same need, same 40%.

    </details>

25. **[6 · critique · apply]** A patch note for an invented RPG that uses the d20 rule says: "The new Ring of Aim gives +1 to hit. It is worth the same to every character." Test the claim against AC 15 for three characters with `B = −4`, `B = +12` and `B = +13`, and rewrite the note.

    <details>
    <summary>Answer</summary>

    `B = −4`: `need = 19`, 10% becomes 15%, a gain of 50% in expected damage. `B = +12`: `need = 3`, 90% becomes 95%, a gain of `5 / 90 ≈ 5.6%`. `B = +13`: already at the 95% ceiling, gain 0%.

    Each character gains the same 5 percentage points of hit chance between the clamps, so the note is right in absolute terms and wrong in relative terms. The ring is worth nine times as much to the weak character as to the strong one, and nothing to the character at the ceiling. Rewrite: "The Ring of Aim adds 5 points of hit chance, up to the 95% cap. It helps most when your hit chance is low."

    </details>

26. **[6 · compute · apply]** An invented action RPG uses a smooth hit formula `P = AR / (AR + DR)`, clamped to 5% and 95%, like the lecture's Diablo II case. A monster has `DR = 400`. (a) What attack rating gives 50%, 80% and 95%? (b) What happens to attack rating above the 95% value? (c) What design problem does this create for item bonuses?

    <details>
    <summary>Answer</summary>

    (a) 50%: `AR = DR = 400`. 80%: `AR / (AR + 400) = 0.8` gives `0.2 AR = 320`, so `AR = 1,600`. 95%: `0.05 AR = 380`, so `AR = 7,600`.

    (b) It adds nothing. The clamp holds the result at 95%.

    (c) Each step from 50% to 80% to 95% costs four times and then almost five times as much attack rating. Bonuses feel strong early and weak late, and a player past 7,600 against this monster gains nothing from further attack rating. The designer should check the "what +1 is worth" curve across the expected range of `AR` and `DR` so no stat falls into a dead zone by accident.

    </details>

27. **[6 · critique · apply]** A blog post says: "Dragon Quest is basically a copy of Ultima." Using the lecture's four critiques of family trees and its standard for a lineage claim, explain what is wrong and write a better claim.

    <details>
    <summary>Answer</summary>

    Trees hide the network. Horii played both Wizardry and Ultima, so a single parent is already wrong. Trees suggest single authors. Dragon Quest had Horii, Toriyama's art and Sugiyama's music. Trees suggest progress or copying. Horii set out to make the genre easy for console players who found those interfaces intimidating, so the design gave things up and added things. A good lineage claim names a specific feature, shows it in both works and cites evidence that the later designer knew the earlier one.

    Better: "Yuji Horii has said he played Wizardry and Ultima before designing Dragon Quest (Famicom, 1986). [Name one specific feature you can show in both games] appears in both, while Dragon Quest simplified the interface for console players." The specific feature must come from your own play or a cited source.

    </details>

## Week 7 · The PC era, strategy, simulation and modding

Lecture: [w07-the-pc-era-strategy-simulation-modding.md](../lectures/w07-the-pc-era-strategy-simulation-modding.md)

28. **[7 · compute · apply]** A class adds two invented cases to the lecture's six. Case X: host game 2014, mod 2015, the host's owner releases the standalone in 2019. Case Y: host game 2016, mod 2016, a different company releases a standalone in 2018. (a) Compute `L_M`, `L_S` and `L` for each and code the owner. (b) Recompute the median `L_S` for each owner group. (c) Does the lecture's pattern survive, and what kind of case would break it?

    <details>
    <summary>Answer</summary>

    (a) X: `L_M = 1`, `L_S = 4`, `L = 5`, host-owned. Y: `L_M = 0`, `L_S = 2`, `L = 2`, third-party.

    (b) Host-owned `L_S` values {1, 1, 4}, median 1. Third-party {3, 6, 10, 4, 2}, median 4.

    (c) The gap narrows from four years (1 against 5) to three (1 against 4), and both new cases cut against the pattern. It survives in the medians, but it is getting weaker. A few more fast third-party cases, or slow host-owned ones, would erase it. Remember also that every case in the table is a success, so the comparison says nothing about how often mods become products.

    </details>

29. **[7 · critique · apply]** Apply the lecture's three questions about "first" claims (by what definition, first to whom, what was upstream) to the claim "Aeon of Strife invented the MOBA", and write a version that survives all three.

    <details>
    <summary>Answer</summary>

    By what definition: if a MOBA is a real-time strategy game with base-building removed and one hero per player, you must check which of those features Aeon of Strife had. First to whom: Aeon of Strife was a StarCraft custom map. DotA (2003, Warcraft III) is the map that made the idea popular and that League of Legends and Dota 2 grew from. What was upstream: Aeon of Strife itself ran inside StarCraft, a commercial RTS with a map editor, so the idea sits inside the RTS genre.

    Surviving version: "Aeon of Strife, a StarCraft custom map, is the earliest step the sources name in the lineage that led to DotA (2003) and then to League of Legends (2009) and Dota 2 (2013)." A lineage table with dated links is a better answer than a single "first".

    </details>

30. **[7 · design · apply]** You run a studio about to ship a PC strategy game with a full map editor. Using the mod pipeline model and the Valve and Blizzard histories from the lecture, propose two decisions (licence terms, hiring, tools) and predict their effect on `L_M` and `L_S` for any successful mod. Name one cost of each.

    <details>
    <summary>Answer</summary>

    Example 1: ship the editor and an open data format on day one. This shortens `L_M`, as Warcraft III's bundled editor and Doom's open WAD files did. Cost: you lose control over what is built with your tools, including competitors' future products.

    Example 2: licence terms that give the studio first right to commercialize any mod made with the editor, plus a practice of hiring standout modders. This shortens `L_S` for mods that become products, as Valve's purchase of Counter-Strike did, and avoids Blizzard's outcome, where the most valuable idea built with its editor became two other companies' products. Cost: some modders will stay away if the studio claims rights over their work, so fewer mods get made.

    Any pair is acceptable if it names the lag it moves and a real cost.

    </details>

## Week 8 · 3D and the genre explosion

Lecture: [w08-3d-and-the-genre-explosion.md](../lectures/w08-3d-and-the-genre-explosion.md)

31. **[8 · compute · apply]** An invented console has a spec throughput of `R = 300,000` polygons a second. Assume efficiency `e = 0.4`. A game shows a detailed character and enemies costing `C = 1,500` polygons a frame, scenery density `ρ = 0.8` polygons per square metre and a 75° field of view. (a) Compute `P`, `P_world` and draw distance `d` at 30 fps. (b) Recompute at 60 fps. (c) By what fraction did `d` fall, and why is it more than the 29% the lecture found without fixed costs?

    <details>
    <summary>Answer</summary>

    75° is `75 × π / 180 ≈ 1.309` radians.

    (a) `P = 300,000 × 0.4 / 30 = 4,000`. `P_world = 2,500`. `d = √(2 × 2,500 / (0.8 × 1.309)) = √4,775 ≈ 69.1 m`.

    (b) `P = 2,000`. `P_world = 500`. `d = √(2 × 500 / 1.047) ≈ 30.9 m`.

    (c) `30.9 / 69.1 ≈ 0.45`, a fall of about 55%. The fixed cost comes off the top, so halving `P` cut the scenery budget from 2,500 to 500, a factor of five. The square root softens that to a factor of √5 ≈ 2.24 in distance. Without `C` the budget only halves and `d` falls by `1 − 1/√2 ≈ 29%`.

    </details>

32. **[8 · design · apply]** A team on the lecture's PlayStation assumptions (`R = 180,000`, `e = 0.5`, 30 fps, `C = 0`, `ρ = 0.5`, 90°) wants a 100 m draw distance. (a) Show that the budget cannot pay for it as set. (b) Find the field of view that would reach 100 m with everything else fixed, and the density that would reach it at 90°. (c) What does each option cost the player?

    <details>
    <summary>Answer</summary>

    (a) Area needed `= (θ / 2) × d² = 0.785 × 10,000 = 7,854 m²`. At `ρ = 0.5` that needs `P_world = 3,927` polygons, more than the 3,000 available.

    (b) Field of view: `θ = 2 × 3,000 / (0.5 × 10,000) = 1.2` radians, about 68.8°. Density: `ρ = 2 × 3,000 / (1.571 × 10,000) ≈ 0.38` polygons per square metre.

    (c) A narrow view makes players feel boxed in and hides threats at the sides. Thinner scenery makes the world emptier and less detailed. A third choice is to drop to 20 fps, which costs responsiveness. The lecture's judgment is that each of these buys distance with something else, and a critic should ask which one a team chose.

    </details>

33. **[8 · critique · apply]** A classmate writes: "The Nintendo 64 created the 3D platformer." Using the lecture's constraint-reading method and its point that technology is a pressure, not a cause, rewrite the claim.

    <details>
    <summary>Answer</summary>

    The lecture supports these facts. The Nintendo 64 launched in Japan on 23 June 1996 with an analog stick designed for moving in 3D, alongside Super Mario 64, whose team started development with the characters and the camera system. The genre, as the lecture defines it, is a cluster of answers to a 3D problem (where to put the camera): analog movement, a following adjustable camera and open levels.

    Rewrite: "3D hardware created a new problem, placing a camera every frame, and the Nintendo 64's analog stick made movement in any direction practical. Nintendo's Super Mario 64 team chose a following, adjustable camera and open levels as its answer, and later games that kept that cluster of answers form the 3D platformer." This names the pressure, the trace (camera, analog movement) and the choice, and gives the designers the credit the hardware claim hides.

    </details>

## Week 9 · Graphical MMOs

Lecture: [w09-graphical-mmos-meridian-59-ultima-online-everquest.md](../lectures/w09-graphical-mmos-meridian-59-ultima-online-everquest.md)

34. **[9 · compute · apply]** An invented 2006 MMO reports 180,000 subscribers and a peak of 24,000 concurrent players across 10 shards. (a) Compute `r` and `W`, and label them. (b) The company wants 3,000 players per shard at peak. How many shards should it run? (c) What will players notice?

    <details>
    <summary>Answer</summary>

    (a) `r = 24,000 / 180,000 ≈ 0.133`, a peak ratio. `W = 24,000 / 10 = 2,400` players per shard at peak.

    (b) `N = r × S / W = 0.133 × 180,000 / 3,000 = 8` shards.

    (c) Two shards must merge or move their players. Worlds feel busier at peak, and some friends end up on the same shard while others are split, depending on how the merge is done. That is why operators add character transfers.

    </details>

35. **[9 · compute · apply]** An invented MMO published only one number: 320,000 subscribers at its peak. A developer interview says servers held "about 2,000 players at busy times". Estimate total peak concurrency and the number of servers for `r` = 0.10, 0.125 and 0.15, and write the estimate as a sentence a careful historian could publish.

    <details>
    <summary>Answer</summary>

    | `r` | `C = r × 320,000` | `N = C / 2,000` |
    |---|---|---|
    | 0.10 | 32,000 | 16 |
    | 0.125 | 40,000 | 20 |
    | 0.15 | 48,000 | 24 |

    Sentence: "Assuming that 10% to 15% of its 320,000 peak subscribers were online at the busiest time, and that each server held about 2,000 players, as a developer said in an interview, the game would have needed roughly 16 to 24 servers. The company did not publish its server count."

    </details>

36. **[9 · explain · apply]** Classify each invented statement as `S` (subscribers), `C` (concurrent, peak or average), `W` (players in one world at once), a registered-account count, or unclear. Say what extra information you would need. (a) "Our realms hold up to 4,000 adventurers each." (b) "1.2 million heroes have joined since launch." (c) "Last Sunday at 8pm, 38,000 players were online." (d) "On a typical evening, 20,000 players are online." (e) "We have 250,000 active subscriptions as of June."

    <details>
    <summary>Answer</summary>

    (a) `W`, but a cap, not a measured figure. Need the actual peak per realm. (b) A registered-account count. It can only grow and says nothing about current players. (c) `C`, peak. Need to know whether it is a record and across how many worlds. (d) `C`, average (or typical). Need the date. (e) `S` at a date. Need the company's definition of "active subscription" (paid, prepaid, free trial?).

    Pairing (c) with (e) gives a peak ratio of `38,000 / 250,000 ≈ 0.15`, if they refer to the same month. Pairing (d) with (e) gives an average ratio of 0.08. Label which one you use.

    </details>

37. **[9 · explain · apply]** An invented online RPG switches in 1998 from hourly pricing to a flat monthly fee. Using the lecture's argument about pricing as a design force, predict two design changes the operator now has a reason to make, and name one EverQuest feature from the lecture that fits the same incentive.

    <details>
    <summary>Answer</summary>

    Under hourly pricing the operator earns more from long sessions. Under a flat fee it earns the same from one hour or a hundred, so it needs renewal next month. Likely changes: goals that take months to reach (long level curves, rare items), and social ties that make leaving costly (guilds, group content that needs a stable team). The operator may also try to make short sessions satisfying, since long ones no longer earn more.

    EverQuest's raids fit the flat-fee incentive. They need a stable group of dozens of players over weeks, which is a strong reason to keep paying.

    </details>

## Week 10 · World of Warcraft and the mass-market MMO

Lecture: [w10-world-of-warcraft-and-the-mass-market-mmo.md](../lectures/w10-world-of-warcraft-and-the-mass-market-mmo.md)

38. **[10 · compute · apply]** An invented MMO grows from 200,000 to 1,800,000 subscribers in 18 months. (a) Compute the growth factor and the distance between the two points on a log10 axis. (b) Compute the average monthly growth factor and the average number added per month. (c) Which chart, linear or log, would make this look more impressive, and which would show whether growth is slowing?

    <details>
    <summary>Answer</summary>

    (a) Factor `= 1,800,000 / 200,000 = 9`. Log distance `= log10(9) ≈ 0.954`.

    (b) Monthly factor `= 9^(1/18) ≈ 1.130`, about 13% a month. Added per month `= 1,600,000 / 18 ≈ 88,889`.

    (c) The linear chart shows the absolute climb, which looks steep and keeps looking steep as long as the added-per-month number stays high. The log chart shows the growth rate. A straight line means a constant factor, and a line bending flatter means growth is slowing even while absolute numbers still climb. Draw the log chart for the rate question, quote the absolute numbers in the text, and name the scale.

    </details>

39. **[10 · compute · apply]** An invented MMO announces a peak of 45,000 concurrent players and no subscriber count. Its players average 2.5 hours a day, and the busiest hour has 1.4 times the average number online. (a) Estimate `r` and the implied subscriber count. (b) Recompute with 1.5 hours a day. (c) What must you write next to the estimate?

    <details>
    <summary>Answer</summary>

    (a) `r ≈ (2.5 / 24) × 1.4 ≈ 0.146`. `S ≈ 45,000 / 0.146 ≈ 308,600`.

    (b) `r ≈ (1.5 / 24) × 1.4 = 0.0875`. `S ≈ 45,000 / 0.0875 ≈ 514,300`.

    (c) The assumptions (`h` and `f`), the range they produce (about 310,000 to 510,000), and the fact that the company published only the concurrent figure. Less play per player implies more players for the same peak, so the estimate swings by two thirds on one assumption.

    </details>

40. **[10 · critique · recall]** Using the lecture's World of Warcraft milestone table, name the period with the highest monthly growth factor and the period with the most subscribers added per month. Then explain how a linear chart and a log chart of the same data would lead a reader to different conclusions.

    <details>
    <summary>Answer</summary>

    Highest monthly factor: December 2004 to March 2005, 1.554 (about 55% a month). Most added per month: March to June 2005, about 583,333 a month.

    The factor fell in every period from the first. The number added per month stayed above 130,000 into 2008. A linear chart shows the second story: the line still climbs steeply in 2007, so a reader thinks growth was strong. A log chart shows the first: the curve bends flat within the first year, so a reader thinks growth slowed early. Both are true. The writer should say which question the chart answers.

    </details>

41. **[10 · critique · apply]** An invented slide titled "Biggest MMOs" puts three bars side by side: Game A, 2 million registered accounts (2020); Game B, 300,000 subscribers (2006); Game C, 90,000 peak concurrent players (2019). (a) Which comparisons are defensible as drawn? (b) Convert Game C to an implied subscriber range with `r = 0.125` and `r = 0.1875`. (c) Rewrite the slide title and captions.

    <details>
    <summary>Answer</summary>

    (a) None as drawn. The three bars count different things in different years. A registered-account total only grows and cannot be converted to `S` or `C` without the share still active.

    (b) `90,000 / 0.125 = 720,000`. `90,000 / 0.1875 = 480,000`. So Game C implies roughly 480,000 to 720,000 active players under stated assumptions, which may be larger than Game B's 300,000, but in a different year and from a different kind of number.

    (c) Title: "Three MMO population figures, three different measures". Captions that state each metric, its date and its source, for example "Game B: 300,000 subscribers as the company defined them, 2006". Draw Game A separately or not at all, since its number cannot be compared with the others.

    </details>

## Week 11 · Free-to-play, mobile and live service

Lecture: [w11-free-to-play-mobile-and-live-service.md](../lectures/w11-free-to-play-mobile-and-live-service.md)

42. **[11 · compute · apply]** An invented mobile game has 5 million monthly players. 2.5% of them pay, and each payer spends $24 a month on average. (a) Compute monthly revenue and ARPU. (b) How many $15-a-month subscribers would earn the same? (c) How many free players does it take to earn what one subscriber pays?

    <details>
    <summary>Answer</summary>

    (a) `R = 5,000,000 × 0.025 × 24 = $3,000,000` a month. `ARPU = 0.025 × 24 = $0.60`.

    (b) `3,000,000 / 15 = 200,000` subscribers.

    (c) `15 / 0.60 = 25` free players per subscriber.

    </details>

43. **[11 · compute · apply]** An analytics report for an invented game says the top 10% of payers produce 60% of revenue. Using the lecture's Pareto rule, (a) find `α`, (b) compute the share from the top 1% and the top 20%, and (c) with an average spend per payer of $20, compute the median payer's spend. (d) What does the gap between mean and median tell a designer?

    <details>
    <summary>Answer</summary>

    (a) `0.1^(1 − 1/α) = 0.6`, so `1 − 1/α = ln 0.6 / ln 0.1 ≈ 0.2218` and `α ≈ 1.285`.

    (b) Top 1%: `0.01^0.2218 ≈ 0.36`, 36%. Top 20%: `0.2^0.2218 ≈ 0.70`, 70%.

    (c) `x_m = 20 × (α − 1) / α = 20 × 0.285 / 1.285 ≈ 4.44`. Median `= 4.44 × 2^(1/1.285) ≈ 4.44 × 1.715 ≈ $7.61`.

    (d) The typical payer spends $7.61, not $20, and a hundredth of payers bring in over a third of the money. Pressure builds to design around those few. The lecture asks the designer to decide knowingly what to sell to them and what to refuse.

    </details>

44. **[11 · compute · apply]** An invented live game has ARPU $0.90 a month and monthly retention of 80%. (a) Compute expected lifetime and LTV. (b) A battle pass raises retention to 86% and ARPU to $0.95. (c) A loot-box event instead raises ARPU to $1.20 but lowers retention to 75%. Which option gives the higher LTV, and what else should decide the choice?

    <details>
    <summary>Answer</summary>

    (a) `L = 1 / (1 − 0.8) = 5` months. `LTV = 0.90 × 5 = $4.50`.

    (b) `L = 1 / 0.14 ≈ 7.14` months. `LTV ≈ 0.95 × 7.14 ≈ $6.79`.

    (c) `L = 1 / 0.25 = 4` months. `LTV = 1.20 × 4 = $4.80`.

    The battle pass wins by LTV ($6.79 against $4.80), because retention multiplies everything. Other deciders: random paid rewards carry legal risk (the lecture's Netherlands and Belgium cases), the loot box concentrates spending on fewer players (smaller `α`), and the experience of the player who never pays.

    </details>

45. **[11 · critique · apply]** An invented free-to-play game's store sells: (a) a $0.99 starter pack once per account, (b) a $4.99 skip that ends a 24-hour build timer, (c) a $9.99 seasonal pass, (d) $19.99 random premium chests with a 1% chance of the strongest weapon, (e) $14.99 character outfits. Label each (cosmetic, convenience, content, power, random), name the term of `N × p × A` or `r` it mainly moves, and write one claim about whose experience the store serves.

    <details>
    <summary>Answer</summary>

    (a) Convenience or content, moves `p` by making a first purchase easy. (b) Convenience, moves `A`, and gives the game a reason to make timers longer. (c) Content with a fixed price, moves `r` and `p`, and puts a soft ceiling on most payers' spend. (d) Random and power, moves `A` for the few who chase the weapon, and pushes spending toward a small `α`. (e) Cosmetic, moves `A` without touching balance.

    Claim, for example: "This store is built for players who will spend on random power, so the strongest weapon is designed to be rare enough that non-payers will almost never hold it." A reader could dispute it, and the chest odds and price support it.

    </details>

## Week 12 · Indie games and the auteur designer

Lecture: [w12-indie-games-and-the-auteur-designer.md](../lectures/w12-indie-games-and-the-auteur-designer.md)

46. **[12 · compute · apply]** In Papers, Please's Class-8 apartment with rent 25, an inspector processes 15 entrants and receives 5 citations. (a) Compute pay, fines, income and surplus after full care for four relatives. (b) After paying rent, what can the inspector afford?

    <details>
    <summary>Answer</summary>

    (a) Pay `= 5 × (15 − 5) = 50`. Fines `= 0 + 0 + 5 + 5 + 10 = 20`. Income `= 30`. Surplus `= 30 − 55 = −25`.

    (b) Rent takes 25 and leaves 5. That feeds the son, who can go only one day without food. No heat, and the wife, mother-in-law and uncle go hungry. Rushing to 15 entrants with five mistakes left the family worse off than the careful 10-entrant day (−5).

    </details>

47. **[12 · compute · apply]** Using the lecture's steady-state budget, a niece joins the family, so `F = 5`. (a) How many correct entrants a day are needed to break even with full care? (b) An inspector processes 12 entrants and lets one sympathetic entrant through, taking one citation. Compute the surplus with `F = 5` and with `F = 4`. (c) What does the rule set now say about mercy?

    <details>
    <summary>Answer</summary>

    (a) Care `= 25 + 10 + 5 × 5 = 60`, so `60 / 5 = 12` correct entrants.

    (b) Pay `= 5 × (12 − 1) = 55`, fines 0 (the first citation is a warning). With `F = 5` the surplus is `55 − 60 = −5`. With `F = 4` it is `55 − 55 = 0`.

    (c) The one act of mercy cost 5 credits of lost pay, one person's food for a day. A larger family raises the break-even line, so the same mercy that was free of hardship with four relatives now leaves someone hungry. The rules place the family's needs and a stranger's needs in one currency.

    </details>

48. **[12 · design · apply]** A designer wants Papers, Please to be easier for new players to read, but wants to keep its claim that a careful, honest worker cannot quite afford full care. Propose one rule change and show with the budget that a zero-citation inspector at 10 entrants is still below break-even every day. Say what your change does to the argument.

    <details>
    <summary>Answer</summary>

    Example: start the game with 40 credits of savings instead of adding 20 credits a day. The daily budget is unchanged. At `n = 10, c = 0`, income is 50 and care is 55, so the surplus is still −5 a day. Savings fall from 40 to −10 over ten days, so the squeeze arrives later but still arrives. The buffer gives a new player a few days to learn the rulebook before choosing who goes cold.

    Easy mode's +20 a day, by contrast, turns −5 into +15 and removes the claim. Other acceptable answers: a tutorial day with no bills, or clearer ledger labels. Any change that leaves the daily surplus below zero for the careful inspector keeps the argument. The answer must show the numbers.

    </details>

49. **[12 · critique · apply]** A student essay says: "Stardew Valley and Hollow Knight prove that indie means made by one person with no help." (a) Use the lecture's three meanings of "indie" to correct it. (b) Weekly Steam releases rose from about 5 to about 180. If players' total attention stayed flat, what share of pre-2012 attention does the average new game get, and why is the average misleading?

    <details>
    <summary>Answer</summary>

    (a) "Indie" can mean financially independent, small, or an aesthetic. Stardew Valley was designed and built by one person, Eric Barone, but had a publisher, Chucklefish, from partway through development, so it is small but not financially independent in the strict sense. Hollow Knight was made by Team Cherry, a small studio, and partly funded by a Kickstarter that raised over A$57,000 in 2014, so it is small and independent but not one person. Neither proves the claim.

    (b) `5 / 180 ≈ 1/36`, about 2.8% of the pre-2012 attention per game. The average hides the distribution. A few games take most of the attention, and the 2025 estimate in the lecture found that 40% of new games earned under US$100.

    </details>

## Week 13 · Ludology vs narratology

Lecture: [w13-ludology-vs-narratology.md](../lectures/w13-ludology-vs-narratology.md)

50. **[13 · compute · apply]** An invented game offers the same choice 15 times. Killing a captured bandit pays 90 gold; sparing pays 30 gold, and every fifth spare earns a 250-gold reward from a grateful village. The fiction condemns killing. (a) Compute `I_encounter` and `I_game` for the pure strategies. (b) What does a player who kills only once end with? (c) What is the smallest number of kills that beats spare-all? (d) Classify the choice.

    <details>
    <summary>Answer</summary>

    (a) `I_encounter = 90 / 30 = 3.0`. Kill all: `15 × 90 = 1,350`. Spare all: `15 × 30 + 3 × 250 = 450 + 750 = 1,200`. `I_game = 1,350 / 1,200 = 1.125`.

    (b) One kill leaves 14 spares and 2 rewards: `90 + 420 + 500 = 1,010`, 190 less than spare-all, because the kill breaks a set of five.

    (c) Four kills give `360 + 330 + 500 = 1,190`, still below. Five kills give `450 + 300 + 500 = 1,250`, above. The answer is 5.

    (d) Tense in the moment (3:1), much milder over the game (about 1.13:1). As in BioShock, whether the designers meant it depends on whether players know about the village reward when they choose.

    </details>

51. **[13 · compute · apply]** Using the lecture's BioShock values (21 Little Sisters, 160 ADAM per harvest, 80 per rescue, a 200-ADAM gift per three rescues), find every number of harvests `h` other than 0 that gives exactly the rescue-all total of 3,080 ADAM. Explain the pattern.

    <details>
    <summary>Answer</summary>

    `ADAM(h) = 160h + 80(21 − h) + 200 × floor((21 − h) / 3)`.

    `h = 5`: 16 rescues, 5 gifts. `800 + 1,280 + 1,000 = 3,080`. `h = 10`: 11 rescues, 3 gifts. `1,600 + 880 + 600 = 3,080`. No other `h` gives 3,080.

    Pattern: compared with rescue-all, each harvest gains 80 ADAM (160 instead of 80), and each gift lost costs 200. With `h` harvests you lose `ceil(h / 3)` of the 7 gifts. The totals match when `80h = 200 × ceil(h / 3)`. At `h = 5` you lose 2 gifts (400) and gain `5 × 80 = 400`. At `h = 10` you lose 4 gifts (800) and gain 800. The floor makes the whole-game line a sawtooth, so a player can harvest ten girls and end with exactly the same ADAM as a player who saved them all.

    </details>

52. **[13 · critique · apply]** A reviewer writes of an invented game: "Game Q is ludonarratively dissonant. Its story preaches pacifism, but you earn experience by fighting." The game also offers a non-lethal route through every fight that pays 95% of the experience, and its closing scene comments on the player's body count. Use the ledger to assess the review.

    <details>
    <summary>Answer</summary>

    Over the whole game, `I_game = 1 / 0.95 ≈ 1.05`. The rules pay almost the same for the act the fiction condemns and the act it praises, so the choice is close to neutralized, not tense. Dissonance, in the lecture's sense, needs tension the work does not seem to know it has. Here the tension is small, and the closing scene shows the game is aware of it.

    The reviewer has noticed that fighting pays, which is true of the default route, but has not counted the alternative or the span. A better review: "Game Q pays almost the same experience for non-lethal play, so its pacifism costs the player very little. The choice is a fiction choice, and the ending makes sure you notice which one you made."

    </details>

53. **[13 · explain · apply]** Apply the lecture's test of Murray's Tetris reading to an invented abstract puzzle game with no characters, no text and a single rule: coloured tiles fall and vanish when four of one colour touch. A critic reads it as "an allegory of social integration". (a) What does the rules-fiction ledger find? (b) State Eskelinen's objection in one sentence. (c) What would the critic need to show to make the reading stronger?

    <details>
    <summary>Answer</summary>

    (a) The ledger fails at the first step. There is no choice the fiction frames as right or wrong, because the game has almost no fiction. Every meaning in the reading comes from the critic, not from either layer.

    (b) A reading that would work equally well for a painting of falling tiles has skipped the game, which is made of rules and player action.

    (c) Tie the claim to the rules: show which rule produces the effect the allegory names, for example that mixing colours scores more than grouping them, or that the game punishes one pattern. Or use procedural rhetoric in Bogost's sense and argue from what the process forces the player to do. Without a rule to point at, the reading tells us about the critic.

    </details>

## Week 14 · Games and representation

Lecture: [w14-games-and-representation.md](../lectures/w14-games-and-representation.md)

54. **[14 · compute · apply]** An invented hero shooter has 20 human playable characters, 7 of them women. (a) Compute the female share and the representation index against a 50% population baseline and against a 38% player baseline (the figure the 2009 paper uses in its discussion). State each in the "percent under-represented" form. (b) Which baseline fits the question "does the roster look like the people who play it?"

    <details>
    <summary>Answer</summary>

    (a) Share `= 7 / 20 = 35%`. Against 50%: `RI = 0.70`, 30% under-represented. Against 38%: `RI = 0.35 / 0.38 ≈ 0.92`, about 8% under-represented.

    (b) The player baseline, if you can source a player figure for this genre and year. Name it in the same sentence as the number. The same roster reads as badly short against society and close to proportional against players.

    </details>

55. **[14 · compute · apply]** An invented census covers two games. Game A sold 3 million copies and 10% of its characters are women. Game B sold 1 million and 40% of its characters are women. (a) Compute the female share with each game counted once (the average of the two games' shares) and weighted by sales. (b) What does each figure describe? (c) Relate the result to the 2017 replication's two figures.

    <details>
    <summary>Answer</summary>

    (a) Unweighted: `(10% + 40%) / 2 = 25%`. Weighted: `(0.10 × 3 + 0.40 × 1) / 4 = 17.5%`.

    (b) The unweighted figure describes what studios made. The weighted figure describes what players saw, since the best-seller counts three times as much.

    (c) The replication found the same direction: 22.41% unweighted and 18.98% weighted in 2017. In both, the best-selling games had a smaller share of women than the average game made.

    </details>

56. **[14 · compute · apply]** Two coders code gender for 50 human characters. Coder A's totals are woman 13, man 33, cannot determine 4. Coder B's are woman 11, man 33, cannot determine 6. They agreed on 10 women, 30 men and 3 cannot-determine. (a) Compute percent agreement and Cohen's κ. (b) Compare with the κ values the two published censuses report, and say what your value means for your figures.

    <details>
    <summary>Answer</summary>

    (a) `p_o = (10 + 30 + 3) / 50 = 0.86`. `p_e = (13 × 11 + 33 × 33 + 4 × 6) / 50² = (143 + 1,089 + 24) / 2,500 = 0.5024`. `κ = (0.86 − 0.5024) / (1 − 0.5024) ≈ 0.72`.

    (b) The 2009 census reports 0.93 for gender and the 2017 replication 0.95. Your 0.72 is close to the replication's race and age values (0.73). That is acceptable, but your gender shares carry more error than the published ones. Look at the disagreements (mostly the cannot-determine row) and tighten the codebook rule before pooling.

    </details>

57. **[14 · critique · apply]** Two invented reports describe the same kind of finding. Report 1: a group is 30% of characters and 20% of the population. Report 2: a group is 12% of characters and 8% of the population. (a) Compute each result both as a ratio index and as a difference in percentage points. (b) A headline says "Both groups are 50% over-represented." Is it right, and what does it hide?

    <details>
    <summary>Answer</summary>

    (a) Report 1: `RI = 30 / 20 = 1.5` (50% over in the ratio form), difference 10 points. Report 2: `RI = 12 / 8 = 1.5`, difference 4 points.

    (b) It is right in the ratio form, the one the 2009 paper uses. It hides that the gap in the first case is two and a half times larger in points, which is the form the 2025 paper uses. When you read "X% over-represented", check which measure the author means, and report the shares and the baseline alongside it.

    </details>

## Integrated cases

58. **[3, 9, 11 · explain · apply]** Compare four payment models covered in the course: the arcade coin, hourly online pricing, the flat monthly subscription and free-to-play. For each, name what the operator is paid for, the variable a designer is pushed to move, and one design trait that follows. Then compute one comparison: at the lecture's Pong calibration (`p = $0.25`, `L = 3`, `u = 0.75`) a cabinet earns $3.75 an hour of opening time. A subscriber who pays $15 a month and plays 30 hours pays how much per hour of play?

    <details>
    <summary>Answer</summary>

    Arcade: paid per session, pushed to cut `L`, so ramps, lives and short sessions. Hourly: paid per hour, pushed to lengthen sessions. Flat monthly fee: paid for renewal, pushed toward goals that take months and social ties (raids, guilds). Free-to-play: paid by a minority, pushed to raise `N`, `p`, `A` and `r`, so open doors, a store, seasons and retention events.

    Subscriber: `$15 / 30 = $0.50` per hour of play. The arcade figure is per hour of machine time across many players, so the two are not the same measure, but the contrast shows why subscription games stopped cutting sessions short.

    </details>

59. **[4, 7, 12 · critique · apply]** "Opening a platform to everyone always ends in a crash." Test the claim with three cases from the course: the Atari 2600 in 1982, the PC modding scene in the 1990s and 2000s, and Steam from Greenlight to Direct. Use one number from each lecture where you can.

    <details>
    <summary>Answer</summary>

    Atari 2600: the platform opened after Activision won in court, and Atari games on the market went from about 100 to over 400 in six months (four times). With failed returns and $5 bins, US home sales fell about 97% by 1985. The claim fits here.

    PC modding: the PC had no gatekeeper, and mods reached the public within four years of their hosts (median `L_M` of 1 year in the lecture's six cases). The open platform produced new genres, not a crash, because copies cost nothing to store and players built on the host rather than competing with it on a shelf.

    Steam: weekly releases rose from about 5 to about 180 (36 times). There was no crash of the store, but the lecture's 2025 estimate found 40% of new games earned under US$100. The damage moved from prices to attention.

    Verdict: openness raises `S`. Whether that crashes a market depends on whether surplus can be dumped cheaply and cannibalize full-price sales. The claim is too strong. A better one names the bin.

    </details>

60. **[several · design · apply]** Write a timeline-project cause entry for "Meridian 59 charges a flat monthly subscription (1996)" in the course format: date and precision, event, evidence type, cause type, mechanism naming a model variable, one alternative explanation, and source with era. Use only facts from the week 9 lecture.

    <details>
    <summary>Answer</summary>

    - Date: 7 October 1996 (day), commercial launch.
    - Event: Meridian 59 launches with a flat monthly subscription rather than hourly pricing.
    - Evidence type: press and conference record (a panel of online game service heads at the September 1996 Online Game Developer's Conference called flat-rate pricing unsustainable, via Next Generation).
    - Cause type: business.
    - Mechanism: a flat fee removes the per-hour price, so the operator is paid for renewal rather than session length. This rewards long-term goals and social ties, which later appear in EverQuest's raids (week 9).
    - Alternative explanation: the choice may reflect competition with hourly services such as AOL rather than a design philosophy; the sources here do not record the company's reasons.
    - Source: Wikipedia, "Meridian 59", accessed September 2026, as cited in week 9.

    Marking notes: accept any entry that separates the fact from the mechanism, names the variable, and states what the sources do not say.

    </details>

61. **[1, 12, 13 · critique · apply]** Compare where the argument lives in The Landlord's Game (1904), Papers, Please (2013) and BioShock (2007). For each, name the rule that carries the argument, say whether rules and fiction push the same way, and state which game the phrase "ludonarrative dissonance" fits best, if any.

    <details>
    <summary>Answer</summary>

    The Landlord's Game: the rent rule. Under the monopolist rules, rent flows to landowners, so one player's surplus is everyone else's shortfall. Rules and fiction push the same way (landlords ruin tenants), which was Magie's point. The alternative rule set changed the flow of money and so changed the argument.

    Papers, Please: the fine schedule and the daily budget. Mercy costs 5 credits at first and 20 by the sixth citation, and the fiction frames mercy as kind. The layers are tense on purpose. The game wants kindness to cost the family something.

    BioShock: 160 against 80 ADAM per encounter, 3,360 against 3,080 over the game once gifts are counted. Tense in the moment, close to neutralized over the game.

    None fits "dissonance" cleanly. BioShock's Little Sisters are the usual example, but the gifts neutralize the choice, and Hocking's own essay aims at the Atlas contract, not the Little Sisters.

    </details>

---

## Viva prompts for the final presentation

The assessor adapts an "apply" question to the student's own essay game. These show the pattern. Each viva uses two prompts, one on a model and one on sources or method.

- "Which rule in your game carries the argument you make? Compute what it pays for each option over the span the player decides over." (Adapted from 50 and 61.)
- "Your essay cites a population figure. Is it `S`, `C`, `W` or a registered-account count, who published it, and what would change if you used another measure?" (Adapted from 36 and 41.)
- "Name one technical constraint your game's era faced and one trace of it you saw in play. What did the designers choose to do with it?" (Adapted from 33.)
- "Your timeline gives a cause for one event. What is the strongest alternative cause, and what evidence would decide between them?" (Adapted from 16 and 60.)
- "Where does your game's business model show up in its rules? Name the variable it pushes the designer to move." (Adapted from 13 and 58.)
- "Your representation claim uses a baseline. Why that one, and what does the verdict become against another?" (Adapted from 54.)
- "Which of your 'first' or 'invented' claims would fail the three questions from week 7, and how would you rewrite it?" (Adapted from 29.)
