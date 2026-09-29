"""Tests for AU101 Lab 12. Values come from the week 12 lecture.
Run with `python3 test_raid_mix.py` (or pytest)."""
from raid_mix import (Req, allocate_flat, allocate_tiered, crowd_gain_db, expected_voices,
                      kept_share, make_raid, requests_at)

RESERVE = {"self": 4, "boss": 6, "party": 8, "others": 14}


def close(a, b, tol=0.05):
    return abs(a - b) <= tol


def test_expected_voices():
    assert close(expected_voices(1, 2, 1.5, 1.2), 1.6)
    assert close(expected_voices(20, 2, 1.5, 1.2), 32)
    assert close(expected_voices(40, 2, 1.5, 1.2), 64)


def test_crowd_gain():
    assert close(crowd_gain_db(1), 0)
    assert close(crowd_gain_db(10), 10)
    assert close(crowd_gain_db(35), 15.44)
    assert crowd_gain_db(0) == float("-inf")


def test_flat_is_first_come():
    reqs = [Req("others", 5, 0.2, "a"), Req("self", 0, 0.9, "me"), Req("boss", 20, 0.0, "b"),
            Req("party", 12, 0.5, "p")]
    assert [r.name for r in allocate_flat(reqs, 2)] == ["b", "a"]


def test_tiered_reservations():
    reqs = ([Req("others", 2 + i, 0.0, f"o{i}") for i in range(10)]
            + [Req("self", 0, 1.0, "me1"), Req("self", 0, 1.0, "me2"), Req("boss", 20, 0.0, "b1")])
    one_each = {"self": 1, "boss": 1, "party": 1, "others": 1}
    # pass 1: me1, b1, (no party), o0 ; pass 2: me2 (self first), then o1
    assert [r.name for r in allocate_tiered(reqs, 5, one_each)] == ["me1", "b1", "o0", "me2", "o1"]
    assert [r.name for r in allocate_tiered(reqs, 3, one_each)] == ["me1", "b1", "o0"]


def test_tiered_never_exceeds_budget():
    reqs = requests_at(10.0, make_raid(40))
    assert len(allocate_tiered(reqs, 32, RESERVE)) == 32
    assert len(allocate_flat(reqs, 32)) == 32


def test_simulated_demand_matches_littles_law():
    raid = make_raid(40)
    counts = [len(requests_at(i * 0.05, raid)) - 4 for i in range(100, 700)]
    predicted = expected_voices(40, 2, 1.5, 1.2)
    assert abs(sum(counts) / len(counts) - predicted) < predicted * 0.05


def test_tiers_protect_your_sounds():
    raid = make_raid(40)
    assert kept_share(raid, 32, allocate_tiered, reserve=RESERVE, seconds=15) == 1.0
    assert kept_share(raid, 32, allocate_tiered, tier="party", reserve=RESERVE, seconds=15) == 1.0


if __name__ == "__main__":
    failed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print("PASS", name)
            except Exception as e:  # noqa: BLE001
                failed += 1
                print("FAIL", name, type(e).__name__, e)
    raise SystemExit(1 if failed else 0)
