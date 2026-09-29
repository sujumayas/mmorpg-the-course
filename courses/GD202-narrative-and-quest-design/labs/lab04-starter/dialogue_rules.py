"""GD202 Lab 04 starter: a rule-based dialogue matcher and checker.

Standard library only. Fill in the four TODO functions, then run the tests:

    .venv/bin/python courses/GD202-narrative-and-quest-design/labs/lab04-starter/test_rules.py

The model is the one from week 4, section 2:
  - a rule matches a state when every one of its conditions is true;
  - a rule's score is its number of conditions;
  - the chosen rule is the matching rule with the highest score;
  - two or more matching rules sharing the top score are a tie.
"""
import operator
from dataclasses import dataclass, field
from itertools import product

OPS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">=": operator.ge,
    "<=": operator.le,
    ">": operator.gt,
    "<": operator.lt,
}


@dataclass
class Rule:
    name: str
    conditions: list = field(default_factory=list)  # list of (fact, op, value) tuples
    line: str = ""

    @property
    def score(self):
        return len(self.conditions)


def matches(rule, state):
    """TODO 1. Return True if every condition (fact, op, value) of `rule`
    holds in `state` (a dict fact -> value). A rule with no conditions
    always matches. Use OPS[op](state[fact], value)."""
    raise NotImplementedError("matches() is yours to write")


def winners(rules, state):
    """TODO 2. Return the names of the matching rules with the highest score,
    in the order they appear in `rules`. Return [] if nothing matches."""
    raise NotImplementedError("winners() is yours to write")


def all_states(domains):
    """TODO 3. `domains` is a dict fact -> list of possible values, e.g.
    {"met": [False, True], "wolves": [0, 10, 20, 30]}. Return a list of
    dicts, one per combination, in itertools.product order over the
    facts in the dict's key order."""
    raise NotImplementedError("all_states() is yours to write")


def audit(rules, domains):
    """TODO 4. Check a rule set against every state. Return a dict:
      "states":    number of states,
      "silent":    list of states (dicts) where no rule matches,
      "ties":      list of (state, [names]) where two or more rules tie,
      "wins":      dict rule name -> number of states it wins alone,
      "dead":      names of rules that never win alone and never tie,
      "only_ties": names of rules that never win alone but appear in a tie.
    Keep rule order in "dead" and "only_ties"."""
    raise NotImplementedError("audit() is yours to write")


# The barkeep from the week 4 lecture, section 2.
BARKEEP = [
    Rule("R0", [], "Welcome, traveller. Sit anywhere."),
    Rule("R1", [("met", "==", True)], "Back again? Same table as before."),
    Rule("R2", [("wolves_dead", "==", True)], "You're the one who cleared the wolves!"),
    Rule("R3", [("thief", "==", True)], "Keep your hands where I can see them."),
    Rule("R4", [("met", "==", True), ("wolves_dead", "==", True)],
         "Back again, wolf-slayer. First drink's on me."),
    Rule("R5", [("wolves_dead", "==", True), ("thief", "==", True)],
         "Hero or not, I'm watching my till."),
]
BARKEEP_DOMAINS = {"met": [False, True], "wolves_dead": [False, True], "thief": [False, True]}


if __name__ == "__main__":
    try:
        report = audit(BARKEEP, BARKEEP_DOMAINS)
    except NotImplementedError as e:
        raise SystemExit(f"Not finished yet: {e}. Run test_rules.py to see what is left.")
    print("states:", report["states"])
    print("silent:", len(report["silent"]))
    print("ties:  ", [names for _, names in report["ties"]])
    print("dead:  ", report["dead"], " only ties:", report["only_ties"])
