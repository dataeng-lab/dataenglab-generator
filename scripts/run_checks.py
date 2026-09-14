import argparse
import subprocess
import sys
from pathlib import Path


def format_command(argv):
    return " ".join(str(item) for item in argv)


def run(argv):
    print("\n$", format_command(argv), flush=True)
    result = subprocess.run(argv, check=False)
    status = "PASS" if result.returncode == 0 else f"FAIL ({result.returncode})"
    print(status + ":", format_command(argv), flush=True)
    return result.returncode == 0


def detect_mode(output_dir):
    has_course_spec = (output_dir / "course-spec.json").is_file()
    has_lab_spec = (output_dir / "lab-spec.md").is_file()

    if has_course_spec and has_lab_spec:
        return "course"
    if has_course_spec:
        return "course"
    if has_lab_spec:
        return "lab"
    return None


def course_commands(course_dir, scripts_dir):
    py = sys.executable
    commands = [
        [py, str(scripts_dir / "validate_spec.py"), str(course_dir)],
        [py, str(scripts_dir / "validate_course.py"), str(course_dir)],
        [py, str(scripts_dir / "validate_content.py"), str(course_dir)],
        [py, str(scripts_dir / "validate_lab.py"), str(course_dir / "student-lab")],
        [py, str(scripts_dir / "validate_lab_execution.py"), str(course_dir)],
    ]

    landing_page = course_dir / "elementor" / "landing-page.json"
    if landing_page.is_file():
        commands.append([py, str(scripts_dir / "validate_elementor_json.py"), str(landing_page)])

    return commands


def lab_commands(lab_output_dir, scripts_dir):
    py = sys.executable
    return [[py, str(scripts_dir / "run_lab_checks.py"), str(lab_output_dir)]]


def main():
    parser = argparse.ArgumentParser(
        description="Run DataEngLab validation checks for a full course or standalone lab output."
    )
    parser.add_argument("output_dir", type=Path)
    parser.add_argument(
        "--mode",
        choices=("auto", "course", "lab"),
        default="auto",
        help="Validation mode. Defaults to auto-detecting course-spec.json or lab-spec.md.",
    )
    args = parser.parse_args()

    output_dir = args.output_dir
    scripts_dir = Path(__file__).resolve().parent

    if not output_dir.is_dir():
        print("ERROR: missing output directory", output_dir)
        return 1

    mode = detect_mode(output_dir) if args.mode == "auto" else args.mode
    if mode is None:
        print("ERROR: cannot determine output type for", output_dir)
        print("Expected course-spec.json for a full course or lab-spec.md for a standalone lab.")
        return 1

    print("Detected validation mode:", mode, flush=True)
    commands = course_commands(output_dir, scripts_dir) if mode == "course" else lab_commands(output_dir, scripts_dir)

    ok = True
    for command in commands:
        ok = run(command) and ok

    print("ALL CHECKS PASSED" if ok else "CHECKS FAILED", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
