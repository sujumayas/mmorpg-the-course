"""MMO402 Lab 12 starter: audit an "anonymized" character release.

Usage:  python lab12-starter.py [seed]

What it does now:
  1. generate() builds a synthetic server of 10,000 characters with realistic skew.
  2. It prints the lecture's uniform-model estimate and the actual equivalence-class
     counts for the raw release fields.
  3. It builds a list of 500 public profiles (name + visible fields) that an attacker
     could look up, the way public character pages work in many MMOs.

What you add (see labs/lab12.md): link_attack(), generalize(), suppress(), and the
release that passes k-anonymity while still answering the research question.

Research question the release must answer:
  "Are characters in small guilds more likely to quit within 30 days than
   characters in large guilds or in no guild?"

Pure standard library. Python 3.8+.
"""
import math
import random
import sys
from collections import Counter

N = 10_000
CLASSES = [f"class{i:02d}" for i in range(10)]
RACES = [f"race{i:02d}" for i in range(10)]
MAX_LEVEL = 60
N_GUILDS = 200
ZONES = [f"zone{i:02d}" for i in range(40)]


def zipf_weights(n, s=1.0):
    return [1.0 / (i + 1) ** s for i in range(n)]


def generate(seed=412):
    """Return a list of dict records. `name` is the direct identifier to remove."""
    rng = random.Random(seed)
    cw = zipf_weights(len(CLASSES))
    rw = zipf_weights(len(RACES))
    gw = zipf_weights(N_GUILDS)
    guild_names = [f"guild{i:03d}" for i in range(N_GUILDS)]
    records = []
    for i in range(N):
        level = MAX_LEVEL if rng.random() < 0.40 else rng.randint(1, MAX_LEVEL - 1)
        guild = "none" if rng.random() < 0.25 else rng.choices(guild_names, gw)[0]
        records.append({
            "name": f"Char{i:05d}",
            "class": rng.choices(CLASSES, cw)[0],
            "race": rng.choices(RACES, rw)[0],
            "level": level,
            "guild": guild,
            "zone": rng.choice(ZONES),
        })
    # guild sizes and the outcome variable
    sizes = Counter(r["guild"] for r in records if r["guild"] != "none")
    for r in records:
        size = sizes.get(r["guild"], 0)
        r["guild_size"] = size
        if r["guild"] == "none":
            p_quit = 0.35
        elif size < 20:
            p_quit = 0.30
        elif size < 100:
            p_quit = 0.20
        else:
            p_quit = 0.12
        r["quit_30d"] = int(rng.random() < p_quit)
    return records


def equivalence_classes(records, fields):
    """Counter mapping each combination of `fields` to its class size."""
    return Counter(tuple(r[f] for f in fields) for r in records)


def class_report(records, fields, k=5):
    classes = equivalence_classes(records, fields)
    n = len(records)
    unique = sum(1 for c in classes.values() if c == 1)
    below_k = sum(c for c in classes.values() if c < k)
    return {
        "fields": ",".join(fields),
        "classes": len(classes),
        "unique_records": unique,
        "unique_share": unique / n,
        f"share_below_{k}": below_k / n,
    }


def uniform_estimate(n, value_counts, k=5):
    """Lecture formula: lambda = (N-1)/C, unique share, share in class < k."""
    c = math.prod(value_counts)
    lam = (n - 1) / c
    unique = (1 - 1 / c) ** (n - 1)
    below = sum(math.exp(-lam) * lam ** j / math.factorial(j) for j in range(k - 1))
    return {"C": c, "lambda": lam, "unique_share": unique, "share_below_k": below}


def public_profiles(records, n=500, seed=7):
    """What an attacker can look up: names with their visible fields."""
    rng = random.Random(seed)
    return [{f: r[f] for f in ("name", "class", "race", "level", "guild")}
            for r in rng.sample(records, n)]


def release(records, fields):
    """Drop the name; keep only `fields` plus the outcome."""
    return [{**{f: r[f] for f in fields}, "quit_30d": r["quit_30d"]} for r in records]


# ---------------------------------------------------------------- your work

def link_attack(released, profiles, fields):
    """TODO Part B. For each profile, find released rows matching it on `fields`.
    Return the number of profiles that match exactly one row (re-identified)."""
    raise NotImplementedError


def generalize(record):
    """TODO Part C. Return a copy of `record` with coarser fields, for example a level
    bracket instead of an exact level, or a guild size band instead of a guild name."""
    raise NotImplementedError


def suppress(records, fields, k):
    """TODO Part C. Remove records whose class on `fields` is smaller than k.
    Return (kept_records, number_removed)."""
    raise NotImplementedError


def answer_question(records):
    """TODO Part D. Quit rate by guild group (none / small / medium / large) from a
    release. Compare with the same numbers computed on the raw data."""
    raise NotImplementedError


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 412
    data = generate(seed)
    print("Uniform model, class+race+level:",
          {k: round(v, 4) for k, v in uniform_estimate(N, [10, 10, 60]).items()})
    print("Uniform model, class+race+level+guild:",
          {k: round(v, 4) for k, v in uniform_estimate(N, [10, 10, 60, 200]).items()})
    for fields in (["class"], ["class", "race"], ["class", "race", "level"],
                   ["class", "race", "level", "guild"]):
        rep = class_report(data, fields)
        print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in rep.items()})
    profiles = public_profiles(data)
    print(f"{len(profiles)} public profiles available to the attacker.")
