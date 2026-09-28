# CS101 · Lab 01: The state of a text adventure

**Week:** 1 · **Time:** 2 hours in the lab · **Weight:** one of the weekly exercises (40% of the course across the semester)

**Lecture:** [Week 01, programs, variables and types](../lectures/w01-programs-variables-and-types.md)

## Objective

Store a small cave's state in variables of the right type, convert keyboard input, and implement the two edge behaviours from the lecture. Gold is clamped at a cap. The level counter wraps like Pac-Man's 8-bit counter. By the end you can predict every value your program prints before you run it.

## Starter materials

- [`lab01-starter/state.py`](lab01-starter/state.py). The program you edit. It runs as given, but every value it prints is wrong or has the wrong type. Each part is marked `TODO`.
- [`lab01-starter/check_lab01.py`](lab01-starter/check_lab01.py). A checker that runs your program with four sets of keyboard input and reports which parts pass. Do not edit it.
- Python 3.12 or newer. Nothing else to install.

Run both from inside the `lab01-starter` folder:

```
python state.py
python check_lab01.py
```

## Steps

1. **Run it first (5 min).** Run `state.py`, type `5`, `2.5` and `3`, and read the STATUS line. Run the checker and read its report. Everything fails. That is expected.
2. **Part A, types (15 min).** Fix the types of `lamp_oil` and `lamp_lit`. Before you change anything, write down what `type()` returns for each value now, and what it should return.
3. **Part B, conversion (15 min).** Convert the three inputs. Try the program with the input `12` for coins before you convert, and note in your log what `gold + found` does with a string. Then fix it.
4. **Part C, the move north (10 min).** Light the lamp, move to the hall and spend the oil.
5. **Part D, clamp (15 min).** Add the coins but never go above `GOLD_CAP`. Test with 5 coins (expect 995) and with 20 coins (expect 999).
6. **Part E, wrap (20 min).** Add the levels gained, wrapped to 8 bits. Before running, predict the stored level for 3, 10 and 262 levels gained from a start of 250. Write the predictions in your log, then check them.
7. **Run the checker (5 min).** Fix anything it reports until it prints `4/4 parts pass`.
8. **Stretch (optional).** Add a 16-bit `turn_counter` that starts at 65,530 and wraps. Add a `LEVEL_SIGNED` switch that reports the level as a signed 8-bit value using the lecture's signed formula.

## Deliverable

Submit a zip with:
- Your edited `state.py`.
- A plain-text or Markdown log (about 200 words) with: the `type()` of each variable before and after Part A; what happened when you added a string to an int in Part B, including the exact error message; your three predictions from step 6 next to the actual values; and one sentence on when you would choose clamping over wrapping in a game of your own.
- A screenshot or pasted copy of the checker output.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Missing or wrong (0-1) | Weight |
|---|---|---|---|---|
| Checker parts | 4/4 parts pass | 2-3 parts pass | 0-1 parts pass | 40% |
| Types and conversions | Every variable has the right type; conversions happen once, where input is read | Right types, but conversions repeated or done late | Wrong types remain | 15% |
| Predictions | All three wrap predictions written before running, with the arithmetic shown | Predictions present but some after the fact or without working | No predictions | 20% |
| Log quality | Exact error message quoted; clamp vs wrap sentence names a concrete game value | Log complete but vague | Log missing parts | 15% |
| Code readability | Clear names, comments only where they add something, STATUS line untouched | Minor clutter | Hard to follow or checker format broken | 10% |
