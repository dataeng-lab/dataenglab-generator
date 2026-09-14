# Summary: validate-event-order-eval-ws (built with the lab-design skill)

## Real output path

```
E:\dataeng-lab\dataenglab-generator\output\validate-event-order-eval-ws\
```

This is a real, materialized directory in the repo — not simulated.

## Scenario

Business-facing title: "Detect and Handle Out-of-Order Event Timestamps."
SensorGrid's IoT temperature-sensor feed streams readings into a CSV
export. Delivery is unreliable (late arrivals, one clock-skewed sensor).
The current live-feed script trusts file/arrival order with no timestamp
checking, so it displays real-but-impossible regressions (a temperature
"dip" from a late-arriving reading, and a "spike then drop" from a
clock-fault reading 6 hours in the future). The student writes
`process_readings()` to detect out-of-order readings (reorder them back
into a corrected sequence) versus clock-skew/missing-timestamp readings
(quarantine them out), using Python's standard library only (no pandas,
no Docker, no network).

## Every file/directory created under `output/validate-event-order-eval-ws/`

```
output/validate-event-order-eval-ws/
|-- lab-spec.md
|-- page-content.md
|-- validate.json
|-- student-lab/
|   |-- README.md
|   |-- reset.py
|   |-- datasets/
|   |   `-- sensor_readings.csv        (23 rows, 4 devices, hand-verified edge cases)
|   |-- starter/
|   |   |-- naive_trend.py             (read-only buggy reference script)
|   |   `-- order_guard.py             (student implements process_readings(); raises NotImplementedError)
|   `-- tests/
|       |-- test_solution.py           (7 unittest cases, exits non-zero on failure)
|       |-- expected_corrected.csv     (21-row fixture)
|       `-- expected_flagged.csv       (3-row fixture)
|-- instructor/
|   |-- instructor-guide.md
|   |-- troubleshooting.md
|   `-- solution/
|       `-- order_guard.py             (full working solution)
`-- packages/
    `-- validate-event-order-eval-ws-student-lab.zip   (8 files, student-facing only)
```

Note: `student-lab/output/` is also created/recreated by `reset.py` at
setup/reset time and is where the scripts write their CSV outputs; it is
not a lab-design deliverable file. `instructor/solution/__pycache__/` is
a Python bytecode cache left over from manual verification runs, already
covered by the repo's `.gitignore` (`__pycache__/`).

## Dataset design (deterministic, hand-verified)

