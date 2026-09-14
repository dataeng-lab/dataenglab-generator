-- This is the CURRENT revenue dashboard query, unmodified.
-- It is the one the finance team says is "double-counting sales".
-- Read it, run it (Task 1), but do not edit it — it's your reference for
-- what NOT to do. Write your fix in solution.sql instead.

SELECT
    o.order_id,
    o.status,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM orders o
JOIN order_items oi
    ON oi.order_id = o.order_id
GROUP BY
    o.order_id,
    o.status;
