import argparse
import zipfile
from pathlib import Path


EXCLUDED_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "output"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def should_include(relative_path):
    if any(part in EXCLUDED_DIRS for part in relative_path.parts):
        return False
    if relative_path.suffix in EXCLUDED_SUFFIXES:
        return False
    return True


def add_file(archive, source, archive_path):
    info = zipfile.ZipInfo(str(archive_path).replace("\\", "/"))
    # Fixed timestamp keeps repeated packages deterministic.
    info.date_time = (2024, 1, 1, 0, 0, 0)
    info.compress_type = zipfile.ZIP_DEFLATED
    archive.writestr(info, source.read_bytes())


def main():
    parser = argparse.ArgumentParser(description="Package only the student-lab directory for a DataEngLab course/lab.")
    parser.add_argument("course_dir", type=Path)
    args = parser.parse_args()

    course_dir = args.course_dir.resolve()
    student_lab = course_dir / "student-lab"
    if not student_lab.is_dir():
        print("ERROR: missing student-lab")
        return 1

    output_dir = course_dir / "packages"
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / f"{course_dir.name}-student-lab.zip"
    root_name = f"{course_dir.name}-student-lab"

    files = [
        path
        for path in sorted(student_lab.rglob("*"))
        if path.is_file() and should_include(path.relative_to(student_lab))
    ]
    if not files:
        print("ERROR: student-lab has no packageable files")
        return 1

    with zipfile.ZipFile(archive_path, "w") as archive:
        for source in files:
            add_file(archive, source, Path(root_name) / source.relative_to(student_lab))

    print("OK:", archive_path)
    print("Files:", len(files))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
