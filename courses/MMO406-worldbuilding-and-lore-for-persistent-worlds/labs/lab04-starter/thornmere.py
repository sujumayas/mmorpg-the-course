"""Sample timeline for the invented world of Thornmere (week 4).

It contains exactly four planted problems. The tests expect your checker
to find all four and nothing else."""

ERAS = {
    "Twin Crowns": (640, 911),
    "The Drowning": (912, 980),
    "Long Truce": (981, 1200),
}

PEOPLE = {
    "Queen Adelmar": (1142, 1188),
    "Ysolde": (1184, None),
    "Brother Caddoc": (1120, 1179),
    "Harrow the Elder": (870, 941),
    "Mira of the Fens": (1150, None),
}

EVENTS = [
    {"id": "E01", "year": 700, "era": "Twin Crowns", "participants": []},
    {"id": "E02", "year": 912, "era": "The Drowning", "participants": ["Harrow the Elder"]},
    {"id": "E03", "year": 941, "era": "The Drowning", "participants": ["Harrow the Elder"]},
    {"id": "E04", "year": 985, "era": "Twin Crowns", "participants": []},                       # planted: outside era
    {"id": "E05", "year": 1160, "era": "Long Truce", "participants": ["Queen Adelmar", "Mira of the Fens"]},
    {"id": "E06", "year": 1181, "era": "Long Truce", "participants": ["Brother Caddoc"]},       # planted: after death
    {"id": "E07", "year": 1184, "era": "Long Truce", "participants": ["Ysolde", "Queen Adelmar"]},
    {"id": "E08", "year": 1190, "era": "Long Truce", "participants": ["Ysolde"]},
    {"id": "E09", "year": 1140, "era": "Long Truce", "participants": ["Queen Adelmar"]},        # planted: before birth
    {"id": "E10", "year": 1199, "era": "Long Truce", "participants": ["Lord Fenwick"]},         # planted: unknown person
]
