# UX201 · Week 13 — Biometrics and Eye-Tracking Overview

**Why this matters:** Sensors that read a player's sweat, pulse and gaze look like a way to skip the unreliable part of research, which is asking people what they felt. They aren't. A skin-conductance spike tells you that something happened in the player's body. It doesn't tell you what. This week you learn what each signal can actually support, and how to avoid the most common mistake in biometric studies, which is reading an emotion off a number that only measures intensity.

**You will be able to:**
- Name the common physiological and gaze signals used in games user research, and say for each whether it indexes arousal, valence or attention, with its main weakness.
- Compute the probability that an arousal peak came from a given emotional state, using base rates and hit rates, and show how a second data channel changes it.
- Compute and interpret eye-tracking area-of-interest metrics (hit ratio, time to first fixation, dwell time), and explain why a heatmap can mislead.
- Critique a biometric study design or a biofeedback game mechanic for reverse inference, baseline, timing and consent.

**Before class:** Mike Ambinder, "Biofeedback in Gameplay: How Valve Measures Physiology to Enhance Gaming Experience" (GDC 2011), the slide deck from Valve's publications page (71 slides, about 20 minutes). Mike Ambinder, "Valve's Approach to Playtesting: The Application of Empiricism" (GDC 2009), the slides from "Technical Approaches" to the end. Celia Hodent, *The Gamer's Brain* (CRC Press, 2017), reread the chapter "Attention" (pp. 51-58). The Wikipedia articles "Electrodermal activity" and "Eye tracking" (the sections on measurement and on attention).

**Prerequisites from earlier courses:** [UX201 week 1, perception, attention and memory](w01-perception-attention-memory.md), for inattentional blindness and the difference between visible and noticed. [UX201 week 3, flow and difficulty](w03-flow-and-difficulty.md), for arousal, anxiety and boredom as channel states. [MA102 week 2, independent events](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w02-independent-events-and-the-gamblers-fallacy.md), for conditional probability `P(A | B)`, which section 2 turns around. [MA102 week 13, sampling and confidence](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w13-sampling-confidence-and-why-n5-lies.md), for the Wilson interval used in section 3. [MA102 week 14, hypothesis testing](../../MA102-mathematics-for-games-ii-probability-and-statist/lectures/w14-intro-to-hypothesis-testing-ab.md), for multiple comparisons. [GD102 week 3, positive feedback loops](../../GD102-systems-design-and-game-mechanics/lectures/w03-positive-feedback-loops-snowballing.md), which explains what goes wrong when a game feeds arousal back into difficulty. [GD101 week 7, playtesting](../../GD101-introduction-to-game-design/lectures/w07-playtesting-observe-dont-explain.md), for observation protocol.

**Interactive:** [examples/w13-arousal-peaks.html](../examples/w13-arousal-peaks.html). Use it during section 2.

---

## 1. What the body can tell you, and what it can't

**Biometrics**, in games user research, means measuring the player's body during play: sweat, heart, eyes, face, brain. The more careful name is **psychophysiology**, the study of how mental states show up in physiological signals. The appeal is that a think-aloud comment arrives late and is shaped by what the tester thinks you want to hear, while a sensor records continuously and can't be polite.

The catch is in what the signals measure. Psychologists describe an emotional state with at least two numbers. **Arousal** is how activated you are, from sleepy to keyed-up. **Valence** is whether the state feels good or bad. Fear and excitement are both high arousal. Fear has negative valence and excitement positive. Valve's Mike Ambinder used this two-axis picture in both of his GDC talks on the topic, adapted from the psychologist Peter Lang.

Here is where the common signals sit, drawn from Valve's two talks and the standard references.

