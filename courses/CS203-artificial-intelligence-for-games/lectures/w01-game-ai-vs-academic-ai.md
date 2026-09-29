# CS203 · Week 01 — Game AI vs Academic AI: The Goal Is Fun

**Why this matters:** Writing an enemy that beats you every time is easy. Writing one that loses well, looks clever while doing it and teaches you how to beat it is the actual job. This week sets the rule for the whole course. Every technique you learn is judged by the experience it creates for the player, not by how well the NPC scores.

**You will be able to:**
- Contrast the academic definition of AI (an agent that maximizes its chance of success) with the game definition (a system that produces a designed experience), using a shipped game as evidence.
- Compute the four Pac-Man ghost target tiles and a ghost's turn choice from a given board state, by hand and in Python.
- Compute how much rest a mode schedule gives the player, and explain why removing it makes the game worse, not harder in a good way.
- Critique an NPC design against five tests: readable, beatable, varied, cheap and authorable.

**Before class:** Millington, *AI for Games* (3rd ed., 2019), chapters 1 and 2 (what game AI is, the model of movement, decision making and strategy). Kevin Dill, "What Is Game AI?", *Game AI Pro* (2013), chapter 1, free online. Steve Rabin, "The Illusion of Intelligence", *Game AI Pro 3* (2017), chapter 1, free online. Play five minutes of any faithful Pac-Man port and watch one ghost at a time.

