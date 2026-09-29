"""Server generators for MMO309 Lab 10. Do not edit.

Each generator returns (accounts, gifts):
  accounts: dict id -> {"kind": "honest" | "rmt", "op": None | "A" | "B",
                        "guild": int | None, "hours": float, "age": int, "gold": int}
  gifts:    list of (sender_id, receiver_id, amount), one-way transfers only
"""
import random


def toy_server():
    """The week 10 lecture's deterministic toy server (10,054 accounts)."""
    accounts, gifts = {}, []

    def add(aid, kind, guild, hours, age, gold, op=None):
        accounts[aid] = dict(kind=kind, op=op, guild=guild, hours=hours, age=age, gold=gold)

    for i in range(9600):
        add(f"p{i}", "honest", i // 48, 17 if i % 64 == 0 else 4, 400, 30_000)
    for g in range(50):
        add(f"bank{g}", "honest", g, 1, 900, 500_000)
        for m in range(20):
            gifts.append((f"p{g*48+m}", f"bank{g}", 10_000))
        for m in range(20, 30):
            target = f"p{(g*48+m+2400) % 9600}" if g == 0 else f"p{g*48+m}"
            gifts.append((f"bank{g}", target, 5_000))
    for k in range(4):
        add(f"mule{k}", "rmt", None, 8, 20, 2_000_000, "A")
    for f in range(200):
        add(f"farm{f}", "rmt", None, 20 if f < 180 else 10, 10, 5_000, "A")
        gifts.append((f"farm{f}", f"mule{f % 4}", 20_000))
    for b in range(1000):
        gifts.append((f"mule{b % 4}", f"p{(b*7) % 9600}", 50_000))
    for v in range(6):
        gifts.append((f"p{9000+v}", "mule0", 30_000))
    return accounts, gifts


def lab_server(seed=10):
    """A noisier server with two operations.

    Operation A: 5 mules, 250 farms, one layer (farm -> mule -> buyers).
    Operation B: 3 mules, 30 collectors, 240 farms, two layers
                 (farm -> collector -> mule -> buyers). Collectors pay only their mule.
                 About a fifth of its farms are bought, aged accounts (40-120 days old).
    Honest noise: 11,000 players in 220 guilds, 300 unguilded newcomers, heavy
    players, guild banks, two giveaway banks (some newcomers donate to them),
    friend gifts inside guilds, and 20 stolen accounts stripped into operation accounts.
    """
    rng = random.Random(seed)
    accounts, gifts = {}, []

    def add(aid, kind, guild, hours, age, gold, op=None):
        accounts[aid] = dict(kind=kind, op=op, guild=guild, hours=hours, age=age, gold=gold)

    n_players, gsize = 11_000, 50
    for i in range(n_players):
        heavy = rng.random() < 0.02
        add(f"p{i}", "honest", i // gsize, round(rng.uniform(16, 22) if heavy else rng.uniform(1, 9), 1),
            rng.randint(40, 3000), rng.randint(2_000, 80_000))
    # friend gifts inside guilds
    for i in range(n_players):
        for _ in range(rng.choice([0, 0, 1, 2])):
            j = (i // gsize) * gsize + rng.randrange(gsize)
            if j != i:
                gifts.append((f"p{i}", f"p{j}", rng.randint(500, 20_000)))
    # unguilded newcomers; 30 of them donate to the two giveaway banks
    for i in range(300):
        add(f"n{i}", "honest", None, round(rng.uniform(1, 6), 1), rng.randint(1, 29), rng.randint(500, 20_000))
    for i in range(30):
        gifts.append((f"n{i}", f"bank{i % 2}", rng.randint(500, 5_000)))
    # guild banks, two of them giveaway banks that pay strangers
    for g in range(60):
        add(f"bank{g}", "honest", g, 0.5, rng.randint(200, 3000), rng.randint(100_000, 900_000))
        members = rng.sample(range(g * gsize, (g + 1) * gsize), 30)
        for m in members[:rng.randint(12, 25)]:
            gifts.append((f"p{m}", f"bank{g}", rng.randint(2_000, 30_000)))
        for m in members[25:30]:
            target = rng.randrange(n_players) if g < 2 else m
            gifts.append((f"bank{g}", f"p{target}", rng.randint(1_000, 10_000)))
    # operation A
    for k in range(5):
        add(f"amule{k}", "rmt", None, rng.uniform(4, 10), rng.randint(5, 25), rng.randint(1_000_000, 3_000_000), "A")
    for f in range(250):
        add(f"afarm{f}", "rmt", None, rng.uniform(10, 23), rng.randint(1, 29), rng.randint(1_000, 9_000), "A")
        gifts.append((f"afarm{f}", f"amule{f % 5}", rng.randint(10_000, 30_000)))
    for b in range(900):
        gifts.append((f"amule{b % 5}", f"p{rng.randrange(n_players)}", rng.randint(20_000, 100_000)))
    # operation B, two layers
    for k in range(3):
        add(f"bmule{k}", "rmt", None, rng.uniform(4, 10), rng.randint(5, 25), rng.randint(2_000_000, 4_000_000), "B")
    for c in range(30):
        add(f"bcoll{c}", "rmt", None, rng.uniform(2, 6), rng.randint(3, 25), rng.randint(100_000, 300_000), "B")
        gifts.append((f"bcoll{c}", f"bmule{c % 3}", rng.randint(100_000, 300_000)))
    for f in range(240):
        age = rng.randint(40, 120) if rng.random() < 0.2 else rng.randint(1, 29)
        add(f"bfarm{f}", "rmt", None, rng.uniform(10, 23), age, rng.randint(1_000, 9_000), "B")
        gifts.append((f"bfarm{f}", f"bcoll{f % 30}", rng.randint(10_000, 30_000)))
    for b in range(600):
        buyer = f"n{rng.randrange(300)}" if rng.random() < 0.1 else f"p{rng.randrange(n_players)}"
        gifts.append((f"bmule{b % 3}", buyer, rng.randint(20_000, 100_000)))
    # stolen honest accounts stripped into operation accounts
    victims = rng.sample(range(n_players), 20)
    for n, v in enumerate(victims):
        target = f"amule{n % 5}" if n < 10 else f"bcoll{n % 30}"
        gifts.append((f"p{v}", target, rng.randint(10_000, 60_000)))
    return accounts, gifts
