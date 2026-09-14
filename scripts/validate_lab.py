import argparse
import re
from pathlib import Path


SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "AWS key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Windows user path": re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+"),
    "Unix home path": re.compile(r"/home/[^/\s]+/"),
}
SOLUTION_FILENAMES = {"solution.py", "solution.sql", "answers.md", "answer.md", "completed.py"}
CACHE_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


def relative(path, root):
    return str(path.relative_to(root)).replace("\\", "/")


def is_cache_path(path):
    return any(part in CACHE_DIRS for part in path.parts) or path.suffix in {".pyc", ".pyo"}


def has_content_file(path):
    return any(item.is_file() and not is_cache_path(item) for item in path.rglob("*"))


def scan_file(path, lab_dir, errors):
    rel = path.relative_to(lab_dir)
    rel_text = relative(path, lab_dir)
    if is_cache_path(rel):
        errors.append(f"Cache/bytecode file should not be in student lab: {rel_text}")
        return

    in_starter = bool(rel.parts) and rel.parts[0] == "starter"
    if not in_starter and path.name.lower() in SOLUTION_FILENAMES:
        errors.append(f"Possible solution leak: {rel_text}")

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return

    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            errors.append(f"{label} found in {rel_text}")


def check_required_lab_paths(lab_dir, errors):
    readme = lab_dir / "README.md"
    if not readme.is_file() or readme.stat().st_size == 0:
        errors.append("Missing or empty README.md")

    for dirname in ("starter", "datasets", "tests"):
        path = lab_dir / dirname
        if not path.is_dir():
            errors.append(f"Missing directory: {dirname}")
        elif dirname != "datasets" and not has_content_file(path):
            errors.append(f"Directory has no content files: {dirname}")

    tests = lab_dir / "tests"
    if tests.is_dir() and not has_content_file(tests):
        errors.append("No automated tests")


def main():
    parser = argparse.ArgumentParser(description="Validate a DataEngLab student lab directory.")
    parser.add_argument("lab_dir", type=Path)
    args = parser.parse_args()

    lab_dir = args.lab_dir
    errors = []
    if not lab_dir.is_dir():
        print("ERROR: missing lab", lab_dir)
        return 1

    check_required_lab_paths(lab_dir, errors)
    for path in lab_dir.rglob("*"):
        if path.is_file():
            scan_file(path, lab_dir, errors)

    for error in errors:
        print("ERROR:", error)
    if errors:
        return 1
    print("OK:", lab_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
