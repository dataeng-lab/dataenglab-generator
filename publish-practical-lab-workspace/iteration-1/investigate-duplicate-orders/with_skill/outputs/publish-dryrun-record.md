# Publish run record — investigate-duplicate-orders (DRY RUN)

## Step 0 — confirm there's something to publish

`output/investigate-duplicate-orders/` exists and has `page-content.md`
(and a matching `lab-spec.md`, `student-lab/`, `instructor/`, `validate.json`).
`output/investigate-duplicate-orders/elementor/labs-page.json` did **not**
already exist before this run, so this is a **first publish**, not an
update — no before/after diff is needed, just a description of the new page.

`page-content.md` and `student-lab/README.md`/`lab-spec.md` were consistent
(same tasks, hints, expected output, troubleshooting entries), so no
divergence fix was needed before building the JSON.

## Step 1 — reference tier resolved: Tier 2

Checked `references/elementor-reference.json` — **absent** (confirmed fresh
via `ls references/`, which lists only `brand.md`, `dataenglab-live-theme.md`,
`README.md`). So tier 1 does not apply.

Tier 2 applies: the existing `elementor/` corpus —
`elementor/course-page-template.json` and `elementor/sections/07-faq.json` —
for widget types and setting keys, combined with the confirmed live palette
in `references/dataenglab-live-theme.md` (indigo `#5A4FE5` primary, coral
`#FF5A36`, teal `#0E9C8B`, amber `#D98F1B`, ink `#14151A`, warm off-white
`#FBFBF8`) rather than `references/brand.md`'s superseded blue palette.

This matches the skill's own note that "as of this writing, tier 1 doesn't
exist" — re-verified rather than assumed.

## Step 2 — Elementor JSON built

Written to `output/investigate-duplicate-orders/elementor/labs-page.json`
(copy included in this outputs folder). 31 elements total, all unique IDs
(verified programmatically). Structure, section by section:

1. Badges (Free / SQL / Beginner / 25 min / 5 Tasks) as inline-styled pill
   `<span>`s in one `text-editor`, tints varied per badge.
2. Lede: `heading` (h1, "Investigate Duplicate Orders") + `text-editor`
   paragraph (secondary text color).
3. Outcomes: `icon-list` widget, one entry per outcome from
   `page-content.md`, `fa-check` icon, teal icon color.
4. Environment: two side-by-side (`_column_size: 50`) `heading` +
   `text-editor` (HTML `<table>`) blocks for `orders` and `order_items`,
   field/type/description copied verbatim from `page-content.md`.
5. Tasks: `accordion` widget, one tab per task (5 tabs); Tasks 3 and 4's
   `Hint:` lines folded into their tab's content as `<em>` text, per the
   skill's mapping doc.
6. Expected output: plain `text-editor`, the 12-rows/$359.00 vs.
   17-rows/$490.00 numbers copied verbatim from `page-content.md` — no
   fabricated stats.
7. Troubleshooting: `accordion` widget, one tab per entry, tab titles
   copied verbatim (e.g. "Still 17 rows instead of 12"), same boxed
   container/background/border/radius pattern as
   `elementor/sections/07-faq.json`.
8. Back-to-labs / download CTA: two `button` widgets, both linking to `#`
   (no real labs-index or packaged-zip URL exists to link to — not invented).

No header/logo/nav/footer included. No per-widget typography set (inherits
the live Kit). No explicit `_tablet`/`_mobile` overrides — relies on native
container flex (`flex_direction`, `flex_wrap`), same restraint as the corpus.

`output/investigate-duplicate-orders/elementor/SOURCE.md` was written
disclosing tier 2, the exact source files, the palette source, and
restating `elementor/README.md`'s own unverified-draft caveat (never
produced from a real Elementor export; not confirmed to render in a live
Elementor instance).

## Step 3 — structural validation (real execution)

Command run:

```
cd E:/dataeng-lab/dataenglab-generator
python scripts/validate_elementor_json.py output/investigate-duplicate-orders/elementor/labs-page.json
```

Output:

```
OK: output\investigate-duplicate-orders\elementor\labs-page.json
```

