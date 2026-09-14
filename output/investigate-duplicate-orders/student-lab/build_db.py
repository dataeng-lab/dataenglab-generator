"""Setup step for the lab: (re)builds lab.db from the CSVs in datasets/.

Usage: python build_db.py
Safe to re-run at any time (this is also the reset procedure).
"""
import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "lab.db"
SCHEMA_PATH = ROOT / "starter" / "schema.sql"
DATASETS = ROOT / "datasets"


def load_csv(cursor, table, csv_path, columns):
    placeholders = ",".join("?" for _ in columns)
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [tuple((row[c] if row[c] != "" else None) for c in columns) for row in reader]
    cursor.executemany(
        f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})", rows
    )


def main():
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(str(DB_PATH))
    try:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        cur = conn.cursor()
        load_csv(
            cur,
            "orders",
            DATASETS / "orders.csv",
            ["event_id", "order_id", "customer_id", "status", "order_ts", "updated_at", "order_version"],
        )
        load_csv(
            cur,
            "order_items",
            DATASETS / "order_items.csv",
            ["order_item_id", "order_id", "sku", "quantity", "unit_price"],
        )
        conn.commit()
    finally:
        conn.close()

    print(f"Built {DB_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
