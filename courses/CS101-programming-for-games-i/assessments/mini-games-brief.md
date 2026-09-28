# CS101 · Mini-games brief

**Weight:** 30% of the course grade, 15% for each mini-game.
**Work mode:** pairs. Each pair hands in one project. The viva is individual, and each partner answers about the whole project, not only the part they wrote.
**Engine:** Godot 4 (standard build), GDScript.

## Why two small games

A lab proves one idea in isolation. A mini-game proves you can make several ideas work together in a running engine, under a player's hands, on a machine that is not yours. Mini-game 1 is about the frame: input, movement and time. Mini-game 2 is about the rules around the frame: collision and the game's flow from menu to game over. Both are small on purpose. A finished game with four good parts beats an ambitious one where nothing is tuned.

Each spec below lists **must** items (needed to pass the core rubric row) and **may** items (ideas for extra polish that earn marks on the feel row, never required).

## Mini-game 1: Ledge Run

**Weeks 7 to 9. Builds on:** [Lab 03](../labs/lab03.md) (the read, change, check turn), [Lab 07](../labs/lab07.md) (scene tree and update order), [Lab 08](../labs/lab08.md) (the jump model) and [Lab 09](../labs/lab09.md) (frame-rate independence).

A one-screen platformer. The player runs and jumps across gaps to reach an exit before a timer runs out.

### Spec

The player must:

- Be a `CharacterBody2D` that moves with `move_and_slide()` in `_physics_process`.
- Accelerate with `move_toward` toward a top speed, with a lower acceleration in the air ([week 8 lecture](../lectures/w08-input-handling-and-movement.md), section 4). All movement constants are `@export` or `const` values with names, not numbers inside expressions.
- Jump on `just_pressed`, never on `held`, using the two-timer model with a coyote window `C` and a buffer window `B` stored in **seconds**. Both timers count with `delta`.
- Read input through Input Map actions (`move_left`, `move_right`, `jump`), not raw keys.

The level must:

- Have at least three gaps that need a jump, and at least one gap that is only possible with the coyote window you chose (so a strict jump fails it and yours passes). Mark it in the level with a sign.
- Have at least five coins the player collects with an `Area2D`, and a HUD showing coins and time left.
- End in a win when the player reaches the exit, and in a loss when the player falls below the screen or the timer, counted down in seconds, reaches 0. Check the outcome once per physics tick, after movement, in the read, change, check order from lab 03. Write down what happens if the player touches the exit on the tick the timer reaches 0, and make the code do that.
- Restart on a key press after a win or a loss.

The game must play the same at 30 and 144 frames per second. Tutors will set *Project Settings → Application → Run → Max FPS* to 30 and then to 144 (vsync off) and play it. Crossing speed, jump height, the coyote window and the timer must not change in a way a player can see.

You may add variable jump height on `just_released`, a double jump (decide what a coyote jump spends), moving platforms, or a best-time record.

### Deliverables

1. The Godot project folder, zipped, that opens and runs in Godot 4 with no errors in the Debugger panel.
2. A `README.md` of at most 500 words with:
   - A tuning table: top speed, ground and air acceleration, gravity, jump velocity, `C` and `B`, each with one sentence on why you chose it.
   - A frame-rate table measured at 30, 60 and 144 fps: time to run a marked 600 px stretch from standing, jump apex height in px (print the smallest `y` reached), and the distance past the ledge of the latest coyote jump that works. Put the prediction from the week 8 and 9 models next to each measured value.
   - Your answer to the exit-on-the-last-tick question.
3. A 60-second screen recording: one clean run to the exit, one death by falling and one by timeout, and the coyote gap taken as late as you can.
4. The viva (below).

### Milestones

| When | Checkpoint | Graded? |
|---|---|---|
| End of week 7 lab | Scene tree with player, floor and one ledge; player moves left and right | No, tutor sign-off |
| End of week 8 lab | Two-timer jump in seconds; coins and HUD | No, tutor sign-off |
| Week 9 lab | Lab 09 step 8, the audit of every `+=`, `-=` and `*=` in your project | Part of lab 09 |
| Sunday of week 9, 23:59 | Submission | Yes |
| Week 10 lab | 5-minute viva per student | Yes |

## Mini-game 2: Arena

**Weeks 10 to 12. Builds on:** [Lab 10](../labs/lab10.md) (collision toolkit), [Lab 11](../labs/lab11.md) (the game-flow machine) and [Lab 12](../labs/lab12.md) (debugging).

A top-down arena. The player collects coins and dodges hazards and bullets for as long as three lives last.

### Spec

The player must:

- Move in eight directions with `Input.get_vector`, so diagonals are not faster, in `_physics_process`.
- Stay inside the arena and out of at least four inner walls, either with `move_and_slide()` or with your own `push_out` from lab 10.
- Have three lives and 1 second of invulnerability after each hit, timed in seconds.

Collision must:

- Use **your own** overlap tests, ported from lab 10 to GDScript, for at least two kinds of pair. One is circle against circle (coins against the player) with squared distances and no `sqrt`. The other is box against box or circle against box (hazards against the player) with the strict rule.
- Include at least one kind of bullet fired toward the player at a fixed speed in px/s. State the tunneling condition `v / f > t + s` for your fastest bullet and your thinnest wall at your physics tick rate, and show that your walls pass it (or that you substep).
- Draw every collider as an outline when a debug key (F1) is on, so the tutor can check hitboxes against sprites.