Exit status: **0** (success). This confirms every element has a unique
`id` and an `elType`, and that every `elements` array is well-formed. It
does **not** confirm the page renders correctly in a real Elementor
editor — nothing in this repo can check that from here.

## Step 4 — the message I would show the user to get explicit go-ahead

This is the natural stopping point for this dry run. Below is exactly what
I would present to a real user before calling any live-publish mechanism —
no "yes" was simulated, and no Novamira/Angie ability was called.

---

> **Proposed publish: new lab page at `dataenglab.com/labs/investigate-duplicate-orders`**
>
> This is a **new** page (nothing currently published at this slug) built
> from `output/investigate-duplicate-orders/page-content.md`. It contains:
>
> - **Badges row** — Free · SQL · Beginner · 25 min · 5 Tasks
> - **Title + lede** — "Investigate Duplicate Orders": a revenue dashboard
>   double-counting sales because of a mismatched-grain join; the student's
>   job is to trace it and hand back a trustworthy query.
> - **What you'll learn** — 5 outcomes (finding true grain from data,
>   explaining fan-out from mismatched-grain joins, deterministic
>   `ROW_NUMBER()` dedup with NULL/tie handling, aggregate-before-join,
>   surfacing a NULL-driven data-quality flag instead of hiding it).
> - **Environment** — two side-by-side field tables for `orders` (grain:
>   1 row per status update) and `order_items` (grain: 1 row per line
>   item), copied verbatim from the lab's own schema documentation.
> - **Tasks** — a 5-tab accordion (Reproduce the Bug → Find the Grain
>   Problem → Deduplicate to One Row per Order → Fix the Join Instead of
>   the Symptom → Assemble and Verify), with the Task 3/4 hints folded in
>   as collapsed text inside each tab.
> - **Expected output** — 12 rows, $359.00 total revenue (vs. 17 rows /
>   $490.00 from the current buggy dashboard query) — numbers taken
>   directly from the lab spec, nothing invented.
> - **Troubleshooting** — a 3-tab accordion matching the lab's own
>   troubleshooting section verbatim ("lab.db not found", "Still 17 rows
>   instead of 12", "Revenue is close but not exact").
> - **Back to Labs** and **Download starter files** buttons, both pointed
>   at `#` for now since there's no live labs-index URL or hosted zip URL
>   to link to yet — I did not invent one.
>
> No header, logo, nav, or footer is included — this is page content only,
> meant to be inserted into an otherwise-empty page. No fabricated
> statistics were added anywhere on the page.
>
> The full JSON is at
> `output/investigate-duplicate-orders/elementor/labs-page.json` if you
> want to inspect it directly, and the sourcing is disclosed in
> `output/investigate-duplicate-orders/elementor/SOURCE.md`. One thing
> worth knowing before you say yes: the underlying widget corpus this was
> built from (`elementor/course-page-template.json`,
> `elementor/sections/07-faq.json`) is itself a **self-described
> unverified draft** — it was never produced from a real Elementor export
> and hasn't been confirmed to render correctly in the live editor. It's
> worth a look in the actual Elementor editor before calling this done,
> same caveat that applies to the course landing pages.
>
> **Do you want me to publish exactly this page to
> `dataenglab.com/labs/investigate-duplicate-orders` now?** (A plain "looks
> good" about the file isn't the same as a yes to publish — let me know
> explicitly either way.)

---

## Where this run stopped

Per the dry-run safety constraint, I stopped immediately after drafting the
message above. I did **not**:

- call `mcp-adapter-discover-abilities` / `mcp-adapter-get-ability-info` /
  `mcp-adapter-execute-ability`,
- call any `novamira/*` or `angie/*` ability (including
  `novamira/create-admin-access-link`, `angie/get-elementor-kit`,
  `angie/update-elementor-kit`),
- drive any browser automation toward a live save/publish action,
- simulate or fabricate a user "yes."

Step 5 (native publish via Novamira) and Step 6 (report back with a live
URL and a real look at the rendered page) were not attempted, and would
only be attempted after a real user gives explicit go-ahead to the exact
message above.
