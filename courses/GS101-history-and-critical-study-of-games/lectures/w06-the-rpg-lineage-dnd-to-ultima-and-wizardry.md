# GS101 · Week 06 — The RPG Lineage: D&D to Ultima and Wizardry

**Why this matters:** Hit points, experience levels, character classes, armor class and a 5% chance to hit no matter what. Computer role-playing games did not invent these. They inherited them from a 1974 tabletop game that used paper, pencils and a 20-sided die. Knowing the lineage lets you tell which parts of a modern RPG are deliberate design and which are fossils from a physical die, and a fossil is something you are allowed to change.

**You will be able to:**
- Trace the line from Chainmail and Dungeons & Dragons through the PLATO dungeon games to Ultima, Wizardry and Dragon Quest, with dates and what each step added.
- Compute a d20 hit chance for any attack bonus and armor class, including the natural-1 and natural-20 limits, and convert an AD&D THAC0 roll into the same form.
- Explain why each +1 to hit is worth a constant 5 percentage points but a very different share of your damage, and use that to critique a stat design.
- Critique a "family tree" history of a genre by naming what it leaves out.

**Before class:** Donovan, *Replay* (2010), the pages on the birth of computer role-playing games (Ultima, Wizardry and the PLATO games). The course reader lists the pages. Bartle, *Designing Virtual Worlds* (2003), chapter 1, the section "Role-Playing Games" on D&D's influence on virtual worlds (pp. 97-107 in the author's free PDF edition at mud.co.uk/richard/DesigningVirtualWorlds.pdf). Bring a 20-sided die if you have one, or use any dice app.

**Prerequisites from earlier courses:** None. GS101 has no prerequisites. This week builds on [GS101 week 5, text adventures and MUD1](w05-text-adventures-and-mud1.md), because MUD1's "D" is the same dungeon. The probability here uses only counting outcomes on one die; you will do it properly in [MA102 week 1, sample spaces and events](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w01-sample-spaces-and-events.md), which studies D&D's advantage rule, and [MA102 week 4, expected value](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w04-expected-value-comparing-weapons.md). The Diablo II hit formula in section 3 is worked through later, in [MMO303 week 2, armor and damage mitigation](../../MMO303-game-balance-i-combat-and-class-balance/lectures/w02-armor-and-damage-mitigation.md) (year 3).

**Interactive:** [The d20 hit chance](../examples/w06-d20-hit-chance.html). Use it during section 3.

---

## 1. From wargame to role-playing game

### Chainmail and the idea of one figure

Before role-playing games there were wargames, tabletop games that simulate battles with miniature figures on a map. Each figure usually stood for many soldiers, and the rules resolved combat with dice and tables.

In 1971, Gary Gygax and Jeff Perren published Chainmail, a set of rules for medieval miniatures battles. It included a fantasy supplement with heroes, wizards and monsters. The important change was scale. In the fantasy rules, one figure could be one person, a single hero with a name.

Dave Arneson, another wargamer, took that idea further in his own campaign. Each player controlled one character, kept that character from session to session and explored a dungeon run by a referee. Gygax and Arneson developed the idea together. In 1974 Tactical Studies Rules (TSR) published it as Dungeons & Dragons, a small boxed set that spread quickly, first among wargamers.

### What D&D handed down

Look at what a 1974 D&D character sheet holds, and notice how much of it you already know from computer games:

- **Hit points,** a pool of damage you can take before dying.
- **Experience points and levels,** so the same character grows stronger over many sessions.
- **Classes.** The 1974 set had three, the fighting-man, the magic-user and the cleric, each with different abilities.
- **Armor class (AC),** one number summarizing how hard you are to hit. The term came over from Chainmail.
- **A roll to hit,** made with dice against a number derived from the target's armor class.

Every one of these solved a tabletop problem. Arneson, who coined the term "hit points," explained that his players did not mind failing to kill a monster in one blow, but they did not want a monster to kill them in one blow. A pool of hit points lets a character survive several hits, so one bad roll does not end a months-long campaign. Levels gave players a reason to return each week. A single AC number let a referee resolve a fight in seconds without simulating every piece of armor.

Then the rules moved to computers, where none of those tabletop problems exist. A computer can track fifty damage types, resolve a hit with any probability you like and never needs a quick summary number. The rules came over anyway. That is what we mean by a lineage, and it is why the worked example in section 3 looks at a die.

