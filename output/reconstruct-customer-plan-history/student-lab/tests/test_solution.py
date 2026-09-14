"""Validation for the "Reconstruct Customer Plan History" lab.

Run from inside student-lab/:
    python tests/test_solution.py

Exits non-zero (via unittest) if starter/solution.sql does not yet return
one correctly plan-attributed row per order.
"""
import csv
import sqlite3
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "lab.db"
SOLUTION_PATH = ROOT / "starter" / "solution.sql"
EXPECTED_PATH = ROOT / "tests" / "expected_orders.csv"

REQUIRED_COLUMNS = ("order_id", "customer_id", "order_ts", "amount", "plan_at_order", "plan_source")
VALID_SOURCES = {"reconstructed", "current_plan_only", "unknown_pre_history"}


def _norm(value):
    """Treat '' and None as the same thing (NULL) when comparing CSV vs sqlite3 results."""
    if value is None or value == "":
        return None
    return value


class TestPlanAtOrder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not DB_PATH.exists():
            raise RuntimeError(
                "lab.db not found. Run `python build_db.py` first (see README.md)."
            )
        cls.conn = sqlite3.connect(str(DB_PATH))

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def _run_solution(self):
        sql = SOLUTION_PATH.read_text(encoding="utf-8")
        cur = self.conn.cursor()
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        return cols, rows

    def test_has_required_columns(self):
        cols, _ = self._run_solution()
        for col in REQUIRED_COLUMNS:
            self.assertIn(col, cols, f"result is missing a `{col}` column")

    def test_one_row_per_order(self):
        cols, rows = self._run_solution()
        idx = cols.index("order_id")
        order_ids = [r[idx] for r in rows]
        self.assertEqual(
            len(order_ids),
            len(set(order_ids)),
            "duplicate order_id found in the result — grain is not one row per order",
        )

    def test_plan_source_values_are_valid(self):
        cols, rows = self._run_solution()
        idx = cols.index("plan_source")
        for r in rows:
            self.assertIn(
                r[idx],
                VALID_SOURCES,
                f"unexpected plan_source value {r[idx]!r} — must be one of {sorted(VALID_SOURCES)}",
            )

    def test_matches_expected_plan_attribution(self):
        cols, rows = self._run_solution()
        idx = {c: i for i, c in enumerate(cols)}

        actual = {}
        for r in rows:
            actual[r[idx["order_id"]]] = (
                str(r[idx["customer_id"]]),
                str(r[idx["order_ts"]]),
                round(float(r[idx["amount"]]), 2),
                _norm(r[idx["plan_at_order"]]),
                str(r[idx["plan_source"]]),
            )

        expected = {}
        with open(EXPECTED_PATH, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                expected[row["order_id"]] = (
                    row["customer_id"],
                    row["order_ts"],
                    round(float(row["amount"]), 2),
                    _norm(row["plan_at_order"]),
                    row["plan_source"],
                )

        self.assertEqual(
            set(actual.keys()),
            set(expected.keys()),
            "result order_ids don't match the expected order list (missing or extra orders)",
        )
        for order_id, exp in expected.items():
            self.assertEqual(
                actual[order_id],
                exp,
                f"mismatch for {order_id}: expected {exp}, got {actual[order_id]}",
            )


if __name__ == "__main__":
    unittest.main()
