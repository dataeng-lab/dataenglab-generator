"""Validation for the "Deduplicate Late-Arriving Order Events" lab.

Run from inside student-lab/:
    python tests/test_solution.py

Exits non-zero (via unittest) if starter/dedupe.py does not yet produce the
trusted one-row-per-order result.
"""
import csv
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEDUPE_SCRIPT = ROOT / "starter" / "dedupe.py"
OUTPUT_PATH = ROOT / "output" / "orders_deduped.csv"
EXPECTED_PATH = ROOT / "tests" / "expected_orders.csv"

REQUIRED_COLUMNS = ("order_id", "status", "event_ts", "had_duplicate_delivery")


def _read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class TestDedupedOrders(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if OUTPUT_PATH.exists():
            OUTPUT_PATH.unlink()
        cls.run_result = subprocess.run(
            [sys.executable, str(DEDUPE_SCRIPT)], cwd=ROOT, capture_output=True, text=True
        )
        cls.rows = _read_csv(OUTPUT_PATH) if OUTPUT_PATH.exists() else None

    def test_script_runs_and_writes_output(self):
        self.assertTrue(
            OUTPUT_PATH.exists(),
            "starter/dedupe.py did not produce output/orders_deduped.csv "
            f"(stdout: {self.run_result.stdout!r} stderr: {self.run_result.stderr!r})",
        )

    def test_has_required_columns(self):
        self.assertIsNotNone(self.rows, "no output to check — see previous failure")
        self.assertTrue(self.rows, "output/orders_deduped.csv has no rows")
        for col in REQUIRED_COLUMNS:
            self.assertIn(col, self.rows[0], f"result is missing a `{col}` column")

    def test_one_row_per_order(self):
        if self.rows is None:
            self.skipTest("no output to check — see test_script_runs_and_writes_output")
        order_ids = [r["order_id"] for r in self.rows]
        self.assertEqual(
            len(order_ids),
            len(set(order_ids)),
            "duplicate order_id found in the result — grain is not one row per order",
        )

    def test_matches_trusted_result(self):
        if self.rows is None:
            self.skipTest("no output to check — see test_script_runs_and_writes_output")
        expected = {
            r["order_id"]: (r["status"], r["event_ts"], r["had_duplicate_delivery"])
            for r in _read_csv(EXPECTED_PATH)
        }
        actual = {
            r["order_id"]: (r["status"], r["event_ts"], r["had_duplicate_delivery"])
            for r in self.rows
        }
        self.assertEqual(
            set(actual.keys()),
            set(expected.keys()),
            "result order_ids don't match the trusted order list (missing or extra orders)",
        )
        for order_id, exp in expected.items():
            self.assertEqual(
                actual[order_id], exp, f"mismatch for {order_id}: expected {exp}, got {actual[order_id]}"
            )


if __name__ == "__main__":
    unittest.main()
