# Elementor templates — UNVERIFIED drafts, read before importing

Two files here, generated at your explicit request:

- `learning-path-template.json` — the whole `docs/learning-path-improved.html` page (305 elements), rebuilt as native Elementor containers/widgets.
- `course-page-template.json` — a reusable, placeholder-driven course landing page template (142 elements), for any single DataEngLab course.

## Why these are marked unverified

Neither file was produced from a real Elementor export. There is no root-level `elementor-reference.json` in this repo, and I could not reach `https://dataenglab.com` from this environment (WebFetch got HTTP 403; `curl` failed with a TLS revocation-check error — this sandbox has no working path to the live internet). Everything here was inferred from:

- `docs/learning-path-improved.html` (the whole-page template's actual content and layout, read in full — 1439 lines).
- General knowledge of Elementor's container/widget JSON schema (widget names, `_column_size`, flex settings) — **not confirmed against this site's actual Elementor version.**
- For the course template specifically: no source page existed anywhere in this repo, so its structure (hero → outcomes → audience → curriculum accordion → lab → instructor → related courses → FAQ → enroll) was designed from scratch, informed by the `bundle-card` pattern already used in the learning-path page.

**Import both into a staging Elementor site and check every widget renders before trusting them.** Treat this the same as the earlier `test-course` Elementor draft: a starting point, not a verified deliverable.

## Deliberate design choices worth knowing about

- **Palette (updated 2026-08-04)**: every file here now uses the real, current dataenglab.com theme tokens, extracted directly from the live homepage's inline CSS custom properties (confirmed Elementor, `elementor-kit-652` / `elementor-page-35747`). Primary accent is indigo `#5A4FE5`, with coral `#FF5A36`, teal `#0E9C8B`, and amber `#D98F1B` as secondary accents; ink `#14151A` for text, warm off-white `#FBFBF8` / white `#FFFFFF` for backgrounds, `#E7E3D9` for borders. This replaces an earlier inferred palette (teal `#0F766E`, orange `#E85D2A`, blue `#1A73E8`) that was guessed from an HTML export no longer in this repo — every hex value was mechanically remapped 1:1, so structure/IDs/layout are untouched. Card radii were also normalized to the live site's real scale (16px / 26px); pill radius (999px) was already correct and unchanged.
- **Pill/tag chips** (`meta-pill`, `stack-pill`, `entry-tag`, `phase-tag` in the HTML): Elementor has no native "badge" widget. These are built as a single **Text Editor** widget per row, containing inline-styled `<span>` chips (a real, commonly-used Elementor pattern for tag rows — not a "custom CSS widget"). This keeps element count sane but means each pill row is one text block in the Elementor editor, not individually-selectable pill elements.
- **Bulleted lists** (`entry-list`, `track-list`, `bundle-list`, `timeline-outcomes`, `workflow-list`): mapped to the native **Icon List** widget.
- **FAQ / accordion sections** (site FAQ, and the course template's curriculum modules): mapped to the native **Accordion** widget's `tabs` repeater.
- **Column widths**: multi-column card rows use `_column_size` (a real, long-standing Elementor key for proportional widths — e.g. 33 for a 3-up row, 50 for 2-up) rather than the newer CSS Grid container mode, because `_column_size` is the better-documented, more stable mechanism and less likely to have drifted across Elementor versions.
- **Anchors**: sections that need a same-page jump target (`#curriculum`, `#enroll` in the course template) set `custom_id` on the container — confirm this is still the correct key in your Elementor version; older versions used `_element_id`.

## Live theme tokens

Captured from the live homepage on 2026-08-04 and used by the current
Elementor corpus:

| Role | Token | Value |
|---|---|---|
| Primary text | `--ink` | `#14151A` |
| Secondary text | `--ink-soft` | `#54575F` |
| Tertiary text | `--ink-faint` | `#92959E` |
| Page background | `--bg` | `#FBFBF8` |
| Surface | `--surface` | `#FFFFFF` |
| Subtle surface | `--surface-tint` | `#F3F1EA` |
| Border | `--border` | `#E7E3D9` |
| Primary accent | `--indigo` | `#5A4FE5` |
| Primary hover | `--indigo-dark` | `#372DBF` |
| Primary tint | `--indigo-bg` | `#ECEAFB` |
| Coral accent | `--coral` / `--coral-bg` | `#FF5A36` / `#FFEAE2` |
| Teal accent | `--teal` / `--teal-bg` / `--teal-ink` | `#0E9C8B` / `#E0F4F1` / `#0B5A50` |
| Amber accent | `--amber` / `--amber-bg` | `#D98F1B` / `#FBEED9` |

Radius scale: 10px small, 16px medium, 26px large, and 999px pills. Leave
per-widget typography unset when the corpus does; the live Elementor kit
supplies fonts.

## Course template placeholders

`course-page-template.json` is a **template**, meant to be duplicated per course. Every course-specific string is a `{{token}}` placeholder — find-and-replace (or drive via Elementor Theme Builder dynamic tags / ACF) before publishing. Full token list:

```text
{{path_name}} {{course_title}} {{course_one_line_pitch}} {{level}} {{duration}} {{format}}
{{lessons_count}} {{labs_count}} {{quizzes_count}}
{{tools_intro}} {{tool_1..5}} {{prerequisite_1..3}}
{{outcome_1..6}}
{{audience_1..3_tag}} {{audience_1..3_title}} {{audience_1..3_body}}
{{curriculum_intro}} {{module_1..3_title}} {{module_1..3_lesson_1..3}} {{module_4_lab_summary}}
{{lab_title}} {{lab_scenario}} {{lab_deliverable}}
{{instructor_name}} {{instructor_bio}}
{{related_1..3_tag}} {{related_1..3_title}} {{related_1..3_body}} {{related_1..3_meta}}
{{faq_1..3_question}} {{faq_1..3_answer}}
{{enroll_supporting_copy}}
```

## What was checked, and what wasn't

- Both files pass `dataenglab-generator/scripts/validate_elementor_json.py` — every element has a unique `id`, an `elType`, and a valid `elements` array.
- Neither file has been opened in an actual Elementor editor or confirmed to import without errors.
- The whole-page template's copy (headings, body text, list items, FAQ answers) is copied verbatim from `learning-path-improved.html` — not reworded or summarized.
- All external links reuse the exact URLs already present in `learning-path-improved.html`; the course template's links are placeholders (`#`) since it isn't a specific course yet.

## Accessibility fix (2026-09-14)

Every inline-styled pill/tag chip using the teal accent as **text-on-tint**
(`background:#E0F4F1` or `background:#FFFFFF` with `color:#0E9C8B`) failed
WCAG AA contrast for 13px bold text — measured ≈3.0:1 on the teal tint and
≈3.4:1 on white, both below the 4.5:1 threshold (13px bold doesn't qualify
for the relaxed 3:1 "large text" exception). Every occurrence (39 across
`learning-path-template.json`, `course-page-template.json`,
`01-hero-overview.json`, `sections/02-entry-points.json`,
`sections/04-paths.json`, `sections/05-courses.json`) was changed to
`color:#0B5A50`, the `--teal-ink` token in the live theme set, documented as
"text on teal tint" — now ≈8:1 on tint and ≈8.1:1 on
white. No coral/amber text-on-tint pills exist yet in this corpus (checked);
indigo text-on-tint (`#5A4FE5` on `#ECEAFB`) already passes at ≈4.8:1 and was
left unchanged. `icon_color`/decorative icon uses of `#0E9C8B` were left
unchanged (icons only need the 3:1 non-text contrast ratio, which they meet).
All edited files still pass `scripts/validate_elementor_json.py`.

**Known gap, not fixed here:** none of the files in this folder set any
`_tablet`/`_mobile` responsive overrides anywhere (checked — zero matches
repo-wide), so multi-column card rows (e.g. `05-courses.json`'s 3-up
`_column_size: 33` grid) don't have an explicit tablet/mobile breakpoint
behavior, only CSS wrap. Per this repo's own rule of never using a setting
key that isn't traceable to the reference tier, responsive-suffix keys
weren't invented to patch this — it needs either a real
`elementor-reference.json` export (to confirm the live site's actual
Elementor version's responsive key names) or an explicit decision to accept
well-known Elementor conventions without in-corpus precedent.

## Retracted: "welcome page" drafts (corrected 2026-09-14)

Earlier revisions of this file described nonexistent welcome-page Elementor
draft JSON files ("Draft v1", `-v2`, and `-v3` follow-ups), including a
narrated live-Elementor-editor verification session for v3 (a mobile
text-overflow fix, checked across desktop/tablet/mobile). **None of those files
have ever existed in this repository's git history.**
The verification narrative was fabricated and has been removed rather than
"marked unverified," because there is nothing on disk to verify.

Two things from that removed text are still real and worth keeping:

- The retired DataEngLab hero Elementor JSON did exist (added in the initial
  commit) and was a single Elementor **HTML widget** with an
  inline `<style>` block — a real, confirmed violation of CLAUDE.md's ban on
  Elementor HTML widgets and custom CSS. It has since been deleted from this
  repo entirely (not "left in place as a warning"); `login-register-elementor.json`
  was removed alongside it. Do not recreate anything shaped like either file.
- The generic-AI-template failure pattern the removed text used v1/v2 to
  illustrate (dark full-bleed hero photo, ALL-CAPS eyebrow pill, three
  identical persona cards, a generic icon-row, a second dark CTA panel
  mirroring the hero) is still worth checking new pages against — see the
  `frontend-agent` skill and `frontend-design` skill for that guidance on its
  own merits, without citing example files that don't exist.

If a future session actually builds and verifies a welcome-page draft, document
it here with a real file path that `git ls-files` or `find` can confirm, and
never describe a live-editor check that didn't actually happen in this
session.

## Regenerating

Both files were produced by a small generator script (kept only for this session, not committed here) that walks the HTML content and emits the container/widget tree. If you want section-level tweaks reflected consistently across both files (e.g. a palette fix, a different pill implementation), ask for a regenerate rather than hand-editing the JSON — hand edits will drift from the generator on the next pass.
