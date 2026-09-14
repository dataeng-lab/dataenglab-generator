-- Schema for the "Investigate Duplicate Orders" lab.
-- Loaded automatically by build_db.py — you don't need to run this by hand.

CREATE TABLE orders (
    event_id      INTEGER PRIMARY KEY,
    order_id      TEXT    NOT NULL,
    customer_id   TEXT,               -- NULL for guest checkouts
    status        TEXT    NOT NULL,   -- created | paid | refunded | cancelled
    order_ts      TEXT    NOT NULL,   -- when the order was first created
    updated_at    TEXT,               -- when this status row was written; NULL on the very first event
    order_version INTEGER NOT NULL    -- increases every time the order pipeline appends a new row
);

CREATE TABLE order_items (
    order_item_id TEXT    PRIMARY KEY,
    order_id      TEXT    NOT NULL,
    sku           TEXT    NOT NULL,
    quantity      INTEGER NOT NULL,
    unit_price    REAL                -- NULL on a handful of rows: a known upstream data-quality gap
);
