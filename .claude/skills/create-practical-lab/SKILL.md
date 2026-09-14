---
name: create-practical-lab
description: Generate one complete, standalone practical data-engineering lab for DataEngLab (dataenglab.com/labs) — business scenario, deterministic dataset with deliberate edge cases, numbered tasks with hints, automated validation that actually runs, a separate instructor solution, and live-page-ready content — without building a full course around it. Use this whenever the user asks to create, add, draft, or update a lab, exercise, or hands-on scenario for DataEngLab or the labs page, or describes a data bug/scenario students should practice diagnosing or fixing (e.g. "students should practice deduplicating late-arriving records", "add a lab about slowly changing dimensions", "we need something on window functions for anomaly detection") — even when the word "lab" never comes up. Do not use this for building an entire course (curriculum, lessons, quizzes, Elementor landing page); that's the separate `/create-course` workflow, and this skill should point there if the user actually wants a full course.
---

# Create a practical lab for DataEngLab

A DataEngLab lab is a small, self-contained exercise: a student downloads a zip, runs a build script against a deterministic dataset, works through a handful of numbered tasks, and checks their answer with an automated test that exits non-zero on failure. It is deliberately lighter than a full course
— no curriculum, no quizzes, no Elementor landing page — and it lives on its own at `dataenglab.com/labs/<slug>`.

`output/investigate-duplicate-orders/` is a real, working example of everything this skill produces. When anything below is ambiguous, go look at that directory rather than guessing.

## Before you start: confirm this is a lab, not a course

If the user actually wants a full course (multiple lessons, a curriculum, quizzes, a landing page), stop and point them at `/create-course` instead — this skill only produces the standalone lab pieces described in `CLAUDE.md`'s "Practical labs" section, not the rest of a course.

## What makes a lab worth publishing

Before writing anything, get clear on the one bug or design problem the lab teaches. Every good DataEngLab lab has:

- **A specific, real-sounding failure** a data engineer would actually be asked to fix — not "here's a dataset, explore it," but "the dashboard double-counts revenue, find out why." The business framing is what makes the tasks feel worth doing.
- **A dataset small enough to read directly**, but constructed so it *contains* the exact edge cases the tasks are about. If a task is about handling NULLs and ties in a dedup key, the CSV needs an order with a NULL timestamp and another with two rows that tie exactly — not because more data would hurt, but because a student should be able to open the CSV, see the ugly row, and understand the bug with their own eyes. Invented data that doesn't actually exercise the target bug produces a lab whose automated check can't tell a correct fix from a lucky one.
- **Tasks that build on each other toward one final query/script**, each one a checkpoint a student can verify before moving on, ending in a task that assembles everything and runs the real automated check.

Ask the user (or infer from what they've said, and confirm) before drafting:

1. What's the failure/scenario, in one or two sentences, and who "asks" the student to fix it?
2. What tool/language (SQL against SQLite, pandas, a CLI script, etc.) and any hard constraints (no installs, no Docker, no network)?
3. Roughly what level (beginner/intermediate/advanced) and how long should it take? At least half of that time needs to be the student actually writing code against Task hints below — a lab that's mostly reading is a lesson, not a lab.
4. Anything about the DataEngLab brand or template you already know they want reflected (see `references/brand.md` for the color tokens if the live-page content needs them).

## Steps

### 1. Pick a slug and lay out the directory

Kebab-case the title into `<slug>`, then create `output/<slug>/` with this shape (mirrors `output/investigate-duplicate-orders/` exactly):

```text
output/<slug>/
├── lab-spec.md
├── validate.json
├── page-content.md
├── student-lab/
│   ├── README.md
│   ├── build_db.py            (or equivalent setup script)
│   ├── datasets/
│   ├── starter/
│   └── tests/
├── instructor/
│   ├── solution/
│   ├── instructor-guide.md
│   └── troubleshooting.md
└── packages/                  (created by the packaging script, step 6)
```

### 2. Write `lab-spec.md`

This is the lab's source of truth — write it before the README, tests, or anything else, the same way `course-spec.json` anchors a full course. Cover every item CLAUDEmd's "Practical labs" section requires: business context, measurable objectives, setup, starter files, deterministic data (and which specific edge cases it encodes and why),numbered tasks, where hints live, expected output, automated checks, reset procedure, and where the instructor solution and troubleshooting live. If you can't fill in one of these sections concretely, the lab design isn't finished yet — don't move on.

### 3. Build the dataset and starter files

Generate the CSVs (or other source data) with the deliberate edge cases from step 2, plus a `build_db.py` (or equivalent) that's idempotent — running it twice, or running it after the student has broken their local state, always gets back to the same starting point. That script is also the lab's reset procedure, so say so explicitly rather han describing a separate one.

Put the buggy/incomplete artifact students start from in `starter/` — e.g. a `dashboard_query.sql` that reproduces the bug (read-only reference, tasks should say not to edit it) and a `solution.sql`/`solution.py` the student fills in themselves. That exact filename is safe to use: `validate_lab.py`'s leak check only flags `solution.sql`/solution.py`/etc. *outside* `starter/` — inside it, that name is expected to be an incomplete placeholder, not a leak.

When a dataset field can be NULL, represent it the same way the reference lab does: an empty string in the CSV, which SQLite reads back as `NULL`. Whatever test script compares database output to an expected-results fixture will need to treat `''` and `NULL`/`None` as equivalent — write that normalization once rather than let a false mismatch block a correct answer.

### 4. Write `student-lab/README.md`

This is what the student reads, and — because DataEngLab labs are published to a page that mirrors it closely — it's also the raw material for `page-content.md` in step 5. Structure:

```markdown
# <Title>
**Level:** ... · **Duration:** ~<n> min · **Tags:** ...

## Business context
## Environment
## Setup
## Tasks
### Task 1 — ...
### Task 2 — ...
...
## Hints
(one collapsible section per task that needs one, using <details>/<summary>)
## Expected output
## Validation
## Reset procedure
## Troubleshooting
```

Two things matter more than the exact wording:

- **Troubleshooting entries must name the actual wrong output a student  would see** ("still get 17 rows instead of 12") rather than generic advice — that's what makes them diagnostic instead of decorative.
- **Never put a working solution inside `student-lab/`.** Nothing under that directory should let a student skip the exercise — that's a hard  rule, not a style choice, and `scripts/validate_lab.py` (step 6) checks for common solution-file names and rejects the lab if it finds one.

### 5. Write `page-content.md` (the live-page-ready content)

DataEngLab's `/labs/<slug>` page template renders specific fields — badges, schema/environment cards, a task/hint sequence, troubleshooting, a progress checklist. Write `page-content.md` with one section per field so whoever publishes this lab (see CLAUDE.md's "Publishing to dataenglab.com" section) can map it straight onto the template without re-deriving anything from the README by hand:

