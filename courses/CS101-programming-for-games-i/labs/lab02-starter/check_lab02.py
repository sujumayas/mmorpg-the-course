"""Checker for CS101 Lab 02. Run from this folder:  python check_lab02.py [file]"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "cave.py"

MOVES = [  # room, has_key, command, expected
    ("entrance", "no", "north", "ROOM hall"),
    ("hall", "no", "south", "ROOM entrance"),
    ("hall", "no", "west", "ROOM well"),
    ("well", "no", "east", "ROOM hall"),
    ("hall", "no", "east", "ROOM armory"),
    ("armory", "no", "west", "ROOM hall"),
    ("vault", "yes", "south", "ROOM hall"),
    ("entrance", "no", "south", "BLOCKED"),
    ("well", "yes", "north", "BLOCKED"),
    ("hall", "no", "dance", "BLOCKED"),
    ("Hall", "no", " WEST ", "ROOM well"),
]
KEY = [
    ("hall", "yes", "north", "ROOM vault"),
    ("hall", "no", "north", "LOCKED"),
    ("hall", "yes", "North", "ROOM vault"),
]
DUELS = [  # p1, p2, expected
    (30, 20, "keep playing"), (30, 0, "P1 wins"), (0, 20, "P2 wins"), (0, 0, "sudden death"),
    (-5, -12, "sudden death"), (30, -4, "P1 wins"), (-1, 7, "P2 wins"), (1, 1, "keep playing"),
]


def run(stdin):
    out = subprocess.run([sys.executable, str(TARGET)], input=stdin, capture_output=True,
                         text=True, timeout=10)
    if out.returncode != 0:
        return "ERROR " + (out.stderr.strip().splitlines()[-1] if out.stderr else "crashed")
    lines = [l.split(": ")[-1].strip() for l in out.stdout.strip().splitlines()]
    tagged = [l[l.find(t):] for l in lines for t in ("ROOM", "LOCKED", "BLOCKED", "RESULT") if t in l]
    return tagged[-1] if tagged else "no output line"


def part(name, cases, make_stdin, expect):
    ok = True
    for c in cases:
        got = run(make_stdin(c))
        want = expect(c)
        if got != want:
            ok = False
            print(f"  {name}: input {c[:-1]} got '{got}' want '{want}'")
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
    return ok


def main():
    results = [
        part("Part A movement", MOVES, lambda c: f"move\n{c[0]}\n{c[1]}\n{c[2]}\n", lambda c: c[3]),
        part("Part B locked vault", KEY, lambda c: f"move\n{c[0]}\n{c[1]}\n{c[2]}\n", lambda c: c[3]),
        part("Part C duel", DUELS, lambda c: f"duel\n{c[0]}\n{c[1]}\n", lambda c: "RESULT " + c[2]),
    ]
    print(f"{sum(results)}/3 parts pass")
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
