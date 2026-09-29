"""MMO406 Lab 04 starter: the lore clock and a timeline checker.

Standard library only. Fill in the three TODO functions, then run the tests:

    .venv/bin/python courses/MMO406-worldbuilding-and-lore-for-persistent-worlds/labs/lab04-starter/test_lore_clock.py

Model (week 4, section 2), with t in real years since launch:

    w(t) = w0 + r * t + J * floor(t / T)      (no jump term when T is None)
    S(t) = w(t) - w0                           span, also the new player's time gap
    D(t) = E * t / max(S(t), 1)                story beats per in-world year
    a(t) = a0 + S(t)                           a character's age
"""
from math import floor  # noqa: F401  (you will need it)


def world_year(t, w0, r, J=0, T=None):
    """TODO 1. Return the in-world year after t real years.

    J is the jump per expansion and T the expansion period in real years.
    When T is None there are no expansion jumps."""
    raise NotImplementedError("world_year() is yours to write")


def clock_summary(t, w0, r, J=0, T=None, E=6, a0=16):
    """TODO 2. Return a dict with keys 'span', 'gap', 'density', 'age'.

    'gap' is the time gap for a player who starts the launch content at real
    year t. Week 4 shows it equals the span."""
    raise NotImplementedError("clock_summary() is yours to write")


def check_timeline(events, people, eras):
    """TODO 3. Return a sorted list of (event_id, code) problems.

    events: list of dicts with keys 'id', 'year', 'era', 'participants'.
    people: dict name -> (born, died); died is None for the living.
    eras:   dict era name -> (start_year, end_year), inclusive at both ends.

    Codes, one tuple per problem found (an event can have several):
      'UNKNOWN_PERSON'  a participant is not in `people`
      'BEFORE_BIRTH'    a participant acts before the year they were born
      'AFTER_DEATH'     a participant acts after the year they died
                        (acting in the year of death is allowed)
      'OUTSIDE_ERA'     the event's year is outside its era's range,
                        or the era name is not in `eras`
    Report BEFORE_BIRTH / AFTER_DEATH once per offending participant, so the
    same code can appear twice for one event."""
    raise NotImplementedError("check_timeline() is yours to write")


if __name__ == "__main__":
    from thornmere import ERAS, EVENTS, PEOPLE

    for name, r, J, T in [("Frozen", 0, 0, None), ("Slow drift", 0.25, 0, None),
                          ("Real time", 1, 0, None), ("Stepped", 0, 3, 2.5)]:
        print(name, clock_summary(10, 1200, r, J, T))
    for problem in check_timeline(EVENTS, PEOPLE, ERAS):
        print(problem)
