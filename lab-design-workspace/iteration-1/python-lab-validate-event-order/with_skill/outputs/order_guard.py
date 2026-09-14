"""Instructor solution: detect out-of-order and clock-skew readings and
produce a trustworthy, corrected sequence per device.

Fixes applied, in the same order as the student tasks:
  1/2. Diagnosed that sensor_readings.csv is a live, per-reading delivery
       log, not a chronologically-sorted table, and that trusting file
       order for a live feed displays real-but-impossible regressions.
  3.   Detected out-of-order readings by tracking a running maximum valid
       timestamp per device_id, in arrival order, and flagging any row
       whose timestamp is earlier than that running max.
  4.   Distinguished an ordinary out-of-order reading (still corrected
       back into the sequence) from a clock-skew anomaly (timestamp more
       than ANOMALY_THRESHOLD_HOURS ahead of the running max - quarantined,
       not reordered in) and a missing timestamp (also quarantined,
       handled without crashing).
  5.   Assembled corrected_readings.csv (every non-quarantined reading,
       chronologically sorted per device with an arrival_seq tie-break)
       and flagged_readings.csv (every flagged reading with its reason).
"""
import csv
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "datasets" / "sensor_readings.csv"
CORRECTED_OUTPUT = ROOT / "output" / "corrected_readings.csv"
FLAGGED_OUTPUT = ROOT / "output" / "flagged_readings.csv"

TS_FORMAT = "%Y-%m-%d %H:%M:%S"

ANOMALY_THRESHOLD_HOURS = 2

CORRECTED_FIELDNAMES = ("device_id", "event_ts", "temperature_c", "arrival_seq", "out_of_order")
FLAGGED_FIELDNAMES = ("reading_id", "device_id", "arrival_seq", "event_ts", "temperature_c", "flag_reason")


def load_readings(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            row["arrival_seq"] = int(row["arrival_seq"])
            row["temperature_c"] = float(row["temperature_c"])
            row["event_ts"] = row["event_ts"] or None
            rows.append(row)
    return rows


def process_readings(rows):
    running_max = {}  # device_id -> datetime, only ever a "trusted" value
    corrected_rows = []
    flagged_rows = []

    for row in sorted(rows, key=lambda r: r["arrival_seq"]):
        device_id = row["device_id"]
        raw_ts = row["event_ts"]

        if raw_ts is None:
            flagged_rows.append({
                "reading_id": row["reading_id"],
                "device_id": device_id,
                "arrival_seq": row["arrival_seq"],
                "event_ts": "",
                "temperature_c": row["temperature_c"],
                "flag_reason": "invalid_timestamp",
            })
            continue  # quarantined: no running_max update, not in corrected output

        ts = datetime.strptime(raw_ts, TS_FORMAT)
        prev_max = running_max.get(device_id)

        out_of_order = False
        anomalous = False

        if prev_max is not None:
            if ts > prev_max + timedelta(hours=ANOMALY_THRESHOLD_HOURS):
                anomalous = True
            elif ts < prev_max:
                out_of_order = True

        if anomalous:
            flagged_rows.append({
                "reading_id": row["reading_id"],
                "device_id": device_id,
                "arrival_seq": row["arrival_seq"],
                "event_ts": raw_ts,
                "temperature_c": row["temperature_c"],
                "flag_reason": "anomalous_clock_skew",
            })
            continue  # quarantined: no running_max update, not in corrected output

        if not out_of_order:
            # New trusted max: first valid reading, a later timestamp, or a tie.
            running_max[device_id] = ts

        corrected_rows.append({
            "device_id": device_id,
            "event_ts": raw_ts,
            "temperature_c": row["temperature_c"],
            "arrival_seq": row["arrival_seq"],
            "out_of_order": 1 if out_of_order else 0,
        })

        if out_of_order:
            flagged_rows.append({
                "reading_id": row["reading_id"],
                "device_id": device_id,
                "arrival_seq": row["arrival_seq"],
                "event_ts": raw_ts,
                "temperature_c": row["temperature_c"],
                "flag_reason": "out_of_order",
            })

    corrected_rows.sort(
        key=lambda r: (r["device_id"], datetime.strptime(r["event_ts"], TS_FORMAT), r["arrival_seq"])
    )
    flagged_rows.sort(key=lambda r: r["arrival_seq"])

    return corrected_rows, flagged_rows


def write_outputs(corrected_rows, flagged_rows):
    CORRECTED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(CORRECTED_OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CORRECTED_FIELDNAMES)
        writer.writeheader()
        for row in corrected_rows:
            writer.writerow(row)

    with open(FLAGGED_OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FLAGGED_FIELDNAMES)
        writer.writeheader()
        for row in flagged_rows:
            writer.writerow(row)


def main():
    rows = load_readings(DATASET)
    corrected_rows, flagged_rows = process_readings(rows)
    write_outputs(corrected_rows, flagged_rows)
    print(f"Wrote {CORRECTED_OUTPUT.relative_to(ROOT)} ({len(corrected_rows)} rows)")
    print(f"Wrote {FLAGGED_OUTPUT.relative_to(ROOT)} ({len(flagged_rows)} rows)")


if __name__ == "__main__":
    main()
