"""AU101 Lab 12 starter: forty players, one voice budget.

Standard library only. Run the tests with

    python3 test_raid_mix.py

Functions marked TODO raise NotImplementedError until you write them.
Times are in seconds. A "voice" is one playing sound instance.
"""
import random
from dataclasses import dataclass

TIERS = ["self", "boss", "party", "others"]   # highest importance first


# ---------------------------------------------------------------- TODO part A
def expected_voices(players, sounds_per_action, action_interval, duration):
    """Average number of voices playing at once (Little's law).

    rate per player = sounds_per_action / action_interval   (sounds per second)
    voices          = players * rate * duration
    """
    raise NotImplementedError("expected_voices")


def crowd_gain_db(n_active):
    """Level of n equal, uncorrelated sounds relative to one of them:
    10 * log10(n). Return float('-inf') for n <= 0."""
    raise NotImplementedError("crowd_gain_db")


# ---------------------------------------------------------------- TODO part B
@dataclass
class Req:
    tier: str        # one of TIERS
    distance: float  # metres from the listener
    start: float     # when the sound started (s); smaller = older
    name: str = ""


def allocate_flat(reqs, budget):
    """No tiers, every sound equal: first come, first served. Keep the
    `budget` oldest requests (smallest start; ties keep input order), which is
    week 10's "discard newest" rule. Return the kept requests."""
    raise NotImplementedError("allocate_flat")


def allocate_tiered(reqs, budget, reserve):
    """Tiers with reservations.

    Pass 1: each tier, in TIERS order, keeps up to reserve[tier] of its own
            requests, nearest first.
    Pass 2: any slots still free go to the requests not yet kept, in TIERS
            order and nearest first within a tier, until the budget is used.
    The total kept never exceeds budget. Return the kept requests in the
    order they were chosen.
    """
    raise NotImplementedError("allocate_tiered")


# ---------------------------------------------------------------- simulation (done)
def make_raid(n_players, party_size=5, seed=1):
    """Player 0 is you. Players 1..party_size-1 are your party. The rest are
    'others'. Each gets a distance (m) and a random phase within the GCD."""
    rng = random.Random(seed)
    raid = []
    for i in range(n_players):
        tier = "self" if i == 0 else ("party" if i < party_size else "others")
        dist = 0.0 if i == 0 else rng.uniform(3, 40)
        raid.append((tier, dist, rng.uniform(0, 1.5)))
    return raid


def requests_at(t, raid, gcd=1.5, duration=1.2, sounds_per_action=2,
                boss_voices=4):
    """All requests alive at time t. Each player acts every gcd seconds from
    their phase and each action starts `sounds_per_action` sounds of
    `duration` seconds. The boss always wants `boss_voices` voices."""
    reqs = [Req("boss", 20.0, 0.0, f"boss{k}") for k in range(boss_voices)]
    for i, (tier, dist, phase) in enumerate(raid):
        k = int((t - phase) // gcd)
        while k >= 0 and t - (phase + k * gcd) < duration:
            start = phase + k * gcd
            reqs.extend(Req(tier, dist, start, f"p{i}a{k}s{j}") for j in range(sounds_per_action))
            k -= 1
    return reqs


def kept_share(raid, budget, allocator, tier="self", seconds=30, dt=0.05, **kw):
    """Fraction of `tier` requests that got a voice, over the whole run."""
    want = got = 0
    for i in range(int(seconds / dt)):
        reqs = requests_at(i * dt, raid)
        kept = allocator(reqs, budget, **kw)
        want += sum(r.tier == tier for r in reqs)
        got += sum(r.tier == tier for r in kept)
    return got / want if want else 1.0


if __name__ == "__main__":
    try:
        for n in (1, 5, 10, 20, 40, 100):
            print(f"{n:3d} players -> {expected_voices(n, 2, 1.5, 1.2):6.1f} voices on average")
        raid = make_raid(40)
        reserve = {"self": 4, "boss": 6, "party": 8, "others": 14}
        print("your sounds kept, flat  :", round(kept_share(raid, 32, allocate_flat), 2))
        print("your sounds kept, tiered:", round(kept_share(raid, 32, allocate_tiered,
                                                            reserve=reserve), 2))
    except NotImplementedError as e:
        print("Not written yet:", e)
