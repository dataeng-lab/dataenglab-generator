# Lab Output Contract

Read this when creating or materially revising a standalone DataEngLab lab.
Keep generated content specific to the requested scenario; these examples are
contracts, not filler text.

## Output Tree

```text
output/<slug>/
|-- lab-spec.md
|-- page-content.md
|-- validate.json
|-- student-lab/
|   |-- README.md
|   |-- build_db.py              optional name, but setup must be idempotent
|   |-- datasets/
|   |-- starter/
|   `-- tests/
|-- instructor/
|   |-- solution/
|   |-- instructor-guide.md
|   `-- troubleshooting.md
`-- packages/                   created by package_student_lab.py
```

Every path except `packages/` must exist before validation. The package script creates `packages/<slug>-student-lab.zip` from `student-lab/` only.

## lab-spec.md

Write this first. It is the source of truth for the README, page content, tests, and instructor material.

```markdown
# Practical Lab Specification

## Business context
Who noticed the problem, what is broken, and why a data engineer must fix it.

## Learning objectives
- Observable skill 1
- Observable skill 2

## Environment
Tool versions, install assumptions, and explicit no-network/no-Docker notes when applicable.

## Estimated duration
<n> minutes. At least half the time should be hands-on work.

## Starter files
- `student-lab/...` - what each file is for

## Dataset
Name each dataset, its row count or approximate size, its grain, and the exact edge cases it contains.

## Tasks
1. Reproduce or observe the failure.
2. Diagnose the root cause.
3. Implement the fix in the starter file.
4. Validate the final output.

## Hints
Where hints appear in the README and which tasks get them.

## Validation
Commands run from inside `student-lab/`. These must match `validate.json`.

## Expected output
Concrete row counts, totals, columns, files, or messages students should see.

## Reset procedure
Usually the setup command again, if it rebuilds deterministic state.

## Troubleshooting
Point to student-facing and instructor-facing troubleshooting.

## Instructor solution
List every solution file and its matching starter path.
```

## Student README

The README is student-facing and should be usable without instructor context.
Use this structure unless the lab genuinely needs a small variation.

````markdown
# <Title>

**Level:** <Beginner|Intermediate|Advanced> | **Duration:** ~<n> min | **Tags:** <tag>, <tag>

## Business context
Short scenario with the concrete failure.

## Environment
- Python 3.9+ or the chosen runtime
- Any install, Docker, or no-network note

## Setup
```bash
python build_db.py
```

## Tasks

### Task 1 - <verb phrase>
Prompt and optional command/query.

### Task 2 - <verb phrase>
Prompt and optional command/query.

## Hints

<details>
<summary>Hint for Task N</summary>
One focused nudge. Do not paste the complete solution.
</details>

## Expected output
Concrete result: row count, schema, file path, total, or passing message.

## Validation
```bash
python tests/test_solution.py
```
Mention what the test checks and that it exits non-zero on failure.

## Reset procedure
```bash
python build_db.py
```

## Troubleshooting
- **Concrete symptom** - likely cause and next action.
````

Troubleshooting entries should name wrong outputs students will actually see:
"Still 17 rows instead of 12" is useful; "dedup did not work" is too vague.

## page-content.md

This is live-page-ready content, not Elementor JSON. Keep it consistent with the
README so the future page does not drift from the downloadable lab.

```markdown
# Page content: <Title>

## Badges
Price: Free | Topic: <SQL/Python/etc.> | Level: <...>
Duration: <n> min | Tasks: <n>

## Lede
One to three sentences introducing the business failure.

## Outcomes
- Outcome 1
- Outcome 2

## Environment

### <table or data source> - grain: <one row per ...>
One-line description.

| key | field | type | description |
|-----|-------|------|-------------|
| yes/no | field_name | text/integer/etc. | ... |

## Tasks

### Task 1 - <title>
Same meaning as the README task, shortened only if needed for the page.
Hint: Optional hint.

## Expected output
Concrete final output.

## Troubleshooting
- **Concrete symptom** - likely cause and next action.
```

## validate.json

`validate.json` lives at the lab root and contains argv arrays, not shell
strings. Commands run from inside `student-lab/`.

```json
{
  "setup": [["python", "build_db.py"]],
  "validate": [["python", "tests/test_solution.py"]]
}
```

The setup command can be empty only when the lab truly needs no setup. The
validate array is mandatory.

## Tests

Tests should check the exercise outcome, not just that a file exists. Prefer
assertions like:

- required columns are present;
- one row per business key;
- expected rows or aggregate totals match a fixture;
- invalid records are quarantined or flagged;
- reset/setup produces deterministic state.

The starter version may fail. The instructor solution must pass after `validate_lab_execution.py` overlays it onto matching starter files.

## Instructor Files

`instructor/solution/` must mirror the relative path of each file students are meant to complete under `student-lab/starter/`.

Example:

```text
student-lab/starter/solution.sql
instructor/solution/solution.sql
```

Add `instructor/instructor-guide.md` for the reasoning behind the solution and
`instructor/troubleshooting.md` for coaching notes that should not appear in the
student ZIP.
