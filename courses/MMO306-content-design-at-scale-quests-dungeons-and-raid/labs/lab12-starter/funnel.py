"""MMO306 Lab 12 starter: the defect funnel from the week 12 lecture.

The constants are the lecture's teaching values. Write run_pipeline and
insert_after, then use them for Part C of the lab.
"""

DEFECTS = {"data": 60, "logic": 30, "interaction": 10}   # per 1,000 content items

# (stage name, hours to fix one defect found here, catch rate by class)
PIPELINE = [
    ("author", 0.25, {"data": 0.30, "logic": 0.20, "interaction": 0.00}),
    ("review", 1.0, {"data": 0.30, "logic": 0.20, "interaction": 0.10}),
    ("QA", 4.0, {"data": 0.50, "logic": 0.60, "interaction": 0.30}),
    ("PTR", 8.0, {"data": 0.50, "logic": 0.40, "interaction": 0.50}),
]
VALIDATOR = ("validator", 0.5, {"data": 0.90, "logic": 0.30, "interaction": 0.00})
LIVE_COST = 40.0


def run_pipeline(defects, stages, live_cost=LIVE_COST):
    """Push defects through the stages in order. Each stage finds
    (defects of a class still left) x (its catch rate for that class).
    Whatever is left after the last stage is found live at live_cost each.

    Return a dict:
        "found":       {stage name: defects found there, plus "live"}
        "hours":       {stage name: hours spent there, plus "live"}
        "escaped":     {class: defects that reached live}
        "total_hours": sum of all hours
    Do not modify `defects`.
    """
    raise NotImplementedError("TODO: run_pipeline")


def insert_after(stages, after_name, new_stage):
    """Return a new stage list with new_stage placed right after the stage called after_name."""
    raise NotImplementedError("TODO: insert_after")
