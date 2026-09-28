"""DB201 Lab 11: generate the collector's landing file, events.ndjson (deterministic, seed 1111).

Run:  python make_events.py                 # 400 players, 14 days, about 400k lines, 135 MB
      python make_events.py --players 1000  # about 1M lines, 335 MB, for the scaling step

Each line is one event as the collector received it. Clients send events in
batches of up to 20. The file reproduces two things every real pipeline sees:

* Retries: about 2% of batches appear twice, because the client never got the
  server's acknowledgement and sent the batch again. Same event_ids both times.
* Late arrivals: about 1% of batches were written on day d but reached the
  collector after midnight UTC (client was offline). event_time is on day d,
  received_at is on day d+1.

Standard library only.
"""
import argparse
import json
import random
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
START = datetime(2026, 3, 1, tzinfo=timezone.utc)
DAYS = 14
ZONES = list(range(1, 13))          # 12 zones
ZONE_DANGER = {z: 0.6 + 0.1 * z for z in ZONES}   # zone 12 is the deadliest per minute
ZONE_DANGER[7] = 2.4                               # zone 7 has an overtuned boss
MOBS = {z: [z * 100 + k for k in range(1, 6)] for z in ZONES}
BATCH = 20


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def generate(players, seed=1111):
    rng = random.Random(seed)

    def uid():
        return str(uuid.UUID(int=rng.getrandbits(128), version=4))

    for day in range(DAYS):
        day_start = START + timedelta(days=day)
        build = 1405 if day < 7 else 1406
        for p in range(1, players + 1):
            if rng.random() > 0.6:
                continue
            session = uid()
            t = day_start + timedelta(minutes=rng.randint(0, 23 * 60))
            minutes = rng.randint(20, 150)
            events = []

            def emit(name, when, props):
                events.append({
                    "event_id": uid(), "event_name": name, "event_time": iso(when),
                    "player_id": p, "session_id": session, "build_id": build,
                    "properties": props,
                })

            zone = rng.choice(ZONES)
            emit("session_started", t, {"zone_id": zone})
            end = t + timedelta(minutes=minutes)
            while t < end:
                t += timedelta(seconds=rng.randint(20, 70))
                r = rng.random()
                if r < 0.05:
                    zone = rng.choice(ZONES)
                    emit("zone_entered", t, {"zone_id": zone})
                elif r < 0.05 + 0.02 * ZONE_DANGER[zone]:
                    emit("player_died", t, {"zone_id": zone, "x": round(rng.uniform(0, 800), 1),
                                            "y": round(rng.uniform(0, 800), 1),
                                            "killer_id": rng.choice(MOBS[zone])})
                elif r < 0.55:
                    emit("mob_killed", t, {"zone_id": zone, "mob_id": rng.choice(MOBS[zone])})
                else:
                    emit("item_looted", t, {"zone_id": zone, "item_type_id": rng.randint(1, 300)})
            emit("session_ended", t, {"zone_id": zone, "minutes": minutes})

            for i in range(0, len(events), BATCH):
                batch = events[i:i + BATCH]
                batch_id = uid()
                last = datetime.strptime(batch[-1]["event_time"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
                if rng.random() < 0.01:
                    next_midnight = (last + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                    received = next_midnight + timedelta(minutes=rng.randint(1, 180))
                else:
                    received = last + timedelta(seconds=rng.randint(1, 30))
                copies = 2 if rng.random() < 0.02 else 1
                for c in range(copies):
                    rec = received + timedelta(seconds=15 * c)
                    for e in batch:
                        yield dict(e, received_at=iso(rec), batch_id=batch_id)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--players", type=int, default=400)
    ap.add_argument("--out", default=str(HERE / "events.ndjson"))
    args = ap.parse_args()
    n = 0
    with open(args.out, "w") as f:
        for e in generate(args.players):
            f.write(json.dumps(e, separators=(",", ":")) + "\n")
            n += 1
    size = Path(args.out).stat().st_size
    print(f"wrote {n:,} lines, {size / 1e6:.1f} MB, {size / n:.0f} bytes per line -> {args.out}")


if __name__ == "__main__":
    main()
