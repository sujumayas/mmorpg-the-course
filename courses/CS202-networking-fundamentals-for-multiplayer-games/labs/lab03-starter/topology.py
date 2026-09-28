"""CS202 Lab 03: who pays the upload, and how long does an action take to reach everyone?

    python topology.py --check                 # tests your functions against the lecture
    python topology.py scenario.json           # full report for a scenario
    python topology.py scenario.json --n 16    # bandwidth table for 16 players

The model is the week 3 lecture, section 2. All bandwidth in bytes per second; the report
also prints kilobits per second (bytes * 8 / 1000). Standard library only.
"""
import itertools
import json
import sys


# ---------- bandwidth (n players, r updates per second, s bytes of state per player,
# ---------- i bytes of input per client packet, h bytes of IPv4 + UDP header) ----------

def mesh_upload(n, r, s, h):
    """Full-mesh peer-to-peer state sync: each peer sends its own state to n - 1 peers,
    one packet each, r times per second. TODO."""
    raise NotImplementedError


def snapshot_bytes(n, s, h):
    """One server snapshot to one client: every player's state plus one header. TODO."""
    raise NotImplementedError


def server_upload(n, r, s, h):
    """Dedicated server: one snapshot to each of n clients, r times per second. TODO."""
    raise NotImplementedError


def listen_host_upload(n, r, s, h):
    """Listen server: the host is also a player, so it sends snapshots to n - 1 others. TODO."""
    raise NotImplementedError


def client_upload(r, i, h):
    """Client of a server: one input packet r times per second. TODO."""
    raise NotImplementedError


# ---------- latency ----------

def direct(scn, a, b):
    """One-way latency between two players over their direct internet path."""
    if a == b:
        return 0
    d = scn["direct"]
    return d.get(f"{a}-{b}", d.get(f"{b}-{a}"))


def pair_latency(scn, a, b, topology, via=None):
    """One-way time for player a's action to reach player b.

    topology "mesh":   the direct path.
    topology "server": a -> server `via` -> b, using scn["servers"][via].
    topology "listen": a -> host player `via` -> b over direct paths (0 if a or b is the host).
    TODO: implement the three cases.
    """
    raise NotImplementedError


def worst_pair(scn, topology, via=None):
    """(pair, latency) for the slowest pair of players. TODO: use itertools.combinations."""
    raise NotImplementedError


# ---------- report ----------

def kbps(bps):
    return bps * 8 / 1000


def bandwidth_table(scn, n):
    r, s, i, h = scn["rate_hz"], scn["state_bytes"], scn["input_bytes"], scn["header_bytes"]
    print(f"{n} players, {r} Hz, {s} B state, {i} B input, {h} B header")
    rows = [("mesh peer upload", mesh_upload(n, r, s, h)),
            ("client upload (server)", client_upload(r, i, h)),
            ("client download (server)", r * snapshot_bytes(n, s, h)),
            ("dedicated server upload", server_upload(n, r, s, h)),
            ("listen host upload", listen_host_upload(n, r, s, h))]
    for name, b in rows:
        print(f"  {name:<26} {b:>10,.0f} B/s {kbps(b):>9.1f} kbps")


def latency_report(scn):
    print("worst pair, one way:")
    print("  mesh           ", worst_pair(scn, "mesh"))
    for sv in scn["servers"]:
        print(f"  server {sv:<8} ", worst_pair(scn, "server", sv))
    for p in scn["players"]:
        print(f"  listen host {p:<3} ", worst_pair(scn, "listen", p))


def check():
    with open("scenario.json") as f:
        scn = json.load(f)
    r, s, i, h = 20, 40, 12, 28
    expect = {
        "mesh n=8": (mesh_upload(8, r, s, h), 9520),
        "snapshot n=8": (snapshot_bytes(8, s, h), 348),
        "server n=8": (server_upload(8, r, s, h), 55680),
        "listen n=8": (listen_host_upload(8, r, s, h), 48720),
        "client up": (client_upload(r, i, h), 800),
        "server n=64": (server_upload(64, r, s, h), 3312640),
        "C->D via S1": (pair_latency(scn, "C", "D", "server", "S1"), 91),
        "B->D host A": (pair_latency(scn, "B", "D", "listen", "A"), 70),
        "worst mesh": (worst_pair(scn, "mesh")[1], 60),
        "worst S2": (worst_pair(scn, "server", "S2")[1], 50),
        "worst host C": (worst_pair(scn, "listen", "C")[1], 65),
    }
    bad = [k for k, (got, want) in expect.items() if got != want]
    print("all checks passed" if not bad else f"check these: {bad}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "--check":
        check()
    else:
        with open(args[0]) as f:
            scn = json.load(f)
        n = int(args[args.index("--n") + 1]) if "--n" in args else len(scn["players"])
        bandwidth_table(scn, n)
        latency_report(scn)
