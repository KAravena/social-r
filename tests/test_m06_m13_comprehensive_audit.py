"""Automated Comprehensive Audit Regression Suite for Social R (Modules 06 to 13).

Ensures all published activities (regular exercises and final challenges) satisfy:
1. Cold start setups run cleanly without missing dependencies or leftover state.
2. Checkers parse cleanly in R without syntax errors or unescaped character strings.
3. Canonical solutions execute without runtime errors.
4. Canonical solutions pass their checkers.
5. Final challenges execute and pass checkers.
6. Unmodified starter codes do NOT falsely pass checkers.
7. Plausible dummy wrong answers are cleanly rejected without crashes.
"""
import unittest
from pathlib import Path
from tests.audit_engine import load_all_activities, run_r_audit

ROOT = Path(__file__).resolve().parent.parent


class TestM06M13ComprehensiveAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.target_modules = list(range(6, 14))
        cls.activities = load_all_activities(cls.target_modules)
        cls.results = run_r_audit(cls.activities)

    def test_activity_count(self):
        regular_count = sum(1 for a in self.activities if not a["is_challenge"])
        challenge_count = sum(1 for a in self.activities if a["is_challenge"])
        self.assertEqual(len(self.target_modules), 8, "Expected 8 modules (06 to 13)")
        self.assertEqual(regular_count, 53, "Expected 53 regular exercises across M06-M13")
        self.assertEqual(challenge_count, 8, "Expected 8 final challenges across M06-M13")
        self.assertEqual(len(self.activities), 61, "Expected 61 total activities audited across M06-M13")

    def test_all_activity_setups_run_cleanly(self):
        cold_start_fails = [
            f"{r['id']}: {r['cold_start_error']}"
            for r in self.results.values()
            if not r["cold_start_pass"]
        ]
        self.assertEqual(len(cold_start_fails), 0, f"Cold-start failures:\n" + "\n".join(cold_start_fails))

    def test_all_activity_checkers_parse(self):
        parse_fails = [
            f"{r['id']}: {r['checker_parse_error']}"
            for r in self.results.values()
            if not r["checker_parse_pass"]
        ]
        self.assertEqual(len(parse_fails), 0, f"Checker parse failures:\n" + "\n".join(parse_fails))

    def test_all_canonical_solutions_execute(self):
        exec_fails = [
            f"{r['id']}: {r['canonical_exec_error']}"
            for r in self.results.values()
            if not r["canonical_exec_pass"]
        ]
        self.assertEqual(len(exec_fails), 0, f"Canonical solution execution failures:\n" + "\n".join(exec_fails))

    def test_all_canonical_solutions_pass_checker(self):
        checker_fails = [
            f"{r['id']}: {r['canonical_checker_message']}"
            for r in self.results.values()
            if not r["canonical_checker_pass"]
        ]
        self.assertEqual(len(checker_fails), 0, f"Canonical solution checker failures:\n" + "\n".join(checker_fails))

    def test_all_challenges_canonical_solutions_pass(self):
        challenge_fails = [
            f"{r['id']}: {r['canonical_checker_message']}"
            for r in self.results.values()
            if r["is_challenge"] and not r["canonical_checker_pass"]
        ]
        self.assertEqual(len(challenge_fails), 0, f"Challenge failures:\n" + "\n".join(challenge_fails))

    def test_all_starter_codes_not_false_passing(self):
        false_passes = [
            f"{r['id']}: {r['starter_wrong_message']}"
            for r in self.results.values()
            if r.get("starter_false_pass")
        ]
        self.assertEqual(len(false_passes), 0, f"Starter code false passes:\n" + "\n".join(false_passes))

    def test_all_wrong_answers_rejected_cleanly(self):
        wrong_fails = [
            f"{r['id']}: {r['wrong_answer_message']}"
            for r in self.results.values()
            if not r["wrong_answer_pass"]
        ]
        self.assertEqual(len(wrong_fails), 0, f"Wrong answer handling failures:\n" + "\n".join(wrong_fails))


if __name__ == "__main__":
    unittest.main()
