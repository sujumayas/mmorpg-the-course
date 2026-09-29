"""MMO307 Lab 10: matchmaking quality vs queue time.

Part A is the closed-form model from the week 10 lecture. Part B is a
second-by-second simulation of a real queue, where waiting players can match
each other and every player's search window widens while they wait.

    python3 queue_model.py            # prints the part A table and a part B run
    python3 test_queue_model.py       # runs the tests

Standard library only.
"""
import math
import random

MU, SIGMA = 1500.0, 200.0   # rating population: mean and standard deviation
LAM = 12.0                  # players entering the queue per minute


def phi(z):
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def favourite_score(gap):
    """Elo expected score of the stronger player when ratings differ by `gap`."""
    return 1.0 / (1.0 + 10.0 ** (-abs(gap) / 400.0))


# ---------------------------------------------------------------- Part A

def share_in_window(r, w, mu=MU, sigma=SIGMA):
    """Fraction of arriving players whose rating lies in [r - w, r + w]."""
    # TODO: implement (see lab sheet).
    raise NotImplementedError("share_in_window")


def mean_wait(r, w, lam=LAM, mu=MU, sigma=SIGMA):
    """Mean wait in seconds for a player at rating r with a fixed window w,
    counting only newly arriving opponents (lecture section 2)."""
    # TODO: implement (see lab sheet).
    raise NotImplementedError("mean_wait")


def mean_favourite_score(r, w, mu=MU, sigma=SIGMA, steps=2000):
    """Average favourite_score over the opponents a player at r accepts with
    window w. Opponents are weighted by the normal density (midpoint rule)."""
    # TODO: implement (see lab sheet).
    raise NotImplementedError("mean_favourite_score")


# ---------------------------------------------------------------- Part B

def window(waited, w0, growth, w_max):
    """Search window after `waited` seconds in queue."""
    return min(w0 + growth * waited, w_max)


def match_pool(pool, now, w0, growth, w_max):
    """One matchmaking pass.

    pool: list of (rating, join_time) for players still waiting.
    Returns (matches, remaining). Each match is (gap, wait_a, wait_b).

    Rule: sort the pool by rating and walk it from the lowest rating up.
    Pair a player with the next player in sorted order when their rating gap
    is at most the smaller of the two players' current windows. A paired
    player leaves the pool; an unpaired player stays for the next second.
    """
    # TODO: implement (see lab sheet).
    raise NotImplementedError("match_pool")


def simulate_queue(seconds=3600, lam=LAM, w0=25.0, growth=5.0, w_max=400.0,
                   seed=1, mu=MU, sigma=SIGMA):
    """Run the queue for `seconds`. Returns a list of matches
    (gap, wait_a, wait_b)."""
    rng = random.Random(seed)
    pool, out = [], []
    rate = lam / 60.0
    for now in range(seconds):
        # Poisson arrivals in one second, by counting exponential gaps.
        t = rng.expovariate(rate)
        while t < 1.0:
            pool.append((rng.gauss(mu, sigma), now))
            t += rng.expovariate(rate)
        matches, pool = match_pool(pool, now, w0, growth, w_max)
        for gap, wa, wb in matches:
            out.append((gap, wa, wb))
    return out


def summarise(matches):
    """Mean wait (s), mean gap and mean favourite score over all matches."""
    waits = [w for _, wa, wb in matches for w in (wa, wb)]
    gaps = [g for g, _, _ in matches]
    return (sum(waits) / len(waits), sum(gaps) / len(gaps),
            sum(favourite_score(g) for g in gaps) / len(gaps))


def main():
    print("Part A: fixed window, arrivals only")
    for r in (1500, 1900, 2100):
        for w in (50, 100, 200):
            try:
                print(f"  r={r} w={w:3d}  wait {mean_wait(r, w):7.1f} s  "
                      f"favourite {mean_favourite_score(r, w):.3f}")
            except NotImplementedError as e:
                print("  TODO:", e)
                break
    print("Part B: simulated pool, window 25 + 5 per second, cap 400")
    try:
        m = simulate_queue()
        wait, gap, fav = summarise(m)
        print(f"  {len(m)} matches, mean wait {wait:.1f} s, mean gap {gap:.1f}, "
              f"favourite {fav:.3f}")
    except NotImplementedError as e:
        print("  TODO:", e)


if __name__ == "__main__":
    main()
