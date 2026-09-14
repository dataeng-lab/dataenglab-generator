# Building a Clean/Quarantine Pipeline

## Learning objective
Assemble validation and deduplication into a small, testable pipeline that produces a clean output file and a quarantine output file.

## Prerequisites
Lessons 1 and 2.

## Concept
A clean/quarantine pipeline is built from small, single-purpose functions chained together:
1. `load_orders(path)` — read the raw CSV into a DataFrame.
2. `validate_orders(df)` — split into `(valid_df, quarantine_df)` using the invalid mask from Lesson 2.
3. `deduplicate_orders(df)` — remove repeated `order_id`s from the valid rows, keeping the first occurrence.
4. `write_outputs(clean_df, quarantine_df, output_dir)` — write both results to disk.

Keeping each step as its own function makes the pipeline easy to test: each function can be checked in isolation with a small, known input, instead of only being able to test the whole script end to end.

## Architecture or data flow
```text
load_orders(path)
      │
      ▼
validate_orders(df) ──▶ quarantine_df ──▶ write to quarantine_orders.csv
      │
   valid_df
      │
      ▼
deduplicate_orders(valid_df)
      │
      ▼
   clean_df ──▶ write to clean_orders.csv
```

## Practical example
```python
def validate_orders(df):
    price_invalid = df["unit_price"].isna() | (df["unit_price"] <= 0)
    quantity_invalid = df["quantity"] <= 0
    invalid_mask = price_invalid | quantity_invalid
    return df[~invalid_mask].copy(), df[invalid_mask].copy()

def deduplicate_orders(df):
    return df.drop_duplicates(subset=["order_id"], keep="first")

def write_outputs(clean_df, quarantine_df, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(output_dir / "clean_orders.csv", index=False)
    quarantine_df.to_csv(output_dir / "quarantine_orders.csv", index=False)
```

Every row from the input ends up in exactly one place: `clean_orders.csv`, or `quarantine_orders.csv`. No row silently disappears, and duplicates of already-valid rows are dropped (not quarantined — they are not invalid data, just redundant).

## Common mistakes
- Writing `clean_df = df` before validating — this mutates or aliases the original DataFrame instead of producing a filtered copy. Always assign the result of filtering.
- Deduplicating before validating, which can let an invalid duplicate "protect" a later valid row from being considered the canonical one.
- Forgetting `.copy()` after boolean indexing, which can trigger pandas' `SettingWithCopyWarning` on later modifications.

## Mini exercise
Trace this input through the pipeline by hand:
```csv
order_id,quantity,unit_price
1,2,10.00
2,-1,10.00
1,2,10.00
```
List which rows end up in `clean_orders.csv` and which end up in `quarantine_orders.csv`.

## Expected result
- `quarantine_orders.csv`: row with `order_id=2` (negative quantity).
- `clean_orders.csv`: row with `order_id=1` (first occurrence only — the second `order_id=1` row is a duplicate of an already-valid row and is dropped, not quarantined).

## Summary
The pipeline is four small functions — load, validate, deduplicate, write — chained in order. Validating before deduplicating ensures duplicate detection only runs on trustworthy rows.

## Next step
Complete the practical lab: implement this exact pipeline for the bookstore's real orders file and make the automated tests pass.
