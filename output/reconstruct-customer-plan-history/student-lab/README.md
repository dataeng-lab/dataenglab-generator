# Reconstruct Customer Plan History

**Level:** Beginner-to-Intermediate · **Duration:** ~25-30 min · **Tags:** SQL, slowly changing dimensions, window functions, effective-dated history

## Business context

Marketing analytics wants a revenue-by-pricing-tier report: for every
historical order, which plan (`Starter` / `Pro` / `Enterprise`) was the
customer actually on *at the moment they placed that order*?

The current report just joins `orders` to `customers.current_plan` — but
`current_plan` is overwritten in place every time a customer changes plans.
There is no history in that column. The result: every order a customer has
ever placed gets attributed to whatever plan they happen to be on **today**,
even orders placed months before their most recent upgrade. Finance has
noticed pricing-tier revenue numbers that don't reconcile with what the
billing system reports.

You have three tables to work with:

- `customers` — one row per customer, holding only their **current** plan.
  No history.
- `customer_plan_events` — a separate log table. One row is written every
  time a customer's plan changes, with the plan they changed **to** and the
  timestamp it took effect. Not every customer appears here (see Task 3).
- `orders` — one row per order, with a timestamp and amount.

The current (buggy) report lives in
[`starter/naive_report.sql`](starter/naive_report.sql). Don't edit it — it's
your reference for what's currently in production. Your fix goes in
[`starter/solution.sql`](starter/solution.sql).

## Environment

- Python 3.9+ (only the standard library — `sqlite3` and `unittest` ship
  with Python; no installs needed)
- No Docker, no network access required

## Setup

```bash
python build_db.py
```

This (re)builds `lab.db` from the CSVs in `datasets/`. Re-run it any time
you want to reset the database to its original state (see **Reset
procedure** below).

## Tasks

### Task 1 — Reproduce the misattribution

Run the current report and look specifically at customer `C-01` (Acme Inc),
who has changed plans twice:

```bash
python -c "
import sqlite3
conn = sqlite3.connect('lab.db')
cur = conn.cursor()
cur.execute(open('starter/naive_report.sql').read())
for row in cur.fetchall():
    print(row)
"
```

`C-01` placed an order back in February, another in April, and another in
July. Now compare those timestamps to `C-01`'s rows in
`customer_plan_events`. The naive report labels **all three** orders
`Enterprise` — the plan `C-01` is on today — even though the February order
happened while they were still on `Starter`, and the April order happened
while they were on `Pro`. Confirm this mismatch for yourself before moving
on.

### Task 2 — Reconstruct effective-dated plan versions

