"""Run: python test_mesh.py   (prints 'all lab 09 tests passed')"""
from mesh import (tick_ms, capacity, servers_for, ghost_updates, spread_tick_ms,
                  spread_capacity, AuthorityTable, pause_scenario)


def near(got, want, tol, label):
    assert abs(got - want) <= tol, f"{label}: got {got}, want {want}"


for k, want in [(1, 153.2), (2, 217.7), (4, 308.3), (16, 612.8), (64, 1198.7), (256, 2283.1)]:
    near(capacity(k), want, 0.05, f"capacity({k})")
    near(tick_ms(capacity(k), k), 50.0, 1e-6, f"capacity({k}) fills the budget")
for k, want in [(1, 2020.0), (4, 508.0), (16, 130.0), (64, 35.5)]:
    near(tick_ms(1000, k), want, 0.05, f"tick_ms(1000, {k})")
near(tick_ms(600, 16), 48.0, 1e-9, "check-this-example 1")
near(tick_ms(800, 32), 43.6, 1e-9, "check-yourself 2")
assert servers_for(153) == 1 and servers_for(1000) == 44 and servers_for(2000) == 192
assert servers_for(900) == 36
assert servers_for(20_000) is None
assert ghost_updates(1000, 1) == 0 and ghost_updates(800, 32) == 24_800
near(spread_tick_ms(625, 1), 50.0, 1e-9, "spread k=1")
for k, want in [(1, 625.0), (4, 2488.0), (16, 9952.0)]:
    near(spread_capacity(k), want, 0.02, f"spread_capacity({k})")
assert spread_capacity(16) > 15 * capacity(16), "spread must scale far better than crowd"

t = AuthorityTable()
assert t.owner(5) is None and t.state(5) is None
assert t.grant(5, "A") == 1
assert t.write(5, "A", 1, "s1") is True and t.state(5) == "s1"
assert t.write(5, "B", 1, "bad") is False, "non-owner write must be rejected"
assert t.grant(5, "B") == 2 and t.state(5) == "s1", "grant keeps state"
assert t.write(5, "A", 1, "stale") is False, "old epoch must be rejected"
assert t.write(5, "B", 1, "wrong epoch") is False, "owner with the wrong epoch is rejected"
assert t.write(5, "B", 2, "s2") is True and t.state(5) == "s2" and t.owner(5) == "B"
assert len(t.log) == 5, "one log line per write"
t, late = pause_scenario()
assert late is False and t.state(12) == {"hp": 80} and t.owner(12) == "B"
print("all lab 09 tests passed")
