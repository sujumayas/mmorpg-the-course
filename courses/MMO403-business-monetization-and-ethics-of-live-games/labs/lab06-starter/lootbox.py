"""MMO403 Lab 06: the cost of a collection.

Run:  python lootbox.py       # prints the lecture 06 table once your functions work
      python check_lab06.py   # PASS / FAIL / TODO per function

Standard library only. Fill in every function that raises NotImplementedError.

A set is described by tiers: a list of (count, chance_per_item) pairs, for
example [(15, 0.054), (4, 0.045), (1, 0.01)]. Each box holds exactly one item,
so the sum of count * chance over all tiers must be 1. The LAST tier is the
rarest; pity rules apply to it.
"""
import math
import random
from itertools import product

SET = [(15, 0.054), (4, 0.045), (1, 0.01)]


def terms(tiers):
    """Given (from lecture 06). Yield (signed count, probability) for every mix
    of j_1 items from tier 1, j_2 from tier 2, and so on."""
    for picks in product(*(range(n + 1) for n, _ in tiers)):
        ways = 1
        for (n, _), j in zip(tiers, picks):
            ways *= math.comb(n, j)
        q = sum(j * p for (_, p), j in zip(tiers, picks))
        yield (-1) ** sum(picks) * ways, q


def expected_boxes(tiers):
    """Exact mean boxes to own every item, no protection, no pity.
    Inclusion-exclusion: sum over non-empty groups of (-1)^(|S|+1) / P(S)."""
    raise NotImplementedError


def p_complete(n, tiers):
    """Exact chance that n boxes contain every item, no protection, no pity:
    sum over all groups of (-1)^|S| * (1 - P(S))^n."""
    raise NotImplementedError


def protected_cdf(tiers, n_max):
    """Duplicate protection, no pity. Tiers are drawn at their total chance
    (count * chance); within a tier you always get an item you do not own yet,
    until you own them all. The set is complete after `count` hits on every
    tier. Return cdf, a list of length n_max + 1 with cdf[n] = P(complete
    within n boxes). Use a dynamic program over capped hit counts per tier."""
    raise NotImplementedError


def mean_from_cdf(cdf):
    """E[T] = sum over n of (1 - cdf[n]), for n = 0 .. len(cdf) - 2."""
    raise NotImplementedError


def percentile_from_cdf(cdf, share):
    """Smallest n with cdf[n] >= share."""
    raise NotImplementedError


def simulate(tiers, protect=False, pity=None, trials=10_000, seed=406):
    """Monte Carlo. Return a list of `trials` completion times (boxes).
    Each box: if pity is set, you do not yet own every last-tier item, and the
    last pity - 1 boxes held no last-tier item, this box is a last-tier item
    (the lecture's pity stops once the Legendary is owned); otherwise draw the tier at its total
    chance. Then pick the item: uniform within the tier, or, if protect is
    True, uniform among the tier's items you do not own yet (uniform over the
    whole tier if you own them all). A last-tier item resets the pity count.
    Use random.Random(seed)."""
    raise NotImplementedError


def summarize(samples):
    """Return (mean, median, p90) of a list of completion times, where the
    median and p90 are the smallest values v with at least 50% and 90% of
    samples <= v."""
    raise NotImplementedError


def box_price_in_money(box_gems, bundle_gems, bundle_price):
    """Real-money price of one box at a bundle's exchange rate."""
    raise NotImplementedError


def main():
    print(f"no protection : mean {expected_boxes(SET):.2f}")
    cdf = protected_cdf(SET, 3000)
    print(f"protection    : mean {mean_from_cdf(cdf):.2f}, median "
          f"{percentile_from_cdf(cdf, 0.5)}, p90 {percentile_from_cdf(cdf, 0.9)}")
    for prot, pity in ((False, 40), (True, 40)):
        m, med, p90 = summarize(simulate(SET, prot, pity))
        print(f"sim protect={prot!s:5} pity={pity}: mean {m:.1f}, median {med}, p90 {p90}")


if __name__ == "__main__":
    main()