```markdown
# Page content: <Title>

## Badges
Price: Free | Topic: <e.g. SQL> | Level: <Beginner/Intermediate/Advanced>
Duration: <n> min | Tasks: <n>

## Lede
<the 1-3 sentence business-scenario hook>

## Outcomes (checklist)
- ...

## Environment (one block per table/data source)
### <table name> — grain: <one row per ...>
<one-line description>
| key | field | type | description |
|-----|-------|------|-------------|
...

## Tasks
### Task <n> — <title>
<prompt, same wording as the README>
Hint: <if present>

## Expected output
## Troubleshooting
```

Keep this content word-for-word consistent with `student-lab/README.md` — they describe the same lab from two surfaces, and letting them drift is exactly the kind of divergence CLAUDE.md's `validate.json`/README rule guards against for the machine-readable side; do the same here for the human-readable side.

### 6. Write the instructor solution and `validate.json`

`instructor/solution/` must contain a file for **every** starter file the student is meant to complete, at the **same relative path** as its `starter/` counterpart — `scripts/validate_lab_execution.py` (next step) copies `student-lab/` to a temp directory and overlays these files directly onto the matching `starter/` paths, so a name that doesn't line up silently fails the check with "instructor/solution file has no matching starter file."

Write `validate.json` at the lab root:

```json
{"setup": [["python", "build_db.py"]], "validate": [["python", "tests/test_solution.py"]]}
```

Every entry is a full argv list (no shell syntax), run from inside `student-lab/`, and must be **exactly** the commands your README's
`## Validation` section documents — that's the contract between the human-readable and machine-readable instructions, and it's checked, not just a convention.

The test script itself (`tests/test_solution.py` or equivalent) must exit non-zero on failure — never assert success without checking; a lab whose check always passes is worse than no check.

### 7. Actually run validation — don't skip this

```bash
python scripts/validate_lab.py output/<slug>/student-lab
python scripts/validate_lab_execution.py output/<slug>
```

The first checks structural hygiene (README present, tests present, no solution-file leaks, no accidental credentials or machine-specific paths). The second is the real proof the lab is solvable: it copies `student-lab/` to a temp directory, overlays `instructor/solution/` onto `starter/`, and runs the exact `setup`/`validate` commands from `validate.json` there — the student-facing `starter/` files are *expected* to fail this (that's the exercise); it's the solution that has to pass. If either script ails, fix the lab and re-run — don't move on with a red check, and don't report a lab as done based on what you expect the test to do rather than what it actually did.

### 8. Package student-facing files

```bash
python scripts/package_student_lab.py output/<slug>
```

Produces `output/<slug>/packages/<slug>-student-lab.zip` from `student-lab/`
only — instructor material and `page-content.md` never go in the zip.

### 9. Report back

Tell the user: the slug/directory, a one-line summary of the scenario and tasks, the two validation commands and their real exit status (never "should pass" — only what ctually happened when you ran them), and that `page-content.md` is ready whenever they want to publish it, which is a separate, explicitly-confirmed step per CLAUDE.md's Publishing to dataenglab.com" section — this skill prepares the lab, it doesn't push it live.

## Reference

- `output/investigate-duplicate-orders/` — a complete worked example of
  every file this skill produces.
- `CLAUDE.md`'s "Practical labs" and "Publishing to dataenglab.com" sections
  — the rules this skill implements.
- `references/brand.md` — color tokens, if `page-content.md`'s badges or
  any styling notes need them.
