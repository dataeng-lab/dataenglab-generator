# Elementor Patterns

Durable DataEngLab frontend facts for course landing-page work.

## Reference Tiers

- Course pages use `output/<slug>/elementor/landing-page.json`.
- Standalone lab pages use `output/<slug>/elementor/labs-page.json` via the `publish-practical-lab` workflow.
- As of 2026-09-14, no valid root `elementor-reference.json` is present. Check again every run because a real export would override tier 2.
- Tier 2 uses the checked-in `elementor/` corpus and must write `SOURCE.md` disclosing the corpus and its unverified-draft caveat.
- Tier 2 is explicitly unverified because it was not produced from a real Elementor export. Any tier-2 output needs a human Elementor or staging-site import check before being trusted live.

## Palette And Widgets

- For Elementor output, use the live theme tokens documented in `elementor/README.md`; they supersede the older blue palette.
- Live theme tokens include indigo `#5A4FE5`, coral `#FF5A36`, teal `#0E9C8B`, amber `#D98F1B`, ink `#14151A`, warm off-white `#FBFBF8`, white `#FFFFFF`,
  and border `#E7E3D9`.
- Leave per-widget typography unset when the corpus does; the live Elementor kit supplies fonts.
- Reusable native-widget patterns: inline `<span>` chips inside `text-editor`, Icon List for checklists, Accordion `tabs` for curriculum/FAQ, and native Heading/Button/Text Editor widgets inside Containers.
- A terminal/code panel built as a `text-editor` widget with inline-styled `<div>` elements is a reasonable pattern to validate fresh, but no verified reusable example currently exists in this repo.

## Known Limits

- `scripts/validate_elementor_json.py` checks JSON shape and bans HTML/shortcode widgets plus `<style>`/`<script>` in settings. It does not prove import or rendering in Elementor.
- `_tablet` and `_mobile` responsive keys follow common Elementor conventions but are not confirmed against this site's Elementor version until a real export or editor check proves them.
- Avoid generic AI-template composition: dark full-bleed hero photo, all-caps eyebrow pill, identical persona cards, generic icon rows, and mirrored dark CTA panels. Ground sections in real course/lab content, actual lab scenarios, real deliverables, and real validation signals.
- Earlier memory cited nonexistent `v1`/`v2`/`v3` welcome-page example files. Those files never existed in this repo. Keep the design guidance, but do not cite those examples.
