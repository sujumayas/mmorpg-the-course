"""Lab 14 tests. Run with `python test_harness.py` or `pytest test_harness.py`.
Every test fails on the starter and passes on a correct harness.py."""
import os

from harness import (DEAD_END, available, dead_ends, explore, load_story,
                     outcome_probabilities, random_playthroughs, runs_needed,
                     speaker_violations, unreachable_nodes)

HERE = os.path.dirname(os.path.abspath(__file__))
STORY = load_story(os.path.join(HERE, "lantern.json"))


def close(a, b, tol=1e-12):
    return abs(a - b) <= tol


def test_available_respects_requires_and_forbids():
    story = {"nodes": {"a": {"speaker": None, "ending": False, "choices": [
        {"text": "x", "to": "a"},
        {"text": "y", "to": "a", "requires": ["k"]},
        {"text": "z", "to": "a", "forbids": ["k"]},
    ]}}}
    assert [c["text"] for c in available(story, "a", frozenset())] == ["x", "z"]
    assert [c["text"] for c in available(story, "a", frozenset({"k"}))] == ["x", "y"]


def test_explore_counts_states_not_nodes():
    states = explore(STORY)
    assert len(states) == 32
    assert ("dock", frozenset()) in states
    assert ("lamp", frozenset({"asked", "oil", "trusted"})) in states


def test_finds_the_planted_bugs():
    states = explore(STORY)
    assert unreachable_nodes(STORY, states) == ["ending_rescue"]
    assert dead_ends(STORY, states) == [("cellar", ("asked", "keeper_dead"))]
    assert speaker_violations(STORY, states) == [("gallery", ("keeper_dead", "rope"))]


def test_outcome_probabilities_exact():
    p = outcome_probabilities(STORY)
    assert set(p) == {"ending_dark", "ending_lit", DEAD_END}
    assert close(p[DEAD_END], 1 / 8)
    assert close(p["ending_lit"], 5 / 64)
    assert close(p["ending_dark"], 51 / 64)


def test_random_playthroughs_match_exact_rates():
    runs = 4000
    counts = random_playthroughs(STORY, runs, seed=7)
    assert sum(counts.values()) == runs
    exact = outcome_probabilities(STORY)
    assert set(counts) <= set(exact)
    for outcome, p in exact.items():
        assert abs(counts[outcome] / runs - p) < 0.03, outcome
    assert random_playthroughs(STORY, runs, seed=7) == counts  # same seed, same result
    assert sum(random_playthroughs(STORY, 0, seed=1).values()) == 0


def test_runs_needed_lecture_values():
    assert runs_needed(0.5) == 5
    assert runs_needed(1 / 81) == 242
    assert runs_needed(1 / 729) == 2183
    assert runs_needed(5 / 64) == 37


if __name__ == "__main__":
    import sys
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS {name}")
            except Exception as e:  # NotImplementedError counts as a failure
                failed += 1
                print(f"FAIL {name}: {type(e).__name__} {e}")
    sys.exit(1 if failed else 0)
