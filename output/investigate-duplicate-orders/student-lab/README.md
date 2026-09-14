# Investigate Duplicate Orders

**Level:** Beginner · **Duration:** ~25 min · **Tags:** JOIN, grain, deduplication, NULLs

## Business context

The revenue dashboard for an online store is double-counting sales. Finance
noticed that the dashboard's total revenue doesn't match the payment
processor's numbers, and a few order IDs appear more than once in the
export. You've been asked to find out why and hand back a query the
dashboard team can trust.

You have two tables to work with:

- `orders` — an append-only, event-sourced fact table: a new row is written
  every time an order's status changes (`created` → `paid` →
  `refunded`/`cancelled`). `order_id` is the business/natural key and
  repeats across versions; `event_id` is the surrogate primary key for each
  individual version row. The table's *intended* grain is one row per
  order, but because ingestion appends rather than updates, its *actual*
  grain is one row per status update.
- `order_items` — a line-item-grain fact table, the correct child grain for
  joining to an order-grain parent. Several rows per `order_id` here are
  expected and correct — this table's grain is not the problem.

The current dashboard query lives in [`starter/dashboard_query.sql`](starter/dashboard_query.sql).
Don't edit it — it's your reference for what's currently in production.
Your fixed version goes in [`starter/solution.sql`](starter/solution.sql).

## Environment

- Python 3.9+ (only the standard library — no installs needed)
- No Docker, no network access required

## Setup

```bash
python build_db.py
```

This (re)builds `lab.db` from the CSVs in `datasets/`. Re-run it any time
you want to reset the database to its original state (see **Reset
procedure** below).

## Tasks

### Task 1 — Reproduce the bug

Run the current dashboard query and compare its row count to the number of
distinct orders:

```bash
python -c "
import sqlite3
conn = sqlite3.connect('lab.db')
cur = conn.cursor()
cur.execute(open('starter/dashboard_query.sql').read())
rows = cur.fetchall()
print('dashboard rows:', len(rows))
print('distinct order_id in orders table:', cur.execute('SELECT COUNT(DISTINCT order_id) FROM orders').fetchone()[0])
"
```

The dashboard returns more rows than there are orders, and its total
revenue is noticeably higher than it should be. That's the double-counting
finance flagged. Confirm this for yourself before moving on.

### Task 2 — Find the grain problem

Query the `orders` table directly to see why:

```sql
SELECT order_id, COUNT(*)
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;
```

Some `order_id`s appear 2 or 3 times. Look at those rows' `status`,
`updated_at` and `order_version` columns. `orders` isn't at
one-row-per-order grain — it's at one-row-per-status-update grain. That
mismatch is what fans out when it's joined to `order_items`.

### Task 3 — Deduplicate `orders` down to one row per order

Write a query (you can prototype this directly against the database before
moving it into `solution.sql`) that keeps only the *latest* version of each
order: the row with the greatest `updated_at`.

A naive `SELECT * FROM orders GROUP BY order_id` looks like it dedupes, but
it isn't reliable: most engines, SQLite included, allow non-aggregated
columns in the SELECT list that aren't in the GROUP BY, and silently return
an *arbitrary* row's value for them. `GROUP BY order_id` alone only
guarantees one row per order — not that it's the latest one.

Two more things will trip up a naive `ORDER BY updated_at DESC` / `MAX(updated_at)`:

- **NULLs**: `updated_at` is `NULL` on an order's very first row (it's only
  stamped when an update happens). Use `COALESCE(updated_at, order_ts)` so
  the first version still has something to sort by.
- **Ties**: at least one order has two rows with the *identical*
  `updated_at` (a webhook retry that replayed the same event), and another
  has two rows that are *both* `NULL`. Add `order_version` as a tie-breaker
  so exactly one row wins per order regardless.

`ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY ... DESC) = 1` is the
standard way to do this in SQL — worth using here.

### Task 4 — Fix the join instead of the symptom

