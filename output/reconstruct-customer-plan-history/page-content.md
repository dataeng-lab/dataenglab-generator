# Page content: Reconstruct Customer Plan History

## Badges
Price: Free | Topic: SQL | Level: Beginner-to-Intermediate
Duration: 25-30 min | Tasks: 5

## Lede
Marketing analytics wants to know which pricing plan a customer was on at
the moment each of their historical orders was placed — but the
`customers` table only stores their CURRENT plan, overwritten in place on
every change. Reconstruct effective-dated plan history from a separate
change-event log, then correctly attribute every order to the plan that
was actually in effect when it was placed.

## Outcomes (checklist)
- Recognize when a "current state" column has no history and a companion
  change log is needed to reconstruct it
- Turn a change-event log into effective-dated (`valid_from`/`valid_to`)
  intervals using `LEAD() OVER (PARTITION BY ... ORDER BY ...)`
- Resolve two events sharing the exact same timestamp with a deterministic
  tie-break, instead of leaving the result non-deterministic
- Tell apart "no history exists because nothing ever changed" from
  "history exists but doesn't reach back far enough" — and refuse to guess
  in the second case
- Join a fact table to reconstructed history on a half-open interval with a
  `LEFT JOIN`, surfacing unmatched rows with an explicit flag

## Environment (one block per table/data source)

### `customers` — grain: one row per customer
Current, overwritten-in-place state only. No history.
| key | field | type | description |
|-----|-------|------|-------------|
| PK | customer_id | TEXT | customer identifier |
|  | name | TEXT | customer/company name |
|  | current_plan | TEXT | plan as of right now (`Starter` / `Pro` / `Enterprise`) |
|  | signup_ts | TEXT | when the customer signed up |

### `customer_plan_events` — grain: one row per plan change
Not every customer appears here — some have never changed plans.
| key | field | type | description |
|-----|-------|------|-------------|
| PK | event_id | INTEGER | monotonically increasing; use as a tie-break when `changed_at` collides |
|  | customer_id | TEXT | which customer changed plans |
|  | plan | TEXT | the plan they changed **to** |
|  | changed_at | TEXT | when the change took effect |

### `orders` — grain: one row per order
| key | field | type | description |
|-----|-------|------|-------------|
| PK | order_id | TEXT | order identifier |
|  | customer_id | TEXT | which customer placed the order |
|  | order_ts | TEXT | when the order was placed |
|  | amount | REAL | order amount |

## Tasks

### Task 1 — Reproduce the misattribution
Run `starter/naive_report.sql` and compare customer `C-01`'s three orders
(spanning all three of their plan changes) against their
`customer_plan_events` rows. All three orders come back `Enterprise` — the
plan `C-01` is on today — even though two of them happened while on
`Starter` and `Pro`.

### Task 2 — Reconstruct effective-dated plan versions
Turn `customer_plan_events` rows into `valid_from`/`valid_to` intervals with
`LEAD()`.
Hint: `ORDER BY changed_at, event_id` — `event_id` breaks the exact-timestamp
tie on customer `C-04`.

### Task 3 — Handle customers with no event history at all
Customer `C-03` never appears in `customer_plan_events` — their
`current_plan` is their whole history, valid since `signup_ts` forever.
Hint: build a second version set from `customers` for anyone missing from
`customer_plan_events`, and `UNION ALL` it with Task 2's result.

### Task 4 — Join orders to the version in effect, and flag what's unknown
`LEFT JOIN` orders to the combined versions on
`valid_from <= order_ts < valid_to`. Customer `C-06` placed an order before
their earliest logged event — leave `plan_at_order` `NULL` there instead of
guessing.
Hint: an `INNER JOIN` would silently drop that order; a `LEFT JOIN` keeps it
and lets you flag it.

### Task 5 — Assemble and verify
Combine everything into one query returning
`order_id, customer_id, order_ts, amount, plan_at_order, plan_source`, one
row per order.

## Expected output
15 rows, one per order. 14 have a determined `plan_at_order`; exactly one
(`O-013`) has `plan_at_order = NULL` and `plan_source = 'unknown_pre_history'`.
Both the naive and corrected reports total $1,635.00 overall — the bug
misallocates revenue between tiers, it doesn't lose or duplicate any of it.

## Troubleshooting
- `lab.db not found` — run `python build_db.py` first.
- `C-04`'s orders on/after `2024-04-10 14:00:00` come out `Pro` instead of
  `Enterprise`, or flip between runs — missing the `event_id` tie-break in
  the `LEAD()` window's `ORDER BY`.
- Row count under 15 — an `INNER JOIN` in Task 4 dropped `O-013`; it must
  survive via `LEFT JOIN` with `plan_at_order = NULL`.
- `C-03`'s orders come out `unknown_pre_history` — the Task 3 branch (zero-
  event customers) is missing from the `UNION ALL`.