### Editions change the notation, not the idea

D&D has been revised many times. Three editions matter for this lecture.

- **Advanced Dungeons & Dragons (1977 to 1979),** a fuller rule set published alongside a simpler basic game.
- **AD&D 2nd edition (1989).** Its hit roll used a number called THAC0, "to hit armor class 0." You subtract the defender's AC from your THAC0 to find the number you need on a d20. Armor class counted downward, so lower AC was better. An unarmored person had AC 10.
- **3rd edition (2000).** It introduced the d20 System, which resolves nearly every action as a d20 roll plus modifiers. To attack, you roll a d20, add your attack bonus, and hit if the total equals or beats the target's AC. AC now counted upward, starting at 10 plus bonuses. A natural 1 (the die shows 1) always misses, and a natural 20 always hits. Wizards of the Coast published the core rules under the Open Game License as the System Reference Document (SRD), so other companies could build on them.

In section 3 you will see that THAC0 and the 3rd edition roll are the same model written two ways.

## 2. From the table to the terminal

### PLATO: dungeons on a university network

The first computer games built on D&D appeared almost immediately, on PLATO, a networked teaching system at the University of Illinois with terminals at many campuses. PLATO had graphics terminals and a large community of student programmers.

- **dnd (1974 to 1975),** by Gary Whisenhunt and Ray Wood at Southern Illinois University, took its name from the abbreviation "D&D." Players explored a multi-level dungeon for treasure. It is credited as the first game with what we would now call a boss, a single powerful monster guarding the goal. Others kept extending it for about a decade.
- **Oubliette (1977)** was another PLATO dungeon game, and it directly inspired Wizardry.

These games ran on university systems that ordinary buyers could not reach. They were free, shared and constantly modified. Their influence traveled through students who played them and later wrote commercial games.

### Ultima: an open world on the Apple II

Richard Garriott wrote Akalabeth: World of Doom as a teenager and first sold copies himself, in Ziploc bags with photocopied instructions. Most sources, including Garriott, date those first sales to 1979, while the historian Jimmy Maher argues they began in summer 1980. California Pacific's retail release came in 1980. Akalabeth combined a simple top-down map with first-person dungeons. He then wrote Ultima during his first year at the University of Texas, with help from Ken W. Arnold. Large parts of Akalabeth became subroutines inside Ultima, running its first-person dungeon sections.

California Pacific Computer Company published Ultima for the Apple II in June 1981. It was written in Applesoft BASIC, with assembly language for its tile-based graphics. The overworld was drawn top-down in the third person and the dungeons in the first person. It sold 20,000 copies by June 1982 and eventually about 50,000. Ultima is often called one of the first open-world computer games, a world you could roam in any order rather than a fixed sequence of levels. That ambition led, fifteen years later, to Ultima Online, which you meet in week 9.

### Wizardry: the party in the maze

Andrew Greenberg and Robert Woodhead built Wizardry: Proving Grounds of the Mad Overlord for Sir-Tech Software, and it came out for the Apple II in September 1981. You created a party of up to six characters and led them down through a ten-level maze drawn in first-person wireframe. It started in Applesoft BASIC and was rewritten in UCSD Pascal because the BASIC version ran too slowly.

Wizardry was the more commercial success of the two. It sold 200,000 copies in its first three years, more than the first Ultima.

Place the two side by side and you see two designs pulling apart from the same D&D source. Ultima kept the wandering, the open map and the single hero. Wizardry kept the party, the dungeon and the tactical fight. Nearly every later computer RPG leans toward one or the other.

### Dragon Quest: the lineage crosses the Pacific

In Japan, designer Yuji Horii played Wizardry and Ultima and wanted to bring the genre to console players who found those games' interfaces intimidating. His answer was Dragon Quest, released for Nintendo's Famicom on May 27, 1986, with characters drawn by manga artist Akira Toriyama and music by Koichi Sugiyama. Horii said he aimed for a system that was easy to understand and emotionally involving.

Dragon Quest sold about 1.5 million copies in Japan and reached North America as Dragon Warrior in August 1989. It set the template for console role-playing games. Wizardry itself influenced both Dragon Quest and Final Fantasy.

