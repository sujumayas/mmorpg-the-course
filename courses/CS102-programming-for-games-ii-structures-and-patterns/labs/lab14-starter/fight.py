"""A deterministic 30-second duel driven by recorded commands (CS102 week 12, Command).

A command is (tick, actor, action). The fight runs at 10 ticks per second for 300 ticks.
Actions: "attack", "guard" (halves the next hit taken), "potion" (+15 HP, max 100).
"""
import json
import random


def damage(raw, armor):
    return max(1, raw - armor)


def simulate(commands, seed):
    rng = random.Random(seed)
    units = {
        "knight": {"hp": 100, "armor": 3, "min": 6, "max": 12, "guard": False},
        "bandit": {"hp": 100, "armor": 1, "min": 4, "max": 14, "guard": False},
    }
    by_tick = {}
    for tick, actor, action in commands:
        by_tick.setdefault(tick, []).append((actor, action))
    for tick in range(300):
        for actor, action in by_tick.get(tick, []):
            me = units[actor]
            other = units["bandit" if actor == "knight" else "knight"]
            if me["hp"] <= 0 or other["hp"] <= 0:
                continue
            if action == "attack":
                hit = damage(rng.randint(me["min"], me["max"]), other["armor"])
                if other["guard"]:
                    hit //= 2
                    other["guard"] = False
                other["hp"] -= hit
            elif action == "guard":
                me["guard"] = True
            elif action == "potion":
                me["hp"] = min(100, me["hp"] + 15)
    return units


def fingerprint(units):
    """One string that changes if anything about the final state changes."""
    return ";".join(f"{name}:{u['hp']}:{int(u['guard'])}" for name, u in sorted(units.items()))


def record(path, seed=12, n_commands=90):
    """Generate a random command list once and save it with its result."""
    gen = random.Random(seed)
    actions = ["attack"] * 6 + ["guard", "potion"]
    commands = sorted((gen.randrange(300), gen.choice(["knight", "bandit"]), gen.choice(actions))
                      for _ in range(n_commands))
    fp = fingerprint(simulate(commands, seed))
    with open(path, "w") as f:
        json.dump({"seed": seed, "commands": commands, "fingerprint": fp}, f)
    return fp


if __name__ == "__main__":
    import sys
    if "--record" in sys.argv:              # overwrites replay_30s.json: only on purpose
        print("recorded", record("replay_30s.json"))
    else:
        with open("replay_30s.json") as f:
            saved = json.load(f)
        fp = fingerprint(simulate([tuple(c) for c in saved["commands"]], saved["seed"]))
        print(fp, "MATCH" if fp == saved["fingerprint"] else f"DIFFERS from saved {saved['fingerprint']}")
