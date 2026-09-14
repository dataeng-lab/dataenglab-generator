# Elementor source disclosure — test-course-fe-ws

## Reference tier used

**Tier 2** (checked-in `elementor/` template corpus). No root-level
`elementor-reference.json` exists in this repository (checked fresh this
session — `ls elementor-reference.json` returns "No such file or directory"),
so tier 1 does not apply. Tier 2 files were confirmed present and valid JSON
this session:

- `elementor/course-page-template.json` (parses as valid JSON; primary
  structural reference for section layout, widget types, and setting keys)
- `elementor/sections/02-entry-points.json` through
  `elementor/sections/09-footer.json` (all parse as valid JSON; consulted for
  widget/key conventions, not copied verbatim into this page)
- `elementor/00-topbar-nav.json`, `elementor/01-hero-overview.json`,
  `elementor/learning-path-template.json` (all parse as valid JSON)
- `elementor/README.md` (read in full for the live theme token table, the
  pill/tag-chip pattern, the `_column_size` convention, the accordion/FAQ
  pattern, and the anchor/`custom_id` convention)

## Corpus's own unverified-draft status (restated here)

Per `elementor/README.md`: neither `course-page-template.json` nor the other
files in this corpus were produced from a real Elementor export of
dataenglab.com. They were inferred from general knowledge of Elementor's
container/widget JSON schema, not confirmed against this site's actual
Elementor version. `elementor/README.md` explicitly says: "Import ... into a
staging Elementor site and check every widget renders before trusting them."
That caveat applies unchanged to this course's `landing-page.json` — it
inherits the corpus's unverified status and has not been opened in a live
Elementor editor.

## What was built from the corpus vs. new for this course

- Container/widget nesting, `_column_size` column-width pattern, card
  background/border/radius values, pill/tag-chip inline-styled `<span>`
  pattern, and the `accordion` widget's `tabs` repeater are all reused
  directly from `elementor/course-page-template.json`.
- Colors are the live theme tokens from `elementor/README.md`'s token table
  (`#14151A` ink, `#54575F` ink-soft, `#FBFBF8` bg, `#FFFFFF` surface,
  `#E7E3D9` border, `#5A4FE5` indigo accent, `#0E9C8B`/`#0B5A50` teal
  accent-on-tint per the 2026-09-14 accessibility fix noted in that README).
- The header/topbar-nav block and the global footer block present in
  `course-page-template.json` were deliberately **excluded**, per CLAUDE.md's
  "exclude the header/logo/menu/footer" rule.
- The template's "Your Instructor" and "Continue The Path" (related courses)
  sections were deliberately **omitted**: this course-spec has no real
  instructor bio or real related-course data, and fabricating either would
  violate CLAUDE.md's ban on invented/unverifiable claims. No FAQ section was
  added for the same reason (no course-specific FAQ content exists in this
  course's generated files).
- All page copy (title, business scenario, deliverable, validation criteria,
  outcomes, prerequisites, audience, curriculum breakdown, technologies) is
  drawn directly from `output/test-course-fe-ws/course-spec.json` and
  `output/test-course-fe-ws/tutor-lms/curriculum.md`. No fabricated
  statistics, testimonials, or claims were added. Lesson/quiz/lab counts (3
  lessons, 2 quizzes, 1 lab) are real counts from the curriculum, not
  invented figures.
- All links point to `#` (unknown/enrollment URL) or same-page anchors
  (`#curriculum`, `#enroll`) already established as a corpus pattern.

## Responsive keys

This page does **not** use any `_tablet`/`_mobile`-suffixed setting keys.
Responsiveness relies solely on container `flex_wrap: wrap` behavior, the
same approach the corpus itself uses (per `elementor/README.md`'s "Known
gap, not fixed here" section, zero `_tablet`/`_mobile` keys exist anywhere in
this repo's Elementor corpus). No responsive-suffix keys were invented here
either.

## `faq_schema` setting on the curriculum accordion

The curriculum accordion in this page sets `"faq_schema": "no"`, unlike the
corpus's own curriculum accordion (which sets `"yes"`). This accordion is not
FAQ content, so `"no"` was chosen as the semantically correct value for the
same real, corpus-traceable `faq_schema` control — not an invented setting
key.

## Validation performed this session

```
python scripts/validate_elementor_json.py output/test-course-fe-ws/elementor/landing-page.json
```

See `frontend-agent-workspace/iteration-1/elementor-test-course/with_skill/outputs/summary.md`
for the exact command output.

## What was NOT verified

This file has not been imported into a live Elementor editor. Structural
JSON validation is necessary but not sufficient — it cannot catch import
errors, incorrect widget rendering, or mobile layout/overflow issues. Live
Elementor desktop/tablet/mobile verification still needs to happen before
this is trusted for a real publish, per CLAUDE.md's publishing rules.
