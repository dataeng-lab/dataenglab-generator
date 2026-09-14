"""Bookstore order cleaning pipeline (starter).

Complete every TODO below. Do not change function names or signatures —
the automated tests import and call these functions directly.
"""
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ["order_id", "book_title", "quantity", "unit_price", "order_date"]


def load_orders(path):
    """Read the raw orders CSV into a DataFrame."""
    return pd.read_csv(path)


def validate_orders(df):
    """Split df into (valid_df, quarantine_df).

    A row is INVALID when:
      - unit_price is missing, OR unit_price <= 0
      - quantity <= 0

    Return a tuple: (valid_rows, invalid_rows). Neither DataFrame should
    share memory with df (use .copy()).
    """
    # TODO 1: build a boolean mask `price_invalid` that is True when
    #         df["unit_price"] is missing or not greater than 0.
    #         Hint: use .isna() and the | operator.

    # TODO 2: build a boolean mask `quantity_invalid` that is True when
    #         df["quantity"] is not greater than 0.

    # TODO 3: combine both masks into a single `invalid_mask`.

    # TODO 4: return (df[~invalid_mask].copy(), df[invalid_mask].copy())

    raise NotImplementedError("Implement validate_orders")


def deduplicate_orders(df):
    """Remove rows with a repeated order_id, keeping the first occurrence."""
    # TODO 5: return df.drop_duplicates(subset=["order_id"], keep="first")
    raise NotImplementedError("Implement deduplicate_orders")


def write_outputs(clean_df, quarantine_df, output_dir):
    """Write clean_df and quarantine_df to output_dir as CSV files."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(output_dir / "clean_orders.csv", index=False)
    quarantine_df.to_csv(output_dir / "quarantine_orders.csv", index=False)


def run_pipeline(input_path, output_dir):
    """Run the full pipeline and return (clean_df, quarantine_df)."""
    df = load_orders(input_path)
    valid_df, quarantine_df = validate_orders(df)
    clean_df = deduplicate_orders(valid_df)
    write_outputs(clean_df, quarantine_df, output_dir)
    return clean_df, quarantine_df


def main():
    here = Path(__file__).resolve().parent
    input_path = here.parent / "datasets" / "orders.csv"
    output_dir = here.parent / "output"
    clean_df, quarantine_df = run_pipeline(input_path, output_dir)
    print(f"Clean rows: {len(clean_df)}")
    print(f"Quarantined rows: {len(quarantine_df)}")


if __name__ == "__main__":
    main()
