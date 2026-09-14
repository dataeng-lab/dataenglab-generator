# Practical Lab Specification

## Business context
A marketing analytics team wants to know which pricing plan/tier a customer
was on at the moment each of their historical orders was placed, so revenue
can be reported correctly by tier. The `customers` table only stores each
customer's CURRENT plan — it's overwritten in place on every change, so
there's no history in that column. A separate `customer_plan_events` log
records every plan change with a timestamp. The current report joins orders
straight to `customers.current_plan`, silently attributing every historical
order to whatever plan the customer is on *today*, misattributing revenue to
the wrong pricing tier. The student plays the data engineer asked to trace
the root cause and hand back a query the marketing analytics team can trust.

## Learning objectives
By the end of the lab, students can:
- Recognize that a "current state" column overwritten in place carries no
  history, and identify when a companion event/change log is needed to
  reconstruct history instead.
- Turn a change-event log into effective-dated ("slowly changing dimension"
  style) intervals using `valid_from`/`valid_to`, computed with
  `LEAD() OVER (PARTITION BY ... ORDER BY ...)`.
- Handle two events sharing the exact same timestamp with a deterministic
  secondary sort key (`event_id`), and explain why an unordered tie
  produces non-deterministic — not just wrong — results.
- Distinguish "no event history exists because nothing ever changed" (the
  current value applies for all time) from "history exists but doesn't
  reach far enough back" (the value before recorded history is genuinely
  unknown and must not be guessed).
- Join a fact table to reconstructed effective-dated history using a
  half-open interval (`valid_from <= ts < valid_to`) and a `LEFT JOIN` so
  unmatched rows are surfaced with an explicit flag rather than silently
  dropped or misattributed.

## Environment
Python 3.9+ (standard library only — `sqlite3` and `unittest` ship with
Python; no `pip install`, no Docker, no network access). SQL runs against
SQLite.

## Estimated duration
25-30 minutes.

## Starter files
- `student-lab/build_db.py` — builds `lab.db` from the CSV datasets.
- `student-lab/starter/schema.sql` — table definitions (informational;
  applied automatically).
- `student-lab/starter/naive_report.sql` — the current, buggy
  revenue-by-plan report (read-only reference).
- `student-lab/starter/solution.sql` — where the student writes the fixed
  query.

## Dataset
`student-lab/datasets/customers.csv` (7 customers), `customer_plan_events.csv`
(12 change events across 6 of the 7 customers), and `orders.csv` (15 orders).
Deliberately encoded edge cases:
- **Never in the event log at all** — `C-03` (Gamma Co) has zero rows in
  `customer_plan_events`; their `current_plan` is their only history, valid
  since `signup_ts` with no upper bound.
- **Exact-timestamp tie** — `C-04` (Delta Corp) has two events
  (`event_id` 7 and 8) both stamped `2024-04-10 14:00:00` (one to `Pro`, one
  moments later to `Enterprise`, from a retrying billing webhook); requires
  an `event_id` tie-break so `LEAD()`'s ordering is deterministic and
  matches `current_plan` (`Enterprise`). An order (`O-009`) is placed at
  that exact boundary instant to test the half-open interval directly.
- **Order before recorded history begins** — `C-06` (Zeta Group) has one
  logged event (`Pro`, effective `2024-03-01`) but placed an order on
  `2024-02-15`, before that. The correct answer is `plan_at_order = NULL`
  with `plan_source = 'unknown_pre_history'` — not a guess based on the
  first known plan.
- **Simple control cases** — `C-01`, `C-02`, `C-05` upgrade cleanly with no
  ties, to confirm the baseline reconstruction logic works before the edge
  cases complicate it. `C-07` has exactly one event that matches
  `signup_ts`, distinguishing "one event, no history gap" from `C-03`'s
  "zero events."

## Tasks
1. Reproduce the misattribution by running `naive_report.sql` and comparing
   `C-01`'s three orders (spanning all three of their plan changes) against
   their `customer_plan_events` rows — all three come back `Enterprise`.
2. Reconstruct `valid_from`/`valid_to` plan versions from
   `customer_plan_events` using `LEAD()`, with `event_id` as a tie-break for
   the `C-04` timestamp collision.
3. Add a branch for customers with zero rows in `customer_plan_events`
   (`current_plan` valid since `signup_ts`, open-ended) and `UNION ALL` it
   with Task 2's versions.
4. `LEFT JOIN` orders to the combined versions on the half-open interval,
   leaving `plan_at_order` `NULL` and flagging `plan_source` when no version
   matches (pre-history orders).
5. Assemble the final query (`order_id, customer_id, order_ts, amount,
   plan_at_order, plan_source`) and verify one row per order.

## Hints
Provided as `<details>` blocks in `student-lab/README.md`, one per task
that needs one (Tasks 2, 3, and 4).

## Validation
```bash
python build_db.py
python tests/test_solution.py
```
Both commands run from inside `student-lab/`. `test_solution.py` checks
required columns, one-row-per-order grain, valid `plan_source` values, and
an exact match (including the `NULL` case) against
`tests/expected_orders.csv`. It exits non-zero on any failure. Matches
`validate.json` at this lab's root exactly.

## Expected output
15 rows, one per order; 14 with a determined `plan_at_order` and exactly one
(`O-013`) with `plan_at_order = NULL` / `plan_source = 'unknown_pre_history'`.
See `instructor/instructor-guide.md` for the full before/after
revenue-by-plan breakdown ($1,635.00 total in both cases — only the
per-tier split changes).

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
