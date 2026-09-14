-- Instructor solution: one trusted row per real customer.
--
-- Fixes applied, in the same order as the student tasks:
--   1. Diagnosed that the production report (naive_report.sql) matches on
--      first_name + last_name, which wrongly merges two different real
--      customers who both happen to be named "John Smith".
--   2. Diagnosed that a raw `GROUP BY email` is unsafe in the other
--      direction too: it misses the Amy Chen group (case/whitespace
--      differences make the raw strings compare as distinct) and it
--      falsely clusters the two NULL-email guest checkouts together,
--      because SQL's GROUP BY treats all NULLs as one group.
--   3. Built a normalized dedupe_key: LOWER(TRIM(email)) for real emails,
--      and a per-row-unique fallback ('no-email-' || customer_id) for
--      NULL emails so guest checkouts can never collide with each other.
--   4. Picked one canonical row per dedupe_key deterministically (the
--      earliest created_at, tie-broken by customer_id), backfilled a
--      missing phone from any duplicate that has one (MAX ignores NULLs),
--      and summed loyalty_points across the group so consolidating
--      accounts doesn't destroy anyone's earned balance.
--   5. Result: exactly one row per real customer, total loyalty_points
--      conserved (590), and the two John Smiths remain separate.

WITH normalized AS (
    SELECT
        customer_id,
        CASE WHEN email IS NULL THEN NULL ELSE LOWER(TRIM(email)) END AS norm_email,
        CASE
            WHEN email IS NULL THEN 'no-email-' || customer_id
            ELSE LOWER(TRIM(email))
        END AS dedupe_key,
        first_name,
        last_name,
        phone,
        loyalty_points,
        created_at
    FROM customers
),
ranked AS (
    SELECT
        n.*,
        ROW_NUMBER() OVER (
            PARTITION BY dedupe_key
            ORDER BY created_at ASC, customer_id ASC
        ) AS rn,
        MAX(phone) OVER (PARTITION BY dedupe_key) AS filled_phone,
        SUM(loyalty_points) OVER (PARTITION BY dedupe_key) AS total_points,
        COUNT(*) OVER (PARTITION BY dedupe_key) AS duplicate_count
    FROM normalized n
)
SELECT
    customer_id,
    norm_email AS email,
    first_name,
    last_name,
    filled_phone AS phone,
    total_points AS loyalty_points,
    duplicate_count
FROM ranked
WHERE rn = 1
ORDER BY customer_id;
