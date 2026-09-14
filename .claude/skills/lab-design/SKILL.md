---
name: lab-design
description: Create or update one standalone DataEngLab practical lab under output, including lab-spec, student files, deterministic data, tests, instructor solution, validate.json, page-content, validation, and packaging. Use for lab, exercise, or hands-on data scenario requests, not full courses or live publishing.
metadata:
  short-description: Build a standalone DataEngLab lab
---

# Lab Design

Build one small, self-contained DataEngLab lab. A lab is not a course and not a publish action: the student downloads a ZIP, builds a deterministic local dataset, completes numbered tasks, and proves the answer with an automated test that exits non-zero on failure.

## Routing

- If the user wants lessons, quizzes, curriculum, or a course landing page, stop and point them to the `course-design` skill.
- If the user wants an existing lab published to `dataenglab.com`, use `publish-practical-lab` only after `output/<slug>/page-content.md` exists.
- Otherwise, create or update the standalone lab files. Infer reasonable defaults when possible. Ask only when the missing scenario, tool, level, or constraint would make the lab impossible to design concretely.

## Read First

Before creating or materially revising a lab:

1. Read `CLAUDE.md` for the project overview, then `.claude/rules/labs.md`
   (practical lab requirements) and `.claude/rules/publishing.md` (the
   publishing boundary). `CLAUDE.md` is now a short overview that delegates to
   `.claude/rules/*.md` rather than containing these sections itself.
2. Read [contracts/lab-output-contract.md](contracts/lab-output-contract.md) for the required output tree, file contracts, and validation contract.
3. Memory: when this workflow is executed by the `lab-engineer` subagent, use
   that agent's project memory and open relevant topic files only as needed.
   When invoking this skill directly, read
   [contracts/memory.md](contracts/memory.md) for durable environment and
   validation patterns. Pattern memory is not a substitute for verifying fresh.
4. If a shape decision is ambiguous, inspect `output/investigate-duplicate-orders/` as the canonical working example.

When updating an existing lab, read its current `lab-spec.md`, `student-lab/README.md`, `page-content.md`, `validate.json`, tests, and instructor solution before editing.

## Quality Bar

A publishable DataEngLab lab has:

- one concrete data-engineering failure or design problem, framed as a realistic business request;
- a small deterministic dataset that visibly contains the edge cases the tasks  teach;
- tasks that build toward one final query, script, or artifact;
- hints that unblock reasoning without giving away the full answer;
- tests that assert the real behavior and fail non-zero on wrong answers;
- a separate instructor solution that exactly matches the starter files it replaces during validation;
- student-facing and public content in English;
- no credentials, API keys, network dependency, or machine-specific paths.

Prefer SQLite plus SQL for query, grain, modeling, and debugging labs. Prefer Python plus pytest or unittest for file and ETL labs. Avoid Docker and external services unless the user explicitly requests them or the lab cannot be realistic without them.

## Workflow

1. Design the lab first in `output/<slug>/lab-spec.md`. Name the failure, tool, level, duration, dataset edge cases, tasks, validation, reset procedure, and instructor-only artifacts before writing implementation files.
2. Create `student-lab/` with deterministic datasets, idempotent setup/reset, incomplete starter files, and automated tests.
3. Write `student-lab/README.md` from the spec. Keep the tasks, validation commands, expected output, and troubleshooting concrete.
4. Write `page-content.md` from the same facts as the README so the future labs page can be built without reinterpreting the exercise.
5. Write `instructor/solution/`, `instructor/instructor-guide.md`, and `instructor/troubleshooting.md`.
6. Write `validate.json` at the lab root. Its argv arrays run from inside `student-lab/` and must match the commands documented in the README.
7. Run `python scripts/run_lab_checks.py output/<slug>`. Fix every failure and rerun until it passes.
8. Run `python scripts/package_student_lab.py output/<slug>` only after validation passes.
9. Report the slug, scenario, files produced or changed, exact commands run, real results, package path, and any remaining limitation.

## Gotchas

- Standalone labs use `lab-spec.md`, not `course-spec.json`.
- `scripts/run_checks.py output/<slug>` auto-detects standalone labs, but `scripts/run_lab_checks.py output/<slug>` is the direct lab checker.
- `validate_lab_execution.py` copies `student-lab/` to a temp directory and overlays every file in `instructor/solution/` onto the matching relative path under `student-lab/starter/`. A solution file with no starter counterpart fails validation.
- Starter placeholders named `solution.sql` or `solution.py` are allowed inside `student-lab/starter/`. Working solutions anywhere else under `student-lab/` are leaks.
- Empty CSV fields are the project convention for SQL `NULL` values. Normalize `""`, `NULL`, and `None` in tests when that distinction is incidental.
- The setup script should also be the reset procedure when practical. It must be idempotent.
- `page-content.md` and instructor files are not included in the student ZIP.
- Do not publish. Live publishing requires a separate explicit approval handled by `publish-practical-lab`.

## Validation Commands

Use the wrapper first:

```bash
python scripts/run_lab_checks.py output/<slug>
```

For debugging individual stages:

```bash
python scripts/validate_lab.py output/<slug>/student-lab
python scripts/validate_lab_execution.py output/<slug>
python scripts/validate_elementor_json.py output/<slug>/elementor/labs-page.json
```

Run the Elementor JSON validator only when a lab page JSON exists. Do not claim any check passed unless you actually ran it and saw a passing result.