The lineage now runs in a loop. An American tabletop game shaped American computer games, which shaped Japanese console games, which were then exported back to the United States and shaped the next generation there. Remember that console you studied last week, the Famicom, launched in Japan in the middle of the American crash. It is the machine that carried this lineage to its largest audience yet.

## 3. Worked example: the die inside the machine

### The hook

A computer can produce any probability. It can make your chance to hit 61.8% or 0.3%. Yet the D&D rules that computer games from Baldur's Gate (1998) to Baldur's Gate 3 (2023) adapted decide a hit with one d20, so your chance moves in steps of exactly 5%. Under the 3rd edition rules it also never drops below 5% or rises above 95%. Nothing in the computer requires either rule. So where do the 5% steps come from, and do they matter?

They come from a plastic die with twenty faces. Let's see what that die does to the value of a stat.

### The model

Use the 3rd edition rule as written in the SRD. You roll a d20 and add your attack bonus `B`. You hit if the total is at least the target's armor class `AC`. A natural 1 always misses and a natural 20 always hits.

```
need     = AC − B                        the lowest die face that hits
P(hit)   = (21 − need) / 20              faces from "need" up to 20, out of 20
         = (21 + B − AC) / 20
clamped  : P(hit) is at least 1/20 = 5%  (a natural 20 always hits)
           and at most 19/20 = 95%       (a natural 1 always misses)
expected damage per swing = P(hit) × average damage on a hit
```

- `B` is your attack bonus. It adds up level, strength and weapon bonuses.
- `AC` is the defender's armor class, 10 plus bonuses.
- `need` is the die face you must roll. The count of faces from `need` to 20 is `21 − need`.

Two properties follow directly from the formula. Between the clamps, each +1 to `B` adds exactly one face, so 5 percentage points. Outside the clamps, +1 adds nothing.

### Numbers you can check

Take a target with `AC 15`, and a weapon that deals 10 damage on a hit.

| Attack bonus B | Need on d20 | P(hit) | Expected damage | Damage gained by the next +1 |
|---|---|---|---|---|
| −6 | 21 (only a natural 20) | 5% | 0.5 | +0% |
| −5 | 20 | 5% | 0.5 | +100% |
| −4 | 19 | 10% | 1.0 | +50% |
| 0 | 15 | 30% | 3.0 | +16.7% |
| +4 | 11 | 50% | 5.0 | +10% |
| +5 | 10 | 55% | 5.5 | +9.1% |
| +10 | 5 | 80% | 8.0 | +6.25% |
| +13 | 2 | 95% | 9.5 | +0% |
| +14 | 1 (a natural 1 still misses) | 95% | 9.5 | +0% |

Check the `B = 0` row. You need 15 or more. The faces 15, 16, 17, 18, 19 and 20 are six faces, so `P = 6/20 = 30%`. Adding +1 makes you need 14, which is seven faces, 35%. Expected damage rises from 3.0 to 3.5, a gain of 0.5 on 3.0, which is 16.7%.

Look down the last column. Every +1 between the clamps adds the same 5 points of hit chance and the same 0.5 expected damage. But as a share of the damage you already deal, the same +1 is worth +100% to a character who hits only on a 20, +16.7% to one at 30%, and +6.25% to one at 80%. At both ends it is worth nothing.

This is the same trap as the armor tooltip in MMO303. A constant absolute gain hides a relative gain that changes a lot. When a player at 80% says "+1 to hit is useless," and a player at 30% says "+1 to hit is the best stat in the game," they are both reading the same formula correctly.

### The visual

Open the interactive. The left chart, "What the die shows," draws `P(hit)` against `B` as a staircase of 5% steps, with the two flat zones at 5% and 95% shaded as "the die's floor" and "the die's ceiling." The right chart, "What +1 is worth," draws the percentage damage gain from the next +1 at every `B`.

Drag the target's AC and watch the whole staircase slide sideways without changing shape. The right chart shows a tall spike at the bottom edge, a long decline and a drop to zero at the top. Now switch the notation to "AD&D 2e (THAC0)." The labels change to THAC0 and descending AC, and not one number on the charts moves.

### Cross-game recognition

Rewrite each case into `P(hit) = (21 + B − AC) / 20` with its clamps, and ask which part of the die survived.

