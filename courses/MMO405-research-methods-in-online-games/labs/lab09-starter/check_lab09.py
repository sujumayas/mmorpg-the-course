"""MMO405 Lab 09 checker. Run after gen_census.py:  python check_lab09.py"""
import sys

import sna as s

TOL = 1e-9


def close(a, b, tol=TOL):
    return abs(a - b) <= tol


def row(snap, char, guild, zone, grouped):
    return {"snapshot": str(snap), "day": "1", "minute": "1140", "character": char,
            "guild": guild, "zone": zone, "grouped": grouped}


ROWS = [row(1, "A", "G", "Ashfen", "y"), row(1, "B", "G", "Ashfen", "y"),
        row(1, "C", "G", "Ashfen", "n"), row(1, "D", "G", "Capital", "y"),
        row(1, "E", "G", "Capital", "y"), row(1, "F", "H", "Ashfen", "y"),
        row(2, "A", "G", "Ashfen", "y"), row(2, "B", "G", "Ashfen", "y"),
        row(2, "C", "G", "Ashfen", "y"), row(3, "C", "G", "Frostvale", "y"),
        row(3, "A", "G", "Ashfen", "y")]
SMALL = {"a": {"b", "c", "d"}, "b": {"a"}, "c": {"a", "d"}, "d": {"a", "c", "e"}, "e": {"d"}}


def t_members():
    return s.members(ROWS, "G") == ["A", "B", "C", "D", "E"]


def t_build_ties():
    return s.build_ties(ROWS, "G") == {("A", "B"): 20, ("A", "C"): 10, ("B", "C"): 10}


def t_graph():
    adj = s.graph({("A", "B"): 20, ("A", "C"): 10}, ["A", "B", "C", "D"], min_minutes=15)
    return adj == {"A": {"B"}, "B": {"A"}, "C": set(), "D": set()}


def t_degree():
    d = s.degree_centrality(SMALL)
    return close(d["a"], 0.75) and close(d["b"], 0.25) and close(d["d"], 0.75)


def t_strength():
    ties = {("A", "B"): 20, ("A", "C"): 10}
    st = s.strength(s.graph(ties, ["A", "B", "C"], 15), ties)
    return st == {"A": 20, "B": 20, "C": 0}


def t_betweenness():
    b = s.betweenness(SMALL)
    return close(b["a"], 0.5) and close(b["d"], 0.5) and close(b["c"], 0.0) and close(b["e"], 0.0)


def t_eigenvector():
    x = s.eigenvector({"a": {"b"}, "b": {"a", "c"}, "c": {"b"}})
    return close(x["b"], 1.0) and close(x["a"], 2 ** -0.5, 1e-9) and close(x["c"], 2 ** -0.5, 1e-9)


def t_top():
    ties = {("A", "B"): 50, ("B", "C"): 50, ("C", "D"): 500, ("D", "E"): 500, ("E", "F"): 500}
    return s.top_by_threshold(ties, list("ABCDEF"), [0, 100], s.betweenness) == {0: "C", 100: "D"}


def t_generated():
    rows = s.load("census.csv")
    nodes = s.members(rows, "Lanternfall")
    ties = s.build_ties(rows, "Lanternfall")
    adj = s.graph(ties, nodes)
    return (len(nodes) == 13 and len(ties) == 40 and ties[("Quill", "Sable")] == 700
            and ties[("Harrow", "Mako")] == 20
            and close(s.betweenness(adj)["Quill"], 0.19949494949494948, 1e-9)
            and close(s.eigenvector(adj)["Harrow"], 0.5029466514250142, 1e-6)
            and s.top_by_threshold(ties, nodes, [0, 100, 400], s.betweenness)
            == {0: "Quill", 100: "Quill", 400: "Sable"})


TESTS = {"members": t_members, "build_ties": t_build_ties, "graph": t_graph,
         "degree_centrality": t_degree, "strength": t_strength,
         "betweenness": t_betweenness, "eigenvector": t_eigenvector,
         "top_by_threshold": t_top, "generated_census": t_generated}


def main():
    ok = True
    for name, test in TESTS.items():
        try:
            passed = bool(test())
        except NotImplementedError:
            print(f"TODO {name}")
            ok = False
            continue
        except FileNotFoundError:
            print(f"FAIL {name}: run gen_census.py first")
            ok = False
            continue
        except Exception as e:
            print(f"FAIL {name}: {type(e).__name__}: {e}")
            ok = False
            continue
        print(("PASS " if passed else "FAIL ") + name)
        ok = ok and passed
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
