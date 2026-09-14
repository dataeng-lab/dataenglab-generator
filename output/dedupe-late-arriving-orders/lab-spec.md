# Practical Lab Specification

## Business context
A checkout system's webhook delivery is at-least-once and can arrive out
of order. A CSV export job ingests these order-status events into
`order_events.csv`, and the current status report reads that file
assuming one row per order — so an exact-duplicate redelivery inflates
event counts, and an out-of-order delivery makes the report show a stale
status. Support escalated that order `O-2008` shows as `paid` when it was
actually refunded. The student plays the data engineer asked to write a
script that produces the trusted current status per order.

## Learning objectives
By the end of the lab, students can:
- Recognize that a raw event log is not the same as "current state," and
  that the file's physical row order is not a reliable proxy for event
  chronology.
- Deduplicate exact-duplicate deliveries (idempotency at ingestion) before
  doing any further processing.
- Deterministically pick the true latest record per key when the ordering
  column can be missing or tied, using a documented fallback + tie-break
  rule instead of an ad hoc `ORDER BY`/last-row heuristic.
- Surface a dropped-duplicate signal (`had_duplicate_delivery`) instead of
  silently discarding the fact that a redelivery happened.

## Environment
Python 3.9+ (standard library only — no `pip install`, no Docker, no
network access).

## Estimated duration
20 minutes.

## Starter files
- `student-lab/reset.py` — (re)creates an empty `output/` directory.
- `student-lab/starter/naive_report.py` — the current, buggy status report
  (read-only reference).
- `student-lab/starter/dedupe.py` — where the student implements `dedupe()`.

## Dataset
`student-lab/datasets/order_events.csv` (16 rows / 8 distinct `order_id`).
Edge cases encoded: an exact-duplicate delivery (`O-2003`, same `event_id`
twice), a same-timestamp status race requiring a `sequence_no` tie-break
(`O-2004`), a missing `event_ts` on the first event of an order (`O-2005`),
both events missing `event_ts` entirely (`O-2006`), and two out-of-order
deliveries where the physically later file row is chronologically earlier
(`O-2007`, `O-2008`).

## Tasks
1. Reproduce the bug by running `naive_report.py` and comparing its row
   count to `COUNT(DISTINCT order_id)`, and spotting the wrong status it
   reports for `O-2008`.
2. Diagnose the extra rows: distinguish legitimate multi-event orders from
   `O-2003`'s exact-duplicate redelivery.
3. Drop exact-duplicate deliveries, tracking which `order_id`s lost one.
4. Pick the true latest event per order: a real `event_ts` beats a missing
   one, and `sequence_no` breaks ties (including double-missing
   timestamps).
5. Assemble the final script (one row per order: `order_id, status,
   event_ts, had_duplicate_delivery`) and verify there are no duplicate
   `order_id`s.

## Hints
Provided as `<details>` blocks in `student-lab/README.md`, one per task
that needs one (Tasks 3 and 4).

## Validation
```bash
python reset.py
python tests/test_solution.py
```
Both commands run from inside `student-lab/`. `test_solution.py` runs
`starter/dedupe.py`, then checks the output exists, has the required
columns, is at one-row-per-order grain, and matches
`tests/expected_orders.csv` exactly. It exits non-zero on any failure.
Matches `validate.json` at this lab's root exactly.

## Expected output
8 rows, one per `order_id`, matching `tests/expected_orders.csv` — notably
`O-2008: refunded` (not `paid`) and `O-2004: cancelled` (not `paid`). See
`instructor/instructor-guide.md` for the full before/after breakdown.

## Reset procedure
`python reset.py` — recreates an empty `output/` directory at any time;
`datasets/` and the starter files are never modified by setup/reset.

## Troubleshooting
See `student-lab/README.md`'s Troubleshooting section (student-facing) and
`instructor/troubleshooting.md` (instructor-facing, covers common wrong
turns and how to steer students back).

## Instructor solution
`instructor/solution/dedupe.py`, with `instructor/instructor-guide.md`
explaining the reasoning behind each fix and `instructor/troubleshooting.md`
covering common student mistakes.
