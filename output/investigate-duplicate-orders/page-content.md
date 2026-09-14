# Page content: Investigate Duplicate Orders

## Badges
Price: Free | Topic: SQL | Level: Beginner
Duration: 25 min | Tasks: 5

## Lede
A revenue dashboard is double-counting sales. Finance noticed the dashboard's total doesn't match the payment processor, and a few order IDs show up more than once in exports. You've been asked to trace the issue and hand back a query the dashboard team can trust.

## Outcomes (checklist)
- Determine a table's actual grain from its data, not from its name
- Explain how joining tables at mismatched grains fans out rows and inflates totals
- Deduplicate late-arriving records deterministically with `ROW_NUMBER()`, including NULLs and exact ties
- Aggregate to the correct grain before joining instead of joining raw and hoping `GROUP BY` fixes it
- Surface a data-quality flag instead of letting `SUM()` silently drop a NULL value

## Environment (one block per table/data source)

### orders — grain: 1 row per status update
An append-only, event-sourced fact table: a new row is written every time an order's status changes, so the table holds one row per status update, not one row per order. `order_id` is the business/natural key and repeats across versions; `event_id` is the surrogate primary key for each individual version row.

| key | field | type | description |
|-----|-------|------|-------------|
| PK | event_id | integer | Surrogate primary key for this version row |
| KEY | order_id | text | The order's business/natural key — repeats across versions |
| | customer_id | text | NULL for guest checkouts |
| | status | text | created / paid / refunded / cancelled |
| | order_ts | timestamp | When the order was first created |
| | updated_at | timestamp | When this version row was written; NULL on the very first event |
| | order_version | integer | Increases every time a new row is appended for this order |

### order_items — grain: 1 row per line item
A line-item-grain fact table — the correct child grain for joining to an order-grain parent. One row per line item per order is expected and correct; several rows per order_id here are not a bug.

| key | field | type | description |
|-----|-------|------|-------------|
| PK | order_item_id | text | Primary key |
| FK | order_id | text | Foreign key → orders.order_id |
| | sku | text | Product SKU |
| | quantity | integer | Units ordered |
| | unit_price | numeric | NULL on a few rows — a known upstream data gap |

## Tasks

### Task 1 — Reproduce the Bug
Run the current dashboard query (`starter/dashboard_query.sql`, provided as-is — don't edit it) and compare its row count to the number of distinct orders. The dashboard returns more rows than there are orders, and a noticeably higher total revenue. Confirm this for yourself before moving on.

### Task 2 — Find the Grain Problem
Query `orders` directly. Some order_ids appear 2 or 3 times — look at their status, updated_at and order_version. The table isn't at one-row-per-order grain; it's at one-row-per-status-update grain, and that's exactly what fans out when it's joined to order_items.

### Task 3 — Deduplicate to One Row per Order
Keep only the latest version of each order. `orders` is an append-only, event-sourced fact — "the current state of an order" isn't handed to you as one row per key, it has to be derived by picking one row per business key out of every version that was ever written.

A naive `SELECT * FROM orders GROUP BY order_id` looks like it dedupes, but it doesn't reliably: most engines, SQLite included, allow non-aggregated columns in the SELECT list that aren't in the GROUP BY, and silently return an arbitrary row's value for them. `GROUP BY order_id` only guarantees one row per order — it does not guarantee that row is the *latest* one, and which row you get can be undefined behavior. A correlated-subquery approach using `MAX(updated_at)` doesn't fully solve it either: `updated_at` is NULL on an order's very first row, and under standard NULL semantics comparisons against NULL (`>`, `MAX()`, `ORDER BY`) silently exclude or mishandle that row. And at least one order has two rows sharing the exact same `updated_at` (a replayed webhook) plus another with two rows that are both NULL, so "the row with the latest updated_at" isn't even unique — the tie has to be broken deterministically or the result isn't reproducible.

The reliable pattern for "latest row per key" is a window function: `COALESCE(updated_at, order_ts)` as the primary ordering key (falling back to `order_ts` exactly when `updated_at` is NULL), `order_version` as an explicit tie-break, and `ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY ...)` to rank rows within each order — then filter to `rn = 1`.

Hint: Partition by order_id, order by the coalesced timestamp then version, keep `rn = 1`.

### Task 4 — Fix the Join Instead of the Symptom
Even with orders deduplicated to one row per order, joining it straight to `order_items` and grouping is fragile — because that conflates two different problems into a single `GROUP BY`. `order_items` is correctly at line-item grain, so joining it to the order-grain `orders` table is a legitimate one-to-many join, unlike the status-update fan-out you just fixed in Task 3. But once you group by `order_id` to collapse that expected fan-out, every non-aggregated column you select (`status`, `customer_id`, ...) must either be in the `GROUP BY` clause or wrapped in an aggregate — miss that, and SQLite (like MySQL's non-strict mode) won't error, it will just hand back an arbitrary row's value for that column, which is easy to miss in review because the query still runs and mostly looks right.

Aggregating `order_items` to order grain first — one row per `order_id`, with revenue already summed — turns the second join into a clean 1:1 merge against your deduplicated orders, so there's no fan-out left to accidentally group away and no ambiguity about which row's `status` survives.

Separately, one line item has a NULL `unit_price`. `SUM()` ignores NULLs rather than propagating them, so `SUM(quantity * unit_price)` silently drops that line item's contribution to revenue instead of failing loudly — the total still looks plausible, just wrong. Use `COALESCE(unit_price, 0)` to make the zero explicit, and add a `has_missing_price` flag so anyone reading the output knows that order's revenue is incomplete rather than assuming it's exact.

Hint: Aggregate order_items to order grain in its own step before joining anything to it.

### Task 5 — Assemble and Verify the Trusted Query
Combine Tasks 3 and 4 into one query in `starter/solution.sql` returning exactly one row per order_id, with columns order_id, status, revenue, has_missing_price. Then run the automated check: `python tests/test_solution.py`. It checks required columns, one-row-per-order grain, and an exact match against the trusted revenue and status for every order — and exits non-zero if any check fails.

## Expected output
Your query should return 12 rows — one per order in the dataset — with combined revenue of $359.00. The unfixed dashboard query returns 17 rows and $490.00 for the same data.

## Troubleshooting
- **lab.db not found** — run `python build_db.py` first.
- **Still 17 rows instead of 12** — your dedup step isn't filtering to `rn = 1`, or the order_version tie-break is missing so two rows survive for an order with an exact-duplicate updated_at.
- **Revenue is close but not exact** — check the `COALESCE(unit_price, 0)` on the NULL-price line item, or confirm you're aggregating order_items before joining, not after.
