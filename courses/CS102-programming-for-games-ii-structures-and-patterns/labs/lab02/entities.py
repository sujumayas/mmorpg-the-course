"""Factory used by the tests. The tests only call make() and the World.

When you refactor, change these functions to build GameObjects from
components. Keep the names and parameters the same.
"""
from god_entity import Entity, World  # noqa: F401  (World is re-exported for tests)


def make(kind, x=0.0, y=0.0):
    if kind == "bush":
        return Entity("Bush", x, y, renders=True, sprite="bush")
    if kind == "trigger":
        return Entity("Trigger", x, y, collides=True, radius=2.0)
    if kind == "crate":
        return Entity("Crate", x, y, renders=True, sprite="crate",
                      collides=True, radius=0.5, has_health=True, max_hp=20)
    if kind == "rock":
        return Entity("Rock", x, y, renders=True, sprite="rock",
                      collides=True, radius=0.5, moves=True)
    if kind == "grenade":
        return Entity("Grenade", x, y, renders=True, sprite="grenade",
                      collides=True, radius=0.2, moves=True, vx=4.0,
                      explodes=True, blast_radius=3.0, blast_damage=25, fuse=1.0)
    if kind == "barrel":
        return Entity("Barrel", x, y, renders=True, sprite="barrel",
                      collides=True, radius=0.6, has_health=True, max_hp=10,
                      explodes=True, blast_radius=4.0, blast_damage=40)
    if kind == "goblin":
        return Entity("Goblin", x, y, renders=True, sprite="goblin",
                      collides=True, radius=0.5, moves=True,
                      has_health=True, max_hp=30, has_ai=True, chase_speed=2.0)
    raise ValueError(f"unknown kind {kind!r}")
