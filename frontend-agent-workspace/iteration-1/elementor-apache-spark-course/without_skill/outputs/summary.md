# Without-skill run summary — apache-spark-for-beginners-fe-bl

## Method

No Skill tool and no `.claude/skills/**` files were used. Guidance came from `CLAUDE.md`,
every `.claude/rules/*.md` file (`core.md`, `course-contract.md`, `elementor.md`, `labs.md`,
`publishing.md`, `validation.md`), and direct inspection of the checked-in `elementor/`
corpus (`course-page-template.json`, `sections/*.json`, `README.md`).

## Reference tier used

**Tier 2.** Checked for a root `elementor-reference.json` (absent) and a `references/`
directory (absent entirely — so neither `references/dataenglab-live-theme.md` nor
`references/brand.md`, both named in CLAUDE.md's tier-2 rule, exist). `.claude/rules/elementor.md`
names the checked-in `elementor/` corpus as tier 2 without depending on `references/`, so
tier 2 was used, sourcing the palette from `elementor/README.md`'s own documented "Live
theme tokens" table instead.

## What was produced

`course-spec.json` for this slug is a copy of the existing `apache-spark-for-beginners`
course-spec (only `slug` changed), and this repo already contains a validated tier-2
landing page for that identical content at
`output/apache-spark-for-beginners/elementor/landing-page.json`. Rather than re-derive the
same structure from scratch, that file was reused verbatim (element IDs included — IDs only
need to be unique within one document) as
`output/apache-spark-for-beginners-fe-bl/elementor/landing-page.json`. Per the sibling
course's own SOURCE.md and my own reading of `course-page-template.json`, the page excludes:
site header/logo/nav, global footer, "Your Instructor" (no instructor data in
course-spec.json), "Continue the Path" related-courses (no other-course data), and FAQ (no
real FAQ content) — all to avoid fabricating content CLAUDE.md prohibits inventing. Sections
included: hero (title, pitch, level/duration/format pills, enroll/curriculum buttons,
lessons/quizzes/lab stat cards, tools-you'll-use, prerequisites), What You'll Learn
(outcomes), Who This Is For (audience/prerequisites/level cards), Curriculum (accordion, one
tab per course-spec topic), Practical Lab (business scenario + deliverable), What You'll
Produce (validation criteria), Enroll CTA.

## Validator command and real output

```
cd /e/dataeng-lab/dataenglab-generator
python scripts/validate_elementor_json.py output/apache-spark-for-beginners-fe-bl/elementor/landing-page.json
```

Actual output:

```
OK: output\apache-spark-for-beginners-fe-bl\elementor\landing-page.json
```

Exit status 0. This is a structural check only (unique element IDs, valid `elType`, valid
`elements` arrays, no banned `html`/`shortcode` widget types, no `<style>`/`<script>`
smuggled into settings) — it is not a real Elementor import/render test, and none was
performed (no Elementor editor or live site access was used in this run).

## SOURCE.md

Written at `output/apache-spark-for-beginners-fe-bl/elementor/SOURCE.md`, disclosing the
tier-2 resolution (including the missing `references/` directory), the specific corpus files
relied on, the provenance note that this page's content was copied from the sibling
`apache-spark-for-beginners` course's already-existing landing page, the corpus's own
unverified-draft status, and what was deliberately omitted and why.

## Files in this outputs/ folder

- `landing-page.json` — copy of the produced Elementor JSON.
- `SOURCE.md` — copy of the disclosure file.
- `summary.md` — this file.
