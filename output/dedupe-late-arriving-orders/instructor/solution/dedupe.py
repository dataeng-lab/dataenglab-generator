"""Instructor solution: one trusted row per order_id.

Fixes applied, in the same order as the student tasks:
  1/2. Diagnosed that order_events.csv holds one row per status-update
       delivery, not one row per order, and that one delivery (O-2003) was
       redelivered as an exact duplicate.
  3.   Dropped exact duplicate deliveries (identical event_id + every
       field) before doing anything else, flagging had_duplicate_delivery
       for any order that had one removed.
  4.   Picked the true latest event per order by event_ts, treating a row
       with a real event_ts as later than any row without one, and using
       sequence_no as the tie-break whenever event_ts is missing or tied
       (covers the same-timestamp race on O-2004, the double-NULL
       event_ts on O-2006, and the late-arriving/out-of-order delivery on
       O-2007 and O-2008 that a naive "last row in the file" read gets
       wrong).
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
    # Task 3: drop exact duplicate deliveries, remembering which order_ids
    # had at least one dropped.
    seen = set()
    deduped_rows = []
    duplicate_order_ids = set()
    for row in rows:
        key = (row["event_id"], row["order_id"], row["status"], row["event_ts"], row["sequence_no"])
        if key in seen:
            duplicate_order_ids.add(row["order_id"])
            continue
        seen.add(key)
        deduped_rows.append(row)

    # Task 4: pick the true latest event per order_id. A real event_ts
    # always beats a missing one; sequence_no breaks ties (including
    # double-missing event_ts).
    by_order = {}
    for row in deduped_rows:
        by_order.setdefault(row["order_id"], []).append(row)

    result = []
    for order_id, events in by_order.items():
        latest = max(
            events,
            key=lambda r: (r["event_ts"] is not None, r["event_ts"] or "", r["sequence_no"]),
        )
        result.append({
            "order_id": order_id,
            "status": latest["status"],
            "event_ts": latest["event_ts"],
            "had_duplicate_delivery": 1 if order_id in duplicate_order_ids else 0,
        })
    return result


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
