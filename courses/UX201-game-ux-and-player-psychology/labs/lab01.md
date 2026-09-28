# UX201 · Lab 01: Measuring search cost

Assigned in week 1 ([lecture](../lectures/w01-perception-attention-memory.md)). Due at the start of week 2. Individual work; you need five participants, and you may pool recruitment with one classmate but must run and analyse your own sessions.

## Objective

Measure the intercept `a` and slope `k` of the search model `T = a + k × N` for pop-out and item-by-item search, with the target present and absent, on real people. Then use your own numbers, not the lecture's, to price a loot, minimap or menu screen from a shipped game and propose a redesign.

## Starter materials

**1. Display generator.** [`lab01-starter/make_displays.py`](lab01-starter/make_displays.py), standard-library Python 3. Run

```
python3 make_displays.py --out displays --seed <your student number>
```

It writes 48 SVG displays (2 modes × set sizes 4, 8, 16, 32 × target present or absent × 3 repetitions) in a random order, plus `trials.csv` (the run sheet you fill in) and `key.csv` (which trials have a target, and where). In pop-out mode the target is the only orange circle among grey circles. In conjunction mode the target is an orange circle among orange squares and grey circles. Your seed makes your displays different from your classmates'.

**2. Timing method.** Use one of these, and use the same one for every participant.

- *Preferred:* the interactive `examples/w01-loot-search.html` in its trial mode, once it is built. It times clicks to the millisecond and exports CSV.
- *Fallback:* open each SVG full screen in a browser. You press a key to show it and start a phone stopwatch at the same moment. The participant says "here" (and points) or "no" aloud, and you stop the watch. Stopwatch timing adds roughly 150 to 300 ms of noise per trial. That is acceptable because you are fitting slopes across set sizes, and the noise mostly lands in `a`.

**3. Participant script (read it word for word).**

> You'll see a set of shapes. Some screens contain one orange circle, some don't. As fast as you can without mistakes, say "here" and point if you see it, or say "no" if it isn't there. There are 48 screens and it takes about eight minutes. You can stop at any time.

**4. Consent line.** "I agree to take part in a timed visual search task for a course exercise. My name will not be recorded with my data, and I can stop at any time."

**5. Analysis sheet template.** One row per participant per condition. Fill in the mean RT of correct trials.

| Participant | Mode | Present? | N = 4 | N = 8 | N = 16 | N = 32 | Fitted `a` | Fitted `k` |
|---|---|---|---|---|---|---|---|---|
| P1 | popout | yes | | | | | | |

In a spreadsheet, fit each row with `=INTERCEPT(means, set_sizes)` and `=SLOPE(means, set_sizes)`.

## Steps

1. **Generate displays** with your seed. Open three at random to check they display correctly.
2. **Pilot on yourself.** Run all 48 trials. You now know the task. Mark your own data as a pilot and exclude it from the analysis.
3. **Run five participants.** Use the script and the consent line, one session each, the same screen and the same distance. Record RT and answer in `trials.csv`, and write any interruptions in the notes column.
4. **Score answers** against `key.csv`. Drop incorrect trials from the RT means and report the error rate per condition.
5. **Fit the four lines** (pop-out present, pop-out absent, conjunction present, conjunction absent) for each participant and for the group mean.
6. **Compare with theory.** Is the pop-out slope near zero? Is the conjunction target-absent slope about twice the present slope? Report your ratio.
7. **Price a real screen.** Pick one screen from a shipped game with many items to search: a loot drop, a minimap, a crafting list or a vendor. Take a screenshot for your own notes (don't submit copyrighted art; describe it and sketch it). Count `N`, decide which search type applies, and estimate a player's search time per visit with *your* fitted numbers. Then estimate visits per hour, as in the lecture's session table.
8. **Redesign.** Propose one change that lowers `N` or `k`. Predict the new time per visit and per hour. Name one risk of your change from the lecture's judgment list.

## Deliverable

A PDF of at most four pages, plus `trials.csv` for every participant as an appendix.

- Method in one paragraph: participants (no names), setting, timing method.
- A chart of mean RT against `N` for the four conditions, with fitted lines, and a table of fitted `a` and `k` per participant and for the group.
- Error rates per condition, and one sentence on whether any participant traded accuracy for speed.
- The shipped-game screen: a sketch, `N`, search type, and cost per visit and per hour.
- Your redesign with its predicted saving and one named risk.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Data collection | Five participants, script used, errors scored, interruptions noted, pilot excluded | Minor deviations, mostly documented | Fewer than four participants or undocumented method | 25% |
| Fitting and analysis | Correct fits for all four conditions, group and individual; present/absent ratio computed and discussed | Fits present with small errors or missing individual data | Fits missing or wrong | 25% |
| Comparison with theory | Clear statement of where the data match the model and where they don't, with a plausible reason | Comparison made but shallow | No comparison | 15% |
| Shipped-game pricing | `N`, search type and visit rate justified; arithmetic correct with the student's own `a` and `k` | Reasonable but uses lecture values or unexplained counts | Missing or unsupported | 20% |
| Redesign and writing | Change targets `N` or `k` explicitly, saving predicted, risk named; plain, numbers first | Redesign present, weak link to the model | Vague or missing | 15% |
