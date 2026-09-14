import argparse
import json
import re
from pathlib import Path


FIELD_RE = re.compile(r"^-\s+([A-Za-z][A-Za-z /]*):\s*(.*)$")
OPTION_RE = re.compile(r"^\s+([A-Za-z])\.\s+(.+)$")
REQUIRED_FIELDS = ("Type", "Difficulty", "Related lesson", "Question", "Options", "Correct answer", "Explanation")
NON_OPTION_FIELDS = ("Type", "Difficulty", "Related lesson", "Question", "Correct answer", "Explanation")
REQUIRED_LESSON_HEADINGS = (
    "Learning objective",
    "Prerequisites",
    "Concept",
    "Architecture or data flow",
    "Practical example",
    "Common mistakes",
    "Mini exercise",
    "Expected result",
    "Summary",
    "Next step",
)


def heading_positions(text):
    return [(match.start(), match.end(), match.group(1).strip()) for match in re.finditer(r"^##[ \t]+(.+)$", text, re.M)]


def sections(text):
    positions = heading_positions(text)
    out = {}
    for index, (start, end, name) in enumerate(positions):
        section_end = positions[index + 1][0] if index + 1 < len(positions) else len(text)
        out[name] = text[end:section_end].strip()
    return out


def read_text(path, errors):
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        errors.append(f"File is not valid UTF-8: {path} ({exc})")
    except OSError as exc:
        errors.append(f"Cannot read {path}: {exc}")
    return ""


def load_spec_lesson_ids(course_dir):
    spec_path = course_dir / "course-spec.json"
    if not spec_path.is_file():
        return set()
    try:
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()

    lesson_ids = set()
    for topic in spec.get("curriculum", []) if isinstance(spec, dict) else []:
        if not isinstance(topic, dict):
            continue
        for lesson in topic.get("lessons", []) or []:
            if isinstance(lesson, dict) and isinstance(lesson.get("id"), str):
                lesson_ids.add(lesson["id"])
    return lesson_ids


def required_lesson_headings():
    return list(REQUIRED_LESSON_HEADINGS)


def check_lesson(path, required, expected_ids, errors):
    text = read_text(path, errors)
    if not text:
        return
    section_map = sections(text)
    for heading in required:
        if heading not in section_map:
            errors.append(f"Missing heading: {heading} in {path}")
        elif not section_map[heading]:
            errors.append(f"Empty section: {heading} in {path}")

    lesson_id = path.stem
    if expected_ids and lesson_id not in expected_ids:
        errors.append(f"Lesson file is not referenced by course-spec.json: {path.name}")


def parse_quiz_question(content):
    fields = {}
    option_letters = []
    current_field = None

    for line in content.splitlines():
        field_match = FIELD_RE.match(line)
        if field_match:
            current_field = field_match.group(1).strip()
            if current_field in fields:
                fields[current_field] += "\n" + field_match.group(2).strip()
            else:
                fields[current_field] = field_match.group(2).strip()
            continue

        option_match = OPTION_RE.match(line)
        if option_match and current_field == "Options":
            option_letters.append(option_match.group(1).upper())

    return fields, option_letters


def check_quiz(path, expected_ids, errors):
    text = read_text(path, errors)
    if not text:
        return

    question_count = 0
    for question_name, content in sections(text).items():
        if not question_name.lower().startswith("question"):
            continue
        question_count += 1
        fields, option_letters = parse_quiz_question(content)
        tag = f"{path} ({question_name})"

        for field in REQUIRED_FIELDS:
            if field not in fields:
                errors.append(f"Missing field: {field} in {tag}")

        for field in NON_OPTION_FIELDS:
            if field in fields and not fields[field]:
                errors.append(f"Empty field: {field} in {tag}")

        duplicates = sorted({letter for letter in option_letters if option_letters.count(letter) > 1})
        if duplicates:
            errors.append(f"Duplicate option letters {','.join(duplicates)} in {tag}")
        if len(set(option_letters)) < 2:
            errors.append(f"Fewer than 2 options in {tag}")

        answer = fields.get("Correct answer", "").strip()
        answer_match = re.match(r"^([A-Za-z])", answer)
        answer_letter = answer_match.group(1).upper() if answer_match else ""
        if answer_letter not in set(option_letters):
            errors.append(f'Correct answer "{answer}" does not match any option in {tag}')

        related_lesson = fields.get("Related lesson", "").strip()
        if expected_ids and related_lesson and related_lesson not in expected_ids:
            errors.append(f'Related lesson "{related_lesson}" is not in course-spec.json in {tag}')

    if question_count == 0:
        errors.append(f"No quiz questions found in {path}")


def main():
    parser = argparse.ArgumentParser(description="Validate DataEngLab lesson and quiz Markdown content.")
    parser.add_argument("course_dir", type=Path)
    args = parser.parse_args()

    course_dir = args.course_dir
    errors = []
    required = required_lesson_headings()
    expected_ids = load_spec_lesson_ids(course_dir)

    lessons = course_dir / "tutor-lms" / "lessons"
    if lessons.is_dir():
        lesson_files = sorted(lessons.glob("*.md"))
        if not lesson_files:
            errors.append("No lesson Markdown files found in tutor-lms/lessons")
        for path in lesson_files:
            check_lesson(path, required, expected_ids, errors)
    else:
        errors.append("Missing directory: tutor-lms/lessons")

    quizzes = course_dir / "tutor-lms" / "quizzes"
    if quizzes.is_dir():
        quiz_files = sorted(quizzes.glob("*.md"))
        if not quiz_files:
            errors.append("No quiz Markdown files found in tutor-lms/quizzes")
        for path in quiz_files:
            check_quiz(path, expected_ids, errors)
    else:
        errors.append("Missing directory: tutor-lms/quizzes")

    for error in errors:
        print("ERROR:", error)
    if errors:
        return 1
    print("OK:", course_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
