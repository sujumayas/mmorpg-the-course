"""MMO401 Lab 09 starter: two regional markets joined by a hauling route.

Standard library only. Run:  python3 lab09-starter.py

Region A is the hub (cheap to produce), region B is the frontier. Each region has a linear
market that clears every day given how many units haulers moved from A to B:

    A: demand 100 - P, supply P,      so excess supply in A at price P is 2P - 100
    B: demand 100 - P, supply P - 40, so excess demand in B at price P is 140 - 2P

With no hauling, P_A = 50 and P_B = 70. The lecture's analytic answer with a per-unit
transport cost tau (0 <= tau <= 20) is P_A = 60 - tau/2, P_B = P_A + tau, flow F = 20 - tau.

Your job is the hauler agents (TODO below).
"""
import csv
import random
from dataclasses import dataclass


def clear_region_a(exports):
    """Price in A when `exports` units per day leave A: 2P - 100 = exports."""
    return (100 + exports) / 2


def clear_region_b(imports):
    """Price in B when `imports` units per day arrive: 140 - 2P = imports."""
    return (140 - imports) / 2


@dataclass
class Route:
    trip_hours: float = 0.5      # hours for one round trip
    capacity: int = 200          # units per trip
    loss_chance: float = 0.0     # chance the whole cargo is lost on a trip
    toll: float = 0.0            # gold per unit, paid on arrival
    wage: float = 600.0          # gold per hour a hauler could earn elsewhere

    def tau(self, price_a):
        """Per-unit transport cost used in the lecture: time cost + toll + expected loss.
        Expected loss is charged on the purchase price in A."""
        return self.wage * self.trip_hours / self.capacity + self.toll + self.loss_chance * price_a


@dataclass
class Hauler:
    name: str
    active: bool = False
    profit: float = 0.0


# ---------------------------------------------------------------- TODO
def decide(hauler, route, price_a, price_b, rng):
    """TODO: return True if this hauler runs a trip today.

    Rule to implement (entry and exit, using yesterday's prices):
    - profitable = price_b * (1 - loss_chance) - price_a - toll > wage * trip_hours / capacity
    - an inactive hauler starts hauling with probability 0.05 per day while the route is profitable;
    - an active hauler stops with probability 0.05 per day while it is not profitable;
    - otherwise the hauler keeps its current state (hauler.active).
    Slow entry and exit stop the whole fleet from switching at once and overshooting.
    """
    raise NotImplementedError


def run_trip(hauler, route, price_a, price_b, rng):
    """TODO: carry `capacity` units bought at price_a. With probability loss_chance the cargo
    is lost (return 0 units delivered and record the loss). Otherwise return capacity units
    delivered and add the margin (price_b - price_a - toll) * capacity minus the time cost
    wage * trip_hours to hauler.profit.
    Return the number of units delivered to B.
    """
    raise NotImplementedError


# ---------------------------------------------------------------- simulation
def simulate(route, n_haulers=120, days=600, trips_per_day_scale=0.0025, seed=409):
    """Each day: haulers decide using yesterday's prices, deliveries are summed, both markets
    clear. `trips_per_day_scale` converts units carried into the lecture's units of daily flow
    (a 200-unit trip adds 0.5 to F with the default), so 120 haulers can move up to F = 60.
    Prices are smoothed (half old, half new) so the system does not oscillate.
    """
    rng = random.Random(seed)
    haulers = [Hauler(f"h{i}") for i in range(n_haulers)]
    pa, pb = 50.0, 70.0
    rows = []
    for day in range(days):
        delivered = 0.0
        shipped = 0.0
        for h in haulers:
            h.active = decide(h, route, pa, pb, rng)
            if h.active:
                shipped += route.capacity * trips_per_day_scale
                delivered += run_trip(h, route, pa, pb, rng) * trips_per_day_scale
        pa = 0.5 * pa + 0.5 * clear_region_a(shipped)
        pb = 0.5 * pb + 0.5 * clear_region_b(delivered)
        rows.append({"day": day, "p_a": pa, "p_b": pb, "shipped": shipped, "delivered": delivered,
                     "active": sum(h.active for h in haulers)})
    return rows


def analytic(tau):
    tau = min(max(tau, 0.0), 20.0)
    pa = 60 - tau / 2
    return {"tau": tau, "p_a": pa, "p_b": pa + tau, "flow": 20 - tau, "gains": (20 - tau) ** 2 / 2}


def lecture_tau(route):
    """Solve tau = t0 + loss * P_A with P_A = 60 - tau/2 (the lecture's closed form)."""
    t0 = route.wage * route.trip_hours / route.capacity + route.toll
    return (t0 + 60 * route.loss_chance) / (1 + route.loss_chance / 2)


def write_csv(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    scenarios = {
        "highway": Route(),
        "long": Route(trip_hours=2.0),
        "danger": Route(loss_chance=0.10),
        "long_danger": Route(trip_hours=2.0, loss_chance=0.10),
    }
    for name, r in scenarios.items():
        a = analytic(lecture_tau(r))
        print(f"{name:12s} analytic: tau={a['tau']:.2f}  P_A={a['p_a']:.2f}  P_B={a['p_b']:.2f}  F={a['flow']:.2f}")
    try:
        for name, r in scenarios.items():
            rows = simulate(r)
            write_csv(rows, f"lab09-{name}.csv")
            last = rows[-200:]
            pa = sum(x["p_a"] for x in last) / len(last)
            pb = sum(x["p_b"] for x in last) / len(last)
            print(f"{name:12s} simulated (mean of last 200 days): P_A={pa:.2f}  P_B={pb:.2f}  gap={pb - pa:.2f}")
    except NotImplementedError:
        print("Simulation: not run yet (implement decide and run_trip).")
