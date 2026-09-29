"""CS201 Lab 14 starter: the tool half of a reflection layer.

Run `python reflect.py` to print a short demo. Parts you have not written yet print a dash.

Provided:
- prop(): declare a field once with its metadata (range, save, edit, net).
- @component: registers a dataclass in REGISTRY under its class name.
- Three components: Health, Spawner, Door.
- descriptors(): the list of dataclass fields of a component, in declaration order.

You write the five parts marked TODO. Every tool must loop over descriptors();
no tool may mention a component or a field by name.
"""
from dataclasses import dataclass, field, fields

REGISTRY = {}


def prop(default, lo=None, hi=None, save=True, edit=True, net=False):
    """Declare a field once; the metadata tells every tool what to do with it."""
    return field(default=default,
                 metadata={"lo": lo, "hi": hi, "save": save, "edit": edit, "net": net})


def component(cls):
    """Class decorator: make cls a dataclass and register it by name."""
    cls = dataclass(cls)
    REGISTRY[cls.__name__] = cls
    return cls


def descriptors(obj_or_cls):
    return list(fields(obj_or_cls))


@component
class Health:
    current: int = prop(100, lo=0, hi=9_999, net=True)
    maximum: int = prop(100, lo=1, hi=9_999)
    regen_rate: float = prop(1.5, lo=0.0, hi=50.0)
    last_hit_by: int = prop(0, save=False, edit=False)


@component
class Spawner:
    enemy: str = prop("goblin")
    waves: int = prop(3, lo=1, hi=20)
    interval_s: float = prop(8.0, lo=0.5, hi=120.0)
    radius: float = prop(4.0, lo=0.0, hi=50.0)
    spawned: int = prop(0, save=False, edit=False)


@component
class Door:
    locked: bool = prop(False, net=True)
    key_id: int = prop(0, lo=0, hi=65_535)
    open_time_s: float = prop(0.75, lo=0.0, hi=10.0)


def clamp(value, meta):
    """Clamp a number to the field's range. Leaves non-numbers and bools alone."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return value
    lo, hi = meta["lo"], meta["hi"]
    if lo is not None and value < lo:
        return lo
    if hi is not None and value > hi:
        return hi
    return value


# ---------------------------------------------------------------- TODO 1
def inspector_rows(obj):
    """Return [(name, value, lo, hi)] for every field with edit=True, in declaration order."""
    raise NotImplementedError("inspector_rows")


# ---------------------------------------------------------------- TODO 2
def save(obj):
    """Return {"type": <class name>, "fields": {name: value}} for every field with save=True."""
    raise NotImplementedError("save")


# ---------------------------------------------------------------- TODO 3
def load(data, redirects=None):
    """Build a component from save() output. Return (obj, warnings).

    - Look the class up in REGISTRY by data["type"].
    - redirects maps "Type.old_name" to "new_name". Apply it to each saved key first.
    - A saved key that (after redirects) is not a declared save=True field is skipped,
      with the warning "<Type>.<key>: not declared".
    - Values are clamped with clamp(). If clamping changed a value, add the warning
      "<Type>.<name>: <value> clamped to <clamped>".
    - Fields missing from the data keep their defaults, with no warning.
    - Warnings are in the order the saved keys appear.
    """
    raise NotImplementedError("load")


# ---------------------------------------------------------------- TODO 4
def diff(a, b):
    """Return [(name, a_value, b_value)] for every save=True field that differs, in order.

    a and b must be the same component type; raise TypeError otherwise.
    """
    raise NotImplementedError("diff")


# ---------------------------------------------------------------- TODO 5
class History:
    """Undo and redo with transactions, for any field of any component.

    begin(label) opens a transaction. set(obj, name, value) clamps value with the
    field's metadata, writes it, and records it; repeated sets of the same field of
    the same object in one transaction keep the first old value and the last new
    value. end() closes the transaction (an empty one is dropped) and clears the redo
    stack. undo() and redo() return the transaction's label, or None if there is
    nothing to undo or redo. set() outside a transaction raises RuntimeError.
    """

    def __init__(self):
        raise NotImplementedError("History")

    def begin(self, label):
        raise NotImplementedError("History.begin")

    def set(self, obj, name, value):
        raise NotImplementedError("History.set")

    def end(self):
        raise NotImplementedError("History.end")

    def undo(self):
        raise NotImplementedError("History.undo")

    def redo(self):
        raise NotImplementedError("History.redo")


def _try(fn, *args):
    try:
        return fn(*args)
    except NotImplementedError:
        return "-"


if __name__ == "__main__":
    sp = Spawner(waves=5)
    print("inspector:", _try(inspector_rows, sp))
    print("save:     ", _try(save, sp))
    old = {"type": "Spawner", "fields": {"enemy": "orc", "waves": 40, "interval": 3.0}}
    print("load:     ", _try(load, old, {"Spawner.interval": "interval_s"}))
    print("diff:     ", _try(diff, Spawner(), sp))
