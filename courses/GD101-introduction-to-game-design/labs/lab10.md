# GD101 · Lab 10: Measuring luck in your prototype

**Week:** 10 · **Time:** 2 hours in the lab plus up to 2 hours at home · **Weight:** counts toward the paper prototype component (iteration evidence)

**Lecture:** [Week 10, Chance vs skill: the role of randomness](../lectures/w10-chance-vs-skill-and-randomness.md)

## Objective

Check the "skill plus a die" model against real rolls, then use it to measure how much luck decides the result of your own paper prototype. By the end you will have a number for your prototype's upset rate, a list of every random element in it, and one tested change that moves the upset rate toward a target you chose on purpose.

## Starter materials

- Dice: two d6 and one d20 per pair (physical or any dice app).
- A spreadsheet program (Google Sheets, LibreOffice Calc or Excel).
- Your team's paper prototype from week 6, in its current iteration.
- The simulation sheet below. Build it yourself from this description; it takes about ten minutes.

**Simulation sheet layout.** One row per round, 1,000 rows.

| Column | Header | Formula in row 2 (copy down) |
|---|---|---|
| A | A roll | `=RANDBETWEEN(1, $H$1)` |
| B | B roll | `=RANDBETWEEN(1, $H$1)` |
| C | A total | `=A2 + $H$2` |
| D | Result | `=IF(C2>B2, "W", IF(C2=B2, "T", "L"))` |

Put the die size `d` in cell H1 and the skill gap `g` in H2. In H4 compute the observed round edge with `=COUNTIF(D:D,"W") / (COUNTIF(D:D,"W") + COUNTIF(D:D,"L"))`. In H5 put the exact value from the lecture's formula: `=( $H$1^2 - ($H$1-$H$2) - ($H$1-$H$2-1)*($H$1-$H$2)/2 ) / ( $H$1^2 - ($H$1-$H$2) )`. That is `W / (W + L)` with `W = d² − T − L`. Press the recalculate key a few times and watch H4 move around H5.

**Luck audit table** (copy into your report):

| Random element | When it happens | Input or output | Size of swing (best case minus worst case) | Can the player respond after it? |
|---|---|---|---|---|

## Steps

1. **Roll the model by hand (20 minutes).** In pairs, play 50 rounds with a d6 and `g = 1`, then 50 rounds with a d20 and `g = 1`. Re-roll ties and do not count them. Record the win count for A. Compare your round edge with the lecture's 0.677 and 0.551.
2. **Simulate it (15 minutes).** Build the simulation sheet. Record H4 for five recalculations at each of these settings: d6 g1, d20 g1, d20 g3. Check that the averages sit within about 0.03 of 0.677, 0.551 and 0.645. Write one sentence on why your 50 hand-rolled rounds were further from the exact value than 1,000 simulated ones.
3. **Audit your prototype (25 minutes).** List every random element in your prototype in the luck audit table: dice, shuffles, draws, random setup, hidden information dealt at random. For each, estimate the swing: how much better the best outcome is than the worst, in your game's own units (spaces, points, cards). Classify each as input or output randomness.
4. **Find the biggest die (5 minutes).** Circle the element with the largest swing that the player cannot respond to afterward. That is the element most likely to decide games by itself.
5. **Measure the upset rate (30 minutes).** Pick one teammate who knows the prototype well (the "experienced" player) and recruit one person from another team who has never played it (the "new" player). Play as many complete games as time allows, at least four. Record the winner of each. The upset rate is the share of games the new player wins. With four to eight games this number is rough; say so in your report.
6. **Choose a target and turn one dial (at home).** Decide who your game is for and write a target upset rate with a reason ("a family game where the new player wins about 1 game in 3"). Then change exactly one thing: shrink or grow the circled random element, add or remove a decision that lets skill show, or change how many rounds or turns decide the game. Predict the direction the upset rate will move, using the lecture's three dials.
7. **Retest (at home).** Play at least four more experienced-versus-new games with the change. Record the new upset rate and whether it moved in the predicted direction.

## Deliverable

One document containing:

- The step 1 tallies and the step 2 table of simulated round edges.
- The completed luck audit table with the biggest-swing element circled.
- Before-and-after upset rates with the number of games for each.
- A 250-word design note: your target and why, the dial you turned, your prediction, what happened, and whether the sample was large enough to trust.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Model check | Hand and simulated edges recorded; simulation within 0.03 of exact; sample-size sentence is correct | Values recorded, explanation missing or vague | Missing or simulation built wrong | 20% |
| Luck audit | Every random element listed with swing in game units and a correct input/output label | Most elements listed; one or two labels wrong | Fewer than half the elements, or no labels | 25% |
| Test method | Experienced and new players identified; at least 4 games before and 4 after; results recorded game by game | Fewer games or missing per-game record | No test run | 20% |
| One-dial change | Exactly one change, linked to a named dial, with a prediction made before retesting | Change made but several things changed at once, or no prediction | No change | 20% |
| Design note | Target justified by audience; result compared with prediction; honest about sample size | Target stated without reason, or no comparison | Missing | 15% |
