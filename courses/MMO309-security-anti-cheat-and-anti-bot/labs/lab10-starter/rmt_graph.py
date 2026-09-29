"""MMO309 Lab 10: follow the gold.

Fill in every function marked TODO. The model is the one from the week 10 lecture:
  fan-in(a)         number of distinct accounts that sent gifts to a
  fan-out(a)        number of distinct accounts a sent gifts to
  stranger share(a) share of a's fan-out that is outside a's guild
                    (every recipient counts as a stranger if a has no guild)
  hub               fan-in >= k and stranger share >= s
  careful expansion add senders of flagged accounts that have no guild and age < max_age,
                    repeated for `hops` rounds (each round expands from everything flagged so far)

Run `python rmt_graph.py` to print the results table for the lab server.
"""
from make_server import lab_server, toy_server


def build_index(gifts):
    """Return (senders, receivers): dicts mapping an account id to a set of ids.
    senders[a] = accounts that sent gifts to a; receivers[a] = accounts a sent gifts to."""
    raise NotImplementedError("TODO")


def stranger_share(a, accounts, receivers):
    """Share of a's distinct recipients outside a's guild. 0 if a sent nothing."""
    raise NotImplementedError("TODO")


def find_hubs(accounts, senders, receivers, k=10, s=0.5):
    """Set of accounts with fan-in >= k and stranger share >= s."""
    raise NotImplementedError("TODO")


def expand(flagged, accounts, senders, hops=1, careful=True, max_age=30):
    """Add senders of flagged accounts, `hops` times. If careful, only add senders
    with no guild and age < max_age. Return a new set; do not modify `flagged`."""
    raise NotImplementedError("TODO")


def score(flagged, accounts):
    """Return dict with tp, fp, fn, precision, recall and seized (gold held by flagged RMT
    accounts). Positives are accounts whose kind is "rmt". Precision is 0 if nothing is flagged."""
    raise NotImplementedError("TODO")


def best_rule(accounts, gifts):
    """Your recommended rule for the lab server. Return the set of flagged accounts.
    Target: precision >= 0.95 and recall >= 0.90 on lab_server(seed=10)."""
    raise NotImplementedError("TODO")


if __name__ == "__main__":
    for name, (acc, g) in [("toy", toy_server()), ("lab", lab_server(10))]:
        snd, rcv = build_index(g)
        hubs = find_hubs(acc, snd, rcv)
        for label, flagged in [("hubs", hubs),
                               ("hubs + 1 careful hop", expand(hubs, acc, snd, hops=1)),
                               ("hubs + 2 careful hops", expand(hubs, acc, snd, hops=2)),
                               ("best_rule", best_rule(acc, g))]:
            r = score(flagged, acc)
            print(f"{name:4} {label:24} TP {r['tp']:4} FP {r['fp']:4} FN {r['fn']:4} "
                  f"precision {r['precision']:.1%} recall {r['recall']:.1%} seized {r['seized']:,}")