| Signal | What the sensor reads | Indexes | Main weaknesses |
|---|---|---|---|
| Electrodermal activity (EDA), also called skin conductance or GSR | Sweat-driven changes in the skin's electrical conductance, usually on two fingers | Arousal | No valence; responses lag the event by 1 to 3 seconds; range differs a lot between people |
| Heart rate | Beat-to-beat interval | Arousal | Movement artifacts; slower onset; also changes with posture, breathing, caffeine |
| Pupil diameter | Pupil size from an eye tracker | Arousal and mental effort | The pupil also reacts to screen brightness, which in games changes all the time |
| Facial expression (video coding or facial EMG) | Muscle activity around brows, cheeks, mouth | Valence, some arousal | Intrusive (EMG) or needs trained coders or a black-box classifier (video) |
| EEG | Electrical activity at the scalp | Rough arousal and engagement bands | Expensive, intrusive, very noisy, hard to validate |
| Eye tracking (gaze) | Where the eyes point, as fixations and saccades | Where the eyes went, a rough proxy for attention | Gaze is not attention; expensive to analyse |

Two lines in that table decide most of this lecture. First, the cheap, robust signals (EDA and heart rate) measure **arousal only**. Valve's 2011 slides list "difficult to determine valence" as a weakness of both. Second, eye tracking measures **where the eyes pointed**, which is related to attention but is not the same thing. Section 2 deals with the first problem and section 3 with the second.

### Electrodermal activity in one paragraph

When the sympathetic nervous system activates (the "fight or flight" branch), sweat glands in the palms and fingers fill slightly, and the skin conducts electricity better. A sensor records the conductance in microsiemens (µS). The slow drift of this signal is the **tonic level**. The quick bumps on top of it are **skin conductance responses (SCRs)**, which we'll call peaks. A peak starts 1 to 3 seconds after the event that caused it. You can't control it consciously, which is why it is part of the polygraph. It rises for fear, anger, surprise, laughter and a hard puzzle solved, and the change alone doesn't say which.

## 2. Worked example: what does a sweat spike mean?

### The hook

Nevermind (Flying Mollusk, Windows and macOS, September 2015) is a psychological horror game that watches your body. With a supported sensor, such as an Intel RealSense camera that reads pulse, it estimates how stressed you are. The more stressed you are, the harder the game gets. The screen fogs and wobbles and navigation gets harder. Calm down, and the game eases off.

It's a clever loop, and it rests on one assumption. A stress signal during a horror game is taken to mean the player is afraid. But your pulse also jumps when you finally solve a puzzle, when you die for the third time in the same corridor, and when you laugh at a cheap jump scare. Which of those was fear?

Every biometric study has to answer that question before it reports anything. Researchers call the mistake **reverse inference**. You know that fear causes arousal, so you read arousal as fear. The direction of the arrow matters, and base rates decide how wrong the reversal is.

### The model

Split a play session into short windows, say 5 seconds each. In each window the player is in one true state `s`. We'll use four: neutral, fear, frustration and excitement. A peak detector flags a window if an SCR starts in it (after shifting for the 1 to 3 second lag).

- `n_s` is the number of windows in which the player is in state `s`. This is the **base rate**, as a count.
- `h_s` is the **hit rate** for state `s`, the probability that a window in state `s` contains a peak, `P(peak | s)`. For the neutral state this is the **false-alarm rate**, peaks from noise, movement or the doorbell.
- The expected number of peaks from state `s` is `n_s × h_s`.

What a designer wants is the other direction, `P(s | peak)`, the chance that a flagged window really was state `s`. It is the share of all peaks that came from `s`:

```
P(s | peak) = (n_s × h_s) / Σ (n_j × h_j)
```

The sum runs over all states `j`. This is Bayes' rule written with counts, sometimes called the natural-frequency form. You met `P(A | B)` in MA102 week 2. Here you compute it by counting peaks by where they came from, which avoids fractions of fractions.

One property of this formula carries the lesson. **If two states have the same hit rate, a peak can't change the ratio between them.** Their shares of the peaks are in the same ratio as their base rates. A signal that responds equally to fear and frustration carries no information about which one you're looking at.

### Numbers you can check

A single tester plays 25 minutes of a horror game: 300 windows of 5 seconds. A trained observer later codes each window from the face-camera video, the think-aloud audio and a short post-session interview, to give the "true" state. The counts and rates are invented for teaching.

| True state `s` | Windows `n_s` | Hit rate `h_s` | Peaks `n_s × h_s` | Share of peaks `P(s | peak)` |
|---|---|---|---|---|
| Neutral | 240 | 0.05 | 12 | 12 / 60 = 20.0% |
| Fear | 20 | 0.80 | 16 | 16 / 60 = 26.7% |
| Frustration | 25 | 0.80 | 20 | 20 / 60 = 33.3% |
| Excitement | 15 | 0.80 | 12 | 12 / 60 = 20.0% |
| Total | 300 | — | 60 | 100% |

