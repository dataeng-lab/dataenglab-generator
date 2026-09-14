# Course Output Contract

Read this when creating or materially revising a complete DataEngLab course.
This document captures the required output shape and validation-sensitive
formats. Keep generated content specific to the user's course request.

## Output Tree

```text
output/<slug>/
|-- course-spec.json
|-- review-report.md
|-- validate.json
|-- elementor/
|   |-- landing-page.json        when a valid Elementor reference tier exists
|   |-- SOURCE.md                required when tier 2 is used
|   `-- REFERENCE_REQUIRED.md    when no valid reference tier exists
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
`-- packages/                   created by package_student_lab.py
```

## course-spec.json

Write this before lessons, quizzes, lab files, or Elementor output. The slug
must match the output directory name.

```json
{
  "title": "Course title",
  "slug": "course-slug",
  "audience": "Who this is for",
  "level": "beginner",
  "prerequisites": ["..."],
  "outcomes": ["..."],
  "technologies": ["..."],
  "business_scenario": "...",
  "deliverable": "...",
  "validation_criteria": ["..."],
  "acquired_skills": ["..."],
  "duration_minutes": {
    "lecture": 60,
    "practical": 90
  },
  "curriculum": [
    {
      "topic": "Topic title",
      "lessons": [
        {
          "id": "01-lesson-slug",
          "title": "Lesson title",
          "objective": "Observable learning objective",
          "minutes_lecture": 10,
          "minutes_practical": 15
        }
      ],
      "quiz": "quiz-01-topic-slug.md"
    }
  ]
}
```

Rules:

- Every field must contain real content derived from the request.
- `level` should be one of `beginner`, `intermediate`, or `advanced`.
- Practical time must be at least 50 percent of total time.
- Curriculum lesson IDs should be stable, ordered, lowercase, and filesystem
  safe.
- Quiz filenames in the spec must match files written under
  `tutor-lms/quizzes/`.

## Documentation Verification

Before writing version-sensitive technical content, use Context7 MCP when it is
available:

1. Resolve each relevant external technology to a Context7 library ID.
2. Fetch focused docs for the course topics that affect commands, imports,
   configuration, APIs, dependency versions, or lab behavior.
3. Apply those docs to lesson examples, lab starter code, tests, setup commands,
   and troubleshooting.

Examples of technologies that should trigger Context7: Airflow, dbt, Spark,
pandas, Polars, DuckDB, PostgreSQL, pytest, Docker Compose, Kafka, and cloud
SDKs.

Do not use Context7 as a substitute for local DataEngLab rules. `CLAUDE.md`,
this contract, validators, and existing project skills define the output
contract. If Context7 is unavailable in the session, record that limitation in
the final report.

## Tutor LMS Content

`tutor-lms/course-overview.md` should summarize:

- title, audience, level, prerequisites, duration, and technologies;
- business scenario;
- outcomes and acquired skills;
- deliverable and validation criteria;
- how the practical lab fits into the course.

`tutor-lms/curriculum.md` should mirror `course-spec.json`:

- topics in the same order;
- lesson IDs and titles;
- practical work per lesson;
- quiz filenames;
- final lab deliverable.

Do not introduce lesson topics, outcomes, tools, or claims that are absent from
the spec unless you also update the spec first.

## Lessons

Each lesson file under `tutor-lms/lessons/` must use this exact `##` heading
contract:

```markdown
# Lesson Title

## Learning objective
## Prerequisites
## Concept
## Architecture or data flow
## Practical example
## Common mistakes
## Mini exercise
## Expected result
## Summary
## Next step
```

Use practical examples and mini exercises that connect directly to the course
lab. Avoid generic prose that does not help the student complete the final
deliverable.

## Quizzes

Each quiz file under `tutor-lms/quizzes/` must follow this field structure for
each question:

```markdown
## Question 1
- Type: single choice
- Difficulty: beginner|intermediate|advanced
- Related lesson: 01-lesson-slug
- Question: ...
- Options:
  A. ...
  B. ...
  C. ...
- Correct answer: B
- Explanation: ...
```

Validation expects:

- at least two options;
- unique option letters;
- a correct answer letter that matches one option;
- non-empty type, difficulty, related lesson, question, correct answer, and
  explanation.

## Practical Lab

The course lab follows the same core rules as standalone labs:

- realistic business context;
- deterministic dataset with deliberate edge cases;
- incomplete starter files only under `student-lab/starter/`;
- automated tests under `student-lab/tests/`;
- instructor solution under `instructor/solution/`, matching starter relative
  paths;
- student README with setup, tasks, hints, expected output, validation, reset,
  and troubleshooting.

The root `validate.json` must contain argv arrays run from inside
`student-lab/`:

```json
{
  "setup": [["python", "build_db.py"]],
  "validate": [["python", "tests/test_solution.py"]]
}
```

The `validate` array is mandatory. Commands must match the README validation
section exactly.

## Elementor Output

Use `.claude/skills/frontend-agent/SKILL.md` for the actual Elementor workflow.
The course-design skill only requires the final outcome:

- `output/<slug>/elementor/landing-page.json` when generated;
- `output/<slug>/elementor/SOURCE.md` when tier 2 was used;
- or `output/<slug>/elementor/REFERENCE_REQUIRED.md` when no valid reference
  tier exists.

Never invent Elementor widget types or setting keys. Never add custom CSS,
custom JavaScript, PHP, shortcodes, header, navigation, or footer.

## review-report.md

Use this structure:

```markdown
# Review: <course title>

## Findings
- [severity: blocking|minor] path/to/file - finding and why it matters

## VERDICT: PASS
```

Use `FAIL` when any blocking finding remains. A `PASS` review still may list
minor findings.

## Packaging

Run:

```bash
python scripts/package_student_lab.py output/<slug>
```

The package should contain only `student-lab/` content. Instructor solution,
troubleshooting, Elementor files, and review material must stay out of the ZIP.
