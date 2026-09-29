"""CS203 Lab 08 starter: utility scoring you can tune. Standard library only.

Fill in the TODO functions, then run the tests:

    python3 test_utility.py

Then run this file to replay the lecture's 12-tick fight and your own:

    python3 utility.py

Conventions follow the week 8 lecture. Every input x and every curve output is
a number in [0, 1]. An action's score is the product of its considerations.
"""
import math

# ------------------------------------------------------------ your code: curves


def clamp01(x):
    return max(0.0, min(1.0, x))


def power(x, k):
    """TODO step 1. Return clamp01(x) ** k. k = 1 is linear, k > 1 stays low
    and rises late, 0 < k < 1 rises early."""
    raise NotImplementedError("power() is yours to write")


def logistic(x, mid=0.5, steep=10.0):
    """TODO step 1. Return 1 / (1 + e^(-steep * (x - mid))) for clamp01(x).
    The curve passes 0.5 at x = mid; larger steep makes it closer to a step."""
    raise NotImplementedError("logistic() is yours to write")


def piecewise(x, points):
    """TODO step 2. points is a list of (x, y) pairs sorted by x, first x = 0,
    last x = 1. Return y at x by linear interpolation between the two
    neighbouring points (MA101 week 8 lerp). Clamp x to [0, 1] first."""
    raise NotImplementedError("piecewise() is yours to write")


# ------------------------------------------------------------ your code: scoring


def score(considerations, combine="product"):
    """TODO step 3. considerations is a list of zero-argument functions, each
    returning a number in [0, 1]. Evaluate them in order.
    - If any returns 0, stop at once and return 0.0 (do not call the rest).
    - combine="product": return the product of all values.
    - combine="geomean": return the product ** (1 / number of considerations).
    """
    raise NotImplementedError("score() is yours to write")


def choose(scores, current=None, bonus=0.0):
    """TODO step 4. scores maps action name -> score. Multiply the score of
    `current` (if it is in scores) by (1 + bonus), then return the name with
    the highest score. Break exact ties by keeping `current` if it is tied,
    otherwise by the order of the dict."""
    raise NotImplementedError("choose() is yours to write")


# ------------------------------------------------------------ provided: the lecture's fight

LECTURE_HP = [30, 24, 21, 25, 22, 18, 23, 21, 24, 20, 23, 27]   # percent, per tick


def attack_desire(enemy_hp):
    """The lecture's Attack curve: 0.6 against a fresh enemy, rising linearly
    to 0.9 as the enemy's health fraction falls to 0."""
    return 0.6 + 0.3 * (1 - clamp01(enemy_hp))


def brute_scores(hp_percent, k=2.0, enemy_hp=1.0, potions=1):
    """The lecture's two actions. Attack depends on the enemy's health; Drink
    rises as our health falls and is disqualified when no potion is left."""
    x = hp_percent / 100
    return {
        "attack": score([lambda: attack_desire(enemy_hp)]),
        "drink": score([lambda: 1.0 if potions > 0 else 0.0,
                        lambda: power(1 - x, k)]),
    }


def replay(hp_trace, bonus=0.0, k=2.0, enemy_hp=1.0, channel=3):
    """Re-decide every tick. Returns (choices, switches, tick the first potion
    would finish or None). A potion finishes after `channel` drink ticks in a
    row; switching away restarts the channel."""
    current, switches, streak, finished, choices = "attack", 0, 0, None, []
    for tick, hp in enumerate(hp_trace, start=1):
        pick = choose(brute_scores(hp, k, enemy_hp), current, bonus)
        switches += pick != current
        streak = streak + 1 if pick == "drink" else 0
        if streak == channel and finished is None:
            finished = tick
        current = pick
        choices.append(pick)
    return choices, switches, finished


def decision_map(k=2.0, cols=20, rows=10):
    """Print which action wins for our HP (columns, 0% to 95%) against enemy
    HP (rows, 100% at the top to 10% at the bottom). D = drink, . = attack."""
    for r in range(rows):
        enemy = 1.0 - r / rows
        line = "".join("D" if max(brute_scores(100 * c / cols, k, enemy).items(),
                                   key=lambda kv: kv[1])[0] == "drink" else "."
                       for c in range(cols))
        print(f"enemy {enemy:4.0%}  {line}")
    print("           our HP 0% -> 95%, one column per 5%")


def crossover(k=2.0, attack=0.6):
    """TODO step 5. Return the HP fraction below which Drink beats Attack when
    there is no bonus: solve (1 - hp) ** k = attack for hp."""
    raise NotImplementedError("crossover() is yours to write")


if __name__ == "__main__":
    print(f"crossover k=1: {crossover(1):.4f}  k=2: {crossover(2):.4f}  k=3: {crossover(3):.4f}")
    for e in (1.0, 0.5, 0.1):
        print(f"enemy at {e:.0%}: drink below {crossover(2, attack_desire(e)):.1%} HP")
    for b in (0.0, 0.1, 0.2):
        choices, switches, done = replay(LECTURE_HP, bonus=b)
        row = " ".join("D" if c == "drink" else "A" for c in choices)
        print(f"bonus {b:.1f}: {row}   switches {switches}   first potion {done}")
    decision_map()