**AD&D 2nd edition and Baldur's Gate (1998).** BioWare's Baldur's Gate ran a modified version of the AD&D 2nd edition rules, computing each roll for the player. In 2e you need `THAC0 − AC_2e` on a d20. Define `B = 20 − THAC0` and `AC = 20 − AC_2e`. Then `THAC0 − AC_2e = (20 − B) − (20 − AC) = AC − B`, which is exactly our `need`. A fighter with THAC0 20 is our `B = 0`. A target with 2e AC 5 is our `AC 15`. Both need a 15, both hit 30% of the time. An unarmored AC 10 is AC 10 in both systems. The descending numbers look different, but the model is the same one. Ignore how 2e tables treat natural 1s and 20s here, as those rules varied between tables and games.

**Advantage in D&D 5th edition and Baldur's Gate 3 (2023 and later patches).** Fifth edition (2014) added advantage. You roll two d20s and keep the higher. You miss only if both dice miss, so `P(adv) = 1 − (1 − p)²`, where `p` is the single-roll chance from our formula. At `p = 55%`, advantage gives 79.75%, close to the +5 the rules suggest as a shortcut for passive checks. At `p = 5%` it gives 9.75%, about +1. At `p = 95%` it gives 99.75%. Baldur's Gate 3 uses the same two-dice rule. The die is still a d20, now rolled twice, and the value of advantage depends on where you stand on the staircase, just like +1 does. MA102 week 1 computes where "advantage is worth +5" holds and where it fails.

**Diablo II (original game, including Lord of Destruction).** Blizzard's chance to hit was not a die roll. It was a smooth formula, which with equal levels becomes `AR / (AR + DR)` for attack rating `AR` and defense `DR`. There are no 5% steps; any value is possible. But the result is still clamped between 5% and 95%. The d20's granularity is gone. Its floor and ceiling remain, as a rule that no attack is hopeless and none is certain.

Three games, three notations, one die. When you meet a hit formula in a new game, ask four questions. What is `B`? What is `AC`? Is it stepped or smooth? Where are the clamps?

### Design judgment, eyes open

The d20 model is an inheritance, not a law. Decide what to keep.

- **What the steps buy.** A player can compute a d20 chance in their head. "I need an 11" means 50%, instantly. That readability is why the tabletop used it, and it is still worth something on a screen, especially when a game shows the roll.
- **What the steps cost.** A 5% step means +1 is the smallest improvement you can give. Items and levels must hand out bonuses in whole points, so power grows in lumps. A computer can use finer steps, as Diablo II does.
- **What the clamps buy and cost.** The 5% floor keeps hope alive in a hopeless fight and the 95% ceiling keeps tension in an easy one. They also make every stat worthless at the ends of its range, and they guarantee that players will sometimes miss a 95% attack at the worst moment, which feels unfair even though it is exactly 1 in 20.
- **What to decide deliberately.** Choose your granularity, your clamps and whether players see the roll. If you keep the d20, keep it because readability matters to your players, not because the genre always had it. Then check the "what +1 is worth" curve for your expected range of bonuses and ACs, so no stat falls into a dead zone by accident.

## 4. Reading a family tree critically

Genre histories love family trees. Chainmail begets D&D, D&D begets dnd and Oubliette, which beget Wizardry and Ultima, which beget Dragon Quest. This lecture has told the story in that shape because it is easy to follow. Now take it apart.

**Trees hide the network.** Influence rarely runs in one line. Ultima drew on D&D and on Garriott's own earlier Akalabeth. MUD1 drew on D&D and on Zork. Dragon Quest drew on Wizardry and on Ultima, then shaped games that Western designers later played. A better diagram is a graph with many arrows, some pointing backward in geography.

**Trees favor what was sold.** Wizardry and Ultima were commercial products with sales figures and box art, so they enter histories easily. The PLATO games were free, lived on university networks and survived mainly in the memories of players. A history built from sales charts will under-count them. When you research your timeline project, ask what evidence exists for a game at all, and who kept it.

**Trees suggest progress.** A tree drawn left to right implies each game improved on the one before. Wizardry is not a better D&D. It is a different thing that gave up the referee, the improvisation and the shared table in exchange for a machine that could run a dungeon alone at 3am. Say what each step gained and what it lost.

