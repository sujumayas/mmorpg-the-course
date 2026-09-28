"""CS101 lab 13, part A: three piece randomizers and a drought report.

Run:   python randomizers.py            (prints the drought report)
Test:  python test_lab13.py

Each randomizer is a generator: call next() on it to get the next piece.
Every randomizer takes its own random.Random object, so a seed fully decides
the sequence. Never call the module-level random.random() in this file.
"""
import random

PIECES = "IJLOSTZ"


def pure_random(rng):
    """Every piece is an independent roll: 1 in 7 each, no memory."""
    while True:
        yield rng.choice(PIECES)


def nes_style(rng):
    """The NES Tetris (1989) rule, copied as an algorithm.

    Roll 0-7. If the roll is 7 (a dummy value) or names the same piece as the
    previous one, roll again 0-6 and deal that second roll no matter what.
    Otherwise deal the first roll.

    TODO (step 2): replace the fallback line below with the rule above.
    Keep the previous piece in a local variable inside this generator.
    """
    while True:
        yield rng.choice(PIECES)  # TODO: fallback so the file runs; replace it


def seven_bag(rng):
    """The Guideline "Random Generator": shuffle all seven, deal them, repeat.

    TODO (step 3): build a list of the seven pieces, rng.shuffle() it,
    yield each piece, then start a new bag.
    """
    while True:
        yield rng.choice(PIECES)  # TODO: fallback so the file runs; replace it


def take(gen, n):
    """Return the next n pieces from a randomizer as a string."""
    return "".join(next(gen) for _ in range(n))


def gaps_between(seq, piece="I"):
    """Number of other pieces between consecutive copies of `piece`.

    Example: gaps_between("IJJIOI") == [2, 1]

    TODO (step 4): walk the string, remember the index of the last `piece`,
    and append (i - last - 1) each time you meet `piece` again.
    """
    return []


def repeat_rate(seq):
    """Fraction of positions where a piece equals the one before it."""
    if len(seq) < 2:
        return 0.0
    return sum(seq[i] == seq[i - 1] for i in range(1, len(seq))) / (len(seq) - 1)


def report(seed=13, n=100_000):
    """Print one row per randomizer. Compare with the lecture's table."""
    print(f"seed={seed}, {n:,} pieces each")
    print(f"{'randomizer':<12}{'I share':>9}{'mean gap':>10}{'max gap':>9}"
          f"{'gaps>=20':>10}{'repeats':>9}")
    for name, make in [("pure", pure_random), ("nes", nes_style), ("bag", seven_bag)]:
        seq = take(make(random.Random(seed)), n)
        gaps = gaps_between(seq)
        mean_gap = sum(gaps) / len(gaps) if gaps else float("nan")
        max_gap = max(gaps) if gaps else 0
        long_share = sum(g >= 20 for g in gaps) / len(gaps) if gaps else float("nan")
        print(f"{name:<12}{seq.count('I') / n:>9.4f}{mean_gap:>10.3f}{max_gap:>9}"
              f"{long_share:>10.4f}{repeat_rate(seq):>9.4f}")


if __name__ == "__main__":
    report()
