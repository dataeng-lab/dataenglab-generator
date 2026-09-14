-- Schema for the "Reconstruct Customer Plan History" lab.
-- Loaded automatically by build_db.py — you don't need to run this by hand.

CREATE TABLE customers (
    customer_id  TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    current_plan TEXT NOT NULL,   -- overwritten in place every time the plan changes; NO history
    signup_ts    TEXT NOT NULL
);

CREATE TABLE customer_plan_events (
    event_id    INTEGER PRIMARY KEY,
    customer_id TEXT    NOT NULL,   -- not every customer appears here (see README)
    plan        TEXT    NOT NULL,   -- the plan the customer changed TO at changed_at
    changed_at  TEXT    NOT NULL    -- at least one pair of rows shares an exact changed_at
);

CREATE TABLE orders (
    order_id    TEXT PRIMARY KEY,
    customer_id TEXT    NOT NULL,
    order_ts    TEXT    NOT NULL,
    amount      REAL    NOT NULL
);