**Trees suggest single authors.** "Gygax's D&D" and "Garriott's Ultima" hide co-creators. D&D was Gygax and Arneson, drawing on Chainmail by Gygax and Perren. Ultima had Ken Arnold. Wizardry had two designers. Credit disputes shaped this history, including the founding of Activision you studied in week 4. Week 12 asks how the idea of the auteur designer came to dominate the way we talk about games.

A good lineage claim has the same shape as a good causal claim from week 4. It names a specific feature ("the party of six," "the first-person maze," "the 5% floor"), shows it in the earlier work and the later one, and cites evidence that the later designer knew the earlier work. Horii's own statements that he played Wizardry and Ultima are evidence. Two games that merely look alike are not.

## In-class activity (25 minutes)

Pairs. You need one d20 (physical or an app) per pair.

1. (8 min) Pick a target AC between 12 and 18 and an attack bonus between 0 and +6. Compute `P(hit)` with the formula. Then roll 40 attacks and count hits. Put your predicted and observed rates on the board. As a class, compare the spread of observed rates with the predictions.
2. (7 min) Take one modern RPG you know that shows a hit chance as a percentage. Decide whether it looks stepped (multiples of 5%) or smooth, and whether it seems to have a floor and a ceiling. Write the evidence you would need to be sure.
3. (10 min) Draw a lineage graph (not a tree) for that game with at least five nodes from this lecture and at least one arrow that points "backward" in time or geography. Label each arrow with one specific inherited feature.

Expected output: the board table from step 1, your stepped-or-smooth verdict with the evidence you would need, and a labeled graph.

## Common misconceptions

- **"Computer RPGs invented levels and hit points."** They inherited them from D&D (1974), which took combat ideas from wargames like Chainmail (1971).
- **"THAC0 and the 3rd edition roll are different systems."** They are the same model with the numbers flipped. `B = 20 − THAC0` and `AC = 20 − AC_2e` turn one into the other.
- **"+1 to hit is always worth the same."** It always adds 5 percentage points between the clamps, but its value as a share of your damage ranges from +100% to nothing.
- **"A 95% chance means it basically can't miss."** It misses 1 time in 20. Over a long campaign, a player who attacks 400 times at 95% expects about 20 misses.

## Check yourself

1. A character with attack bonus +7 attacks a target with AC 19. What must they roll, and what is their chance to hit? What is the chance with advantage?
2. An AD&D 2e fighter has THAC0 15 and attacks a monster with AC 2 (descending). Convert to the 3rd edition form and compute the hit chance.
3. A designer adds a ring that gives +2 to hit. For which of these two players does the ring increase expected damage more, in percent, one at `B = +1` against AC 15 or one at `B = +8` against AC 15? Show the numbers.
4. A game uses a smooth formula `P = AR / (AR + DR)` clamped to 5% to 95%. With `DR = 300`, what `AR` gives 50%? What `AR` gives 95%, and what happens to extra `AR` beyond that?

<details>
<summary>Answers</summary>

1. `need = 19 − 7 = 12`, so faces 12 to 20, nine faces, `P = 9/20 = 45%`. With advantage, `1 − 0.55² = 1 − 0.3025 = 69.75%`.
2. `B = 20 − 15 = +5` and `AC = 20 − 2 = 18`. `need = 18 − 5 = 13` (also `THAC0 − AC_2e = 15 − 2 = 13`). Faces 13 to 20 are eight, so `P = 40%`.
3. At `B = +1`, `P` goes from 35% to 45%, a gain of `10/35 = 28.6%`. At `B = +8`, `P` goes from 70% to 80%, a gain of `10/70 = 14.3%`. The ring doubles in relative value for the weaker character, even though both gain the same 10 points.
4. `AR / (AR + 300) = 0.5` gives `AR = 300`. `AR / (AR + 300) = 0.95` gives `AR = 0.95 AR + 285`, so `AR = 5,700`. Any attack rating above 5,700 adds nothing, because the result is clamped at 95%.

</details>

## Lab / assignment hook

[Lab 06, lineage graph and dice audit](../labs/lab06.md). Build a sourced lineage graph for one RPG of your choice back to D&D, and audit one of its hit or skill-check formulas against the d20 model. The graph is a candidate entry for your timeline project.

## Sources

