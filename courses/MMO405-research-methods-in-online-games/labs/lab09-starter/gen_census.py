"""MMO405 Lab 09: writes census.csv, four weeks of /who-style snapshots (seed 809).

One snapshot every 10 minutes from 19:00 to 22:00 server time on 28 evenings.
Each row is one character seen online in one snapshot:
    snapshot, day, minute, character, guild, zone, grouped (y/n)
Cities are "Capital" and "Harbor". The guild under study is Lanternfall; other
characters online belong to other guilds or none. ranks.csv (supplied) holds
Lanternfall's rank list.
Run:  python gen_census.py
"""
import csv
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
CITIES = ["Capital", "Harbor"]
FIELD = ["Ashfen", "Brightmoor", "Cinder Reach", "Duskwood Hollow", "Emberline", "Frostvale"]
RAID = ["Quill", "Sable", "Tovin", "Wren", "Yara", "Oren"]
CASUAL = ["Mako", "Lise", "Pim", "Dace"]
PVP = ["Brask", "Vell"]
GM = "Harrow"
ONLINE_P = {**{m: 0.8 for m in RAID}, **{m: 0.6 for m in CASUAL}, **{m: 0.5 for m in PVP},
            GM: 0.35, "Quill": 0.95}


def main():
    rng = random.Random(809)
    rows, snap = [], 0
    for day in range(28):
        raid_night = day % 7 in (1, 3)
        online = [m for m, p in ONLINE_P.items() if rng.random() < p]  # list: fixed order
        plan = {m: ("solo", rng.choice(FIELD)) for m in online}
        if raid_night:
            for m in RAID:
                if m in online:
                    plan[m] = ("raid", "Emberline")
        else:
            zone = rng.choice(FIELD)
            for m in CASUAL + (["Quill"] if rng.random() < 0.6 else []):
                if m in online:
                    plan[m] = ("casual", zone)
            if "Sable" in online and rng.random() < 0.5:
                plan["Sable"] = ("casual", zone)
        pvp_zone = rng.choice(FIELD)
        for m in PVP:
            if m in online:
                plan[m] = ("pvp", pvp_zone)
        if GM in online:
            plan[GM] = ("city", "Capital")
            if "Tovin" in online and rng.random() < 0.4:
                plan[GM] = ("gm", "Brightmoor")
                plan["Tovin"] = ("gm", "Brightmoor")
        start = {m: rng.randint(0, 6) for m in online}
        length = {m: rng.randint(8, 18) for m in online}
        for k in range(18):
            snap += 1
            minute = 19 * 60 + 10 * k
            for m in sorted(online):
                if not start[m] <= k < start[m] + length[m]:
                    continue
                act, zone = plan[m]
                if k == start[m] or k == start[m] + length[m] - 1:
                    act, zone = "city", rng.choice(CITIES)
                grouped = act not in ("solo", "city")
                if act == "casual" and rng.random() < 0.15:
                    grouped = False
                rows.append((snap, day + 1, minute, m, "Lanternfall", zone, "y" if grouped else "n"))
            for j in range(rng.randint(6, 12)):
                g = rng.choice(["Ironbound", "Ironbound", "Starwake", ""])
                rows.append((snap, day + 1, minute, f"X{rng.randint(1, 60):02d}", g,
                             rng.choice(FIELD + CITIES), "y" if rng.random() < 0.4 else "n"))
    with open(HERE / "census.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["snapshot", "day", "minute", "character", "guild", "zone", "grouped"])
        w.writerows(rows)
    print(f"wrote census.csv ({len(rows)} rows, {snap} snapshots)")


if __name__ == "__main__":
    main()
