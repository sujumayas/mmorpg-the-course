"""Tests for Lab 02. Values come from the week 2 lecture.
Run with ../../../../.venv/bin/python test_zone.py (or pytest)."""
from zone import (hub_seen, hub_seen_skipping, level_minutes, load_xp_table, quests_needed,
                  zone_demand)

T = load_xp_table()
HUBS = [10, 10, 10]


def close_list(a, b, tol=1e-9):
    return len(a) == len(b) and all(abs(x - y) < tol for x, y in zip(a, b))


def test_demand():
    assert zone_demand(T, 10, 15) == 12000
    assert zone_demand(T, 20, 24) == 17800
    try:
        zone_demand(T, 20, 30)
    except KeyError:
        pass
    else:
        raise AssertionError("expected KeyError for a missing level")


def test_quests_needed():
    assert abs(quests_needed(12000, 400, 0.25, 0) - 24.0) < 1e-9
    assert abs(quests_needed(12000, 400, 0.5, 0) - 20.0) < 1e-9
    assert abs(quests_needed(12000, 400, 0.25, 0.2) - 19.2) < 1e-9
    assert abs(quests_needed(12000, 400, 0.25, 0.5) - 12.0) < 1e-9


def test_hub_seen():
    assert close_list(hub_seen(24, HUBS), [1.0, 1.0, 0.4])
    assert close_list(hub_seen(19.2, HUBS), [1.0, 0.92, 0.0])
    assert close_list(hub_seen(12, HUBS), [1.0, 0.2, 0.0])
    assert close_list(hub_seen(40, HUBS), [1.0, 1.0, 1.0])
    assert close_list(hub_seen(15.0, [10, 8, 8]), [1.0, 0.625, 0.0])


def test_skipping():
    walked, played = hub_seen_skipping(24, HUBS, 0.8)
    assert close_list(walked, [1.0, 1.0, 1.0])
    assert close_list(played, [0.8, 0.8, 0.8])
    walked, played = hub_seen_skipping(12, HUBS, 0.5)
    assert close_list(walked, [1.0, 1.0, 0.4])
    assert close_list(played, [0.5, 0.5, 0.2])


def test_level_minutes():
    m = level_minutes(T, 10, 15, 400, 0.25, 6)
    assert sorted(m) == [10, 11, 12, 13, 14]
    assert abs(m[10] - 24.0) < 1e-9 and abs(m[14] - 33.6) < 1e-9
    assert abs(sum(m.values()) - 144.0) < 1e-9


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print("PASS", name)
            except Exception as e:  # noqa: BLE001
                failed += 1
                print("FAIL", name, type(e).__name__, e)
    raise SystemExit(1 if failed else 0)
