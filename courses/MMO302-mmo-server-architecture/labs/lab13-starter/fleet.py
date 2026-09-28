"""MMO302 Lab 13: a minute-by-minute zone-server fleet simulator.

You write the policy in policy.py. Do not change this file; the tests use it as is.

Model (matches lecture week 13):
- Each server holds at most CAP players. A launched server is ready LAG minutes later.
- Every minute, each server loses ceil(players / SESSION_MEAN) players to logout
  (roughly exponential sessions with a 90-minute mean).
- New logins = demand now - players online after logout, plus anyone still queued.
  They are placed on ready servers that are not draining, in the order your policy's
  place() returns. Anyone who does not fit waits in the queue.
- You pay for every server that exists (booting, ready or draining) every minute.
- Terminating a server that still holds players raises PlayersKicked.
"""
import math
from dataclasses import dataclass, field

CAP = 500
LAG = 8
SESSION_MEAN = 90


class PlayersKicked(Exception):
    pass


@dataclass
class Server:
    id: int
    ready_at: int
    players: int = 0
    draining: bool = False

    def ready(self, t):
        return t >= self.ready_at


@dataclass
class Result:
    peak_queue: int = 0
    queue_player_minutes: int = 0
    server_minutes: int = 0
    history: list = field(default_factory=list)

    @property
    def server_hours(self):
        return self.server_minutes / 60


def evening_trace():
    """17:00 to 21:00: 12,000 players rising to 40,000, then flat."""
    return [min(40_000, 12_000 + 140 * t) for t in range(240)]


def launch_trace():
    """Expansion launch: 20,000 online, +3,000/min for 20 minutes, then flat for 100."""
    return [20_000 + 3_000 * min(t, 20) for t in range(120)]


HOURLY = [22, 17, 14, 12, 12, 12, 13, 15, 17, 19, 21, 22,
          23, 24, 25, 27, 30, 34, 38, 40, 39, 35, 30, 26]


def daily_trace():
    """One weekday, 1,440 minutes, linear between the hourly values (thousands)."""
    out = []
    for m in range(1440):
        h, f = divmod(m, 60)
        a, b = HOURLY[h], HOURLY[(h + 1) % 24]
        out.append(round(1000 * (a + (b - a) * f / 60)))
    return out


def run(demand, policy):
    """Run policy over a demand trace. policy has decide(t, demand, servers, queue) and place(servers)."""
    servers = []
    next_id = 0
    # Start with enough ready servers for the first minute at 80% utilization.
    for _ in range(math.ceil(demand[0] / (0.8 * CAP))):
        servers.append(Server(next_id, ready_at=0))
        next_id += 1
    queue = 0
    res = Result()
    for t, d in enumerate(demand):
        # 1. Logouts.
        for s in servers:
            if s.players:
                s.players -= min(s.players, math.ceil(s.players / SESSION_MEAN))
        online = sum(s.players for s in servers)
        # 2. Logins, placed in the policy's order.
        want_in = max(0, d - online)
        open_servers = [s for s in servers if s.ready(t) and not s.draining]
        for s in policy.place(open_servers):
            take = min(CAP - s.players, want_in)
            s.players += take
            want_in -= take
        queue = want_in
        # 3. Policy acts.
        action = policy.decide(t, d, list(servers), queue)
        for _ in range(action.get("launch", 0)):
            servers.append(Server(next_id, ready_at=t + LAG))
            next_id += 1
        by_id = {s.id: s for s in servers}
        for sid in action.get("drain", []):
            by_id[sid].draining = True
        for sid in action.get("undrain", []):
            by_id[sid].draining = False
        for sid in action.get("terminate", []):
            if by_id[sid].players > 0:
                raise PlayersKicked(f"minute {t}: server {sid} still has {by_id[sid].players} players")
            servers.remove(by_id[sid])
        # 4. Accounting.
        res.peak_queue = max(res.peak_queue, queue)
        res.queue_player_minutes += queue
        res.server_minutes += len(servers)
        res.history.append((t, d, sum(s.ready(t) for s in servers), len(servers), queue))
    return res


if __name__ == "__main__":
    import sys
    import policy
    names = sys.argv[1:] or ["evening", "launch", "daily"]
    for name in names:
        r = run(globals()[name + "_trace"](), policy.Policy())
        print(f"{name:8} peak queue {r.peak_queue:7,}  queue player-min {r.queue_player_minutes:10,}  "
              f"server-hours {r.server_hours:8.1f}")
