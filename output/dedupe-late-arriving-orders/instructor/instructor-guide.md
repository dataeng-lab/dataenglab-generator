# Instructor Guide — Deduplicate Late-Arriving Order Events

## What this lab is really testing

Most beginners can write a `for` loop that overwrites a dict by key. This
lab checks whether they stop to ask "what determines which row is
actually the latest?" before trusting file order — the single habit that
prevents stale-state bugs in any event-sourced or append-only pipeline.

## Root cause, in one sentence

`naive_report.py` trusts the physical order of rows in the file as a proxy
for chronological event order, but delivery is at-least-once (exact
duplicates) and can arrive out of order, so "last row in the file" is not
the same as "most recent event."

## Before / after (verified by running the scripts against the dataset)

| | O-2004 | O-2007 | O-2008 |
|---|---|---|---|
| Naive report (`starter/naive_report.py`) | paid | created | paid |
| Trusted result (`instructor/solution/dedupe.py`) | cancelled | paid | refunded |

`order_events.csv` has 16 physical rows for 8 distinct `order_id`s — one
of those extra rows is a pure duplicate (`O-2003`), the rest are
legitimate status updates.

## Dataset cheat sheet

| `order_id` | Rows | Why it's interesting |
|---|---|---|
| O-2001 | 1 | Baseline, no dedup needed |
| O-2002 | 2 | Ordinary update, file order matches chronology |
| O-2003 | 2 | **Exact duplicate** delivery — same `event_id`, identical row |
| O-2004 | 2 | **Identical `event_ts`** on both rows — needs the `sequence_no` tie-break |
| O-2005 | 2 | First event has **no `event_ts`**; second does — tests the missing-vs-present rule |
| O-2006 | 2 | **Both** events missing `event_ts` — relies purely on `sequence_no` |
| O-2007 | 2 | File order is **reversed** relative to `event_ts` — tests that students sort by timestamp, not file position |
| O-2008 | 3 | File order is **scrambled**; the true latest (`refunded`) appears first in the file — the headline "shows paid, should be refunded" bug |

## Where students typically go wrong

- Deduplicating by `order_id` alone (keeping "the last row per order_id
  seen") instead of first removing exact-duplicate deliveries — this
  usually still produces the right final status for this dataset, but
  destroys the ability to set `had_duplicate_delivery`, which is the
  actual point of Task 3.
- Sorting by `event_ts` alone without the `sequence_no` tie-break —
  passes on most orders but fails `O-2004` (identical timestamps) and
  `O-2006` (both missing).
- Treating a missing `event_ts` as sorting *before* an empty string (e.g.
  comparing `None` directly) — raises a `TypeError` in Python 3 the moment
  it hits `O-2005`/`O-2006`. Use the `(event_ts is not None, event_ts or
  "", sequence_no)` tuple pattern instead of comparing `None` to a string.
- Fixing the symptom by hardcoding `sorted(rows, key=..., reverse=True)[0]`
  without deduplicating first — for `O-2003` this happens to give the
  right status (the duplicate rows are identical anyway), but leaves
  `had_duplicate_delivery` unset, which is graded.

## Grading

Run `python tests/test_solution.py` against the student's `dedupe.py`. All
four checks must pass. There's no partial credit built into the script —
if the intent is to grade tasks individually, use the per-order breakdown
in `tests/expected_orders.csv` as an answer key instead of the automated
pass/fail.
