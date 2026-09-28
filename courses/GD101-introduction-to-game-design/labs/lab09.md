# GD101 · Lab 09: Solve it, then fix it

Assigned in week 9 ([lecture](../lectures/w09-choice-and-meaningful-decisions.md)). Due at the start of week 10. This is playtest report 3 of 3.

## Objective

Use a minimax solver to see exactly where tic-tac-toe's decisions die, then apply the same thinking to your own prototype: audit its choice points, find the weakest decision, and test one rule change aimed at it with silent playtesters.

## Starter materials

- Python 3 (any version from 3.8). No extra packages. If you have never run Python, the lab room machines have it installed; run the script with `python lab09_solver.py`.
- The solver below. Copy it into a file named `lab09_solver.py`.
- The decision audit table from lecture section 3 (copy it into your report).
- The week 9 interactive, [the tic-tac-toe tree](../examples/w09-tictactoe-tree.html), to check individual positions.

```python
"""GD101 lab 09 starter: solve tic-tac-toe (and variants) by minimax."""
from functools import lru_cache
from collections import Counter

LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
MISERE = False   # True: completing a line LOSES instead of winning

def line_owner(b):
    for a, c, d in LINES:
        if b[a] != '.' and b[a] == b[c] == b[d]:
            return b[a]
    return None

def to_move(b):
    return 'X' if b.count('X') == b.count('O') else 'O'

def is_over(b):
    return line_owner(b) is not None or '.' not in b

def children(b):
    p = to_move(b)
    return {i: b[:i] + p + b[i+1:] for i in range(9) if b[i] == '.'}

@lru_cache(maxsize=None)
def value(b):
    """Minimax value from X's point of view: +1 X wins, 0 draw, -1 O wins."""
    owner = line_owner(b)
    if owner:
        v = 1 if owner == 'X' else -1
        return -v if MISERE else v
    if '.' not in b:
        return 0
    vals = [value(c) for c in children(b).values()]
    return max(vals) if to_move(b) == 'X' else min(vals)

def classify(b):
    vals = [value(c) for c in children(b).values()]
    if len(vals) == 1:
        return 'forced'
    return 'no-stakes' if len(set(vals)) == 1 else 'stakes'

def all_positions():
    seen, stack = set(), ['.' * 9]
    while stack:
        b = stack.pop()
        if b in seen:
            continue
        seen.add(b)
        if not is_over(b):
            stack.extend(children(b).values())
    return seen

def count_games(b='.' * 9):
    if is_over(b):
        o = line_owner(b)
        return Counter({o or 'draw': 1})
    total = Counter()
    for c in children(b).values():
        total += count_games(c)
    return total

if __name__ == '__main__':
    pos = all_positions()
    open_pos = [b for b in pos if not is_over(b)]
    print('games (by who completed a line):', dict(count_games()))
    print('positions:', len(pos), ' unfinished:', len(open_pos))
    print('value of empty board:', value('.' * 9))
    print('decision classes:', dict(Counter(classify(b) for b in open_pos)))
    for sq in range(9):
        b = '.' * 9
        b = b[:sq] + 'X' + b[sq+1:]
        print('X opens at', sq, '-> O move values:', {i: value(c) for i, c in children(b).items()})
```

**Expected output for standard tic-tac-toe (`MISERE = False`).** Your run must show 131,184 X wins, 77,904 O wins and 46,080 draws (255,168 games), 5,478 positions of which 4,520 are unfinished, an empty-board value of 0, and decision classes of 3,191 stakes, 1,107 no-stakes and 222 forced. For X opening at square 0, only O's move to square 4 has value 0. If your numbers differ, you copied the script wrong.

**How to read positions.** A board is a 9-character string, squares 0 to 8 left to right, top to bottom, `.` for empty. For example `'..OXO.XOX'` is the worked position from lecture section 2.

## Steps

1. **Reproduce.** Run the script and confirm the expected output. Paste it into your report.
2. **Check the hand example.** Add a line that prints `{i: value(c) for i, c in children('..OXO.XOX').items()}` and confirm squares 0, 1 and 5 give +1, 0 and −1.
3. **Run the variant.** Set `MISERE = True` (completing a line now loses) and run again. Record the empty-board value and the three decision-class counts. Compare them with standard tic-tac-toe in a small table. The game counts do not change, because the same move sequences are possible; only the values do.
4. **Explain the difference.** In three or four sentences: did the misère rule make more or fewer decisions stakes? Does that make misère tic-tac-toe more interesting for a human? Play it five times with a partner before you answer.
5. **Audit your prototype.** Fill in the section 3 audit table for every choice point in your paper prototype (at least four). Mark the weakest decision and the test it fails.
6. **Design one fix.** Write a single rule change aimed at that test, and write two situations in which different options should now be best. If you cannot write two, redesign the fix.
7. **Test the fix.** Run three silent playtests (lab 07 protocol) with the new rule. At the choice point, log hesitation, instant identical choices and "does it matter?" questions. Record which option each tester picked in each situation.
8. **Decide.** Apply a keep, change or kill decision (lab 08 format) using criteria you wrote before step 7.

## Deliverable

A PDF of at most four pages plus raw logs as an appendix.

- The script output for standard and misère tic-tac-toe, with the comparison table and your explanation.
- The completed audit table for your prototype, with the weakest decision marked.
- The fix, the two situations, the kill criteria, and the playtest evidence with counts.
- Your decision, and one sentence on what the next loop should test.

## Rubric

| Criterion | Excellent (4) | Adequate (2-3) | Weak (0-1) | Weight |
|---|---|---|---|---|
| Solver work | Output matches expected values, misère run correct, comparison explained using the forced / no-stakes / stakes terms | Output correct, explanation thin | Output missing or wrong | 20% |
| Decision audit | Every choice point audited against all tests, weakest decision identified with a clear reason | Most choice points audited, reasons thin | Fewer than four or tests misapplied | 25% |
| Fix design | One rule change aimed at the failed test, two situations with different best options | Plausible fix, situations weak | Fix unrelated to the failed test | 20% |
| Playtest evidence | Three silent sessions, counts of hesitation and choices per situation, criteria set before testing | Evidence present but partly anecdotal | No usable evidence | 25% |
| Writing | Clear, numbers first, at most four pages | Readable but padded | Hard to follow | 10% |
