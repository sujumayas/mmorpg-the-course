"""Run: python test_zone_sim.py   (prints 'all lab 04 tests passed'; takes a few seconds)"""
from zone_sim import (handoff_rate, ghost_fraction, busiest_zone, next_owner, simulate,
                      idle_crowd, ZoneServer, Network)


def near(got, want, tol, label):
    assert abs(got - want) <= tol, f"{label}: got {got}, want {want} +- {tol}"


# the lecture's tables
near(handoff_rate(3000, 6000, 2.0, 2), 1.27, 0.005, "H at g=2")
near(handoff_rate(3000, 6000, 2.0, 4), 3.82, 0.005, "H at g=4")
near(handoff_rate(3000, 6000, 2.0, 8), 8.91, 0.005, "H at g=8")
near(handoff_rate(3000, 6000, 2.0, 1), 0.0, 1e-12, "no borders at g=1")
near(ghost_fraction(6000, 100, 4), 0.20, 1e-9, "ghosts at g=4")
near(ghost_fraction(6000, 100, 8), 0.4667, 1e-4, "ghosts at g=8")
near(busiest_zone(3000, 0.4, 2), 1650, 1e-9, "busiest g=2")
near(busiest_zone(3000, 0.4, 4), 1312.5, 1e-9, "busiest g=4")
near(handoff_rate(5000, 10000, 1.5, 5), 3.82, 0.005, "check-this-example 1")

# hysteresis
assert next_owner((0, 0), 1000.5, 10, 2000, 2, 0) == (1, 0), "h=0 hands off at the line"
assert next_owner((0, 0), 1000.5, 10, 2000, 2, 2) == (0, 0), "inside the band, keep owner"
assert next_owner((0, 0), 1001.5, 10, 2000, 2, 2) == (1, 0), "past the band, hand off"
assert next_owner((1, 0), 999.5, 10, 2000, 2, 2) == (1, 0), "band works both ways"

# the formula against the simulation (1,000 walkers, 600 s)
got = simulate(1000, 6000, 2.0, 4, seconds=600)
near(got, handoff_rate(1000, 6000, 2.0, 4), 0.12 * handoff_rate(1000, 6000, 2.0, 4),
     "simulated H within 12% of the formula")

# ping-pong (shorter runs than the lecture; loose tolerance)
h0 = idle_crowd(0, seconds=3600)
h2 = idle_crowd(2, seconds=3600)
near(h0, 1.60, 0.20, "idle crowd, no band")
near(h2, 0.39, 0.08, "idle crowd, 2 m band")

# protocol: normal handoff
a, b = ZoneServer("A"), ZoneServer("B")
net = Network(a, b)
a.spawn("p", {"hp": 100})
net.send(a.start_handoff("p", "B"))
assert net.owners("p") == [], "while in flight nobody simulates p"
net.deliver()            # HANDOFF reaches B
assert net.owners("p") == ["B"], "B owns after accepting"
net.deliver()            # ACK reaches A
assert net.owners("p") == ["B"] and "p" in a.ghosts, "A keeps a ghost"
assert a.start_handoff("p", "B") is None, "a non-owner cannot hand off"

# protocol: lost ACK never makes two owners
a, b = ZoneServer("A"), ZoneServer("B")
net = Network(a, b)
a.spawn("p", {})
net.send(a.start_handoff("p", "B"))
net.deliver()
net.queue.clear()        # the ACK is lost
assert net.owners("p") == ["B"], "lost ACK: still exactly one owner"
assert a.start_handoff("p", "B") is None, "A is still leaving and may not start again"

# protocol: a stale, duplicated HANDOFF is rejected
a, b = ZoneServer("A"), ZoneServer("B")
net = Network(a, b)
a.spawn("p", {"x": 1})
first = a.start_handoff("p", "B")
net.send(first)
net.deliver()
net.deliver()            # p now on B (seq 1)
net.send(b.start_handoff("p", "A"))
net.deliver()
net.deliver()            # p back on A (seq 2)
net.send(first)          # the network replays the old seq-1 message to B
net.deliver()
assert net.owners("p") == ["A"], "stale HANDOFF must not create a second owner"

print("all lab 04 tests passed")