Check a row. Frustration: `25 × 0.80 = 20` peaks, and `20 / 60 = 0.333`.

Now read it as a designer.

- **"Something happened" is a good bet.** 48 of the 60 peaks, 80%, come from one of the three aroused states. Arousal is what EDA measures, and it measures it well.
- **"The player was afraid" is a bad bet.** Only 16 of 60 peaks, 26.7%, were fear. A Nevermind-style rule that reads every peak as fear is right about one time in four. More peaks came from frustration than from fear.
- **The ratio among aroused states is the base-rate ratio.** Fear, frustration and excitement have equal hit rates, so their peaks split 20 : 25 : 15, exactly the ratio of the windows they occupied. The peak said nothing about which one.

### Adding a second channel

The fix is not a better sweat sensor. It is a second source of information that does discriminate. The cheapest one is already in your build. It is the **game's event log**. Take only the windows that start within 5 seconds of a scripted scare, 20 windows in this session. The observer's coding of those 20 is 4 neutral, 12 fear, 1 frustration and 3 excitement.

| True state (scare windows only) | `n_s` | `h_s` | Peaks | `P(s | peak, scare)` |
|---|---|---|---|---|
| Neutral | 4 | 0.05 | 0.2 | 1.5% |
| Fear | 12 | 0.80 | 9.6 | 73.8% |
| Frustration | 1 | 0.80 | 0.8 | 6.2% |
| Excitement | 3 | 0.80 | 2.4 | 18.5% |
| Total | 20 | — | 13.0 | 100% |

The sensor is the same. The formula is the same. The only change is the base rate, because the log told you what kind of moment it was. A peak right after a scripted scare is fear about three times in four. Do the same for the 20 windows right after a player death (4 neutral, 2 fear, 14 frustration, 0 excitement) and a peak there is frustration 86.2% of the time.

The general rule is short. **Physiology tells you when and how much. Context tells you what.** Context can be the event log, a facial-expression channel that reads valence, or a question you ask afterward while replaying the moment.

### A visual you can move

Open `examples/w13-arousal-peaks.html`. The left panel is what the sensor sees, a 25-minute skin-conductance trace with the 60 detected peaks marked. Every peak marker looks the same, because to the sensor they are the same. The right panel is what was happening, a grid of 300 small squares, one per window, coloured by the observer-coded state, with the peak windows outlined. Under it, a bar splits the 60 peaks by true state.

On first load the bar reads 20% neutral, 26.7% fear, 33.3% frustration and 20% excitement. Press "Colour the peaks" and the identical markers on the left take their true colours. They are a mix, and fear is a minority. Change the context filter to "after a scripted scare" and watch the bar swing to 73.8% fear. Then drag the neutral false-alarm rate from 0.05 to 0.10. Neutral becomes the largest single source of peaks (24 of 72), which is what a loose sensor or a fidgety tester does to your data.

### Cross-game recognition

**Valve, Left 4 Dead 2 (GDC 2011).** The Left 4 Dead AI Director paces zombie spawns, items and boss appearances from an *estimated* intensity for each survivor. That estimate rises when the player takes damage or sees a teammate go down, and decays over time. Valve replaced the estimate with measured skin conductance and reported that measured arousal produced more enjoyment than estimated arousal. In our terms, the Director never needed valence. Its job is to create peaks and valleys of intensity, and arousal is exactly what EDA measures. It's a design that asks the sensor only the question the sensor can answer.

**Valve, Alien Swarm mod (same talk).** Players had to kill 100 enemies in 240 seconds, and the timer ran faster when their skin conductance rose. Valve reported a positive feedback loop: arousal sped up the timer, which raised arousal, which sped it further. A decay factor helped. The same slide admits that the link between arousal and in-game events was not always clear. This is GD102 week 3's snowball, driven by the player's nervous system. Nevermind's loop has the same shape: in our table, a third of the peaks are frustration, and a game that gets harder whenever the player is frustrated is building exactly that loop.

