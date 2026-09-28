"""Run: python test_layers.py   (prints 'all lab 02 tests passed')"""
from collections import Counter
from layers import make_population, assign_random, assign_guild, cohesion

order, guild_of = make_population()
assert len(order) == 3000 and sorted(order) == list(range(3000)), "population"

tiny_guilds = [0, 0, 1, 1, None]
assert cohesion({0: 0, 1: 0, 2: 1, 3: 2, 4: 0}, tiny_guilds) == 0.5, "cohesion counts pairs"

r = assign_random(order, guild_of, 20, 180)
g = assign_guild(order, guild_of, 20, 180)
for name, lay in (("random", r), ("guild", g)):
    assert len(lay) == 3000, f"{name}: every player placed"
    assert max(Counter(lay.values()).values()) <= 180, f"{name}: cap respected"

lr, lg = Counter(r.values()), Counter(g.values())
assert (max(lr.values()), min(lr.values())) == (172, 131), f"random loads {max(lr.values())}/{min(lr.values())}"
assert (max(lg.values()), min(lg.values())) == (159, 149), f"guild loads {max(lg.values())}/{min(lg.values())}"
assert round(cohesion(r, guild_of), 3) == 0.049, f"random cohesion {cohesion(r, guild_of):.4f}"
assert cohesion(g, guild_of) == 1.0, f"guild cohesion {cohesion(g, guild_of):.4f}"
assert round(cohesion(assign_guild(order, guild_of, 20, 150), guild_of), 3) == 0.978, "tight cap splits some guilds"
print("all lab 02 tests passed")
