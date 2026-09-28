"""CS202 Lab 07: snapshots and delta compression.

    python snapcodec.py --check              # tests your codec against the lecture's numbers
    python snapcodec.py --sim                # 30 s match, 5% loss, both baseline policies
    python snapcodec.py --sim --loss 0.2 --seed 3

The model is the week 7 lecture, section 2. Every entity has five fields. A full snapshot
writes every entity. A delta snapshot writes only entities whose fields differ from a
baseline snapshot, and for each one only the fields that differ, as absolute values.
Standard library only.
"""
import random
import struct
import sys

# name, struct code. 4 + 4 + 2 + 1 + 1 = 12 bytes per entity.
FIELDS = [("x", "f"), ("y", "f"), ("yaw", "H"), ("hp", "B"), ("anim", "B")]
HEADER = struct.Struct("<IIH")   # tick, baseline tick (0 = full), entity count: 10 bytes
ENT_ID = struct.Struct("<H")     # 2 bytes
MASK = struct.Struct("<B")       # 1 byte, bit i set = field i present
UDP_IP_HEADER = 28               # week 1


def field_size(code):
    return struct.calcsize("<" + code)


# ---------- full snapshots (given) ----------

def encode_full(tick, world):
    """world: dict entity_id -> dict of the five fields. Returns bytes."""
    out = [HEADER.pack(tick, 0, len(world))]
    for eid in sorted(world):
        out.append(ENT_ID.pack(eid))
        for name, code in FIELDS:
            out.append(struct.pack("<" + code, world[eid][name]))
    return b"".join(out)


def decode(data, baselines):
    """Decode a full or delta snapshot. baselines: dict tick -> world the client holds.
    Returns (tick, world). Raises KeyError if a delta's baseline is missing."""
    tick, base_tick, count = HEADER.unpack_from(data, 0)
    pos = HEADER.size
    if base_tick == 0:
        world = {}
        for _ in range(count):
            (eid,) = ENT_ID.unpack_from(data, pos); pos += ENT_ID.size
            ent = {}
            for name, code in FIELDS:
                (ent[name],) = struct.unpack_from("<" + code, data, pos); pos += field_size(code)
            world[eid] = ent
        return tick, world
    return tick, apply_delta(data, baselines[base_tick])


# ---------- delta snapshots (your work: the two TODOs) ----------

def encode_delta(tick, base_tick, base, world):
    """Delta of `world` against `base` (the world at base_tick).
    Layout: HEADER(tick, base_tick, number of changed entities), then for each changed
    entity in id order: ENT_ID, MASK, then the changed fields in FIELDS order.
    Unchanged entities are not written at all."""
    # TODO: build the body entity by entity, count the changed entities, then
    # return HEADER.pack(tick, base_tick, changed) + body.
    raise NotImplementedError("encode_delta")


def apply_delta(data, base):
    """Inverse of encode_delta: copy `base`, then overwrite the fields the delta carries."""
    # TODO: copy base (a new dict per entity), read the header, then for each entry
    # read the id and mask and overwrite the fields whose bit is set.
    raise NotImplementedError("apply_delta")


# ---------- the lecture's arena (given) ----------

def make_world(players=16, props=48):
    w = {}
    for i in range(players + props):
        w[i + 1] = {"x": float(i), "y": 0.0, "yaw": 0, "hp": 100, "anim": 0}
    return w


def step_world(world, tick, rng, players=16, p_prop=0.02):
    """Advance one tick: every player moves and turns; each prop changes hp and anim
    with probability p_prop (a pickup respawns, a door opens)."""
    new = {eid: dict(ent) for eid, ent in world.items()}
    for eid in new:
        e = new[eid]
        if eid <= players:
            e["x"] += 0.25
            e["y"] += 0.125
            e["yaw"] = (e["yaw"] + 91) % 65536
        elif rng.random() < p_prop:
            e["hp"] = (e["hp"] + 1) % 256
            e["anim"] = (e["anim"] + 1) % 256
    return new


def expected_delta_bytes(k, players=16, props=48, p_prop=0.02):
    """The lecture's model: expected delta size against a baseline k ticks old."""
    moving = 2 + 1 + 4 + 4 + 2           # id, mask, x, y, yaw
    prop = 2 + 1 + 1 + 1                 # id, mask, hp, anim
    return HEADER.size + players * moving + props * (1 - (1 - p_prop) ** k) * prop


