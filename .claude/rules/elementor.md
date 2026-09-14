---
paths:
  - "elementor/**"
  - "output/**/elementor/**"
  - ".claude/skills/frontend-agent/**"
  - ".claude/skills/publish-practical-lab/**"
  - ".claude/agents/frontend-agent.md"
---

# Elementor Rules

Resolve the Elementor reference tier before writing JSON:

1. If root `elementor-reference.json` exists and parses as JSON, it is the canonical technical source. Reuse its Elementor version, widget names, containers, setting keys, responsive keys, global colors, typography, and nesting.
2. Otherwise use the checked-in `elementor/` corpus: 
   `elementor/course-page-template.json`, `elementor/sections/*.json`, and  `elementor/README.md`. Every widget type and setting key must be traceable to that corpus. Tier 2 output must include `elementor/SOURCE.md` explaining the corpus and its unverified-draft status.
3. If neither tier is available or valid, do not fabricate Elementor JSON. Write `elementor/REFERENCE_REQUIRED.md` instead.

Elementor output must:

- use native Elementor containers/widgets only;
- remain editable in Elementor;
- exclude header, logo, navigation, and global footer;
- use unique element IDs;
- use `#` for unknown links;
- avoid fake statistics, testimonials, and unsupported claims;
- avoid `html` and `shortcode` widgets;
- avoid `<style>` and `<script>` inside settings.

Simple inline HTML inside a native Text Editor widget is allowed only when it is traceable to an established corpus or skill contract pattern.