**The polygraph.** A polygraph records skin conductance, heart rate, breathing and blood pressure, and the examiner infers deception. It is reverse inference with high stakes. In 2003 the US National Academy of Sciences reviewed the evidence and judged it "scanty and scientifically weak," and found the accuracy insufficient for employee security screening. The reason is our table. Arousal comes from anxiety, fear, confusion and many other states, and the machine cannot tell anxiety about lying from anxiety about being tested. Rewrite it in our form: "deceptive" is one state among several with similar hit rates, and in screening, where almost nobody tested is a spy, its base rate is tiny.

Three settings, one rule. Arousal signals answer "how much is happening to this person right now?" They don't answer "what is happening?" unless something else narrows the states down first.

### Eyes-open design judgment

- **Match the question to the signal.** Pacing, intensity curves and "where did the tester go flat?" are arousal questions. EDA and heart rate are good at them. "Was this scary or annoying?" is a valence question, and needs a face channel, context or a follow-up interview.
- **Base rates change between games and between moments.** In a horror game, fear is common. In a competitive shooter, frustration and excitement dominate. The same peak means different things in different games.
- **Biofeedback as a mechanic is a loop you are designing.** Before shipping "harder when stressed," ask what share of stress will be frustration, and whether you are happy to punish it. Valve's timer needed a decay term, and many designs need a cap or a cooldown.
- **A null result is informative.** A flat trace through your "big moment" is strong evidence that the moment didn't land for that tester, because in a clean recording strong arousal rarely passes without a peak.
- **Don't let the sensor replace the interview.** Valve's 2009 slides list physiological measures alongside observation and surveys, not instead of them. Use peaks to choose which moments to replay and ask about.

### Check yourself (worked example)

1. Using the full-session table, suppose the fear hit rate is 0.90 and the frustration hit rate drops to 0.60, with everything else unchanged. Compute `P(fear | peak)`. Does a peak now favour fear or frustration?
2. A calmer game has 270 neutral windows and 10 each of fear, frustration and excitement, with the same hit rates as the table. What share of peaks are neutral? What does that mean for a researcher who reports "the player had 37 emotional reactions"?
3. Explain in two sentences why the Left 4 Dead 2 experiment escapes the reverse-inference problem and Nevermind doesn't.

<details>
<summary>Answers</summary>

1. Peaks: neutral 12, fear `20 × 0.9 = 18`, frustration `25 × 0.6 = 15`, excitement 12, total 57. `P(fear | peak) = 18 / 57 = 31.6%` against 26.3% for frustration. A peak now slightly favours fear, because the hit rates differ. It is still wrong about fear more than two times in three.
2. Peaks: neutral `270 × 0.05 = 13.5`, and 8 each from the others, total 37.5. Neutral share `13.5 / 37.5 = 36%`. More than a third of those "emotional reactions" are false alarms. The fewer real reactions a game produces, the larger the false-alarm share becomes.
3. The Director only needs intensity, and EDA measures intensity, so it never infers a specific emotion. Nevermind reads stress as fear, so every frustration or excitement peak is misread as fear and punished with more difficulty.

</details>

## 3. Eye tracking: where the eyes went

An **eye tracker** shines infrared light at the eyes and films the reflections to estimate where on the screen the player is looking, many times a second. Remote trackers sit under the monitor. Wearable ones look like glasses. The raw stream is split into two kinds of event. **Fixations** are pauses where the eye stays roughly still and takes in detail. **Saccades** are the fast jumps between them, during which vision is largely suppressed. You met this in week 1: search is a sequence of fixations, one or a few items at a time.

### Areas of interest and the metrics that matter

Analysis starts by drawing **areas of interest (AOIs)** on the screen: the minimap, the health bar, a tutorial prompt, a quest marker. For each tester and each AOI you compute a few numbers.

- **Hit** (yes or no): did the tester fixate the AOI at least once while it was visible? Across testers, the **hit ratio** is the share of testers with a hit.
- **Time to first fixation (TTFF):** seconds from when the AOI appeared to the first fixation on it, for testers who hit it.
- **Dwell time:** total fixation time inside the AOI. Some tools also report fixation count.

