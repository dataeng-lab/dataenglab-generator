# Page content: Deduplicate Late-Arriving Order Events

## Badges
Price: Free | Topic: Python | Level: Beginner
Duration: 20 min | Tasks: 5

## Lede
Support escalated that a customer's order tracker shows an order as paid when it was actually refunded three days ago. The event delivery is at-least-once and can arrive out of order — you've been asked to trace the issue and hand back a script that produces the trusted, current status for every order.

## Outcomes (checklist)
- Recognize that a raw event log isn't the same as "current state," and that file row order isn't a reliable proxy for event chronology
- Deduplicate exact-duplicate deliveries before doing any further processing
- Deterministically pick the true latest record per key when the ordering column can be missing or tied
- Surface a dropped-duplicate signal instead of silently discarding the fact that a redelivery happened

## Environment (one block per table/data source)

### order_events — grain: 1 row per status-update delivery
One row is written every time an order's status changes, plus the occasional exact-duplicate redelivery — the table can hold more than one row per order, and one of those rows can be a pure duplicate.

| key | field | type | description |
|-----|-------|------|-------------|
| KEY | event_id | text | Delivery ID — repeats on an exact-duplicate redelivery |
| KEY | order_id | text | The order's business ID — repeats across status updates |
| | status | text | created / paid / refunded / cancelled |
| | event_ts | timestamp | When the event happened; missing on a few rows |
| | sequence_no | integer | Monotonic per-order delivery counter; always present |

## Tasks

### Task 1 — Reproduce the Bug
Run the current report (`starter/naive_report.py`, provided as-is — don't edit it) and compare its row count to the number of distinct orders. Then check its reported status for O-2008 against what the payments team confirms (refunded, not paid). Confirm this mismatch for yourself before moving on.

### Task 2 — Find Where the Extra Rows Come From
Look at `order_events.csv` grouped by order_id. Most orders with more than one row went through legitimate status changes — that's expected. One order, O-2003, has two byte-for-byte identical rows: the same delivery arriving twice, not a second update.

### Task 3 — Drop Exact Duplicate Deliveries
Remove rows that exactly match another row already kept (same event_id, order_id, status, event_ts and sequence_no), and remember which order_id(s) had one dropped so you can surface a had_duplicate_delivery flag instead of silently discarding the fact that a redelivery happened.
Hint: build a set of seen (event_id, order_id, status, event_ts, sequence_no) tuples and skip any row that repeats one.

### Task 4 — Pick the True Latest Event, Not the Last One in the File
Among the remaining rows for an order, the true latest event is the one with the greatest event_ts — except a few rows are missing event_ts entirely (treat any row with a real timestamp as later than one without), and a few tie on event_ts exactly. Use sequence_no as the tie-break whenever event_ts is missing or tied.
Hint: group by order_id, then pick `max(events, key=lambda r: (r["event_ts"] is not None, r["event_ts"] or "", r["sequence_no"]))`.

### Task 5 — Assemble and Verify
Combine Tasks 3–4 into `starter/dedupe.py` so it returns exactly one row per order_id: order_id, status, event_ts, had_duplicate_delivery. Then run the automated check: `python tests/test_solution.py`. It checks the output exists, has the required columns, one-row-per-order grain, and an exact match against the trusted result for every order — and exits non-zero if any check fails.

## Expected output
`output/orders_deduped.csv` should have 8 rows, one per order — including O-2008: refunded (not paid) and O-2004: cancelled (not paid).

## Troubleshooting
- **output/orders_deduped.csv not found when running the test** — run `python starter/dedupe.py` yourself first; the starter ships with `dedupe()` raising `NotImplementedError` until you implement it.
- **Still shows O-2008 as paid, not refunded** — you're likely still picking "the last row for this order_id in the file" instead of sorting by event_ts/sequence_no; O-2008's events arrive in the file out of chronological order.
- **O-2004 comes back paid instead of cancelled** — its two events share the exact same event_ts; you need sequence_no as the tie-break, not just event_ts alone.
