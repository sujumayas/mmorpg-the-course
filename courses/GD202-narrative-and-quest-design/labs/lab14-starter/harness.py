"""GD202 Lab 14: a narrative test harness.

Run:   python harness.py lantern.json
Tests: python test_harness.py   (or pytest test_harness.py)

A story is a graph of nodes. A choice is available in a state when every flag in
its "requires" list is set and no flag in its "forbids" list is set. Taking a
choice moves to "to" and adds the flags in "sets". Missing lists mean empty.
A state is (node_id, frozenset_of_flags). The story starts at story["start"]
with no flags. Stories in this lab have no cycles.
"""
import json
import math
import random
import sys
from collections import Counter

DEAD_END = "(dead end)"


def load_story(path):
    with open(path) as f:
        return json.load(f)


def available(story, node, flags):
    """List of the choice dicts at `node` that are open in the flag set `flags`."""
    raise NotImplementedError("available")


def explore(story):
    """Set of every reachable (node, frozenset(flags)) state. Use breadth-first search."""
    raise NotImplementedError("explore")


def unreachable_nodes(story, states):
    """Sorted list of node ids that appear in no reachable state."""
    raise NotImplementedError("unreachable_nodes")


def dead_ends(story, states):
    """Sorted list of (node, tuple(sorted(flags))) for reachable states that are
    not endings and have no available choice."""
    raise NotImplementedError("dead_ends")


def speaker_violations(story, states):
    """Sorted list of (node, tuple(sorted(flags))) where the node's speaker is
    dead. story["dead_flags"] maps a speaker name to the flag that means they
    are dead."""
    raise NotImplementedError("speaker_violations")


def outcome_probabilities(story):
    """Exact chance of each outcome for a bot that picks uniformly among the
    available choices at every step. Keys are ending node ids, plus DEAD_END
    for runs that get stuck. Values sum to 1. Omit outcomes with chance 0."""
    raise NotImplementedError("outcome_probabilities")


def random_playthroughs(story, runs, seed):
    """Play `runs` random playthroughs with random.Random(seed), picking
    uniformly among available choices. Return a Counter of outcomes
    (ending id, or DEAD_END)."""
    raise NotImplementedError("random_playthroughs")


def runs_needed(q, confidence=0.95):
    """Smallest N with 1 - (1 - q)**N >= confidence. Use the log formula and
    math.ceil, as in the lecture."""
    raise NotImplementedError("runs_needed")


def report(story):
    states = explore(story)
    print(f"{story.get('title', 'story')}: {len(story['nodes'])} nodes, "
          f"{len(states)} reachable states")
    print("unreachable nodes:", unreachable_nodes(story, states) or "none")
    print("dead ends:", dead_ends(story, states) or "none")
    print("dead speakers:", speaker_violations(story, states) or "none")
    for outcome, p in sorted(outcome_probabilities(story).items()):
        print(f"  {outcome:16s} p = {p:.4f}  runs for 95%: {runs_needed(p)}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "lantern.json"
    try:
        report(load_story(path))
    except NotImplementedError as e:
        print(f"TODO: implement {e} in harness.py")