Each metric answers a different design question. Hit ratio asks "does the element get seen at all?" TTFF asks "does it get seen soon enough?" Dwell asks "how long do eyes stay?", which is ambiguous. Long dwell on a tutorial prompt may mean careful reading or confusion, and long dwell on a health bar may mean the player is anxious about it or can't parse it.

### A small study, computed

Six testers play the first encounter of a prototype. A prompt, "Hold R to reload," appears at the bottom left for 8 seconds during the first fight. The analysis counts a fixation on the AOI when gaze stays inside it for at least 100 ms, a threshold the team chose before the study.

| Tester | Hit | TTFF (s) | Dwell (ms) | Could say what the prompt said afterward |
|---|---|---|---|---|
| P1 | yes | 0.4 | 3,200 | yes |
| P2 | no | — | 0 | no |
| P3 | no | — | 0 | no |
| P4 | yes | 5.1 | 450 | no |
| P5 | no | — | 0 | no |
| P6 | no | — | 0 | no |

- Hit ratio: 2 of 6. The Wilson 95% interval from MA102 week 13 is 9.7% to 70.0%. Even with six testers, you can say that a real share of players will never look at the prompt.
- TTFF for the two who looked: 0.4 s and 5.1 s. P4 found it with 2.9 seconds of display left, mid-fight.
- Mean dwell: `(3,200 + 450) / 6 = 608` ms per tester.
- Recall: 1 of 6 could say what the prompt told them.

Now picture the **heatmap** the tool produces. A heatmap sums dwell over all testers and colours the screen by the total. The prompt area glows, because 3,650 ms of fixation landed there. In a meeting, that reads as "players look at the prompt." One tester looked hard, one glanced, four never looked, and five of six can't tell you what it said. A heatmap is a sum, so it can't show you how many people contributed to a hot spot. Always report the hit ratio next to it.

### Looked at is not the same as seen

The **eye-mind hypothesis**, stated by Marcel Just and Patricia Carpenter in 1980 for reading, assumes there is no appreciable lag between what is fixated and what is processed. It fails often in games. P4 fixated the prompt for 450 ms and couldn't recall it, the same "looked but didn't see" failure as the week 1 gorilla study, with the eyes actually on target. The reverse happens too. **Covert attention** lets people attend to something they aren't looking at directly, such as a flashing health bar in peripheral vision. Gaze data shows where the eyes were, not where attention was.

So eye tracking inherits the reverse-inference problem from section 2. A fixation is evidence of possible attention, and it needs a second channel (recall, behaviour, a replay interview) before you can say the player took the information in.

### Gaze as input

Eye tracking is also a controller. Valve's 2011 talk showed a Portal 2 experiment where the player moved with the hands and aimed with the eyes, with the crosshair redrawn at the gaze point 60 times a second. Valve concluded that eyes are viable aiming controllers. Before Your Eyes (GoodbyeWorld Games, 2021) uses a webcam to detect blinks, and each blink moves the story forward. As input, the signal's meaning is defined by the design, so nobody has to guess what a blink meant.

## 4. Running a small biometric study without fooling yourself

Consumer wristbands, webcams and free gaze software make small studies possible without a lab. The same five rules apply at any budget.

### Take a baseline, and compare each tester with themselves

Valve's slides note that the range of skin conductance varies a lot between people. One tester's resting level can be higher than another's peak. Record 2 to 3 minutes of rest (a neutral menu or a blank screen) before play, and express each tester's signal relative to their own baseline, for example as a z-score, `z = (x − mean_baseline) / sd_baseline`. Compare moments within a tester, and compare testers only after normalizing.

### Mark events, and shift for the lag

Synchronize the sensor stream with the game's event log and the screen recording from the first second, with a clap, a flash or a logged sync event. When you look for the response to an event, search a window that starts about 1 second after it and ends 3 to 5 seconds after it for EDA. A peak at the moment of the event was caused by something earlier.

### Decide the analysis before you look

Choose your peak threshold, your windows and your AOIs before you see the data. Valve's 2011 analysis correlated several features of the conductance waveform (peak count, amplitude, range) with survey answers about excitement, frustration and challenge. The results slide shows 21 correlations (seven waveform features against three questions). Sixteen are within ±0.2, and the largest is −0.39, mean skin-conductance level against the challenge question. MA102 week 14 showed that with 20 tests at the 5% level, the chance of at least one false "discovery" is about 64%. Pre-register a few questions and treat everything else as a lead for the next study.