- Wikipedia, "Dungeons & Dragons" and "Editions of Dungeons & Dragons" (accessed September 2026). Gygax and Arneson; Chainmail (1971) origin; first publication by TSR in 1974; spread among wargamers; basic and Advanced split 1977 to 1979; 2nd edition 1989 and THAC0 minus AC; 3rd edition 2000, the d20 System and the Open Game License; 5th edition 2014.
- Wikipedia, "Chainmail (game)" (accessed September 2026). Gygax and Perren, Guidon Games, 1971; medieval miniatures rules with a fantasy supplement in which single figures stand for heroes. Armor class credited to Arneson and used in Chainmail and D&D (Wikipedia, "Health (game terminology)").
- Wizards of the Coast, *System Reference Document 3.5*, "Combat Statistics" (d20srd.org). Attack roll d20 plus attack bonus, hit if equal to or above AC; natural 1 always misses; natural 20 always hits. Paraphrased.
- Wikipedia, "dnd (video game)" (accessed September 2026). Whisenhunt and Wood, Southern Illinois University, 1974 to 1975, PLATO; name from "D&D"; first boss; later additions by others to 1985.
- Wikipedia, "Akalabeth: World of Doom" (accessed September 2026). Self-published in Ziploc bags; the 1979 versus 1980 dating dispute (Garriott and Origin versus Jimmy Maher); California Pacific release 1980; top-down map and first-person dungeons. Maher, J. (2011, December 18). "Akalabeth." *The Digital Antiquarian* (filfre.net/2011/12/akalabeth/), the source of the summer-1980 argument.
- Gygax, G. and Arneson, D. (1974). *Dungeons & Dragons*, vol. 1, *Men & Magic*. TSR. The primary source for the 1974 rules: the three classes, experience-point tables that set each class's level, hit dice per level, armor class, and the attack matrix that turns a d20 roll against the defender's armor class into a hit. Wikipedia, "Dungeons & Dragons (1974)" (accessed September 2026) summarizes the three booklets, the three classes and character levels.
- Rausch, A. (2004, August 19). "Dave Arneson Interview." GameSpy (archived at web.archive.org/web/20040822043947/http://pc.gamespy.com/articles/540/540395p1.html). Arneson on coining "hit points" and why, paraphrased; also summarized in Wikipedia, "Health (game terminology)".
- Wikipedia, "Wizardry: Proving Grounds of the Mad Overlord" (accessed September 2026). Greenberg and Woodhead, Sir-Tech, Apple II, September 1981; party of up to six; ten-level maze; inspired by Oubliette (1977); BASIC to UCSD Pascal; 200,000 copies in three years, outselling Ultima; influence on Dragon Quest and Final Fantasy.
- Wikipedia, "Ultima I: The First Age of Darkness" (accessed September 2026). Garriott and Arnold; Akalabeth code reused; California Pacific, Apple II, June 1981; Applesoft BASIC and assembly tiles; top-down overworld and first-person dungeons; 20,000 copies by June 1982, about 50,000 in all.
- Wikipedia, "Dragon Quest (video game)" (accessed September 2026). Famicom release May 27, 1986; Horii, Toriyama, Sugiyama; inspiration from Wizardry and Ultima; about 1.5 million sold in Japan; Dragon Warrior in North America, August 1989.
- Wikipedia, "Baldur's Gate (video game)" (accessed September 2026). BioWare and Interplay, 1998; modified AD&D 2nd edition rules computed by the game.
- bg3.wiki, "Advantage" (Baldur's Gate 3, release version 2023 and later patches), as cited in MA102 week 1. Roll two d20s and use the higher.
- The Amazon Basin, "Technical Formulas" (Diablo II and Lord of Destruction), as cited in MMO303 week 2. Chance to hit from attack rating and defense with a 5% to 95% clamp.
- Donovan, T. (2010). *Replay: The History of Video Games*. Yellow Ant, East Sussex (xiv + 501 pp.). Bartle, R. (2003). *Designing Virtual Worlds*. New Riders. Free PDF edition from the author, mud.co.uk/richard/DesigningVirtualWorlds.pdf (chapter 1 is pp. 1-107).
- The damage values and the table in section 3 are computed from the stated model and can be checked by counting die faces.

## Interactive spec: examples/w06-d20-hit-chance.html

**The one insight:** on a d20, each +1 to hit adds a constant 5 percentage points between the clamps, but the share of your damage it adds swings from +100% near the floor to 0% at the ceiling. THAC0 notation and 3rd edition notation draw the identical staircase.

**Layout.** Two linked charts side by side on desktop, stacked on mobile (staircase on top). Shared horizontal axis "Attack bonus B" from −10 to +25, integer steps.

- **Left chart, "What the die shows":** `P(hit)` for each integer `B`, drawn as a step line (horizontal segment per integer). Vertical axis 0% to 100%. Shade the region where `P = 5%` (floor) and where `P = 95%` (ceiling) with a faint fill, labeled "the die's floor" and "the die's ceiling". When advantage is on, draw a second step line for `P_adv` in a second palette color with a legend.
- **Right chart, "What +1 is worth":** bars at each integer `B` showing `gain(B) = (P(B+1) − P(B)) / P(B)` as a percentage (use `P_adv` when advantage is on). Vertical axis 0% to 110%, and label bars at 100% or more with their value.
- A vertical cursor at the selected `B` in both charts.
- **Readouts (copyable):** need on d20, `P(hit)` (one decimal percent), `P_adv` (two decimals when advantage is on), expected damage per swing (two decimals), gain from next +1 (one decimal percent). In THAC0 mode also show THAC0 and 2e AC.

**Controls (keyboard accessible, labeled):**

1. Selected attack bonus `B`: slider −10 to +25, step 1, default 0.
2. Target AC: slider 5 to 30, step 1, default 15.
3. Damage per hit: stepper 1 to 50, default 10.
4. Toggle "Advantage (roll two, keep higher)", default off.
5. Notation: radio "3rd edition (bonus vs AC)" (default) or "AD&D 2e (THAC0)". In 2e mode, relabel the horizontal axis "THAC0" with value `20 − B` (so it runs from 30 down to −5, left to right unchanged) and the AC control "Target AC (2e)" displaying `20 − AC`. Charts must not change.
6. Reset button.

**Formulas.**

```
need      = AC − B
raw       = (21 + B − AC) / 20
P         = min(0.95, max(0.05, raw))
P_adv     = 1 − (1 − P)^2
expected  = P (or P_adv) × damage
gain(B)   = (P(B+1) − P(B)) / P(B)
THAC0     = 20 − B      AC_2e = 20 − AC
```

Display `need` as "20 (natural 20 only)" when `need ≥ 20` and as "any roll but a natural 1" when `need ≤ 2`.

**Test values** (AC 15, damage 10):

| B | Need | P | Expected | Gain from +1 | P_adv |
|---|---|---|---|---|---|
| −6 | 21 | 5% | 0.50 | 0.0% | 9.75% |
| −5 | 20 | 5% | 0.50 | 100.0% | 9.75% |
| −4 | 19 | 10% | 1.00 | 50.0% | 19.00% |
| 0 | 15 | 30% | 3.00 | 16.7% | 51.00% |
| +4 | 11 | 50% | 5.00 | 10.0% | 75.00% |
| +5 | 10 | 55% | 5.50 | 9.1% | 79.75% |
| +10 | 5 | 80% | 8.00 | 6.25% | 96.00% |
| +13 | 2 | 95% | 9.50 | 0.0% | 99.75% |
| +14 | 1 | 95% | 9.50 | 0.0% | 99.75% |

Check-yourself cases: `B = +7`, AC 19 gives need 12, `P = 45%`, `P_adv = 69.75%`. THAC0 mode with THAC0 15 and 2e AC 2 corresponds to `B = +5`, AC 18, need 13, `P = 40%`.

**First screen:** AC 15, `B = 0`, no advantage, 3rd edition notation. The staircase shows both shaded flat zones, and the right chart shows the tall 100% bar at `B = −5` falling away to zero at `B = +13`. Caption above both charts: "Every +1 adds 5 points of hit chance. At B = 0 it adds 16.7% damage; at B = +10, 6.25%."

**Content rules.** Draw the die as a plain 20-sided outline or just the number; no D&D logos, trade dress or game art. Small text under the charts: "Model: 3rd edition SRD attack roll. THAC0 conversion B = 20 − THAC0, AC = 20 − AC(2e)."
