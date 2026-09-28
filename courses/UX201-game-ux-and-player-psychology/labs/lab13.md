# UX201 · Lab 13: Arousal peaks and a second channel

Assigned in week 13 ([lecture](../lectures/w13-biometrics-and-eye-tracking.md)). Due at the start of week 14. Pairs; each pair submits one memo.

## Objective

Part A: take a skin-conductance session whose peaks have already been detected, and find out what a peak means. Compute `P(state | peak)` for the whole session and for each game-event context, and measure how wrong a "peak means fear" rule would be. Part B: run a small gaze study on one HUD element with a low-cost method, and report hit ratio, time to first look and recall instead of a heatmap. The point of both parts is the same. A body signal tells you where to look. It needs a second channel before it tells you what happened.

## Starter materials

**1. Session data.** [`lab13-starter/session_T2.csv`](lab13-starter/session_T2.csv) is a 30-minute session from one invented tester, split into 360 windows of 5 seconds. Columns: `window`, `start_s`, `context` (the game-log event that started 0 to 5 s before the window: `scare`, `death`, `solve` or `none`), `coded_state` (an observer's coding from face video, think-aloud and a replay interview: `neutral`, `fear`, `frustration` or `excitement`), and `peak` (1 if a skin-conductance response starts in the window, already shifted for the 1 to 3 s lag). The file is a teaching data set, not a real recording. [`lab13-starter/make_session.py`](lab13-starter/make_session.py) regenerates it deterministically and documents how it was built. Read it after you finish Part A, not before.

**2. Analysis script.** [`lab13-starter/reverse_inference.py`](lab13-starter/reverse_inference.py), standard-library Python 3. It prints, for the chosen windows, each state's window count, peak count, observed hit rate and `P(state | peak)`, plus the share of peaks from aroused states. Options: `--context` (`all`, `none`, `scare`, `death`, `solve`) and `--blind-rule` (a state; reports how often "every peak = that state" is right).

**3. Gaze method for Part B (pick one).**

- *Webcam gaze estimation.* WebGazer.js (Brown University, open source, runs in the browser with a webcam, no video leaves the machine) gives rough on-screen gaze points after a short calibration. Expect errors of a few centimetres, so use AOIs no smaller than about a fifth of the screen width.
- *Face-cam coding.* Record the tester's face with a phone mounted above the screen, and record the screen at the same time. Sync both with a clap. Code, frame by frame, whether the eyes move toward the AOI's screen region. Coarser than WebGazer, and more reliable in poor light.

**4. Stimulus for Part B.** Any game or prototype with a HUD element that appears at a known moment and carries information the player needs within a few seconds: a tutorial prompt, a new-quest marker, a low-health warning. Write down, before testing, the AOI, when the element appears, how long it stays, and the **deadline** by which the player must have noticed it for it to be useful.

**5. Consent sheet.** One paragraph that names what you record (webcam or face video, screen, answers), why, how long you keep it, and that the tester can stop at any time. Testers sign or tick it before recording starts. Store files under tester codes (P1, P2, ...), never names.

**6. Recall question (ask it exactly, right after the segment).** "Did anything on screen tell you what to do in that fight? If so, what did it say?"

## Steps

### Part A: what a peak means (in the lab session)

1. **Predict.** Before running anything, write down your guess for the share of all peaks that are fear.
2. **Whole session.** Run `python3 reverse_inference.py session_T2.csv --blind-rule fear`. Record the table. Compare the share of peaks from aroused states with the share that are fear.
3. **By context.** Rerun with `--context none`, `scare`, `death` and `solve`. Build one table with a row per context and columns for window count, peak count and `P(fear | peak)`, `P(frustration | peak)`, `P(excitement | peak)`.
4. **Check one row by hand.** Pick the death context. Recompute `P(frustration | peak)` from the window and peak counts using `n_s × h_s / Σ n_j × h_j`, and confirm it matches the script.
5. **Hit rates.** Look at the observed hit rates by state in the whole session. Are they close enough to equal that the peak alone can't separate the aroused states? Say which pair is most nearly separable, and by how much.
6. **Read the generator.** Open `make_session.py` and compare its `HIT` and `CONTEXT_MIX` values with what you measured. Explain any gap with sample size (the fear windows in the `none` context number only about 14).

### Part B: one HUD element, four or more testers

7. **Pilot** on one classmate. Check that your AOI is large enough for your method and that you can find the element's appearance time in the recording.
8. **Run four to six testers** who have not played the segment. Read the consent sheet, calibrate (if using WebGazer), play the segment, ask the recall question.
9. **Code each tester.** Hit (did gaze enter the AOI while it was visible?), time to first look in seconds, whether the first look came before your deadline, and recall (yes, partial, no).
10. **Compute.** Hit ratio with its Wilson 95% interval (MA102 week 13), the share who looked before the deadline, and the share with correct recall. If your tool draws a heatmap, include it, then write one sentence on what it hides.

## Deliverable

A memo of at most one page plus appendices.

- Part A: your prediction, the whole-session table, the context table, your hand check, and three sentences on what this tester's peaks can and cannot support.
- Part B: the element, AOI, deadline and method; a per-tester table (hit, time to first look, before deadline, recall); hit ratio with interval; the "in time" and recall shares; and one design recommendation.
- A closing paragraph: if your team had one sensor budget for next month's playtests, which question would you answer with it and which second channel would you pair it with?
- Appendices: script output, coding sheet, signed consent tick-list (codes only).

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Reverse inference (Part A) | Tables correct, hand check matches, clear distinction between "aroused" and "afraid", context effect quantified | Tables correct, interpretation thin | Reads peaks as a specific emotion | 30% |
| Sampling and hit rates | Uses window counts to judge how far observed hit rates can be trusted; explains gaps with the generator | Mentions sample size without using it | Treats observed rates as exact | 15% |
| Gaze study method (Part B) | AOI, deadline and threshold set before testing; consent handled; recording synced; coding consistent | Minor gaps in setup or coding | No deadline, or coding unclear | 20% |
| Gaze metrics | Hit ratio with Wilson interval, in-time share and recall reported per tester and in total; heatmap limits stated | Metrics reported without interval or recall | Heatmap or mean dwell alone | 20% |
| Recommendation and closing | Recommendation follows from the in-time and recall data; sensor plan pairs one signal with a named second channel | Plausible but generic | Missing, or "add biometrics" with no question | 15% |
