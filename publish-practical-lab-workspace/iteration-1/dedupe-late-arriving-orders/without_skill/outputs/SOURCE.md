# Source disclosure — dedupe-late-arriving-orders landing page

Per `CLAUDE.md`'s Elementor reference-tier resolution:

1. **Tier 1 checked first**: `references/elementor-reference.json` does not exist in this
   repo (confirmed via `ls`), so tier 1 does not apply.
2. **Tier 2 used**: the existing `elementor/` template corpus, combined with the confirmed
   live palette in `references/dataenglab-live-theme.md` (per CLAUDE.md, this supersedes
   the older palette in `references/brand.md`).

Specific files this landing page's widget types and setting keys were traced to:

- `elementor/course-page-template.json` — source of every widget/key convention reused
  here: `container` (flex_direction/flex_gap/padding/border_radius/background_color/
  `_column_size` shapes), `widget:heading` (`title`, `header_size`, `title_color`, `align`),
  `widget:text-editor` (`editor`, `text_color`), `widget:icon-list` (`icon_list` item shape
  with `text`/`selected_icon`/`_id`, `icon_color`, `text_color`), `widget:accordion`
  (`tabs` repeater with `tab_title`/`tab_content`/`_id`), `widget:button` (`text`, `link`,
  `border_radius`, `background_color`, `button_text_color`, `border_color`).
- `elementor/README.md` — documents that this same corpus is an **unverified draft**,
  never opened in a real Elementor editor or confirmed to import without errors, and that
  pill/badge chips are conventionally built as a single Text Editor widget with inline-styled
  `<span>` elements (no native Elementor "badge" widget) — the same pattern used for this
  page's badge row.
- `references/dataenglab-live-theme.md` — the color tokens used throughout (ink `#14151A`,
  ink-soft `#54575F`, bg `#FBFBF8`, surface `#FFFFFF`, surface-tint `#F3F1EA`,
  border `#E7E3D9`, indigo `#5A4FE5` / indigo-dark `#372DBF` / indigo-bg `#ECEAFB`,
  teal `#0E9C8B` / teal-bg `#E0F4F1`, amber `#D98F1B` / amber-bg `#FBEED9`) and radius
  scale (16px / 26px, 999px pills).

**Restating the corpus's own unverified-draft status** (from `elementor/README.md`):
neither `course-page-template.json` nor any file under `elementor/sections/` was produced
from a real Elementor export, was opened in an actual Elementor editor, or was confirmed to
import without errors. The widget names and setting keys are Elementor's documented schema
as of general knowledge, but have **not** been confirmed against dataenglab.com's actual
installed Elementor version. This new `landing-page.json` inherits that same unverified
status — it has only been checked with `scripts/validate_elementor_json.py` (unique ids,
valid `elType`/`elements` shape on every node — confirmed OK), never opened in a live or
staging Elementor editor.

## Content provenance

All page copy is taken verbatim (not reworded, not invented) from:
- `output/dedupe-late-arriving-orders/page-content.md` (badges, lede, outcomes checklist,
  environment table, task descriptions, expected output, troubleshooting)
- `output/dedupe-late-arriving-orders/lab-spec.md` (cross-checked, consistent)

No fabricated statistics were added. Both CTA button links use `#` (unknown/placeholder —
this lab has no live URL yet, so "Start the lab" cannot point anywhere real).

## What was intentionally excluded

Per CLAUDE.md: site header, logo, nav menu and footer are not part of this JSON — it is
meant to be inserted into a page/template slot on dataenglab.com that already carries the
site's global header/footer via Elementor Theme Builder, not to replace them.