`sensor_readings.csv`: 23 rows, devices `D-100`..`D-103`, global
`arrival_seq` 1-23 = file order. Edge cases:
- `D-100`: 5 baseline in-order rows, no flags.
- `D-101`: 6 rows, one (`R-0010`) genuinely out-of-order (arrives after a
  later timestamp already raised the device's running max) - corrected
  back into the sequence, flagged.
- `D-102`: 6 rows, one (`R-0011`) with a blank `event_ts` (invalid,
  quarantined), plus an exact-timestamp tie between two rows requiring an
  `arrival_seq` tie-break.
- `D-103`: 6 rows, one (`R-0012`) six hours ahead of the device's running
  max - a clock-skew anomaly, quarantined - followed by a normal reading
  that must not be mis-flagged out-of-order against the quarantined value.

The expected `corrected_readings.csv` (21 rows) and
`flagged_readings.csv` (3 rows) fixtures were hand-derived by walking the
algorithm row by row before writing any code, then confirmed by actually
running the instructor solution and diffing its real output against
those fixtures (see Commands below) - not just by inspection.

## Every command run, with real results

All commands were actually executed in this session (Windows / Git Bash),
from the paths shown. None were simulated.

1. `mkdir -p output/validate-event-order-eval-ws/student-lab/{datasets,starter,tests} output/validate-event-order-eval-ws/instructor/solution`
   Result: directories created (verified with `ls`).

2. `python reset.py` (cwd: `student-lab/`)
   Result: `Reset output` - created an empty `output/` directory.

3. `python starter/naive_trend.py` (cwd: `student-lab/`)
   Result: ran cleanly, printed the full 23-row live-feed transcript.
   Confirmed the designed bug is real and visible: `D-101` shows a value
   going down at `08:04:00` (flagged inline as `<-- value went DOWN`),
   `D-103` spikes to `61.0C at 2026-03-02 14:08:00` then drops to `60.9C`
   a few lines later, and the "final displayed value per device" section
   happens to self-correct to the true final values for all 4 devices -
   confirming the bug is about transient impossible values, not a
   permanently wrong final answer.

4. Manual sanity check of the instructor solution's algorithm, run
   directly via `python -c "..."` importing
   `instructor/solution/order_guard.py` (with `DATASET` path overridden
   to point at `student-lab/datasets/sensor_readings.csv` from that
   working directory, since the solution module's own path arithmetic
   assumes it is running from `student-lab/starter/`, which is where it
   lands after the validator's overlay step).
   Result: `corrected count 21`, `flagged count 3`; the 3 flagged rows
   and all 21 corrected rows printed and matched the hand-derived
   `tests/expected_corrected.csv` / `tests/expected_flagged.csv` fixtures
   exactly, row for row.

5. `python scripts/run_lab_checks.py output/validate-event-order-eval-ws`
   (cwd: repo root)
   Result: PASS on both stages -
   - `validate_lab.py output/validate-event-order-eval-ws/student-lab` ->
     `OK` / `PASS` (structural contract check: starter/tests/datasets
     present, no leaked solutions under `student-lab/`, etc.)
   - `validate_lab_execution.py output/validate-event-order-eval-ws` ->
     `OK: instructor solution passes the lab tests` / `PASS` (copied
     `student-lab/` to a temp dir, overlaid `instructor/solution/` onto
     `starter/`, ran `validate.json`'s setup + validate commands there,
     and the instructor solution passed all 7 unittest cases)
   - Final line: `ALL LAB CHECKS PASSED`

6. `python reset.py` then `python tests/test_solution.py`
   (cwd: `student-lab/`, unmodified starter - i.e. before any student
   edits)
   Result: exit code 1, 3 failures / 4 skipped, as required by the
   contract ("starter-facing files are expected to fail validation -
   that's the exercise"). The failure output shows
   `starter/order_guard.py` raising the intended
   `NotImplementedError: implement process_readings() - see README.md
   Tasks 3-5`, proving the starter is genuinely incomplete rather than a
   silently-passing stub.

7. `python reset.py` (cwd: `student-lab/`) - reset back to a clean state
   after the deliberate starter-failure check, before packaging.

8. `python scripts/package_student_lab.py output/validate-event-order-eval-ws`
   (cwd: repo root)
   Result: `OK: .../packages/validate-event-order-eval-ws-student-lab.zip`,
   `Files: 8`.

9. Verified package contents via `python -c "import zipfile; ..."`
   listing all 8 zip entries. Result: only student-facing files present
   (`datasets/sensor_readings.csv`, `README.md`, `reset.py`,
   `starter/naive_trend.py`, `starter/order_guard.py`,
   `tests/test_solution.py`, `tests/expected_corrected.csv`,
   `tests/expected_flagged.csv`) - no `page-content.md`, no
   `instructor/`, confirming no solution leak.

Total real commands run: 9 (plus routine `ls` / `find` / `grep`
directory listings used for verification, not counted as lab-build or
validation commands).

## Limitations / things not done

- The lab-design skill's workflow step 7 says "Run
  `python scripts/run_lab_checks.py output/<slug>`. Fix every failure and
  rerun until it passes." This passed on the first real run after the
  content was written - no fix-and-rerun cycle was needed, so there is no
  iteration history to report beyond the one passing run.
- No Elementor/labs-page JSON was generated for this lab (the skill's
  Gotchas/contract don't require one for a lab build unless a
  `labs-page.json`-style landing page is separately requested; this task
  only asked for the standalone lab). `scripts/validate_elementor_json.py`
  was correctly not run, since no such file exists for this lab.
- This is a standalone lab, not a full course - no Tutor LMS
  curriculum/lessons/quizzes or course-level Elementor landing page were
  produced, per the `lab-design` skill's own routing rule (that would be
  `course-design`'s job).
- Context7 (MCP docs lookup) was not needed or used - the lab uses only
  Python's standard library (`csv`, `datetime`, `pathlib`), no
  third-party API surface to verify against current docs.
- No live publishing was performed or attempted (out of scope for
  `lab-design`; that is `publish-practical-lab`'s job and requires
  separate explicit user approval).
