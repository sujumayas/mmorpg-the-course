"""MMO406 Lab 05 starter: naming languages players can tell apart.

Standard library only. Fill in the four TODO functions, then run the tests:

    .venv/bin/python courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab05-starter/test_naming.py

Model (week 5, section 2). A naming language is a dict {syllable: usage weight},
weights adding up to 1.

    o_count  = |S_A ∩ S_B| / |S_A|
    o        = sum of A's weights over the shared syllables
    P_amb(L) = (1 - m) * o**L        chance an L-syllable A-name could pass for B
"""
import random  # noqa: F401  (you will need it for generate)


def overlap(a, b, weighted=True):
    """TODO 1. Share of A's syllables (weighted=False) or of A's usage
    (weighted=True) that B also uses. Direction matters: overlap(a, b) is
    generally not overlap(b, a)."""
    raise NotImplementedError("overlap() is yours to write")


def ambiguity(o, L, m=0.0):
    """TODO 2. P_amb for names of exactly L syllables, marker share m."""
    raise NotImplementedError("ambiguity() is yours to write")


def mixed_ambiguity(o, length_probs, m=0.0):
    """TODO 3. P_amb when name length varies.

    length_probs is a dict {L: probability}, for example {2: 0.5, 3: 0.5}.
    Return the length-weighted average of ambiguity(o, L, m)."""
    raise NotImplementedError("mixed_ambiguity() is yours to write")


def generate(weights, n, L, seed=1, marker=None, m=0.0):
    """TODO 4. Return n names, each a tuple of L syllables.

    Use rng = random.Random(seed) and draw each syllable with
    rng.choices(syllables, weights=w)[0], so results are repeatable.
    If `marker` is a set of syllables and m > 0, then for each name draw
    rng.random() once before its syllables; if that draw is below m, the
    name's LAST syllable is drawn only from the marker syllables (by their
    weights, renormalized). Other syllables are drawn as usual."""
    raise NotImplementedError("generate() is yours to write")


def could_pass(name, other):
    """True if every syllable of `name` also occurs in the other culture."""
    return all(s in other for s in name)


if __name__ == "__main__":
    from cultures import DURHK, VESSARI

    for label, a, b in [("Vessari", VESSARI, DURHK), ("Durhk", DURHK, VESSARI)]:
        print(label, "count", round(overlap(a, b, False), 3), "weighted", round(overlap(a, b), 3))
    for name in generate(VESSARI, 12, 2, seed=1):
        flag = "  <- could pass for Durhk" if could_pass(name, DURHK) else ""
        print("".join(name).capitalize() + flag)