Even with `orders` deduplicated, joining it straight to `order_items` and
grouping is fragile, because it conflates two different problems into one
`GROUP BY`. `order_items` is legitimately one-to-many against `orders` (an
order can have several line items — that fan-out is correct, unlike the
status-update fan-out you just fixed). But once you group by `order_id` to
collapse it, every non-aggregated column you select (`status`,
`customer_id`, ...) must be in the GROUP BY or wrapped in an aggregate —
miss that, and SQLite (like MySQL's non-strict mode) won't error, it will
just hand back an arbitrary row's value for that column, which is easy to
miss because the query still runs and mostly looks right.

Aggregate `order_items` to order grain **first** (one row per `order_id`,
revenue summed) in its own step, then join that 1:1 to your deduplicated
orders — both sides are now one row per key, so there's no fan-out left to
accidentally group away.

While you're in `order_items`, notice that one line item has a `NULL`
`unit_price` (a known upstream data gap). Because `SUM()` silently ignores
`NULL` terms, that line's revenue just vanishes with no indication anything
was wrong. Use `COALESCE(unit_price, 0)` so it contributes 0 explicitly,
and add a `has_missing_price` flag (`1`/`0`) so the dashboard team can see
which orders have incomplete pricing data instead of an unexplained gap.

### Task 5 — Assemble and verify the trusted query

Combine Tasks 3 and 4 into a single query in `starter/solution.sql` that
returns exactly one row per `order_id`, with columns:
`order_id, status, revenue, has_missing_price`.

Verify it yourself before running the automated check:

```sql
-- should return 0 rows
SELECT order_id, COUNT(*) FROM (<your query>) GROUP BY order_id HAVING COUNT(*) > 1;
```

## Hints

Stuck? Expand only the hint you need.

<details>
<summary>Hint for Task 3 (dedup)</summary>

```sql
SELECT *, ROW_NUMBER() OVER (
    PARTITION BY order_id
    ORDER BY COALESCE(updated_at, order_ts) DESC, order_version DESC
) AS rn
FROM orders;
```

Keep only `rn = 1`.
</details>

<details>
<summary>Hint for Task 4 (aggregate before joining)</summary>

```sql
SELECT order_id, SUM(COALESCE(quantity, 0) * COALESCE(unit_price, 0)) AS revenue
FROM order_items
GROUP BY order_id;
```

Join this result to your deduplicated orders — both sides are now one row
per `order_id`, so the join can't fan out.
</details>

<details>
<summary>Hint: what about the order_item row for O-1099?</summary>

`order_items` has one line item whose `order_id` doesn't exist in `orders`
at all — an orphaned record. An inner join naturally excludes it from your
result. That's the right behavior here, but in a real pipeline you'd also
want a separate check that counts orphaned `order_items` rows so they don't
disappear unnoticed.
</details>

## Expected output

Your query, run against `lab.db`, should return 12 rows — one per order in
the dataset — with a combined revenue of **$359.00**. The unfixed dashboard
query returns 17 rows and a combined revenue of $490.00 for the same data.

## Validation

```bash
python tests/test_solution.py
```

Checks that `starter/solution.sql`:
1. returns the required columns,
2. returns exactly one row per `order_id`,
3. matches the trusted revenue and status for every order.

Exits non-zero if any check fails.

## Reset procedure

```bash
python build_db.py
```

Rebuilding always starts from the original CSVs in `datasets/`, so you can
reset at any point without losing the starter files.

## Troubleshooting

- **`lab.db not found`** — run `python build_db.py` first.
- **`sqlite3.OperationalError: near "SELECT": syntax error`** — check for a
  stray semicolon or comment left over from `solution.sql`'s starter
  template.
- **Revenue is close but not exact** — you're likely missing the
  `COALESCE(unit_price, 0)` on the `NULL`-price line item, or still
  joining `order_items` to `orders` before aggregating.
- **Still 17 rows instead of 12** — your dedup step isn't filtering to
  `rn = 1`, or the tie-break on `order_version` is missing so two rows
  survive for an order with an exact-duplicate `updated_at`.
