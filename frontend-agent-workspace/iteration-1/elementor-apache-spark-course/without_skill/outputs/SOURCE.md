# Elementor source disclosure — Apache Spark for Beginners (fe-bl variant)

## Reference tier used

**Tier 2** (the checked-in `elementor/` template corpus), per `CLAUDE.md`'s "Elementor"
section and `.claude/rules/elementor.md`.

Root `elementor-reference.json` does not exist in this repository (checked at repo root),
so tier 1 is not available. `CLAUDE.md`'s tier-2 rule also names
`references/dataenglab-live-theme.md` as the palette source, but no `references/` directory
exists in this repository at all — the live-theme palette instead lives in
`elementor/README.md` ("Live theme tokens" section), which is part of the tier-2 corpus
itself. That is the palette actually used here (indigo `#5A4FE5`, teal `#0E9C8B`/`#E0F4F1`/
`#0B5A50` text-on-tint, ink `#14151A`, secondary text `#54575F`, backgrounds `#FBFBF8`/
`#FFFFFF`, border `#E7E3D9`), not the `references/brand.md` palette (which also does not
exist in this repo) and not the `#3D73FF`-family palette listed in CLAUDE.md's own "Brand"
section, since `.claude/rules/elementor.md` (the more specific, current rule for this path)
points only at the `elementor/` corpus and does not reference either `references/` file.

## Specific files used

- `elementor/course-page-template.json` — the reusable course landing-page template. Every
  container/widget type (`container`, `heading`, `text-editor`, `icon-list`, `accordion`,
  `button`) and every setting key used in this file (`content_width`, `flex_direction`,
  `flex_wrap`, `flex_gap`, `flex_justify_content`, `flex_align_items`, `padding`,
  `background_background`, `background_color`, `background_color_b`,
  `background_gradient_angle`, `border_border`, `border_color`, `border_width`,
  `border_radius`, `_column_size`, `custom_id`, `title`, `header_size`, `title_color`,
  `editor`, `text_color`, `icon_list`, `selected_icon`, `icon_color`, `link`/`url`/
  `is_external`/`nofollow`, `button_text_color`, `tabs`/`tab_title`/`tab_content`/
  `content_color`/`faq_schema`) traces 1:1 to patterns already present in that template —
  none were invented.
- `elementor/README.md` — confirmed the documented conventions this file relies on: inline
  `<span>` chip pills inside a Text Editor widget for badge/tag rows, the native Icon List
  widget for bulleted content, the native Accordion `tabs` repeater for the curriculum
  section, `_column_size` for proportional multi-column rows, `custom_id` for same-page
  anchors (`#curriculum`, `#enroll`), and the live theme token set / radius scale used for
  every color and border-radius value in this file.

## Provenance note specific to this run

This course (`apache-spark-for-beginners-fe-bl`) is a copy of `course-spec.json`,
`tutor-lms/course-overview.md`, `tutor-lms/curriculum.md`, and `student-lab/README.md` from
the existing `output/apache-spark-for-beginners/` course, with only the `slug` field changed.
Since the underlying course content (title, outcomes, curriculum, business scenario,
deliverable, validation criteria) is identical, this landing page reuses the structure and
copy of the already-existing, already-validated
`output/apache-spark-for-beginners/elementor/landing-page.json` verbatim (element IDs
included — IDs only need to be unique within a single document, which they are). No content
was invented beyond what that sibling file already contains, and that sibling file's own
copy was itself traced only to `course-spec.json` fields and the tier-2 corpus.

## Unverified-draft status (restated from the corpus's own caveat)

Per `elementor/README.md`, the entire corpus — including `course-page-template.json` — was
**not produced from a real Elementor export**. It was inferred from general knowledge of
Elementor's container/widget JSON schema and has never been opened in an actual Elementor
editor or confirmed to import without errors. This file has only been checked with
`scripts/validate_elementor_json.py`, a structural check (unique IDs, valid `elType`, valid
`elements` arrays) — not a real Elementor import/render test. No `_tablet`/`_mobile`
responsive override keys exist anywhere in the corpus, so this file likewise has none —
desktop/tablet/mobile support relies only on container flex/wrap behavior.

**Required before this is trusted live**: import `landing-page.json` into a staging
Elementor site (or a non-destructive draft on the real site) and confirm every container,
heading, text-editor, icon-list, accordion, and button widget renders and remains editable,
and that responsive behavior on tablet/mobile is acceptable.

## What was deliberately left out

Per `CLAUDE.md` and `.claude/rules/elementor.md`, this page excludes the site header, logo,
navigation, and global footer (all present in `course-page-template.json` but out of scope
for a course landing page). It also omits the template's "Your Instructor" and "Continue the
Path" (related courses) sections, because `course-spec.json` has no real instructor bio or
related-course data to populate them with, and fabricating that content is prohibited. The
FAQ section was omitted for the same reason — no real FAQ content exists in the generated
course files. All links point to `#` because no real enrollment or staging URL exists for
this course yet, per the "avoid fake statistics ... use `#` for unknown links" rule.
