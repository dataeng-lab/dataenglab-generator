# Practical Lab Specification

## Business context
A revenue dashboard at an online store is double-counting sales. Finance
flagged that dashboard totals don't reconcile with the payment processor
and that some order IDs appear more than once in exports. The student
plays the data engineer asked to trace the root cause and hand back a
query the dashboard team can trust.

## Learning objectives
By the end of the lab, students can:
- Determine a table's actual grain from its data rather than assuming it
  from its name (`orders` looks like one-row-per-order but isn't).
- Explain how joining tables at mismatched grains fans out rows and
  inflates aggregates, and recognize the symptom (`COUNT(*)` of a result >
  `COUNT(DISTINCT key)`).
- Deduplicate late-arriving/duplicated records deterministically using
  `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)`, including handling
  `NULL` values and exact ties in the ordering column.
- Aggregate a table to the correct grain *before* joining instead of
  joining raw and hoping `GROUP BY` cleans it up afterward.
- Recognize that `SUM()` silently ignores `NULL`s, and surface a data
  quality flag instead of letting a bad value disappear unexplained.

## Environment
Python 3.9+ (standard library only — `sqlite3` and `unittest` ship with
Python; no `pip install`, no Docker, no network access).

## Estimated duration
25 minutes.

## Starter files
- `student-lab/build_db.py` — builds `lab.db` from the CSV datasets.
- `student-lab/starter/schema.sql` — table definitions (informational; applied automatically).
- `student-lab/starter/dashboard_query.sql` — the current, buggy dashboard query (read-only reference).
- `student-lab/starter/solution.sql` — where the student writes the fixed query.

## Dataset
`student-lab/datasets/orders.csv` (18 rows / 12 distinct `order_id`) and
`student-lab/datasets/order_items.csv` (20 rows, including one orphaned
`order_id` and one `NULL unit_price`). See inline comments in
`README.md` for the specific edge cases encoded: exact-duplicate
`updated_at` (webhook replay), double-`NULL` `updated_at` requiring a
tie-break, a guest order with `NULL customer_id`, and a `NULL unit_price`
line item.

## Tasks
1. Reproduce the bug by running the dashboard query and comparing its row
   count to `COUNT(DISTINCT order_id)`.
2. Diagnose the grain problem by grouping `orders` by `order_id` and
   finding the ones with more than one row.
3. Deduplicate `orders` to one row per `order_id` (latest version, with
   `COALESCE(updated_at, order_ts)` and an `order_version` tie-break).
4. Aggregate `order_items` to order grain before joining, and handle the
   `NULL unit_price` line item explicitly rather than letting `SUM` hide it.
5. Assemble the final query (one row per order: `order_id, status,
   revenue, has_missing_price`) and verify it has no duplicate `order_id`s.

## Hints
Provided as `<details>` blocks in `student-lab/README.md`, one per task
that needs one (Tasks 3 and 4), plus a note on the orphaned `order_items`
row so students don't spend time trying to "fix" it into appearing.

## Validation
```bash
python build_db.py
python tests/test_solution.py
```
Both commands run from inside `student-lab/`. `test_solution.py` checks
required columns, one-row-per-order grain, and exact revenue/status match
against `tests/expected_orders.csv`. It exits non-zero on any failure.
Matches `validate.json` at this lab's root exactly.

## Expected output
12 rows, one per `order_id`, total revenue **$359.00** (vs. $490.00 / 17
rows from the unfixed dashboard query — see
`instructor/instructor-guide.md` for the full before/after breakdown).

## Reset procedure
`python build_db.py` — rebuilds `lab.db` from the original CSVs at any
time; the starter files themselves are never modified by setup/reset.

## Troubleshooting
See `student-lab/README.md`'s Troubleshooting section (student-facing) and
`instructor/troubleshooting.md` (instructor-facing, covers common wrong
turns and how to steer students back).

## Instructor solution
`instructor/solution/solution.sql`, with `instructor/instructor-guide.md`
explaining the reasoning behind each fix and `instructor/troubleshooting.md`
covering common student mistakes.
