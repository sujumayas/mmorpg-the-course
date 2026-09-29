"""MMO308 Lab 05: last month's day-7 retention on each of 40 servers.

Run:  python gen_servers.py     (writes server_history.csv, seed 505)

Each server has its own true retention rate, drawn around 30%. The spread
between servers is what you estimate as the intraclass correlation.
"""
import csv
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 505
SERVERS = 40
BASE = 0.30
SIGMA_B = 0.046          # between-server standard deviation of the true rate


def main():
    rng = random.Random(SEED)
    rows = []
    for s in range(1, SERVERS + 1):
        # a normal draw from two uniforms (Box-Muller), so the file is identical everywhere
        u1, u2 = rng.random(), rng.random()
        z = math.sqrt(-2 * math.log(1 - u1)) * math.cos(2 * math.pi * u2)
        true_rate = min(0.9, max(0.05, BASE + SIGMA_B * z))
        installs = 800 + int(rng.random() * 1600)
        retained = sum(1 for _ in range(installs) if rng.random() < true_rate)
        rows.append((f"srv{s:02d}", installs, retained))
    with open(HERE / "server_history.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(("server", "new_players", "d7_retained"))
        w.writerows(rows)
    print(f"{SERVERS} servers, {sum(r[1] for r in rows)} new players")


if __name__ == "__main__":
    main()
