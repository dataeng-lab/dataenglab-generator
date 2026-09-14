# Elementor source disclosure - Pandas Data Cleaning Basics: Nulls and Duplicates

## Reference tier used

**Tier 2** (the checked-in `elementor/` template corpus), per `CLAUDE.md`'s
"Elementor" section and `.claude/rules/elementor.md`.

There is no root-level `elementor-reference.json` in this repository (confirmed
with `ls`/`find` before writing this file), so tier 1 is not available. Tier 2
was used instead.

## Specific files used

- `elementor/course-page-template.json` and the already-generated
  `output/apache-spark-for-beginners-eval-bl/elementor/landing-page.json` (an
  existing course output built from that same template) were used as the
  structural pattern for this file. Every container/widget type (`container`,
  `heading`, `text-editor`, `icon-list`, `accordion`, `button`) and every
  setting key used here (`content_width`, `flex_direction`, `flex_wrap`,
  `flex_gap`, `flex_justify_content`, `flex_align_items`, `padding`,
  `background_background`, `background_color`, `background_color_b`,
  `background_gradient_angle`, `border_border`, `border_color`,
  `border_width`, `border_radius`, `_column_size`, `custom_id`, `title`,
  `header_size`, `title_color`, `editor`, `text_color`, `icon_list`,
  `selected_icon`, `icon_color`, `link`/`url`/`is_external`/`nofollow`,
  `button_text_color`, `tabs`/`tab_title`/`tab_content`/`content_color`/
  `faq_schema`) is copied 1:1 from that existing pattern - none were invented
  for this file.
- `elementor/README.md` - confirmed the documented conventions this file
  relies on: inline `<span>` chip pills inside a Text Editor widget for
  badge/tag rows, the native Icon List widget for bulleted content, the
  native Accordion `tabs` repeater for the curriculum section, `_column_size`
  for proportional multi-column rows, and `custom_id` for same-page anchors
  (`#curriculum`, `#enroll`).
- `elementor/README.md` - supplied the live theme token set used for every
  hex color in this file (indigo `#5A4FE5` / `#ECEAFB`, teal `#0E9C8B` /
  `#E0F4F1` / `#0B5A50` text-on-tint, ink `#14151A`, secondary text `#54575F`,
  off-white background `#FBFBF8`, surface white `#FFFFFF`, border `#E7E3D9`),
  plus the 26px/16px card radius scale and 999px pill radius.

No widget type or setting key in `landing-page.json` was invented; everything
traces back to one of the files above.

## Palette note (read before assuming a conflict with CLAUDE.md)

`CLAUDE.md`'s "Brand" section lists a different palette (blue `#3D73FF`
primary, dark terminal `#0B1220`, etc.) and its "Elementor" section says tier
2 should combine the corpus with "the confirmed palette in
`references/dataenglab-live-theme.md` (not the superseded palette in
`references/brand.md`)". Neither `references/dataenglab-live-theme.md` nor
`references/brand.md` nor any `references/` directory exists anywhere in this
repository (checked with `ls references/` before writing this file - it does
not exist). `.claude/rules/elementor.md`, the more specific and apparently
more current rule file for this exact area, defines tier 2 without mentioning
either references file at all: corpus files + `elementor/README.md` only.
Given that neither cited references file exists, this file follows
`.claude/rules/elementor.md`'s literal tier-2 definition and reuses
`elementor/README.md`'s own documented "confirmed... from the live homepage"
palette (indigo/teal/ink/off-white), matching the precedent already set by
`output/apache-spark-for-beginners-eval-bl/elementor/SOURCE.md`, rather than
inventing colors from CLAUDE.md's Brand section that cannot be traced to any
file in the tier-2 corpus. This is a deliberate, disclosed judgment call, not
an oversight - flag it if a maintainer confirms `references/brand.md` should
take precedence instead.

## Unverified-draft status (restated from the corpus's own caveat)

Per `elementor/README.md`, this entire corpus - including
`course-page-template.json` - was **not produced from a real Elementor
export**. It was inferred from general knowledge of Elementor's
container/widget JSON schema and has never been opened in an actual Elementor
editor or confirmed to import without errors. The corpus's own known gap also
applies here: no `_tablet`/`_mobile` responsive override keys exist anywhere
in the corpus, so this file likewise has none - desktop/tablet/mobile support
relies only on container flex/wrap behavior, not explicit responsive
breakpoint settings.

**Required before this is trusted live**: import `landing-page.json` into a
staging Elementor site (or the real dataenglab.com editor via a
non-destructive draft) and confirm every container, heading, text-editor,
icon-list, accordion, and button widget renders and remains editable, and
that responsive behavior on tablet/mobile is acceptable. This file has only
been checked with `scripts/validate_elementor_json.py` (see **What was
checked** below), which is a structural check (unique IDs, valid `elType`,
valid `elements` arrays) - not a real Elementor import/render test. No
Elementor import or rendering has been verified in this session.

## What was checked, and what wasn't

- `python scripts/validate_elementor_json.py output/pandas-data-cleaning-basics-eval-bl/elementor/landing-page.json`
  was run for real in this session (see the course's generation report for
  the exact command output) and confirms every element has a unique `id`, a
  valid `elType`, and a valid `elements` array.
- This file has NOT been opened in a real Elementor editor. No import or
  render check has actually happened.
- All copy (headings, body text, list items, curriculum summaries) is written
  specifically for this course from `course-spec.json`; nothing is copied
  from an unrelated course.
- All links point to `#`, since no real enrollment or staging URL exists for
  this course, per "avoid fake statistics ... use `#` for unknown links."

## What was deliberately left out

Per `CLAUDE.md` and the tier-2 corpus's page-shape precedent, this page
excludes the site header, logo, navigation, and global footer (all present in
`course-page-template.json` but out of scope for a course landing page). It
also omits an "Instructor" bio section and a "Related courses" section,
because `course-spec.json` has no real instructor bio or related-course data
to populate them with, and fabricating that content is prohibited. No FAQ
section was added for the same reason - no real FAQ content exists in the
generated course files.
