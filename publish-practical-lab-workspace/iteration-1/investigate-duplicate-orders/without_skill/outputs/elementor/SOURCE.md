# Source disclosure — investigate-duplicate-orders landing page

## Reference tier used

**Tier 2** (per `CLAUDE.md` → Elementor → reference-tier resolution order).

`references/elementor-reference.json` is absent from this repo, so tier 1 does not apply. Tier 2
was used instead: the existing `elementor/` template corpus, combined with the confirmed live
palette in `references/dataenglab-live-theme.md` (not the superseded palette in
`references/brand.md`, and not the near-identical palette restated in `CLAUDE.md`'s own top-level
"Brand" section, which the Elementor section explicitly says is superseded for this purpose).

## Specific files consulted

- `elementor/course-page-template.json` — source of every widget type and every setting key used
  below (container, heading, text-editor, icon-list, accordion, button), read in full to confirm
  exact key names, value shapes (e.g. `border_radius`/`padding`/`flex_gap` as `{unit, top, right,
  bottom, left, isLinked}` or `{unit, size}` objects), and nesting conventions (outer
  `isInner:false` boxed containers, inner `isInner:true` containers, `_column_size` for
  proportional multi-column rows).
- `elementor/README.md` — corpus-wide conventions: pills/badges as a single Text Editor widget
  containing inline-styled `<span>` chips (not a custom-CSS widget), bulleted lists mapped to the
  native Icon List widget, FAQ/curriculum-style disclosure mapped to the native Accordion widget's
  `tabs` repeater, `_column_size` preferred over CSS Grid container mode.
- `references/dataenglab-live-theme.md` — the color tokens actually used (`--ink #14151A`,
  `--ink-soft #54575F`, `--bg #FBFBF8`, `--surface #FFFFFF`, `--border #E7E3D9`, `--indigo #5A4FE5`
  / `--indigo-bg #ECEAFB`, `--teal #0E9C8B` / `--teal-bg #E0F4F1`, `--panel-dark #1B1940`) and the
  radius scale (16px / 26px cards, 999px pills).

Every `widgetType` (`heading`, `text-editor`, `icon-list`, `accordion`, `button`, `container`) and
every setting key (`title`, `header_size`, `title_color`, `editor`, `text_color`, `icon_list`,
`icon_color`, `tabs`, `tab_title`, `tab_content`, `faq_schema`, `link`, `border_radius`,
`background_color`, `button_text_color`, `border_color`, `_column_size`, `flex_direction`,
`flex_wrap`, `flex_gap`, `flex_justify_content`, `flex_align_items`, `padding`,
`background_background`, `border_border`, `border_width`) is copied from a real element in
`course-page-template.json` — none were invented for this page.

## Restating the corpus's own unverified-draft status

`elementor/README.md` states, and this file repeats: **neither `course-page-template.json` nor
any file under `elementor/sections/` was produced from a real Elementor export, and neither has
been opened in an actual Elementor editor or confirmed to import without errors.** The widget
names and setting-key shapes are inferred from general knowledge of Elementor's container/widget
JSON schema, not confirmed against dataenglab.com's actual installed Elementor version. This new
`landing-page.json` inherits that same unverified status one level further — it reuses the
corpus's conventions faithfully, but that does not make the conventions themselves confirmed.
**Import into a staging Elementor site and check every widget renders before trusting this file.**

## What this file is, structurally

A new page (`landing-page.json`), not a variant of the existing course-page template — the course
template's section order (hero → outcomes → audience → curriculum accordion → lab → instructor →
related → FAQ → enroll) is built for a full *course*, and this is a standalone *lab* page. The
corpus has no lab-page template to reuse wholesale, so this file is a new composition built
strictly from the corpus's demonstrated widget/setting vocabulary, structured around
`output/investigate-duplicate-orders/page-content.md` (the lab's already-written, approved copy):

1. Hero — price/topic/level pills, title, lede, duration/task-count pills, CTA buttons (`#` links).
2. Outcomes — Icon List of the 5 checklist items.
3. Environment — two bordered cards (`orders`, `order_items`), each with a plain semantic
   `<table>` of fields inside a Text Editor widget. Unlike the pill spans, this table carries no
   inline styling — it relies on the theme's own default table rendering, to stay unambiguously on
   the "rich content in a native widget" side of the CSS ban rather than approximate a "custom
   widget" with hand-styled markup.
4. Tasks — Accordion, one tab per numbered task (5), hints folded into the tab body as `<strong>
   Hint:</strong>` paragraphs, matching how `student-lab/README.md` presents them.
5. Expected output — a bordered callout card.
6. Troubleshooting — Accordion (`faq_schema: "yes"`, matching the corpus's own FAQ pattern), one
   tab per troubleshooting entry (3).
7. Closing CTA — dark panel band (`--panel-dark #1B1940`) with repeated Start/Download buttons.

Header, logo, primary menu and footer are intentionally excluded, per the Elementor section's
rules. All links are `#` (no real lab URL or download asset exists yet). No fake statistics are
used — the only numbers on the page (12 rows / $359.00 / 17 rows / $490.00, 25 min, 5 tasks) are
copied verbatim from `page-content.md` / `lab-spec.md`, not invented.

## Responsive behavior

No `elementor-reference.json` and no example in the tier-2 corpus demonstrates device-specific
keys (e.g. `_tablet`, `_mobile` suffixes), so none are invented here — inventing them would
violate the "never invent unsupported keys" rule just as much as inventing a widget type would.
Desktop/tablet/mobile support instead comes from the same mechanism the corpus itself relies on:
every multi-column row uses `flex_wrap: "wrap"` with percentage-driven `_column_size` columns, so
containers reflow to a single column on narrow viewports under Elementor's native container
breakpoints without any extra per-breakpoint settings. This should still be checked in the
Elementor editor's responsive preview before publishing, same as everything else in this file.

## Validation performed

`python scripts/validate_elementor_json.py output/investigate-duplicate-orders/elementor/landing-page.json`
→ `OK` (every element has a unique `id`, an `elType`, and a valid `elements` array; 45 elements
total, 0 duplicate IDs). This checks structural well-formedness only — it does **not** confirm the
file imports cleanly into the live Elementor editor, which is the real Elementor version check that
still has not happened (see above).

## What was NOT done, and why

No live-site write of any kind was made or attempted. Per `CLAUDE.md`'s Publishing section, native
Elementor JSON like this may only be *applied* to the live site through Elementor's own native
mechanisms (`angie/update-elementor-kit`, the Template Library, or driving the Elementor editor UI
via browser automation with an admin session) — and only after describing the exact change and
getting the user's explicit go-ahead for that specific publish. That description and request are
in this workspace's `summary.md`, not executed here.
