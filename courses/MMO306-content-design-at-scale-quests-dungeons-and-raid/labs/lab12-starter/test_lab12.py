"""Tests for Lab 12. Run:  python -m unittest test_lab12.py

Every test fails on the starter and passes on a correct solution.
"""
import copy
import os
import unittest

import funnel
import validate_content as v

HERE = os.path.dirname(os.path.abspath(__file__))
CLEAN = os.path.join(HERE, "content", "zone_clean.json")
SEEDED = os.path.join(HERE, "content", "zone_seeded.json")

EXPECTED_SEEDED = {
    ("DUP_ID", "q_den"),
    ("REF_NPC", "q_alpha"),
    ("XP_BUDGET", "q_alpha"),
    ("REF_STRING", "q_alpha"),
    ("LEVEL_ORDER", "q_return"),
    ("LEVEL_ORDER", "q_wolves"),
    ("REF_ITEM", "q_herbs"),
    ("REF_QUEST", "q_lost"),
    ("CYCLE", "q_wolves"),
    ("CYCLE", "q_return"),
    ("CYCLE", "q_alpha"),
    ("CYCLE", "q_den"),
    ("LOOT_SUM", "lt_alpha"),
    ("REF_ITEM", "lt_wolf"),
}


def codes(errors):
    return {(code, rid) for code, rid, _ in errors}


class TestValidator(unittest.TestCase):
    def test_clean_zone_has_no_errors(self):
        self.assertEqual(v.validate(v.load(CLEAN)), [])

    def test_seeded_zone_finds_every_seeded_defect(self):
        found = codes(v.validate(v.load(SEEDED)))
        self.assertEqual(found, EXPECTED_SEEDED)

    def test_errors_are_triples_with_messages(self):
        for e in v.validate(v.load(SEEDED)):
            self.assertEqual(len(e), 3)
            self.assertTrue(e[2])

    def test_loot_sum_uses_a_tolerance(self):
        c = v.load(CLEAN)
        c["loot_tables"].append(
            {"id": "lt_tenths", "entries": [{"item": "it_pelt", "chance": 0.1}] * 10})
        self.assertEqual(v.validate(c), [])   # 0.1 x 10 is not exactly 1.0 in floats

    def test_long_chain_is_not_a_cycle(self):
        c = v.load(CLEAN)
        prev = "q_herbs"
        for i in range(30):
            c["quests"].append({"id": f"q_chain{i}", "level": 10, "giver": "npc_hana",
                                "requires": [prev], "xp": 100, "text": "s_q5",
                                "reward_items": []})
            prev = f"q_chain{i}"
        self.assertEqual(v.validate(c), [])

    def test_self_requirement_is_a_cycle(self):
        c = v.load(CLEAN)
        c["quests"][4]["requires"] = ["q_herbs"]
        self.assertEqual(codes(v.validate(c)), {("CYCLE", "q_herbs")})


class TestFunnel(unittest.TestCase):
    def test_lecture_without_validator(self):
        r = funnel.run_pipeline(funnel.DEFECTS, funnel.PIPELINE)
        self.assertAlmostEqual(r["total_hours"], 853.0, delta=0.05)
        self.assertAlmostEqual(r["found"]["live"], 15.11, delta=0.01)
        self.assertAlmostEqual(r["escaped"]["data"], 7.35, delta=0.001)

    def test_lecture_with_validator(self):
        stages = funnel.insert_after(funnel.PIPELINE, "author", funnel.VALIDATOR)
        self.assertEqual([s[0] for s in stages], ["author", "validator", "review", "QA", "PTR"])
        r = funnel.run_pipeline(funnel.DEFECTS, stages)
        self.assertAlmostEqual(r["total_hours"], 415.8, delta=0.05)
        self.assertAlmostEqual(r["found"]["validator"], 45.0, delta=0.01)
        self.assertAlmostEqual(r["escaped"]["interaction"], 3.15, delta=0.001)

    def test_inputs_not_modified(self):
        d = copy.deepcopy(funnel.DEFECTS)
        funnel.run_pipeline(funnel.DEFECTS, funnel.PIPELINE)
        self.assertEqual(d, funnel.DEFECTS)


if __name__ == "__main__":
    unittest.main()
