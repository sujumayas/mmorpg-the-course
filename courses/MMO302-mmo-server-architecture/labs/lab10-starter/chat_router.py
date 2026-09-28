"""MMO302 lab 10 starter: a chat router that counts its own fan-out.

Standard library only. Run the self-check with:
    python chat_router.py
Run the tests with:
    python -m unittest test_chat_router.py

Fill in every function marked TODO. Do not change the function signatures:
the tests call them exactly as written.
"""
import random
import zlib
from collections import defaultdict


class TokenBucket:
    """Rate limiter. Holds up to `capacity` tokens and refills `rate` tokens per second.

    allow(now) refills the bucket for the time since the last call, then spends one
    token and returns True if at least one token is available, else returns False.
    The bucket starts full, and the first call happens at time `now >= 0`.
    """

    def __init__(self, capacity, rate):
        self.capacity = capacity
        self.rate = rate
        self.tokens = capacity
        self.last = 0.0

    def allow(self, now):
        # TODO: refill (never above capacity), then spend a token if you can.
        raise NotImplementedError("TokenBucket.allow")


class Router:
    """Routes chat messages from a sender to every other member of a channel.

    Keeps counters so you can measure the load the lecture predicts:
      self.accepted    messages that passed the rate limit
      self.dropped     messages the rate limit rejected
      self.deliveries  copies sent to receivers (the sender does not get a copy)
    """

    def __init__(self, burst=3, refill_per_s=0.2):
        self.members = defaultdict(set)      # channel name -> set of member ids
        self.buckets = {}                    # member id -> TokenBucket
        self.burst = burst
        self.refill_per_s = refill_per_s
        self.accepted = 0
        self.dropped = 0
        self.deliveries = 0

    def subscribe(self, member, channel):
        self.members[channel].add(member)

    def unsubscribe(self, member, channel):
        self.members[channel].discard(member)

    def publish(self, sender, channel, now):
        """Return the number of copies delivered (0 if the sender was rate limited).

        Rules:
          1. Each sender has one TokenBucket (create it on first use with
             self.burst and self.refill_per_s). A rejected message counts in
             self.dropped and delivers nothing.
          2. An accepted message counts in self.accepted and is delivered to every
             member of the channel except the sender.
          3. A sender who is not a member of the channel cannot post: return 0 and
             change no counters.
        """
        # TODO
        raise NotImplementedError("Router.publish")


def shard_name(channel, member, k):
    """Name of the sub-channel `member` joins when `channel` is split k ways.

    Use a stable hash so the same member always lands in the same sub-channel,
    even after a server restart: zlib.crc32(member.encode()) % k.
    Return f"{channel}#{index}". With k == 1 return the channel name unchanged.
    """
    # TODO
    raise NotImplementedError("shard_name")


def simulate(listeners, posts_per_listener_per_s, seconds, k=1, seed=1, limit=True):
    """Simulate one busy channel and return (deliveries per second, dropped share).

    - Members are "p0" .. f"p{listeners-1}", each subscribed to
      shard_name("trade", member, k).
    - Each member posts as a Poisson process: draw gaps with
      rng.expovariate(posts_per_listener_per_s) from rng = random.Random(seed).
      Generate every member's post times first, then publish them all in time order.
    - If limit is False, give the router a huge burst (10**9) so nothing is dropped.
    """
    # TODO
    raise NotImplementedError("simulate")


def predicted_deliveries(listeners, posts_per_listener_per_s, k=1):
    """The lecture's model: q * L * (L/k - 1), members spread evenly over k channels."""
    return posts_per_listener_per_s * listeners * (listeners / k - 1)


if __name__ == "__main__":
    q = 0.05 / 60
    for L in [400, 1000, 3000]:
        try:
            got, _ = simulate(L, q, seconds=600, limit=False)
        except NotImplementedError as e:
            print(f"L={L}: not run yet ({e})")
            continue
        print(f"L={L:>5}: simulated {got:10.1f}/s   model {predicted_deliveries(L, q):10.1f}/s")
