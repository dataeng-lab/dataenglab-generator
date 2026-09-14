-- Instructor solution: correct plan-at-order attribution for every order.
--
-- Fixes applied, in the same order as the student tasks:
--   1. Diagnosed that `customers.current_plan` is a snapshot, not history:
--      the naive report joins every order straight to it, so any customer
--      who has ever changed plans gets ALL of their orders relabeled with
--      whatever plan they happen to be on today.
--   2. Reconstructed effective-dated plan "versions" from
--      customer_plan_events: valid_from = changed_at, valid_to = the next
--      event's changed_at (via LEAD), ordered by (changed_at, event_id) so
--      that C-04's two events sharing the exact same changed_at (Pro and
--      Enterprise both stamped 2024-04-10 14:00:00) resolve deterministically
--      — the higher event_id wins as "what actually ended up true", which
--      collapses Pro into a zero-width, unreachable interval and makes
--      Enterprise the version that starts at that instant. That matches
--      customers.current_plan for C-04 (Enterprise), which is a good sanity
--      check that the tie-break direction is correct.
--   3. Added a `no_history_versions` branch for customers with ZERO rows in
--      customer_plan_events (C-03): current_plan is presumed to have applied
--      since signup_ts, with no upper bound.
--   4. Joined orders to whichever version's [valid_from, valid_to) window
--      contains order_ts, using a LEFT JOIN so an order that falls before a
--      customer's EARLIEST logged event (C-06's 2024-02-15 order, before
--      their first event on 2024-03-01) matches no version at all instead of
--      being guessed. plan_at_order is left NULL and plan_source flags it as
--      'unknown_pre_history' rather than silently attributing it to
--      whatever the first known plan happens to be.
--   5. Every order gets exactly one row and one plan_source explaining how
--      its plan_at_order was determined (or why it couldn't be).

WITH ordered_events AS (
    SELECT
        customer_id,
        plan,
        changed_at,
        LEAD(changed_at) OVER (
            PARTITION BY customer_id
            ORDER BY changed_at, event_id
        ) AS valid_to
    FROM customer_plan_events
),
event_versions AS (
    SELECT
        customer_id,
        plan,
        changed_at AS valid_from,
        valid_to,
        'reconstructed' AS plan_source
    FROM ordered_events
),
no_history_versions AS (
    -- Customers who never appear in customer_plan_events at all: their
    -- current_plan IS their only history, valid since signup with no
    -- upper bound (edge case: C-03).
    SELECT
        customer_id,
        current_plan AS plan,
        signup_ts AS valid_from,
        NULL AS valid_to,
        'current_plan_only' AS plan_source
    FROM customers
    WHERE customer_id NOT IN (SELECT DISTINCT customer_id FROM customer_plan_events)
),
all_versions AS (
    SELECT * FROM event_versions
    UNION ALL
    SELECT * FROM no_history_versions
)
SELECT
    o.order_id,
    o.customer_id,
    o.order_ts,
    o.amount,
    v.plan AS plan_at_order,
    COALESCE(v.plan_source, 'unknown_pre_history') AS plan_source
FROM orders o
LEFT JOIN all_versions v
    ON v.customer_id = o.customer_id
    AND o.order_ts >= v.valid_from
    AND (v.valid_to IS NULL OR o.order_ts < v.valid_to)
ORDER BY o.order_id;
