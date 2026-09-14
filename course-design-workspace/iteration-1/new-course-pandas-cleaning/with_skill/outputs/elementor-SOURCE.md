# Elementor source disclosure - Pandas Data Cleaning Basics: Nulls and Duplicates

## Reference tier used

**Tier 2** (the checked-in `elementor/` template corpus), per `CLAUDE.md`'s
"Elementor" section, `.claude/rules/elementor.md`, and the
`.claude/skills/frontend-agent/SKILL.md` workflow.

There is no root-level `elementor-reference.json` anywhere in this repository
(confirmed before writing this file: no such file at the repo root, and no
`references/` directory exists at all, so the `references/dataenglab-live-theme.md`
and `references/brand.md` files named in `CLAUDE.md`'s prose do not exist
either). Tier 1 is therefore unavailable and tier 2 was used instead, matching
how `output/dedupe-late-arriving-orders/elementor/SOURCE.md` and
`output/pandas-data-cleaning-basics-eval-bl/elementor/SOURCE.md` already
resolved this exact situation for other courses in this repo.

## Specific corpus files used

- `elementor/course-page-template.json` — source of the overall page shape
  (hero → tools → outcomes → audience → curriculum accordion → practical lab
  → what-you-produce → enroll CTA) and of every container/widget type used
  here: `container`, `heading`, `text-editor`, `icon-list`, `accordion`,
  `button`.
- `output/pandas-data-cleaning-basics-eval-bl/elementor/landing-page.json` —
  an already-generated course page built from the same corpus, used as the
  structural precedent for setting-key usage. Every setting key in this file
  (`content_width`, `flex_direction`, `flex_wrap`, `flex_gap`,
  `flex_justify_content`, `flex_align_items`, `padding`,
  `background_background`, `background_color`, `background_color_b`,
  `background_gradient_angle`, `border_border`, `border_color`,
  `border_width`, `border_radius`, `_column_size`, `custom_id`, `title`,
  `header_size`, `title_color`, `editor`, `text_color`, `icon_list`,
  `selected_icon`, `icon_color`, `link`/`url`/`is_external`/`nofollow`,
  `button_text_color`, `tabs`/`tab_title`/`tab_content`/`content_color`/
  `faq_schema`) is reused 1:1 from that precedent — none were invented for
  this file. All copy (headings, body text, list items, curriculum labels,
  business scenario, deliverable, validation criteria) was written fresh for
  this specific course from `course-spec.json`, `tutor-lms/course-overview.md`,
  and `student-lab/README.md` — none of it is copied from the unrelated
  "customer feedback" scenario in the `eval-bl` sibling file.
- `elementor/README.md` — source of the documented native-widget conventions
  relied on here: inline `<span>` chip pills inside a Text Editor widget for
  badge/tag rows, the native Icon List widget for bulleted content, the
  native Accordion `tabs` repeater for the curriculum section, `_column_size`
  for proportional multi-column rows, and `custom_id` for same-page anchors
  (`#curriculum`, `#enroll`).

No widget type or setting key in `landing-page.json` was invented; every one
traces back to one of the files above.

## Palette tokens used (from `elementor/README.md`'s "Live theme tokens" table)

- Ink (primary text): `#14151A`
- Secondary text: `#54575F`
- Page background / warm off-white: `#FBFBF8`
- Surface (card background): `#FFFFFF`
- Border: `#E7E3D9`
- Primary accent (indigo): `#5A4FE5`, tint `#ECEAFB`
- Teal accent: `#0E9C8B`, tint `#E0F4F1`, text-on-tint `#0B5A50`
- Radius scale: 26px large (cards/sections), 999px pills

`CLAUDE.md`'s "Brand" section lists a different palette (blue `#3D73FF`
primary, dark terminal `#0B1220`, etc.), and its "Elementor" section points
tier 2 at "the confirmed palette in `references/dataenglab-live-theme.md`"
— but that file does not exist anywhere in this repo (checked). Per the more
specific, currently-loaded `.claude/rules/elementor.md`, tier 2 is defined
using the corpus files plus `elementor/README.md` only, with no reference to
a `references/` directory. This file therefore reuses `elementor/README.md`'s
own documented "confirmed... from the live homepage" palette, matching the
precedent already set by `output/pandas-data-cleaning-basics-eval-bl/elementor/SOURCE.md`
and `output/dedupe-late-arriving-orders/elementor/SOURCE.md`. This is a
deliberate, disclosed judgment call, not an oversight.

## Unverified-draft status (restated from the corpus's own caveat)

Per `elementor/README.md`, this entire corpus — including
`course-page-template.json` — was **not produced from a real Elementor
export**. It was inferred from general knowledge of Elementor's
container/widget JSON schema and has never been opened in an actual Elementor
editor or confirmed to import without errors. The corpus's own known gap
also applies here: no `_tablet`/`_mobile` responsive override keys exist
anywhere in the corpus, and none were added to this file either — desktop,
tablet, and mobile support relies only on container flex-wrap behavior, not
explicit responsive breakpoint settings.

**Required before this is trusted live**: import `landing-page.json` into a
staging Elementor site (or a non-destructive draft on the real
dataenglab.com editor) and confirm every container, heading, text-editor,
icon-list, accordion, and button widget renders and remains editable, and
that the layout is acceptable on desktop, tablet, and mobile. **This has not
happened.** No live Elementor editor or browser tool is available to this
subagent in this session — the only check performed is the structural
validator below.

## What was checked, and what wasn't

- `python scripts/validate_elementor_json.py output/pandas-data-cleaning-basics-eval-ws/elementor/landing-page.json`
  was run for real in this session — see the frontend-agent's final report
  for the exact command output. It confirms every element has a unique
  `id`, a valid `elType`, a valid `elements` array, and that no banned
  `html`/`shortcode` widget or `<style>`/`<script>` tag exists anywhere in
  settings. This is a structural check only — it does not prove the file
  imports or renders correctly in a real Elementor editor.
- This file has NOT been opened in a real Elementor editor. No import or
  render check has actually happened this session or any prior session.
- All links point to `#`, since no real enrollment or staging URL exists for
  this course, per CLAUDE.md's "use `#` for unknown links" rule.
- No fake statistics, testimonials, or invented employment/outcome claims
  were added. Lesson counts (4), quiz counts (2), lab count (1), and
  duration (40 min lecture + 50 min practical = 90 min total) are taken
  directly from `course-spec.json`.

## What was deliberately left out

Per `CLAUDE.md` and the tier-2 corpus's page-shape precedent, this page
excludes the site header, logo, navigation, and global footer (all present
in `course-page-template.json` but out of scope for a single course landing
page). It also omits an "Instructor" bio section, a "Related courses"
section, and an FAQ section, because none of the generated course files
(`course-spec.json`, `tutor-lms/course-overview.md`,
`student-lab/README.md`) contain real instructor-bio, related-course, or FAQ
content to populate them with, and fabricating that content is prohibited.
