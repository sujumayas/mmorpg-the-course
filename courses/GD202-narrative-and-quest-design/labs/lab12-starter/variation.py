"""GD202 Lab 12: variation engine.

Standard library only. Fill in the TODO parts, then run the tests:

    .venv/bin/python courses/GD202-narrative-and-quest-design/labs/lab12-starter/test_variation.py

Once they pass, compare the rules:

    .venv/bin/python courses/GD202-narrative-and-quest-design/labs/lab12-starter/variation.py

Every selector picks among n variants, numbered 0..n-1. Call next() once per
time the line fires. It returns a variant index, or None when a once-only
selector has run out. Selectors that use randomness take a random.Random
object so that results can be repeated with a seed (like ink's SEED_RANDOM).
"""
import random


class Stopping:
    """Play 0, 1, ..., n-1 in order, then keep playing n-1 (ink: {a|b|c})."""

    def __init__(self, n):
        self.n = n
        self.plays = 0

    def next(self):
        i = min(self.plays, self.n - 1)
        self.plays += 1
        return i


class Once:
    """TODO 1. Play 0, 1, ..., n-1 in order, then return None forever
    (ink: {!a|b|c}; Yarn Spinner: <<once>>)."""

    def __init__(self, n):
        self.n = n

    def next(self):
        raise NotImplementedError("Once.next() is yours to write")


class Cycle:
    """TODO 2. Play 0, 1, ..., n-1, then start again at 0 (ink: {&a|b|c})."""

    def __init__(self, n):
        self.n = n

    def next(self):
        raise NotImplementedError("Cycle.next() is yours to write")


class RandomPick:
    """TODO 3. Each play, a uniform random index, independent of the past
    (ink: RANDOM; Yarn Spinner: dice). Use self.rng.randrange."""

    def __init__(self, n, rng):
        self.n = n
        self.rng = rng

    def next(self):
        raise NotImplementedError("RandomPick.next() is yours to write")


class ShuffleBag:
    """TODO 4. Shuffle all n indices (self.rng.shuffle), play them in order,
    and reshuffle when the bag is empty. The new bag may start with the line
    that ended the old one (ink: {~a|b|c}; Yarn Spinner's default saliency)."""

    def __init__(self, n, rng):
        self.n = n
        self.rng = rng

    def next(self):
        raise NotImplementedError("ShuffleBag.next() is yours to write")


class NoRepeatBag(ShuffleBag):
    """TODO 5. Like ShuffleBag, but when a new bag would start with the line
    that was just played, swap that first line with another position chosen
    at random from the rest of the new bag. Never plays the same line twice in
    a row when n >= 2."""

    def next(self):
        raise NotImplementedError("NoRepeatBag.next() is yours to write")


def plays(selector, k):
    """Provided: the first k picks of a selector, as a list."""
    return [selector.next() for _ in range(k)]


def count_back_to_back(seq):
    """TODO 6. How many positions i >= 1 have seq[i] == seq[i - 1]
    (ignoring None values)?"""
    raise NotImplementedError("count_back_to_back() is yours to write")


def first_repeat(seq):
    """TODO 7. The 1-based play number at which a line is heard for the second
    time, or None if no line repeats. Example: [3, 1, 3] -> 3."""
    raise NotImplementedError("first_repeat() is yours to write")


def p_any_repeat(n, k):
    """TODO 8. Chance that k independent uniform picks from n lines contain at
    least one repeat: 1 - (n/n)((n-1)/n)...((n-k+1)/n). Return 1.0 if k > n."""
    raise NotImplementedError("p_any_repeat() is yours to write")


def lines_needed(k, target):
    """TODO 9. The fewest lines n >= k such that k random picks are all
    different with chance at least `target`."""
    raise NotImplementedError("lines_needed() is yours to write")


def compare(n=5, k=100, trials=2000, seed=1):
    """Provided: average back-to-back repeats per k plays for each rule."""
    rng = random.Random(seed)
    makers = {
        "random": lambda: RandomPick(n, rng),
        "shuffle bag": lambda: ShuffleBag(n, rng),
        "no-repeat bag": lambda: NoRepeatBag(n, rng),
        "cycle": lambda: Cycle(n),
        "stopping": lambda: Stopping(n),
    }
    out = {}
    for name, make in makers.items():
        total = sum(count_back_to_back(plays(make(), k)) for _ in range(trials))
        out[name] = total / trials
    return out


if __name__ == "__main__":
    for n in (3, 5, 10):
        res = compare(n=n)
        print(f"n = {n:>2}: " + ", ".join(f"{name} {v:.2f}" for name, v in res.items()))
    print("lines needed so 5 random plays are all different 90% of the time:", lines_needed(5, 0.9))