For customers who *do* appear in `customer_plan_events`, turn their rows
into a sequence of plan "versions", each with a `valid_from` (the event's
`changed_at`) and a `valid_to` (the *next* event's `changed_at`, or open-
ended if it's their most recent event). The SQL window function
`LEAD(changed_at) OVER (PARTITION BY customer_id ORDER BY changed_at)` gets
you most of the way there.

One thing will trip up a naive `ORDER BY changed_at` alone: customer `C-04`
has **two events stamped with the exact same `changed_at`**
(`2024-04-10 14:00:00`) — one says they moved to `Pro`, the other (written
moments later by a retrying billing webhook) says `Enterprise`. Without a
tie-break, SQL doesn't guarantee which of the two rows `LEAD()` treats as
"first" — you could end up with `Enterprise` (correct, matches
`customers.current_plan`) or, just as easily, the two rows swapped, which
would make `Pro` look like the customer's permanent, open-ended current
plan. Add `event_id` as a secondary `ORDER BY` key (higher `event_id` =
happened later, even when the timestamp column doesn't have enough
precision to prove it) so the sequence is fully deterministic.

### Task 3 — Handle customers with no event history at all

Customer `C-03` (Gamma Co) **never appears in `customer_plan_events`** —
not because their history is missing, but because they have never changed
plans since they signed up. For a customer like this, `customers.current_plan`
*is* their entire history: it has applied continuously since `signup_ts`,
with no upper bound.

Build a second set of "versions" — one per customer with zero rows in
`customer_plan_events` — using `current_plan` and `signup_ts`, and combine
it with the versions from Task 2 (`UNION ALL`) into one table of all known
plan versions for all customers.

### Task 4 — Join each order to the version in effect at order time, and flag what you can't determine

Join `orders` to your combined versions on `customer_id`, keeping only the
version where `order_ts` falls in `[valid_from, valid_to)` (inclusive
start, exclusive end — this matters for orders placed at the exact instant
a plan change took effect).

Use a `LEFT JOIN`, not an inner join. Customer `C-06` (Zeta Group) placed an
order on `2024-02-15`, but their *earliest* logged event isn't until
`2024-03-01` — the order predates recorded history. This is **not** the
same situation as `C-03`: `C-06` clearly changed plans at least once (that's
why an event exists at all), so we have no basis for assuming any particular
plan applied before that first event. Do not guess by using the first known
plan retroactively — leave `plan_at_order` as `NULL` for orders like this,
and flag them so the report is honest about what it doesn't know.

### Task 5 — Assemble and verify the final query

Combine Tasks 2-4 into a single query in `starter/solution.sql` that returns
exactly one row per `order_id`, with columns:

```
order_id, customer_id, order_ts, amount, plan_at_order, plan_source
```

`plan_source` must be one of:
- `reconstructed` — determined from `customer_plan_events`
- `current_plan_only` — customer never appears in `customer_plan_events`
- `unknown_pre_history` — order predates the customer's earliest logged
  event; `plan_at_order` must be `NULL`

Verify it yourself before running the automated check:

```sql
-- should return 0 rows
SELECT order_id, COUNT(*) FROM (<your query>) GROUP BY order_id HAVING COUNT(*) > 1;
```

## Hints

Stuck? Expand only the hint you need.

<details>
<summary>Hint for Task 2 (building valid_from/valid_to)</summary>

```sql
SELECT
    customer_id,
    plan,
    changed_at AS valid_from,
    LEAD(changed_at) OVER (
        PARTITION BY customer_id
        ORDER BY changed_at, event_id
    ) AS valid_to
FROM customer_plan_events;
```

The last event for each customer gets `valid_to = NULL` automatically —
`LEAD()` returns `NULL` when there's no next row in the partition. That's
exactly the "open-ended, still current" case you want.
</details>

<details>
<summary>Hint for Task 3 (customers with zero events)</summary>

```sql
SELECT customer_id, current_plan AS plan, signup_ts AS valid_from, NULL AS valid_to
FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM customer_plan_events);
```

`UNION ALL` this with your Task 2 result (matching column order/names) to
get one combined table of plan versions covering every customer.
</details>

<details>
<summary>Hint for Task 4 (the join condition and the LEFT JOIN)</summary>

```sql
FROM orders o
LEFT JOIN all_versions v
    ON v.customer_id = o.customer_id
    AND o.order_ts >= v.valid_from
    AND (v.valid_to IS NULL OR o.order_ts < v.valid_to)
```

If no version matches, `v.plan` comes back `NULL` on the `LEFT JOIN` — use
`COALESCE` (or a `CASE`) on `v.plan_source` (or an equivalent marker column
you carry through from Task 2/3) to turn that into the literal string
`'unknown_pre_history'` rather than leaving `plan_source` `NULL` too.
</details>

## Expected output

15 rows, one per order. 14 have a known `plan_at_order` (either
`reconstructed` or `current_plan_only`); exactly one — `O-013`, for
customer `C-06` — has `plan_at_order = NULL` and
`plan_source = 'unknown_pre_history'`. See
`instructor/instructor-guide.md` for the full before/after revenue-by-plan
breakdown.

## Validation

```bash
python build_db.py
python tests/test_solution.py
```

Both commands run from inside `student-lab/`. `test_solution.py` checks
required columns, one-row-per-order grain, valid `plan_source` values, and
an exact match against `tests/expected_orders.csv` for every order
(including the `NULL` case). It exits non-zero on any failure. Matches
`validate.json` at this lab's root exactly.

## Reset procedure

`python build_db.py` — rebuilds `lab.db` from the original CSVs at any
time; the starter files themselves are never modified by setup/reset.

## Troubleshooting

- **`lab.db not found`** — run `python build_db.py` first.
- **`sqlite3.OperationalError: near "SELECT": syntax error`** — check that
  you replaced the entire `SELECT 1;` placeholder in `solution.sql`, not
  appended your query after it.
- **`C-04`'s orders come out `Pro` instead of `Enterprise` for anything on
  or after `2024-04-10 14:00:00`** — your `ORDER BY` inside the `LEAD()`
  window is missing the `event_id` tie-break, so the two same-timestamp
  events for `C-04` aren't in a guaranteed order.
- **`O-013` comes out `Pro` instead of `NULL`** — you're using an `INNER
  JOIN` (which would just drop the row) or your `LEFT JOIN` result is
  falling back to the customer's `current_plan`/first event instead of
  leaving `plan_at_order` unmatched. Only rows that fall inside an actual
  `[valid_from, valid_to)` window should get a plan.
- **Row count is less than 15** — you likely used an `INNER JOIN` in Task 4;
  `O-013` has no matching version by design and must still appear in the
  output with `plan_at_order = NULL` via a `LEFT JOIN`.
- **`C-03`'s orders come out with `plan_at_order = NULL`** — `C-03` has zero
  rows in `customer_plan_events`; make sure your Task 3 branch (using
  `current_plan`/`signup_ts`) is actually included in the `UNION ALL`.
