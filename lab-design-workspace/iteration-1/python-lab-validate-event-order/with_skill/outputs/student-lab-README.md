# Detect and Handle Out-of-Order Event Timestamps

**Level:** Beginner · **Duration:** ~25 min · **Tags:** out-of-order events, watermarks, timestamps, data quality, Python

## Business context

SensorGrid runs a fleet of IoT temperature sensors that stream readings
into a CSV export used by an on-call monitoring dashboard. Delivery is
unreliable:

- **Late arrivals** — a reading occasionally reaches the file with an
  earlier timestamp than one already shown as "current" for that device,
  because of network retries and buffering.
- **Clock faults** — one sensor's onboard clock can drift so badly that a
  reading claims to be from hours in the future.

The current dashboard feed just displays whatever value arrives next, in
file order, with no timestamp checking. On-call was paged twice last
week:

- Device `D-103` appeared to spike to **61.0C at 14:08**, then "drop"
  back to 60.9C a few readings later — nothing physically changed, the
  14:08 reading was a clock fault.
- Device `D-101`'s displayed temperature **dipped from 30.4C to 30.2C**
  before climbing again — a late-arriving reading, not a real dip.

You've been asked to write a script that catches both problems before
they reach the feed, and produces a trustworthy, chronologically
corrected sequence per device.

The current feed lives in
[`starter/naive_trend.py`](starter/naive_trend.py). Don't edit it — it's
your reference for what's currently in production. Your fix goes in
[`starter/order_guard.py`](starter/order_guard.py).

## Environment

- Python 3.9+ (only the standard library — no installs needed)
- No Docker, no network access required

## Setup

```bash
python reset.py
```

This (re)creates an empty `output/` directory. Re-run it any time you want
to reset your working state (see **Reset procedure** below) — it never
touches `datasets/` or the starter files.

## Tasks

### Task 1 — Reproduce the bug

Run the current live feed:

```bash
python starter/naive_trend.py
```

Read the transcript top to bottom. Find the line where `D-103` shows
`61.0C at 2026-03-02 14:08:00` — a few lines later it "drops" to 60.9C.
Also find where `D-101` shows a value going down (`<-- value went DOWN`)
around `08:04:00`/`08:06:00`. Confirm both are the timestamp-order bug
Support/on-call flagged, not real sensor behavior.

### Task 2 — Find the three different problems

Look directly at `datasets/sensor_readings.csv`, grouped by `device_id`.
You should find three distinct issues, each needing different handling:

- One row (`D-101`) has a real timestamp that is **earlier** than a
  timestamp already seen for that device — an ordinary late delivery.
- One row (`D-102`) has a **blank** `event_ts` — no timestamp at all.
- One row (`D-103`) has a timestamp **hours ahead** of anything else seen
  for that device — implausible, a clock fault rather than a genuine late
  delivery.

### Task 3 — Detect out-of-order readings

In `process_readings()`, walk each device's rows in arrival order (the
order they already appear in the file) and track a running maximum valid
timestamp per `device_id`. If a row's timestamp is **earlier** than that
device's running max so far, flag it `out_of_order`. It still belongs in
the final corrected sequence — just reordered to its correct chronological
position — and it must **not** update the running max (it isn't the new
latest).

### Task 4 — Detect clock-skew and missing timestamps

Two more cases need different handling than an ordinary out-of-order row:

- A row whose timestamp is more than `ANOMALY_THRESHOLD_HOURS` (2) **ahead
  of** the running max is `anomalous_clock_skew`. Unlike an out-of-order
  row, it is **quarantined**: excluded from the corrected output, and it
  must never update the running max either.
- A row with a **blank** `event_ts` is `invalid_timestamp`. Same
  treatment: quarantined, and it must not crash your script or update the
  running max.

### Task 5 — Assemble and verify

Combine Tasks 3–4 into `process_readings()` in `starter/order_guard.py` so
it writes:

- `output/corrected_readings.csv` — every non-quarantined reading
  (`device_id`, `event_ts`, `temperature_c`, `arrival_seq`,
  `out_of_order`), sorted by `device_id`, then `event_ts`, with
  `arrival_seq` as the tie-break for two readings with the identical
  timestamp.
