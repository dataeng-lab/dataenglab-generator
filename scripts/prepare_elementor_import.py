"""Validate a DataEngLab-generated Elementor template and print manual import steps.

This is intentionally read-only: no network calls, no site credentials, no
WordPress plugin. Elementor's own "Import Templates" feature in wp-admin is
the only thing that ever writes the template into a site's database - this
script just checks the JSON is well-formed and tells you exactly where to
click.

Usage:
    python scripts/prepare_elementor_import.py --template elementor/sections/05-courses.json
    python scripts/prepare_elementor_import.py --template elementor/course-page-template.json
"""
import argparse
import json
import sys
from pathlib import Path

REQUIRED_TOP_LEVEL_KEYS = ("title", "type", "version", "content")
VALID_TYPES = ("page", "section")


def collect_element_errors(elements, path, errors, seen_ids):
    for index, element in enumerate(elements):
        here = f"{path}[{index}]"
        if not isinstance(element, dict):
            errors.append(f"{here}: element is not an object")
            continue

        element_id = element.get("id")
        if not isinstance(element_id, str) or not element_id:
            errors.append(f"{here}: missing or empty id")
        elif element_id in seen_ids:
            errors.append(f"{here}: duplicate id '{element_id}'")
        else:
            seen_ids.add(element_id)

        if not element.get("elType"):
            errors.append(f"{here} (id={element_id}): missing elType")

        children = element.get("elements", [])
        if isinstance(children, list):
            collect_element_errors(children, f"{here}.elements", errors, seen_ids)
        else:
            errors.append(f"{here} (id={element_id}): 'elements' must be a list")


def validate(doc):
    errors = []

    for key in REQUIRED_TOP_LEVEL_KEYS:
        if key not in doc:
            errors.append(f"missing required top-level key: '{key}'")

    template_type = doc.get("type")
    if template_type is not None and template_type not in VALID_TYPES:
        errors.append(f"unexpected top-level 'type': '{template_type}' (expected one of {VALID_TYPES})")

    content = doc.get("content")
    if not isinstance(content, list):
        errors.append("top-level 'content' must be a list")
        return errors

    collect_element_errors(content, "content", errors, set())
    return errors


def print_import_steps(path, doc):
    template_type = doc.get("type", "page")
    title = doc.get("title", path.name)
    element_count = len(doc.get("content", []))

    print()
    print("=" * 72)
    print("Manual import steps (do this yourself in wp-admin - nothing here")
    print("touches your site):")
    print("=" * 72)
    print(f"File:     {path}")
    print(f"Title:    {title}")
    print(f"Type:     {template_type}")
    print(f"Elements: {element_count} top-level element(s)")
    print()
    print("1. In wp-admin, go to Templates > Saved Templates.")
    print("2. Click 'Import Templates' (top of the page) and upload this JSON file.")
    print("   It will appear in your Saved Templates / Template Library as")
    print(f"   '{title}'.")
    if template_type == "page":
        print("3. Open the target page with Elementor (or create a new one).")
        print("4. Click the folder icon (Template Library) > My Templates,")
        print("   find the imported template, and click Insert.")
        print("   For a full page, insert it into an otherwise-empty page.")
    else:
        print("3. Open the target page with Elementor at the point you want")
        print("   this section to appear.")
        print("4. Click the folder icon (Template Library) > My Templates,")
        print("   find the imported template, and click Insert at that location.")
    print("5. Review every widget on a staging site before publishing -")
    print("   this file has not been opened in Elementor yet.")
    print("=" * 72)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--template", required=True, type=Path, help="Path to an Elementor template JSON file (full page or one section)")
    args = parser.parse_args()

    if not args.template.exists():
        print(f"ERROR: file not found: {args.template}")
        sys.exit(1)

    try:
        doc = json.loads(args.template.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON in {args.template}: {e}")
        sys.exit(1)

    if not isinstance(doc, dict):
        print(f"ERROR: top level of {args.template} must be a JSON object")
        sys.exit(1)

    errors = validate(doc)
    if errors:
        print(f"INVALID: {args.template}")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    print(f"OK: {args.template}")
    print_import_steps(args.template, doc)
    sys.exit(0)


if __name__ == "__main__":
    main()
