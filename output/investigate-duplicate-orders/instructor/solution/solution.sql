-- Instructor solution: one reliable row per order.
--
-- Fixes applied, in the same order as the student tasks:
--   1/2. Diagnosed that `orders` is at (order_id, version) grain, not
--        (order_id) grain — the pipeline appends a new row per status
--        change instead of updating in place.
--   3.   Deduplicated `orders` down to one row per order_id: the row with
--        the latest COALESCE(updated_at, order_ts), tie-broken by the
--        highest order_version (covers both the exact-duplicate replay on
--        O-1009 and the double-NULL updated_at on O-1011).
--   4.   Aggregated order_items to order grain BEFORE joining, so the join
--        is one-to-one instead of fanning out. COALESCE guards the NULL
--        unit_price on O-1008 so a bad line item contributes 0 instead of
--        making the whole SUM silently drop it unflagged.
--   5.   Surfaced a has_missing_price flag instead of hiding the data
--        quality issue, and the result is one row per order_id.

WITH latest_order AS (
    SELECT
        order_id,
        customer_id,
        status,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY COALESCE(updated_at, order_ts) DESC, order_version DESC
        ) AS rn
    FROM orders
),
deduped_order AS (
    SELECT order_id, customer_id, status
    FROM latest_order
    WHERE rn = 1
),
item_totals AS (
    SELECT
        order_id,
        SUM(COALESCE(quantity, 0) * COALESCE(unit_price, 0)) AS revenue,
        MAX(CASE WHEN unit_price IS NULL THEN 1 ELSE 0 END) AS has_missing_price
    FROM order_items
    GROUP BY order_id
)
SELECT
    d.order_id,
    d.customer_id,
    d.status,
    it.revenue,
    it.has_missing_price
FROM deduped_order d
JOIN item_totals it
    ON it.order_id = d.order_id
ORDER BY d.order_id;