- `output/flagged_readings.csv` — every flagged reading (`reading_id`,
  `device_id`, `arrival_seq`, `event_ts`, `temperature_c`,
  `flag_reason`), sorted by `arrival_seq`.

Run it and check your own output before running the automated check:

```bash
python starter/order_guard.py
```

`output/corrected_readings.csv` should have 21 rows, and
`output/flagged_readings.csv` should have exactly 3.

## Hints

Stuck? Expand only the hint you need.

<details>
<summary>Hint for Task 3 (detect out-of-order readings)</summary>

```python
running_max = {}  # device_id -> datetime
for row in rows:  # already in arrival order
    ts = datetime.strptime(row["event_ts"], TS_FORMAT)
    prev_max = running_max.get(row["device_id"])
    out_of_order = prev_max is not None and ts < prev_max
    if not out_of_order:
        running_max[row["device_id"]] = ts
```

This alone doesn't yet handle blank timestamps or clock skew — that's
Task 4.
</details>

<details>
<summary>Hint for Task 4 (clock skew and missing timestamps)</summary>

Check the blank-timestamp case first (skip it before you try to parse a
`None` as a date), then check clock skew before out-of-order, since a
skewed reading is never a "normal" late delivery:

```python
if row["event_ts"] is None:
    reason = "invalid_timestamp"
elif prev_max is not None and ts > prev_max + timedelta(hours=ANOMALY_THRESHOLD_HOURS):
    reason = "anomalous_clock_skew"
elif prev_max is not None and ts < prev_max:
    reason = "out_of_order"
else:
    reason = None  # normal; update running_max
```

`invalid_timestamp` and `anomalous_clock_skew` rows are quarantined
(excluded from `corrected_readings.csv`); `out_of_order` rows are not.
</details>

## Expected output

`output/corrected_readings.csv` should have 21 rows (23 minus the 2
quarantined readings), with exactly one `out_of_order=1` row (`D-101` at
`08:04:00`) and all others `0`. `output/flagged_readings.csv` should have
exactly 3 rows: one `out_of_order`, one `invalid_timestamp`, one
`anomalous_clock_skew`. See `instructor/instructor-guide.md` for the full
row-by-row derivation.

## Validation

```bash
python tests/test_solution.py
```

Runs `starter/order_guard.py` and checks that its two outputs:
1. exist and have the required columns,
2. have the expected row counts,
3. match the trusted result exactly, and
4. never include a quarantined (`invalid_timestamp` or
   `anomalous_clock_skew`) reading in `corrected_readings.csv`.

Exits non-zero if any check fails.

## Reset procedure

```bash
python reset.py
```

Always starts from an empty `output/` directory; `datasets/` and the
starter files are never modified.

## Troubleshooting

- **`output/corrected_readings.csv not found` when running the test** —
  run `python starter/order_guard.py` yourself first and check it doesn't
  raise an error (the starter ships with `process_readings()` raising
  `NotImplementedError` until you implement it).
- **`D-103` still shows the 14:08:00 reading in `corrected_readings.csv`**
  — you're flagging it `out_of_order` instead of
  `anomalous_clock_skew`; check the direction of the comparison
  (`ts > prev_max + threshold`, not `ts < prev_max`) and make sure
  clock-skew rows are excluded from the corrected output, not just
  flagged.
- **`D-103`'s `08:13:00` reading is wrongly flagged `out_of_order`** —
  your running max was updated by the anomalous `14:08:00` reading. The
  running max must only ever advance on a normal reading, never on an
  anomalous or missing-timestamp one.
- **`TypeError` comparing `NoneType` and `datetime`** — you're trying to
  parse or compare a blank `event_ts` before checking for `None`. Handle
  `invalid_timestamp` first, before any date parsing.
- **`D-102` has the two `08:12:00` rows in the wrong order** — add
  `arrival_seq` as the tie-break in your sort key; two readings can share
  the exact same `event_ts`.
