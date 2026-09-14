# Course Contract Rules

Every full course is generated under `output/<slug>/` and must include:

```text
output/<slug>/
|-- course-spec.json
|-- review-report.md
|-- validate.json
|-- elementor/
|   |-- landing-page.json      when a valid reference tier is used
|   |-- SOURCE.md              required for tier 2 Elementor output
|   `-- REFERENCE_REQUIRED.md  when no valid Elementor tier is available
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
`-- packages/                 created only by package_student_lab.py
```

- `course-spec.json` is written first and is the source of truth for title, slug, audience, level, prerequisites, outcomes, duration, technologies, business scenario, deliverable, validation criteria, acquired skills, and curriculum.
- Practical time must be at least 50 percent of total learning time.
- Tutor LMS content must include course overview, curriculum, lessons, and  quizzes. Do not assume Tutor LMS Pro.
- Lessons must satisfy the required heading contract enforced by `scripts/validate_content.py` and the course output contract.
- Quizzes must include type, difficulty, related lesson, question, options,correct answer, and explanation.
- Packages are final delivery artifacts. Create them only after validation and review pass, and include student files only.

