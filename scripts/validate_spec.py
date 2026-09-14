import argparse
import json
import re
from pathlib import Path


REQUIRED_FIELDS = (
    "title",
    "slug",
    "audience",
    "level",
    "prerequisites",
    "outcomes",
    "technologies",
    "business_scenario",
    "deliverable",
    "validation_criteria",
    "acquired_skills",
    "duration_minutes",
    "curriculum",
)
LIST_FIELDS = (
    "prerequisites",
    "outcomes",
    "technologies",
    "validation_criteria",
    "acquired_skills",
)
LEVELS = {"beginner", "intermediate", "advanced"}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def is_blank(value):
    return value in (None, "", [], {})


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON: {exc}") from exc


def check_required_fields(data, errors):
    for field in REQUIRED_FIELDS:
        if field not in data or is_blank(data[field]):
            errors.append(f"Missing or empty field: {field}")


def check_slug(data, course_dir, errors):
    slug = data.get("slug")
    if not slug:
        return
    if not isinstance(slug, str):
        errors.append("slug must be a string")
        return
    if not SLUG_RE.match(slug):
        errors.append(f'slug "{slug}" must be lowercase kebab-case')
    if slug != course_dir.name:
        errors.append(f'slug "{slug}" does not match directory name "{course_dir.name}"')


def check_level(data, errors):
    level = data.get("level")
    if isinstance(level, str) and level.lower() in LEVELS:
        return
    errors.append(f'level must be one of {", ".join(sorted(LEVELS))}')


def check_list_fields(data, errors):
    for field in LIST_FIELDS:
        value = data.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"{field} must be a non-empty list")
            continue
        for index, item in enumerate(value, start=1):
            if not isinstance(item, str) or not item.strip():
                errors.append(f"{field}[{index}] must be a non-empty string")


def check_duration(data, errors):
    duration = data.get("duration_minutes")
    if not isinstance(duration, dict):
        errors.append("duration_minutes must be an object")
        return

    lecture = duration.get("lecture")
    practical = duration.get("practical")
    if not is_number(lecture) or lecture < 0:
        errors.append("duration_minutes.lecture must be a non-negative number")
        lecture = 0
    if not is_number(practical) or practical < 0:
        errors.append("duration_minutes.practical must be a non-negative number")
        practical = 0

    total = lecture + practical
    if total <= 0:
        errors.append("duration_minutes.lecture + practical must be greater than 0")
    elif practical / total < 0.5:
        percent = round(100 * practical / total)
        errors.append(f"Practical time is only {percent}% of duration_minutes; must be at least 50%")


def check_lesson(topic_index, lesson_index, lesson, errors):
    label = f"curriculum[{topic_index}].lessons[{lesson_index}]"
    if not isinstance(lesson, dict):
        errors.append(f"{label} must be an object")
        return

    for field in ("id", "title", "objective"):
        value = lesson.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{label}.{field} must be a non-empty string")

    lesson_id = lesson.get("id")
    if isinstance(lesson_id, str) and not SLUG_RE.match(lesson_id):
        errors.append(f'{label}.id "{lesson_id}" must be lowercase kebab-case')

    for field in ("minutes_lecture", "minutes_practical"):
        value = lesson.get(field)
        if not is_number(value) or value < 0:
            errors.append(f"{label}.{field} must be a non-negative number")


def check_curriculum(data, errors):
    curriculum = data.get("curriculum")
    if not isinstance(curriculum, list) or not curriculum:
        errors.append("curriculum must be a non-empty list")
        return

    lesson_ids = set()
    for topic_index, topic in enumerate(curriculum, start=1):
        label = f"curriculum[{topic_index}]"
        if not isinstance(topic, dict):
            errors.append(f"{label} must be an object")
            continue

        topic_name = topic.get("topic")
        if not isinstance(topic_name, str) or not topic_name.strip():
            errors.append(f"{label}.topic must be a non-empty string")

        lessons = topic.get("lessons")
        if not isinstance(lessons, list) or not lessons:
            errors.append(f"{label}.lessons must be a non-empty list")
        else:
            for lesson_index, lesson in enumerate(lessons, start=1):
                check_lesson(topic_index, lesson_index, lesson, errors)
                lesson_id = lesson.get("id") if isinstance(lesson, dict) else None
                if lesson_id in lesson_ids:
                    errors.append(f'Duplicate lesson id in curriculum: "{lesson_id}"')
                elif isinstance(lesson_id, str):
                    lesson_ids.add(lesson_id)

        quiz = topic.get("quiz")
        if not isinstance(quiz, str) or not quiz.strip():
            errors.append(f"{label}.quiz must be a non-empty string")
        elif not quiz.endswith(".md"):
            errors.append(f'{label}.quiz "{quiz}" must be a Markdown filename')


def validate_course_spec(course_dir):
    errors = []
    spec_path = course_dir / "course-spec.json"
    if not spec_path.is_file():
        return [f"missing course-spec.json in {course_dir}"]

    try:
        data = load_json(spec_path)
    except ValueError as exc:
        return [f"invalid course-spec.json: {exc}"]

    if not isinstance(data, dict):
        return ["course-spec.json must contain a JSON object"]

    check_required_fields(data, errors)
    check_slug(data, course_dir, errors)
    check_level(data, errors)
    check_list_fields(data, errors)
    check_duration(data, errors)
    check_curriculum(data, errors)
    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate DataEngLab course-spec.json.")
    parser.add_argument("course_dir", type=Path)
    args = parser.parse_args()

    course_dir = args.course_dir.resolve()
    errors = validate_course_spec(course_dir)
    for error in errors:
        print("ERROR:", error)
    if errors:
        return 1
    print("OK:", course_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