**Prerequisites from earlier courses:** [CS101 week 11, game state machines](../../CS101-programming-for-games-i/lectures/w11-game-state-machines.md) (Pac-Man's scatter and chase schedule as a state machine; this week uses it and does not re-teach it). [GD101 week 5, player experience goals](../../GD101-introduction-to-game-design/lectures/w05-player-experience-goals-and-the-8-kinds-of-fun.md) (naming the experience you want). [GD101 week 12, feedback and readability](../../GD101-introduction-to-game-design/lectures/w12-feedback-juice-clarity-readability.md) (telegraphs). [MA101 week 14, distances and squared distance](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w14-distances-ranges-and-squared-distance.md) (comparing distances without a square root). [MA101 week 12, 2D vectors](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w12-2d-vectors.md) (adding, subtracting and scaling vectors).

**Interactive:** [`examples/w01-ghost-targets.html`](../examples/w01-ghost-targets.html). Keep it open during section 2.

---

## 1. Two jobs called "AI"

Open a university AI textbook and you will find a definition close to this one. An **agent** perceives its environment and chooses actions that maximize its chance of success. Chess engines, route planners and spam filters are judged this way. More wins, shorter routes, fewer errors. Call this **academic AI**.

Kevin Dill opens *Game AI Pro* by quoting that definition and then setting it aside. His point is that game characters are closer to cartoon characters than to chess engines. Wile E. Coyote does not maximize his chance of catching the Road Runner. He exists to create an experience for the viewer. Dill's rule for **game AI** is that every technique, trick and algorithm should serve one goal, the experience the designers want the player to have. That experience may be fun, fear, tension, or the feeling of being powerful. "Fun" is the shorthand in this course's title, but the real target is whatever experience goal you wrote down in GD101 week 5.

The two goals pull in different directions more often than you would expect.

- **An academic agent should win.** A game enemy usually should lose, and lose in a way that makes the player feel they earned it.
- **An academic agent may use any information it can get.** A game enemy that uses information the player thinks it cannot have feels like cheating, even when the numbers are fair.
- **An academic agent is judged by outcomes.** A game NPC is judged by how its behavior *looks*. Rabin puts it bluntly. Game AI is seldom about deep intelligence and mostly about the *illusion* of intelligence. If the player cannot see a clever decision, it did not happen.
- **An academic agent should think as hard as it can afford.** Dill warns that an AI that thinks too hard can make choices that are sensible inside its model but look random to a player who cannot see the model.

Dill names the one failure you must avoid at all costs: **artificial stupidity**, an action that looks obviously wrong. Walking into walls, getting stuck on geometry and ignoring a player who is shooting you all break the player's belief in the character. Notice that artificial stupidity is about appearance. An NPC can be deliberately weak without looking stupid, and a strong NPC can look stupid if it changes its mind with no visible reason.

### The parts of a game AI

Millington splits game AI into three layers, and this course follows the same order.

1. **Movement.** Turning a decision into motion: steering (week 2) and pathfinding (weeks 3 to 5).
2. **Decision making.** Choosing what to do next: state machines, behavior trees, utility AI and planners (weeks 6 to 9).
3. **Strategy and groups.** Coordinating many agents: perception, formations, MMO mob rules and boss encounters (weeks 10 to 13).

Around all three sits the **agent loop**, often called sense, think, act. Each update the NPC reads the world (where is the player, how hurt am I), decides, and then moves or attacks. The loop runs inside the game loop you built in CS101, which means it shares the frame with rendering, physics and networking. At 60 frames per second a frame lasts 1000 / 60 = 16.7 ms, and the AI gets whatever part of that the rest of the game leaves over. Week 14 is about stretching that budget. Until then, remember that "cheap" is a design requirement, not a nice extra.

## 2. Worked example: four ghosts, four one-line rules

### The hook

Players describe Pac-Man's ghosts (Namco, 1980) as characters. The red one hunts you, the pink one ambushes you, the cyan one is unpredictable and the orange one seems to lose interest. Two ghosts will often come at you from opposite ends of a corridor, and it feels planned.

Nothing is planned. Jamey Pittman's reverse-engineered *Pac-Man Dossier* and Chad Birch's summary of it show that every ghost runs the same tiny movement rule and differs from the others in a single line, the choice of a **target tile**. No ghost plans a path. No ghost knows where the others are going. The trap you feel is four greedy rules overlapping on the same board.

The designer's intent was explicit. Birch quotes Toru Iwatani, Pac-Man's creator, saying he gave each ghost its own character and movement so they would not all chase Pac-Man "in single file", which he thought would be tiresome. The academic answer to "catch Pac-Man" is four perfect pursuers. The designer's answer was four imperfect ones with personalities.

### The model

The board is a grid of tiles. Write a tile as `(x, y)`, with `x` growing to the right and `y` growing *downward*, as in the arcade hardware. A direction is a unit step: up `(0, −1)`, left `(−1, 0)`, down `(0, 1)`, right `(1, 0)`.

**The turn rule (same for every ghost).** When a ghost is about to enter a tile, it looks at the exits of that tile, excluding the way it came in, since ghosts never choose to reverse. For each exit it measures the straight-line distance from the tile beyond that exit to its target tile. It takes the exit with the smallest distance. Ties go to the first direction in the order up, left, down, right. The ghost looks exactly one tile ahead and no further.

**The targets (one per ghost, in chase mode).** Let `P` be Pac-Man's tile, `f` the direction he faces, and `B` Blinky's tile.

| Ghost | Chase target | In words |
|---|---|---|
| Blinky (red) | `P` | where Pac-Man is |
| Pinky (pink) | `P + 4f` | four tiles ahead of Pac-Man |
| Inky (cyan) | `2(P + 2f) − B` | take the tile two ahead of Pac-Man, draw the vector from Blinky to it, and double it |
| Clyde (orange) | `P` if his distance to `P` is 8 tiles or more, otherwise his home corner | chases from far away, retreats when close |

Two details make the table honest. First, the arcade code has an overflow bug. When Pac-Man faces up, "four ahead" becomes four up *and four left*, and Inky's "two ahead" becomes two up and two left. Both sources agree on this, and a faithful model must include it. Second, the sources say Clyde chases when "more than eight tiles away" and retreats when closer. They do not settle what happens at exactly 8. The code below treats exactly 8 as chasing, and the lab tests avoid that edge.

**The schedule.** On top of the targets sits the timer you built in CS101 week 11. In scatter mode every ghost's target becomes a fixed tile outside its own corner of the maze, so the ghosts stop hunting and circle their corners. On level 1 the schedule is scatter 7 s, chase 20 s, scatter 7 s, chase 20 s, scatter 5 s, chase 20 s, scatter 5 s, then chase forever.

Here is the whole targeting model in Python.

```python
UP, LEFT, DOWN, RIGHT = (0, -1), (-1, 0), (0, 1), (1, 0)

def ahead(tile, facing, n):
    """n tiles ahead of Pac-Man, with the arcade's facing-up bug."""
    x, y = tile
    dx, dy = facing
    if facing == UP:
        return (x - n, y - n)          # up AND left: the overflow bug
    return (x + n * dx, y + n * dy)

def blinky_target(pac, facing, blinky):
    return pac

def pinky_target(pac, facing, blinky):
    return ahead(pac, facing, 4)

def inky_target(pac, facing, blinky):
    ox, oy = ahead(pac, facing, 2)
    bx, by = blinky
    return (2 * ox - bx, 2 * oy - by)  # double the vector Blinky -> offset

def clyde_target(pac, clyde, corner):
    dx, dy = pac[0] - clyde[0], pac[1] - clyde[1]
    return pac if dx * dx + dy * dy >= 8 * 8 else corner

pac, facing = (14, 20), UP
blinky, clyde = (20, 14), (10, 24)
print("Blinky", blinky_target(pac, facing, blinky))
print("Pinky ", pinky_target(pac, facing, blinky))
print("Inky  ", inky_target(pac, facing, blinky))
print("Clyde ", clyde_target(pac, clyde, corner=(0, 30)))
```

Output:

```
Blinky (14, 20)
Pinky  (10, 16)
Inky   (4, 22)
Clyde  (0, 30)
```

Clyde's test compares squared distances, the trick from MA101 week 14. You never need the square root to ask "is this closer than 8?". Compare against `8 * 8 = 64` instead.

And the turn rule, the only movement logic a ghost has:

```python
UP, LEFT, DOWN, RIGHT = (0, -1), (-1, 0), (0, 1), (1, 0)
ORDER = [UP, LEFT, DOWN, RIGHT]        # tie-break order

def choose_direction(tile, heading, open_dirs, target):
    """Pick the exit whose next tile is closest to target. Never reverse."""
    reverse = (-heading[0], -heading[1])
    best, best_d2 = None, None
    for d in ORDER:
        if d not in open_dirs or d == reverse:
            continue
        nx, ny = tile[0] + d[0], tile[1] + d[1]
        d2 = (nx - target[0]) ** 2 + (ny - target[1]) ** 2
        if best is None or d2 < best_d2:
            best, best_d2 = d, d2
    return best

# A ghost heading right reaches a crossroads at (5, 5). Its target is (9, 1).
print(choose_direction((5, 5), RIGHT, {UP, LEFT, DOWN, RIGHT}, (9, 1)))
```

Output:

```
(0, -1)
```

Up wins, and it wins on a tie. The tile above `(5, 5)` is `(5, 4)`, at squared distance `(9 − 5)² + (1 − 4)² = 16 + 9 = 25` from the target. The tile to the right is `(6, 5)`, at `(9 − 6)² + (1 − 5)² = 9 + 16 = 25`. Down is `(5, 6)`, at `16 + 25 = 41`. Left is the reverse and is never considered. Up and right tie at 25, and up comes first in the tie order. Ties like this are common on a grid, which is why the tie order is part of the model and not a footnote.

This function is the bare turn rule, and it has one gap. At a dead end, where the only open exit is the reverse, the loop skips everything and returns `None`. The arcade maze has no dead ends, so the arcade never hits this case. Your lab maze and the interactive handle it with one extra rule: if no exit other than the reverse is open, the ghost reverses. Lab 01 asks you to add that line.

### Numbers you can check

The board state from the code, worked by hand. Pac-Man is at `(14, 20)` facing up. Blinky is at `(20, 14)`, Clyde at `(10, 24)`, Clyde's corner at `(0, 30)`.

| Ghost | Working | Target |
|---|---|---|
| Blinky | `P` | (14, 20) |
| Pinky | facing up, so `(14 − 4, 20 − 4)` with the bug | (10, 16) |
| Inky | offset `(14 − 2, 20 − 2) = (12, 18)`; `2 × (12, 18) − (20, 14)` | (4, 22) |
| Clyde | `(14 − 10)² + (20 − 24)² = 32 < 64`, so he is within 8 tiles | corner (0, 30) |

Turn Pac-Man to face right and only Pinky and Inky change. Pinky's target becomes `(18, 20)`, the intended four ahead. Inky's offset becomes `(16, 20)` and his target `(12, 26)`. Notice what Inky's rule does geometrically. Blinky sits up and to the right of Pac-Man, so Inky's target lands down and to the left. The two ghosts approach from opposite sides without any shared plan. The "pincer" is a property of the vector arithmetic.

Now the schedule. How much of the opening is rest? The table was computed frame by frame at 60 Hz from the published schedules (the lab has the code).

| Levels | Schedule (s), starting with scatter | Scatter in first 60 s | Scatter in first 180 s |
|---|---|---|---|
| 1 | 7, 20, 7, 20, 5, 20, 5, then chase | 19 s (31.7%) | 24 s (13.3%) |
| 2 to 4 | 7, 20, 7, 20, 5, 1033, 1/60, then chase | 19 s (31.7%) | 19 s (10.6%) |
| 5 and up | 5, 20, 5, 20, 5, 1037, 1/60, then chase | 15 s (25.0%) | 15 s (8.3%) |

Two things stand out. The first minute of every level gives the player a quarter to a third of the time with nobody hunting. And the relief shrinks as the game goes on, both inside a level (later scatters are shorter) and across levels. The difficulty curve is written in the rest, not only in ghost speed.

### Move it yourself

Open [the interactive](../examples/w01-ghost-targets.html). The left view is a small maze with Pac-Man and four ghosts. Drag Pac-Man, change his facing, and watch the four target markers move. Inky's construction line from Blinky through the offset tile is drawn so you can see the doubling. The right view steps the ghosts forward with the turn rule and shows the mode timeline underneath. Switch on "four Blinkys" and every ghost uses Blinky's target. Watch the "bunched" readout climb as the ghosts collapse into one group trailing Pac-Man, the flat chase Iwatani avoided. In the lab's version of this run (Pac-Man looping the outer ring for 200 s of game time), the four ghosts are bunched in 10% of chase steps with their personalities and 80% as four Blinkys. Their mean spacing halves, from 7.4 tiles to 3.7. Switch it off and they spread out again.

### Why the greedy rule is a feature

The turn rule is short-sighted. Birch shows a case where the straight-line choice sends a ghost on a 26-tile route when the other exit would have reached the target in 8. By academic standards that is a bug. By game standards it is part of the design.

- **It is readable.** A player can learn "the pink one goes where I am facing" in a few games. Nobody can learn the output of a full search.
- **It is beatable.** Short-sighted ghosts can be baited. Good players turn at the last moment so Pinky commits to the wrong corridor.
- **It is cheap.** At most three squared distances per ghost per tile, with no search, ran comfortably on 1980 arcade hardware.
- **It telegraphs.** Because ghosts never reverse on their own, the forced reversal at a mode change is the one moment a ghost turns around. Birch notes that this reversal acts as a signal to the player that the mode has changed. The design turns a constraint into feedback.

Rabin makes the same point about the schedule. He argues that enemies that sometimes back off are more enjoyable than ones that pursue relentlessly, and cites the ghosts' attack and retreat waves as an early example.

### Cross-game recognition

**Left 4 Dead (Valve, 2008), the AI Director.** Michael Booth's 2009 talk on the game's AI describes an "adaptive dramatic pacing" system. It estimates each survivor's intensity from damage taken and nearby deaths, and it moves through four states. Build Up spawns a full threat population until intensity peaks. Sustain Peak holds it for 3 to 5 seconds. Peak Fade drops to a minimal population and waits for intensity to decay. Relax keeps the population minimal for 30 to 45 seconds, or until the survivors have travelled far enough, and then Build Up starts again. Booth's reasoning is that constant combat is fatiguing and long quiet stretches are boring. This is Pac-Man's scatter and chase schedule, rewritten with a feedback signal. Pac-Man's timer is fixed. The Director's timer is driven by the players' state. Both give the player designed rest.

**F.E.A.R. (Monolith, 2005), squad dialogue.** Rabin describes how F.E.A.R.'s soldiers talk to each other while searching ("where did he go?", "behind the boxes!") and how players read that as coordination. He reports that a separate module watched the situation and triggered the lines, so the talk was presentation rather than planning. It is the same trick as the ghost reversal. The AI's state is made visible to the player on purpose, and the player's mind supplies the intelligence.

**Barks and icons in general.** Dill lists short shouted lines ("Grenade!") and thought icons over characters' heads, as in The Sims, as tools whose job is to explain an NPC's decisions *to the player*. The AI characters do not need them to communicate with each other; they share data in code.

Three games, one principle. The visible behavior is designed for the player: rest periods, telegraphs and explanations. The hidden logic can be as simple as a target tile.

### Eyes-open design judgment

Pac-Man's ghosts are not a template to copy. They are a set of choices to make deliberately.

- **Determinism.** The ghosts are fully predictable, which let players learn exact patterns and let experts master the game. The cost is that once a pattern is known, the enemy stops being a threat. If you want surprise, add controlled randomness, and accept that players can then no longer plan against it.
- **Omniscience.** Every ghost always knows Pac-Man's tile. Players accept it because the rule is consistent and visible in the ghosts' movement. In a stealth game the same omniscience would feel like cheating, because the game has promised the player that hiding works. Decide what the NPC is allowed to know based on what your game has promised.
- **Rest.** A schedule with rest is kinder and more readable. A schedule without it is harder but flatter. Level 2's 1,033-second chase phase shows the designers deliberately removing most of the rest once players had learned the game.
- **Personality through targets.** Four targets from one rule is cheap variety. The cost is that the variety is only as rich as the target rules. When you need NPCs that choose *what* to do as well as *where* to go, you need the decision-making tools of weeks 6 to 9.

## 3. Five tests for an NPC

Use these five tests on every NPC you design in this course. They come from the readings, and each one points to a later week.

1. **Readable.** Can a player explain what the NPC is doing after a few encounters? Readability comes from telegraphs, barks, animation and consistent rules. GD101 week 12 gave you the telegraph budget. Here, ask it of AI decisions as well as attacks.
2. **Beatable, and fair about it.** Can the player win by playing well, and does losing feel like the player's own fault? Rabin gives a concrete number. Humans take at least about 0.2 s to react, and about 0.4 s when a mental comparison is needed. He recommends delaying the NPC's reaction to a decision by at least that much. An NPC that reacts in one frame (16.7 ms) is reacting faster than any human can, and players will feel it even if they cannot name it.
3. **Varied.** Does the NPC produce different situations, or the same one every time? Pac-Man gets variety from four targets. Left 4 Dead gets it from the Director.
4. **Cheap.** Does it fit its share of the frame, for every NPC that will be on screen at once? A rule that costs 0.1 ms is fine for four ghosts and a problem for four hundred MMO mobs.
5. **Authorable.** Can a designer tune it to produce the intended experience? Dill draws the trade-off as a line from scripted AI (full authorial control, little autonomy) through state machines and utility AI to machine learning (much autonomy, little control). He notes that World of Warcraft chose heavily scripted encounters that are predictable on purpose, while games like The Sims need more autonomy. Neither is wrong. They deliver different experiences.

A useful habit is to write these five tests at the top of every AI design document and fill in how your design passes each one.

## 4. Cheating, and when it is allowed

Game AI cheats constantly. The ghosts know where Pac-Man is. Strategy AIs often receive extra resources on hard difficulties. Racing AIs are often tuned to stay near the player. Whether cheating is acceptable is a design question with a practical test. **Players judge what they can see.**

- **Invisible, consistent advantages** (knowing the player's position in a maze chase, a hidden resource bonus) are usually accepted as long as the outcomes feel fair.
- **Visible violations of the game's own rules** (an enemy that sees through a wall the game told you hides you, or a shot that hits from behind cover) break trust fast, because the player can point to the moment the rule was broken.
- **Advantages that remove the player's agency** (an enemy that reacts faster than humanly possible and so cannot be baited) make the game feel unfair even when the player cannot say why.

When you do cheat, cheat in the player's favor as often as against them, and never in a way the player can catch in the act.

## 5. How this course is built

Every week follows the same pattern. A technique from the game AI toolbox is introduced, built in Python in the lab, and then judged with the five tests. Weeks 2 to 5 cover movement. Weeks 6 to 9 cover decisions. Weeks 10 to 13 cover perception, groups and the MMO-specific problems of mob aggro, threat and bosses. Week 14 covers performance. The final demo asks you to build a small NPC ecosystem and defend it against the five tests, so start collecting examples of AI that passes and fails them now.

## In-class activity (25 minutes)

Pairs. Each pair gets a printed 12 × 12 tile grid with walls, one Pac-Man position and facing, and the positions of all four ghosts.

1. **Targets (8 min).** Compute all four chase targets by hand. Mark them on the grid in different colors. Draw Inky's construction line.
2. **One step (7 min).** For the two ghosts nearest an intersection, apply the turn rule. Show the squared distances for each legal exit and name the tie-break if one is needed.
3. **Swap one rule (7 min).** Invent a fifth ghost with a new target rule in one line (for example, "the tile halfway between Pac-Man and the nearest power pellet"). Predict in one sentence how it will feel to play against. Score it against the five tests from section 3.
4. **Share (3 min).** One pair per table presents their fifth ghost. The class votes on whether it is readable.

Expected output: the marked grid, a turn table with squared distances, and a one-line fifth-ghost rule with its five-test scores.

## Common misconceptions

- **"Good game AI is smart AI."** Good game AI produces the intended experience. The ghosts are short-sighted by any academic measure, and that is part of why the game works. Ask "what should the player feel?" before "how clever can it be?".
- **"The ghosts coordinate their attacks."** No ghost reads another's plan. Inky reads Blinky's *position*, and that is all. The pincer you feel comes from the geometry of four targets.
- **"More information makes a better NPC."** More information makes a stronger NPC. Whether it makes a better one depends on what the player believes the NPC can know. Knowing the player's position is fine in Pac-Man and unfair in a stealth game.
- **"Rest periods make a game easier, so hard modes should remove them."** Rest periods give the player time to read the situation and plan. Removing them makes a game flatter as well as harder. Pac-Man shrinks its rests gradually across levels; it never removes them in the first minute.

## Check yourself

1. Pac-Man is at `(10, 12)` facing left. Blinky is at `(14, 8)`. Give Pinky's and Inky's chase targets.
2. Clyde is at `(4, 18)` and Pac-Man at `(10, 12)`. Is Clyde chasing or retreating? What if Clyde is at `(5, 16)`? Answer without taking a square root.
3. A ghost heading left arrives at `(7, 5)`, where the exits are up, left, down and right. Its target is `(10, 2)`. Which way does it turn? Show the squared distances.
4. On level 5, how many seconds of scatter does the player get in the first 55 seconds? What fraction is that?
5. A designer wants to make the ghosts "smarter" by replacing the turn rule with a full shortest-path search to each target. Name one of the five tests this helps and one it hurts, with a reason for each.

<details>
<summary>Answers</summary>

1. Facing left, `f = (−1, 0)`, no bug. Pinky: `(10 − 4, 12) = (6, 12)`. Inky: offset `(8, 12)`, target `2 × (8, 12) − (14, 8) = (2, 16)`.
2. At `(4, 18)`: `6² + 6² = 72 ≥ 64`, so Clyde is 8 or more tiles away and chases Pac-Man's tile `(10, 12)`. At `(5, 16)`: `5² + 4² = 41 < 64`, so he retreats to his corner.
3. Right is the reverse and is skipped. Up `(7, 4)`: `3² + 2² = 13`. Left `(6, 5)`: `4² + 3² = 25`. Down `(7, 6)`: `3² + 4² = 25`. Up wins with 13.
4. The schedule is 5 scatter, 20 chase, 5 scatter, 20 chase, 5 scatter, which is exactly 55 s. Scatter totals 15 s, so 15 / 55 = 27.3%.
5. It hurts "cheap", since a search per ghost per intersection costs far more than three distance checks. It hurts "readable", since players can no longer predict a ghost from a one-line rule. It also hurts "beatable" for most players, because a ghost that never takes the wrong corridor cannot be baited. It can help a designer who wants a harder expert mode, which is a "varied" argument, a different ghost for a different audience. Any answer that ties a test to a concrete mechanism is correct.

</details>

## Lab / assignment hook

[Lab 01, ghost brains](../labs/lab01.md). Implement the four target rules, the turn rule and the mode schedule in Python so the provided tests pass, then run the included maze simulation and measure how much the ghosts bunch together with and without their personalities. Deliverable: the passing code, a table of your measurements and a 300-word design note on a fifth ghost of your own.

## Sources

- Dill, K. (2013). "What Is Game AI?" In S. Rabin (ed.), *Game AI Pro*, chapter 1. CRC Press. Free at gameaipro.com. The academic definition of an agent, the cartoon comparison, artificial stupidity, barks and icons, and the authorial control versus autonomy trade-off with World of Warcraft and The Sims as examples.
- Rabin, S. (2017). "The Illusion of Intelligence." In S. Rabin (ed.), *Game AI Pro 3*, chapter 1. CRC Press. Free at gameaipro.com. Game AI as illusion; human reaction times of about 0.2 s and 0.4 s; enemies that back off being more enjoyable, with Pac-Man's attack and retreat waves as the example; F.E.A.R.'s squad dialogue triggered by a separate module (citing Orkin).
- Pittman, J. (2009). "The Pac-Man Dossier." Game Developer (originally Gamasutra), February 2009. Original arcade Pac-Man (Namco, 1980). Target tiles for all four ghosts; the facing-up offset bug for Pinky and Inky; the turn rule with the up, left, down, right tie order; no voluntary reversal; scatter and chase schedules for level 1, levels 2 to 4 and levels 5 and up; forced reversal on mode changes. https://www.gamedeveloper.com/design/the-pac-man-dossier
- Birch, C. (2010). "Understanding Pac-Man Ghost Behavior." GameInternals, December 2, 2010 (read via the Internet Archive, September 2026). Straight-line distance for the turn rule; the 26-tile versus 8-tile wrong-turn example; Clyde's eight-tile rule; the reversal as a signal to the player; the Iwatani quotation about ghosts not chasing in single file.
- Booth, M. (2009). "The AI Systems of Left 4 Dead." Valve. Slides from the 2009 talk. Adaptive dramatic pacing; survivor intensity; Build Up, Sustain Peak (3 to 5 s), Peak Fade and Relax (30 to 45 s) states; the Counter-Strike inspiration. https://steamcdn-a.akamaihd.net/apps/valve/2009/ai_systems_of_l4d_mike_booth.pdf
- Millington, I. (2019). *AI for Games*, 3rd ed. CRC Press. Chapters 1 and 2. The movement, decision making and strategy model.
- The 12 × 12 activity grid, the fifth-ghost exercise and the board positions in the tables are invented for teaching.

## Interactive spec: examples/w01-ghost-targets.html

**The one insight:** four ghosts running one greedy turn rule with four different target tiles produce a pincer that no ghost planned; give them all Blinky's target and they collapse into one trailing group. Seeing the targets move as you drag Pac-Man, and then seeing the group form when the personalities are switched off, is the moment the lesson lands.

**Layout.** Two linked views, side by side at 1280 px, stacked at 390 px (maze on top).

- **Left, "Targets":** a 25 × 29 tile maze (fixed layout, below) drawn with generic shapes. Pac-Man is a filled circle with a small wedge showing facing. Ghosts are rounded squares in four palette colors with text labels B, P, I, C (color is never the only cue). Each ghost's current target is an X marker in its color with the same letter. Inky's construction is drawn as a thin dashed line from Blinky through the offset tile (small hollow circle) to Inky's target. Clyde's 8-tile radius is a faint circle around Pac-Man, and Clyde's marker reads "C (retreat)" when inside it. Targets outside the grid are drawn clipped at the edge with an arrow.
- **Right, "Run":** the same maze at smaller scale where ghosts move one tile per step using the turn rule. Below it, a horizontal mode timeline for the selected level preset, with scatter bands and chase bands labelled with their seconds, a playhead, and the readouts "scatter so far: N s (P%)" for the first 60 s and first 180 s.

**Maze.** 25 columns (`x` 0 to 24) by 29 rows (`y` 0 to 28). A tile is a wall block when both `x` and `y` are odd; every other tile is open. This gives a regular lattice with intersections at even-even tiles. Tunnels and the ghost house are omitted. Scatter corners (targets outside the grid): Blinky `(24, −2)`, Pinky `(0, −2)`, Inky `(24, 30)`, Clyde `(0, 30)`. Clyde's corner matches the lecture's code.

**Controls (keyboard accessible, labelled):**

1. Drag Pac-Man to any open tile, or move him with arrow keys when the maze has focus. Facing buttons Up, Left, Down, Right (also W, A, S, D).
2. Drag any ghost to any open tile (keyboard alternative: a "Ghost" select plus arrow keys).
3. Mode select: Chase, Scatter. In Scatter all targets jump to the corners.
4. Checkbox "Facing-up bug" (on by default). Off shows the intended targets.
5. Checkbox "Four Blinkys" (off by default): every ghost uses Blinky's target.
6. Run view: Play/Pause, Step, Reset, speed select (1, 2, 4 steps per second), level preset select (Level 1, Levels 2 to 4, Level 5+). In the run view Pac-Man moves along a fixed looping route so runs are reproducible, exactly as `simulate()` in `labs/lab01-starter/ghosts.py`. The route starts at `(0, 0)` and goes right along row 0, down column 24, left along row 28 and up column 0, one tile per step. Ghosts start at Blinky `(12, 14)`, Pinky `(12, 12)`, Inky `(10, 14)`, Clyde `(14, 14)`, all heading left. At step `s` Pac-Man is at route tile `s` and faces route tile `s + 1`; the mode is `mode_at(0.25 s)`; every ghost then moves one tile (reversing if the mode changed since the previous step, otherwise using the turn rule); then the readouts update if the mode is chase.
7. Readouts "mean spacing" (mean Manhattan distance over the 6 ghost pairs) and "bunched" (fraction of chase-mode steps in which all four ghosts fit in a box whose width plus height is at most 6 tiles), both accumulated since the last Reset.

**Formulas.** Directions up `(0, −1)`, left `(−1, 0)`, down `(0, 1)`, right `(1, 0)`. `ahead(P, f, n) = (P.x − n, P.y − n)` if `f` is up and the bug is on, else `P + n·f`. Blinky `P`. Pinky `ahead(P, f, 4)`. Inky `2·ahead(P, f, 2) − B`. Clyde `P` if `(P − C)·(P − C) ≥ 64`, else his corner. Turn rule: exclude the reverse of the current heading; among open exits in order up, left, down, right, pick the smallest squared distance from the next tile to the target; ties to the earlier direction. At a dead end (only the reverse open) the ghost reverses. On a mode change every ghost reverses on its next step. Schedules: Level 1 `[7, 20, 7, 20, 5, 20, 5]`; Levels 2 to 4 `[7, 20, 7, 20, 5, 1033, 1/60]`; Level 5+ `[5, 20, 5, 20, 5, 1037, 1/60]`; even indices are scatter, after the list chase forever. The run view maps 1 step to 0.25 s of game time for the timeline.

**Test values (must match).**

- Pac-Man `(14, 20)` facing up, Blinky `(20, 14)`, Clyde `(10, 24)`, bug on: Blinky target `(14, 20)`, Pinky `(10, 16)`, Inky `(4, 22)`, Clyde retreats (squared distance 32).
- Same, facing right: Pinky `(18, 20)`, Inky `(12, 26)`.
- Same, facing up with the bug off: Pinky `(14, 16)`, Inky offset `(14, 18)`, Inky target `(8, 22)`.
- Pac-Man `(10, 12)` facing left, Blinky `(14, 8)`: Pinky `(6, 12)`, Inky `(2, 16)`. Clyde at `(4, 18)` chases (72); at `(5, 16)` retreats (41).
- Turn rule (function-level tests, independent of the maze): at `(5, 5)` heading right, target `(9, 1)`, all four exits open: up and right tie at 25, up chosen. At `(7, 5)` heading left, target `(10, 2)`: up 13, left 25, down 25, up chosen.
- Run view, Level 1, Reset then 800 steps: with personalities, mean spacing 7.39 tiles and bunched 10%; with "Four Blinkys", 3.66 tiles and 80%. These match `simulate()` in the lab starter with a correct solution.
- Timeline readouts: Level 1, 19.00 s (31.7%) and 24.00 s (13.3%). Levels 2 to 4, 19.00 s (31.7%) and 19.00 s (10.6%). Level 5+, 15.00 s (25.0%) and 15.00 s (8.3%).

**First screen.** Chase mode, Pac-Man at `(14, 20)` facing up with Blinky `(20, 14)`, Pinky `(2, 2)`, Inky `(18, 18)`, Clyde `(10, 24)`, all four target markers and Inky's dashed line visible. Caption: "Same rule, four targets. Drag Pac-Man and watch them spread."

**Accessibility.** All controls reachable by Tab with visible focus. A live region announces target changes in text ("Pinky target 10, 16"). Respects `prefers-reduced-motion` (Play steps once per second with no tweening) and `prefers-color-scheme`. Palette from `templates/interactive-tokens.css`. No Pac-Man or ghost art: circles and rounded squares only.
