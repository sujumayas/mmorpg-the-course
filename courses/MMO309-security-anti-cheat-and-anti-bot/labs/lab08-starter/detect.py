"""MMO309 Lab 08: from detector scores to decisions.

Fill in every function marked TODO. Keep the names and arguments; check_lab08.py
imports them. Standard library only. An account is flagged when score >= threshold.
"""


def confusion(scores, labels, threshold):
    """Return (tp, fp, fn, tn) for the rule 'flag if score >= threshold'."""
    # TODO
    raise NotImplementedError


def precision_recall(scores, labels, threshold):
    """Return (precision, recall). Precision is 1.0 when nothing is flagged."""
    # TODO
    raise NotImplementedError


def threshold_for_precision(scores, labels, target):
    """Lowest threshold, chosen from the distinct score values, whose precision
    on this data is at least target. Return None if no threshold reaches it."""
    # TODO
    raise NotImplementedError


def expected_cost(scores, labels, threshold, c_fp, c_fn):
    """Total cost of the decisions: c_fp per false positive plus c_fn per missed bot."""
    # TODO
    raise NotImplementedError


def precision_at_prevalence(recall, fpr, prevalence):
    """Precision the same detector would have in a population with a different
    share of bots. recall and fpr are rates measured on labelled data."""
    # TODO
    raise NotImplementedError


def review_band(scores, auto_threshold, capacity):
    """Lowest threshold t, chosen from the distinct score values below auto_threshold,
    such that the number of accounts with t <= score < auto_threshold is at most
    capacity. These are the cases human reviewers see. Return auto_threshold if
    even the highest such score would exceed capacity."""
    # TODO
    raise NotImplementedError
