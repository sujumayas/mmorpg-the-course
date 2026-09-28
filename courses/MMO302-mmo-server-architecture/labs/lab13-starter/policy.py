"""MMO302 Lab 13: your autoscaling policy. Edit this file.

decide() is called once per minute after logins are placed. It returns a dict with any of:
    "launch":    number of new servers to start (ready LAG minutes later)
    "drain":     ids of servers that should stop taking new players
    "undrain":   ids of draining servers to reopen
    "terminate": ids of servers to shut down (must hold 0 players)

place() orders the open servers for new logins. The simulator fills them in that order.
"""
import math

from fleet import CAP, LAG


class Policy:
    def __init__(self):
        self.last_demand = None

    def place(self, open_servers):
        # Starter: least-full first. This spreads players out; see step 4 of the lab.
        return sorted(open_servers, key=lambda s: s.players)

    def decide(self, t, demand, servers, queue):
        # Starter: never scale. Replace with target tracking + headroom (step 2),
        # a ramp estimate (step 3) and draining for scale-in (step 4).
        return {}
