# DataEngLab Course Factory

This repository is a Claude Code kit for generating complete, practical Data Engineering learning assets for DataEngLab. It produces full Tutor LMS courses, standalone hands-on labs, native Elementor JSON when a valid reference exists, automated validation, instructor-only solutions, and student-ready ZIP packages.

The project is intentionally content-only. It does not generate PHP, WordPress plugins, WordPress themes, shortcodes, custom Elementor JavaScript, custom Elementor CSS, database changes, hosting changes, or deployments.

## What it generates

For a full course, the kit creates:

- a structured `course-spec.json` used as the source of truth;
- a Tutor LMS-compatible course overview, curriculum, lessons, and quizzes;
- a runnable student lab with deterministic data and automated tests;
- separate instructor solutions, guide, and troubleshooting notes;
- a native Elementor landing page JSON when the available reference tier allows it;
- a `validate.json` contract that records the setup and validation commands;
- a student-only ZIP package.

For a standalone lab, it creates:

- `lab-spec.md` as the lab design source of truth;
- live-page-ready `page-content.md`;
- `student-lab/` with setup, starter files, datasets, tasks, hints, and tests;
- instructor-only solution and troubleshooting files;
- validation and packaging artifacts.

## Repository layout

```text
.claude/                Claude Code agents and skills
elementor/              Elementor template corpus and generated sections
output/                 Generated courses and labs
scripts/                Validation and packaging scripts
CLAUDE.md               Main project rules and generation workflow
START_HERE.md           First-run checklist
```

## Prerequisites

- Python available as `python`.
- Claude Code, if you want to use the `course-design` / `lab-design` skill workflows.
- For verified Elementor generation, place a real Elementor export at
  `elementor-reference.json` in the repository root.

If no canonical Elementor export is present, the frontend workflow falls back to the checked-in Elementor corpus when permitted by `CLAUDE.md`, and writes a `SOURCE.md` disclosure next to generated JSON. If no valid reference tier is available, it writes `elementor/REFERENCE_REQUIRED.md` instead of inventing an Elementor page.

## Quick start

Open this repository in Claude Code and ask it to read the project context:

```text
Read CLAUDE.md and the relevant skill files under .claude/.
Do not modify anything yet.
Tell me whether the Elementor reference is usable.
```

Then generate a full course by invoking the `course-design` skill with a
course brief:

```text
/course-design
Title: Build a Reliable Python ETL Pipeline
Audience: Beginners who know basic Python
Level: Beginner
Duration: 2 hours
Technologies: Python, pandas, pytest, CSV, Parquet
Scenario: A logistics company receives shipment files with missing fields,
invalid dates, and duplicate shipment IDs.
Deliverable: A tested ETL script that writes clean and quarantined outputs.
```

Include the title, slug when you need a specific output directory, audience,
level, duration, technologies, scenario, outcomes, lab tasks, deliverables, and
validation criteria. The skill can also read a brief from any path you provide.

## Full-course workflow

The `course-design` skill (`.claude/skills/course-design/SKILL.md`) follows this sequence:

1. Claude writes `output/<slug>/course-spec.json` first, as the source of truth.
2. The `content-writer` subagent generates Tutor LMS content: course overview, curriculum, lessons, and quizzes.
3. The `lab-engineer` subagent generates the student lab, tests, instructor files, and `validate.json`.
4. The `frontend-agent` skill/subagent creates `output/<slug>/elementor/landing-page.json` or a safe fallback notice.
5. `scripts/run_checks.py` validates structure, content, Elementor JSON, and lab execution.
6. The `course-reviewer` subagent writes `review-report.md` with a `PASS` or `FAIL` verdict.
7. Claude fixes blocking review findings, reruns checks, and repeats review until the course passes or the limitation is explicitly reported.
8. `scripts/package_student_lab.py` creates the student ZIP.

Expected full-course output:

```text
output/<slug>/
|-- course-spec.json
|-- review-report.md
|-- validate.json
|-- elementor/
|-- tutor-lms/
|   |-- course-overview.md
|   |-- curriculum.md
|   |-- lessons/
|   `-- quizzes/
|-- student-lab/
|   |-- README.md
|   |-- starter/
|   |-- datasets/
|   `-- tests/
|-- instructor/
|   |-- solution/
|   |-- instructor-guide.md
|   `-- troubleshooting.md
`-- packages/
```

## Standalone lab workflow

Use the `lab-design` skill when you want a single lab rather than a complete course. A good lab starts from one concrete data-engineering failure, for example: duplicate revenue in a dashboard, late-arriving events, broken customer history, invalid timestamps, or a pipeline that is not idempotent. Use the `publish-practical-lab` skill afterward only if you want to push that lab's already-written `page-content.md` live to dataenglab.com, with explicit approval.
Expected standalone-lab output:

```text
output/<slug>/
|-- lab-spec.md
|-- page-content.md
|-- validate.json
|-- student-lab/
|   |-- README.md
|   |-- build_db.py
|   |-- datasets/
|   |-- starter/
|   `-- tests/
|-- instructor/
|   |-- solution/
|   |-- instructor-guide.md
|   `-- troubleshooting.md
`-- packages/
```

## Validation

Run the combined checker for either a full course or a standalone lab:

```powershell
python scripts/run_checks.py output/<slug>
```

`run_checks.py` auto-detects the output type:

- `course-spec.json` means full-course validation;
- `lab-spec.md` means standalone-lab validation.

For standalone labs, you can also run:

```powershell
python scripts/run_lab_checks.py output/<slug>
```

For focused debugging, use the lower-level scripts:

```powershell
python scripts/validate_spec.py output/<slug>
python scripts/validate_course.py output/<slug>
python scripts/validate_content.py output/<slug>
python scripts/validate_lab.py output/<slug>/student-lab
python scripts/validate_lab_execution.py output/<slug>
python scripts/validate_elementor_json.py output/<slug>/elementor/landing-page.json
```

`validate_lab_execution.py` is the proof that a lab is actually solvable. It
copies `student-lab/` to a temporary directory, overlays files from
`instructor/solution/` onto matching files in `student-lab/starter/`, then runs
the exact setup and validation commands from `validate.json`.

## Packaging

Create the student-only lab archive:

```powershell
python scripts/package_student_lab.py output/<slug>
```

The package is written to:

```text
output/<slug>/packages/<slug>-student-lab.zip
```

Only `student-lab/` is included. Instructor solutions, troubleshooting notes, and page publishing content stay out of the ZIP.

## Project rules

- Public and student-facing content must be English.
- At least 50 percent of course learning time must be practical.
- Keep instructor solutions out of `student-lab/`.
- Keep `validate.json` commands in sync with the lab README validation section.
- Use deterministic datasets with deliberate edge cases.
- Never claim checks passed unless the scripts were actually run.
- Do not publish to `dataenglab.com` without explicit approval for the exact
  page and change.

Read `CLAUDE.md` before generating or publishing anything. It is the source of truth for project constraints, Elementor reference tiers, validation rules, and the live-site safety policy.
