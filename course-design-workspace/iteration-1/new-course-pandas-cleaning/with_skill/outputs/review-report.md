# Review: Pandas Data Cleaning Basics: Nulls and Duplicates

## Verification performed

- Read `CLAUDE.md` (root) in full, plus `.claude/rules/labs.md`,
  `.claude/rules/elementor.md`, and `.claude/rules/validation.md`.
- Read `course-spec.json` and every file under `tutor-lms/` (course-overview,
  curriculum, all 4 lessons, both quizzes), `student-lab/` (README, starter,
  datasets, tests, requirements.txt), `instructor/` (instructor-guide,
  troubleshooting, solution), `elementor/` (landing-page.json, SOURCE.md), and
  `packages/`.
- Ran `python scripts/run_checks.py output/pandas-data-cleaning-basics-eval-ws`
  myself just now. Result: `ALL CHECKS PASSED` — all 6 stages passed
  (`validate_spec`, `validate_course`, `validate_content`, `validate_lab`,
  `validate_lab_execution`, `validate_elementor_json`), including
  `validate_lab_execution.py` confirming the instructor solution passes the
  lab tests.
- Independently re-verified duration arithmetic by reading
  `course-spec.json`, `tutor-lms/curriculum.md`, `tutor-lms/course-overview.md`,
  `student-lab/README.md`, `instructor/instructor-guide.md`, and
  `elementor/landing-page.json` side by side and adding up the numbers myself
  rather than trusting any prior report:
  - `course-spec.json`: lecture = 10×4 = 40; `minutes_practical` per lesson =
    5×4 = 20 (mini-exercises only); `practical_breakdown_note` states
    20 (mini-exercises) + 30 (separate final lab) = 50; 40 + 50 = 90 total.
  - `curriculum.md`: restates the same split explicitly ("20 + 30 = 50
    practical minutes; 40 + 50 = 90 minutes total"), gives each topic's
    lecture/mini-exercise subtotal (20/10 per topic, ×2 = 40/20), and a
    "Total time reconciliation" section: 40 + 10 + 10 + 30 = 90. Matches.
  - `course-overview.md`: "90 minutes total - 40 minutes... and 50 minutes...
    20 minutes of short mini-exercises... plus a separate 30-minute final
    practical lab." Matches.
  - `student-lab/README.md`: "Estimated duration: 30 minutes... 20
    (mini-exercises) + 30 (this lab) = 50 practical minutes for the whole
    course." Matches — this is the fix for the previously-flagged
    self-contradiction (the README no longer claims the lab alone equals the
    full 50-minute practical budget).
  - `instructor-guide.md`: "Suggested delivery (90 minutes total)" lists
    10+5 per lesson ×4, then explicitly: the lab is "a SEPARATE, final
    30-minute block... not part of any lesson's own practical time... its 30
    minutes are not already included in the 20 minutes of lesson
    mini-exercises." Matches, and explicitly resolves the ambiguity flagged
    in the previous review round.
  - `elementor/landing-page.json`: hero badge reads "40 min lecture + 50 min
    practical"; the curriculum accordion lists each lesson as "10 min
    lecture, 5 min mini-exercise"; the practical-lab section heading reads
    "Clean a real newsletter subscriber export in pandas. (30-minute
    capstone lab)". All consistent with the above.
  - All six files now agree: 40 lecture + 20 mini-exercise + 30 lab = 90
    total, 50/90 ≈ 55.6% practical (meets the ≥50% practical rule). The
    double-counting defect from the prior review round is genuinely fixed
    everywhere checked, not just in the file previously cited.
- Re-read `student-lab/starter/clean_subscribers.py` side by side with
  `instructor/solution/clean_subscribers.py`. The starter's TODO comments
  (TODO 1, TODO 2, TODO 3/4) point to lesson numbers and describe the
  concept needed ("build a boolean mask," "fill only the columns listed...
  without touching any other column," "row order matters before you
  deduplicate") without naming the exact method (`notna`/`dropna`/`fillna`/
  `sort_values`/`drop_duplicates`) or exact argument/variable names used in
  the instructor solution. This is a genuine, still-intact fix of the
  answer-key defect found in the two prior review rounds.
- Unzipped `packages/pandas-data-cleaning-basics-eval-ws-student-lab.zip`
  and listed its contents: `datasets/subscribers.csv`, `README.md`,
  `requirements.txt`, `starter/clean_subscribers.py`,
  `tests/test_clean_subscribers.py`. No `instructor/`, no
  `troubleshooting.md`, no `course-spec.json`, no solution code — correct
  student/instructor separation.
- Read all 4 lessons and both quizzes in full (a genuinely fresh pass, not
  limited to previously-flagged files). Lesson "Practical example"/"Expected
  result" sections use a *different*, smaller illustrative dataset
  (`amina@example.com`/`boris`/`carla`/`dev`, dates in `2026-01-xx`, 4-5
  rows) than the lab's actual `datasets/subscribers.csv` (`alice`/`bob`/
  `carol`/.../`heidi`, dates in `2024-01-xx`, 13 rows) — this is not the
  literal-same-dataset defect confirmed blocking in this course family's
  earlier/sibling reviews.
- Checked the dataset for determinism and real edge cases: 13 fixed rows, 1
  missing email, an exact duplicate (`alice`), four same-email/different-date
  duplicates (`bob`, `carol`, `dave`, `grace`), and blank `name`/
  `referral_source` on rows that survive deduplication — matches the README
  and instructor-guide's description exactly, and matches what the tests
  assert.
- Grepped the whole course directory for credentials/machine-specific paths
  (`C:\Users`, `/home/`, `password`, `api_key`, `secret`, `AKIA`, private-key
  markers): no matches in any course content file (only a self-referential
  mention of "credentials" inside the previous `review-report.md`, which
  this report replaces).
