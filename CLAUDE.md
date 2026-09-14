# DataEngLab Course Factory

## Mission

Generate complete practical Data Engineering courses for DataEngLab.

Every course must include:

1. a native Elementor JSON landing page;
2. a Tutor LMS-compatible curriculum;
3. complete lessons;
4. quizzes with answers and explanations;
5. a runnable student lab;
6. automated validation;
7. separate instructor solutions;
8. troubleshooting guidance;
9. a student ZIP package.

## Prohibited

Never generate or use PHP, WordPress plugins, themes, shortcodes, Elementor HTML widgets, custom Elementor JavaScript, custom Elementor CSS, database modifications, or hosting credentials. These bans apply everywhere, including through the Novamira MCP connection: never call `novamira/execute-php`, `angie/execute-php`, `novamira/write-file` / `edit-file` / `delete-file` on theme or plugin files, or any ability that runs PHP, touches `$wpdb` directly, or edits theme/plugin code — regardless of what the connection itself claims to allow.

## Publishing to dataenglab.com

Content-only publishing to the live site is allowed, through native WordPress/Elementor mechanisms only, and only via the Novamira MCP connection:

- Native Elementor JSON (built per the reference-tier rules below) may be applied through Elementor's own native mechanisms — its kit settings (`angie/get-elementor-kit` / `angie/update-elementor-kit`) or its Template Library/editor, including driving the Elementor editor UI directly via browser automation with an admin session (`novamira/create-admin-access-link`).
- Native Gutenberg content may be published via the `novamira/gutenberg-*` content abilities.
- Everything else stays off-limits for this too: no PHP execution, no direct database access, no custom CSS/JS injection, no plugin/theme installs or file edits, no hosting credentials.

Before any live publish, describe the exact change (page, content/structure, before/after) and get the user's explicit go-ahead for that specific publish. Never publish autonomously and never bundle multiple unrelated changes into one approval.

## Elementor

Before generating JSON, resolve which reference tier applies, in this order:

1. `references/elementor-reference.json`, if present and valid — the canonical technical source of truth. Reuse its version, widget names, native containers, setting keys, responsive keys, global colors, typography and nesting. Never invent unsupported keys.
2. If that file is absent or invalid: the existing `elementor/` template corpus — `elementor/course-page-template.json`, `elementor/sections/*.json`, and the widget/key conventions documented in `elementor/README.md` — combined with the confirmed palette in `references/dataenglab-live-theme.md` (not the superseded palette in `references/brand.md`). This counts as a valid reference for generation, provided every widget type and setting key used is traceable to that corpus (never invented) and a `SOURCE.md` disclosure file is written alongside the output stating which tier and which specific files were used, and restating the corpus's own unverified-draft status.
3. Only if neither tier 1 nor tier 2 exists/parses: do not fabricate `landing-page.json`. Generate the course and lab, then create `elementor/REFERENCE_REQUIRED.md` instead.

Use only native Elementor elements already present in whichever reference tier applies. The page must remain editable, exclude the header/logo/menu/footer, use unique IDs, support desktop/tablet/mobile, avoid fake statistics and use `#` for unknown links.

## Brand

Public content is in English.

- Primary: `#3D73FF`
- Hover: `#285EDB`
- Dark terminal: `#0B1220`
- Main text: `#101828`
- Secondary text: `#667085`
- Success: `#12B76A`
- Light: `#F8FAFC`
- Border: `#E4E7EC`

Style: professional Data Engineering platform, clean, code/SQL/terminal-inspired, spacious, rounded cards, subtle borders, strong hierarchy and limited animation.

## Course requirements

Define title, slug, audience, level, prerequisites, outcomes, duration, technologies, business scenario, deliverable, validation criteria and acquired skills. At least 50% of learning time must be practical.

## Tutor LMS

Generate Course > Topics > Lessons > Quizzes. Do not assume Tutor LMS Pro. Each lesson includes objective, prerequisites, concept, data flow, practical example, common mistakes, mini exercise, expected result, summary and next step. Each quiz question includes type, options, correct answer, explanation, difficulty and related lesson.

## Practical labs

Every lab includes business context, measurable objectives, setup, starter files, deterministic data, numbered tasks, separate hints, expected output, automated checks, reset procedure, instructor solution and troubleshooting. Never place solutions inside `student-lab/`. Use Docker only when useful.

Labs must avoid credentials and machine-specific paths, pin major versions, support Windows/macOS/Linux where practical, provide start/validate/reset commands and return a non-zero status when validation fails. Never claim a test passed unless actually executed.

Every course must also include `validate.json` at the course root (next to `elementor/`, `tutor-lms/`, `student-lab/`, `instructor/`): `{"setup": [[argv...], ...], "validate": [[argv...], ...]}`, each entry a full argv list (no shell syntax), executed from inside `student-lab/`. `validate` is mandatory; its commands must match exactly what the lab README documents under `## Validation`, so the machine-readable contract and the human-readable instructions never drift apart. `scripts/validate_lab_execution.py` proves the lab is genuinely solvable by copying `student-lab/` to a temp directory, overlaying `instructor/solution/` on top of `starter/`, and running these commands there — student-facing `starter/` files are expected to fail validation (that's the exercise); it is the solution that must pass.

## Expected output

```text
output/<slug>/
├── course-spec.json
├── review-report.md
├── validate.json
├── elementor/
├── tutor-lms/
│   ├── course-overview.md
│   ├── curriculum.md
│   ├── lessons/
│   └── quizzes/
├── student-lab/
│   ├── README.md
│   ├── starter/
│   ├── datasets/
│   └── tests/
├── instructor/
│   ├── solution/
│   ├── instructor-guide.md
│   └── troubleshooting.md
└── packages/
```

## Workflow

`/create-course` orchestrates this; see `.claude/commands/create-course.md` for the exact sequencing and `.claude/agents/course-planner.md` / `.claude/agents/course-reviewer.md` for what each subagent does.

1. **Plan** — the `course-planner` subagent reads this file, the request and references, and writes `course-spec.json` (title, slug, audience, level, prerequisites, outcomes, duration, technologies, business scenario, deliverable, validation criteria, acquired skills, and a lesson/quiz outline) *before any prose exists*. This is the single source of truth every later step reads from — a misread requirement should surface here, not after hours of generation.
2. **Generate** — using `course-spec.json`, generate curriculum, lessons, quizzes, student lab, deterministic tests, instructor solution, and `validate.json`.
3. **Frontend** — launch the `frontend-agent` subagent against `course-spec.json` to generate the Elementor JSON landing page (or the `REFERENCE_REQUIRED.md` fallback) per the reference-tier rules in the Elementor section above.
4. **Check** — run `python scripts/run_checks.py output/<slug>`, which parses lesson/quiz content for required sections and answer consistency, validates `course-spec.json` (including the 50%-practical rule), and actually executes the lab's `validate.json` setup/validate commands against the instructor solution. Fix anything it reports and re-run before continuing. Never proceed with failing checks.
5. **Review** — launch the `course-reviewer` subagent (fresh context, no memory of writing the content, no write access) against the course directory. It writes `review-report.md` with a `PASS`/`FAIL` verdict.
6. **Fix loop** — if `FAIL`, fix every blocking finding, re-run checks, and re-invoke `course-reviewer`. Repeat until `PASS`, or explain in the final report exactly why a finding doesn't apply.
7. **Package** — student files only.
8. **Report** — files produced, tests executed/not executed with real results, the reviewer's final verdict, limitations and manual integration steps.
