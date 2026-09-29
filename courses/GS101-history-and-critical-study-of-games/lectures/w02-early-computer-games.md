# GS101 · Week 02 — Early computer games: Spacewar!, Tennis for Two

**Why this matters:** Every action game you will build runs a loop that nudges velocity, then position, many times a second. That loop was already running in a physics lab in 1958 and on a university minicomputer in 1962. Knowing where it came from, and what the people who built it could and could not afford, lets you read early games as design decisions rather than curiosities.

**You will be able to:**
- Compare the candidates for "the first video game" against explicit criteria and defend which criteria you chose.
- Compute a few steps of a projectile and an orbit by hand using the update loop, and predict how update order and step size change the result.
- Explain how Tennis for Two and Spacewar! use the same loop with different acceleration rules, and recognise that loop in later games.
- Critique the claim that Spacewar! "could have been" a commercial product in 1962, using the cost of the hardware as evidence.

**Before class:** Donovan, *Replay: The History of Video Games* (2010), the early pages on the pre-commercial pioneers (Tennis for Two, Spacewar! and their predecessors). The course reader lists the pages. Brookhaven National Laboratory, "The First Video Game?" (the lab's own history page, about 1,000 words). Graetz, J. M. (1981), "The Origin of Spacewar," *Creative Computing*, August 1981 (a first-hand account by one of the authors; read the sections on the gravity star and hyperspace).

**Prerequisites from earlier courses:** None formally. From this course, [week 1](w01-play-before-computers.md) (evidence types and the close-reading method). If you are taking MA101 alongside, [MA101 week 3, polynomials and quadratic curves](../../MA101-mathematics-for-games-i-algebra-functions-trigon/lectures/w03-polynomials-and-quadratic-curves.md) derives the projectile parabola and warns about step-by-step drift. The full treatment of integration methods is in MA201 week 7, numerical integration (see the [MA201 week 7 lecture](../../MA201-linear-algebra-and-physics-for-games/lectures/w07-numerical-integration-euler-semi-implicit-verlet.md)). [GD101 week 1](../../GD101-introduction-to-game-design/lectures/w01-what-is-a-game.md) gives the definitions of "game" that section 1 relies on.

**Interactive:** [One update loop, two games](../examples/w02-one-update-loop.html). Keep it open during section 2.

---

## 1. Which game was first? It depends on your definition

Ask ten people for the first video game and you will hear *Pong*, *Spacewar!*, *Tennis for Two* and possibly something older. They are not disagreeing about facts. They are disagreeing about the definition. Here are the main candidates, all dated from the sources at the end of the lecture.

| Year | Name | Where | Ran on a computer? | Picture on a screen? | Moving picture updated in real time? | Made mainly for play? |
|---|---|---|---|---|---|---|
| 1947 (patent filed) | Cathode-ray tube amusement device, Goldsmith and Mann | USA | No, analog circuits | Yes, CRT with paper overlays | Yes, a moving dot | Yes, but never manufactured |
| 1950 | Bertie the Brain, Josef Kates | Canadian National Exhibition, Toronto | Yes, a special-purpose machine | No, light bulbs | — | No, it demonstrated a new vacuum tube |
| 1951 | Nimrod, Ferranti | Festival of Britain | Yes | No, light bulbs | — | No, it demonstrated computing |
| 1952 | OXO, A. S. Douglas | EDSAC, University of Cambridge | Yes | Yes, a 35 × 16 dot CRT | No, a static board redrawn after moves | No, part of a doctoral thesis |
| 1958 | Tennis for Two, William Higinbotham | Brookhaven National Laboratory | Yes, an analog computer | Yes, an oscilloscope | Yes | Yes, for a public visitors' day |
| 1962 | Spacewar!, Steve Russell and others | MIT, DEC PDP-1 | Yes, a digital minicomputer | Yes, a vector display | Yes | Yes |

Pick your criteria and the "first" changes. If you require a digital computer and a real-time moving picture, Spacewar! wins. If an analog computer counts, Tennis for Two wins. If a computer is not required, the 1947 device, which was never sold, has a claim. If you require the game to have been sold, you have to wait until 1971, which is next week.

The historian's job is not to crown one. It is to state the criteria and show what each one includes. Notice that the table uses the same move as GD101 week 1: turn a vague word into a checklist, then run the candidates through it.

Two patterns stand out in the table. First, nearly every early machine was built to demonstrate something else: a vacuum tube, a computer, a research idea about how people interact with machines. Play was the demonstration that crowds understood. Nimrod's official guidebook argued that teaching a machine to play games was worthwhile because it proved the machine could handle complex problems, and the Festival crowds ignored the argument and simply played. Second, almost none of these machines could be copied. Each was a one-off, tied to a building and a budget. That changes with Spacewar!, and section 3 explains why only partly.

### Tennis for Two (1958)

William Higinbotham was head of the Instrumentation Division at Brookhaven National Laboratory, a US government research lab on Long Island. Each year the lab opened to visitors, and the displays were static. For the visitors' day on 18 October 1958 he designed a game, and the technician Robert Dvorak assembled it in about three weeks.

The display was a five-inch oscilloscope showing a side view of a tennis court: a ground line and a short vertical net. Each player held a small box with a knob to set the angle of the shot and a button to hit. The ball flew in an arc, bounced, and could hit the net. There was no score on screen.

The computer was a Donner Model 30 analog computer. An analog computer does not count in steps. It represents quantities as voltages and uses amplifier circuits that integrate continuously, so a voltage for velocity feeds a circuit whose output is position. The Donner's own manual included examples of trajectories of a bullet and a bouncing ball under gravity and air resistance. Higinbotham used some of the computer's amplifiers to generate the ball's motion and others to detect when the ball hit the ground or the net. In 1959 the game returned with a larger screen and settings for low gravity, like the Moon, and high gravity, like Jupiter. Then it was taken apart for its parts.

It was nearly forgotten. It came back into the record in the late 1970s and early 1980s, when Higinbotham testified in patent litigation between Magnavox, maker of the first home console, and its competitors. Keep that in mind when you read "firsts." Some games are remembered because they were famous at the time. Others are remembered because a lawsuit needed them.

### Spacewar! (1962)

In September 1961 a Digital Equipment Corporation (DEC) PDP-1 minicomputer was installed at MIT. It had a round vector display, which draws lines and points directly rather than scanning a grid. A group of students and staff, several of them members of MIT's model railroad club, decided that the best demonstration of the machine would be a game. Steve Russell had a movable dot running before the end of January 1962 and rotating ships by February, roughly 200 hours of work. Martin Graetz and Wayne Wiitanen were among the originators of the idea.

Two ships, "the needle" and "the wedge," fly in open space and fire torpedoes at each other. Each ship has limited fuel and a limited number of torpedoes. The game was not finished when it first ran. Others added the features that made it last:

- **The star field.** Peter Samson wrote the "Expensive Planetarium," a background of real stars drawn from star charts.
- **The gravity star.** Dan Edwards thought plain ships flying in straight lines were dull and added a star at the centre that pulls both ships toward it. Section 2 is about this.
- **Hyperspace.** A panic button that makes the ship vanish and reappear somewhere random, with increasing risk of destruction in later versions.
- **Control boxes.** Alan Kotok and Bob Saunders built hand controllers, so players no longer had to crowd around the computer's own switches.

## 2. Worked example: one loop, two games

### The hook

Tennis for Two's ball and Spacewar!'s ships look like different problems. One is a ball arcing over a net. The other is a spaceship falling around a star. Yet you can reproduce both with the same four lines of code. And if you swap the order of two of those lines, Spacewar!'s ship drifts away from the star within a single orbit. The historical Spacewar! code puts the lines in the order that keeps the orbit.

### The model

A moving object has a position `(x, y)` and a velocity `(vx, vy)`. An **acceleration rule** says how velocity changes, given where the object is. Each tick of the loop advances time by a step `dt`:

```
(ax, ay) = accel(x, y)       # the only part that differs between games
vx = vx + ax × dt            # update velocity first
vy = vy + ay × dt
x  = x + vx × dt             # then position, using the new velocity
y  = y + vy × dt
```

Updating velocity first and then position with the new velocity is called **semi-implicit Euler** (or symplectic Euler). Doing it the other way round, position with the old velocity and then velocity, is **explicit Euler**. Both are one-line changes of each other.

The two games differ only in `accel`:

- **Tennis ball (uniform gravity):** `accel(x, y) = (0, −g)`, with `g` the gravity strength. Tennis for Two computed this continuously with analog circuits, which is the limit of the loop as `dt` shrinks toward zero.
- **Spacewar! (central star):** `accel(x, y) = (−x / d³, −y / d³) × G`, where `d = √(x² + y²)` is the distance to the star at the origin and `G` sets its strength. This is the form Norbert Landsteiner documents in his line-by-line reading of the PDP-1 source code: the program computes the distance, cubes it and divides each coordinate by it. The size of this vector is `d / d³ = 1 / d²`, so the pull falls off with the square of distance, like Newton's gravity.

### Numbers you can check: the tennis ball

Launch a ball from the ground with `vx = 4` and `vy = 6` (units per second), `g = 9.8`, and `dt = 0.1` s. The exact answer from physics class is a parabola with its highest point at `vy² / (2g) = 36 / 19.6 ≈ 1.84` units.

| Time | Exact height | Semi-implicit height | Explicit height |
|---|---|---|---|
| 0.0 | 0.000 | 0.000 | 0.000 |
| 0.1 | 0.551 | 0.502 | 0.600 |
| 0.2 | 1.004 | 0.906 | 1.102 |
| 0.3 | 1.359 | 1.212 | 1.506 |
| 0.6 | 1.836 | 1.542 | 2.130 |
| Highest point | 1.837 | 1.542 | 2.142 |

Check the first semi-implicit row. Velocity first: `vy = 6 − 9.8 × 0.1 = 5.02`. Then position: `y = 0 + 5.02 × 0.1 = 0.502`. For the explicit row, position first with the old velocity: `y = 0 + 6 × 0.1 = 0.6`, then `vy = 5.02`.

At this coarse step, one version flies about 0.3 units too low and the other about 0.3 too high. The exact curve sits between them. For a tennis game that is harmless, since the ball just flies a slightly different arc every time in the same way. Halve `dt` and both errors halve.

### Numbers you can check: the orbit

Now put a ship at `(1, 0)` moving at `(0, 1)` around a star with `G = 1`. With those numbers, the exact motion is a circle of radius 1 that takes `2π ≈ 6.28` time units per lap. Run the loop with `dt = 0.1` for one lap (63 steps).

| Method | Distance after 1 step | After 2 steps | After 3 steps | After one lap |
|---|---|---|---|---|
| Semi-implicit | 0.995 | 0.990 | 0.985 | 1.001 |
| Explicit | 1.005 | 1.010 | 1.015 | 2.090 |

Check the first explicit step: position first, `(1 + 0 × 0.1, 0 + 1 × 0.1) = (1, 0.1)`, distance `√1.01 ≈ 1.005`. The ship has stepped along the tangent, off the circle and outward.

The semi-implicit ship wobbles slightly and comes back to radius 1.001 after a full lap. The explicit ship has more than doubled its distance in one lap and keeps spiralling out. Halving the step to `dt = 0.05` leaves the semi-implicit ship at 1.000 and the explicit one still drifts to 1.58. For a tennis ball, update order changes the arc a little. For an orbit, it decides whether orbits exist at all.

Landsteiner's reading of the Spacewar! source shows the gravity terms being added into the ship's velocity each frame, and the position then moved by a small fraction of that velocity. That is velocity first, the stable order. Whether Edwards chose it for stability or because it was the natural way to write it is not recorded in the sources for this lecture. The effect is clear either way. Ships can slingshot around the star and settle into repeatable paths, which is what made the star a tactical object rather than a random hazard.

### A visual you can move

Open `examples/w02-one-update-loop.html`. The left panel is the tennis court. The right panel is the star. Both are driven by one loop and one step-size slider. Toggle "update order" and watch the tennis arc shift a little while the orbit on the right either holds or spirals away. Then drag `dt` down toward zero and watch both methods converge on the exact curve, the curve Tennis for Two's analog circuits drew directly.

### Cross-game recognition

The loop with a swappable `accel` is the skeleton of most real-time games. Here are three more from the period this course covers, each written in the same form.

- **Lunar Lander (Jim Storer's 1969 text game for the PDP-8, and Atari's 1979 vector arcade game).** `accel = (0, −g) + thrust`, where thrust is set by the player and burns fuel. Gravity alone is the tennis ball. The game is the player's fight against it. The arcade version also let players buy more fuel with more coins, a link to next week.
- **Asteroids (Atari, 1979).** `accel = thrust − friction × velocity`, with thrust only in the facing direction. There is no gravity. The ship keeps drifting for a while after you let go and slowly comes to rest. The small friction term is a design choice. Remove it and the ship drifts forever, as in real space, which is harder to control.
- **Computer Space and Galaxy Game (both 1971).** Both began as Spacewar! for paying customers. Galaxy Game kept the gravity star, so its `accel` is Spacewar!'s. Computer Space dropped it, so its `accel` is thrust alone. Next week you will see how that one difference sat inside two very different business plans.

When you meet a new action game, ask two questions. What is `accel` here, and what sets the initial velocity? The rest is the loop.

### Eyes-open design judgment

- **Realism is a setting, not a virtue.** Tennis for Two in 1959 let players pick Moon or Jupiter gravity. The designers treated `g` as a dial for play, not a physical constant. Spacewar!'s star exists because someone thought straight-line flight was dull. Both are design choices dressed as physics.
- **Step size and update order are part of your game's rules.** If `dt` depends on frame rate, your jump height or orbit depends on the player's hardware. Modern engines use a fixed physics step for this reason. MA201 treats the methods formally. As a designer you need only remember that "the same code" can play differently at 30 and 60 frames per second unless someone chose otherwise.
- **Pick the method that preserves what the player relies on.** In a tennis game the player relies on arcs looking consistent, and any method works if `dt` is fixed. In an orbital game the player relies on orbits being stable, so the cheaper explicit method breaks the game. Choose by what must not drift.

### Check the model

1. Using semi-implicit Euler with `g = 9.8`, `dt = 0.1` and a launch at `vy = 6`, compute the height after the fourth step, starting from the 0.3 row of the table.
2. In a Spacewar!-style field with `G = 1`, a ship sits at distance 2 from the star. How strong is the pull compared with distance 1?
3. Tennis for Two's Moon setting lowered `g`. If `g` drops to one sixth and the launch velocity stays the same, what happens to the highest point of the exact arc?

<details>
<summary>Answers</summary>

1. After three steps `y = 1.212` and `vy = 3.06`. Step four: `vy = 3.06 − 0.98 = 2.08`, `y = 1.212 + 0.208 = 1.420`.
2. The pull is `1 / d²`, so at distance 2 it is one quarter as strong.
3. The highest point is `vy² / (2g)`, so it becomes six times higher, about 11.0 units. The ball also stays in the air six times longer.

</details>

## 3. Who played, and why nobody sold it

Spacewar! spread in a way no earlier game had. DEC learned of it soon after it was written and demonstrated it on PDP-1s. People carried copies of the program to other PDP-1 sites, including Stanford and the research firm Bolt Beranek and Newman. Other programmers extended it. On 19 October 1972 the Stanford Artificial Intelligence Laboratory hosted the "Intergalactic Spacewar! Olympics," sponsored by *Rolling Stone* magazine and often called the first video game tournament.

So why did no one sell it? Look at the hardware. A PDP-1 cost $120,000 at the time, and DEC sold only 53 of them. A game that needs a machine priced like a large house, and that exists in about 50 copies worldwide, has no market. The people who played Spacewar! in the 1960s were students, researchers and engineers at institutions that owned such machines for other reasons.

This matters for how you read the period. The early games were not "ahead of their time" in some vague sense. They sat inside a specific economic arrangement. Governments and universities bought expensive computers for research. Staff had after-hours access. Software was shared freely among a small community, because there was nobody to sell it to and the culture of those labs valued sharing. Games grew in that space as demonstrations, as tests and as fun.

Two things had to change before a game could be a product. The cost of the machine per player had to fall by orders of magnitude, and someone had to find a way to charge each player. Both happened in 1971, when two different teams tried to turn Spacewar! into a coin-operated machine. One built a $20,000 minicomputer installation. The other threw the computer out entirely. That is next week's story.

## 4. Reading Spacewar! closely

Use the method from week 1 on Spacewar!.

**Describe.** Two ships, a central star, limited fuel, limited torpedoes, a hyperspace escape, a starry background, no score on screen in early versions. Evidence: the surviving source code, which has been preserved and emulated, plus first-hand accounts by Graetz and others. This is unusually good evidence. You can run the actual program today in an emulator, which you cannot do for Senet.

**Find the machine.** The gravity star. With it, every manoeuvre has a cost that depends on position. Flying close to the star is fast and dangerous. Firing a torpedo near the star bends its path. The star turns an open space into a map with regions.

**Name the experience.** In Caillois's terms, mostly agon: a symmetric duel of skill. Hyperspace adds a dose of alea, a gamble taken in desperation. The Expensive Planetarium adds something close to mimicry, since it asks the player to believe in a real sky.

**Context.** A tiny, highly skilled audience of engineers who could read the code and change it. Nobody was paying per play. There was no reason to keep sessions short or to make the game learnable in a minute.

**Claim.** Here is one you could argue: *Spacewar!'s depth and its difficulty both come from the same place, the fact that its players were also its programmers.* The next lecture tests that claim. When Nolan Bushnell and Ted Dabney took the Spacewar! idea to bars in 1971, the game that had delighted engineers proved too complicated for the general public. The audience changed, and the design had to change with it.

## In-class activity (25 min)

In pairs, one laptop or one sheet of squared paper per pair.

1. Run the semi-implicit loop by hand, or in a spreadsheet, for the tennis ball with `dt = 0.2` instead of 0.1. Record the highest point.
2. Do the same with explicit Euler.
3. Compare both with the exact 1.84 and with your `dt = 0.1` values from the table. How does the error scale when `dt` doubles?
4. Choose one of Lunar Lander, Asteroids or an artillery game. Write its `accel` rule and one sentence about what the rule does to how the game feels.

Expected output: two short tables, a sentence on how the error scales, and one `accel` rule with a sentence of judgment.

## Common misconceptions

- **"Pong was the first video game."** Pong (1972) was the first hugely successful arcade video game. Several earlier games ran on screens, and Computer Space was sold before it.
- **"Tennis for Two ran a program."** It ran on an analog computer, which integrates voltages continuously. There was no stored program and no step size.
- **"Spacewar!'s gravity is only a visual effect."** It changes velocity every frame and shapes every manoeuvre. It is the game's main tactical system.
- **"Physics in games is about being realistic."** Early designers changed gravity for fun (Moon and Jupiter settings) and added a star because flight was dull. Physics is a set of dials.

## Check yourself

1. Using the table in section 1, write a definition of "video game" under which OXO is the first. Then name one reasonable criterion that excludes it.
2. A PDP-1 cost $120,000. Suppose a university shared one among 20 research groups and each group allowed its staff one hour of Spacewar! per week, 50 weeks a year, for five years. What is the hardware cost per hour of play, if you (unfairly) charged the whole machine to play?
3. A student writes a Spacewar! clone. Orbits look fine at 60 frames per second but ships spiral away at 20. What two things should they check first?
4. Rewrite a basketball free throw in the form of this section's model. What is `accel`, and what sets the initial velocity?

<details>
<summary>Answers</summary>

1. "A game played on an electronic digital computer that shows its state on a screen." OXO qualifies in 1952. Requiring the picture to move in real time excludes it, since OXO redraws a static board after each move.
2. `20 groups × 1 h × 50 weeks × 5 years = 5,000` hours. `$120,000 / 5,000 = $24` per hour of play for one pair of players. The charge is unfair because the machine did other work, but it shows the scale. Next week, Pong earned a few dollars an hour.
3. Update order (explicit Euler spirals out) and whether `dt` is tied to frame rate (a larger step makes any drift worse). A fixed step with velocity updated first fixes both.
4. `accel = (0, −g)`, the tennis ball. The player's release angle and force set the initial velocity.

</details>

## Lab / assignment hook

[Lab 02, rebuild the loop](../labs/lab02.md). You will implement the update loop in a spreadsheet (or code, if you prefer), reproduce the tennis and orbit tables, add Tennis for Two's Moon and Jupiter settings, and write a 400-word note on what one early designer's choice of `accel` did to play. It feeds the timeline project, where each entry must name a technical cause.

## Sources

- Brookhaven National Laboratory, "The First Video Game?" (bnl.gov history page, accessed September 2026). Visitors' day on 18 October 1958; Higinbotham and Dvorak; about three weeks to build; five-inch oscilloscope; knob and button controls; amplifiers used for motion and for detecting ground and net; 1959 larger screen with Moon and Jupiter gravity.
- Wikipedia, "Tennis for Two" (accessed September 2026). Donner Model 30 analog computer; its manual's trajectory examples; later dismantling; rediscovery through Higinbotham's testimony in patent litigation involving Magnavox.
- Wikipedia, "Spacewar!" (accessed September 2026). 1962, PDP-1 at MIT; installed at MIT in September 1961; Russell's timeline (moving dot by end of January 1962, about 200 hours of work); Russell, Graetz, Wiitanen and others; Edwards's gravity star; Samson's Expensive Planetarium; Kotok and Saunders's controllers; PDP-1 price $120,000 and 53 units sold; spread to Stanford and BBN; DEC demonstrations; the *Rolling Stone* Spacewar! Olympics at the Stanford AI Lab on 19 October 1972; influence on Computer Space and Galaxy Game.
- Landsteiner, N. "Inside Spacewar!, Part 6: Gravity" (masswerk.at, accessed September 2026). Line-by-line reading of the PDP-1 source: gravity components `−x/d³` and `−y/d³` added to velocity each frame, position advanced by a fraction of velocity, no ship-to-ship gravity; Russell's remark on why Edwards added gravity.
- Graetz, J. M. (1981). "The Origin of Spacewar." *Creative Computing* 7(8), August 1981, pp. 56-67. First-hand account.
- Wikipedia, "Lunar Lander (video game genre)" (accessed September 2026). Storer's 1969 FOCAL game for the PDP-8; Atari's August 1979 vector arcade game with extra fuel bought by coin.
- Wikipedia, "Asteroids (video game)" (accessed September 2026). Atari, November 1979; the ship keeps momentum and slowly comes to a stop without thrust.
- Wikipedia, "Galaxy Game" and "Computer Space" (accessed September 2026). Galaxy Game kept Spacewar!'s gravity star; Computer Space had no gravity well.
- Wikipedia, "Cathode-ray tube amusement device" (accessed September 2026). Goldsmith and Mann; filed 25 January 1947, issued 14 December 1948; analog circuitry; never manufactured.
- Wikipedia, "Bertie the Brain" (accessed September 2026). Canadian National Exhibition, 1950; Josef Kates; light-bulb display; built to show the additron tube.
- Wikipedia, "Nimrod (computer)" (accessed September 2026). Ferranti, Festival of Britain 1951; Nim on light panels; built to demonstrate computing; the guidebook's argument for game-playing machines.
- Wikipedia, "OXO (video game)" (accessed September 2026). A. S. Douglas, 1952, EDSAC at Cambridge; 35 × 16 dot CRT; rotary telephone dial input; part of a thesis on human-computer interaction.
- Donovan, T. (2010). *Replay: The History of Video Games*. Yellow Ant, East Sussex (xiv + 501 pp.).

## Interactive spec: examples/w02-one-update-loop.html

**Purpose.** Show that one update loop drives both Tennis for Two's ball and Spacewar!'s ship, and that step size and update order are design-relevant choices.

**The one insight the visual must make obvious.** Flipping update order barely changes the tennis arc but decides whether the orbit holds or spirals away. The same loop, the same slider, two different consequences.

**Layout.** Two panels side by side on desktop, stacked on mobile, sharing one control bar.
- Left, "Court (uniform gravity)": ground line, a short net at `x = 3`, the exact parabola as a thin line, and the stepped trajectory as dots joined by line segments. Ball launched from `(0, 0)` with `vx = 4`, `vy = 6`. Stop when `y < 0` (no bounce in the default view; see the bounce toggle).
- Right, "Star (central gravity)": a dot at the origin for the star, the exact circle `r = 1` as a thin line, and the stepped path. Ship starts at `(1, 0)` with velocity `(0, 1)`. Run for a chosen number of laps.
- Numbers panel under each: for the court, the highest point (stepped and exact) and landing `x`. For the star, the distance after 1, 2 and 3 steps and after each full lap, plus the energy `E = ½(vx² + vy²) − G/d` (exact value −0.5).

**Controls.**
- Step size `dt`: slider 0.01 to 0.30, step 0.01, default 0.10.
- Update order: toggle "velocity first (semi-implicit)" / "position first (explicit)". Default velocity first. Optional third option "show both" draws both paths in two token colours.
- Gravity preset for the court: "Earth `g = 9.8`", "Moon `g = 1.63`", "Jupiter `g = 24.8`", and a free slider 0.5 to 30. These are play settings in the spirit of the 1959 version; label them as illustrative and do not claim they are the values Tennis for Two used.
- Star strength `G`: slider 0.5 to 2, default 1. When `G ≠ 1`, the exact circle is no longer the true path; grey it out and say so.
- Laps: 1, 3 or 10 (default 1). Run with `N = round(laps × 2π / dt)` steps.
- Optional bounce toggle for the court: on ground contact, `vy = −e × vy` with restitution `e` slider 0 to 1 (default 0.7), up to 5 bounces.
- Play/pause button that animates the step dots; with reduced motion, draw the full path immediately.

**Formulas.**
- Court: `accel = (0, −g)`.
- Star: `d = √(x² + y²)`, `accel = (−G x / d³, −G y / d³)`. If `d < 0.05`, stop and show "captured by the star".
- Semi-implicit: `v += a dt; p += v dt`. Explicit: `p += v dt; v += a dt` (with `a` computed at the old position).
- Exact court path: `y(t) = vy0 t − ½ g t²`, `x(t) = vx0 t`; apex `vy0² / (2g)`.

**Test values.**
- Court, `g = 9.8`, `dt = 0.1`: semi-implicit heights 0.502, 0.906, 1.212, 1.420, 1.530, 1.542 (apex) at steps 1 to 6; explicit 0.600, 1.102, 1.506, 1.812, 2.020, 2.130, 2.142 (apex at step 7). Exact apex 1.837.
- Star, `G = 1`, `dt = 0.1`, 63 steps: semi-implicit distances 0.995, 0.990, 0.985 for steps 1 to 3 and 1.001 after the lap, energy −0.500. Explicit 1.005, 1.010, 1.015 and 2.090 after the lap, energy about −0.274.
- Star, `dt = 0.05`, 126 steps: semi-implicit 1.000; explicit 1.579.

**Style.** Shared tokens. Draw the ship as a small generic triangle. No Spacewar! ship shapes or screenshots. First screen shows both panels with "show both" orders on, so the spiral is visible before any input.
