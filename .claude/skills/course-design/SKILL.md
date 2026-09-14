---
name: course-design
description: Create or update one complete DataEngLab course under output, including course-spec, Tutor LMS content, lessons, quizzes, student lab, instructor files, validate.json, Elementor course page output, validation, review, and packaging. Use for full course requests, not standalone labs or live publishing.
metadata:
  short-description: Build a complete DataEngLab course
---

# Course Design

Build one complete practical DataEngLab course. A course includes a structured
spec, Tutor LMS content, lessons, quizzes, a runnable student lab, instructor
material, Elementor page output or safe fallback, validation, review, and a
student ZIP package.

## Routing

- If the user wants only one downloadable exercise or lab, use `lab-design`.
- If the user wants a finished standalone lab published live, use
  `publish-practical-lab` after its `page-content.md` exists.
- If the user wants a full course with curriculum, lessons, quizzes, and a
  practical lab, use this skill.
- Do not publish to `dataenglab.com` from this skill. Publishing always needs a
  separate explicit approval for the exact live-site change.

## Read First

Before creating or materially revising a course:

1. Read `CLAUDE.md`; it is the source of truth for course rules, Elementor
   reference tiers, validation, and publishing boundaries.
2. Read the course request file or the user's requested course brief.
3. Read [contracts/course-output-contract.md](contracts/course-output-contract.md)
   for the output tree, `course-spec.json` schema, content contracts, and
   validation expectations.
4. Use Context7 MCP for current framework/library documentation when the course
   depends on specific tools, APIs, or version-sensitive behavior.
5. For Elementor output, use `.claude/skills/frontend-agent/SKILL.md`; do not
   duplicate that workflow here.

When updating an existing course, read its current `course-spec.json`,
`tutor-lms/`, `student-lab/README.md`, `validate.json`, instructor files,
Elementor output, and `review-report.md` before editing.

## Quality Bar

A valid DataEngLab course has:

- a `course-spec.json` written before course prose and used as the source of
  truth for title, slug, audience, level, outcomes, duration, technologies,
  scenario, deliverable, validation criteria, acquired skills, and curriculum;
- at least 50 percent practical learning time in `duration_minutes`;
- Tutor LMS-compatible content: course overview, curriculum, lessons, and
  quizzes, without assuming Tutor LMS Pro;
- lessons that follow the repository's required lesson heading contract;
- quizzes with answer letters, explanations, difficulty, and related lesson;
- a deterministic student lab with automated validation and separate instructor
  solution;
- a root `validate.json` whose commands match the lab README validation section;
- Elementor JSON generated only from the allowed reference tier, or
  `elementor/REFERENCE_REQUIRED.md` when no tier is available;
- technical claims, commands, examples, and lab code aligned with current
  library/framework docs checked through Context7 MCP when available;
- public and student-facing content in English;
- no PHP, custom Elementor CSS or JavaScript, shortcodes, credentials, direct
  database operations, or live-site deployment.

## Context7 MCP

Use Context7 before writing technical explanations, commands, dependencies, or
lab code that rely on current behavior of libraries or frameworks such as
Airflow, dbt, Spark, pandas, Polars, DuckDB, PostgreSQL, pytest, Docker Compose,
Kafka, or cloud SDKs.

Default flow when Context7 tools are available:

1. Resolve the package or framework with Context7's library-ID lookup.
2. Fetch focused docs for the specific topic the course uses, such as DAG
   scheduling, dbt incremental models, pytest fixtures, pandas IO, or Docker
   Compose service health.
3. Use the docs to choose commands, imports, config keys, version constraints,
   and examples.
4. Keep the course practical: cite docs internally through accurate code and
   instructions, but do not paste long documentation excerpts into lessons.

If Context7 is unavailable in the current tool session, continue from stable
project knowledge and local examples, but state in the final report that
external library docs were not Context7-verified.

## Workflow

1. Create or update `output/<slug>/course-spec.json` first. If the request is
   contradictory or infeasible, stop before generating content.
2. Run the Context7 MCP docs check for the technologies that affect commands,
   code, dependencies, or version-sensitive behavior.
3. Launch the `content-writer` subagent against `course-spec.json` to generate
   Tutor LMS content: `tutor-lms/course-overview.md`, `tutor-lms/curriculum.md`,
   lessons, and quizzes.
4. Launch the `lab-engineer` subagent against `course-spec.json` to generate
   the practical lab under `student-lab/` and `instructor/`, plus root
   `validate.json`.
5. Generate course Elementor output through the `frontend-agent` skill:
   `elementor/landing-page.json` with `SOURCE.md` when tier 2 is used, or
   `elementor/REFERENCE_REQUIRED.md`.
6. Run `python scripts/run_checks.py output/<slug>`. Fix every failure and
   rerun until it passes.
7. Launch the `course-reviewer` subagent against the course directory; it
   writes `review-report.md` with a `PASS`/`FAIL` verdict.
8. Fix blocking review findings, rerun checks, and re-review until the verdict
   is `PASS` or a specific finding is explained as not applicable.
9. Run `python scripts/package_student_lab.py output/<slug>` only after checks
   and review pass.
10. Report files produced or changed, Context7 libraries/topics checked or the
   reason Context7 was unavailable, commands run with real results, final review
   verdict, package path, limitations, and manual integration steps.

## Gotchas

- The course directory name must match `course-spec.json`'s `slug`.
- `duration_minutes.lecture + duration_minutes.practical` must be greater than
  zero, and practical time must be at least 50 percent.
- `validate_lab_execution.py` tests the instructor solution, not the starter
  answer. Starter files are expected to fail until students complete them.
- Every instructor solution file must match a relative starter path under
  `student-lab/starter/`.
- Do not put solution code, answer keys, or instructor troubleshooting inside
  `student-lab/` or the student ZIP.
- If `landing-page.json` exists, run the Elementor JSON validator. If only
  `REFERENCE_REQUIRED.md` exists, do not run it.
- The Elementor tier-2 corpus is unverified. Tier-2 output needs `SOURCE.md`
  and a real Elementor editor check before it's trusted live — the
  `frontend-agent` subagent cannot do this itself (no browser/Novamira
  tools), but the orchestrating session usually can: create an unpublished
  draft page via `novamira/create-admin-access-link` + browser automation,
  import the generated JSON through Elementor's own Template Library, and
  check desktop/tablet/mobile rendering before calling the course finished.
  Structural validation (`validate_elementor_json.py`) cannot catch rendering
  problems like mobile text overflow — treat the real-editor check as
  load-bearing, not optional busywork. (An earlier version of this note cited
  a specific file and bug it supposedly caught; that file never existed in
  this repo's git history and the claim was fabricated — see
  `elementor/README.md`'s "Retracted" section. The underlying instruction to
  actually do a live-editor check still stands.)
- Context7 is for external technology documentation, not DataEngLab project
  rules. Local contracts in `CLAUDE.md`, the course output contract,
  validators, and skills win over generic external docs.
- Never claim validation or review passed unless it actually ran and passed.

## Validation Commands

Use the wrapper:

```bash
python scripts/run_checks.py output/<slug>
```

For focused debugging:

```bash
python scripts/validate_spec.py output/<slug>
python scripts/validate_course.py output/<slug>
python scripts/validate_content.py output/<slug>
python scripts/validate_lab.py output/<slug>/student-lab
python scripts/validate_lab_execution.py output/<slug>
python scripts/validate_elementor_json.py output/<slug>/elementor/landing-page.json
```

Package only after passing validation and review:

```bash
python scripts/package_student_lab.py output/<slug>
```
