# Course Review Patterns

Durable, empirically observed facts for reviewing DataEngLab courses. These
come from actual review runs in this repo, not speculation.

## Recurring Blocking Findings

- Lesson/lab drift: lesson examples or mini exercises may reference function
  names, column names, or return shapes that do not match
  `student-lab/starter/*` and `instructor/solution/*`. Cross-check snippets
  against actual lab files, not just `course-spec.json`.
- Packaging timing: a first review may find `packages/` missing because the
  workflow packages after review. It is still a legitimate blocking finding
  until `package_student_lab.py` has produced the student ZIP.
- Restated contradictions: when a scenario claim appears in several files, a
  fix in one place may leave stale wording elsewhere. Grep for the corrected
  phrase across the full course output.
- Numeric drift: compare duration/timing claims in `course-spec.json`,
  `tutor-lms/curriculum.md`, and `student-lab/README.md`. Seen concretely:
  `curriculum.md` credits the lab's practical minutes inside a lesson's
  `minutes_practical` (e.g. "23 min practical, includes the practical lab"),
  while `student-lab/README.md`'s own header states a materially larger
  duration (e.g. "~45 min") for that same lab. `validate_spec.py` only
  checks that `duration_minutes` sums internally consistently within
  `course-spec.json` — it does not, and cannot, catch drift against the lab
  README's own stated duration. Always grep for "Duration"/"min" across
  `course-spec.json`, `curriculum.md`, `course-overview.md`,
  `instructor-guide.md`, and `student-lab/README.md` and compare the numbers.
- Task text as answer key: `run_checks.py`/`validate_lab.py` cannot detect
  that a lab's own numbered Task descriptions (not just the "Hints" section)
  spell out the exact one-line pandas/SQL call — arguments and all — needed
  to implement each TODO, word-for-word identical to
  `instructor/solution/*`. This is a real, repeated pattern in this repo —
  confirmed independently in both `pandas-data-cleaning-basics-eval-bl` and
  `pandas-data-cleaning-basics-eval-ws` (same course family, regenerated
  twice, same defect both times) — and is a blocking violation of
  CLAUDE.md's/`labs.md`'s "never place solutions inside `student-lab/`" even
  though it's dressed up as "guidance" rather than a labeled solution block.
  Read the Task list and Hints together and diff them mentally against
  `instructor/solution/` — if a hint or task sentence is character-for-
  character (or trivially paraphrased) the function body, it's a solution,
  not a hint. Treat this as a structural risk for any short,
  single-line-per-TODO pandas/SQL lab this repo generates, not a one-off.
- Packages-missing isn't always "too early to check": if any sibling course
  in `output/` already has a `packages/` dir at review time, a course
  lacking one is a real gap, not just "review ran before packaging" — flag
  it blocking per CLAUDE.md's required output tree.
- Matching numbers don't always resolve duration ambiguity: even when the
  lab README's stated duration literally equals `course-spec.json`'s
  practical-minutes total, check whether lesson-level mini-exercise time and
  the final lab's own claimed duration are implicitly being double-counted
  into that same total. If only an instructor-only doc (e.g.
  `instructor-guide.md`) resolves the ambiguity, that's still worth a minor
  finding since the student-facing README carries the same ambiguity
  unresolved.
- Fix-relocation, not fix: on re-review after a "spelled-out solution"
  finding, check every student-facing file that describes the same TODO, not
  just the one file the prior report cited. Seen concretely in
  `pandas-data-cleaning-basics-eval-bl`: a FAIL for `student-lab/README.md`
  naming the exact `df.dropna(subset=REQUIRED_COLUMNS)`-style call was
  "fixed" by rewriting the README's Tasks/Hints to be conceptual (genuinely
  improved), but the same method-name + argument + variable-to-pass recipe
  was left untouched in `student-lab/starter/<file>.py`'s own TODO
  docstrings — which ship in the student ZIP and are just as much
  "`student-lab/`" as the README is. `run_checks.py` cannot catch this; it
  doesn't diff prose/docstrings against `instructor/solution/`. Always
  re-check README task/hint text AND every starter file's own TODO/docstring
  text against the instructor solution on every re-review, not just whatever
  file the previous finding named.
