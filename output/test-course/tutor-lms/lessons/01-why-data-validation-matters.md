# Why Data Validation Matters

## Learning objective
Explain why raw data must be validated before it is used for reporting, and identify the categories of problems a validation step should catch.

## Prerequisites
Basic Python (variables, functions, for loops).

## Concept
Data rarely arrives clean. It comes from upstream systems — websites, APIs, third-party exports — that have their own bugs, retries and edge cases. If a pipeline trusts raw data blindly, bad rows silently corrupt downstream reports: revenue totals get inflated by duplicate orders, or averages get skewed by missing prices treated as zero.

A validation step has one job: look at every incoming row and decide whether it is trustworthy enough to use. Rows that fail should never be silently dropped (you lose the ability to investigate) and never crash the whole pipeline (one bad row shouldn't block thousands of good ones). Instead, they are set aside — quarantined — for a human or a downstream process to review.

Three common problems this course will handle:
- **Missing required values** — a field the business logic depends on (like a price) is empty.
- **Invalid values** — a field is present but nonsensical (like a negative quantity).
- **Duplicates** — the same business event (an order) appears more than once because of retries or re-exports.

## Architecture or data flow
```text
raw orders.csv
      │
      ▼
 [ validate ] ──invalid──▶ quarantine_orders.csv
      │
   valid rows
      │
      ▼
 [ deduplicate ]
      │
      ▼
 clean_orders.csv ──▶ reporting
```

## Practical example
Consider a single raw row:

```csv
order_id,book_title,quantity,unit_price,order_date
1002,The Pragmatic Programmer,1,,2026-01-05
```

The `unit_price` field is empty. If this row is loaded as-is, `quantity * unit_price` either crashes or silently becomes `NaN`, and any `SUM(revenue)` report built on top of it becomes unreliable without anyone noticing. The correct behavior is to flag this row as invalid and route it to a quarantine file, not to guess a price or drop the row without a trace.

## Common mistakes
- Treating a missing value as `0` instead of flagging it — this hides the problem instead of surfacing it.
- Dropping invalid rows with no record of what was dropped or why, making the issue impossible to debug later.
- Letting one malformed row crash the entire pipeline run instead of isolating just that row.

## Mini exercise
Look at these three rows and decide, for each, whether it is **valid**, **invalid (missing/invalid field)**, or **duplicate**:

```csv
order_id,book_title,quantity,unit_price,order_date
2001,Clean Code,2,25.00,2026-01-05
2002,Refactoring,-1,35.50,2026-01-06
2001,Clean Code,2,25.00,2026-01-05
```

## Expected result
- Row `2001` (first occurrence): valid.
- Row `2002`: invalid — quantity is negative.
- Row `2001` (second occurrence): duplicate — same `order_id` as an already-seen valid row.

## Summary
Validation exists to catch missing values, invalid values and duplicates before they reach reporting. Invalid rows are quarantined, not dropped silently or allowed to crash the pipeline.

## Next step
Lesson 2 shows how to detect these three problem categories in a full dataset at once using pandas boolean masks.
