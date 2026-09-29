"""MMO306 Lab 09 starter: measuring a dungeon generator.

The generator and validator at the top are given. Fill in every function marked
TODO below them. Standard library only.
Run the checks with:   python test_lab09.py
Run the report with:   python generator.py
"""
import math
import random
from collections import Counter

# ---------- given: the generator ----------

AXES = {
    "layout":   {"Crypt": 3, "Mine": 3, "Library": 2, "Sewer": 1, "Garden": 1},
    "boss":     {"Golem": 1, "Lich": 1, "Hydra": 1, "Matron": 1},
    "modifier": {"Fog": 4, "Haste": 3, "Frenzy": 1, "Ember": 1, "Frost": 1},
}
SALIENT = ("layout", "boss", "modifier")


def generate(rng, axes=AXES):
    """One raw dungeon: a salient value per axis plus decoration players don't remember."""
    inst = {name: rng.choices(list(vals), weights=list(vals.values()))[0]
            for name, vals in axes.items()}
    inst["decoration_seed"] = rng.getrandbits(32)
    inst["torch_count"] = rng.randint(8, 30)
    return inst


def validate(inst):
    """Design rule: the Hydra needs water, so it cannot appear in the Library or the Garden."""
    return not (inst["boss"] == "Hydra" and inst["layout"] in ("Library", "Garden"))


def generate_valid(rng, axes=AXES, max_attempts=20, fallback=None):
    """Generate until valid, at most max_attempts times. Return (instance, attempts).
    If every attempt fails, return (fallback, max_attempts)."""
    for attempt in range(1, max_attempts + 1):
        inst = generate(rng, axes)
        if validate(inst):
            return inst, attempt
    return fallback, max_attempts


# ---------- yours ----------

def signature(inst, salient=SALIENT):
    """The tuple of salient values, in the order of `salient`. Ignore everything else."""
    raise NotImplementedError("TODO: signature")


def effective_variety(weights):
    """1 / sum of squared probabilities. weights: any positive numbers."""
    raise NotImplementedError("TODO: effective_variety")


def perceived_and_effective(axes=AXES):
    """Return (M, M_eff) for independent axes: product of value counts, product of effective varieties."""
    raise NotImplementedError("TODO: perceived_and_effective")


def p_repeat(n, m_eff):
    """Approximate chance that some two of n runs share a signature."""
    raise NotImplementedError("TODO: p_repeat")


def p_repeat_uniform_exact(n, m):
    """Exact chance of a repeat within n draws from m equally likely signatures."""
    raise NotImplementedError("TODO: p_repeat_uniform_exact")


def n50(m_eff):
    """0.5 + sqrt(0.25 + 2 ln 2 * m_eff)."""
    raise NotImplementedError("TODO: n50")


def measured_m_eff(signatures):
    """Estimate effective variety from observed signatures: 1 / sum of squared frequencies."""
    raise NotImplementedError("TODO: measured_m_eff")


def first_repeat_median(trials, seed, axes=AXES, memory=0):
    """Median run number of the first repeated signature over `trials` simulated players.
    Each run calls generate_valid(rng, axes) and takes its signature over every axis in
    `axes` (so an added axis counts as salient). With memory k > 0,
    a signature equal to any of the last k is redrawn (a redraw is not a run).
    Use one random.Random(seed) for everything. Median = sorted list [trials // 2]."""
    raise NotImplementedError("TODO: first_repeat_median")


def expected_attempts(v):
    """Expected attempts until a valid output when a fraction v pass."""
    raise NotImplementedError("TODO: expected_attempts")


def p_more_than(v, k):
    """Chance of needing more than k attempts."""
    raise NotImplementedError("TODO: p_more_than")


def report():
    m, me = perceived_and_effective()
    print(f"inputs: M={m}  M_eff={me:.1f}  n50={n50(me):.1f}")
    rng = random.Random(1)
    sigs, tries = [], []
    for _ in range(20000):
        inst, a = generate_valid(rng)
        sigs.append(signature(inst))
        tries.append(a)
    v = 20000 / sum(tries)
    print(f"accepted: {len(set(sigs))} distinct signatures, measured M_eff={measured_m_eff(sigs):.1f}")
    print(f"pass rate v={v:.3f}  expected attempts={expected_attempts(v):.2f}  "
          f"P(>5 attempts)={p_more_than(v, 5):.5f}")
    print("simulated median first repeat:", first_repeat_median(4000, seed=2))
    print("with memory 3:", first_repeat_median(4000, seed=2, memory=3))


if __name__ == "__main__":
    report()
