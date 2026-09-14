# Practical Lab Specification

## Title
Validate Event Order

## Slug
validate-event-order-eval-bl

## Audience
Junior/aspiring data engineers and analysts who work with CSV-based event
logs and need to reason about data quality before trusting a report.

## Level
Beginner

## Prerequisites
- Basic Python (functions, dicts, lists, `for` loops)
- Comfortable reading/writing CSV files with the standard library `csv`
  module
- No prior data-engineering or ordering/idempotency background required

## Business context
A fleet of IoT temperature sensors reports readings to a central CSV
export, `sensor_events.csv`. Each sensor pushes a reading roughly every
five minutes, but the ingestion tier is a pool of parallel workers with
retries — rows land in the file in **network arrival order**, which is
not guaranteed to match the order the readings actually happened
(`event_ts`). A fault-detection script currently in production
(`starter/spike_report.py`) assumes file order is chronological order:
it compares each row's reading to the row written immediately before it
for the same device. That assumption is false, and it produces both a
false alarm and a missed real one. The student plays the data engineer
asked to build a script that (a) detects which rows are genuinely out of
order relative to their device's other readings, and (b) reconstructs the
trustworthy, chronologically-ordered stream so any downstream analysis
(fault detection or otherwise) can rely on it.

## Learning objectives
By the end of the lab, students can:
- Recognize that the physical row order of an append-only/event-log CSV
  is not a reliable proxy for the true chronological order of the events
  it contains.
- Detect an out-of-order event per grouping key using a running-maximum
  comparison, distinguishing it from a naive "compare to the previous row
  only" check that misses cascading cases.
- Handle a missing ordering timestamp without crashing or silently
  mis-flagging it, by explicitly excluding it from the out-of-order
  judgment.
- Deterministically reconstruct chronological order per key using a
  documented primary-sort-plus-tie-break rule (`event_ts`, then
  `sequence_no`) instead of an ad hoc single-column sort.

## Environment
Python 3.9+ (standard library only — no `pip install`, no Docker, no
network access). Runs the same on Windows, macOS, and Linux.

## Estimated duration
25 minutes (fully practical — there is no passive/reading-only portion
beyond the README task descriptions).

## Technologies
Python 3.9+, the `csv` and `pathlib` standard-library modules, `unittest`
for automated validation.

## Deliverable
A student-authored `starter/order_check.py` that produces two CSV
outputs from `datasets/sensor_events.csv`:
- `output/order_flags.csv` — every input row, unchanged order, annotated
  with an `is_out_of_order` flag.
- `output/corrected_events.csv` — every input row regrouped by
  `device_id` and reordered into true chronological order.

## Starter files
- `student-lab/build_dataset.py` — (re)generates the deterministic
  dataset and an empty `output/` directory. Also the reset procedure.
- `student-lab/starter/spike_report.py` — the current, buggy fault
  scanner (read-only reference).
- `student-lab/starter/order_check.py` — where the student implements
  `detect_out_of_order()` and `reorder_events()`.

## Dataset
`student-lab/datasets/sensor_events.csv` (16 rows / 5 distinct
`device_id`), generated deterministically by `build_dataset.py`. Edge
cases encoded:
- `D-01` — baseline, already in chronological order (no out-of-order
  rows, sanity check that a well-behaved device isn't falsely flagged).
- `D-02` — headline bug: the genuine latest reading (a real 30.5°C
  overheat event) is written to the file **first**; the two earlier,
  unremarkable readings arrive after it. Tests that both later rows are
  correctly flagged, and that the naive previous-row-only fault scanner
  both invents a false signal and misses the real one.
- `D-03` — two rows share the exact same `event_ts`, with their
  `sequence_no` values in the *opposite* order from their file position —
  tests the `sequence_no` tie-break in the chronological reconstruction.
- `D-04` — the first row is missing `event_ts` entirely — tests that a
  missing timestamp is handled without crashing and without being
  (mis)flagged as out of order.
- `D-05` — two out-of-order rows **back-to-back** — tests that detection
  uses a running-maximum comparison rather than comparing only to the
  immediately preceding row (which would only catch the first one).

## Tasks
1. Run `spike_report.py` and observe the false/missed signal on `D-02`.
2. Compare file order to `event_ts` order per device by hand; identify
   which devices/rows disagree.
3. Implement `detect_out_of_order()`: running-max-per-device comparison,
   ignoring rows with a missing `event_ts`.
4. Implement `reorder_events()`: regroup by device, sort chronologically
   with a `sequence_no` tie-break and a documented rule for missing
   timestamps.
5. Run the script and verify `output/order_flags.csv` (16 rows, 4
   flagged) and `output/corrected_events.csv` (16 rows, correctly
   reordered) before running the automated check.

## Hints
Provided as `<details>` blocks in `student-lab/README.md`, one per task
that needs one (Tasks 3 and 4).

## Validation
```bash
python build_dataset.py
python tests/test_solution.py
```
Both commands run from inside `student-lab/`. `test_solution.py` runs
`starter/order_check.py`, then checks both output files exist, have the
required columns, preserve/produce the expected row count, and match
`tests/expected_order_flags.csv` / `tests/expected_corrected_events.csv`
exactly. It exits non-zero on any failure. Matches `validate.json` at
this lab's root exactly.

## Expected output
`output/order_flags.csv`: 16 rows, original file order preserved, with
exactly 4 rows flagged (`E-9005`, `E-9006` on `D-02`; `E-9015`, `E-9016`
on `D-05`). `output/corrected_events.csv`: 16 rows grouped by device in
true chronological order. See `instructor/instructor-guide.md` for the
full before/after breakdown, actually verified by running both the
naive script and the instructor solution against the dataset.

## Reset procedure
`python build_dataset.py` — regenerates the same 16-row dataset and an
empty `output/` directory at any time; the starter files are never
modified.

## Troubleshooting
See `student-lab/README.md`'s Troubleshooting section (student-facing)
and `instructor/troubleshooting.md` (instructor-facing, covers common
wrong turns and how to steer students back).

## Instructor solution
`instructor/solution/order_check.py`, with
`instructor/instructor-guide.md` explaining the reasoning behind each
fix and `instructor/troubleshooting.md` covering common student
mistakes.

## Validation criteria
- `scripts/run_lab_checks.py output/validate-event-order-eval-bl` passes:
  required files/dirs present, `student-lab/` passes the structural/leak
  scan, and the instructor solution overlaid on the starter passes
  `validate.json`'s setup + validate commands end to end.
- The starter (unmodified) fails validation — that is the exercise, not
  a bug.

## Acquired skills
- Distinguishing physical/arrival order from logical/chronological order
  in an event log.
- Writing a deterministic, running-state comparison (not a one-shot
  previous-row diff) to catch cascading anomalies.
- Designing an explicit tie-break and missing-value rule for a sort key
  instead of relying on implementation-defined behavior.
- Writing an automated, exit-code-based check for a data-cleaning script.
