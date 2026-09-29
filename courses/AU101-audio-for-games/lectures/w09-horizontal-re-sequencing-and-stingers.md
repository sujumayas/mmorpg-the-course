# AU101 · Week 09 — Horizontal Re-sequencing and Stingers

**Why this matters:** Layering (last week) can make music thicker or thinner, but it cannot make music go somewhere: into a boss's second phase, out to a victory fanfare, back to exploring. For that, the music has to switch to a different section, and a switch that lands in the middle of a beat sounds like a mistake. This week gives you the rule for when a switch may happen, the arithmetic of how long the player waits for it, and the trick that hides the wait.

**You will be able to:**
- Compute the next sync point and the wait for a transition request at any tempo, time signature and sync unit.
- Derive the average and worst-case wait for a sync unit, and use them to choose a unit for each transition in a game.
- Design a transition matrix for a set of music states and predict what a quantized music director does with a burst of game events.
- Design stingers that acknowledge an event on the next beat and fit the harmony underneath.

**Before class:** Collins, *Game Sound* (2008), chapter 8, "Compositional approaches to dynamic game music." Read the abstract and claims 1 to 3 of US patent 5,315,057 (LucasArts, 1994) on Google Patents; skim, do not study the legal language.

**Prerequisites from earlier courses:** [AU101 week 8, vertical layering](w08-adaptive-music-vertical-layering.md) (stems, intensity, smoothing, the equal-power crossfade). [CS101 week 11, game state machines](../../CS101-programming-for-games-i/lectures/w11-game-state-machines.md) (states, transitions and why a transition table beats nested ifs). [MA102 week 11, Monte Carlo simulation](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w11-monte-carlo-simulation.md) (checking a formula by simulating many random cases). [AU101 week 6, middleware events and parameters](w06-middleware-events-and-parameters.md) (events and parameters).

**Interactive:** [examples/w09-sync-points.html](../examples/w09-sync-points.html). Keep it open during section 2.

---

## 1. Music as a set of sections and rules

Horizontal re-sequencing treats a score as a set of **segments** (short pieces of music, often 4 to 16 bars, many of them loops) plus rules for moving between them. Four terms carry the rest of the lecture.

- A **music state** is what the game wants to hear: explore, tension, combat, boss, victory. Each state owns one or more segments.
- A **transition request** is the game saying "switch to state S now." It can arrive at any time.
- A **sync point** is a moment where a switch is allowed: the next beat, the next bar, the next phrase (a group of bars, often 4 or 8), the end of the current segment, or a point the composer marked by hand. The **sync unit** is the spacing between sync points.
- A **stinger** is a short musical phrase (one to four seconds) played on top of whatever is playing, to mark an event without changing state. Think of a brass stab when a rare item drops.

Two optional tools make switches smoother. A **transition segment** (or bridge) is a short piece written to lead from one state's music into another's, such as a drum fill into the combat loop. A **destination** says where the new segment starts: at its beginning, or at the matching bar position when both segments are arrangements of the same piece.

Last week's rule was "nothing starts or stops; only volumes move." This week's rule is the opposite: **things start and stop, but only on sync points.**

## 2. Worked example: how long does the fight music wait?

### The hook

In Monkey Island 2: LeChuck's Revenge (LucasArts, 1991), the first game to use the iMUSE system, the town of Woodtick has a theme. Walk into a building and the music turns into a variation of that theme with different instruments. Walk out and a short closing flourish leads back into the basic town theme. Nothing cuts off in the middle of a phrase. The composers, Michael Land and Peter McConnell, patented the method: sequences of music carry **decision points**, marked places where a branch in the performance may happen, and the sound driver decides at each one whether to branch based on what the game has done.

Compare Super Mario Bros. (NES, 1985). When the timer reaches 100, the level music stops, the "hurry up" jingle plays, and the music comes back faster. It is clear, but it is an interruption, not a transition.

So a well-behaved transition waits for a decision point. The question every designer then faces: how long is the player willing to wait between "the enemy saw me" and "the combat music starts"?

### The model

