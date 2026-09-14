# Troubleshooting — Investigate Duplicate Orders (instructor-facing)

**"My query passes test_one_row_per_order but fails test_matches_trusted_revenue"**
Grain is fixed but a value is wrong. Ask the student to check, in order:
1. Did they aggregate `order_items` *before* joining, or after? Joining
   first and grouping by `order_id` afterward can still produce the right
   row count while summing the wrong amount if their dedup step kept a
   different order version than the one with the "true" latest status.
2. Did they `COALESCE(unit_price, 0)` on O-1008's `NULL` line, or did they
   filter it out with `WHERE unit_price IS NOT NULL`? For this dataset both
   give the same number, so if revenue is right but `has_missing_price` is
   missing or always 0, that's the tell.

**"My query returns 17 rows, not 12 — I don't see what I'm missing"**
Almost always the `order_version` tie-break is missing. `ORDER BY
COALESCE(updated_at, order_ts) DESC` alone leaves O-1009 and O-1011 tied,
and depending on the SQL engine's stability guarantees, `ROW_NUMBER()` can
assign `rn = 1` to *both* rows in a tie unless the `ORDER BY` is fully
deterministic. Have them add `, order_version DESC` to the `ORDER BY`.

**"I get a syntax error near SELECT"**
The starter `solution.sql` ships with a placeholder `SELECT 1;` comment
block above it. Make sure the whole placeholder statement was replaced,
not appended to.

**"Should cancelled/refunded orders count as revenue?"**
Deliberately left open in this lab — the task only asks for one reliable
row per order with whatever the latest status is, not a business rule
about what counts as revenue. If a student asks, that's a good moment to
point out that "grain" and "business definition of revenue" are two
separate problems, and this lab only tackles the first one.

**A student "fixes" the orphaned `O-1099` line item**
There's nothing to fix — it has no matching `order_id` in `orders` and is
correctly excluded by the inner join. If a student adds a `LEFT JOIN` to
try to surface it, they'll get a row with `order_id = NULL` on the orders
side, which breaks `test_one_row_per_order`'s implicit assumption and is a
good opportunity to discuss why `LEFT JOIN` isn't a free upgrade over
`INNER JOIN` — it just changes what gets hidden.
