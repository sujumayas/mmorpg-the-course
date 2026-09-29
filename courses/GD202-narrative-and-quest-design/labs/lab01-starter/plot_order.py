"""GD202 Lab 01 starter: plot order audit. Standard library only.

Fill in the TODO functions, then run the tests from this folder:

    ../../../../.venv/bin/python test_plot_order.py

A plot is a list of story-event numbers in the order the player met them.
Story events are numbered 1..n in chronological (story) order.
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def validate(plot):
    """TODO step 1. Raise ValueError unless plot contains each number 1..n
    exactly once, where n = len(plot). Return None if it is valid."""
    raise NotImplementedError("validate() is yours to write")


def inversions(plot):
    """TODO step 2. Number of pairs (i < j) with plot[i] > plot[j]."""
    raise NotImplementedError("inversions() is yours to write")


def scramble(plot):
    """TODO step 3. inversions / (n(n-1)/2). Return 0.0 when n < 2."""
    raise NotImplementedError("scramble() is yours to write")


def open_questions(plot):
    """TODO step 4. A list with one entry per plot position p (0-based).
    Entry p counts the events shown so far (plot[0..p]) that still have at
    least one earlier story event (a smaller number) not yet shown.
    Example: [6, 1, 2, 3, 4, 5, 7, 8] -> [1, 1, 1, 1, 1, 0, 0, 0]."""
    raise NotImplementedError("open_questions() is yours to write")


def load_log(path):
    """Read a discovery log CSV with columns plot_position,story_number,label
    and return the plot as a list of story numbers sorted by plot_position."""
    with open(path, newline="") as f:
        rows = sorted(csv.DictReader(f), key=lambda r: int(r["plot_position"]))
    return [int(r["story_number"]) for r in rows]


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "sample_log.csv")
    plot = load_log(path)
    validate(plot)
    print("plot:", plot)
    print("inversions:", inversions(plot))
    print(f"scramble: {scramble(plot):.2f}")
    print("open questions by position:", open_questions(plot))
