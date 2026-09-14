# Deduplicate Late-Arriving Order Events

**Level:** Beginner · **Duration:** ~20 min · **Tags:** deduplication, ordering, idempotency, NULLs

## Business context

Your checkout system emits an "order status" event every time an order
changes state (`created` → `paid` → `refunded`/`cancelled`). A CSV export
job ingests those events into `order_events.csv`, and a status report reads
that file assuming one row per order. Two things break that assumption:

- The webhook delivery is **at-least-once** — the same event occasionally
  gets redelivered as an exact duplicate.
- Delivery can arrive **out of order** — an earlier event sometimes reaches
  the file after a later one, because of retries or network delays.

Support just escalated: the customer-facing order tracker shows order
`O-2008` as **paid**, but the payments team's system says it was refunded
three days ago. You've been asked to find out why and hand back a script
that produces the trusted, current status for every order.

The current report lives in
[`starter/naive_report.py`](starter/naive_report.py). Don't edit it — it's
your reference for what's currently in production. Your fix goes in
[`starter/dedupe.py`](starter/dedupe.py).

## Environment

- Python 3.9+ (only the standard library — no installs needed)
- No Docker, no network access required

## Setup

```bash
python reset.py
```

This (re)creates an empty `output/` directory. Re-run it any time you want
to reset your working state (see **Reset procedure** below) — it never
touches `datasets/` or the starter files.

## Tasks

### Task 1 — Reproduce the bug

Run the current report:

```bash
python starter/naive_report.py
```

Compare `total event rows` to `distinct order_id` — there are more event
rows than orders. Then look at the "current status per order" list: does
`O-2008` say `paid`? That's the bug Support flagged. Confirm this for
yourself before moving on.

### Task 2 — Find where the extra rows come from

Look directly at `datasets/order_events.csv`, grouped by `order_id`. Some
orders have more than one event because they went through several
legitimate status changes — that's expected. But one order, `O-2003`, has
**two identical rows**: same `event_id`, same everything. That's not a
second update, it's the same delivery arriving twice.

### Task 3 — Drop exact duplicate deliveries

In `dedupe()`, remove rows that are byte-for-byte duplicates of another row
already kept (same `event_id`, `order_id`, `status`, `event_ts` and
`sequence_no`). While you're at it, remember which `order_id`s had at least
one duplicate dropped — you'll surface that as a `had_duplicate_delivery`
flag in the final output, rather than silently discarding the fact that a
redelivery happened.

### Task 4 — Pick the true latest event, not the last one in the file

`naive_report.py`'s bug is that it trusts *file order*, not *event order*.
Among the remaining rows for an order, the true latest event is the one
with the greatest `event_ts` — except:

- **Missing timestamps**: a few rows have no `event_ts` at all. Treat any
  row that *does* have a real `event_ts` as later than one that doesn't.
- **Ties**: at least one order has two rows with the exact same
  `event_ts` (a status-change race), and another has two rows that are
  *both* missing `event_ts`. Use `sequence_no` as the tie-break in both
  cases — it's always present and always reflects true delivery order.

### Task 5 — Assemble and verify

Combine Tasks 3–4 into `dedupe()` in `starter/dedupe.py` so it returns
exactly one row per `order_id`, with fields: `order_id`, `status`,
`event_ts`, `had_duplicate_delivery`. Run it and check your own output
before running the automated check:

```bash
python starter/dedupe.py
```

`output/orders_deduped.csv` should have exactly 8 rows (one per
`order_id`) — no duplicates.

## Hints

Stuck? Expand only the hint you need.

<details>
<summary>Hint for Task 3 (drop exact duplicates)</summary>

```python
seen = set()
deduped_rows = []
duplicate_order_ids = set()
for row in rows:
    key = (row["event_id"], row["order_id"], row["status"], row["event_ts"], row["sequence_no"])
    if key in seen:
        duplicate_order_ids.add(row["order_id"])
        continue
    seen.add(key)
    deduped_rows.append(row)
```
</details>

<details>
<summary>Hint for Task 4 (pick the true latest event)</summary>

Group the deduped rows by `order_id`, then for each group:

```python
latest = max(
    events,
    key=lambda r: (r["event_ts"] is not None, r["event_ts"] or "", r["sequence_no"]),
)
```

The tuple compares left to right: "has a real timestamp" beats "doesn't",
then the timestamp itself, then `sequence_no` breaks any remaining tie
(including when both timestamps are missing).
</details>

## Expected output

`output/orders_deduped.csv` should have 8 rows, one per order, matching
the trusted status for every order — including `O-2008: refunded` (not
`paid`) and `O-2004: cancelled` (not `paid`). See
`instructor/instructor-guide.md` for the full before/after breakdown.

## Validation

```bash
python tests/test_solution.py
```

Runs `starter/dedupe.py` and checks that its output:
1. exists and has the required columns,
2. has exactly one row per `order_id`,
3. matches the trusted status, timestamp and duplicate flag for every
   order.

Exits non-zero if any check fails.

## Reset procedure

```bash
python reset.py
```

Always starts from an empty `output/` directory; `datasets/` and the
starter files are never modified.

## Troubleshooting

- **`output/orders_deduped.csv not found` when running the test** — run
  `python starter/dedupe.py` yourself first and check it doesn't raise an
  error (the starter ships with `dedupe()` raising `NotImplementedError`
  until you implement it).
- **Still shows `O-2008` as `paid`, not `refunded`** — you're likely still
  picking "the last row for this order_id in the file" instead of sorting
  by `event_ts`/`sequence_no`; `O-2008`'s events arrive in the file out of
  chronological order.
- **`O-2004` comes back `paid` instead of `cancelled`** — its two events
  share the exact same `event_ts`; you need `sequence_no` as the tie-break,
  not just `event_ts` alone.
- **`had_duplicate_delivery` is `0` everywhere** — check that your
  duplicate-detection key really matches on `event_id` (and the other
  fields), and that you're recording the order_id *before* discarding the
  duplicate row.
