"""Run with:  python test_fleet.py   (or pytest)."""
import math

import fleet
import policy

CAP = fleet.CAP


def ideal_server_hours(demand):
    """Every minute, exactly enough servers at 100% fill. Nobody can beat this."""
    return sum(math.ceil(d / CAP) for d in demand) / 60


def test_evening_has_no_queue():
    r = fleet.run(fleet.evening_trace(), policy.Policy())
    assert r.peak_queue == 0, f"evening peak queue {r.peak_queue}"


def test_launch_queue_is_bounded():
    r = fleet.run(fleet.launch_trace(), policy.Policy())
    assert r.queue_player_minutes <= 80_000, f"queue player-minutes {r.queue_player_minutes}"
    assert r.server_hours <= 400, f"server-hours {r.server_hours:.1f} (headroom too expensive)"


def test_daily_cost_and_queue():
    demand = fleet.daily_trace()
    r = fleet.run(demand, policy.Policy())
    assert r.peak_queue == 0, f"daily peak queue {r.peak_queue}"
    limit = 1.35 * ideal_server_hours(demand)
    assert r.server_hours <= limit, f"server-hours {r.server_hours:.1f} > {limit:.1f}"


if __name__ == "__main__":
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print("PASS", name)
            except (AssertionError, fleet.PlayersKicked) as e:
                failed += 1
                print("FAIL", name, "-", e)
    raise SystemExit(1 if failed else 0)
