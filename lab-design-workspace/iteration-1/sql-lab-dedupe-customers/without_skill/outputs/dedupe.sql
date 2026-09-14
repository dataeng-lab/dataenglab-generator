-- ============================================================
-- fix-duplicate-customers-eval-bl : instructor solution
--
-- Same contract as student-lab/starter/dedupe.sql: build a
-- customers_clean table with exactly one row per real customer.
-- ============================================================

DROP TABLE IF EXISTS customers_clean;

CREATE TABLE customers_clean AS
WITH normalized AS (
    SELECT
        customer_id,
        full_name,
        email,
        phone,
        signup_date,
        source_system,
        LOWER(TRIM(email)) AS normalized_email
    FROM customers
),
ranked AS (
    SELECT
        n.*,
        COUNT(*) OVER (PARTITION BY normalized_email) AS duplicate_count,
        ROW_NUMBER() OVER (
            PARTITION BY normalized_email
            ORDER BY signup_date ASC, customer_id ASC
        ) AS row_rank
    FROM normalized n
)
SELECT
    customer_id,
    full_name,
    normalized_email AS email,
    phone,
    signup_date,
    source_system,
    duplicate_count
FROM ranked
WHERE row_rank = 1;
