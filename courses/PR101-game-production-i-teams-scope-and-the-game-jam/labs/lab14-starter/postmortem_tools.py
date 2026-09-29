"""PR101 lab 14: Pareto tables and recurrence from coded post-mortems.

Run:  python postmortem_tools.py                 (Politowski counts + example team)
      python postmortem_tools.py my_team.csv     (your own coded problems)

Two input formats:
  counts CSV    columns category,count           (politowski_types.csv)
  problems CSV  columns project,category,problem,action_item,owner,done
                one row per coded problem          (example_team.csv)

The loaders and the report are complete. The five functions marked TODO are
stubs that return something harmless so the file runs. Lecture sections 2 and 4.
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_counts(path):
    """{category: count} from a category,count CSV."""
    with open(path, newline="", encoding="utf-8") as f:
        return {row["category"].strip(): int(row["count"]) for row in csv.DictReader(f)}


def load_problems(path):
    """List of dicts, one per coded problem, with whitespace stripped."""
    with open(path, newline="", encoding="utf-8") as f:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(f)]


def count_by_category(problems, project):
    """{category: number of problems} for the rows whose project matches.

    Example: the jam rows of example_team.csv give
    {"scope": 2, "planning": 1, "communication": 1, "bugs": 1, "crunch time": 1}.
    """
    return {}  # TODO: replace this stub


def pareto(counts):
    """Pareto rows [(category, n, share, cumulative_share), ...].

    Sort by count, largest first; break ties alphabetically by category name.
    share = n / total, cumulative_share = running total / total.
    Categories with a count of 0 are left out. An empty dict gives [].
    """
    return [(name, n, 0.0, 0.0) for name, n in counts.items()]  # TODO: replace this stub


def vital_few(rows, threshold=0.8):
    """Smallest k (1-based) whose cumulative share is >= threshold.

    Compare with a small tolerance (1e-9) so that exactly 80% counts.
    Return 0 for an empty list.
    """
    return len(rows)  # TODO: replace this stub


def recurrence(problems, first, second):
    """(R, repeated) for two projects.

    C1 = set of categories in project `first`, C2 = set in project `second`.
    R = |C1 & C2| / |C1|, and repeated = sorted list of C1 & C2.
    If C1 is empty, return (0.0, []).
    """
    return 0.0, []  # TODO: replace this stub


def closure(problems, project):
    """(closure_rate, open_items) for one project's action items.

    Look only at rows of `project` with a non-empty action_item. The same
    action item text may appear on several rows; count each distinct text once.
    An item is closed if its done field is "yes" (any case) on any of its rows.
    closure_rate = closed items / distinct items (0.0 if there are none).
    open_items = sorted list of the distinct item texts that are not closed.
    """
    return 1.0, []  # TODO: replace this stub


# ---------------------------------------------------------------------------
# Complete. Prints the tables the lab asks for.

def print_pareto(title, counts, threshold=0.8):
    rows = pareto(counts)
    print(title)
    for k, (name, n, share, cum) in enumerate(rows, start=1):
        print(f"  {k:2} {name:20} {n:4} {share:6.1%} {cum:6.1%}")
    print(f"  k_{round(threshold * 100)} = {vital_few(rows, threshold)} of {len(rows)} categories\n")


def report(problems_path):
    print_pareto("Politowski et al., 927 problems by type", load_counts(HERE / "politowski_types.csv"))
    problems = load_problems(problems_path)
    projects = list(dict.fromkeys(p["project"] for p in problems))
    for project in projects:
        print_pareto(f"{problems_path.name}: {project}", count_by_category(problems, project))
        rate, still_open = closure(problems, project)
        if still_open or rate:
            print(f"  action items closed: {rate:.0%}; open: {still_open}\n")
    if len(projects) >= 2:
        r, repeated = recurrence(problems, projects[0], projects[1])
        print(f"recurrence {projects[0]} -> {projects[1]}: R = {r:.0%}, repeated: {repeated}")


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "example_team.csv"
    report(path)
