import argparse
import json
from pathlib import Path


REQUIRED_FILES = (
    "course-spec.json",
    "validate.json",
    "tutor-lms/course-overview.md",
    "tutor-lms/curriculum.md",
    "student-lab/README.md",
    "instructor/instructor-guide.md",
    "instructor/troubleshooting.md",
)
REQUIRED_DIRS = (
    "tutor-lms/lessons",
    "tutor-lms/quizzes",
    "student-lab/starter",
    "student-lab/datasets",
    "student-lab/tests",
    "instructor/solution",
)
NON_EMPTY_DIRS = (
    "tutor-lms/lessons",
    "tutor-lms/quizzes",
    "student-lab/starter",
    "student-lab/datasets",
    "student-lab/tests",
)


def read_json(path, errors, label):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"Missing: {path.relative_to(path.parents[1])}")
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid {label}: {exc}")
    return None


def relative(path, root):
    return str(path.relative_to(root)).replace("\\", "/")


def has_non_cache_file(path):
    for item in path.rglob("*"):
        if not item.is_file():
            continue
        if item.suffix == ".pyc" or "__pycache__" in item.parts or ".pytest_cache" in item.parts:
            continue
        return True
    return False


def check_required_paths(course_dir, errors):
    for item in REQUIRED_FILES:
        path = course_dir / item
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"Missing or empty: {item}")

    for item in REQUIRED_DIRS:
        path = course_dir / item
        if not path.is_dir():
            errors.append(f"Missing directory: {item}")

    for item in NON_EMPTY_DIRS:
        path = course_dir / item
        if path.is_dir() and not has_non_cache_file(path):
            errors.append(f"Directory has no content files: {item}")


def check_manifest(course_dir, errors):
    manifest_path = course_dir / "validate.json"
    if not manifest_path.is_file():
        return

    manifest = read_json(manifest_path, errors, "validate.json")
    if not isinstance(manifest, dict):
        errors.append("validate.json must contain a JSON object")
        return

    setup = manifest.get("setup", [])
    validate = manifest.get("validate")
    check_command_list(setup, "validate.json.setup", errors, required=False)
    check_command_list(validate, "validate.json.validate", errors, required=True)


def check_command_list(value, label, errors, required):
    if value in (None, []):
        if required:
            errors.append(f"{label} must contain at least one command")
        return

    if not isinstance(value, list):
        errors.append(f"{label} must be a list of argv lists")
        return

    for index, command in enumerate(value, start=1):
        command_label = f"{label}[{index}]"
        if not isinstance(command, list) or not command:
            errors.append(f"{command_label} must be a non-empty argv list")
            continue
        for arg_index, arg in enumerate(command, start=1):
            if not isinstance(arg, str) or not arg:
                errors.append(f"{command_label}[{arg_index}] must be a non-empty string")


def check_spec_links(course_dir, errors):
    spec_path = course_dir / "course-spec.json"
    if not spec_path.is_file():
        return

    spec = read_json(spec_path, errors, "course-spec.json")
    if not isinstance(spec, dict):
        return

    for topic_index, topic in enumerate(spec.get("curriculum", []) or [], start=1):
        if not isinstance(topic, dict):
            continue

        for lesson in topic.get("lessons", []) or []:
            if not isinstance(lesson, dict):
                continue
            lesson_id = lesson.get("id")
            if isinstance(lesson_id, str) and lesson_id:
                lesson_path = course_dir / "tutor-lms" / "lessons" / f"{lesson_id}.md"
                if not lesson_path.is_file():
                    errors.append(f"Spec lesson missing from tutor-lms/lessons: {lesson_id}.md")

        quiz = topic.get("quiz")
        if isinstance(quiz, str) and quiz:
            quiz_path = course_dir / "tutor-lms" / "quizzes" / quiz
            if not quiz_path.is_file():
                errors.append(f"Spec quiz missing from tutor-lms/quizzes: {quiz}")
        elif quiz is not None:
            errors.append(f"curriculum[{topic_index}].quiz must be a Markdown filename")


def check_solution_overlay(course_dir, errors):
    solution_dir = course_dir / "instructor" / "solution"
    starter_dir = course_dir / "student-lab" / "starter"
    if not solution_dir.is_dir() or not starter_dir.is_dir():
        return

    solution_files = [
        path
        for path in solution_dir.rglob("*")
        if path.is_file() and path.suffix != ".pyc" and "__pycache__" not in path.parts
    ]
    if not solution_files:
        errors.append("instructor/solution has no solution files")
        return

    for path in solution_files:
        rel = path.relative_to(solution_dir)
        if not (starter_dir / rel).is_file():
            errors.append(f"instructor/solution file has no matching starter file: {rel}")


def check_elementor_choice(course_dir, errors):
    elementor_dir = course_dir / "elementor"
    if not elementor_dir.exists():
        errors.append("Missing directory: elementor")
        return
    if not elementor_dir.is_dir():
        errors.append("elementor exists but is not a directory")
        return

    landing = elementor_dir / "landing-page.json"
    fallback = elementor_dir / "REFERENCE_REQUIRED.md"
    has_landing = landing.is_file()
    has_fallback = fallback.is_file()

    if has_landing and has_fallback:
        errors.append("elementor contains both landing-page.json and REFERENCE_REQUIRED.md; choose one outcome")
    elif not has_landing and not has_fallback:
        errors.append("elementor must contain landing-page.json or REFERENCE_REQUIRED.md")

    source = elementor_dir / "SOURCE.md"
    if has_landing and source.is_file() and source.stat().st_size == 0:
        errors.append("elementor/SOURCE.md is empty")


def check_readme_manifest_sync(course_dir, errors):
    manifest_path = course_dir / "validate.json"
    readme_path = course_dir / "student-lab" / "README.md"
    if not manifest_path.is_file() or not readme_path.is_file():
        return

    manifest = read_json(manifest_path, errors, "validate.json")
    if not isinstance(manifest, dict):
        return

    try:
        readme = readme_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"student-lab/README.md is not valid UTF-8: {exc}")
        return

    for section in ("setup", "validate"):
        for command in manifest.get(section, []) or []:
            if not isinstance(command, list) or not all(isinstance(arg, str) for arg in command):
                continue
            command_text = " ".join(command)
            if command_text not in readme:
                errors.append(f"validate.json {section} command not documented exactly in student-lab/README.md: {command_text}")


def main():
    parser = argparse.ArgumentParser(description="Validate the DataEngLab course output structure.")
    parser.add_argument("course_dir", type=Path)
    args = parser.parse_args()

    course_dir = args.course_dir.resolve()
    errors = []
    if not course_dir.is_dir():
        print("ERROR: missing course directory", course_dir)
        return 1

    check_required_paths(course_dir, errors)
    check_manifest(course_dir, errors)
    check_spec_links(course_dir, errors)
    check_solution_overlay(course_dir, errors)
    check_elementor_choice(course_dir, errors)
    check_readme_manifest_sync(course_dir, errors)

    for error in errors:
        print("ERROR:", error)
    if errors:
        return 1
    print("OK:", course_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
