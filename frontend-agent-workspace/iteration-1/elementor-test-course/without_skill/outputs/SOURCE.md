# Elementor source disclosure (test-course-fe-bl)

## Reference tier used

**Tier 2** (checked-in `elementor/` corpus), per CLAUDE.md's Elementor section
and `.claude/rules/elementor.md`.

Tier 1 was checked first and is absent: there is no `elementor-reference.json`
at the repo root, and no `references/` directory at all (so
`references/dataenglab-live-theme.md` / `references/brand.md` do not exist
either). Tier 2 therefore applies.

## Specific files used

- `elementor/course-page-template.json` -- the placeholder-driven course
  landing page template. This file was the sole structural/content source:
  every container, widget type, and setting key in `landing-page.json` is
  copied verbatim from it (only placeholder tokens and a handful of list
  items were changed/trimmed; no new widget type or setting key was
  invented).
- `elementor/README.md` -- read for the corpus's own palette table and its
  "unverified draft" status (reproduced below), and for the placeholder
  token list used to fill the template.

`elementor/sections/*.json` was not needed: `course-page-template.json`
already contains a complete course-page section set (hero, outcomes,
audience, curriculum, lab, FAQ, enroll) as one file.

## Corpus's own unverified-draft status (restated here)

Per `elementor/README.md`: neither `course-page-template.json` nor the rest
of the corpus was produced from a real Elementor export. It was inferred
from general knowledge of Elementor's container/widget JSON schema and from
`docs/learning-path-improved.html`, and has **not** been opened in an actual
Elementor editor or confirmed to import without errors. Treat
`landing-page.json` the same way: a starting point, not a verified
deliverable. Import it into a staging Elementor site and check every widget
renders before trusting it.

## Palette note

CLAUDE.md's own "Brand" section lists a different palette (primary
`#3D73FF`, dark terminal `#0B1220`, etc.). CLAUDE.md's Elementor tier-2 rule
says to combine the corpus with "the confirmed palette in
`references/dataenglab-live-theme.md` (not the superseded palette in
`references/brand.md`)" -- but neither `references/` file exists in this
repo. In the absence of that file, this output uses the palette the
`elementor/` corpus itself already documents in its README ("Live theme
tokens" table, captured 2026-08-04 from the live homepage: indigo `#5A4FE5`
primary, ink `#14151A` text, `#FBFBF8`/`#FFFFFF` backgrounds, `#E7E3D9`
borders, teal/coral/amber accents), since every color value in
`landing-page.json` had to stay traceable to the tier-2 corpus per the
"never invent unsupported keys/values" rule, and that corpus was built
against its own documented palette, not the CLAUDE.md brand-section colors.
This discrepancy between CLAUDE.md's stated brand palette and the actual
tier-2 corpus's palette is flagged here rather than silently resolved either
way.

## Content adaptations made (and why)

`course-page-template.json` is a generic template with more placeholder
slots than `output/test-course-fe-bl/course-spec.json` has real data for.
Rather than inventing content to fill every slot, unfillable slots were
dropped:

- **Header (logo/nav) and global footer excluded entirely** -- required by
  CLAUDE.md/`elementor.md` ("exclude header, logo, navigation, and global
  footer").
- **"{{path_name}} Path" pill removed from the hero** -- course-spec.json has
  no learning-path field; inventing a path name/link would be an unsupported
  claim.
- **Prerequisites**: spec lists one prerequisite string. Split into three
  genuinely grounded bullets (the stated prerequisite, its "no pandas
  needed" clause, and the Python 3.11+ runtime requirement already in
  `spec.technologies`) instead of inventing two unrelated ones.
- **Tools row**: filled from `spec.technologies` (4 items); the template's
  5th tool-pill slot was dropped rather than inventing a 5th tool.
- **Outcomes**: spec has 5 outcomes; the template's unused 6th slot was
  dropped rather than inventing a 6th outcome.
- **"Who This Is For"**: spec has one audience description, not three
  personas. Kept one real audience card and dropped the other two
  placeholder persona cards (which would otherwise need fabricated
  audience segments).
- **Curriculum accordion**: spec's curriculum has exactly one topic/module
  (3 real lessons). The template's two extra placeholder modules
  (`module_2`, `module_3`) were dropped; kept the one real module and a
  "Practical Lab" tab built from `spec.deliverable`.
- **"Your Instructor" section dropped entirely** -- course-spec.json has no
  instructor name/bio, and CLAUDE.md bans fabricated content.
- **"Continue The Path" (related courses) section dropped entirely** --
  no real related-course data exists for this test course; inventing three
  other course titles/summaries would be fabricated content.
- **FAQ**: filled with three questions genuinely answerable from
  `course-spec.json` fields (`audience`, `deliverable`,
  `validation_criteria`) rather than invented Q&A.
- **Enroll section**: kept the "Enroll Now" -> `#` button; dropped the
  "Back to {{path_name}} Path" button (no real path/link to send it to).
- **`{{quizzes_count}}` set to 2`, not 1`**: `course-spec.json`'s curriculum
  array names only `quiz-01-validation-concepts.md`, but
  `tutor-lms/quizzes/` (copied alongside this spec) actually contains two
  quiz files (`quiz-01-validation-concepts.md` and
  `quiz-02-building-the-pipeline.md`). The on-disk count was used since it
  reflects what a student will actually see, rather than repeating the
  spec's partial list.
- All links to unknown/unverified destinations use `#` (e.g. "Start the
  Lab", "Enroll Now"). The one live URL kept ("Open full course catalog",
  `https://dataenglab.com/data-engineering-courses/`) is copied unchanged
  from the corpus template, where it was already used as a general site
  link (not course-specific).

## What was checked

- `python scripts/validate_elementor_json.py output/test-course-fe-bl/elementor/landing-page.json`
  was run and printed `OK: output\test-course-fe-bl\elementor\landing-page.json`
  (every element has a unique `id`, an `elType`, a valid `elements` array, no
  banned `html`/`shortcode` widget types, and no `<style>`/`<script>` markup
  in settings strings).
- **Not checked**: this file has not been opened in an actual Elementor
  editor. Import/rendering has not been verified, per the corpus's own
  standing caveat above.
