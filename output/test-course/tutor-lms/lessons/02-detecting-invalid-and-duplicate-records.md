# Detecting Invalid and Duplicate Records with pandas

## Learning objective
Use pandas boolean masks to identify rows with missing/invalid fields, and use `duplicated()` to identify repeated business keys.

## Prerequisites
Lesson 1 (Why Data Validation Matters). Basic Python.

## Concept
pandas lets you evaluate a condition across an entire column at once, producing a column of `True`/`False` values called a **boolean mask**. Combining masks with `&` (and) / `|` (or) lets you express validation rules declaratively, without writing a manual `for` loop over rows.

Two masks matter for this course:
- A mask for **invalid rows**: `unit_price` is missing (`isna()`) or not greater than zero, OR `quantity` is not greater than zero.
- A mask for **duplicate rows**: `duplicated(subset=["order_id"])` returns `True` for every occurrence of an `order_id` after its first appearance.

## Architecture or data flow
```text
DataFrame (all rows)
      │
      ├─ price_invalid   = df["unit_price"].isna() | (df["unit_price"] <= 0)
      ├─ quantity_invalid = df["quantity"] <= 0
      │
      ▼
 invalid_mask = price_invalid | quantity_invalid
      │
      ├── True  ─▶ quarantine
      └── False ─▶ candidate for clean output (still needs dedup)
```

## Practical example
```python
import pandas as pd

df = pd.read_csv("orders.csv")

price_invalid = df["unit_price"].isna() | (df["unit_price"] <= 0)
quantity_invalid = df["quantity"] <= 0
invalid_mask = price_invalid | quantity_invalid

quarantine_df = df[invalid_mask]
candidate_df = df[~invalid_mask]

is_dup = candidate_df.duplicated(subset=["order_id"], keep="first")
duplicates_df = candidate_df[is_dup]
clean_df = candidate_df[~is_dup]

print(len(df), len(quarantine_df), len(duplicates_df), len(clean_df))
```

Note the `~` operator: it flips a boolean mask, so `~invalid_mask` means "rows that are NOT invalid."

## Common mistakes
- Using `==` to compare against `NaN` (`df["unit_price"] == None`) — this never matches. Always use `.isna()`.
- Forgetting `keep="first"` in `duplicated()` — without it pandas still defaults to `"first"`, but being explicit avoids surprises when the default changes or is misremembered.
- Computing the duplicate mask on the *full* dataset instead of the *already-valid* candidate rows, which can quarantine-then-dedupe in the wrong order and produce inconsistent counts.

## Mini exercise
Given this DataFrame (as CSV):
```csv
order_id,quantity,unit_price
A,2,10.00
B,0,10.00
A,2,10.00
```
Write the boolean mask expression for "quantity is invalid" and state which row(s) it flags.

## Expected result
`df["quantity"] <= 0` flags row `B` (`quantity` is `0`). Row order `A` (first) is valid; the second `A` is a duplicate of the first, detected only after invalid rows are removed.

## Summary
Boolean masks let you express "which rows are invalid" and "which rows are duplicates" as vectorized pandas expressions instead of manual loops. Compute the invalid mask first, then compute duplicates only on the surviving rows.

## Next step
Lesson 3 assembles these masks into a full clean/quarantine pipeline with two output files, which is exactly what the lab asks you to build.
