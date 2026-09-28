# CS101 · Final arcade game brief

**Weight:** 30% of the course grade.
**Work mode:** teams of two or three. The product is marked as a team. The viva is individual.
**Engine:** Godot 4 (standard build), GDScript.
**Release:** week 15, at an open play session (the release session).

## The brief

Make and release a complete small arcade game. A run starts from a title screen, gets harder in waves, ends in a game over with a score, and can be replayed at once. A new player should understand it in under 30 seconds and finish a typical run in under 10 minutes.

The genre is yours: a shooter, a dodger, a single-screen platformer, a brick breaker, a snake-like. You may start from your mini-game 2 project. If you do, the release notes must list what is new, and the rubric marks the finished game, not the parts you already handed in.

"Complete" is the whole point of this assessment. A small game with every part working, tuned and tested scores higher than a large one with loose ends. Cut scope before you cut the checklist.

## Technical checklist

Every item maps to a week of the course. The rubric checks each one.

| # | Requirement | Week and lab |
|---|---|---|
| 1 | Gameplay runs in `_physics_process` at a fixed tick rate. Nothing in the rules counts frames. Tutors test the release at 30 and 144 fps and it must play the same. | [Week 9](../lectures/w09-delta-time-and-frame-rate-independence.md), [Lab 09](../labs/lab09.md) |
| 2 | Input goes through Input Map actions. One-shot actions use `just_pressed` or an input event. Any timing-critical action (a jump, a dash, a shot on a beat) has a forgiveness window stored in seconds. | [Week 8](../lectures/w08-input-handling-and-movement.md), [Lab 08](../labs/lab08.md) |
| 3 | Every collider is a deliberate shape. Hitboxes are tuned against sprites and documented. Your fastest object passes the tunneling condition `v / f ≤ t + s` against your thinnest wall at your tick rate, or it substeps. | [Week 10](../lectures/w10-collision-basics-aabb-and-circles.md), [Lab 10](../labs/lab10.md) |
| 4 | Game flow is one state machine with at least `MENU`, `PLAY`, `PAUSE`, `GAME_OVER` and one more state of your choice (a `GET_READY` countdown, high-score entry, an options screen). Resets happen on transitions, not in enter actions that pause can reach. | [Week 11](../lectures/w11-game-state-machines.md), [Lab 11](../labs/lab11.md) |
| 5 | Waves get harder by a rule tied to the wave number. Randomness picks values inside ranges that are written down as data. | [Week 13](../lectures/w13-randomness-spawning-and-procedural-variety.md), section 5 |
| 6 | Spawning uses its own seeded `RandomNumberGenerator`, separate from any effect's generator. The run seed shows on the game-over screen, and a debug setting starts a run from a fixed seed. Positions come from a sampler with a safe radius and an attempt cap, or from a sampler that picks the allowed region directly. | [Week 13](../lectures/w13-randomness-spawning-and-procedural-variety.md), [Lab 13](../labs/lab13.md) |
| 7 | Enemy, pickup and wave definitions live in one dictionary or a JSON file keyed by readable strings, and are checked by a `validate` function at start-up. | [Week 6](../lectures/w06-dictionaries-item-databases.md), [Lab 06](../labs/lab06.md) |
| 8 | Polish follows the lecture's pass: trauma shake through the camera offset, particles sized with `alive = rate × lifetime`, sound with pitch variation, all driven by one polish table. The options menu has shake scale, particle amount and effects volume. With all three at 0 the game plays identically. | [Week 14](../lectures/w14-polish-pass-sound-particles-screen-shake.md), [Lab 14](../labs/lab14.md) |
| 9 | At least three bugs found and fixed with the week 12 loop, each with a regression test (a Python model of the rule, or a GDScript test scene) that fails on the old code and passes on the new. | [Week 12](../lectures/w12-debugging-breakpoints-logging-rubber-ducking.md), [Lab 12](../labs/lab12.md) |

## Deliverables

1. **Release build.** An exported build for Windows, macOS, Linux or the Web that runs on a lab machine with no Godot editor. Name the file with the team name and version, for example `teamname-1.0`.
2. **Source.** The Godot project folder, zipped, with no errors in the Debugger panel on start.
3. **Release notes** (`RELEASE.md`, at most 1,000 words):
   - Controls and the goal, in the words you would put on the game's store page.
   - The transition table and a state diagram.
   - A tuning table for movement and input (speeds, accelerations, forgiveness windows) with one sentence per value.
   - A collision table (object pairs, shapes, test, response) and the tunneling calculation with your numbers.
   - The wave rule and the spawn table with its weights and ranges.
   - The polish table: five frequent events and one rare event, each with trauma, particle burst and lifetime, and sound pitch range.
   - The particle budget predicted with `rate × lifetime`, next to the count you measured in the busiest wave with Godot's Monitors tab.
   - Known bugs you chose not to fix, and why.
4. **Bug journal** (`BUGS.md`, at most 600 words). Three bugs, each with the reproduction (seed, frame or steps), the evidence (a log excerpt or a debugger screenshot), a one-sentence hypothesis, the fix as a short diff, and the name of the regression test.
5. **Video.** 90 seconds of play from title screen to game over, including a pause, the rare event, and the options menu with shake set to 0.
6. **Contribution statement.** One paragraph per team member, written by that member, naming the systems they built and the files they own. The team signs it.
7. **Release session and viva** in week 15 (below).