### Keep the confounds out of the signal

Pupil size tracks arousal and mental effort, and it also shrinks when the screen gets brighter. In a game that cuts from a dark cave to daylight, the pupil change is mostly light. Heart rate rises when a tester leans forward or laughs. List the confounds for each signal and control what you can, such as room, screen brightness and seating.

### Treat the data as sensitive, and say so in the consent form

Physiological recordings can reveal health information, and face video can identify people. The EU's GDPR, Article 9, puts data concerning health and biometric data used to identify a person into special categories that may only be processed under specific conditions, one of which is explicit consent for a stated purpose. Whatever your jurisdiction, say exactly what you record and why, let testers stop at any time without penalty, store the files under a code rather than a name, and delete raw video when the study ends unless the tester agreed otherwise.

## In-class activity (25 minutes)

Groups of three. Each group receives a printed trace: 10 minutes of one tester's skin conductance with 18 marked peaks, the game's event log for the same period (deaths, scripted scares, puzzle solves, menu opens), and a list of the tester's think-aloud remarks with timestamps.

1. **Label blind (8 min).** Using only the trace, label each peak as fear, frustration, excitement or noise. Write your labels down.
2. **Label with context (10 min).** Now use the event log and the remarks. Relabel each peak, shifting each event by 1 to 3 seconds. Count how many labels changed.
3. **Build the table (5 min).** From your context labels, fill a four-row table like the one in section 2. What would a "peak means fear" rule have got right?
4. **Report (2 min).** One sentence naming which second channel changed the most labels, the event log or the remarks.

Expected output: two label lists, the number of changed labels, a filled table and the one-sentence answer.

## Common misconceptions

- **"The body can't lie, so biometrics give the true emotion."** The body can't fake arousal easily, but arousal is not emotion. Peaks from fear, frustration, excitement and noise look the same on the trace.
- **"A better sensor would tell fear from frustration."** A more sensitive EDA sensor raises every hit rate together, and equal hit rates carry no information about which state it was. You need a signal that responds differently to the states, or context.
- **"The heatmap is hot, so players saw it."** A heatmap sums dwell across testers. One tester staring for three seconds makes a hot spot. Report the hit ratio, and check recall or behaviour.
- **"If the eyes were on it, the player read it."** Fixation is not processing. Testers fixate text they don't take in, and notice things in peripheral vision they never fixated.

## Check yourself

1. A tester's resting skin conductance is 4.0 µS with a standard deviation of 0.5 µS. During a boss intro it reaches 5.5 µS. A second tester rests at 9.0 µS (SD 1.5) and reaches 10.5 µS. Compute each tester's z-score. Which tester responded more strongly, relative to their own baseline?
2. In the scare-window table of section 2, what is `P(fear | peak, scare)` if the observer's coding is instead 4 neutral, 8 fear, 5 frustration and 3 excitement? What might have caused the frustration windows around scares?
3. Eight testers see a new minimap marker. Six fixate it, with TTFF of 0.8, 1.2, 1.5, 2.0, 9.5 and 11.0 s. The marker matters only in the first 5 seconds. What is the hit ratio, and what share of all eight testers saw it in time? Which number goes in the report headline?

<details>
<summary>Answers</summary>

1. Tester 1: `(5.5 − 4.0) / 0.5 = 3.0`. Tester 2: `(10.5 − 9.0) / 1.5 = 1.0`. Both rose by 1.5 µS, but tester 1 responded three standard deviations above baseline and tester 2 only one. Raw microsiemens would have called them equal.
2. Peaks: neutral 0.2, fear 6.4, frustration 4.0, excitement 2.4, total 13.0. `P(fear | peak, scare) = 6.4 / 13.0 = 49.2%`. Frustration around scares might come from scares that interrupt a task or follow a death. Context narrowed things less, so target those moments in the replay interview.
3. Hit ratio 6/8 = 75%. Seen within 5 s: 4 of 8 = 50%. The headline is "half the testers saw the marker in time," with "two never saw it and two saw it too late" next to it. The 75% hit ratio overstates the design's success.

