"""DB201 Lab 10: tracking-plan and event validator.

Run from this folder:
    python validate_events.py                      # checks tracking_plan.json and sample_events.ndjson
    python validate_events.py --dau 40000          # change the audience used for the storage estimate
    python validate_events.py --plan my_plan.json --events my_events.ndjson

What it does, in order:
1. Checks the tracking plan: event names, property types, and that every event
   answers at least one question listed in the plan.
2. Estimates bytes per stored row for each event (the same size model as the
   week 10 lecture) and the storage per day and per year.
3. Validates every line of the sample event stream against the plan and prints
   one line per problem.

Standard library only. Python 3.10 or later.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Bytes per value, using PostgreSQL's on-disk sizes. "text" is special: see size_of().
TYPE_BYTES = {
    "uuid": 16,
    "timestamptz": 8,
    "bigint": 8,
    "int": 4,
    "smallint": 2,
    "real": 4,
    "double": 8,
    "bool": 1,
}
# Every stored row pays this: 24-byte heap tuple header (23 bytes, aligned) + 4-byte line pointer.
ROW_OVERHEAD = 28

# The envelope: fields every event carries, and how each is stored.
# event_name travels as a string but is stored as a smallint id from an event_types table.
ENVELOPE = {
    "event_id": "uuid",
    "event_name": "smallint",
    "event_time": "timestamptz",
    "player_id": "bigint",
    "session_id": "uuid",
    "build_id": "int",
}

NAME_RULE = re.compile(r"^[a-z]+(_[a-z]+)+$")          # object_action, lower snake case, no digits
PAST_TENSE = re.compile(r"(ed|en|un|lt|ught|ost|old|on|et|id|ade|ew|ove)$")  # crude; see lab sheet


def size_of(type_name):
    """Return bytes for one stored value. text:N means average N characters (+1 byte header)."""
    if type_name.startswith("text:"):
        return int(type_name.split(":", 1)[1]) + 1
    if type_name not in TYPE_BYTES:
        raise ValueError(f"unknown type {type_name!r}")
    return TYPE_BYTES[type_name]


def python_type_ok(type_name, value):
    """Loose check that a JSON value can be stored in the declared column type."""
    if value is None:
        return True  # nullable; the lab sheet asks you to decide which fields may be null
    if type_name in ("int", "smallint", "bigint"):
        return isinstance(value, int) and not isinstance(value, bool)
    if type_name in ("real", "double"):
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if type_name == "bool":
        return isinstance(value, bool)
    if type_name in ("uuid", "timestamptz") or type_name.startswith("text:"):
        return isinstance(value, str)
    return False


def check_plan(plan):
    problems = []
    questions = {q["id"] for q in plan.get("questions", [])}
    names = set()
    for ev in plan.get("events", []):
        name = ev.get("name", "")
        if name in names:
            problems.append(f"plan: event {name!r} defined twice")
        names.add(name)
        if not NAME_RULE.match(name):
            problems.append(f"plan: {name!r} is not lower_snake object_action (no digits, at least two words)")
        elif not PAST_TENSE.search(name.split("_")[-1]):
            problems.append(f"plan: {name!r} last word does not look past tense (warning; override in your memo if wrong)")
        if not ev.get("answers"):
            problems.append(f"plan: {name!r} answers no question. Why log it?")
        for qid in ev.get("answers", []):
            if qid not in questions:
                problems.append(f"plan: {name!r} answers unknown question {qid!r}")
        for prop, t in ev.get("properties", {}).items():
            if prop in ENVELOPE:
                problems.append(f"plan: {name!r} repeats envelope field {prop!r} as a property")
            try:
                size_of(t)
            except ValueError as e:
                problems.append(f"plan: {name!r}.{prop}: {e}")
        if "per_player_per_day" not in ev:
            problems.append(f"plan: {name!r} has no per_player_per_day estimate")
    answered = {q for ev in plan.get("events", []) for q in ev.get("answers", [])}
    for q in sorted(questions - answered):
        problems.append(f"plan: question {q!r} is not answered by any event")
    return problems


def storage_report(plan, dau):
    env = sum(size_of(t) for t in ENVELOPE.values())
    rows = []
    for ev in plan.get("events", []):
        try:
            props = sum(size_of(t) for t in ev.get("properties", {}).values())
        except ValueError:
            continue
        row = ROW_OVERHEAD + env + props
        per_day = dau * ev.get("per_player_per_day", 0)
        rows.append((ev["name"], row, per_day, row * per_day))
    print(f"\nStorage estimate at {dau:,} DAU (envelope {env} B + row overhead {ROW_OVERHEAD} B per row)")
    print(f"{'event':28} {'B/row':>6} {'rows/day':>12} {'MB/day':>9} {'GB/year':>8}")
    total = 0
    for name, row, per_day, b in rows:
        total += b
        print(f"{name:28} {row:6d} {per_day:12,.0f} {b / 1e6:9.1f} {b * 365 / 1e9:8.2f}")
    print(f"{'TOTAL':28} {'':6} {'':12} {total / 1e6:9.1f} {total * 365 / 1e9:8.2f}")
    return total


def check_events(plan, lines):
    problems = []
    by_name = {ev["name"]: ev for ev in plan.get("events", [])}
    seen_ids = set()
    for n, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError as e:
            problems.append(f"line {n}: not JSON ({e.msg})")
            continue
        for field, t in ENVELOPE.items():
            if field not in ev:
                problems.append(f"line {n}: missing envelope field {field!r}")
            elif field != "event_name" and not python_type_ok(t, ev[field]):
                problems.append(f"line {n}: envelope {field!r} has wrong type for {t}")
        eid = ev.get("event_id")
        if eid in seen_ids:
            problems.append(f"line {n}: duplicate event_id {eid} (a retry? see week 11)")
        seen_ids.add(eid)
        name = ev.get("event_name")
        spec = by_name.get(name)
        if spec is None:
            problems.append(f"line {n}: event {name!r} is not in the tracking plan")
            continue
        props = ev.get("properties", {})
        for p, t in spec.get("properties", {}).items():
            if p not in props:
                problems.append(f"line {n}: {name} missing property {p!r}")
            elif not python_type_ok(t, props[p]):
                problems.append(f"line {n}: {name}.{p} = {props[p]!r} is not a {t}")
        for p in props:
            if p not in spec.get("properties", {}):
                problems.append(f"line {n}: {name} sends undeclared property {p!r}")
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", default=str(HERE / "tracking_plan.json"))
    ap.add_argument("--events", default=str(HERE / "sample_events.ndjson"))
    ap.add_argument("--dau", type=int, default=40000)
    args = ap.parse_args(argv)

    plan = json.loads(Path(args.plan).read_text())
    plan_problems = check_plan(plan)
    print(f"Tracking plan: {len(plan.get('events', []))} events, {len(plan.get('questions', []))} questions")
    for p in plan_problems:
        print("  -", p)
    if not plan_problems:
        print("  plan OK")

    storage_report(plan, args.dau)

    lines = Path(args.events).read_text().splitlines()
    ev_problems = check_events(plan, lines)
    print(f"\nEvent stream: {len([l for l in lines if l.strip()])} events")
    for p in ev_problems:
        print("  -", p)
    if not ev_problems:
        print("  events OK")
    return 0 if not (plan_problems or ev_problems) else 1


if __name__ == "__main__":
    sys.exit(main())