## Milestones

| When | Milestone | What you show | Graded? |
|---|---|---|---|
| Week 11 lab | Team formed | Team name and members to the tutor | No |
| Week 12 lab | Pitch | One page: the core loop in two sentences, what a wave is, what ends a run, a first state diagram, and which of mini-game 2's code you will reuse | Feedback only |
| Week 13 lab | Vertical slice | One wave playable from menu to game over, seeded spawner running (lab 13 step 8), seed on the game-over screen | Tutor sign-off, required before the beta |
| Week 14 lab | Beta | Content complete. Polish pass done (lab 14 step 7 to 9). Three classmates from other teams play it while you watch and take notes without helping. Bring the bug list you made from their play. | Tutor sign-off |
| Week 15 | Release session | Build, notes, journal, video and contribution statement submitted by the start of the session. Game on show for the whole session. | Yes |

A team that misses the vertical slice sign-off must show it at the next lab before the beta. The sign-offs carry no points, but a project with no sign-offs gets a tutor check of the contribution statements before marking.

## Release session and viva

The release session is open play. Keep your game running on a lab machine for the session, and play at least three other teams' games. Leave each team one written observation ("I died to a spawn I could not see coming at wave 4", not "fun!").

Each team member has a 5-minute viva at your machine. The assessor asks two questions.

1. **A model question with your numbers.** The assessor picks an **apply** question from the [exam bank](exam-bank.md), usually from weeks 9, 10, 13 or 14, and replaces its values with your game's values. For example, question 59 becomes "your arena size and your safe radius", and question 63 becomes "your big hit's trauma, your decay and your exponent". You answer with the model and then show the line of code.
2. **A change question.** The assessor points at part of your game and asks what would happen if it changed. "Your sparks start using `spawn_rng`. What breaks, and how would a tester notice?" "The frame rate drops to 30. Which of your objects can now pass through a wall?"

Each member answers alone, about any part of the game, not only their own files.

## Rubric (out of 100)

| Criterion | Excellent | Good | Weak | Missing |
|---|---|---|---|---|
| **Complete, playable release** (20) | 18 to 20: the exported build runs on a lab machine; title to game over to retry works every time; no crashes or errors during the release session | 12 to 17: complete with one rough edge (a stuck state, a missing retry) | 5 to 11: playable but unfinished (no waves, no game over screen) | 0 to 4: no working build |
| **Time and input** (checklist 1 and 2) (10) | 9 to 10: identical play at 30 and 144 fps in the tutor's test; forgiveness windows in seconds and tuned | 6 to 8: one frame-rate difference a player can see, or a window in frames | 3 to 5: several frame-rate bugs | 0 to 2: not addressed |
| **Collision** (checklist 3) (10) | 9 to 10: every shape chosen and documented, hitboxes fair in play, tunneling condition met with your numbers | 6 to 8: works, one unfair hitbox or no tunneling evidence | 3 to 5: visible pass-through or snagging | 0 to 2: broken |
| **Game flow** (checklist 4) (10) | 9 to 10: one state variable, five or more states, table matches the code, pause never changes score or lives, ignored events do nothing | 6 to 8: one flow bug | 3 to 5: flags mixed with states, or several bugs | 0 to 2: no state machine |
| **Randomness and data** (checklist 5 to 7) (15) | 13 to 15: separate seeded spawn generator, seed shown and a fixed-seed replay matches, fair spawn sampler, waves harder by a written rule, data in one validated table | 8 to 12: one item missing (for example effects share the spawn generator) | 3 to 7: unseeded or unfair spawns, or data spread through the code | 0 to 2: missing |
| **Polish and accessibility** (checklist 8) (10) | 9 to 10: the rare event clearly outranks frequent ones, shake and particles frame-rate independent, all three settings work and the zero test passes, measured particle count within 20% of the budget | 6 to 8: effects present, one setting missing or budget not checked | 3 to 5: effects that shake the HUD, jitter, or change gameplay | 0 to 2: no polish pass |
| **Debugging evidence** (checklist 9) (10) | 9 to 10: three bugs with reproduction, evidence, hypothesis, minimal fix and a test that fails before and passes after | 6 to 8: three bugs, one without a test or evidence | 3 to 5: one or two bugs, or fixes without tests | 0 to 2: no journal |
| **Release notes** (5) | 5: every section present with measured numbers next to predictions | 3 to 4: one or two sections thin | 1 to 2: notes mostly missing | 0: none |
| **Viva** (10, individual) | 9 to 10: both answers correct, with your game's numbers and the right line of code | 6 to 8: one answer correct and the other partly | 3 to 5: can describe the game but not apply the models | 0 to 2: cannot explain the game |

The first eight rows (90 points) are a team mark. The viva (10 points) is individual. If the contribution statements, the commit history and the vivas show that a member built much less than the others, the course lead may lower that member's team mark after talking with the team.

## Scope advice

Two-person teams should aim for one enemy type with two variants, one hazard, one pickup and five waves that loop with a harder rule. Three-person teams can add a second enemy type or a boss wave. Anything past that is optional, and none of it earns points the checklist does not already cover. The week 14 lecture's stopping rule applies to the whole project: stop adding when the rare event clearly outranks the frequent ones and the checklist is green.