- Fix-relocation round 2, into `tutor-lms/lessons/`: after
  `pandas-data-cleaning-basics-eval-bl`'s README and starter-file leaks were
  both genuinely fixed (conceptual hints, fill-in-the-blank skeletons), the
  identical literal one-liner solution for every lab task turned up a third
  time — inside the lesson content itself (`tutor-lms/lessons/02-*`,
  `03-*`, `04-*`). Each lesson's "Practical example"/"Expected result"
  ran the technique against the *literal same lab dataset* (same file path,
  same column names, same fill values, same dedup key) and produced the
  *exact* one-liners (`df.dropna(subset=[...])`, `df.fillna(value={...})`,
  `df.sort_values(...).drop_duplicates(subset=..., keep="last")`) and even
  the full, verbatim `clean_pipeline()` — while the lab README's own
  conceptual task text explicitly pointed students back to "Lesson 2"/
  "Lesson 3" for the missing method name, closing the loop back to the
  literal answer in one hop. This is NOT literally inside `student-lab/`,
  so it doesn't trip the letter of `labs.md`'s rule, but it defeats the
  same principle in substance and is just as blocking. Lesson "Practical
  example" / "Expected result" sections are a required heading (`CLAUDE.md`
  mandates them), so they will almost always exist — the check is whether
  the worked example's dataset/columns/values are identical to the lab's
  own, producing the literal graded one-liner, versus a comparably
  different illustrative example that still requires the student to adapt.
  On every review of a lesson-driven single-scenario lab course, diff
  lesson "Practical example"/"Expected result" code blocks against
  `instructor/solution/*` and against the lab's actual dataset file, not
  just the README/starter file — this defect has now moved through three
  different files across three review rounds in the same course family and
  should be assumed capable of relocating to lessons by default.
  CONFIRMED AGAIN in `pandas-data-cleaning-basics-eval-ws` on a later
  re-review: the README fix this time was genuinely good (conceptual, no
  exact calls, no instructor path names), and `packages/` was correctly
  added — but the starter file's `# TODO` comments (not docstrings this
  time, inline comments right above `raise NotImplementedError`) still
  spelled out every method name, argument, and even matching variable/dict
  names verbatim against `instructor/solution/`. Two regenerations of the
  same course family, two times the fix landed in the file that was
  explicitly named in the prior report and left the starter file untouched.
  Treat `student-lab/starter/*`'s own comments/docstrings as at least as
  likely a leak site as the README — check it first, not last, on every
  re-review of a "spelled-out solution" finding, and check it even when the
  README fix looks clean.

- Explicit-but-wrong duration resolution: don't stop at "the numbers match"
  or "the ambiguity is unresolved" — check whether a file actually resolves
  the mini-exercise-vs-lab double-counting question, and if so, verify that
  resolution against the lesson content itself. Confirmed in
  `pandas-data-cleaning-basics-eval-ws`: `student-lab/README.md` explicitly
  asserted "this lab IS the course's practical time budget, not an addition
  to it," which sounds like a deliberate, checked design decision — but
  `curriculum.md`'s own per-lesson table already allocates that identical
  practical-minutes total to the four lessons' own mini-exercises, and
  reading the lessons confirmed each mini-exercise runs on a distinct,
  smaller illustrative dataset, not the lab's dataset. So the explicit
  resolution was itself false: real hands-on time was roughly double the
  claimed total. `validate_spec.py` only checks the top-level
  lecture/practical ratio inside `course-spec.json`; it never sums
  per-lesson `minutes_practical` against the top-level total and has no
  visibility into the lab README's separately-stated duration. Treat any
  lesson-vs-lab duration reconciliation claim as a claim to verify, not
  evidence the drift was actually checked.
- Fix-relocation round 4, back into the SAME file's own unscrutinized
  section: after `pandas-data-cleaning-basics-eval-bl`'s README Tasks/Hints
  (round 1), starter-file docstrings (round 2), and lesson content (round 3)
  were each genuinely fixed in turn, the identical leak pattern reappeared a
  fourth time — inside `student-lab/README.md`'s own **Troubleshooting**
  section, a part of the *same file* that had already been "fixed" and
  presumably re-checked in round 2, but whose Troubleshooting subsection
  specifically had never been diffed against `instructor/solution/` before.
  The Hints for Tasks 3/4 correctly blanked out the method names
  (`df.____(value=____)`, `sorted_df.____(subset=____, keep=____)`), but the
  Troubleshooting bullets two sections below spelled out the literal
  answers in plain prose: "applied `drop_duplicates()` without
  `subset=DEDUPLICATION_KEY`" and "`OPTIONAL_FILL_VALUES` was not passed to
  `fillna()`" — exact method + argument + variable names copied from
  `instructor/solution/`, undoing the Hints' own blanking two sections
  earlier in the identical file. Lesson: a "fixed" file is not clean end to
  end just because the specific subsection named in the prior finding
  (Tasks/Hints, or a docstring) is now clean — grep the *entire* file,
  including Troubleshooting/FAQ/Common-mistakes-style sections, for the
  instructor solution's literal method names, argument names, and constant
  names every time, not just the subsection type that leaked last round.
  This defect has now demonstrably relocated through four different
  locations across four review rounds in one course family (README
  Tasks/Hints → starter docstrings → lesson practical examples → README
  Troubleshooting) — treat any remaining student-facing prose section in a
  short pandas/SQL-per-TODO lab as a candidate leak site by default, not
  just the sections a past finding happened to name.
