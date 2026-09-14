-- This is the CURRENT marketing revenue-by-plan report, unmodified.
-- It is the one marketing analytics says is "misattributing revenue to the
-- wrong pricing tier". Read it, run it (Task 1), but do not edit it — it's
-- your reference for what NOT to do. Write your fix in solution.sql instead.

SELECT
    o.order_id,
    o.customer_id,
    o.order_ts,
    o.amount,
    c.current_plan AS plan_at_order
FROM orders o
JOIN customers c
    ON c.customer_id = o.customer_id;