Let the music start at time 0 with tempo `BPM` and `b` beats per bar. A sync unit spans `k` beats (1 for a beat, `b` for a bar, `4b` for a four-bar phrase), so its length is

```
U = k · 60 / BPM          seconds
```

A request at time `t` is served at the next sync point at or after `t`:

```
next_sync(t) = ceil(t / U) · U
wait(t)      = next_sync(t) − t
```

- `t` is the request time in seconds since the music started.
- `U` is the length of the sync unit in seconds.
- `ceil` rounds up to the next whole number, so a request that lands exactly on a sync point is served at once.

Requests come from gameplay, which pays no attention to the beat. If request times are spread evenly across the bar, the wait is spread evenly between 0 and `U`. That gives three numbers you can use in a design review:

```
average wait     = U / 2
worst-case wait  = U     (just after a sync point passes)
P(wait > s)      = 1 − s / U      for 0 ≤ s ≤ U
```

### Numbers you can check

At 120 BPM in 4/4 (FMOD Studio's default tempo when an event has no tempo marker):

| Sync unit | U | Average wait | Worst wait | Share of requests waiting over 1 s |
|---|---|---|---|---|
| Beat | 0.5 s | 0.25 s | 0.5 s | 0% |
| Bar | 2.0 s | 1.0 s | 2.0 s | 50% |
| 4-bar phrase | 8.0 s | 4.0 s | 8.0 s | 87.5% |

Other tempos scale the column. At 90 BPM a bar of 4/4 is `4 × 60/90 = 2.67 s`, so the average wait is 1.33 s. At 150 BPM a bar is 1.6 s and the average is 0.8 s. Fast music is more responsive at the same sync unit.

The "uniformly random" assumption is worth checking rather than trusting. This simulation draws 100,000 request times over 64 seconds of music and measures the waits. It runs as shown with `.venv/bin/python`.

```python
import math
import random

def next_sync(t, unit):
    return math.ceil(t / unit - 1e-9) * unit

rng = random.Random(9)
requests = [rng.uniform(0, 64) for _ in range(100_000)]

for name, unit in [("beat", 0.5), ("bar", 2.0), ("4 bars", 8.0)]:
    waits = [next_sync(t, unit) - t for t in requests]
    mean = sum(waits) / len(waits)
    late = sum(w > 1.0 for w in waits) / len(waits)
    print(f"{name:<7} mean wait {mean:.3f} s   worst {max(waits):.3f} s   over 1 s: {late:.1%}")
```

It prints:

```
beat    mean wait 0.251 s   worst 0.500 s   over 1 s: 0.0%
bar     mean wait 1.001 s   worst 2.000 s   over 1 s: 50.1%
4 bars  mean wait 3.999 s   worst 8.000 s   over 1 s: 87.5%
```

The small `1e-9` stops floating-point noise from pushing a request that sits exactly on a sync point to the next one. Lab 9's tests check this case.

Check one row by hand. For a 4-bar phrase, a wait over 1 s happens unless the request arrives in the last second of the 8-second phrase, so the share is `1 − 1/8 = 87.5%`.

### The visual

Open the interactive. The top view is a timeline of bars scrolling under a playhead, with sync points drawn for the chosen unit. Press "enemy spotted" (or the space bar) at any moment. An arrow runs from your press to the next sync point, and at that moment the calm loop hands over to the combat loop. Switch the unit between beat, bar and phrase and press again.

The bottom view is a histogram of every wait so far. After a dozen presses at the phrase unit, the bars fill in evenly from 0 to 8 s. That flat shape is the model, and the average line settles near 4 s. The top view makes one wait look like bad luck. The bottom view shows it is the rule. Now turn on "stinger on spotted" and press again. A short brass stab plays on the next beat, and the combat music still arrives at the phrase boundary. The wait is the same, but it no longer feels like a wait.

### Cross-game recognition

**iMUSE (LucasArts, from Monkey Island 2, 1991).** The patent's decision points are sync points placed by the composer, not by a grid. That lets the music branch only at phrase ends that make musical sense, at the cost of a wait set by where the composer put the points. The model still applies, with `U` replaced by the gap between decision points.

**FMOD Studio (2.03).** Transitions are logic markers on the timeline. A transition region makes playback jump to a destination marker or loop region, and quantization makes it trigger only on certain beats or bars. The beats and bars come from the event's tempo markers, with 120 BPM and 4/4 assumed when there are none. A transition timeline holds a bridge that plays during the jump. The same quantization can be applied to an instrument, which is one way to build a stinger.

**Super Mario World (SNES, 1990).** When the timer reaches 99, a ten-note hurry-up jingle plays while the background music keeps going, and the music switches straight to its sped-up version. The jingle is a stinger, laid over the music, and the switch uses the "immediate" unit (`U = 0`). It works because the destination is the same piece at a new tempo. Super Mario Bros. (1985) instead pauses the music while the jingle plays. That is a transition segment rather than a stinger.

**Mario Kart series (many entries).** The Mario Wiki notes that the same "Timer Warning" jingle family plays when a player starts the final lap. It marks the event musically at the moment it happens.

Every one of these answers the same two questions: where are the sync points, and what fills the gap while the player waits?

### Eyes-open design judgment

- **Choose the unit per transition, not per game.** Into combat, the player needs confirmation fast, so use a beat or a bar. Out of combat, a phrase is fine and even helpful. A long wait on the way out means a fight that briefly pauses does not drop the combat music. Victory is usually a beat, because a fanfare that lands two seconds after the boss dies feels disconnected.
- **Fill the wait with a stinger.** A stinger quantized to the next beat has an average delay of 0.25 s at 120 BPM. It tells the player "the game noticed" while the real transition waits for a musical boundary. This is the most useful trick in the lecture.
- **Let later requests replace earlier ones.** If the game asks for combat and then asks for explore before the combat switch has happened, the right answer is usually to cancel both and keep playing. Section 4 shows how a director does this.
- **Hand-placed sync points beat a grid when the music has phrases.** A grid at every bar can land a switch in the middle of a melodic phrase. Composer-marked exit points (iMUSE's decision points) are musical, but the wait becomes less predictable. Measure the longest gap between marked points and treat it as your worst case.
- **Test with the worst case, not the average.** Players remember the time the music took eight seconds to notice a boss. If `U` is long, make sure something else (a stinger, a sound effect, a camera move) answers the event at once.

### Check yourself on the waits

1. A combat track is in 3/4 at 144 BPM. What are the average and worst-case waits for a bar-quantized transition?
2. Your design rule says at least 90% of "enemy spotted" requests must be answered musically within 0.5 s. Which sync units meet it at 120 BPM in 4/4?
3. A composer marks exit points in an 8-bar explore loop at 120 BPM (4/4) at the ends of bars 2, 3 and 8. Assuming uniform requests, what is the average wait?

<details>
<summary>Answers</summary>

1. A bar is 3 beats, so `U = 3 × 60/144 = 1.25 s`. Average 0.625 s, worst 1.25 s.
2. `P(wait ≤ 0.5) = 0.5 / U` must be at least 0.9, so `U ≤ 0.556 s`. The beat (0.5 s) passes. The bar (2 s) gives only 25%. Only the beat unit meets the rule, or a stinger on the beat.
3. Bars are 2 s long, so the points are at 4, 6 and 16 s, and the loop repeats every 16 s. The gaps are 4 s (0 to 4), 2 s (4 to 6) and 10 s (6 to 16). A request in a gap of length `g` waits `g/2` on average, and the chance of landing in that gap is `g/16`. The average is `(4² + 2² + 10²) / (2 × 16) = 120/32 = 3.75 s`. Uneven gaps cost you: the long gap dominates.

</details>

## 3. Stingers that fit

A stinger plays on top of the current music, so it must agree with it in two ways.

**Time.** Quantize the stinger to the next beat (or the next eighth note for very short stabs). The stinger's own first note should fall on the beat, so any lead-in (a pickup note before the beat) has to start early. If your engine only starts sounds on sync points, author the stinger with its downbeat at time 0 and no pickup.

**Harmony.** A pitched stinger played over the wrong chord clashes. Take last week's progression, one chord per bar: A minor (A, C, E), F major (F, A, C), G major (G, B, D), E major (E, G sharp, B). No single note belongs to all four chords. A stinger built on A fits bars 1 and 2 and clashes with bar 4. You have three options:

- Write the stinger unpitched or nearly so (percussion, a noise swell, a very short stab where the clash is too brief to hear).
- Write one variant per chord and let the director pick the variant for the bar the stinger will land in. That is four small files.
- Write it on notes the progression uses most, and accept a brief clash in some bars. Check which bars by ear.

**Level and frequency.** A stinger is information, so it should sit on top of the music. But a stinger that fires every few seconds turns into noise, and players stop hearing it. Give each stinger a cooldown (for example, no more than one per bar), and reserve pitched stingers for events that are rare enough to deserve them.

## 4. The transition matrix and the director

Once there are more than two states, write the rules as a **transition matrix**: a table with one row per current state and one column per target state. Each cell says how to switch: the sync unit, an optional bridge segment, and where the destination starts. Empty cells fall back to a default.

| From \ To | explore | combat | boss | victory |
|---|---|---|---|---|
| explore | — | bar | beat | bar (default) |
| combat | phrase | — | bar | beat |
| boss | bar (default) | bar (default) | — | beat |
| victory | phrase | bar (default) | bar (default) | — |

This is CS101 week 11's state machine with a clock added. The code that runs it is a **music director**. It holds the current state and at most one pending switch, and follows three rules:

1. A request for a new state sets the pending switch to the next sync point for that transition.
2. A newer request replaces the pending one.
3. A request for the state already playing cancels the pending switch.

Here is lab 9's director running a short fight at 120 BPM with the matrix above. The game sends:

```
 3.3  state combat       (enemy spots the player)
 3.3  stinger spotted
 9.1  stinger crit
12.2  state explore      (enemy loses track of the player)
13.0  state combat       (and finds them again)
20.6  state victory
21.0  state explore
```

The director logs:

```
   3.50  stinger  spotted
   4.00  switch  explore  combat
   9.50  stinger  crit
  21.00  switch  combat  victory
  24.00  switch  victory  explore
```

The spotted stinger lands on the next beat (3.5 s), 0.2 s after the event. The combat switch waits for the bar at 4.0 s. At 12.2 s the game asks for explore. That transition uses the phrase unit, so the switch is set for 16.0 s. At 13.0 s the game asks for combat again, which is the state already playing, so the pending switch is cancelled. The player never hears the music drop out and come back. The phrase unit and the cancel rule together do what last week's slow release did for layers. Victory lands on the beat at 21.0 s. The return to explore waits for the phrase boundary at 24.0 s, giving the fanfare three seconds to play.

## 5. Mixing horizontal and vertical

Real scores combine the two techniques. A common structure:

- **Horizontal between states.** Explore, combat, boss and victory are different segments with different tempos or keys if the composer wants. The director switches between them on sync points.
- **Vertical within a state.** The combat segment has stems, and an intensity parameter (week 8) fades them in and out with no waiting.
- **Stingers on top.** Events that deserve a musical answer but not a state change get a quantized stinger.

The rule of thumb: vertical for "how much," horizontal for "what," stingers for "that just happened." When you design a score, go through your game's events and put each one into one of these three boxes before the composer writes a note.

## In-class activity (25 minutes)

Work in groups of three. You are scoring a raid boss encounter in an MMO dungeon ([week 12](w12-audio-for-mmos-many-players-one-mix.md) returns to the MMO problems). The states are: explore (the dungeon), pull (the boss is engaged), phase 2 (below 50% health), enrage (a timer ran out), victory and wipe (the whole party died).

1. Draw the transition matrix. For every cell that can happen, write a sync unit and whether it needs a bridge. Mark cells that cannot happen.
2. The music is 128 BPM in 4/4. Compute the average and worst wait for each unit you used.
3. Choose two stingers and write when they fire, their quantization and their cooldown.
4. Write the director's log for this sequence: pull at 10.0 s, phase 2 at 41.3 s, a player dies at 55.0 s (stinger?), enrage at 70.2 s, wipe at 75.9 s.
5. Swap with another group and find one transition where their worst-case wait is longer than the event it answers deserves.

Expected output: a 6 × 6 matrix, a wait table, two stinger rules and a five-line director log.

## Common misconceptions

- **"Quantizing to the bar adds a two-second delay."** It adds an average of one second and at most two, at 120 BPM in 4/4. The delay depends on tempo and meter: a bar of 3/4 at 144 BPM is 1.25 s.
- **"Immediate transitions are always bad."** They work when the destination fits the source at that instant: the same piece at a new tempo (Super Mario World's hurry-up), or a switch hidden under a loud sound effect or a crossfade.
- **"A stinger is a short track that replaces the music."** A stinger plays over the music. If the music pauses for it, it is a transition segment, as in Super Mario Bros.'s hurry-up jingle.
- **"The game should send a music event every frame the state is true."** The director only needs changes. Sending the current state again is harmless with the cancel rule, but sending a stream of alternating states will be absorbed only if the sync unit is long enough. Clean the events up on the game side first.

## Check yourself

1. At 100 BPM in 4/4, a transition request arrives at `t = 7.3 s`. When is it served with beat, bar and 4-bar phrase units?
2. Using the matrix in section 4, the director is in explore. Requests arrive: combat at 5.1 s, boss at 5.4 s. What does the log show?
3. A designer wants combat music to start within 0.3 s on average at 120 BPM. What is the longest sync unit that meets it? Would you choose that unit, or a stinger plus a bar? Why?
4. A pitched stinger is written on the notes E and B. Over which chords of the A minor, F, G, E progression does it fit without a clash?

<details>
<summary>Answers</summary>

1. A beat is 0.6 s, a bar 2.4 s, a phrase 9.6 s. Beat: `ceil(7.3/0.6) = 13`, so 7.8 s. Bar: `ceil(7.3/2.4) = 4`, so 9.6 s. Phrase: `ceil(7.3/9.6) = 1`, so 9.6 s. At this moment the bar and the phrase happen to agree.
2. Combat is requested at 5.1 s (bar unit), pending at 6.0 s. Boss at 5.4 s replaces it. Explore to boss uses the beat unit, so the switch is at 5.5 s. The log shows one entry: `5.50 switch explore boss`.
3. Average wait `U/2 ≤ 0.3`, so `U ≤ 0.6 s`, which at 120 BPM is the beat (0.5 s). A beat-quantized switch into a new segment can land mid-phrase and sound abrupt. A stinger on the beat (average 0.25 s) plus a bar-quantized switch answers the event almost as fast and keeps the switch on a musical boundary.
4. E is in A minor and E major; B is in G major and E major. Both notes fit only E major. Over A minor the B clashes mildly. Over F major both notes clash. Over G major the E is foreign. The stinger needs variants, or it should only fire in bar 4.

</details>

## Lab / assignment hook

[Lab 09, a quantized music director](../labs/lab09.md). You implement `next_sync`, the director's request rule and beat-quantized stingers, then design a transition matrix for the raid encounter from the in-class activity and run a scripted fight through it. Together with lab 8, this is the adaptive music assessment.

## Sources

- Land, M. Z. & McConnell, P. N., US patent 5,315,057, "Method and apparatus for dynamically composing music and sound effects using a computer entertainment system," assigned to LucasArts Entertainment Co. Filed November 25, 1991; published May 24, 1994. Abstract: musical sequences with decision points where branches in the performance may occur. https://patents.google.com/patent/US5315057A/en
- Wikipedia, "iMUSE" (accessed September 2026). Monkey Island 2: LeChuck's Revenge as the first game to use iMUSE; the Woodtick example of theme variations per building and a closing flourish on leaving.
- Super Mario Wiki, "Timer Warning" and "Time Limit" (accessed September 2026). Super Mario Bros. (1985) jingle at 100 time units with the music speeding up afterwards; Super Mario World's ten-note arrangement at 99 seconds playing while the music continues and switching straight to the sped-up version; the jingle family's use at the start of the final lap in the Mario Kart series.
- Firelight Technologies, *FMOD Studio User Manual 2.03* (2.03.14, May 2026), chapter 28 "Glossary": quantization, tempo marker (120 BPM and 4/4 by default), transition marker, transition region, transition timeline, destination marker, loop region.
- Collins, K. (2008). *Game Sound: An Introduction to the History, Theory, and Practice of Video Game Music and Sound Design*. MIT Press. Chapter 8.

## Interactive spec: examples/w09-sync-points.html

**The one insight.** A quantized transition waits, on average, half a sync unit and, at worst, a whole one, and a single press cannot show you that. The histogram of many presses can. A stinger on the next beat answers the event at once while the real switch still waits.

**Audio (Web Audio, procedural only).** One `AudioContext`, lookahead scheduler (25 ms timer, 100 ms lookahead), tempo from a slider (default 120 BPM), 4/4.
- **Calm loop (explore):** 4 bars. Soft sine pad on A minor and F major, alternating per bar; a single triangle note on beat 1 of each bar.
- **Combat loop:** 4 bars. Kick on every beat, snare (noise burst through a band-pass at 1.8 kHz) on beats 2 and 4, sawtooth bass eighth notes on A2 and F2 alternating per bar, square-wave stab on beat 1.
- **Stinger "spotted":** three quick notes A5, C6, A6 (triangle, 90 ms each, 20 ms gaps), starting exactly on its scheduled beat. A and C belong to both A minor and F major, so the stinger fits every bar of both loops (section 3's harmony rule).
- A switch stops the old loop's scheduling at the sync point and starts the new loop at its bar 0 at the same sample. Apply a 10 ms fade-out on the old loop to avoid clicks. No other crossfade.

**Model (exact).**

```
U = k * 60 / BPM, k = 1 (beat), 4 (bar), 16 (4-bar phrase), 0 (immediate)
next_sync(t) = U == 0 ? t : ceil(t / U - 1e-9) * U     (t measured from music start)
wait = next_sync(t) - t
stinger time = next_sync(t) with k = 1
```

**Controls.**
- Button "enemy spotted" (space bar). Toggles the requested state between explore and combat, so each press is a new request. A pending request that is reversed before its sync point is cancelled (and drawn as a crossed-out arrow).
- Sync unit radio: immediate, beat, bar (default), 4-bar phrase.
- Tempo slider 60 to 180 BPM, step 1.
- Toggle "stinger on spotted" (off by default).
- Button "simulate 1,000 presses": draws 1,000 uniform request times over 64 s of music (seeded PRNG, seed 9, so the result is repeatable) and adds their waits to the histogram without playing audio.
- Button "clear histogram".

**Views.**
1. **Timeline:** 8 bars visible, playhead fixed at 25% from the left, music scrolling left. Beat ticks thin, bar lines thick, sync points for the chosen unit drawn as diamonds. Each press draws an arrow from the press time to its sync point, labelled with the wait (2 decimals). Stingers drawn as a small flag on their beat. Background colour of each bar shows which loop was playing. Under `prefers-reduced-motion`, the timeline pages (jumps one screen at a time) instead of scrolling.
2. **Histogram:** x axis wait from 0 to `U` in 20 equal bins, y axis count. A vertical line at the running mean and a dashed line at `U/2`. Show the theoretical flat density as a dashed horizontal line at `n/20`.
3. **Readouts:** `U` (2 decimals), last wait, mean wait, worst wait, share of waits over 1 s (1 decimal percent), number of presses, and for the stinger the last stinger delay.

**Test values.** At 120 BPM: `U` = 0.50, 2.00, 8.00 s for beat, bar and phrase. A press at music time 3.30 s with the bar unit is served at 4.00 s (wait 0.70 s), and with the stinger on, the stinger plays at 3.50 s. At 100 BPM, a press at 7.30 s is served at 7.80 s (beat), 9.60 s (bar) and 9.60 s (phrase). After "simulate 1,000 presses" at 120 BPM with the phrase unit, the mean must be within 0.3 s of 4.00 and the share over 1 s within 3 points of 87.5%.

**Accessibility.** Keyboard: space presses, 1 to 4 choose the unit, S toggles the stinger. Visible focus on every control; readouts in an `aria-live="polite"` region. Light and dark themes from the shared tokens. If audio is blocked, the timeline and histogram still work.
