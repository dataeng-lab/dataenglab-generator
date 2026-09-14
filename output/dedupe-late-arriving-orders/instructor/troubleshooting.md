# Troubleshooting — Deduplicate Late-Arriving Order Events (instructor-facing)

**"My query passes test_one_row_per_order but fails test_matches_trusted_result"**
Grain is fixed but a value is wrong. Ask the student to check, in order:
1. Are they sorting with `event_ts` compared directly (including `None`)
   instead of the `(event_ts is not None, event_ts or "", sequence_no)`
   tuple? A direct comparison either raises a `TypeError` on `O-2005`/
   `O-2006` or (in languages without that guard) silently mis-sorts them.
2. Is `sequence_no` included as the *second* tie-break element, not the
   first? If it's compared before `event_ts`, orders with different real
   timestamps can still pick the wrong row.

**"had_duplicate_delivery is always 0"**
The duplicate-detection key almost always needs to include `event_id` —
if a student keys only on `(order_id, status, event_ts)`, that's usually
right for this dataset, but if they build the key *after* already
collapsing to one row per order, the duplicate signal is lost before it's
recorded. Have them log/print `duplicate_order_ids` right after Task 3,
before Task 4 runs.

**"My script raises a TypeError comparing NoneType and str"**
Somewhere `event_ts` (which can be `None`) is being compared directly
instead of going through the `event_ts or ""` fallback. Point them at
`O-2005` and `O-2006`, the two orders with a missing `event_ts`.

**"O-2004 comes back paid instead of cancelled"**
Both of `O-2004`'s rows have the *identical* `event_ts`
(`2026-02-01 11:00:00`). Without `sequence_no` as a tie-break, whichever
row happens to be considered "last" by the sort's stability wins — which
is implementation-dependent and easy to get wrong. `sequence_no` is the
one field guaranteed to be unique and monotonic per order.

**"Should I trust event_ts or sequence_no as the primary signal?"**
Deliberately event_ts-primary in this lab (it reflects when the event
actually happened; sequence_no is a delivery-order counter used only as a
fallback/tie-break). If a student argues sequence_no should be primary
instead, that's a reasonable real-world design discussion — but it
won't match `tests/expected_orders.csv` as written, since `O-2005`
specifically tests that a later real timestamp wins over an earlier
sequence number's absence of one.