# ---------- the network (given) ----------

def simulate(policy, loss=0.05, ticks=600, rtt_ticks=2, seed=1, players=16, props=48):
    """Server sends one snapshot per tick at 20 Hz. Each snapshot is lost with probability
    `loss`. The client acks every snapshot it decodes; acks reach the server rtt_ticks
    later and are never lost (keeps the model small).

    policy "acked": delta against the newest snapshot the client has acknowledged.
    policy "sent":  delta against the previous snapshot sent, acked or not (the bug).
    Returns (mean bytes per snapshot incl. UDP/IP, fulls sent, share of decoded snapshots
    after which the client's world differs from the server's, undecodable snapshots)."""
    rng_world, rng_net = random.Random(seed), random.Random(seed + 1000)
    world = make_world(players, props)
    history = {}                 # server: tick -> world it sent
    acked, pending_acks = 0, []  # newest acked tick, (arrival_tick, acked_tick)
    client, client_hist = None, {}
    total, fulls, undecodable, decoded, wrong = 0, 0, 0, 0, 0
    for tick in range(1, ticks + 1):
        world = step_world(world, tick, rng_world, players)
        history[tick] = world
        for arrive, t in [a for a in pending_acks if a[0] <= tick]:
            acked = max(acked, t)
        pending_acks = [a for a in pending_acks if a[0] > tick]
        if policy == "acked":
            base_tick = acked if acked and tick - acked < 29 else 0
        else:
            base_tick = tick - 1 if tick > 1 else 0
        if base_tick:
            data = encode_delta(tick, base_tick, history[base_tick], world)
        else:
            data = encode_full(tick, world)
            fulls += 1
        total += len(data) + UDP_IP_HEADER
        if rng_net.random() < loss:
            continue
        if policy == "sent" and base_tick and base_tick not in client_hist and client is not None:
            # a careless client applies the delta to whatever it has
            client = apply_delta(data, client)
            client_hist[tick] = client
        else:
            try:
                _, client = decode(data, client_hist)
                client_hist[tick] = client
            except KeyError:
                undecodable += 1
                continue
        decoded += 1
        wrong += client != world
        pending_acks.append((tick + rtt_ticks, tick))
    return total / ticks, fulls, wrong / max(decoded, 1), undecodable


# ---------- checks ----------

def check():
    try:
        _check()
    except NotImplementedError as e:
        print(f"TODO: implement {e} first")


def _check():
    w0 = make_world()
    w1 = step_world(w0, 1, random.Random(99), p_prop=0.0)
    w1[20]["hp"] = 50; w1[20]["anim"] = 3            # exactly one prop changes
    full = encode_full(1, w1)
    delta = encode_delta(2, 1, w0, w1)
    still = encode_delta(3, 1, w1, w1)
    expect = {
        "full snapshot bytes (64 entities)": (len(full), 906),
        "delta bytes, 16 moving + 1 prop": (len(delta), 223),
        "delta bytes, nothing changed": (len(still), 10),
        "full round trip": (decode(full, {})[1] == w1, True),
        "delta round trip": (apply_delta(delta, w0) == w1, True),
        "expected delta, k=1": (round(expected_delta_bytes(1), 1), 222.8),
        "expected delta, k=20": (round(expected_delta_bytes(20), 1), 297.8),
    }
    bad = [k for k, (got, want) in expect.items() if got != want]
    for k, (got, want) in expect.items():
        print(f"  {k:<36} got {got!s:<8} want {want}")
    print("all checks passed" if not bad else f"check these: {bad}")


def run_sim(args):
    loss = float(args[args.index("--loss") + 1]) if "--loss" in args else 0.05
    seed = int(args[args.index("--seed") + 1]) if "--seed" in args else 1
    print(f"30 s at 20 Hz, 64 entities, loss {loss:.0%}, seed {seed}")
    for policy in ("acked", "sent"):
        mean, fulls, wrong, bad = simulate(policy, loss=loss, seed=seed)
        print(f"  baseline = last {policy:<5}  {mean:6.1f} B/snapshot  {mean * 20 * 8 / 1000:5.1f} kbit/s"
              f"  fulls {fulls:2d}  client wrong after {wrong:6.1%} of snapshots  undecodable {bad}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--sim" in a:
        try:
            run_sim(a)
        except NotImplementedError as e:
            print(f"TODO: implement {e} first")
    else:
        check()