- Confirmed `requirements.txt` pins major versions (`pandas>=2.0,<3.0`,
  `pytest>=7.0,<9.0`).
- Confirmed `validate.json`'s `setup`/`validate` argv lists
  (`["pip","install","-r","requirements.txt"]`, `["pytest","tests/","-q"]`)
  match `student-lab/README.md`'s `## Validation` section exactly.
- Confirmed `troubleshooting.md` is instructor-only (explicitly labeled as
  such, and absent from `student-lab/` and the shipped ZIP).
- Confirmed title/slug consistency: "Pandas Data Cleaning Basics: Nulls and
  Duplicates" / `pandas-data-cleaning-basics-eval-ws` matches across
  `course-spec.json`, `curriculum.md`, `landing-page.json`, and
  `student-lab/README.md`.
- Confirmed all content is English, and `elementor/landing-page.json` has no
  fabricated statistics/testimonials — all counts (4 lessons, 2 quizzes, 1
  lab, duration) trace to `course-spec.json`, and unresolved links use `#`.
- Confirmed `elementor/SOURCE.md` discloses tier 2 usage (no
  `elementor-reference.json` present anywhere in the repo), names the
  specific corpus files relied on, and every widget type/setting key in
  `landing-page.json` traces to that corpus; the unverified-draft caveat is
  restated.

## Findings

- [severity: minor] `tutor-lms/lessons/02-*.md`, `03-*.md`, `04-*.md` and
  `student-lab/README.md`'s Hints — the lesson "Practical example" sections
  teach the exact pandas one-liners the lab's TODOs need
  (`df.dropna(subset=["email"])`, `df.fillna({"name": "unknown",
  "referral_source": "unknown"})`, `df.sort_values("signup_date")` then
  `df.drop_duplicates(subset=["email"], keep="first")`) using the same
  column names as the lab (`email`, `name`, `referral_source`,
  `signup_date`, inherent to the shared business scenario), and the README's
  last Hint explicitly says: "Stuck on an exact method or argument name?
  Re-read the 'Practical example' section of the matching lesson (01-04) —
  each one walks through the same method on a similar small dataset." A
  student can transplant these lines into the starter's function bodies
  with near-zero adaptation and pass the tests. This is not the same defect
  already confirmed blocking twice in this course family (there the
  lesson's illustrative dataset was the literal same file/values as the
  lab's own dataset, or the README/starter text itself named the exact
  call) — here the illustrative dataset's rows/values genuinely differ, and
  the README/starter text itself stays conceptual. Because the pattern has
  recurred three times across this course family by relocating to a new
  file each time, this is flagged for visibility even though it does not
  meet the stricter bar (identical dataset, or literal exact-call text) that
  made the earlier findings blocking.
- [severity: minor] `elementor/landing-page.json` — uses the tier-2 corpus's
  own documented "live theme" palette (`#14151A`, `#54575F`, `#FBFBF8`,
  `#5A4FE5`, `#0E9C8B`, `#E7E3D9`, etc.) rather than the hex values literally
  listed in `CLAUDE.md`'s "Brand" section (`#3D73FF`, `#0B1220`, `#101828`,
  etc.). `elementor/SOURCE.md` discloses and justifies this explicitly:
  `references/dataenglab-live-theme.md` (named in `CLAUDE.md`'s prose) does
  not exist anywhere in the repo, so tier 2 falls back to
  `elementor/README.md`'s own documented, corpus-internal palette table —
  consistent with how the sibling courses `dedupe-late-arriving-orders` and
  `pandas-data-cleaning-basics-eval-bl` already resolved the identical
  situation. Flagged for visibility since the output does literally diverge
  from `CLAUDE.md`'s stated Brand hex values, though the divergence is fully
  disclosed and is a defensible reading of the tier-2 rule as written.
- [severity: minor] `instructor/solution/__pycache__/clean_subscribers.cpython-311.pyc`
  — a stray Python bytecode cache checked into the instructor solution
  directory. Confirmed it is not shipped to students (absent from the
  `packages/*.zip`), so this is cosmetic repo hygiene, not a
  student/instructor separation violation.

## Passing checks worth recording

- Duration/timing figures are now consistent and arithmetically honest
  across all six cross-checked files (see "Verification performed" above) —
  the double-counting defect from the immediately prior review round is
  fully fixed, not just relocated.
- The answer-key defect confirmed blocking in the two prior review rounds
  (`student-lab/README.md`'s Tasks/Hints, then `student-lab/starter/
  clean_subscribers.py`'s own TODO comments) remains genuinely fixed on this
  fresh re-read: neither file names an exact method, argument, or
  variable/dict name matching the instructor solution.
- `packages/pandas-data-cleaning-basics-eval-ws-student-lab.zip` exists and
  contains only student-facing files; no instructor solution, troubleshooting
  guide, or course-spec leaked into it.
- Lab dataset is deterministic, real, and matches its own documentation
  exactly (13 rows, specific named edge cases, expected output counts).
- `run_checks.py` passes all 6 stages, including a real execution of the
  instructor solution against the pytest suite via `validate_lab_execution.py`.
- No credentials, API keys, or machine-specific paths anywhere in the course
  content.
- All public/student content is English only.
- No fabricated statistics or testimonials.
- Quizzes include all required fields (type, options, correct answer,
  explanation, difficulty, related lesson) with technically accurate
  explanations.
- Lessons follow the required heading contract (objective, prerequisites,
  concept, data flow, practical example, common mistakes, mini exercise,
  expected result, summary, next step).

## VERDICT: PASS
