import argparse
import json
import re
from pathlib import Path


BANNED_WIDGET_TYPES = {"html", "shortcode", "sc_shortcode"}
BANNED_MARKUP_RE = re.compile(r"<\s*(style|script)\b", re.IGNORECASE)


def collect_widget_types(document):
    """Recursively collect every widgetType value used in a parsed Elementor document."""
    found = set()

    def walk_any(node):
        if isinstance(node, dict):
            if node.get("elType") == "widget" and isinstance(node.get("widgetType"), str):
                found.add(node["widgetType"])
            for child in node.values():
                walk_any(child)
        elif isinstance(node, list):
            for child in node:
                walk_any(child)

    walk_any(document)
    return found


def load_corpus_allowlist():
    """Build the set of widget types traceable to an approved reference: a real
    elementor-reference.json at the repo root if present, unioned with the
    checked-in elementor/ tier-2 corpus. Returns None if neither is found/valid,
    meaning there is nothing to trace against (the caller should skip this check
    rather than block on it)."""
    # Anchor on the script's own location rather than the target file's depth,
    # since that's constant regardless of where the file being validated lives.
    repo_root = Path(__file__).resolve().parent.parent

    allowlist = set()
    found_any_source = False

    tier1 = repo_root / "elementor-reference.json"
    if tier1.is_file():
        try:
            allowlist |= collect_widget_types(json.loads(tier1.read_text(encoding="utf-8")))
            found_any_source = True
        except (json.JSONDecodeError, OSError):
            pass

    elementor_dir = repo_root / "elementor"
    corpus_files = []
    for name in ("course-page-template.json", "learning-path-template.json"):
        candidate = elementor_dir / name
        if candidate.is_file():
            corpus_files.append(candidate)
    sections_dir = elementor_dir / "sections"
    if sections_dir.is_dir():
        corpus_files.extend(sorted(sections_dir.glob("*.json")))

    for corpus_file in corpus_files:
        try:
            allowlist |= collect_widget_types(json.loads(corpus_file.read_text(encoding="utf-8")))
            found_any_source = True
        except (json.JSONDecodeError, OSError):
            continue

    return allowlist if found_any_source else None


def scan_settings_strings(value, element_id, errors):
    """Reject custom CSS/JS smuggled into otherwise-native widget settings."""
    if isinstance(value, str):
        if BANNED_MARKUP_RE.search(value):
            errors.append(
                f"Banned <style>/<script> markup inside settings for {element_id} "
                "(CLAUDE.md: no custom Elementor CSS/JS)"
            )
    elif isinstance(value, dict):
        for child in value.values():
            scan_settings_strings(child, element_id, errors)
    elif isinstance(value, list):
        for child in value:
            scan_settings_strings(child, element_id, errors)


def walk(elements, ids, errors, corpus_allowlist, path="content"):
    for index, element in enumerate(elements):
        current_path = f"{path}[{index}]"
        if not isinstance(element, dict):
            errors.append(f"{current_path}: element is not an object")
            continue

        element_id = element.get("id")
        if not isinstance(element_id, str) or not element_id:
            errors.append(f"{current_path}: missing id")
        else:
            ids.append(element_id)

        el_type = element.get("elType")
        if not el_type:
            errors.append(f"{current_path} ({element_id}): missing elType")

        widget_type = element.get("widgetType")
        if el_type == "widget" and isinstance(widget_type, str):
            if widget_type.lower() in BANNED_WIDGET_TYPES:
                errors.append(
                    f'Banned widgetType "{widget_type}" for {element_id} '
                    "(CLAUDE.md: no Elementor HTML/shortcode widgets)"
                )
            elif corpus_allowlist is not None and widget_type not in corpus_allowlist:
                errors.append(
                    f'Untraceable widgetType "{widget_type}" for {element_id} '
                    "(not found in elementor-reference.json or the checked-in elementor/ "
                    "corpus - every widget type must be traceable to the approved reference, "
                    "not just avoid the explicit html/shortcode ban; this is how a third-party "
                    "plugin widget like eael-code-snippet slipped through undetected before)"
                )

        scan_settings_strings(element.get("settings", {}), element_id, errors)

        children = element.get("elements", [])
        if isinstance(children, list):
            walk(children, ids, errors, corpus_allowlist, f"{current_path}.elements")
        else:
            errors.append(f"{current_path} ({element_id}): elements must be a list")


def validate_document(document, corpus_allowlist=None):
    errors = []
    if not isinstance(document, dict):
        return ["top level must be a JSON object"]

    content = document.get("content")
    if not isinstance(content, list):
        return ["content must be list"]

    ids = []
    walk(content, ids, errors, corpus_allowlist)

    seen = set()
    duplicates = sorted({item for item in ids if item in seen or seen.add(item)})
    if duplicates:
        errors.append("Duplicate IDs: " + ",".join(duplicates))
    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate native Elementor JSON structure and banned widgets.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    try:
        document = json.loads(args.path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("ERROR: file not found:", args.path)
        return 1
    except json.JSONDecodeError as exc:
        print("ERROR:", exc)
        return 1

    corpus_allowlist = load_corpus_allowlist()
    errors = validate_document(document, corpus_allowlist)
    for error in errors:
        print("ERROR:", error)
    if errors:
        return 1
    print("OK:", args.path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
