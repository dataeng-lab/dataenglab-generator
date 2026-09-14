# Validate Event Order

**Level:** Beginner · **Duration:** ~25 min · **Tags:** data quality, ordering, timestamps, CSV

## Business context

A fleet of IoT temperature sensors reports readings to a central CSV log,
`sensor_events.csv`. Each sensor pushes a reading every five minutes, but
the ingestion tier is a pool of parallel workers with retries, so rows
land in the file in **network arrival order**, not necessarily in the
order the readings actually happened (`event_ts`).

The on-call fault-detection script,
[`starter/spike_report.py`](starter/spike_report.py), doesn't know that.
It walks the file and compares each row's reading to the row written
immediately before it for the same device — trusting file order as if it
were chronological order. Don't edit it, it's your reference for what's
currently in production. Your fix goes in
[`starter/order_check.py`](starter/order_check.py).

## Environment

- Python 3.9+ (only the standard library — no installs needed)
- No Docker, no network access required

## Setup

```bash
python build_dataset.py
```

This (re)generates `datasets/sensor_events.csv` (deterministic — the same
16 rows every time) and (re)creates an empty `output/` directory. Re-run
it any time you want to reset your working state (see **Reset procedure**
below) — it never touches the starter files.

## Tasks

### Task 1 — Reproduce the bug

Run the current fault scanner:

```bash
python starter/spike_report.py
```

It reports one flagged fault for device `D-02`: a suspicious -11.5°C drop
between `E-9004` and `E-9005`. Now open `datasets/sensor_events.csv` and
look at `D-02`'s three rows by `event_ts`, not by file position. Is a
-11.5°C *drop* really what happened at `08:00:00`? What does the reading
at `08:10:00` (30.5°C) actually mean, and why doesn't the scanner ever
mention it?

### Task 2 — Find where file order and event order disagree

For each `device_id` in `sensor_events.csv`, compare the row order as
written in the file to the order you'd get by sorting on `event_ts`. Most
devices already match. `D-02` and `D-05` don't — write down, for each of
those two devices, which rows are out of place.

### Task 3 — Detect out-of-order rows

In `detect_out_of_order()`, walk each device's rows **in file order**
(the order they appear in the CSV — do not sort first) while tracking the
greatest real `event_ts` seen so far for that device (a running max). Flag
a row as out of order when it has a real `event_ts` that is *strictly
earlier* than that running max.

Two things to get right:
- A row with a **missing `event_ts`** can't be judged — never flag it, and
  never let it update the running max.
- The running max must be **monotonic** (never decreases). `D-05` has two
  out-of-order rows back-to-back — if you only compare each row to the one
  immediately before it, you will only catch the first one. Compare
  against the running max, not just the previous row.

### Task 4 — Reconstruct the true chronological order

In `reorder_events()`, regroup all rows by `device_id` (devices sorted
alphabetically), then sort each device's rows into true chronological
order:
- A missing `event_ts` can't be placed by time, so surface it **first**
  within its device (ties among missing-timestamp rows broken by
  `sequence_no`), ahead of every row that does have a real timestamp.
- Otherwise sort by `event_ts` ascending.
- When two rows share the **exact same** `event_ts` (`D-03`), use
  `sequence_no` (ascending) as the tie-break — it's always present and
  always reflects true delivery order.

### Task 5 — Verify

Run your script and check your own output before running the automated
check:

```bash
python starter/order_check.py
```

`output/order_flags.csv` should have 16 rows (same as the input, same
order, one new `is_out_of_order` column) with exactly 4 rows flagged.
`output/corrected_events.csv` should have 16 rows regrouped by device in
true chronological order.

## Hints

Stuck? Expand only the hint you need.

<details>
<summary>Hint for Task 3 (detect out-of-order rows)</summary>

```python
running_max_by_device = {}
for row in rows:  # file order — do not sort
    device_id = row["device_id"]
    ts = row["event_ts"]
    is_out_of_order = False
    if ts is not None:
        running_max = running_max_by_device.get(device_id)
        if running_max is not None and ts < running_max:
            is_out_of_order = True
        else:
            running_max_by_device[device_id] = ts if running_max is None else max(running_max, ts)
```
`running_max_by_device` only ever moves forward — an out-of-order row
must never lower it, or a second consecutive out-of-order row (like
`D-05`'s) would wrongly slip through.
</details>

<details>
<summary>Hint for Task 4 (reconstruct chronological order)</summary>

```python
events_sorted = sorted(
    events_for_one_device,
    key=lambda r: (r["event_ts"] is not None, r["event_ts"] or "", r["sequence_no"]),
)
```
The tuple compares left to right: "has a real timestamp" (`False` sorts
before `True`, so missing-timestamp rows come first), then the timestamp
itself, then `sequence_no` breaks any remaining tie.
</details>

## Expected output

`output/order_flags.csv`: 16 rows, same order as the input, 4 flagged
(`E-9005`, `E-9006` on `D-02`; `E-9015`, `E-9016` on `D-05`).
`output/corrected_events.csv`: 16 rows, grouped by device, each device's
rows in true chronological order — e.g. `D-02` becomes
`E-9005 (08:00) → E-9006 (08:05) → E-9004 (08:10)`, correctly moving the
real 30.5°C overheat reading to last instead of first. See
`instructor/instructor-guide.md` for the full breakdown.

## Validation

```bash
python tests/test_solution.py
```

Runs `starter/order_check.py` and checks that:
1. both `output/order_flags.csv` and `output/corrected_events.csv` exist,
2. `order_flags.csv` has the required columns, keeps the original 16 rows
   in their original file order, and matches the trusted `is_out_of_order`
   flag for every row,
3. `corrected_events.csv` has the required columns and matches the
   trusted device-grouped chronological order exactly.

Exits non-zero if any check fails.

## Reset procedure

```bash
python build_dataset.py
```

Always regenerates the same 16-row dataset and starts from an empty
`output/` directory; the starter files are never modified.

## Troubleshooting

- **`output/order_flags.csv not found` when running the test** — run
  `python starter/order_check.py` yourself first and check it doesn't
  raise an error (the starter ships with both functions raising
  `NotImplementedError` until you implement them).
- **`D-05` only has one row flagged instead of two** — you're likely
  comparing each row only to the row immediately before it, not to a
  running max. `D-05`'s second out-of-order row (`E-9016`, `08:10:00`) is
  later than the row right before it (`E-9015`, `08:00:00`) but still
  earlier than the true max already seen for that device (`E-9014`,
  `08:15:00`).
- **A row with a missing `event_ts` gets flagged as out of order** — a
  missing timestamp can't be compared; make sure your code checks for
  `None` before comparing, and skips updating the running max for that
  row.
- **`D-03`'s two same-timestamp rows come out in the wrong order in
  `corrected_events.csv`** — sorting by `event_ts` alone leaves ties in
  their original (file) order; add `sequence_no` as the second sort key.
