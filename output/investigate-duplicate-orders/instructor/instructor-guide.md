# Instructor Guide — Investigate Duplicate Orders

## What this lab is really testing

Most beginners can write a `JOIN` and a `GROUP BY`. This lab checks whether
they stop to ask "what does one row of this table represent?" before
joining it to anything — the single habit that prevents the majority of
double-counted-revenue incidents in production analytics.

## Root cause, in one sentence

The `orders` table is append-only (one row per status change) but everyone
downstream treats it as one row per order, so joining it to `order_items`
multiplies line-item revenue by however many status updates that order has
had.

## Before / after (verified by running the queries against `lab.db`)

| | Rows | Total revenue |
|---|---|---|
| Buggy dashboard query (`starter/dashboard_query.sql`) | 17 | $490.00 |
| Trusted query (`instructor/solution/solution.sql`) | 12 | $359.00 |

`orders` itself has 18 physical rows for 12 distinct `order_id`s — the fan
-out already starts before the join to `order_items` even happens.

## Dataset cheat sheet

| `order_id` | Versions | Why it's interesting |
|---|---|---|
| O-1002 | 2 | Ordinary late-arriving status update (`created` → `paid`) |
| O-1004 | 3 | Three updates; latest (`refunded`) must win |
| O-1007 | 2 | `created` → `cancelled`; tests that "latest" isn't always `paid` |
| O-1009 | 2 | **Identical** `updated_at` on both rows (webhook replay) — needs the `order_version` tie-break |
| O-1011 | 2 | **Both** rows have `NULL updated_at` — needs `COALESCE(updated_at, order_ts)` *and* the tie-break, since `order_ts` is identical on both rows too |
| O-1005 | 1 | Guest checkout, `NULL customer_id` — a red herring; it doesn't affect grain or revenue, only trips up students who assume every `NULL` is "the bug" |
| O-1008 | 1 | One `order_items` line has `NULL unit_price` — tests whether students notice `SUM()` silently drops it |
| O-1099 (items only) | — | Orphaned `order_items` row with no matching order — correctly disappears via `INNER JOIN`; worth a verbal callout even though it's not graded |

## Where students typically go wrong

- Deduplicating with `MAX(updated_at)` and a plain `GROUP BY orders.*`
  instead of `ROW_NUMBER()` — this only works if every non-grouped column
  is functionally dependent on the max, which silently breaks the moment
  two versions differ in `status` (SQLite will accept it and return
  whichever row it feels like for the ungrouped columns; stricter engines
  would reject the query outright). Use this as a teaching moment about
  why `ROW_NUMBER() ... WHERE rn = 1` is the more portable pattern.
- Forgetting the `order_version` tie-break and being surprised that
  O-1009 or O-1011 still produces "close but not exact" numbers.
- Fixing the join by adding more `GROUP BY` columns instead of fixing the
  grain mismatch — this hides the symptom for this dataset but doesn't
  generalize (see `troubleshooting.md`).
- Dropping the `NULL unit_price` row with a `WHERE unit_price IS NOT NULL`
  filter instead of `COALESCE`-ing it — numerically this happens to match
  (0 vs. filtered out) for this dataset, but it destroys the ability to
  flag `has_missing_price`, which is the actual point of Task 4.

## Grading

Run `python tests/test_solution.py` against the student's `solution.sql`.
All three checks (`test_has_required_columns`, `test_one_row_per_order`,
`test_matches_trusted_revenue`) must pass. There's no partial credit built
into the script — if the intent is to grade tasks individually, use the
per-order breakdown in `tests/expected_orders.csv` as an answer key instead
of the automated pass/fail.
