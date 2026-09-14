"""YOUR TASK: implement dedupe() so that it returns exactly one trusted row
per order_id. Work through Tasks 1-5 in README.md before writing this.

Usage: python starter/dedupe.py
Reads datasets/order_events.csv, writes output/orders_deduped.csv.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "datasets" / "order_events.csv"
OUTPUT = ROOT / "output" / "orders_deduped.csv"

FIELDNAMES = ("order_id", "status", "event_ts", "had_duplicate_delivery")


def load_events(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            row["event_ts"] = row["event_ts"] or None
            row["sequence_no"] = int(row["sequence_no"])
            rows.append(row)
    return rows


def dedupe(rows):
    """Return one dict per order_id: order_id, status, event_ts,
    had_duplicate_delivery.

    TODO:
      Task 3 — drop exact duplicate deliveries: two rows are the same
      delivery if every field (event_id, order_id, status, event_ts,
      sequence_no) is identical. Remember which order_id(s) had at least
      one duplicate dropped, so you can set had_duplicate_delivery.

      Task 4 — among the remaining rows for an order_id, pick the row with
      the latest event_ts. event_ts can be missing (None): treat a row
      with a real event_ts as later than any row without one, and use
      sequence_no as the tie-break whenever event_ts is missing or tied
      between two rows for the same order.
    """
    raise NotImplementedError("implement dedupe() — see README.md Tasks 3-4")


def main():
    rows = load_events(DATASET)
    result = dedupe(rows)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in sorted(result, key=lambda r: r["order_id"]):
            writer.writerow({
                "order_id": row["order_id"],
                "status": row["status"],
                "event_ts": row["event_ts"] or "",
                "had_duplicate_delivery": row["had_duplicate_delivery"],
            })
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