</details>

## Lab hook

[Lab 13, arousal peaks and a second channel](../labs/lab13.md). You compute `P(state | peak)` overall and by context for a provided skin-conductance session, then run a small low-cost gaze study on one HUD element. Deliverable: the tables, the gaze results and a one-page memo.

## Sources

- Ambinder, M. (2011). "Biofeedback in Gameplay: How Valve Measures Physiology to Enhance Gaming Experience." Game Developers Conference, March 3, 2011. Slides from Valve's publications page (cdn.fastly.steamstatic.com/apps/valve/2011/ValveBiofeedback-Ambinder.pdf). Arousal and valence after Lang (1995); signal pros and cons ("difficult to determine valence" for heart rate and conductance; conductance range varies between people); Left 4 Dead 2 Director result; correlation table (checked against the PDF, September 2026); Alien Swarm mod (100 enemies in 240 s, timer tied to conductance, feedback loop, decay); Portal 2 eye aiming at 60 Hz.
- Ambinder, M. (2009). "Valve's Approach to Playtesting: The Application of Empiricism." Game Developers Conference, March 2009. Slides from Valve's publications page. Physiological measures listed alongside observation, verbal reports, surveys and stats; eye tracking "can lead to costly over-analysis."
- Wikipedia, "Nevermind (2015 video game)" (accessed September 2026). Developer Flying Mollusk; Windows and OS X release September 29, 2015 (confirmed on the Steam store page, app 342260, September 2026), Xbox One January 2017; Intel RealSense pulse tracking and Affectiva's Affdex; the game gets harder as stress rises and easier as the player calms down.
- Wikipedia, "Electrodermal activity" (accessed September 2026). Sympathetic control; EDA indexes arousal and the electrical change alone does not identify the emotion; 1 to 3 second response delay; use in polygraphs.
- Wikipedia, "Polygraph" (accessed September 2026), summarizing National Research Council (2003), *The Polygraph and Lie Detection*, National Academies Press. Evidence "scanty and scientifically weak"; accuracy insufficient for employee security screening; polygraphs measure arousal from many causes.
- Wikipedia, "Eye tracking" (accessed September 2026). Fixations and saccades; Just and Carpenter's (1980) strong eye-mind hypothesis; covert attention; heatmaps show gaze, not attention.
- Wikipedia, "Pupillary response" (accessed September 2026). Constriction to light; dilation with arousal, interest and cognitive load.
- Wikipedia, "Before Your Eyes" (accessed September 2026). GoodbyeWorld Games, Windows release April 8, 2021 (date and developer confirmed on the Steam store page, app 1082430, September 2026); webcam blink detection moves the story forward.
- Regulation (EU) 2016/679 (GDPR), Article 9, via gdpr-info.eu. Special categories include biometric data for uniquely identifying a person and data concerning health; explicit consent as a condition for processing.
- Hodent, C. (2017). *The Gamer's Brain*. CRC Press. Chapter "Attention."
- The 300-window session, all state counts, the hit rates of 0.80 and 0.05, the scare and death context tables, the six-tester prompt study and the 100 ms fixation threshold are teaching examples, not measurements from any game.

## Interactive spec: examples/w13-arousal-peaks.html

**Purpose.** Show that identical-looking arousal peaks come from a mix of emotional states in proportion to base rate times hit rate, and that context from a second channel, not a better sensor, is what narrows the mix.

**The one insight the visual must make obvious.** On first load, 60 peak markers on the left all look the same, while the bar under the right grid shows that only 26.7% of them were fear and 33.3% were frustration.

**Layout.** Two panels side by side at 1280px, stacked at 390px with the trace first. Controls and numbers panel below.

- Left, "What the sensor sees": a synthetic skin-conductance trace over 0 to 25 minutes (x axis, minutes) against conductance in µS (y axis, 2 to 8). Detected peaks are marked with identical neutral triangles above the trace. With "Colour the peaks" on, each triangle takes the colour and pattern of its window's true state.
- Right, "What was happening": a 20 × 15 grid of 300 squares in reading order (window 1 top left), each filled by true state. Peak windows get a thick outline. Under the grid, one horizontal stacked bar "Where the peaks came from," segmented by state with percentages printed in each segment, and a second bar "Where the time went" showing window shares, so students can compare the two.

