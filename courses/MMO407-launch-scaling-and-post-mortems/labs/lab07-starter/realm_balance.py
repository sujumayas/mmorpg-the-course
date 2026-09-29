"""MMO407 lab 07: faction balance simulator.

One step is one week. Counts are floats (a fluid model of averages), as in the
lecture. Standard library only. Run the tests from inside lab07-starter/ with:
    python -m unittest test_realm_balance.py
"""

LECTURE = dict(J=1000, c=0.05, k=2, e=0.2)


def newcomer_share(s, k):
    """Share of this week's newcomers who pick faction A when A holds share s.

    p = s^k / (s^k + (1 - s)^k). Must return 0.5 at s = 0.5 for any k.
    """
    # TODO 1: the lecture's newcomer rule
    raise NotImplementedError("TODO 1")


def week(A, B, J=1000, c=0.05, k=2, e=0.2, lock=None, spill=0.5):
    """Advance one week. Returns (A, B, turned_away).

    Newcomers: J * p pick A and J * (1 - p) pick B.
    Lock: if lock is not None and A's share s > lock, A's newcomers are
    blocked; a fraction `spill` of them join B, the rest leave (turned away).
    The same rule applies to B when 1 - s > lock.
    Leaving: both factions lose c; the smaller one also loses e * |2s - 1|.
    """
    # TODO 2: follow the docstring; compute s, newcomers, lock, leaving
    raise NotImplementedError("TODO 2")


def simulate(A, B, weeks, **kw):
    """Run `weeks` steps. Returns a list of (A, B) of length weeks + 1,
    where entry 0 is the start. Also returns total turned away.
    """
    rows = [(A, B)]
    turned = 0.0
    for _ in range(weeks):
        A, B, t = week(A, B, **kw)
        turned += t
        rows.append((A, B))
    return rows, turned


def share(row):
    A, B = row
    return A / (A + B)


def first_week_at(rows, threshold):
    """First week whose share of A is >= threshold, or None."""
    # TODO 3: scan rows in order
    raise NotImplementedError("TODO 3")


def realm_choice(pops, J, k):
    """Split J newcomers across several realms: pop_i^k / sum(pop_j^k).
    Returns a list of newcomer counts, one per realm (used in Part C)."""
    # TODO 4: the lecture's section 3 rule
    raise NotImplementedError("TODO 4")


if __name__ == "__main__":
    rows, _ = simulate(5500, 4500, 52, **LECTURE)
    for w in (0, 1, 4, 8, 12, 16, 26, 52):
        print(f"week {w:2d}: A share {100 * share(rows[w]):5.1f}%")
