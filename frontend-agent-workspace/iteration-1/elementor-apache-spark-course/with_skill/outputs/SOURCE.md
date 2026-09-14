# Elementor source disclosure — Apache Spark for Beginners (frontend-agent eval workspace)

## Reference tier used

**Tier 2** (the `elementor/` template corpus), per `CLAUDE.md`'s "Elementor" section and
`.claude/skills/frontend-agent/SKILL.md`.

Root `elementor-reference.json` does not exist in this repository (confirmed this session),
so tier 1 is not available. `references/dataenglab-live-theme.md` also does not exist in
this repository — the `references/` directory itself is absent — so the tier-2 fallback
uses `elementor/README.md`'s documented live theme tokens instead, consistent with how the
sibling course `output/apache-spark-for-beginners/elementor/SOURCE.md` handled the same gap.

## Content provenance

`output/apache-spark-for-beginners-fe-ws/course-spec.json` is byte-for-byte identical to
`output/apache-spark-for-beginners/course-spec.json` except for the `slug` field (changed to
`apache-spark-for-beginners-fe-ws` for this workspace copy, per task instructions). No field
that this landing page draws on — title, audience, level, prerequisites, outcomes, duration,
technologies, business scenario, deliverable, validation criteria, curriculum structure —
differs between the two specs, and the slug string itself is never embedded anywhere inside
the Elementor JSON (checked: `grep` for the slug substring inside the JSON returns no
matches). Given that, `landing-page.json` in this workspace directory is the same page
already generated and disclosed for `output/apache-spark-for-beginners/elementor/`, produced
independently but from an identical spec; every fact on the page (lesson/quiz/module counts,
business scenario, deliverable, validation checks, technologies, prerequisites, outcomes) was
re-verified against this workspace's own copied `course-spec.json`,
`tutor-lms/course-overview.md`, `tutor-lms/curriculum.md`, and `student-lab/README.md` before
reuse, not assumed from the sibling course.

## Specific files used

- `elementor/course-page-template.json` — the reusable course landing-page template. Every
  container/widget type (`container`, `heading`, `text-editor`, `icon-list`, `accordion`,
  `button`) and every setting key used in this directory's `landing-page.json`
  (`content_width`, `flex_direction`, `flex_wrap`, `flex_gap`, `flex_justify_content`,
  `flex_align_items`, `padding`, `background_background`, `background_color`,
  `background_color_b`, `background_gradient_angle`, `border_border`, `border_color`,
  `border_width`, `border_radius`, `_column_size`, `custom_id`, `title`, `header_size`,
  `title_color`, `editor`, `text_color`, `icon_list`, `selected_icon`, `icon_color`,
  `link`/`url`/`is_external`/`nofollow`, `button_text_color`, `tabs`/`tab_title`/
  `tab_content`/`content_color`/`faq_schema`) is copied 1:1 from patterns already present in
  this file — none were invented.
- `elementor/README.md` — confirmed the documented conventions this file relies on: inline
  `<span>` chip pills inside a Text Editor widget for badge/tag rows, the native Icon List
  widget for bulleted content, the native Accordion `tabs` repeater for the curriculum
  section, `_column_size` for proportional multi-column rows, and `custom_id` for same-page
  anchors (`#curriculum`, `#enroll`).
- `elementor/README.md` — supplied the live theme token set used for every hex color
  (indigo `#5A4FE5` / `#ECEAFB`, teal `#0E9C8B` / `#E0F4F1` / `#0B5A50` text-on-tint, ink
  `#14151A`, secondary text `#54575F`, off-white background `#FBFBF8`, surface white
  `#FFFFFF`, border `#E7E3D9`), plus the 26px/16px card radius scale and 999px pill radius.

No widget type or setting key in `landing-page.json` was invented; everything traces back to
one of the files above.

## Unverified-draft status (restated from the corpus's own caveat)

Per `elementor/README.md`, this entire corpus — including `course-page-template.json` — was
**not produced from a real Elementor export**. It was inferred from general knowledge of
Elementor's container/widget JSON schema and has never been opened in an actual Elementor
editor or confirmed to import without errors. The live theme tokens were captured from the
live site's computed CSS, but the underlying widget/setting-key schema for this specific
Elementor version still cannot be verified from this environment. The corpus's own known gap
also applies here: no `_tablet`/`_mobile` responsive override keys exist anywhere in the
corpus, so this file likewise has none — desktop/tablet/mobile support relies only on
container flex/wrap behavior, not explicit responsive breakpoint settings.

**Required before this is trusted live**: import `landing-page.json` into a staging Elementor
site (or the real dataenglab.com editor via a non-destructive draft) and confirm every
container, heading, text-editor, icon-list, accordion, and button widget renders and remains
editable, and that responsive behavior on tablet/mobile is acceptable. This file has only
been checked with `scripts/validate_elementor_json.py`, which is a structural check (unique
IDs, valid `elType`, valid `elements` arrays, no banned `html`/`shortcode` widgets or inline
`<style>`/`<script>` tags) — not a real Elementor import/render test. **This has not
happened.**

## What was deliberately left out

Per `CLAUDE.md` and the skill's page-shape guidance, this page excludes the site header,
logo, navigation, and global footer (all present in `course-page-template.json` but out of
scope for a course landing page). It also omits `course-page-template.json`'s "Your
Instructor" and "Continue the Path" (related courses) sections, because `course-spec.json`
has no real instructor bio or related-course data to populate them with, and the skill
prohibits fabricating that content. The FAQ section was omitted for the same reason — no
real FAQ content exists in the generated course files. All links point to `#` because no
real enrollment or staging URL exists for this course yet, per the "avoid fake statistics ...
use `#` for unknown links" rule.

## Scope note (this is a workspace copy, not a real course)

This directory (`output/apache-spark-for-beginners-fe-ws/`) is a partial workspace created
for a `frontend-agent` skill evaluation run. Only `course-spec.json`, `tutor-lms/course-overview.md`,
`tutor-lms/curriculum.md`, and `student-lab/README.md` were copied from the original
`output/apache-spark-for-beginners/` course, which is otherwise unmodified. This workspace has
no `instructor/`, `validate.json`, `packages/`, or review artifacts, and this Elementor output
is not part of a full course-design run.