The game flow must:

- Be one state variable, `enum State { MENU, PLAY, PAUSE, GAME_OVER }`, changed only through a `change_state()` function, as in the [week 11 lecture](../lectures/w11-game-state-machines.md), section 3.
- Pause with the pause action through `_unhandled_input`, using `get_tree().paused` and process modes (the game node Always, the pause menu When Paused).
- Reset score and lives on the `start` and `retry` transitions only. Pausing and resuming must never change the score or lives.
- Ignore all input on the game-over screen for 1 second, and keep the best score for the session on the menu.

You may add a `GET_READY` countdown state, more hazard types, a pickup that changes the rules for a few seconds (and pauses or not, your choice), or a wave counter.

### Deliverables

1. The Godot project folder, zipped, running with no errors.
2. A `README.md` of at most 600 words with:
   - A state diagram (a photo of paper is fine) and the transition table, with the number of ignored state and event pairs.
   - A collision table with one row per pair of object kinds that can touch: shapes, which test (yours or Godot's), and the response.
   - The tunneling calculation with your real numbers.
   - One bug you found with the week 12 loop: the reproduction, what you observed, your one-sentence hypothesis and the fix.
3. A 60-second screen recording showing start, collecting, a hit with invulnerability, pause and resume (score unchanged), game over, the 1-second input lock, and retry. Show the F1 debug view for a few seconds.
4. The viva (below).

### Milestones

| When | Checkpoint | Graded? |
|---|---|---|
| End of week 10 lab | Arena, walls and player; coins picked up with your circle test | No, tutor sign-off |
| End of week 11 lab | Lab 11 step 6 done in this project: the four-state machine with pause | Part of lab 11 |
| Sunday of week 12, 23:59 | Submission | Yes |
| Week 13 lab | 5-minute viva per student | Yes |

## The viva

Five minutes per student, with the project open on a lab machine. The tutor asks two questions.

1. **A model question.** The tutor takes an **apply** question from the [exam bank](exam-bank.md) for the weeks the mini-game covers and swaps in your game's values. For mini-game 1 that means weeks 7 to 9 (for example question 33 with your `C` and run speed). For mini-game 2 it means weeks 10 and 11 (for example question 46 with your bullet and wall).
2. **A code question.** The tutor points at a line and asks what breaks if it changes. For example, "What happens if this `delta` is removed?" or "Move this reset into `on_enter`. What does the player see?"

A strong answer puts your numbers into the lecture's model and points at the line of code that implements it. You may look at your code and the lecture notes.

## Rubric (each mini-game, out of 100)

The two mini-games use the same rows. The "frame and flow" row reads as frame-rate independence for mini-game 1 and as the state machine for mini-game 2.

| Criterion | Excellent | Good | Weak | Missing |
|---|---|---|---|---|
| **Core spec** (25) | 22 to 25: every "must" item works in the build, no errors in the Debugger panel | 15 to 21: one "must" item missing or broken | 6 to 14: several missing, but the game can be played start to end | 0 to 5: does not run, or cannot be finished |
| **Frame and flow** (20) | 18 to 20: MG1 plays the same at 30 and 144 fps in the tutor's test; MG2 has one state variable, correct pause process modes, resets only on start and retry, working input lock | 12 to 17: one visible difference between frame rates (MG1) or one flow bug such as a pause key that stops working (MG2) | 5 to 11: several frame-rate bugs, or flags instead of a state variable | 0 to 4: not addressed |
| **Model use** (15) | 13 to 15: MG1 timers in seconds and `move_toward` tuned with the lecture model; MG2 your own squared-distance and strict box tests, tunneling condition met | 8 to 12: models used with one slip (a window in frames, a `sqrt` in the circle test) | 3 to 7: engine defaults only, no evidence of the week's model | 0 to 2: missing |
| **Code structure** (10) | 9 to 10: named constants, one job per function, rules separate from input and drawing | 6 to 8: some magic numbers or long functions | 3 to 5: most logic in one long `_physics_process` | 0 to 2: hard to follow |
| **README evidence** (10) | 9 to 10: every table present with measured numbers beside predictions, gaps explained | 6 to 8: tables present, predictions or explanations thin | 3 to 5: some tables missing | 0 to 2: no README |
| **Feel and tuning** (5) | 5: controls feel deliberate, tuning table reasons match what the tutor feels in play | 3 to 4: works but one value feels off (for example floaty air control) | 1 to 2: untuned defaults | 0: not playable |
| **Viva** (15, individual) | 13 to 15: both answers correct, with your numbers and the right line of code | 8 to 12: one answer correct, the other partly | 3 to 7: can describe the code but not apply the model | 0 to 2: cannot explain the project |

The first six rows (85 points) are a pair mark. The viva (15 points) is individual.

## Late work and help

Submissions up to 48 hours late lose 10 points. After 48 hours the mini-game is marked out of 50. A pair that splits up during a mini-game tells the tutor at the next lab, and each partner hands in the version they have with a note saying who built what.

Bring problems to the lab early. The checkpoint sign-offs exist so that a jump that fails at 144 fps shows up in week 8, not the night before the deadline.
