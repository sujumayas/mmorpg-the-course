"""GD201 Lab 01: retry cost and checkpoint placement.

A level is a list of challenges in the order the player meets them. Each challenge is a dict:
    walk  seconds to walk from the previous challenge (or the level start) to this one
    t     seconds for one attempt at the challenge (success or failure)
    p     chance of success per attempt, 0 < p <= 1

A checkpoint list holds the indices of challenges that have a checkpoint just before them.
Index 0 is always a checkpoint (the level start). When the player fails a challenge, they wait
`respawn` seconds and restart at the most recent checkpoint. See lecture week 1, section 2.

Run `python retry.py` to print a report for the sample level.
"""
from itertools import combinations

SAMPLE_LEVEL = [
    {"name": "dock grapple",   "walk": 5,  "t": 6,  "p": 0.4},
    {"name": "wheel jump",     "walk": 10, "t": 8,  "p": 0.7},
    {"name": "sluice swing",   "walk": 8,  "t": 10, "p": 0.3},
    {"name": "gear gap",       "walk": 12, "t": 7,  "p": 0.6},
    {"name": "rooftop run",    "walk": 6,  "t": 15, "p": 0.5},
    {"name": "bell climb",     "walk": 9,  "t": 12, "p": 0.8},
]


def expected_time(t, p, r):
    """Expected seconds to clear one challenge: (t + r(1 - p)) / p."""
    # TODO: lecture week 1, section 2, 'The model'.
    raise NotImplementedError("expected_time")

def penalty_ratio(t, p, r):
    """expected_time with recovery r divided by expected_time with r = 0."""
    # TODO: divide expected_time by the r = 0 case, or use the closed form.
    raise NotImplementedError("penalty_ratio")

def segment_time(costs, probs, respawn):
    """Expected seconds to clear challenges in a row, restarting the whole segment on any failure.

    costs[i] is the time to reach and attempt challenge i within one run.
    """
    # TODO: track the chance of reaching each challenge (see the lecture's code block).
    raise NotImplementedError("segment_time")

def level_time(level, checkpoints, respawn):
    """Expected seconds to finish the level.

    The walk to the first challenge of each segment is paid once. Inside a segment, every
    later challenge costs walk + t per run; the first costs only t.
    """
    # TODO: split the level at the checkpoints and add up segment_time for each segment.
    raise NotImplementedError("level_time")

def best_checkpoints(level, k, respawn):
    """The list of k checkpoint indices (always including 0) with the lowest level_time.

    Break ties by choosing the list that sorts first.
    """
    # TODO: try every choice of k - 1 extra indices with itertools.combinations.
    raise NotImplementedError("best_checkpoints")

def report():
    print(f"expected_time(8, 0.2, 52) = {expected_time(8, 0.2, 52):.1f} s")
    for cps in ([0], [0, 2], [0, 2, 4], list(range(len(SAMPLE_LEVEL)))):
        print(f"checkpoints {cps}: {level_time(SAMPLE_LEVEL, cps, 2):.1f} s")
    for k in (2, 3):
        cps = best_checkpoints(SAMPLE_LEVEL, k, 2)
        print(f"best {k} checkpoints: {cps} -> {level_time(SAMPLE_LEVEL, cps, 2):.1f} s")


if __name__ == "__main__":
    try:
        report()
    except NotImplementedError as e:
        print(f"Not implemented yet: {e}(). Fill in the TODOs, then run check_lab01.py.")