**Data generation.** Deterministic, seeded (seed 13). Assign states to windows so that the counts match the controls exactly. Place fear windows in clusters of 2 to 3 around 8 scripted scare markers, frustration windows in clusters after 6 death markers, and excitement windows in clusters around 4 puzzle-solve markers; the rest neutral. For each state, mark exactly `round(n_s × h_s)` of its windows as peaks, chosen by the seeded generator, so the displayed counts equal the table. Draw the trace as a slow random-walk tonic level (range 3 to 5 µS) plus, for each peak window, an SCR shape starting 1.5 s after the window start, rising over 1.5 s to an amplitude of 0.6 to 1.2 µS and decaying with a time constant of 4 s. The amplitude must not depend on the state (this is the point).

**Controls.**

- Windows per state (number inputs): neutral 240, fear 20, frustration 25, excitement 15 (defaults). Keep the total at 300 by adjusting neutral automatically and showing a note.
- Hit rate per aroused state: sliders 0.0 to 1.0, step 0.05, default 0.80 each, with a "lock together" checkbox (default on).
- Neutral false-alarm rate: slider 0.00 to 0.30, step 0.01, default 0.05.
- Context filter (radio): "All windows" (default), "After a scripted scare," "After a death." Filtering greys out other windows in the grid and trace and recomputes the bars from the filtered set. The filtered sets use fixed coded counts: scare 20 windows (4 neutral, 12 fear, 1 frustration, 3 excitement), death 20 windows (4 neutral, 2 fear, 14 frustration, 0 excitement). In filtered mode, compute peaks as `n_s × h_s` without rounding and show one decimal.
- Toggle "Colour the peaks."
- Presets: "Default session," "Lock rates at 0.95," "Loose sensor (false alarms 0.10)," "Calm game (270 neutral, 10 each)," "Fear 0.9, frustration 0.6."
- Reset.

**Formulas.** `peaks_s = n_s × h_s` (rounded to whole windows in the unfiltered view); `P(s | peak) = peaks_s / Σ peaks_j`; share of aroused peaks = (fear + frustration + excitement peaks) / total peaks. Also show a verdict line: "A 'peak = fear' rule is right X% of the time."

**Numbers panel.** A four-row table with columns state, windows, hit rate, peaks, share of peaks, matching the lecture table. Plus total peaks and the verdict line.

**Test values.**

- Defaults: peaks 12, 16, 20, 12, total 60; shares 20.0%, 26.7%, 33.3%, 20.0%; aroused share 80.0%; verdict "right 26.7% of the time."
- Scare filter: peaks 0.2, 9.6, 0.8, 2.4, total 13.0; fear 73.8%.
- Death filter: peaks 0.2, 1.6, 11.2, 0.0, total 13.0; frustration 86.2%.
- False-alarm 0.10: peaks 24, 16, 20, 12, total 72; neutral 33.3%, fear 22.2%.
- Fear 0.9, frustration 0.6 (unlocked): peaks 12, 18, 15, 12, total 57; fear 31.6%, frustration 26.3%.
- Calm game (270, 10, 10, 10): peaks 13.5 shown as 14 when rounded in unfiltered view; to keep the test exact, display unrounded peaks in the numbers panel (13.5, 8, 8, 8, total 37.5) and neutral share 36.0%. The grid may outline 14 windows for neutral.
- All aroused rates 0.95 locked: peaks 12, 19, 23.75 (display 24 outlined), 14.25 (display 14), numbers panel unrounded, fear share 19 / 69 = 27.5%.

**Accessibility and style.** Shared tokens from `templates/interactive-tokens.css`, light and dark. States differ by colour and by fill pattern (neutral plain, fear diagonal hatch, frustration crosshatch, excitement dots), and the legend names them in text. Peak markers are large enough to see at 390px. All controls keyboard operable with visible focus. The numbers panel is readable by screen readers and updates with `aria-live="polite"`. Respect reduced motion: no animated trace drawing. No game art, logos, screenshots or real sensor data.