- When re-verifying "starter fails / solution passes" claims and the repo's
  own `.venv` lacks the lab's dependencies (e.g. no pandas) with no network
  access to install them, check for another interpreter on the system
  (`py -3.11`, global `python`, etc.) with the needed packages before giving
  up on independent verification — one was available in this repo's
  environment and let the pytest re-run happen for real instead of only
  trusting `run_checks.py`'s own report.

- Duration double-count, confirmed fixed via an explicit breakdown note:
  `pandas-data-cleaning-basics-eval-ws`'s prior FAIL (lesson mini-exercises
  and the final lab both separately claiming the full practical-minutes
  total) was resolved by (a) lowering each lesson's `minutes_practical` in
  `course-spec.json` to cover ONLY that lesson's own mini-exercise, (b)
  adding a `practical_breakdown_note` field spelling out
  mini-exercise-total + lab-total = practical-total arithmetic, and (c)
  propagating the identical breakdown sentence to `curriculum.md`,
  `course-overview.md`, `student-lab/README.md`, `instructor-guide.md`, and
  the Elementor landing page. On re-review this was independently verified
  by doing the addition myself across all six files rather than trusting
  the fix description — it held. This is the correct fix shape for this
  defect: don't just resolve the ambiguity in prose, change the underlying
  numbers so the two budgets are structurally additive, then restate the
  same reconciliation sentence everywhere duration is mentioned.
- Lesson-teaches-the-lab's-exact-one-liner is a spectrum, not a binary leak:
  on `pandas-data-cleaning-basics-eval-ws`'s 4th review round, lessons'
  "Practical example" sections taught the literal pandas calls the lab's
  TODOs needed (same column names, since it's one continuous business
  scenario) and the README's Hints explicitly pointed back to "the matching
  lesson" for "an exact method or argument name." This looks like the
  pattern confirmed blocking three times before in this same course family
  — but the deciding factor that kept it MINOR here, not blocking, was that
  the lesson's illustrative dataset used different rows/values/row-counts
  than the lab's own dataset (unlike the earlier blocking instances, where
  the lesson's example was the literal same file/values as the lab, or the
  README/starter text itself named the exact call/argument). Judgment rule
  going forward: flag blocking only when (1) the lesson's worked example
  uses the lab's own dataset/values verbatim (so the worked output IS the
  lab's answer), or (2) student-facing task/hint/TODO text itself names the
  exact method+argument+variable matching the instructor solution. Flag
  minor (not blocking) when only the technique/column-name overlap is
  identical but the illustrative data differs and the student-facing text
  stays conceptual — that overlap is largely unavoidable in any
  single-scenario course whose lessons are required to build toward the
  lab, and CLAUDE.md's lesson-contract and "lab is an integration exercise"
  design intent (seen explicitly stated in this course's own
  `course-overview.md`) actively wants this teach-then-apply structure.

- Fix-relocation chain resolved after 5 rounds, confirmed by re-reading every
  file fresh: `pandas-data-cleaning-basics-eval-bl`'s literal-solution leak
  relocated four times (README Tasks/Hints -> starter docstrings -> lesson
  practical examples -> README Troubleshooting) across rounds 1-4, and the
  round-5 fix (rewriting Troubleshooting bullets to name only a Task number
  and a "re-read the Hint" pointer, dropping the literal method+argument
  combination) held up under a full independent re-sweep of every
  student-facing file. Lesson: once a fix genuinely removes the literal
  method+argument+variable combination from a section, it can actually be
  done - this defect is not infinitely relocatable if each fix is real
  (conceptual language, blanked hints) rather than cosmetic. Don't assume a
  5th-round re-review will automatically find a new relocation; verify fresh
  each time, but a clean result is possible.
- New minor-severity variant spotted on this same review: quizzes (not
  lessons/README/starter) reusing the lab's own real column names and a real
  constant's exact value (e.g. a quiz explanation showing
  `df.fillna(value={"region": "Unknown"})`, which is exactly
  `OPTIONAL_FILL_VALUES["region"]`, and `df.duplicated(subset=["customer_email",
  "survey_date"])`, exactly `DEDUPLICATION_KEY`) instead of the lesson's own
  illustrative scenario. Judged non-blocking here specifically because (a)
  those constants are already openly disclosed, unhidden, at the top of
  `student-lab/starter/*.py` - so quoting their values isn't disclosing a
  secret, and (b) no quiz spelled out the *complete* one-line call that
  solves a Task (no matching `subset=`/`keep=`/`value=` combination glued to
  the real function name in one line) or reproduced the lab's actual graded
  row counts/IDs. Treat quizzes as a candidate leak-relocation site too, not
  just README/starter/lessons - grep quiz Explanations for the lab's real
  constant names and constant values, not only its function names.

## Process Habits

- Rerun `python scripts/run_checks.py output/<slug>` for every review and
  re-review; never rely on another agent's report.
- A `PASS` can include minor findings. Any unresolved blocking finding means
  `FAIL`.
- On re-review, verify that fixes were applied everywhere the issue appeared,
  not just at the originally cited location.
