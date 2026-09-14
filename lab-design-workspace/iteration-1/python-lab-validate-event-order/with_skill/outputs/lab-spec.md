# Practical Lab Specification

## Business context
SensorGrid runs a fleet of IoT temperature sensors that stream readings to
a CSV export used by an on-call monitoring dashboard. The ingestion path
delivers readings over an unreliable network: retries and buffering mean a
reading can reach the file with an earlier timestamp than one already
displayed as "current" for that device, and one sensor's onboard clock can
drift so far that a reading claims to be from hours in the future. The
current dashboard feed just displays whatever value arrives next, in file
order, with no timestamp checking. On-call was paged twice last week for
"impossible" readings: device `D-103` appeared to spike to 61.0C at
14:08 and then "drop" back to 60.9C a few readings later (nothing
physically changed — the 14:08 reading was a clock-fault), and `D-101`'s
displayed temperature dipped from 30.4C to 30.2C before climbing again
(a late-arriving reading, not a real dip). The student plays the data
engineer asked to write a script that detects out-of-order and clock-fault
readings before they reach the feed, and produces a trustworthy,
chronologically corrected sequence per device.

## Learning objectives
By the end of the lab, students can:
- Recognize that "arrived later in the file" is not the same as
  "happened later," and that trusting file/arrival order for a live feed
  can display real but temporally-impossible regressions.
- Detect an out-of-order event per key by tracking a running maximum
  valid timestamp per device, rather than trusting row position.
- Distinguish an ordinary late-arriving event (plausible network delay,
  timestamp behind the running max) from a clock-skew anomaly
  (timestamp implausibly far ahead of the running max) using a documented
  threshold, and handle each differently: reorder the former in, quarantine
  the latter out.
- Handle a missing timestamp without crashing, and exclude it from both
  ordering decisions and the corrected output while still reporting it.

## Environment
Python 3.9+ (standard library only — no `pip install`, no Docker, no
network access).

## Estimated duration
25 minutes.

## Starter files
- `student-lab/reset.py` — (re)creates an empty `output/` directory.
- `student-lab/starter/naive_trend.py` — the current, buggy live-feed
  transcript (read-only reference, do not edit).
- `student-lab/starter/order_guard.py` — where the student implements
  `process_readings()`.

## Dataset
`student-lab/datasets/sensor_readings.csv` (23 rows / 4 devices: `D-100`
.. `D-103`, global `arrival_seq` 1-23 in file order). Edge cases encoded:
- `D-100` — 5 in-order readings, no issues (baseline).
- `D-101` — 6 readings, one (`R-0010`, `arrival_seq` 10, `08:04:00`)
  arrives after a later reading (`R-0006`, `08:06:00`) already raised the
  device's running max — an ordinary out-of-order delivery.
- `D-102` — 6 readings, one (`R-0011`) has a blank `event_ts` — a missing
  timestamp — plus a legitimate exact-timestamp tie between `R-0015` and
  `R-0019` (both `08:12:00`) requiring an `arrival_seq` tie-break in the
  corrected sort order.
- `D-103` — 6 readings, one (`R-0012`, `14:08:00`) is 6 hours ahead of the
  device's running max (`08:08:00`) — a clock-skew anomaly, not a
  plausible late delivery — followed by a normal `08:13:00` reading that
  must not be judged out-of-order against the anomalous value.

## Tasks
1. Reproduce the bug by running `naive_trend.py` and reading its live-feed
   transcript: spot `D-103`'s impossible spike-then-drop around `14:08:00`
   and `D-101`'s dip-then-climb around `08:04:00`-`08:06:00`.
2. Diagnose by inspecting `sensor_readings.csv` grouped by `device_id`:
   find the one genuinely out-of-order row, the one missing-timestamp row,
   and the one clock-skew row, and confirm the note in the dataset section
   above.
3. Implement out-of-order detection: process each device's rows in
   arrival order, track a running maximum valid timestamp per device, and
   flag `out_of_order` when a row's timestamp is earlier than that
   device's running max so far.
4. Implement clock-skew detection: flag `anomalous_clock_skew` when a
   row's timestamp is more than `ANOMALY_THRESHOLD_HOURS` (2) ahead of the
   running max — quarantine it (exclude from the corrected output and
   never let it update the running max), unlike an out-of-order row, which
   is corrected back into the sequence. Also flag `invalid_timestamp` for
   a blank timestamp, quarantining it the same way, without crashing.
5. Assemble `process_readings()` in `order_guard.py` so it writes
   `output/corrected_readings.csv` (every non-quarantined reading,
   chronologically sorted per device with an `arrival_seq` tie-break, plus
   an `out_of_order` column) and `output/flagged_readings.csv` (every
   flagged reading with its `flag_reason`), then verify the row counts.

## Hints
Provided as `<details>` blocks in `student-lab/README.md`, one per task
that needs one (Tasks 3 and 4).

## Validation
```bash
python reset.py
python tests/test_solution.py
```
Both commands run from inside `student-lab/`. `test_solution.py` runs
`starter/order_guard.py`, then checks both output files exist, have the
required columns, and match `tests/expected_corrected.csv` and
`tests/expected_flagged.csv` exactly. It exits non-zero on any failure.
Matches `validate.json` at this lab's root exactly.

## Expected output
`output/corrected_readings.csv`: 21 rows (23 minus the 2 quarantined
rows), one `out_of_order=1` row (`D-101` at `08:04:00`), all others `0`.
`output/flagged_readings.csv`: exactly 3 rows — `out_of_order` (`D-101`),
`invalid_timestamp` (`D-102`), `anomalous_clock_skew` (`D-103`). See
`instructor/instructor-guide.md` for the full row-by-row derivation.

## Reset procedure
`python reset.py` — recreates an empty `output/` directory at any time;
`datasets/` and the starter files are never modified by setup/reset.

## Troubleshooting
See `student-lab/README.md`'s Troubleshooting section (student-facing) and
`instructor/troubleshooting.md` (instructor-facing, covers common wrong
turns and how to steer students back).

## Instructor solution
`instructor/solution/order_guard.py`, with `instructor/instructor-guide.md`
explaining the reasoning behind each fix and `instructor/troubleshooting.md`
covering common student mistakes.
