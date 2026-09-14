"""Instructor solution: detect out-of-order sensor events and reconstruct
a trustworthy, chronologically-ordered view of the stream.

Fixes applied, in the same order as the student tasks:
  1/2. Diagnosed that sensor_events.csv is written in ingestion/file
       order, which is not guaranteed to match the device's true event
       order (event_ts) -- spike_report.py's bug is that it treats file
       order as chronological order.
  3.   detect_out_of_order(): walks each device's rows in FILE order,
       tracking the running-max real event_ts seen so far for that
       device. A row is flagged when its event_ts is strictly earlier
       than that running max. A missing event_ts is never flagged (can't
       be judged) and never updates the running max. The running max is
       monotonic -- it is never lowered by an out-of-order row, which is
       what makes D-05's cascading case (two out-of-order rows in a row)
       come out right.
  4.   reorder_events(): regroups by device_id and sorts each device's
       rows by (event_ts is not None, event_ts or "", sequence_no) --
       missing timestamps sort first (can't be placed, so surfaced up
       front), real timestamps sort chronologically, and sequence_no
       breaks any exact tie (D-03) since it is always present and always
       reflects true delivery order.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "datasets" / "sensor_events.csv"
FLAGS_OUTPUT = ROOT / "output" / "order_flags.csv"
CORRECTED_OUTPUT = ROOT / "output" / "corrected_events.csv"

FLAGS_FIELDNAMES = ("event_id", "device_id", "event_ts", "reading_c", "sequence_no", "is_out_of_order")
CORRECTED_FIELDNAMES = ("device_id", "event_id", "event_ts", "reading_c", "sequence_no")


def load_events(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            row["event_ts"] = row["event_ts"] or None
            row["sequence_no"] = int(row["sequence_no"])
            rows.append(row)
    return rows


def detect_out_of_order(rows):
    running_max_by_device = {}
    result = []
    for row in rows:
        device_id = row["device_id"]
        ts = row["event_ts"]
        is_out_of_order = False
        if ts is not None:
            running_max = running_max_by_device.get(device_id)
            if running_max is not None and ts < running_max:
                is_out_of_order = True
            else:
                running_max_by_device[device_id] = ts if running_max is None else max(running_max, ts)
        new_row = dict(row)
        new_row["is_out_of_order"] = is_out_of_order
        result.append(new_row)
    return result


def reorder_events(rows):
    by_device = {}
    for row in rows:
        by_device.setdefault(row["device_id"], []).append(row)

    result = []
    for device_id in sorted(by_device):
        events_sorted = sorted(
            by_device[device_id],
            key=lambda r: (r["event_ts"] is not None, r["event_ts"] or "", r["sequence_no"]),
        )
        result.extend(events_sorted)
    return result


def write_flags(rows, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FLAGS_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "event_id": row["event_id"],
                "device_id": row["device_id"],
                "event_ts": row["event_ts"] or "",
                "reading_c": row["reading_c"],
                "sequence_no": row["sequence_no"],
                "is_out_of_order": 1 if row["is_out_of_order"] else 0,
            })


def write_corrected(rows, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CORRECTED_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "device_id": row["device_id"],
                "event_id": row["event_id"],
                "event_ts": row["event_ts"] or "",
                "reading_c": row["reading_c"],
                "sequence_no": row["sequence_no"],
            })


def main():
    rows = load_events(DATASET)

    flagged = detect_out_of_order(rows)
    write_flags(flagged, FLAGS_OUTPUT)
    print(f"Wrote {FLAGS_OUTPUT.relative_to(ROOT)}")

    corrected = reorder_events(rows)
    write_corrected(corrected, CORRECTED_OUTPUT)
    print(f"Wrote {CORRECTED_OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
