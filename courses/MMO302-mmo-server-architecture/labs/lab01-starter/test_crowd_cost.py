"""Run: python test_crowd_cost.py   (prints 'all lab 01 tests passed')"""
from crowd_cost import deliveries, layout, per_server, c_max, tick_ms, scenario


def check(got, want, label):
    assert got == want, f"{label}: got {got}, want {want}"


check(deliveries([25] * 400, 5), 1_200_000, "baseline world")
check(deliveries([1000], 5), 4_995_000, "one crowd of 1,000")
check(deliveries([1, 1, 1], 5), 0, "players alone deliver nothing")
check(sum(layout(10_000, 1000)), 10_000, "layout keeps every player")
check(layout(10_000, 1000)[1:3], [23, 23], "remainder goes to low zones")
check(layout(10_000, 1000)[-1], 22, "last zone gets no extra")
players, dels = per_server(layout(10_000, 25), 5)
check((players[0], dels[0]), (500, 60_000), "baseline server")
for c, row in {250: (714, 489, 365_610, 57_360, 1_454_250),
               500: (953, 477, 1_299_250, 54_510, 2_331_260),
               1000: (1429, 452, 5_041_310, 48_840, 5_965_530),
               2670: (3019, 368, 35_661_480, 32_040, 36_268_260)}.items():
    s = scenario(10_000, c, 5)
    check((s["p0"], s["p1"], s["d0"], s["d1"], s["world"]), row, f"lecture row c={c}")
check(c_max(1_000_000, 5), 447, "c_max B=1e6 u=5")
check(c_max(2_000_000, 5), 632, "c_max B=2e6 u=5")
check(c_max(1_000_000, 1), 1000, "c_max B=1e6 u=1")
check(c_max(1_000_000, 0.1), 3162, "c_max B=1e6 u=0.1")
assert abs(tick_ms(500, 60_000) - 33.0) < 1e-9, "baseline tick 33.0 ms"
assert abs(tick_ms(1429, 5_041_310) - 577.581) < 1e-6, "crowd tick 577.6 ms"
print("all lab 01 tests passed")
